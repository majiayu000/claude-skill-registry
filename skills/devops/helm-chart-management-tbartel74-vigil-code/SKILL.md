---
name: helm-chart-management
description: Helm chart development and management for Vigil Guard v2.0.0. Use when creating Vigil Guard Helm charts, managing chart dependencies for 11 services including heuristics and semantic subcharts, configuring values for different environments, or publishing charts to repositories.
version: 2.0.0
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
---

# Vigil Guard Helm Chart Management (v2.0.0)

## Overview

Project-specific guidance for developing and managing Helm charts for Vigil Guard v2.0.0. This skill bridges the generic helm-expert knowledge with Vigil Guard's 3-branch parallel detection architecture (11 services).

## When to Use This Skill

- Creating Vigil Guard Helm chart from scratch
- Packaging existing Docker Compose setup (11 services) as Helm chart
- Managing multi-environment deployments (dev, staging, prod)
- Configuring chart dependencies for 3-branch detection
- Adding heuristics-service and semantic-service subcharts (v2.0.0)
- Publishing Vigil Guard chart to Artifact Hub or OCI registry
- Creating umbrella chart for all Vigil Guard services
- Templating Vigil Guard configurations (unified_config.json v5.0.0)

## Vigil Guard Chart Architecture (v2.0.0)

### Recommended Chart Structure

```
charts/
├── vigil-guard/                    # Umbrella chart
│   ├── Chart.yaml
│   ├── Chart.lock
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-staging.yaml
│   ├── values-prod.yaml
│   ├── templates/
│   │   ├── NOTES.txt
│   │   ├── _helpers.tpl
│   │   └── tests/
│   └── charts/                     # Subcharts (11 services)
│       ├── n8n/
│       ├── web-ui/
│       ├── presidio-pii/
│       ├── language-detector/
│       ├── prompt-guard/
│       ├── heuristics-service/     # NEW v2.0.0 - Branch A
│       ├── semantic-service/       # NEW v2.0.0 - Branch B
│       ├── clickhouse/
│       └── grafana/
└── vigil-guard-common/             # Library chart
    ├── Chart.yaml
    └── templates/
        └── _common.tpl
```

### Chart.yaml (Umbrella Chart - v2.0.0)

```yaml
apiVersion: v2
name: vigil-guard
version: 2.0.0
appVersion: "2.0.0"
description: |
  Enterprise-grade prompt injection detection and defense platform
  for Large Language Model applications with 3-branch parallel detection.
type: application
keywords:
  - security
  - llm
  - prompt-injection
  - pii-detection
  - ai-safety
  - 3-branch-detection
home: https://github.com/vigil-guard/vigil-guard
sources:
  - https://github.com/vigil-guard/vigil-guard
maintainers:
  - name: Vigil Guard Team
    email: team@vigil-guard.example
icon: https://vigil-guard.example/icon.png
dependencies:
  # Internal subcharts
  - name: n8n
    version: "2.x.x"
    repository: "file://charts/n8n"
    condition: n8n.enabled
  - name: web-ui
    version: "2.x.x"
    repository: "file://charts/web-ui"
    condition: webUI.enabled
  - name: presidio-pii
    version: "2.x.x"
    repository: "file://charts/presidio-pii"
    condition: presidio.enabled
  - name: language-detector
    version: "2.x.x"
    repository: "file://charts/language-detector"
    condition: languageDetector.enabled
  - name: prompt-guard
    version: "2.x.x"
    repository: "file://charts/prompt-guard"
    condition: promptGuard.enabled
  # v2.0.0: 3-Branch Detection subcharts
  - name: heuristics-service
    version: "2.x.x"
    repository: "file://charts/heuristics-service"
    condition: heuristics.enabled
  - name: semantic-service
    version: "2.x.x"
    repository: "file://charts/semantic-service"
    condition: semantic.enabled
  # External dependencies
  - name: clickhouse
    version: "4.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: clickhouse.enabled
  - name: grafana
    version: "7.x.x"
    repository: "https://grafana.github.io/helm-charts"
    condition: grafana.enabled
```

## Master values.yaml (v2.0.0)

