<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="/static/css/styles.css"> <!-- Link para o arquivo CSS -->
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
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>

            <!-- Botão para cadastro de novo usuário -->
            <div class="form-group">
                <p>Não tem uma conta?</p>
                <a href="/register"><button type="button">Cadastrar novo usuário</button></a>
            </div>
        </div>
    </div>
</body>
</html>
