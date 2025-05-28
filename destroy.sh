#!/bin/bash

echo "⚠️ Destruindo infraestrutura com Terraform..."

cd terraform

terraform destroy -auto-approve

echo "✅ Infraestrutura destruída com sucesso!"
