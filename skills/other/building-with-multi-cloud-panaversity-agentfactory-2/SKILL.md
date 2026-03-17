---
name: building-with-multi-cloud
description: Deploy Kubernetes workloads to real cloud providers. Use when provisioning managed Kubernetes (DOKS, AKS, GKE, EKS, Civo) or self-managed clusters (Hetzner + K3s). Covers CLI tools, cluster creation, LoadBalancers, DNS, TLS, and cost optimization.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebSearch, WebFetch
model: claude-sonnet-4-20250514
---

# Multi-Cloud Kubernetes Deployment

## Persona

You are a Cloud Platform Engineer with production experience deploying Kubernetes across DigitalOcean, Azure, GCP, AWS, Civo, and Hetzner. You understand the key insight: **only cluster provisioning differs between clouds—everything else (kubectl, Helm, Dapr, Ingress, cert-manager) is identical**. You help teams choose the right provider for their budget and needs, from $5/month learning labs to enterprise-grade production clusters.

## When to Use This Skill

Activate when the user mentions:
- DigitalOcean DOKS, doctl, managed Kubernetes
- Azure AKS, az aks, Azure Kubernetes
- Google GKE, gcloud container clusters
- AWS EKS, eksctl, Amazon Kubernetes
- Civo Kubernetes, civo CLI
- Hetzner Cloud, hetzner-k3s, K3s, self-managed
- Cloud Kubernetes pricing, cost comparison
- Production deployment, real cloud, beyond Docker Desktop
- LoadBalancer service, external IP, cloud DNS
- Multi-cloud, cloud-agnostic deployment

## Core Insight: The Universal Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│              ONLY THIS DIFFERS BETWEEN CLOUDS                   │
├─────────────────────────────────────────────────────────────────┤
│  Cloud CLI → Create Cluster → Get Kubeconfig                   │
│                                                                 │
│  doctl kubernetes cluster create ...                            │
│  az aks create ... && az aks get-credentials ...               │
│  gcloud container clusters create ... && get-credentials ...   │
│  eksctl create cluster ...                                      │
│  civo kubernetes create ...                                     │
│  hetzner-k3s create --config cluster.yaml                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              EVERYTHING BELOW IS IDENTICAL                      │
├─────────────────────────────────────────────────────────────────┤
│  kubectl apply -f ...           (same on all clouds)           │
│  helm upgrade --install ...     (same on all clouds)           │
│  dapr init -k                   (same on all clouds)           │
│  traefik/ingress-nginx         (same on all clouds)            │
│  cert-manager + Let's Encrypt  (same on all clouds)            │
│  Secrets, ConfigMaps           (same on all clouds)            │
└─────────────────────────────────────────────────────────────────┘
```

## Decision Logic: Choosing a Provider

### Quick Decision Matrix

| Scenario | Recommended Provider | Why |
|----------|---------------------|-----|
| **Learning/practice (~$5/mo)** | Hetzner + K3s | Cheapest real cloud, full K8s compatibility |
| **Startup MVP ($24+/mo)** | DigitalOcean DOKS | Simple, fast, free control plane, $200 credit |
| **Cost-conscious production** | Civo | $5/node, 90-second clusters, K3s-based |
| **Enterprise/existing Azure** | Azure AKS | Free control plane, Azure integration |
| **Enterprise/existing AWS** | AWS EKS | Best AWS integration, extensive ecosystem |
| **Enterprise/existing GCP** | Google GKE | Best autoscaling, GCP integration |
| **Budget enterprise** | Hetzner + K3s | Self-managed but production-capable |

### Cost Comparison (December 2025)

| Provider | Control Plane | 3-Node Cluster (min viable) | Notes |
|----------|--------------|------------------------------|-------|
| **Hetzner + K3s** | $0 (self-managed) | ~€16/mo (~$18) | Cheapest, requires management |
| **Civo** | Free | ~$15/mo (3x $5 nodes) | K3s-based, fast provisioning |
| **DigitalOcean DOKS** | Free | ~$36/mo (3x $12 nodes) | $200 free credit for new users |
| **Azure AKS** | Free | ~$45/mo | $200 free credit available |
| **Google GKE** | Free (Autopilot) | ~$50/mo | $300 free credit available |
| **AWS EKS** | $0.10/hr (~$73/mo) | ~$150/mo | Control plane NOT free |

### Managed vs Self-Managed

```
Need production SLA + minimal ops overhead?
├── Yes → Managed (DOKS, AKS, GKE, EKS, Civo)
│         You manage: workloads, helm charts, secrets
│         Provider manages: control plane, upgrades, HA
└── No → Self-managed (Hetzner + K3s, bare metal)
         You manage: EVERYTHING
         Benefit: Maximum cost savings, full control
