# 🏗️ Skill: Terraform Infrastructure as Code

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-terraform` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `terraform`, `iac`, `infrastructure-as-code`, `hcl`, `provisioning` |
| **Referencia** | [Terraform Docs](https://www.terraform.io/docs) |

## 🔑 Keywords para Invocación

- `terraform`
- `iac`
- `infrastructure-as-code`
- `hcl`
- `provisioning`
- `@skill:terraform`

### Ejemplos de Prompts

```
Configura infraestructura con Terraform para backend Flutter
```

```
Crea módulos de Terraform para Kubernetes y RDS
```

```
@skill:terraform - Provision infrastructure para app monorepo
```

## 📖 Descripción

Terraform permite definir y provision infraestructura cloud de manera declarativa usando HCL. Este skill cubre la creación de módulos reutilizables para backends de Flutter: Kubernetes clusters, databases, storage, networking y más.

### ✅ Cuándo Usar Este Skill

- Infraestructura multi-cloud
- Versionado de infraestructura
- Reutilización con módulos
- State management centralizado
- Infraestructura reproducible
- Disaster recovery

### ❌ Cuándo NO Usar Este Skill

- Infraestructura muy simple
- Preferencia por UI/CLI manual
- Ya usas otra herramienta IaC (Pulumi, CDK)

## 🏗️ Estructura del Proyecto

```
infrastructure/
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   ├── outputs.tf
│   │   │   └── terraform.tfvars
│   │   ├── staging/
│   │   └── production/
│   │
│   ├── modules/
│   │   ├── kubernetes/
│   │   │   ├── main.tf
│   │   │   ├── variables.tf
│   │   │   └── outputs.tf
│   │   ├── database/
│   │   │   ├── postgres/
│   │   │   └── redis/
│   │   ├── storage/
│   │   ├── networking/
│   │   └── monitoring/
│   │
│   ├── backend.tf
│   └── versions.tf
│
└── scripts/
    ├── init.sh
    └── deploy.sh
```

## 💻 Implementación

### 1. Backend Configuration (S3 + DynamoDB)

```hcl
# infrastructure/terraform/backend.tf
terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket         = "myapp-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"

    # Workspace support
    workspace_key_prefix = "env"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }
  }
}
```

### 2. Módulo: Kubernetes Cluster (EKS)

```hcl
# infrastructure/terraform/modules/kubernetes/main.tf
resource "aws_eks_cluster" "main" {
  name     = var.cluster_name
  role_arn = aws_iam_role.cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = var.enable_public_access
    public_access_cidrs     = var.public_access_cidrs

    security_group_ids = [aws_security_group.cluster.id]
  }

  enabled_cluster_log_types = [
    "api",
    "audit",
    "authenticator",
    "controllerManager",
    "scheduler"
  ]

  encryption_config {
    provider {
      key_arn = aws_kms_key.eks.arn
    }
    resources = ["secrets"]
  }

  tags = merge(
    var.tags,
    {
      Name        = var.cluster_name
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  )

  depends_on = [
    aws_iam_role_policy_attachment.cluster_AmazonEKSClusterPolicy,
    aws_iam_role_policy_attachment.cluster_AmazonEKSVPCResourceController,
  ]
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.cluster_name}-node-group"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = var.private_subnet_ids

  scaling_config {
    desired_size = var.desired_nodes
    max_size     = var.max_nodes
    min_size     = var.min_nodes
  }

  update_config {
    max_unavailable = 1
  }

  instance_types = var.instance_types
  capacity_type  = var.capacity_type  # ON_DEMAND or SPOT

  disk_size = var.disk_size

  labels = {
    Environment = var.environment
    NodeGroup   = "main"
  }

  tags = var.tags

  depends_on = [
    aws_iam_role_policy_attachment.node_AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.node_AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.node_AmazonEC2ContainerRegistryReadOnly,
  ]
}

# infrastructure/terraform/modules/kubernetes/variables.tf
variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for the EKS cluster"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for node groups"
  type        = list(string)
}

variable "desired_nodes" {
  description = "Desired number of nodes"
  type        = number
  default     = 3
}

variable "min_nodes" {
  description = "Minimum number of nodes"
  type        = number
  default     = 2
}

variable "max_nodes" {
  description = "Maximum number of nodes"
  type        = number
  default     = 10
}

