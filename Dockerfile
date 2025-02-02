# Usa a imagem oficial do Python como base
FROM python:3.9-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho no contêiner
WORKDIR /usr/src/app

# Copia o arquivo de dependências para dentro do contêiner
COPY requirements.txt ./

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o contêiner
COPY . .

# Expõe a porta que a FastAPI vai rodar
EXPOSE 8000

# Comando para rodar a aplicação FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
