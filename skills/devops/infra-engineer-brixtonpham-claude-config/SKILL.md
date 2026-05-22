---
name: infra-engineer
description: "Comprehensive infrastructure engineering covering DevOps, cloud platforms, FinOps, and DevSecOps. Platforms: AWS (EC2, Lambda, S3, ECS, EKS, RDS, CloudFormation), Azure basics, Cloudflare (Workers, R2, D1, Pages), GCP (GKE, Cloud Run, Cloud Storage), Docker, Kubernetes. Capabilities: CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins), GitOps, infrastructure as code (Terraform, CloudFormation), container orchestration, cost optimization, security scanning, vulnerability management, secrets management, compliance (SOC2, HIPAA). Actions: deploy, configure, manage, scale, monitor, secure, optimize cloud infrastructure. Keywords: AWS, EC2, Lambda, S3, ECS, EKS, RDS, CloudFormation, Azure, Kubernetes, k8s, Docker, Terraform, CI/CD, GitHub Actions, GitLab CI, Jenkins, ArgoCD, Flux, cost optimization, FinOps, reserved instances, spot instances, security scanning, SAST, DAST, vulnerability management, secrets management, Vault, compliance, monitoring, observability. Use when: deploying to AWS/Azure/GCP/Cloudflare, setting up CI/CD pipelines, implementing GitOps workflows, managing Kubernetes clusters, optimizing cloud costs, implementing security best practices, managing infrastructure as code, container orchestration, compliance requirements, cost analysis and optimization."
license: MIT
version: 2.0.0
---

# Infrastructure Engineering Skill

Comprehensive guide for modern infrastructure engineering covering DevOps practices, multi-cloud platforms (AWS, Azure, GCP, Cloudflare), FinOps cost optimization, and DevSecOps security practices.

## When to Use This Skill

Use this skill when:
- **DevOps**: Setting up CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins), implementing GitOps workflows (ArgoCD, Flux)
- **AWS**: Deploying to EC2, Lambda, ECS, EKS, managing S3, RDS, using CloudFormation/CDK
- **Azure**: Working with Azure VMs, App Service, AKS, Azure Functions, Storage Accounts
- **GCP**: Managing Compute Engine, GKE, Cloud Run, Cloud Storage, App Engine
- **Cloudflare**: Deploying Workers, R2 storage, D1 databases, Pages applications
- **Kubernetes**: Managing clusters, deployments, services, ingress, Helm charts, operators
- **Docker**: Containerizing applications, multi-stage builds, Docker Compose, registries
- **FinOps**: Analyzing cloud costs, optimizing spend, reserved instances, spot instances, rightsizing
- **DevSecOps**: Security scanning (SAST/DAST), vulnerability management, secrets management, compliance
- **IaC**: Terraform, CloudFormation, Pulumi, configuration management
- **Monitoring**: Setting up observability, logging, metrics, alerting, distributed tracing

## Platform Selection Guide

### When to Use AWS

**Best For:**
- General-purpose cloud computing at scale
- Mature ecosystem with 200+ services
- Enterprise workloads with compliance requirements
- Hybrid cloud with AWS Outposts
- Extensive third-party integrations
- Advanced networking and security controls

**Key Services:**
- EC2 (virtual machines, flexible compute)
- Lambda (serverless functions, event-driven)
- ECS/EKS (container orchestration)
- S3 (object storage, industry standard)
- RDS (managed relational databases)
- DynamoDB (NoSQL, global tables)
- CloudFormation/CDK (infrastructure as code)
- IAM (identity and access management)
- VPC (virtual private cloud networking)

**Cost Profile:** Pay-as-you-go, reserved instances (up to 72% discount), savings plans, spot instances (up to 90% discount)

### When to Use Azure

**Best For:**
- Microsoft-centric organizations (.NET, Active Directory)
- Hybrid cloud scenarios (Azure Arc, Stack)
- Enterprise agreements with Microsoft
- Windows Server and SQL Server workloads
- Integration with Microsoft 365 and Dynamics
- Strong compliance certifications (90+ certifications)

