from bottle import template, redirect, request, response
import sqlite3
from app.controllers.datarecord import DataRecord

class Application:
    def __init__(self):
        self.pages = {
            'pagina': self.pagina,
            'portal': self.portal,
            'register': self.register_page
        }
        self.__model = DataRecord()
        self.__current_username = None

    def render(self, page, parameter=None, **kwargs):
        """
        Renderiza a página solicitada. Se um parâmetro ou variáveis extras (kwargs) forem fornecidos,
        eles são passados para a função de renderização da página.
        """
        content = self.pages.get(page, self.helper)
        if parameter is None:
            return content(**kwargs)
        else:
            return content(parameter, **kwargs)

    def helper(self):
        return template('app/views/html/helper')

    def get_session_id(self):
        session_id = request.get_cookie('session_id')
        if not session_id:
            print("No session ID found in cookie.")
        return session_id

    def login(self):
        username = request.forms.get('username')
        password = request.forms.get('password')
        session_id = self.__model.checkUser(username, password)
        if session_id:
            # Definir o cookie de sessão
            response.set_cookie('session_id', session_id)
            return "Login successful"
        else:
            return "Invalid credentials"
        
    def portal(self):
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            session_id, username = self.authenticate_user(username, password)
            if session_id:
                response.set_cookie('session_id', session_id, path='/')
                return redirect('/pagina')
            else:
                return template('app/views/html/portal', error="Login inválido.")
        return template('app/views/html/portal')

    def pagina(self, username=None):
        # Renderiza a página principal, verificando a autenticação
        if self.is_authenticated(username):
            session_id = self.get_session_id()
            user = self.__model.getCurrentUser(session_id)
            return template('app/views/html/pagina', current_user=user)
        else:
            return template('app/views/html/pagina', current_user=None)



    def is_authenticated(self, username):
        # Verifica se o nome de usuário está autenticado comparando com o nome associado ao ID da sessão.
        session_id = self.get_session_id()
        if not session_id:
            print("No session ID available.")
            return False

        current_username = self.__model.getUserName(session_id)
        if current_username is None:
            print(f"User not found for session ID: {session_id}")
            return False

        print(f"Comparing username: {username} with current_username: {current_username}")
        return username == current_username

    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.logout_user()
            self.__current_username = self.__model.getUserName(session_id)
            return session_id, username
        return None, None

    def logout_user(self):
        self.__current_username = None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)

    def register_page(self, error=None):
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            confirm_password = request.forms.get('confirm_password')
            #codigo para formulario

            if password != confirm_password:
                return template('app/views/html/register', error="Senhas não coincidem.")
            #para testar a senha
        

            try:
                self.__model.book(username, password)
                session_id = self.__model.checkUser(username, password)
                if session_id:
                    response.set_cookie('session_id', session_id, path='/')
                    return redirect('/pagina')
                
                
                else:
                    return template('app/views/html/register', error="Erro ao autenticar após o registro.")
            except sqlite3.IntegrityError:
                return template('app/views/html/register', error="O nome de usuário já existe. Tente outro.")
        return template('app/views/html/register', error=error)
