---
name: operational-excellence
description: Use when implementing Kubernetes cost visibility (OpenCost, VPA), backup/disaster recovery (Velero, RTO/RPO), or chaos engineering (Chaos Mesh). Triggers on cost optimization, right-sizing, FinOps, backup schedules, restore procedures, resilience testing, game days. NOT for basic resource requests/limits (Ch50) or HPA/KEDA autoscaling (Ch56).
---

# Operational Excellence

## Persona

You are an SRE/FinOps expert who understands that operational excellence means balancing cost efficiency with disaster preparedness and system resilience. You've managed production Kubernetes clusters and know that cost savings mean nothing if systems can't recover from failure.

## Decision Tree

```
What operational task?
├── Cost Visibility/Optimization
│   ├── Need to see where money goes? → OpenCost (L03)
│   ├── Pods over/under-provisioned? → VPA recommendations (L02)
│   ├── Need budget alerts? → FinOps practices (L04)
│   └── Team-level billing? → Cost allocation labels (L04)
│
├── Backup & Disaster Recovery
│   ├── Need namespace backups? → Velero Schedule (L06)
│   ├── Defining recovery requirements? → RTO vs RPO analysis (L05)
│   ├── Database-aware backups? → Velero hooks (L06)
│   └── Following 3-2-1 rule? → Multi-location storage (L05)
│
├── Resilience Testing
│   ├── Test pod failure recovery? → PodChaos (L07)
│   ├── Test network partitions? → NetworkChaos (L07)
│   ├── Planned resilience validation? → Game Day (L07)
│   └── Recurring chaos tests? → Chaos Mesh Schedule (L07)
│
└── Compliance
    └── Data residency requirements? → Data sovereignty (L08)
```

## Core Technologies

### VPA (Vertical Pod Autoscaler)

**Purpose**: Right-size pods based on actual usage

**Modes**:
| Mode | Behavior | When to Use |
|------|----------|-------------|
| `Off` | Generate recommendations only | Production first steps; validate before acting |
| `Initial` | Apply to new pods only | Conservative; existing pods unchanged |
| `Recreate` | Evict and recreate pods | After validation; when restarts acceptable |

**VPA + HPA Coexistence**:
- NEVER use VPA Recreate/Auto with HPA on same metrics (CPU/memory)
- Safe pattern: VPA in Off mode + HPA on custom metrics (requests/sec)
- Alternative: VPA manages memory, HPA manages CPU

**Example CRD**:
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: task-api-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: task-api
  updatePolicy:
    updateMode: "Off"  # Start here
  resourcePolicy:
    containerPolicies:
    - containerName: task-api
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 2000m
        memory: 2Gi
```

### OpenCost

**Purpose**: CNCF cost visibility for Kubernetes

**Key Concepts**:
- Prometheus integration for metrics
- Cost allocation by namespace, label, pod
- Formula: `max(request, usage) × hourly_rate`
- Idle cost = provisioned - allocated

**FinOps Progression**:
1. **Visibility (Showback)**: Report costs to teams (builds trust)
2. **Allocation**: Map to business entities via labels
3. **Chargeback**: Formal billing to cost centers

**Cost Allocation Labels** (add to all resources):
```yaml
labels:
  team: product-team
  app: task-api
  environment: production
  cost-center: engineering
```

**API Query Pattern**:
```bash
curl -G http://opencost:9003/allocation \
  -d window=7d \
  -d aggregate=namespace \
  -d shareIdle=true
```

### Velero

**Purpose**: Kubernetes backup and disaster recovery (CNCF project)

**Key CRDs**:
- `Backup`: On-demand backup
- `Restore`: Restore from backup
- `Schedule`: Recurring backups (cron)
- `BackupStorageLocation`: Where backups go (S3, GCS, MinIO)

**RTO vs RPO**:
| Concept | Definition | Velero Impact |
|---------|------------|---------------|
| RPO (Recovery Point Objective) | Max data loss acceptable | Schedule frequency |
| RTO (Recovery Time Objective) | Max downtime acceptable | Restore speed |

**3-2-1 Backup Rule**:
- 3 copies of data
- 2 different storage types
- 1 off-site location

**Schedule Example**:
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: task-api-daily
  namespace: velero
spec:
  schedule: "0 2 * * *"  # 2 AM daily
  template:
    includedNamespaces:
      - production
    snapshotVolumes: true
    ttl: 720h  # 30-day retention
    hooks:
      resources:
        - name: db-freeze
          includedNamespaces: [production]
          pre:
            - exec:
                container: postgres
                command: ["/bin/sh", "-c", "pg_dump -U app -d taskdb > /tmp/backup.sql"]
                onError: Fail
                timeout: 60s
```

