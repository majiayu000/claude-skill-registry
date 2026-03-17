---
name: azure-aks
description: Managed Kubernetes with Azure Kubernetes Service. Configure node pools, networking, identity, monitoring, and scaling. Use for container orchestration, microservices deployment, and Kubernetes workloads on Azure.
---

# Azure Kubernetes Service (AKS)

Expert guidance for managed Kubernetes on Azure.

## Create Cluster

```bash
# Create AKS cluster
az aks create \
  --name myAKSCluster \
  --resource-group myResourceGroup \
  --node-count 3 \
  --node-vm-size Standard_DS2_v2 \
  --generate-ssh-keys \
  --enable-managed-identity \
  --network-plugin azure \
  --network-policy azure

# Get credentials
az aks get-credentials \
  --name myAKSCluster \
  --resource-group myResourceGroup

# Verify
kubectl get nodes
```

## Node Pools

```bash
# Add node pool
az aks nodepool add \
  --resource-group myResourceGroup \
  --cluster-name myAKSCluster \
  --name gpupool \
  --node-count 2 \
  --node-vm-size Standard_NC6 \
  --node-taints gpu=true:NoSchedule \
  --labels workload=gpu

# Scale node pool
az aks nodepool scale \
  --resource-group myResourceGroup \
  --cluster-name myAKSCluster \
  --name nodepool1 \
  --node-count 5

# Enable autoscaling
az aks nodepool update \
  --resource-group myResourceGroup \
  --cluster-name myAKSCluster \
  --name nodepool1 \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 10
```

## Networking

### Azure CNI

```bash
# Create with Azure CNI
az aks create \
  --name myAKSCluster \
  --resource-group myResourceGroup \
  --network-plugin azure \
  --vnet-subnet-id /subscriptions/.../subnets/aks-subnet \
  --service-cidr 10.0.0.0/16 \
  --dns-service-ip 10.0.0.10
```

### Ingress Controller

```bash
# Install NGINX Ingress
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --create-namespace \
  --namespace ingress-nginx \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz

# Application Gateway Ingress
az aks enable-addons \
  --name myAKSCluster \
  --resource-group myResourceGroup \
  --addons ingress-appgw \
  --appgw-name myAppGateway \
  --appgw-subnet-cidr 10.2.0.0/16
```

## Identity & RBAC

### Workload Identity

```bash
# Enable workload identity
az aks update \
  --name myAKSCluster \
  --resource-group myResourceGroup \
  --enable-oidc-issuer \
  --enable-workload-identity

# Create user-assigned identity
az identity create \
  --name myIdentity \
  --resource-group myResourceGroup

# Federate identity
az identity federated-credential create \
  --name myFederatedIdentity \
  --identity-name myIdentity \
  --resource-group myResourceGroup \
  --issuer $(az aks show --name myAKSCluster --resource-group myResourceGroup --query "oidcIssuerProfile.issuerUrl" -o tsv) \
  --subject system:serviceaccount:default:my-service-account
```

### Pod with Workload Identity

```yaml
apikind: ServiceAccount
metadata:
  name: my-service-account
  annotations:
    azure.workload.identity/client-id: <client-id>
---
apikind: Deployment
metadata:
  name: my-app
spec:
  template:
    metadata:
      labels:
        azure.workload.identity/use: "true"
    spec:
      serviceAccountName: my-service-account
      containers:
        - name: app
          image: myapp:latest
```

## Azure Container Registry

```bash
# Attach ACR
az aks update \
  --name myAKSCluster \
  --resource-group myResourceGroup \
  --attach-acr myContainerRegistry

# Or use service principal
az aks update-credentials \
  --name myAKSCluster \
  --resource-group myResourceGroup \
  --reset-service-principal \
  --service-principal $SP_ID \
  --client-secret $SP_SECRET
```

## Monitoring

```bash
# Enable monitoring
az aks enable-addons \
  --name myAKSCluster \
  --resource-group myResourceGroup \
  --addons monitoring \
  --workspace-resource-id /subscriptions/.../workspaces/myWorkspace

# Enable Prometheus
az aks update \
  --name myAKSCluster \
  --resource-group myResourceGroup \
  --enable-azure-monitor-metrics
```

## GitOps with Flux

```bash
# Enable GitOps
az k8s-configuration flux create \
  --name gitops-config \
  --cluster-name myAKSCluster \
  --resource-group myResourceGroup \
  --cluster-type managedClusters \
  --scope cluster \
  --url https://github.com/myorg/fleet-infra \
  --branch main \
  --kustomization name=infra path=./infrastructure
```

## Storage

```yaml
# Azure Disk StorageClass
apikind: StorageClass
metadata:
  name: managed-premium
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_LRS
  kind: Managed
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
---
# Azure Files StorageClass
apikind: StorageClass
metadata:
  name: azurefile-csi
provisioner: file.csi.azure.com
parameters:
  skuName: Standard_LRS
reclaimPolicy: Delete
volumeBindingMode: Immediate
mountOptions:
  - dir_mode=0777
  - file_mode=0777
```

## Bicep Deployment

```bicep
resource aks 'Microsoft.ContainerService/managedClusters@2023-08-01' = {
  name: clusterName
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    dnsPrefix: dnsPrefix
    kubernetes    agentPoolProfiles: [
      {
        name: 'systempool'
        count: 3
        vmSize: 'Standard_DS2_v2'
        mode: 'System'
        osType: 'Linux'
        enableAutoScaling: true
        minCount: 1
        maxCount: 5
      }
    ]
    networkProfile: {
      networkPlugin: 'azure'
      networkPolicy: 'azure'
      loadBalancerSku: 'standard'
    }
    addonProfiles: {
      azureKeyvaultSecretsProvider: {
        enabled: true
      }
      omsagent: {
        enabled: true
        config: {
          logAnalyticsWorkspaceResourceID: workspaceId
        }
      }
    }
  }
}
```

## Resources

- [AKS Documentation](https://learn.microsoft.com/azure/aks/)
- [AKS Best Practices](https://learn.microsoft.com/azure/aks/best-practices)
- [AKS Baseline](https://github.com/mspnp/aks-baseline)
