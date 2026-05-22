---
name: deploying-postgres-k8s
description: |
  Deploys PostgreSQL on Kubernetes using the CloudNativePG operator with automated failover.
  Use when setting up PostgreSQL for production workloads, high availability, or local K8s development.
  Covers operator installation, cluster creation, connection secrets, and backup configuration.
  NOT when using managed Postgres (Neon, RDS, Cloud SQL) or simple Docker containers.
---

# Deploying PostgreSQL on Kubernetes

Deploy production-ready PostgreSQL clusters using CloudNativePG operator (v1.28+) with automated failover.

## Quick Start

```bash
# 1. Install CloudNativePG operator
kubectl apply --server-side -f \
  https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.28/releases/cnpg-1.28.0.yaml

# 2. Wait for operator
kubectl rollout status deployment -n cnpg-system cnpg-controller-manager

# 3. Deploy PostgreSQL cluster
kubectl apply -f - <<EOF
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: pg-cluster
spec:
  instances: 3
  storage:
    size: 10Gi
EOF

# 4. Wait for cluster
kubectl wait cluster/pg-cluster --for=condition=Ready --timeout=300s
```

## Operator Installation

### Direct Manifest (Recommended)

```bash
kubectl apply --server-side -f \
  https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.28/releases/cnpg-1.28.0.yaml

# Verify
kubectl rollout status deployment -n cnpg-system cnpg-controller-manager
kubectl get pods -n cnpg-system
```

### Helm Installation

```bash
helm repo add cnpg https://cloudnative-pg.github.io/charts
helm repo update

helm upgrade --install cnpg \
  --namespace cnpg-system \
  --create-namespace \
  cnpg/cloudnative-pg
```

### Namespace-Scoped (Enhanced Security)

```bash
helm upgrade --install cnpg \
  --namespace cnpg-system \
  --create-namespace \
  --set config.clusterWide=false \
  cnpg/cloudnative-pg
```

## Cluster Configurations

### Development (Single Instance)

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: pg-dev
spec:
  instances: 1
  imageName: ghcr.io/cloudnative-pg/postgresql:17.2
  primaryUpdateStrategy: unsupervised
  storage:
    size: 5Gi
  postgresql:
    parameters:
      max_connections: "100"
      shared_buffers: "256MB"
```

### Production (HA with 3 Replicas)

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: pg-production
spec:
  instances: 3
  imageName: ghcr.io/cloudnative-pg/postgresql:17.2
  primaryUpdateStrategy: unsupervised

  storage:
    storageClass: standard
    size: 100Gi

  resources:
    requests:
      memory: "2Gi"
      cpu: "1"
    limits:
      memory: "4Gi"
      cpu: "2"

  postgresql:
    parameters:
      max_connections: "200"
      shared_buffers: "1GB"
      effective_cache_size: "3GB"
      maintenance_work_mem: "256MB"
      checkpoint_completion_target: "0.9"
      wal_buffers: "16MB"
      default_statistics_target: "100"
      random_page_cost: "1.1"
      effective_io_concurrency: "200"

  affinity:
    podAntiAffinityType: required  # Spread across nodes

  monitoring:
    enablePodMonitor: true
```

### With Bootstrap Database

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: pg-cluster
spec:
  instances: 3
  storage:
    size: 10Gi

  bootstrap:
    initdb:
      database: learnflow
      owner: app_user
      secret:
        name: app-user-secret
```

Create the secret first:

```bash
kubectl create secret generic app-user-secret \
  --from-literal=username=app_user \
  --from-literal=password=$(openssl rand -hex 16)
```

## Connection Secrets

CloudNativePG automatically creates connection secrets:

| Secret | Contents |
|--------|----------|
| `pg-cluster-app` | App credentials (recommended) |
| `pg-cluster-superuser` | Superuser credentials |

### Get Connection String

```bash
# Get app credentials
kubectl get secret pg-cluster-app -o jsonpath='{.data.uri}' | base64 -d