```yaml
# values.yaml - Vigil Guard Umbrella Chart v2.0.0

global:
  # Image settings
  imageRegistry: ""
  imagePullSecrets: []
  storageClass: ""

  # Vigil Guard version
  vigilVersion: "2.0.0"

  # Network
  domain: "vigil.example.com"
  tlsEnabled: true

  # Security
  podSecurityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000

# ========================================
# n8n Workflow Engine (24-node pipeline)
# ========================================
n8n:
  enabled: true
  replicaCount: 1  # n8n doesn't support multiple replicas well

  image:
    repository: n8nio/n8n
    tag: "1.20.0"
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: 5678

  persistence:
    enabled: true
    size: 5Gi
    storageClass: ""

  resources:
    requests:
      cpu: 200m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 2Gi

  config:
    timezone: "Europe/Warsaw"
    webhookUrl: ""  # Auto-generated if empty

  # v2.0.0: 24-node workflow configuration
  workflow:
    autoImport: true
    configPath: /home/node/.n8n/config
    # 3-Branch service URLs
    heuristicsUrl: "http://vigil-heuristics:5005"
    semanticUrl: "http://vigil-semantic:5006"
    promptGuardUrl: "http://vigil-prompt-guard:8000"

# ========================================
# Heuristics Service (Branch A) - NEW v2.0.0
# ========================================
heuristics:
  enabled: true
  replicaCount: 2

  image:
    repository: vigil-guard/heuristics-service
    tag: ""  # Defaults to global.vigilVersion

  service:
    type: ClusterIP
    port: 5005

  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

  config:
    # Branch A weight in arbiter fusion
    weight: 0.30
    # Pattern matching timeout
    timeoutMs: 1000
    # Config file path
    configPath: /config/unified_config.json

# ========================================
# Semantic Service (Branch B) - NEW v2.0.0
# ========================================
semantic:
  enabled: true
  replicaCount: 2

  image:
    repository: vigil-guard/semantic-service
    tag: ""  # Defaults to global.vigilVersion

  service:
    type: ClusterIP
    port: 5006

  resources:
    requests:
      cpu: 200m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

  config:
    # Branch B weight in arbiter fusion
    weight: 0.35
    # Embedding model
    modelName: "all-MiniLM-L6-v2"
    embeddingDim: 384
    # Service timeout
    timeoutMs: 2000

# ========================================
# Prompt Guard (Branch C) - LLM Validation
# ========================================
promptGuard:
  enabled: false  # Optional component
  replicaCount: 1

  image:
    repository: vigil-guard/prompt-guard-api
    tag: ""

  service:
    type: ClusterIP
    port: 8000

  resources:
    requests:
      cpu: 500m
      memory: 2Gi
    limits:
      cpu: 2000m
      memory: 8Gi

  config:
    # Branch C weight in arbiter fusion
    weight: 0.35
    # Service timeout
    timeoutMs: 3000
    modelPath: /models/prompt-guard

  # Model download job
  modelDownload:
    enabled: true
    image: curlimages/curl:latest

# ========================================
# Web UI (Frontend + Backend)
# ========================================
webUI:
  enabled: true

  frontend:
    replicaCount: 2
    image:
      repository: vigil-guard/web-ui-frontend
      tag: ""  # Defaults to global.vigilVersion
    resources:
      requests:
        cpu: 50m
        memory: 64Mi
      limits:
        cpu: 200m
        memory: 128Mi

  backend:
    replicaCount: 2
    image:
      repository: vigil-guard/web-ui-backend
      tag: ""
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        cpu: 500m
        memory: 512Mi

    config:
      sessionSecret: ""  # Required, use existing secret
      jwtSecret: ""      # Required, use existing secret
      jwtExpiry: "24h"

    existingSecret: ""   # Name of existing secret with credentials

# ========================================
# Presidio PII Detection
# ========================================
presidio:
  enabled: true
  replicaCount: 2

  image:
    repository: vigil-guard/presidio-pii-api
    tag: "2.0.0"

  service:
    type: ClusterIP
    port: 5001

  resources:
    requests:
      cpu: 200m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

  config:
    dualLanguageMode: true
    languages:
      - "pl"
      - "en"
    scoreThreshold: 0.7
    contextEnhancement: true

# ========================================
# Language Detector
# ========================================
languageDetector:
  enabled: true
  replicaCount: 2

  image:
    repository: vigil-guard/language-detector
    tag: "1.0.1"

  service:
    type: ClusterIP
    port: 5002

  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

# ========================================
# Arbiter Configuration (v2.0.0)
# ========================================
arbiter:
  # Decision thresholds
  blockThreshold: 70
  sanitizeThreshold: 30
  # Branch weights (must sum to 1.0)
  branchWeights:
    a: 0.30  # Heuristics
    b: 0.35  # Semantic
    c: 0.35  # LLM Guard
  # Degradation behavior
  failsafeDecision: "BLOCK"  # When all branches fail

# ========================================
# ClickHouse Analytics (v2.0.0 Schema)
# ========================================
clickhouse:
  enabled: true

  # Using Bitnami ClickHouse chart
  auth:
    username: admin
    existingSecret: vigil-clickhouse-secret
    existingSecretKey: password

  persistence:
    enabled: true
    size: 50Gi
    storageClass: "ssd"

  resources:
    requests:
      cpu: 500m
      memory: 2Gi
    limits:
      cpu: 2000m
      memory: 8Gi

  # v2.0.0: Custom init scripts with branch columns
  initdbScripts:
    init-vigil.sql: |
      CREATE DATABASE IF NOT EXISTS n8n_logs;

      CREATE TABLE IF NOT EXISTS n8n_logs.events_processed (
        timestamp DateTime64(3),
        sessionId String,
        original_input String,
        final_status String,
        threat_score Float32,
        -- v2.0.0: 3-Branch columns
        branch_a_score Float32 DEFAULT 0,
        branch_b_score Float32 DEFAULT 0,
        branch_c_score Float32 DEFAULT 0,
        branch_a_timing_ms UInt32 DEFAULT 0,
        branch_b_timing_ms UInt32 DEFAULT 0,
        branch_c_timing_ms UInt32 DEFAULT 0,
        arbiter_decision String DEFAULT '',
        -- PII columns
        pii_detected UInt8 DEFAULT 0,
        pii_entities String DEFAULT '[]',
        detected_language String DEFAULT '',
        pipeline_version String DEFAULT '2.0.0'
      ) ENGINE = MergeTree()
      PARTITION BY toYYYYMM(timestamp)
      ORDER BY (timestamp, sessionId)
      TTL timestamp + INTERVAL 90 DAY;

# ========================================
# Grafana Monitoring
# ========================================
grafana:
  enabled: true

  # Using Grafana Helm chart
  adminPassword: ""  # Use existingSecret

  persistence:
    enabled: true
    size: 5Gi

  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: ClickHouse
          type: grafana-clickhouse-datasource
          url: http://vigil-clickhouse:8123
          access: proxy
          isDefault: true

  dashboardProviders:
    dashboardproviders.yaml:
      apiVersion: 1
      providers:
        - name: 'vigil-guard'
          folder: 'Vigil Guard'
          type: file
          options:
            path: /var/lib/grafana/dashboards/vigil-guard

  dashboardsConfigMaps:
    vigil-guard: vigil-grafana-dashboards

# ========================================
# Workflow Configuration (v2.0.0)
# ========================================
workflow:
  config:
    # v2.0.0: unified_config.json v5.0.0 (303 lines - patterns merged)
    unified:
      version: "5.0.0"
      normalization:
        unicode_form: "NFKC"
        max_iterations: 3
      thresholds:
        allow_max: 29
        sanitize_light_max: 64
        sanitize_heavy_max: 84
        block_min: 85
      pii_detection:
        presidio_enabled: true
        dual_language_mode: true
        languages: ["pl", "en"]
      arbiter:
        branch_a_weight: 0.30
        branch_b_weight: 0.35
        branch_c_weight: 0.35
        block_threshold: 70
        sanitize_threshold: 30
      categories:
        SQL_XSS_ATTACKS:
          base_weight: 50
          multiplier: 1.3
        PROMPT_INJECTION:
          base_weight: 60
          multiplier: 1.5
    # v2.0.0: pii.conf (361 lines)
    pii:
      entities:
        - PERSON
        - EMAIL
        - PHONE
        - PESEL
        - NIP
        - REGON
        - CREDIT_CARD
        - IBAN
      languages:
        - pl
        - en
      score_threshold: 0.7

# ========================================
# Ingress Configuration
# ========================================
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
  hosts:
    - host: vigil.example.com
      paths:
        - path: /ui
          pathType: Prefix
          service: web-ui-frontend
        - path: /api
          pathType: Prefix
          service: web-ui-backend
        - path: /n8n
          pathType: Prefix
          service: n8n
        - path: /grafana
          pathType: Prefix
          service: grafana
  tls:
    - secretName: vigil-tls
      hosts:
        - vigil.example.com

# ========================================
# Network Policies
# ========================================
networkPolicy:
  enabled: true
  # Allow traffic only within vigil-guard namespace
  # Plus ingress from ingress-nginx namespace

# ========================================
# Pod Disruption Budgets
# ========================================
podDisruptionBudget:
  enabled: true
  minAvailable: 1

# ========================================
# Service Account
# ========================================
serviceAccount:
  create: true
  annotations: {}
  name: ""

# ========================================
# Autoscaling
# ========================================
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80
```

