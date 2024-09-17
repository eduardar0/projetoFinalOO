<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="/static/img/favicon.png" />
    <link rel="stylesheet" href="/static/css/delete_account.css">
    <title>.:: Confirmar Exclusão ::.</title>
</head>
<body>
  <div class="container">
    <h3>Você tem certeza de que deseja excluir sua conta?</h3>
      <form action="/delete_account_confirm" method="post">
        <button class="button" type="submit">Sim, quero que seja deletada</button>
      </form>
  </div>

</html>
