---
name: cloud-deploy-blueprint
description: End-to-end cloud deployment skill for Kubernetes (AKS/GKE/DOKS) with CI/CD pipelines. Covers managed services integration (Neon, Upstash), ingress configuration, SSL certificates, GitHub Actions workflows with selective builds, and Next.js build-time vs runtime environment handling. Battle-tested from 9-hour deployment session.
version: 1.0.0
---

# Cloud Deploy Blueprint

## Overview

This skill captures the complete knowledge for deploying a multi-service application to cloud Kubernetes, based on battle-tested learnings from deploying TaskFlow (5 microservices) to Azure AKS.

## When to Use

- Deploying to AKS, GKE, or DOKS
- Setting up CI/CD with GitHub Actions
- Integrating managed services (Neon PostgreSQL, Upstash Redis)
- Configuring ingress with SSL certificates
- Handling Next.js `NEXT_PUBLIC_*` variables in Docker/K8s

## Architecture Pattern

```
                         INTERNET
                             │
                             ▼
                    ┌─────────────────┐
                    │  Load Balancer  │  (Single Public IP)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Ingress (Traefik│  Routes by subdomain
                    │   or nginx)     │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
  ┌──────────┐        ┌──────────┐        ┌──────────┐
  │   Web    │        │   SSO    │        │   MCP    │
  │ (PUBLIC) │        │ (PUBLIC) │        │ (PUBLIC) │
  └────┬─────┘        └────┬─────┘        └────┬─────┘
       │                   │                   │
       │              ┌────▼─────┐             │
       └──────────────►   API    ◄─────────────┘
                      │(INTERNAL)│
                      └────┬─────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      ┌─────────────┐           ┌─────────────┐
      │    Neon     │           │   Upstash   │
      │ (Postgres)  │           │   (Redis)   │
      │  EXTERNAL   │           │  EXTERNAL   │
      └─────────────┘           └─────────────┘
```

## Critical Concept: Build-Time vs Runtime Variables

### The Problem

Next.js `NEXT_PUBLIC_*` variables are **embedded at build time**, not runtime. This means:

```dockerfile
# WRONG: Setting NEXT_PUBLIC_* at runtime does NOTHING
ENV NEXT_PUBLIC_API_URL=https://api.example.com

# RIGHT: Must be set as build ARG
ARG NEXT_PUBLIC_API_URL=https://api.example.com
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
```

### The Solution

1. **In Dockerfile**: Use ARG for NEXT_PUBLIC_* variables
2. **In CI/CD**: Pass --build-arg with domain-specific values
3. **In values.yaml**: These are NOT runtime configurable

### Build-Time Variables (Next.js)

| Service | Variable | Purpose |
|---------|----------|---------|
| Web | `NEXT_PUBLIC_SSO_URL` | SSO endpoint for browser OAuth |
| Web | `NEXT_PUBLIC_API_URL` | API endpoint for browser fetch |
| Web | `NEXT_PUBLIC_APP_URL` | App URL for redirects |
| SSO | `NEXT_PUBLIC_BETTER_AUTH_URL` | Better Auth URL for browser |
| SSO | `NEXT_PUBLIC_CONTINUE_URL` | Redirect after email verify |

### Runtime Variables (ConfigMaps/Secrets)

| Service | Variable | Source |
|---------|----------|--------|
| SSO | `DATABASE_URL` | Secret (Neon) |
| SSO | `BETTER_AUTH_SECRET` | Secret |
| API | `SSO_URL` | ConfigMap (internal K8s URL) |
| MCP | `TASKFLOW_SSO_URL` | ConfigMap (internal K8s URL) |

## Internal K8s Service Names

Services communicate via K8s service names, NOT public URLs:

```yaml
# CORRECT - Internal communication
SSO_URL: http://sso-platform:3001
API_URL: http://taskflow-api:8000

# WRONG - Don't use public URLs for internal traffic
SSO_URL: https://sso.example.com
```

## GitHub Actions CI/CD Pattern

### Selective Builds with Path Filters

```yaml
jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
    steps:
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            api:
              - 'apps/api/**'
            web:
              - 'apps/web/**'

  build-api:
    needs: changes
    if: needs.changes.outputs.api == 'true' || github.event_name == 'workflow_dispatch'
```

### Next.js Build Args Pattern

```yaml
- name: Build and push (web)
  uses: docker/build-push-action@v5
  with:
    build-args: |
      NEXT_PUBLIC_SSO_URL=https://sso.${{ vars.DOMAIN }}
      NEXT_PUBLIC_API_URL=https://api.${{ vars.DOMAIN }}
      NEXT_PUBLIC_APP_URL=https://${{ vars.DOMAIN }}
```

## GitHub Secrets & Variables

### Secrets (Sensitive)

```
NEON_SSO_DATABASE_URL
NEON_API_DATABASE_URL
NEON_CHATKIT_DATABASE_URL
NEON_NOTIFICATION_DATABASE_URL
UPSTASH_REDIS_HOST
UPSTASH_REDIS_PASSWORD
REDIS_URL
REDIS_TOKEN
BETTER_AUTH_SECRET
OPENAI_API_KEY
SMTP_USER
SMTP_PASSWORD
AZURE_CREDENTIALS (or GCP_CREDENTIALS)
```

### Variables (Non-sensitive)

```
DOMAIN=example.com
CLOUD_PROVIDER=azure
AZURE_RESOURCE_GROUP=myapp-rg
AZURE_CLUSTER_NAME=myapp-cluster
INGRESS_CLASS=traefik
```

