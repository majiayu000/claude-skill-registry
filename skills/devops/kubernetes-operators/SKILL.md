---
name: kubernetes-operators
description: Kubernetes infrastructure patterns including operators, Helm, GitOps, and component provisioning.
agents: [bolt]
triggers: [kubernetes, k8s, helm, argocd, operator, infrastructure]
---

# Kubernetes Infrastructure Patterns

Infrastructure provisioning using Kubernetes operators, Helm, and GitOps practices.

## Core Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| Container | Docker | Image building |
| Orchestration | Kubernetes | Workload management |
| Package Manager | Helm | Chart management |
| GitOps | ArgoCD, Kustomize | Declarative deployments |
| CI/CD | GitHub Actions, Argo Workflows | Automation |
| Monitoring | Prometheus, Grafana, Loki | Observability |
| Networking | Ingress, NetworkPolicies | Traffic management |

## Context7 Library IDs

Query these for current best practices:

- **ArgoCD**: `/argoproj/argo-cd`
- **Helm**: `/helm/helm`

## Execution Rules

1. **GitOps first.** All changes through git, not `kubectl apply` ad-hoc
2. **Helm best practices.** Values.yaml for configuration, templates for logic
3. **Security.** No secrets in code, use External Secrets Operator
4. **Idempotent.** All operations safe to retry
5. **Validate.** Always `helm template` and `kubectl diff` before apply

## Available Operators

| Type | Operator | CRD Kind | Namespace |
|------|----------|----------|-----------|
| PostgreSQL | CloudNative-PG | `Cluster` | databases |
| Redis/Valkey | Redis Operator | `Redis` | databases |
| S3/Storage | SeaweedFS | Helm | seaweedfs |
| Kafka | Strimzi | `Kafka` | kafka |
| MongoDB | Percona | `PerconaServerMongoDB` | databases |
| MySQL | Percona | `PerconaXtraDBCluster` | databases |
| NATS | NATS Helm | Helm | nats |
| RabbitMQ | RabbitMQ Operator | `RabbitmqCluster` | messaging |

## Size Presets

| Size | CPU Request | Memory | Storage | Replicas |
|------|-------------|--------|---------|----------|
| small | 100m | 256Mi | 5Gi | 1 |
| medium | 500m | 1Gi | 20Gi | 1-2 |
| large | 1000m | 4Gi | 100Gi | 3 |

## Infrastructure Provisioning Process

### Step 1: Parse Requirements

Extract infrastructure from task XML:

```xml
<infrastructure>
    <component type="postgresql" name="app-db">
        <size>small</size>
        <replicas>1</replicas>
        <database>app_production</database>
    </component>
</infrastructure>
```

### Step 2: Generate Manifests

Create manifests in the `infra/` directory:

```
infra/
├── postgresql/
│   └── cluster.yaml
├── valkey/
│   └── redis.yaml
├── seaweedfs/
│   └── bucket-init.yaml
└── kustomization.yaml
```

### Step 3: PostgreSQL Example

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: app-db
  namespace: databases
spec:
  instances: 1
  storage:
    size: 5Gi
    storageClass: mayastor
  bootstrap:
    initdb:
      database: app_production
      owner: app_user
```

### Step 4: Valkey/Redis Example

```yaml
apiVersion: redis.redis.opstreelabs.in/v1beta2
kind: Redis
metadata:
  name: app-cache
  namespace: databases
spec:
  kubernetesConfig:
    image: redis:7-alpine
  storage:
    volumeClaimTemplate:
      spec:
        storageClassName: mayastor
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
```

### Step 5: Apply and Wait

```bash
# Apply manifests
kubectl apply -k infra/

# Wait for PostgreSQL
kubectl wait --for=condition=Ready cluster/app-db -n databases --timeout=300s

# Wait for Valkey
kubectl wait --for=condition=Ready redis/app-cache -n databases --timeout=300s
```

### Step 6: Create Infrastructure ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-infra-config
  namespace: app
  labels:
    cto.platform/type: infrastructure-config
data:
  DATABASE_URL: postgresql://app_user:$DB_PASSWORD@app-db-rw.databases.svc:5432/app
  DATABASE_HOST: app-db-rw.databases.svc
  DATABASE_PORT: "5432"
  DATABASE_NAME: app
  
  REDIS_URL: redis://app-cache.databases.svc:6379
  REDIS_HOST: app-cache.databases.svc
  REDIS_PORT: "6379"
  
  S3_ENDPOINT: http://seaweedfs-filer.seaweedfs.svc:8333
  S3_BUCKET: app-uploads
```

## Validation Commands

```bash
# Helm validation
helm lint ./chart
helm template ./chart --debug

# Kubernetes validation
kubectl diff -f manifest.yaml
kubeval manifest.yaml

# ArgoCD
argocd app diff app-name

# Check status
kubectl get all -n databases
kubectl get cluster -n databases -o wide
kubectl get redis -n databases
```

## Error Handling

If provisioning fails:

1. Check operator logs: `kubectl logs -n operators -l app.kubernetes.io/name=<operator>`
2. Describe the resource: `kubectl describe cluster/app-db -n databases`
3. Check events: `kubectl get events -n databases --sort-by='.lastTimestamp'`
4. Verify storage class: `kubectl get storageclass mayastor`

## Guidelines

- Use operators for stateful services (databases, caches)
- Store connection details in ConfigMaps for other agents
- Always wait for resources to be ready before completing
- Document connection information in infra/README.md
- Use GitOps (ArgoCD) for production deployments
- Never hardcode secrets in manifests
