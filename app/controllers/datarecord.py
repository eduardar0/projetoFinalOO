import uuid
import sqlite3
from app.models.user_account import UserAccount

class DataRecord:
    """Classe responsável por gerenciar a autenticação e os dados de usuários."""

    def __init__(self, db_name='app/controllers/db/user_accounts.db'):
        """Inicializa a conexão com o banco de dados SQLite e cria a tabela de usuários se ela não existir."""
        self.db_name = db_name
        self.__authenticated_users = {}  # Dicionário de usuários autenticados {session_id: user}
        self.create_table()

    def create_table(self):
        """Cria a tabela de usuários no banco de dados se ela não existir."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    def book(self, username, password):
        """Registra um novo usuário no banco de dados SQLite."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
            except sqlite3.IntegrityError:
                print(f"Erro: O usuário {username} já está registrado.")

    def checkUser(self, username, password):
        """Verifica se o usuário está no banco de dados e gera um ID único para a sessão."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user_data = cursor.fetchone()

            if user_data:  # Se o usuário estiver no banco de dados, cria um ID de sessão
                session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                user = UserAccount(username, password)
                self.__authenticated_users[session_id] = user
                return session_id  # Retorna o ID de sessão para o usuário
            return None

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

    def logout(self, session_id):
        """Remove o usuário autenticado do dicionário, efetivamente realizando o logout."""
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]