## Helm Values Pattern

### values-cloud.yaml (Committed, Non-sensitive defaults)

```yaml
global:
  domain: ""  # Set via --set
  namespace: taskflow
  imagePullPolicy: Always

managedServices:
  neon:
    enabled: true
    # Connection strings injected via --set from secrets
  upstash:
    enabled: true
    # Credentials injected via --set from secrets

sso:
  enabled: true
  name: sso-platform
  postgresql:
    enabled: false  # Using Neon
  env:
    NODE_ENV: production
    BETTER_AUTH_URL: ""  # Set via --set
```

### Helm --set Pattern

```bash
helm upgrade --install taskflow ./infrastructure/helm/taskflow \
  --values values-cloud.yaml \
  --set global.imageRegistry="ghcr.io/owner/repo" \
  --set global.imageTag="${{ github.sha }}" \
  --set "managedServices.neon.ssoDatabase=${{ secrets.NEON_SSO_DATABASE_URL }}" \
  --set "sso.env.BETTER_AUTH_SECRET=${{ secrets.BETTER_AUTH_SECRET }}"
```

## CRITICAL: CPU Architecture Check

**BEFORE ANY DEPLOYMENT**, check your cluster's node architecture:

```bash
kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.architecture}'
```

- `amd64` → Use `platforms: linux/amd64`
- `arm64` → Use `platforms: linux/arm64`

**ARM64 is increasingly common** (Azure, AWS Graviton, Apple Silicon dev). Don't assume amd64!

### Docker Build for Correct Architecture

```yaml
- uses: docker/build-push-action@v5
  with:
    platforms: linux/arm64      # MATCH YOUR CLUSTER!
    provenance: false           # Avoid manifest issues
    no-cache: true              # When debugging
```

**Why `provenance: false`?**
Buildx attestation creates complex manifest lists that can cause "no match for platform" errors. Disable for simple, reliable images.

## Common Gotchas (Battle-Tested)

### 1. Logout Redirect to 0.0.0.0

**Problem:** `request.url` in K8s returns container bind address
**Solution:** Use `NEXT_PUBLIC_APP_URL` env var for redirects

```typescript
// WRONG
const response = NextResponse.redirect(new URL("/", request.url));

// RIGHT
const APP_URL = process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";
const response = NextResponse.redirect(new URL("/", APP_URL));
```

### 2. Email Verification Redirect to localhost

**Problem:** Missing `NEXT_PUBLIC_CONTINUE_URL` in SSO Dockerfile
**Solution:** Add to Dockerfile and CD pipeline:

```dockerfile
ARG NEXT_PUBLIC_CONTINUE_URL=http://localhost:3000
ENV NEXT_PUBLIC_CONTINUE_URL=$NEXT_PUBLIC_CONTINUE_URL
```

### 3. Browser Making Requests to localhost

**Problem:** `NEXT_PUBLIC_*` not passed as build arg
**Solution:** Check ALL `NEXT_PUBLIC_*` variables systematically:

```bash
grep -r "NEXT_PUBLIC_" apps/web/src --include="*.ts" --include="*.tsx" | \
  grep -oE "NEXT_PUBLIC_[A-Z_]+" | sort -u
```

### 4. Hardcoded Sensitive Data

**Problem:** Email/passwords hardcoded in values files
**Solution:** Use `--set` from GitHub Secrets for ALL sensitive data

### 5. Missing Database Sections in values.yaml

**Problem:** Helm templates expect `database.host`, `postgresql.name` etc.
**Solution:** Include empty/default sections even for managed services:

```yaml
postgresql:
  enabled: false
  name: sso-platform-postgres

database:
  host: ""
  port: "5432"
  name: taskflow_sso
  user: postgres
```

## SSL Certificate Pattern (cert-manager)

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: traefik
```

## Ingress Annotations for TLS

```yaml
annotations:
  cert-manager.io/cluster-issuer: letsencrypt-prod
  traefik.ingress.kubernetes.io/router.tls: "true"
```

## Pre-Deployment Checklist

### Code Changes
- [ ] All `NEXT_PUBLIC_*` vars documented and in Dockerfiles
- [ ] Redirect URLs use env vars, not `request.url`
- [ ] No hardcoded localhost in production code paths

### Dockerfiles
- [ ] All `NEXT_PUBLIC_*` as ARG and ENV
- [ ] Multi-stage build for slim production image
- [ ] Health check endpoint configured

### CI/CD Pipeline
- [ ] Build args for Next.js apps
- [ ] Path filters for selective builds
- [ ] All secrets listed and documented
- [ ] Helm --set for all sensitive values

### Helm Chart
- [ ] values-cloud.yaml has all required sections
- [ ] No sensitive data in committed files
- [ ] Internal service names for inter-service communication
- [ ] Ingress configured with correct class

### GitHub Setup
- [ ] All secrets created in repository settings
- [ ] All variables created in repository settings
- [ ] Azure/GCP credentials configured

## Related Skills

- `aks-deployment-troubleshooter` - Debug ImagePullBackOff, CrashLoopBackOff, architecture issues
- `containerize-apps` - Dockerization patterns
- `helm-charts` - Helm chart structure
- `kubernetes-essentials` - K8s fundamentals
- `better-auth-sso` - SSO integration

## Related Agents

- `impact-analyzer-agent` - Pre-containerization analysis
