---
name: root-cause-tracing
description: Rastrear origem de bugs
---

Metodologia para encontrar a causa raiz de bugs em sistemas async.

## Processo de 5 Passos

### 1. OBSERVAR: Coletar Sintomas
```bash
# O que acontece?
# - Qual o erro exato?
# - Quando acontece?
# - E consistente ou intermitente?

# Coletar logs
docker compose logs backend 2>&1 | tail -100
```

### 2. FORMULAR: Hipoteses Ordenadas
```
Listar possiveis causas por probabilidade:
1. [Mais provavel] Timeout de conexao com API externa
2. [Provavel] Dados invalidos na entrada
3. [Menos provavel] Race condition no async
```

### 3. ISOLAR: Testar Hipoteses
```python
# Criar script de teste isolado
# backend/scripts/debug_issue.py

import asyncio
from app.services.suspeito import funcao_suspeita

async def main():
    # Testar com dados conhecidos
    resultado = await funcao_suspeita("entrada_teste")
    print(f"Resultado: {resultado}")

asyncio.run(main())
```

### 4. RASTREAR: Seguir o Fluxo
```
Fluxo tipico no Ta na Mao:

Request HTTP
    |
Router (app/routers/)
    |
Agent (app/agent/agent.py)
    |
Tool (app/agent/tools/)
    |
Service (app/services/)
    |
Database/API Externa
```

### 5. CONFIRMAR: Validar Causa Raiz
```bash
# Reproduzir com fix aplicado
pytest backend/tests/test_bug_fix.py -v

# Verificar que nao quebrou outras coisas
pytest backend/tests/ -v
```

## Ferramentas de Debug

### Logs Estruturados
```python
import logging
logger = logging.getLogger(__name__)

async def funcao_suspeita(entrada):
    logger.debug(f"Entrada: {entrada}")
    # ... processamento
    logger.debug(f"Saida: {resultado}")
    return resultado
```

### Breakpoints com pdb
```python
import pdb; pdb.set_trace()
# ou em async:
import asyncio
# breakpoint() funciona em Python 3.7+
```

### Trace de Chamadas
```python
import traceback
try:
    resultado = await funcao_suspeita()
except Exception as e:
    traceback.print_exc()
    raise
```

## Padroes Comuns de Bugs Async

| Sintoma | Causa Provavel | Solucao |
|---------|----------------|---------|
| Timeout | await faltando | Adicionar await |
| Dados inconsistentes | Race condition | Usar lock/semaphore |
| Conexao recusada | Pool esgotado | Verificar pool size |
| Resultado None | Excecao silenciosa | Adicionar try/except |
| Memoria alta | Coroutines nao finalizadas | Verificar gather/wait |

## Checklist de Investigacao

- [ ] Erro aparece nos logs?
- [ ] Consigo reproduzir localmente?
- [ ] Acontece com todos os inputs?
- [ ] Qual commit introduziu o bug?
- [ ] Testes existentes cobrem esse caso?
