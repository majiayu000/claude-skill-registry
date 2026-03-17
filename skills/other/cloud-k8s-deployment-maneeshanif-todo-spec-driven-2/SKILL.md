---
name: cloud-k8s-deployment
description: Deploy to cloud Kubernetes clusters - DigitalOcean DOKS primary, with multi-cloud patterns for AWS EKS and GKE. Use when deploying Phase 5 to production cloud environments. (project)
allowed-tools: Bash, Write, Read, Glob, Edit, Grep
---

# Cloud Kubernetes Deployment Skill

## Quick Start

1. **Read Phase 5 Constitution** - `constitution-prompt-phase-5.md`
2. **Choose cloud provider** - DigitalOcean DOKS (primary)
3. **Create cluster** - Using cloud CLI or Terraform
4. **Configure kubectl** - Get credentials
5. **Install prerequisites** - Ingress, cert-manager, Dapr
6. **Deploy with Helm** - Using environment-specific values

## Cloud Provider Comparison

| Feature | DigitalOcean DOKS | AWS EKS | Google GKE |
|---------|-------------------|---------|------------|
| **Cost** | $$ (Cheapest) | $$$$ | $$$ |
| **Ease** | Easy | Complex | Medium |
| **Managed** | Yes | Yes | Yes |
| **Free Tier** | None | Some | Some |
| **Best For** | Startups, MVP | Enterprise | ML/AI |

## DigitalOcean DOKS Setup (Primary)

### Install doctl CLI

```bash
# macOS
brew install doctl

# Linux
cd ~ && curl -OL https://github.com/digitalocean/doctl/releases/download/v1.104.0/doctl-1.104.0-linux-amd64.tar.gz
tar xf ~/doctl-1.104.0-linux-amd64.tar.gz
sudo mv ~/doctl /usr/local/bin

# Authenticate
doctl auth init
```

### Create DOKS Cluster

```bash
# Create cluster
doctl kubernetes cluster create todo-production \
  --region nyc1 \
  --version 1.29.1-do.0 \
  --node-pool "name=default;size=s-2vcpu-4gb;count=3;auto-scale=true;min-nodes=2;max-nodes=5" \
  --wait

# Get kubeconfig
doctl kubernetes cluster kubeconfig save todo-production

# Verify
kubectl get nodes
```

### Terraform Configuration

Create `terraform/digitalocean/main.tf`:

```hcl
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_kubernetes_cluster" "todo" {
  name    = "todo-production"
  region  = "nyc1"
  version = "1.29.1-do.0"

  node_pool {
    name       = "default"
    size       = "s-2vcpu-4gb"
    auto_scale = true
    min_nodes  = 2
    max_nodes  = 5
  }

  maintenance_policy {
    start_time = "04:00"
    day        = "sunday"
  }
}

resource "digitalocean_container_registry" "todo" {
  name                   = "todo-registry"
  subscription_tier_slug = "basic"
}

output "cluster_id" {
  value = digitalocean_kubernetes_cluster.todo.id
}

output "kubeconfig" {
  value     = digitalocean_kubernetes_cluster.todo.kube_config[0].raw_config
  sensitive = true
}
```

## Install Prerequisites

### NGINX Ingress Controller

```bash
# Install via Helm
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.publishService.enabled=true
```

### Cert-Manager (TLS)

```bash
# Install cert-manager
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
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
            class: nginx
EOF
```

### Dapr

```bash
# Install Dapr
helm repo add dapr https://dapr.github.io/helm-charts/
helm repo update

helm install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --wait
```

### Strimzi (Kafka)

```bash
# Install Strimzi operator
helm repo add strimzi https://strimzi.io/charts/
helm repo update

helm install strimzi-kafka-operator strimzi/strimzi-kafka-operator \
  --namespace kafka \
  --create-namespace
```

## Production Values File

Create `helm/evolution-todo/values-production.yaml`:

