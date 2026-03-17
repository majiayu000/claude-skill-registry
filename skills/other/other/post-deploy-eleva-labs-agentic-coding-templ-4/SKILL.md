---
name: post-deploy
description: >-
  Infrastructure post-deployment validation and monitoring. TODO: Implement for devops.
  Invoked by: "/post-deploy", "verify deployment", "infra check", "validate infrastructure".
---

# Post-Deploy (DevOps)

**Status**: Stub - Not Implemented
**Domain**: DevOps

## Overview

DevOps-specific post-deployment skill for validating infrastructure changes, verifying cluster health, checking resource utilization, and ensuring proper service mesh configuration after deployments.

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| environment | Target environment | staging, production |
| --skip-k8s | Skip Kubernetes checks | --skip-k8s |
| --skip-metrics | Skip metrics verification | --skip-metrics |

## Usage Examples

```bash
# Run all post-deployment checks
/post-deploy production

# Infrastructure only, skip metrics
/post-deploy staging --skip-metrics

# Full production validation
/post-deploy production --verbose
```

## DevOps-Specific Checks

- Kubernetes cluster health (nodes, pods, deployments)
- Container resource utilization
- Service mesh health (Istio, Linkerd)
- Load balancer configuration
- SSL/TLS certificate validity
- DNS propagation verification
- Terraform state verification
- Infrastructure drift detection
- Secrets management verification
- Backup job verification

## TODO

- [ ] Define Kubernetes health check workflow
- [ ] Add Terraform state verification
- [ ] Define infrastructure drift detection
- [ ] Add service mesh validation
- [ ] Document SSL certificate checks
- [ ] Add resource utilization thresholds
- [ ] Define alerting verification steps

---

**End of Skill**
