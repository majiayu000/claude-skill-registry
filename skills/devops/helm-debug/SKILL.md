---
name: helm:debug
description: Debug Helm chart issues - template rendering, value overrides, hook failures
---

# Debug Helm Charts

## When to Use

- Helm install/upgrade fails
- Template rendering produces unexpected output
- Values not applied correctly
- Hook jobs failing

## Template Debugging

Render templates locally without installing:

```bash
helm template kagenti charts/kagenti -n kagenti-system -f charts/kagenti/.secrets.yaml
```

Render a specific template:

```bash
helm template kagenti charts/kagenti -n kagenti-system -s templates/ui-oauth-secret-job.yaml
```

Compare rendered output with what's deployed:

```bash
helm get manifest kagenti -n kagenti-system
```

## Value Debugging

Show computed values:

```bash
helm get values kagenti -n kagenti-system
```

Show all values (including defaults):

```bash
helm get values kagenti -n kagenti-system -a
```

Show chart default values:

```bash
helm show values charts/kagenti
```

## Release Debugging

Check release status:

```bash
helm status kagenti -n kagenti-system
```

Check release history:

```bash
helm history kagenti -n kagenti-system
```

## Hook Debugging

Hooks run as Jobs. Check their status:

```bash
kubectl get jobs -n kagenti-system
```

Check hook job logs:

```bash
kubectl logs -n kagenti-system job/<hook-job-name>
```

## Dependency Issues

Update chart dependencies:

```bash
helm dependency update charts/kagenti
```

List dependencies:

```bash
helm dependency list charts/kagenti
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `UPGRADE FAILED: another operation in progress` | Stale lock | `kubectl delete secret -n kagenti-system -l status=pending-upgrade` |
| Template render error | Bad YAML indent | Use `helm template` to see exact error |
| Values not applied | Wrong `-f` order | Later files override earlier ones |
| Hook timeout | Job takes too long | Check job logs, increase timeout |

## Related Skills

- `kagenti:deploy` - Platform deployment
- `kagenti:operator` - Operator management
- `k8s:pods` - Debug pod issues from hook jobs
- `rca:hypershift` - RCA when Helm issues cause test failures
- `rca:kind` - RCA on local Kind cluster
- `tdd:hypershift` - TDD loop that includes Helm reinstall iterations
- `tdd:kind` - TDD loop on Kind cluster
