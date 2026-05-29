---
name: storage-operators
description: Mayastor block storage and SeaweedFS object storage patterns for Kubernetes persistent data.
agents: [bolt]
triggers: [storage, mayastor, seaweedfs, pvc, csi, s3, persistent, volume]
---

# Storage Operators

Block storage (Mayastor) and object storage (SeaweedFS) for Kubernetes workloads.

## Storage Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Storage Layer                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐    ┌─────────────────────┐            │
│  │      Mayastor       │    │     SeaweedFS       │            │
│  │   (Block Storage)   │    │  (Object Storage)   │            │
│  │                     │    │                     │            │
│  │  - NVMe optimized   │    │  - S3 compatible    │            │
│  │  - CSI driver       │    │  - File uploads     │            │
│  │  - Replicated       │    │  - Backups          │            │
│  └─────────────────────┘    └─────────────────────┘            │
│           │                          │                          │
│           ▼                          ▼                          │
│    StorageClass:              S3 Endpoint:                      │
│    mayastor                   seaweedfs-filer.seaweedfs:8333    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Mayastor (Block Storage)

NVMe-optimized distributed block storage via CSI.

### StorageClass

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: mayastor
provisioner: io.openebs.csi-mayastor
parameters:
  protocol: nvmf
  repl: "2"  # Replication factor
reclaimPolicy: Delete
volumeBindingMode: Immediate
allowVolumeExpansion: true
```

### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-volume
  namespace: myapp
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: mayastor
  resources:
    requests:
      storage: 10Gi
```

### Using in Deployments

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
        - name: app
          volumeMounts:
            - name: data
              mountPath: /data
      volumes:
        - name: data
          persistentVolumeClaim:
            claimName: data-volume
```

### StatefulSet Storage

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: mayastor
        resources:
          requests:
            storage: 20Gi
```

## SeaweedFS (Object Storage)

S3-compatible object storage for files, uploads, and backups.

### S3 Endpoint

```
http://seaweedfs-filer.seaweedfs.svc:8333
```

### Create Bucket

```bash
# Using AWS CLI
aws s3 mb s3://myapp-uploads \
  --endpoint-url http://seaweedfs-filer.seaweedfs.svc:8333

# Using weed shell
kubectl exec -n seaweedfs seaweedfs-master-0 -- \
  weed shell -master=localhost:9333 -filer=seaweedfs-filer:8888 \
  -shell.command='s3.bucket.create -name myapp-uploads'
```

### Application Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
        - name: app
          env:
            - name: S3_ENDPOINT
              value: "http://seaweedfs-filer.seaweedfs.svc:8333"
            - name: S3_BUCKET
              value: "myapp-uploads"
            - name: AWS_ACCESS_KEY_ID
              valueFrom:
                secretKeyRef:
                  name: seaweedfs-s3-credentials
                  key: access-key
            - name: AWS_SECRET_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: seaweedfs-s3-credentials
                  key: secret-key
```

### SDK Usage (Node.js)

```typescript
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

const s3 = new S3Client({
  endpoint: process.env.S3_ENDPOINT,
  region: "us-east-1",
  forcePathStyle: true,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});

await s3.send(new PutObjectCommand({
  Bucket: "myapp-uploads",
  Key: "files/document.pdf",
  Body: fileBuffer,
}));
```

## Storage Selection Guide

| Use Case | Storage | Why |
|----------|---------|-----|
| Database data | Mayastor | Low latency, consistent I/O |
| Redis/Valkey | Mayastor | Fast block access |
| File uploads | SeaweedFS | S3 API, scalable |
| Backups | SeaweedFS | Cost-effective, durable |
| Logs archive | SeaweedFS | Bulk storage |
| Application state | Mayastor | POSIX filesystem |

## Validation Commands

```bash
# Check Mayastor status
kubectl get diskpools -n mayastor
kubectl get volumes -n mayastor

# Check PVCs
kubectl get pvc -A
kubectl describe pvc <name> -n <namespace>

# Check SeaweedFS
kubectl get pods -n seaweedfs
aws s3 ls --endpoint-url http://localhost:8333  # with port-forward

# Storage class
kubectl get storageclass
```

## Troubleshooting

### PVC stuck in Pending

```bash
# Check events
kubectl describe pvc <name> -n <namespace>

# Check Mayastor pools
kubectl get diskpools -n mayastor

# Check CSI driver
kubectl get pods -n mayastor -l app=mayastor-csi
```

### SeaweedFS connection issues

```bash
# Check filer status
kubectl logs -n seaweedfs -l app=seaweedfs-filer

# Test S3 connectivity
kubectl run -it --rm s3-test --image=amazon/aws-cli -- \
  s3 ls --endpoint-url http://seaweedfs-filer.seaweedfs.svc:8333
```

## Best Practices

1. **Use Mayastor for databases** - NVMe-optimized for low latency
2. **Use SeaweedFS for files** - S3 API is standard, scalable
3. **Set appropriate replication** - `repl: 2` minimum for production
4. **Monitor disk pools** - Alert on low capacity
5. **Backup critical data** - Use SeaweedFS for backup storage
6. **Size PVCs appropriately** - Expansion is supported but disruptive
