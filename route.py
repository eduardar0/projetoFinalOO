from app.controllers.application import Application
from bottle import Bottle, request, static_file, redirect, template, response, TEMPLATE_PATH
import sqlite3
from app.controllers.datarecord import DataRecord

db = DataRecord()
app = Bottle()
ctl = Application()

# Configura o caminho para a pasta de templates
TEMPLATE_PATH.insert(0, './app/views')

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
    tasks = ctl.get_tasks(session_id)  # Obtém as tarefas associadas ao usuário
    return ctl.pagina(user_name, tasks)

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')

@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, user_name = ctl.authenticate_user(username, password)
    
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
    
    if password != confirm_password:
        return template('register', error="Senhas não coincidem.")
    
    try:
        ctl.model.book(None, username, password, is_admin=False)  # Use ctl.model
        session_id = ctl.model.checkUser(username, password)
        if session_id:
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            return redirect('/portal')
        else:
            return template('register', error="Erro ao autenticar após o registro.")
    except sqlite3.IntegrityError:
        return template('register', error="O nome de usuário já existe. Tente outro.")
    except Exception as e:
        return template('portal', error=f"Erro inesperado: {e}")


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




if __name__ == '__main__':
    app.run(host='localhost', port=8084, debug=True)