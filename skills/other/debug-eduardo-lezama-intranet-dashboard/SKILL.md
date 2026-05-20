---
name: debug
description: Usar al investigar un bug o error en la aplicación
---

## Cuándo usar esta skill

- Cuando hay un error o comportamiento inesperado
- Al investigar logs de error
- Para diagnosticar problemas de integración con servicios externos

## Contexto necesario antes de empezar

1. Mensaje de error exacto (si existe)
2. Pasos para reproducir el problema
3. Logs relevantes de Flask
4. Qué funcionaba antes (si aplica)

## Pasos

### 1. Reproducir el problema
- Verificar que el error es reproducible
- Anotar condiciones exactas

### 2. Localizar el origen
- Revisar logs de Flask (`current_app.logger`)
- Identificar archivo y línea del error
- Verificar stack trace completo

### 3. Analizar el código
- Leer el código involucrado
- Verificar flujo de datos
- Comprobar configuración relacionada

### 4. Hipótesis y verificación
- Formular hipótesis del problema
- Añadir logging temporal si es necesario:
  ```python
  current_app.logger.debug(f"DEBUG: variable={variable}")
  ```
- Verificar hipótesis

### 5. Implementar fix
- Aplicar corrección mínima
- Verificar que resuelve el problema
- Verificar que no rompe otra cosa

### 6. Limpiar
- Eliminar logging temporal de debug
- Ejecutar validaciones

```bash
ruff check .
python -c "from app import app"
```

<patrones_criticos>
SIEMPRE:
- Reproducir antes de arreglar
- Entender la causa raíz
- Verificar el fix
- Documentar si el bug era sutil

NUNCA:
- Arreglar síntomas sin entender causa
- Dejar logging de debug en producción
- Asumir sin verificar

PREFERENTEMENTE:
- Añadir test que capture el bug
- Fix mínimo y enfocado
- Commit separado para el fix
</patrones_criticos>

## Herramientas de debug disponibles

### Flask logging
```python
current_app.logger.debug("mensaje debug")
current_app.logger.info("mensaje info")
current_app.logger.error(f"Error: {e}")
```

### Endpoints de debug existentes
- `/api/mealie/debug` - Debug de Mealie
- `/api/settleup/debug-transactions` - Debug de Settle Up

### Variables de entorno
- `FLASK_DEBUG=True` - Modo debug activo

## Checklist de validación

- [ ] Bug reproducido y entendido
- [ ] Causa raíz identificada
- [ ] Fix implementado y verificado
- [ ] No hay logging de debug residual
- [ ] `ruff check .` pasa
- [ ] La app arranca correctamente
