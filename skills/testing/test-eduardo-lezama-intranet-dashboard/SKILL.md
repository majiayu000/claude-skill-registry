---
name: test
description: Usar al crear o modificar tests con pytest
---

## Cuándo usar esta skill

- Al crear tests para código nuevo o existente
- Cuando se pida "testear", "añadir tests", "verificar"
- Después de arreglar un bug (test de regresión)

## Contexto necesario antes de empezar

1. Código a testear (leer y entender)
2. Comportamiento esperado
3. Casos edge a considerar
4. Dependencias externas a mockear

## Pasos

### 1. Verificar estructura de tests

Si no existe `tests/`, crear:
```bash
mkdir tests
touch tests/__init__.py
touch tests/conftest.py
```

### 2. Crear conftest.py (si no existe)

```python
# tests/conftest.py
import pytest
from app import create_app


@pytest.fixture
def app():
    """Crear app en modo testing"""
    app = create_app('development')
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Cliente de test Flask"""
    return app.test_client()
```

### 3. Crear archivo de test

Nombrar: `tests/test_[módulo].py`

```python
# tests/test_endpoints.py
def test_api_status_returns_ok(client):
    """GET /api/status debe retornar status ok"""
    response = client.get('/api/status')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
```

### 4. Mockear APIs externas

```python
from unittest.mock import patch, Mock

def test_energy_client_handles_error(client):
    """Endpoint debe manejar errores del cliente"""
    with patch('blueprints.main.EnergyClient') as mock:
        mock.return_value.get_energy_summary.side_effect = Exception("API down")
        
        response = client.get('/api/energy')
        
        assert response.status_code == 500
        assert 'error' in response.get_json()
```

### 5. Ejecutar tests

```bash
pytest tests/ -v              # Todos
pytest tests/test_app.py -v   # Un archivo
pytest -k "test_api" -v       # Por nombre
pytest -x                     # Parar en primer fallo
```

<patrones_criticos>
SIEMPRE:
- Un assert principal por test
- Nombres descriptivos: `test_[qué]_[condición]_[resultado]`
- Mockear APIs externas (nunca llamar servicios reales)
- Usar fixtures para setup repetitivo

NUNCA:
- Tests que dependen de servicios externos reales
- Tests que dependen del orden de ejecución
- Hardcodear datos que deberían ser fixtures

PREFERENTEMENTE:
- Tests pequeños y enfocados
- Cubrir casos de error además de happy path
- Documentar con docstring qué se está testeando
</patrones_criticos>

## Estructura de tests recomendada

```
tests/
├── __init__.py
├── conftest.py           # Fixtures compartidos
├── test_app.py           # Tests de la app Flask
├── test_endpoints.py     # Tests de endpoints API
├── test_energy_client.py # Tests del cliente Energy
├── test_mealie_client.py # Tests del cliente Mealie
└── test_pihole_client.py # Tests del cliente Pi-hole
```

## Checklist de validación

- [ ] Tests pasan: `pytest tests/ -v`
- [ ] Tests son independientes entre sí
- [ ] APIs externas mockeadas
- [ ] Casos de error cubiertos
- [ ] `ruff check tests/` pasa
