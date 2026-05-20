---
name: crear-cliente
description: Usar al crear un cliente para consumir una API externa (Home Assistant, Pi-hole, etc.)
---

## Cuándo usar esta skill

- Al integrar un nuevo servicio externo
- Cuando se necesite un cliente HTTP reutilizable
- Para encapsular lógica de autenticación de APIs

## Contexto necesario antes de empezar

1. Leer clientes existentes en `blueprints/` para ver patrones
2. Documentación de la API externa a consumir
3. Tipo de autenticación (Bearer token, API key, SID, etc.)

## Pasos

### 1. Crear archivo `blueprints/[servicio]_client.py`

```python
"""
Cliente para [Servicio] API
"""
import requests
from flask import current_app


class ServicioClient:
    """Cliente para API de [Servicio]"""
    
    def __init__(self, base_url, api_token=None, timeout=None):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.timeout = timeout or current_app.config.get('API_TIMEOUT', 15)
        self.headers = self._build_headers()
    
    def _build_headers(self):
        """Construir headers de autenticación"""
        headers = {'Content-Type': 'application/json'}
        if self.api_token:
            headers['Authorization'] = f'Bearer {self.api_token}'
        return headers
    
    def get_data(self):
        """Obtener datos principales"""
        try:
            url = f"{self.base_url}/api/endpoint"
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error ServicioClient: {e}")
            return {'error': str(e)}
```

### 2. Añadir configuración en `config.py`

```python
# En clase Config
SERVICIO_URL = env_target('SERVICIO_URL', 'http://local', 'http://docker')
SERVICIO_TOKEN = env_str('SERVICIO_TOKEN')
```

### 3. Documentar en `.env` y README

### 4. Importar en endpoint

```python
from blueprints.servicio_client import ServicioClient
```

<patrones_criticos>
SIEMPRE:
- Usar `requests.Session()` si hay múltiples llamadas
- Manejar timeouts explícitamente
- Logging de errores
- Retornar dict con 'error' key en caso de fallo

NUNCA:
- Hardcodear URLs o tokens
- Ignorar excepciones silenciosamente
- Usar `print()` para debug

PREFERENTEMENTE:
- Métodos pequeños y específicos
- Docstrings en clase y métodos públicos
- Type hints si es posible
</patrones_criticos>

## Ejemplos reales del proyecto

Ver `blueprints/energy_client.py`, `blueprints/mealie_client.py`, `blueprints/pihole_auth.py`

## Checklist de validación

- [ ] Cliente maneja errores gracefully
- [ ] Timeouts configurados
- [ ] Logging de errores implementado
- [ ] `ruff check .` pasa
- [ ] Variables de entorno documentadas
