---
name: traefik-rewrite-body-compression
description: |
  Fix for Traefik rewrite-body plugin (packruler/rewrite-body) failing with
  "flate: corrupt input before offset 5" errors when backends send gzip-compressed
  responses. Use when: (1) rewrite-body plugin logs show "Error loading content:
  flate: corrupt input before offset 5", (2) rybbit analytics script injection
  breaks WebSocket connections or authentication flows, (3) HA Companion app
  stuck in external_auth loop with repeated GET /?external_auth=1 requests,
  (4) mobile apps fail to connect while browser works fine, (5) HTTP 499 errors
  on webhook POST requests. Root cause: the plugin attempts to decompress all
  responses before checking content-type, and fails on certain gzip encodings,
  corrupting the response body.
author: Claude Code
version: 1.0.0
date: 2026-02-11
---

# Traefik Rewrite-Body Plugin Compression Fix

## Problem
The `packruler/rewrite-body` Traefik plugin (used for injecting analytics scripts
like rybbit into HTML responses) fails to decompress gzip-compressed responses from
backends. Despite the `monitoring.types = ["text/html"]` filter, the plugin attempts
to decompress ALL responses before checking content type. When decompression fails,
it corrupts the response body, breaking:
- WebSocket upgrade handshakes
- Authentication flows (HA Companion app's `external_auth` callback)
- Mobile app connectivity (while browser appears to work due to auto-reconnect)

## Context / Trigger Conditions
- Traefik logs show: `Rewrite-Body | ERROR ... Error loading content: flate: corrupt input before offset 5`
- Mobile apps (e.g., Home Assistant Companion) fail while browser works
- HA Companion app shows repeated `GET /?external_auth=1` requests (auth loop)
- WebSocket connections (`/api/websocket`) are very short-lived (seconds instead of minutes)
- HTTP 499 errors on API calls (client disconnects due to corrupted responses)
- Using `packruler/rewrite-body` plugin v1.2.0 with `monitoring.types = ["text/html"]`

## Misleading Symptoms
- HTTP/3 (QUIC) may appear to be the cause because HTTP/3 requests show 499 errors.
  This is a red herring - the rewrite-body plugin corruption affects all protocols.
- WebSocket issues may look like a timeout or proxy configuration problem.
- The `monitoring.types = ["text/html"]` config suggests the plugin should only touch
  HTML, but it still processes all responses for decompression before filtering.

## Solution

### Step 1: Create a strip-accept-encoding middleware
Add a Traefik middleware that removes `Accept-Encoding` from requests, forcing
backends to send uncompressed responses that the plugin can safely process:

```hcl
# In traefik/middleware.tf
resource "kubernetes_manifest" "middleware_strip_accept_encoding" {
  manifest = {
    apiVersion = "traefik.io/v1alpha1"
    kind       = "Middleware"
    metadata = {
      name      = "strip-accept-encoding"
      namespace = kubernetes_namespace.traefik.metadata[0].name
    }
    spec = {
      headers = {
        customRequestHeaders = {
          "Accept-Encoding" = ""
        }
      }
    }
  }
  depends_on = [helm_release.traefik]
}
```

### Step 2: Add middleware to routes with rewrite-body
In the ingress factory middleware chain, add `strip-accept-encoding` BEFORE the
rewrite-body middleware:

```hcl
var.rybbit_site_id != null ? "traefik-strip-accept-encoding@kubernetescrd" : null,
var.rybbit_site_id != null ? "${var.namespace}-rybbit-analytics-${var.name}@kubernetescrd" : null,
```

The order matters: strip-accept-encoding must come first so the request reaches
the backend without Accept-Encoding, and the uncompressed response then passes
through the rewrite-body plugin.

## Verification
1. Check Traefik logs for absence of `flate: corrupt input` errors:
   ```bash
   kubectl logs -n traefik -l app.kubernetes.io/name=traefik --tail=200 | grep -i "flate\|rewrite-body"
   ```
2. Verify the middleware chain includes strip-accept-encoding before rybbit:
   ```bash
   kubectl get ingress -n <namespace> <name> -o jsonpath='{.metadata.annotations.traefik\.ingress\.kubernetes\.io/router\.middlewares}'
   ```
3. Test mobile app connectivity (HA Companion, etc.)

## Notes
- This affects ALL services using the rewrite-body plugin, not just HA
- The fix is applied conditionally: `strip-accept-encoding` is only added to the
  middleware chain when `rybbit_site_id` is set, so services without analytics
  are unaffected
- Both `ingress_factory` and `reverse_proxy/factory` modules need the fix
- Traefik may still compress responses to clients via its own compression middleware;
  the strip only affects the backend request
- The plugin's `monitoring.types` filter works for deciding what to rewrite, but
  decompression is attempted on all responses regardless

## See Also
- `ingress-factory-migration` - Covers the ingress factory module that creates
  rybbit analytics middlewares
- `traefik-http3-quic` - HTTP/3 configuration (not the cause, but often a red herring
  when debugging this issue)
