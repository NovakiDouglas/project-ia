
# Meu Projeto IA

## Como rodar local com Docker

```bash
docker-compose up --build
```

Acesse: [http://localhost:5000/predict?id=123](http://localhost:5000/predict?id=123)

## Como provisionar na AWS

1. Configure AWS CLI:

```bash
aws configure
```

2. Execute o Terraform:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

3. Veja o IP público no output e acesse:

```bash
http://IP_PUBLICO:5000/predict?id=123
```
