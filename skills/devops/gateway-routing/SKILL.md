---
name: gateway-routing
description: |
  Gateway API routing, TLS certificates, and WAF configuration for the homelab Kubernetes platform.

  Use when: (1) Exposing a service via HTTPRoute, (2) Choosing between internal and external gateways,
  (3) Setting up TLS certificates with cert-manager, (4) Debugging TLS or routing issues,
  (5) Understanding WAF (Coraza) behavior and tuning, (6) Testing WAF-protected endpoints.

  Triggers: "httproute", "gateway", "expose service", "add route", "certificate", "tls",
  "coraza", "waf", "internal gateway", "external gateway", "dns", "ingress",
  "routing", "cert-manager", "letsencrypt", "homelab-ca"
user-invocable: false
---

# Gateway Routing

The homelab uses Kubernetes Gateway API with Istio as the gateway controller. Two gateways handle traffic:
- **internal** -- accessible only within the home network
- **external** -- accessible from the internet, protected by Coraza WAF

All gateway resources live in the `istio-gateway` namespace. HTTPRoutes in any namespace reference these gateways via `parentRefs`.

## Gateway Selection Decision Tree

```
Does this service need internet access?
|
+-- YES --> external gateway
|           - Domain: *.${external_domain}
|           - TLS: letsencrypt-production (Cloudflare DNS-01)
|           - WAF: Coraza OWASP CRS active
|           - IP: ${external_ingress_ip} (Cilium LB)
|
+-- NO  --> internal gateway
|           - Domain: *.${internal_domain}
|           - TLS: homelab-ca (self-signed CA)
|           - WAF: None
|           - IP: ${internal_ingress_ip} (Cilium LB)
|
+-- BOTH -> Create two HTTPRoutes (one per gateway)
            Examples: Authelia, Immich, Kromgo
```

**Rule of thumb**: Most platform dashboards (Grafana, Prometheus, Alertmanager, Longhorn, Hubble, Garage) are internal-only. User-facing apps (Authelia, Immich, Zipline) need external access and often also an internal route for LAN users.

## Creating an HTTPRoute

### Step 1: Choose Gateway and Hostname

Determine which gateway (or both) your service needs and the subdomain.

### Step 2: Create the HTTPRoute YAML

Internal-only route (most common for platform services):

```yaml
---
# yaml-language-server: $schema=https://kubernetes-schemas.pages.dev/gateway.networking.k8s.io/httproute_v1.json
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app
spec:
  parentRefs:
    - name: internal
      namespace: istio-gateway
  hostnames:
    - "my-app.${internal_domain}"
  rules:
    - backendRefs:
        - name: my-app-service
          port: 8080
```

External route (internet-facing, WAF-protected):

```yaml
---
# yaml-language-server: $schema=https://kubernetes-schemas.pages.dev/gateway.networking.k8s.io/httproute_v1.json
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: my-app-external
  namespace: my-app
spec:
  parentRefs:
    - name: external
      namespace: istio-gateway
  hostnames:
    - "my-app.${external_domain}"
  rules:
    - backendRefs:
        - name: my-app-service
          port: 8080
```

### Step 3: Place the Route File

| Service Type | Location | Example |
|-------------|----------|---------|
| Platform service | `kubernetes/platform/config/<subsystem>/` | `config/monitoring/grafana-route.yaml` |
| Cluster-specific app | `kubernetes/clusters/<cluster>/config/<app>/` | `clusters/live/config/authelia/external-route.yaml` |

Add the route file to the subsystem's `kustomization.yaml`.

### Step 4: Network Policy

Ensure the app namespace has the correct network policy profile label:

| Gateway Used | Required Profile |
|-------------|-----------------|
| Internal only | `internal` or `internal-egress` |
| External only | `standard` |
| Both | `standard` |

Set in `kubernetes/platform/namespaces.yaml`:

```yaml
- name: my-app
  labels:
    network-policy.homelab/profile: standard
```

## parentRefs Structure

The `parentRefs` field links an HTTPRoute to a Gateway listener. Key details:

```yaml
parentRefs:
  - name: internal          # Gateway name: "internal" or "external"
    namespace: istio-gateway # Gateways live in istio-gateway namespace
    sectionName: https       # Optional: target specific listener (https or http)
```

