---
name: helm-development
description: Helm chart development workflow including chart structure, values management, testing, linting, and publishing for EKS deployments with Keycloak integration
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
triggers:
  - helm chart
  - helm create
  - helm values
  - helm template
  - helm lint
  - chart development
  - helm test
---

# Helm Development Skill

Develop, test, and publish Helm charts for EKS deployments.

## Use For
- Chart scaffolding, values management, chart testing
- Linting, security scanning, chart publishing

## Chart Structure for EKS + Keycloak

```
charts/my-service/
├── Chart.yaml
├── Chart.lock
├── values.yaml
├── values-dev.yaml
├── values-staging.yaml
├── values-prod.yaml
├── .helmignore
├── templates/
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── serviceaccount.yaml
│   ├── hpa.yaml
│   ├── pdb.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── external-secret.yaml      # For AWS Secrets Manager
│   ├── networkpolicy.yaml
│   └── tests/
│       └── test-connection.yaml
└── ci/
    ├── test-values.yaml
    └── lint-values.yaml
```

## Chart.yaml Template

```yaml
apiVersion: v2
name: my-service
description: A Helm chart for my-service with Keycloak authentication
type: application
version: 0.1.0
appVersion: "1.0.0"
kubeVersion: ">=1.25.0"

keywords:
  - microservice
  - keycloak
  - eks

home: https://github.com/org/my-service
sources:
  - https://github.com/org/my-service

maintainers:
  - name: Platform Team
    email: platform@example.com

dependencies:
  - name: common
    version: "2.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: common.enabled

annotations:
  artifacthub.io/category: integration
  artifacthub.io/license: MIT
```

## Values Schema (values.yaml)

```yaml
# Default values for my-service

# -- Number of replicas
replicaCount: 1

image:
  # -- Image repository
  repository: ""
  # -- Image pull policy
  pullPolicy: IfNotPresent
  # -- Image tag (defaults to chart appVersion)
  tag: ""

# -- Image pull secrets
imagePullSecrets: []
# -- Override chart name
nameOverride: ""
# -- Override full name
fullnameOverride: ""

serviceAccount:
  # -- Create service account
  create: true
  # -- Service account annotations (for IRSA)
  annotations: {}
  # -- Service account name
  name: ""

# -- Pod annotations
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "9090"

# -- Pod security context
podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# -- Container security context
securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

service:
  # -- Service type
  type: ClusterIP
  # -- Service port
  port: 80
  # -- Target port
  targetPort: 3000

ingress:
  # -- Enable ingress
  enabled: false
  # -- Ingress class name
  className: "alb"
  # -- Ingress annotations
  annotations:
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
  # -- Ingress hosts
  hosts:
    - host: ""
      paths:
        - path: /
          pathType: Prefix
  # -- Ingress TLS
  tls: []

# -- Resource limits and requests
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 128Mi

autoscaling:
  # -- Enable HPA
  enabled: true
  # -- Minimum replicas
  minReplicas: 2
  # -- Maximum replicas
  maxReplicas: 10
  # -- Target CPU utilization
  targetCPUUtilizationPercentage: 80
  # -- Target memory utilization
  targetMemoryUtilizationPercentage: 80

# -- Node selector
nodeSelector: {}
# -- Tolerations
tolerations: []
# -- Affinity rules
affinity: {}

# Keycloak Configuration
keycloak:
  # -- Enable Keycloak authentication
  enabled: true
  # -- Keycloak server URL
  url: ""
  # -- Keycloak realm
  realm: ""
  # -- Keycloak client ID
  clientId: ""
  # -- Reference to client secret
  clientSecretRef:
    name: ""
    key: "client-secret"

# AWS Configuration
aws:
  # -- AWS region
  region: "us-west-2"
  # -- IAM role ARN for IRSA
  iamRoleArn: ""

# External Secrets
externalSecrets:
  # -- Enable external secrets
  enabled: true
  # -- Secret store reference
  secretStoreRef: "aws-secrets-manager"

# -- Environment variables
env: []
# -- Environment variables from secrets/configmaps
envFrom: []

# Health checks
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: http
  initialDelaySeconds: 5
  periodSeconds: 5

# Pod Disruption Budget
podDisruptionBudget:
  # -- Enable PDB
  enabled: true
  # -- Minimum available pods
  minAvailable: 1

# Network Policy
networkPolicy:
  # -- Enable network policy
  enabled: false
```

