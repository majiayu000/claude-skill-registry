---
name: helm
description: |
  Use when creating or managing Helm charts for Kubernetes applications. Covers chart structure, values files, templates, Go template functions, dependencies, and release management.
  USE FOR: Helm charts, Kubernetes package management, Go templates, values files, chart dependencies, release management
  DO NOT USE FOR: raw Kubernetes manifests without templating (use kubernetes), cloud provisioning (use terraform or pulumi), container builds (use docker)
license: MIT
metadata:
  displayName: "Helm"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "Helm Documentation"
    url: "https://helm.sh/docs/"
  - title: "Helm GitHub Repository"
    url: "https://github.com/helm/helm"
---

# Helm

## Overview
Helm is the package manager for Kubernetes. Charts are packages of pre-configured Kubernetes manifests with templating, making applications distributable, configurable, and upgradeable. Helm manages releases — versioned installations of charts into a cluster.

## Chart Structure
```
my-chart/
  Chart.yaml           # Chart metadata (name, version, dependencies)
  values.yaml          # Default configuration values
  templates/
    deployment.yaml    # Templated Kubernetes manifests
    service.yaml
    ingress.yaml
    _helpers.tpl       # Reusable template snippets
    NOTES.txt          # Post-install instructions
```

## Chart.yaml
```yaml
apiVersion: v2
name: my-app
description: A Helm chart for my application
version: 1.0.0
appVersion: "2.0.0"
dependencies:
  - name: postgresql
    version: "15.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

## values.yaml
```yaml
replicaCount: 3
image:
  repository: my-app
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  host: my-app.example.com

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 256Mi

postgresql:
  enabled: true
```

## Template Example
```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels:
    {{- include "my-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "my-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "my-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: 8080
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
```

## Helper Templates
```yaml
# templates/_helpers.tpl
{{- define "my-app.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{- define "my-app.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
{{- end -}}

{{- define "my-app.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
```

## Key Commands
```bash
# Install a release
helm install my-release ./my-chart -f custom-values.yaml

# Upgrade a release
helm upgrade my-release ./my-chart -f prod-values.yaml

# Dry run (preview rendered manifests)
helm template my-release ./my-chart -f values.yaml

# Lint a chart
helm lint ./my-chart

# Show computed values
helm get values my-release

# Rollback
helm rollback my-release 1

# Uninstall
helm uninstall my-release
```

## Common Template Functions
| Function | Example | Description |
|----------|---------|-------------|
| `include` | `{{ include "name" . }}` | Render a named template |
| `toYaml` | `{{ toYaml .Values.x \| nindent 4 }}` | Convert to YAML string |
| `default` | `{{ default "val" .Values.x }}` | Default value |
| `required` | `{{ required "msg" .Values.x }}` | Fail if not set |
| `quote` | `{{ .Values.x \| quote }}` | Wrap in quotes |
| `trunc` | `{{ .name \| trunc 63 }}` | Truncate string |
| `b64enc` | `{{ .secret \| b64enc }}` | Base64 encode |

## Best Practices
- Always run `helm template` or `helm install --dry-run` to preview rendered manifests before deploying.
- Use `_helpers.tpl` for shared templates (labels, names, selectors) to keep DRY.
- Use `values.yaml` for defaults and `-f` flag for environment overrides.
- Pin chart dependency versions to avoid breaking changes.
- Use `helm lint` in CI to catch template errors early.
- Use Helm's built-in `required` function to fail fast on missing values.
- Use semantic versioning for chart versions and `appVersion` for the application version.