**Key Services:**
- Virtual Machines (Windows/Linux compute)
- App Service (PaaS for web apps)
- AKS (managed Kubernetes)
- Azure Functions (serverless compute)
- Storage Accounts (Blob, File, Queue, Table)
- SQL Database (managed SQL Server)
- Active Directory (identity management)
- ARM Templates/Bicep (infrastructure as code)

**Cost Profile:** Pay-as-you-go, reserved instances, Azure Hybrid Benefit for Windows/SQL Server licenses

### When to Use Cloudflare

**Best For:**
- Edge-first applications with global distribution
- Ultra-low latency requirements (<50ms)
- Static sites with serverless functions
- Zero egress cost scenarios (R2 storage)
- WebSocket/real-time applications (Durable Objects)
- AI/ML at the edge (Workers AI)

**Key Products:**
- Workers (serverless functions)
- R2 (object storage, S3-compatible)
- D1 (SQLite database with global replication)
- KV (key-value store)
- Pages (static hosting + functions)
- Durable Objects (stateful compute)
- Browser Rendering (headless browser automation)

**Cost Profile:** Pay-per-request, generous free tier, zero egress fees

### When to Use Kubernetes

**Best For:**
- Container orchestration at scale
- Microservices architectures with 10+ services
- Multi-cloud and hybrid deployments
- Self-healing and auto-scaling workloads
- Complex deployment strategies (blue/green, canary)
- Service mesh architectures (Istio, Linkerd)
- Stateful applications with operators

**Key Features:**
- Declarative configuration (YAML manifests)
- Automated rollouts and rollbacks
- Service discovery and load balancing
- Self-healing (restarts failed containers)
- Horizontal pod autoscaling
- Secret and configuration management
- Storage orchestration
- Batch job execution

**Managed Options:** EKS (AWS), AKS (Azure), GKE (GCP), managed k8s providers

**Cost Profile:** Cluster management fees + node costs (optimize with spot instances, cluster autoscaling)

### When to Use Docker

**Best For:**
- Local development consistency
- Microservices architectures
- Multi-language stack applications
- Traditional VPS/VM deployments
- Foundation for Kubernetes workloads
- CI/CD build environments
- Database containerization (dev/test)

**Key Capabilities:**
- Application isolation and portability
- Multi-stage builds for optimization
- Docker Compose for multi-container apps
- Volume management for data persistence
- Network configuration and service discovery
- Cross-platform compatibility (amd64, arm64)
- BuildKit for improved build performance

**Cost Profile:** Infrastructure cost only (compute + storage), no orchestration overhead

### When to Use Google Cloud

**Best For:**
- Enterprise-scale applications
- Data analytics and ML pipelines (BigQuery, Vertex AI)
- Hybrid/multi-cloud deployments
- Kubernetes at scale (GKE)
- Managed databases (Cloud SQL, Firestore, Spanner)
- Complex IAM and compliance requirements

**Key Services:**
- Compute Engine (VMs)
- GKE (managed Kubernetes)
- Cloud Run (containerized serverless)
- App Engine (PaaS)
- Cloud Storage (object storage)
- Cloud SQL (managed databases)

**Cost Profile:** Varied pricing, sustained use discounts, committed use contracts

## Quick Start

### AWS Lambda Function

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# Configure credentials
aws configure

# Create Lambda function with SAM
sam init --runtime python3.11
sam build && sam deploy --guided
```

See: `references/aws-lambda.md`

### AWS EKS Kubernetes Cluster

```bash
# Install eksctl
brew install eksctl  # or curl download

# Create cluster
eksctl create cluster \
  --name my-cluster \
  --region us-west-2 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 3 \
  --nodes-min 1 \
  --nodes-max 4
```

See: `references/kubernetes-basics.md`

### Azure Deployment

```bash
# Install Azure CLI
curl -L https://aka.ms/InstallAzureCli | bash

# Login and create resources
az login
az group create --name myResourceGroup --location eastus
az webapp create --resource-group myResourceGroup \
  --name myapp --runtime "NODE:18-lts"
```

See: `references/azure-basics.md`

### Cloudflare Workers

```bash
# Install Wrangler CLI
npm install -g wrangler

# Create and deploy Worker
wrangler init my-worker
cd my-worker
wrangler deploy
```

See: `references/cloudflare-workers-basics.md`

### Kubernetes Deployment

```bash
# Create deployment
kubectl create deployment nginx --image=nginx:latest
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Apply from manifest
kubectl apply -f deployment.yaml

