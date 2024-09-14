<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página Principal</title>
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <div class="container">
        <h1>Bem-vindo, {{ user_name }}!</h1>
          <h2>Aqui estão suas tarefas:</h2>



<ul>
    % for task in tasks:
        <li>
            {{ task['description'] }}
            <form action="/pagina/delete_task" method="post" style="display:inline;">
                <input type="hidden" name="task_id" value="{{ task['id'] }}">
                <button type="submit">Excluir</button>
            </form>
        </li>
    % end
</ul>

        <!-- Formulário para adicionar novas tarefas -->
        <form action="/pagina/add_task" method="post">
            <label for="task_description">Nova Tarefa:</label>
            <input type="text" id="task_description" name="task_description" required>
            <button type="submit">Adicionar</button>
        </form>
        
        <!-- Botão de Logout -->
        <form action="/logout" method="post">
            <button type="submit">Logout</button>
        </form>

        <!-- Botão para visualizar os dados -->
        <form action="/dados" method="get">
            <button type="submit">Meus Dados</button>
        </form>

    </div>
</body>
</html>