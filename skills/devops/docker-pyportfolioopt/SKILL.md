---
name: pyportfolioopt-docker
description: Generate Dockerfile and requirements.txt for containerizing web applications using PyPortfolioOpt optimization library. Use when containerizing Python apps with PyPortfolioOpt, portfolio optimization, or financial optimization that requires OSQP solver. Handles system-level build dependencies for numerical libraries.
---

# PyPortfolioOpt Docker Containerization

Generate production-ready Docker configuration for Python web applications using PyPortfolioOpt.

## Requirements.txt

Must contain these packages in this order:

```
osqp
pyportfolioopt>=1.5.6
```

Add other project dependencies after these two core packages.

## Dockerfile Template

```dockerfile
FROM python:3.11-slim

# System dependencies for numerical/optimization libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    pkg-config \
    libblas-dev \
    liblapack-dev \
    gfortran \
    libopenblas-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Key Rules

1. **System deps before pip**: Install all apt packages before `pip install`
2. **Clean apt cache**: Always end apt stanza with `&& rm -rf /var/lib/apt/lists/*`
3. **OSQP first**: `osqp` must be in requirements.txt before `pyportfolioopt`
4. **Slim base**: Use `python:3.X-slim` for smaller image size

## Customization

- Adjust `CMD` for your framework (FastAPI/uvicorn shown above)
- Add additional Python packages to requirements.txt after the core two
- For Gunicorn: `CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]`
