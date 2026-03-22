---
name: nueva-feature
description: Usar al implementar una funcionalidad nueva de principio a fin
---

## Cuándo usar esta skill

- Al implementar una nueva funcionalidad completa
- Cuando el usuario pida "añadir", "crear", "implementar" algo nuevo
- Para features que tocan múltiples capas (backend + frontend)

## Contexto necesario antes de empezar

1. Leer archivos relacionados con la feature
2. Identificar qué capas se verán afectadas
3. Verificar si hay patrones similares en el código existente
4. Comprobar dependencias necesarias

## Pasos

### 1. Planificación
- Definir scope exacto de la feature
- Listar archivos a crear/modificar
- Identificar dependencias externas (APIs, configs)

### 2. Backend (si aplica)
- Añadir configuración en `config.py` si es necesario
- Crear cliente en `blueprints/[servicio]_client.py` si hay API externa
- Añadir endpoint en `blueprints/main.py`
- Aplicar `@cache.cached()` si corresponde

### 3. Frontend (si aplica)
- Añadir método en `static/js/dashboard.js`
- Añadir estilos en `static/css/components.css` o `dashboard.css`
- Añadir HTML en template correspondiente

### 4. Validación
```bash
ruff check .
ruff format --check .
python -c "from app import app"
```

### 5. Test manual
- Verificar que la feature funciona en navegador
- Comprobar logs de Flask

### 6. Commit
- Usar skill `@commit` para generar mensaje

<patrones_criticos>
SIEMPRE:
- Seguir patrones existentes en el código
- Añadir logging con `current_app.logger`
- Documentar nuevas variables de entorno en README

NUNCA:
- Instalar dependencias sin preguntar
- Hardcodear valores que deberían ir en config
- Crear archivos fuera de la estructura existente

PREFERENTEMENTE:
- Reutilizar componentes CSS existentes
- Usar `utils.fetchJSON()` en frontend
- Cache para endpoints de lectura
</patrones_criticos>

## Sobre versiones y documentación

Al implementar esta skill, si usas APIs de Flask, requests, o Flask-Caching:
- Verifica la versión en `requirements.txt`
- Consulta el código existente para ver cómo se usa
- Si hay dudas sobre una API, indica qué versión asumes

## Checklist de validación

- [ ] `ruff check .` pasa sin errores
- [ ] `ruff format --check .` pasa
- [ ] La app arranca sin errores
- [ ] La feature funciona en navegador
- [ ] No se han tocado archivos fuera del scope
- [ ] Variables de entorno documentadas si las hay
