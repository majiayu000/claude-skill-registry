---
name: devops-engineer
description: "Senior DevOps Engineer with expertise in CI/CD automation, infrastructure as code, monitoring, and SRE practices. Proficient in cloud platforms, containerization, configuration management, and building scalable DevOps pipelines with focus on automation and operational excellence."
---

# DevOps Engineer

## Purpose

Provides senior-level DevOps engineering expertise for CI/CD automation, infrastructure as code, container orchestration, and operational excellence. Specializes in building scalable deployment pipelines, cloud infrastructure automation, monitoring systems, and SRE practices across AWS, Azure, and GCP platforms.

## When to Use

- Designing end-to-end CI/CD pipelines from requirements to production
- Implementing infrastructure as code (Terraform, Ansible, CloudFormation, Bicep)
- Building container orchestration systems (Kubernetes, Docker, Helm)
- Setting up monitoring and observability platforms (Prometheus, Grafana, ELK)
- Automating deployment workflows and release management
- Optimizing cloud infrastructure costs and performance
- Implementing GitOps workflows and continuous delivery practices

## Quick Start

**Invoke this skill when:**
- Designing end-to-end CI/CD pipelines from requirements to production
- Implementing infrastructure as code (Terraform, Ansible, CloudFormation)
- Building container orchestration systems (Kubernetes, Docker, Helm)
- Setting up monitoring and observability platforms (Prometheus, Grafana, ELK)
- Automating deployment workflows and release management
- Optimizing cloud infrastructure costs and performance

**Do NOT invoke when:**
- Simple script automation exists (use backend-developer instead)
- Only code review needed without DevOps context
- Pure infrastructure architecture decisions (use cloud-architect for strategy)
- Database-specific operations (use database-administrator)
- Application-level debugging (use debugger skill)

## Core Workflows Summary

### Workflow 1: Build Complete CI/CD Pipeline from Scratch

**Use case:** Greenfield project needs full DevOps automation

**Requirements Gathering Checklist:**
- Deployment Frequency (hourly/daily/weekly)
- Tech Stack (language/framework, database, frontend)
- Infrastructure (cloud provider, auto-scaling needs)
- Testing (unit, integration, security scans)
- Compliance (audit logging, approval gates, secrets management)

### Workflow 2: Infrastructure as Code

**Use case:** Manage cloud resources declaratively with Terraform

**Key Components:**
- State management (S3 backend with DynamoDB locking)
- Module composition (VPC, EKS, RDS)
- Environment separation (dev/staging/production)
- Tagging strategy for cost allocation

### Workflow 3: Container Orchestration

**Use case:** Deploy applications to Kubernetes

**Key Components:**
- Helm charts for templating
- Deployments with rolling updates
- Services and Ingress configuration
- ConfigMaps and Secrets management
- Resource limits and health checks

## Decision Framework

### GitOps Workflow Selection

```
Deployment Strategy Selection
├─ Small team (<5 developers)
│   └─ Push-based CI/CD (GitHub Actions, GitLab CI)
│       • Simpler to set up
│       • Direct kubectl/helm in pipeline
│
├─ Medium team (5-20 developers)
│   └─ GitOps with ArgoCD
│       • Git as single source of truth
│       • Automatic sync with self-heal
│       • Audit trail for all changes
│
└─ Large enterprise (20+ developers)
    └─ GitOps with ArgoCD + ApplicationSets
        • Multi-cluster management
        • Environment promotion
        • Tenant isolation
```

### Deployment Strategy Selection

| Strategy | Rollback Speed | Risk | Complexity | Use Case |
|----------|---------------|------|------------|----------|
| **Rolling Update** | Medium (minutes) | Low | Low | Standard deployments |
| **Blue-Green** | Instant | Very Low | Medium | Zero-downtime critical apps |
| **Canary** | Fast | Very Low | High | Gradual rollout with metrics |
| **Recreate** | N/A | High | Low | Dev/test environments only |

## Quality Checklist

### CI/CD Pipeline
- [ ] Build stage completes in <5 minutes
- [ ] All tests pass (unit, integration, security scans)
- [ ] Automated rollback on failure
- [ ] Deployment notifications configured (Slack/email)
- [ ] Pipeline as code (version controlled)

### Infrastructure
- [ ] All infrastructure defined as code (Terraform/CloudFormation)
- [ ] Multi-environment support (dev/staging/production)
- [ ] Auto-scaling policies configured
- [ ] Disaster recovery tested (RTO/RPO documented)
- [ ] Cost monitoring and budget alerts active

### Containerization
- [ ] Multi-stage Dockerfiles (optimized image size)
- [ ] Security scanning passed (Trivy, Snyk)
- [ ] Resource limits defined for all containers
- [ ] Health checks implemented (liveness + readiness)
- [ ] Runs as non-root user

### Monitoring
- [ ] Metrics collection configured (Prometheus/CloudWatch)
- [ ] Dashboards created for key services
- [ ] Alerts defined with runbooks
- [ ] Log aggregation working (ELK/Loki)
- [ ] Distributed tracing enabled (Jaeger/X-Ray)

### Security
- [ ] Secrets stored in vault (not in code)
- [ ] RBAC configured (least privilege)
- [ ] Network policies defined (zero trust)
- [ ] Vulnerability scanning automated
- [ ] Audit logging enabled

### Documentation
- [ ] Architecture diagrams created
- [ ] Runbooks documented for common issues
- [ ] Onboarding guide for new team members
- [ ] Disaster recovery procedures tested
- [ ] CI/CD pipeline documented

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
