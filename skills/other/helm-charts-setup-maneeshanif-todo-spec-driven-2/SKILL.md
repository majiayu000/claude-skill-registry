---
name: helm-charts-setup
description: Create and manage Helm charts for Todo application deployment
allowed-tools: Bash, Write, Read, Glob, Edit
---

# Helm Charts Setup Skill

## Quick Start

1. **Read Phase 4 Constitution** - `prompts/constitution-prompt-phase-4.md`
2. **Create Helm chart structure** - Use `helm create` or manual structure
3. **Write templates** - Convert K8s manifests to Helm templates
4. **Create values files** - Separate for dev, staging, production
5. **Test and install** - Verify chart works on Minikube

## Helm Chart Structure

```
helm/todo-app/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-staging.yaml
├── values-prod.yaml
├── .helmignore
├── templates/
│   ├── NOTES.txt
│   ├── _helpers.tpl
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── serviceaccount.yaml
└── tests/
    └── test-connection.yaml
```

## Chart.yaml

```yaml
apiVersion: v2
name: todo-app
description: A Helm chart for Todo Chatbot - Evolution of Todo Phase 4
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - chatbot
  - nextjs
  - fastapi
  - mcp
  - kubernetes
maintainers:
  - name: Developer
    email: dev@example.com
home: https://github.com/username/todo-web-hackthon
icon: https://raw.githubusercontent.com/username/todo-web-hackthon/main/assets/logo.png
sources:
  - https://github.com/username/todo-web-hackthon
```

## .helmignore

```
# Patterns to ignore when packaging
*.md
.git
.gitignore
tests/
*.tgz
node_modules/
__pycache__/
venv/
.env
.vscode/
.idea/
```

## Values.yaml

```yaml
# Default values for todo-app

# Global configuration
global:
  namespace: todo-app
  imagePullPolicy: IfNotPresent
  registry: docker.io

# Frontend configuration
frontend:
  enabled: true
  replicaCount: 2
  image:
    repository: username/todo-frontend
    tag: "latest"
    pullPolicy: IfNotPresent
  service:
    type: NodePort
    port: 80
    targetPort: 3000
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi
  autoscaling:
    enabled: false
    minReplicas: 2
    maxReplicas: 5
    targetCPUUtilizationPercentage: 70
  env:
    NODE_ENV: production
    NEXT_PUBLIC_API_URL: ""
    NEXT_PUBLIC_MCP_URL: ""

# Backend configuration
backend:
  enabled: true
  replicaCount: 2
  image:
    repository: username/todo-backend
    tag: "latest"
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 1000m
      memory: 512Mi
  autoscaling:
    enabled: false
    minReplicas: 2
    maxReplicas: 5
    targetCPUUtilizationPercentage: 70
  env:
    DATABASE_URL: ""
    GEMINI_API_KEY: ""
    BETTER_AUTH_SECRET: ""
    MCP_SERVER_URL: ""

# MCP Server configuration
mcpServer:
  enabled: true
  replicaCount: 1
  image:
    repository: username/todo-mcp-server
    tag: "latest"
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8001
  resources:
    requests:
      cpu: 100m
      memory: 64Mi
    limits:
      cpu: 300m
      memory: 128Mi
  env:
    GEMINI_API_KEY: ""

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  annotations: {}
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
  tls: []

# Service Account
serviceAccount:
  create: true
  annotations: {}
  name: ""

# Dapr configuration (Phase 5)
dapr:
  enabled: false
  config: app-config
```

## Values Files by Environment

### values-dev.yaml (Minikube Local)
```yaml
global:
  registry: ""  # Use local images

frontend:
  replicaCount: 1
  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 250m
      memory: 128Mi

backend:
  replicaCount: 1
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi

mcpServer:
  replicaCount: 1

ingress:
  enabled: true
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
```

### values-staging.yaml (Pre-production)
```yaml
global:
  registry: docker.io

frontend:
  replicaCount: 2
  autoscaling:
    enabled: true

backend:
  replicaCount: 2
  autoscaling:
    enabled: true

mcpServer:
  replicaCount: 1
```

### values-prod.yaml (Production)
```yaml
global:
  registry: ghcr.io  # GitHub Container Registry

frontend:
  replicaCount: 3
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

backend:
  replicaCount: 3
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

ingress:
  enabled: true
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  tls:
    - secretName: todo-tls
      hosts:
        - todo.example.com
  hosts:
    - host: todo.example.com
      paths:
        - path: /
          pathType: Prefix
```