### Chaos Mesh

**Purpose**: CNCF chaos engineering for Kubernetes

**Experiment Types**:
| CRD | What It Does |
|-----|--------------|
| `PodChaos` | Kill pods, container failures |
| `NetworkChaos` | Delay, loss, partition |
| `IOChaos` | I/O latency, failures |
| `StressChaos` | CPU/memory stress |

**Safety Features**:
- Namespace filtering: Only annotated namespaces
- RBAC authorization
- Duration limits
- Selectors for precise targeting

**PodChaos Example**:
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: task-api-pod-kill
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces: [staging]  # Start in staging!
    labelSelectors:
      app: task-api
  duration: "30s"
```

**Game Day Pattern**:
1. Define hypothesis: "Task API recovers within 30s after pod kill"
2. Set up monitoring/dashboards
3. Run experiment in staging first
4. Observe and document behavior
5. Iterate: fix issues, re-test
6. Graduate to production (off-peak)

## Prerequisites

- Kubernetes 1.21+
- Helm 3+
- Prometheus (for OpenCost and metrics)
- Metrics Server (for VPA)
- Object storage (S3, MinIO) for Velero

## Safety Guardrails

**Cost**:
- Start with VPA Off mode; validate recommendations before Recreate
- Never enable chargeback without validated showback first
- Review cost data for 1-2 weeks before trusting reports

**Backup**:
- Always test restore procedures before trusting backups
- Validate restore in non-production environment
- Enable encryption and immutability for backup storage
- Verify RPO/RTO requirements match business needs

**Chaos**:
- NEVER run chaos in production without testing in staging first
- Start with minimal scope (one pod, short duration)
- IOChaos can damage data - use with extreme caution
- Have runbooks ready before chaos experiments
- Schedule chaos during low-impact windows

## Task API Example

Complete operational excellence for Task API:

### 1. VPA for Right-Sizing
```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: task-api-vpa
  namespace: production
  labels:
    team: product-team
    app: task-api
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: task-api
  updatePolicy:
    updateMode: "Off"  # Recommendations only
```

### 2. Cost Allocation Labels
```yaml
# Add to Deployment
metadata:
  labels:
    team: product-team
    app: task-api
    environment: production
    cost-center: engineering
```

### 3. Daily Backup Schedule
```yaml
apiVersion: velero.io/v1
kind: Schedule
metadata:
  name: task-api-daily-backup
  namespace: velero
spec:
  schedule: "0 2 * * *"
  template:
    includedNamespaces: [production]
    includedResources: ["*"]
    snapshotVolumes: true
    ttl: 720h
```

### 4. Resilience Test
```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: task-api-resilience-test
  namespace: chaos-mesh
spec:
  action: pod-kill
  mode: one
  selector:
    namespaces: [staging]
    labelSelectors:
      app: task-api
  duration: "60s"
```

## Installation Commands

```bash
# VPA
helm repo add fairwinds-stable https://charts.fairwinds.com/stable
helm install vpa fairwinds-stable/vpa -n vpa --create-namespace

# OpenCost
helm repo add opencost https://opencost.github.io/opencost-helm-chart
helm install opencost opencost/opencost -n opencost --create-namespace

# Velero (with MinIO for local)
helm repo add vmware-tanzu https://vmware-tanzu.github.io/helm-charts
helm install velero vmware-tanzu/velero -n velero --create-namespace \
  --set configuration.backupStorageLocation.bucket=velero-backups \
  --set configuration.backupStorageLocation.config.s3Url=http://minio:9000

# Chaos Mesh
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh -n chaos-mesh --create-namespace
```
