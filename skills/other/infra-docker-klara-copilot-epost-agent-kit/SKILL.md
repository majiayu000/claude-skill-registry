---
name: infra-docker
description: (ePost) Use when working with Dockerfiles, docker-compose, containers, or containerized deployments
user-invocable: false

metadata:
  agent-affinity: [epost-fullstack-developer, epost-planner]
  keywords: [docker, container, dockerfile, compose, deployment, devops]
  platforms: [all]
  triggers: ["Dockerfile", "docker-compose.yml", "container", "docker"]
---

# Docker Skill

## Purpose
Containerization for development and deployment.

## When Active
User mentions Docker, container, deployment.

## Expertise

### Dockerfile Patterns
- Multi-stage builds
- Layer optimization
- Caching strategies
- Security scanning

### Docker Compose
- Service definition
- Volume management
- Network configuration
- Environment variables

### Build Optimization
- Layer ordering
- .dockerignore
- BuildKit features
- Cache mounts

### Production Patterns
- Minimal base images
- Non-root user
- Health checks
- Signal handling

### Volume Management
- Named volumes
- Bind mounts
- Volume drivers
- Backup strategies

### Network Configuration
- Bridge networks
- Overlay networks
- Service discovery
- Load balancing

## Patterns

### Multi-stage Node.js Build
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --omit=dev
CMD ["node", "dist/index.js"]
```

### Development Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    volumes:
      - .:/app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
  db:
    image: postgres:15
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secret

volumes:
  postgres-data:
```

### Production Compose
```yaml
version: '3.8'
services:
  app:
    image: registry.example.com/app:latest
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
```

### .dockerignore
```
node_modules
npm-debug.log
.git
.env
*.md
```

## Best Practices
- Use specific version tags
- Run as non-root user
- Minimize layers
- COPY before RUN for cache
- Use health checks
- Don't bundle development dependencies

## Dependencies
- Docker Engine 20+
- Docker Compose v2
