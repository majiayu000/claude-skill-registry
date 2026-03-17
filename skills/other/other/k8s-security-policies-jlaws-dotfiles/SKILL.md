---
name: k8s-security-policies
description: Kubernetes security policy patterns including NetworkPolicy, RBAC, Pod Security Standards, and OPA Gatekeeper. Use when securing clusters, implementing network isolation, or enforcing pod security.
---

# Kubernetes Security Policies

## Pod Security Standards

Apply via namespace labels. Three tiers:

| Level | Use Case | Key Restrictions |
|-------|----------|-----------------|
| `privileged` | System workloads (CNI, monitoring agents) | None |
| `baseline` | Most workloads | No hostNetwork, no privileged containers, no hostPath |
| `restricted` | Sensitive workloads | Must: runAsNonRoot, drop ALL caps, seccompProfile, readOnlyRootFilesystem |

**Default**: `restricted` for app namespaces, `baseline` for infrastructure, `privileged` only for system.

```yaml
metadata:
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

Use `audit` + `warn` at stricter level than `enforce` during migration to see violations without breaking workloads.

## Network Policies

### Strategy: Default-Deny + Allow-List

1. Apply default-deny to every namespace:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

2. Allow DNS egress (everything breaks without this):
```yaml
spec:
  podSelector: {}
  policyTypes: [Egress]
  egress:
  - to:
    - namespaceSelector:
        matchLabels: { name: kube-system }
    ports:
    - { protocol: UDP, port: 53 }
```

3. Allow specific service-to-service communication via label selectors.

**Opinions:**
- Always deny by default. Allowlists are safer than denylists.
- Use `namespaceSelector` + `podSelector` together for cross-namespace policies.
- NetworkPolicy requires a CNI that supports it (Calico, Cilium). Default kubenet does NOT enforce policies.
- Test policies in staging with `audit` mode before enforcing.

## RBAC

### Principles
- **Least privilege**: Start with zero permissions, add only what's needed
- **Namespace-scoped Roles over ClusterRoles**: Minimize blast radius
- **Dedicated ServiceAccounts**: Never use `default` SA. Set `automountServiceAccountToken: false` unless needed.
- **No wildcard verbs**: `"*"` on resources = admin. Always enumerate specific verbs.

### Common Role Patterns

| Role | Resources | Verbs |
|------|-----------|-------|
| Pod reader | pods | get, list, watch |
| Deployment manager | deployments, pods | get, list, watch, create, update, patch, delete |
| CI/CD deployer | deployments, services, configmaps | get, list, create, update, patch |
| Secret reader (scoped) | secrets (by resourceNames) | get |

**Key opinion**: CI/CD service accounts should NOT have `delete` on pods -- let the deployment controller handle pod lifecycle.

### Debugging RBAC
```bash
kubectl auth can-i list pods --as system:serviceaccount:ns:my-sa
kubectl auth can-i '*' '*' --as system:serviceaccount:ns:my-sa  # Check for admin
kubectl get rolebindings,clusterrolebindings -A -o wide | grep my-user
```

## Pod Security Context (Always Set)

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
```

- `readOnlyRootFilesystem` + emptyDir at `/tmp` for writable temp files
- Never run as root. If image requires it, fix the image.
- `seccompProfile: RuntimeDefault` blocks dangerous syscalls with zero app changes.

## OPA Gatekeeper

Use for policies that Pod Security Standards can't enforce:
- Required labels on all resources
- Image registry restrictions (only pull from approved registries)
- Resource limit requirements
- Naming conventions

**Opinion**: Start with `dryrun` enforcement action, promote to `deny` after review. Gatekeeper violations in CI prevent merge; violations in cluster prevent deployment.

## Service Mesh mTLS (Istio)

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
spec:
  mtls:
    mode: STRICT  # PERMISSIVE during migration
```

- `STRICT` in production -- reject all non-mTLS traffic
- `PERMISSIVE` during mesh rollout -- accept both
- Use `AuthorizationPolicy` for fine-grained service-to-service access control

## Security Checklist

- [ ] Default-deny NetworkPolicy in all namespaces
- [ ] DNS egress allowed
- [ ] Pod Security Standards enforced (restricted for apps)
- [ ] Dedicated ServiceAccounts per workload
- [ ] `automountServiceAccountToken: false` where not needed
- [ ] No containers running as root
- [ ] All capabilities dropped
- [ ] Read-only root filesystem
- [ ] Seccomp profile enabled
- [ ] RBAC follows least privilege
- [ ] Image pull from approved registries only
