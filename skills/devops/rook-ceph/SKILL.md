---
name: rook-ceph
description: Multi-node Rook Ceph deployment for Kubernetes production clusters. This skill should be used when deploying Ceph storage across multiple nodes with high availability. Covers Helm installation of Rook operator and Ceph cluster with production settings (3 mons, 2 mgrs, replication size 3, failure domains).
---

# Rook Ceph Multi-Node

Production Rook Ceph deployment with high availability across multiple nodes.

## Design

- 3+ nodes for high availability
- Dedicated disks on each node for Ceph OSDs
- mon.count: 3, mgr.count: 2
- Pool replication size: 3
- Failure domain: host (survives node failure)

## Prerequisites

- Kubernetes 1.30+
- 3+ nodes with dedicated raw disks
- Each node labeled for Ceph: `kubectl label node <name> ceph-node=true`

## Quick Install

```bash
# Add Rook Helm repo
helm repo add rook-release https://charts.rook.io/release
helm repo update

# Install operator
helm install --create-namespace --namespace rook-ceph \
  rook-ceph rook-release/rook-ceph

# Wait for operator
kubectl -n rook-ceph wait --for=condition=ready pod -l app=rook-ceph-operator --timeout=300s

# Install cluster (use values from references/cluster-values.md)
helm install --namespace rook-ceph rook-ceph-cluster \
  --set operatorNamespace=rook-ceph \
  rook-release/rook-ceph-cluster -f cluster-values.yaml
```

## Verify Installation

```bash
# Check pods (expect 3 mons, 2 mgrs, OSDs per disk)
kubectl -n rook-ceph get pods -o wide

# Check cluster status
kubectl -n rook-ceph get cephcluster

# Ceph health (should be HEALTH_OK)
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph status
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd tree
```

## Storage Classes

Created automatically by Helm. Verify with:

```bash
kubectl get sc
```

Default classes: `ceph-block` (RBD), `ceph-filesystem` (CephFS)

## Scaling

### Add OSD (new disk)
Update `cephClusterSpec.storage.nodes` in values and upgrade Helm release.

### Add Node
1. Label node: `kubectl label node <name> ceph-node=true`
2. Add to `storage.nodes` in values
3. Helm upgrade

## Troubleshooting

```bash
# Cluster health
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph health detail

# OSD status
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph osd status

# Pool status
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph df

# PG status (placement groups)
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph pg stat
```

## References

- `references/cluster-values.md` - Helm values for multi-node cluster
- `references/storageclass.md` - StorageClass definitions
- `references/maintenance.md` - Maintenance and operations
- `scripts/install.sh` - Automated install script
