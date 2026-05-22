---
name: infrastructure
description: Infrastructure as Code (IaC) practices for provisioning and managing cloud resources. Use when provisioning cloud resources, managing infrastructure changes, setting up environments, disaster recovery planning, or infrastructure audits.
---

# Infrastructure as Code

## Core Principle

**Infrastructure is code. Version it, test it, review it, automate it.**

Infrastructure should be defined declaratively, stored in version control, reviewed like code, and deployed automatically. Manual infrastructure changes lead to drift, inconsistency, and production issues. Treat your infrastructure with the same rigor as application code.

---

## When to Use

Use this skill when:
- Provisioning new cloud resources (compute, storage, networking)
- Managing infrastructure changes across environments
- Setting up new environments (dev, staging, production)
- Implementing disaster recovery and business continuity
- Conducting infrastructure audits and cost optimization
- Migrating infrastructure between cloud providers
- Establishing infrastructure standards and patterns
- Scaling infrastructure to meet demand
- Implementing security and compliance requirements

---

## Infrastructure as Code Tools

### Terraform (Multi-Cloud)

**Best for:** Multi-cloud deployments, complex infrastructure, mature ecosystems

```hcl
# Example: Terraform AWS EC2 instance
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name        = "web-server"
    Environment = "production"
    ManagedBy   = "terraform"
  }

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y httpd
              systemctl start httpd
              systemctl enable httpd
              EOF
}

resource "aws_security_group" "web_sg" {
  name        = "web-security-group"
  description = "Allow HTTP and HTTPS traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

**Key Features:**
- Declarative configuration language (HCL)
- Multi-cloud support (AWS, Azure, GCP, 1000+ providers)
- State management (tracks actual vs desired state)
- Plan preview before applying changes
- Module system for reusability
- Large community and ecosystem

---

### Pulumi (Code-First IaC)

**Best for:** Teams preferring general-purpose languages, complex logic, existing code reuse

```typescript
// Example: Pulumi AWS S3 bucket with TypeScript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

// Create an S3 bucket with versioning and encryption
const bucket = new aws.s3.Bucket("my-bucket", {
    versioning: {
        enabled: true,
    },
    serverSideEncryptionConfiguration: {
        rule: {
            applyServerSideEncryptionByDefault: {
                sseAlgorithm: "AES256",
            },
        },
    },
    tags: {
        Environment: "production",
        ManagedBy: "pulumi",
    },
});

// Create a bucket policy
const bucketPolicy = new aws.s3.BucketPolicy("my-bucket-policy", {
    bucket: bucket.id,
    policy: bucket.arn.apply(arn => JSON.stringify({
        Version: "2012-10-17",
        Statement: [{
            Effect: "Allow",
            Principal: "*",
            Action: "s3:GetObject",
            Resource: `${arn}/*`,
            Condition: {
                IpAddress: {
                    "aws:SourceIp": ["203.0.113.0/24"]
                }
            }
        }],
    })),
});

// Export the bucket name
export const bucketName = bucket.id;
export const bucketArn = bucket.arn;
```

**Key Features:**
- Use familiar programming languages (TypeScript, Python, Go, C#)
- Full programming language features (loops, conditionals, functions)
- Strong typing and IDE support
- Component-based architecture
- Automatic state management
- Built-in secrets management

---

### AWS CloudFormation

**Best for:** AWS-only infrastructure, AWS-native tooling

```yaml
# Example: CloudFormation VPC with subnets
AWSTemplateFormatVersion: '2010-09-09'
Description: 'VPC with public and private subnets'

Parameters:
  EnvironmentName:
    Type: String
    Default: production
    Description: Environment name prefix

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${EnvironmentName}-vpc'

  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: 10.0.1.0/24
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${EnvironmentName}-public-subnet-1'

  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: 10.0.11.0/24
      Tags:
        - Key: Name
          Value: !Sub '${EnvironmentName}-private-subnet-1'

  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub '${EnvironmentName}-igw'

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub '${EnvironmentName}-VPC-ID'
```

---

### Azure Resource Manager (ARM) / Bicep

**Best for:** Azure-only infrastructure, Azure-native tooling

```bicep
// Example: Bicep - Azure App Service with SQL Database
param location string = resourceGroup().location
param appName string = 'myapp-${uniqueString(resourceGroup().id)}'

resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: '${appName}-plan'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
    capacity: 1
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2021-02-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|18-lts'
      appSettings: [
        {
          name: 'WEBSITE_NODE_DEFAULT_VERSION'
          value: '18-lts'
        }
      ]
    }
  }
}

resource sqlServer 'Microsoft.Sql/servers@2021-11-01' = {
  name: '${appName}-sql'
  location: location
  properties: {
    administratorLogin: 'sqladmin'
    administratorLoginPassword: 'P@ssw0rd123!'  // Use Key Vault in production!
  }
}

resource sqlDatabase 'Microsoft.Sql/servers/databases@2021-11-01' = {
  parent: sqlServer
  name: 'appdb'
  location: location
  sku: {
    name: 'Basic'
    tier: 'Basic'
  }
}

output webAppUrl string = webApp.properties.defaultHostName
output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName
```

---

### Google Cloud Deployment Manager

**Best for:** GCP-only infrastructure

```yaml
# Example: GCP Deployment Manager - Compute Instance
resources:
- name: web-server
  type: compute.v1.instance
  properties:
    zone: us-central1-a
    machineType: zones/us-central1-a/machineTypes/n1-standard-1
    disks:
    - deviceName: boot
      type: PERSISTENT
      boot: true
      autoDelete: true
      initializeParams:
        sourceImage: projects/debian-cloud/global/images/family/debian-11
    networkInterfaces:
    - network: global/networks/default
      accessConfigs:
      - name: External NAT
        type: ONE_TO_ONE_NAT
    metadata:
      items:
      - key: startup-script
        value: |
          #!/bin/bash
          apt-get update
          apt-get install -y nginx
          systemctl start nginx
          systemctl enable nginx
    tags:
      items:
      - http-server
      - https-server
```

---

## IaC Best Practices

### 1. Version Control Everything

**All infrastructure code must be in version control.**

```bash
# Standard IaC repository structure
infrastructure/
├── README.md
├── .gitignore           # Ignore: .terraform/, *.tfstate, secrets
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── production/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
└── modules/
    ├── networking/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── compute/
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── database/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

**What to ignore:**
```gitignore
# Terraform
.terraform/
*.tfstate
*.tfstate.backup
*.tfvars  # If contains secrets

# Pulumi
.pulumi/
Pulumi.*.yaml  # If contains secrets

# Secrets
*.pem
*.key
secrets.yaml
credentials.json
```

---

### 2. Modular Infrastructure

**Create reusable modules for common patterns.**

```hcl
# modules/web-app/main.tf
variable "app_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "instance_count" {
  type    = number
  default = 2
}

resource "aws_launch_template" "app" {
  name_prefix   = "${var.app_name}-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  vpc_security_group_ids = [aws_security_group.app.id]

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name        = var.app_name
      Environment = var.environment
    }
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "${var.app_name}-asg"
  vpc_zone_identifier = var.subnet_ids
  min_size            = var.instance_count
  max_size            = var.instance_count * 2
  desired_capacity    = var.instance_count

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  target_group_arns = [aws_lb_target_group.app.arn]
}

# Usage in production environment
module "web_app" {
  source = "../../modules/web-app"

  app_name       = "myapp"
  environment    = "production"
  instance_count = 4
  subnet_ids     = module.networking.private_subnet_ids
}
```

---

### 3. Environment Separation

**Separate environments to prevent accidents.**

```
Strategy 1: Separate directories (Terraform)
environments/
├── dev/
│   └── main.tf       # Points to dev AWS account
├── staging/
│   └── main.tf       # Points to staging AWS account
└── production/
    └── main.tf       # Points to prod AWS account (requires approval)

Strategy 2: Separate projects (Pulumi)
pulumi/
├── dev/              # Pulumi stack: dev
├── staging/          # Pulumi stack: staging
└── production/       # Pulumi stack: production

Strategy 3: Workspaces (Terraform)
terraform workspace list
  default
  dev
  staging
* production
```

