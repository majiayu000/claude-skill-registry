---
name: kubernetes-helm-deployment
description: Kubernetes deployment patterns with Helm charts. Covers deployments, services, ConfigMaps, Secrets, Dapr sidecar injection, health probes, and resource management.
---

# Kubernetes & Helm Deployment Skill

Kubernetes deployment patterns using Helm charts for containerized applications.

## Quick Start

### Installation

```bash
# Helm 3.x
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# kubectl
# See: https://kubernetes.io/docs/tasks/tools/
```

## 1. Helm Chart Structure

### Chart Directory

```
todo-app/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── values-minikube.yaml # Minikube-specific values
├── values-oke.yaml     # OKE-specific values
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    └── ingress.yaml
```

### Chart.yaml

```yaml
apiVersion: v2
name: todo-app
description: Todo Chatbot Application
type: application
version: 1.0.0
appVersion: "1.0.0"
```

## 2. Deployment Template

### Basic Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.backend.name }}
  labels:
    app: {{ .Values.backend.name }}
spec:
  replicas: {{ .Values.backend.replicas }}
  selector:
    matchLabels:
      app: {{ .Values.backend.name }}
  template:
    metadata:
      labels:
        app: {{ .Values.backend.name }}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "{{ .Values.backend.name }}"
        dapr.io/app-port: "{{ .Values.backend.port }}"
        dapr.io/config: "dapr-config"
    spec:
      containers:
        - name: {{ .Values.backend.name }}
          image: {{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}
          ports:
            - containerPort: {{ .Values.backend.port }}
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: database-secrets
                  key: url
            - name: DAPR_HTTP_PORT
              value: "3500"
          resources:
            requests:
              cpu: {{ .Values.backend.resources.requests.cpu }}
              memory: {{ .Values.backend.resources.requests.memory }}
            limits:
              cpu: {{ .Values.backend.resources.limits.cpu }}
              memory: {{ .Values.backend.resources.limits.memory }}
          livenessProbe:
            httpGet:
              path: /health/live
              port: {{ .Values.backend.port }}
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: {{ .Values.backend.port }}
            initialDelaySeconds: 5
            periodSeconds: 5
```

## 3. Service Template

### Service for Backend

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ .Values.backend.name }}
  labels:
    app: {{ .Values.backend.name }}
spec:
  type: {{ .Values.backend.service.type }}
  ports:
    - port: {{ .Values.backend.service.port }}
      targetPort: {{ .Values.backend.port }}
      protocol: TCP
  selector:
    app: {{ .Values.backend.name }}
```

## 4. Dapr Sidecar Injection

### Dapr Annotations

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "backend"
  dapr.io/app-port: "8000"
  dapr.io/config: "dapr-config"
  dapr.io/log-level: "info"
  dapr.io/log-as-json: "true"
```

### Dapr Configuration

```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: dapr-config
  namespace: default
spec:
  tracing:
    samplingRate: "1.0"
    zipkin:
      endpointAddress: "http://zipkin:9411/api/v2/spans"
  metrics:
    enabled: true
```

## 5. Values Files

### values.yaml (Default)

```yaml
backend:
  name: backend
  replicas: 2
  port: 8000
  image:
    repository: todo-backend
    tag: latest
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      cpu: "100m"
      memory: "256Mi"
    limits:
      cpu: "500m"
      memory: "512Mi"

frontend:
  name: frontend
  replicas: 2
  port: 3000
  image:
    repository: todo-frontend
    tag: latest
  service:
    type: ClusterIP
    port: 3000
```

### values-minikube.yaml

```yaml
backend:
  service:
    type: NodePort
  resources:
    requests:
      cpu: "50m"
      memory: "128Mi"
    limits:
      cpu: "200m"
      memory: "256Mi"

frontend:
  service:
    type: NodePort
```

### values-oke.yaml

```yaml
backend:
  service:
    type: LoadBalancer
  resources:
    requests:
      cpu: "200m"
      memory: "512Mi"
    limits:
      cpu: "1000m"
      memory: "1Gi"

frontend:
  service:
    type: LoadBalancer
```

## 6. ConfigMap

### ConfigMap Template

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.app.name }}-config
data:
  app.env: "production"
  log.level: "info"
  kafka.brokers: "{{ .Values.kafka.brokers }}"
```

## 7. Secrets

### Secret Template

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: database-secrets
type: Opaque
stringData:
  url: "postgresql://user:password@host:5432/db"
  password: "secret-password"
```

### Using Dapr Secrets Instead

```yaml
# Reference Dapr secret store
env:
  - name: DATABASE_PASSWORD
    value: "dapr-secret-store:database-secrets:password"
```

## 8. Microservices Deployment

### Recurring Task Service

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: recurring-task-service
spec:
  replicas: 2
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "recurring-task-service"
        dapr.io/app-port: "8001"
    spec:
      containers:
        - name: recurring-task-service
          image: recurring-task-service:latest
          ports:
            - containerPort: 8001
          env:
            - name: DAPR_HTTP_PORT
              value: "3500"
```

### Notification Service

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: notification-service
spec:
  replicas: 2
  template:
    metadata:
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "notification-service"
        dapr.io/app-port: "8002"
    spec:
      containers:
        - name: notification-service
          image: notification-service:latest
          ports:
            - containerPort: 8002
```

## 9. Health Probes

### Liveness Probe

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

### Readiness Probe

```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

## 10. Resource Management

### Resource Requests and Limits

```yaml
resources:
  requests:
    cpu: "100m"      # Minimum CPU
    memory: "256Mi"  # Minimum memory
  limits:
    cpu: "500m"      # Maximum CPU
    memory: "512Mi"  # Maximum memory
```

### Always-Free Tier (OKE)

```yaml
# OKE always-free tier constraints
resources:
  requests:
    cpu: "200m"
    memory: "512Mi"
  limits:
    cpu: "2000m"  # 2 OCPUs max
    memory: "2Gi"  # 24GB total / 12 pods
```

## 11. Network Policies

### Network Policy Template

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: dapr-sidecar
      ports:
        - protocol: TCP
          port: 3500
    - to:
        - namespaceSelector:
            matchLabels:
              name: postgresql
      ports:
        - protocol: TCP
          port: 5432
```

## 12. Deployment Commands

### Install Chart

```bash
# Install with default values
helm install todo-app ./helm/todo-app

# Install with custom values
helm install todo-app ./helm/todo-app -f values-oke.yaml

# Install with overrides
helm install todo-app ./helm/todo-app \
  --set backend.replicas=3 \
  --set frontend.image.tag=v1.0.0
```

### Upgrade Chart

```bash
# Upgrade deployment
helm upgrade todo-app ./helm/todo-app -f values-oke.yaml

# Rollback on failure
helm rollback todo-app
```

### Uninstall Chart

```bash
helm uninstall todo-app
```

## Best Practices

### 1. Use Values Files for Environment-Specific Config

```bash
# Development
helm install todo-app ./helm/todo-app -f values-minikube.yaml

# Production
helm install todo-app ./helm/todo-app -f values-oke.yaml
```

### 2. Always Set Resource Limits

```yaml
resources:
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### 3. Enable Dapr Sidecar

```yaml
annotations:
  dapr.io/enabled: "true"
  dapr.io/app-id: "backend"
```

### 4. Health Probes

Always include liveness and readiness probes:

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
```

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Dapr Kubernetes](https://docs.dapr.io/operations/hosting/kubernetes/)

