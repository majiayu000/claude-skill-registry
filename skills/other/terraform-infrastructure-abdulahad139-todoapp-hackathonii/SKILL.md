---
name: terraform-infrastructure
description: Infrastructure as Code with Terraform for cloud Kubernetes clusters. Covers OKE (Oracle), AKS (Azure), GKE (Google) provisioning, multi-cloud patterns, and state management.
---

# Terraform Infrastructure Skill

Infrastructure as Code patterns using Terraform for provisioning cloud Kubernetes clusters.

## Quick Start

### Installation

```bash
# Terraform
# See: https://developer.hashicorp.com/terraform/downloads
```

## 1. Terraform Structure

### Directory Layout

```
terraform/
├── oke/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── terraform.tfstate
├── aks/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── gke/
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

## 2. OKE (Oracle Kubernetes Engine) - Primary

### main.tf

```terraform
terraform {
  required_providers {
    oci = {
      source  = "oracle/oci"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0"
    }
  }
}

provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  user_ocid        = var.user_ocid
  fingerprint      = var.fingerprint
  private_key_path = var.private_key_path
  region           = var.region
}

# OKE Cluster
resource "oci_containerengine_cluster" "todo_cluster" {
  compartment_id     = var.compartment_ocid
  kubernetes_version = "v1.28.2"
  name               = "todo-oke-cluster"
  vcn_id             = oci_core_vcn.todo_vcn.id

  options {
    service_lb_subnet_ids = [
      oci_core_subnet.todo_lb_subnet.id
    ]
  }
}

# Node Pool (Always-Free Tier)
resource "oci_containerengine_node_pool" "todo_node_pool" {
  cluster_id         = oci_containerengine_cluster.todo_cluster.id
  compartment_id     = var.compartment_ocid
  kubernetes_version = "v1.28.2"
  name               = "todo-node-pool"

  node_config_details {
    size = 2  # Always-free: 2 nodes

    placement_configs {
      availability_domain = data.oci_identity_availability_domains.ads.availability_domains[0].name
      subnet_id           = oci_core_subnet.todo_node_subnet.id
    }

    node_pool_pod_network_options_details {
      cni_type = "OCI_VCN_IP_NATIVE"
    }
  }

  node_shape_config {
    memory_in_gbs = 12  # Always-free: 12GB per node
    ocpus         = 2   # Always-free: 2 OCPUs per node
  }

  node_source_details {
    image_id    = data.oci_core_images.node_images.images[0].id
    source_type = "IMAGE"
  }

  node_shape = "VM.Standard.A1.Flex"  # Always-free shape
}

# VCN
resource "oci_core_vcn" "todo_vcn" {
  compartment_id = var.compartment_ocid
  cidr_blocks    = ["10.0.0.0/16"]
  display_name   = "todo-vcn"
  dns_label      = "todovcn"
}

# Subnets
resource "oci_core_subnet" "todo_node_subnet" {
  cidr_block     = "10.0.1.0/24"
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.todo_vcn.id
  display_name   = "todo-node-subnet"
}

resource "oci_core_subnet" "todo_lb_subnet" {
  cidr_block     = "10.0.2.0/24"
  compartment_id = var.compartment_ocid
  vcn_id         = oci_core_vcn.todo_vcn.id
  display_name   = "todo-lb-subnet"
}

# Data Sources
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}

data "oci_core_images" "node_images" {
  compartment_id           = var.compartment_ocid
  operating_system         = "Oracle Linux"
  operating_system_version = "8"
  shape                    = "VM.Standard.A1.Flex"
  sort_by                  = "TIMECREATED"
  sort_order               = "DESC"
}

# Kubernetes Provider
provider "kubernetes" {
  host                   = oci_containerengine_cluster.todo_cluster.endpoints[0].kubernetes_api_endpoint
  cluster_ca_certificate = base64decode(oci_containerengine_cluster.todo_cluster.kubeconfig[0].cluster_ca_certificate)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "oci"
    args = [
      "ce", "cluster", "create-kubeconfig",
      "--cluster-id", oci_containerengine_cluster.todo_cluster.id,
      "--file", "/dev/stdout",
      "--region", var.region,
      "--token-version", "2.0.0"
    ]
  }
}

# Dapr Installation
resource "null_resource" "dapr_init" {
  provisioner "local-exec" {
    command = <<-EOT
      kubectl config use-context ${oci_containerengine_cluster.todo_cluster.name}
      dapr init -k --runtime-version 1.12 --enable-mtls=true
    EOT
  }

  depends_on = [
    oci_containerengine_node_pool.todo_node_pool
  ]
}
```

### variables.tf

```terraform
variable "tenancy_ocid" {
  description = "OCI Tenancy OCID"
  type        = string
}

variable "user_ocid" {
  description = "OCI User OCID"
  type        = string
}

variable "fingerprint" {
  description = "OCI API Key Fingerprint"
  type        = string
}

variable "private_key_path" {
  description = "Path to OCI API Key Private Key"
  type        = string
}

variable "compartment_ocid" {
  description = "OCI Compartment OCID"
  type        = string
}

variable "region" {
  description = "OCI Region"
  type        = string
  default     = "us-ashburn-1"
}
```

### outputs.tf

```terraform
output "cluster_id" {
  description = "OKE Cluster ID"
  value       = oci_containerengine_cluster.todo_cluster.id
}

