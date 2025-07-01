# INTRUÇÕES DE USO E CONFIGURAÇÕES #

1 - Caso utilize o Visual Studio Code, instale oa entensão Python Extension Pack;

2 - Abra a pasta principal do diretorio e selecione seu interpretador Python;

3 - Abra o terminal do VS Code ou Pycharm e digit o comando "python -m venv venv", para criar um ambiente virtualizado do Python;

4 - Após a criação da venv, digite os seguintes comandos no terminal:
  Para terminal CMD: "venv\Script\activate"
  Para terminal BASH: "source venv/Script/activate"

5 - Após ativar o ambiente virtual, instale o Django na sua venv utilizando este comando no terminal:
  "pip install Django"

6 - Após a instalação do Django o projeto já estará pronto para abrir o servidor e ser utilizado.
  Para Isto, dentro do terminal com venv ativado e Django instalado, digite: "manage.py runserver"

7 - Para fechar o servidor, vá até o terminal onde foi aberto o servidor e aperte as teclas "ctrl + C"
