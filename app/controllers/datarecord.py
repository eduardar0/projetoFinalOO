import os
import sqlite3
import uuid
from app.models.user_account import UserAccount

class DataRecord:
    """Classe responsável por gerenciar a autenticação e os dados de usuários."""

    def __init__(self, db_name='app/controllers/db/user_accounts.db'):
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
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    description TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
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

    def get_all_users(self, session_id, admin_only):
        """Retorna todos os usuários do banco de dados, apenas para administradores."""
        if admin_only:
            if session_id is None or not self.is_admin(session_id):
              print("Acesso negado: apenas administradores podem visualizar todos os usuários.")
              return []
        #### cRud (READ)
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            if admin_only:
               cursor.execute("SELECT * FROM users")
            else:
                cursor.execute("SELECT username, password FROM users")
            return cursor.fetchall()
        
    def get_username(self, session_id): ########
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

    def delete_account(self, session_id ):
        """Remove a conta do usuário logado"""
        user = self.getCurrentUser(session_id)
        if user:
            username = user.username
            with sqlite3.connect(self.db_name) as conn:
               cursor = conn.cursor()
               cursor.execute("DELETE FROM users WHERE username = ?", (username,))
               conn.commit()
               print(f"Usuário {username} excluído com sucesso!")

               if session_id in self.__authenticated_users:
                    del self.__authenticated_users[session_id]
                    print(f"Session ID '{session_id}' removido da lista de usuários autenticados")
        else:
            print("Nenhum usuário logado para exclusão")
    



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

    def getUserPassword(self, username):
        """Retorna a senha do usuário com base no nome de usuário."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            password = cursor.fetchone()
            return password[0] if password else None
        
   



#sqlite3 /mnt/c/Users/Joelma/Documents/bonusPF/bmvc/app/controllers/db/user_accounts.db

####funções para as tarefas

    # def get_user_id(self, username):
    # #"""Obtém o ID do usuário com base no nome de usuário."""
    #     with sqlite3.connect(self.db_name) as conn:  # Abre uma conexão com o banco de dados SQLite.
    #         cursor = conn.cursor()  # Cria um cursor para executar comandos SQL.
    #         cursor.execute("SELECT id FROM users WHERE username = ?", (username,))  # Busca o ID do usuário pelo nome de usuário.
    #         user_data = cursor.fetchone()  # Obtém a primeira linha do resultado.
    #         return user_data[0] if user_data else None  # Retorna o ID do usuário ou None se o usuário não existir.



    def add_task(self, session_id, description):
        """Adiciona uma nova tarefa para o usuário autenticado."""
        user = self.getCurrentUser(session_id)  # Obtém o usuário autenticado com base no ID da sessão.
        if user:  # Se o usuário estiver autenticado:
            with sqlite3.connect(self.db_name) as conn:  # Abre uma conexão com o banco de dados SQLite.
                cursor = conn.cursor()  # Cria um cursor para executar comandos SQL.
            
            # Busca o ID do usuário pelo nome de usuário.
                cursor.execute("SELECT id FROM users WHERE username = ?", (user.username,))
                user_data = cursor.fetchone()
            
                if user_data:  # Verifica se o usuário foi encontrado.
                    user_id = user_data[0]
                    cursor.execute("INSERT INTO tasks (user_id, description) VALUES (?, ?)", 
                                (user_id, description))  # Insere uma nova tarefa para o usuário autenticado.
                    conn.commit()  # Confirma as alterações no banco de dados.
                    print(f"Tarefa '{description}' adicionada para o usuário {user.username}.")
                else:
                    print("Erro: Usuário não encontrado no banco de dados.")
        else:
            print("Erro: Usuário não autenticado.")  # Exibe erro se o usuário não estiver autenticado.
# Exibe erro se o usuário não estiver autenticado.

    def delete_task(self, session_id, task_id):
        """Remove uma tarefa associada ao usuário autenticado."""
        user = self.getUserSessionId(session_id)
        if user:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", 
                            (task_id, self.get_user_id(user.username)))
                conn.commit()
                print(f"Tarefa {task_id} removida para o usuário {user.username}.")
        else:
            print("Erro: Usuário não autenticado.")
            
    def get_tasks(self, session_id):
        """Retorna todas as tarefas associadas ao usuário autenticado."""
        user = self.getUserSessionId(session_id)
        if user:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (self.get_user_id(user.username),))
                return cursor.fetchall()
        else:
            print("Erro: Usuário não autenticado.")
            return []
