---
name: traefik
description: Traefik v3 reverse proxy and load balancer for Kubernetes and Docker. Use when configuring Traefik entrypoints, HTTP/TCP/UDP routing, IngressRoute CRDs, middlewares (auth, rate limiting, headers, redirects), load balancing, TLS/ACME certificates, or Kubernetes Ingress annotations.
---

# Traefik v3

Cloud-native reverse proxy and load balancer with automatic service discovery. Traefik connects incoming requests to backend services using dynamic configuration from providers (Kubernetes, Docker, etc.).

## Quick Start (Kubernetes Helm)

```bash
helm repo add traefik https://traefik.github.io/charts
helm install traefik traefik/traefik
```

**Install CRDs manually (if needed):**
```bash
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.6/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.6/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml
```

## Core Concepts

| Component | Description |
|-----------|-------------|
| **EntryPoints** | Network ports where Traefik listens (e.g., :80, :443) |
| **Routers** | Match incoming requests using rules (Host, Path, Headers) |
| **Services** | Define backend targets with load balancing |
| **Middlewares** | Transform requests/responses (auth, headers, redirects) |
| **Providers** | Configuration sources (Kubernetes, Docker, File) |

## Task Reference

### Routing Configuration
- HTTP routing rules, matchers, priority → [references/routing.md](references/routing.md)
- Rule syntax (Host, Path, Headers, Query) → [references/routing.md](references/routing.md)

### Kubernetes CRDs
- IngressRoute, Middleware, TraefikService → [references/kubernetes-crd.md](references/kubernetes-crd.md)
- Full IngressRoute examples → [references/kubernetes-crd.md](references/kubernetes-crd.md)

### Middlewares
- All available middlewares → [references/middlewares.md](references/middlewares.md)
- Auth, rate limiting, headers, redirects → [references/middlewares.md](references/middlewares.md)

### Load Balancing & Services
- Strategies, health checks, sticky sessions → [references/services.md](references/services.md)
- Mirroring, failover, weighted routing → [references/services.md](references/services.md)

### TLS & Certificates
- ACME/Let's Encrypt, TLS options → [references/tls.md](references/tls.md)
- Certificate resolvers, challenges → [references/tls.md](references/tls.md)

### EntryPoints
- Configuration, HTTP/HTTPS setup → [references/entrypoints.md](references/entrypoints.md)
- Redirections, proxy protocol → [references/entrypoints.md](references/entrypoints.md)

## Minimal IngressRoute Example

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: myapp
  namespace: default
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`myapp.example.com`)
      kind: Rule
      services:
        - name: myapp-svc
          port: 80
      middlewares:
        - name: myapp-headers
  tls:
    certResolver: letsencrypt
```

## Common CLI/Static Config

```yaml
# traefik.yml (static configuration)
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

providers:
  kubernetesCRD: {}
  kubernetesIngress: {}

certificateResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /data/acme.json
      httpChallenge:
        entryPoint: web
```

## Official Documentation
- [Traefik Docs](https://doc.traefik.io/traefik/)
- [Kubernetes CRD Reference](https://doc.traefik.io/traefik/reference/install-configuration/providers/kubernetes/kubernetes-crd/)
- [Middleware Reference](https://doc.traefik.io/traefik/reference/routing-configuration/http/middlewares/overview/)
