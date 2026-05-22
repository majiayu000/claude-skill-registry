---
name: cicd-patterns
description: "CI/CD pipeline patterns for GitHub Actions including deployment strategies and pipeline security. Use when designing pipelines, deployment strategies, or writing workflow YAML. Do NOT use for Infrastructure as Code (Terraform, CDK, CloudFormation) -- use cdk-patterns instead. Do NOT use for Git Flow or multi-branch release workflows."
durability: encoded-preference
---

# CI/CD Pipeline Patterns

Principles for CI/CD pipeline design. Assumes trunk-based development (single main branch, no Git Flow).

## Pipeline Stage Ordering

Security scanning runs BEFORE tests and builds. A vulnerability found after a 20-minute test suite wastes CI minutes.

```
checkout -> security-scan -> test -> build -> deploy -> verify
```

### Security Scanning Order

Run scans in order of speed and severity impact:

1. **SAST (Static Analysis)** -- Fastest, catches code-level vulnerabilities
2. **Secrets scanning** -- Prevents credential leaks before they reach remote
3. **Dependency scanning** -- Identifies known CVEs in dependencies
4. **Container scanning** -- Scans built images for OS-level vulnerabilities (runs after build stage)

For security scanning tool details, see security-patterns skill.

### GitHub Actions Patterns

#### Trunk-Based Pipeline Structure

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    # Runs first, no dependencies
  test:
    needs: security-scan
  build:
    needs: test
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'  # Deploy only from main
```

#### Key Principles

- **Pin action versions by SHA**, not tag (e.g., `actions/checkout@<sha>` not `@v4`). Tags are mutable.
- **Minimize secret exposure**: Use `environment` protection rules. Restrict deploy secrets to the deploy job only.
- **Cache dependencies** between jobs to reduce build time (actions/cache or setup-* cache options).
- **Fail the pipeline on audit warnings** for production branches. Use `--audit-level high` or equivalent.

## Deployment Strategies

### Decision Heuristic

| Strategy | When to use | Trade-off |
|----------|-------------|-----------|
| **Rolling** | Stateless services, high replica count, tolerance for mixed versions | Simplest. Temporary version inconsistency during rollout. |
| **Blue-Green** | Stateful services, need instant rollback, zero mixed-version tolerance | Full duplicate environment cost. Instant rollback by traffic switch. |
| **Canary** | High-traffic services, need gradual risk validation, metrics-driven decisions | Most complex. Requires good observability to evaluate canary health. |

For zero-downtime database migrations during deployments, see database-patterns skill.

## Anti-Patterns

| Anti-Pattern | Why it fails | Correct approach |
|-------------|-------------|------------------|
| Running security scans after build | Wastes CI minutes on vulnerable code | Security scan as first pipeline stage |
| Mutable action version tags (`@v4`) | Supply chain risk -- tag can be moved to malicious commit | Pin by SHA |
| Destructive DB migration + code change in one deploy | Old instances crash when column disappears | Two-phase migration (see database-patterns) |
| Manual rollback only | MTTR measured in human response time, not seconds | Automated rollback with metric thresholds |
| Deploying from feature branches | Bypasses trunk integration testing | Deploy only from main branch |
