---
name: helm-production-patterns
description: Implement production deployment strategies including secrets management, blue-green deployments, canary releases, and upgrade procedures. Use when deploying charts to production, implementing secrets management, setting up blue-green or canary deployments, configuring chart testing strategies, or planning upgrade and rollback procedures.
version: 1.0.0
dependencies: helm>=3.0, kubectl>=1.19
---

# Helm Production Deployment Patterns

## Purpose
Provide production-proven patterns for deploying Helm charts safely and reliably, including secrets management, testing strategies, deployment patterns, and upgrade procedures.

## Secrets Management

### Using Helm Secrets Plugin

**Installation:**
```bash
# Install helm-secrets plugin
helm plugin install https://github.com/jkroepke/helm-secrets
```

**Usage:**
```bash
# Encrypt secrets file with SOPS
helm secrets enc secrets.yaml

# Install with encrypted secrets
helm secrets install myrelease . -f secrets.yaml

# Upgrade with encrypted secrets
helm secrets upgrade myrelease . -f secrets.yaml

# View decrypted secrets (without applying)
helm secrets view secrets.yaml
```

**Secrets file structure:**
```yaml
# secrets.yaml (before encryption)
database:
  password: supersecretpassword123
  connectionString: postgresql://user:pass@host:5432/db

api:
  apiKey: sk-abc123def456
  webhookSecret: whsec_xyz789
```

### External Secrets Operator

**SecretStore configuration:**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: {{ .Release.Namespace }}
spec:
  provider:
    vault:
      server: "https://vault.example.com"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp-prod"
```

**ExternalSecret definition:**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ include "mychart.fullname" . }}-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: {{ include "mychart.fullname" . }}-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-password
    remoteRef:
      key: myapp/database
      property: password
```

## Testing Strategies

### Unit Testing with helm-unittest

**Installation:**
```bash
helm plugin install https://github.com/helm-unittest/helm-unittest
```

**Test file example:**
```yaml
# tests/deployment_test.yaml
suite: test deployment
templates:
  - deployment.yaml
tests:
  - it: should create deployment with correct replicas
    set:
      replicaCount: 3
    asserts:
      - equal:
          path: spec.replicas
          value: 3

  - it: should have resource limits
    asserts:
      - exists:
          path: spec.template.spec.containers[0].resources.limits
      - equal:
          path: spec.template.spec.containers[0].resources.limits.cpu
          value: 500m

  - it: should use specific image tag
    set:
      image.tag: "1.2.3"
    asserts:
      - equal:
          path: spec.template.spec.containers[0].image
          value: "myapp:1.2.3"

  - it: should have security context
    asserts:
      - equal:
          path: spec.template.spec.securityContext.runAsNonRoot
          value: true
```

**Run tests:**
```bash
# Run all tests
helm unittest charts/myapp

# Run specific test file
helm unittest -f tests/deployment_test.yaml charts/myapp
```

### Integration Testing with helm test

**Test pod definition:**
```yaml
# templates/tests/test-connection.yaml
apiVersion: v1
kind: Pod
metadata:
  name: "{{ include "mychart.fullname" . }}-test-connection"
  annotations:
    "helm.sh/hook": test
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  restartPolicy: Never
  containers:
    - name: test
      image: curlimages/curl:latest
      command:
        - sh
        - -c
        - |
          echo "Testing service connectivity..."
          curl -f http://{{ include "mychart.fullname" . }}:{{ .Values.service.port }}/healthz
          echo "Service is healthy"
```

**Run integration tests:**
```bash
# Install chart
helm install myrelease ./charts/myapp --namespace test --create-namespace

# Run tests
helm test myrelease --namespace test

# View test logs
kubectl logs -n test myrelease-test-connection
```

## Multi-Stage Deployment

### Database Migration Pre-Upgrade Hook

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-migration
  annotations:
    "helm.sh/hook": pre-upgrade,pre-install
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migration
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          command: ["./migrate"]
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ include "mychart.fullname" . }}-secrets
                  key: database-url
```

### Backup Job Before Upgrade

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-backup
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-10"
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: backup
          image: postgres:14-alpine
          command:
            - sh
            - -c
            - |
              pg_dump $DATABASE_URL > /backup/dump-$(date +%Y%m%d-%H%M%S).sql
              echo "Backup completed"
```

## Rolling Update Configuration

