FROM python:3.9-slim

# Instala dependências
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação e modelos
COPY src/main.py .
COPY src/predictor.py .
COPY models/ models/

# Expondo a porta
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "main.py"]
