---
name: varlock
description: Gerenciamento de secrets e .env
---

Gerenciamento seguro de variaveis de ambiente e secrets.

## Arquivos de Configuracao

```
backend/
├── .env              # Valores reais (NAO COMMITAR)
├── .env.example      # Template (commitar)
└── .env.test         # Valores para testes (opcional)
```

## Estrutura do .env.example

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0

# APIs Externas
GOOGLE_MAPS_API_KEY=
BRASIL_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=

# Agente IA
GEMINI_API_KEY=
OPENAI_API_KEY=

# Aplicacao
SECRET_KEY=
DEBUG=false
LOG_LEVEL=INFO
```

## Regras de Seguranca

### 1. Nunca Commitar Secrets
```bash
# .gitignore deve conter:
.env
.env.local
*.key
*.pem
credentials.json
```

### 2. Verificar Antes de Commit
```bash
# Verificar se .env esta sendo tracked
git status | grep .env

# Se aparecer, remover do tracking
git rm --cached .env
```

### 3. Rotacionar Secrets Expostos
Se um secret foi commitado:
1. Revogar imediatamente (gerar novo)
2. Atualizar em todos os ambientes
3. Verificar logs de uso suspeito

## Carregar Variaveis

### Python (backend)
```python
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")
```

### Docker Compose
```yaml
services:
  backend:
    env_file:
      - .env
```

### Linha de Comando
```bash
# Carregar e executar
source .env && python script.py

# Ou com export
export $(cat .env | xargs) && python script.py
```

## Validacao de Variaveis

```python
# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    GEMINI_API_KEY: str
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()  # Valida na inicializacao
```

## Checklist de Seguranca

- [ ] `.env` esta no `.gitignore`?
- [ ] `.env.example` tem todas as variaveis (sem valores)?
- [ ] Secrets de producao diferentes de dev?
- [ ] API keys tem escopo minimo necessario?
- [ ] Secrets rotacionados periodicamente?

## Secrets por Ambiente

| Variavel | Dev | Prod |
|----------|-----|------|
| DEBUG | true | false |
| DATABASE_URL | localhost | RDS/Cloud |
| LOG_LEVEL | DEBUG | INFO |
| API_KEY | Key de dev | Key de prod |

## Comandos Uteis

```bash
# Verificar variaveis carregadas
env | grep -E "DATABASE|REDIS|API"

# Validar .env existe
test -f .env && echo "OK" || echo "FALTA .env"

# Copiar template
cp .env.example .env
```
