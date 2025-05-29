FROM python:3.9-slim

# Instala dependências
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação e modelos
COPY src/main.py .
COPY src/predictor.py .
#COPY models/ models/

# Expondo a porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "main.py"]
