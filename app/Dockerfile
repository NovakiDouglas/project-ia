FROM python:3.9-slim

# Instala dependências do sistema
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código fonte
COPY src/ .

# Expõe a porta
EXPOSE 5000

# Comando de inicialização
CMD ["python", "main.py"]
