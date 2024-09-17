from app.controllers.application import Application
from bottle import Bottle, request, static_file, redirect, template, response, TEMPLATE_PATH
import sqlite3
from app.controllers.datarecord import DataRecord

db = DataRecord()
app = Bottle()
ctl = Application()

# Configura o caminho para a pasta de templates
TEMPLATE_PATH.insert(0, './app/views')

@app.route('/')
@app.route('/home', get='GET')
def home_getter():
    return ctl.render('home')

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper():
    return ctl.render('helper')

@app.route('/pagina', methods=['GET'])
@app.route('/pagina/<user_name>', methods=['GET'])
def pagina(user_name=None):
    session_id = ctl.get_session_id()  # Obtém o ID da sessão
    user_name = ctl.get_username_by_session(session_id)  # Obtém o nome de usuário
    piu = ctl.get_tasks(session_id)  # Obtém as tarefas associadas ao usuário
    tasks = []
    for task in tasks:
        tasks.append(f"{task}")
        tasks.append(f"{task}\n")  

    return ctl.pagina(user_name, tasks)

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')

@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username = ctl.authenticate_user(username, password)
    
    print(f"Session ID: {session_id}")  # Verifica se o ID de sessão está sendo gerado

    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, max_age=3600)
        return redirect('/pagina')
    else:
        return redirect('/portal')

@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    return redirect('/portal')

@app.route('/register', method='GET')
def register_page():
    return ctl.register_page()

@app.route('/register', method='POST')
def register_user():
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')
    
    # Verifica se as senhas são iguais
    if password != confirm_password:
        return template('html/register', error="As senhas não coincidem.")  # Corrigido o nome do template
    
    try:
        # Tenta registrar o usuário
        ctl.model.book(username, password, is_admin=False)  # Assumindo que book cria o usuário
        
        # Autentica o usuário logo após o registro
        session_id = ctl.model.checkUser(username, password)
        if session_id:
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            return redirect('/portal', success_message="Usuário cadastrado com sucesso.")  # Certifique-se de que o caminho de redirecionamento está correto
        else:
            return template('html/register', error="Erro ao autenticar após o registro.")
    except sqlite3.IntegrityError:
        return template('html/register', error="O nome de usuário já existe. Tente outro.")
    except Exception as e:
        return template('html/portal', success_message="Usuário cadastrado com sucesso.")


@app.route('/delete_account_confirm/<session_id>', method='GET')
def delete_account_confirm(session_id):
    return template('app/views/html/delete_account_confirm', session_id=session_id)

@app.route('/delete_account_confirm', method='POST')
def delete_account_confirm(): 
    ctl.delete_account_confirm()
    return redirect('/portal')
##### --- tarefaas 

@app.route('/pagina/add_task', method='POST')
def add_task():
    session_id = request.get_cookie('session_id')
    task_description = request.forms.get('task_description')
    if session_id and task_description:
        ctl.model.add_task(session_id, task_description)
        return redirect('/pagina')
    return "Erro ao adicionar tarefa."

@app.route('/pagina/delete_task', method='POST')
def delete_task():
    session_id = request.get_cookie('session_id')
    task_id = request.forms.get('task_id')
    if session_id and task_id:
        ctl.model.delete_task(session_id, task_id)
        return redirect('/pagina')
    return "Erro ao excluir tarefa."

@app.route('/dados', method = ['GET','POST'])
def dados():
    return ctl.render('dados')

@app.route('/edit_password', method='GET')
def edit_password():
    return ctl.render('edit_password')

@app.route('/edit_password', method='POST')
def update_password():
    return ctl.render('edit_password')


if __name__ == '__main__':
    app.run(host='localhost', port=8086, debug=True)