## Template Files

### _helpers.tpl

```yaml
{{- /*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- /*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
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

{{- /*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- /*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- /*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### templates/deployment.yaml

```yaml
{{- if .Values.frontend.enabled }}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-frontend
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.frontend.replicaCount }}
  selector:
    matchLabels:
      app: frontend
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        app: frontend
        {{- include "todo-app.selectorLabels" . | nindent 8 }}
    spec:
      containers:
      - name: frontend
        image: "{{ .Values.global.registry }}/{{ .Values.frontend.image.repository }}:{{ .Values.frontend.image.tag }}"
        imagePullPolicy: {{ .Values.frontend.image.pullPolicy }}
        ports:
        - name: http
          containerPort: {{ .Values.frontend.service.targetPort }}
          protocol: TCP
        env:
        - name: NODE_ENV
          value: {{ .Values.frontend.env.NODE_ENV | quote }}
        {{- range $key, $value := .Values.frontend.env }}
        {{- if ne $key "NODE_ENV" }}
        - name: {{ $key }}
          value: {{ $value | quote }}
        {{- end }}
        {{- end }}
        resources:
          {{- toYaml .Values.frontend.resources | nindent 10 }}
        livenessProbe:
          httpGet:
            path: /
            port: {{ .Values.frontend.service.targetPort }}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: {{ .Values.frontend.service.targetPort }}
          initialDelaySeconds: 5
          periodSeconds: 5
{{- end }}
```

### templates/service.yaml

```yaml
{{- if .Values.frontend.enabled }}
---
apiVersion: v1
kind: Service
metadata:
  name: {{ include "todo-app.fullname" . }}-frontend
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
spec:
  type: {{ .Values.frontend.service.type }}
  selector:
    app: frontend
    {{- include "todo-app.selectorLabels" . | nindent 4 }}
  ports:
  - name: http
    port: {{ .Values.frontend.service.port }}
    targetPort: {{ .Values.frontend.service.targetPort }}
    protocol: TCP
{{- end }}
```

### templates/hpa.yaml

```yaml
{{- if and .Values.frontend.enabled .Values.frontend.autoscaling.enabled }}
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ include "todo-app.fullname" . }}-frontend
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "todo-app.fullname" . }}-frontend
  minReplicas: {{ .Values.frontend.autoscaling.minReplicas }}
  maxReplicas: {{ .Values.frontend.autoscaling.maxReplicas }}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {{ .Values.frontend.autoscaling.targetCPUUtilizationPercentage }}
{{- end }}
```

### templates/configmap.yaml

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "todo-app.fullname" . }}-config
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
data:
  MCP_SERVER_URL: "http://{{ include "todo-app.fullname" . }}-mcp-server:8001"
  {{- if .Values.frontend.enabled }}
  NEXT_PUBLIC_API_URL: "http://{{ include "todo-app.fullname" . }}-backend:8000"
  NEXT_PUBLIC_MCP_URL: "http://{{ include "todo-app.fullname" . }}-mcp-server:8001"
  {{- end }}
```

### templates/secret.yaml

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "todo-app.fullname" . }}-secrets
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
type: Opaque
stringData:
  GEMINI_API_KEY: {{ .Values.backend.env.GEMINI_API_KEY | default "" | quote }}
  BETTER_AUTH_SECRET: {{ .Values.backend.env.BETTER_AUTH_SECRET | default "" | quote }}
  {{- if .Values.backend.env.DATABASE_URL }}
  DATABASE_URL: {{ .Values.backend.env.DATABASE_URL | quote }}
  {{- end }}
```

### templates/ingress.yaml

```yaml
{{- if .Values.ingress.enabled }}
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ include "todo-app.fullname" . }}-ingress
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
  {{- with .Values.ingress.annotations }}
  annotations:
    {{- toYaml . | nindent 4 }}
  {{- end }}
spec:
  {{- if .Values.ingress.className }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  rules:
  {{- range .Values.ingress.hosts }}
  - host: {{ .host }}
    http:
      paths:
      {{- range .paths }}
      - path: {{ .path }}
        pathType: {{ .pathType }}
        backend:
          service:
            name: {{ include "todo-app.fullname" $ }}-frontend
            port:
              number: {{ $.Values.frontend.service.port }}
      {{- end }}
  {{- end }}
  {{- if .Values.ingress.tls }}
  tls:
  {{- toYaml .Values.ingress.tls | nindent 2 }}
  {{- end }}
{{- end }}
```

### templates/NOTES.txt

```txt
Thank you for installing {{ .Chart.Name }}!

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}

