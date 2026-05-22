---
name: traefik-helm-configuration
description: |
  Consolidated Traefik Helm chart configuration skill covering HTTP/3 (QUIC), UDP
  cross-namespace routing, and plugin download failures. Use when:
  (1) enabling HTTP/3 on Traefik or Alt-Svc header shows wrong port (e.g., 8443 instead of 443),
  (2) HTTP/3 is configured in Helm values but not working end-to-end,
  (3) Cloudflare-proxied domains need HTTP/3 enabled,
  (4) custom UDP entrypoints don't appear in the LoadBalancer Service,
  (5) IngressRouteUDP logs show "udp service is not in the parent resource namespace",
  (6) DNS or other UDP traffic through Traefik times out despite correct IngressRouteUDP config,
  (7) all Traefik routes suddenly return 404 after a restart or pod recreation,
  (8) Traefik logs show "Plugins are disabled because an error has occurred",
  (9) plugin download fails with "context deadline exceeded" for crowdsec-bouncer or rewrite-body.
author: Claude Code
version: 1.0.0
date: 2026-02-22
---

# Traefik Helm Chart Configuration

Consolidated guide for three common Traefik Helm chart issues: HTTP/3 (QUIC) enablement,
UDP cross-namespace routing, and plugin download failures causing global 404s.

---

## HTTP/3 (QUIC)

### Problem

You want to enable HTTP/3 (QUIC) on a Traefik ingress controller in Kubernetes so that
clients can negotiate HTTP/3 connections via the `Alt-Svc` response header.

### Context / When to Use

- Enabling HTTP/3 for the first time on Traefik
- Troubleshooting HTTP/3 not working despite configuration
- Alt-Svc header shows internal container port (8443) instead of external port (443)
- Need to enable HTTP/3 on both origin (Traefik) and CDN (Cloudflare)

### Solution

#### Step 1: Configure Traefik Helm Chart Values

In the Traefik Helm release values, add `http3` configuration to the `websecure` entrypoint:

```hcl
# In modules/kubernetes/traefik/main.tf
ports = {
  websecure = {
    port        = 8443
    exposedPort = 443
    protocol    = "TCP"
    http = {
      tls = {
        enabled = true
      }
    }
    # Enable HTTP/3 (QUIC)
    http3 = {
      enabled        = true
      advertisedPort = 443  # CRITICAL: Must match the external port
    }
  }
}
```

**Key gotcha: `advertisedPort = 443`**

Without `advertisedPort`, Traefik advertises the *internal container port* (8443) in the
`Alt-Svc` header:
```
Alt-Svc: h3=":8443"; ma=2592000
```

This is wrong because clients connect on external port 443, not 8443. The correct header is:
```
Alt-Svc: h3=":443"; ma=2592000
```

Setting `advertisedPort = 443` fixes this.

#### Step 2: Ensure Helm Chart Fully Re-renders

Changing `http3.enabled=true` in values alone may not cause the Helm chart to add the
required UDP port to the Service and Deployment specs. The Traefik Helm chart templates
need to re-render to include `websecure-http3: 443/UDP` in the Service.

