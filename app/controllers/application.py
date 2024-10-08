from bottle import template, redirect, request, response
import sqlite3
from app.controllers.datarecord import DataRecord

class Application:
    def __init__(self):
        self.pages = {
            'pagina': self.pagina,
            'portal': self.portal,
            'register': self.register_page,
            'dados': self.dados,
            'delete_account_confirm': self.delete_account_confirm, 
            'home': self.home,
            'edit_password': self.edit_password
        }
        self.model = DataRecord()
        self.__current_username = None

    def render(self, page, parameter=None, **kwargs):
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
    
    def get_username_by_session(self, session_id):
        # Supondo que o método getUserBySessionId existe no DataRecord para buscar o nome pelo session_id
        return self.model.get_username(session_id)
    

    def home(self):
        return template('app/views/html/home')

    def login(self):
        username = request.forms.get('username')
        password = request.forms.get('password')
        session_id = self.model.checkUser(username, password)
        if session_id:
            # Definir o cookie de sessão com o ID da sessão
            response.set_cookie('session_id', session_id, path='/')
            return "Login successful"
        else:
            return "Invalid credentials"
        

    def dados(self, username=None):
        session_id = self.get_session_id()
        if session_id:
            user = self.model.getCurrentUser(session_id)
            if user:
                username = username
                password = self.model.getUserPassword(username)
                return template('app/views/html/dados', current_user=user, username=username, password=password)
        return template('app/views/html/pagina', current_user=None, username=None, password=password)
     
    def delete_account_confirm(self):
        session_id = request.get_cookie('session_id')  # Obtém o ID da sessão do cookie
        if session_id:
            self.model.delete_account(session_id)
            return template('app/views/html/portal')  # Redireciona para a página de logout ou qualquer outra página desejada
        else:
            return "Você não está logado."

    def edit_password(self):
        session_id = self.get_session_id()
        if session_id:
           if request.method == 'POST':
              old_password = request.forms.get('old_password')
              new_password = request.forms.get('new_password')
              confirm_new_password = request.forms.get('confirm_new_password')

              if new_password != confirm_new_password:
                  return template('app/views/html/edit_password', error="As novas senhas não coincidem.")
              if self.model.update_password(session_id, old_password=old_password, new_password=new_password):
                  return redirect('/portal')
           else:
               return template('app/views/html/edit_password', error="Senha antiga incorreta ou erro ao atualizar a senha")
        return template('app/views/html/edit_password')


    
    def portal(self):
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            session_id, username = self.authenticate_user(username, password)
            if session_id:
                response.set_cookie('session_id', session_id, path='/')
                return template('html/pagina.tpl', current_user=username)
            else:
                return template('html/portal', error="Login inválido.")
        return template('html/portal')

    def pagina(self, user_name=None, tasks= None):
        if self.is_authenticated(user_name):
            session_id = self.get_session_id()
            user = self.model.getCurrentUser(session_id)
            tasks = self.model.get_tasks(session_id)
            return template('html/pagina', current_user=user, user_name=user_name, tasks=tasks)
        else:
            return template('html/pagina', current_user=user, user_name=user_name, tasks=tasks)
        


    def is_authenticated(self, username):
        session_id = self.get_session_id()
        if not session_id:
            print("No session ID available.")
            return False

        current_username = self.model.getUserName(session_id)
        if current_username is None:
            print(f"User not found for session ID: {session_id}")
            return False

        print(f"Comparing username: {username} with current_username: {current_username}")
        return username == current_username

    def authenticate_user(self, username, password):
        session_id = self.model.checkUser(username, password)
        if session_id:
            self.__current_username = self.model.get_username(session_id)  # Usa o novo método
            return session_id, self.__current_username
        else:
            return None, None

    def logout_user(self):
        self.__current_username = None
        session_id = self.get_session_id()
        if session_id:
            self.model.logout(session_id)

    def register_page(self, error=None):
        if request.method == 'POST':
            username = request.forms.get('username')
            password = request.forms.get('password')
            confirm_password = request.forms.get('confirm_password')

            if password != confirm_password:
                return template('app/views/html/register', error="Senhas não coincidem.")

            try:
                self.model.book(self.get_session_id(), username, password)
                session_id = self.model.checkUser(username, password)
                if session_id:
                    response.set_cookie('session_id', session_id, path='/')
                    return redirect('/pagina')
                else:
                    return template('app/views/html/register', error="Erro ao autenticar após o registro.")
            except sqlite3.IntegrityError:
                return template('app/views/html/register', error="O nome de usuário já existe. Tente outro.")
        return template('app/views/html/register', error=error)
    
    def get_tasks(self, session_id):
        """Chama o método get_tasks_ do DataRecord."""
        taskses= self.model.get_tasks(session_id)
        for task in taskses:
            return task