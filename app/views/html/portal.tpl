<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.png" />
    <link rel="stylesheet" href="/static/css/portal.css">
    <title>.:: Pink List (Login) ::.</title>

</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Login</h2>
        </div>
        <div class="form-container">
            <form action="/portal" method="POST">
                <!-- Formulário de login -->
                <div class="form-group">
                    <label for="username">Usuário:</label>
                    <input type="text" id="username" name="username" placeholder="Digite seu nome de usuário" required>
                </div>
                <div class="form-group">
                    <label for="password">Senha:</label>
                    <input type="password" id="password" name="password" placeholder="Digite sua senha" required>
                </div>
                <div class="button-container">
                <button type="submit">Entrar</button>

            </form>

            <!-- Botão para cadastro de novo usuário -->
            <div class="button-container">
                <p>Não tem uma conta?</p>
                <a href="/register"><button type="button">Cadastrar novo usuário</button></a>
            </div>
        </div>
    </div>
</body>
</html>
