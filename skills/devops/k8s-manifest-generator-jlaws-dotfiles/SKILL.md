---
name: k8s-manifest-generator
description: Kubernetes manifest patterns, resource configuration opinions, and configuration validation. Use when generating K8s YAML, creating Helm charts, packaging K8s applications, or validating configs across environments.
---

# Kubernetes Manifest Generator

## Workflow

1. Gather requirements (stateless/stateful, ports, storage, scaling, health endpoints)
2. Create Deployment/StatefulSet
3. Create Service (ClusterIP/LoadBalancer/NodePort)
4. Add ConfigMap and/or Secret
5. Add PVC if stateful
6. Apply security context
7. Add standard labels
8. Validate with `kubectl apply --dry-run=server`

## Resource Limit Opinions

### CPU and Memory
| Workload Type | Requests | Limits |
|---------------|----------|--------|
| API server | 250m / 256Mi | 500m / 512Mi |
| Worker/queue consumer | 500m / 512Mi | 1000m / 1Gi |
| Batch job | 1000m / 1Gi | 2000m / 2Gi |
| Sidecar (envoy, etc.) | 100m / 128Mi | 200m / 256Mi |

**Rules:**
- Always set requests. Limits are optional but recommended for memory.
- CPU limits are controversial -- they cause throttling. Omit CPU limits for latency-sensitive services; use only requests.
- Memory limits should be 1.5-2x requests. OOMKill is worse than throttling.
- Never set requests = limits unless you want Guaranteed QoS (rare).

### Startup vs Liveness vs Readiness
- **startupProbe**: Slow-starting apps (JVM, ML models). `failureThreshold * periodSeconds` = max startup time.
- **livenessProbe**: Detect deadlocks. Conservative: `failureThreshold: 3`, `periodSeconds: 10`. Don't check dependencies.
- **readinessProbe**: Gate traffic. Check app health + critical dependencies. `periodSeconds: 5`.

**Common mistake**: Liveness probe checks database connectivity -> DB blip restarts all pods -> cascading failure.

## Security Context (Always Apply)

```yaml
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: [ALL]
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}
```

- `readOnlyRootFilesystem: true` requires `/tmp` emptyDir mount for apps that write temp files
- Drop ALL capabilities, add back only what's needed (almost never)

## Labels (Use Standard K8s Labels)

```yaml
app.kubernetes.io/name: <app>
app.kubernetes.io/version: "<version>"
app.kubernetes.io/component: backend|frontend|worker
app.kubernetes.io/part-of: <system>
app.kubernetes.io/managed-by: helm|kustomize|kubectl
```

## Service Selection

| Type | When |
|------|------|
| `ClusterIP` | Internal services (default) |
| `LoadBalancer` | External-facing, cloud provider LB |
| `NodePort` | Development only, never production |
| `ClusterIP: None` (headless) | StatefulSets needing stable DNS |

## Secret Management
- Never commit plaintext secrets to Git
- Use: External Secrets Operator (AWS SM/Vault), Sealed Secrets, or SOPS
- `stringData` in manifests is for local dev only

## Manifest Organization

**Kustomize** (default choice):
```
base/            # Shared manifests
overlays/
  dev/           # Dev overrides (replica count, resource limits)
  prod/          # Prod overrides
```

**Helm** (when you need templating + packaging):
- Use `values.schema.json` to validate inputs
- Template helpers in `_helpers.tpl` -- keep DRY
- Always support `resources`, `nodeSelector`, `tolerations`, `affinity` in values
- Use `helm template --dry-run --debug` to verify before install

### Helm Anti-Patterns
- Overly complex templates with deeply nested conditionals
- Not pinning chart dependencies to exact versions
- Using `helm install` without `--atomic` (leaves partial deploys)
- Storing secrets in values files

## Configuration Validation

### Schema Validation Opinions
- **Always validate with JSON Schema** -- use `values.schema.json` for Helm, JSON Schema for app configs
- Use `allErrors: true` to surface all issues at once, not fail on first
- Add custom formats for domain types: `port` (1-65535), `duration` (`\d+[smhd]`), `url-https`
- Schema files are code -- version them, review them, test them

### Environment-Specific Rules

| Rule | Dev | Staging | Prod |
|------|-----|---------|------|
| Debug mode allowed | Yes | No | No |
| HTTPS required | No | Yes | Yes |
| Min replicas | 1 | 2 | 3 |
| Resource limits required | No | Yes | Yes |
| Secret encryption required | No | No | Yes |

**Enforce in CI**: validate configs against environment-specific rulesets before merge. Treat violations as blocking.

### Config Validation Gotchas
- **Drift between environments**: Use overlays/values files per env, never manual edits. Diff configs across envs in CI.
- **Hot-reload pitfalls**: Validate new config before applying. If validation fails in prod, keep current config and alert -- never crash.
- **Config migration**: Version your config schema. When schema changes, write explicit up/down migrations. Never silently ignore unknown fields.
- **Sensitive values**: Validate that secrets are references (ESO, Vault paths), not plaintext. Regex-scan values files for high-entropy strings.

## Validation Pipeline

```bash
kubectl apply -f manifest.yaml --dry-run=server  # API server validation
kube-linter lint manifest.yaml                     # Best practices
kube-score score manifest.yaml                     # Security scoring
```

Run all three in CI before merge.
