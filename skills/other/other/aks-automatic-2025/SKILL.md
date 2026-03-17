---
name: aks-automatic-2025
description: Azure Kubernetes Service Automatic mode GA 2025 features including Karpenter, auto-scaling, and zero operational overhead
---

# AKS Automatic - 2025 GA Features

Complete knowledge base for Azure Kubernetes Service Automatic mode (GA October 2025).

## Overview

AKS Automatic is a fully-managed Kubernetes offering that eliminates operational overhead through intelligent automation and built-in best practices.

## Key Features (GA October 2025)

### 1. Zero Operational Overhead
- Fully-managed control plane and worker nodes
- Automatic OS patching and security updates
- Built-in monitoring and diagnostics
- Integrated security and compliance

### 2. Karpenter Integration
- Dynamic node provisioning based on real-time demand
- Intelligent bin-packing for cost optimization
- Automatic node consolidation and deprovisioning
- Support for multiple node pools and instance types

### 3. Auto-Scaling (Enabled by Default)
- **Horizontal Pod Autoscaler (HPA)**: Scale pods based on CPU/memory
- **Vertical Pod Autoscaler (VPA)**: Adjust pod resource requests/limits
- **KEDA**: Event-driven autoscaling for external triggers

### 4. Enhanced Security
- Microsoft Entra ID integration for authentication
- Azure RBAC for Kubernetes authorization
- Network policies enabled by default
- Automatic security patches
- Workload identity for pod-level authentication

### 5. Advanced Networking
- Azure CNI Overlay for efficient IP usage
- Cilium dataplane for high-performance networking
- Network policies for microsegmentation
- Private clusters supported

### 6. New Billing Model (Effective October 19, 2025)
- Hosted control plane fee: **$0.16/cluster/hour**
- Compute charges based on actual node usage
- No separate cluster management fee
- Cost savings from Karpenter optimization

### 7. Node Operating System
- Ubuntu 22.04 for Kubernetes < 1.34
- Ubuntu 24.04 for Kubernetes >= 1.34
- Automatic OS upgrades with node image channel

## Creating AKS Automatic Cluster

### Basic Creation

```bash
az aks create \
  --resource-group MyRG \
  --name MyAKSAutomatic \
  --sku automatic \
  --kubernetes-version 1.34 \
  --location eastus
```

### Production-Ready Configuration

```bash
az aks create \
  --resource-group MyRG \
  --name MyAKSAutomatic \
  --location eastus \
  --sku automatic \
  --tier standard \
  \
  # Kubernetes version
  --kubernetes-version 1.34 \
  \
  # Karpenter (default in automatic mode)
  --enable-karpenter \
  \
  # Networking
  --network-plugin azure \
  --network-plugin-mode overlay \
  --network-dataplane cilium \
  --service-cidr 10.0.0.0/16 \
  --dns-service-ip 10.0.0.10 \
  --load-balancer-sku standard \
  \
  # Use custom VNet (optional)
  --vnet-subnet-id /subscriptions/<sub-id>/resourceGroups/MyRG/providers/Microsoft.Network/virtualNetworks/MyVNet/subnets/AKSSubnet \
  \
  # Availability zones
  --zones 1 2 3 \
  \
  # Authentication and authorization
  --enable-managed-identity \
  --enable-aad \
  --enable-azure-rbac \
  --aad-admin-group-object-ids <group-object-id> \
  \
  # Auto-upgrade
  --auto-upgrade-channel stable \
  --node-os-upgrade-channel NodeImage \
  \
  # Security
  --enable-defender \
  --enable-workload-identity \
  --enable-oidc-issuer \
  \
  # Monitoring
  --enable-addons monitoring \
  --workspace-resource-id /subscriptions/<sub-id>/resourceGroups/MyRG/providers/Microsoft.OperationalInsights/workspaces/MyWorkspace \
  \
  # Tags
  --tags Environment=Production ManagedBy=AKSAutomatic
```

### With Azure Policy Add-on

```bash
az aks create \
  --resource-group MyRG \
  --name MyAKSAutomatic \
  --sku automatic \
  --enable-addons azure-policy \
  --kubernetes-version 1.34
```

## Karpenter Configuration

AKS Automatic uses Karpenter for intelligent node provisioning. Customize node provisioning with AKSNodeClass and NodePool CRDs.

### Default AKSNodeClass

