---
name: bun-deploy
description: Generate optimized Docker images for Bun applications. Use when deploying to containers, minimizing image sizes, setting up CI/CD pipelines, or deploying to Kubernetes.
compatibility: Requires Bun 1.0+ and Docker
allowed-tools: ["Bash", "Write", "Read"]
metadata:
  author: dale
  category: bun-runtime
  tags: [bun, docker, deployment, containers, kubernetes]
---

# Bun Docker Deployment

Create optimized Docker images for Bun applications. Bun's small runtime and binary compilation reduce image sizes by 88MB+ compared to Node.js.

## Quick Reference

For detailed patterns, see:
- **Dockerfile Templates**: [dockerfile-templates.md](references/dockerfile-templates.md) - 12+ optimized templates
- **Kubernetes**: [kubernetes.md](references/kubernetes.md) - K8s manifests, HPA, ingress
- **CI/CD**: [ci-cd.md](references/ci-cd.md) - GitHub Actions, GitLab CI, build scripts
- **Multi-Platform**: [multi-platform.md](references/multi-platform.md) - ARM64/AMD64 builds

## Core Workflow

### 1. Check Prerequisites

```bash
# Verify Docker is installed
docker --version

# Verify Bun is installed locally
bun --version

# Check if project is ready for deployment
ls -la package.json bun.lockb
```

### 2. Determine Deployment Strategy

Ask the user about their needs:

- **Application Type**: Web server, API, worker, or CLI
- **Image Size Priority**: Minimal size (40MB binary) vs. debugging tools (90MB Alpine)
- **Platform**: Single platform or multi-platform (AMD64 + ARM64)
- **Orchestration**: Docker Compose, Kubernetes, or standalone containers

### 3. Create Production Dockerfile

Choose the appropriate template based on needs:

**Standard Multi-Stage (Recommended)**

```dockerfile
# syntax=docker/dockerfile:1

FROM oven/bun:1-alpine AS deps
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile --production

FROM oven/bun:1-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN bun run build

FROM oven/bun:1-alpine AS runtime
WORKDIR /app

RUN addgroup --system --gid 1001 bunuser && \
    adduser --system --uid 1001 bunuser

COPY --from=deps --chown=bunuser:bunuser /app/node_modules ./node_modules
COPY --from=builder --chown=bunuser:bunuser /app/dist ./dist
COPY --from=builder --chown=bunuser:bunuser /app/package.json ./

USER bunuser
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD bun run healthcheck.ts || exit 1

CMD ["bun", "run", "dist/index.js"]
```

**Minimal Binary (40MB)**

For smallest possible images:

```dockerfile
FROM oven/bun:1-alpine AS builder
WORKDIR /app

COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

COPY . .
RUN bun build ./src/index.ts --compile --outfile server

FROM gcr.io/distroless/base-debian12
COPY --from=builder /app/server /server
EXPOSE 3000
ENTRYPOINT ["/server"]
```

**For other scenarios** (monorepo, database apps, CLI tools, etc.), see [dockerfile-templates.md](references/dockerfile-templates.md).

### 4. Create .dockerignore

```dockerignore
node_modules
bun.lockb
dist
*.log
.git
.env
.env.local
tests/
*.test.ts
coverage/
.vscode/
.DS_Store
Dockerfile
docker-compose.yml
```

### 5. Create Health Check Script

Create `healthcheck.ts`:

```typescript
#!/usr/bin/env bun

const port = process.env.PORT || 3000;
const healthEndpoint = process.env.HEALTH_ENDPOINT || '/health';

try {
  const response = await fetch(`http://localhost:${port}${healthEndpoint}`, {
    method: 'GET',
    timeout: 2000,
  });

  if (response.ok) {
    process.exit(0);
  } else {
    console.error(`Health check failed: ${response.status}`);
    process.exit(1);
  }
} catch (error) {
  console.error('Health check error:', error);
  process.exit(1);
}
```

Add health endpoint to your server:

```typescript
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: Date.now(),
    uptime: process.uptime(),
  });
});
```

### 6. Build and Test Image

```bash
# Build image
docker build -t myapp:latest .

# Check image size
docker images myapp:latest

# Run container
docker run -p 3000:3000 myapp:latest

# Test health endpoint
curl http://localhost:3000/health
```

### 7. Setup for Environment

**For Local Development with Docker Compose:**

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

Run with: `docker-compose up`

**For Kubernetes Deployment:**

See [kubernetes.md](references/kubernetes.md) for complete manifests including:
- Deployment configuration
- Service and Ingress
- Secrets and ConfigMaps
- Horizontal Pod Autoscaling
- Resource limits optimized for Bun

**For CI/CD:**

See [ci-cd.md](references/ci-cd.md) for:
- GitHub Actions workflow
- GitLab CI configuration
- Build and push scripts
- Automated deployments

**For Multi-Platform (ARM64 + AMD64):**

See [multi-platform.md](references/multi-platform.md) for:
- Multi-platform Dockerfile
- Buildx configuration
- Testing on different architectures

### 8. Update package.json

Add Docker scripts:

```json
{
  "scripts": {
    "docker:build": "docker build -t myapp:latest .",
    "docker:run": "docker run -p 3000:3000 myapp:latest",
    "docker:dev": "docker-compose up",
    "docker:clean": "docker system prune -af"
  }
}
```

## Image Size Comparison

Bun produces significantly smaller images:

| Configuration | Size | Use Case |
|--------------|------|----------|
| **Bun Binary (distroless)** | ~40 MB | Production (minimal) |
| **Bun Alpine** | ~90 MB | Production (standard) |
| **Node.js Alpine** | ~180 MB | Baseline comparison |

**88MB+ savings with Bun!**

## Security Best Practices

1. **Use non-root user** (included in Dockerfiles above)
2. **Scan for vulnerabilities**: `docker scan myapp:latest`
3. **Use official base images**: `oven/bun` is official
4. **Keep images updated**: Rebuild regularly with latest Bun
5. **Never hardcode secrets**: Use environment variables or secret managers

## Optimization Tips

**Layer caching:**
```dockerfile
# Copy dependencies first (changes less often)
COPY package.json bun.lockb ./
RUN bun install

# Copy source code last (changes more often)
COPY . .
RUN bun run build
```

**Reduce layer count:**
```dockerfile
# Combine RUN commands
RUN bun install && \
    bun run build && \
    rm -rf tests/
```

**Minimize final image:**
```dockerfile
# Only copy what's needed in runtime
COPY --from=builder /app/dist ./dist
# Don't copy: src/, tests/, .git/, node_modules (if using binary)
```

## Completion Checklist

- ✅ Dockerfile created (multi-stage or binary)
- ✅ .dockerignore configured
- ✅ Health check implemented
- ✅ Non-root user configured
- ✅ Image built and tested locally
- ✅ Image size verified (<100MB for Alpine, <50MB for binary)
- ✅ Environment configuration ready (docker-compose or K8s)
- ✅ CI/CD pipeline configured (if needed)

## Next Steps

After basic deployment:

1. **Monitoring**: Add Prometheus metrics endpoint
2. **Logging**: Configure structured logging
3. **Secrets**: Set up proper secret management
4. **Scaling**: Configure horizontal pod autoscaling (K8s)
5. **CI/CD**: Automate builds and deployments
6. **Multi-region**: Deploy to multiple regions for redundancy

For detailed implementations, see the reference files linked above.
