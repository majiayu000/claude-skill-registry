---
name: helm-chart-writing
description: Create and validate production-ready Helm charts with proper Chart.yaml structure, values organization, and template patterns. Use when creating new Helm charts from scratch, scaffolding chart directory structure, configuring Chart.yaml and values.yaml, writing template helpers and deployment manifests, or validating chart structure and syntax.
version: 1.0.0
---

# Helm Chart Writing

## Purpose
Guide the creation of production-ready Helm charts from initial scaffolding through validation, ensuring proper structure, security, and best practices.

## Quick Start Workflow

### Step 1: Create Chart Structure
```bash
helm create <chart-name>
```

This creates the standard directory structure:
```
<chart-name>/
├── Chart.yaml
├── values.yaml
├── charts/
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── _helpers.tpl
    └── NOTES.txt
```

### Step 2: Configure Chart.yaml

**Required fields for production:**
```yaml
apiVersion: v2
name: mychart
description: A production-ready Helm chart
type: application
version: 1.0.0              # Chart version (SemVer2)
appVersion: "1.16.0"        # Application version

keywords:
  - mychart
  - kubernetes

home: https://github.com/myorg/mychart
sources:
  - https://github.com/myorg/mychart

maintainers:
  - name: Your Name
    email: your.email@example.com

dependencies:
  - name: postgresql
    version: ~12.1.0        # Use version ranges (~)
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

**Key requirements:**
- ✅ Version MUST follow SemVer2 format (MAJOR.MINOR.PATCH)
- ✅ Dependencies MUST use version ranges (~) for flexibility
- ✅ Use `condition` field to allow dependency toggle
- ✅ Include maintainer contact information

### Step 3: Organize values.yaml

**Best practices for values structure:**

```yaml
# Default values for mychart

# replicaCount is the number of pod replicas
replicaCount: 2

# image contains the container image configuration
image:
  repository: myapp
  pullPolicy: IfNotPresent
  tag: ""  # Overrides the image tag (default is appVersion)

imagePullSecrets: []

nameOverride: ""
fullnameOverride: ""

# serviceAccount configuration
serviceAccount:
  create: true
  annotations: {}
  name: ""

# podSecurityContext for pod-level security
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# securityContext for container-level security
securityContext:
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: true
  allowPrivilegeEscalation: false

# service configuration
service:
  type: ClusterIP
  port: 80
  targetPort: http

# resources for container limits
resources:
  limits:
    cpu: 500m
    memory: 256Mi
  requests:
    cpu: 250m
    memory: 128Mi

# autoscaling configuration
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

nodeSelector: {}
tolerations: []
affinity: {}

# podDisruptionBudget configuration
podDisruptionBudget:
  enabled: true
  minAvailable: 1
```

**Values organization rules:**
- ✅ ALL values MUST have descriptive comments
- ✅ Use camelCase for consistency
- ✅ Quote all string values explicitly
- ✅ Prefer flat structure over deep nesting
- ✅ Set secure, production-ready defaults

### Step 4: Write Template Helpers (_helpers.tpl)

**Standard helper functions every chart needs:**

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "mychart.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "mychart.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "mychart.labels" -}}
helm.sh/chart: {{ include "mychart.chart" . }}
{{ include "mychart.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ include "mychart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "mychart.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "mychart.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

**Helper function rules:**
- ✅ Always truncate names to 63 characters (Kubernetes limit)
- ✅ Remove trailing dashes after truncation
- ✅ Use consistent naming pattern: `<chartname>.<helpername>`

### Step 5: Create Deployment Template

**Production-ready deployment:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "mychart.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "mychart.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
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
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

**Deployment requirements:**
- ✅ Add checksum annotation for ConfigMap/Secret changes
- ✅ Include both liveness and readiness probes
- ✅ Set resource limits and requests
- ✅ Support conditional autoscaling

### Step 6: Validate Chart

```bash
# Lint chart for errors
helm lint ./mychart

# Template and review output
helm template mychart ./mychart --debug

# Template with specific values file
helm template mychart ./mychart -f values-prod.yaml

# Dry run install
helm install test ./mychart --dry-run --debug
```

## Common Patterns

### Safe Nil Pointer Handling

```yaml
# ❌ Bad - can cause nil pointer errors
{{ .Values.nested.value }}

# ✅ Good - safe navigation with default
{{ .Values.nested.value | default "default" }}

# ✅ Better - with existence checks
{{- if .Values.nested }}
  {{- if .Values.nested.value }}
    {{ .Values.nested.value }}
  {{- end }}
{{- end }}
```

### Conditional Resource Creation

```yaml
{{- if .Values.ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  # ... ingress spec
{{- end }}
```

### ConfigMap Changes Trigger Pod Restart

```yaml
# Add checksum annotation to force pod restart on config change
metadata:
  annotations:
    checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
    checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
```

## File Naming Conventions

**Template files:**
- ✅ Use lowercase with dashes: `deployment.yaml`, `service-account.yaml`
- ✅ One resource type per file
- ✅ Use descriptive names: `database-secret.yaml` not `secret.yaml`

## Common Issues and Solutions

### Issue: Long resource names exceeding limits

```yaml
# Solution: Always use truncation in fullname helper
{{- define "mychart.fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
```

### Issue: Image tag not respecting appVersion

```yaml
# Solution: Use default filter in image specification
image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
```

## Testing Commands

```bash
# Create chart
helm create mychart

# Validate structure
helm lint ./mychart

# Test rendering locally
helm template ./mychart --debug

# Dry run installation
helm install test ./mychart --dry-run --debug

# Install to test namespace
helm install mychart ./mychart --namespace test --create-namespace

# Upgrade existing release
helm upgrade mychart ./mychart --namespace test
```

## Resources

- [Official Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Kubernetes Labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/)
- [SemVer 2.0](https://semver.org)

---

## Related Agent

For comprehensive Helm/Kubernetes guidance that coordinates this and other Helm skills, use the **`helm-kubernetes-expert`** agent.
