---
name: faion-devops-engineer
description: "DevOps Engineer role: Docker, Kubernetes, Terraform, AWS/GCP/Azure, CI/CD (GitHub Actions, GitLab CI), infrastructure as code, monitoring (Prometheus, Grafana), logging, secrets management, nginx, load balancing."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---

# DevOps Domain Skill

**Communication: User's language. Config/code: English.**

## Purpose

Orchestrates infrastructure and deployment activities. Covers containerization, orchestration, infrastructure as code, cloud services, and CI/CD pipelines.

---

## Agents

| Agent | Purpose |
|-------|---------|
| faion-devops-agent | Infrastructure and deployment automation |

---

## References

Detailed technical context for each area:

| Reference | Content | Lines |
|-----------|---------|-------|
| [docker.md](references/docker.md) | Containers, Compose, multi-stage builds | ~1140 |
| [kubernetes.md](references/kubernetes.md) | K8s resources, Helm, operators | ~960 |
| [terraform.md](references/terraform.md) | IaC, modules, state management | ~1090 |
| [aws.md](references/aws.md) | AWS CLI, services, IAM, networking | ~1480 |

**Total:** ~4,670 lines of technical reference

---

## Quick Reference

### Tool Selection

| Tool | Use Case |
|------|----------|
| **Docker** | Containerization, local dev, CI builds |
| **Kubernetes** | Container orchestration, scaling |
| **Terraform** | Multi-cloud IaC, infrastructure provisioning |
| **Pulumi** | IaC with programming languages |
| **Ansible** | Configuration management, server setup |

### Cloud Provider Selection

| Provider | Strengths |
|----------|-----------|
| **AWS** | Most services, enterprise, mature |
| **GCP** | Kubernetes, ML, BigQuery |
| **Azure** | Microsoft ecosystem, hybrid |
| **Hetzner** | Cost-effective, EU data residency |
| **DigitalOcean** | Simple, developer-friendly |

### CI/CD Tools

| Tool | Best For |
|------|----------|
| **GitHub Actions** | GitHub repos, simple pipelines |
| **GitLab CI** | GitLab repos, full DevOps platform |
| **Jenkins** | Complex pipelines, self-hosted |
| **ArgoCD** | GitOps, Kubernetes deployments |

---

## Methodologies (16)

### Docker (M-DOC-*)

| ID | Name | Purpose |
|----|------|---------|
| M-DOC-001 | Multi-stage Builds | Smaller production images |
| M-DOC-002 | Docker Compose | Multi-container local dev |
| M-DOC-003 | Security Scanning | Vulnerability detection |
| M-DOC-004 | Layer Optimization | Build cache efficiency |

### Kubernetes (M-K8S-*)

| ID | Name | Purpose |
|----|------|---------|
| M-K8S-001 | Resource Management | Requests, limits, QoS |
| M-K8S-002 | Helm Charts | Package management |
| M-K8S-003 | ConfigMaps & Secrets | Configuration management |
| M-K8S-004 | Ingress & Networking | Traffic routing |

### Terraform (M-TF-*)

| ID | Name | Purpose |
|----|------|---------|
| M-TF-001 | Module Design | Reusable infrastructure |
| M-TF-002 | State Management | Remote state, locking |
| M-TF-003 | Workspaces | Environment separation |
| M-TF-004 | Testing | Terratest, plan validation |

### AWS (M-AWS-*)

| ID | Name | Purpose |
|----|------|---------|
| M-AWS-001 | IAM Best Practices | Least privilege, roles |
| M-AWS-002 | VPC Design | Networking, security groups |
| M-AWS-003 | Cost Optimization | Reserved, spot, rightsizing |
| M-AWS-004 | Disaster Recovery | Backup, multi-region |

---

## Workflows

### Container Deployment

```
1. Write Dockerfile
2. Build and test locally
3. Push to registry
4. Update K8s manifests
5. Apply to cluster
6. Verify deployment
7. Monitor logs/metrics
```

### Infrastructure Change

```
1. Create feature branch
2. Write Terraform code
3. Run `terraform plan`
4. Review plan output
5. Create PR
6. Apply after approval
7. Verify resources
```

### CI/CD Pipeline

```yaml
# GitHub Actions example
name: Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push
        run: |
          docker build -t app:${{ github.sha }} .
          docker push registry/app:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to K8s
        run: |
          kubectl set image deployment/app \
            app=registry/app:${{ github.sha }}
```

---

## Common Commands

### Docker

```bash
# Build image
docker build -t app:latest .

# Run container
docker run -d -p 8080:80 app:latest

# View logs
docker logs -f container_id

# Compose up
docker compose up -d

# Clean up
docker system prune -af
```

### Kubernetes

```bash
# Apply manifests
kubectl apply -f deployment.yaml

# Get resources
kubectl get pods,svc,deploy

# View logs
kubectl logs -f pod/app-xxx

# Port forward
kubectl port-forward svc/app 8080:80

# Scale
kubectl scale deploy/app --replicas=3
```

### Terraform

```bash
# Initialize
terraform init

# Plan
terraform plan -out=tfplan

# Apply
terraform apply tfplan

# Destroy
terraform destroy

# State list
terraform state list
```

### AWS CLI

```bash
# Configure
aws configure

# S3
aws s3 sync ./dist s3://bucket/

# ECR login
aws ecr get-login-password | docker login --username AWS --password-stdin xxx.ecr.region.amazonaws.com

# Lambda invoke
aws lambda invoke --function-name func output.json
```

---

## Security Checklist

### Container Security

- [ ] Non-root user in Dockerfile
- [ ] Minimal base image (distroless, alpine)
- [ ] No secrets in image
- [ ] Image scanning enabled
- [ ] Read-only root filesystem

### Kubernetes Security

- [ ] RBAC configured
- [ ] Network policies defined
- [ ] Pod security standards
- [ ] Secrets encrypted at rest
- [ ] Resource limits set

### Infrastructure Security

- [ ] Least privilege IAM
- [ ] Private subnets for workloads
- [ ] Security groups restrictive
- [ ] Encryption enabled
- [ ] Logging to central system

---

## Monitoring Stack

### Observability Triad

| Pillar | Tools |
|--------|-------|
| **Metrics** | Prometheus, Grafana, CloudWatch |
| **Logs** | Loki, ELK, CloudWatch Logs |
| **Traces** | Jaeger, Tempo, X-Ray |

### Alerting

```yaml
# Prometheus alert example
groups:
  - name: app
    rules:
      - alert: HighErrorRate
        expr: |
          rate(http_requests_total{status=~"5.."}[5m])
          / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| faion-developer-domain-skill | Application code to deploy |
| faion-ml-domain-skill | ML model deployment |

---

## Error Handling

| Issue | Action |
|-------|--------|
| Unknown cloud provider | Ask user or check existing config |
| Complex infrastructure | Read references/ for patterns |
| Multi-cloud setup | Combine relevant references |

---

*DevOps Domain Skill v1.0*
*4 Reference Files | 16 Methodologies*
*Aggregated from: docker, kubernetes, terraform, aws*
