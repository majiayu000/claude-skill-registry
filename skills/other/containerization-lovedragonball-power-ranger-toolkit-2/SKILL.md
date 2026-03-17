---
name: containerization
description: Docker and Kubernetes workflows for containerization. Use for building containers, orchestration, and cloud-native deployments.
---

# 🐳 Containerization Skill

## Docker Basics

### Dockerfile
```dockerfile
# Multi-stage build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://db:5432/app
    depends_on:
      - db
  
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Docker Commands

```bash
# Build
docker build -t myapp:latest .

# Run
docker run -d -p 3000:3000 --name myapp myapp:latest

# Compose
docker-compose up -d
docker-compose down

# Clean up
docker system prune -a
```

---

## Kubernetes Basics

### Deployment
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
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:latest
          ports:
            - containerPort: 3000
          resources:
            limits:
              memory: "256Mi"
              cpu: "500m"
```

### Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
    - port: 80
      targetPort: 3000
  type: LoadBalancer
```

---

## K8s Commands

```bash
# Apply configs
kubectl apply -f deployment.yaml

# Get resources
kubectl get pods
kubectl get services

# Logs & Debug
kubectl logs pod-name
kubectl exec -it pod-name -- /bin/sh

# Scale
kubectl scale deployment myapp --replicas=5
```

---

## Best Practices

| Practice | Description |
|----------|-------------|
| .dockerignore | Exclude node_modules, .git |
| Multi-stage | Smaller production images |
| Non-root | Run as non-root user |
| Health checks | Add HEALTHCHECK directive |
| Resource limits | Set CPU/memory limits |

---

## Checklist

- [ ] Create Dockerfile (multi-stage)
- [ ] Add .dockerignore
- [ ] Set up docker-compose for dev
- [ ] Configure health checks
- [ ] Create K8s manifests
- [ ] Set resource limits
