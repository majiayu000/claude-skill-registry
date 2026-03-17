---
name: traefik-rewrite-body-troubleshooting
description: |
  Troubleshooting guide for the Traefik rewrite-body plugin (packruler/rewrite-body).
  Covers two failure modes: (1) Compression failure — plugin logs "flate: corrupt input
  before offset 5" when backends send gzip-compressed responses, corrupting response
  bodies and breaking WebSocket connections, authentication flows, and mobile app
  connectivity. (2) Silent skip — plugin silently skips content injection (rybbit
  analytics, trap links, or any HTML rewriting) when the request Accept header doesn't
  contain "text/html" (e.g., curl's default Accept: */*), making it appear broken
  despite correct configuration.
author: Claude Code
version: 1.0.0
date: 2026-02-22
---

# Traefik Rewrite-Body Plugin Troubleshooting

Two distinct failure modes for the `packruler/rewrite-body` Traefik plugin used for
injecting analytics scripts (rybbit) and anti-AI trap links into HTML responses.

---

## Problem 1: Compression Failure

### Symptoms
- Traefik logs show: `Rewrite-Body | ERROR ... Error loading content: flate: corrupt input before offset 5`
- Mobile apps (e.g., Home Assistant Companion) fail while browser works
- HA Companion app shows repeated `GET /?external_auth=1` requests (auth loop)
- WebSocket connections (`/api/websocket`) are very short-lived (seconds instead of minutes)
- HTTP 499 errors on API calls (client disconnects due to corrupted responses)
- Using `packruler/rewrite-body` plugin v1.2.0 with `monitoring.types = ["text/html"]`

### Root Cause
Despite the `monitoring.types = ["text/html"]` filter, the plugin attempts to decompress
ALL responses before checking content type. When decompression fails on certain gzip
encodings, it corrupts the response body, breaking:
- WebSocket upgrade handshakes
- Authentication flows (HA Companion app's `external_auth` callback)
- Mobile app connectivity (while browser appears to work due to auto-reconnect)

### Misleading Symptoms
- HTTP/3 (QUIC) may appear to be the cause because HTTP/3 requests show 499 errors.
  This is a red herring -- the rewrite-body plugin corruption affects all protocols.
- WebSocket issues may look like a timeout or proxy configuration problem.
- The `monitoring.types = ["text/html"]` config suggests the plugin should only touch
  HTML, but it still processes all responses for decompression before filtering.

### Solution

#### Step 1: Create a strip-accept-encoding middleware
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

#### Step 2: Add middleware to routes with rewrite-body
In the ingress factory middleware chain, add `strip-accept-encoding` BEFORE the
rewrite-body middleware:

```hcl
var.rybbit_site_id != null ? "traefik-strip-accept-encoding@kubernetescrd" : null,
var.rybbit_site_id != null ? "${var.namespace}-rybbit-analytics-${var.name}@kubernetescrd" : null,
```

The order matters: strip-accept-encoding must come first so the request reaches
the backend without Accept-Encoding, and the uncompressed response then passes
through the rewrite-body plugin.

### Verification (Compression Fix)
1. Check Traefik logs for absence of `flate: corrupt input` errors:
   ```bash
   kubectl logs -n traefik -l app.kubernetes.io/name=traefik --tail=200 | grep -i "flate\|rewrite-body"
   ```
2. Verify the middleware chain includes strip-accept-encoding before rybbit:
   ```bash
   kubectl get ingress -n <namespace> <name> -o jsonpath='{.metadata.annotations.traefik\.ingress\.kubernetes\.io/router\.middlewares}'
   ```
3. Test mobile app connectivity (HA Companion, etc.)

### Notes (Compression)
- This affects ALL services using the rewrite-body plugin, not just HA
- The fix is applied conditionally: `strip-accept-encoding` is only added to the
  middleware chain when `rybbit_site_id` is set, so services without analytics
  are unaffected
- Both `ingress_factory` and `reverse_proxy/factory` modules need the fix
- Traefik may still compress responses to clients via its own compression middleware;
  the strip only affects the backend request
- The plugin's `monitoring.types` filter works for deciding what to rewrite, but
  decompression is attempted on all responses regardless

---

## Problem 2: Silent Skip (Accept Header Mismatch)

### Symptoms
- rewrite-body middleware is in the ingress middleware chain and shows status "enabled" in Traefik API
- `curl https://example.com/` returns original HTML with no injected content
- Browser shows injected content (rybbit script, trap links, etc.)
- No errors in Traefik logs -- the plugin silently skips processing
- `monitoring.types = ["text/html"]` is configured in the middleware spec
- Middleware chain order is correct (strip-accept-encoding before rewrite-body)

### Root Cause
In the plugin source code, `SupportsProcessing()` checks the **request** `Accept`
header (not the response `Content-Type`) against `monitoring.types`:

```go
func (r *Rewriter) SupportsProcessing(req *http.Request) bool {
    accept := req.Header.Get("Accept")
    for _, monitoringType := range r.monitoring.Types {
        if strings.Contains(accept, monitoringType) {
            return true
        }
    }
    return false
}
```

It uses `strings.Contains(accept, "text/html")`. The curl default `Accept: */*` does
NOT contain the substring `text/html`, so the plugin returns false and skips all
processing. Browser requests include `Accept: text/html,application/xhtml+xml,...`
which does match.

### Misleading Symptoms
- Appears as if the middleware isn't working at all
- May look like a middleware ordering issue or configuration error
- `kubectl get middleware` shows the resource exists with correct spec
- Traefik API (`/api/http/middlewares/`) shows the middleware as "enabled"
- Checking the rewrite-body regex patterns seems pointless since nothing is being processed

### Solution
This is **working as designed** -- not a bug. The fix depends on context:

#### For testing with curl
Add the `Accept` header to simulate a browser:
```bash
curl -s -H "Accept: text/html,application/xhtml+xml" https://example.com/
```

#### For verifying injection is working
```bash
# Check for injected content (trap links, analytics, etc.)
curl -s -H "Accept: text/html,application/xhtml+xml" https://example.com/ \
  | grep -oE 'href="https://poison[^"]*"'

# Check for rybbit analytics
curl -s -H "Accept: text/html,application/xhtml+xml" https://example.com/ \
  | grep -oE 'src="https://rybbit[^"]*"'
```

#### For programmatic clients that need injection
If a non-browser client needs to receive injected content, ensure it sends
`Accept: text/html` in its request headers.

### Verification (Accept Header)
```bash
# Without Accept header -- no injection (expected)
curl -s https://example.com/ | grep -c "rybbit"
# Output: 0

# With Accept header -- injection works
curl -s -H "Accept: text/html" https://example.com/ | grep -c "rybbit"
# Output: 1
```

### Notes (Accept Header)
- This behavior is independent of the compression issue (Problem 1 above)
- The check is on the **request** `Accept` header, not the **response** `Content-Type`
- `Accept: */*` does NOT match -- `strings.Contains("*/*", "text/html")` is false
- Real AI scrapers typically send browser-like Accept headers, so trap links will be
  injected for them correctly
- API calls (which typically send `Accept: application/json`) are correctly skipped

---

## See Also
- `traefik-helm-configuration` -- Traefik Helm chart configuration and entrypoints
- `ingress-factory-migration` -- Covers the ingress factory module that creates
  rybbit analytics middlewares
