#!/bin/bash

set -e  # Encerra se houver erro

# Define o ambiente com fallback para "dev"
ENVIRONMENT="${1:-dev}"

# Valida ambiente permitido
if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "prod" ]]; then
  echo "❌ Ambiente inválido. Use: ./deploy.sh [dev|prod]"
  exit 1
fi

echo "🚀 Iniciando deploy com Terraform para ambiente: $ENVIRONMENT"

# Verifica se pasta terraform existe
if [ ! -d terraform ]; then
  echo "❌ Diretório 'terraform' não encontrado."
  exit 1
fi

cd terraform

echo "🔍 Selecionando workspace..."
terraform workspace select "$ENVIRONMENT" || terraform workspace new "$ENVIRONMENT"

echo "📦 Inicializando Terraform..."
terraform init -input=false

echo "📐 Gerando plano para $ENVIRONMENT..."
terraform plan -var="env=$ENVIRONMENT" -out=tfplan

echo "🚀 Aplicando plano para $ENVIRONMENT..."
terraform apply -input=false tfplan

echo "✅ Deploy do ambiente '$ENVIRONMENT' finalizado com sucesso!"