# Get superuser credentials (admin tasks only)
kubectl get secret pg-cluster-superuser -o jsonpath='{.data.uri}' | base64 -d
```

### Use in Deployment

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: pg-cluster-app
        key: uri
```

## Service Endpoints

| Service | Port | Use |
|---------|------|-----|
| `pg-cluster-rw` | 5432 | Read-Write (primary) |
| `pg-cluster-ro` | 5432 | Read-Only (replicas) |
| `pg-cluster-r` | 5432 | Any instance |

### Connect from Another Namespace

```yaml
env:
  - name: DATABASE_URL
    value: "postgresql://app_user:password@pg-cluster-rw.default.svc.cluster.local:5432/learnflow"
```

## Database Operations

### Connect with psql

```bash
# Using kubectl cnpg plugin (recommended)
kubectl cnpg psql pg-cluster -- -c "SELECT version();"

# Or directly
kubectl exec -it pg-cluster-1 -- psql -U postgres
```

### Create Database and User

```bash
kubectl exec -it pg-cluster-1 -- psql -U postgres <<EOF
CREATE DATABASE myapp;
CREATE USER myapp_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE myapp TO myapp_user;
\c myapp
GRANT ALL ON SCHEMA public TO myapp_user;
EOF
```

### Run Migrations

```bash
# From local machine
kubectl port-forward svc/pg-cluster-rw 5432:5432 &
DATABASE_URL="postgresql://postgres:password@localhost:5432/learnflow" alembic upgrade head
```

## Backup Configuration

### Backup to S3

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: pg-cluster
spec:
  instances: 3
  storage:
    size: 10Gi

  backup:
    barmanObjectStore:
      destinationPath: "s3://my-bucket/pg-backups"
      s3Credentials:
        accessKeyId:
          name: s3-creds
          key: ACCESS_KEY_ID
        secretAccessKey:
          name: s3-creds
          key: SECRET_ACCESS_KEY
      wal:
        compression: gzip
      data:
        compression: gzip
    retentionPolicy: "30d"
```

### Schedule Backups

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: ScheduledBackup
metadata:
  name: pg-backup-daily
spec:
  schedule: "0 0 * * *"  # Daily at midnight
  backupOwnerReference: cluster
  cluster:
    name: pg-cluster
```

## Monitoring

### Check Cluster Status

```bash
kubectl get cluster pg-cluster
kubectl describe cluster pg-cluster
kubectl get pods -l cnpg.io/cluster=pg-cluster
```

### View Logs

```bash
kubectl logs pg-cluster-1 -f
kubectl logs -l cnpg.io/cluster=pg-cluster --all-containers
```

### Prometheus Metrics

With `enablePodMonitor: true`, metrics available at:
- `cnpg_backends_total` - Active connections
- `cnpg_pg_replication_lag_seconds` - Replica lag
- `cnpg_pg_database_size_bytes` - Database size

## Troubleshooting

### Cluster Not Ready

```bash
kubectl describe cluster pg-cluster
kubectl get pods -l cnpg.io/cluster=pg-cluster
kubectl logs pg-cluster-1
```

### Connection Issues

```bash
# Test connectivity
kubectl run pg-client --rm -it --restart=Never \
  --image=postgres:17 -- \
  psql "postgresql://app_user:password@pg-cluster-rw:5432/learnflow" -c "SELECT 1;"
```

### Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| PVC pending | No storage class | Add `storageClass` to spec |
| Connection refused | Wrong service name | Use `cluster-rw` for writes |
| Auth failed | Wrong credentials | Check secret `cluster-app` |
| Replica lag high | Heavy writes | Scale up, increase resources |

## Cleanup

```bash
# Delete cluster (keeps PVCs by default)
kubectl delete cluster pg-cluster

# Delete PVCs (data loss!)
kubectl delete pvc -l cnpg.io/cluster=pg-cluster

# Remove operator
kubectl delete -f \
  https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.28/releases/cnpg-1.28.0.yaml
```

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `operating-k8s-local` - Local Minikube cluster setup
- `scaffolding-fastapi-dapr` - FastAPI services with SQLModel
- `deploying-kafka-k8s` - Kafka for event-driven architecture