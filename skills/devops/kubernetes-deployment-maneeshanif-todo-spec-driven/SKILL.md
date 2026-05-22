---
name: kubernetes-deployment
description: Create Kubernetes manifests, deployments, services, and configure Minikube for local development
allowed-tools: Bash, Write, Read, Glob, Edit
---

# Kubernetes Deployment Skill

## Quick Start

1. **Read Phase 4 Constitution** - `prompts/constitution-prompt-phase-4.md`
2. **Check Docker images** - Ensure images are built with `@docker-containerization-builder`
3. **Create namespace** - `kubectl create namespace todo-app`
4. **Apply manifests** - `kubectl apply -f k8s/ -n todo-app`
5. **Verify deployment** - `kubectl get pods -n todo-app`

## Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     KUBERNETES CLUSTER (Minikube)              │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Frontend   │  │  Backend    │  │  MCP Server │            │
│  │  (Next.js)   │  │  (FastAPI)  │  │  (FastMCP) │            │
│  │  Port: 3000 │  │  Port: 8000 │  │  Port: 8001 │            │
│  │  Replicas: 2 │  │  Replicas: 2 │  │  Replicas: 1 │            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│         │                  │                  │                       │
│         └──────────────────┴──────────────────┘                       │
│                          │                                       │
│                    ┌─────▼─────┐                                 │
│                    │ Ingress    │                                 │
│                    │ (nginx)    │                                 │
│                    └─────┬─────┘                                 │
└────────────────────────────┼─────────────────────────────────────────────┘
                         │
                    ┌─────▼─────┐
                    │   User     │
                    │  Browser   │
                    └─────────────┘
```

## Directory Structure

Create `k8s/` directory in project root:
```
k8s/
├── 00-namespace.yaml
├── 01-configmap.yaml
├── 02-secret.yaml
├── 03-mcp-server-deployment.yaml
├── 04-mcp-server-service.yaml
├── 05-backend-deployment.yaml
├── 06-backend-service.yaml
├── 07-frontend-deployment.yaml
├── 08-frontend-service.yaml
└── 09-ingress.yaml
```

## Manifest Templates

### 00-namespace.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
  labels:
    name: todo-app
```

### 01-configmap.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
  namespace: todo-app
data:
  # Database connection (Neon - external)
  DATABASE_URL: ""

  # MCP Server URL (internal)
  MCP_SERVER_URL: "http://mcp-server:8001"

  # Frontend environment
  NEXT_PUBLIC_API_URL: "http://backend:8000"
  NEXT_PUBLIC_MCP_URL: "http://mcp-server:8001"
```

### 02-secret.yaml
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: backend-secrets
  namespace: todo-app
type: Opaque
stringData:
  # Gemini API Key for AI Agent
  GEMINI_API_KEY: ""

  # Better Auth Secret
  BETTER_AUTH_SECRET: ""

  # Database URL (if using internal DB)
  # DATABASE_URL: "postgresql://user:pass@host:5432/db"
```

### 03-mcp-server-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
  namespace: todo-app
  labels:
    app: mcp-server
    tier: backend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
        tier: backend
    spec:
      containers:
      - name: mcp-server
        image: todo-mcp-server:latest
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8001
          protocol: TCP
        env:
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: GEMINI_API_KEY
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "300m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 04-mcp-server-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mcp-server
  namespace: todo-app
  labels:
    app: mcp-server
spec:
  type: ClusterIP
  selector:
    app: mcp-server
  ports:
  - name: http
    port: 8001
    targetPort: http
    protocol: TCP
```

### 05-backend-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-app
  labels:
    app: backend
    tier: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
        tier: backend
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: DATABASE_URL
        - name: MCP_SERVER_URL
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: MCP_SERVER_URL
        - name: GEMINI_API_KEY
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: GEMINI_API_KEY
        - name: BETTER_AUTH_SECRET
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: BETTER_AUTH_SECRET
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 06-backend-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: todo-app
  labels:
    app: backend
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - name: http
    port: 8000
    targetPort: http
    protocol: TCP
```

### 07-frontend-deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-app
  labels:
    app: frontend
    tier: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        tier: frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 3000
          protocol: TCP
        env:
        - name: NEXT_PUBLIC_API_URL
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: NEXT_PUBLIC_API_URL
        - name: NEXT_PUBLIC_MCP_URL
          valueFrom:
            configMapKeyRef:
              name: backend-config
              key: NEXT_PUBLIC_MCP_URL
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 08-frontend-service.yaml
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: todo-app
  labels:
    app: frontend
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
```

### 09-ingress.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress
  namespace: todo-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  ingressClassName: nginx
  rules:
  - host: todo.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 80
```

## Minikube Setup

