---
name: helm-chart-patterns
description: Helm chart development patterns for packaging and deploying Kubernetes applications. Use when creating reusable Helm charts, managing multi-environment deployments, or building application catalogs for Kubernetes.
---

# Helm Chart Patterns

Expert guidance for developing production-grade Helm charts covering chart structure, templating patterns, multi-environment configuration, dependency management, testing strategies, and distribution workflows for Kubernetes application packaging.

## When to Use This Skill

- Creating reusable Helm charts for applications and services
- Building application catalogs and chart repositories
- Managing multi-environment deployments (dev, staging, production)
- Implementing advanced templating with conditionals and loops
- Managing chart dependencies and subcharts
- Implementing chart hooks for lifecycle management
- Testing and validating chart templates
- Packaging and distributing charts via repositories
- Using Helmfile for multi-chart orchestration

## Core Concepts

### Chart Types
- **Application charts**: Standard deployable charts for your services
- **Library charts**: Reusable template helpers (not directly installable)

### Key Files
| File | Purpose |
|------|---------|
| `Chart.yaml` | Metadata, version, dependencies |
| `values.yaml` | Default configuration |
| `values.schema.json` | Input validation |
| `templates/_helpers.tpl` | Reusable template functions |
| `templates/*.yaml` | Kubernetes manifests |

### Template Essentials
- **Quote strings**: `{{ .Values.name | quote }}`
- **Indent properly**: `{{- toYaml . | nindent 4 }}`
- **Use helpers**: `{{ include "my-app.fullname" . }}`
- **Check nil**: `{{- if .Values.optional }}`

## Quick Reference

| Task | Load reference |
| --- | --- |
| Chart structure & Chart.yaml | `skills/helm-chart-patterns/references/chart-structure.md` |
| Values file patterns | `skills/helm-chart-patterns/references/values-patterns.md` |
| Template patterns & functions | `skills/helm-chart-patterns/references/template-patterns.md` |
| Dependencies & subcharts | `skills/helm-chart-patterns/references/dependencies.md` |
| Hooks & lifecycle | `skills/helm-chart-patterns/references/hooks.md` |
| Testing patterns | `skills/helm-chart-patterns/references/testing.md` |
| Packaging & distribution | `skills/helm-chart-patterns/references/packaging.md` |
| Helmfile multi-chart | `skills/helm-chart-patterns/references/helmfile.md` |
| Best practices checklist | `skills/helm-chart-patterns/references/best-practices.md` |

## Workflow

1. **Structure** - Set up chart directory with Chart.yaml and values.yaml
2. **Template** - Create Kubernetes manifests with Go templating
3. **Helpers** - Extract common patterns into _helpers.tpl
4. **Validate** - Use values.schema.json for input validation
5. **Test** - Lint, template, and run chart tests
6. **Package** - Create .tgz and publish to repository

## Essential Commands

```bash
# Development
helm create my-app          # Scaffold new chart
helm lint ./my-app          # Validate chart
helm template my-app ./my-app  # Render templates

# Dependencies
helm dependency update      # Download dependencies
helm dependency list        # Show dependencies

# Testing
helm install my-app ./my-app --dry-run --debug
helm test my-app

# Distribution
helm package ./my-app
helm repo index . --url https://charts.example.com
helm push my-app-1.0.0.tgz oci://registry.example.com/charts
```

## Common Mistakes

- Forgetting to quote strings in templates
- Not using `nindent` for proper YAML formatting
- Committing secrets to values files
- Missing security contexts (runAsNonRoot, drop capabilities)
- Not pinning dependency versions
- Skipping values.schema.json validation
- Not testing upgrades from previous versions

## Resources

- **Helm Documentation**: https://helm.sh/docs/
- **Chart Template Guide**: https://helm.sh/docs/chart_template_guide/
- **Best Practices**: https://helm.sh/docs/chart_best_practices/
- **Helmfile**: https://github.com/helmfile/helmfile
- **Chart Testing**: https://github.com/helm/chart-testing
