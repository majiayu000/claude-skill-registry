---
name: kubernetes-operations
description: |
  Kubernetes and OpenShift cluster operations, maintenance, and lifecycle management. Use this skill when:
  (1) Performing cluster upgrades (K8s, OCP, EKS, GKE, AKS)
  (2) Backup and disaster recovery (etcd, Velero, cluster state)
  (3) Node management: drain, cordon, scaling, replacement
  (4) Capacity planning and cluster scaling
  (5) Certificate rotation and management
  (6) etcd maintenance and health checks
  (7) Resource quota and limit range management
  (8) Namespace lifecycle management
  (9) Cluster migration and workload portability
  (10) Monitoring and alerting configuration
  (11) Log aggregation setup
  (12) Cost optimization and resource rightsizing
metadata:
  author: cluster-skills
  version: "1.0.0"
---

# Kubernetes / OpenShift Cluster Operations

Day-2 operations, maintenance, and lifecycle management for production clusters.

## Current Versions & Documentation (January 2026)

| Platform | Current Version | Upgrade Path | Documentation |
|----------|-----------------|--------------|---------------|
| **Kubernetes** | 1.31.x | 1.30 → 1.31 | https://kubernetes.io/docs/tasks/administer-cluster/ |
| **OpenShift** | 4.17.x | 4.16 → 4.17 | https://docs.openshift.com/container-platform/4.17/ |
| **EKS** | 1.31 | Rolling updates | https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html |
| **AKS** | 1.31 | Blue-green or rolling | https://learn.microsoft.com/azure/aks/upgrade-cluster |
| **GKE** | 1.31 | Surge upgrades | https://cloud.google.com/kubernetes-engine/docs/how-to/upgrading-a-cluster |

### Key Tools & Versions

| Tool | Version | Install | Purpose |
|------|---------|---------|--------|
| **kubeadm** | 1.31.x | Package manager | Cluster bootstrap |
| **Velero** | 1.15.x | Helm/CLI | Backup & restore |
| **kube-prometheus-stack** | v67.x | Helm | Monitoring |
| **VPA** | 1.3.x | kubectl apply | Vertical scaling |
| **Cluster Autoscaler** | 1.31.x | Helm | Node autoscaling |
| **Karpenter** | 1.1.x | Helm | AWS node provisioning |

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` as the primary command. When working with:
- **OpenShift/ARO clusters**: Replace `kubectl` with `oc`
- **Standard Kubernetes (AKS, EKS, GKE)**: Use `kubectl` as shown

## Node Operations

### Node Lifecycle

```bash
# View node status
kubectl get nodes -o wide

# Detailed node info
kubectl describe node ${NODE_NAME}

# Check node resources
kubectl top nodes

# Node labels and taints
kubectl get nodes --show-labels
kubectl describe node ${NODE} | grep -A 5 Taints
```

### Drain and Cordon

```bash
# Cordon: Mark node unschedulable (no new pods)
kubectl cordon ${NODE_NAME}

# Drain: Evict pods safely
kubectl drain ${NODE_NAME} \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=60 \
  --timeout=300s

# Force drain (use with caution)
kubectl drain ${NODE_NAME} \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --force \
  --grace-period=30

# Uncordon: Allow scheduling again
kubectl uncordon ${NODE_NAME}
```

### Cluster Autoscaler Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      containers:
        - name: cluster-autoscaler
          image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.31.0
          command:
            - ./cluster-autoscaler
            - --v=4
            - --cloud-provider=${CLOUD_PROVIDER}
            - --nodes=${MIN}:${MAX}:${NODE_GROUP}
            - --scale-down-delay-after-add=10m
            - --scale-down-unneeded-time=10m
            - --scale-down-utilization-threshold=0.5
            - --skip-nodes-with-local-storage=false
            - --skip-nodes-with-system-pods=true
            - --balance-similar-node-groups=true
```

## Backup and Recovery

### etcd Backup

```bash
# Backup etcd (run on control plane node)
ETCDCTL_API=3 etcdctl snapshot save /backup/etcd-$(date +%Y%m%d-%H%M%S).db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/healthcheck-client.crt \
  --key=/etc/kubernetes/pki/etcd/healthcheck-client.key

# Verify backup
ETCDCTL_API=3 etcdctl snapshot status /backup/etcd-snapshot.db --write-out=table
```

