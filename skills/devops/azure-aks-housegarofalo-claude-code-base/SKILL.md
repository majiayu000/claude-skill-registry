---
name: azure-aks
description: Managed Kubernetes with Azure Kubernetes Service. Configure node pools, networking, identity, monitoring, and scaling. Use for container orchestration, microservices deployment, and Kubernetes workloads on Azure.
---

# Azure Kubernetes Service (AKS) Skill

Deploy and manage containerized applications with Azure Kubernetes Service.

## Triggers

Use this skill when you see:
- azure aks, aks cluster, azure kubernetes
- managed kubernetes, aks node pool
- aks networking, aks identity
- aks monitoring, container insights

## Instructions

### Create AKS Cluster

```bash
# Create resource group
az group create --name mygroup --location eastus

# Create AKS cluster
az aks create \
    --resource-group mygroup \
    --name myaks \
    --node-count 3 \
    --node-vm-size Standard_DS2_v2 \
    --enable-managed-identity \
    --enable-addons monitoring \
    --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group mygroup --name myaks

# Verify connection
kubectl get nodes
```

### Node Pools

```bash
# Add node pool
az aks nodepool add \
    --resource-group mygroup \
    --cluster-name myaks \
    --name gpupool \
    --node-count 2 \
    --node-vm-size Standard_NC6 \
    --node-taints sku=gpu:NoSchedule \
    --labels workload=gpu

# Scale node pool
az aks nodepool scale \
    --resource-group mygroup \
    --cluster-name myaks \
    --name nodepool1 \
    --node-count 5

# Enable cluster autoscaler
az aks nodepool update \
    --resource-group mygroup \
    --cluster-name myaks \
    --name nodepool1 \
    --enable-cluster-autoscaler \
    --min-count 1 \
    --max-count 10

# List node pools
az aks nodepool list --resource-group mygroup --cluster-name myaks -o table
```

### Networking

```bash
# Create AKS with Azure CNI
az aks create \
    --resource-group mygroup \
    --name myaks \
    --network-plugin azure \
    --vnet-subnet-id /subscriptions/.../subnets/aks-subnet \
    --service-cidr 10.0.0.0/16 \
    --dns-service-ip 10.0.0.10 \
    --docker-bridge-address 172.17.0.1/16

# Enable HTTP application routing
az aks enable-addons \
    --resource-group mygroup \
    --name myaks \
    --addons http_application_routing

# Create internal load balancer
kubectl apply -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: internal-app
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  ports:
    - port: 80
  selector:
    app: myapp
EOF
```

### Azure Container Registry Integration

```bash
# Create ACR
az acr create --resource-group mygroup --name myacr --sku Standard

# Attach ACR to AKS
az aks update \
    --resource-group mygroup \
    --name myaks \
    --attach-acr myacr

# Build and push image
az acr build --registry myacr --image myapp:v1 .

# Use in deployment
# image: myacr.azurecr.io/myapp:v1
```

### Identity and Security

```bash
# Enable workload identity
az aks update \
    --resource-group mygroup \
    --name myaks \
    --enable-oidc-issuer \
    --enable-workload-identity

# Create managed identity
az identity create \
    --name myapp-identity \
    --resource-group mygroup

# Create service account with workload identity
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  annotations:
    azure.workload.identity/client-id: <CLIENT_ID>
EOF

# Enable Azure RBAC for Kubernetes
az aks update \
    --resource-group mygroup \
    --name myaks \
    --enable-azure-rbac

# Assign Azure Kubernetes Service RBAC Cluster Admin
az role assignment create \
    --role "Azure Kubernetes Service RBAC Cluster Admin" \
    --assignee <USER_PRINCIPAL_ID> \
    --scope /subscriptions/.../resourceGroups/mygroup/providers/Microsoft.ContainerService/managedClusters/myaks
```

### Monitoring

```bash
# Enable Container Insights
az aks enable-addons \
    --resource-group mygroup \
    --name myaks \
    --addons monitoring \
    --workspace-resource-id /subscriptions/.../workspaces/myworkspace

# View logs
az aks browse --resource-group mygroup --name myaks

# Query logs with KQL
# ContainerLog
# | where LogEntry contains "error"
# | project TimeGenerated, LogEntry
```

### Ingress Controller

```bash
# Install NGINX ingress controller
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
    --namespace ingress-nginx \
    --create-namespace \
    --set controller.service.annotations."service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"=/healthz

# Create ingress
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-service
                port:
                  number: 80
EOF
```

### GitOps with Flux

```bash
# Enable GitOps extension
az k8s-extension create \
    --resource-group mygroup \
    --cluster-name myaks \
    --cluster-type managedClusters \
    --name flux \
    --extension-type microsoft.flux

# Create Flux configuration
az k8s-configuration flux create \
    --resource-group mygroup \
    --cluster-name myaks \
    --cluster-type managedClusters \
    --name gitops-config \
    --namespace flux-system \
    --url https://github.com/myorg/myrepo \
    --branch main \
    --kustomization name=infra path=./infrastructure prune=true \
    --kustomization name=apps path=./apps prune=true dependsOn=infra
```

### Maintenance

```bash
# Upgrade AKS
az aks get-upgrades --resource-group mygroup --name myaks -o table
az aks upgrade --resource-group mygroup --name myaks --kubernetes-version 1.28.0

# Start/Stop cluster (dev/test)
az aks stop --resource-group mygroup --name myaks
az aks start --resource-group mygroup --name myaks

# Get cluster info
az aks show --resource-group mygroup --name myaks -o table
```

## Best Practices

1. **Node Pools**: Use multiple node pools for different workloads
2. **Autoscaling**: Enable cluster autoscaler for cost optimization
3. **Security**: Use workload identity, enable Azure RBAC
4. **Networking**: Use Azure CNI for production workloads
5. **Monitoring**: Enable Container Insights for observability

## Common Workflows

### Deploy Application to AKS
1. Create AKS cluster with managed identity
2. Attach ACR for container images
3. Deploy application manifests
4. Configure ingress for external access
5. Set up monitoring with Container Insights

### Set Up GitOps
1. Enable Flux extension on AKS
2. Create Git repository with manifests
3. Configure Flux to sync from repository
4. Use Kustomize for environment overlays
5. Monitor sync status in Azure Portal