## Environment-Specific Values (v2.0.0)

### values-dev.yaml

```yaml
global:
  domain: "vigil-dev.example.com"
  tlsEnabled: false
  vigilVersion: "2.0.0"

n8n:
  replicaCount: 1
  resources:
    requests:
      cpu: 100m
      memory: 256Mi

# v2.0.0: 3-Branch Detection (reduced replicas for dev)
heuristics:
  replicaCount: 1
  resources:
    requests:
      cpu: 50m
      memory: 128Mi

semantic:
  replicaCount: 1
  resources:
    requests:
      cpu: 100m
      memory: 256Mi

promptGuard:
  enabled: false  # Disable Branch C in dev for speed

webUI:
  frontend:
    replicaCount: 1
  backend:
    replicaCount: 1

presidio:
  replicaCount: 1

languageDetector:
  replicaCount: 1

clickhouse:
  persistence:
    size: 10Gi

ingress:
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-staging
```

### values-prod.yaml

```yaml
global:
  domain: "vigil.example.com"
  tlsEnabled: true
  vigilVersion: "2.0.0"

n8n:
  resources:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 4Gi

# v2.0.0: 3-Branch Detection (full production)
heuristics:
  replicaCount: 4
  resources:
    requests:
      cpu: 200m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi

semantic:
  replicaCount: 4
  resources:
    requests:
      cpu: 500m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 2Gi

promptGuard:
  enabled: true  # Enable Branch C in production
  replicaCount: 2
  resources:
    requests:
      cpu: 1000m
      memory: 4Gi
    limits:
      cpu: 4000m
      memory: 16Gi

webUI:
  frontend:
    replicaCount: 3
  backend:
    replicaCount: 3

presidio:
  replicaCount: 4

languageDetector:
  replicaCount: 3

clickhouse:
  persistence:
    size: 100Gi
    storageClass: "ssd-premium"
  resources:
    requests:
      cpu: 2000m
      memory: 8Gi
    limits:
      cpu: 4000m
      memory: 16Gi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20

podDisruptionBudget:
  enabled: true
  minAvailable: 2
```

