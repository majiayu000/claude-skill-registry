---
name: kubernetes-helm
description: "Deploy and manage Kubernetes applications with Helm charts. Covers K8s manifests, kubectl, Kustomize, RBAC, and container orchestration. Use for container deployments, microservices, and cloud-native applications."
---

# Kubernetes & Helm Skill

> Expert guidance for Kubernetes container orchestration and Helm package management.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Kubernetes Core Concepts](#kubernetes-core-concepts)
- [Helm Charts](#helm-charts)
- [kubectl Commands](#kubectl-commands)
- [Kustomize](#kustomize)
- [Ingress & Networking](#ingress--networking)
- [RBAC & Security](#rbac--security)
- [Autoscaling](#autoscaling)
- [Persistent Volumes](#persistent-volumes)
- [Debugging & Troubleshooting](#debugging--troubleshooting)
- [Deployment Patterns](#deployment-patterns)

---

## Quick Reference

### Essential kubectl Commands

| Command                                         | Description                           |
| ----------------------------------------------- | ------------------------------------- |
| `kubectl get pods -A`                           | List all pods in all namespaces       |
| `kubectl get deploy,svc,ing`                    | List deployments, services, ingresses |
| `kubectl describe pod <name>`                   | Show detailed pod information         |
| `kubectl logs <pod> -f`                         | Stream pod logs                       |
| `kubectl logs <pod> -c <container>`             | Logs from specific container          |
| `kubectl exec -it <pod> -- /bin/sh`             | Interactive shell in pod              |
| `kubectl port-forward <pod> 8080:80`            | Forward local port to pod             |
| `kubectl apply -f manifest.yaml`                | Apply configuration                   |
| `kubectl delete -f manifest.yaml`               | Delete resources from file            |
| `kubectl rollout status deploy/<name>`          | Watch deployment rollout              |
| `kubectl rollout undo deploy/<name>`            | Rollback deployment                   |
| `kubectl top pods`                              | Show pod resource usage               |
| `kubectl get events --sort-by='.lastTimestamp'` | Recent cluster events                 |

### Essential Helm Commands

| Command                                    | Description                 |
| ------------------------------------------ | --------------------------- |
| `helm install <release> <chart>`           | Install a chart             |
| `helm upgrade <release> <chart>`           | Upgrade a release           |
| `helm upgrade --install <release> <chart>` | Install or upgrade          |
| `helm list -A`                             | List all releases           |
| `helm status <release>`                    | Show release status         |
| `helm history <release>`                   | Show release history        |
| `helm rollback <release> <revision>`       | Rollback to revision        |
| `helm uninstall <release>`                 | Uninstall a release         |
| `helm template <chart>`                    | Render templates locally    |
| `helm show values <chart>`                 | Show chart's default values |
| `helm dependency update`                   | Update chart dependencies   |
| `helm repo add <name> <url>`               | Add chart repository        |
| `helm search repo <keyword>`               | Search repositories         |

---

## Kubernetes Core Concepts

### Pod

The smallest deployable unit in Kubernetes.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: app-pod
  labels:
    app: myapp
    version: v1
spec:
  containers:
    - name: app
      image: myapp:1.0.0
      ports:
        - containerPort: 8080
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
        initialDelaySeconds: 10
        periodSeconds: 30
        failureThreshold: 3
      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 10
      volumeMounts:
        - name: config-volume
          mountPath: /etc/config
        - name: data-volume
          mountPath: /data
  volumes:
    - name: config-volume
      configMap:
        name: app-config
    - name: data-volume
      persistentVolumeClaim:
        claimName: app-pvc
  restartPolicy: Always
```

### Deployment

Manages ReplicaSets and provides declarative updates for Pods.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
  revisionHistoryLimit: 5
  selector:
    matchLabels:
      app: myapp
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: myapp
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    spec:
      serviceAccountName: myapp-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: app
          image: myapp:1.0.0
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          envFrom:
            - configMapRef:
                name: myapp-config
            - secretRef:
                name: myapp-secrets
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
            timeoutSeconds: 5
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: myapp
                topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app: myapp
```

### Service

Exposes pods as a network service.

```yaml
# ClusterIP Service (internal)
apiVersion: v1
kind: Service
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  type: ClusterIP
  ports:
    - name: http
      port: 80
      targetPort: 8080
      protocol: TCP
  selector:
    app: myapp
---
# LoadBalancer Service (external)
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
spec:
  type: LoadBalancer
  ports:
    - port: 443
      targetPort: 8080
  selector:
    app: myapp
---
# NodePort Service
apiVersion: v1
kind: Service
metadata:
  name: myapp-nodeport
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 8080
      nodePort: 30080
  selector:
    app: myapp
---
# Headless Service (for StatefulSets)
apiVersion: v1
kind: Service
metadata:
  name: myapp-headless
spec:
  clusterIP: None
  ports:
    - port: 8080
  selector:
    app: myapp
```

### ConfigMap

Stores non-confidential configuration data.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  # Simple key-value pairs
  LOG_LEVEL: "info"
  FEATURE_FLAG: "true"
  MAX_CONNECTIONS: "100"

  # Multi-line configuration file
  app.properties: |
    server.port=8080
    server.timeout=30s
    database.pool.size=10

  nginx.conf: |
    server {
        listen 80;
        location / {
            proxy_pass http://localhost:8080;
        }
    }
```

**Using ConfigMaps:**

```yaml
# As environment variables
envFrom:
  - configMapRef:
      name: myapp-config

# Individual keys
env:
  - name: LOG_LEVEL
    valueFrom:
      configMapKeyRef:
        name: myapp-config
        key: LOG_LEVEL

# As volume mount
volumes:
  - name: config
    configMap:
      name: myapp-config
      items:
        - key: app.properties
          path: application.properties
```

### Secret

Stores sensitive data like passwords, tokens, and keys.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
type: Opaque
data:
  # Base64 encoded values
  database-password: cGFzc3dvcmQxMjM=
  api-key: c2VjcmV0LWFwaS1rZXk=
stringData:
  # Plain text (will be encoded)
  connection-string: "Server=db;Database=myapp;User=admin;Password=secret"
---
# Docker registry secret
apiVersion: v1
kind: Secret
metadata:
  name: registry-credentials
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-encoded-docker-config>
---
# TLS secret
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>
```

**Creating secrets via kubectl:**

```bash
# From literal values
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=secret123

# From file
kubectl create secret generic tls-secret \
  --from-file=tls.crt=./cert.pem \
  --from-file=tls.key=./key.pem

# Docker registry
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=user \
  --docker-password=password
```

### Namespace

Provides scope for names and resource isolation.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    env: production
    team: platform
---
# Resource Quota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    pods: "100"
    services: "20"
    persistentvolumeclaims: "20"
---
# Limit Range
apiVersion: v1
kind: LimitRange
metadata:
  name: production-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "512Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
      max:
        cpu: "2"
        memory: "4Gi"
      min:
        cpu: "50m"
        memory: "64Mi"
```

---

## Helm Charts

### Chart Structure

```
mychart/
├── Chart.yaml           # Chart metadata
├── Chart.lock           # Dependency lock file
├── values.yaml          # Default configuration values
├── values.schema.json   # JSON schema for values validation
├── .helmignore          # Files to ignore when packaging
├── templates/           # Template files
│   ├── NOTES.txt        # Post-install notes
│   ├── _helpers.tpl     # Template helpers
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── serviceaccount.yaml
│   ├── hpa.yaml
│   └── tests/
│       └── test-connection.yaml
├── charts/              # Dependency charts
└── crds/                # Custom Resource Definitions
```

### Chart.yaml

```yaml
apiVersion: v2
name: myapp
description: A Helm chart for MyApp
type: application
version: 1.0.0
appVersion: "2.0.0"
kubeVersion: ">=1.25.0"
keywords:
  - myapp
  - web
home: https://github.com/org/myapp
sources:
  - https://github.com/org/myapp
maintainers:
  - name: Platform Team
    email: platform@example.com
icon: https://example.com/icon.png
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled
  - name: redis
    version: "17.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
annotations:
  artifacthub.io/license: Apache-2.0
```

### values.yaml

```yaml
# Default values for myapp

# Number of replicas
replicaCount: 3

image:
  repository: myapp
  tag: "" # Defaults to Chart.appVersion
  pullPolicy: IfNotPresent

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  create: true
  annotations: {}
  name: ""

podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8080"

podSecurityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

securityContext:
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL

service:
  type: ClusterIP
  port: 80
  targetPort: 8080

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: myapp.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: myapp-tls
      hosts:
        - myapp.example.com

resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
  targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

# Application configuration
config:
  logLevel: info
  databaseUrl: ""
  featureFlags:
    newUI: true
    betaFeatures: false

# External dependencies
postgresql:
  enabled: true
  auth:
    database: myapp
    username: myapp

redis:
  enabled: false
```

### Template Helpers (\_helpers.tpl)

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
{{- define "myapp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "myapp.labels" -}}
helm.sh/chart: {{ include "myapp.chart" . }}
{{ include "myapp.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "myapp.selectorLabels" -}}
app.kubernetes.io/name: {{ include "myapp.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "myapp.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "myapp.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Return the proper image name
*/}}
{{- define "myapp.image" -}}
{{- $tag := .Values.image.tag | default .Chart.AppVersion }}
{{- printf "%s:%s" .Values.image.repository $tag }}
{{- end }}
```

### Deployment Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "myapp.fullname" . }}
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "myapp.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        {{- with .Values.podAnnotations }}
        {{- toYaml . | nindent 8 }}
        {{- end }}
      labels:
        {{- include "myapp.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "myapp.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: {{ include "myapp.image" . }}
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.targetPort }}
              protocol: TCP
          envFrom:
            - configMapRef:
                name: {{ include "myapp.fullname" . }}
            - secretRef:
                name: {{ include "myapp.fullname" . }}
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
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

### Helm Hooks

```yaml
# Pre-install/Pre-upgrade Job (e.g., database migration)
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-migrate
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    metadata:
      name: {{ include "myapp.fullname" . }}-migrate
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: {{ include "myapp.image" . }}
          command: ["./migrate.sh"]
          envFrom:
            - secretRef:
                name: {{ include "myapp.fullname" . }}
---
# Post-install Job (e.g., seed data)
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "myapp.fullname" . }}-seed
  annotations:
    "helm.sh/hook": post-install
    "helm.sh/hook-weight": "0"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: seed
          image: {{ include "myapp.image" . }}
          command: ["./seed.sh"]
```

### Helm Test

```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "myapp.fullname" . }}-test-connection"
  labels:
    {{- include "myapp.labels" . | nindent 4 }}
  annotations:
    "helm.sh/hook": test
spec:
  containers:
    - name: wget
      image: busybox
      command: ['wget']
      args: ['{{ include "myapp.fullname" . }}:{{ .Values.service.port }}/health']
  restartPolicy: Never
```

---

## kubectl Commands

### Resource Management

```bash
# Apply resources
kubectl apply -f manifest.yaml
kubectl apply -f ./manifests/ --recursive
kubectl apply -k ./kustomize/overlays/production/

# Create resources
kubectl create deployment nginx --image=nginx
kubectl create service clusterip nginx --tcp=80:80
kubectl create configmap app-config --from-file=config.properties
kubectl create secret generic db-secret --from-literal=password=secret

# Delete resources
kubectl delete pod myapp-pod
kubectl delete -f manifest.yaml
kubectl delete pods --all -n dev
kubectl delete pods -l app=myapp

# Edit resources
kubectl edit deployment myapp
kubectl patch deployment myapp -p '{"spec":{"replicas":5}}'
kubectl set image deployment/myapp app=myapp:v2
```

### Viewing Resources

```bash
# Get resources
kubectl get pods -o wide
kubectl get pods -o yaml
kubectl get pods -o json
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
kubectl get all -n production

# Describe resources
kubectl describe pod myapp-pod
kubectl describe node node-1

# Resource usage
kubectl top nodes
kubectl top pods --containers
kubectl top pods -A --sort-by=memory

# Watch resources
kubectl get pods -w
kubectl get events -w --sort-by='.lastTimestamp'
```

### Debugging

```bash
# Logs
kubectl logs myapp-pod
kubectl logs myapp-pod -c sidecar
kubectl logs myapp-pod --previous
kubectl logs -f myapp-pod
kubectl logs -l app=myapp --all-containers
kubectl logs myapp-pod --since=1h
kubectl logs myapp-pod --tail=100

# Execute commands
kubectl exec myapp-pod -- ls /app
kubectl exec -it myapp-pod -- /bin/sh
kubectl exec -it myapp-pod -c sidecar -- /bin/bash

# Copy files
kubectl cp myapp-pod:/app/logs/app.log ./app.log
kubectl cp ./config.yaml myapp-pod:/app/config.yaml

# Port forwarding
kubectl port-forward pod/myapp-pod 8080:80
kubectl port-forward svc/myapp 8080:80
kubectl port-forward deploy/myapp 8080:80

# Debug containers
kubectl debug myapp-pod -it --image=busybox --target=app
kubectl debug node/node-1 -it --image=ubuntu
```

### Deployment Operations

```bash
# Rollout management
kubectl rollout status deployment/myapp
kubectl rollout history deployment/myapp
kubectl rollout history deployment/myapp --revision=2
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2
kubectl rollout restart deployment/myapp
kubectl rollout pause deployment/myapp
kubectl rollout resume deployment/myapp

# Scaling
kubectl scale deployment myapp --replicas=5
kubectl autoscale deployment myapp --min=3 --max=10 --cpu-percent=70
```

### Context and Config

```bash
# Context management
kubectl config get-contexts
kubectl config current-context
kubectl config use-context production
kubectl config set-context --current --namespace=myapp

# Create contexts
kubectl config set-cluster dev --server=https://dev.k8s.local
kubectl config set-credentials admin --token=<token>
kubectl config set-context dev --cluster=dev --user=admin

# View config
kubectl config view
kubectl config view --minify
```

---

## Kustomize

### Directory Structure

```
kustomize/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── ingress.yaml
└── overlays/
    ├── development/
    │   ├── kustomization.yaml
    │   ├── replica-patch.yaml
    │   └── config-patch.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   └── namespace.yaml
    └── production/
        ├── kustomization.yaml
        ├── replica-patch.yaml
        ├── resource-patch.yaml
        └── hpa.yaml
```

### Base kustomization.yaml

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
  - ingress.yaml

commonLabels:
  app: myapp

commonAnnotations:
  team: platform

configMapGenerator:
  - name: app-config
    literals:
      - LOG_LEVEL=info

secretGenerator:
  - name: app-secrets
    literals:
      - API_KEY=default-key
    type: Opaque
```

### Production Overlay

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
  - ../../base
  - hpa.yaml
  - pdb.yaml

namePrefix: prod-
nameSuffix: ""

commonLabels:
  env: production

commonAnnotations:
  prometheus.io/scrape: "true"

replicas:
  - name: myapp
    count: 5

images:
  - name: myapp
    newTag: v2.0.0

configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - LOG_LEVEL=warn
      - ENABLE_DEBUG=false

patches:
  # Strategic merge patch
  - path: replica-patch.yaml
  # JSON patch
  - target:
      kind: Deployment
      name: myapp
    patch: |-
      - op: replace
        path: /spec/template/spec/containers/0/resources/limits/memory
        value: 1Gi
```

### Patches

```yaml
# replica-patch.yaml (Strategic Merge Patch)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  template:
    spec:
      containers:
        - name: app
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: 1000m
              memory: 1Gi
```

### Kustomize Commands

```bash
# Build and view output
kubectl kustomize ./overlays/production/
kustomize build ./overlays/production/

# Apply directly
kubectl apply -k ./overlays/production/

# Diff before applying
kubectl diff -k ./overlays/production/

# Build with specific output
kustomize build ./overlays/production/ -o ./rendered/
```

---

## Ingress & Networking

### Nginx Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "60"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "60"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/limit-rps: "50"
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - myapp.example.com
        - api.example.com
      secretName: myapp-tls
  rules:
    - host: myapp.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-frontend
                port:
                  number: 80
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: myapp-api
                port:
                  number: 80
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp-api
                port:
                  number: 80
```

### Network Policies

```yaml
# Default deny all ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
---
# Allow traffic from specific pods
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-api
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
        - namespaceSelector:
            matchLabels:
              name: monitoring
      ports:
        - protocol: TCP
          port: 8080
---
# Allow egress to external services
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-external-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
            except:
              - 10.0.0.0/8
              - 172.16.0.0/12
              - 192.168.0.0/16
      ports:
        - protocol: TCP
          port: 443
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

### Service Mesh (Istio Example)

```yaml
# VirtualService for traffic management
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
    - myapp
  http:
    - match:
        - headers:
            x-version:
              exact: v2
      route:
        - destination:
            host: myapp
            subset: v2
    - route:
        - destination:
            host: myapp
            subset: v1
          weight: 90
        - destination:
            host: myapp
            subset: v2
          weight: 10
---
# DestinationRule for load balancing
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
spec:
  host: myapp
  trafficPolicy:
    connectionPool:
      http:
        h2UpgradePolicy: UPGRADE
    loadBalancer:
      simple: ROUND_ROBIN
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

---

## RBAC & Security

### ServiceAccount

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: production
  annotations:
    # Azure Workload Identity
    azure.workload.identity/client-id: "<client-id>"
    # AWS IAM Role
    eks.amazonaws.com/role-arn: "arn:aws:iam::123456789:role/myapp-role"
automountServiceAccountToken: true
```

### Role and RoleBinding

```yaml
# Namespace-scoped Role
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: production
subjects:
  - kind: ServiceAccount
    name: myapp-sa
    namespace: production
  - kind: User
    name: developer@example.com
    apiGroup: rbac.authorization.k8s.io
  - kind: Group
    name: developers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

### ClusterRole and ClusterRoleBinding

```yaml
# Cluster-wide ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: namespace-admin
rules:
  - apiGroups: [""]
    resources: ["namespaces"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods", "services", "configmaps", "secrets"]
    verbs: ["*"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets", "statefulsets"]
    verbs: ["*"]
  - apiGroups: ["networking.k8s.io"]
    resources: ["ingresses"]
    verbs: ["*"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: namespace-admin-binding
subjects:
  - kind: Group
    name: platform-team
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: namespace-admin
  apiGroup: rbac.authorization.k8s.io
```

### Pod Security Standards

```yaml
# Pod Security Admission (Kubernetes 1.25+)
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
---
# Secure Pod Configuration
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
    - name: app
      image: myapp:1.0.0
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL
      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache
  volumes:
    - name: tmp
      emptyDir: {}
    - name: cache
      emptyDir: {}
```

---

## Autoscaling

### Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 20
  metrics:
    # CPU-based scaling
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    # Memory-based scaling
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    # Custom metric (Prometheus)
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: 1000
    # External metric
    - type: External
      external:
        metric:
          name: queue_messages_ready
          selector:
            matchLabels:
              queue: myapp-queue
        target:
          type: AverageValue
          averageValue: 30
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
        - type: Pods
          value: 2
          periodSeconds: 60
      selectPolicy: Min
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
        - type: Pods
          value: 4
          periodSeconds: 15
      selectPolicy: Max
```

### Vertical Pod Autoscaler (VPA)

```yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: myapp-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  updatePolicy:
    updateMode: "Auto" # Off, Initial, Recreate, Auto
  resourcePolicy:
    containerPolicies:
      - containerName: "*"
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 2
          memory: 4Gi
        controlledResources: ["cpu", "memory"]
```

### Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  # OR
  # maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

---

## Persistent Volumes

### PersistentVolume and PersistentVolumeClaim

```yaml
# Static PersistentVolume
apiVersion: v1
kind: PersistentVolume
metadata:
  name: myapp-pv
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /data/myapp
---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myapp-pvc
spec:
  storageClassName: managed-premium # Azure
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---
# Using PVC in Pod
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: app
      image: myapp:1.0.0
      volumeMounts:
        - mountPath: /data
          name: data-volume
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: myapp-pvc
```

### StorageClass

```yaml
# Azure Disk StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: managed-premium
provisioner: disk.csi.azure.com
parameters:
  skuName: Premium_LRS
  cachingMode: ReadOnly
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
---
# AWS EBS StorageClass
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

### StatefulSet with PVC Template

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  serviceName: database
  replicas: 3
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
        - name: postgres
          image: postgres:15
          ports:
            - containerPort: 5432
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
          env:
            - name: POSTGRES_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secrets
                  key: password
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        storageClassName: managed-premium
        resources:
          requests:
            storage: 50Gi
```

---

## Debugging & Troubleshooting

### Common Issues Checklist

| Issue                  | Diagnostic Commands                                     |
| ---------------------- | ------------------------------------------------------- |
| Pod not starting       | `kubectl describe pod <name>`, `kubectl get events`     |
| CrashLoopBackOff       | `kubectl logs <pod> --previous`, `kubectl describe pod` |
| ImagePullBackOff       | Check image name/tag, registry credentials              |
| Pending pod            | Check resource requests, node capacity, affinity rules  |
| Service not accessible | `kubectl get endpoints`, verify selectors match         |
| Ingress not working    | Check ingress controller, TLS secrets, annotations      |
| PVC pending            | Check StorageClass, available PVs                       |
| OOMKilled              | Increase memory limits, check for memory leaks          |

### Debugging Commands

```bash
# Pod debugging
kubectl describe pod <pod-name>
kubectl get pod <pod-name> -o yaml
kubectl logs <pod-name> --all-containers
kubectl logs <pod-name> --previous
kubectl get events --field-selector involvedObject.name=<pod-name>

# Network debugging
kubectl run debug --rm -it --image=nicolaka/netshoot -- /bin/bash
kubectl exec -it <pod> -- curl -v http://service-name:port
kubectl exec -it <pod> -- nslookup service-name
kubectl exec -it <pod> -- nc -zv service-name port

# Node debugging
kubectl describe node <node-name>
kubectl get node <node-name> -o yaml
kubectl top node
kubectl debug node/<node-name> -it --image=ubuntu

# Resource debugging
kubectl get pods -o wide --field-selector status.phase!=Running
kubectl get pods --all-namespaces -o jsonpath='{range .items[?(@.status.phase!="Running")]}{.metadata.namespace}/{.metadata.name}{"\n"}{end}'

# API resources
kubectl api-resources
kubectl explain deployment.spec.strategy
kubectl get --raw /metrics
```

### Debug Container

```yaml
# Ephemeral debug container
kubectl debug myapp-pod -it \
  --image=busybox \
  --target=app \
  --copy-to=myapp-debug

# Debug with network tools
kubectl debug myapp-pod -it \
  --image=nicolaka/netshoot \
  -- /bin/bash

# Node-level debugging
kubectl debug node/worker-1 -it --image=ubuntu
```

### Common Fixes

```bash
# Restart deployment
kubectl rollout restart deployment/myapp

# Force delete stuck pod
kubectl delete pod <pod> --grace-period=0 --force

# Patch deployment
kubectl patch deployment myapp -p '{"spec":{"template":{"metadata":{"annotations":{"restart":"'$(date +%s)'"}}}}}'

# Scale to fix issues
kubectl scale deployment myapp --replicas=0
kubectl scale deployment myapp --replicas=3

# Cordon/drain node
kubectl cordon <node>
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
kubectl uncordon <node>

# Check resource quotas
kubectl describe resourcequota -n <namespace>
kubectl describe limitrange -n <namespace>
```

### Health Check Patterns

```yaml
# Comprehensive health checks
spec:
  containers:
    - name: app
      # Startup probe (for slow-starting containers)
      startupProbe:
        httpGet:
          path: /health/startup
          port: 8080
        initialDelaySeconds: 10
        periodSeconds: 10
        failureThreshold: 30

      # Liveness probe (restart if fails)
      livenessProbe:
        httpGet:
          path: /health/live
          port: 8080
        initialDelaySeconds: 0
        periodSeconds: 15
        timeoutSeconds: 5
        failureThreshold: 3

      # Readiness probe (remove from service if fails)
      readinessProbe:
        httpGet:
          path: /health/ready
          port: 8080
        initialDelaySeconds: 0
        periodSeconds: 5
        timeoutSeconds: 3
        failureThreshold: 3
```

---

## Deployment Patterns

### Blue-Green Deployment

```yaml
# Blue deployment (current)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
  labels:
    app: myapp
    version: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue
  template:
    metadata:
      labels:
        app: myapp
        version: blue
    spec:
      containers:
        - name: app
          image: myapp:v1
---
# Green deployment (new version)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
  labels:
    app: myapp
    version: green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green
  template:
    metadata:
      labels:
        app: myapp
        version: green
    spec:
      containers:
        - name: app
          image: myapp:v2
---
# Service (switch between blue/green)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue # Change to 'green' to switch
  ports:
    - port: 80
      targetPort: 8080
```

### Canary Deployment

```yaml
# Stable deployment (90%)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-stable
spec:
  replicas: 9
  selector:
    matchLabels:
      app: myapp
      track: stable
  template:
    metadata:
      labels:
        app: myapp
        track: stable
    spec:
      containers:
        - name: app
          image: myapp:v1
---
# Canary deployment (10%)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-canary
spec:
  replicas: 1
  selector:
    matchLabels:
      app: myapp
      track: canary
  template:
    metadata:
      labels:
        app: myapp
        track: canary
    spec:
      containers:
        - name: app
          image: myapp:v2
---
# Service routes to both
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp # Matches both stable and canary
  ports:
    - port: 80
      targetPort: 8080
```

### Rolling Update Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2 # Can exceed replicas by 2
      maxUnavailable: 1 # At most 1 unavailable during update
  template:
    spec:
      containers:
        - name: app
          image: myapp:v2
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
      # Ensure graceful shutdown
      terminationGracePeriodSeconds: 60
```

### Multi-Environment Setup

```bash
# Development
helm upgrade --install myapp ./chart \
  -f values.yaml \
  -f values.dev.yaml \
  --namespace dev

# Staging
helm upgrade --install myapp ./chart \
  -f values.yaml \
  -f values.staging.yaml \
  --namespace staging

# Production
helm upgrade --install myapp ./chart \
  -f values.yaml \
  -f values.prod.yaml \
  --namespace production \
  --wait \
  --timeout 10m
```

---

## Best Practices Summary

### Security

- ✅ Run containers as non-root
- ✅ Use read-only root filesystem
- ✅ Drop all capabilities, add only what's needed
- ✅ Use Network Policies to restrict traffic
- ✅ Store secrets in external secret managers
- ✅ Enable Pod Security Standards
- ✅ Use RBAC with least privilege
- ✅ Scan images for vulnerabilities

### Reliability

- ✅ Set resource requests and limits
- ✅ Configure liveness and readiness probes
- ✅ Use Pod Disruption Budgets
- ✅ Spread pods across zones (topology spread)
- ✅ Use anti-affinity for critical workloads
- ✅ Configure appropriate replica counts
- ✅ Enable HPA for variable workloads

### Operations

- ✅ Use namespaces for isolation
- ✅ Label everything consistently
- ✅ Use Helm or Kustomize for templating
- ✅ Version control all manifests
- ✅ Implement GitOps workflows
- ✅ Monitor with Prometheus/Grafana
- ✅ Centralize logging (Loki, ELK)
- ✅ Document runbooks for common issues
