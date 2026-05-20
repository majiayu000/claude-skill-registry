---
name: network-policy
description: |
  Manage Cilium network policies: profile selection, access labels, Hubble debugging,
  platform namespace CNPs, and emergency escape hatch procedures.

  Use when: (1) Deploying a new application and setting network profile,
  (2) Debugging blocked traffic with Hubble, (3) Adding shared resource access,
  (4) Creating platform namespace CNPs, (5) Using the escape hatch for emergencies,
  (6) Verifying network policy enforcement.

  Triggers: "network policy", "hubble", "dropped traffic", "cilium", "blocked traffic",
  "network profile", "access label", "escape hatch", "cnp", "ccnp"
user-invocable: false
---

# Network Policy Management

## Architecture Quick Reference

All cluster traffic is **implicitly denied** via Cilium baseline CCNPs. Two layers control access:

1. **Baselines** (cluster-wide CCNPs): DNS egress, health probes, Prometheus scrape, opt-in kube-API
2. **Profiles** (per-namespace via label): Ingress/egress rules matched by `network-policy.homelab/profile=<value>`

Platform namespaces (`kube-system`, `monitoring`, `database`, etc.) use hand-crafted CNPs — **never** apply profiles to them.

---

## Workflow: Deploy App with Network Policy

### Step 1: Choose a Profile

| Profile | Ingress | Egress | Use Case |
|---------|---------|--------|----------|
| `isolated` | None | DNS only | Batch jobs, workers |
| `internal` | Internal gateway | DNS only | Internal dashboards |
| `internal-egress` | Internal gateway | DNS + HTTPS | Internal apps calling external APIs |
| `standard` | Both gateways | DNS + HTTPS | Public-facing web apps |

**Decision tree:**
- Does the app need to be reached from the internet? -> `standard`
- Internal-only but needs to call external APIs? -> `internal-egress`
- Internal-only, no external calls? -> `internal`
- No ingress needed at all? -> `isolated`

### Step 2: Apply Profile Label to Namespace

In the namespace YAML (committed to git, not `kubectl apply`):

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-app
  labels:
    network-policy.homelab/profile: standard
```

### Step 3: Add Shared Resource Access Labels

If the app needs database, cache, or S3 access, add access labels to the namespace:

```yaml
labels:
  network-policy.homelab/profile: standard
  access.network-policy.homelab/postgres: "true"     # PostgreSQL (port 5432)
  access.network-policy.homelab/dragonfly: "true"    # Dragonfly/Redis (port 6379)
  access.network-policy.homelab/garage-s3: "true"    # Garage S3 (port 3900)
  access.network-policy.homelab/kube-api: "true"     # Kubernetes API (port 6443)
```

### Step 4: Verify Connectivity

After deployment, check for dropped traffic:

```bash
hubble observe --verdict DROPPED --namespace my-app --since 5m
```

If drops appear, see the Debugging section below.

---

## Workflow: Debug Blocked Traffic

### Step 1: Identify Drops

```bash
# All drops in a namespace
hubble observe --verdict DROPPED --namespace my-app --since 5m

# With source/destination details
hubble observe --verdict DROPPED --namespace my-app --since 5m -o json | \
  jq '{src: .source.namespace + "/" + .source.pod_name, dst: .destination.namespace + "/" + .destination.pod_name, port: (.l4.TCP.destination_port // .l4.UDP.destination_port)}'
```

### Step 2: Classify the Drop

| Drop Pattern | Likely Cause | Fix |
|---|---|---|
| Egress to `kube-system:53` dropped | Missing DNS baseline | Should not happen — check if baseline CCNP exists |
| Egress to `database:5432` dropped | Missing postgres access label | Add `access.network-policy.homelab/postgres=true` |
| Egress to `database:6379` dropped | Missing dragonfly access label | Add `access.network-policy.homelab/dragonfly=true` |
| Egress to internet `:443` dropped | Profile doesn't allow HTTPS egress | Switch to `internal-egress` or `standard` |
| Ingress from `istio-gateway` dropped | Profile doesn't allow gateway ingress | Switch to `internal`, `internal-egress`, or `standard` |
| Ingress from `monitoring:prometheus` dropped | Missing baseline | Should not happen — check baseline CCNP |

### Step 3: Verify Specific Flows

```bash
# DNS resolution
hubble observe --namespace my-app --protocol UDP --port 53 --since 5m

# Database connectivity
hubble observe --namespace my-app --to-namespace database --port 5432 --since 5m

# Internet egress
hubble observe --namespace my-app --to-identity world --port 443 --since 5m