## Common Tasks (v2.0.0)

### Create Vigil Guard Chart from Scratch

```bash
# 1. Create chart structure
helm create charts/vigil-guard
cd charts/vigil-guard

# 2. Remove default templates (we'll create custom ones)
rm -rf templates/*.yaml

# 3. Create subchart directories (11 services)
mkdir -p charts/{n8n,web-ui,presidio-pii,language-detector,prompt-guard,heuristics-service,semantic-service}

# 4. For each subchart:
for chart in n8n web-ui presidio-pii language-detector prompt-guard heuristics-service semantic-service; do
  helm create charts/$chart
  # Customize templates for each service
done

# 5. Update Chart.yaml with dependencies (including v2.0.0 branches)

# 6. Update umbrella chart dependencies
helm dependency update .

# 7. Lint all charts
helm lint .

# 8. Template to verify
helm template vigil-guard . -f values-dev.yaml
```

### Create Heuristics Service Subchart (v2.0.0)

```bash
# charts/heuristics-service/Chart.yaml
apiVersion: v2
name: heuristics-service
version: 2.0.0
appVersion: "2.0.0"
description: Heuristics pattern matching service (Branch A) for Vigil Guard
type: application
```

```yaml
# charts/heuristics-service/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "heuristics-service.fullname" . }}
  labels:
    {{- include "heuristics-service.labels" . | nindent 4 }}
    branch: "a"
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "heuristics-service.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "heuristics-service.selectorLabels" . | nindent 8 }}
        branch: "a"
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          env:
            - name: PORT
              value: "{{ .Values.service.port }}"
            - name: PATTERN_TIMEOUT_MS
              value: "{{ .Values.config.timeoutMs }}"
            - name: CONFIG_PATH
              value: "{{ .Values.config.configPath }}"
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          volumeMounts:
            - name: workflow-config
              mountPath: /config
              readOnly: true
          livenessProbe:
            httpGet:
              path: /health
              port: {{ .Values.service.port }}
            initialDelaySeconds: 10
          readinessProbe:
            httpGet:
              path: /health
              port: {{ .Values.service.port }}
            initialDelaySeconds: 5
      volumes:
        - name: workflow-config
          configMap:
            name: {{ .Release.Name }}-workflow-config
```

