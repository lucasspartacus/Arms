:test_tube: Case Desenvolvedor(a) - Arms

:desktop_computer: Lucas Spartacus

###  Estrutura projeto:

<h1>Inteligência Artificial (IA) </h1>

- Gemini API

<h1>Backend </h1>

- Python 3
- Flask
- ThreadPoolExecutor
- JSON

<h1>Frontend</h1>

- HTML5
- Jinja2 
- Bootstrap 5

###  Rodar Projeto:

Primeiramente rode o seguinte comando no seus prompt para clonar o repositorio github:

```
git clone https://github.com/lucasspartacus/Arms.git
```
Entre na pasta rh-selecao-inteligente.
Após isso rode o comando abaixo para criar um ambiente virtual:

```
python -m venv venv
```
Após isso rode o comando abaixo para ativar o ambiente:

```
venv\Scripts\activate
```
Após isso rode o comando abaixo para instalar todas as dependências:

```
pip install -r requirements.txt
```

Seguindo rode o código abaixo para rodar o projeto:

```
python app.py
```

Vá ao seu navegador na url http://127.0.0.1:5000 para usar a aplicação web.

Na aplicação você pode buscar por um arquivo json que contenha o formato correto referente aos usuário. Tal arquivo será analisado as Habilidades, Experiência e Valores do usuário serão passadas como prompt para gemini que realiza uma análise dos critérios técnicos e culturais, com isso verificar se o perfil dos candidatos se encaixam com a empresa. Retornando uma tela de feedback com todos os usuário borda e texto verde caso os mesmos tenham sido aprovados e vermelho caso o contrário.

Tela de resultados do processo seletivo da aplicação:

<img width="1143" height="733" alt="Image" src="https://github.com/user-attachments/assets/d82ac162-6a70-448b-a966-85064cdf6a64" />
