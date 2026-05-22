---
name: docker-k8s
description: Docker, Docker Compose, and Kubernetes patterns for containerization and orchestration
license: MIT
compatibility: opencode
---

# Docker & Kubernetes Skill

Comprehensive patterns for containerization with Docker and orchestration with Kubernetes.

## What I Know

### Dockerfile Best Practices

**Multi-Stage Build (Node.js)**
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies first (caching)
COPY package*.json ./
RUN npm ci --only=production

# Copy source and build
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy only necessary files
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

USER nodejs
EXPOSE 3000

CMD ["node", "dist/index.js"]
```

**Multi-Stage Build (Python)**
```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production stage
FROM python:3.12-slim AS production
WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY --chown=app:app . .

USER app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Multi-Stage Build (Go)**
```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Install certificates for HTTPS
RUN apk --no-cache add ca-certificates

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download

# Build binary
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server ./cmd/server

# Production stage - scratch for minimal image
FROM scratch AS production
WORKDIR /app

# Copy certificates and binary
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/server .

EXPOSE 8080
ENTRYPOINT ["/app/server"]
```

### .dockerignore

```dockerignore
# Git
.git
.gitignore

# Dependencies
node_modules
vendor
__pycache__

# Build artifacts
dist
build
*.pyc
*.pyo

# IDE
.idea
.vscode
*.swp

# Environment
.env
.env.*
!.env.example

# Tests
tests
__tests__
coverage
.pytest_cache

# Documentation
docs
*.md
!README.md

# Docker
Dockerfile*
docker-compose*
.docker

# CI/CD
.github
.gitlab-ci.yml
```

### Docker Compose

**Development Setup**
```yaml
# docker-compose.yml
version: '3.9'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgres://user:password@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    command: npm run dev

  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

volumes:
  postgres_data:
  redis_data:
```

**Production Setup**
```yaml
# docker-compose.prod.yml
version: '3.9'

services:
  app:
    image: ${REGISTRY}/app:${TAG:-latest}
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Kubernetes Manifests

**Deployment**
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  template:
    metadata:
      labels:
        app: app
    spec:
      serviceAccountName: app
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: app
          image: registry.example.com/app:v1.0.0
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
              protocol: TCP
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "200m"
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
      imagePullSecrets:
        - name: regcred
```

**Service**
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: app
  labels:
    app: app
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 3000
      protocol: TCP
      name: http
  selector:
    app: app
```

**Ingress**
```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app
                port:
                  number: 80
```

**ConfigMap**
```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  CACHE_TTL: "3600"
  MAX_CONNECTIONS: "100"
```

**Secret**
```yaml
# k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-url: "postgres://user:password@db:5432/app"
  jwt-secret: "your-jwt-secret"
```

**HorizontalPodAutoscaler**
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
```

**PodDisruptionBudget**
```yaml
# k8s/pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: app
```

### Helm Chart Structure

```
charts/app/
├── Chart.yaml
├── values.yaml
├── values-production.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── pdb.yaml
```

**Chart.yaml**
```yaml
apiVersion: v2
name: app
description: My Application Helm Chart
version: 1.0.0
appVersion: "1.0.0"
```

**values.yaml**
```yaml
replicaCount: 2

image:
  repository: registry.example.com/app
  tag: latest
  pullPolicy: Always

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls
      hosts:
        - app.example.com

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

env:
  NODE_ENV: production
```

### CI/CD with Docker

**GitHub Actions**
```yaml
# .github/workflows/docker.yml
name: Build and Push Docker

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Security Best Practices

**Image Scanning**
```yaml
# In CI pipeline
- name: Scan image for vulnerabilities
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE_NAME }}:${{ github.sha }}
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
```

**Security Checklist**
- [ ] Use specific image tags, not `latest`
- [ ] Run as non-root user
- [ ] Use read-only root filesystem
- [ ] Drop all capabilities
- [ ] Set resource limits
- [ ] Use network policies
- [ ] Scan images for vulnerabilities
- [ ] Sign images with Cosign
- [ ] Use secrets management (Vault, Sealed Secrets)

### Debugging

**Docker Commands**
```bash
# View logs
docker logs -f container_name

# Execute into container
docker exec -it container_name /bin/sh

# Inspect container
docker inspect container_name

# View resource usage
docker stats

# Clean up
docker system prune -a --volumes
```

**Kubernetes Commands**
```bash
# View pod logs
kubectl logs -f pod-name

# Execute into pod
kubectl exec -it pod-name -- /bin/sh

# Describe resource
kubectl describe pod pod-name

# Port forward
kubectl port-forward pod/pod-name 3000:3000

# View events
kubectl get events --sort-by='.lastTimestamp'

# Debug with ephemeral container
kubectl debug pod-name -it --image=busybox
```

### Common Pitfalls

1. **Using `latest` tag** - Always use specific version tags
2. **Running as root** - Create and use non-root user
3. **No health checks** - Always add liveness and readiness probes
4. **No resource limits** - Set CPU and memory limits
5. **Secrets in images** - Use environment variables or secrets
6. **Large images** - Use multi-stage builds and alpine base
7. **No .dockerignore** - Exclude unnecessary files
8. **Hardcoded config** - Use ConfigMaps and environment variables

---

*Part of SuperAI GitHub - Centralized OpenCode Configuration*
