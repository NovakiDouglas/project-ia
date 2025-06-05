# Projeto IA - Predição com Modelos Plug e Lâmpada

## ✅ Descrição

API em Flask para realizar predições usando dois modelos distintos:

- Modelo **Plug** (consumo de dispositivos plugados)
- Modelo **Lâmpada** (consumo de iluminação)

Cada modelo é versionado e servido de forma independente via **TensorFlow Serving**.  
A API suporta requisições via POST e permite indicar qual versão do modelo utilizar.  

---

## ✅ Endpoints

- `POST /predict/plug`  
- `POST /predict/lampada`  

### Corpo da requisição:
```json
{
  "instances": [
    [2, 123.4, 110.0, 15.2],
    [5, 130.0, 129.0, 8.3]
  ],
  "version": "2"  // opcional. Se não enviado, utiliza "latest"
}
```


[12,12,12,12,12,12,12,12,12,12,12,12] => [12,12,12,12,12,12,12]

---

## ✅ Como rodar localmente com Docker

```bash
docker-compose up --build
```

Acesse em:

- [http://localhost:5000/predict/plug](http://localhost:5000/predict/plug)
- [http://localhost:5000/predict/lampada](http://localhost:5000/predict/lampada)

---

## ✅ Estrutura de Pastas para os Modelos

Cada modelo fica em sua pasta, com subpastas numeradas:

```
model-plug/
└── 2/
    ├── saved_model.pb
    └── variables/

model-lampada/
└── 1/
    ├── saved_model.pb
    └── variables/
```

> ⚠️ O TensorFlow Serving exige que cada versão fique dentro de uma pasta numerada (ex: `/1/`, `/2/`).

---

## ✅ Como testar a API

```bash
python app/src/test_predict.py
```

Esse script testa:
- Versão mais recente de cada modelo
- Versões específicas válidas e inválidas
- Formato de resposta e tratamento de erro

---

## ✅ Provisionar na AWS com Terraform

1. Configure sua AWS:

```bash
aws configure
```

2. Execute o provisionamento:

```bash
cd terraform
terraform init
terraform apply
```

3. Acesse no IP público:

```bash
http://<IP_PUBLICO>:5000/predict/plug
```

---

## ✅ Atualizar um modelo

1. Adicione a nova versão dentro da pasta correta (`model-plug/3/`, `model-lampada/2/` etc)
2. Faça `commit` e `push` para o repositório
3. Rode novamente `docker-compose up -d --build` ou `terraform apply`

> ✅ A versão nova será carregada automaticamente pelo TensorFlow Serving

---

## ✅ Tecnologias Utilizadas

- Python 3.9
- Flask
- Docker / Docker Compose
- TensorFlow Serving
- Terraform
- AWS EC2

---

## ✅ Autor

**Novaki**  
📧 [novakiart@gmail.com](mailto:novakiart@gmail.com)