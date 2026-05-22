---
name: docker-helper
description: Docker and Docker Compose mastery for containers, images, networks, volumes, and debugging. Use when user asks to "build a container", "run docker", "debug container", "write dockerfile", "docker compose up", "check container logs", "optimize docker image", or any container operations.
---

# Docker Helper

Essential Docker and Docker Compose commands and patterns.

## Container Operations

```bash
# Run container
docker run -d --name myapp -p 8080:80 nginx
docker run -it --rm ubuntu bash  # Interactive, auto-remove

# With volume and env
docker run -d \
  -v $(pwd):/app \
  -e NODE_ENV=production \
  --name myapp \
  node:18 npm start

# List containers
docker ps          # Running
docker ps -a       # All

# Logs
docker logs myapp
docker logs -f myapp        # Follow
docker logs --tail 100 myapp

# Exec into container
docker exec -it myapp bash
docker exec -it myapp sh    # Alpine

# Stop/remove
docker stop myapp
docker rm myapp
docker rm -f myapp  # Force
```

## Image Operations

```bash
# Build
docker build -t myapp:latest .
docker build -t myapp:v1.0 -f Dockerfile.prod .

# List/remove
docker images
docker rmi myapp:latest
docker image prune -a  # Remove unused

# Tag/push
docker tag myapp:latest registry.io/myapp:latest
docker push registry.io/myapp:latest
```

## Docker Compose

```bash
# Start services
docker compose up -d
docker compose up -d --build  # Rebuild

# Stop
docker compose down
docker compose down -v  # Remove volumes

# Logs
docker compose logs -f
docker compose logs -f web

# Scale
docker compose up -d --scale web=3

# Exec
docker compose exec web bash
```

### Compose File Pattern

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret

volumes:
  postgres_data:
```

## Debugging

```bash
# Container inspection
docker inspect myapp
docker inspect --format '{{.NetworkSettings.IPAddress}}' myapp

# Resource usage
docker stats
docker stats myapp

# Processes in container
docker top myapp

# Filesystem changes
docker diff myapp

# Copy files
docker cp myapp:/app/file.txt ./
docker cp ./file.txt myapp:/app/
```

## Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a --volumes
```

## Dockerfile Best Practices

```dockerfile
# Use specific tags
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files first (layer caching)
COPY package*.json ./
RUN npm ci --only=production

# Copy source
COPY . .

# Non-root user
RUN addgroup -g 1001 appgroup && \
    adduser -S -u 1001 -G appgroup appuser
USER appuser

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -q --spider http://localhost:3000/health || exit 1

CMD ["node", "server.js"]
```

## Reference

For multi-stage builds, networking, and optimization: `references/advanced.md`