- **namespace** is required when the HTTPRoute is in a different namespace than the Gateway (which is always the case -- gateways are in `istio-gateway`, routes are in app namespaces or the gateway namespace for platform routes)
- **sectionName** is optional. Omit it to match any listener. Use `http` only for redirect routes.
- Both gateways use `allowedRoutes.namespaces.from: All` on the HTTPS listener, so any namespace can attach routes.

## Route Patterns from the Codebase

### Simple Backend (most common)

```yaml
rules:
  - backendRefs:
      - name: service-name
        port: 80
```

Used by: Grafana, Longhorn, Hubble, Alertmanager, Prometheus, Garage, Kromgo.

### Dual Gateway Exposure (external + internal)

Create two separate HTTPRoute resources, one per gateway. Examples:

- `authelia-external` + `authelia-internal` (same backend, different gateways/domains)
- `immich-external` + `immich-internal`
- `kromgo-external` + `kromgo-internal`

The routes are identical except for `parentRefs.name` and `hostnames` domain.

### HTTP-to-HTTPS Redirect (platform-managed)

Both gateways have automatic HTTP-to-HTTPS redirects configured in `config/gateway/http-to-https-redirect.yaml`. You do not need to create redirect routes for new services.

## TLS Certificate Setup

### Architecture

Certificates are provisioned at the gateway level, not per-route. Each gateway has a wildcard certificate:

| Gateway | Certificate | Secret | Issuer | Domain |
|---------|------------|--------|--------|--------|
| external | `external` | `external-tls` | `${tls_issuer:-cloudflare}` | `*.${external_domain}` |
| internal | `internal` | `internal-tls` | `${tls_issuer:-cloudflare}` | `*.${internal_domain}` |

