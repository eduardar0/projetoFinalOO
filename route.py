from app.controllers.application import Application
from bottle import Bottle, request, static_file, redirect, template, response
import sqlite3
from app.controllers.datarecord import DataRecord
app = Bottle()
ctl = Application()

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper():
    return ctl.render('helper')

@app.route('/pagina', methods=['GET'])
@app.route('/pagina/<parameter>', methods=['GET'])
def pagina(parameter=None):
    return ctl.render('pagina', parameter)

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
    return redirect('/helper')


@app.route('/register', method='GET')
def register_page():
    return ctl.register_page()

@app.route('/register', method='POST')
def register_user():
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')
    
    if password != confirm_password:
        return template('app/views/html/register', error="Senhas não coincidem.")
    
    try:
        ctl.model.book(None, username, password, is_admin=False)  # Use ctl.model
        session_id = ctl.model.checkUser(username, password)
        if session_id:
            response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
            return redirect('/pagina')
        else:
            return template('app/views/html/register', error="Erro ao autenticar após o registro.")
    except sqlite3.IntegrityError:
        return template('app/views/html/register', error="O nome de usuário já existe. Tente outro.")
    except Exception as e:
        return template('app/views/html/pagina', error=f"Erro inesperado: {e}")



if __name__ == '__main__':
    app.run(host='localhost', port=8083, debug=True)
