---
name: opentofu-kubernetes-explorer
description: Explore and manage Kubernetes clusters and resources using OpenTofu/Terraform
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: container-orchestration
---

# OpenTofu Kubernetes Explorer

## What I do

I guide you through managing Kubernetes clusters and resources using Kubernetes provider for OpenTofu/Terraform. I help you:

- **Cluster Management**: Deploy and manage Kubernetes clusters
- **Resource Deployment**: Create pods, deployments, services, and configmaps
- **Ingress and Networking**: Configure ingress controllers and network policies
- **Storage**: Create and manage persistent volumes and storage classes
- **Helm Charts**: Deploy Helm charts for complex applications
- **Best Practices**: Follow Kubernetes and provider documentation patterns

## When to use me

Use this skill when you need to:
- Automate Kubernetes resource management as code
- Deploy applications to Kubernetes clusters
- Manage Kubernetes configuration (ConfigMaps, Secrets)
- Configure ingress controllers and load balancers
- Setup persistent storage and storage classes
- Deploy Helm charts for application packages
- Manage multi-cluster Kubernetes deployments

**Note**: OpenTofu and Terraform are used interchangeably throughout this skill. OpenTofu is an open-source implementation of Terraform and maintains full compatibility with Terraform providers.

## Prerequisites

- **OpenTofu CLI installed**: Install from https://opentofu.org/docs/intro/install/
- **Kubernetes Cluster**: Running Kubernetes cluster (EKS, GKE, AKS, or self-managed)
- **kubectl**: Kubernetes command-line tool for local testing
- **kubeconfig**: Valid Kubernetes configuration file
- **Basic Kubernetes Knowledge**: Understanding of pods, services, deployments, and concepts

## Provider Documentation

- **Terraform Registry (Kubernetes Provider)**: https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs
- **Latest Provider Version**: hashicorp/kubernetes ~> 2.24.0
- **Provider Source**: https://github.com/hashicorp/terraform-provider-kubernetes
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Helm Provider**: https://registry.terraform.io/providers/hashicorp/helm/latest/docs

## Steps

### Step 1: Install and Configure OpenTofu

```bash
# Verify OpenTofu installation
tofu version

# Initialize project
mkdir kubernetes-terraform
cd kubernetes-terraform
tofu init
```

### Step 2: Configure Kubernetes Provider

Create `versions.tf`:

```hcl
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.24.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11.0"
    }
  }
  required_version = ">= 1.0"

  # Remote state backend
  backend "s3" {
    bucket         = "terraform-state"
    key            = "kubernetes/terraform.tfstate"
    region         = "ap-southeast-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Step 3: Configure Provider Connection

Create `provider.tf`:

```hcl
provider "kubernetes" {
  # Method 1: Use default kubeconfig (recommended)
  # Uses ~/.kube/config by default
  # Best for local development and single cluster

  # Method 2: Specify kubeconfig path
  config_path = var.kubeconfig_path

  # Method 3: Use config context
  config_context = "my-cluster-context"

  # Method 4: Direct cluster configuration (for EKS)
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token

  # Namespace configuration
  config_context_auth_info = false
}

provider "helm" {
  kubernetes {
    config_path = var.kubeconfig_path
  }
}
```

### Step 4: Configure Environment Variables

```bash
# Method 1: Use default kubeconfig
# Provider automatically uses ~/.kube/config

# Method 2: Specify kubeconfig path
export KUBECONFIG="/path/to/kubeconfig"

# Method 3: Use config context
export KUBECONFIG="/path/to/kubeconfig"
kubectl config use-context my-cluster-context

# Method 4: For EKS with AWS credentials
# Set AWS environment variables
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="ap-southeast-1"
```

### Step 5: Create Namespace

Create `namespace.tf`:

```hcl
# Application namespace
resource "kubernetes_namespace" "app" {
  metadata {
    name = var.app_namespace
    labels = {
      app       = var.application_name
      managedBy = "terraform"
      environment = var.environment
    }
  }
}

# Monitoring namespace
resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
    labels = {
      name   = "monitoring"
      managedBy = "terraform"
    }
  }
}

