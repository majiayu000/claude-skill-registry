---
name: docker-setup
description: Setup and create Dockerfiles, Docker Compose, and container build configurations for Todo application
allowed-tools: Bash, Write, Read, Glob, Edit
---

# Docker Setup Skill

## Quick Start

1. **Read Phase 4 Constitution** - `prompts/constitution-prompt-phase-4.md`
2. **Check existing files** - Use `Glob` to find existing `Dockerfile*` or `docker-compose.yml`
3. **Create Dockerfiles** - One for each service (frontend, backend, mcp-server)
4. **Create docker-compose.yml** - For local development
5. **Create .dockerignore files** - Optimize build context
6. **Build and test images** - Verify containers start correctly

## Containerization Overview

This project requires 3 containerized services:

| Service | Base Image | Runtime Port | Purpose |
|----------|-------------|---------------|----------|
| Frontend | node:20-alpine | 3000 | Next.js + ChatKit UI |
| Backend | python:3.13-slim | 8000 | FastAPI + Agents SDK |
| MCP Server | python:3.13-slim | 8001 | FastMCP task tools |

## Frontend Dockerfile Pattern

Create `frontend/Dockerfile`:

```dockerfile
# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

# Set environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy from builder
COPY --from=builder /app/public ./public
COPY --from=builder --app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Set permissions
RUN chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

**Requirements for Next.js**:
- `output: "standalone"` in `next.config.js`
- `npm run build` creates `.next/standalone` directory

## Backend Dockerfile Pattern

Create `backend/Dockerfile`:

```dockerfile
# Builder stage
FROM python:3.13-slim AS builder

WORKDIR /app

# Install uv and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

# Copy dependencies
COPY pyproject.toml uv.lock ./

# Install to .venv
RUN uv sync --frozen --no-dev

# Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Install uv for runtime
RUN pip install --no-cache-dir uv

# Copy .venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/
COPY alembic/ ./alembic/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser

# Activate venv
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## MCP Server Dockerfile Pattern

Create `backend/Dockerfile.mcp`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install FastMCP and dependencies
RUN pip install --no-cache-dir fastmcp mcp openai litellm

# Copy MCP server code
COPY mcp_server/ ./mcp_server/

EXPOSE 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["python", "-m", "mcp_server.server"]
```

## Docker Compose Setup

Create `docker-compose.yml` in project root:

```yaml
version: '3.9'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: todo-frontend
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - NEXT_PUBLIC_MCP_URL=http://mcp-server:8001
    depends_on:
      backend:
        condition: service_healthy
      mcp-server:
        condition: service_healthy
    networks:
      - todo-network
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: todo-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - MCP_SERVER_URL=http://mcp-server:8001
    depends_on:
      mcp-server:
        condition: service_healthy
    networks:
      - todo-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  mcp-server:
    build:
      context: ./backend
      dockerfile: Dockerfile.mcp
    container_name: todo-mcp-server
    ports:
      - "8001:8001"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    networks:
      - todo-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

networks:
  todo-network:
    driver: bridge
```

Create `.env` file (don't commit to git):
```bash
DATABASE_URL=postgresql://user:password@host:5432/todo_db
GEMINI_API_KEY=your-gemini-api-key
BETTER_AUTH_SECRET=your-auth-secret
```

## .dockerignore Files

### Frontend .dockerignore
Create `frontend/.dockerignore`:
```
node_modules
.next
.git
.gitignore
README.md
.DS_Store
.env.local
.env.production.local
*.log
npm-debug.log*
yarn-error.log*
.vscode
.idea
coverage
```

### Backend .dockerignore
Create `backend/.dockerignore`:
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
.venv
env/
venv/
ENV/
.git
.gitignore
.env
*.log
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.dmypy.json
dmypy.json
.pyrepl.json
.DS_Store
.vscode
.idea
```

## Docker AI (Gordon) Integration

When Docker AI (Gordon) is available:

### Enabling Gordon
1. Install Docker Desktop 4.53+
2. Go to Settings → Beta features
3. Toggle "Docker AI" on

### Using Gordon Commands
```bash
# Check capabilities
docker ai "What can you do?"

# Generate Dockerfile
docker ai "Create a Dockerfile for FastAPI application"

# Optimize Dockerfile
docker ai "Optimize this Dockerfile for smaller image size" < Dockerfile

# Debug build issues
docker ai "Why is my container crashing on startup?"

# Security scan
docker ai "Scan this image for security vulnerabilities" todo-backend:latest

# Multi-stage build
docker ai "Convert this to a multi-stage Dockerfile" < Dockerfile
```

## Build Commands

```bash
# Build individual images
docker build -t todo-frontend:latest ./frontend
docker build -t todo-backend:latest ./backend
docker build -t todo-mcp-server:latest -f backend/Dockerfile.mcp ./backend

# Build without cache
docker build --no-cache -t todo-frontend:latest ./frontend

# Build with build args
docker build --build-arg NODE_ENV=production -t todo-frontend:latest ./frontend

# Using Docker Compose
docker-compose build
docker-compose up -d
docker-compose down
docker-compose logs -f

# Tag for registry
docker tag todo-frontend:latest docker.io/username/todo-frontend:v1.0.0
```

## Run Commands

```bash
# Run individual containers
docker run -d -p 3000:3000 --name todo-frontend todo-frontend:latest
docker run -d -p 8000:8000 --name todo-backend todo-backend:latest
docker run -d -p 8001:8001 --name todo-mcp-server todo-mcp-server:latest

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=${DATABASE_URL} \
  -e GEMINI_API_KEY=${GEMINI_API_KEY} \
  --name todo-backend todo-backend:latest

# Run with volume mount (for development)
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/backend/src:/app/src \
  --name todo-backend todo-backend:latest
```

## Verification Checklist

After setup, verify:
- [ ] All Dockerfiles created (frontend, backend, mcp-server)
- [ ] docker-compose.yml created in project root
- [ ] .dockerignore files created for each service
- [ ] .env file created and added to .gitignore
- [ ] Frontend Dockerfile uses multi-stage build
- [ ] Backend Dockerfile uses non-root user
- [ ] All containers have health checks
- [ ] Images build successfully
- [ ] `docker-compose up -d` starts all services
- [ ] Services can communicate via Docker network
- [ ] Gordon commands work (if available)

## Troubleshooting

| Issue | Likely Cause | Solution |
|--------|--------------|-----------|
| `npm ci` fails | node_modules exists | Remove node_modules first |
| Build timeout | Large context | Check .dockerignore |
| Container exits immediately | Entry point error | Verify CMD and healthcheck |
| Port already in use | Previous container | `docker-compose down` first |
| Can't connect to DB | Wrong network name | Use Docker Compose network |
| Permission denied | Running as root | Ensure non-root user in Dockerfile |

## Next Steps

After Docker setup:
1. Test locally with `docker-compose up -d`
2. Access frontend at http://localhost:3000
3. Verify backend health at http://localhost:8000/health
4. Proceed to Kubernetes deployment with `@devops-kubernetes-builder`

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker AI (Gordon)](https://docs.docker.com/ai/gordon/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Phase 4 Constitution](../../../prompts/constitution-prompt-phase-4.md)
- [Phase 4 Plan](../../../prompts/plan-prompt-phase-4.md)
