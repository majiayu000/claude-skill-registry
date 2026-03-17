---
name: devops-role-skill
version: 1.0.0
category: infrastructure
complexity: high
status: active
created: 2025-12-12
author: claude-command-and-control

description: |
  Professional DevOps engineering skill for creating CI/CD pipelines, implementing
  infrastructure as code, managing environments, and establishing monitoring and
  observability across all deployment stages.

triggers:
  - "create pipeline"
  - "setup cicd"
  - "infrastructure as code"
  - "deploy infrastructure"
  - "setup monitoring"

dependencies: []

tags:
  - devops
  - cicd
  - infrastructure
  - monitoring
  - automation
  - deployment
---

# DevOps Role Skill

## Description

Create CI/CD pipelines, automate build and deployment processes, implement monitoring and observability, and manage infrastructure across all environments. This skill implements professional DevOps practices including pipeline automation, infrastructure as code, environment management, and comprehensive monitoring.

## When to Use This Skill

- Creating CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)
- Implementing infrastructure as code (Terraform, CloudFormation)
- Setting up environment configurations (dev, staging, production)
- Implementing monitoring and observability (Prometheus, Grafana)
- Automating deployment processes
- Managing containerization and orchestration (Docker, Kubernetes)
- Implementing security scanning and compliance checks

## When NOT to Use This Skill

- For application code development (use builder-role-skill)
- For system architecture design (use architect-role-skill)
- For code testing and validation (use validator-role-skill)
- For documentation writing (use scribe-role-skill)

## Prerequisites

- Access to CI/CD platform (GitHub Actions, GitLab, Jenkins)
- Cloud provider credentials (AWS, GCP, Azure)
- Infrastructure as Code tools installed (Terraform, Ansible)
- Container registry access
- Kubernetes cluster access (if using K8s)
- Monitoring tools configured

---

## Workflow

### Phase 1: CI/CD Pipeline Creation

Implement automated build, test, and deployment workflows.

**Step 1.1: Requirements Analysis**

```
Load context files:
- DEVELOPMENT_PLAN.md (deployment strategy)
- ARCHITECTURE.md (system components)
- README.md (project overview)
- Security requirements
```

**Step 1.2: Create Pipeline Configuration**

#### GitHub Actions Example

Create `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '18.x'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ============================================
  # LINT & FORMAT CHECK
  # ============================================
  lint:
    name: Lint and Format Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Check formatting
        run: npm run format:check

  # ============================================
  # BUILD
  # ============================================
  build:
    name: Build Application
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-artifacts
          path: dist/
          retention-days: 7

  # ============================================
  # TEST
  # ============================================
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        test-type: [unit, integration]
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ${{ matrix.test-type }} tests
        run: npm run test:${{ matrix.test-type }}

      - name: Generate coverage report
        if: matrix.test-type == 'unit'
        run: npm run coverage

      - name: Upload coverage to Codecov
        if: matrix.test-type == 'unit'
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
          flags: unittests

  # ============================================
  # SECURITY SCAN
  # ============================================
  security:
    name: Security Scanning
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4

      - name: Run dependency audit
        run: npm audit --audit-level=moderate

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  # ============================================
  # BUILD DOCKER IMAGE
  # ============================================
  docker:
    name: Build and Push Docker Image
    runs-on: ubuntu-latest
    needs: [build, test, security]
    if: github.event_name == 'push'
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ============================================
  # DEPLOY TO STAGING
  # ============================================
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: docker
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}

      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:develop-${{ github.sha }}
          kubectl rollout status deployment/app

      - name: Run smoke tests
        run: |
          npm run test:smoke -- --url=https://staging.example.com

  # ============================================
  # DEPLOY TO PRODUCTION
  # ============================================
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: docker
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://www.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}

      - name: Deploy to Kubernetes (Blue-Green)
        run: |
          # Deploy green version
          kubectl apply -f k8s/green-deployment.yaml
          kubectl set image deployment/app-green \
            app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main-${{ github.sha }}

          # Wait for rollout
          kubectl rollout status deployment/app-green

          # Run health checks
          kubectl run health-check --rm -i --restart=Never \
            --image=curlimages/curl -- \
            curl http://app-green-service/health

          # Switch traffic to green
          kubectl patch service app-service \
            -p '{"spec":{"selector":{"version":"green"}}}'

          # Delete old blue deployment
          kubectl delete deployment app-blue || true

          # Rename green to blue for next deploy
          kubectl label deployment app-green version=blue --overwrite

      - name: Run production smoke tests
        run: |
          npm run test:smoke -- --url=https://www.example.com

      - name: Notify team
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Production deployment successful!",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Production Deployment Complete* :rocket:\nCommit: ${{ github.sha }}\nAuthor: ${{ github.actor }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

**Step 1.3: Create Dockerfile**

```dockerfile
# Multi-stage build for optimal image size
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# ============================================
# Production image
# ============================================
FROM node:18-alpine

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy built artifacts and dependencies
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/main.js"]
```

---

### Phase 2: Infrastructure as Code

Manage infrastructure using declarative configuration.

**Step 2.1: Terraform Configuration**

Create `terraform/main.tf`:

```hcl
# ============================================
# Provider Configuration
# ============================================
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "app/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "MyApp"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# ============================================
# VPC and Networking
# ============================================
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "${var.project_name}-${var.environment}-vpc"
  cidr = var.vpc_cidr

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = true
  enable_vpn_gateway = false

  enable_dns_hostnames = true
  enable_dns_support   = true
}

