<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.png" />
    <link rel="stylesheet" href="/static/css/edit_password.css">
    <title>.:: Alterar Senha ::.</title>
</head>
<body>

    <div class="container">    
    <h2>Alterar Senha</h2>
    
    
    <!-- Formulário para alteração de senha -->
    <form method="post" action="/edit_password">
        <label for="old_password">Senha Atual:</label>
        <input type="password" id="old_password" name="old_password" placeholder="Digite sua senha atual" required><br><br>
        
        <label for="new_password">Nova Senha:</label>
        <input type="password" id="new_password" name="new_password" placeholder="Digite uma nova senha" required><br><br>
        
        <label for="confirm_new_password">Confirmar Nova Senha:</label>
        <input type="password" id="confirm_new_password" name="confirm_new_password" placeholder="Digite novamente a senha nova" required><br><br>
        
        <input class="button" type="submit" value="Alterar Senha">
    </form>
</body>
</html>

