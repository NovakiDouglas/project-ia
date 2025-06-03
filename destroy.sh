#!/bin/bash

set -e  # Encerra em caso de erro

# Ambiente alvo (dev por padrão)
ENVIRONMENT="${1:-dev}"

# Validação de ambiente permitido
if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "prod" ]]; then
  echo "❌ Ambiente inválido. Use: ./destroy.sh [dev|prod]"
  exit 1
fi

echo "⚠️ Destruindo infraestrutura do ambiente: $ENVIRONMENT"

# Entra na pasta terraform
if [ ! -d terraform ]; then
  echo "❌ Diretório 'terraform' não encontrado."
  exit 1
fi

cd terraform

echo "🔍 Selecionando workspace..."
terraform workspace select "$ENVIRONMENT" || {
  echo "❌ Workspace '$ENVIRONMENT' não encontrado."
  exit 1
}

echo "🔥 Destruindo recursos..."
terraform destroy -auto-approve -var="env=$ENVIRONMENT"

echo "✅ Infraestrutura do ambiente '$ENVIRONMENT' destruída com sucesso!"