**Environment-specific configuration:**
```hcl
# variables.tf
variable "environment_config" {
  type = map(object({
    instance_type = string
    instance_count = number
    db_instance_class = string
  }))
  default = {
    dev = {
      instance_type     = "t3.micro"
      instance_count    = 1
      db_instance_class = "db.t3.micro"
    }
    staging = {
      instance_type     = "t3.small"
      instance_count    = 2
      db_instance_class = "db.t3.small"
    }
    production = {
      instance_type     = "t3.medium"
      instance_count    = 4
      db_instance_class = "db.r5.large"
    }
  }
}

locals {
  config = var.environment_config[var.environment]
}

resource "aws_instance" "app" {
  instance_type = local.config.instance_type
  count         = local.config.instance_count
  # ...
}
```

---

### 4. State Management

**Terraform state must be stored remotely and locked.**

```hcl
# backend.tf - S3 backend with DynamoDB locking
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "production/myapp/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

**Creating the S3 backend resources:**
```hcl
# bootstrap/main.tf - Run this once to create backend
resource "aws_s3_bucket" "terraform_state" {
  bucket = "mycompany-terraform-state"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

**Pulumi state:**
```bash
# Pulumi automatically manages state in Pulumi Cloud
# Or configure self-hosted backend:
pulumi login s3://my-pulumi-state-bucket
```

---

### 5. Plan Before Apply

**Always preview changes before applying.**

```bash
# Terraform workflow
terraform init          # Initialize providers and modules
terraform validate      # Validate configuration syntax
terraform fmt           # Format code consistently
terraform plan          # Preview changes
terraform plan -out=plan.tfplan  # Save plan
terraform apply plan.tfplan      # Apply saved plan

# Never run: terraform apply -auto-approve (in production)
```

```bash
# Pulumi workflow
pulumi preview          # Preview changes
pulumi up               # Apply changes (with confirmation)
pulumi up --yes         # Auto-approve (CI/CD only)
```

---

### 6. Code Review for Infrastructure

**Review infrastructure changes like application code.**

```yaml
# .github/workflows/terraform-pr.yml
name: Terraform PR Check

on:
  pull_request:
    paths:
      - 'infrastructure/**'

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure/production

      - name: Terraform Format Check
        run: terraform fmt -check
        working-directory: infrastructure/production

      - name: Terraform Validate
        run: terraform validate
        working-directory: infrastructure/production

      - name: Terraform Plan
        run: terraform plan -no-color
        working-directory: infrastructure/production
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Comment PR with Plan
        uses: actions/github-script@v6
        with:
          script: |
            const output = `#### Terraform Plan
            \`\`\`
            ${{ steps.plan.outputs.stdout }}
            \`\`\`
            `;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });
```

---

## Infrastructure Patterns

### Multi-Tier Web Application

**Classic 3-tier architecture: Web → Application → Database**

```hcl
# Example: AWS 3-tier architecture with Terraform
module "networking" {
  source = "./modules/networking"

  vpc_cidr = "10.0.0.0/16"
  availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]

  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnet_cidrs = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
  db_subnet_cidrs      = ["10.0.21.0/24", "10.0.22.0/24", "10.0.23.0/24"]
}

# Web tier - ALB in public subnets
module "web_tier" {
  source = "./modules/alb"

  name            = "web-alb"
  vpc_id          = module.networking.vpc_id
  subnet_ids      = module.networking.public_subnet_ids
  security_groups = [module.networking.web_sg_id]

  certificate_arn = aws_acm_certificate.app.arn
}

# Application tier - EC2 instances in private subnets
module "app_tier" {
  source = "./modules/ec2-asg"

  name               = "app-servers"
  vpc_id             = module.networking.vpc_id
  subnet_ids         = module.networking.private_subnet_ids
  security_groups    = [module.networking.app_sg_id]
  target_group_arns  = [module.web_tier.target_group_arn]

  min_size     = 2
  max_size     = 10
  desired_size = 4

  instance_type = "t3.medium"
}

# Database tier - RDS in database subnets
module "db_tier" {
  source = "./modules/rds"

  identifier          = "app-db"
  engine              = "postgres"
  engine_version      = "15.4"
  instance_class      = "db.r5.large"
  allocated_storage   = 100

  db_name  = "appdb"
  username = "dbadmin"
  password = data.aws_secretsmanager_secret_version.db_password.secret_string

