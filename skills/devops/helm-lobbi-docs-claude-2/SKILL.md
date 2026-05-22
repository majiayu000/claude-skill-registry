---
name: helm
description: Helm chart development, deployment, and management. Activate for helm install, upgrade, charts, values, templates, and Kubernetes package management.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Helm Skill

Provides comprehensive Helm chart development and deployment capabilities for the Golden Armada AI Agent Fleet Platform.

## When to Use This Skill

Activate this skill when working with:
- Helm chart creation and modification
- Values file configuration
- Template development
- Chart deployment and upgrades
- Release management

## Quick Reference

### Common Commands
\`\`\`bash
# Install/Upgrade
helm install <release> <chart> -n <namespace>
helm upgrade --install <release> <chart> -n <namespace>
helm upgrade --install golden-armada ./deployment/helm/golden-armada -n agents

# With values
helm install <release> <chart> -f values.yaml
helm install <release> <chart> --set key=value

# List/Status
helm list -n agents
helm status <release> -n agents
helm history <release> -n agents

# Uninstall
helm uninstall <release> -n agents

# Debug
helm template <release> <chart>
helm lint <chart>
helm get values <release> -n agents
helm get manifest <release> -n agents
\`\`\`

## Chart Structure

\`\`\`
golden-armada/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── ingress.yaml
└── charts/
\`\`\`

## Chart.yaml

\`\`\`yaml
apiVersion: v2
name: golden-armada
description: AI Agent Fleet Platform
type: application
version: 1.0.0
appVersion: "1.0.0"
dependencies:
  - name: redis
    version: "17.x.x"
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
\`\`\`

## Values.yaml

\`\`\`yaml
# Global settings
replicaCount: 2
image:
  repository: golden-armada/agent
  tag: latest
  pullPolicy: IfNotPresent

# Resources
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

# Service
service:
  type: ClusterIP
  port: 80
  targetPort: 8080

# Ingress
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: agents.example.com
      paths:
        - path: /
          pathType: Prefix

# Environment
env:
  - name: LOG_LEVEL
    value: "info"

# Secrets (use external secret manager in production)
secrets:
  anthropicApiKey: ""
\`\`\`

## Template Examples

### _helpers.tpl
\`\`\`yaml
{{- define "golden-armada.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "golden-armada.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
\`\`\`

### deployment.yaml
\`\`\`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "golden-armada.fullname" . }}
  labels:
    {{- include "golden-armada.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app.kubernetes.io/name: {{ .Chart.Name }}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: {{ .Chart.Name }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          ports:
            - containerPort: {{ .Values.service.targetPort }}
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          env:
            {{- toYaml .Values.env | nindent 12 }}
\`\`\`

## Golden Armada Commands

\`\`\`bash
# Deploy to development
helm upgrade --install golden-armada ./deployment/helm/golden-armada \
  -n agents \
  -f deployment/helm/golden-armada/values-dev.yaml

# Deploy to production
helm upgrade --install golden-armada ./deployment/helm/golden-armada \
  -n agents \
  -f deployment/helm/golden-armada/values-prod.yaml

# Dry run
helm upgrade --install golden-armada ./deployment/helm/golden-armada \
  -n agents --dry-run --debug
\`\`\`
