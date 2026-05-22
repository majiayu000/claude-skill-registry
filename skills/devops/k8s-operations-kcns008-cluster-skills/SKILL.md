---
name: k8s-operations
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
---

# Kubernetes / OpenShift Cluster Operations

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

**IMPORTANT**: This skill uses `kubectl` as the primary command in all examples. When working with:
- **OpenShift/ARO clusters**: Replace all `kubectl` commands with `oc`
- **Standard Kubernetes clusters (AKS, EKS, GKE, etc.)**: Use `kubectl` as shown

The agent will automatically detect the cluster type and use the appropriate command.

Day-2 operations, maintenance, and lifecycle management for production clusters.

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

### Node Maintenance Script

```bash
#!/bin/bash
# node-maintenance.sh ${NODE_NAME}
NODE=$1

echo "Starting maintenance for node: $NODE"

# 1. Cordon the node
kubectl cordon $NODE

# 2. Wait for running pods to complete gracefully
echo "Draining node..."
kubectl drain $NODE \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=120 \
  --timeout=600s

# 3. Verify no pods (except daemonsets)
echo "Remaining pods on node:"
kubectl get pods -A --field-selector spec.nodeName=$NODE

# 4. Perform maintenance...
echo "Node ready for maintenance"
echo "Run 'kubectl uncordon $NODE' when complete"
```

### Node Scaling

#### Manual Node Addition (kubeadm)

```bash
# On control plane: Generate join command
kubeadm token create --print-join-command

# On new node: Join cluster
kubeadm join ${CONTROL_PLANE}:6443 --token ${TOKEN} \
  --discovery-token-ca-cert-hash sha256:${HASH}
```

#### Cluster Autoscaler Configuration

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
          image: registry.k8s.io/autoscaling/cluster-autoscaler:v1.28.0
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

### etcd Restore

```bash
# Stop kube-apiserver (move manifests)
mv /etc/kubernetes/manifests/kube-apiserver.yaml /tmp/

# Restore etcd
ETCDCTL_API=3 etcdctl snapshot restore /backup/etcd-snapshot.db \
  --name=${ETCD_NAME} \
  --initial-cluster=${ETCD_NAME}=https://${ETCD_IP}:2380 \
  --initial-cluster-token=etcd-cluster-1 \
  --initial-advertise-peer-urls=https://${ETCD_IP}:2380 \
  --data-dir=/var/lib/etcd-restored

# Update etcd data directory in manifest and restart
# Move kube-apiserver manifest back
mv /tmp/kube-apiserver.yaml /etc/kubernetes/manifests/
```

### Velero Backup

**Current Version: Velero 1.15.x (January 2026)**

```bash
# Install Velero CLI (v1.15.x)
brew install velero
# OR
curl -LO https://github.com/vmware-tanzu/velero/releases/latest/download/velero-v1.15.0-linux-amd64.tar.gz

# Install Velero server with AWS provider
velero install \
  --provider aws \
  --bucket ${BUCKET_NAME} \
  --secret-file ./credentials-velero \
  --backup-location-config region=${REGION} \
  --snapshot-location-config region=${REGION} \
  --plugins velero/velero-plugin-for-aws:v1.10.0 \
  --use-node-agent  # For file-system backups (CSI volumes)

# Install with Azure provider
velero install \
  --provider azure \
  --bucket ${CONTAINER_NAME} \
  --secret-file ./credentials-velero \
  --backup-location-config resourceGroup=${RG},storageAccount=${STORAGE_ACCOUNT} \
  --snapshot-location-config resourceGroup=${RG} \
  --plugins velero/velero-plugin-for-microsoft-azure:v1.10.0 \
  --use-node-agent

# Install with GCP provider
velero install \
  --provider gcp \
  --bucket ${BUCKET_NAME} \
  --secret-file ./credentials-velero \
  --plugins velero/velero-plugin-for-gcp:v1.10.0 \
  --use-node-agent

# Create backup
velero backup create ${BACKUP_NAME} \
  --include-namespaces ${NAMESPACES} \
  --ttl 720h \
  --default-volumes-to-fs-backup  # Use fs backup for CSI volumes

# Create scheduled backup
velero schedule create daily-backup \
  --schedule="0 2 * * *" \
  --include-namespaces ${NAMESPACES} \
  --ttl 168h \
  --default-volumes-to-fs-backup

# Restore from backup
velero restore create --from-backup ${BACKUP_NAME}

# Check backup status
velero backup describe ${BACKUP_NAME} --details
velero backup logs ${BACKUP_NAME}

# List all backups and schedules
velero backup get
velero schedule get
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
  defaultVolumesToFsBackup: false
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

### OpenShift Backup

```bash
# Backup etcd (OpenShift)
oc debug node/${CONTROL_PLANE_NODE} -- chroot /host \
  /usr/local/bin/cluster-backup.sh /home/core/backup