```yaml
global:
  environment: production
  domain: todo.yourdomain.com
  image:
    registry: ghcr.io
    repository: your-org/evolution-todo
    tag: latest
    pullPolicy: Always

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: todo.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api
          pathType: Prefix
          service: backend
  tls:
    - secretName: todo-tls
      hosts:
        - todo.yourdomain.com

backend:
  replicas: 3
  resources:
    requests:
      cpu: 250m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

frontend:
  replicas: 2
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

kafka:
  enabled: true
  external: true
  brokers: "redpanda-cloud-broker:9092"

redis:
  enabled: true
  cluster:
    enabled: false
  master:
    persistence:
      size: 5Gi

postgresql:
  enabled: false  # Using Neon
  external:
    host: "your-neon-host.neon.tech"
    database: "todo_prod"
```

## Deploy to Production

```bash
# Create namespace
kubectl create namespace todo-app

# Create secrets
kubectl create secret generic todo-secrets \
  --namespace todo-app \
  --from-literal=DATABASE_URL="postgresql://user:pass@host/db" \
  --from-literal=GEMINI_API_KEY="your-key" \
  --from-literal=BETTER_AUTH_SECRET="your-secret"

# Deploy with Helm
helm upgrade --install evolution-todo ./helm/evolution-todo \
  --namespace todo-app \
  --values ./helm/evolution-todo/values-production.yaml \
  --wait

# Verify deployment
kubectl get pods -n todo-app
kubectl get ingress -n todo-app
```

## DNS Configuration

After deployment, configure DNS:

```bash
# Get Load Balancer IP
kubectl get svc -n ingress-nginx ingress-nginx-controller -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Create A record:
# todo.yourdomain.com → <LOAD_BALANCER_IP>
```

## Multi-Environment Strategy

```
Production (DOKS)
├── Namespace: todo-app
├── Domain: todo.yourdomain.com
├── Database: Neon (Production)
├── Kafka: Redpanda Cloud
└── Replicas: 3-10 (autoscaled)

Staging (DOKS)
├── Namespace: todo-staging
├── Domain: staging.todo.yourdomain.com
├── Database: Neon (Staging)
├── Kafka: Strimzi (in-cluster)
└── Replicas: 1-3

Development (Minikube)
├── Namespace: todo-dev
├── Domain: localhost
├── Database: PostgreSQL (in-cluster)
├── Kafka: Strimzi (single node)
└── Replicas: 1
```

## Monitoring Setup

### Prometheus & Grafana

```bash
# Install kube-prometheus-stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=admin \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

### DigitalOcean Monitoring

```bash
# Enable cluster monitoring
doctl kubernetes cluster update todo-production \
  --enable-control-plane-monitoring
```

## Cost Optimization

| Resource | Development | Staging | Production |
|----------|-------------|---------|------------|
| Nodes | 1 (s-1vcpu-2gb) | 2 (s-2vcpu-4gb) | 3-5 (s-2vcpu-4gb) |
| Cost/month | ~$12 | ~$48 | ~$72-120 |
| Load Balancer | None | 1 ($12) | 1 ($12) |
| Block Storage | 10GB | 20GB | 50GB |

## Verification Checklist

- [ ] DOKS cluster created and running
- [ ] kubectl configured with cluster credentials
- [ ] Ingress controller installed
- [ ] Cert-manager installed with ClusterIssuer
- [ ] Dapr installed in dapr-system namespace
- [ ] Secrets created in todo-app namespace
- [ ] Helm deployment successful
- [ ] TLS certificate issued
- [ ] DNS configured
- [ ] Application accessible via domain
- [ ] Monitoring enabled

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Pods pending | No nodes | Check node pool autoscaling |
| TLS not working | Cert not issued | Check cert-manager logs |
| Ingress 502 | Backend unhealthy | Check pod health |
| DNS not resolving | A record missing | Add DNS record |
| High latency | Region mismatch | Deploy closer to users |

## References

- [DigitalOcean Kubernetes](https://docs.digitalocean.com/products/kubernetes/)
- [NGINX Ingress](https://kubernetes.github.io/ingress-nginx/)
- [Cert-Manager](https://cert-manager.io/docs/)
- [Dapr on Kubernetes](https://docs.dapr.io/operations/hosting/kubernetes/)
- [Phase 5 Constitution](../../../constitution-prompt-phase-5.md)
