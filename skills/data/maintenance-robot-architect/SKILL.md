---
name: Maintenance Robot Architect
description: Especialista en la actualización del sistema de auto-migración "Maintenance Robot" en orchestrator_service/main.py.
---

# Maintenance Robot Architect

Este Skill instruye al agente sobre cómo modificar, extender y mantener el sistema de inicialización de base de datos automatizado, conocido como "Maintenance Robot". Dicho sistema reside en la lista `migration_steps` dentro de `orchestrator_service/main.py`.

## Propósito

Asegurar que **CADA NUEVO DESPLIEGUE** en un entorno limpio (Zero-Config / Self-Hosted) nazca completamente funcional, con:
1.  Todas las tablas necesarias creadas.
2.  Datos semilla ("seed data") críticos insertados.
3.  Columnas nuevas agregadas a tablas existentes.

Esto elimina la necesidad de ejecutar scripts SQL manuales o depender de carpetas `db/init` que a veces no se montan correctamente en orquestadores como EasyPanel.

## Reglas de Oro (Protocolo Omega)

1.  **Idempotencia Absoluta**:
    *   Todo create table debe ser `CREATE TABLE IF NOT EXISTS`.
    *   Toda inserción de datos semilla debe tener `ON CONFLICT DO NOTHING` (o `DO UPDATE` si es configuración mutable).
    *   Toda alteración de columna debe usar bloques `DO $$ ... EXCEPTION ... END $$` para capturar errores si la columna ya existe.

2.  **Atomicidad por Paso**:
    *   Cada elemento de la lista `migration_steps` se ejecuta como una transacción individual implícita.
    *   Si un paso falla, se loguea el error pero el sistema intenta continuar (Soft Fail), a menos que sea una tabla crítica que impida el arranque.

3.  **No Borrar Pasos Antiguos**:
    *   La historia de migración se mantiene secuencial. Agrega nuevos pasos al final de la lista.
    *   Solo modifica pasos existentes si detectas un error grave de sintaxis que rompe el arranque.

## Guía de Implementación

### 1. Ubicación
El código vive en `orchestrator_service/main.py`. Busca la variable:
```python
migration_steps = [
    # ... pasos previos ...
]
```

### 2. Formato de Nuevo Paso
Para agregar una nueva tabla o semilla, añade un string triple-comilla al final de la lista:

```python
    # N. Nombre Descriptivo (vX.X Update)
    """
    -- Tu SQL Aquí
    CREATE TABLE IF NOT EXISTS nueva_tabla (...);
    
    INSERT INTO nueva_tabla (...) VALUES (...) ON CONFLICT DO NOTHING;
    """
```

### 3. Manejo de Seeds Complejos
Si necesitas lógica condicional (ej: "Solo insertar X si existe Y"), usa bloques PL/pgSQL anónimos:

```sql
DO $$
DECLARE
    parent_id INT;
BEGIN
    SELECT id INTO parent_id FROM parent_table WHERE name = 'target';
    
    IF parent_id IS NOT NULL THEN
        INSERT INTO child_table (parent_id, ...) VALUES (parent_id, ...);
    END IF;
END $$;
```

## Casos de Uso Comunes

-   **Nuevas Credenciales**: Si el sistema ahora soporta un nuevo proveedor (ej: TikTok), debes agregar el `INSERT` en `oauth_providers` y sus tipos en `credential_types` aquí.
-   **Nuevas Columnas**: Si el modelo SQLAlchemy agrega un campo, agrega el `ALTER TABLE` aquí para que las BD existentes se actualicen al reiniciar.
-   **Configuración Global**: Si cambias políticas globales (ej: Prompt del Sistema por defecto), actualiza el paso de `UPDATE tenants SET system_prompt_template = ...`.