**Deployment strategy:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  replicas: {{ .Values.replicaCount }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: {{ .Values.rollingUpdate.maxSurge | default "25%" }}
      maxUnavailable: {{ .Values.rollingUpdate.maxUnavailable | default "25%" }}
```

**Conservative rolling update (Production):**
```yaml
# values-prod.yaml
rollingUpdate:
  maxSurge: 1           # Add 1 pod at a time
  maxUnavailable: 0     # Never reduce available pods

replicaCount: 3         # Ensure redundancy
```

**Aggressive rolling update (Development):**
```yaml
# values-dev.yaml
rollingUpdate:
  maxSurge: "100%"      # Double pods during update
  maxUnavailable: "50%" # Allow half to be unavailable

replicaCount: 2
```

## Pod Disruption Budget

```yaml
{{- if .Values.podDisruptionBudget.enabled }}
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  {{- if .Values.podDisruptionBudget.minAvailable }}
  minAvailable: {{ .Values.podDisruptionBudget.minAvailable }}
  {{- end }}
  {{- if .Values.podDisruptionBudget.maxUnavailable }}
  maxUnavailable: {{ .Values.podDisruptionBudget.maxUnavailable }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
{{- end }}
```

**Values:**
```yaml
podDisruptionBudget:
  enabled: true
  minAvailable: 1        # At least 1 pod always available
```

## Monitoring and Observability

**ServiceMonitor for Prometheus:**
```yaml
{{- if .Values.monitoring.serviceMonitor.enabled }}
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  endpoints:
    - port: metrics
      interval: {{ .Values.monitoring.serviceMonitor.interval }}
      path: {{ .Values.monitoring.serviceMonitor.path }}
{{- end }}
```

## Upgrade Procedures

### Pre-Upgrade Checklist

```bash
# 1. Review changes
helm diff upgrade myrelease ./charts/myapp

# 2. Backup current state
helm get values myrelease > myrelease-backup-values.yaml
helm get manifest myrelease > myrelease-backup-manifest.yaml

# 3. Dry run upgrade
helm upgrade myrelease ./charts/myapp --dry-run --debug

# 4. Perform upgrade
helm upgrade myrelease ./charts/myapp \
  --wait \
  --timeout 10m \
  --atomic  # Rollback on failure
```

### Safe Upgrade Pattern

```bash
# Upgrade with safety features
helm upgrade myrelease ./charts/myapp \
  --install \           # Install if doesn't exist
  --create-namespace \  # Create namespace if needed
  --wait \              # Wait for resources to be ready
  --wait-for-jobs \     # Wait for Jobs to complete
  --timeout 10m \       # Timeout after 10 minutes
  --atomic \            # Rollback on failure
  --cleanup-on-fail     # Delete new resources on failure
```

### Rollback Procedure

```bash
# View release history
helm history myrelease

# Rollback to previous revision
helm rollback myrelease

# Rollback to specific revision
helm rollback myrelease 3

# Rollback with options
helm rollback myrelease 3 \
  --wait \
  --timeout 5m \
  --cleanup-on-fail
```

## Production Deployment Checklist

### Pre-Deployment

- [ ] All tests pass (unit, integration, E2E)
- [ ] Security scanning completed
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped appropriately
- [ ] Tested in staging
- [ ] Rollback procedure documented
- [ ] Resource quotas validated
- [ ] Network policies tested
- [ ] Monitoring/alerting configured
- [ ] On-call engineer notified

### During Deployment

- [ ] Execute pre-upgrade hooks (backups, migrations)
- [ ] Monitor pod rollout status
- [ ] Check application logs for errors
- [ ] Verify metrics in monitoring dashboard
- [ ] Run smoke tests
- [ ] Verify traffic routing

### Post-Deployment

- [ ] Smoke tests pass
- [ ] Metrics flowing correctly
- [ ] Logs accessible
- [ ] Alerts functioning
- [ ] Team notified
- [ ] Post-deployment review scheduled

## Blue-Green Deployment Pattern

**Service selector pattern:**
```yaml
{{- if .Values.blueGreen.enabled }}
apiVersion: v1
kind: Service
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  selector:
    {{- include "mychart.selectorLabels" . | nindent 4 }}
    slot: {{ .Values.blueGreen.activeSlot }}  # "blue" or "green"
  ports:
    - port: {{ .Values.service.port }}
---
# Blue deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}-blue
spec:
  replicas: {{ if eq .Values.blueGreen.activeSlot "blue" }}{{ .Values.replicaCount }}{{ else }}0{{ end }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
      slot: blue
---
# Green deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}-green
spec:
  replicas: {{ if eq .Values.blueGreen.activeSlot "green" }}{{ .Values.replicaCount }}{{ else }}0{{ end }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
      slot: green
{{- end }}
```

**Switch traffic:**
```yaml
# values.yaml
blueGreen:
  enabled: true
  activeSlot: blue  # Switch to "green" to flip traffic
```

## Canary Deployment with Flagger

**Canary resource:**
```yaml
{{- if .Values.canary.enabled }}
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: {{ include "mychart.fullname" . }}
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ include "mychart.fullname" . }}

  service:
    port: {{ .Values.service.port }}

  analysis:
    interval: {{ .Values.canary.analysis.interval }}
    threshold: {{ .Values.canary.analysis.threshold }}
    maxWeight: {{ .Values.canary.analysis.maxWeight }}
    stepWeight: {{ .Values.canary.analysis.stepWeight }}

    metrics:
      - name: request-success-rate
        thresholdRange:
          min: {{ .Values.canary.successRate }}
        interval: 1m
{{- end }}
```

**Values:**
```yaml
canary:
  enabled: false
  analysis:
    interval: 30s
    threshold: 5
    maxWeight: 50
    stepWeight: 10
  successRate: 99
```

## Validation Commands

```bash
# Validate chart structure
helm lint ./charts/myapp

# Render templates
helm template myapp ./charts/myapp --debug

# Dry run installation
helm install test ./charts/myapp --dry-run --debug

# Install chart
helm install myrelease ./charts/myapp

# Upgrade chart
helm upgrade myrelease ./charts/myapp --wait --atomic

# Rollback
helm rollback myrelease

# Uninstall
helm uninstall myrelease
```

## Resources

- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Secrets Plugin](https://github.com/jkroepke/helm-secrets)
- [External Secrets Operator](https://external-secrets.io/)
- [Helm Unittest Plugin](https://github.com/helm-unittest/helm-unittest)
- [Flagger Documentation](https://flagger.app/)

---

## Related Agent

For comprehensive Helm/Kubernetes guidance that coordinates this and other Helm skills, use the **`helm-kubernetes-expert`** agent.
