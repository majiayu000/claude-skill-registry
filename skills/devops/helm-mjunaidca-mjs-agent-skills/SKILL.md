---
name: helm
description: |-
  Production-grade Helm 4 chart development, release management, and debugging.
  This skill should be used when users ask to create Helm charts, deploy with Helm,
  manage releases (install/upgrade/rollback), push charts to OCI registries, debug
  failed deployments, configure chart dependencies, create umbrella charts, set up
  GitOps with ArgoCD/Flux, or troubleshoot Helm issues. Auto-detects from Dockerfile/code,
  generates production-hardened charts with library patterns. Complements kubernetes skill.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/verify-helm-context.sh"
---

# Helm

Helm 4 chart development and operations with security-first defaults.

## What This Skill Does

**Chart Development:**
- Creates production charts with library pattern (reusable base + thin apps)
- Generates templates, helpers, hooks, and dependencies
- Auto-detects from Dockerfile: ports, health endpoints, resources
- Supports umbrella charts for multi-service deployments
- Adds values schema validation (JSON Schema)

**Release Management:**
- Install, upgrade, rollback with atomic operations
- Release history and status inspection
- Values precedence management across environments
- Hook lifecycle (pre-install, pre-upgrade, post-upgrade, test)

**Registry & Distribution:**
- OCI registry workflows (push, pull, digest pinning)
- Chart versioning and artifact management
- GitOps integration (ArgoCD, Flux)

**Debugging:**
- Template rendering and debugging workflow
- Failed release recovery (stuck states, hook failures)
- Values resolution tracing
- Policy validation (OPA/Kyverno, security scanning)

## What This Skill Does NOT Do

- Generate raw Kubernetes manifests (use kubernetes skill)
- Create Kustomize-only overlays without Helm
- Deploy Operators/CRDs (chart can include, but not operator setup)
- Manage cluster infrastructure (use kubernetes skill)
- Handle non-Helm deployments

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Dockerfile, existing charts, values patterns |
| **Conversation** | Target environment, chart name, special requirements |
| **Skill References** | Chart patterns, Helm 4 features, hooks, security |
| **kubernetes skill** | Manifest patterns for templates (complementary) |

---

## Required Clarifications

After auto-detection, confirm if ambiguous:

| Question | When to Ask |
|----------|-------------|
| Chart type | "Creating new chart, library chart, or umbrella chart?" |
| Target registry | "OCI registry (GHCR, ECR, Harbor) or Git repo for GitOps?" |
| Environment strategy | "Single values file or per-environment overlays (dev/staging/prod)?" |
| Release namespace | "Deploy to specific namespace or chart-managed?" |

---

## Helm 4 Defaults (CRITICAL)

Helm 4 introduces breaking changes from v3:

| Feature | Helm 4 Behavior | Notes |
|---------|-----------------|-------|
| **Server-Side Apply** | Default ON | Better conflict detection, GitOps alignment |
| **kstatus watching** | Accurate health | Replaces old `--wait` behavior |
| **OCI-first** | Native support | `oci://` protocol, digest pinning |
| **Wasm plugins** | Sandboxed | Post-renderers require plugin format |

See `references/helm4-features.md` for migration guidance.

---

## Auto-Detection Matrix

### From Dockerfile

| Detect | How | Chart Generation |
|--------|-----|------------------|
| Port | EXPOSE | `containerPort` in deployment template |
| Health | CMD pattern | Liveness/readiness probe paths |
| User | USER instruction | `securityContext.runAsUser` |
| Base image | FROM | Resource hints (alpine=small, python=medium) |

### From Code

| Detect | How | Chart Generation |
|--------|-----|------------------|
| Framework | imports/deps | Health endpoint patterns |
| GPU deps | torch, tensorflow | tolerations, nodeSelector, GPU resources |
| Sidecar needs | dapr.io, istio | Annotations for injection |

---

## Workflow