## Template Helpers (_helpers.tpl)

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "my-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "my-service.fullname" -}}
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
{{- define "my-service.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "my-service.labels" -}}
helm.sh/chart: {{ include "my-service.chart" . }}
{{ include "my-service.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "my-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "my-service.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "my-service.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "my-service.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Keycloak environment variables
*/}}
{{- define "my-service.keycloakEnv" -}}
{{- if .Values.keycloak.enabled }}
- name: KEYCLOAK_URL
  value: {{ .Values.keycloak.url | quote }}
- name: KEYCLOAK_REALM
  value: {{ .Values.keycloak.realm | quote }}
- name: KEYCLOAK_CLIENT_ID
  value: {{ .Values.keycloak.clientId | quote }}
- name: KEYCLOAK_CLIENT_SECRET
  valueFrom:
    secretKeyRef:
      name: {{ .Values.keycloak.clientSecretRef.name }}
      key: {{ .Values.keycloak.clientSecretRef.key }}
{{- end }}
{{- end }}
```

## Development Commands

### Create New Chart
```bash
# Create chart from scratch
helm create charts/my-service

# Or use a starter template
helm create charts/my-service --starter eks-keycloak-starter
```

### Lint Chart
```bash
# Basic lint
helm lint charts/my-service

# Lint with values
helm lint charts/my-service -f charts/my-service/values-dev.yaml

# Strict lint (fail on warnings)
helm lint charts/my-service --strict

# Lint all charts
find charts -name Chart.yaml -exec dirname {} \; | xargs -I {} helm lint {}
```

### Template Rendering
```bash
# Render templates
helm template my-service charts/my-service

# Render with specific values
helm template my-service charts/my-service \
  -f charts/my-service/values-prod.yaml \
  --set image.tag=v1.2.3

# Render specific template
helm template my-service charts/my-service \
  --show-only templates/deployment.yaml

# Debug template issues
helm template my-service charts/my-service --debug

# Validate against cluster
helm template my-service charts/my-service | kubectl apply --dry-run=server -f -
```

### Test Chart
```bash
# Run Helm tests
helm test my-service -n my-namespace

# Test with timeout
helm test my-service -n my-namespace --timeout 5m

# Show test logs
helm test my-service -n my-namespace --logs
```

### Package and Publish
```bash
# Package chart
helm package charts/my-service

# Package with specific version
helm package charts/my-service --version 1.2.3 --app-version 1.2.3

# Push to OCI registry (ECR)
aws ecr get-login-password --region us-west-2 | helm registry login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com

helm push my-service-1.2.3.tgz oci://123456789012.dkr.ecr.us-west-2.amazonaws.com/charts
```

## Chart Testing with ct

```yaml
# ct.yaml - Chart Testing configuration
remote: origin
target-branch: main
chart-dirs:
  - charts
chart-repos:
  - bitnami=https://charts.bitnami.com/bitnami
helm-extra-args: --timeout 600s
validate-maintainers: false
check-version-increment: true
```

```bash
# Lint changed charts
ct lint --config ct.yaml

# Install and test changed charts
ct install --config ct.yaml

# Full test (lint + install)
ct lint-and-install --config ct.yaml
```

## Security Scanning

```bash
# Trivy scan
trivy config charts/my-service

# Checkov scan
checkov -d charts/my-service

# Kubesec scan rendered manifests
helm template my-service charts/my-service | kubesec scan -

# Polaris audit
helm template my-service charts/my-service | polaris audit --audit-path -
```

## Values Validation Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["image", "service"],
  "properties": {
    "replicaCount": {
      "type": "integer",
      "minimum": 1
    },
    "image": {
      "type": "object",
      "required": ["repository"],
      "properties": {
        "repository": { "type": "string" },
        "tag": { "type": "string" },
        "pullPolicy": {
          "type": "string",
          "enum": ["Always", "IfNotPresent", "Never"]
        }
      }
    },
    "keycloak": {
      "type": "object",
      "properties": {
        "enabled": { "type": "boolean" },
        "url": { "type": "string", "format": "uri" },
        "realm": { "type": "string" },
        "clientId": { "type": "string" }
      },
      "if": { "properties": { "enabled": { "const": true } } },
      "then": { "required": ["url", "realm", "clientId"] }
    }
  }
}
```

## Environment-Specific Values Pattern

```yaml
# values-dev.yaml
replicaCount: 1
image:
  repository: 123456789012.dkr.ecr.us-west-2.amazonaws.com/my-service
  tag: dev-latest
ingress:
  enabled: true
  hosts:
    - host: my-service.dev.example.com
keycloak:
  url: "https://keycloak.dev.example.com"
  realm: "development"
resources:
  limits:
    cpu: 250m
    memory: 256Mi

---
# values-prod.yaml
replicaCount: 3
image:
  repository: 123456789012.dkr.ecr.us-west-2.amazonaws.com/my-service
ingress:
  enabled: true
  annotations:
    alb.ingress.kubernetes.io/wafv2-acl-arn: arn:aws:wafv2:...
  hosts:
    - host: my-service.example.com
keycloak:
  url: "https://keycloak.example.com"
  realm: "production"
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Template syntax error | Use `helm template --debug` to see full error |
| Values not applied | Check indentation, verify values file path |
| Release stuck | Check hooks, use `helm rollback` or delete release |
| CRD issues | Install CRDs separately before chart |
| Dependency issues | Run `helm dependency update` |

## References
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Chart Testing](https://github.com/helm/chart-testing)
