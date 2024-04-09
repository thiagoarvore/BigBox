<h1>Sistema de Gestão de Estoque (SGE)</h1>
<p>Bem-vindo ao Sistema de Gestão de Estoque (SGE), um projeto desenvolvido em Django para facilitar o gerenciamento de estoque. Este README fornece informações essenciais sobre como configurar e executar o projeto em seu ambiente local.</p>

<h2>Requisitos</h2>
<p>Certifique-se de que você tenha os seguintes requisitos instalados em seu sistema:</p>

Python (versão recomendada: 3.7 ou superior)
Django (instalado automaticamente ao seguir as instruções abaixo)
Outras dependências listadas no arquivo requirements.txt
Instalação das Dependências
Com o ambiente virtual ativado, instale as dependências do projeto usando o comando:

pip install -r requirements.txt
Rodar o projeto
Após instalar as dependências, aplique as migrations no banco de dados com o comando:

python manage.py migrate
Agora o projeto jã pode ser inicializado com o comando:

python manage.py runserver
Após isso, o sistema estará pronto para ser acessado em: http://localhost:8000