### Create Semantic Service Subchart (v2.0.0)

```yaml
# charts/semantic-service/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "semantic-service.fullname" . }}
  labels:
    {{- include "semantic-service.labels" . | nindent 4 }}
    branch: "b"
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "semantic-service.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "semantic-service.selectorLabels" . | nindent 8 }}
        branch: "b"
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          env:
            - name: PORT
              value: "{{ .Values.service.port }}"
            - name: MODEL_NAME
              value: "{{ .Values.config.modelName }}"
            - name: EMBEDDING_DIM
              value: "{{ .Values.config.embeddingDim }}"
            - name: TIMEOUT_MS
              value: "{{ .Values.config.timeoutMs }}"
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /health
              port: {{ .Values.service.port }}
            initialDelaySeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: {{ .Values.service.port }}
            initialDelaySeconds: 20
```

### Package and Publish Chart (v2.0.0)

```bash
# 1. Package chart
helm package charts/vigil-guard

# 2. Push to OCI registry
helm push vigil-guard-2.0.0.tgz oci://registry.example.com/charts

# 3. Or publish to chart repository
helm repo index . --url https://charts.example.com
# Upload index.yaml and .tgz to hosting

# 4. Add repository
helm repo add vigil-guard https://charts.example.com
helm repo update
```

### Deploy to Different Environments

```bash
# Development
helm upgrade --install vigil-guard ./charts/vigil-guard \
  -f ./charts/vigil-guard/values-dev.yaml \
  -n vigil-dev \
  --create-namespace

# Staging
helm upgrade --install vigil-guard ./charts/vigil-guard \
  -f ./charts/vigil-guard/values-staging.yaml \
  -n vigil-staging \
  --create-namespace

# Production (with extra safety)
helm upgrade --install vigil-guard ./charts/vigil-guard \
  -f ./charts/vigil-guard/values-prod.yaml \
  -n vigil-prod \
  --create-namespace \
  --atomic \
  --timeout 15m \
  --wait
```

### Upgrade with Custom Values (v2.0.0)

```bash
# Override specific values
helm upgrade vigil-guard ./charts/vigil-guard \
  -f values-prod.yaml \
  --set heuristics.replicaCount=6 \
  --set semantic.replicaCount=6 \
  --set global.vigilVersion=2.0.0 \
  -n vigil-prod

# Check diff before upgrade
helm diff upgrade vigil-guard ./charts/vigil-guard \
  -f values-prod.yaml \
  -n vigil-prod

# Update arbiter weights
helm upgrade vigil-guard ./charts/vigil-guard \
  -f values-prod.yaml \
  --set arbiter.branchWeights.a=0.25 \
  --set arbiter.branchWeights.b=0.40 \
  --set arbiter.branchWeights.c=0.35 \
  -n vigil-prod
```

### Add Custom Configuration (v2.0.0)

```yaml
# In templates/configmap-workflow.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "vigil-guard.fullname" . }}-workflow-config
  labels:
    {{- include "vigil-guard.labels" . | nindent 4 }}
data:
  # v2.0.0: unified_config.json v5.0.0 (patterns merged)
  unified_config.json: |
    {{- .Values.workflow.config.unified | toJson | nindent 4 }}
  # v2.0.0: pii.conf (361 lines)
  pii.conf: |
    {{- .Values.workflow.config.pii | toJson | nindent 4 }}
```

## Template Helpers (_helpers.tpl) - v2.0.0

