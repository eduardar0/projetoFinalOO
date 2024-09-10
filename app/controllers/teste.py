# teste.py
from app.controllers.datarecord import DataRecord

def main():
    data_record = DataRecord()
    
    # Criação de um superusuário
    session_id = data_record.checkUser('novo_admin', 'senha_segura')
    if session_id:
        print("Superusuário autenticado com sucesso.")
        
        # Tenta criar um novo usuário administrador
        data_record.book(session_id, 'novo_usuario', 'nova_senha', is_admin=True)

        # Liste todos os usuários (só pode ser feito por administradores)
        #cRud (READ)
        mostrar = data_record.get_all_users(session_id)
        print("Usuários no banco de dados:", mostrar)
    else:
        print("Falha no login. Verifique o nome de usuário e a senha.")

if __name__ == "__main__":
    main()
