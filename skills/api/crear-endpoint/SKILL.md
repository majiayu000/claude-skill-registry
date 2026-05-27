---
name: crear-endpoint
description: Usar al crear un nuevo endpoint API en blueprints/main.py
---

## Cuándo usar esta skill

- Al crear un nuevo endpoint `/api/[recurso]`
- Cuando se necesite exponer datos de un servicio externo
- Para añadir nuevas rutas al blueprint principal

## Contexto necesario antes de empezar

1. Leer `blueprints/main.py` para ver patrones existentes
2. Verificar si ya existe un cliente para el servicio
3. Comprobar configuración necesaria en `config.py`

## Pasos

### 1. Definir el endpoint
- Ruta: `/api/[recurso]`
- Método: GET (lectura), POST (crear), DELETE (eliminar)
- Respuesta: JSON

### 2. Añadir configuración (si es necesario)
```python
# En config.py, clase Config
NUEVO_SERVICIO_URL = env_target('NUEVO_SERVICIO_URL', 'http://local', 'http://docker')
NUEVO_SERVICIO_TOKEN = env_str('NUEVO_SERVICIO_TOKEN')
```

### 3. Crear cliente (si hay API externa)
- Usar skill `@crear-cliente`

### 4. Implementar endpoint en `blueprints/main.py`
```python
@main_bp.route('/api/nuevo')
@cache.cached(timeout=180)
def api_nuevo():
    """Descripción del endpoint"""
    try:
        url = current_app.config.get('NUEVO_SERVICIO_URL')
        token = current_app.config.get('NUEVO_SERVICIO_TOKEN')
        
        if not url:
            return jsonify({'error': 'NUEVO_SERVICIO_URL no configurado'}), 500
        
        client = NuevoClient(url, token)
        data = client.get_data()
        
        return jsonify(data)
        
    except Exception as e:
        current_app.logger.error(f"Error nuevo: {str(e)}")
        return jsonify({'error': str(e)}), 500
```

### 5. Validar
```bash
ruff check blueprints/main.py
python -c "from app import app"
```

<patrones_criticos>
SIEMPRE:
- Usar `@cache.cached()` para endpoints de lectura
- Validar configuración antes de usar
- Logging de errores con `current_app.logger.error()`
- Retornar JSON con estructura consistente

NUNCA:
- Endpoints sin manejo de errores
- Hardcodear URLs o tokens
- Usar `print()` en lugar de logger

PREFERENTEMENTE:
- Timeout de cache según frecuencia de cambio del dato
- Docstring describiendo el endpoint
</patrones_criticos>

## Checklist de validación

- [ ] Endpoint responde correctamente
- [ ] Errores se manejan y loguean
- [ ] Cache configurado apropiadamente
- [ ] `ruff check .` pasa
- [ ] Documentado en README si es público