# Backup cluster resources
oc get all -A -o yaml > cluster-resources.yaml
oc get pv -o yaml > persistent-volumes.yaml
oc get sc -o yaml > storage-classes.yaml
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

echo -e "\n=== etcd Health ==="
kubectl get pods -n kube-system -l component=etcd

echo -e "\n=== Backup Status ==="
# Check recent backups exist
ls -la /backup/etcd-*.db 2>/dev/null || echo "No local etcd backups found"
```

### Kubernetes Upgrade (kubeadm)

```bash
# 1. Upgrade control plane
# On first control plane node:
apt update && apt-cache madison kubeadm
apt-mark unhold kubeadm && apt-get update && apt-get install -y kubeadm=${VERSION} && apt-mark hold kubeadm

# Verify upgrade plan
kubeadm upgrade plan

# Apply upgrade
kubeadm upgrade apply v${VERSION}

# Upgrade kubelet and kubectl
apt-mark unhold kubelet kubectl && apt-get update && apt-get install -y kubelet=${VERSION} kubectl=${VERSION} && apt-mark hold kubelet kubectl
systemctl daemon-reload && systemctl restart kubelet

# 2. Upgrade worker nodes (one at a time)
kubectl drain ${NODE} --ignore-daemonsets --delete-emptydir-data

# On worker node:
apt-mark unhold kubeadm && apt-get update && apt-get install -y kubeadm=${VERSION} && apt-mark hold kubeadm
kubeadm upgrade node
apt-mark unhold kubelet kubectl && apt-get update && apt-get install -y kubelet=${VERSION} kubectl=${VERSION} && apt-mark hold kubelet kubectl
systemctl daemon-reload && systemctl restart kubelet

# Back on control plane:
kubectl uncordon ${NODE}
```

### AKS Upgrade (Azure)

**Documentation**: https://learn.microsoft.com/azure/aks/upgrade-cluster

```bash
# Check current version and available upgrades
az aks get-versions --location ${LOCATION} -o table
az aks show --resource-group ${RG} --name ${CLUSTER} --query kubernetesVersion
az aks get-upgrades --resource-group ${RG} --name ${CLUSTER} -o table

# Upgrade control plane and node pools together (default)
az aks upgrade --resource-group ${RG} --name ${CLUSTER} \
  --kubernetes-version 1.31.0

# Upgrade control plane only
az aks upgrade --resource-group ${RG} --name ${CLUSTER} \
  --kubernetes-version 1.31.0 \
  --control-plane-only

# Upgrade specific node pool
az aks nodepool upgrade --resource-group ${RG} --cluster-name ${CLUSTER} \
  --name ${NODEPOOL} --kubernetes-version 1.31.0

# Use blue-green upgrade with max surge
az aks nodepool upgrade --resource-group ${RG} --cluster-name ${CLUSTER} \
  --name ${NODEPOOL} --kubernetes-version 1.31.0 \
  --max-surge 33%

# Enable auto-upgrade channel
az aks update --resource-group ${RG} --name ${CLUSTER} \
  --auto-upgrade-channel stable

# Check upgrade status
az aks show --resource-group ${RG} --name ${CLUSTER} \
  --query 'provisioningState'
```

### GKE Upgrade (Google Cloud)

**Documentation**: https://cloud.google.com/kubernetes-engine/docs/how-to/upgrading-a-cluster

```bash
# Check available versions
gcloud container get-server-config --region ${REGION}
gcloud container clusters list --format="table(name,currentMasterVersion,currentNodeVersion)"

# Check upgrade availability
gcloud container clusters describe ${CLUSTER} --region ${REGION} \
  --format="get(currentMasterVersion)"

# Upgrade control plane (master)
gcloud container clusters upgrade ${CLUSTER} --region ${REGION} \
  --master --cluster-version 1.31

# Upgrade node pools with surge
gcloud container clusters upgrade ${CLUSTER} --region ${REGION} \
  --node-pool ${POOL} \
  --cluster-version 1.31

# Blue-green upgrade for node pools
gcloud container node-pools update ${POOL} --cluster ${CLUSTER} \
  --region ${REGION} \
  --enable-blue-green-upgrade \
  --node-pool-soak-duration 3600s

# Enable release channel for auto-upgrades
gcloud container clusters update ${CLUSTER} --region ${REGION} \
  --release-channel regular