If the Service doesn't show a UDP port after applying:
- See the companion skill `helm-release-force-rerender` for fixing this
- The root cause is that `helm upgrade --reuse-values` (Terraform's default behavior)
  may not trigger template re-rendering for structural changes like adding new ports

After a successful apply, verify the Service has the UDP port:
```bash
kubectl get svc traefik -n traefik -o yaml | grep -A5 "443"
```

Expected output should include both:
```yaml
- name: websecure
  port: 443
  protocol: TCP
  targetPort: websecure
- name: websecure-http3
  port: 443
  protocol: UDP
  targetPort: websecure-http3
```

#### Step 3: Enable HTTP/3 on Cloudflare (if using Cloudflare proxy)

For Cloudflare-proxied domains, HTTP/3 must also be enabled at the Cloudflare zone level.

**Cloudflare Provider v4** (current in this repo):
```hcl
resource "cloudflare_zone_settings_override" "http3" {
  zone_id = var.cloudflare_zone_id

  settings {
    http3 = "on"  # String values: "on" or "off"
  }
}
```

**Note**: In Cloudflare provider v5, this uses `cloudflare_zone_setting` (singular) with
different syntax. The v4 resource is `cloudflare_zone_settings_override` (plural + override).

#### Step 4: Verify End-to-End

##### Testing from macOS

macOS system curl does NOT support HTTP/3. Install curl with HTTP/3:
```bash
brew install curl
```

Then use the Homebrew version explicitly:
```bash
# Test HTTP/3 negotiation (Alt-Svc header)
/opt/homebrew/opt/curl/bin/curl -sI https://example.viktorbarzin.me 2>&1 | grep -i alt-svc
# Expected: alt-svc: h3=":443"; ma=2592000

# Test actual HTTP/3 connection
/opt/homebrew/opt/curl/bin/curl --http3-only -sI https://example.viktorbarzin.me
# Expected: HTTP/3 200
```

##### Testing from within the Cluster

```bash
# Use a curl image with HTTP/3 support (amd64 only)
kubectl run curl-h3 --rm -it --image=ymuski/curl-http3 --restart=Never -- \
  curl --http3-only -sI https://example.viktorbarzin.me

# Note: ymuski/curl-http3 is amd64-only; it will fail on arm64 nodes
```

##### Checking Traefik Logs

```bash
kubectl logs -n traefik -l app.kubernetes.io/name=traefik --tail=100 | grep -i quic
```

### Verification Checklist

1. Traefik Service shows UDP port 443 (`websecure-http3`)
2. `Alt-Svc` response header shows `h3=":443"` (not `h3=":8443"`)
3. `/opt/homebrew/opt/curl/bin/curl --http3-only` successfully connects
4. Cloudflare zone has HTTP/3 enabled (for proxied domains)

### Current Configuration (This Repo)

- **Traefik config**: `modules/kubernetes/traefik/main.tf` (lines 89-92)
- **Cloudflare HTTP/3**: `modules/kubernetes/cloudflared/cloudflare.tf` (line 153)
- **MetalLB IP**: 10.0.20.202 (Traefik LoadBalancer service)

### Notes

- HTTP/3 uses QUIC over UDP. Firewalls must allow UDP 443 inbound.
- Traefik automatically handles TLS for HTTP/3 using the same certs as HTTPS.
- The `Alt-Svc` header is sent on HTTP/2 responses to tell clients HTTP/3 is available.
  Clients then upgrade to HTTP/3 on subsequent requests.
- For non-Cloudflare (direct DNS) domains, only the Traefik-side config is needed.
- Cloudflare handles its own HTTP/3 negotiation with end users; the origin connection
  between Cloudflare and Traefik uses HTTP/1.1 or HTTP/2 (not HTTP/3).

---

## UDP Cross-Namespace Routing

### Problem

Adding a custom UDP entrypoint (e.g., DNS on port 53) to Traefik v3 via Helm chart values
doesn't work out of the box. Traffic times out even though the Traefik pod listens on the
port internally. Two separate issues compound:

1. The Helm chart defaults `expose` to `false` for custom entrypoints -- the port is never
   added to the LoadBalancer Service
2. `allowCrossNamespace` defaults to `false` -- IngressRouteUDP in namespace A can't
   reference a Service in namespace B

### Context / Trigger Conditions

- Traefik Helm chart v39.0.0+ (Traefik v3.x)
- Custom UDP entrypoint defined in `ports` values
- `IngressRouteUDP` referencing a service in a different namespace
- Symptoms:
  - `kubectl get svc traefik` doesn't show your custom UDP port
  - UDP traffic to the LoadBalancer IP times out
  - Traefik logs show: `"udp service <namespace>/<service> is not in the parent resource namespace <traefik-namespace>"`
  - `netstat -ulnp` inside Traefik pod confirms it IS listening on the port

### Solution

#### Fix 1: Expose the UDP port on the Service

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

#### Fix 2: Enable cross-namespace CRD references

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

### Verification

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

### Example

DNS forwarding through Traefik to Technitium DNS:
- IngressRouteUDP in `traefik` namespace routes `dns-udp` entrypoint to
  `technitium-dns:53` in `technitium` namespace
- Without Fix 1: port 53 never exposed on LoadBalancer -- traffic can't reach Traefik
- Without Fix 2: Traefik rejects the route -- logs error every ~60 seconds
- With both fixes: DNS queries to LoadBalancer IP:53 -> Traefik -> Technitium

### Notes

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

---

## Plugin Download Failure (Global 404)

### Problem

After a node maintenance operation (containerd restart, node drain/uncordon, etc.),
all Traefik-managed routes return 404. Services, Ingresses, and Middlewares all exist
and look correct, making this extremely confusing to debug.

### Context / Trigger Conditions

- ALL Traefik routes return 404 simultaneously (not just one service)
- Traefik pods are Running and Ready
- Ingress resources exist with correct annotations
- Middlewares exist in the correct namespaces
- TLS secrets exist
- Traefik startup logs contain: `Plugins are disabled because an error has occurred`
- Plugin download error: `unable to download plugin ... context deadline exceeded`
- Happened after a node restart, containerd restart, or network disruption

### Root Cause

Traefik downloads plugins (crowdsec-bouncer, rewrite-body, etc.) from
`plugins.traefik.io` on **every pod startup**. If the download fails (network
unreachable, DNS not ready, timeout), Traefik **disables ALL plugins entirely**.

Since the `crowdsec` middleware is a plugin-based middleware referenced in virtually
every Ingress annotation (`traefik-crowdsec@kubernetescrd`), Traefik treats the
missing plugin middleware as a fatal routing error and returns 404 for every route
that references it -- which is typically all of them.

### Solution

```bash
# 1. Confirm the diagnosis - check Traefik startup logs
kubectl logs -n traefik -l app.kubernetes.io/name=traefik | head -20
# Look for: "Plugins are disabled because an error has occurred"

# 2. Verify outbound connectivity is restored
kubectl exec -n traefik $(kubectl get pods -n traefik -l app.kubernetes.io/name=traefik \
  -o jsonpath='{.items[0].metadata.name}') -- wget -q -O- --timeout=5 https://plugins.traefik.io

# 3. Rollout restart to retry plugin download
kubectl rollout restart deployment -n traefik traefik

# 4. Verify plugins loaded
kubectl logs -n traefik -l app.kubernetes.io/name=traefik | grep "Plugins"
# Should show: "Plugins loaded."

# 5. Verify routes work
curl -s -o /dev/null -w "%{http_code}" -H "Host: viktorbarzin.me" https://10.0.20.202 -k
# Should return 200 instead of 404
```

### Verification

- Traefik logs show `Plugins loaded.` (not `Plugins are disabled`)
- Routes return expected HTTP status codes (200, 302, etc.) instead of 404
- `kubectl logs -n traefik <pod> | grep "does not exist"` shows no middleware errors

### Why This Is Hard to Debug

1. **Traefik pods show Running/Ready** -- health checks pass even without plugins
2. **All Kubernetes resources look correct** -- Ingresses, Services, Middlewares all exist
3. **The error is in startup logs only** -- not in per-request logs (requests just get 404)
4. **The 404 is Traefik's default** -- same as "no route matched", not a backend error
5. **The middleware error is logged once at startup** -- easy to miss in a stream of logs

### Prevention

- During planned maintenance (node drain, containerd restart), restart Traefik pods
  AFTER network connectivity is confirmed restored
- Consider pre-caching Traefik plugins in the container image or using an init container
- Monitor for the `Plugins are disabled` log message in your alerting system

### Notes

- This affects ALL plugin-based middlewares, not just crowdsec
- The `rewrite-body` plugin (used for rybbit analytics injection) is also affected
- Traefik v3.x downloads plugins on every startup; there is no persistent cache
- If only some routes return 404, the problem is likely different (missing middleware
  or TLS secret, not a plugin issue)

---

## References

- [Traefik HTTP/3 Documentation](https://doc.traefik.io/traefik/routing/entrypoints/#http3)
- [Traefik Helm Chart Values](https://github.com/traefik/traefik-helm-chart/blob/master/traefik/values.yaml)
- [Cloudflare HTTP/3 Settings](https://developers.cloudflare.com/speed/optimization/protocol/http3/)
- [Traefik Helm Chart Ports Configuration](https://github.com/traefik/traefik-helm-chart)
- [Traefik v3 Providers Documentation](https://doc.traefik.io/traefik/providers/kubernetes-crd/)

## See Also

- `traefik-rewrite-body-troubleshooting` -- Traefik rewrite-body plugin troubleshooting (compression, Accept header issues)
- `helm-release-force-rerender` -- Force Helm chart re-render when structural changes don't take effect
