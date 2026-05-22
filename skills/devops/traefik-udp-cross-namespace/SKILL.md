---
name: traefik-udp-cross-namespace
description: |
  Fix Traefik v3 (Helm chart v39+) UDP entrypoints not working for cross-namespace
  IngressRouteUDP resources. Use when: (1) Traefik pod listens on a UDP port internally
  but the LoadBalancer service doesn't expose it, (2) IngressRouteUDP logs show
  "udp service <namespace>/<service> is not in the parent resource namespace" error,
  (3) DNS or other UDP traffic through Traefik times out despite correct IngressRouteUDP
  config, (4) Custom entrypoints added to Traefik Helm values don't appear in the
  Service ports. Requires two fixes: expose the port AND enable cross-namespace CRD refs.
author: Claude Code
version: 1.0.0
date: 2026-02-07
---

# Traefik v3 UDP Entrypoint + Cross-Namespace Routing

## Problem
Adding a custom UDP entrypoint (e.g., DNS on port 53) to Traefik v3 via Helm chart values
doesn't work out of the box. Traffic times out even though the Traefik pod listens on the
port internally. Two separate issues compound:

1. The Helm chart defaults `expose` to `false` for custom entrypoints — the port is never
   added to the LoadBalancer Service
2. `allowCrossNamespace` defaults to `false` — IngressRouteUDP in namespace A can't
   reference a Service in namespace B

## Context / Trigger Conditions
- Traefik Helm chart v39.0.0+ (Traefik v3.x)
- Custom UDP entrypoint defined in `ports` values
- `IngressRouteUDP` referencing a service in a different namespace
- Symptoms:
  - `kubectl get svc traefik` doesn't show your custom UDP port
  - UDP traffic to the LoadBalancer IP times out
  - Traefik logs show: `"udp service <namespace>/<service> is not in the parent resource namespace <traefik-namespace>"`
  - `netstat -ulnp` inside Traefik pod confirms it IS listening on the port

## Solution

### Fix 1: Expose the UDP port on the Service

In the Helm values, add `expose = { default = true }` to the entrypoint:

```hcl
# Terraform HCL
ports = {
  dns-udp = {
    port        = 5353
    exposedPort = 53
    protocol    = "UDP"
    expose      = { default = true }  # <-- Required for custom entrypoints
  }
}
```

```yaml
# Helm values YAML equivalent
ports:
  dns-udp:
    port: 5353
    exposedPort: 53
    protocol: UDP
    expose:
      default: true
```

Note: The built-in `web` and `websecure` entrypoints have `expose.default = true` by
default, but custom entrypoints do NOT.

### Fix 2: Enable cross-namespace CRD references

In the Helm values, add `allowCrossNamespace = true` to the kubernetesCRD provider:

```hcl
# Terraform HCL
providers = {
  kubernetesCRD = {
    enabled              = true
    allowCrossNamespace  = true  # <-- Required for cross-namespace IngressRouteUDP
  }
}
```

```yaml
# Helm values YAML
providers:
  kubernetesCRD:
    enabled: true
    allowCrossNamespace: true
```

This is required whenever an `IngressRouteUDP` (or `IngressRouteTCP`, `IngressRoute`)
references a Kubernetes Service in a different namespace.

## Verification

```bash
# 1. Verify the port appears in the Service
kubectl get svc -n traefik traefik -o jsonpath='{.spec.ports[*].name}'
# Should include your custom entrypoint name (e.g., "dns-udp")

# 2. Check Traefik logs for cross-namespace errors
kubectl logs -n traefik -l app.kubernetes.io/name=traefik | grep "not in the parent resource namespace"
# Should return nothing after the fix

# 3. Test the UDP service
dig @<traefik-lb-ip> example.com
```

## Example

DNS forwarding through Traefik to Technitium DNS:
- IngressRouteUDP in `traefik` namespace routes `dns-udp` entrypoint to
  `technitium-dns:53` in `technitium` namespace
- Without Fix 1: port 53 never exposed on LoadBalancer — traffic can't reach Traefik
- Without Fix 2: Traefik rejects the route — logs error every ~60 seconds
- With both fixes: DNS queries to LoadBalancer IP:53 → Traefik → Technitium

## Notes

1. **Debugging order matters**: Fix 1 (expose) must come first. Without the port on the
   Service, you can't even test if the routing works. Fix 2 (cross-namespace) errors only
   appear in Traefik logs, not as user-visible failures.
2. **`allowCrossNamespace` is a security consideration**: It allows any IngressRoute CRD
   to reference services in any namespace. If this is too broad, consider using
   `TraefikService` middleware or moving the IngressRouteUDP to the target namespace.
3. **Rolling update**: Changing `allowCrossNamespace` triggers a Traefik pod restart
   (new CLI args). Changing `expose` only updates the Service (no pod restart needed).
4. **This applies to TCP too**: `IngressRouteTCP` with cross-namespace services needs the
   same `allowCrossNamespace` setting.

## References
- Traefik Helm chart ports configuration: https://github.com/traefik/traefik-helm-chart
- Traefik v3 providers documentation: https://doc.traefik.io/traefik/providers/kubernetes-crd/

## See also
- `traefik-http3-quic` — related Traefik Helm chart configuration skill