# Ingress namespace
resource "kubernetes_namespace" "ingress" {
  metadata {
    name = "ingress-nginx"
    labels = {
      app   = "ingress-nginx"
      managedBy = "terraform"
    }
  }
}
```

### Step 6: Create ConfigMap and Secret

Create `config.tf`:

```hcl
# Application ConfigMap
resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "app-config"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  data = {
    "application.properties" = <<-EOT
      server.port=8080
      database.url=${var.database_url}
      logging.level=INFO
      environment=${var.environment}
    EOT

    "logback.xml" = file("${path.module}/config/logback.xml")
  }
}

# Application Secret
resource "kubernetes_secret" "app_secret" {
  metadata {
    name      = "app-secret"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  data = {
    "database-password" = var.database_password
    "api-key"          = var.api_key
  }

  type = "Opaque"
}
```

### Step 7: Create Deployment

Create `deployment.tf`:

```hcl
# Application Deployment
resource "kubernetes_deployment" "app" {
  metadata {
    name      = var.application_name
    namespace = kubernetes_namespace.app.metadata[0].name
    labels = {
      app = var.application_name
    }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = {
        app = var.application_name
      }
    }

    template {
      metadata {
        labels = {
          app = var.application_name
        }
      }

      spec {
        container {
          name  = "app"
          image = var.container_image

          port {
            container_port = 8080
          }

          # Environment variables
          env {
            name  = "SERVER_PORT"
            value = "8080"
          }

          env {
            name = "DATABASE_URL"
            value_from {
              secret_key_ref {
                name = kubernetes_secret.app_secret.metadata[0].name
                key  = "database-password"
              }
            }
          }

          # Resource limits
          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }

          # Liveness probe
          liveness_probe {
            http_get {
              path = "/health"
              port = 8080
            }
            initial_delay_seconds = 10
            period_seconds        = 10
            timeout_seconds      = 5
            failure_threshold    = 3
          }

          # Readiness probe
          readiness_probe {
            http_get {
              path = "/ready"
              port = 8080
            }
            initial_delay_seconds = 5
            period_seconds        = 5
            timeout_seconds      = 3
            failure_threshold    = 2
          }
        }
      }
    }
  }

  # Prevent pod disruption during update
  strategy {
    type = "RollingUpdate"

    rolling_update {
      max_surge       = 1
      max_unavailable = 0
    }
  }
}
```

### Step 8: Create Service

Create `service.tf`:

```hcl
# Application Service (ClusterIP)
resource "kubernetes_service" "app" {
  metadata {
    name      = var.application_name
    namespace = kubernetes_namespace.app.metadata[0].name
    labels = {
      app = var.application_name
    }
  }

  spec {
    type = "ClusterIP"

    selector {
      app = var.application_name
    }

    port {
      name        = "http"
      protocol    = "TCP"
      port        = 80
      target_port = 8080
    }
  }
}

# Application Service (LoadBalancer)
resource "kubernetes_service" "app_lb" {
  metadata {
    name      = "${var.application_name}-lb"
    namespace = kubernetes_namespace.app.metadata[0].name
    labels = {
      app = var.application_name
    }
    annotations = {
      "service.beta.kubernetes.io/aws-load-balancer-type" = "nlb"
    }
  }

  spec {
    type = "LoadBalancer"

    selector {
      app = var.application_name
    }

    port {
      name        = "http"
      protocol    = "TCP"
      port        = 80
      target_port = 8080
    }

    port {
      name        = "https"
      protocol    = "TCP"
      port        = 443
      target_port = 8080
    }
  }
}

