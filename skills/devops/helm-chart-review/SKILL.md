---
name: helm-chart-review
description: Conduct comprehensive Helm chart security and quality audits with automated checks for security contexts, resource limits, and production readiness. Use when reviewing pull requests with Helm chart changes, conducting pre-release chart audits, security scanning Helm manifests, validating chart structure and best practices, or preparing charts for production deployment.
version: 1.0.0
---

# Helm Chart Review

## Purpose

Provide comprehensive review checklists and automated validation for ensuring Helm charts meet production quality and security standards before deployment.

## Complete Review Workflow

### Step 1: Run Automated Validation

```bash
# Lint checks
helm lint ./charts/mychart

# Template rendering validation
helm template mychart ./charts/mychart --debug

# Test with different value files
helm template mychart ./charts/mychart -f values-prod.yaml

# Dry run installation
helm install test ./charts/mychart --dry-run --debug --namespace test
```

### Step 2: Security Review Checklist

**Critical security items (must pass):**

- [ ] **No hardcoded secrets** in values.yaml or templates
- [ ] **Image tags are specific** (no `:latest` tag)
- [ ] **Security contexts are defined** and restrictive:
  ```yaml
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    readOnlyRootFilesystem: true
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - ALL
  ```
- [ ] **RBAC is properly configured** with least privilege
- [ ] **Resource limits** are set for all containers
- [ ] **Service accounts** are explicitly created (not using default)
- [ ] **Secrets** use external secret management (not inline)

**Security red flags:**

```yaml
# ❌ NEVER allow these
securityContext:
  privileged: true # Unacceptable
  runAsUser: 0 # Root user - requires justification
  allowPrivilegeEscalation: true # Security risk

image:
  tag: latest # Non-deterministic

# Hardcoded secrets
password: "hardcoded123" # NEVER hardcode secrets
```

### Step 3: Structure Review Checklist

- [ ] **Chart.yaml** has all required fields:
  - `apiVersion: v2`
  - `name`, `description`, `type`
  - `version` (follows SemVer2)
  - `appVersion`
  - `maintainers` with contact info
- [ ] **Version follows SemVer2** format (MAJOR.MINOR.PATCH)
- [ ] **Dependencies** use version ranges (~)
- [ ] **One resource per file** in templates/
- [ ] **Template helpers** are properly namespaced
- [ ] **File naming** follows conventions (lowercase, dashes)
- [ ] **NOTES.txt** provides useful post-install information
- [ ] **README.md** exists with usage documentation

### Step 4: Values Review Checklist

- [ ] **All values are documented** with clear comments
- [ ] **Naming is consistent** (camelCase throughout)
- [ ] **Types are explicit** (strings quoted: `tag: "1.0"`)
- [ ] **Flat structure** preferred over deep nesting
- [ ] **Defaults are secure** and production-ready
- [ ] **Environment-specific values** separated (values-{env}.yaml)
- [ ] **Boolean values** use lowercase (`true`/`false`)
- [ ] **Resource requests/limits** have realistic values

**Good vs bad values:**

```yaml
# ✅ Good
replicaCount: 2 # Documented, reasonable default

image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: "" # Empty, uses appVersion

resources:
  limits:
    cpu: 500m
    memory: 256Mi
  requests:
    cpu: 250m
    memory: 128Mi

# ❌ Bad
replicas: 1 # Undocumented, single point of failure
ImageTag: latest # Wrong case, non-specific tag
database:
  password: "changeme" # Hardcoded secret
```

### Step 5: Template Review Checklist

- [ ] **Labels are consistent** and follow k8s recommendations:
  - `app.kubernetes.io/name`
  - `app.kubernetes.io/instance`
  - `app.kubernetes.io/version`
  - `app.kubernetes.io/managed-by`
- [ ] **Nil checks** for nested values (prevent nil pointer errors)
- [ ] **Whitespace properly managed** (`{{-` and `-}}` used correctly)
- [ ] **Helper functions** used for repeated logic
- [ ] **Conditionals** properly structured
- [ ] **Resources can be disabled** via values
- [ ] **Image tags** default to Chart.AppVersion
- [ ] **ConfigMap/Secret changes** trigger pod restarts (checksum annotations)
- [ ] **Names truncated** to 63 characters

**Template quality patterns:**

```yaml
# ✅ Good
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
  annotations:
    checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}

{{- if .Values.ingress.enabled }}
# ... conditional resource
{{- end }}

image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"

# Safe nil handling
{{- with .Values.tolerations }}
tolerations:
  {{- toYaml . | nindent 8 }}
{{- end }}

# ❌ Bad
name: my-app-{{ .Release.Name }}       # Hardcoded
image: {{ .Values.image }}:latest      # Hardcoded latest
{{ .Values.nested.value }}             # No nil check
```

