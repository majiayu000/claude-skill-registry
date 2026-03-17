---
name: traefik-http3-quic
description: |
  Enable HTTP/3 (QUIC) on a Traefik ingress controller in Kubernetes, managed via
  Terraform Helm charts. Use when: (1) you want to enable HTTP/3 on Traefik,
  (2) Alt-Svc header shows wrong port (e.g., 8443 instead of 443),
  (3) HTTP/3 is configured in Helm values but not working end-to-end,
  (4) Cloudflare-proxied domains need HTTP/3 enabled.
  Covers Traefik Helm chart values, advertisedPort gotcha, Cloudflare zone settings,
  and end-to-end verification.
author: Claude Code
version: 1.0.0
date: 2026-02-07
---

# Traefik HTTP/3 (QUIC) Enablement

## Problem
You want to enable HTTP/3 (QUIC) on a Traefik ingress controller in Kubernetes so that
clients can negotiate HTTP/3 connections via the `Alt-Svc` response header.

## Context / When to Use
- Enabling HTTP/3 for the first time on Traefik
- Troubleshooting HTTP/3 not working despite configuration
- Alt-Svc header shows internal container port (8443) instead of external port (443)
- Need to enable HTTP/3 on both origin (Traefik) and CDN (Cloudflare)

## Solution

### Step 1: Configure Traefik Helm Chart Values

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

### Step 2: Ensure Helm Chart Fully Re-renders

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

### Step 3: Enable HTTP/3 on Cloudflare (if using Cloudflare proxy)

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

### Step 4: Verify End-to-End

#### Testing from macOS

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

#### Testing from within the Cluster

```bash
# Use a curl image with HTTP/3 support (amd64 only)
kubectl run curl-h3 --rm -it --image=ymuski/curl-http3 --restart=Never -- \
  curl --http3-only -sI https://example.viktorbarzin.me

# Note: ymuski/curl-http3 is amd64-only; it will fail on arm64 nodes
```

#### Checking Traefik Logs

```bash
kubectl logs -n traefik -l app.kubernetes.io/name=traefik --tail=100 | grep -i quic
```

## Verification Checklist

1. Traefik Service shows UDP port 443 (`websecure-http3`)
2. `Alt-Svc` response header shows `h3=":443"` (not `h3=":8443"`)
3. `/opt/homebrew/opt/curl/bin/curl --http3-only` successfully connects
4. Cloudflare zone has HTTP/3 enabled (for proxied domains)

## Current Configuration (This Repo)

- **Traefik config**: `modules/kubernetes/traefik/main.tf` (lines 89-92)
- **Cloudflare HTTP/3**: `modules/kubernetes/cloudflared/cloudflare.tf` (line 153)
- **MetalLB IP**: 10.0.20.202 (Traefik LoadBalancer service)

## Notes

- HTTP/3 uses QUIC over UDP. Firewalls must allow UDP 443 inbound.
- Traefik automatically handles TLS for HTTP/3 using the same certs as HTTPS.
- The `Alt-Svc` header is sent on HTTP/2 responses to tell clients HTTP/3 is available.
  Clients then upgrade to HTTP/3 on subsequent requests.
- For non-Cloudflare (direct DNS) domains, only the Traefik-side config is needed.
- Cloudflare handles its own HTTP/3 negotiation with end users; the origin connection
  between Cloudflare and Traefik uses HTTP/1.1 or HTTP/2 (not HTTP/3).

## References

- [Traefik HTTP/3 Documentation](https://doc.traefik.io/traefik/routing/entrypoints/#http3)
- [Traefik Helm Chart Values](https://github.com/traefik/traefik-helm-chart/blob/master/traefik/values.yaml)
- [Cloudflare HTTP/3 Settings](https://developers.cloudflare.com/speed/optimization/protocol/http3/)