# For Autopilot clusters (auto-managed)
gcloud container clusters update ${CLUSTER} --region ${REGION} \
  --maintenance-window-start 02:00 \
  --maintenance-window-end 06:00

# Monitor upgrade
gcloud container operations list --filter="targetLink~${CLUSTER}"
```

### OpenShift Upgrade

**Documentation**: https://docs.openshift.com/container-platform/4.17/updating/index.html

```bash
# Check available updates
oc adm upgrade

# View current version and channel
oc get clusterversion
oc get clusterversion version -o jsonpath='{.spec.channel}'

# Change channel (if needed) - EUS channels for extended support
oc adm upgrade channel stable-4.17
# OR for extended update support
oc adm upgrade channel eus-4.16  # EUS to EUS upgrades

# Start upgrade to latest in channel
oc adm upgrade --to-latest

# OR upgrade to specific version
oc adm upgrade --to=4.17.5

# For EUS-to-EUS upgrades (4.14 EUS → 4.16 EUS)
oc adm upgrade --to-multi-arch --to=4.16.0

# Monitor upgrade progress
watch -n 10 'oc get clusterversion && echo && oc get clusteroperators | grep -v "True.*False.*False"'

# Detailed progress
oc get clusterversion version -o jsonpath='{.status.conditions}' | jq
oc get clusteroperators
oc get nodes

# Check machine config pool status
oc get mcp

# Troubleshoot stuck upgrades
oc adm upgrade --include=current
oc describe clusterversion version

# ARO (Azure Red Hat OpenShift) upgrade
az aro update --resource-group ${RG} --name ${CLUSTER}

# ROSA (Red Hat OpenShift on AWS) upgrade
rosa upgrade cluster --cluster ${CLUSTER} --version 4.17.5
rosa describe upgrade --cluster ${CLUSTER}
```

### EKS Upgrade

**Documentation**: https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html

```bash
# Check current version and available updates
aws eks describe-cluster --name ${CLUSTER_NAME} --query 'cluster.version'
aws eks describe-addon-versions --kubernetes-version 1.31 | jq '.addons[].addonName'

# Pre-upgrade: Update aws-cli and eksctl
brew upgrade awscli eksctl

# Update control plane (1.30 → 1.31)
aws eks update-cluster-version \
  --name ${CLUSTER_NAME} \
  --kubernetes-version 1.31

# Wait for completion (can take 20-40 minutes)
aws eks wait cluster-active --name ${CLUSTER_NAME}
aws eks describe-update --name ${CLUSTER_NAME} --update-id ${UPDATE_ID}

# Update EKS add-ons to compatible versions
for addon in vpc-cni coredns kube-proxy eks-pod-identity-agent; do
  aws eks update-addon --cluster-name ${CLUSTER_NAME} \
    --addon-name $addon \
    --resolve-conflicts PRESERVE
done

# Update managed node groups
aws eks update-nodegroup-version \
  --cluster-name ${CLUSTER_NAME} \
  --nodegroup-name ${NODEGROUP_NAME}

# For Karpenter-managed nodes (v1.0+)
# Update Karpenter to compatible version first
helm upgrade karpenter oci://public.ecr.aws/karpenter/karpenter \
  --namespace karpenter \
  --set settings.clusterName=${CLUSTER_NAME} \
  --set controller.image.tag=1.1.0

# Karpenter will automatically roll nodes with drift
kubectl get nodeclaims

# Verify upgrade
kubectl get nodes
kubectl version
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
    count/deployments.apps: "20"
    count/services: "20"
    count/secrets: "50"
    count/configmaps: "50"
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
    # Default limits for containers
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
    # Limits for PVCs
    - type: PersistentVolumeClaim
      max:
        storage: 50Gi
      min:
        storage: 1Gi
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

# Detailed resource report
kubectl get pods -n ${NAMESPACE} -o custom-columns=\
NAME:.metadata.name,\
CPU_REQ:.spec.containers[*].resources.requests.cpu,\
CPU_LIM:.spec.containers[*].resources.limits.cpu,\
MEM_REQ:.spec.containers[*].resources.requests.memory,\
MEM_LIM:.spec.containers[*].resources.limits.memory
```

## Certificate Management

### Check Certificate Expiry

```bash
# kubeadm certificates
kubeadm certs check-expiration

# Manual check
openssl x509 -in /etc/kubernetes/pki/apiserver.crt -noout -dates

