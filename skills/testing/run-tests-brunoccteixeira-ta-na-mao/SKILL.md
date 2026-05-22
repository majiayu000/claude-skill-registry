---
name: run-tests
description: Executar testes com workflow TDD
---

## Comandos Rapidos
```bash
# Backend
pytest backend/tests/                           # Todos os testes
pytest backend/tests/ -v --cov=app              # Com coverage
pytest backend/tests/test_agent.py -v           # Arquivo especifico
pytest backend/tests/ -k "test_consulta"        # Por nome

# Frontend
cd frontend && npm test                         # Todos os testes
cd frontend && npm test -- --watch              # Watch mode
cd frontend && npm test -- ChatMessage.test.tsx # Arquivo especifico
```

## Workflow TDD (Red -> Green -> Refactor)

### 1. RED: Escrever teste que falha
```python
# backend/tests/test_nova_feature.py
import pytest
from app.services.nova_feature import processar

@pytest.mark.asyncio
async def test_processar_retorna_resultado_esperado():
    resultado = await processar("entrada")
    assert resultado == "saida esperada"
```

### 2. GREEN: Implementar minimo para passar
```python
# backend/app/services/nova_feature.py
async def processar(entrada: str) -> str:
    return "saida esperada"
```

### 3. REFACTOR: Melhorar mantendo testes verdes
```bash
pytest backend/tests/test_nova_feature.py -v  # Verificar que ainda passa
```

## Fixtures Uteis (pytest)
```python
@pytest.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
def mock_cpf():
    return "12345678901"

@pytest.fixture
def mock_beneficio():
    return {"programa": "Bolsa Familia", "valor": 600.0}
```

## Watch Mode
```bash
# Backend (usando pytest-watch)
ptw backend/tests/ -- -v

# Frontend
cd frontend && npm test -- --watch
```

## Arquivos de Configuracao
- `backend/pytest.ini` - Configuracao pytest
- `backend/.coveragerc` - Configuracao coverage
- `frontend/vitest.config.ts` - Configuracao Vitest

## Coverage Report
```bash
pytest backend/tests/ --cov=app --cov-report=html
open backend/htmlcov/index.html
```