# ============================================
# EKS Cluster
# ============================================
module "eks" {
  source = "terraform-aws-modules/eks/aws"

  cluster_name    = "${var.project_name}-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    general = {
      desired_size = var.node_desired_size
      min_size     = var.node_min_size
      max_size     = var.node_max_size

      instance_types = var.node_instance_types
      capacity_type  = "ON_DEMAND"

      labels = {
        role = "general"
      }

      tags = {
        NodeGroup = "general"
      }
    }
  }

  # Cluster access entry
  enable_cluster_creator_admin_permissions = true
}

# ============================================
# RDS Database
# ============================================
module "db" {
  source = "terraform-aws-modules/rds/aws"

  identifier = "${var.project_name}-${var.environment}-db"

  engine               = "postgres"
  engine_version       = "15.4"
  family              = "postgres15"
  major_engine_version = "15"
  instance_class       = var.db_instance_class

  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage

  db_name  = var.db_name
  username = var.db_username
  port     = 5432

  multi_az               = var.environment == "production"
  db_subnet_group_name   = module.vpc.database_subnet_group
  vpc_security_group_ids = [aws_security_group.database.id]

  backup_retention_period = var.environment == "production" ? 30 : 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "Mon:04:00-Mon:05:00"

  deletion_protection = var.environment == "production"

  enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

  tags = {
    Name = "${var.project_name}-${var.environment}-db"
  }
}

# ============================================
# ElastiCache Redis
# ============================================
module "redis" {
  source = "terraform-aws-modules/elasticache/aws"

  cluster_id           = "${var.project_name}-${var.environment}-redis"
  engine              = "redis"
  engine_version      = "7.0"
  node_type           = var.redis_node_type
  num_cache_nodes     = 1
  parameter_group_family = "redis7"

  subnet_ids         = module.vpc.private_subnets
  security_group_ids = [aws_security_group.redis.id]

  snapshot_retention_limit = var.environment == "production" ? 5 : 1
  snapshot_window         = "05:00-06:00"
  maintenance_window      = "sun:06:00-sun:07:00"
}

