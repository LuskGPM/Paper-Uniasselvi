# Documentação do Projeto: Sistema de Gestão de Produtos com Níveis de Acesso

---

## 🚀 Visão Geral do Projeto

Este projeto consiste em um sistema web completo para a gestão de produtos, desenvolvido com **Flask** (Python) e **SQLAlchemy** para interação com o banco de dados. Ele implementa um sistema robusto de controle de acesso baseado em papéis, diferenciando as funcionalidades disponíveis para usuários **Administradores** e **Júniores**.

O sistema permite que administradores gerenciem produtos de forma direta, enquanto júniores podem visualizar produtos e **solicitar alterações** em campos específicos, que posteriormente precisam ser aprovadas ou rejeitadas pelos administradores.

---

## ✨ Funcionalidades Principais

* **Autenticação e Autorização:**
    * **Login e Cadastro de Usuários:** Permite que novos usuários se registrem e usuários existentes façam login com segurança.
    * **Controle de Acesso por Papel (RBAC):** Diferencia automaticamente usuários `Administradores` (`is_adm=True`) de `Júniores` (`is_adm=False`), redirecionando-os para painéis e funcionalidades apropriadas.
    * **Hash de Senhas:** Utiliza `werkzeug.security` para armazenar senhas de forma segura.

* **Gestão de Produtos (para Administradores):**
    * **Listagem de Produtos:** Visualiza todos os produtos cadastrados.
    * **Cadastro de Novos Produtos:** Adiciona novos produtos ao sistema com detalhes como nome, descrição, preço de venda, quantidade e data de validade.
    * **Edição Direta de Produtos:** Administradores podem atualizar diretamente qualquer informação de um produto existente.
    * **Exclusão de Produtos:** Remove produtos do sistema.

* **Fluxo de Solicitação de Alteração (para Júniores):**
    * **Visualização de Produtos:** Júniores podem ver os detalhes dos produtos.
    * **Solicitação de Alterações:** Júniores podem propor mudanças em `preço de venda`, `quantidade` e `data de validade` de um produto. Essas solicitações são registradas em uma tabela separada (`SolicitarAlteracao`) e ficam com o status `Pendente`.
    * **Monitoramento de Solicitações:** Júniores têm uma página dedicada para visualizar o status de **todas as suas solicitações**, categorizadas como `Pendentes`, `Aceitas` ou `Recusadas`, incluindo o motivo da recusa quando aplicável.

* **Gestão de Solicitações (para Administradores):**
    * **Listagem de Solicitações Pendentes:** Administradores acessam um painel para ver todas as solicitações de alteração que ainda aguardam aprovação.
    * **Aprovação de Solicitações:** Administradores podem **aceitar** uma solicitação. Ao aceitar, o sistema automaticamente atualiza o produto real no banco de dados com os novos valores propostos e marca a solicitação como `Aprovada`.
    * **Rejeição de Solicitações:** Administradores podem **rejeitar** uma solicitação, marcando-a como `Rejeitada` e, opcionalmente, registrando um motivo.

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.x com Flask
* **Banco de Dados:** SQLAlchemy ORM (para interação com SQLite, PostgreSQL, MySQL, etc.)
* **Autenticação:** Flask-Login
* **Migrações de Banco de Dados:** Flask-Migrate (Alembic)
* **Segurança de Senhas:** Werkzeug
* **HTML/CSS/JavaScript:** Para a interface do usuário (templates Jinja2)

---

## ⚙️ Configuração e Execução do Projeto

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

### Pré-requisitos

* Python 3.x instalado
* Pip (gerenciador de pacotes do Python)

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <nome_da_pasta_do_projeto>
```

### 2. Criar e Ativar o Ambiente Virtual (Opcional)

```bash
python -m venv venv
```
# No Windows
```bash
.\venv\Scripts\activate
```
# No macOS/Linux
```bash
source venv/bin/activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. o Banco de Dados
este projeto utiliza SQLAlchemy com Flask-Migrate (Alembic) para gerenciar o banco de dados.
o Banco será criado assim que for iniciado a aplicação na pasta '/src/db/farma.db'

### 5. Execução do aplicativo Flask
```bash
python run.py
```
O servidor estará rodando em http://127.0.0.1:5000/ (ou outra porta, dependendo da sua configuração)

\#\# 📂 Estrutura do Projeto

\`\`\`
.
├── venv/                   \# Ambiente virtual (ignorado pelo git)
├── migrations/             \# Arquivos de migração do Alembic
├── src/
│   ├── \_\_init\_\_.py         \# Inicialização da aplicação Flask
│   ├── app.py              \# Configuração principal da aplicação e banco de dados
│   ├── models.py           \# Definição dos modelos de banco de dados (User, Produtos, SolicitarAlteracao)
│   ├── routes/
│   │   ├── \_\_init\_\_.py
│   │   ├── auth.py         \# Rotas de autenticação (login, cadastro, logout)
│   │   ├── main.py         \# Rotas principais (dashboard)
│   │   ├── produtos.py     \# Rotas de gestão de produtos (admin e redirecionamento junior)
│   │   ├── alteracao.py    \# Rotas de solicitação de alteração (junior) e aprovação/rejeição (admin)
│   │   └── user.py         \# Rotas de gerenciamento de usuário e administração (listar solicitações admin)
│   ├── static/             \# Arquivos estáticos (CSS, JS, imagens)
│   └── templates/          \# Arquivos de template HTML (Jinja2)
│       ├── base.html       \# Template base para herança
│       ├── auth/           \# Templates de autenticação
│       ├── main/           \# Templates do dashboard
│       ├── produtos/       \# Templates relacionados a produtos (detalhes\_admin, detalhes\_junior)
│       ├── admin/          \# Templates para funcionalidades administrativas (listar\_solicitacoes)
│       └── junior/         \# Templates para funcionalidades do júnior (minhas\_solicitacoes)
├── .env                    \# Variáveis de ambiente (ex: CHAVE\_SECRETA, DATABASE\_URL)
├── .flaskenv               \# Variáveis de ambiente Flask (ex: FLASK\_APP)
├── requirements.txt        \# Dependências do projeto
├── run.py                  \# Script para iniciar a aplicação
└── README.md               \# Este arquivo!
\`\`\`

---

\#\# 👤 Níveis de Acesso

* **Administrador (\`is\_adm = True\`):**
    * Acesso total à gestão de produtos (criar, ler, atualizar, excluir).
    * Acesso ao painel de gerenciamento de solicitações de alteração (aprovar/rejeitar).
* **Júnior (\`is\_adm = False\`):**
    * Apenas visualização de produtos.
    * Capacidade de enviar solicitações de alteração para aprovação.
    * Página de acompanhamento do status de suas próprias solicitações.

---

\#\# 🤝 Contribuição

Sinta-se à vontade para explorar, modificar e melhorar este projeto.

---

\#\# 📄 Licença

Este projeto é de código aberto e está disponível sob a \[Licença MIT\](https://opensource.org/licenses/MIT).

---