```
1. PRE-FLIGHT
   - Verify helm version (v4.x required)
   - Check target registry/cluster access
   - Identify existing charts
         ↓
2. ANALYZE PROJECT
   - Read Dockerfile for detection
   - Scan code for patterns
   - Check existing values patterns
         ↓
3. DETERMINE CHART TYPE
   - Application chart (default)
   - Library chart (reusable templates)
   - Umbrella chart (multi-service)
         ↓
4. GENERATE CHART
   - Chart.yaml with dependencies
   - values.yaml with schema
   - Templates with helpers
   - Hooks if lifecycle needs
         ↓
5. VALIDATE
   - helm lint
   - helm template --debug
   - helm install --dry-run
   - Policy validation (optional)
         ↓
6. DELIVER
   - Chart in charts/ directory
   - Summary of what was created
   - Next steps (push to registry, GitOps setup)
```

---

## Chart Structure (Library Pattern)

```
charts/
├── myapp-lib/                    # Library chart (reusable)
│   ├── Chart.yaml                # type: library
│   ├── templates/
│   │   ├── _deployment.tpl       # Reusable deployment template
│   │   ├── _service.tpl          # Reusable service template
│   │   ├── _helpers.tpl          # Common helpers
│   │   └── _security.tpl         # Security context helpers
│   └── values.yaml               # Default values
│
└── myapp/                        # Application chart (thin)
    ├── Chart.yaml                # Dependencies: myapp-lib
    ├── templates/
    │   ├── deployment.yaml       # {{ include "myapp-lib.deployment" . }}
    │   ├── service.yaml          # {{ include "myapp-lib.service" . }}
    │   └── _helpers.tpl          # App-specific helpers
    ├── values.yaml               # App defaults
    ├── values.schema.json        # Schema validation
    └── values/                   # Environment overlays
        ├── dev.yaml
        ├── staging.yaml
        └── prod.yaml
```

---

## Core Templates

### Chart.yaml (Application)

```yaml
apiVersion: v2
name: myapp
version: 0.1.0                    # Chart version (SemVer)
appVersion: "1.0.0"               # App version
type: application                 # or: library
description: |
  Brief description of what this chart deploys.

# Dependencies (subchart pattern)
dependencies:
  - name: myapp-lib
    version: ">=0.1.0"
    repository: "oci://ghcr.io/myorg/charts"
  - name: redis
    version: "17.x.x"
    repository: "oci://registry-1.docker.io/bitnamicharts"
    condition: redis.enabled      # Conditional dependency

# Kubernetes version constraint
kubeVersion: ">=1.25.0"

# Maintainers
maintainers:
  - name: DevRaftel
    email: team@devraftel.com
```

### values.yaml (Structured)

```yaml
# -- Number of replicas
replicaCount: 2

image:
  # -- Container image repository
  repository: myorg/myapp
  # -- Image pull policy
  pullPolicy: IfNotPresent
  # -- Image tag (defaults to appVersion)
  tag: ""

# -- Resource requests and limits
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"

# -- Security context (pod level)
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# -- Security context (container level)
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop: ["ALL"]

# -- Service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: 8080

# -- Health probes
probes:
  liveness:
    path: /health/live
    initialDelaySeconds: 10
  readiness:
    path: /health/ready
    initialDelaySeconds: 5

# -- Enable autoscaling
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilization: 80
```

---

## Command Reference

### Chart Development

```bash
# Create new chart
helm create myapp

# Lint chart
helm lint ./myapp

# Render templates locally
helm template myapp ./myapp -f values.yaml

# Render with debug (shows template errors)
helm template myapp ./myapp --debug 2>&1 | head -100

# Package chart
helm package ./myapp

# Update dependencies
helm dependency update ./myapp
helm dependency build ./myapp
```

### Release Management

