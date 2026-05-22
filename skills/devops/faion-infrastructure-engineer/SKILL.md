---
name: faion-infrastructure-engineer
description: "Infrastructure: Docker, Kubernetes, Terraform, AWS/GCP, IaC, containerization."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Infrastructure Engineer Sub-Skill

**Communication: User's language. Config/code: English.**

## Purpose

Manages infrastructure provisioning, containerization, orchestration, and cloud platforms. Covers Docker, Kubernetes, Terraform, AWS, GCP, and IaC patterns.

---

## Context Discovery

### Auto-Investigation

Detect existing infrastructure from project:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| Dockerfile | `Glob("**/Dockerfile")` or `Glob("**/.dockerfile")` | Docker containerization |
| docker-compose | `Glob("**/docker-compose*.yml")` | Multi-container local dev |
| K8s manifests | `Glob("**/k8s/**/*.yaml")` or `Glob("**/kubernetes/*")` | Kubernetes deployment |
| Helm charts | `Glob("**/charts/*")` or `Glob("**/Chart.yaml")` | Helm package management |
| Terraform | `Glob("**/*.tf")` or `Glob("**/terraform/*")` | IaC with Terraform |
| AWS config | `Grep("aws_", "**/*.tf")` or `Glob("**/.aws/*")` | AWS infrastructure |
| GCP config | `Grep("google_", "**/*.tf")` or `Glob("**/.gcp/*")` | GCP infrastructure |
| Cloud init | `Glob("**/cloud-init*.yaml")` | VM provisioning |

**Read existing infrastructure:**
- docker-compose.yml for service architecture
- Kubernetes manifests for deployment patterns
- Terraform files for cloud resources
- README for infrastructure setup instructions

### Discovery Questions

#### Q1: Infrastructure Layer

```yaml
question: "What infrastructure layer do you need help with?"
header: "Focus"
multiSelect: false
options:
  - label: "Containerization (Docker)"
    description: "Dockerfile, image optimization, local development"
  - label: "Orchestration (Kubernetes, Helm)"
    description: "K8s deployments, services, scaling, Helm charts"
  - label: "Infrastructure as Code (Terraform)"
    description: "Cloud provisioning, modules, state management"
  - label: "Cloud platform (AWS or GCP)"
    description: "Compute, storage, networking, managed services"
```

#### Q2: Deployment Stage

```yaml
question: "What stage is your infrastructure at?"
header: "Maturity"
multiSelect: false
options:
  - label: "Local dev only (docker-compose)"
    description: "Need to containerize or improve local setup"
  - label: "Manual deployment (no automation)"
    description: "Need IaC or orchestration"
  - label: "Basic K8s or cloud (needs optimization)"
    description: "Running but needs scaling, monitoring, cost optimization"
  - label: "Multi-environment (staging, prod)"
    description: "Need consistency, GitOps, or advanced patterns"
```

#### Q3: Cloud Provider

```yaml
question: "Which cloud provider are you using?"
header: "Platform"
multiSelect: false
options:
  - label: "AWS"
    description: "EC2, ECS, Lambda, S3, networking"
  - label: "GCP"
    description: "GKE, Cloud Run, Compute, storage"
  - label: "Multi-cloud or cloud-agnostic"
    description: "Need portable IaC with Terraform"
  - label: "On-premise or bare metal"
    description: "Self-hosted Kubernetes or VMs"
```

---

## Quick Decision Tree

| If you need... | Use | File |
|---------------|-----|------|
| **Containerization** |
| Single service Dockerfile | docker-containerization | docker-containerization.md |
| Multi-service local dev | docker-compose | docker-compose.md |
| Dockerfile patterns | dockerfile-patterns | dockerfile-patterns.md |
| **Kubernetes** |
| K8s basics | k8s-basics | k8s-basics.md |
| K8s resources | k8s-resources | k8s-resources.md |
| K8s deployment | kubernetes-deployment | kubernetes-deployment.md |
| Helm charts | helm-basics, helm-advanced | helm-basics.md |
| **Infrastructure as Code** |
| Terraform basics | terraform-basics | terraform-basics.md |
| Terraform modules | terraform-modules | terraform-modules.md |
| Terraform state | terraform-state | terraform-state.md |
| IaC patterns | iac-basics, iac-patterns | iac-basics.md |
| **AWS** |
| AWS foundations | aws-architecture-foundations | aws-architecture-foundations.md |
| AWS services | aws-architecture-services | aws-architecture-services.md |
| EC2/ECS | aws-ec2-ecs | aws-ec2-ecs.md |
| Lambda | aws-lambda | aws-lambda.md |
| S3/Storage | aws-s3-storage | aws-s3-storage.md |
| Networking | aws-networking | aws-networking.md |
| **GCP** |
| GCP basics | gcp-arch-basics | gcp-arch-basics.md |
| GCP patterns | gcp-arch-patterns | gcp-arch-patterns.md |
| Compute/GKE | gcp-compute | gcp-compute.md |
| Cloud Run | gcp-cloud-run | gcp-cloud-run.md |
| Storage | gcp-storage | gcp-storage.md |
| Networking | gcp-networking | gcp-networking.md |

---

## Methodologies (30)

### Docker (6)
- docker-basics
- docker-compose
- docker-containerization
- dockerfile-patterns
- docker (reference)

### Kubernetes (6)
- k8s-basics
- k8s-resources
- kubernetes-deployment
- helm-basics
- helm-advanced

### Terraform & IaC (6)
- terraform-basics
- terraform-modules
- terraform-state
- terraform (reference)
- iac-basics
- iac-patterns

### AWS (7)
- aws (reference)
- aws-architecture-foundations
- aws-architecture-services
- aws-ec2-ecs
- aws-lambda
- aws-s3-storage
- aws-networking

### GCP (6)
- gcp (reference)
- gcp-arch-basics
- gcp-arch-patterns
- gcp-compute
- gcp-cloud-run
- gcp-storage
- gcp-networking

---

## Common Workflows

### Container Deployment
```
1. Write Dockerfile
2. Build and test locally
3. Push to registry
4. Update K8s manifests
5. Apply to cluster
6. Verify deployment
```

### Infrastructure Provisioning
```
1. Create feature branch
2. Write Terraform code
3. Run terraform plan
4. Review plan output
5. Create PR
6. Apply after approval
7. Verify resources
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-devops-engineer | Parent skill |
| faion-cicd-engineer | Sibling (CI/CD and monitoring) |

---

*Infrastructure Engineer Sub-Skill v1.0*
*30 Methodologies | Docker, K8s, Terraform, AWS, GCP*
