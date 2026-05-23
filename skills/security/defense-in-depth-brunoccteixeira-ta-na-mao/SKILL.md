---
name: defense-in-depth
description: Checklist de seguranca multi-camada
---

Checklist de seguranca para codigo que lida com dados sensiveis (CPF, beneficios).

## Camada 1: Validacao de Entrada

### CPF
```python
import re

def validar_cpf(cpf: str) -> bool:
    # Remove caracteres nao numericos
    cpf = re.sub(r'[^0-9]', '', cpf)

    # Verifica tamanho
    if len(cpf) != 11:
        return False

    # Verifica se nao sao todos iguais
    if cpf == cpf[0] * 11:
        return False

    # Validacao dos digitos verificadores
    # ... implementar algoritmo
    return True
```

### Sanitizacao
```python
from html import escape

def sanitizar_input(texto: str) -> str:
    # Remove HTML/scripts
    texto = escape(texto)
    # Limita tamanho
    texto = texto[:1000]
    return texto
```

## Camada 2: Autenticacao & Autorizacao

### Verificar Sessao
```python
async def verificar_sessao(session_id: str) -> bool:
    session = await redis.get(f"session:{session_id}")
    return session is not None
```

### Rate Limiting
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/v1/beneficios")
@limiter.limit("10/minute")
async def consultar_beneficios():
    pass
```

## Camada 3: Dados em Transito

### HTTPS Obrigatorio
```python
# Em producao, forcar HTTPS
if not request.url.scheme == "https":
    raise HTTPException(status_code=400)
```

### Headers de Seguranca
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tanamao.gov.br"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## Camada 4: Dados em Repouso

### Nao Logar Dados Sensiveis
```python
# ERRADO
logger.info(f"Consultando CPF: {cpf}")

# CERTO
logger.info(f"Consultando CPF: ***{cpf[-4:]}")
```

### Variaveis de Ambiente
```bash
# Nunca commitar .env
# Usar .env.example como template
DATABASE_URL=
REDIS_URL=
API_KEY=
```

## Camada 5: Monitoramento

### Alertas de Seguranca
```python
# Detectar tentativas suspeitas
if tentativas_falhas > 5:
    logger.warning(f"Multiplas falhas de autenticacao: {ip}")
    await notificar_admin(ip)
```

## Checklist de Revisao de Codigo

| Item | Verificar |
|------|-----------|
| CPF | Validacao e mascaramento em logs |
| SQL | Queries parametrizadas (SQLAlchemy) |
| Inputs | Sanitizacao de texto do usuario |
| Sessoes | Expiracao e invalidacao |
| Senhas | Nunca em texto plano |
| APIs | Rate limiting configurado |
| Logs | Sem dados sensiveis |
| .env | Nao commitado |

## Dados Sensiveis no Projeto

- CPF
- NIS (Numero de Identificacao Social)
- Valores de beneficios
- Enderecos
- Telefones
- Informacoes de saude (laudos BPC)