  vpc_id                 = module.networking.vpc_id
  subnet_ids             = module.networking.db_subnet_ids
  vpc_security_group_ids = [module.networking.db_sg_id]

  backup_retention_period = 7
  multi_az                = true
  storage_encrypted       = true
}
```

---

### Kubernetes Cluster Infrastructure

**EKS cluster with managed node groups:**

```hcl
# modules/eks/main.tf
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.28"

  vpc_id     = var.vpc_id
  subnet_ids = var.subnet_ids

  # Cluster access
  cluster_endpoint_public_access = true
  cluster_endpoint_private_access = true

  # Managed node groups
  eks_managed_node_groups = {
    general = {
      desired_size = 3
      min_size     = 2
      max_size     = 10

      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"

      labels = {
        role = "general"
      }

      tags = {
        NodeGroup = "general"
      }
    }

    compute = {
      desired_size = 2
      min_size     = 1
      max_size     = 5

      instance_types = ["c5.xlarge"]
      capacity_type  = "SPOT"

      labels = {
        role = "compute"
      }

      taints = [{
        key    = "workload"
        value  = "compute"
        effect = "NO_SCHEDULE"
      }]
    }
  }

  # Cluster addons
  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
  }
}
```

---

### Serverless Infrastructure

**AWS Lambda with API Gateway and DynamoDB:**

```typescript
// Pulumi - TypeScript serverless stack
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

// DynamoDB table
const table = new aws.dynamodb.Table("app-table", {
    attributes: [
        { name: "id", type: "S" },
    ],
    hashKey: "id",
    billingMode: "PAY_PER_REQUEST",
});

// Lambda function
const lambda = new aws.lambda.Function("api-handler", {
    runtime: aws.lambda.Runtime.NodeJS18dX,
    handler: "index.handler",
    role: lambdaRole.arn,
    code: new pulumi.asset.AssetArchive({
        ".": new pulumi.asset.FileArchive("./lambda"),
    }),
    environment: {
        variables: {
            TABLE_NAME: table.name,
        },
    },
});

// API Gateway
const api = new awsx.apigateway.API("api", {
    routes: [
        {
            path: "/items",
            method: "GET",
            eventHandler: lambda,
        },
        {
            path: "/items",
            method: "POST",
            eventHandler: lambda,
        },
        {
            path: "/items/{id}",
            method: "GET",
            eventHandler: lambda,
        },
    ],
});

// IAM role for Lambda
const lambdaRole = new aws.iam.Role("lambda-role", {
    assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({
        Service: "lambda.amazonaws.com",
    }),
});

// Attach policies
new aws.iam.RolePolicyAttachment("lambda-basic-execution", {
    role: lambdaRole,
    policyArn: aws.iam.ManagedPolicy.AWSLambdaBasicExecutionRole,
});

new aws.iam.RolePolicy("lambda-dynamodb-policy", {
    role: lambdaRole,
    policy: pulumi.all([table.arn]).apply(([tableArn]) => JSON.stringify({
        Version: "2012-10-17",
        Statement: [{
            Effect: "Allow",
            Action: [
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Query",
                "dynamodb:Scan",
            ],
            Resource: tableArn,
        }],
    })),
});

export const apiUrl = api.url;
export const tableName = table.name;
```

---

## Security Best Practices

### 1. Secrets Management

**Never hardcode secrets in IaC.**

❌ **Bad:**
```hcl
resource "aws_db_instance" "db" {
  username = "admin"
  password = "SuperSecret123!"  # NEVER DO THIS
}
```

✅ **Good: Use secrets manager**
```hcl
# Store secret in AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "production/db/password"
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.db_password  # Passed via environment variable
}

# Reference secret in RDS
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
}

