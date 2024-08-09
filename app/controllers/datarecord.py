from app.models.user_account import UserAccount
import json
import uuid

class DataRecord:
    """Classe responsável por gerenciar a autenticação e os dados de usuários."""

    def __init__(self):
        """Inicializa o banco de dados, carregando usuários e autenticações atuais."""
        self.__user_accounts = []  # Lista de contas de usuários
        self.__authenticated_users = {}  # Dicionário de usuários autenticados {session_id: user}
        self.read()

    def read(self):
        """Lê os dados do arquivo JSON e carrega as contas de usuários."""
        try:
            with open("app/controllers/db/user_accounts.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('Guest', '010101', '101010'))

    def book(self, username, password):
        """Registra um novo usuário e salva no arquivo JSON."""
        new_user = UserAccount(username, password)
        self.__user_accounts.append(new_user)
        with open("app/controllers/db/user_accounts.json", "w") as arquivo_json:
            user_data = [vars(user_account) for user_account in self.__user_accounts]
            json.dump(user_data, arquivo_json)

    def getCurrentUser(self, session_id):
        """Retorna o usuário autenticado com base no ID da sessão."""
        return self.__authenticated_users.get(session_id)

    def getUserName(self, session_id):
        """Retorna o nome do usuário autenticado com base no ID da sessão."""
        user = self.getCurrentUser(session_id)
        return user.username if user else None

    def getUserSessionId(self, username):
        """Retorna o ID de sessão associado a um nome de usuário."""
        for session_id, user in self.__authenticated_users.items():
            if username == user.username:
                return session_id
        return None  # Retorna None se o usuário não for encontrado

    def checkUser(self, username, password):
        """Verifica as credenciais do usuário e retorna um ID de sessão único se a autenticação for bem-sucedida."""
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                self.__authenticated_users[session_id] = user
                return session_id  # Retorna o ID de sessão para o usuário
        return None

    def logout(self, session_id):
        """Remove o usuário autenticado do dicionário, efetivamente realizando o logout."""
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]
