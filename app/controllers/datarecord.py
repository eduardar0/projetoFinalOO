import os
import sqlite3
import uuid
from app.models.user_account import UserAccount

class DataRecord:
    """Classe responsável por gerenciar a autenticação e os dados de usuários."""

    def __init__(self, db_name='/mnt/c/Users/Joelma/Documents/bonusPF/bmvc/app/controllers/db/user_accounts.db'):
        """Inicializa a conexão com o banco de dados SQLite e cria a tabela de usuários se ela não existir."""
        # Gera o caminho absoluto para o banco de dados
        self.db_name = os.path.abspath(db_name)
        self.__authenticated_users = {}  # Dicionário de usuários autenticados {session_id: user}
        print(f"Caminho absoluto do banco de dados: {self.db_name}")
        self.create_table()

    def create_table(self):
        """Cria a tabela de usuários no banco de dados se ela não existir."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        is_admin INTEGER DEFAULT 0
                    )
                ''')
                conn.commit()
        except sqlite3.OperationalError as e:
            print(f"Erro ao abrir o banco de dados: {e}")

    # Outros métodos...

    def book(self, session_id, username, password, is_admin=False):
        """Cria um novo usuário com base no nível de permissão (comum ou administrador)."""
    # Crud (create)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            try:
            # Converter a permissão em 1 para superusuário e 0 para usuário comum
                admin_flag = 1 if is_admin else 0
                cursor.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
                        (username, password, admin_flag))
                conn.commit()
                print(f"Usuário {username} criado com sucesso.")
            except sqlite3.IntegrityError:
                print(f"Erro: O usuário {username} já está registrado.")
                raise

    def get_all_users(self, session_id):
        """Retorna todos os usuários do banco de dados, apenas para administradores."""
        if not self.is_admin(session_id):
            print("Acesso negado: apenas administradores podem visualizar todos os usuários.")
            return []
        #### cRud (READ)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
        
    def get_username(self, session_id):
        """Retorna o nome de usuário associado ao session_id."""
        user = self.__authenticated_users.get(session_id)  # Obtém o objeto UserAccount pela session_id
        if user:
            return user.username  # Retorna o nome de usuário
        return None  # Se a sessão não for encontrada, retorna None

    def update_user(self, session_id, user_id, new_username=None, new_password=None):
        """Atualiza o username e/ou password de um usuário específico, apenas para administradores."""
        if not self.is_admin(session_id):
            print("Acesso negado: apenas administradores podem atualizar usuários.")
            return
        ### Atualização de Usuários crUd (Update)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if new_username:
                cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
            if new_password:
                cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
            conn.commit()
            print(f"Usuário {user_id} atualizado com sucesso.")

    def delete_user(self, session_id, user_id):
        """Remove um usuário do banco de dados, apenas para administradores."""
        if not self.is_admin(session_id):
            print("Acesso negado: apenas administradores podem remover usuários.")
            return
        ### cruD (delete)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            print(f"Usuário {user_id} removido com sucesso.")

    def checkUser(self, username, password):
        """Verifica se o usuário está no banco de dados e gera um ID único para a sessão."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user_data = cursor.fetchone()

            if user_data:  # Se o usuário estiver no banco de dados
                session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                user = UserAccount(username, password, is_admin=user_data[3])  # Inclui o campo is_admin
                self.__authenticated_users[session_id] = user
                return session_id  # Retorna o ID de sessão para o usuário
            return None

    def is_admin(self, session_id):
        """Verifica se o usuário autenticado é um administrador."""
        user = self.getCurrentUser(session_id)
        if user:
            return user.is_admin  # Retorna True se o usuário for administrador
        return False

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



#sqlite3 /mnt/c/Users/Joelma/Documents/bonusPF/bmvc/app/controllers/db/user_accounts.db