### Velero Backup (v1.15.x)

```bash
# Install Velero CLI
brew install velero

# Install Velero server with AWS provider
velero install \
  --provider aws \
  --bucket ${BUCKET_NAME} \
  --secret-file ./credentials-velero \
  --backup-location-config region=${REGION} \
  --snapshot-location-config region=${REGION} \
  --plugins velero/velero-plugin-for-aws:v1.10.0 \
  --use-node-agent

# Create backup
velero backup create ${BACKUP_NAME} \
  --include-namespaces ${NAMESPACES} \
  --ttl 720h \
  --default-volumes-to-fs-backup

# Create scheduled backup
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces ${NAMESPACES} \
  --ttl 168h

# Restore from backup
velero restore create --from-backup ${BACKUP_NAME}
```

### Velero Backup Manifest

```yaml
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: ${BACKUP_NAME}
  namespace: velero
spec:
  includedNamespaces:
    - ${NAMESPACE_1}
    - ${NAMESPACE_2}
  excludedResources:
    - events
    - events.events.k8s.io
  storageLocation: default
  volumeSnapshotLocations:
    - default
  ttl: 720h0m0s
  snapshotVolumes: true
  hooks:
    resources:
      - name: backup-hook
        includedNamespaces:
          - ${NAMESPACE}
        labelSelector:
          matchLabels:
            app: database
        pre:
          - exec:
              container: database
              command:
                - /bin/sh
                - -c
                - "pg_dump -U postgres > /backup/pre-backup.sql"
              onError: Fail
              timeout: 120s
```

## Cluster Upgrades

### Pre-Upgrade Checklist

```bash
#!/bin/bash
# pre-upgrade-check.sh

echo "=== Cluster Version ==="
kubectl version --short

echo -e "\n=== Node Status ==="
kubectl get nodes

echo -e "\n=== Pods Not Running ==="
kubectl get pods -A --field-selector=status.phase!=Running,status.phase!=Succeeded

echo -e "\n=== PDBs That May Block Drain ==="
kubectl get pdb -A

echo -e "\n=== Pending PVCs ==="
kubectl get pvc -A --field-selector=status.phase=Pending

echo -e "\n=== Deprecated APIs in Use ==="
kubectl get --raw /metrics | grep apiserver_requested_deprecated_apis
```

### AKS Upgrade (Azure)

```bash
# Check current version and available upgrades
az aks get-versions --location ${LOCATION} -o table
az aks get-upgrades --resource-group ${RG} --name ${CLUSTER} -o table

# Upgrade control plane and node pools
az aks upgrade --resource-group ${RG} --name ${CLUSTER} \
  --kubernetes-version 1.31.0

# Use blue-green upgrade with max surge
az aks nodepool upgrade --resource-group ${RG} --cluster-name ${CLUSTER} \
  --name ${NODEPOOL} --kubernetes-version 1.31.0 \
  --max-surge 33%

# Enable auto-upgrade channel
az aks update --resource-group ${RG} --name ${CLUSTER} \
  --auto-upgrade-channel stable
```

### EKS Upgrade

```bash
# Update control plane
aws eks update-cluster-version \
  --name ${CLUSTER_NAME} \
  --kubernetes-version 1.31

# Wait for completion
aws eks wait cluster-active --name ${CLUSTER_NAME}

# Update EKS add-ons
for addon in vpc-cni coredns kube-proxy eks-pod-identity-agent; do
  aws eks update-addon --cluster-name ${CLUSTER_NAME} \
    --addon-name $addon \
    --resolve-conflicts PRESERVE
done

# Update managed node groups
aws eks update-nodegroup-version \
  --cluster-name ${CLUSTER_NAME} \
  --nodegroup-name ${NODEGROUP_NAME}
```

### GKE Upgrade

