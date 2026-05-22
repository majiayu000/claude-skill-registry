---
name: kubernetes-resources
description: Use when managing Kubernetes resources including deployments, services, configmaps, and secrets.
allowed-tools: []
---

# Kubernetes Resources

Understanding Kubernetes resource types and their relationships.

## Core Resources

### Pods

The smallest deployable unit in Kubernetes:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: app
    image: nginx:1.21
```

### ReplicaSets

Maintains a stable set of replica Pods:

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-replicaset
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    # Pod template
```

### Deployments

Manages ReplicaSets and provides declarative updates:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  # ...
```

## Networking Resources

### Services

Exposes Pods to network traffic:

- **ClusterIP**: Internal cluster access only
- **NodePort**: Exposes on each Node's IP
- **LoadBalancer**: Cloud provider load balancer
- **ExternalName**: DNS CNAME record

```yaml
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
```

### Ingress

HTTP/HTTPS routing to services:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: myapp.example.com
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

## Storage Resources

### PersistentVolume

Cluster-level storage resource:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: standard
```

### PersistentVolumeClaim

Request for storage:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

## Configuration Resources

### ConfigMaps

Non-sensitive configuration data:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  config.json: |
    {
      "key": "value"
    }
```

### Secrets

Sensitive information:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  username: admin
  password: secret123
```

## Workload Resources

### StatefulSet

For stateful applications:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    # Pod template
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```

### DaemonSet

Runs a Pod on every Node:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: monitoring-agent
spec:
  selector:
    matchLabels:
      name: monitoring-agent
  template:
    # Pod template
```

### Job

Run-to-completion tasks:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: batch-job
spec:
  template:
    spec:
      containers:
      - name: job
        image: busybox
        command: ["echo", "Hello"]
      restartPolicy: Never
  backoffLimit: 4
```

### CronJob

Scheduled jobs:

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scheduled-job
spec:
  schedule: "0 0 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: job
            image: busybox
            command: ["echo", "Daily task"]
          restartPolicy: OnFailure
```
