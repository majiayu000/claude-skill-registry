---
name: kubernetes-essentials
description: Quick reference for Kubernetes core concepts and kubectl commands. This skill should be used as a refresher for basic K8s operations including pods, deployments, services, configmaps, secrets, and namespaces. Use this skill when working with Kubernetes clusters for Phase IV+ deployments.
---

# Kubernetes Essentials Skill

## Core Concepts Overview

### Kubernetes Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Control Plane                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐ │
│  │ API Server  │  │ Scheduler   │  │ Controller  │  │  etcd   │ │
│  │             │  │             │  │  Manager    │  │         │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Worker Nodes                              │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Node 1                          Node 2                      │ │
│  │ ┌─────────┐ ┌─────────┐        ┌─────────┐ ┌─────────┐     │ │
│  │ │  Pod    │ │  Pod    │        │  Pod    │ │  Pod    │     │ │
│  │ │┌───────┐│ │┌───────┐│        │┌───────┐│ │┌───────┐│     │ │
│  │ ││ Cont. ││ ││ Cont. ││        ││ Cont. ││ ││ Cont. ││     │ │
│  │ │└───────┘│ │└───────┘│        │└───────┘│ │└───────┘│     │ │
│  │ └─────────┘ └─────────┘        └─────────┘ └─────────┘     │ │
│  │      kubelet, kube-proxy            kubelet, kube-proxy    │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Key Resources

| Resource | Purpose | Shorthand |
|----------|---------|-----------|
| **Pod** | Smallest deployable unit, runs containers | `po` |
| **Deployment** | Manages ReplicaSets, handles rollouts | `deploy` |
| **Service** | Network endpoint for pods | `svc` |
| **ConfigMap** | Configuration data (non-sensitive) | `cm` |
| **Secret** | Sensitive configuration data | `secret` |
| **Namespace** | Virtual cluster isolation | `ns` |
| **Ingress** | External HTTP/S routing | `ing` |
| **PersistentVolumeClaim** | Storage request | `pvc` |

## Essential kubectl Commands

### Context and Configuration

```bash
# View current context
kubectl config current-context

# List all contexts
kubectl config get-contexts

# Switch context
kubectl config use-context my-context

# Set default namespace
kubectl config set-context --current --namespace=my-namespace
```

### Getting Information

```bash
# List resources
kubectl get pods                    # Pods in current namespace
kubectl get pods -A                 # All namespaces
kubectl get pods -o wide            # Additional details (node, IP)
kubectl get pods -o yaml            # Full YAML output
kubectl get all                     # All common resources

# Describe resources (detailed info + events)
kubectl describe pod my-pod
kubectl describe deployment my-deploy

# View logs
kubectl logs my-pod                 # Current logs
kubectl logs my-pod -f              # Follow logs
kubectl logs my-pod -c container    # Specific container
kubectl logs my-pod --previous      # Previous container (after crash)
```

### Creating Resources

```bash
# From YAML file
kubectl apply -f manifest.yaml

# Imperative creation
kubectl create deployment nginx --image=nginx
kubectl create service clusterip nginx --tcp=80:80
kubectl create configmap my-config --from-literal=key=value
kubectl create secret generic my-secret --from-literal=password=secret123

# Generate YAML without applying
kubectl create deployment nginx --image=nginx --dry-run=client -o yaml > deploy.yaml
```

### Modifying Resources

```bash
# Edit in place
kubectl edit deployment my-deploy

# Scale deployment
kubectl scale deployment my-deploy --replicas=3

# Update image
kubectl set image deployment/my-deploy container=image:v2

# Patch resource
kubectl patch deployment my-deploy -p '{"spec":{"replicas":5}}'
```

### Deleting Resources

```bash
# Delete by name
kubectl delete pod my-pod
kubectl delete deployment my-deploy

# Delete from file
kubectl delete -f manifest.yaml

# Delete all pods in namespace
kubectl delete pods --all -n my-namespace

# Force delete stuck pod
kubectl delete pod my-pod --grace-period=0 --force
```

### Executing Commands

```bash
# Run command in pod
kubectl exec my-pod -- ls /app

# Interactive shell
kubectl exec -it my-pod -- /bin/sh

# Specific container
kubectl exec -it my-pod -c my-container -- /bin/bash
```

### Port Forwarding

```bash
# Forward pod port to local
kubectl port-forward pod/my-pod 8080:80

# Forward service port
kubectl port-forward svc/my-service 8080:80
```

## Resource Manifests

### Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    app: my-app
spec:
  containers:
    - name: main
      image: nginx:1.21
      ports:
        - containerPort: 80
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 256Mi
```

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
          image: nginx:1.21
          ports:
            - containerPort: 80
          livenessProbe:
            httpGet:
              path: /health
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
```

### Service

```yaml
# ClusterIP (internal only)
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: ClusterIP
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080

---
# NodePort (external via node IP)
apiVersion: v1
kind: Service
metadata:
  name: my-nodeport
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080

---
# LoadBalancer (cloud provider LB)
apiVersion: v1
kind: Service
metadata:
  name: my-lb
spec:
  type: LoadBalancer
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-config
data:
  DATABASE_HOST: postgres
  DATABASE_PORT: "5432"
  config.json: |
    {
      "debug": true,
      "logLevel": "info"
    }
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  # base64 encoded values
  password: cGFzc3dvcmQxMjM=
  api-key: YWJjZGVmMTIzNDU2
```

### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.local
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 8000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 3000
```

## Using ConfigMaps and Secrets

### As Environment Variables

```yaml
spec:
  containers:
    - name: app
      env:
        # Single value from ConfigMap
        - name: DATABASE_HOST
          valueFrom:
            configMapKeyRef:
              name: my-config
              key: DATABASE_HOST
        # Single value from Secret
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: my-secret
              key: api-key
      # All values from ConfigMap
      envFrom:
        - configMapRef:
            name: my-config
        - secretRef:
            name: my-secret
```

### As Volumes

```yaml
spec:
  containers:
    - name: app
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
  volumes:
    - name: config-volume
      configMap:
        name: my-config
```

## Debugging Quick Reference

```bash
# Pod not starting?
kubectl describe pod my-pod          # Check Events section
kubectl get events --sort-by='.lastTimestamp'

# Container crashing?
kubectl logs my-pod --previous       # Logs from crashed container

# Network issues?
kubectl exec -it my-pod -- nslookup my-service
kubectl exec -it my-pod -- wget -qO- http://my-service:80

# Check resource usage
kubectl top pods
kubectl top nodes
```

## Resources

Refer to `references/troubleshooting.md` for common issues and solutions.
