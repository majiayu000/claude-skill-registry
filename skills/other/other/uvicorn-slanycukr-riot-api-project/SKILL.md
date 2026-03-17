---
name: uvicorn
description: ASGI server for Python web applications - Fast, production-ready server for async frameworks
when_to_use: |
  - Running FastAPI, Starlette, Django Channels, or other ASGI applications
  - Development servers with hot reload
  - Production deployment with multiple workers
  - WebSocket applications
  - Async Python web services
---

# Uvicorn Skill Guide

Uvicorn is a lightning-fast ASGI server implementation, using uvloop and httptools. It's the go-to server for modern Python async web frameworks.

## Quick Start

### Basic Usage

```bash
# Run ASGI app
uvicorn main:app

# With host/port
uvicorn main:app --host 0.0.0.0 --port 8000

# Development with auto-reload
uvicorn main:app --reload
```

## Common Patterns

### 1. Simple ASGI Application

```python
# main.py
async def app(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [(b'content-type', b'text/plain')],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, World!',
    })
```

### 2. FastAPI Application

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

```bash
uvicorn main:app --reload
```

### 3. Application Factory Pattern

```python
# main.py
from fastapi import FastAPI

def create_app():
    app = FastAPI()
    # Configure app
    return app

app = create_app()
```

```bash
uvicorn --factory main:create_app
```

### 4. Programmatic Server Control

```python
import uvicorn

# Simple run
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

```python
import asyncio
import uvicorn

async def main():
    config = uvicorn.Config("main:app", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

### 5. Configuration with Environment Variables

```bash
export UVICORN_HOST="0.0.0.0"
export UVICORN_PORT="8000"
export UVICORN_RELOAD="true"
uvicorn main:app
```

## Production Deployment

### Multi-Process Workers

```bash
# Use multiple worker processes
uvicorn main:app --workers 4

# Note: Can't use --reload with --workers
```

### Gunicorn + Uvicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with Gunicorn process manager
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### HTTPS/SSL

```bash
uvicorn main:app --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
```

### Unix Socket

```bash
uvicorn main:app --uds /tmp/uvicorn.sock
```

## Configuration Options

### Common CLI Flags

```bash
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --reload-dir ./app \
  --log-level info \
  --access-log \
  --workers 4
```

### Key Settings

- `--host`: Bind host (default: 127.0.0.1)
- `--port`: Bind port (default: 8000)
- `--reload`: Enable auto-reload for development
- `--workers`: Number of worker processes
- `--log-level`: Logging level (critical, error, warning, info, debug)
- `--access-log`: Enable access logging
- `--factory`: Treat app as application factory

## Docker Integration

### Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Run with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose with Hot Reload

```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - UVICORN_RELOAD=true
    volumes:
      - .:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change port or kill existing process
2. **Module not found**: Check PYTHONPATH or use `--app-dir`
3. **Reload not working**: Ensure watching correct directories with `--reload-dir`
4. **Worker count**: Use `--workers` for production, avoid with `--reload`

### Debug Mode

```bash
uvicorn main:app --reload --log-level debug
```

### Health Checks

```python
@app.get("/health")
async def health():
    return {"status": "healthy"}
```
