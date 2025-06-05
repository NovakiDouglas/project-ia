# ✅ Checklist Realista para Evolução do Projeto

## 1. Segurança (essencial)
- [x] Proteção por API Key (via Secrets Manager)
- [ ] Adicionar HTTPS com certificado (SSL)
- [ ] Habilitar CORS apenas para origens confiáveis

## 2. Documentação
- [ ] Escrever README com exemplos de uso da API
- [ ] Criar Swagger/OpenAPI (pode ser com Flask-RESTX ou migrar p/ FastAPI depois)

## 3. Monitoramento e Confiabilidade
- [ ] Adicionar `/health` endpoint para health checks
- [ ] Configurar CloudWatch Logs (opcional)

## 4. Deploy e Infra
- [x] Docker Compose estruturado (multi-container)
- [x] Elastic IP
- [x] Deploy com Terraform automatizado (dev e prod)
- [x] EC2 com IAM para Secrets
- [ ] Melhorar logging com timestamps e erros claros

## 5. Testes
- [x] Script local de testes automatizados (`test_predict.py`)
- [ ] Testes unitários por endpoint com dados mockados

## 6. Organização e Manutenção
- [x] Separação clara entre modelos (`model-plug/`, `model-lampada/`)
- [x] Versionamento de modelos por subpasta `/1`, `/2`
- [ ] Criar script para empacotar novos modelos (`model_upload.sh`)

## 7. Futuro (pode ser adiado)
- [ ] Migrar para ECS Fargate (quando escalar horizontalmente)
- [ ] Habilitar ALB + Auto Scaling Group
- [ ] Considerar FastAPI para performance e documentação embutida
