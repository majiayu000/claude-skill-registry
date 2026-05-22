---
name: FastAPI Kubernetes Deployment
description: This skill should be used when the user asks to "deploy FastAPI to Kubernetes", "create Dockerfile", "build Docker image", "write Helm chart", "configure K8s deployment", "add health checks", "scale FastAPI", or mentions Docker, Kubernetes, K8s, containers, Helm, or deployment. Provides containerization and orchestration patterns.
version: 0.1.0
---

# FastAPI Docker & Kubernetes Deployment

This skill provides production-ready patterns for containerizing FastAPI applications and deploying to Kubernetes.

## Dockerfile (Multi-Stage)

### Production Dockerfile

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy wheels and install
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY ./app /app/app

# Change ownership
RUN chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')" || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Development Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install -r requirements.txt -r requirements-dev.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

## Docker Compose (Development)

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    volumes:
      - ./app:/app/app
    environment:
      - MONGODB_URL=mongodb://mongo:27017
      - REDIS_URL=redis://redis:6379
      - KEYCLOAK_URL=http://keycloak:8080
    depends_on:
      - mongo
      - redis

  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  keycloak:
    image: quay.io/keycloak/keycloak:23.0
    environment:
      - KEYCLOAK_ADMIN=admin
      - KEYCLOAK_ADMIN_PASSWORD=admin
    command: start-dev
    ports:
      - "8080:8080"

volumes:
  mongo_data:
```

## Health Check Endpoints

```python
from fastapi import APIRouter, Response
from typing import Dict
import asyncio

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Basic liveness probe."""
    return {"status": "healthy"}

@router.get("/health/ready")
async def readiness_check(
    db: Database = Depends(get_db),
    cache: Redis = Depends(get_cache)
) -> Dict[str, any]:
    """Readiness probe - checks all dependencies."""
    checks = {}

    # Check MongoDB
    try:
        await db.command("ping")
        checks["mongodb"] = "ok"
    except Exception as e:
        checks["mongodb"] = f"error: {str(e)}"

    # Check Redis
    try:
        await cache.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"

    # Overall status
    all_ok = all(v == "ok" for v in checks.values())

    if not all_ok:
        return Response(
            content=json.dumps({"status": "unhealthy", "checks": checks}),
            status_code=503,
            media_type="application/json"
        )

    return {"status": "healthy", "checks": checks}

@router.get("/health/live")
async def liveness_check() -> Dict[str, str]:
    """Kubernetes liveness probe."""
    return {"status": "alive"}
```

## Kubernetes Deployment

### Deployment Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
  labels:
    app: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi-app
  template:
    metadata:
      labels:
        app: fastapi-app
    spec:
      containers:
        - name: api
          image: registry.example.com/fastapi-app:latest
          ports:
            - containerPort: 8000
          env:
            - name: MONGODB_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: mongodb-url
            - name: REDIS_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: redis-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            readOnlyRootFilesystem: true
```

### Service & Ingress

```yaml
apiVersion: v1
kind: Service
metadata:
  name: fastapi-app
spec:
  selector:
    app: fastapi-app
  ports:
    - port: 80
      targetPort: 8000
  type: ClusterIP
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fastapi-app
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: fastapi-app
                port:
                  number: 80
```

## Helm Chart Structure

```
fastapi-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── _helpers.tpl
```

### values.yaml

```yaml
replicaCount: 3

image:
  repository: registry.example.com/fastapi-app
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com

resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "500m"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

mongodb:
  url: ""  # Set via secret

redis:
  url: ""  # Set via secret
```

## Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fastapi-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fastapi-app
  minReplicas: 3
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
```

## Additional Resources

### Reference Files

For detailed deployment patterns:
- **`references/helm-chart.md`** - Complete Helm chart templates
- **`references/ci-cd.md`** - GitHub Actions deployment pipeline
- **`references/monitoring.md`** - Prometheus/Grafana setup

### Example Files

Working examples in `examples/`:
- **`examples/Dockerfile`** - Production Dockerfile
- **`examples/docker-compose.yml`** - Development compose
- **`examples/k8s/`** - Complete K8s manifests