# Gateway ingress
hubble observe --from-namespace istio-gateway --to-namespace my-app --since 5m

# Prometheus scraping
hubble observe --from-namespace monitoring --to-namespace my-app --since 5m
```

### Step 4: Check Policy Status

```bash
# List all policies affecting a namespace
kubectl get cnp -n my-app
kubectl get ccnp | grep -E 'baseline|profile'

# Check which profile is active
kubectl get namespace my-app --show-labels | grep network-policy
```

---

## Workflow: Emergency Escape Hatch

**Use only when network policies block legitimate traffic and you need immediate relief.**

### Step 1: Disable Enforcement

```bash
kubectl label namespace <ns> network-policy.homelab/enforcement=disabled
```

This triggers alerts:
- `NetworkPolicyEnforcementDisabled` (warning) after 5 minutes
- `NetworkPolicyEnforcementDisabledLong` (critical) after 24 hours

### Step 2: Verify Traffic Flows

```bash
hubble observe --namespace <ns> --since 1m
```

### Step 3: Investigate Root Cause

Use the debugging workflow above to identify what policy is missing or misconfigured.

### Step 4: Fix the Policy (via GitOps)

Apply the fix through a PR — never `kubectl apply` directly.

### Step 5: Re-enable Enforcement

```bash
kubectl label namespace <ns> network-policy.homelab/enforcement-
```

See `docs/runbooks/network-policy-escape-hatch.md` for the full procedure.

---

## Workflow: Add Platform Namespace CNP

Platform namespaces need hand-crafted CNPs (not profiles). Create in `kubernetes/platform/config/network-policy/platform/`.

### Required Rules

Every platform CNP must include:

1. **DNS egress** to `kube-system/kube-dns` (port 53 UDP/TCP)
2. **Prometheus scrape ingress** from `monitoring` namespace
3. **Health probe ingress** from `health` entity and `169.254.0.0/16`
4. **HBONE rules** if namespace participates in Istio mesh (port 15008 to/from `istio-system/ztunnel`)
5. **Service-specific rules** for the namespace's actual traffic patterns

### Template

```yaml
---
apiVersion: cilium.io/v2
kind: CiliumNetworkPolicy
metadata:
  name: <namespace>-default
  namespace: <namespace>
spec:
  description: "<Namespace purpose>: describe allowed traffic"
  endpointSelector: {}
  ingress:
    # Health probes
    - fromEntities: [health]
    - fromCIDR: ["169.254.0.0/16"]
    # Prometheus scraping
    - fromEndpoints:
        - matchLabels:
            io.kubernetes.pod.namespace: monitoring
            app.kubernetes.io/name: prometheus
      toPorts:
        - ports:
            - port: "<metrics-port>"
              protocol: TCP
    # HBONE (if mesh participant)
    - fromEndpoints:
        - matchLabels:
            io.kubernetes.pod.namespace: istio-system
            app: ztunnel
      toPorts:
        - ports:
            - port: "15008"
              protocol: TCP
  egress:
    # DNS
    - toEndpoints:
        - matchLabels:
            io.kubernetes.pod.namespace: kube-system
            k8s-app: kube-dns
      toPorts:
        - ports:
            - port: "53"
              protocol: UDP
            - port: "53"
              protocol: TCP
    # HBONE (if mesh participant)
    - toEndpoints:
        - matchLabels:
            io.kubernetes.pod.namespace: istio-system
            app: ztunnel
      toPorts:
        - ports:
            - port: "15008"
              protocol: TCP
```

After creating, add to `kubernetes/platform/config/network-policy/platform/kustomization.yaml`.

---

## Anti-Patterns

- **NEVER** create explicit `default-deny` policies — baselines provide implicit deny
- **NEVER** use profiles for platform namespaces — they need custom CNPs
- **NEVER** hardcode IP addresses — use endpoint selectors and entities
- **NEVER** allow `any` port — always specify explicit port lists
- **NEVER** disable enforcement without following the escape hatch runbook
- **NEVER** apply network policy changes via `kubectl` on integration/live — always through GitOps
- **Dev cluster exception**: Direct `kubectl apply` of network policies is permitted on dev for testing

---

## Cross-References

- [network-policy/CLAUDE.md](../../kubernetes/platform/config/network-policy/CLAUDE.md) — Full architecture and directory structure
- [docs/runbooks/network-policy-escape-hatch.md](../../docs/runbooks/network-policy-escape-hatch.md) — Emergency bypass procedure
- [docs/runbooks/network-policy-verification.md](../../docs/runbooks/network-policy-verification.md) — Hubble verification commands