### Install Minikube
```bash
# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# macOS with Homebrew
brew install minikube

# Windows with Chocolatey
choco install minikube
```

### Start Minikube
```bash
# Start with default resources
minikube start

# Start with more resources (recommended)
minikube start --cpus=4 --memory=8192 --disk-size=50gb

# Enable ingress addon
minikube addons enable ingress

# Enable metrics server (optional)
minikube addons enable metrics-server
```

### Load Images to Minikube
```bash
# Load local Docker images to Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
minikube image load todo-mcp-server:latest
```

### Apply Manifests
```bash
# Apply all manifests
kubectl apply -f k8s/ -n todo-app

# Or apply in order
kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/01-configmap.yaml
kubectl apply -f k8s/02-secret.yaml
kubectl apply -f k8s/03-mcp-server-deployment.yaml
kubectl apply -f k8s/04-mcp-server-service.yaml
kubectl apply -f k8s/05-backend-deployment.yaml
kubectl apply -f k8s/06-backend-service.yaml
kubectl apply -f k8s/07-frontend-deployment.yaml
kubectl apply -f k8s/08-frontend-service.yaml
kubectl apply -f k8s/09-ingress.yaml
```

### Verify Deployment
```bash
# Check namespace
kubectl get namespace todo-app

# Check pods
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check deployments
kubectl get deployments -n todo-app

# View pod logs
kubectl logs -f deployment/backend -n todo-app

# Port forward for local access
kubectl port-forward svc/frontend 8080:80 -n todo-app

# Open service in browser
minikube service frontend -n todo-app
```

## kubectl-ai Integration

When kubectl-ai is available:

```bash
# Get kubectl-ai (if not installed)
go install github.com/GoogleCloudPlatform/kubectl-ai@latest

# Set up authentication (if using cloud)
kubectl-ai login

# Use AI for Kubernetes operations
kubectl-ai "deploy todo app with 3 replicas"
kubectl-ai "scale backend to 5 pods"
kubectl-ai "check why pods are crashing"
kubectl-ai "get pod resource usage"

# Troubleshooting
kubectl-ai "fix CrashLoopBackOff on backend pods"
kubectl-ai "optimize resource allocation"
kubectl-ai "analyze cluster health"
```

## Resource Configuration

| Service | CPU Request | CPU Limit | Memory Request | Memory Limit | Replicas |
|----------|-------------|------------|----------------|---------------|----------|
| Frontend | 100m | 500m | 128Mi | 256Mi | 2 |
| Backend | 200m | 1000m | 256Mi | 512Mi | 2 |
| MCP Server | 100m | 300m | 64Mi | 128Mi | 1 |

## Service Discovery

All services communicate using their Kubernetes Service names:
- **Frontend → Backend**: `http://backend:8000`
- **Backend → MCP Server**: `http://mcp-server:8001`
- **External → Frontend**: Via Ingress at `http://todo.local`

## Verification Checklist

After deployment:
- [ ] Namespace `todo-app` exists
- [ ] All pods are Running state
- [ ] All Services have correct endpoints
- [ ] Ingress is configured
- [ ] Frontend accessible via browser
- [ ] Backend health endpoint responds
- [ ] MCP Server is reachable from backend
- [ ] Environment variables are properly set
- [ ] Resource limits are respected

## Troubleshooting

| Issue | Cause | Fix |
|--------|--------|-----|
| ImagePullBackOff | Image not found | Build and load image with `minikube image load` |
| CrashLoopBackOff | App error on startup | Check logs with `kubectl logs` |
| Pending forever | Resource constraints | Increase Minikube memory/CPU |
| Service not accessible | Wrong selector labels | Verify labels match |
| Ingress 404 | Wrong path/host | Check Ingress rules |

## Scaling Operations

```bash
# Scale deployment
kubectl scale deployment backend --replicas=3 -n todo-app
kubectl scale deployment frontend --replicas=4 -n todo-app

# Using kubectl-ai
kubectl-ai "scale backend to handle increased traffic"
kubectl-ai "reduce frontend replicas during off-hours"
```

## Cleanup

```bash
# Delete all resources in namespace
kubectl delete namespace todo-app

# Or delete specific resources
kubectl delete -f k8s/ -n todo-app

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Next Steps

After successful Minikube deployment:
1. Proceed to Helm chart creation with `@aiops-helm-builder`
2. Prepare for Phase 5 (Dapr + Kafka + Production deployment)

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [kubectl-ai GitHub](https://github.com/GoogleCloudPlatform/kubectl-ai)
- [Phase 4 Constitution](../../../prompts/constitution-prompt-phase-4.md)
- [Phase 4 Plan](../../../prompts/plan-prompt-phase-4.md)