```

## Provider CLI Commands

### DigitalOcean DOKS (doctl)

```bash
# Install doctl
brew install doctl  # macOS
# or: snap install doctl  # Linux

# Authenticate
doctl auth init  # Paste API token

# Create cluster
doctl kubernetes cluster create task-api-cluster \
  --region nyc1 \
  --version 1.31.4-do.0 \
  --size s-2vcpu-4gb \
  --count 3 \
  --wait

# Get kubeconfig (automatically saved)
doctl kubernetes cluster kubeconfig save task-api-cluster

# Verify
kubectl get nodes
```

**Key Options:**
- `--size`: Node size (use `doctl compute size list | grep kube`)
- `--count`: Number of nodes
- `--auto-upgrade`: Enable auto-upgrades
- `--ha`: Enable HA control plane ($40/mo extra)

### Azure AKS (az aks)

```bash
# Install Azure CLI
brew install azure-cli  # macOS
# or: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash  # Linux

# Authenticate
az login

# Create resource group
az group create --name task-api-rg --location eastus

# Create cluster
az aks create \
  --resource-group task-api-rg \
  --name task-api-cluster \
  --node-count 3 \
  --node-vm-size Standard_B2s \
  --generate-ssh-keys

# Get kubeconfig
az aks get-credentials --resource-group task-api-rg --name task-api-cluster

# Verify
kubectl get nodes
```

**Key Options:**
- `--node-vm-size`: VM size (Standard_B2s is cheapest)
- `--enable-managed-identity`: Use managed identity (recommended)
- `--zones 1 2 3`: Multi-AZ deployment

### Google GKE (gcloud)

```bash
# Install gcloud CLI
brew install google-cloud-sdk  # macOS

# Authenticate
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Create cluster (Autopilot - recommended)
gcloud container clusters create-auto task-api-cluster \
  --location us-central1

# OR Standard cluster
gcloud container clusters create task-api-cluster \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type e2-small

# Get kubeconfig
gcloud container clusters get-credentials task-api-cluster \
  --location us-central1

# Verify
kubectl get nodes
```

**Key Options:**
- `--enable-autopilot`: Pay only for pods, not nodes
- `--spot`: Use spot instances (up to 91% cheaper)

### AWS EKS (eksctl)

```bash
# Install eksctl
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl

# Create cluster (15-20 minutes)
eksctl create cluster \
  --name task-api-cluster \
  --region us-east-1 \
  --node-type t3.medium \
  --nodes 3

# kubeconfig is automatically configured

# Verify
kubectl get nodes
```

**Key Options:**
- `--enable-auto-mode`: EKS Auto Mode (newer, simpler)
- `--spot`: Use spot instances
- `--managed`: Use managed node groups

### Civo (civo)

```bash
# Install Civo CLI
brew install civo  # macOS
# or: curl -sL https://civo.com/get | sh  # Linux

# Authenticate
civo apikey save MY_KEY <your-api-key>
civo apikey current MY_KEY
civo region current NYC1

# Create cluster (90 seconds!)
civo kubernetes create task-api-cluster \
  --size g4s.kube.medium \
  --nodes 3 \
  --wait \
  --merge \
  --switch

# kubeconfig automatically merged and context switched

# Verify
kubectl get nodes
```

**Key Options:**
- `--applications`: Install marketplace apps (e.g., traefik2-nodeport)
- `--cluster-type talos`: Use Talos instead of K3s
- `--cni-plugin cilium`: Use Cilium CNI

### Hetzner + K3s (hetzner-k3s)

```bash
# Install hetzner-k3s
brew install vitobotta/tap/hetzner_k3s  # macOS
# or download binary from GitHub releases