The `tls_issuer` variable defaults to `cloudflare` (Let's Encrypt DNS-01) but can be overridden to `homelab-ca` per cluster via `.cluster-vars.env`.

### ClusterIssuers

| Issuer Name | Type | Use Case | Secret Source |
|------------|------|----------|---------------|
| `cloudflare` | ACME (DNS-01) | Public certs via Let's Encrypt | ExternalSecret from SSM (`cloudflare-api-token`) |
| `homelab-ca` | CA | Internal services, dev/integration clusters | ExternalSecret from SSM (`homelab-ingress-root-ca`) |
| `istio-mesh-ca` | CA | Istio mesh mTLS (workload identity) | ExternalSecret from SSM (shared across clusters) |

### Adding a New Subdomain

No certificate changes needed -- the wildcard `*.${external_domain}` and `*.${internal_domain}` cover all subdomains. Just create the HTTPRoute.

### Debugging TLS Issues

```bash
# Check certificate status
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get certificates -n istio-gateway

# Check certificate details (Ready condition)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl describe certificate external -n istio-gateway

# Check issuer health
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get clusterissuers

# Check CertificateRequests (shows issuance attempts)
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get certificaterequests -n istio-gateway

# Check the actual TLS secret
KUBECONFIG=~/.kube/<cluster>.yaml kubectl get secret external-tls -n istio-gateway -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -text

# If cert is stuck, check cert-manager logs
KUBECONFIG=~/.kube/<cluster>.yaml kubectl logs -n cert-manager deploy/cert-manager -f
```

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Certificate not Ready | Issuer secret missing | Check ExternalSecret sync for `cloudflare-api-token` |
| ACME challenge failing | DNS propagation / API token issue | Verify Cloudflare token has Zone:DNS:Edit permission |
| `homelab-ca` not Ready | Root CA secret missing | Check ExternalSecret for `homelab-ingress-root-ca` |
| Browser TLS warning (internal) | Self-signed CA not trusted | Expected for `homelab-ca`; add CA to trusted store or use `-k` flag |

## Coraza WAF (External Gateway Only)

### How It Works

The Coraza Web Application Firewall runs as an Istio WasmPlugin attached only to the external gateway:

```yaml
# kubernetes/platform/config/gateway/coraza-wasm-plugin.yaml
apiVersion: extensions.istio.io/v1alpha1
kind: WasmPlugin
metadata:
  name: coraza-waf
spec:
  selector:
    matchLabels:
      gateway.networking.k8s.io/gateway-name: external  # External only
  url: oci://ghcr.io/corazawaf/coraza-proxy-wasm:0.6.0@sha256:...
  phase: AUTHN             # Runs before authentication
  failStrategy: FAIL_OPEN  # Traffic flows if WAF errors
  pluginConfig:
    directives_map:
      default:
        - Include @recommended-conf
        - Include @crs-setup-conf
        - Include @owasp_crs/*.conf
        - SecRuleEngine On
        - SecAction "id:900000,phase:1,pass,t:none,nolog,setvar:tx.blocking_paranoia_level=1"
```

Key settings:
- **Paranoia Level 1**: Lowest false positive rate, catches common attacks
- **FAIL_OPEN**: Prioritizes availability over security -- if WASM fails to load, traffic passes unfiltered
- **AUTHN phase**: WAF runs early in the filter chain, before any authentication checks
- **External only**: Internal gateway traffic is not filtered by WAF

### FAIL_OPEN Implications

If the WASM binary fails to load (wrong digest, image unavailable, OOM), traffic flows unfiltered. Check gateway pod logs for:

```
error in converting the wasm config to local: cannot fetch Wasm module...
applying allow RBAC filter
```

### WAF Rule Customization

Rules are inlined in the WasmPlugin spec (Istio WasmPlugin does not support volume mounts). The `coraza-config.yaml` ConfigMap serves as documentation only.

To disable a rule causing false positives:

```yaml
# Add to the directives_map.default array in coraza-wasm-plugin.yaml
- SecRuleRemoveById 920350  # Example: Host header validation
```

### Testing WAF-Protected Endpoints

Istio gateway listeners match on SNI (Server Name Indication). Raw IP requests are rejected:

```bash
# WRONG -- no SNI, connection reset
curl -kI "https://192.168.10.53/"

# CORRECT -- send proper SNI with --resolve
GATEWAY_IP=$(KUBECONFIG=~/.kube/<cluster>.yaml kubectl get gateway external -n istio-gateway -o jsonpath='{.metadata.annotations.lbipam\.cilium\.io/ips}')
curl -kI --resolve "app.${external_domain}:443:${GATEWAY_IP}" \
  "https://app.${external_domain}/"
```

### Attack Pattern Verification (expect 403)

```bash
# SQL Injection
curl -k --resolve "app.${external_domain}:443:${GATEWAY_IP}" \
  "https://app.${external_domain}/?id=1'%20OR%20'1'='1"

# XSS
curl -k --resolve "app.${external_domain}:443:${GATEWAY_IP}" \
  "https://app.${external_domain}/?q=<script>alert(1)</script>"

# Command Injection
curl -k --resolve "app.${external_domain}:443:${GATEWAY_IP}" \
  "https://app.${external_domain}/?cmd=;cat%20/etc/passwd"
```

### WAF Monitoring

| Metric | What It Shows |
|--------|--------------|
| `istio_requests_total{source_workload=~"external-istio", response_code="403"}` | WAF-blocked requests |
| `istio_requests_total{source_workload=~"external-istio"}` | Total external gateway traffic |

Alerts configured in `config/gateway/coraza-waf-rules.yaml`:

| Alert | Condition | Meaning |
|-------|-----------|---------|
| `CorazaWAFDegraded` | No Istio metrics from external gateway for 5m | Gateway may not be processing traffic |
| `CorazaWAFHighBlockRate` | >10% of requests returning 403 for 10m | Possible attack or WAF false positives |
| `CorazaWAFHighLatency` | p99 gateway latency >50ms for 5m | WAF overhead too high, tune rule exclusions |

## Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Route not working | Missing `namespace: istio-gateway` in `parentRefs` | Add namespace to parentRefs |
| 404 on valid hostname | HTTPRoute not attached to gateway | Check `parentRefs` gateway name matches exactly |
| Connection reset on external | SNI mismatch (testing with IP) | Use `--resolve` flag with proper hostname |
| Pods unreachable from gateway | Missing network policy profile | Add `network-policy.homelab/profile` label to namespace |
| 503 Service Unavailable | Backend service not found or port wrong | Verify service name and port in `backendRefs` |
| Both internal and external needed | Only one route created | Create two separate HTTPRoute resources |
| WAF blocking legitimate traffic | False positive on CRS rule | Add `SecRuleRemoveById <ID>` to WasmPlugin directives |

## Cross-References

| Document | Focus |
|----------|-------|
| `kubernetes/platform/config/gateway/` | Gateway definitions, WAF config |
| `kubernetes/platform/config/issuers/` | ClusterIssuer definitions |
| `kubernetes/platform/config/certs/` | Certificate resources |
| `kubernetes/platform/config/network-policy/CLAUDE.md` | Network policy profiles |
| `kubernetes/platform/CLAUDE.md` | Variable substitution, platform structure |
| `deploy-app` skill | Full app deployment workflow including routing |