output "cluster_endpoint" {
  description = "OKE Cluster Endpoint"
  value       = oci_containerengine_cluster.todo_cluster.endpoints[0].kubernetes_api_endpoint
}

output "kubeconfig" {
  description = "Kubeconfig for OKE cluster"
  value       = oci_containerengine_cluster.todo_cluster.kubeconfig[0].content
  sensitive   = true
}
```

## 3. AKS (Azure Kubernetes Service) - Secondary

### main.tf

```terraform
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "todo_rg" {
  name     = "todo-resource-group"
  location = var.location
}

# AKS Cluster
resource "azurerm_kubernetes_cluster" "todo_cluster" {
  name                = "todo-aks-cluster"
  location            = azurerm_resource_group.todo_rg.location
  resource_group_name = azurerm_resource_group.todo_rg.name
  dns_prefix          = "todoaks"
  kubernetes_version  = "1.28"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_B2s"  # 2 vCPUs, 4GB RAM
  }

  identity {
    type = "SystemAssigned"
  }
}

# Kubernetes Provider
provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.todo_cluster.kube_config[0].host
  client_certificate     = base64decode(azurerm_kubernetes_cluster.todo_cluster.kube_config[0].client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.todo_cluster.kube_config[0].client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.todo_cluster.kube_config[0].cluster_ca_certificate)
}

# Dapr Installation
resource "null_resource" "dapr_init" {
  provisioner "local-exec" {
    command = <<-EOT
      az aks get-credentials --resource-group ${azurerm_resource_group.todo_rg.name} --name ${azurerm_kubernetes_cluster.todo_cluster.name}
      dapr init -k --runtime-version 1.12 --enable-mtls=true
    EOT
  }
}
```

## 4. GKE (Google Kubernetes Engine) - Secondary

### main.tf

```terraform
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# GKE Cluster
resource "google_container_cluster" "todo_cluster" {
  name     = "todo-gke-cluster"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  network    = google_compute_network.todo_vpc.name
  subnetwork = google_compute_subnetwork.todo_subnet.name
}

# Node Pool
resource "google_container_node_pool" "todo_node_pool" {
  name       = "todo-node-pool"
  location   = var.region
  cluster    = google_container_cluster.todo_cluster.name
  node_count = 2

  node_config {
    machine_type = "e2-medium"  # 2 vCPUs, 4GB RAM
    disk_size_gb = 20
  }
}

# VPC Network
resource "google_compute_network" "todo_vpc" {
  name = "todo-vpc"
}

resource "google_compute_subnetwork" "todo_subnet" {
  name          = "todo-subnet"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.todo_vpc.id
}

# Kubernetes Provider
data "google_client_config" "default" {}

data "google_container_cluster" "todo_cluster" {
  name     = google_container_cluster.todo_cluster.name
  location = var.region
}

provider "kubernetes" {
  host                   = "https://${data.google_container_cluster.todo_cluster.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(data.google_container_cluster.todo_cluster.master_auth[0].cluster_ca_certificate)
}

# Dapr Installation
resource "null_resource" "dapr_init" {
  provisioner "local-exec" {
    command = <<-EOT
      gcloud container clusters get-credentials ${google_container_cluster.todo_cluster.name} --region ${var.region}
      dapr init -k --runtime-version 1.12 --enable-mtls=true
    EOT
  }
}
```

## 5. Multi-Cloud Pattern

### Shared Variables

```terraform
# variables.tf (shared)
variable "cluster_name" {
  description = "Kubernetes cluster name"
  type        = string
  default     = "todo-cluster"
}

variable "node_count" {
  description = "Number of nodes"
  type        = number
  default     = 2
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}
```

## 6. Terraform Commands

### Initialize

```bash
cd terraform/oke
terraform init
```

### Plan

```bash
terraform plan -var-file="terraform.tfvars"
```

### Apply

```bash
terraform apply -var-file="terraform.tfvars"
```

### Destroy

```bash
terraform destroy -var-file="terraform.tfvars"
```

## 7. State Management

### Remote State (Optional)

```terraform
terraform {
  backend "s3" {
    bucket = "todo-terraform-state"
    key    = "oke/terraform.tfstate"
    region = "us-east-1"
  }
}
```

### Local State (Default)

```bash
# State file: terraform.tfstate
# Backup before changes
cp terraform.tfstate terraform.tfstate.backup
```

## Best Practices

### 1. Use Variables for Configuration

```terraform
variable "node_count" {
  type    = number
  default = 2
}
```

### 2. Output Important Values

```terraform
output "cluster_endpoint" {
  value = oci_containerengine_cluster.todo_cluster.endpoints[0].kubernetes_api_endpoint
}
```

### 3. Use Data Sources

```terraform
data "oci_identity_availability_domains" "ads" {
  compartment_id = var.tenancy_ocid
}
```

### 4. Dapr Installation After Cluster

```terraform
resource "null_resource" "dapr_init" {
  depends_on = [oci_containerengine_node_pool.todo_node_pool]
  # ...
}
```

## References

- [Terraform Documentation](https://developer.hashicorp.com/terraform)
- [OCI Provider](https://registry.terraform.io/providers/oracle/oci/latest/docs)
- [Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Google Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