resource "aws_db_instance" "db" {
  username = "admin"
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

**Pulumi with encrypted secrets:**
```bash
# Pulumi encrypts secrets automatically
pulumi config set --secret dbPassword "SuperSecret123!"
```

```typescript
// Access in code
const config = new pulumi.Config();
const dbPassword = config.requireSecret("dbPassword");
```

---

### 2. Least Privilege IAM Policies

**Grant minimum required permissions.**

```hcl
# Good: Specific permissions for specific resources
resource "aws_iam_role_policy" "lambda_policy" {
  name = "lambda-specific-access"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query"
        ]
        Resource = aws_dynamodb_table.users.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.uploads.arn}/*"
      }
    ]
  })
}

# Bad: Overly permissive
# policy = "arn:aws:iam::aws:policy/AdministratorAccess"  # NEVER
```

---

### 3. Network Security

**Implement defense in depth.**

```hcl
# Security groups with minimal access
resource "aws_security_group" "app_sg" {
  name        = "app-servers"
  description = "Security group for application servers"
  vpc_id      = aws_vpc.main.id

  # Only allow traffic from ALB
  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  # Allow outbound traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db_sg" {
  name        = "database"
  description = "Security group for database"
  vpc_id      = aws_vpc.main.id

  # Only allow traffic from app servers
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app_sg.id]
  }

  # No outbound internet access needed for DB
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = []
  }
}
```

---

### 4. Encryption at Rest and in Transit

```hcl
# S3 bucket with encryption
resource "aws_s3_bucket" "data" {
  bucket = "app-data-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.id
    }
  }
}

# RDS with encryption
resource "aws_db_instance" "db" {
  storage_encrypted = true
  kms_key_id        = aws_kms_key.rds.arn
  # ...
}

# EBS volumes encrypted by default
resource "aws_ebs_encryption_by_default" "enabled" {
  enabled = true
}
```

---

## Cost Management

### 1. Resource Tagging

**Tag all resources for cost allocation.**

```hcl
# Standard tags for all resources
locals {
  common_tags = {
    Environment = var.environment
    Project     = "myapp"
    ManagedBy   = "terraform"
    CostCenter  = "engineering"
    Owner       = "devops-team"
  }
}

resource "aws_instance" "app" {
  instance_type = "t3.medium"
  ami           = data.aws_ami.amazon_linux.id

  tags = merge(
    local.common_tags,
    {
      Name = "app-server-${count.index + 1}"
      Role = "application"
    }
  )
}
```

---

### 2. Right-Sizing Resources

**Use appropriate instance sizes.**

```hcl
# Bad: Over-provisioned
resource "aws_instance" "app" {
  instance_type = "m5.4xlarge"  # 16 vCPU, 64 GB RAM
  # App only uses 2 vCPU, 4 GB RAM
}

# Good: Right-sized with auto-scaling
resource "aws_autoscaling_group" "app" {
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  min_size         = 2
  max_size         = 10
  desired_capacity = 4

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }
    target_value = 70.0
  }
}
```

---

### 3. Spot Instances for Non-Critical Workloads

```hcl
resource "aws_launch_template" "batch_processing" {
  instance_type = "c5.xlarge"

  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = "0.10"  # 50-70% cost savings
    }
  }
}
```

---

### 4. Scheduled Scaling

**Scale down during off-hours.**

```hcl
# Scale down non-production at night
resource "aws_autoscaling_schedule" "scale_down" {
  count                  = var.environment != "production" ? 1 : 0
  scheduled_action_name  = "scale-down-night"
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
  recurrence             = "0 22 * * *"  # 10 PM daily
  autoscaling_group_name = aws_autoscaling_group.app.name
}

resource "aws_autoscaling_schedule" "scale_up" {
  count                  = var.environment != "production" ? 1 : 0
  scheduled_action_name  = "scale-up-morning"
  min_size               = 2
  max_size               = 10
  desired_capacity       = 2
  recurrence             = "0 8 * * 1-5"  # 8 AM weekdays
  autoscaling_group_name = aws_autoscaling_group.app.name
}
```

---

## Disaster Recovery

### Backup Strategy

```hcl
# RDS automated backups
resource "aws_db_instance" "db" {
  backup_retention_period = 7
  backup_window           = "03:00-04:00"  # UTC
  maintenance_window      = "sun:04:00-sun:05:00"

  # Enable automated backups to S3
  copy_tags_to_snapshot = true

  # Multi-AZ for HA
  multi_az = true
}

# S3 versioning for data protection
resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id

  versioning_configuration {
    status = "Enabled"
  }
}

# S3 lifecycle policy for old versions
resource "aws_s3_bucket_lifecycle_configuration" "data" {
  bucket = aws_s3_bucket.data.id

  rule {
    id     = "archive-old-versions"
    status = "Enabled"

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class   = "GLACIER"
    }

    noncurrent_version_expiration {
      noncurrent_days = 90
    }
  }
}

# AWS Backup for automated backups
resource "aws_backup_plan" "main" {
  name = "daily-backup-plan"

  rule {
    rule_name         = "daily-backups"
    target_vault_name = aws_backup_vault.main.name
    schedule          = "cron(0 2 * * ? *)"  # 2 AM daily

    lifecycle {
      delete_after = 30
    }
  }
}

resource "aws_backup_selection" "main" {
  plan_id = aws_backup_plan.main.id
  name    = "backup-resources"
  iam_role_arn = aws_iam_role.backup.arn

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "Backup"
    value = "true"
  }
}
```

---

### Multi-Region Deployment

```hcl
# Provider configuration for multi-region
provider "aws" {
  alias  = "primary"
  region = "us-west-2"
}

provider "aws" {
  alias  = "secondary"
  region = "us-east-1"
}

# Primary region resources
module "primary_region" {
  source = "./modules/regional-infrastructure"

  providers = {
    aws = aws.primary
  }

  region      = "us-west-2"
  environment = var.environment
}

# Secondary region resources
module "secondary_region" {
  source = "./modules/regional-infrastructure"

  providers = {
    aws = aws.secondary
  }

  region      = "us-east-1"
  environment = var.environment
}

# Route53 health checks with failover
resource "aws_route53_health_check" "primary" {
  fqdn              = module.primary_region.alb_dns_name
  port              = 443
  type              = "HTTPS"
  resource_path     = "/health"
  failure_threshold = 3
  request_interval  = 30
}

resource "aws_route53_record" "app" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "app.example.com"
  type    = "A"

  set_identifier = "primary"

  failover_routing_policy {
    type = "PRIMARY"
  }

  health_check_id = aws_route53_health_check.primary.id

  alias {
    name                   = module.primary_region.alb_dns_name
    zone_id                = module.primary_region.alb_zone_id
    evaluate_target_health = true
  }
}
```

---

## Infrastructure Testing

### 1. Validation Tests

```bash
# Terraform validation
terraform validate
terraform fmt -check
terraform plan -detailed-exitcode  # Exit code 2 if changes needed
```

---

### 2. Policy as Code (Sentinel/OPA)

```python
# Open Policy Agent (OPA) policy
package terraform.required_tags

required_tags = ["Environment", "Project", "ManagedBy"]

deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_instance"
    tags := resource.change.after.tags

    missing_tags := [tag | tag := required_tags[_]; not tags[tag]]
    count(missing_tags) > 0

    msg := sprintf("Instance %s is missing required tags: %v",
                   [resource.address, missing_tags])
}
```

---

### 3. Integration Tests (Terratest)

```go
// terratest example
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/stretchr/testify/assert"
)

func TestTerraformWebApp(t *testing.T) {
    terraformOptions := &terraform.Options{
        TerraformDir: "../examples/web-app",
        Vars: map[string]interface{}{
            "environment": "test",
        },
    }

    defer terraform.Destroy(t, terraformOptions)
    terraform.InitAndApply(t, terraformOptions)

    // Validate outputs
    albDnsName := terraform.Output(t, terraformOptions, "alb_dns_name")
    assert.NotEmpty(t, albDnsName)

    // Test ALB responds
    url := fmt.Sprintf("http://%s/health", albDnsName)
    http.Get(url)  // Should return 200 OK
}
```

---

## Terraform Workflow

### Daily Workflow

```bash
# 1. Pull latest changes
git pull origin main

# 2. Initialize (if first time or modules changed)
terraform init

# 3. Select workspace (if using workspaces)
terraform workspace select production

# 4. Plan changes
terraform plan -out=tfplan

# 5. Review plan carefully
# Check: What's being created, modified, destroyed?

# 6. Apply if plan looks good
terraform apply tfplan

# 7. Commit state lock (if not using remote backend)
git add terraform.tfstate
git commit -m "chore: update terraform state"
git push
```

---

### Making Changes

```bash
# 1. Create feature branch
git checkout -b infra/add-cache-layer

# 2. Make infrastructure changes
vim main.tf

# 3. Format code
terraform fmt -recursive

# 4. Validate
terraform validate

# 5. Plan
terraform plan

# 6. Commit changes
git add .
git commit -m "feat: add Redis cache layer"
git push origin infra/add-cache-layer

# 7. Create PR for review
gh pr create --title "Add Redis cache layer" --body "Adds ElastiCache Redis for session storage"

# 8. After approval, apply
terraform apply

# 9. Merge PR
gh pr merge
```

---

## Quick Reference

### Infrastructure Checklist

Before deploying infrastructure:

- [ ] Code in version control
- [ ] Remote state configured (S3/Cloud Storage)
- [ ] State locking enabled (DynamoDB/Cloud Storage)
- [ ] All secrets in secrets manager (not hardcoded)
- [ ] Resources tagged appropriately
- [ ] IAM policies follow least privilege
- [ ] Encryption enabled (at rest and in transit)
- [ ] Backups configured
- [ ] Multi-AZ/region if needed for HA
- [ ] Cost estimates reviewed
- [ ] Plan reviewed by team
- [ ] Runbook documented for changes

---

### Common Terraform Commands

```bash
# Initialization
terraform init                    # Initialize working directory
terraform init -upgrade           # Upgrade providers

# Planning
terraform plan                    # Show execution plan
terraform plan -out=plan.tfplan   # Save plan to file
terraform show plan.tfplan        # View saved plan

# Applying
terraform apply                   # Apply changes
terraform apply plan.tfplan       # Apply saved plan
terraform apply -auto-approve     # Skip confirmation (CI/CD)

# State
terraform state list              # List resources in state
terraform state show aws_instance.web  # Show resource details
terraform state mv                # Move resource in state
terraform state rm                # Remove resource from state

# Outputs
terraform output                  # Show all outputs
terraform output alb_dns_name     # Show specific output

# Workspaces
terraform workspace list          # List workspaces
terraform workspace new prod      # Create workspace
terraform workspace select prod   # Switch workspace

# Maintenance
terraform fmt -recursive          # Format all files
terraform validate                # Validate configuration
terraform refresh                 # Update state with real resources
terraform destroy                 # Destroy all resources
```

---

### Common Pulumi Commands

```bash
# Project setup
pulumi new aws-typescript         # Create new project
pulumi stack init production      # Create new stack

# Deployment
pulumi preview                    # Preview changes
pulumi up                         # Deploy changes
pulumi up --yes                   # Deploy without confirmation

# State
pulumi stack output               # Show all outputs
pulumi stack output apiUrl        # Show specific output
pulumi stack export > state.json  # Export state
pulumi stack import < state.json  # Import state

# Stack management
pulumi stack ls                   # List stacks
pulumi stack select production    # Switch stack
pulumi stack rm dev               # Delete stack

# Configuration
pulumi config set aws:region us-west-2          # Set config
pulumi config set --secret dbPassword pass123   # Set secret

# Maintenance
pulumi refresh                    # Sync state with real resources
pulumi destroy                    # Destroy all resources
```

---

## Integration with Other Skills

### With Deployment
- Infrastructure provisioned before application deployment
- IaC creates compute, networking, storage resources
- Deployment tools (kubectl, docker) deploy applications to infrastructure
- Infrastructure changes deployed separately from application code

### With CI/CD
- Infrastructure changes tested in CI pipeline
- Terraform/Pulumi plan runs on every PR
- Automated deployment to dev/staging environments
- Manual approval required for production infrastructure changes
- State drift detection in CI

### With Monitoring
- Infrastructure metrics collected (CPU, memory, disk, network)
- Cloud provider metrics integrated (CloudWatch, Azure Monitor)
- Infrastructure alerts for resource exhaustion
- Cost monitoring and budget alerts

### With Security
- IAM policies defined as code
- Security groups and network ACLs in IaC
- Secrets stored in secrets management services
- Compliance scanning for infrastructure code (Checkov, tfsec)

---

**Remember:** Infrastructure is code. Treat it with the same discipline as application code: version control, code review, automated testing, and continuous deployment. Never make manual changes in production—always update the code and redeploy. Infrastructure drift is a bug.
