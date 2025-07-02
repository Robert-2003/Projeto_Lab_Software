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

## Login e Início de uso do sistema ##

Ao acessar o sistema do site, faça login com os seguintes campos:
Matrícula: 1234
Senha: 1234

Com isto você acessara o perfil de Administrador e poderá criar novos usuários de qualquer tipo, e deletar e alterar os mesmos.


### Tipos de Usuários e suas funções ###
Administrador: criar, altera e deleta usuários de qualquer tipo, inclusive outros administradores.


Técnico: Assume chamados disponíveis, onde o mesmo tem uma série de ações com os chamados, seja alterando, adicionando soluções e fechando os chamados.

Cliente: usuário que cria os chamados. O usuário terá uma lista com chamados em respectivos status: disponíveis, aceitos (quando um técnico assumiu um chamado) e fechado (quando um técnico ou o próprio cliente fecham o chamado).
O cliente também pode alterar e excluir seus chamados.