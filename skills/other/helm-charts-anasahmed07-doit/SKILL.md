---
name: helm-charts
description: Creates and manages Helm charts for Kubernetes deployments. This skill should be used when packaging applications for Kubernetes using Helm, creating Chart.yaml, values.yaml, and templates. It covers chart structure, templating, dependencies, and deployment patterns. Use this skill for Phase IV+ Kubernetes deployments.
---

# Helm Charts Skill

## Overview

Helm is the package manager for Kubernetes. It packages Kubernetes manifests into reusable **charts** that can be versioned, shared, and deployed with customizable values.

## Core Concepts

### What is a Helm Chart?

A chart is a collection of files that describe a related set of Kubernetes resources:

```
mychart/
├── Chart.yaml          # Chart metadata (name, version, dependencies)
├── values.yaml         # Default configuration values
├── charts/             # Dependency charts
├── templates/          # Kubernetes manifest templates
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── _helpers.tpl    # Template helpers
│   └── NOTES.txt       # Post-install notes
└── .helmignore         # Files to ignore when packaging
```

### Key Files

| File | Purpose |
|------|---------|
| `Chart.yaml` | Metadata: name, version, appVersion, dependencies |
| `values.yaml` | Default configuration values (overridable) |
| `templates/` | Go-templated Kubernetes manifests |
| `_helpers.tpl` | Reusable template snippets |

## Chart.yaml Structure

```yaml
apiVersion: v2                    # Helm 3 uses v2
name: taskflow                    # Chart name
description: TaskFlow Platform    # Short description
type: application                 # application or library
version: 1.0.0                    # Chart version (SemVer)
appVersion: "1.0.0"               # Application version

# Dependencies (optional)
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

## values.yaml Pattern

```yaml
# Global settings
global:
  imageRegistry: ""
  imagePullSecrets: []

# Per-service configuration
api:
  replicaCount: 1
  image:
    repository: taskflow/api
    tag: "latest"
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  env:
    DATABASE_URL: ""
    SSO_URL: "http://sso:3001"

# Feature flags
postgresql:
  enabled: true
  auth:
    postgresPassword: "postgres"
    database: "taskflow"
```

## Template Syntax

### Accessing Values

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "taskflow.fullname" . }}
  labels:
    {{- include "taskflow.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.api.replicaCount }}
  selector:
    matchLabels:
      {{- include "taskflow.selectorLabels" . | nindent 6 }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.api.image.repository }}:{{ .Values.api.image.tag }}"
          ports:
            - containerPort: {{ .Values.api.service.port }}
          env:
            - name: DATABASE_URL
              value: {{ .Values.api.env.DATABASE_URL | quote }}
```

### Helper Templates (_helpers.tpl)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "taskflow.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "taskflow.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "taskflow.labels" -}}
helm.sh/chart: {{ include "taskflow.chart" . }}
{{ include "taskflow.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "taskflow.selectorLabels" -}}
app.kubernetes.io/name: {{ include "taskflow.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## Essential Commands

### Create New Chart
```bash
helm create mychart
```

### Install Chart
```bash
# From local directory
helm install my-release ./mychart

# With custom values file
helm install my-release ./mychart --values custom-values.yaml

# With inline value overrides
helm install my-release ./mychart \
  --set api.replicaCount=3 \
  --set api.image.tag=v2.0.0

# To specific namespace (create if needed)
helm install my-release ./mychart \
  --namespace production \
  --create-namespace

# Dry run (preview without installing)
helm install my-release ./mychart --dry-run --debug
```

### Upgrade Release
```bash
helm upgrade my-release ./mychart --values new-values.yaml
```

### Rollback
```bash
helm rollback my-release 1  # Rollback to revision 1
```

### Uninstall
```bash
helm uninstall my-release
```

### List Releases
```bash
helm list
helm list --all-namespaces
```

### Debug Templates
```bash
# Render templates without installing
helm template my-release ./mychart

# Debug with computed values
helm template my-release ./mychart --debug
```

## Multi-Service Chart Pattern

For TaskFlow (api, sso, web, mcp-server), use a single chart with multiple templates:

```
helm/taskflow/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── NOTES.txt
│   ├── api/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   ├── sso/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── web/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── mcp-server/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   └── ingress.yaml
```

## ConfigMap and Secrets

### ConfigMap Template
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "taskflow.fullname" . }}-config
data:
  SSO_URL: {{ .Values.sso.url | quote }}
  API_URL: {{ .Values.api.url | quote }}
```

### Secret Template (from values)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "taskflow.fullname" . }}-secrets
type: Opaque
data:
  database-url: {{ .Values.secrets.databaseUrl | b64enc | quote }}
  openai-api-key: {{ .Values.secrets.openaiApiKey | b64enc | quote }}
```

## Health Checks Pattern

```yaml
spec:
  containers:
    - name: api
      livenessProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 30
        periodSeconds: 10
      readinessProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 5
```

## Ingress Pattern

```yaml
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "taskflow.fullname" . }}
  annotations:
    {{- toYaml .Values.ingress.annotations | nindent 4 }}
spec:
  ingressClassName: {{ .Values.ingress.className }}
  rules:
    - host: {{ .Values.ingress.host }}
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: {{ include "taskflow.fullname" . }}-api
                port:
                  number: 8000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ include "taskflow.fullname" . }}-web
                port:
                  number: 3000
{{- end }}
```

## Common Gotchas

1. **Quote strings in templates**: Use `{{ .Values.foo | quote }}` for strings
2. **Indentation matters**: Use `nindent` for proper YAML formatting
3. **Resource names**: Keep under 63 characters (K8s limit)
4. **Image pull policy**: Use `IfNotPresent` in production, `Always` in dev
5. **Secrets**: Never commit real secrets to values.yaml

## Resources

Refer to `references/` for:
- `chart-patterns.md` - Advanced templating patterns
- `values-structure.md` - Values.yaml organization guide

Refer to `assets/` for:
- `base-chart/` - Complete starter chart template