# Check all certs in PKI directory
for cert in /etc/kubernetes/pki/*.crt; do
  echo "=== $cert ==="
  openssl x509 -in $cert -noout -dates
done
```

### Rotate Certificates (kubeadm)

```bash
# Renew all certificates
kubeadm certs renew all

# Renew specific certificate
kubeadm certs renew apiserver

# Restart control plane components
crictl pods --name kube-apiserver -q | xargs crictl stopp
crictl pods --name kube-controller-manager -q | xargs crictl stopp
crictl pods --name kube-scheduler -q | xargs crictl stopp
```

### OpenShift Certificate Management

```bash
# Check certificate status
oc get certificates -A
oc get certificatesigningrequests

# Approve pending CSRs
oc get csr -o go-template='{{range .items}}{{if not .status}}{{.metadata.name}}{{"\n"}}{{end}}{{end}}' | xargs oc adm certificate approve
```

## Monitoring Setup

### Prometheus Stack (kube-prometheus-stack)

**Current Version: Chart v67.x, Prometheus v2.55.x, Grafana v11.x (January 2026)**

```bash
# Add Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Install via Helm (production-ready configuration)
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --version 67.x \
  --set prometheus.prometheusSpec.retention=30d \
  --set prometheus.prometheusSpec.retentionSize=50GB \
  --set prometheus.prometheusSpec.replicas=2 \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.storageClassName=gp3 \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=100Gi \
  --set prometheus.prometheusSpec.resources.requests.memory=2Gi \
  --set prometheus.prometheusSpec.resources.limits.memory=4Gi \
  --set alertmanager.alertmanagerSpec.replicas=3 \
  --set alertmanager.alertmanagerSpec.storage.volumeClaimTemplate.spec.storageClassName=gp3 \
  --set alertmanager.alertmanagerSpec.storage.volumeClaimTemplate.spec.resources.requests.storage=10Gi \
  --set grafana.persistence.enabled=true \
  --set grafana.persistence.size=10Gi \
  --set grafana.persistence.storageClassName=gp3 \
  --set grafana.adminPassword="${GRAFANA_PASSWORD}" \
  --set grafana.sidecar.dashboards.enabled=true \
  --set grafana.sidecar.dashboards.searchNamespace=ALL

# Access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80

# Access Prometheus
kubectl port-forward -n monitoring svc/prometheus-kube-prometheus-prometheus 9090:9090

# Check status
kubectl get servicemonitor -A
kubectl get prometheusrules -A
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
      scheme: http
```

### PrometheusRule (Alerts)

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: ${APP_NAME}-alerts
  namespace: monitoring
  labels:
    release: prometheus
spec:
  groups:
    - name: ${APP_NAME}.rules
      rules:
        - alert: HighErrorRate
          expr: |
            sum(rate(http_requests_total{job="${APP_NAME}",status=~"5.."}[5m])) 
            / sum(rate(http_requests_total{job="${APP_NAME}"}[5m])) > 0.05
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: "High error rate detected"
            description: "Error rate is {{ $value | humanizePercentage }} for {{ $labels.job }}"
        
        - alert: PodCrashLooping
          expr: |
            rate(kube_pod_container_status_restarts_total{namespace="${NAMESPACE}"}[15m]) * 60 * 15 > 0
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Pod crash looping"
            description: "Pod {{ $labels.pod }} is crash looping"
```

## Logging Setup

### Fluent Bit DaemonSet

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: logging
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         5
        Log_Level     info
        Daemon        off
        Parsers_File  parsers.conf
    
    [INPUT]
        Name              tail
        Tag               kube.*
        Path              /var/log/containers/*.log
        Parser            cri
        DB                /var/log/flb_kube.db
        Mem_Buf_Limit     5MB
        Skip_Long_Lines   On
        Refresh_Interval  10
    
    [FILTER]
        Name                kubernetes
        Match               kube.*
        Kube_URL            https://kubernetes.default.svc:443
        Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
        Merge_Log           On
        K8S-Logging.Parser  On
        K8S-Logging.Exclude On
    
    [OUTPUT]
        Name            es
        Match           *
        Host            ${ELASTICSEARCH_HOST}
        Port            9200
        Logstash_Format On
        Retry_Limit     False
  
  parsers.conf: |
    [PARSER]
        Name        cri
        Format      regex
        Regex       ^(?<time>[^ ]+) (?<stream>stdout|stderr) (?<logtag>[^ ]*) (?<message>.*)$
        Time_Key    time
        Time_Format %Y-%m-%dT%H:%M:%S.%L%z
```

## Cost Optimization

### Resource Rightsizing Script

```bash
#!/bin/bash
# resource-rightsizing.sh - Identify over-provisioned workloads

echo "=== Pods with CPU Usage < 10% of Requests ==="
kubectl top pods -A --no-headers | while read ns pod cpu mem; do
  cpu_milli=$(echo $cpu | sed 's/m//')
  requests=$(kubectl get pod $pod -n $ns -o jsonpath='{.spec.containers[*].resources.requests.cpu}' 2>/dev/null | sed 's/m//')
  if [ -n "$requests" ] && [ "$requests" -gt 0 ]; then
    usage_pct=$((cpu_milli * 100 / requests))
    if [ "$usage_pct" -lt 10 ]; then
      echo "$ns/$pod: ${usage_pct}% CPU utilization (${cpu_milli}m / ${requests}m requested)"
    fi
  fi
done

echo -e "\n=== Pods with Memory Usage < 20% of Requests ==="
kubectl top pods -A --no-headers | while read ns pod cpu mem; do
  mem_mi=$(echo $mem | sed 's/Mi//')
  requests=$(kubectl get pod $pod -n $ns -o jsonpath='{.spec.containers[*].resources.requests.memory}' 2>/dev/null)
  requests_mi=$(echo $requests | sed 's/Mi//;s/Gi/*1024/' | bc 2>/dev/null)
  if [ -n "$requests_mi" ] && [ "$requests_mi" -gt 0 ]; then
    usage_pct=$((mem_mi * 100 / requests_mi))
    if [ "$usage_pct" -lt 20 ]; then
      echo "$ns/$pod: ${usage_pct}% Memory utilization (${mem_mi}Mi / ${requests})"
    fi
  fi
done
```

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
    updateMode: "Auto"  # or "Off" for recommendations only
  resourcePolicy:
    containerPolicies:
      - containerName: "*"
        minAllowed:
          cpu: 50m
          memory: 64Mi
        maxAllowed:
          cpu: 4
          memory: 8Gi
        controlledResources: ["cpu", "memory"]
```

## Namespace Lifecycle

### Namespace Template

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ${NAMESPACE}
  labels:
    app.kubernetes.io/managed-by: cluster-code
    environment: ${ENVIRONMENT}
    team: ${TEAM}
    cost-center: ${COST_CENTER}
  annotations:
    owner: ${OWNER_EMAIL}
    description: "${DESCRIPTION}"
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

### Safe Namespace Deletion

```bash
#!/bin/bash
# safe-namespace-delete.sh ${NAMESPACE}
NS=$1

echo "=== Resources in namespace $NS ==="
kubectl get all -n $NS

echo -e "\n=== PVCs (data will be lost!) ==="
kubectl get pvc -n $NS

echo -e "\n=== Secrets ==="
kubectl get secrets -n $NS

read -p "Delete namespace $NS? (yes/no): " confirm
if [ "$confirm" = "yes" ]; then
  # Remove finalizers from stuck resources
  kubectl get all -n $NS -o name | xargs -I {} kubectl patch {} -n $NS -p '{"metadata":{"finalizers":null}}' --type=merge 2>/dev/null
  
  # Delete namespace
  kubectl delete namespace $NS --timeout=120s
  
  # Force delete if stuck
  if kubectl get namespace $NS &>/dev/null; then
    echo "Namespace stuck, removing finalizers..."
    kubectl get namespace $NS -o json | jq '.spec.finalizers = []' | kubectl replace --raw "/api/v1/namespaces/$NS/finalize" -f -
  fi
fi
```

## Disaster Recovery Runbook

### Full Cluster Recovery Checklist

1. **Restore etcd**
   ```bash
   # See etcd restore section above
   ```

2. **Verify Control Plane**
   ```bash
   kubectl get nodes
   kubectl get pods -n kube-system
   kubectl cluster-info
   ```

3. **Restore Workloads (if using Velero)**
   ```bash
   velero restore create --from-backup ${BACKUP_NAME}
   velero restore describe ${RESTORE_NAME}
   ```

4. **Verify Application Health**
   ```bash
   kubectl get pods -A
   kubectl get svc -A
   kubectl get ingress -A
   ```

5. **Restore Secrets (if external)**
   ```bash
   # Sync from external secrets manager
   kubectl annotate externalsecret -A force-sync=$(date +%s) --overwrite
   ```

6. **Verify DNS and Networking**
   ```bash
   kubectl run dns-test --image=busybox --rm -it --restart=Never -- nslookup kubernetes
   ```

7. **Validate Data Integrity**
   ```bash
   # Application-specific data checks
   ```

8. **Update DNS/Load Balancers**
   ```bash
   # Point external traffic to recovered cluster
   ```