### Step 6: Testing Review Checklist

- [ ] **helm lint** passes without errors or warnings
- [ ] **helm template** renders correctly
- [ ] **Dry run** succeeds
- [ ] **Unit tests** exist and pass (helm-unittest)
- [ ] **All conditional paths** tested (enabled/disabled features)
- [ ] **Multiple environments** tested (dev, staging, prod values)

## Security Scanning Integration

### Kubesec Analysis

```bash
# Scan rendered templates for security issues
helm template mychart ./charts/mychart | kubesec scan -

# Look for:
# - Missing security contexts
# - Privileged containers
# - Host path mounts
# - Host network usage
```

### Trivy Image Scanning

```bash
# Extract images from chart
helm template mychart ./charts/mychart | grep "image:" | sort -u

# Scan each image for vulnerabilities
trivy image myapp:1.0.0
```

## Common Review Findings and Fixes

### Finding: Missing Resource Limits

```yaml
# ❌ Problem
containers:
  - name: app
    image: myapp:1.0

# ✅ Solution
containers:
  - name: app
    image: myapp:1.0
    resources:
      limits:
        cpu: 500m
        memory: 256Mi
      requests:
        cpu: 250m
        memory: 128Mi
```

### Finding: Insecure Security Context

```yaml
# ❌ Problem
securityContext: {}

# ✅ Solution
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
```

### Finding: Latest Image Tag

```yaml
# ❌ Problem
image: myapp:latest

# ✅ Solution
image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
```

### Finding: No Liveness/Readiness Probes

```yaml
# ❌ Problem
containers:
  - name: app
    image: myapp:1.0

# ✅ Solution
containers:
  - name: app
    image: myapp:1.0
    livenessProbe:
      httpGet:
        path: /healthz
        port: http
      initialDelaySeconds: 30
      periodSeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: http
      initialDelaySeconds: 5
      periodSeconds: 5
```

## Review Severity Levels

**BLOCKER** (must fix before merge):

- Hardcoded secrets
- Missing security contexts
- Privileged containers
- No resource limits
- Use of `:latest` tag

**CRITICAL** (must fix before production):

- Missing liveness/readiness probes
- Single replica without PDB
- No pod disruption budget
- Incorrect RBAC (too permissive)

**MAJOR** (should fix):

- Undocumented values
- Missing tests
- Incomplete README
- No CHANGELOG entry

**MINOR** (nice to have):

- Improved comments
- Additional examples
- Optimization opportunities

## Pre-Release Checklist

**Before releasing chart:**

- [ ] All security review items pass
- [ ] All structure review items pass
- [ ] All tests pass (lint, unit, integration, dry-run)
- [ ] Security scanning completed (kubesec, trivy)
- [ ] Documentation updated and accurate
- [ ] CHANGELOG.md updated with version notes
- [ ] Version bumped appropriately (major/minor/patch)
- [ ] Tested in staging environment
- [ ] Rollback procedure documented
- [ ] Resource quotas validated
- [ ] Network policies tested
- [ ] Monitoring/alerting configured

## CI/CD Quality Gates

**Example pipeline checks:**

```yaml
# GitLab CI / GitHub Actions
helm-lint:
  stage: test
  script:
    - helm lint ./charts/*

helm-unittest:
  stage: test
  script:
    - helm unittest ./charts/*

helm-security-scan:
  stage: test
  script:
    - helm template ./charts/* | kubesec scan -
    - helm template ./charts/* | trivy config -

helm-dry-run:
  stage: test
  script:
    - helm install test ./charts/mychart --dry-run --debug
```

## Documentation Review

**README.md must include:**

- [ ] Chart description and purpose
- [ ] Prerequisites and dependencies
- [ ] Installation instructions
- [ ] Configuration options (values) table
- [ ] Usage examples
- [ ] Upgrade instructions

**CHANGELOG.md must track:**

- [ ] Version number and date
- [ ] Added features
- [ ] Changed behavior
- [ ] Deprecated features
- [ ] Removed features
- [ ] Fixed bugs
- [ ] Security fixes

## Resources

- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Chart Testing](https://github.com/helm/chart-testing)
- [Helm Unittest Plugin](https://github.com/helm-unittest/helm-unittest)
- [Kubesec Security Scanner](https://kubesec.io/)
- [Trivy Scanner](https://trivy.dev/)

---

## Related Agent

For comprehensive Helm/Kubernetes guidance that coordinates this and other Helm skills, use the **`helm-kubernetes-expert`** agent.
