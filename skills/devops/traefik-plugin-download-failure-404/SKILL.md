---
name: traefik-plugin-download-failure-404
description: |
  Fix for Traefik returning 404 on ALL routes after a restart or pod recreation.
  Use when: (1) all Traefik-managed Ingresses suddenly return 404,
  (2) Traefik logs show "Plugins are disabled because an error has occurred",
  (3) plugin download fails with "context deadline exceeded" for crowdsec-bouncer
  or rewrite-body plugins, (4) Traefik pods started while outbound internet was
  unreachable (e.g. during containerd restart, network disruption, DNS outage),
  (5) services were working before a node maintenance operation but now all return 404.
  Root cause: Traefik downloads plugins on startup; if download fails, ALL plugins
  are disabled, and any middleware referencing a plugin causes its route to 404.
author: Claude Code
version: 1.0.0
date: 2026-02-14
---

# Traefik Plugin Download Failure Causing Global 404

## Problem

After a node maintenance operation (containerd restart, node drain/uncordon, etc.),
all Traefik-managed routes return 404. Services, Ingresses, and Middlewares all exist
and look correct, making this extremely confusing to debug.

## Context / Trigger Conditions

- ALL Traefik routes return 404 simultaneously (not just one service)
- Traefik pods are Running and Ready
- Ingress resources exist with correct annotations
- Middlewares exist in the correct namespaces
- TLS secrets exist
- Traefik startup logs contain: `Plugins are disabled because an error has occurred`
- Plugin download error: `unable to download plugin ... context deadline exceeded`
- Happened after a node restart, containerd restart, or network disruption

## Root Cause

Traefik downloads plugins (crowdsec-bouncer, rewrite-body, etc.) from
`plugins.traefik.io` on **every pod startup**. If the download fails (network
unreachable, DNS not ready, timeout), Traefik **disables ALL plugins entirely**.

Since the `crowdsec` middleware is a plugin-based middleware referenced in virtually
every Ingress annotation (`traefik-crowdsec@kubernetescrd`), Traefik treats the
missing plugin middleware as a fatal routing error and returns 404 for every route
that references it — which is typically all of them.

## Solution

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

## Verification

- Traefik logs show `Plugins loaded.` (not `Plugins are disabled`)
- Routes return expected HTTP status codes (200, 302, etc.) instead of 404
- `kubectl logs -n traefik <pod> | grep "does not exist"` shows no middleware errors

## Why This Is Hard to Debug

1. **Traefik pods show Running/Ready** — health checks pass even without plugins
2. **All Kubernetes resources look correct** — Ingresses, Services, Middlewares all exist
3. **The error is in startup logs only** — not in per-request logs (requests just get 404)
4. **The 404 is Traefik's default** — same as "no route matched", not a backend error
5. **The middleware error is logged once at startup** — easy to miss in a stream of logs

## Prevention

- During planned maintenance (node drain, containerd restart), restart Traefik pods
  AFTER network connectivity is confirmed restored
- Consider pre-caching Traefik plugins in the container image or using an init container
- Monitor for the `Plugins are disabled` log message in your alerting system

## Notes

- This affects ALL plugin-based middlewares, not just crowdsec
- The `rewrite-body` plugin (used for rybbit analytics injection) is also affected
- Traefik v3.x downloads plugins on every startup; there is no persistent cache
- If only some routes return 404, the problem is likely different (missing middleware
  or TLS secret, not a plugin issue)
