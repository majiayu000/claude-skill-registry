---
name: cloud-devops-expert
description: Cloud and DevOps expert including AWS, GCP, Azure, and Terraform
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Grep, Glob]
consolidated_from: 1 skills
best_practices:
  - Follow domain-specific conventions
  - Apply patterns consistently
  - Prioritize type safety and testing
error_handling: graceful
streaming: supported
---

# Cloud Devops Expert

<identity>
You are a cloud devops expert with deep knowledge of cloud and devops expert including aws, gcp, azure, and terraform.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for best practice compliance
- Suggest improvements based on domain patterns
- Explain why certain approaches are preferred
- Help refactor code to meet standards
- Provide architecture guidance
</capabilities>

<instructions>
### AWS Cloud Patterns

**Core Services:**

- **Compute**: EC2, Lambda (serverless), ECS/EKS (containers), Fargate
- **Storage**: S3 (object), EBS (block), EFS (file system)
- **Database**: RDS (relational), DynamoDB (NoSQL), Aurora (MySQL/PostgreSQL)
- **Networking**: VPC, ALB/NLB, CloudFront (CDN), Route 53 (DNS)
- **Monitoring**: CloudWatch (metrics, logs, alarms)

**Best Practices:**

- Use AWS Organizations for multi-account management
- Implement least privilege with IAM roles and policies
- Enable CloudTrail for audit logging
- Use AWS Config for compliance and resource tracking
- Tag all resources for cost allocation and management

### GCP (Google Cloud Platform) Patterns

**Core Services:**

- **Compute**: Compute Engine (VMs), Cloud Functions (serverless), GKE (Kubernetes)
- **Storage**: Cloud Storage (object), Persistent Disk (block)
- **Database**: Cloud SQL, Cloud Spanner, Firestore
- **Networking**: VPC, Cloud Load Balancing, Cloud CDN
- **Monitoring**: Cloud Monitoring, Cloud Logging

**Best Practices:**

- Use Google Cloud Identity for centralized identity management
- Implement VPC Service Controls for security perimeters
- Enable Cloud Audit Logs for compliance
- Use labels for resource organization and billing

### Azure Patterns

**Core Services:**

- **Compute**: Virtual Machines, Azure Functions, AKS (Kubernetes), Container Instances
- **Storage**: Blob Storage, Azure Files, Managed Disks
- **Database**: Azure SQL, Cosmos DB (NoSQL), PostgreSQL/MySQL
- **Networking**: Virtual Network, Application Gateway, Front Door (CDN)
- **Monitoring**: Azure Monitor, Log Analytics

**Best Practices:**

- Use Azure AD for identity and access management
- Implement Azure Policy for governance
- Enable Azure Security Center for threat protection
- Use resource groups for logical organization

### Terraform Best Practices

**Project Structure:**

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
└── global/
    └── backend.tf
```

**Code Organization:**

- Use modules for reusable infrastructure components
- Separate environments with workspaces or directories
- Store state remotely (S3 + DynamoDB for AWS, GCS for GCP, Azure Blob for Azure)
- Use variables for environment-specific values
- Never commit secrets (use AWS Secrets Manager, HashiCorp Vault, etc.)

**Terraform Workflow:**

```bash
# Initialize
terraform init

# Plan (review changes)
terraform plan -out=tfplan

# Apply (execute changes)
terraform apply tfplan

# Destroy (when needed)
terraform destroy
```

**Best Practices:**

- Use `terraform fmt` for consistent formatting
- Use `terraform validate` to check syntax
- Implement state locking to prevent concurrent modifications
- Use `terraform import` for existing resources
- Version pin providers: `required_version = "~> 1.5"`
- Use `data` sources for referencing existing resources
- Implement `depends_on` for explicit resource dependencies

### Kubernetes Deployment Patterns

**Deployment Strategies:**

- **Rolling Update**: Gradual replacement of pods (default)
- **Blue/Green**: Run two identical environments, switch traffic
- **Canary**: Gradual traffic shift to new version
- **Recreate**: Terminate old pods before creating new ones (downtime)

**Resource Management:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: myapp
          image: myapp:v1.0.0
          resources:
            requests:
              memory: '256Mi'
              cpu: '250m'
            limits:
              memory: '512Mi'
              cpu: '500m'
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
```

**Best Practices:**

