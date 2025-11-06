# 💰 Gestor Financeiro Pessoal (Projeto Django)

Este projeto é uma aplicação web desenvolvida em Django que serve como um **Gestor Financeiro Pessoal** simples. Foi desenvolvido como parte de um projeto acadêmico para demonstrar proficiência no framework Django, modelagem de dados e implementação de lógica de negócios.

## 🌟 Funcionalidades Principais

- **Autenticação de Usuário:** Sistema de Login e Logout utilizando o framework de autenticação nativo do Django.
- **Gestão de Transações (CRUD Completo):** Registrar, visualizar, editar e excluir Receitas e Despesas.
- **Gestão de Contas:** Cadastro e gerenciamento de diferentes fontes de recursos (Carteira, Conta Corrente, Poupança, etc.).
- **Gestão de Categorias:** Classificação de transações para fins de relatório (Ex: Alimentação, Salário, Lazer).
- **Dashboard Visual:** Painel de controle inicial com resumo do balanço geral e gráficos básicos (pronto para expansão).
- **Interface Amigável:** Utiliza **Bootstrap 5** para um layout responsivo e moderno.

## 🚀 Guia de Configuração e Instalação

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

### Pré-requisitos

- Python 3.10+
- `pip` (Gerenciador de pacotes do Python)

### 1. Clonar o Repositório

```bash
git clone [https://github.com/MilitaoPedro/GestorFinanceiro_Django.git](https://github.com/MilitaoPedro/GestorFinanceiro_Django.git)
cd GestorFinanceiro_Django
2. Configuração do Ambiente Virtual
É altamente recomendado o uso de um ambiente virtual (venv).

Bash

# Criar o ambiente virtual (se ainda não existe)
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate  # (Linux/macOS)
# venv\Scripts\activate   # (Windows)
3. Instalar Dependências
Com o ambiente virtual ativo, instale os pacotes necessários:

Bash

pip install Django pillow django-contrib-humanize
(Nota: O django-contrib-humanize é necessário para a formatação de números nos templates).

4. Configuração do Banco de Dados
O projeto utiliza SQLite por padrão. Aplique as migrações para criar as tabelas:

Bash

python manage.py makemigrations core
python manage.py migrate
5. Criar Usuário Administrador
Crie um superusuário para acessar o Admin e fazer o primeiro login:

Bash

python manage.py createsuperuser
# Defina login e senha.
6. Rodar a Aplicação
Inicie o servidor de desenvolvimento:

Bash

python manage.py runserver
Abra seu navegador e acesse: http://127.0.0.1:8000/

🛠️ Detalhes da Implementação
Estrutura do Projeto
O projeto utiliza uma estrutura com um único app principal (core):

GestorFinanceiro_Django/
├── core/
│   ├── templates/
│   │   ├── core/           # Templates da aplicação (Dashboard, Extrato, CRUDs)
│   │   └── registration/   # Templates de autenticação (login, etc.)
│   ├── models.py         # Modelagem de dados (Conta, Categoria, Transacao)
│   ├── views.py          # Lógica de negócio (Class-Based Views)
│   └── forms.py          # Lógica dos formulários
├── gestor_financeiro/    # Configurações gerais do projeto (settings.py, urls.py principal)
└── README.md
Tecnologias Utilizadas
Backend: Python 3 + Django 5.x

Frontend: HTML5, CSS3, Bootstrap 5 (CDN)

Database: SQLite3

Visualização de Dados: Chart.js (pronto para integração nos relatórios)

👤 Desenvolvedores
Nomes: João Lucas ramalho e Pedro Militão

GitHub: @MilitaoPedro

Projeto Acadêmico: Gestão Financeira com Django
```