To get the application URL:

  {{- if .Values.ingress.enabled }}
  http://{{ (index .Values.ingress.hosts 0).host }}
  {{- else }}
  Run: kubectl port-forward svc/{{ include "todo-app.fullname" . }}-frontend 8080:80
  {{- end }}

To upgrade the release:

  $ helm upgrade {{ .Release.Name }} .

To rollback the release:

  $ helm rollback {{ .Release.Name }}
```

## Helm Commands

```bash
# Create new chart
helm create todo-app

# Lint chart
helm lint helm/todo-app

# Package chart
helm package helm/todo-app

# Install chart
helm install todo-app ./helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  -f helm/todo-app/values-dev.yaml

# Upgrade chart
helm upgrade todo-app ./helm/todo-app \
  -f helm/todo-app/values-prod.yaml

# Get release status
helm status todo-app

# Get release values
helm get values todo-app

# Get release history
helm history todo-app

# Rollback
helm rollback todo-app [REVISION]

# Uninstall
helm uninstall todo-app

# List all releases
helm list --all-namespaces

# Dry run (preview)
helm upgrade --dry-run --debug todo-app ./helm/todo-app
```

## kubectl-ai Integration

```bash
# Using kubectl-ai with Helm
kubectl-ai "install todo-app helm chart to production namespace"
kubectl-ai "upgrade todo-app with new image tag v1.2.0"
kubectl-ai "scale frontend using helm"
kubectl-ai "analyze helm release for issues"
kubectl-ai "optimize helm values for cost reduction"
```

## Verification Checklist

After creating Helm chart:
- [ ] Chart.yaml has correct API version (v2)
- [ ] All templates use proper helper functions
- [ ] Values file has all configurable parameters
- [ ] .helmignore excludes unnecessary files
- [ ] NOTES.txt provides helpful information
- [ ] Helm lint passes without warnings
- [ ] Chart can be packaged successfully
- [ ] Chart installs on Minikube
- [ ] All services are accessible
- [ ] Upgrades work without issues

## Troubleshooting

| Issue | Cause | Fix |
|--------|--------|-----|
| Template fails | Invalid Helm syntax | Run `helm lint` to find errors |
| Values not applied | Wrong values path | Use `-f` flag with correct path |
| Release fails | Missing secrets | Create secrets separately or use `--set-file` |
| Can't upgrade | Existing release conflict | Use `helm upgrade` instead of `install` |
| Ingress not working | Wrong annotations | Verify ingress controller is installed |

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Build and push Docker images
  run: |
    docker build -t ghcr.io/${{ github.repository }}/frontend:${{ github.sha }} ./frontend
    docker build -t ghcr.io/${{ github.repository }}/backend:${{ github.sha }} ./backend
    docker build -t ghcr.io/${{ github.repository }}/mcp-server:${{ github.sha }} ./backend
    echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
    docker push ghcr.io/${{ github.repository }}/frontend:${{ github.sha }}
    docker push ghcr.io/${{ github.repository }}/backend:${{ github.sha }}
    docker push ghcr.io/${{ github.repository }}/mcp-server:${{ github.sha }}

- name: Deploy with Helm
  run: |
    helm upgrade --install todo-app ./helm/todo-app \
      --namespace todo-app \
      --create-namespace \
      --set global.registry=ghcr.io \
      --set frontend.image.tag=${{ github.sha }} \
      --set backend.image.tag=${{ github.sha }} \
      --set mcpServer.image.tag=${{ github.sha }} \
      -f helm/todo-app/values-prod.yaml
```

## Next Steps

After Helm chart creation:
1. Test on Minikube with values-dev.yaml
2. Test on staging cluster with values-staging.yaml
3. Prepare for production deployment with values-prod.yaml
4. Add Dapr annotations for Phase 5

## References

- [Helm Documentation](https://helm.sh/docs/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Template Guide](https://helm.sh/docs/chart_template_guide/)
- [Phase 4 Constitution](../../../prompts/constitution-prompt-phase-4.md)
- [Phase 4 Plan](../../../prompts/plan-prompt-phase-4.md)
