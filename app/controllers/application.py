from bottle import template, redirect, request
from app.controllers.datarecord import DataRecord

class Application():
    def __init__(self):
        self.pages = {
            # Dicionário feito para armazenar páginas criadas
            'pagina': self.pagina,
            'portal': self.portal
        }
        self.__model = DataRecord()
        # Instância da classe DataRecord, que lida com a manipulação de dados

        self.__current_username = None
        # Armazena o nome do usuário atualmente autenticado
        # Por enquanto é None, pois nenhum usuário está autenticado

    def render(self, page, parameter=None):
        """Renderiza a página solicitada. Se um parâmetro for fornecido, ele é passado para a função de renderização da página."""
        content = self.pages.get(page, self.helper)
        if parameter is None:
            return content()  # Chama a função sem parâmetros
        else:
            return content(parameter)  # Chama a função com o parâmetro

    def helper(self):
        return template('app/views/html/helper')
        # Manda para a página de ajuda, retorna o template app/views/html/helper

    def get_session_id(self):
        # Obtém o ID da sessão do cookie armazenado no navegador
        return request.get_cookie('session_id')

    def portal(self):
        # Renderiza a página de login
        return template('app/views/html/portal')

    def pagina(self, username=None):
        # Renderiza a página principal. 
        # Verifica se o usuário está autenticado antes de exibir o conteúdo.
        if self.is_authenticated(username):
            session_id = self.get_session_id()
            user = self.__model.getCurrentUser(session_id)
            return template('app/views/html/pagina', current_user=user)
        else:
            return template('app/views/html/pagina', current_user=None)

    def is_authenticated(self, username):
        # Verifica se o nome de usuário está autenticado
        # Compara o nome associado ao ID da sessão.
        session_id = self.get_session_id()
        current_username = self.__model.getUserName(session_id)
        return username == current_username

    def authenticate_user(self, username, password):
        # Autentica o usuário, verificando as credenciais e gerando um ID de sessão único.
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.logout_user()  # Realiza logout de qualquer usuário previamente autenticado
            self.__current_username = self.__model.getUserName(session_id)
            return session_id, username
        return None, None

    def logout_user(self):
        # Realiza o logout do usuário atual, removendo o ID de sessão.
        # Remove o ID da sessão e limpa o nome de usuário atual.
        self.__current_username = None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)
            # Se houver um ID de sessão ativo, chama o método logout do modelo para finalizar a sessão.
            
