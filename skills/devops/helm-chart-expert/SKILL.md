---
name: helm-chart-expert
description: Production-ready Helm chart creation and review guide. Covers chart structure, ArgoCD/GitOps integration, secrets management, testing strategies, deployment patterns (blue-green, canary), monitoring, and troubleshooting. Use when creating charts, reviewing for security/quality, integrating with ArgoCD, or debugging chart issues.
version: 2.0.0
---

# Helm Chart Expert Skill

## Purpose

Guide for creating production-ready Helm charts and conducting comprehensive chart reviews. Core workflow covers essential patterns with references to detailed examples for complex scenarios.

## Quick Start Checklist

### New Chart Creation

```bash
# 1. Create chart structure
helm create mychart

# 2. Validate structure
helm lint ./mychart

# 3. Test rendering
helm template ./mychart --debug

# 4. Dry run
helm install test ./mychart --dry-run --debug
```

### Quick Template Check

```bash
# Render without installing
helm template myrelease ./mychart -f values-dev.yaml

# Debug with values
helm install myrelease ./mychart --dry-run --debug

# Diff before upgrade (requires helm-diff plugin)
helm diff upgrade myrelease ./mychart
```

## When to Load Additional References

The quick reference above covers essential chart creation patterns. Load detailed references when:

**For detailed chart templates and examples:**

```
Read `~/.claude/skills/helm-chart-expert/references/TEMPLATES.md`
```

Use when: Creating new charts, need Chart.yaml/values.yaml/deployment examples, implementing all Kubernetes resources

**For ArgoCD integration patterns:**

```
Read `~/.claude/skills/helm-chart-expert/references/ARGOCD-PATTERNS.md`
```

Use when: Integrating with ArgoCD, multi-environment deployments, ApplicationSets, sync waves, GitOps workflows

**For production deployment patterns:**

```
Read `~/.claude/skills/helm-chart-expert/references/PRODUCTION-PATTERNS.md`
```

Use when: Secrets management, testing strategies, blue-green/canary deployments, monitoring setup, upgrade strategies

**For troubleshooting and advanced techniques:**

```
Read `~/.claude/skills/helm-chart-expert/references/TROUBLESHOOTING.md`
```

Use when: Debugging chart issues, nil pointer errors, advanced templating, dynamic resource generation, performance optimization

---

## Chart Review Checklist

### Security Review

- [ ] **No hardcoded secrets** in values.yaml or templates
- [ ] **Image tags are specific** (no `latest`)
- [ ] **Security contexts** are defined and restrictive
- [ ] **RBAC is properly configured** with least privilege
- [ ] **Network policies** are defined where applicable
- [ ] **Pod Security Standards** are enforced
- [ ] **Resource limits** are set for all containers

### Structure Review

- [ ] **Chart.yaml** has all required fields
- [ ] **Version follows SemVer2** format
- [ ] **Dependencies** use version ranges (~)
- [ ] **One resource per file** in templates/
- [ ] **Template helpers** are properly namespaced
- [ ] **File naming** follows conventions (lowercase, dashes)

### Values Review

- [ ] **All values are documented** with clear comments
- [ ] **Naming is consistent** (camelCase)
- [ ] **Types are explicit** (strings are quoted)
- [ ] **Flat structure** preferred where possible
- [ ] **Defaults are secure** and production-ready
- [ ] **Environment-specific values** are separated

### Template Review

- [ ] **Labels are consistent** and follow k8s recommendations
- [ ] **Nil checks** for nested values
- [ ] **Whitespace is properly managed** ({{- and -}})
- [ ] **Helper functions** are used for repeated logic
- [ ] **Conditionals** are properly structured
- [ ] **Resources can be disabled** via values

### Testing Review

- [ ] **helm lint** passes without errors
- [ ] **helm template** renders correctly
- [ ] **Dry run** succeeds
- [ ] **Unit tests** exist and pass
- [ ] **Integration tests** for critical paths
- [ ] **Helm test** hooks are defined

### Documentation Review

- [ ] **README.md** exists with usage examples
- [ ] **CHANGELOG.md** tracks versions
- [ ] **values.yaml** is fully documented
- [ ] **Examples** for common scenarios
- [ ] **Upgrade notes** for breaking changes
- [ ] **Dependencies** are documented

---

## Final Review Checklist

### Before Release

- [ ] All tests pass (lint, unit, integration)
- [ ] Security scanning completed
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped appropriately
- [ ] Tested in staging environment
- [ ] Rollback procedure documented
- [ ] Resource quotas validated
- [ ] Network policies tested
- [ ] Monitoring/alerting configured

### After Release

- [ ] Smoke tests pass
- [ ] Metrics flowing
- [ ] Logs accessible
- [ ] Alerts configured
- [ ] Documentation published
- [ ] Team notified

## Integration with Other Skills

### Works With:

- **security-scan** - Scan rendered Helm templates for hardcoded secrets
- **quality-check** - Lint YAML files for formatting issues
- Manual invocation for Helm-specific work

### Invokes:

- None (standalone reference skill)

### Invoked By:

- User (manual invocation when working with Helm)

## Example Usage

```bash
# Manual invocation
/skill helm-chart-expert

# User requests
User: "Help me create a production-ready Helm chart"
User: "Review this Helm chart for security issues"
User: "Show me how to integrate with ArgoCD"
User: "How do I handle secrets in Helm?"
```

## References

- [Official Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Kubernetes Labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/)
- [SemVer 2.0](https://semver.org)
- [Helm Security](https://helm.sh/docs/topics/security/)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [GitOps Principles](https://opengitops.dev/)

---

**Maintained by**: DevOps team
**Review Schedule**: Quarterly
**Last Updated**: 2025-01-12

---

## Related Agent

For comprehensive Helm/Kubernetes guidance that coordinates this and other Helm skills, use the **`helm-kubernetes-expert`** agent.
