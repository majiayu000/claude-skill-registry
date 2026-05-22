---
name: faion-k8s-cli-skill
user-invocable: false
description: ""
---

# Kubernetes CLI Skill

**Comprehensive guide for Kubernetes operations with kubectl, Helm, and Kustomize**

---

## Quick Reference

**Supported versions:**
- Kubernetes: 1.28+ (prefer 1.30+)
- kubectl: match cluster version
- Helm: 3.12+
- Kustomize: built into kubectl 1.14+

---

## kubectl Operations

### Resource Management

```bash
# Get resources
kubectl get pods                          # List pods
kubectl get pods -o wide                  # With node info
kubectl get pods -A                       # All namespaces
kubectl get pods -l app=myapp             # By label
kubectl get pods --field-selector=status.phase=Running

# Describe (detailed info)
kubectl describe pod <pod-name>
kubectl describe deployment <deploy-name>
kubectl describe service <svc-name>

# Create/Apply
kubectl apply -f manifest.yaml            # Apply config
kubectl apply -f ./manifests/             # Apply directory
kubectl apply -k ./kustomize/             # Apply with kustomize

# Delete
kubectl delete -f manifest.yaml
kubectl delete pod <pod-name>
kubectl delete pod <pod-name> --grace-period=0 --force  # Force delete
```

### Common Resource Types

| Resource | Short | Description |
|----------|-------|-------------|
| pods | po | Running containers |
| deployments | deploy | Manages ReplicaSets |
| services | svc | Network endpoints |
| configmaps | cm | Configuration data |
| secrets | - | Sensitive data |
| ingress | ing | HTTP routing |
| persistentvolumeclaims | pvc | Storage claims |
| namespaces | ns | Cluster partitions |
| nodes | no | Cluster nodes |
| replicasets | rs | Pod replicas |
| daemonsets | ds | Node-level pods |
| statefulsets | sts | Stateful apps |
| jobs | - | One-time tasks |
| cronjobs | cj | Scheduled tasks |

### Namespace Operations

```bash
# Namespace context
kubectl config set-context --current --namespace=<ns>
kubectl get pods -n <namespace>

# Create namespace
kubectl create namespace <name>

# Resource quotas
kubectl get resourcequotas -n <namespace>
kubectl describe resourcequota -n <namespace>
```

---

## Deployments

### Creating Deployments

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
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
      - name: myapp
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
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
        - name: ENV
          value: "production"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: password
```

### Scaling

```bash
# Manual scaling
kubectl scale deployment myapp --replicas=5

# Autoscaling (HPA)
kubectl autoscale deployment myapp --min=2 --max=10 --cpu-percent=80

# Check HPA status
kubectl get hpa
kubectl describe hpa myapp
```

### Rollouts

```bash
# Update image
kubectl set image deployment/myapp myapp=myapp:2.0.0

# Rollout status
kubectl rollout status deployment/myapp

# Rollout history
kubectl rollout history deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp
kubectl rollout undo deployment/myapp --to-revision=2

# Pause/Resume
kubectl rollout pause deployment/myapp
kubectl rollout resume deployment/myapp
```

### Update Strategies

```yaml
# Rolling Update (default)
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%

# Recreate (all at once)
spec:
  strategy:
    type: Recreate
```

---

## Services

### Service Types

```yaml
# ClusterIP (internal only)
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 8080

# NodePort (external via node port)
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080

# LoadBalancer (cloud provider LB)
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
```

### Service Discovery

```bash
# DNS format: <service>.<namespace>.svc.cluster.local
# Example: myapp-service.default.svc.cluster.local

# Get endpoints
kubectl get endpoints myapp-service

# Test service
kubectl run curl --image=curlimages/curl -it --rm -- curl http://myapp-service:80
```

---

## ConfigMaps and Secrets

### ConfigMaps

```bash
# Create from literal
kubectl create configmap myconfig --from-literal=key1=value1 --from-literal=key2=value2

# Create from file
kubectl create configmap myconfig --from-file=config.properties

# Create from env file
kubectl create configmap myconfig --from-env-file=config.env
```

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: myconfig
data:
  DATABASE_HOST: "postgres.default.svc.cluster.local"
  LOG_LEVEL: "info"
  config.json: |
    {
      "key": "value",
      "nested": {
        "key": "value"
      }
    }
```

### Secrets

