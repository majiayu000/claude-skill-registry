---
name: docker-compose-basics
description: Use when defining and running multi-container Docker applications with Docker Compose YAML configuration.
allowed-tools: []
---

# Docker Compose Basics

Docker Compose for defining and running multi-container applications.

## Basic Structure

```yaml
version: '3.8'

services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    environment:
      - NGINX_HOST=localhost
    depends_on:
      - api
      
  api:
    build: ./api
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgres://db:5432/myapp
    depends_on:
      - db
      
  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp

volumes:
  pgdata:
```

## Common Commands

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Rebuild
docker compose build

# Execute command
docker compose exec web sh

# Scale service
docker compose up -d --scale api=3
```

## Best Practices

### Environment Variables

```yaml
services:
  api:
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - API_KEY=${API_KEY}
```

### Health Checks

```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Resource Limits

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```
