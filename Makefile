
# Arquivo: Makefile

# Variáveis
IMAGE_NAME = minha-api
TAG = latest
DOCKER_CONTEXT = ./api

# Build da imagem Docker
build:
	docker build -t $(IMAGE_NAME):$(TAG) $(DOCKER_CONTEXT)

# Subir com Docker Compose
up:
	docker-compose up --build -d

# Parar e remover containers
down:
	docker-compose down

# Testar a API local
test:
	curl "http://localhost:5000/predict?id=123&version=v1"

# Deploy com Terraform
deploy:
	cd terraform && terraform apply -auto-approve

# Destruir infraestrutura
destroy:
	cd terraform && terraform destroy -auto-approve
