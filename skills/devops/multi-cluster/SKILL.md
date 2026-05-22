---
name: multi-cluster
description: Multi-cluster Kubernetes management, federation, and hybrid deployments
sasmp_version: "1.3.0"
eqhm_enabled: true
bonded_agent: 01-cluster-admin
bond_type: PRIMARY_BOND
capabilities: ["Cluster federation", "Cross-cluster networking", "Global load balancing", "Disaster recovery", "GitOps multi-cluster", "Service discovery", "Policy distribution", "Data replication"]
input_schema:
  type: object
  properties:
    action:
      type: string
      enum: ["federate", "connect", "replicate", "failover", "sync"]
    topology:
      type: string
      enum: ["hub-spoke", "mesh", "active-active", "active-passive"]
output_schema:
  type: object
  properties:
    cluster_status:
      type: object
    sync_status:
      type: string
    health:
      type: array
---

# Multi-Cluster Kubernetes

## Executive Summary
Production-grade multi-cluster Kubernetes management covering federation, cross-cluster networking, and disaster recovery patterns. This skill provides deep expertise in designing and operating globally distributed Kubernetes infrastructure.

## Core Competencies

### 1. Multi-Cluster Architecture

**Topology Patterns**
```
Hub-Spoke:
                    ┌─────────┐
                    │   Hub   │
                    │ Cluster │
                    └────┬────┘
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ Spoke 1 │    │ Spoke 2 │    │ Spoke 3 │
    │ (Dev)   │    │ (Stage) │    │ (Prod)  │
    └─────────┘    └─────────┘    └─────────┘

Mesh:
    ┌─────────┐          ┌─────────┐
    │Cluster 1│◄────────►│Cluster 2│
    │ (US)    │          │ (EU)    │
    └────┬────┘          └────┬────┘
         │                    │
         └────────┬───────────┘
              ┌───▼───┐
              │Cluster│
              │3 (AP) │
              └───────┘
```

### 2. ArgoCD Multi-Cluster

**ApplicationSet Generator**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: api-server
  namespace: argocd
spec:
  generators:
  - clusters:
      selector:
        matchLabels:
          env: production
  template:
    metadata:
      name: 'api-server-{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/api-server
        targetRevision: HEAD
        path: k8s/overlays/production
      destination:
        server: '{{server}}'
        namespace: production
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Register External Cluster**
```bash
# Add cluster to ArgoCD
argocd cluster add prod-cluster --name prod --kubeconfig ~/.kube/prod.yaml

# List clusters
argocd cluster list

# Verify connectivity
argocd cluster get prod
```

### 3. Cross-Cluster Networking

**Cilium Cluster Mesh**
```bash
# Enable cluster mesh on each cluster
cilium clustermesh enable --context cluster1
cilium clustermesh enable --context cluster2

# Connect clusters
cilium clustermesh connect --context cluster1 --destination-context cluster2

# Verify
cilium clustermesh status
```

**Global Service**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-server
  annotations:
    service.cilium.io/global: "true"
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: api-server
```

### 4. Disaster Recovery

**Active-Active Configuration**
```yaml
# External DNS for GSLB
apiVersion: externaldns.k8s.io/v1alpha1
kind: DNSEndpoint
metadata:
  name: api-global
spec:
  endpoints:
  - dnsName: api.example.com
    recordType: A
    targets:
    - 52.1.1.1    # US cluster
    - 35.2.2.2    # EU cluster
    setIdentifier: us-east
    recordTTL: 60
---
# Each cluster has identical deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  # ... same configuration in both clusters
```

**Velero Cross-Cluster Backup**
```bash
# Install Velero in both clusters
velero install \
  --provider aws \
  --bucket velero-backups \
  --backup-location-config region=us-east-1

# Create backup
velero backup create prod-backup \
  --include-namespaces production \
  --snapshot-volumes

# Restore in DR cluster
velero restore create --from-backup prod-backup
```

### 5. Fleet Management

**Rancher Fleet**
```yaml
apiVersion: fleet.cattle.io/v1alpha1
kind: GitRepo
metadata:
  name: api-server
  namespace: fleet-default
spec:
  repo: https://github.com/org/api-server
  branch: main
  paths:
  - k8s/
  targets:
  - clusterSelector:
      matchLabels:
        env: production
    name: production
  - clusterSelector:
      matchLabels:
        env: staging
    name: staging
```

## Integration Patterns

### Uses skill: **cluster-admin**
- Cluster provisioning
- Certificate management

### Coordinates with skill: **gitops**
- Multi-cluster GitOps
- ApplicationSets

### Works with skill: **storage-networking**
- Cross-cluster networking
- Data replication

## Troubleshooting Guide

### Decision Tree: Multi-Cluster Issues

```
Multi-Cluster Issue?
│
├── Cluster unreachable
│   ├── Check network connectivity
│   ├── Verify kubeconfig
│   └── Check cluster health
│
├── Sync failures
│   ├── Check ArgoCD logs
│   ├── Verify RBAC permissions
│   └── Check resource conflicts
│
└── Service discovery fails
    ├── Check mesh connectivity
    ├── Verify DNS configuration
    └── Check NetworkPolicies
```

### Debug Commands

```bash
# ArgoCD cluster status
argocd cluster list
argocd app list --dest-server <server>

# Cilium mesh status
cilium clustermesh status
cilium connectivity test

# Cross-cluster DNS
kubectl run debug --rm -it --image=nicolaka/netshoot -- \
  nslookup <service>.default.svc.clusterset.local
```

## Common Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Network latency | Use regional clusters |
| State sync | Eventually consistent design |
| Failover delay | Health checks, DNS TTL |
| Config drift | GitOps, policy enforcement |

## Success Criteria

| Metric | Target |
|--------|--------|
| Cross-cluster latency | <50ms (regional) |
| Failover time | <2 minutes |
| Config consistency | 100% |
| Cluster availability | 99.99% |

## Resources
- [ArgoCD Multi-Cluster](https://argo-cd.readthedocs.io/en/stable/user-guide/clusters/)
- [Cilium Cluster Mesh](https://docs.cilium.io/en/stable/network/clustermesh/)
