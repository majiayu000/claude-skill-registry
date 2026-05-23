# Skill: Helm Chart Generator

**Purpose**: Generate Helm charts for todo app with templated values for different environments (Phase V advanced).

## Trigger Conditions

Invoke this skill when:
- User asks for "Helm chart", "Helm deployment", or "templated K8s"
- Need to deploy to multiple environments (dev, staging, prod)
- Want reusable Kubernetes deployment configuration

## Capabilities

### 1. Chart Structure

Creates `helm/todo-app/`:

```
helm/todo-app/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── namespace.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── backend-configmap.yaml
│   ├── backend-secrets.yaml
│   ├── backend-hpa.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   └── ingress.yaml
└── .helmignore
```

### 2. Chart.yaml

```yaml
apiVersion: v2
name: todo-app
description: Full-stack Todo Application Helm Chart
type: application
version: 1.0.0
appVersion: "1.0.0"
maintainers:
  - name: Your Name
    email: your.email@example.com
```

### 3. values.yaml (defaults)

```yaml
# Global settings
global:
  namespace: todo-app
  environment: development

# Backend configuration
backend:
  name: todo-backend
  replicaCount: 2
  image:
    repository: your-registry/todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 80
    targetPort: 8000
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  config:
    corsOrigins: "http://localhost:3000"
    debug: "true"
  secrets:
    databaseUrl: ""  # Set via --set or values file
    betterAuthSecret: ""
  hpa:
    enabled: false
    minReplicas: 2
    maxReplicas: 10
    targetCPU: 70

# Frontend configuration
frontend:
  name: todo-frontend
  replicaCount: 2
  image:
    repository: your-registry/todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 80
    targetPort: 3000
  resources:
    requests:
      memory: "128Mi"
      cpu: "50m"
    limits:
      memory: "256Mi"
      cpu: "250m"
  config:
    apiUrl: "http://localhost:8000"

# Ingress configuration
ingress:
  enabled: false
  className: nginx
  annotations: {}
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
          service: frontend
    - host: api.todo.local
      paths:
        - path: /
          pathType: Prefix
          service: backend
  tls: []

# Image pull secrets
imagePullSecrets: []
```

### 4. values-prod.yaml

```yaml
global:
  namespace: todo-app
  environment: production

backend:
  replicaCount: 3
  image:
    tag: v1.0.0
  config:
    corsOrigins: "https://your-domain.com"
    debug: "false"
  hpa:
    enabled: true
    minReplicas: 3
    maxReplicas: 20

frontend:
  replicaCount: 3
  image:
    tag: v1.0.0
  config:
    apiUrl: "https://api.your-domain.com"

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: your-domain.com
      paths:
        - path: /
          pathType: Prefix
          service: frontend
    - host: api.your-domain.com
      paths:
        - path: /
          pathType: Prefix
          service: backend
  tls:
    - secretName: todo-tls
      hosts:
        - your-domain.com
        - api.your-domain.com
```

### 5. templates/_helpers.tpl

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- printf "%s" $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.name" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
environment: {{ .Values.global.environment }}
{{- end }}

{{/*
Backend selector labels
*/}}
{{- define "todo-app.backend.selectorLabels" -}}
app: {{ .Values.backend.name }}
{{- end }}

{{/*
Frontend selector labels
*/}}
{{- define "todo-app.frontend.selectorLabels" -}}
app: {{ .Values.frontend.name }}
{{- end }}
```

### 6. templates/backend-deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.backend.name }}
  namespace: {{ .Values.global.namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
    {{- include "todo-app.backend.selectorLabels" . | nindent 4 }}
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      {{- include "todo-app.backend.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "todo-app.backend.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      containers:
      - name: {{ .Values.backend.name }}
        image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
        imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
        ports:
        - containerPort: {{ .Values.backend.service.targetPort }}
        envFrom:
        - configMapRef:
            name: {{ .Values.backend.name }}-config
        - secretRef:
            name: {{ .Values.backend.name }}-secrets
        resources:
          {{- toYaml .Values.backend.resources | nindent 10 }}
        livenessProbe:
          httpGet:
            path: /health
            port: {{ .Values.backend.service.targetPort }}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: {{ .Values.backend.service.targetPort }}
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Helm Commands

```bash
# Install chart (development)
helm install todo-app ./helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  --set backend.secrets.databaseUrl="your-db-url" \
  --set backend.secrets.betterAuthSecret="your-secret"

# Install chart (production)
helm install todo-app ./helm/todo-app \
  -f ./helm/todo-app/values-prod.yaml \
  --namespace todo-app \
  --create-namespace \
  --set backend.secrets.databaseUrl="$DATABASE_URL" \
  --set backend.secrets.betterAuthSecret="$BETTER_AUTH_SECRET"

# Upgrade deployment
helm upgrade todo-app ./helm/todo-app \
  -f ./helm/todo-app/values-prod.yaml \
  --namespace todo-app

# Dry run (test)
helm install todo-app ./helm/todo-app --dry-run --debug

# Uninstall
helm uninstall todo-app -n todo-app

# List releases
helm list -n todo-app
```

## Checklist

- [ ] Create Chart.yaml with metadata
- [ ] Create values.yaml with defaults
- [ ] Create values-prod.yaml for production
- [ ] Create _helpers.tpl with common functions
- [ ] Create all template files
- [ ] Test with: `helm template ./helm/todo-app`
- [ ] Dry run: `helm install --dry-run --debug`
- [ ] Install to dev cluster
- [ ] Test production values