# Check status
kubectl get pods,services,deployments
```

See: `references/kubernetes-basics.md`

### Docker Container

```bash
# Create Dockerfile
cat > Dockerfile <<EOF
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
EOF

# Build and run
docker build -t myapp .
docker run -p 3000:3000 myapp
```

See: `references/docker-basics.md`

## Reference Navigation

### AWS (Amazon Web Services)
- `aws-overview.md` - AWS fundamentals, account setup, IAM basics
- `aws-ec2.md` - EC2 instances, AMIs, security groups, auto-scaling
- `aws-lambda.md` - Serverless functions, SAM, event sources, layers
- `aws-ecs-eks.md` - Container orchestration, ECS vs EKS, Fargate
- `aws-s3-rds.md` - S3 storage, RDS databases, backup strategies
- `aws-cloudformation.md` - Infrastructure as code, CDK, best practices
- `aws-networking.md` - VPC, subnets, security groups, load balancers

### Azure (Microsoft Azure)
- `azure-basics.md` - Azure fundamentals, subscriptions, resource groups
- `azure-compute.md` - VMs, App Service, AKS, Azure Functions
- `azure-storage.md` - Storage Accounts, Blob, Files, managed disks

### Cloudflare Platform
- `cloudflare-platform.md` - Edge computing overview, key components
- `cloudflare-workers-basics.md` - Getting started, handler types, basic patterns
- `cloudflare-workers-advanced.md` - Advanced patterns, performance, optimization
- `cloudflare-workers-apis.md` - Runtime APIs, bindings, integrations
- `cloudflare-r2-storage.md` - R2 object storage, S3 compatibility, best practices
- `cloudflare-d1-kv.md` - D1 SQLite database, KV store, use cases
- `browser-rendering.md` - Puppeteer/Playwright automation on Cloudflare

### Kubernetes & Container Orchestration
- `kubernetes-basics.md` - Core concepts, pods, deployments, services
- `kubernetes-advanced.md` - StatefulSets, operators, custom resources
- `kubernetes-networking.md` - Ingress, service mesh, network policies
- `helm-charts.md` - Package management, charts, repositories

### Docker Containerization
- `docker-basics.md` - Core concepts, Dockerfile, images, containers
- `docker-compose.md` - Multi-container apps, networking, volumes
- `docker-security.md` - Image scanning, secrets, best practices

### Google Cloud Platform
- `gcloud-platform.md` - GCP overview, gcloud CLI, authentication
- `gcloud-services.md` - Compute Engine, GKE, Cloud Run, App Engine

### CI/CD & GitOps
- `cicd-github-actions.md` - GitHub Actions workflows, runners, secrets
- `cicd-gitlab.md` - GitLab CI/CD pipelines, artifacts, caching
- `gitops-argocd.md` - ArgoCD setup, app of apps pattern, sync policies
- `gitops-flux.md` - Flux controllers, GitOps toolkit, multi-tenancy

### FinOps (Cost Optimization)
- `finops-basics.md` - Cost optimization principles, FinOps lifecycle
- `finops-aws.md` - AWS cost optimization, RI, savings plans, spot
- `finops-azure.md` - Azure cost management, reservations, hybrid benefit
- `finops-gcp.md` - GCP cost optimization, committed use, sustained use
- `finops-tools.md` - Cost analysis tools, Kubecost, CloudHealth, Infracost

### DevSecOps (Security)
- `devsecops-basics.md` - Security best practices, shift-left security
- `devsecops-scanning.md` - SAST, DAST, SCA, container scanning
- `secrets-management.md` - Vault, AWS Secrets Manager, sealed secrets
- `compliance.md` - SOC2, HIPAA, PCI-DSS, audit logging

### Infrastructure as Code
- `terraform-basics.md` - Terraform fundamentals, providers, state
- `terraform-advanced.md` - Modules, workspaces, remote state
- `cloudformation-basics.md` - CloudFormation templates, stacks, change sets

### Utilities & Scripts
- `scripts/cloudflare-deploy.py` - Automate Cloudflare Worker deployments
- `scripts/docker-optimize.py` - Analyze and optimize Dockerfiles
- `scripts/cost-analyzer.py` - Cloud cost analysis and reporting
- `scripts/security-scanner.py` - Automated security scanning

## Common Workflows

### Multi-Cloud Architecture

```yaml
# Edge Layer: Cloudflare Workers (global routing, caching)
# Compute Layer: AWS ECS/Lambda or Azure App Service (application logic)
# Data Layer: AWS RDS or Azure SQL (persistent storage)
# CDN/Storage: Cloudflare R2 or AWS S3 (static assets)

