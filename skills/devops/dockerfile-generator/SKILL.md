# Skill: Dockerfile Generator

**Purpose**: Generate optimized Dockerfiles for Next.js frontend and FastAPI backend (Phase IV preparation).

## Trigger Conditions

Invoke this skill when:
- Phase IV (Containerization) begins
- User asks for "Docker setup", "containerize", or "Dockerfile"
- Deployment to Docker-based platform required

## Capabilities

### 1. FastAPI Backend Dockerfile

Creates `backend/Dockerfile`:

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy application code
COPY --chown=appuser:appgroup ./app ./app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Next.js Frontend Dockerfile

Creates `frontend/Dockerfile`:

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci --only=production

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build arguments for environment
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build the application
RUN npm run build

# Stage 3: Runner
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy built assets
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

**Required next.config.js setting**:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
}

module.exports = nextConfig
```

### 3. Docker Compose for Development

Creates `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - CORS_ORIGINS=http://localhost:3000
      - DEBUG=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        - NEXT_PUBLIC_API_URL=http://localhost:8000
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      backend:
        condition: service_healthy
    restart: unless-stopped

networks:
  default:
    name: todo-network
```

### 4. Docker Compose for Production

Creates `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    expose:
      - "8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
      - CORS_ORIGINS=${FRONTEND_URL}
      - DEBUG=false
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
    restart: always

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        - NEXT_PUBLIC_API_URL=${BACKEND_URL}
    expose:
      - "3000"
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 256M
          cpus: '0.25'
    restart: always

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certs:/etc/nginx/certs:ro
    depends_on:
      - frontend
      - backend
    restart: always
```

### 5. .dockerignore Files

`backend/.dockerignore`:
```
__pycache__
*.pyc
*.pyo
.env
.env.*
.git
.gitignore
venv/
.venv/
*.md
tests/
.pytest_cache/
```

`frontend/.dockerignore`:
```
node_modules
.next
.git
.gitignore
*.md
.env*
npm-debug.log*
.DS_Store
```

## Build Commands

```bash
# Build images
docker-compose build

# Run development
docker-compose up

# Run production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f

# Stop all
docker-compose down
```

## Checklist

- [ ] Create backend/Dockerfile
- [ ] Create frontend/Dockerfile
- [ ] Add output: 'standalone' to next.config.js
- [ ] Create docker-compose.yml
- [ ] Create .dockerignore files
- [ ] Test local build: `docker-compose build`
- [ ] Test local run: `docker-compose up`
- [ ] Verify health checks work
