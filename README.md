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
* **Banco de Dados:** SQLite (com transição mapeada para PostgreSQL)
* **Integrações Externas (REST APIs):** 
  * DummyJSON API (Catálogo de produtos)
  * AwesomeAPI (Cotação de câmbio atualizada)
* **Frontend:** HTML5 e CSS3 (Design responsivo e semântico, sem dependência de frameworks externos)

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para testar a aplicação em sua máquina:

**1. Clone este repositório:**
```bash
git clone [https://github.com/GuilhermeParnaibaNunes/wsBackendFabricaDeSoftware26.2.git](https://github.com/GuilhermeParnaibaNunes/wsBackendFabricaDeSoftware26.2.git)
```

**2. Acesse a pasta do projeto e crie o ambiente virtual:**
```bash
cd wsBackendFabricaDeSoftware26.2
python -m venv venv
```

**3. Ative o ambiente virtual:**
* No Windows:
```bash
venv\Scripts\activate
```
* No Linux/Mac:
```bash
source venv/bin/activate
```

**4. Instale as dependências obrigatórias:**
```bash
pip install -r requirements.txt
```

**5. Estruture o banco de dados e crie uma conta administrativa:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

**6. Inicie o servidor de desenvolvimento:**
```bash
python manage.py runserver
```

Acesse `http://localhost:8000` no seu navegador, faça o login com as credenciais criadas no passo 5 e utilize o sistema.