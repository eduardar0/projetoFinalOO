<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registrar Usuário</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <script>
        function validateForm() {
            var password = document.getElementById("password").value;
            var confirm_password = document.getElementById("confirm_password").value;
            if (password !== confirm_password) {
                alert("As senhas não coincidem.");
                return false;
            }
            return true;
        }
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Cadastro de Novo Usuário</h2>
        </div>
        <div class="form-container">
            <form action="/register" method="POST" onsubmit="return validateForm()">
                <div class="form-group">
                    <label for="username">Nome de Usuário:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Senha:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <div class="form-group">
                    <label for="confirm_password">Confirme a Senha:</label>
                    <input type="password" id="confirm_password" name="confirm_password" required>
                </div>
                <button type="submit">Cadastrar</button>
            </form>
            <!-- Exibe erros se existirem -->
           
                <p class="error">{{ error }}</p>
            
        </div>
    </div>
</body>
</html>