```bash
# Create generic secret
kubectl create secret generic mysecret --from-literal=password=s3cr3t

# Create TLS secret
kubectl create secret tls mytls --cert=tls.crt --key=tls.key

# Create docker registry secret
kubectl create secret docker-registry regcred \
  --docker-server=https://index.docker.io/v1/ \
  --docker-username=user \
  --docker-password=password
```

```yaml
# secret.yaml (values must be base64 encoded)
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  password: cGFzc3dvcmQ=    # base64 of "password"
  api-key: YXBpLWtleQ==    # base64 of "api-key"
```

### Using ConfigMaps/Secrets in Pods

```yaml
spec:
  containers:
  - name: myapp
    # As environment variables
    env:
    - name: DATABASE_HOST
      valueFrom:
        configMapKeyRef:
          name: myconfig
          key: DATABASE_HOST
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: mysecret
          key: password
    # All keys as env vars
    envFrom:
    - configMapRef:
        name: myconfig
    - secretRef:
        name: mysecret
    # As volume mount
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
  volumes:
  - name: config-volume
    configMap:
      name: myconfig
```

---

## Ingress

### Basic Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  ingressClassName: nginx
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### TLS Ingress

```yaml
spec:
  tls:
  - hosts:
    - myapp.example.com
    secretName: myapp-tls
  rules:
  - host: myapp.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: myapp-service
            port:
              number: 80
```

### Common Annotations (nginx-ingress)

```yaml
annotations:
  # Rate limiting
  nginx.ingress.kubernetes.io/limit-rps: "10"

  # SSL redirect
  nginx.ingress.kubernetes.io/ssl-redirect: "true"

  # Proxy settings
  nginx.ingress.kubernetes.io/proxy-body-size: "10m"
  nginx.ingress.kubernetes.io/proxy-read-timeout: "60"

  # CORS
  nginx.ingress.kubernetes.io/enable-cors: "true"
  nginx.ingress.kubernetes.io/cors-allow-origin: "https://example.com"
```

---

## NetworkPolicies

### Default Deny All

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
```

### Allow Specific Traffic

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-myapp
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

---

## Helm

### Chart Management

```bash
# Add repository
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# Search charts
helm search repo nginx
helm search hub postgres

# Install chart
helm install myrelease bitnami/nginx
helm install myrelease bitnami/nginx -f values.yaml
helm install myrelease bitnami/nginx --set service.type=LoadBalancer

# Upgrade
helm upgrade myrelease bitnami/nginx -f values.yaml
helm upgrade --install myrelease bitnami/nginx  # Install or upgrade

# Rollback
helm rollback myrelease 1

# Uninstall
helm uninstall myrelease

# List releases
helm list
helm list -A  # All namespaces

# Show chart info
helm show values bitnami/nginx
helm show chart bitnami/nginx
```

### Creating Charts

```bash
# Create new chart
helm create mychart
```

**Chart Structure:**

```
mychart/
  Chart.yaml          # Chart metadata
  values.yaml         # Default values
  charts/             # Dependencies
  templates/          # Kubernetes manifests
    deployment.yaml
    service.yaml
    ingress.yaml
    configmap.yaml
    _helpers.tpl      # Template helpers
    NOTES.txt         # Post-install notes
```

### Chart.yaml

```yaml
apiVersion: v2
name: mychart
description: ""
type: application
version: 0.1.0
appVersion: "1.0.0"
dependencies:
- name: postgresql
  version: "12.x.x"
  repository: https://charts.bitnami.com/bitnami
  condition: postgresql.enabled
```

### values.yaml

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
  - host: myapp.example.com
    paths:
    - path: /
      pathType: Prefix

resources:
  limits:
    cpu: 500m
    memory: 128Mi
  requests:
    cpu: 250m
    memory: 64Mi

postgresql:
  enabled: true
  auth:
    database: myapp
```

### Template Helpers (_helpers.tpl)

```yaml
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
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}
```