variable "instance_types" {
  description = "List of instance types"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "capacity_type" {
  description = "Capacity type (ON_DEMAND or SPOT)"
  type        = string
  default     = "ON_DEMAND"
}

variable "disk_size" {
  description = "Disk size in GB"
  type        = number
  default     = 50
}

variable "enable_public_access" {
  description = "Enable public access to API server"
  type        = bool
  default     = false
}

variable "public_access_cidrs" {
  description = "List of CIDR blocks for public access"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

# infrastructure/terraform/modules/kubernetes/outputs.tf
output "cluster_id" {
  description = "EKS cluster ID"
  value       = aws_eks_cluster.main.id
}

output "cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = aws_eks_cluster.main.endpoint
}

output "cluster_security_group_id" {
  description = "Security group ID attached to the EKS cluster"
  value       = aws_security_group.cluster.id
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data"
  value       = aws_eks_cluster.main.certificate_authority[0].data
  sensitive   = true
}

output "node_group_id" {
  description = "EKS node group ID"
  value       = aws_eks_node_group.main.id
}
```

### 3. Módulo: Database (RDS PostgreSQL)

```hcl
# infrastructure/terraform/modules/database/postgres/main.tf
resource "aws_db_subnet_group" "main" {
  name       = "${var.identifier}-subnet-group"
  subnet_ids = var.subnet_ids

  tags = merge(
    var.tags,
    {
      Name = "${var.identifier}-subnet-group"
    }
  )
}

resource "aws_db_parameter_group" "main" {
  name   = "${var.identifier}-pg"
  family = "postgres${var.engine_version}"

  parameter {
    name  = "log_connections"
    value = "1"
  }

  parameter {
    name  = "log_disconnections"
    value = "1"
  }

  parameter {
    name  = "log_statement"
    value = "all"
  }

  tags = var.tags
}

resource "aws_db_instance" "main" {
  identifier     = var.identifier
  engine         = "postgres"
  engine_version = var.engine_version
  instance_class = var.instance_class

  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true
  kms_key_id            = aws_kms_key.rds.arn

  db_name  = var.database_name
  username = var.master_username
  password = var.master_password  # Use AWS Secrets Manager in production
  port     = 5432

  multi_az               = var.multi_az
  db_subnet_group_name   = aws_db_subnet_group.main.name
  parameter_group_name   = aws_db_parameter_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = var.backup_retention_period
  backup_window           = var.backup_window
  maintenance_window      = var.maintenance_window

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  deletion_protection = var.deletion_protection
  skip_final_snapshot = var.skip_final_snapshot
  final_snapshot_identifier = var.skip_final_snapshot ? null : "${var.identifier}-final-snapshot-${formatdate("YYYYMMDDhhmmss", timestamp())}"

  performance_insights_enabled    = true
  performance_insights_kms_key_id = aws_kms_key.rds.arn

  tags = merge(
    var.tags,
    {
      Name        = var.identifier
      Environment = var.environment
    }
  )
}

# infrastructure/terraform/modules/database/postgres/variables.tf
variable "identifier" {
  description = "Database identifier"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "engine_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "15.4"
}

variable "instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

variable "max_allocated_storage" {
  description = "Maximum allocated storage for autoscaling"
  type        = number
  default     = 100
}

variable "database_name" {
  description = "Name of the database"
  type        = string
}

variable "master_username" {
  description = "Master username"
  type        = string
  default     = "postgres"
}

variable "master_password" {
  description = "Master password"
  type        = string
  sensitive   = true
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
}

variable "multi_az" {
  description = "Enable multi-AZ deployment"
  type        = bool
  default     = true
}

variable "backup_retention_period" {
  description = "Backup retention period in days"
  type        = number
  default     = 7
}

variable "backup_window" {
  description = "Backup window"
  type        = string
  default     = "03:00-04:00"
}

variable "maintenance_window" {
  description = "Maintenance window"
  type        = string
  default     = "sun:04:00-sun:05:00"
}

variable "deletion_protection" {
  description = "Enable deletion protection"
  type        = bool
  default     = true
}

variable "skip_final_snapshot" {
  description = "Skip final snapshot on deletion"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Tags to apply"
  type        = map(string)
  default     = {}
}
```

### 4. Environment Configuration (Production)

```hcl
# infrastructure/terraform/environments/production/main.tf
terraform {
  backend "s3" {
    bucket = "myapp-terraform-state"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "MyApp"
      Environment = "production"
      ManagedBy   = "Terraform"
    }
  }
}

module "vpc" {
  source = "../../modules/networking/vpc"

  name               = "myapp-prod-vpc"
  cidr               = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  database_subnets = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = false
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = local.common_tags
}

module "eks" {
  source = "../../modules/kubernetes"

  cluster_name       = "myapp-prod"
  kubernetes_version = "1.28"
  environment        = "production"

  subnet_ids         = module.vpc.public_subnet_ids
  private_subnet_ids = module.vpc.private_subnet_ids

  desired_nodes  = 5
  min_nodes      = 3
  max_nodes      = 20
  instance_types = ["t3.large", "t3.xlarge"]
  capacity_type  = "ON_DEMAND"

  enable_public_access = false

  tags = local.common_tags
}

module "database" {
  source = "../../modules/database/postgres"

  identifier     = "myapp-prod-db"
  environment    = "production"
  engine_version = "15.4"
  instance_class = "db.r6g.large"

