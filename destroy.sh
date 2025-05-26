#!/bin/bash

echo "🚀 Iniciando deploy com Terraform..."

cd terraform

terraform init
terraform plan
terraform apply -auto-approve

echo "✅ Deploy finalizado!"