```yaml
apiVersion: karpenter.azure.com/v1alpha1
kind: AKSNodeClass
metadata:
  name: default
spec:
  # OS Image - Ubuntu 24.04 for K8s 1.34+
  osImage:
    sku: Ubuntu
    version: "24.04"

  # VM Series
  vmSeries:
    - Standard_D
    - Standard_E

  # Max pods per node
  maxPodsPerNode: 110

  # Security
  securityProfile:
    sshAccess: Disabled
    securityType: Standard
```

### Custom NodePool

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: general-purpose
spec:
  # Constraints
  template:
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
        - key: kubernetes.azure.com/agentpool
          operator: In
          values: ["general"]

      # Node labels
      labels:
        workload-type: general

      # Taints (optional)
      taints:
        - key: "dedicated"
          value: "general"
          effect: "NoSchedule"

      # NodeClass reference
      nodeClassRef:
        group: karpenter.azure.com
        kind: AKSNodeClass
        name: default

  # Limits
  limits:
    cpu: "1000"
    memory: 4000Gi

  # Disruption budget
  disruption:
    consolidationPolicy: WhenEmpty
    consolidateAfter: 30s
    expireAfter: 720h # 30 days
    budgets:
      - nodes: "10%"
        duration: 5m
```

### GPU NodePool for AI Workloads

```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: gpu-workloads
spec:
  template:
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"]
        - key: node.kubernetes.io/instance-type
          operator: In
          values: ["Standard_NC6s_v3", "Standard_NC12s_v3", "Standard_NC24s_v3"]

      labels:
        workload-type: gpu
        gpu-type: nvidia-v100

      taints:
        - key: "nvidia.com/gpu"
          value: "true"
          effect: "NoSchedule"

      nodeClassRef:
        group: karpenter.azure.com
        kind: AKSNodeClass
        name: gpu-nodeclass

  limits:
    cpu: "200"
    memory: 800Gi
    nvidia.com/gpu: "16"

  disruption:
    consolidationPolicy: WhenEmpty
    consolidateAfter: 300s
```

## Autoscaling with HPA, VPA, and KEDA

### Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 50
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 15
```

### Vertical Pod Autoscaler (VPA)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto"  # Auto, Recreate, Initial, Off
  resourcePolicy:
    containerPolicies:
      - containerName: "*"
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 4
          memory: 8Gi
        controlledResources: ["cpu", "memory"]
        controlledValues: RequestsAndLimits
```

### KEDA ScaledObject (Event-Driven)

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: myapp-queue-scaler
spec:
  scaleTargetRef:
    name: myapp
  minReplicaCount: 0  # Scale to zero
  maxReplicaCount: 100
  pollingInterval: 30
  cooldownPeriod: 300
  triggers:
    # Azure Service Bus Queue
    - type: azure-servicebus
      metadata:
        queueName: myqueue
        namespace: myservicebus
        messageCount: "5"
      authenticationRef:
        name: azure-servicebus-auth

    # Azure Storage Queue
    - type: azure-queue
      metadata:
        queueName: myqueue
        queueLength: "10"
        accountName: mystorageaccount
      authenticationRef:
        name: azure-storage-auth

    # Prometheus metrics
    - type: prometheus
      metadata:
        serverAddress: http://prometheus.monitoring.svc.cluster.local:9090
        metricName: http_requests_per_second
        threshold: "100"
        query: sum(rate(http_requests_total[2m]))
```

## Workload Identity (Replaces AAD Pod Identity)

### Setup

```bash
# Workload identity is enabled by default in AKS Automatic

# Create managed identity
az identity create \
  --name myapp-identity \
  --resource-group MyRG

# Get identity details
export IDENTITY_CLIENT_ID=$(az identity show -g MyRG -n myapp-identity --query clientId -o tsv)
export IDENTITY_OBJECT_ID=$(az identity show -g MyRG -n myapp-identity --query principalId -o tsv)

# Assign role to identity
az role assignment create \
  --assignee $IDENTITY_OBJECT_ID \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<sub-id>/resourceGroups/MyRG/providers/Microsoft.Storage/storageAccounts/mystorage

# Create federated credential
export AKS_OIDC_ISSUER=$(az aks show -g MyRG -n MyAKSAutomatic --query oidcIssuerProfile.issuerUrl -o tsv)

az identity federated-credential create \
  --name myapp-federated-credential \
  --identity-name myapp-identity \
  --resource-group MyRG \
  --issuer $AKS_OIDC_ISSUER \
  --subject system:serviceaccount:default:myapp-sa
```