# Headless Service for StatefulSets
resource "kubernetes_service" "app_headless" {
  metadata {
    name      = "${var.application_name}-headless"
    namespace = kubernetes_namespace.app.metadata[0].name
    labels = {
      app = var.application_name
    }
  }

  spec {
    type = "ClusterIP"
    cluster_ip = "None"

    selector {
      app = var.application_name
    }

    port {
      name        = "http"
      protocol    = "TCP"
      port        = 8080
      target_port = 8080
    }
  }
}
```

### Step 9: Create Ingress

Create `ingress.tf`:

```hcl
# Ingress Controller Deployment (nginx)
resource "helm_release" "ingress_nginx" {
  name       = "ingress-nginx"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  namespace  = kubernetes_namespace.ingress.metadata[0].name

  set {
    name  = "controller.service.type"
    value = "LoadBalancer"
  }

  set {
    name  = "controller.publishService.enabled"
    value = "true"
  }
}

# Application Ingress
resource "kubernetes_ingress" "app" {
  metadata {
    name      = var.application_name
    namespace = kubernetes_namespace.app.metadata[0].name
    labels = {
      app = var.application_name
    }
    annotations = {
      "kubernetes.io/ingress.class"           = "nginx"
      "cert-manager.io/cluster-issuer"         = "letsencrypt-prod"
      "nginx.ingress.kubernetes.io/ssl-redirect" = "true"
    }
  }

  spec {
    rule {
      host = var.ingress_host

      http {
        path {
          backend {
            service_name = kubernetes_service.app.metadata[0].name
            service_port = 80
          }

          path = "/"
        }
      }
    }

    tls {
      hosts       = [var.ingress_host]
      secret_name = kubernetes_secret.tls_cert.metadata[0].name
    }
  }
}
```

### Step 10: Create Persistent Volume

Create `storage.tf`:

```hcl
# Storage Class
resource "kubernetes_storage_class" "gp2" {
  metadata {
    name = "gp2"
  }

  storage_provisioner = "kubernetes.io/aws-ebs"
  parameters = {
    type = "gp2"
  }

  allow_volume_expansion = true

  reclaim_policy = "Retain"
  volume_binding_mode = "WaitForFirstConsumer"
}

