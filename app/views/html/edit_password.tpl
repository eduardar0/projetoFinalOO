<!DOCTYPE html>
<html>
<head>
    <title>Alterar Senha</title>
    <style>
        /* Adiciona um estilo básico para mensagens de erro */
        .error {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Alterar Senha</h1>
    
    
    <!-- Formulário para alteração de senha -->
    <form method="post" action="/edit_password">
        <label for="old_password">Senha Antiga:</label>
        <input type="password" id="old_password" name="old_password" required><br><br>
        
        <label for="new_password">Nova Senha:</label>
        <input type="password" id="new_password" name="new_password" required><br><br>
        
        <label for="confirm_new_password">Confirmar Nova Senha:</label>
        <input type="password" id="confirm_new_password" name="confirm_new_password" required><br><br>
        
        <input type="submit" value="Alterar Senha">
    </form>
</body>
</html>

