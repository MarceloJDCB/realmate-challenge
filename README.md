# Webhook Handler API

API para processamento de webhooks de um sistema de atendimento WhatsApp, construída com Django e Django Rest Framework.

## 🚀 Tecnologias

- Python 3.10+
- Django / Django Rest Framework
- Celery (processamento assíncrono)
- Redis (message broker)
- PostgreSQL
- Docker e Docker Compose

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Poetry (opcional, para desenvolvimento local)
- Make (opcional, para usar os comandos do Makefile)

## 🔧 Instalação e Execução

### Com Docker (Recomendado)

1. Clone o repositório:
```bash
git clone https://github.com/MarceloJDCB/realmate-challenge.git
cd realmate-challenge
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

3. Inicie os containers:
```bash
docker-compose up -d
```

4. Execute as migrações:
```bash
docker-compose exec web python manage.py migrate
```

A API estará disponível em: http://localhost:8000

### Desenvolvimento Local (com Poetry)

1. Instale as dependências:
```bash
poetry install
```

2. Configure o ambiente virtual:
```bash
poetry shell
```

3. Execute as migrações:
```bash
python manage.py migrate
```

4. Inicie o servidor:
```bash
python manage.py runserver
```

## 📡 Endpoints

### Webhook
- POST `/webhook/`
  - Recebe eventos de conversas e mensagens
  - Retorna 202 Accepted com ID da tarefa
- GET `/webhook/task_status/{task_id}/`
  - Consulta o estado de processamento de uma tarefa específica
  - Retorna o status atual da tarefa (PENDING, SUCCESS, FAILURE, etc)
  - Útil para acompanhar o processamento assíncrono dos webhooks

### Conversas
- GET `/conversations/{id}/`
  - Retorna detalhes de uma conversa específica com suas mensagens
  - Estado pode ser OPEN ou CLOSED

## 🧪 Testes

### Executando os testes com Pytest
```bash
# Com Docker
docker-compose exec web pytest

# Local
pytest

# Com cobertura de testes
pytest --cov=apps

# Com relatório detalhado
pytest -v --cov=apps --cov-report=term-missing
```

## 🛠 Comandos Make

O projeto inclui diversos comandos úteis via Makefile para facilitar o desenvolvimento:

### Inicialização
- `make init` - Inicializa o projeto (copia .env, build docker e migrações)
- `make raw_init` - Inicialização completa com criação de superuser
- `make install` - Instala dependências via Poetry nos containers

### Gestão de Containers
- `make up` - Inicia os containers
- `make down` - Para e remove os containers
- `make rebuild` - Reconstrói e reinicia os containers
- `make restart` - Reinicia os containers
- `make stop` - Para os containers

### Banco de Dados
- `make migrate` - Aplica as migrações
- `make makemigrations` - Cria novas migrações
- `make drop_db` - Remove o volume do banco de dados
- `make createsuperuser` - Cria um superusuário

### Desenvolvimento
- `make test` - Executa os testes
- `make lint` - Executa verificação de código com flake8
- `make project-clean` - Limpa todos os recursos Docker do projeto

## 🔐 Autenticação e Exemplos de Uso

### Ambientes de Desenvolvimento
Em ambientes locais e de desenvolvimento, a API utiliza autenticação simples via header `Authorization` usando a variável de ambiente `WEBHOOK_API_KEY`. 
Em produção, é utilizada autenticação HMAC usando `WEBHOOK_SECRET` para maior segurança.

### Variáveis de Ambiente
```
WEBHOOK_API_KEY=debug    # Chave para autenticação em ambiente local/dev
WEBHOOK_SECRET=debug     # Chave secreta para HMAC em produção
```

### Exemplos de Requisições

#### 1. Criando uma Nova Conversa
```bash
curl -X POST http://localhost:8000/webhooks/webhook/ \
  -H "Content-Type: application/json" \
  -H "Authorization: debug" \
  -d '{
    "type": "NEW_CONVERSATION",
    "timestamp": "2025-02-21T10:20:41.349308",
    "data": {
        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
  }'

# Resposta esperada (202 Accepted):
# {
#   "task_id": "8f9d4e37-dd95-4018-a3c1-d99d2774e383"
# }
```

#### 2. Enviando uma Nova Mensagem
```bash
curl -X POST http://localhost:8000/webhooks/webhook/ \
  -H "Content-Type: application/json" \
  -H "Authorization: debug" \
  -d '{
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:42.349308",
    "data": {
        "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
        "direction": "RECEIVED",
        "content": "Olá, tudo bem?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
  }'
```

#### 3. Verificando Status da Tarefa
```bash
curl -X GET http://localhost:8000/webhooks/task_status/8f9d4e37-dd95-4018-a3c1-d99d2774e383/ \
  -H "Authorization: debug"

# Resposta esperada:
# {
#   "status": "SUCCESS"
# }
```

#### 4. Consultando uma Conversa
```bash
curl -X GET http://localhost:8000/conversations/6a41b347-8d80-4ce9-84ba-7af66f369f6a/ \
  -H "Authorization: debug"

# Resposta esperada:
# {
#   "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a",
#   "state": "OPEN",
#   "messages": [
#     {
#       "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
#       "direction": "RECEIVED",
#       "content": "Olá, tudo bem?",
#       "timestamp": "2025-02-21T10:20:42.349308"
#     }
#   ]
# }
```

#### 5. Fechando uma Conversa
```bash
curl -X POST http://localhost:8000/webhooks/webhook/ \
  -H "Content-Type: application/json" \
  -H "Authorization: debug" \
  -d '{
    "type": "CLOSE_CONVERSATION",
    "timestamp": "2025-02-21T10:20:45.349308",
    "data": {
        "id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
  }'
```

### Autenticação em Produção (HMAC)
Em ambiente de produção, a autenticação é feita via HMAC usando a variável `WEBHOOK_SECRET`:

```python
# Exemplo de geração do HMAC (Python)
import hmac
import hashlib
import json
import os

# Dados do webhook
webhook_data = {
    "type": "NEW_MESSAGE",
    "timestamp": "2025-02-21T10:20:42.349308",
    "data": {
        "id": "49108c71-4dca-4af3-9f32-61bc745926e2",
        "direction": "RECEIVED",
        "content": "Olá, tudo bem?",
        "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
    }
}

# Converter para string JSON
payload = json.dumps(webhook_data)
webhook_secret = os.getenv("WEBHOOK_SECRET", "debug")

# Gerar assinatura HMAC
signature = hmac.new(
    webhook_secret.encode(),
    payload.encode(),
    hashlib.sha256
).hexdigest()

# Exemplo de requisição com HMAC
curl -X POST http://api.exemplo.com/webhooks/webhook/ \
  -H "Content-Type: application/json" \
  -H "Authorization: HMAC ${signature}" \
  -d '${payload}'
```
