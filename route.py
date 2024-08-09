from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file, redirect, template, response

app = Bottle()
ctl = Application()

#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
# O decorador é responsável por associar uma função Python a uma rota web
def helper():
    return ctl.render('helper')

#-----------------------------------------------------------------------------
# Suas rotas aqui
@app.route('/pagina', methods=['GET'])
@app.route('/pagina/<parameter>', methods=['GET'])
def action_pagina(parameter=None):
    # Rota para exibir a página. Se houver um parâmetro, ele será passado para o controlador
    return ctl.render('pagina', parameter)

@app.route('/portal', method='GET')
def login():
    # Rota para exibir a página de login.
    return ctl.render('portal')

######------------------------------------------------------

# Funções de processamento de dados, do tipo 'POST'

@app.route('/portal', method='POST')
# Rota /portal na URL, tipo POST
def action_portal():
    # Processar o login. Verifica as credenciais e redireciona para a página do usuário.
    username = request.forms.get('username')
    #-----------
    # request.forms.get() é uma função do framework
    # forms é um atributo do objeto request que representa os dados do formulário
    # dados informados pelo usuário por meio do formulário HTML
    #------------
    password = request.forms.get('password')

    # Autenticação do usuário:
    session_id, username = ctl.authenticate_user(username, password)
    # authenticate_user é uma função implementada na classe Application()
    # Se as credenciais forem válidas, ele retorna um ID da sessão, e não, retorna None

    if session_id:
        # Se o usuário for autenticado:
        response.set_cookie('session_id', session_id, httponly=True, secure=True, max_age=3600)
        # Cria um cookie para o usuário e redireciona-o para uma página personalizada
        # de cada usuário
        redirect(f'/pagina/{username}')
    else:
        return redirect('/portal')
    # Se o session_id não existir (for 'None'), o usuário é redirecionado
    # novamente para a página de login '/portal'

@app.route('/logout', method='POST')
def logout():
    """Rota para realizar o logout. Remove o cookie de sessão e redireciona para a página de ajuda."""
    ctl.logout_user()
    response.delete_cookie('session_id')
    redirect('/helper')

#-----------------------------------------------------------------------------

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
