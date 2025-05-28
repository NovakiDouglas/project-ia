#!/bin/bash

set -e  # Para execução em caso de erro

echo "🚀 Iniciando deploy com Terraform..."

if [ ! -d terraform ]; then
  echo "❌ Diretório 'terraform' não encontrado."
  exit 1
fi

cd terraform

echo "🔍 Inicializando Terraform..."
terraform init

echo "📐 Gerando plano..."
terraform plan -out=tfplan

echo "🚀 Aplicando plano..."
terraform apply tfplan

echo "✅ Deploy finalizado com sucesso!"
