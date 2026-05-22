---
name: ingress-factory-migration
description: |
  Migrate raw kubernetes_ingress_v1 resources to the centralized ingress_factory module.
  Use when: (1) a service defines a raw kubernetes_ingress_v1 with hand-rolled Traefik
  middleware annotations, (2) adding a new service that needs standard ingress with
  rate limiting, CrowdSec, CSP headers, rybbit analytics, or authentik auth,
  (3) refactoring existing ingresses for consistency. Covers single-path, multi-path,
  split UI/API, full_host overrides, custom rate limits, and extra middleware injection.
author: Claude Code
version: 1.0.0
date: 2026-02-10
---

# Ingress Factory Migration

## Problem
Services define raw `kubernetes_ingress_v1` resources with hand-rolled Traefik middleware
chains. This creates inconsistency - middleware chains are copy-pasted per service, making
it easy to miss security middleware (CrowdSec, rate limiting) or analytics (rybbit). The
`ingress_factory` module at `modules/kubernetes/ingress_factory/main.tf` provides a single
point of control.

## Context / Trigger Conditions
- Service has a raw `kubernetes_ingress_v1` resource instead of using `module "ingress"`
- Service has a manually defined `kubernetes_manifest` for rybbit analytics middleware
- New service needs standard ingress configuration
- Middleware chain needs to be updated across many services

## Solution

### Standard single-path ingress
Replace the raw resource with:
```hcl
module "ingress" {
  source          = "../ingress_factory"
  namespace       = kubernetes_namespace.<service>.metadata[0].name
  name            = "<service-name>"        # becomes the ingress name AND default hostname
  host            = "<subdomain>"           # optional: override hostname (if different from name)
  service_name    = "<k8s-service-name>"    # optional: defaults to name
  port            = 80                      # optional: defaults to 80
  tls_secret_name = var.tls_secret_name
  protected       = false                   # set true for authentik forward auth
}
```

### Multi-path / split UI+API
Use two module calls with different names but same host:
```hcl
module "ingress" {
  source          = "../ingress_factory"
  namespace       = kubernetes_namespace.<service>.metadata[0].name
  name            = "<service>"
  host            = "<subdomain>"
  service_name    = "<ui-service>"
  tls_secret_name = var.tls_secret_name
  rybbit_site_id  = "<id>"                  # optional: adds rybbit analytics
}

module "ingress-api" {
  source          = "../ingress_factory"
  namespace       = kubernetes_namespace.<service>.metadata[0].name
  name            = "<service>-api"
  host            = "<subdomain>"           # same host as UI
  service_name    = "<api-service>"
  ingress_path    = ["/api"]
  tls_secret_name = var.tls_secret_name
  # No rybbit_site_id - API returns JSON, not HTML
}
```

### Full host override (for root domain like viktorbarzin.me)
```hcl
module "ingress" {
  source          = "../ingress_factory"
  namespace       = kubernetes_namespace.<service>.metadata[0].name
  name            = "<service>"
  service_name    = "<k8s-service>"
  full_host       = "viktorbarzin.me"       # bypasses name.root_domain construction
  tls_secret_name = var.tls_secret_name
}
```

### Custom rate limiting (e.g., immich)
```hcl
module "ingress" {
  source                  = "../ingress_factory"
  namespace               = kubernetes_namespace.<service>.metadata[0].name
  name                    = "<service>"
  skip_default_rate_limit = true
  extra_middlewares        = ["traefik-<custom>-rate-limit@kubernetescrd"]
  tls_secret_name         = var.tls_secret_name
}
```

### Key variables reference
| Variable | Default | Purpose |
|----------|---------|---------|
| `name` | required | Ingress resource name + default hostname |
| `host` | null | Override hostname prefix (name used if null) |
| `full_host` | null | Override entire hostname (bypasses root_domain) |
| `service_name` | null | K8s service name (name used if null) |
| `port` | 80 | Backend service port |
| `ingress_path` | ["/"] | URL paths to match |
| `protected` | false | Adds authentik forward auth middleware |
| `rybbit_site_id` | null | Adds rybbit analytics script injection |
| `skip_default_rate_limit` | false | Omits default rate limiter |
| `extra_middlewares` | [] | Additional middleware references to append |
| `extra_annotations` | {} | Additional ingress annotations |
| `allow_local_access_only` | false | Restricts to LAN/VPN |
| `exclude_crowdsec` | false | Skips CrowdSec middleware |
| `custom_content_security_policy` | null | Custom CSP header |

### After migration, delete:
1. The raw `kubernetes_ingress_v1` resource
2. Any manually defined `kubernetes_manifest "rybbit_analytics"` (the factory creates this automatically when `rybbit_site_id` is set)

## Gotchas

### Duplicate module names
If the service directory has multiple `.tf` files (e.g., `main.tf` and `frame.tf`), check
for existing `module "ingress"` blocks. Module names must be unique within a directory.
Use a descriptive name like `module "ingress-immich"` instead.

### Terraform target module names with hyphens
Module names in `terraform state list` may use hyphens (e.g., `module.real-estate-crawler`).
When using `-target`, you must match the exact name including hyphens:
```bash
# Wrong - underscores:
terraform apply -target=module.kubernetes_cluster.module.real_estate_crawler

# Correct - hyphens (quote to prevent shell interpretation):
terraform apply '-target=module.kubernetes_cluster.module.real-estate-crawler'
```

### Service name defaults
The factory defaults `service_name` to `name`. If the K8s service has a different name
than the ingress, you must explicitly set `service_name`. Common case: headscale has one
K8s service named `headscale` with multiple ports, so the UI ingress needs
`service_name = "headscale"` even though `name = "headscale-ui"`.

### Servarr subdirectory source path
Services under `servarr/` need `../../ingress_factory` as the source path instead of
`../ingress_factory`.

## Verification
1. `terraform validate` - check for syntax errors
2. `terraform plan -target=module.kubernetes_cluster.module.<service>` - verify old ingress destroyed, new created
3. `kubectl get ingress -n <namespace>` - verify ingress exists with correct host/paths
4. Browse the service URL to confirm accessibility

## Notes
- Services using special protocols (gRPC, mTLS, WebSocket with custom headers) should NOT
  be migrated - keep raw `kubernetes_ingress_v1` for those
- The factory automatically includes: rate-limit, CSP headers, CrowdSec, and entrypoint=websecure
- When `rybbit_site_id` is set, the factory creates a `kubernetes_manifest` for the
  rewrite-body middleware that injects the analytics script into HTML responses