### Kubernetes Resources

```yaml
# Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: default
  annotations:
    azure.workload.identity/client-id: "<IDENTITY_CLIENT_ID>"

---
# Deployment using workload identity
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        azure.workload.identity/use: "true"  # Enable workload identity
    spec:
      serviceAccountName: myapp-sa
      containers:
        - name: myapp
          image: myregistry.azurecr.io/myapp:latest
          env:
            - name: AZURE_CLIENT_ID
              value: "<IDENTITY_CLIENT_ID>"
            - name: AZURE_TENANT_ID
              value: "<TENANT_ID>"
            - name: AZURE_FEDERATED_TOKEN_FILE
              value: /var/run/secrets/azure/tokens/azure-identity-token
          volumeMounts:
            - name: azure-identity-token
              mountPath: /var/run/secrets/azure/tokens
              readOnly: true
      volumes:
        - name: azure-identity-token
          projected:
            sources:
              - serviceAccountToken:
                  path: azure-identity-token
                  expirationSeconds: 3600
                  audience: api://AzureADTokenExchange
```

## Monitoring and Observability

### Enable Container Insights

```bash
# Already enabled with --enable-addons monitoring
# Query logs using Azure Monitor

# Get cluster logs
az monitor log-analytics query \
  --workspace <workspace-id> \
  --analytics-query "KubePodInventory | where ClusterName == 'MyAKSAutomatic' | take 10" \
  --output table

# Get Karpenter logs
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter
```

### Prometheus and Grafana

```bash
# Enable managed Prometheus
az aks update \
  --resource-group MyRG \
  --name MyAKSAutomatic \
  --enable-azure-monitor-metrics

# Access Grafana dashboards through Azure Portal
```

## Cost Optimization

### Billing Model (October 2025)
- **Control plane**: $0.16/hour per cluster
- **Compute**: Pay for actual node usage
- **Karpenter**: Automatic bin-packing and consolidation
- **Scale-to-zero**: Possible with KEDA and Karpenter

### Cost-Saving Tips

1. **Use Spot Instances for Non-Critical Workloads**
```yaml
- key: karpenter.sh/capacity-type
  operator: In
  values: ["spot"]
```

2. **Configure Aggressive Consolidation**
```yaml
disruption:
  consolidationPolicy: WhenUnderutilized
  consolidateAfter: 30s
```

3. **Implement Pod Disruption Budgets**
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: myapp
```

4. **Use VPA for Right-Sizing**
- VPA automatically adjusts resource requests based on actual usage

## Migration from Standard AKS to Automatic

AKS Automatic is a new cluster mode - in-place migration is not supported. Follow these steps:

1. **Create new AKS Automatic cluster**
2. **Install workloads in new cluster**
3. **Validate functionality**
4. **Switch traffic** (DNS, load balancer)
5. **Decommission old cluster**

## Best Practices

✓ Use AKS Automatic for new production clusters
✓ Enable workload identity for pod authentication
✓ Configure custom NodePools for specific workload types
✓ Implement HPA, VPA, and KEDA for comprehensive scaling
✓ Use spot instances for batch and fault-tolerant workloads
✓ Enable Container Insights and Managed Prometheus
✓ Configure Pod Disruption Budgets for critical apps
✓ Use network policies for microsegmentation
✓ Enable Azure Policy add-on for compliance
✓ Implement GitOps with Flux or Argo CD

## Troubleshooting

### Check Karpenter Status
```bash
kubectl logs -n kube-system -l app.kubernetes.io/name=karpenter --tail=100
kubectl get nodepools
kubectl get nodeclaims
```

### View Node Provisioning Events
```bash
kubectl get events --field-selector involvedObject.kind=NodePool -A
```

### Debug Workload Identity Issues
```bash
# Check service account annotation
kubectl get sa myapp-sa -o yaml

# Check pod labels
kubectl get pod <pod-name> -o yaml | grep azure.workload.identity

# Check federated credential
az identity federated-credential show \
  --identity-name myapp-identity \
  --resource-group MyRG \
  --name myapp-federated-credential
```

## References

- [AKS Automatic Documentation](https://learn.microsoft.com/en-us/azure/aks/automatic)
- [Karpenter on Azure](https://karpenter.sh)
- [Workload Identity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview)
- [AKS Release Notes](https://github.com/Azure/AKS/releases)

AKS Automatic represents the future of managed Kubernetes on Azure - zero operational overhead with maximum automation!
