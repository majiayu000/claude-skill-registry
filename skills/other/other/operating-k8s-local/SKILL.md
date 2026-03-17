---
name: operating-k8s-local
description: |
  Operates local Kubernetes clusters with Minikube for development and testing.
  Use when setting up local K8s, deploying applications locally, or debugging K8s issues.
  Covers Minikube, kubectl essentials, local image loading, and networking.
---

# Operating K8s Local

## Quick Start

```bash
# Start cluster with resources
minikube start --memory=8192 --cpus=4

# Enable essential addons
minikube addons enable ingress
minikube addons enable metrics-server

# Point Docker to Minikube
eval $(minikube docker-env)

# Build and deploy
docker build -t myapp:local .
kubectl apply -f k8s/
```

## Minikube Essentials

### Cluster Management

```bash
minikube start                          # Start with defaults
minikube start --memory=8192 --cpus=4   # With resources
minikube start --driver=docker          # Specific driver
minikube status                         # Check status
minikube stop                           # Stop (preserves state)
minikube delete                         # Delete completely
```

### Multiple Clusters

```bash
minikube start -p my-cluster    # Named cluster
minikube profile my-cluster     # Switch clusters
minikube profile list           # List all
```

### Addons

```bash
minikube addons list                    # List available
minikube addons enable ingress          # REQUIRED for external access
minikube addons enable metrics-server   # For kubectl top
minikube addons enable dashboard        # Web UI
minikube addons enable storage-provisioner  # For PVCs
```

### Accessing Services

```bash
# Method 1: NodePort
minikube service my-service --url

# Method 2: LoadBalancer (requires tunnel)
minikube tunnel  # Run in separate terminal

# Method 3: Port forward
kubectl port-forward svc/my-service 8080:80
```

### Using Local Docker Images

```bash
# Point to Minikube's Docker
eval $(minikube docker-env)

# Build directly into Minikube
docker build -t my-app:local .

# Use imagePullPolicy: Never in manifests
# Reset to local Docker
eval $(minikube docker-env -u)
```

## kubectl Essentials

### Context Management

```bash
kubectl config current-context              # Current context
kubectl config get-contexts                 # List all
kubectl config use-context minikube         # Switch
kubectl config set-context --current --namespace=my-ns  # Set default ns
```

### Getting Information

```bash
kubectl get pods                    # Current namespace
kubectl get pods -A                 # All namespaces
kubectl get pods -o wide            # With node/IP
kubectl get all                     # All resources
kubectl describe pod my-pod         # Detailed info
kubectl get events --sort-by='.lastTimestamp'  # Recent events
```

### Logs

```bash
kubectl logs my-pod                 # Current logs
kubectl logs my-pod -f              # Follow
kubectl logs my-pod -c container    # Specific container
kubectl logs my-pod --previous      # After crash
kubectl logs my-pod --tail=50       # Last 50 lines
```

### Creating Resources

```bash
kubectl apply -f manifest.yaml
kubectl create deployment nginx --image=nginx
kubectl create configmap my-config --from-literal=key=value
kubectl create secret generic my-secret --from-literal=password=secret

# Generate YAML
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml
```

### Modifying Resources

```bash
kubectl edit deployment my-deploy
kubectl scale deployment my-deploy --replicas=3
kubectl set image deployment/my-deploy container=image:v2
kubectl rollout restart deployment/my-deploy
```

### Debugging

```bash
kubectl exec -it my-pod -- /bin/sh          # Shell into pod
kubectl exec my-pod -- env                   # Run command
kubectl port-forward pod/my-pod 8080:80     # Forward port
kubectl top pods                             # Resource usage
kubectl top nodes
```

## Resource Manifests

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deploy
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: main
          image: my-app:local
          imagePullPolicy: Never  # For local images
          ports:
            - containerPort: 8000
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP  # or NodePort, LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8000
```

### ConfigMap & Secret

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  DATABASE_HOST: postgres
  DATABASE_PORT: "5432"
---
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
stringData:
  password: mysecretpassword
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
```

## Local Development Workflow

```bash
# 1. Start Minikube
minikube start --memory=8192 --cpus=4

# 2. Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# 3. Point to Minikube Docker
eval $(minikube docker-env)

# 4. Build images
docker build -t myapp/api:local ./api
docker build -t myapp/web:local ./web

# 5. Deploy
kubectl apply -f k8s/

# 6. Access
minikube service myapp-web --url
# Or with ingress:
echo "$(minikube ip) myapp.local" | sudo tee -a /etc/hosts
```

## Debugging Quick Reference

```bash
# Pod not starting?
kubectl describe pod my-pod      # Check Events section

# Container crashing?
kubectl logs my-pod --previous   # Logs from crashed container

# Network issues?
kubectl exec -it my-pod -- nslookup my-service
kubectl exec -it my-pod -- wget -qO- http://my-service:80

# Resource issues?
kubectl top pods
kubectl top nodes
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `containerizing-applications` - Docker and Helm charts
- `deploying-cloud-k8s` - Cloud Kubernetes deployment
