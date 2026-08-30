# Pyventory | Sistema de Gestão de Estoque e Vendas

Sistema de gerenciamento de inventário desenvolvido em Python/Django com interface customizada inspirada em terminais de linha de comando (Matrix/Terminal Vibe). O projeto foi construído focando em engenharia de software defensiva, isolamento de dados por usuário e regras de negócio transacionais.

Este repositório atende aos requisitos do processo seletivo **wsBackendFabricaDeSoftware26.2**.

## 🚀 Funcionalidades Principais

* **Segurança e Isolamento:** Sistema de autenticação nativo no qual cada lojista possui acesso e controle exclusivo apenas ao seu próprio estoque e histórico financeiro.
* **CRUD Completo e Relacionamentos:** Operações de Criação, Leitura, Atualização e Exclusão de produtos. O banco de dados utiliza relacionamentos explícitos (`ForeignKey`) entre as entidades `User` (Lojista), `Product` (Estoque) e `Sale` (Vendas).
* **Consumo de API com Engenharia Defensiva:** Importação automatizada de produtos via base global (DummyJSON) com tratamento de exceções, controle de *timeout* (evitando travamento do servidor) e conversão de moeda em tempo real via AwesomeAPI (USD para BRL) com taxa de *fallback* programada.
* **Motor de Vendas Transacional:** Lógica de negócios que, em uma única operação, valida a disponibilidade do item, debita o estoque, credita o valor total no saldo do lojista e registra o histórico imutável da transação.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3 & Django
* **Infraestrutura:** Docker & Docker Compose
* **Banco de Dados:** PostgreSQL (Produção/Docker) e SQLite (Fallback)
* **Integrações Externas (REST APIs):** 
  * DummyJSON API (Catálogo de produtos)
  * AwesomeAPI (Cotação de câmbio atualizada)
* **Frontend:** HTML5 e CSS3 (Design responsivo e semântico, sem dependência de frameworks externos)

## 🗺️ Mapa de Endpoints (Rotas do Sistema)

Embora o sistema utilize renderização no servidor (Templates HTML) ao invés de retornos JSON puros, a arquitetura de rotas foi desenhada seguindo a padronização e previsibilidade RESTful.

| Rota | Método HTTP | Descrição da Ação |
| :--- | :--- | :--- |
| `/accounts/login/` | GET, POST | Autenticação do lojista |
| `/accounts/logout/` | GET | Encerramento de sessão |
| `/` | GET | Redireciona para o inventário principal |
| `/inventory/` | GET | Listagem geral do estoque (Read) |
| `/product/register/` | GET, POST | Cadastro manual de novo produto (Create) |
| `/product/import/` | GET, POST | Importação automatizada de produtos via API externa |
| `/product/detail/<sku>/` | GET | Visualização detalhada de um item específico (Read) |
| `/product/update/<sku>/` | GET, POST | Edição de dados de um produto (Update) |
| `/product/delete/<sku>/` | GET, POST | Exclusão de um produto do estoque (Delete) |
| `/product/sale/` | GET, POST | Registro de venda transacional (baixa de estoque e crédito de saldo) |

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para testar a aplicação em sua máquina:

**1. Clone este repositório e acesse a pasta:**
```bash
git clone https://github.com/GuilhermeParnaibaNunes/wsBackendFabricaDeSoftware26.2.git
cd wsBackendFabricaDeSoftware26.2
```

**2. Configure as Variáveis de Ambiente (.env):**
Crie um arquivo chamado `.env` na raiz do projeto (no mesmo nível do arquivo `manage.py`) e insira as credenciais do banco:
*(Dica: Para gerar uma SECRET_KEY segura, execute `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` no seu terminal e cole o resultado no arquivo).*
```env
SECRET_KEY='cole-a-chave-gerada-aqui'
DEBUG=True
DB_NAME=pyventory_db
DB_USER=pyventory_user
DB_PASSWORD=pyventory_pass
DB_HOST=127.0.0.1
DB_PORT=5433
```

**3. Suba o Banco de Dados com Docker:**
Certifique-se de que o Docker Desktop está rodando e execute:
```bash
docker-compose up -d
```

**4. Crie e ative o ambiente virtual Python:**
* No Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
* No Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

**5. Instale as dependências obrigatórias:**
```bash
pip install -r requirements.txt
```

**6. Estruture o banco de dados e crie uma conta administrativa:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

**7. Inicie o servidor de desenvolvimento:**
```bash
python manage.py runserver
```

Acesse `http://localhost:8000` no seu navegador, faça o login com as credenciais criadas no passo 6 e utilize o sistema.