# ============================================
# Security Groups
# ============================================
resource "aws_security_group" "database" {
  name_prefix = "${var.project_name}-${var.environment}-db-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "redis" {
  name_prefix = "${var.project_name}-${var.environment}-redis-"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [module.eks.node_security_group_id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ============================================
# Outputs
# ============================================
output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "database_endpoint" {
  value = module.db.db_instance_endpoint
}

output "redis_endpoint" {
  value = module.redis.cache_nodes[0].address
}
```

**Step 2.2: Variables and Environments**

Create `terraform/variables.tf`:

```hcl
variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Project name"
  type        = string
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "Private subnet CIDR blocks"
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "Public subnet CIDR blocks"
  type        = list(string)
}

variable "node_desired_size" {
  description = "Desired number of EKS nodes"
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "Minimum number of EKS nodes"
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "Maximum number of EKS nodes"
  type        = number
  default     = 5
}

variable "node_instance_types" {
  description = "EKS node instance types"
  type        = list(string)
  default     = ["t3.medium"]
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "RDS allocated storage (GB)"
  type        = number
  default     = 20
}

variable "db_max_allocated_storage" {
  description = "RDS maximum allocated storage (GB)"
  type        = number
  default     = 100
}

variable "db_name" {
  description = "Database name"
  type        = string
}

variable "db_username" {
  description = "Database username"
  type        = string
}

variable "redis_node_type" {
  description = "ElastiCache Redis node type"
  type        = string
  default     = "cache.t3.micro"
}
```

**Step 2.3: Terraform Execution**

```bash
# Initialize Terraform
terraform init

# Select workspace (environment)
terraform workspace select production || terraform workspace new production

# Plan changes
terraform plan -var-file=environments/production.tfvars

# Apply changes (requires approval)
terraform apply -var-file=environments/production.tfvars

# View outputs
terraform output
```

---

### Phase 3: Monitoring and Observability

Implement comprehensive monitoring, logging, and alerting.

**Step 3.1: Prometheus Configuration**

Create `monitoring/prometheus-config.yaml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    environment: 'prod'

# Alerting configuration
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093

# Load rules
rule_files:
  - /etc/prometheus/rules/*.yml

# Scrape configurations
scrape_configs:
  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Kubernetes API server
  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - source_labels: [__meta_kubernetes_namespace, __meta_kubernetes_service_name, __meta_kubernetes_endpoint_port_name]
        action: keep
        regex: default;kubernetes;https

  # Kubernetes nodes
  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)

  # Application pods
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name
```

**Step 3.2: Alert Rules**

Create `monitoring/alert-rules.yml`:

```yaml
groups:
  - name: application_alerts
    interval: 30s
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
          /
          sum(rate(http_requests_total[5m])) by (service)
          > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "{{ $labels.service }} has error rate {{ $value | humanizePercentage }}"

      # High response time
      - alert: HighResponseTime
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }}s"

      # Service down
      - alert: ServiceDown
        expr: up{job="application"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "{{ $labels.instance }} has been down for more than 2 minutes"

  - name: infrastructure_alerts
    interval: 30s
    rules:
      # High CPU usage
      - alert: HighCPUUsage
        expr: |
          100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "{{ $labels.instance }} CPU usage is {{ $value }}%"

      # High memory usage
      - alert: HighMemoryUsage
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "{{ $labels.instance }} memory usage is {{ $value }}%"

      # Disk space running out
      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{fstype!~"tmpfs"} / node_filesystem_size_bytes{fstype!~"tmpfs"}) * 100 < 15
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Disk space running low"
          description: "{{ $labels.instance }} disk {{ $labels.mountpoint }} has {{ $value }}% free"
```

---

## Collaboration Patterns

### With Architect (or architect-role-skill)

- Review ARCHITECTURE.md for infrastructure requirements
- Validate deployment strategy aligns with design
- Confirm scalability and availability targets

### With Builder (or builder-role-skill)

- Coordinate on build process and artifacts
- Ensure application exposes health check endpoints
- Verify environment variable requirements

### With Validator (or validator-role-skill)

- Integrate test execution into CI/CD pipeline
- Configure automated security scanning
- Implement quality gates

### With Scribe (or scribe-role-skill)

- Collaborate on deployment documentation
- Document infrastructure architecture
- Create runbooks for operations

---

## Examples

### Example 1: GitHub Actions CI/CD Pipeline

**Task**: Create complete CI/CD pipeline for Node.js application

```markdown
## Deliverables
- GitHub Actions workflow with lint, build, test, security scan
- Docker multi-stage build configuration
- Kubernetes deployment manifests
- Blue-green deployment strategy for production

**Result**: Automated pipeline with 8-minute build-to-production time
```

### Example 2: AWS Infrastructure with Terraform

**Task**: Provision production infrastructure on AWS

```markdown
## Infrastructure Created
- VPC with public/private subnets across 3 AZs
- EKS cluster with managed node groups (auto-scaling 2-5 nodes)
- RDS PostgreSQL with multi-AZ failover
- ElastiCache Redis for caching
- All with proper security groups and IAM roles

**Result**: Fully automated infrastructure provisioning in 15 minutes
```

### Example 3: Monitoring Stack Setup

**Task**: Implement comprehensive monitoring and alerting

```markdown
## Monitoring Implemented
- Prometheus for metrics collection
- Grafana dashboards for visualization
- Alert rules for critical metrics (errors, latency, resource usage)
- PagerDuty integration for on-call notifications

**Result**: Full observability with <2 minute alert response time
```

---

## Resources

### Templates

- `resources/github-actions-template.yml` - GitHub Actions workflow template
- `resources/terraform-aws-template.tf` - AWS infrastructure template
- `resources/prometheus-config-template.yaml` - Prometheus configuration template
- `resources/grafana-dashboard-template.json` - Grafana dashboard template

### Scripts

- `scripts/terraform-init.sh` - Terraform initialization script
- `scripts/deploy-monitoring.sh` - Monitoring stack deployment
- `scripts/backup-database.sh` - Database backup automation

---

## References

- [Agent Skills vs. Multi-Agent](../../docs/best-practices/09-Agent-Skills-vs-Multi-Agent.md)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Kubernetes Production Best Practices](https://learnk8s.io/production-best-practices)
- [Prometheus Monitoring Guide](https://prometheus.io/docs/practices/)

---

**Version**: 1.0.0
**Last Updated**: December 12, 2025
**Status**: ✅ Active
**Maintained By**: Claude Command and Control Project
