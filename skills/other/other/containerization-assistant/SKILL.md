---
name: containerization-assistant
description: "Generate Dockerfiles, Docker Compose configurations, and Kubernetes manifests for containerizing applications. Use when: (1) Creating Dockerfiles for Node.js, Python, Java, Go, or other applications, (2) Setting up multi-service environments with Docker Compose, (3) Generating Kubernetes deployments, services, and ingress configurations, (4) Optimizing container images for production, (5) Implementing containerization best practices. Provides both ready-to-use templates and custom-generated configurations based on project requirements."
---

# Containerization Assistant

Generate production-ready Docker and Kubernetes configurations for your applications.

## Quick Start

### Generate a Dockerfile

**For existing templates**:
```bash
# Node.js application
cp assets/Dockerfile.nodejs ./Dockerfile

# Python application
cp assets/Dockerfile.python ./Dockerfile

# Java application (Spring Boot)
cp assets/Dockerfile.java ./Dockerfile

# Go application
cp assets/Dockerfile.go ./Dockerfile
```

**For custom generation**: Describe your application stack and requirements, and a custom Dockerfile will be generated.

### Generate Docker Compose

```bash
# Multi-service application template
cp assets/docker-compose.yml ./
cp assets/.env.example ./.env

# Edit .env with your configuration
```

### Generate Kubernetes Manifests

Kubernetes configurations are generated based on your deployment requirements. See **[kubernetes_patterns.md](references/kubernetes_patterns.md)** for complete examples.

## Available Templates

### Dockerfiles

**Node.js** (`assets/Dockerfile.nodejs`):
- Multi-stage build for minimal image size
- Alpine-based (~170MB vs ~900MB)
- Non-root user for security
- Production-optimized dependencies

**Python** (`assets/Dockerfile.python`):
- Multi-stage build with builder pattern
- Slim base image
- User-space pip installations
- Non-root user

**Java** (`assets/Dockerfile.java`):
- Multi-stage build with JDK builder
- JRE-only runtime for smaller image
- Spring Boot optimized
- Non-root user

**Go** (`assets/Dockerfile.go`):
- Multi-stage build
- Minimal Alpine runtime
- Static binary compilation
- Non-root user

### Docker Compose

**Multi-service stack** (`assets/docker-compose.yml`):
- Web application service
- PostgreSQL database
- Redis cache
- Nginx reverse proxy
- Health checks
- Volume management
- Network isolation

### Environment Configuration

**Environment template** (`assets/.env.example`):
- Database credentials
- Application secrets
- Service configuration
- API keys

## Generation Workflow

### 1. Analyze Project

Identify:
- Programming language and framework
- Dependencies and build tools
- Runtime requirements
- Services needed (database, cache, etc.)

### 2. Choose Approach

**Template-based**:
- Use for common stacks (Node.js, Python, Java, Go)
- Copy and customize template
- Fast and reliable

**Custom generation**:
- Use for unique requirements
- Generate from scratch
- Full customization

### 3. Customize Configuration

**Dockerfile customization**:
```dockerfile
# Update base image version
FROM node:18-alpine  # Change version as needed

# Add build arguments
ARG NODE_ENV=production

# Modify exposed port
EXPOSE 3000  # Change to your port

# Update startup command
CMD ["node", "server.js"]  # Change to your entry point
```

**Docker Compose customization**:
```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"  # Change port mapping
    environment:
      - DATABASE_URL=${DATABASE_URL}  # Add environment variables
```

### 4. Build and Test

```bash
# Build Docker image
docker build -t myapp:1.0.0 .

# Test locally
docker run -p 3000:3000 myapp:1.0.0

# Test with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 5. Optimize and Deploy

See **[dockerfile_best_practices.md](references/dockerfile_best_practices.md)** for:
- Image size optimization
- Security hardening
- Build caching strategies
- Multi-stage build patterns

## Common Scenarios

### Scenario 1: Containerize Node.js Express API

**Requirements**: Node.js 18, PostgreSQL database, Redis cache

**Steps**:
1. Use `Dockerfile.nodejs` template
2. Use `docker-compose.yml` for local development
3. Customize environment variables
4. Add health check endpoint

**Generated files**:
- `Dockerfile` - Multi-stage Node.js build
- `docker-compose.yml` - Web, PostgreSQL, Redis services
- `.env` - Configuration variables
- `.dockerignore` - Exclude unnecessary files

### Scenario 2: Containerize Python Django Application

**Requirements**: Python 3.11, PostgreSQL, Celery workers

**Steps**:
1. Use `Dockerfile.python` template
2. Generate custom docker-compose with Celery service
3. Add migration init container
4. Configure health checks

**Generated files**:
- `Dockerfile` - Multi-stage Python build
- `docker-compose.yml` - Web, PostgreSQL, Redis, Celery
- `celery-worker.Dockerfile` - Celery worker image
- `.env` - Database and Celery configuration

### Scenario 3: Deploy to Kubernetes

**Requirements**: Deploy containerized app to Kubernetes with scaling

**Steps**:
1. Build and push Docker image
2. Generate Deployment manifest
3. Generate Service (LoadBalancer)
4. Generate Ingress with TLS
5. Add HorizontalPodAutoscaler

See **[kubernetes_patterns.md](references/kubernetes_patterns.md)** for complete examples.

### Scenario 4: Microservices Architecture

**Requirements**: Multiple services (API, Auth, Workers) with shared database

**Steps**:
1. Generate Dockerfile for each service
2. Create docker-compose with all services
3. Configure service discovery
4. Set up shared networks and volumes

**Generated structure**:
```
services/
  api/
    Dockerfile
  auth/
    Dockerfile
  worker/
    Dockerfile
