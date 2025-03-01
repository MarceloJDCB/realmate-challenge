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