  allocated_storage     = 100
  max_allocated_storage = 1000

  database_name   = "myapp_prod"
  master_username = "admin"
  master_password = data.aws_secretsmanager_secret_version.db_password.secret_string

  subnet_ids              = module.vpc.database_subnet_ids
  multi_az                = true
  backup_retention_period = 30
  deletion_protection     = true
  skip_final_snapshot     = false

  tags = local.common_tags
}

module "redis" {
  source = "../../modules/database/redis"

  cluster_id       = "myapp-prod-redis"
  environment      = "production"
  engine_version   = "7.0"
  node_type        = "cache.r6g.large"
  num_cache_nodes  = 3

  subnet_ids = module.vpc.private_subnet_ids

  tags = local.common_tags
}

module "s3_storage" {
  source = "../../modules/storage/s3"

  bucket_name = "myapp-prod-storage"
  environment = "production"

  enable_versioning = true
  enable_encryption = true

  lifecycle_rules = [
    {
      id      = "archive-old-objects"
      enabled = true

      transition = {
        days          = 90
        storage_class = "GLACIER"
      }
    }
  ]

  tags = local.common_tags
}

# infrastructure/terraform/environments/production/variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

# infrastructure/terraform/environments/production/outputs.tf
output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint"
  value       = module.eks.cluster_endpoint
  sensitive   = true
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = module.database.endpoint
  sensitive   = true
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = module.redis.endpoint
  sensitive   = true
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = module.s3_storage.bucket_name
}

# infrastructure/terraform/environments/production/locals.tf
locals {
  common_tags = {
    Project     = "MyApp"
    Environment = "production"
    ManagedBy   = "Terraform"
    Team        = "Platform"
  }
}
```

### 5. Terraform Workspace Management

```bash
# infrastructure/scripts/init.sh
#!/bin/bash

set -e

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
  echo "Usage: $0 <environment>"
  echo "Example: $0 production"
  exit 1
fi

cd "environments/$ENVIRONMENT"

echo "Initializing Terraform for $ENVIRONMENT..."
terraform init

echo "Creating/selecting workspace..."
terraform workspace select "$ENVIRONMENT" || terraform workspace new "$ENVIRONMENT"

echo "Validating configuration..."
terraform validate

echo "Planning infrastructure..."
terraform plan -out=tfplan
```

```bash
# infrastructure/scripts/deploy.sh
#!/bin/bash

set -e

ENVIRONMENT=$1
AUTO_APPROVE=${2:-false}

if [ -z "$ENVIRONMENT" ]; then
  echo "Usage: $0 <environment> [auto-approve]"
  echo "Example: $0 production true"
  exit 1
fi

cd "environments/$ENVIRONMENT"

terraform workspace select "$ENVIRONMENT"

if [ "$AUTO_APPROVE" == "true" ]; then
  terraform apply -auto-approve tfplan
else
  terraform apply tfplan
fi

echo "Deployment completed successfully!"
```

## 🎯 Mejores Prácticas

### 1. State Management

```hcl
# Usar S3 backend con encryption y locking
terraform {
  backend "s3" {
    bucket         = "terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
```

### 2. Secrets Management

```hcl
# Usar AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/password"
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

### 3. Resource Naming

```hcl
# Convención: {project}-{environment}-{resource}
resource "aws_eks_cluster" "main" {
  name = "${var.project}-${var.environment}-cluster"
}
```

### 4. Tagging Strategy

```hcl
locals {
  common_tags = {
    Project     = var.project
    Environment = var.environment
    ManagedBy   = "Terraform"
    CostCenter  = var.cost_center
  }
}

resource "aws_instance" "example" {
  tags = merge(local.common_tags, var.additional_tags)
}
```

### 5. Module Versioning

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"  # Pin version
}
```

## 🚀 Comandos Útiles

```bash
# Inicializar Terraform
terraform init

# Validar configuración
terraform validate

# Formatear código
terraform fmt -recursive

# Plan de cambios
terraform plan -out=tfplan

# Aplicar cambios
terraform apply tfplan

# Destroy infrastructure
terraform destroy

# List workspaces
terraform workspace list

# Select workspace
terraform workspace select production

# Show state
terraform show

# Import existing resource
terraform import aws_instance.example i-1234567890

# Taint resource (force recreation)
terraform taint aws_instance.example

# Output values
terraform output

# Graph visualization
terraform graph | dot -Tpng > graph.png
```

## 📚 Recursos Adicionales

- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

## 🔗 Skills Relacionados

- [GitHub Actions](../github-actions/SKILL.md) - CI/CD automation
- [ArgoCD](../argocd/SKILL.md) - GitOps deployment
- [AWS](../aws/SKILL.md) - AWS services
- [Kubernetes](../kubernetes/SKILL.md) - Container orchestration

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
