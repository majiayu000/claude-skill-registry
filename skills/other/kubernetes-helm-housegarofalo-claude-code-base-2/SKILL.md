---
name: kubernetes-helm
description: Kubernetes deployment and Helm chart management. Create manifests, deploy applications, manage Helm charts, configure ingress, services, and persistent storage. Use for container orchestration, microservices deployment, and Kubernetes cluster management.
---

# Kubernetes & Helm Skill

Deploy and manage containerized applications with Kubernetes manifests and Helm charts.

## Triggers

Use this skill when you see:
- kubernetes, k8s, kubectl
- helm, helm chart, helm template
- deployment, service, ingress
- pod, configmap, secret
- kustomize, manifests

## Instructions

### Kubernetes Manifests

#### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
        - name: app
          image: myapp:1.0.0
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: log-level
```

#### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  type: ClusterIP
```

#### Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - app.example.com
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 80
```

#### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  log-level: "info"
  api-url: "https://api.example.com"
  config.json: |
    {
      "feature_flags": {
        "new_ui": true
      }
    }
```

#### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  database-url: "postgres://user:pass@db:5432/app"
  api-key: "your-api-key"
```

#### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: app-data
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: standard
  resources:
    requests:
      storage: 10Gi
```

### Helm Charts

#### Chart Structure

```
mychart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── _helpers.tpl
│   └── NOTES.txt
└── charts/
```

#### Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for my application
type: application
version: 1.0.0
appVersion: "1.0.0"
dependencies:
  - name: postgresql
    version: "12.0.0"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
```

#### values.yaml

```yaml
replicaCount: 3

image:
  repository: myapp
  tag: "1.0.0"
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 80

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: app-tls
      hosts:
        - app.example.com

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"

config:
  logLevel: info
  apiUrl: https://api.example.com

secrets:
  databaseUrl: ""
  apiKey: ""

postgresql:
  enabled: true
  auth:
    postgresPassword: ""
    database: myapp
```

#### templates/deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: 8080
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          env:
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: {{ include "myapp.fullname" . }}-config
                  key: log-level
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "myapp.fullname" . }}-secrets
                  key: database-url
```

#### templates/_helpers.tpl

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "myapp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "myapp.fullname" -}}
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
{{- define "myapp.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
{{ include "myapp.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

### Kubectl Commands

```bash
# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f ./manifests/

# Get resources
kubectl get pods
kubectl get deployments
kubectl get services
kubectl get ingress

# Describe resources
kubectl describe pod myapp-xxx
kubectl describe deployment myapp

# Logs
kubectl logs myapp-xxx
kubectl logs -f myapp-xxx
kubectl logs -l app=myapp --all-containers

# Exec into pod
kubectl exec -it myapp-xxx -- /bin/sh

# Port forwarding
kubectl port-forward svc/myapp 8080:80
kubectl port-forward pod/myapp-xxx 8080:8080

# Scale deployment
kubectl scale deployment myapp --replicas=5

# Rollout
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp
kubectl rollout restart deployment/myapp

# Delete resources
kubectl delete -f deployment.yaml
kubectl delete pod myapp-xxx
```

### Helm Commands

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search charts
helm search repo nginx
helm search hub nginx

# Install chart
helm install myapp ./mychart
helm install myapp ./mychart -f values-prod.yaml
helm install myapp ./mychart --set replicaCount=5

# Upgrade release
helm upgrade myapp ./mychart
helm upgrade myapp ./mychart --install

# List releases
helm list
helm list -A

# Get release info
helm status myapp
helm get values myapp
helm get manifest myapp

# Rollback
helm rollback myapp 1

# Uninstall
helm uninstall myapp

# Template (dry run)
helm template myapp ./mychart
helm template myapp ./mychart --debug

# Package chart
helm package ./mychart
```

### Kustomize

```yaml
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
  - deployment.yaml
  - service.yaml
  - ingress.yaml

configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=info

secretGenerator:
  - name: app-secrets
    literals:
      - DATABASE_URL=postgres://...

images:
  - name: myapp
    newTag: "2.0.0"

replicas:
  - name: app
    count: 5

patchesStrategicMerge:
  - patch-deployment.yaml
```

```bash
# Apply with Kustomize
kubectl apply -k ./overlays/production/

# Build (dry run)
kubectl kustomize ./overlays/production/
```

## Best Practices

1. **Resources**: Always set resource requests and limits
2. **Health Checks**: Configure liveness and readiness probes
3. **Secrets**: Use Kubernetes Secrets or external secret management
4. **Labels**: Use consistent labeling for all resources
5. **Namespaces**: Organize applications by namespace
6. **Helm**: Use Helm for repeatable deployments

## Common Workflows

### Deploy Application
1. Create namespace: `kubectl create namespace myapp`
2. Apply ConfigMaps and Secrets
3. Deploy application: `kubectl apply -f deployment.yaml`
4. Expose with Service and Ingress
5. Verify with `kubectl get pods` and logs

### Helm Release
1. Create chart: `helm create mychart`
2. Configure values.yaml
3. Template check: `helm template myapp ./mychart`
4. Install: `helm install myapp ./mychart -n myapp`
5. Upgrade: `helm upgrade myapp ./mychart`