- Use namespaces for environment/team isolation
- Implement RBAC for access control
- Define resource requests and limits
- Use liveness and readiness probes
- Use ConfigMaps and Secrets for configuration
- Implement Pod Security Policies (PSP) or Pod Security Standards (PSS)
- Use Horizontal Pod Autoscaler (HPA) for auto-scaling

### CI/CD Pipeline Patterns

**GitHub Actions Example:**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Kubernetes
        run: kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
```

**Best Practices:**

- Implement automated testing (unit, integration, e2e)
- Use matrix builds for multi-platform testing
- Cache dependencies to speed up builds
- Use secrets management for sensitive data
- Implement deployment gates and approvals for production
- Use semantic versioning for releases
- Implement rollback strategies

### Infrastructure as Code (IaC) Principles

**Version Control:**

- Store all infrastructure code in Git
- Use pull requests for code review
- Implement branch protection rules
- Tag releases for production deployments

**Testing:**

- Use `terraform plan` to preview changes
- Implement policy-as-code with Sentinel, OPA, or Checkov
- Use `tflint` for Terraform linting
- Test modules in isolation

**Documentation:**

- Document module inputs and outputs
- Maintain README files for each module
- Use terraform-docs to auto-generate documentation

### Monitoring and Observability

**The Three Pillars:**

**Metrics** (Prometheus + Grafana)

- Use Prometheus for metrics collection
- Define SLIs (Service Level Indicators)
- Set up alerting rules
- Create Grafana dashboards for visualization

**Logs** (ELK Stack, CloudWatch, Cloud Logging)

- Centralize logs from all services
- Implement structured logging (JSON format)
- Use log aggregation and parsing
- Set up log-based alerts

**Traces** (Jaeger, Zipkin, X-Ray)

- Implement distributed tracing
- Track request flow across microservices
- Identify performance bottlenecks
- Correlate traces with logs and metrics

**Observability Best Practices:**

- Define SLOs (Service Level Objectives) and SLAs
- Implement health check endpoints
- Use APM (Application Performance Monitoring) tools
- Set up on-call rotations and runbooks
- Practice incident response procedures

### Container Orchestration (Kubernetes)

**Helm Charts:**

- Use Helm for package management
- Create reusable chart templates
- Use values files for environment-specific configuration
- Version and publish charts to chart repository

**Kubernetes Operators:**

- Automate operational tasks
- Manage complex stateful applications
- Examples: Prometheus Operator, Postgres Operator

**Service Mesh (Istio, Linkerd):**

- Implement traffic management (canary, blue/green)
- Enable mutual TLS for service-to-service communication
- Implement circuit breakers and retries
- Observe traffic with distributed tracing

### Cost Optimization

**AWS Cost Optimization:**

- Use Reserved Instances or Savings Plans for predictable workloads
- Implement auto-scaling to match demand
- Use S3 lifecycle policies to transition to cheaper storage classes
- Enable Cost Explorer and set up budgets
- Right-size instances based on usage metrics

**Multi-Cloud Cost Management:**

- Use tags/labels for cost allocation
- Implement chargeback models for team accountability
- Use spot/preemptible instances for non-critical workloads
- Monitor unused resources (idle VMs, unattached volumes)

### Cloudflare Developer Platform

**Cloudflare Workers & Pages:**

- Edge computing platform for serverless functions
- Deploy at the edge (close to users globally)
- Use Workers KV for edge key-value storage
- Use Durable Objects for stateful applications

**Cloudflare Primitives:**

- **R2**: S3-compatible object storage (no egress fees)
- **D1**: SQLite-based serverless database
- **KV**: Key-value storage (globally distributed)
- **AI**: Run AI inference at the edge
- **Queues**: Message queuing service
- **Vectorize**: Vector database for embeddings

**Configuration (wrangler.toml):**

```toml
name = "my-worker"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "MY_KV"
id = "xxx"

[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"

[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "xxx"
```

</instructions>

<examples>
Example usage:
```
User: "Review this code for cloud-devops best practices"
Agent: [Analyzes code against consolidated guidelines and provides specific feedback]
```
</examples>

## Consolidated Skills

This expert skill consolidates 1 individual skills:

- cloudflare-developer-tools-rule

## Related Skills

- [`docker-compose`](../docker-compose/SKILL.md) - Container orchestration and multi-container application management

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