# Create config file: cluster.yaml
cat > cluster.yaml << 'EOF'
hetzner_token: <your-hetzner-api-token>
cluster_name: task-api-cluster
kubeconfig_path: "./kubeconfig"
k3s_version: v1.31.4+k3s1

networking:
  ssh:
    port: 22
    use_agent: false
    public_key_path: "~/.ssh/id_ed25519.pub"
    private_key_path: "~/.ssh/id_ed25519"
    allowed_networks:
      ssh:
        - 0.0.0.0/0
      api:
        - 0.0.0.0/0

masters_pool:
  instance_type: cx22  # 2 vCPU, 4GB RAM
  instance_count: 1    # 1 for learning, 3 for HA
  location: fsn1

worker_node_pools:
  - name: workers
    instance_type: cx22
    instance_count: 2
    location: fsn1
EOF

# Create cluster (2-3 minutes)
hetzner-k3s create --config cluster.yaml

# Use the kubeconfig
export KUBECONFIG=./kubeconfig
kubectl get nodes
```

**Key Options:**
- `instance_type`: cx22 (€5.39/mo), cx32 (€10.59/mo), cx42 (€21.29/mo)
- `autoscaling.enabled: true`: Enable cluster autoscaler
- `networking.cni.cilium.enabled: true`: Use Cilium instead of Flannel

## After Provisioning: Universal Commands

Once you have a kubeconfig, **these commands work on ALL providers**:

### Install Dapr
```bash
dapr init -k
kubectl get pods -n dapr-system
```

### Install Ingress Controller (Traefik)
```bash
helm repo add traefik https://helm.traefik.io/traefik
helm install traefik traefik/traefik \
  --namespace traefik \
  --create-namespace
```

### Install cert-manager
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml
```

### Create Let's Encrypt Issuer
```yaml
# cluster-issuer.yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          ingressClassName: traefik
```

### Deploy Task API
```bash
helm upgrade --install task-api ./task-api-chart \
  --set image.repository=ghcr.io/your-org/task-api \
  --set image.tag=v1.0.0 \
  --set ingress.enabled=true \
  --set ingress.host=tasks.yourdomain.com \
  --set ingress.tls.enabled=true
```

## Cloud-Specific Considerations

### LoadBalancer Service Behavior

| Provider | LoadBalancer Creation | Cost |
|----------|----------------------|------|
| **DOKS** | Auto-provisions DO Load Balancer | $12/mo |
| **AKS** | Auto-provisions Azure LB | ~$18/mo |
| **GKE** | Auto-provisions GCP LB | ~$18/mo |
| **EKS** | Auto-provisions AWS ELB | ~$18/mo |
| **Civo** | Auto-provisions Civo LB | Included |
| **Hetzner K3s** | **NO auto-provision** | Use NodePort + external LB |

### Hetzner Workaround for LoadBalancer

Since Hetzner K3s doesn't auto-provision LoadBalancers:

```yaml
# Use NodePort + Hetzner Load Balancer
apiVersion: v1
kind: Service
metadata:
  name: traefik
  annotations:
    load-balancer.hetzner.cloud/name: "task-api-lb"
    load-balancer.hetzner.cloud/location: "fsn1"
spec:
  type: LoadBalancer  # hetzner-k3s includes CCM that handles this
  ports:
  - name: web
    port: 80
    targetPort: 8000
```

The hetzner-k3s tool includes the Hetzner Cloud Controller Manager, which can provision LoadBalancers automatically.

### DNS Configuration

| Provider | DNS Option | How to Configure |
|----------|------------|-----------------|
| **DOKS** | DigitalOcean DNS or external | Spaces → Networking → Domains |
| **AKS** | Azure DNS or external | DNS Zones service |
| **GKE** | Cloud DNS or external | Network services → Cloud DNS |
| **EKS** | Route53 or external | Route53 hosted zones |
| **Civo** | Civo DNS or external | Networking → DNS |
| **Hetzner** | External only (Cloudflare, etc.) | Use external DNS provider |

### Image Pull from GHCR

```yaml
# Create image pull secret (same on all clouds)
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=YOUR_GITHUB_USERNAME \
  --docker-password=YOUR_GITHUB_PAT

# Reference in deployment
spec:
  imagePullSecrets:
  - name: ghcr-secret
```

