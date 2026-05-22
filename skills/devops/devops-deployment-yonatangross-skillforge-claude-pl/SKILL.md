---
name: DevOps & Deployment
description: Use when setting up CI/CD pipelines, containerizing applications, deploying to Kubernetes, or writing infrastructure as code. DevOps & Deployment covers GitHub Actions, Docker, Helm, and Terraform patterns.
context: fork
agent: data-pipeline-engineer
version: 1.0.0
category: Infrastructure & Deployment
agents: [backend-system-architect, code-quality-reviewer, studio-coach]
keywords: [CI/CD, deployment, Docker, Kubernetes, pipeline, infrastructure, GitOps, container, automation, release]
author: SkillForge
user-invocable: false
---

# DevOps & Deployment Skill

Comprehensive frameworks for CI/CD pipelines, containerization, deployment strategies, and infrastructure automation.

## Overview

- Setting up CI/CD pipelines
- Containerizing applications
- Deploying to Kubernetes or cloud platforms
- Implementing GitOps workflows
- Managing infrastructure as code
- Planning release strategies

## Pipeline Architecture

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│    Code     │──>│    Build    │──>│    Test     │──>│   Deploy    │
│   Commit    │   │   & Lint    │   │   & Scan    │   │  & Release  │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
       │                 │                 │                 │
       v                 v                 v                 v
   Triggers         Artifacts          Reports          Monitoring
```

## Key Concepts

### CI/CD Pipeline Stages

1. **Lint & Type Check** - Code quality gates
2. **Unit Tests** - Test coverage with reporting
3. **Security Scan** - npm audit + Trivy vulnerability scanner
4. **Build & Push** - Docker image to container registry
5. **Deploy Staging** - Environment-gated deployment
6. **Deploy Production** - Manual approval or automated

### Container Best Practices

**Multi-stage builds** minimize image size:
- Stage 1: Install production dependencies only
- Stage 2: Build application with dev dependencies
- Stage 3: Production runtime with minimal footprint

**Security hardening**:
- Non-root user (uid 1001)
- Read-only filesystem where possible
- Health checks for orchestrator integration

### Kubernetes Deployment

**Essential manifests**:
- Deployment with rolling update strategy
- Service for internal routing
- Ingress for external access with TLS
- HorizontalPodAutoscaler for scaling

**Security context**:
- `runAsNonRoot: true`
- `allowPrivilegeEscalation: false`
- `readOnlyRootFilesystem: true`
- Drop all capabilities

### Deployment Strategies

| Strategy | Use Case | Risk |
|----------|----------|------|
| **Rolling** | Default, gradual replacement | Low - automatic rollback |
| **Blue-Green** | Instant switch, easy rollback | Medium - double resources |
| **Canary** | Progressive traffic shift | Low - gradual exposure |

**Rolling Update** (Kubernetes default):
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%
    maxUnavailable: 0  # Zero downtime
```

### Secrets Management

Use External Secrets Operator to sync from cloud providers:
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
- GCP Secret Manager

---

## References

### Docker Patterns
**See: `references/docker-patterns.md`**

Key topics covered:
- Multi-stage build examples with 78% size reduction
- Layer caching optimization
- Security hardening (non-root, health checks)
- Trivy vulnerability scanning
- Docker Compose development setup

### CI/CD Pipelines
**See: `references/ci-cd-pipelines.md`**

Key topics covered:
- Branch strategy (Git Flow)
- GitHub Actions caching (85% time savings)
- Artifact management
- Matrix testing
- Complete backend CI/CD example

### Kubernetes Basics
**See: `references/kubernetes-basics.md`**

Key topics covered:
- Health probes (startup, liveness, readiness)
- Security context configuration
- PodDisruptionBudget
- Resource quotas
- StatefulSets for databases
- Helm chart structure

### Environment Management
**See: `references/environment-management.md`**

Key topics covered:
- External Secrets Operator
- GitOps with ArgoCD
- Terraform patterns (remote state, modules)
- Zero-downtime database migrations
- Alembic migration workflow
- Rollback procedures

