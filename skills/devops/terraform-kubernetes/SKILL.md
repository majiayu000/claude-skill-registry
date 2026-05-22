---
name: terraform-kubernetes
description: Kubernetes cluster provisioning with Terraform across EKS, AKS, and GKE
sasmp_version: "1.3.0"
version: "2.0.0"
bonded_agent: 08-terraform-advanced
bond_type: SECONDARY_BOND
---

# Terraform Kubernetes Skill

Production patterns for Kubernetes cluster provisioning across cloud providers.

## AWS EKS

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "${var.project}-eks"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    default = {
      min_size     = 1
      max_size     = 10
      desired_size = 3

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"

      labels = {
        Environment = var.environment
      }
    }
  }

  manage_aws_auth_configmap = true

  aws_auth_roles = [
    {
      rolearn  = aws_iam_role.admin.arn
      username = "admin"
      groups   = ["system:masters"]
    }
  ]
}
```

## Azure AKS

```hcl
resource "azurerm_kubernetes_cluster" "main" {
  name                = "${var.project}-aks"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  dns_prefix          = var.project

  kubernetes_version        = "1.28"
  automatic_channel_upgrade = "stable"

  default_node_pool {
    name                = "system"
    node_count          = 3
    vm_size             = "Standard_D4s_v3"
    vnet_subnet_id      = azurerm_subnet.aks.id
    zones               = ["1", "2", "3"]
    enable_auto_scaling = true
    min_count           = 1
    max_count           = 10
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    network_policy = "azure"
  }

  azure_active_directory_role_based_access_control {
    managed            = true
    azure_rbac_enabled = true
  }
}
```

## GCP GKE

```hcl
resource "google_container_cluster" "main" {
  name     = "${var.project}-gke"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.private.name

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  private_cluster_config {
    enable_private_nodes    = true
    enable_private_endpoint = false
    master_ipv4_cidr_block  = "172.16.0.0/28"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }
}

resource "google_container_node_pool" "primary" {
  name       = "primary"
  location   = var.region
  cluster    = google_container_cluster.main.name
  node_count = 3

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  node_config {
    machine_type = "e2-standard-4"
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]

    workload_metadata_config {
      mode = "GKE_METADATA"
    }
  }
}
```

## Kubernetes Provider

```hcl
# After cluster creation
provider "kubernetes" {
  host                   = module.eks.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)

  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
  }
}

provider "helm" {
  kubernetes {
    host                   = module.eks.cluster_endpoint
    cluster_ca_certificate = base64decode(module.eks.cluster_certificate_authority_data)

    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      command     = "aws"
      args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name]
    }
  }
}
```

## Helm Releases

```hcl
resource "helm_release" "ingress_nginx" {
  name       = "ingress-nginx"
  repository = "https://kubernetes.github.io/ingress-nginx"
  chart      = "ingress-nginx"
  namespace  = "ingress-nginx"
  version    = "4.8.0"

  create_namespace = true

  set {
    name  = "controller.replicaCount"
    value = "3"
  }
}
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Unauthorized` | Token expired | Refresh kubeconfig |
| `Subnet full` | CIDR too small | Use larger CIDR |
| `Node not ready` | Resource limits | Check node capacity |

## Usage

```python
Skill("terraform-kubernetes")
```

## Related

- **Agent**: 08-terraform-advanced (SECONDARY_BOND)
