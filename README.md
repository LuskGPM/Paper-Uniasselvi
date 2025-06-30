🚀 Visão Geral do Projeto
Este projeto consiste em um sistema web completo para a gestão de produtos, desenvolvido com Flask (Python) e SQLAlchemy para interação com o banco de dados. Ele implementa um sistema robusto de controle de acesso baseado em papéis, diferenciando as funcionalidades disponíveis para usuários Administradores e Júniores.

O sistema permite que administradores gerenciem produtos de forma direta, enquanto júniores podem visualizar produtos e solicitar alterações em campos específicos, que posteriormente precisam ser aprovadas ou rejeitadas pelos administradores.

✨ Funcionalidades Principais
Autenticação e Autorização:

Login e Cadastro de Usuários: Permite que novos usuários se registrem e usuários existentes façam login com segurança.

Controle de Acesso por Papel (RBAC): Diferencia automaticamente usuários Administradores (is_adm=True) de Júniores (is_adm=False), redirecionando-os para painéis e funcionalidades apropriadas.

Hash de Senhas: Utiliza werkzeug.security para armazenar senhas de forma segura.

Gestão de Produtos (para Administradores):

Listagem de Produtos: Visualiza todos os produtos cadastrados.

Cadastro de Novos Produtos: Adiciona novos produtos ao sistema com detalhes como nome, descrição, preço de venda, quantidade e data de validade.

Edição Direta de Produtos: Administradores podem atualizar diretamente qualquer informação de um produto existente.

Exclusão de Produtos: Remove produtos do sistema.

Fluxo de Solicitação de Alteração (para Júniores):

Visualização de Produtos: Júniores podem ver os detalhes dos produtos.

Solicitação de Alterações: Júniores podem propor mudanças em preço de venda, quantidade e data de validade de um produto. Essas solicitações são registradas em uma tabela separada (SolicitarAlteracao) e ficam com o status Pendente.

Monitoramento de Solicitações: Júniores têm uma página dedicada para visualizar o status de todas as suas solicitações, categorizadas como Pendentes, Aceitas ou Recusadas, incluindo o motivo da recusa quando aplicável.

Gestão de Solicitações (para Administradores):

Listagem de Solicitações Pendentes: Administradores acessam um painel para ver todas as solicitações de alteração que ainda aguardam aprovação.

Aprovação de Solicitações: Administradores podem aceitar uma solicitação. Ao aceitar, o sistema automaticamente atualiza o produto real no banco de dados com os novos valores propostos e marca a solicitação como Aprovada.

Rejeição de Solicitações: Administradores podem rejeitar uma solicitação, marcando-a como Rejeitada e, opcionalmente, registrando um motivo.

🛠️ Tecnologias Utilizadas
Backend: Python 3.x com Flask

Banco de Dados: SQLAlchemy ORM (para interação com SQLite, PostgreSQL, MySQL, etc.)

Autenticação: Flask-Login

Migrações de Banco de Dados: Flask-Migrate (Alembic)

Segurança de Senhas: Werkzeug

HTML/CSS/JavaScript: Para a interface do usuário (templates Jinja2)

⚙️ Configuração e Execução do Projeto
Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

Pré-requisitos
Python 3.x instalado

Pip (gerenciador de pacotes do Python)

1. Clonar o Repositório
Bash

git clone <URL_DO_SEU_REPOSITORIO>
cd <nome_da_pasta_do_projeto>
2. Criar e Ativar o Ambiente Virtual
É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.

Bash

python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
3. Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas necessárias:

Bash

pip install -r requirements.txt
Conteúdo Sugerido para requirements.txt:

Flask
Flask-SQLAlchemy
Flask-Login
Flask-Migrate
Werkzeug
python-dotenv
4. Configurar o Banco de Dados
Este projeto utiliza SQLAlchemy com Flask-Migrate (Alembic) para gerenciar o banco de dados.

a. Inicializar o Alembic (se ainda não o fez):

Bash

flask db init
b. Gerar a primeira migração (após definir seus modelos em src/models.py):

Bash

flask db migrate -m "Initial migration"
c. Aplicar as migrações ao banco de dados:

Bash

flask db upgrade
Nota: Se você fizer alterações nos seus modelos (src/models.py) após a primeira migração, repita os passos b e c para gerar e aplicar novas migrações.

5. Executar o Aplicativo Flask
Com tudo configurado, você pode iniciar o servidor de desenvolvimento do Flask:

Bash

python run.py
O servidor estará rodando em http://127.0.0.1:5000/ (ou outra porta, dependendo da sua configuração).

📂 Estrutura do Projeto
.
├── venv/                   # Ambiente virtual (ignorado pelo git)
├── migrations/             # Arquivos de migração do Alembic
├── src/
│   ├── __init__.py         # Inicialização da aplicação Flask
│   ├── app.py              # Configuração principal da aplicação e banco de dados
│   ├── models.py           # Definição dos modelos de banco de dados (User, Produtos, SolicitarAlteracao)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py         # Rotas de autenticação (login, cadastro, logout)
│   │   ├── main.py         # Rotas principais (dashboard)
│   │   ├── produtos.py     # Rotas de gestão de produtos (admin e redirecionamento junior)
│   │   ├── alteracao.py    # Rotas de solicitação de alteração (junior) e aprovação/rejeição (admin)
│   │   └── user.py         # Rotas de gerenciamento de usuário e administração (listar solicitações admin)
│   ├── static/             # Arquivos estáticos (CSS, JS, imagens)
│   └── templates/          # Arquivos de template HTML (Jinja2)
│       ├── base.html       # Template base para herança
│       ├── auth/           # Templates de autenticação
│       ├── perfil/         # Templates do dashboard
│       ├── produtos/       # Templates relacionados a produtos (detalhes_admin, detalhes_junior)
│       ├── admin/          # Templates para funcionalidades administrativas (listar_solicitacoes)
│       └── junior/         # Templates para funcionalidades do júnior (minhas_solicitacoes)
├── .env                    # Variáveis de ambiente (ex: CHAVE_SECRETA, DATABASE_URL)
├── .flaskenv               # Variáveis de ambiente Flask (ex: FLASK_APP)
├── requirements.txt        # Dependências do projeto
├── run.py                  # Script para iniciar a aplicação
└── README.md               # Este arquivo!
👤 Níveis de Acesso
Administrador (is_adm = True):

Acesso total à gestão de produtos (criar, ler, atualizar, excluir).

Acesso ao painel de gerenciamento de solicitações de alteração (aprovar/rejeitar).

Júnior (is_adm = False):

Apenas visualização de produtos.

Capacidade de enviar solicitações de alteração para aprovação.

Página de acompanhamento do status de suas próprias solicitações.

🤝 Contribuição
Sinta-se à vontade para explorar, modificar e melhorar este projeto.

📄 Licença
Este projeto é de código aberto e está disponível sob a licença MIT

🙏 Agradecimentos
Agradecimento especial à inteligência artificial que auxiliou na documentação e desenvolvimento deste projeto.