# Persistent Volume Claim
resource "kubernetes_persistent_volume_claim" "data" {
  metadata {
    name      = "app-data"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  spec {
    access_modes       = ["ReadWriteOnce"]
    storage_class_name = kubernetes_storage_class.gp2.metadata[0].name

    resources {
      requests = {
        storage = "10Gi"
      }
    }
  }
}
```

### Step 11: Deploy Helm Chart

Create `helm.tf`:

```hcl
# Redis Deployment
resource "helm_release" "redis" {
  name       = "redis"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "redis"
  namespace  = kubernetes_namespace.app.metadata[0].name
  version    = "17.11.0"

  set {
    name  = "auth.enabled"
    value = "true"
  }

  set {
    name  = "auth.password"
    value = var.redis_password
  }

  set {
    name  = "persistence.enabled"
    value = "true"
  }

  set {
    name  = "persistence.size"
    value = "8Gi"
  }
}

# PostgreSQL Deployment
resource "helm_release" "postgresql" {
  name       = "postgresql"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"
  namespace  = kubernetes_namespace.app.metadata[0].name
  version    = "12.5.0"

  set {
    name  = "auth.enablePostgresUser"
    value = "true"
  }

  set {
    name  = "auth.password"
    value = var.postgresql_password
  }

  set {
    name  = "auth.database"
    value = "appdb"
  }

  set {
    name  = "primary.persistence.enabled"
    value = "true"
  }

  set {
    name  = "primary.persistence.size"
    value = "20Gi"
  }
}
```

### Step 12: Create Horizontal Pod Autoscaler

Create `autoscaler.tf`:

```hcl
resource "kubernetes_horizontal_pod_autoscaler" "app" {
  metadata {
    name      = "${var.application_name}-hpa"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  spec {
    scale_target_ref {
      api_version = "apps/v1"
      kind       = "Deployment"
      name       = kubernetes_deployment.app.metadata[0].name
    }

    min_replicas = var.min_replicas
    max_replicas = var.max_replicas

    target_cpu_utilization_percentage    = 60
    target_memory_utilization_percentage = 70
  }
}
```

### Step 13: Define Variables

Create `variables.tf`:

```hcl
variable "kubeconfig_path" {
  description = "Path to kubeconfig file"
  type        = string
  default     = "~/.kube/config"
}

variable "app_namespace" {
  description = "Application namespace"
  type        = string
  default     = "app"
}

variable "application_name" {
  description = "Application name"
  type        = string
}

variable "container_image" {
  description = "Container image to deploy"
  type        = string
}

variable "replicas" {
  description = "Number of replicas"
  type        = number
  default     = 3
}

variable "min_replicas" {
  description = "Minimum replicas for autoscaling"
  type        = number
  default     = 2
}

variable "max_replicas" {
  description = "Maximum replicas for autoscaling"
  type        = number
  default     = 10
}

variable "database_url" {
  description = "Database connection URL"
  type        = string
  sensitive   = true
}

variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "api_key" {
  description = "API key"
  type        = string
  sensitive   = true
}

variable "ingress_host" {
  description = "Ingress host"
  type        = string
}

variable "redis_password" {
  description = "Redis password"
  type        = string
  sensitive   = true
}

variable "postgresql_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Step 14: Create Outputs

Create `outputs.tf`:

```hcl
output "namespace" {
  description = "Application namespace"
  value       = kubernetes_namespace.app.metadata[0].name
}

output "deployment_name" {
  description = "Application deployment name"
  value       = kubernetes_deployment.app.metadata[0].name
}

output "service_name" {
  description = "Application service name"
  value       = kubernetes_service.app.metadata[0].name
}

output "load_balancer_url" {
  description = "Load balancer URL"
  value       = kubernetes_service.app_lb.status[0].load_balancer[0].ingress[0].hostname
}

output "ingress_url" {
  description = "Ingress URL"
  value       = "https://${var.ingress_host}"
}
```

### Step 15: Initialize and Apply

```bash
# Set kubeconfig
export KUBECONFIG="/path/to/kubeconfig"

# Initialize providers
tofu init

# Plan changes
tofu plan -out=tfplan

# Apply changes
tofu apply tfplan

# Show outputs
tofu output

# Verify deployment
kubectl get all -n $APP_NAMESPACE
kubectl logs -f deployment/app -n $APP_NAMESPACE
```

## Best Practices

### Resource Management

1. **Use Namespaces**: Separate resources by namespace for isolation
2. **Label Everything**: Apply consistent labels to all resources
3. **Resource Limits**: Set appropriate resource requests and limits
4. **Probes**: Configure liveness and readiness probes
5. **Strategy**: Use RollingUpdate for zero-downtime deployments

### Security

1. **Least Privilege**: Use RBAC to restrict permissions
2. **Secrets Management**: Never store secrets in ConfigMaps; use Kubernetes Secrets
3. **Network Policies**: Implement network policies for pod-to-pod communication
4. **Image Security**: Use signed and verified container images
5. **Pod Security Context**: Define security context for pods and containers

### High Availability

1. **Replicas**: Deploy multiple replicas for critical applications
2. **Anti-Affinity**: Distribute pods across nodes
3. **Pod Disruption Budgets**: Configure PDBs to prevent voluntary disruptions
4. **Health Checks**: Use liveness and readiness probes
5. **Autoscaling**: Configure HPA for automatic scaling

### Storage

1. **Storage Classes**: Use appropriate storage classes for your use case
2. **Persistent Volumes**: Use PVCs for stateful applications
3. **Volume Expansion**: Enable storage expansion when possible
4. **Backup**: Implement backup strategies for persistent data
5. **StatefulSets**: Use StatefulSets for databases and stateful apps

### Ingress and Networking

1. **Ingress Controller**: Deploy an ingress controller for external access
2. **TLS Termination**: Use TLS termination at ingress
3. **Cert-Manager**: Automate TLS certificate management
4. **Load Balancer Type**: Choose appropriate LB type (ALB, NLB, etc.)
5. **DNS**: Configure DNS records for ingress hosts

### Helm Charts

1. **Version Pinning**: Pin chart versions for reproducibility
2. **Values Override**: Use `set` blocks to override default values
3. **Namespace Isolation**: Deploy charts in dedicated namespaces
4. **Release Management**: Use meaningful release names
5. **Upgrade Strategy**: Understand chart upgrade strategies

## Common Issues

### Issue: Provider Connection Failed

**Symptom**: Error `Error: Failed to configure provider`

**Solution**:
```bash
# Verify kubeconfig
kubectl cluster-info
kubectl config current-context

# Check kubeconfig path
ls -la ~/.kube/config

# Test connection
kubectl get nodes

# Verify KUBECONFIG environment variable
echo $KUBECONFIG

# For EKS with AWS credentials
aws eks describe-cluster --name my-cluster --region ap-southeast-1
```

### Issue: Image Pull Error

**Symptom**: Error `Failed to pull image`

**Solution**:
```bash
# Verify image exists
docker pull <image-name>

# Check image registry access
docker login <registry-url>

# Use image pull secrets
kubectl create secret docker-registry regcred \
  --docker-server=<registry-url> \
  --docker-username=<username> \
  --docker-password=<password>

# Reference: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
```

### Issue: Pod Pending State

**Symptom**: Pods stuck in Pending state

**Solution**:
```bash
# Describe pod for details
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'

# Common issues:
# - Insufficient resources (check requests/limits)
# - Node affinity (check node selectors)
# - Taints and tolerations
# - Image pull errors
```

### Issue: Service Not Accessible

**Symptom**: Service is created but not accessible

**Solution**:
```bash
# Check service endpoints
kubectl get endpoints <service-name>

# Verify pod labels match service selector
kubectl get pods --show-labels

# Check service type
# ClusterIP: Only accessible within cluster
# LoadBalancer: External access via LB DNS/URL
# NodePort: External access via NodeIP:Port

# For LoadBalancer, check firewall/security groups
# Allow traffic to LB ports
```

### Issue: Ingress Not Working

**Symptom**: Ingress created but traffic not reaching pods

**Solution**:
```bash
# Verify ingress controller is running
kubectl get pods -n ingress-nginx

# Check ingress class annotation
kubectl describe ingress <ingress-name>

# Verify TLS secret exists
kubectl get secret <tls-secret-name>

# Check ingress backend service
kubectl get svc <backend-service-name>

# Check DNS resolution
nslookup <ingress-host>
dig <ingress-host>

# Reference: https://kubernetes.io/docs/concepts/services-networking/ingress/
```

### Issue: Persistent Volume Not Mounting

**Symptom**: Pod fails with volume mount errors

**Solution**:
```bash
# Check PVC status
kubectl get pvc

# Check storage class
kubectl get sc

# Verify volume exists
kubectl get pv

# Check pod events
kubectl describe pod <pod-name> | grep -A 10 Events

# Ensure storage class supports dynamic provisioning
# Check reclaim_policy and volume_binding_mode
```

### Issue: Helm Chart Upgrade Failed

**Symptom**: Error `Error: failed to upgrade release`

**Solution**:
```bash
# Check Helm release history
helm list -n <namespace>

# Get current values
helm get values <release-name> -n <namespace>

# Dry-run upgrade
helm upgrade --dry-run <release-name> <chart> -n <namespace>

# Rollback if needed
helm rollback <release-name> <revision> -n <namespace>

# Check chart compatibility
# Ensure chart version supports Kubernetes version
kubectl version
helm search repo <chart-name> --versions
```

### Issue: Autoscaling Not Working

**Symptom**: HPA not scaling pods

**Solution**:
```bash
# Check HPA status
kubectl get hpa

# Describe HPA for details
kubectl describe hpa <hpa-name>

# Check resource requests (required for HPA)
kubectl describe pod <pod-name> | grep -A 5 Requests

# Verify metrics server is running
kubectl get pods -n kube-system | grep metrics

# Check metrics availability
kubectl top nodes
kubectl top pods
```

## Reference Documentation

- **Terraform Registry (Kubernetes Provider)**: https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Helm Documentation**: https://helm.sh/docs/
- **Kubernetes API Reference**: https://kubernetes.io/docs/reference/
- **OpenTofu Documentation**: https://opentofu.org/docs/
- **kubectl Documentation**: https://kubernetes.io/docs/reference/kubectl/

## Examples

### Complete Application Deployment

```hcl
# namespace.tf
resource "kubernetes_namespace" "app" {
  metadata {
    name = "production"
  }
}

# config.tf
resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "app-config"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  data = {
    "config.json" = jsonencode({
      port = 8080
      env  = "production"
    })
  }
}

# deployment.tf
resource "kubernetes_deployment" "app" {
  metadata {
    name      = "webapp"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  spec {
    replicas = 3

    template {
      spec {
        container {
          name  = "webapp"
          image = "nginx:1.21"

          port {
            container_port = 80
          }

          resources {
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}
```

### Ingress with TLS

```hcl
# ingress.tf
resource "kubernetes_ingress" "app" {
  metadata {
    name      = "webapp-ingress"
    namespace = kubernetes_namespace.app.metadata[0].name
    annotations = {
      "kubernetes.io/ingress.class" = "nginx"
      "cert-manager.io/cluster-issuer" = "letsencrypt-prod"
    }
  }

  spec {
    rule {
      host = "app.example.com"

      http {
        path {
          backend {
            service_name = kubernetes_service.webapp.metadata[0].name
            service_port = 80
          }
        }
      }
    }

    tls {
      hosts       = ["app.example.com"]
      secret_name = kubernetes_secret.tls_cert.metadata[0].name
    }
  }
}
```

### Helm Chart Deployment

```hcl
# helm.tf
resource "helm_release" "redis" {
  name       = "redis"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "redis"
  namespace  = kubernetes_namespace.app.metadata[0].name

  set {
    name  = "auth.enabled"
    value = "true"
  }

  set {
    name  = "auth.password"
    value = var.redis_password
  }

  set {
    name  = "master.persistence.size"
    value = "8Gi"
  }
}
```

### EKS Cluster with Kubernetes Provider

```hcl
# eks.tf
resource "aws_eks_cluster" "main" {
  name     = "my-eks-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = "1.27"

  vpc_config {
    subnet_ids = aws_subnet.public[*].id
  }
}

data "aws_eks_cluster" "cluster" {
  name = aws_eks_cluster.main.name
}

data "aws_eks_cluster_auth" "cluster" {
  name = aws_eks_cluster.main.name
}

# kubernetes.tf
provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority[0].data)
  token                  = data.aws_eks_cluster_auth.cluster.token
}

resource "kubernetes_deployment" "app" {
  metadata {
    name      = "app"
    namespace = kubernetes_namespace.app.metadata[0].name
  }

  spec {
    template {
      spec {
        container {
          name  = "app"
          image = "my-app:latest"
        }
      }
    }
  }
}
```

## Tips and Tricks

- **Use kubectl**: Verify Terraform-created resources with kubectl
- **Dry Run**: Use `helm upgrade --dry-run` to test changes
- **Port Forward**: Use `kubectl port-forward` for local debugging
- **Logs**: Use `kubectl logs -f` for real-time debugging
- **Describe Everything**: Use `kubectl describe` for detailed resource information
- **Events**: Check events for troubleshooting issues
- **Resource Labels**: Use labels for organization and discovery
- **Namespace Isolation**: Use namespaces for environment separation
- **Helm Values**: Use `helm show values` to understand default configuration
- **Version Control**: Store Helm values files in version control
- **Import Resources**: Import existing Kubernetes resources into Terraform state

## Next Steps

After mastering Kubernetes provider, explore:
- **Kubernetes Advanced**: Learn about StatefulSets, DaemonSets, and Jobs
- **Kubernetes Operators**: Deploy operators for complex applications
- **Service Mesh**: Implement Istio or Linkerd for service-to-service communication
- **GitOps**: Use ArgoCD or Flux for GitOps workflows
- **Monitoring**: Deploy Prometheus and Grafana for observability
- **Kubernetes Security**: Learn about RBAC, network policies, and security contexts
- **Kubernetes Best Practices**: Follow K8s best practices for production workloads