```bash
# Check available versions
gcloud container get-server-config --region ${REGION}

# Upgrade control plane
gcloud container clusters upgrade ${CLUSTER} --region ${REGION} \
  --master --cluster-version 1.31

# Upgrade node pools
gcloud container clusters upgrade ${CLUSTER} --region ${REGION} \
  --node-pool ${POOL} \
  --cluster-version 1.31

# Enable release channel
gcloud container clusters update ${CLUSTER} --region ${REGION} \
  --release-channel regular
```

### OpenShift Upgrade

```bash
# Check available updates
oc adm upgrade

# View current version and channel
oc get clusterversion
oc get clusterversion version -o jsonpath='{.spec.channel}'

# Change channel
oc adm upgrade channel stable-4.17

# Start upgrade
oc adm upgrade --to-latest
# OR upgrade to specific version
oc adm upgrade --to=4.17.5

# Monitor upgrade progress
watch -n 10 'oc get clusterversion && oc get clusteroperators'
```

## Resource Management

### Resource Quotas

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
    persistentvolumeclaims: "10"
    requests.storage: 100Gi
```

### Limit Ranges

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: ${NAMESPACE}
spec:
  limits:
    - type: Container
      default:
        cpu: 500m
        memory: 512Mi
      defaultRequest:
        cpu: 100m
        memory: 128Mi
      max:
        cpu: "4"
        memory: 8Gi
      min:
        cpu: 50m
        memory: 64Mi
```

### Check Resource Usage

```bash
# Namespace resource usage vs quota
kubectl describe quota -n ${NAMESPACE}

# Pod resource usage
kubectl top pods -n ${NAMESPACE} --sort-by=memory
kubectl top pods -n ${NAMESPACE} --sort-by=cpu

# Node resource allocation
kubectl describe nodes | grep -A 5 "Allocated resources"
```

## Certificate Management

### Check Certificate Expiry

```bash
# kubeadm certificates
kubeadm certs check-expiration

# Manual check
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -dates

# Check all certs
for cert in /etc/kubernetes/pki/*.crt; do
  echo "=== $cert ==="
  openssl x509 -in $cert -noout -dates
done
```

### Rotate Certificates

```bash
# Renew all certificates (kubeadm)
kubeadm certs renew all

# Restart control plane components
crictl pods --name kube-apiserver -q | xargs crictl stopp
crictl pods --name kube-controller-manager -q | xargs crictl stopp
crictl pods --name kube-scheduler -q | xargs crictl stopp
```

## Monitoring Setup

### Prometheus Stack (kube-prometheus-stack v67.x)

```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.replicas=2 \
  --set prometheus.prometheusSpec.resources.requests.memory=2Gi \
  --set alertmanager.alertmanagerSpec.replicas=3 \
  --set grafana.persistence.enabled=true

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

### Custom ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: ${APP_NAME}
  namespace: monitoring
  labels:
    release: prometheus
spec:
  namespaceSelector:
    matchNames:
      - ${NAMESPACE}
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  endpoints:
    - port: metrics
      interval: 30s
      path: /metrics
```

## Cost Optimization

### VerticalPodAutoscaler

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ${APP_NAME}-vpa
  namespace: ${NAMESPACE}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ${APP_NAME}
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
      - containerName: "*"
        minAllowed:
          cpu: 50m
          memory: 64Mi
        maxAllowed:
          cpu: 4
          memory: 8Gi
```

## Namespace Lifecycle

### Namespace Template

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    app.kubernetes.io/managed-by: cluster-skills
    environment: ${ENVIRONMENT}
    team: ${TEAM}
  annotations:
    owner: ${OWNER_EMAIL}
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: default-quota
  namespace: ${NAMESPACE}
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    pods: "50"
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: ${NAMESPACE}
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

## Disaster Recovery

### Full Cluster Recovery Checklist

1. **Restore etcd** - See etcd restore section
2. **Verify Control Plane**
   ```bash
   kubectl get nodes
   kubectl get pods -n kube-system
   kubectl cluster-info
   ```
3. **Restore Workloads (Velero)**
   ```bash
   velero restore create --from-backup ${BACKUP_NAME}
   ```
4. **Verify Application Health**
   ```bash
   kubectl get pods -A
   kubectl get svc -A
   ```
5. **Verify DNS and Networking**
   ```bash
   kubectl run dns-test --image=busybox --rm -it --restart=Never -- nslookup kubernetes
   ```