```bash
# Install release
helm install myapp ./myapp -n namespace --create-namespace

# Install with atomic (rollback on failure)
helm install myapp ./myapp --atomic --timeout 5m

# Upgrade release
helm upgrade myapp ./myapp --atomic

# Upgrade or install
helm upgrade --install myapp ./myapp

# Rollback to previous
helm rollback myapp 1

# Uninstall
helm uninstall myapp -n namespace

# Release status
helm status myapp
helm history myapp
```

### OCI Registry

```bash
# Login to registry
helm registry login ghcr.io -u USERNAME

# Push chart to OCI
helm push myapp-0.1.0.tgz oci://ghcr.io/myorg/charts

# Pull from OCI
helm pull oci://ghcr.io/myorg/charts/myapp --version 0.1.0

# Install from OCI
helm install myapp oci://ghcr.io/myorg/charts/myapp --version 0.1.0
```

### Debugging

```bash
# Get release manifest
helm get manifest myapp

# Get computed values
helm get values myapp
helm get values myapp --all  # Including defaults

# Get hooks
helm get hooks myapp

# Dry-run against cluster
helm install myapp ./myapp --dry-run --debug

# Diff before upgrade (requires helm-diff plugin)
helm diff upgrade myapp ./myapp
```

---

## Validation Pipeline

Before delivering charts, run:

```bash
# 1. Lint
helm lint ./myapp --strict

# 2. Template render
helm template myapp ./myapp --debug > /dev/null

# 3. Dry-run against cluster
helm install myapp ./myapp --dry-run --debug -n test

# 4. Schema validation (if values.schema.json exists)
helm lint ./myapp  # Automatically validates against schema

# 5. Policy validation (optional)
# OPA/Conftest
conftest test ./myapp/templates/

# Trivy for security scanning
trivy config ./myapp/
```

---

## Output Checklist

Before delivering, verify:

### Chart Structure
- [ ] Chart.yaml has apiVersion: v2, valid version, kubeVersion
- [ ] values.yaml has comments for helm-docs
- [ ] values.schema.json for validation
- [ ] Templates use `_helpers.tpl` for reusable definitions

### Security
- [ ] `securityContext` in values with secure defaults
- [ ] No secrets in values.yaml (use external secrets)
- [ ] `runAsNonRoot: true` in pod security context
- [ ] Resource limits defined

### Best Practices
- [ ] Labels follow `app.kubernetes.io/*` standard
- [ ] Health probes configurable via values
- [ ] Supports multiple environments (values overlays)
- [ ] Hooks have deletion policies

### Validation
- [ ] `helm lint` passes without warnings
- [ ] `helm template --debug` renders successfully
- [ ] `helm install --dry-run` succeeds against cluster

### GitOps Ready
- [ ] Chart versioned with SemVer
- [ ] OCI-pushable (no local dependencies)
- [ ] ArgoCD/Flux compatible structure

---

## Reference Files

### Always Read First

| File | Purpose |
|------|---------|
| `references/chart-development.md` | **CRITICAL**: Template syntax, helpers, hooks |
| `references/values-patterns.md` | **CRITICAL**: Precedence, environments, schema |
| `references/helm4-features.md` | **CRITICAL**: SSA, Wasm, kstatus, OCI |

### Operations

| File | When to Read |
|------|--------------|
| `references/release-management.md` | Install, upgrade, rollback, atomic |
| `references/oci-workflows.md` | Push, pull, registry auth, digest |
| `references/debugging-workflow.md` | Template errors, failed releases |
| `references/testing-validation.md` | Lint, unittest, dry-run, integration tests |

### Integration

| File | When to Read |
|------|--------------|
| `references/gitops-integration.md` | ArgoCD, Flux, ApplicationSet |
| `references/umbrella-patterns.md` | Multi-service, subcharts, Kustomize |
| `references/ai-agent-patterns.md` | GPU, models, sidecars, KEDA |

### Security & Compliance

| File | When to Read |
|------|--------------|
| `references/security-patterns.md` | Secrets (ESO, Sealed), RBAC, policies |
| `references/hooks-lifecycle.md` | Hook types, weights, deletion policies |
