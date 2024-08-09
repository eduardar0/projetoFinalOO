<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página Principal</title>
    <link rel="stylesheet" href="/static/css/styles.css"> <!-- Link para o arquivo CSS -->
</head>
<body>
    <div class="container">
        <h1>Bem-vindo, {{current_user.username}}</h1>
        <p>Esta é a página principal.</p>
        <form action="/logout" method="POST">
            <!-- Formulário para logout -->
            <button type="submit">Logout</button>
        </form>
    </div>
</body>
</html>
