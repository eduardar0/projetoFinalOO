<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.png" />
    <link rel="stylesheet" href="/static/css/dados.css">
    <title>.:: Dados do Usuário ::.</title>
</head>
<body>
    % if current_user:
    <div class="container">
        <h1>Meus dados cadastrados</h1>


        <div class="text">    
         <h3> Nome de Usuário: {{ current_user.username }}</h3>
         <h3>Senha: {{ current_user.password }}</h3>
        </div> 

        <div class="button-container">
            <!-- Formulário para editar dados -->
            <form action="/edit_password" method="get">
                <button class="button" type="submit">Editar senha</button>
            </form>

            <!-- Formulário para deletar conta -->
            <form action="/delete_account_confirm/{{current_user}}" method="get">
                <button class="button" type="submit">Deletar minha conta</button>
            </form>
        </div>
    </div>
    % else:
    <p>Você não está logado.</p>
    % endif
</body>
</html>
