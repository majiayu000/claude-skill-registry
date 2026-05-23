---
name: añadir-servicio
description: Usar al integrar un nuevo servicio externo completo (config + cliente + endpoint + widget)
---

## Cuándo usar esta skill

- Al integrar un nuevo servicio externo de principio a fin
- Cuando se necesite añadir una API completa al dashboard
- Para crear integraciones tipo Home Assistant, Pi-hole, Mealie, etc.

## Contexto necesario antes de empezar

1. Documentación de la API del servicio a integrar
2. Credenciales necesarias (API key, token, usuario/password)
3. Endpoints disponibles y formato de respuesta
4. Qué datos mostrar en el dashboard

## Pasos

### 1. Añadir configuración en `config.py`

```python
# En clase Config
NUEVO_SERVICIO_URL = env_target(
    'NUEVO_SERVICIO_URL',
    default_local='http://servicio.local',
    default_nas='http://servicio:puerto'
)
NUEVO_SERVICIO_TOKEN = env_str('NUEVO_SERVICIO_TOKEN')
```

### 2. Documentar en `.env`

```bash
# Nuevo Servicio
NUEVO_SERVICIO_URL_LOCAL=http://servicio.local
NUEVO_SERVICIO_URL_NAS=http://servicio:8080
NUEVO_SERVICIO_TOKEN=tu_token_aqui
```

### 3. Crear cliente en `blueprints/nuevo_client.py`

Usar skill `@crear-cliente` para el patrón completo.

```python
"""Cliente para Nuevo Servicio API"""
import requests
from flask import current_app


class NuevoClient:
    def __init__(self, base_url, api_token=None, timeout=None):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.timeout = timeout or current_app.config.get('API_TIMEOUT', 15)
        self.headers = {'Authorization': f'Bearer {self.api_token}'} if api_token else {}
    
    def get_data(self):
        """Obtener datos principales"""
        try:
            url = f"{self.base_url}/api/endpoint"
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error NuevoClient: {e}")
            return {'error': str(e)}
```

### 4. Crear endpoint en `blueprints/main.py`

Usar skill `@crear-endpoint` para el patrón completo.

```python
from blueprints.nuevo_client import NuevoClient

@main_bp.route('/api/nuevo')
@cache.cached(timeout=300)
def api_nuevo():
    """Endpoint Nuevo Servicio"""
    url = current_app.config.get('NUEVO_SERVICIO_URL')
    token = current_app.config.get('NUEVO_SERVICIO_TOKEN')
    
    if not url:
        return jsonify({'error': 'NUEVO_SERVICIO_URL no configurado'}), 500
    
    try:
        client = NuevoClient(url, token)
        data = client.get_data()
        return jsonify(data)
    except Exception as e:
        current_app.logger.error(f"Error nuevo: {e}")
        return jsonify({'error': str(e)}), 500
```

### 5. Crear widget en dashboard

Usar skill `@crear-widget` para el patrón completo.

### 6. Documentar en README.md

Añadir sección describiendo:
- Variables de entorno necesarias
- Cómo obtener credenciales
- Qué datos muestra el widget

<patrones_criticos>
SIEMPRE:
- Usar `env_target()` para URLs que cambian entre local/NAS
- Crear cliente separado en `blueprints/[servicio]_client.py`
- Añadir `@cache.cached()` al endpoint
- Documentar variables en README

NUNCA:
- Hardcodear credenciales
- Poner lógica de negocio en el endpoint directamente
- Olvidar manejo de errores en cliente y endpoint

PREFERENTEMENTE:
- Timeout de cache según frecuencia de cambio
- Endpoint de debug para troubleshooting
- Logging detallado en cliente
</patrones_criticos>

## Orden de ejecución de skills

1. `@crear-cliente` → `blueprints/[servicio]_client.py`
2. `@crear-endpoint` → `blueprints/main.py`
3. `@crear-widget` → `dashboard.js` + `dashboard.html`
4. `@commit` → Commit con scope del servicio

## Checklist de validación

- [ ] Variables en `config.py` y `.env`
- [ ] Cliente creado con manejo de errores
- [ ] Endpoint con cache y validación de config
- [ ] Widget muestra datos correctamente
- [ ] README actualizado
- [ ] `ruff check .` pasa
- [ ] App arranca sin errores