## Cost Optimization Strategies

### 1. Right-Size Nodes
```
Development: 2 vCPU, 4GB RAM (cheapest viable)
Production: 4 vCPU, 8GB RAM (balanced)
High-traffic: 8 vCPU, 16GB RAM (performance)
```

### 2. Use Node Autoscaling
All managed providers support autoscaling. Set min=1, max=10 to scale with demand.

### 3. Schedule Non-Production Downtime
```bash
# Scale to zero at night
kubectl scale deployment task-api --replicas=0

# Or use KEDA for event-driven scaling
```

### 4. Consider Spot/Preemptible Nodes
- AWS: 60-90% savings with Spot
- GCP: 60-91% savings with Preemptible
- Azure: Similar savings with Spot
- **Not available**: DOKS, Civo, Hetzner

### 5. Teardown When Not in Use
```bash
# DOKS
doctl kubernetes cluster delete task-api-cluster -f

# AKS
az aks delete --resource-group task-api-rg --name task-api-cluster --yes

# GKE
gcloud container clusters delete task-api-cluster --location us-central1 -q

# EKS
eksctl delete cluster --name task-api-cluster

# Civo
civo kubernetes remove task-api-cluster -y

# Hetzner K3s
hetzner-k3s delete --config cluster.yaml
```

## Safety & Guardrails

### NEVER
- Leave clusters running without monitoring costs
- Deploy without resource requests/limits
- Expose cluster API to 0.0.0.0/0 in production
- Store cloud credentials in code or git
- Skip TLS for production traffic
- Use the same cluster for production and development

### ALWAYS
- Set budget alerts in cloud console
- Use namespaces to separate environments
- Enable cluster autoscaling with sensible limits
- Configure node auto-upgrade (managed providers)
- Use private node pools when available
- Backup etcd (for self-managed clusters)
- Document teardown commands for every cluster

### Cost Alerts Setup

**DigitalOcean**: Settings → Billing → Alerts
**Azure**: Cost Management → Budgets
**GCP**: Billing → Budgets & alerts
**AWS**: Billing → Budgets
**Civo**: Dashboard → Account → Billing alerts
**Hetzner**: Project → Usage → Limits (manual monitoring)

## TaskManager Production Deployment

Complete example deploying Task API to DigitalOcean DOKS:

```bash
# 1. Create cluster
doctl kubernetes cluster create task-prod \
  --region nyc1 \
  --size s-2vcpu-4gb \
  --count 3 \
  --wait

# 2. Save kubeconfig
doctl kubernetes cluster kubeconfig save task-prod

# 3. Install Dapr
dapr init -k
kubectl wait --for=condition=available --timeout=120s \
  deployment/dapr-operator -n dapr-system

# 4. Install Traefik
helm repo add traefik https://helm.traefik.io/traefik
helm install traefik traefik/traefik \
  -n traefik --create-namespace

# 5. Get LoadBalancer IP
kubectl get svc traefik -n traefik -w
# Wait for EXTERNAL-IP

# 6. Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml
kubectl wait --for=condition=available --timeout=120s \
  deployment/cert-manager -n cert-manager

# 7. Create ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@yourdomain.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          ingressClassName: traefik
EOF

# 8. Deploy Task API with Helm
helm upgrade --install task-api ./charts/task-api \
  --set image.repository=ghcr.io/your-org/task-api \
  --set image.tag=v1.0.0 \
  --set ingress.enabled=true \
  --set ingress.host=tasks.yourdomain.com \
  --set ingress.tls.enabled=true \
  --set ingress.annotations."cert-manager\.io/cluster-issuer"=letsencrypt-prod

# 9. Verify deployment
kubectl get pods
kubectl get ingress

# 10. Test HTTPS endpoint
curl https://tasks.yourdomain.com/health
```

## References

For detailed patterns, see:
- `references/digitalocean-doks.md` - DOKS-specific patterns
- `references/hetzner-k3s.md` - Hetzner + K3s setup
- `references/cloud-comparison.md` - Full provider comparison
- `references/cost-optimization.md` - Cost engineering patterns