### Template Usage

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-{{ .Chart.Name }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    spec:
      containers:
      - name: {{ .Chart.Name }}
        image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
        {{- if .Values.resources }}
        resources:
          {{- toYaml .Values.resources | nindent 12 }}
        {{- end }}
```

---

## Kustomize

### Basic Structure

```
base/
  deployment.yaml
  service.yaml
  kustomization.yaml
overlays/
  development/
    kustomization.yaml
  production/
    kustomization.yaml
    replica-patch.yaml
```

### base/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
- deployment.yaml
- service.yaml

commonLabels:
  app: myapp

images:
- name: myapp
  newTag: latest
```

### overlays/production/kustomization.yaml

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

resources:
- ../../base

namePrefix: prod-

commonLabels:
  environment: production

images:
- name: myapp
  newTag: v1.0.0

patches:
- path: replica-patch.yaml
```

### Patches

```yaml
# Strategic merge patch
# replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5

# JSON patch
patches:
- target:
    kind: Deployment
    name: myapp
  patch: |-
    - op: replace
      path: /spec/replicas
      value: 5
```

### Apply Kustomize

```bash
# Preview
kubectl kustomize overlays/production

# Apply
kubectl apply -k overlays/production
```

---

## Monitoring (Prometheus)

### ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-monitor
  labels:
    release: prometheus
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### PrometheusRule

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: myapp-alerts
  labels:
    release: prometheus
spec:
  groups:
  - name: myapp
    rules:
    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: High error rate on {{ $labels.instance }}
```

### Common PromQL Queries

```promql
# Container CPU usage
rate(container_cpu_usage_seconds_total{container!=""}[5m])

# Container memory usage
container_memory_usage_bytes{container!=""}

# Pod restart count
kube_pod_container_status_restarts_total

# HTTP request rate
rate(http_requests_total[5m])

# HTTP error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# P99 latency
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

---

## Debugging Patterns

### Pod Debugging

```bash
# Get pod logs
kubectl logs <pod-name>
kubectl logs <pod-name> -c <container>    # Specific container
kubectl logs <pod-name> --previous        # Previous instance
kubectl logs <pod-name> -f                # Follow
kubectl logs <pod-name> --tail=100        # Last 100 lines

# Exec into pod
kubectl exec -it <pod-name> -- /bin/sh
kubectl exec -it <pod-name> -c <container> -- /bin/bash

# Copy files
kubectl cp <pod-name>:/path/to/file ./local-file
kubectl cp ./local-file <pod-name>:/path/to/file

# Port forward
kubectl port-forward pod/<pod-name> 8080:80
kubectl port-forward svc/<svc-name> 8080:80
```

### Debugging Pods

```bash
# Pod not starting
kubectl describe pod <pod-name>           # Check Events section
kubectl get pod <pod-name> -o yaml        # Full spec

# Common issues
# - ImagePullBackOff: Check image name, registry auth
# - CrashLoopBackOff: Check logs, resource limits
# - Pending: Check node resources, selectors
# - ContainerCreating: Check PVC, configmaps, secrets

# Debug with ephemeral container
kubectl debug <pod-name> -it --image=busybox

# Debug node
kubectl debug node/<node-name> -it --image=ubuntu
```

### Events and Status

```bash
# Cluster events
kubectl get events --sort-by='.lastTimestamp'
kubectl get events -A --field-selector type=Warning

# Resource status
kubectl get pods -o custom-columns=\
NAME:.metadata.name,\
STATUS:.status.phase,\
RESTARTS:.status.containerStatuses[0].restartCount

# API resources
kubectl api-resources
kubectl explain deployment.spec.strategy
```

### Network Debugging

```bash
# Test DNS
kubectl run dnsutils --image=tutum/dnsutils -it --rm -- nslookup kubernetes

# Test connectivity
kubectl run curl --image=curlimages/curl -it --rm -- curl -v http://service:port

# Check endpoints
kubectl get endpoints <service-name>

# Check network policies
kubectl get networkpolicies
kubectl describe networkpolicy <name>
```

### Resource Troubleshooting

```bash
# Node resources
kubectl top nodes
kubectl describe node <node-name>

# Pod resources
kubectl top pods
kubectl top pods --containers

# Resource quotas
kubectl describe resourcequota -n <namespace>
kubectl describe limitrange -n <namespace>
```

---

## Best Practices

### Resource Requests/Limits

```yaml
resources:
  requests:           # Guaranteed resources
    memory: "64Mi"
    cpu: "250m"
  limits:             # Maximum allowed
    memory: "128Mi"
    cpu: "500m"
```

### Health Checks

```yaml
# Liveness: Restart container if fails
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3

# Readiness: Remove from service if fails
readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5

# Startup: Wait for slow starting containers
startupProbe:
  httpGet:
    path: /health
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

### Security Context

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

### Pod Disruption Budget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 2
  # or: maxUnavailable: 1
  selector:
    matchLabels:
      app: myapp
```

---

## References

For detailed information:

- [Kubernetes Docs](https://kubernetes.io/docs/home/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Helm Docs](https://helm.sh/docs/)
- [Kustomize Docs](https://kustomize.io/)
- [Prometheus Operator](https://prometheus-operator.dev/)
