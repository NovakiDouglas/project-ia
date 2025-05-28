
# Meu Projeto IA

## ✅ Descrição

API simples com Flask que permite realizar predições utilizando modelos de IA versionados.  
O modelo pode ser atualizado facilmente adicionando novas versões à pasta `models/`.  

Suporte a múltiplas versões com parâmetro `version`.  
Exemplo: `/predict?id=123&version=v1`

---

## ✅ Como rodar local com Docker

1. **Build e execução**:

```bash
docker-compose up --build
```

2. **Acessar a API**:  

- Versão padrão (v1):  
  [http://localhost:5000/predict?id=123](http://localhost:5000/predict?id=123)

- Versão específica:  
  [http://localhost:5000/predict?id=123&version=v2](http://localhost:5000/predict?id=123&version=v2)

---

## ✅ Como rodar com Makefile (opcional)

1. **Buildar a imagem**:

```bash
make build
```

2. **Subir o container**:

```bash
make up
```

3. **Testar a API**:

```bash
make test
```

4. **Parar a aplicação**:

```bash
make down
```

---

## ✅ Estrutura de modelos

Os modelos devem estar organizados da seguinte forma:

```
models/
├── v1/
│   └── modelo.pkl
├── v2/
│   └── modelo.pkl
└── ...
```

- A versão padrão é **`v1`**.  
- Para carregar outra versão, use o parâmetro: `?version=v2`.

---

## ✅ Como provisionar na AWS

1. **Configure AWS CLI**:

```bash
aws configure
```

2. **Execute o Terraform**:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

3. **Veja o IP público no output** e acesse:  

```bash
http://IP_PUBLICO:5000/predict?id=123
```

Ou com versão:

```bash
http://IP_PUBLICO:5000/predict?id=123&version=v2
```

---

## ✅ Deploy automático

O provisionamento com **Terraform** já executa:

- Instalação do Docker e Docker Compose
- Clonagem do repositório
- Execução automática da aplicação via `docker-compose up -d`

---

## ✅ Como atualizar o modelo

1. Adicione a nova versão na pasta `models/`  
2. Commit e push para o repositório  
3. Execute:

```bash
make deploy
```

ou

```bash
cd terraform && terraform apply
```

✅ O modelo será carregado automaticamente na nova versão da aplicação.

---

## ✅ Tecnologias utilizadas

- Python 3.9
- Flask
- Docker
- Docker Compose
- Terraform
- AWS EC2

---

## ✅ Autor

- **Novaki**
- Contato: [novakiart@gmail.com](mailto:novakiart@gmail.com)
