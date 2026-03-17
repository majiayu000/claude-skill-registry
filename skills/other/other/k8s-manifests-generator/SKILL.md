# Skill: Kubernetes Manifests Generator

**Purpose**: Generate production-ready Kubernetes manifests for todo app deployment (Phase V preparation).

## Trigger Conditions

Invoke this skill when:
- Phase V (Kubernetes) begins
- User asks for "K8s deployment", "Kubernetes setup", or "manifests"
- Deploying to Kubernetes cluster (EKS, GKE, AKS, etc.)

## Capabilities

### 1. Namespace Configuration

Creates `k8s/namespace.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
  labels:
    app: todo
    environment: production
```

### 2. Backend Deployment

Creates `k8s/backend/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-backend
  namespace: todo-app
  labels:
    app: todo-backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-backend
  template:
    metadata:
      labels:
        app: todo-backend
    spec:
      containers:
      - name: backend
        image: your-registry/todo-backend:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: todo-backend-config
        - secretRef:
            name: todo-backend-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
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
      imagePullSecrets:
      - name: registry-credentials
```

### 3. Backend Service

Creates `k8s/backend/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-backend
  namespace: todo-app
spec:
  selector:
    app: todo-backend
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### 4. Frontend Deployment

Creates `k8s/frontend/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: todo-frontend
  namespace: todo-app
  labels:
    app: todo-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: todo-frontend
  template:
    metadata:
      labels:
        app: todo-frontend
    spec:
      containers:
      - name: frontend
        image: your-registry/todo-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "https://api.your-domain.com"
        resources:
          requests:
            memory: "128Mi"
            cpu: "50m"
          limits:
            memory: "256Mi"
            cpu: "250m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### 5. Frontend Service

Creates `k8s/frontend/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: todo-frontend
  namespace: todo-app
spec:
  selector:
    app: todo-frontend
  ports:
  - port: 80
    targetPort: 3000
  type: ClusterIP
```

### 6. Ingress Configuration

Creates `k8s/ingress.yaml`:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress
  namespace: todo-app
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - your-domain.com
    - api.your-domain.com
    secretName: todo-tls
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-frontend
            port:
              number: 80
  - host: api.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: todo-backend
            port:
              number: 80
```

### 7. ConfigMap

Creates `k8s/backend/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-backend-config
  namespace: todo-app
data:
  CORS_ORIGINS: "https://your-domain.com"
  DEBUG: "false"
```

### 8. Secrets (template)

Creates `k8s/backend/secrets.yaml.template`:

```yaml
# DO NOT COMMIT THIS FILE WITH REAL VALUES
# Use: kubectl create secret generic todo-backend-secrets --from-env-file=.env
apiVersion: v1
kind: Secret
metadata:
  name: todo-backend-secrets
  namespace: todo-app
type: Opaque
stringData:
  DATABASE_URL: "<your-neon-database-url>"
  BETTER_AUTH_SECRET: "<your-auth-secret>"
```

### 9. HorizontalPodAutoscaler

Creates `k8s/backend/hpa.yaml`:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
  namespace: todo-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
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
```

## Directory Structure

```
k8s/
├── namespace.yaml
├── ingress.yaml
├── backend/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml.template
│   └── hpa.yaml
└── frontend/
    ├── deployment.yaml
    └── service.yaml
```

## Deployment Commands

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create secrets (from .env file)
kubectl create secret generic todo-backend-secrets \
  --from-env-file=backend/.env \
  -n todo-app

# Apply all manifests
kubectl apply -f k8s/ -R

# Check deployment status
kubectl get all -n todo-app

# View logs
kubectl logs -f deployment/todo-backend -n todo-app
```

## Checklist

- [ ] Create namespace.yaml
- [ ] Create backend deployment, service, configmap
- [ ] Create frontend deployment, service
- [ ] Create ingress with TLS
- [ ] Create secrets (don't commit real values!)
- [ ] Set up HPA for auto-scaling
- [ ] Test with: `kubectl apply -f k8s/ -R --dry-run=client`
- [ ] Deploy to cluster
- [ ] Verify pods are running: `kubectl get pods -n todo-app`
