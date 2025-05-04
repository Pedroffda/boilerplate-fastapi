![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-3A5EAB?style=for-the-badge&logo=alembic&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3A5EAB?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-4B8BBE?style=for-the-badge&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

# Boilerplate API - FastAPI

A API do projeto **Boilerplate** foi desenvolvida para fornecer funcionalidades relacionadas ao gerenciamento de usuários e outras operações relacionadas. Este projeto utiliza **FastAPI** como framework, **SQLAlchemy** para ORM, e **Alembic** para migrações de banco de dados.

## 🛠️ Tecnologias

| Tecnologia       | Descrição                                                                 |
|------------------|---------------------------------------------------------------------------|
| **FastAPI**      | Framework moderno e rápido para APIs com Python                           |
| **SQLAlchemy**   | ORM poderoso para banco de dados                                          |
| **Alembic**      | Ferramenta de migração de banco de dados                                  |
| **Pydantic**     | Validação de dados e serialização                                         |
| **JWT**          | Autenticação segura com JSON Web Tokens                                   |
| **PostgreSQL**   | Banco de dados relacional recomendado (compatível com SQLite e MySQL)     |
| **Redis**        | Cache e armazenamento para tokens (opcional)                              |
| **Docker**       | Containerização para fácil deploy                                         |
---

## 📦 **Instalação**

### **Pré-requisitos**
- **Python 3.8 ou superior**
- **Banco de dados** (PostgreSQL, MySQL ou SQLite)
- **Dependências do projeto** (instaladas via `pip`)

---

### **Passos para instalação**

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/Pedroffda/boilerplate-fastapi.git
    cd boilerplate-fastapi
    ```

2. **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    venv\Scripts\activate  # Para Windows
    ```

3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure as variáveis de ambiente no arquivo `.env`:**
    ```env
    DATABASE_URL=postgresql://fastapi_user:password123@localhost:5432/fastapi_db
    SECRET_KEY=secret
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    FRONTEND_URL=http://localhost:3000
    SMTP_USER=user
    SMTP_PASSWORD=password
    SMTP_HOST=smtp 
    SMTP_PORT=port
    ```

5. **Aplique as migrações no banco de dados:**
    ```bash
    alembic upgrade head
    ```


6. **Inicie o servidor da API:**
    ```bash
    uvicorn app.main:app --reload
    ```

---



## ⚙️ **Comandos Úteis**

### **Executar a API**
```bash
uvicorn app.main:app --reload
```

### **Criar uma nova migração Alembic**
```bash
alembic revision --autogenerate -m "nome-da-migracao"
```

### **Aplicar migrações no banco de dados**
```bash
alembic upgrade head
```

### **Reverter a última migração**
```bash
alembic downgrade -1
```

---

## 📚 **Documentação da API**
Acesse a documentação da API no navegador:

- **Swagger**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 👨‍💻 **Configuração do Usuário Administrador**

O sistema inclui um comando CLI para criar automaticamente o usuário admin inicial com todas as permissões.

### Como criar o usuário admin:

#### Opção 1: Modo interativo (recomendado para desenvolvimento)
```bash
python cli.py interactive
```
O sistema irá solicitar:
- Email do administrador
- Senha (a entrada será ocultada)

#### Opção 2: Modo direto (para automação)
```bash
python cli.py create --email admin@dominio.com --password SuaSenhaSegura
```

### Permissões padrão do admin:
- Acesso completo a todos os recursos (`*`)
- Permissões `ALLOW` para todas as ações
- Política de acesso global


### Estrutura do usuário admin:
```yaml
id: UUID único
nome: "Administrador"
email: configurado pelo usuário
senha: hash bcrypt
permissões:
  - efeito: allow
  - recursos: ["*"]
  - ações: ["*"]
```

---

Observações:
1. Os comandos assumem que o arquivo `cli.py` está na raiz do projeto
2. As variáveis de ambiente são opcionais
3. A senha é sempre hasheada antes de ser armazenada
4. O sistema verifica se o admin já existe antes de criar