```yaml
{{/*
Vigil Guard common labels
*/}}
{{- define "vigil-guard.labels" -}}
helm.sh/chart: {{ include "vigil-guard.chart" . }}
{{ include "vigil-guard.selectorLabels" . }}
app.kubernetes.io/version: {{ .Values.global.vigilVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/part-of: vigil-guard
pipeline-version: "2.0.0"
{{- end }}

{{/*
Generate service URL based on component
*/}}
{{- define "vigil-guard.serviceUrl" -}}
{{- $component := index . 0 -}}
{{- $root := index . 1 -}}
{{- $port := "" -}}
{{- if eq $component "n8n" }}{{ $port = "5678" }}{{ end -}}
{{- if eq $component "presidio" }}{{ $port = "5001" }}{{ end -}}
{{- if eq $component "language-detector" }}{{ $port = "5002" }}{{ end -}}
{{- if eq $component "clickhouse" }}{{ $port = "8123" }}{{ end -}}
{{/* v2.0.0: 3-Branch services */}}
{{- if eq $component "heuristics" }}{{ $port = "5005" }}{{ end -}}
{{- if eq $component "semantic" }}{{ $port = "5006" }}{{ end -}}
{{- if eq $component "prompt-guard" }}{{ $port = "8000" }}{{ end -}}
http://{{ include "vigil-guard.fullname" $root }}-{{ $component }}:{{ $port }}
{{- end }}

{{/*
Generate n8n webhook URL
*/}}
{{- define "vigil-guard.webhookUrl" -}}
{{- if .Values.n8n.config.webhookUrl -}}
{{ .Values.n8n.config.webhookUrl }}
{{- else if .Values.ingress.enabled -}}
{{- $scheme := ternary "https" "http" .Values.global.tlsEnabled -}}
{{ $scheme }}://{{ .Values.global.domain }}/n8n
{{- else -}}
http://{{ include "vigil-guard.fullname" . }}-n8n:5678
{{- end -}}
{{- end }}

{{/*
v2.0.0: Generate arbiter configuration
*/}}
{{- define "vigil-guard.arbiterConfig" -}}
branch_weights:
  a: {{ .Values.arbiter.branchWeights.a }}
  b: {{ .Values.arbiter.branchWeights.b }}
  c: {{ .Values.arbiter.branchWeights.c }}
block_threshold: {{ .Values.arbiter.blockThreshold }}
sanitize_threshold: {{ .Values.arbiter.sanitizeThreshold }}
failsafe_decision: {{ .Values.arbiter.failsafeDecision }}
{{- end }}
```

## Troubleshooting (v2.0.0)

### Chart Lint Errors

```bash
# Fix common lint errors
helm lint ./charts/vigil-guard --strict

# Common issues:
# - Missing required values: Add defaults or required() function
# - Invalid YAML: Check indentation, use yamllint
# - Deprecated API versions: Update to current K8s versions
```

### Dependency Issues

```bash
# Update dependencies (including v2.0.0 heuristics and semantic)
helm dependency update ./charts/vigil-guard

# Verify dependencies downloaded
ls ./charts/vigil-guard/charts/

# Check dependency versions
helm dependency list ./charts/vigil-guard
```

### Template Rendering Errors

```bash
# Debug with --debug flag
helm template vigil-guard ./charts/vigil-guard --debug 2>&1 | less

# Check specific template (v2.0.0 heuristics)
helm template vigil-guard ./charts/vigil-guard \
  -s charts/heuristics-service/templates/deployment.yaml

# Validate with kubeval
helm template vigil-guard ./charts/vigil-guard | kubeval --strict
```

### Branch Service Issues

```bash
# Test branch service templates
helm template vigil-guard ./charts/vigil-guard \
  -s charts/heuristics-service/templates/deployment.yaml \
  -s charts/semantic-service/templates/deployment.yaml

# Verify branch weights sum to 1.0
helm template vigil-guard ./charts/vigil-guard | grep -A5 "branch_weights"
```

## Best Practices (v2.0.0)

1. **Use library charts** for common templates (_helpers.tpl)
2. **Validate values** with values.schema.json
3. **Version bump Chart.yaml** on every change (currently 2.0.0)
4. **Test with helm test** hooks after deployment
5. **Use --atomic** for production upgrades
6. **Separate values files** per environment
7. **Document all values** in README.md
8. **Use existing secrets** instead of generating
9. **Add NOTES.txt** with post-install instructions
10. **Pin dependency versions** (avoid wildcards in prod)
11. **Label branch services** with branch: a|b|c
12. **Configure arbiter weights** in values.yaml (must sum to 1.0)

## Related Skills

- `kubernetes-operations` - For K8s deployment details (11 services)
- `n8n-vigil-workflow` - For 24-node workflow configuration
- `docker-vigil-orchestration` - For Docker Compose reference
- `clickhouse-grafana-monitoring` - For monitoring with branch columns

## References

- Docker Compose: `docker-compose.yml` (11 services)
- Service structure: `services/*/`
- Workflow: `services/workflow/workflows/Vigil Guard v2.0.0.json` (24 nodes)
- Config: `services/workflow/config/unified_config.json` (v5.0.0, 303 lines)
- PII: `services/workflow/config/pii.conf` (361 lines)

---

**Last Updated:** 2025-12-09
**Version:** v2.0.0
**Architecture:** 3-Branch Parallel Detection (24 nodes)
**Services:** 11 Docker containers (9 subcharts + 2 external)
**Branch Weights:** A:30%, B:35%, C:35%
