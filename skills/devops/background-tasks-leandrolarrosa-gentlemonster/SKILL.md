---
name: background-tasks
description: Manejo de tareas asíncronas con 'arq' (Redis) para escalar la ingesta y procesos pesados.
trigger: background OR async OR queue OR arq OR redis OR task
scope: backend
---

# Background Tasks (arq + Redis)

## Contexto

Para evitar bloquear el request HTTP durante procesos largos (ej. Procesamiento de IA, uploads pesados), usamos `arq` con Redis.
Esta skill fue generada siguiendo el [Protocolo de Adquisición de Conocimiento] usando `ask_context7.py arq`.

## Instalación

```bash
pip install arq redis
```

## Patrón de Implementación (FastAPI)

### 1. Configuración del Worker (`worker.py`)

Crea un archivo dedicado para definir los settings y las funciones del worker.

```python
import asyncio
from arq.connections import RedisSettings
from backend.core.config import settings

async def startup(ctx):
    print("🚀 Worker starting...")
    # Inicializar DB o AI clients aquí y guardarlos en ctx
    # ctx['db'] = ...

async def shutdown(ctx):
    print("🛑 Worker shutting down...")

async def process_ingestion(ctx, file_path: str, user_id: str):
    """
    Tarea pesada de ejemplo.
    """
    print(f"Processing ingestion for {user_id} at {file_path}")
    # Simular trabajo
    await asyncio.sleep(5)
    return "done"

class WorkerSettings:
    functions = [process_ingestion]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )
```

### 2. Encolar Trabajos (Desde un Router)

En tus routers de FastAPI, usa `create_pool` para conectar y encolar.

```python
from arq import create_pool
from arq.connections import RedisSettings

# ... En tu endpoint ...
@router.post("/ingest")
async def ingest_file(file: UploadFile):
    # 1. Guardar archivo temporalmente (o subir a storage rápido)
    # ...

    # 2. Encolar tarea
    redis = await create_pool(RedisSettings())
    await redis.enqueue_job('process_ingestion', file_path="tmp/file.jpg", user_id="123")

    return {"status": "queued", "msg": "Processing in background"}
```

## Best Practices (Context7 Findings)

1.  **Job Deferral:** Puedes programar tareas para el futuro usando `_defer_by` (timedelta) o `_defer_until` (datetime).
    ```python
    await redis.enqueue_job('task_name', _defer_by=timedelta(minutes=5))
    ```
2.  **Context Injection:** Usa `ctx` en las funciones del worker para compartir conexiones a DB/AI (evita crearlas en cada ejecución).
3.  **Error Handling:** `arq` reintenta fallos automáticamente si se configura `max_tries`.

## Referencia

- Generado con: `python scripts/ask_context7.py arq "how to use arq with fastapi"`
