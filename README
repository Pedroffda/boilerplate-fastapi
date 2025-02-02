# Boilerplate API - FastAPI

A API do projeto **Boilerplate** foi desenvolvida para fornecer funcionalidades relacionadas ao gerenciamento de usuários e outras operações relacionadas. Este projeto utiliza **FastAPI** como framework, **SQLAlchemy** para ORM, e **Alembic** para migrações de banco de dados.

---

## 🛠️ **Tecnologias Usadas**

- **FastAPI**: Framework web moderno e rápido para construção de APIs.
- **SQLAlchemy**: ORM para mapeamento objeto-relacional.
- **Alembic**: Ferramenta para migração de esquemas de banco de dados.
- **Pydantic**: Para validação de dados e tipagem estática.
- **Decouple**: Gerenciamento de variáveis de ambiente.

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