Benefits:
- Best-of-breed services per layer
- Geographic redundancy
- Cost optimization across providers
```

### AWS ECS Deployment with CI/CD

```yaml
# GitHub Actions workflow
name: Deploy to ECS
on: push
jobs:
  deploy:
    - Build Docker image
    - Push to ECR
    - Update ECS task definition
    - Deploy to ECS service
    - Wait for deployment stabilization
```

### Kubernetes GitOps with ArgoCD

```yaml
# Git repository structure
/apps
  /production
    - deployment.yaml
    - service.yaml
    - ingress.yaml
  /staging
    - deployment.yaml

# ArgoCD syncs cluster state from Git
# Changes: Git commit → ArgoCD detects → Auto-sync to cluster
```

### Multi-Stage Docker Build

```dockerfile
# Build stage
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
USER node
CMD ["node", "dist/server.js"]
```

### FinOps Cost Optimization Workflow

```yaml
# 1. Discovery: Identify untagged resources
# 2. Analysis: Right-size instances (CPU/memory utilization)
# 3. Optimization:
#    - Convert to reserved instances (predictable workloads)
#    - Use spot instances (fault-tolerant workloads)
#    - Schedule start/stop (dev environments)
# 4. Monitoring: Set budget alerts, track savings
# 5. Governance: Enforce tagging policies
```

### DevSecOps Security Pipeline

```yaml
# 1. Code Commit
# 2. SAST Scan: SonarQube, Semgrep (static code analysis)
# 3. Dependency Check: Snyk, Trivy (vulnerability scanning)
# 4. Build: Docker image
# 5. Container Scan: Trivy, Grype (image vulnerabilities)
# 6. DAST Scan: OWASP ZAP (runtime security testing)
# 7. Deploy: Only if all scans pass
# 8. Runtime Protection: Falco, AWS GuardDuty
```

### Terraform Infrastructure Deployment

```hcl
# 1. Write: Define infrastructure in .tf files
# 2. Init: terraform init (download providers)
# 3. Plan: terraform plan (preview changes)
# 4. Apply: terraform apply (create/update resources)
# 5. State: Store state in S3 with DynamoDB locking
# 6. Modules: Reuse common patterns across environments
```

## Best Practices

### DevOps
- **CI/CD**: Automate testing and deployment, use feature flags for progressive rollouts
- **GitOps**: Declarative infrastructure, Git as single source of truth, automated sync
- **Monitoring**: Implement observability (logs, metrics, traces), set up alerting
- **Incident Management**: Runbooks, postmortems, blameless culture
- **Automation**: Infrastructure as code, configuration management, self-service platforms

### Security (DevSecOps)
- **Shift Left**: Security scanning early in pipeline (SAST, dependency checks)
- **Secrets Management**: Use Vault, AWS Secrets Manager, or sealed secrets (never in code/Git)
- **Container Security**: Run as non-root, minimal base images, regular scanning
- **Network Security**: Zero-trust architecture, service mesh, network policies
- **Access Control**: Least privilege IAM, MFA, temporary credentials
- **Compliance**: Audit logging, encryption at rest/transit, regular security reviews
- **Runtime Protection**: Security monitoring, intrusion detection, automated response

### Cost Optimization (FinOps)
- **Tagging**: Enforce resource tagging for cost allocation and tracking
- **Rightsizing**: Analyze utilization, downsize over-provisioned resources
- **Reserved Capacity**: Purchase RI/savings plans for predictable workloads (up to 72% discount)
- **Spot/Preemptible**: Use for fault-tolerant workloads (up to 90% discount)
- **Scheduling**: Auto-stop dev/test environments during off-hours
- **Storage Optimization**: Lifecycle policies, archive to cheaper tiers, delete orphaned resources
- **Monitoring**: Budget alerts, cost anomaly detection, chargeback/showback
- **Governance**: Approval workflows for expensive resources, quota management

### Kubernetes
- **Resource Management**: Set requests/limits, use horizontal pod autoscaling
- **High Availability**: Multi-zone clusters, pod disruption budgets, anti-affinity rules
- **Security**: RBAC, pod security policies, network policies, admission controllers
- **Observability**: Prometheus metrics, distributed tracing, centralized logging
- **GitOps**: ArgoCD/Flux for declarative deployments, automatic drift correction

### Performance
- **Compute**: Auto-scaling, load balancing, multi-region for low latency
- **Caching**: CDN, in-memory caching (Redis/Memcached), edge computing
- **Storage**: Choose appropriate tier (SSD vs HDD), enable caching, CDN for static assets
- **Containers**: Multi-stage builds, minimal images, layer caching
- **Databases**: Connection pooling, read replicas, query optimization, indexing

### Development
- **Local Development**: Docker Compose for consistent environments, dev containers
- **Testing**: Unit, integration, end-to-end tests in CI/CD pipeline
- **Infrastructure as Code**: Terraform/CloudFormation for repeatability
- **Documentation**: Architecture diagrams, runbooks, API documentation
- **Version Control**: Git for code and infrastructure, semantic versioning

## Decision Matrix

| Need | Choose |
|------|--------|
| **Compute** | |
| Sub-50ms latency globally | Cloudflare Workers |
| Serverless functions (AWS ecosystem) | AWS Lambda |
| Serverless functions (Azure ecosystem) | Azure Functions |
| Containerized workloads (managed) | AWS ECS/Fargate, Azure AKS, GCP Cloud Run |
| Kubernetes at scale | AWS EKS, Azure AKS, GCP GKE |
| VMs with full control | AWS EC2, Azure VMs, GCP Compute Engine |
| **Storage** | |
| Object storage (S3-compatible) | AWS S3, Cloudflare R2 (zero egress), Azure Blob |
| Block storage for VMs | AWS EBS, Azure Managed Disks, GCP Persistent Disk |
| File storage (NFS/SMB) | AWS EFS, Azure Files, GCP Filestore |
| **Database** | |
| Managed SQL (AWS) | AWS RDS (PostgreSQL, MySQL, SQL Server) |
| Managed SQL (Azure) | Azure SQL Database |
| Managed SQL (GCP) | Cloud SQL |
| NoSQL key-value | AWS DynamoDB, Azure Cosmos DB, Cloudflare KV |
| Global SQL (edge reads) | Cloudflare D1, AWS Aurora Global |
| **CI/CD & GitOps** | |
| GitHub-integrated CI/CD | GitHub Actions |
| Self-hosted CI/CD | GitLab CI/CD, Jenkins |
| Kubernetes GitOps | ArgoCD, Flux |
| **Cost Optimization** | |
| Predictable workloads | Reserved Instances, Savings Plans |
| Fault-tolerant workloads | Spot Instances (AWS), Preemptible VMs (GCP) |
| Dev/test environments | Auto-scheduling, budget alerts |
| **Security** | |
| Secrets management | HashiCorp Vault, AWS Secrets Manager, Azure Key Vault |
| Container scanning | Trivy, Snyk, AWS ECR scanning |
| SAST/DAST | SonarQube, Semgrep, OWASP ZAP |
| **Special Use Cases** | |
| Static site + edge functions | Cloudflare Pages, AWS Amplify |
| WebSocket/real-time | Cloudflare Durable Objects, AWS API Gateway WebSocket |
| ML/AI pipelines | AWS SageMaker, GCP Vertex AI, Azure ML |
| Browser automation | Cloudflare Browser Rendering, AWS Lambda + Puppeteer |

## Resources

### Cloud Providers
- **AWS Docs:** https://docs.aws.amazon.com
- **Azure Docs:** https://docs.microsoft.com/azure
- **GCP Docs:** https://cloud.google.com/docs
- **Cloudflare Docs:** https://developers.cloudflare.com

### Container & Orchestration
- **Docker Docs:** https://docs.docker.com
- **Kubernetes Docs:** https://kubernetes.io/docs
- **Helm:** https://helm.sh/docs

### CI/CD & GitOps
- **GitHub Actions:** https://docs.github.com/actions
- **GitLab CI:** https://docs.gitlab.com/ee/ci/
- **ArgoCD:** https://argo-cd.readthedocs.io
- **Flux:** https://fluxcd.io/docs

### Infrastructure as Code
- **Terraform:** https://developer.hashicorp.com/terraform
- **AWS CDK:** https://docs.aws.amazon.com/cdk
- **Pulumi:** https://www.pulumi.com/docs

### Security & Compliance
- **OWASP:** https://owasp.org
- **CIS Benchmarks:** https://www.cisecurity.org/cis-benchmarks
- **HashiCorp Vault:** https://developer.hashicorp.com/vault

### FinOps & Cost Optimization
- **FinOps Foundation:** https://www.finops.org
- **AWS Cost Optimization:** https://aws.amazon.com/pricing/cost-optimization
- **Kubecost:** https://www.kubecost.com

## Implementation Checklist

### AWS Lambda Deployment
- [ ] Install AWS CLI and SAM CLI
- [ ] Configure AWS credentials (access key, secret key)
- [ ] Create Lambda function with SAM template
- [ ] Configure IAM role and policies
- [ ] Test locally with `sam local invoke`
- [ ] Deploy with `sam deploy`
- [ ] Set up CloudWatch monitoring and alarms

### AWS EKS Kubernetes Cluster
- [ ] Install kubectl, eksctl, aws-cli
- [ ] Configure AWS credentials
- [ ] Create EKS cluster with eksctl
- [ ] Configure kubectl context
- [ ] Install cluster autoscaler
- [ ] Set up Helm for package management
- [ ] Deploy applications with kubectl/Helm
- [ ] Configure ingress controller (ALB/NGINX)

### Azure Deployment
- [ ] Install Azure CLI
- [ ] Login with `az login`
- [ ] Create resource group
- [ ] Deploy App Service or AKS
- [ ] Configure continuous deployment
- [ ] Set up monitoring with Application Insights

### Kubernetes on Any Cloud
- [ ] Install kubectl and helm
- [ ] Connect to cluster (update kubeconfig)
- [ ] Create namespaces for environments
- [ ] Apply RBAC policies
- [ ] Deploy applications (deployments, services)
- [ ] Configure ingress for external access
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Implement GitOps with ArgoCD/Flux

### CI/CD Pipeline (GitHub Actions)
- [ ] Create .github/workflows/deploy.yml
- [ ] Configure secrets (cloud credentials, API keys)
- [ ] Add build and test jobs
- [ ] Add container build and push to registry
- [ ] Add deployment job to cloud platform
- [ ] Set up branch protection rules
- [ ] Enable status checks and notifications

### FinOps Cost Optimization
- [ ] Implement resource tagging strategy
- [ ] Enable cost allocation tags
- [ ] Set up budget alerts
- [ ] Analyze resource utilization (CloudWatch, Azure Monitor)
- [ ] Identify rightsizing opportunities
- [ ] Purchase reserved instances for predictable workloads
- [ ] Configure auto-scaling and scheduling
- [ ] Regular cost reviews and optimization

### DevSecOps Security
- [ ] Add SAST scanning to CI/CD (SonarQube, Semgrep)
- [ ] Add dependency scanning (Snyk, Trivy)
- [ ] Implement container image scanning
- [ ] Set up secrets management (Vault, cloud provider)
- [ ] Configure security groups and network policies
- [ ] Enable audit logging
- [ ] Implement security monitoring and alerting
- [ ] Regular vulnerability assessments

### Cloudflare Workers
- [ ] Install Wrangler CLI
- [ ] Create Worker project
- [ ] Configure wrangler.toml (bindings, routes)
- [ ] Test locally with `wrangler dev`
- [ ] Deploy with `wrangler deploy`

### Docker
- [ ] Write Dockerfile with multi-stage builds
- [ ] Create .dockerignore file
- [ ] Test build locally
- [ ] Push to registry (ECR, ACR, GCR, Docker Hub)
- [ ] Deploy to target platform
