# Boilerplate API - FastAPI

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-3A5EAB?style=for-the-badge&logo=alembic&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3A5EAB?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-4B8BBE?style=for-the-badge&logo=pydantic&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

The **Boilerplate** API project was developed to provide user management functionalities and other related operations. This project uses **FastAPI** as the framework, **SQLAlchemy** for ORM, and **Alembic** for database migrations.

## 🛠️ Technologies

| Technology       | Description                                                                 |
|------------------|---------------------------------------------------------------------------|
| **FastAPI**      | Modern and fast API framework for Python                                  |
| **SQLAlchemy**   | Powerful ORM for database                                                 |
| **Alembic**      | Database migration tool                                                   |
| **Pydantic**     | Data validation and serialization                                         |
| **JWT**          | Secure authentication with JSON Web Tokens                                |
| **PostgreSQL**   | Recommended relational database (compatible with SQLite and MySQL)        |
| **Redis**        | Cache and token storage (optional)                                        |
| **Docker**       | Containerization for easy deployment                                      |

---

## 📦 **Installation**

### **Prerequisites**
- **Python 3.8 or higher**
- **Database** (PostgreSQL, MySQL, or SQLite)
- **Project dependencies** (installed via `pip`)

---

### **Installation Steps**

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Pedroffda/boilerplate-fastapi.git
    cd boilerplate-fastapi
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate  # For Windows
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables in the `.env` file:**
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

5. **Apply database migrations:**
    ```bash
    alembic upgrade head
    ```

6. **Start the API server:**
    ```bash
    uvicorn app.main:app --reload
    ```

---

## ⚙️ **Useful Commands**

### **Run the API**
```bash
uvicorn app.main:app --reload
```

### **Create a new Alembic migration**
```bash
alembic revision --autogenerate -m "migration-name"
```

### **Apply database migrations**
```bash
alembic upgrade head
```

### **Revert the last migration**
```bash
alembic downgrade -1
```

---

## 📚 **API Documentation**
Access the API documentation in your browser:

- **Swagger**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 👨‍💻 **Admin User Setup**

The system includes a CLI command to automatically create the initial admin user with all permissions.

### How to create the admin user:

#### Option 1: Interactive mode (recommended for development)
```bash
python cli.py interactive
```
The system will prompt for:
- Admin email
- Password (input will be hidden)

#### Option 2: Direct mode (for automation)
```bash
python cli.py create --email admin@domain.com --password YourSecurePassword
```

### Default admin permissions:
- Full access to all resources (`*`)
- `ALLOW` permissions for all actions
- Global access policy

### Admin user structure:
```yaml
id: Unique UUID
name: "Administrator"
email: user-configured
password: bcrypt hash
permissions:
  - effect: allow
  - resources: ["*"]
  - actions: ["*"]
```

---

Notes:
1. Commands assume `cli.py` is in the project root
2. Environment variables are optional
3. Password is always hashed before storage
4. System checks if admin already exists before creation