docker-compose.yml
.env
```

## Dockerfile Best Practices

### Multi-Stage Builds

Reduce image size by separating build and runtime:

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

### Security

```dockerfile
# Use non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs
USER nodejs

# Use specific versions
FROM node:18.17.0-alpine  # Not 'latest'

# Scan for vulnerabilities
# docker scan myapp:latest
```

### Optimization

```dockerfile
# Order layers from least to most frequently changing
COPY package*.json ./  # Changes less often
RUN npm ci
COPY . .  # Changes more often

# Use .dockerignore
# node_modules
# .git
# *.md
```

For comprehensive best practices, see **[dockerfile_best_practices.md](references/dockerfile_best_practices.md)**.

## Kubernetes Deployment

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:1.0.0
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Service + Ingress

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

For complete Kubernetes patterns including ConfigMaps, Secrets, StatefulSets, Jobs, and more, see **[kubernetes_patterns.md](references/kubernetes_patterns.md)**.

## Configuration Management

### Environment Variables

**Development** (`.env`):
```bash
NODE_ENV=development
DATABASE_URL=postgresql://localhost/myapp_dev
DEBUG=true
```

**Production** (Kubernetes Secret):
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
stringData:
  database_url: "postgresql://prod-db/myapp"
  api_key: "secret-key"
```

### ConfigMaps

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  log_level: "info"
  feature_flags: |
    {
      "new_ui": true,
      "beta_features": false
    }
```

## Troubleshooting

### Docker Build Issues

**Problem**: Build fails with permission errors

**Solution**:
```dockerfile
RUN chown -R appuser:appuser /app
USER appuser
```

**Problem**: Image too large

**Solution**:
- Use multi-stage builds
- Use Alpine base images
- Add .dockerignore file
- Clean up in same RUN layer

### Container Runtime Issues

**Problem**: Container exits immediately

**Solution**:
- Check CMD/ENTRYPOINT
- Verify application starts correctly
- Check logs: `docker logs <container>`

**Problem**: Cannot connect to container

**Solution**:
- Verify port mapping: `-p 3000:3000`
- Check application binds to `0.0.0.0`, not `localhost`
- Verify EXPOSE directive in Dockerfile

### Kubernetes Issues

**Problem**: Pod stuck in Pending state

**Solution**:
```bash
kubectl describe pod <pod-name>
# Check events for resource constraints or image pull issues
```

**Problem**: Pod crashes with OOMKilled

**Solution**:
```yaml
resources:
  limits:
    memory: "512Mi"  # Increase memory limit
```

## Reference Documentation

### Dockerfile Best Practices
See **[dockerfile_best_practices.md](references/dockerfile_best_practices.md)** for:
- Multi-stage build patterns
- Layer caching optimization
- Security best practices
- Image size optimization
- Health checks
- Language-specific patterns (Node.js, Python, Java, Go)
- Development vs Production configurations

### Kubernetes Patterns
See **[kubernetes_patterns.md](references/kubernetes_patterns.md)** for:
- Deployments and StatefulSets
- Services (ClusterIP, LoadBalancer, NodePort)
- ConfigMaps and Secrets
- Ingress with TLS
- HorizontalPodAutoscaler
- PersistentVolumeClaims
- Jobs and CronJobs
- Health probes (liveness, readiness, startup)
- NetworkPolicies
- Multi-container pods and init containers

## Advanced Topics

### CI/CD Integration

**GitHub Actions**:
```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push myapp:${{ github.sha }}
```

### Image Registry

**Push to Docker Hub**:
```bash
docker tag myapp:1.0.0 username/myapp:1.0.0
docker push username/myapp:1.0.0
```

**Push to AWS ECR**:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
docker tag myapp:1.0.0 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:1.0.0
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/myapp:1.0.0
```

### Helm Charts

For complex Kubernetes deployments, consider using Helm charts for templated manifests and version management.