### Observability
**See: `references/observability.md`**

Key topics covered:
- Prometheus metrics exposition
- Grafana dashboard queries (PromQL)
- Alerting rules for SLOs
- Golden signals (SRE)
- Structured logging
- Distributed tracing (OpenTelemetry)

### Deployment Strategies
**See: `references/deployment-strategies.md`**

Key topics covered:
- Rolling deployment
- Blue-green deployment
- Canary releases
- Traffic splitting with Istio

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing in CI
- [ ] Security scans clean
- [ ] Database migrations ready
- [ ] Rollback plan documented

### During Deployment
- [ ] Monitor deployment progress
- [ ] Watch error rates
- [ ] Verify health checks passing

### Post-Deployment
- [ ] Verify metrics normal
- [ ] Check logs for errors
- [ ] Update status page

---

## Helm Chart Structure

```
charts/app/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── _helpers.tpl
└── values/
    ├── staging.yaml
    └── production.yaml
```

---

## Related Skills

- `zero-downtime-migration` - Database migration patterns for zero-downtime deployments
- `security-scanning` - Security scanning integration for CI/CD pipelines
- `observability-monitoring` - Monitoring and alerting for deployed applications
- `alembic-migrations` - Python/Alembic migration workflow for backend deployments

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Container user | Non-root (uid 1001) | Security best practice, required by many orchestrators |
| Deployment strategy | Rolling update (default) | Zero downtime, automatic rollback, resource efficient |
| Secrets management | External Secrets Operator | Syncs from cloud providers, GitOps compatible |
| Health checks | Separate startup/liveness/readiness | Prevents premature traffic, enables graceful shutdown |

---

## Extended Thinking Triggers

Use Opus 4.5 extended thinking for:
- **Architecture decisions** - Kubernetes vs serverless, multi-region setup
- **Migration planning** - Moving between cloud providers
- **Incident response** - Complex deployment failures
- **Security design** - Zero-trust architecture

---

## Templates Reference

| Template | Purpose |
|----------|---------|
| `github-actions-pipeline.yml` | Full CI/CD workflow with 6 stages |
| `Dockerfile` | Multi-stage Node.js build |
| `docker-compose.yml` | Development environment |
| `k8s-manifests.yaml` | Deployment, Service, Ingress |
| `helm-values.yaml` | Helm chart values |
| `terraform-aws.tf` | VPC, EKS, RDS infrastructure |
| `argocd-application.yaml` | GitOps application |
| `external-secrets.yaml` | Secrets Manager integration |

---

## Capability Details

### ci-cd
**Keywords:** ci, cd, pipeline, github actions, gitlab ci, jenkins, workflow
**Solves:**
- How do I set up CI/CD?
- GitHub Actions workflow patterns
- Pipeline caching strategies
- Matrix testing setup

### docker
**Keywords:** docker, dockerfile, container, image, build, compose, multi-stage
**Solves:**
- How do I containerize my app?
- Multi-stage Dockerfile best practices
- Docker Compose development setup
- Container security hardening

### kubernetes
**Keywords:** kubernetes, k8s, deployment, service, ingress, helm, statefulset, pdb
**Solves:**
- How do I deploy to Kubernetes?
- K8s health probes and resource limits
- Helm chart structure
- StatefulSet for databases

### infrastructure-as-code
**Keywords:** terraform, pulumi, iac, infrastructure, provision, gitops, argocd
**Solves:**
- How do I set up infrastructure as code?
- Terraform AWS patterns (VPC, EKS, RDS)
- GitOps with ArgoCD
- Secrets management patterns

### deployment-strategies
**Keywords:** blue green, canary, rolling, deployment strategy, rollback, zero downtime
**Solves:**
- Which deployment strategy should I use?
- Zero-downtime database migrations
- Blue-green deployment setup
- Canary release with traffic splitting

### observability
**Keywords:** prometheus, grafana, metrics, alerting, monitoring, health check
**Solves:**
- How do I add monitoring to my app?
- Prometheus metrics exposition
- Grafana dashboard queries
- Alerting rules for SLOs