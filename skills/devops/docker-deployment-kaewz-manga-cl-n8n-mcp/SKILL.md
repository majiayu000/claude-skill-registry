# Docker Deployment Skill

> Docker patterns for cl-n8n-mcp.

---

## Docker Compose

```yaml
version: '3.8'
services:
  n8n-mcp:
    build: .
    container_name: n8n-mcp-dynamic
    ports:
      - "3011:3000"
    environment:
      - ENABLE_MULTI_TENANT=true
      - AUTH_TOKEN=${AUTH_TOKEN}
      - MCP_MODE=http
      - RATE_LIMIT_PER_MINUTE=50
      - DAILY_LIMIT=100
    restart: unless-stopped
```

## Dockerfile (Two-Stage)

```dockerfile
# Stage 1: Build
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:22-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/data ./data
COPY --from=builder /app/public ./public
COPY package*.json ./
RUN npm ci --production
CMD ["node", "dist/http-server/index.js"]
```

## Commands

```bash
# Build and start
docker compose build
docker compose up -d

# View logs
docker compose logs -f

# Rebuild after code changes
npm run build && docker compose build && docker compose up -d

# Check status
docker ps --filter name=n8n-mcp-dynamic
curl http://localhost:3011/health
```
