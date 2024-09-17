<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/x-icon" href="static/img/favicon.png" />
    <title>.:: Pink List (Home) ::.</title>
    <link rel="stylesheet" type="text/css" href="/static/css/home.css">
</head>
<body>
    <div class="container">
      <h1>Seja bem-vindo ao Pink List</h1>
      <h4>O melhor gerenciador de tarefas (=</h4>
      <img src="{{'static/img/mesa-de-trabalho.jpg'}}" alt="Descrição da Imagem"
         width="300" height="300" onclick="displayText()">
    <h1>Faça o login para começar:</h1>
        <div>
          <form action="/portal" method="get">
              <button type="submit"> Realizar login</button>
          </form>
          <p>Não tem uma conta?</p>
          <form action="/register" method="get">
              <button type="submit">Realizar cadastro</button>
          </form>
        </div>
    </div>
</body>
</html>