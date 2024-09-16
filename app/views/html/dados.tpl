<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.png" />
    <link rel="stylesheet" href="/static/css/styles.css">
    <title>Dados do Usuário</title>
</head>
<body>
    % if current_user:
    <div>
        <h2>Meus dados cadastrados</h2>
        <p>Nome de Usuário: {{ current_user.username }}</p>
        <p>Senha: {{ current_user.password }}</p>

        <div class="button-container">
            <!-- Formulário para editar dados -->
            <form action="/edit_password" method="get">
                <button type="submit">Editar senha</button>
            </form>

            <!-- Formulário para deletar conta -->
            <form action="/delete_account_confirm/{{current_user}}" method="get">
                <button type="submit">Deletar minha conta</button>
            </form>
        </div>
    </div>
    % else:
    <p>Você não está logado.</p>
    % endif
</body>
</html>
