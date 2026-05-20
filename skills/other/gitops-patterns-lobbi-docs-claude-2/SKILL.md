---
name: GitOps Patterns
description: ArgoCD ApplicationSets, progressive delivery, Harness GitX, and multi-cluster GitOps patterns
version: 1.0.0
trigger_phrases:
  - "gitops patterns"
  - "applicationset"
  - "progressive delivery"
  - "argocd sync"
  - "canary deployment"
  - "blue green"
  - "harness gitx"
  - "multi-cluster"
  - "fleet management"
categories: ["gitops", "deployment", "kubernetes", "progressive-delivery"]
---

# GitOps Patterns Skill

## When to Use This Skill

Use this skill when you need to:
- Design ApplicationSet generators for multi-environment deployments
- Implement progressive delivery strategies (canary, blue-green, A/B testing)
- Configure Harness GitX for bi-directional Git synchronization
- Set up sync policies and health assessment patterns
- Design multi-cluster deployment architectures
- Implement fleet management for Kubernetes clusters
- Configure automated rollback and promotion strategies
- Establish GitOps best practices for enterprise deployments

## GitOps Pattern Capabilities

### 1. ApplicationSet Generators

ApplicationSets enable automated generation of multiple Applications from templates, supporting multi-environment and multi-cluster deployments.

#### List Generator: Static Environment Lists

**Use Case:** Fixed set of environments with explicit configuration per environment.

**Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: multi-environment-app
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - environment: dev
            cluster: https://dev-cluster.example.com
            namespace: app-dev
            replicas: 1
            domain: dev.example.com
          - environment: staging
            cluster: https://staging-cluster.example.com
            namespace: app-staging
            replicas: 2
            domain: staging.example.com
          - environment: prod
            cluster: https://prod-cluster.example.com
            namespace: app-prod
            replicas: 5
            domain: example.com
  template:
    metadata:
      name: '{{environment}}-app'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/app-manifests
        targetRevision: HEAD
        path: overlays/{{environment}}
        helm:
          parameters:
            - name: replicaCount
              value: '{{replicas}}'
            - name: ingress.host
              value: '{{domain}}'
      destination:
        server: '{{cluster}}'
        namespace: '{{namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Best For:**
- Small number of well-defined environments
- Environment-specific configuration
- Explicit control over deployment targets
- Testing new environments before automation

---

#### Git Generator: Directory-Based Discovery

**Use Case:** Automatically discover applications from Git repository structure.

**Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: git-directory-discovery
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/org/kubernetes-manifests
        revision: HEAD
        directories:
          - path: apps/*
          - path: infrastructure/*
  template:
    metadata:
      name: '{{path.basename}}'
      labels:
        app-type: '{{path[0]}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/kubernetes-manifests
        targetRevision: HEAD
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

**Directory Structure:**
```
kubernetes-manifests/
├── apps/
│   ├── frontend/
│   │   └── kustomization.yaml
│   ├── backend/
│   │   └── kustomization.yaml
│   └── worker/
│       └── kustomization.yaml
└── infrastructure/
    ├── monitoring/
    │   └── kustomization.yaml
    └── logging/
        └── kustomization.yaml
```

**Best For:**
- Microservices architectures with many applications
- Self-service application onboarding
- Standardized application structure
- Reducing manual ApplicationSet management

---

#### Git Generator: File-Based Discovery

**Use Case:** Discover applications from JSON/YAML files with metadata.

**Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: git-file-discovery
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/org/app-registry
        revision: HEAD
        files:
          - path: "apps/**/app.json"
  template:
    metadata:
      name: '{{app.name}}-{{environment}}'
      labels:
        team: '{{app.team}}'
        tier: '{{app.tier}}'
    spec:
      project: '{{app.project}}'
      source:
        repoURL: '{{app.repoUrl}}'
        targetRevision: '{{app.branch}}'
        path: '{{app.path}}'
        helm:
          valueFiles:
            - values-{{environment}}.yaml
      destination:
        server: '{{cluster.url}}'
        namespace: '{{app.namespace}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Application Registry File (apps/frontend/app.json):**
```json
{
  "app": {
    "name": "frontend",
    "team": "platform",
    "tier": "production",
    "project": "core-services",
    "repoUrl": "https://github.com/org/frontend",
    "branch": "main",
    "path": "deploy/helm",
    "namespace": "frontend"
  },
  "environments": [
    {
      "name": "dev",
      "cluster": {
        "url": "https://dev-cluster.example.com"
      }
    },
    {
      "name": "prod",
      "cluster": {
        "url": "https://prod-cluster.example.com"
      }
    }
  ]
}
```

**Best For:**
- Decentralized application definitions
- Team-owned application metadata
- Complex application configurations
- Application registry patterns

---

#### Cluster Generator: Multi-Cluster Targeting

**Use Case:** Deploy applications to all clusters matching label selectors.

**Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cluster-addons
  namespace: argocd
spec:
  generators:
    - cluster:
        selector:
          matchLabels:
            addon: monitoring
        values:
          revision: v1.2.3
  template:
    metadata:
      name: '{{name}}-prometheus'
    spec:
      project: infrastructure
      source:
        repoURL: https://prometheus-community.github.io/helm-charts
        chart: kube-prometheus-stack
        targetRevision: '{{values.revision}}'
        helm:
          parameters:
            - name: prometheus.prometheusSpec.retention
              value: '{{metadata.labels.retention}}'
            - name: prometheus.prometheusSpec.storageClassName
              value: '{{metadata.labels.storageClass}}'
      destination:
        server: '{{server}}'
        namespace: monitoring
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

**Cluster Registration:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: prod-cluster-east
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
    addon: monitoring
    environment: production
    region: us-east-1
    retention: 30d
    storageClass: fast-ssd
type: Opaque
stringData:
  name: prod-east
  server: https://prod-east.example.com
  config: |
    {
      "tlsClientConfig": {
        "insecure": false,
        "caData": "...",
        "certData": "...",
        "keyData": "..."
      }
    }
```

**Best For:**
- Platform-wide infrastructure components
- Add-ons that should be on all clusters
- Fleet management patterns
- Consistent cluster configuration

---

#### Matrix Generator: Cartesian Product

**Use Case:** Deploy all combinations of environments and clusters.

**Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: matrix-environments-clusters
  namespace: argocd
spec:
  generators:
    - matrix:
        generators:
          # Generator 1: Environments from Git
          - git:
              repoURL: https://github.com/org/environments
              revision: HEAD
              files:
                - path: "environments/*.yaml"
          # Generator 2: Clusters with matching labels
          - cluster:
              selector:
                matchLabels:
                  environment: '{{environment}}'
  template:
    metadata:
      name: 'app-{{environment}}-{{name}}'
      labels:
        environment: '{{environment}}'
        cluster: '{{name}}'
        region: '{{metadata.labels.region}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/app
        targetRevision: HEAD
        path: deploy/overlays/{{environment}}
        helm:
          parameters:
            - name: cluster.name
              value: '{{name}}'
            - name: cluster.region
              value: '{{metadata.labels.region}}'
      destination:
        server: '{{server}}'
        namespace: app-{{environment}}
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Environment File (environments/prod.yaml):**
```yaml
environment: prod
replicaCount: 5
resources:
  limits:
    memory: 2Gi
    cpu: 1000m
  requests:
    memory: 1Gi
    cpu: 500m
```

**Best For:**
- Multi-region deployments
- Testing all environment-cluster combinations
- Complex deployment matrices
- High-availability patterns

---

#### Merge Generator: Layered Configuration

**Use Case:** Merge base configuration with environment-specific overrides.

**Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: merge-configuration
  namespace: argocd
spec:
  generators:
    - merge:
        mergeKeys:
          - name
        generators:
          # Base generator: All environments
          - list:
              elements:
                - name: dev
                  cluster: https://dev.example.com
                - name: staging
                  cluster: https://staging.example.com
                - name: prod
                  cluster: https://prod.example.com
          # Override generator: Production-specific config
          - list:
              elements:
                - name: prod
                  replicaCount: 5
                  resources:
                    limits:
                      memory: 4Gi
                      cpu: 2000m
          # Override generator: Dev-specific config
          - list:
              elements:
                - name: dev
                  replicaCount: 1
                  debug: "true"
  template:
    metadata:
      name: 'app-{{name}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/org/app
        targetRevision: HEAD
        path: deploy
        helm:
          parameters:
            - name: replicaCount
              value: '{{replicaCount | default "2"}}'
            - name: debug
              value: '{{debug | default "false"}}'
            - name: resources.limits.memory
              value: '{{resources.limits.memory | default "1Gi"}}'
      destination:
        server: '{{cluster}}'
        namespace: app
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Best For:**
- Base + override configuration patterns
- DRY (Don't Repeat Yourself) configurations
- Gradual environment-specific customization
- Reducing configuration duplication

---

### 2. Progressive Delivery Strategies

Progressive delivery enables gradual rollout of new versions with automated promotion or rollback based on metrics.

#### Canary Deployment

**Use Case:** Gradually shift traffic to new version while monitoring metrics.

**Traffic Split Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: app-canary
  namespace: production
spec:
  replicas: 10
  revisionHistoryLimit: 3
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
          image: myapp:v2.0.0
          ports:
            - containerPort: 8080
          resources:
            limits:
              memory: 512Mi
              cpu: 500m
  strategy:
    canary:
      # Traffic management
      canaryService: app-canary
      stableService: app-stable
      trafficRouting:
        istio:
          virtualService:
            name: app-vsvc
            routes:
              - primary
      # Progressive steps
      steps:
        # 1. Deploy 1 pod (10% capacity)
        - setWeight: 10
        - pause:
            duration: 5m
        # 2. Increase to 25%
        - setWeight: 25
        - pause:
            duration: 10m
        # 3. Analysis: Check error rate and latency
        - analysis:
            templates:
              - templateName: success-rate
              - templateName: latency-p95
            args:
              - name: service-name
                value: app-canary
        # 4. If analysis passes, 50%
        - setWeight: 50
        - pause:
            duration: 15m
        # 5. Final analysis before full rollout
        - analysis:
            templates:
              - templateName: success-rate
              - templateName: latency-p95
              - templateName: error-spike
        # 6. Full rollout
        - setWeight: 100
      # Automatic rollback on analysis failure
      autoPromotionEnabled: false
      abortScaleDownDelaySeconds: 30
```

**Analysis Templates:**
```yaml
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
    - name: service-name
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result >= 0.95
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(
              http_requests_total{
                service="{{args.service-name}}",
                status=~"2.."
              }[5m]
            ))
            /
            sum(rate(
              http_requests_total{
                service="{{args.service-name}}"
              }[5m]
            ))
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: latency-p95
spec:
  args:
    - name: service-name
  metrics:
    - name: p95-latency
      interval: 1m
      successCondition: result < 500
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            histogram_quantile(0.95,
              sum(rate(
                http_request_duration_seconds_bucket{
                  service="{{args.service-name}}"
                }[5m]
              )) by (le)
            ) * 1000
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: error-spike
spec:
  args:
    - name: service-name
  metrics:
    - name: error-rate-increase
      interval: 1m
      successCondition: result < 1.2
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            # Current error rate
            (
              sum(rate(
                http_requests_total{
                  service="{{args.service-name}}",
                  status=~"5.."
                }[5m]
              ))
            )
            /
            # Baseline error rate (24h ago)
            (
              sum(rate(
                http_requests_total{
                  service="{{args.service-name}}",
                  status=~"5.."
                }[5m] offset 24h
              ))
            )
```

**Istio VirtualService:**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app-vsvc
  namespace: production
spec:
  hosts:
    - app.example.com
  http:
    - name: primary
      match:
        - uri:
            prefix: /
      route:
        - destination:
            host: app-stable
            port:
              number: 80
          weight: 90
        - destination:
            host: app-canary
            port:
              number: 80
          weight: 10
```

**Best For:**
- Risk-averse production deployments
- Gradual confidence building
- Automated metric-based decisions
- Complex microservices
- High-traffic applications

---

#### Blue-Green Deployment

**Use Case:** Instant switch between stable and new version with quick rollback capability.

**Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: app-bluegreen
  namespace: production
spec:
  replicas: 5
  revisionHistoryLimit: 2
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
          image: myapp:v2.0.0
          ports:
            - containerPort: 8080
  strategy:
    blueGreen:
      # Active service receives production traffic
      activeService: app-active
      # Preview service for testing new version
      previewService: app-preview
      # Automatic promotion after analysis
      autoPromotionEnabled: false
      autoPromotionSeconds: 300
      # Scale down old version after promotion
      scaleDownDelaySeconds: 30
      scaleDownDelayRevisionLimit: 1
      # Pre-promotion analysis
      prePromotionAnalysis:
        templates:
          - templateName: smoke-tests
          - templateName: integration-tests
        args:
          - name: service-url
            value: http://app-preview.production.svc.cluster.local
      # Post-promotion analysis
      postPromotionAnalysis:
        templates:
          - templateName: success-rate
          - templateName: latency-p95
        args:
          - name: service-name
            value: app-active
```

**Pre-Promotion Analysis (Smoke Tests):**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: smoke-tests
spec:
  args:
    - name: service-url
  metrics:
    - name: health-check
      count: 3
      interval: 30s
      successCondition: result == "200"
      failureLimit: 1
      provider:
        web:
          url: "{{args.service-url}}/health"
          jsonPath: "{$.status}"
    - name: readiness-check
      count: 3
      interval: 30s
      successCondition: result == "ready"
      provider:
        web:
          url: "{{args.service-url}}/ready"
          jsonPath: "{$.state}"
    - name: version-check
      count: 1
      successCondition: result != ""
      provider:
        web:
          url: "{{args.service-url}}/version"
          jsonPath: "{$.version}"
```

**Services Configuration:**
```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: app-active
  namespace: production
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: app-preview
  namespace: production
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
---
# Ingress points to active service
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  namespace: production
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-active
                port:
                  number: 80
    # Preview environment for testing
    - host: preview.app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-preview
                port:
                  number: 80
```

**Manual Promotion:**
```bash
# Promote preview to active
kubectl argo rollouts promote app-bluegreen -n production

# Abort and rollback
kubectl argo rollouts abort app-bluegreen -n production
kubectl argo rollouts undo app-bluegreen -n production
```

**Best For:**
- Instant rollback requirements
- Pre-production testing in production environment
- Database migration scenarios
- Regulatory compliance needing approval gates
- Low-risk instant switches

---

#### A/B Testing

**Use Case:** Route specific user segments to different versions for experimentation.

**Pattern:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: app-ab-test
  namespace: production
spec:
  replicas: 10
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
          image: myapp:v2.0.0
          ports:
            - containerPort: 8080
  strategy:
    canary:
      canaryService: app-variant-b
      stableService: app-variant-a
      trafficRouting:
        istio:
          virtualService:
            name: app-ab-vsvc
            routes:
              - primary
      steps:
        # Deploy variant B at 50% capacity
        - setWeight: 50
        # Run A/B test for statistical significance
        - analysis:
            templates:
              - templateName: ab-test-analysis
            args:
              - name: variant-a-service
                value: app-variant-a
              - name: variant-b-service
                value: app-variant-b
              - name: metric
                value: conversion_rate
              - name: significance-level
                value: "0.05"
              - name: minimum-sample-size
                value: "1000"
```

**A/B Test Istio VirtualService:**
```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: app-ab-vsvc
  namespace: production
spec:
  hosts:
    - app.example.com
  http:
    - name: primary
      match:
        # Route based on user segment
        - headers:
            x-user-segment:
              exact: "premium"
      route:
        - destination:
            host: app-variant-b
            port:
              number: 80
    - name: beta-users
      match:
        - headers:
            x-user-id:
              regex: ".*[02468]$"  # Even user IDs
      route:
        - destination:
            host: app-variant-b
            port:
              number: 80
    - name: default
      route:
        - destination:
            host: app-variant-a
            port:
              number: 80
```

**A/B Test Analysis Template:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: ab-test-analysis
spec:
  args:
    - name: variant-a-service
    - name: variant-b-service
    - name: metric
    - name: significance-level
      value: "0.05"
    - name: minimum-sample-size
      value: "1000"
  metrics:
    # Collect variant A metrics
    - name: variant-a-metric
      interval: 5m
      count: 12  # Run for 1 hour
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(
              {{args.metric}}{
                service="{{args.variant-a-service}}"
              }[5m]
            )) / sum(rate(
              http_requests_total{
                service="{{args.variant-a-service}}"
              }[5m]
            ))
    # Collect variant B metrics
    - name: variant-b-metric
      interval: 5m
      count: 12
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(
              {{args.metric}}{
                service="{{args.variant-b-service}}"
              }[5m]
            )) / sum(rate(
              http_requests_total{
                service="{{args.variant-b-service}}"
              }[5m]
            ))
    # Statistical significance check
    - name: sample-size-check
      interval: 5m
      successCondition: result >= {{args.minimum-sample-size}}
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            min(
              sum(rate(http_requests_total{service="{{args.variant-a-service}}"}[1h])),
              sum(rate(http_requests_total{service="{{args.variant-b-service}}"}[1h]))
            )
    # Winner determination (requires custom metric provider)
    - name: ab-test-winner
      interval: 5m
      successCondition: result == "B" || result == "inconclusive"
      failureCondition: result == "A"
      provider:
        job:
          spec:
            template:
              spec:
                containers:
                  - name: ab-test-calculator
                    image: ab-test-calculator:latest
                    env:
                      - name: VARIANT_A_SERVICE
                        value: "{{args.variant-a-service}}"
                      - name: VARIANT_B_SERVICE
                        value: "{{args.variant-b-service}}"
                      - name: METRIC_NAME
                        value: "{{args.metric}}"
                      - name: SIGNIFICANCE_LEVEL
                        value: "{{args.significance-level}}"
                restartPolicy: Never
```

**Best For:**
- Feature experimentation
- UI/UX testing
- Conversion optimization
- User segment targeting
- Data-driven product decisions

---

### 3. Harness GitX Configuration

Harness GitX enables bi-directional synchronization between Git repositories and Harness platform.

#### Bi-Directional Sync Setup

**Git Connector Configuration:**
```yaml
connector:
  name: gitx-connector
  identifier: gitx_connector
  orgIdentifier: default
  projectIdentifier: gitops_project
  type: Github
  spec:
    url: https://github.com/org/harness-config
    validationRepo: harness-config
    authentication:
      type: Http
      spec:
        type: UsernameToken
        spec:
          username: gitops-bot
          tokenRef: github_token
    apiAccess:
      type: Token
      spec:
        tokenRef: github_token
    delegateSelectors:
      - gitops-delegate
    executeOnDelegate: true
    type: Repo
```

**GitX Settings:**
```yaml
gitExperience:
  enabled: true
  # Default branch for Git operations
  defaultBranch: main
  # Git connector to use
  connectorRef: gitx_connector
  # Repository root path
  repoName: harness-config
  # File path pattern for entities
  filePath: .harness/
  # Sync mode
  syncMode: bidirectional
  # Conflict resolution
  conflictResolution:
    strategy: manual
    onConflict: createPR
  # Auto-commit settings
  autoCommit:
    enabled: true
    authorName: Harness GitX
    authorEmail: gitx@harness.io
    commitMessage: "GitX: {{operation}} {{entityType}} {{entityName}}"
```

**Repository Structure:**
```
harness-config/
├── .harness/
│   ├── pipelines/
│   │   ├── deploy-prod.yaml
│   │   ├── deploy-staging.yaml
│   │   └── rollback.yaml
│   ├── services/
│   │   ├── frontend.yaml
│   │   ├── backend.yaml
│   │   └── worker.yaml
│   ├── environments/
│   │   ├── dev.yaml
│   │   ├── staging.yaml
│   │   └── prod.yaml
│   ├── infrastructure/
│   │   ├── k8s-dev.yaml
│   │   ├── k8s-staging.yaml
│   │   └── k8s-prod.yaml
│   └── templates/
│       ├── deployment-template.yaml
│       └── rollback-template.yaml
├── .gitignore
└── README.md
```

---

#### Webhook Triggers

**GitHub Webhook Configuration:**
```yaml
trigger:
  name: GitX Pipeline Trigger
  identifier: gitx_pipeline_trigger
  enabled: true
  orgIdentifier: default
  projectIdentifier: gitops_project
  pipelineIdentifier: deploy_pipeline
  source:
    type: Webhook
    spec:
      type: Github
      spec:
        type: Push
        connectorRef: gitx_connector
        autoAbortPreviousExecutions: false
        payloadConditions:
          - key: <+trigger.payload.ref>
            operator: Equals
            value: refs/heads/main
          - key: <+trigger.payload.commits[0].modified>
            operator: Contains
            value: .harness/
        headerConditions: []
        repoName: harness-config
        actions: []
  inputYaml: |
    pipeline:
      identifier: deploy_pipeline
      variables:
        - name: git_commit
          type: String
          value: <+trigger.commitSha>
        - name: git_branch
          type: String
          value: <+trigger.branch>
        - name: changed_files
          type: String
          value: <+trigger.payload.commits[0].modified>
```

**Webhook Handler Script:**
```python
#!/usr/bin/env python3
"""
Harness GitX Webhook Handler
Processes GitHub webhooks and triggers appropriate Harness pipelines
"""

import os
import json
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv('GITHUB_WEBHOOK_SECRET')
HARNESS_API_KEY = os.getenv('HARNESS_API_KEY')
HARNESS_ACCOUNT = os.getenv('HARNESS_ACCOUNT_ID')

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    # Verify webhook signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 403

    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == 'push':
        return handle_push(payload)
    elif event_type == 'pull_request':
        return handle_pull_request(payload)

    return jsonify({'message': 'Event type not handled'}), 200

def verify_signature(payload, signature):
    if not signature:
        return False
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

def handle_push(payload):
    """Handle push events to main branch"""
    ref = payload.get('ref')
    commits = payload.get('commits', [])

    if ref != 'refs/heads/main':
        return jsonify({'message': 'Not main branch'}), 200

    # Check if .harness/ directory was modified
    harness_modified = any(
        file.startswith('.harness/')
        for commit in commits
        for file in commit.get('modified', []) + commit.get('added', [])
    )

    if harness_modified:
        # Trigger Harness sync
        trigger_harness_sync(payload)

    return jsonify({'message': 'Processed'}), 200

def trigger_harness_sync(payload):
    """Trigger Harness GitX sync"""
    import requests

    url = f"https://app.harness.io/gateway/ng/api/git-sync/trigger"
    headers = {
        'x-api-key': HARNESS_API_KEY,
        'Content-Type': 'application/json'
    }

    data = {
        'accountIdentifier': HARNESS_ACCOUNT,
        'orgIdentifier': 'default',
        'projectIdentifier': 'gitops_project',
        'branch': 'main',
        'commitId': payload['after']
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

---

#### Conflict Resolution

**Manual Resolution Workflow:**
```yaml
# When conflicts occur, GitX creates a PR
conflictResolution:
  strategy: manual
  pr:
    # PR title template
    title: "[GitX Conflict] {{entityType}}: {{entityName}}"
    # PR description
    body: |
      ## GitX Conflict Detected

      **Entity Type:** {{entityType}}
      **Entity Name:** {{entityName}}
      **Operation:** {{operation}}

      ### Conflict Details

      The following changes conflict with existing Git state:

      {{conflictDetails}}

      ### Resolution Options

      1. **Accept Harness Changes:** Merge this PR to use Harness UI changes
      2. **Accept Git Changes:** Close this PR to keep Git repository state
      3. **Manual Merge:** Edit files in this PR to combine both changes

      ### Files Changed

      {{changedFiles}}
    # Auto-assign reviewers
    reviewers:
      - gitops-team
    # Labels
    labels:
      - gitx-conflict
      - auto-generated
```

**Automated Resolution for Non-Conflicting Changes:**
```yaml
conflictResolution:
  strategy: automatic
  rules:
    # Auto-merge safe changes
    - type: autoMerge
      conditions:
        - entityType: Pipeline
          operation: Update
          fields:
            - description
            - tags
        - entityType: Service
          operation: Update
          fields:
            - description
            - tags
    # Auto-reject unsafe changes
    - type: autoReject
      conditions:
        - entityType: Secret
          operation: Delete
        - entityType: Connector
          operation: Delete
    # Create PR for manual review
    - type: createPR
      conditions:
        - entityType: Pipeline
          operation: Update
          fields:
            - stages
            - variables
```

---

### 4. Sync Policies

#### Auto-Sync vs Manual Sync

**Auto-Sync Configuration:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: auto-sync-app
  namespace: argocd
spec:
  # ... source and destination ...
  syncPolicy:
    automated:
      # Enable automatic sync
      prune: true       # Delete resources not in Git
      selfHeal: true    # Revert manual changes
      allowEmpty: false # Prevent syncing empty directories
    syncOptions:
      # Create namespace if missing
      - CreateNamespace=true
      # Validate resources before applying
      - Validate=true
      # Use server-side apply
      - ServerSideApply=true
      # Replace resources instead of applying
      - Replace=false
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

**Manual Sync with Approval:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: manual-sync-app
  namespace: argocd
  annotations:
    # Require approval before sync
    notifications.argoproj.io/subscribe.on-sync-running.slack: gitops-channel
    notifications.argoproj.io/subscribe.on-sync-succeeded.slack: gitops-channel
    notifications.argoproj.io/subscribe.on-sync-failed.slack: gitops-channel
spec:
  # ... source and destination ...
  syncPolicy:
    # No automated sync - require manual approval
    syncOptions:
      - CreateNamespace=true
      - Validate=true
```

**Sync Approval Workflow:**
```bash
# Request sync
argocd app sync manual-sync-app --dry-run

# Review changes
argocd app diff manual-sync-app

# Approve and sync
argocd app sync manual-sync-app --prune --force
```

---

#### Self-Heal Configuration

**Self-Heal with Grace Period:**
```yaml
syncPolicy:
  automated:
    selfHeal: true
  syncOptions:
    # Allow manual changes for debugging
    - SelfHealGracePeriod=300  # 5 minutes
```

**Selective Self-Heal:**
```yaml
# Exclude specific resources from self-heal
metadata:
  annotations:
    argocd.argoproj.io/sync-options: SelfHeal=false
---
# Exclude by resource type in Application
spec:
  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas  # Allow manual scaling
    - group: ""
      kind: Service
      jsonPointers:
        - /spec/ports     # Allow manual port changes
```

---

#### Prune Policies

**Safe Pruning:**
```yaml
syncPolicy:
  automated:
    prune: true
  # Prune propagation policy
  syncOptions:
    - PrunePropagationPolicy=foreground  # Wait for resources to be deleted
    - PruneLast=true                     # Prune after applying new resources
```

**Prune Protection:**
```yaml
# Protect specific resources from pruning
metadata:
  annotations:
    argocd.argoproj.io/sync-options: Prune=false
---
# Protect by label
spec:
  syncPolicy:
    automated:
      prune: true
  # Ignore specific resources
  ignoreDifferences:
    - group: ""
      kind: PersistentVolumeClaim
      jsonPointers:
        - /spec
```

---

#### Sync Waves and Hooks

**Sync Waves for Ordered Deployment:**
```yaml
# Wave 0: Namespaces and CRDs
apiVersion: v1
kind: Namespace
metadata:
  name: app
  annotations:
    argocd.argoproj.io/sync-wave: "0"
---
# Wave 1: ConfigMaps and Secrets
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  annotations:
    argocd.argoproj.io/sync-wave: "1"
---
# Wave 2: Deployments and Services
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  annotations:
    argocd.argoproj.io/sync-wave: "2"
---
# Wave 3: Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    argocd.argoproj.io/sync-wave: "3"
```

**Sync Hooks:**
```yaml
# PreSync: Run database migration
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: migrate-tool:latest
          command: ["migrate", "up"]
      restartPolicy: Never
---
# PostSync: Run smoke tests
apiVersion: batch/v1
kind: Job
metadata:
  name: smoke-tests
  annotations:
    argocd.argoproj.io/hook: PostSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  template:
    spec:
      containers:
        - name: test
          image: test-runner:latest
          command: ["run-tests", "--smoke"]
      restartPolicy: Never
---
# SyncFail: Send notification
apiVersion: batch/v1
kind: Job
metadata:
  name: sync-failure-notification
  annotations:
    argocd.argoproj.io/hook: SyncFail
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
spec:
  template:
    spec:
      containers:
        - name: notify
          image: notification-service:latest
          env:
            - name: MESSAGE
              value: "Application sync failed: {{.metadata.name}}"
      restartPolicy: Never
```

---

### 5. Health Assessment

#### Custom Health Checks

**Custom Resource Health:**
```lua
-- Custom health check for Rollout
health_status = {}

if obj.status ~= nil then
    if obj.status.conditions ~= nil then
        for i, condition in ipairs(obj.status.conditions) do
            if condition.type == "Progressing" and condition.reason == "ProgressDeadlineExceeded" then
                health_status.status = "Degraded"
                health_status.message = "Rollout exceeded progress deadline"
                return health_status
            end
            if condition.type == "Progressing" and condition.status == "True" then
                health_status.status = "Progressing"
                health_status.message = "Rollout is progressing"
            end
            if condition.type == "Available" and condition.status == "True" then
                health_status.status = "Healthy"
                health_status.message = "Rollout is healthy"
                return health_status
            end
        end
    end

    if obj.status.replicas ~= nil and obj.status.updatedReplicas ~= nil then
        if obj.status.replicas ~= obj.status.updatedReplicas then
            health_status.status = "Progressing"
            health_status.message = "Waiting for rollout to finish"
            return health_status
        end
    end
end

health_status.status = "Unknown"
health_status.message = "Unable to determine rollout health"
return health_status
```

**ConfigMap for Custom Health Checks:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.health.argoproj.io_Rollout: |
    health_status = {}

    if obj.status ~= nil then
        if obj.status.conditions ~= nil then
            for i, condition in ipairs(obj.status.conditions) do
                if condition.type == "Progressing" and condition.reason == "ProgressDeadlineExceeded" then
                    health_status.status = "Degraded"
                    health_status.message = "Rollout exceeded progress deadline"
                    return health_status
                end
            end
        end
    end

    health_status.status = "Healthy"
    return health_status
```

---

#### Degraded State Handling

**Health Check Timeout:**
```yaml
spec:
  syncPolicy:
    automated:
      selfHeal: true
    # Health check configuration
    healthCheckTimeout: 300  # 5 minutes
    healthCheckMaxRetries: 5
```

**Degraded State Notifications:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  trigger.on-health-degraded: |
    - when: app.status.health.status == 'Degraded'
      send: [app-degraded]

  template.app-degraded: |
    message: |
      Application {{.app.metadata.name}} is degraded.
      Health status: {{.app.status.health.status}}
      Message: {{.app.status.health.message}}

      View in ArgoCD: {{.context.argocdUrl}}/applications/{{.app.metadata.name}}

    slack:
      attachments: |
        [{
          "title": "Application Degraded",
          "title_link": "{{.context.argocdUrl}}/applications/{{.app.metadata.name}}",
          "color": "warning",
          "fields": [
            {
              "title": "Application",
              "value": "{{.app.metadata.name}}",
              "short": true
            },
            {
              "title": "Health Status",
              "value": "{{.app.status.health.status}}",
              "short": true
            },
            {
              "title": "Message",
              "value": "{{.app.status.health.message}}",
              "short": false
            }
          ]
        }]
```

---

#### Rollback Triggers

**Automatic Rollback on Health Degradation:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: auto-rollback-app
spec:
  # ... replicas, selector, template ...
  strategy:
    canary:
      steps:
        - setWeight: 20
        - pause:
            duration: 5m
        - analysis:
            templates:
              - templateName: health-check
        # If health check fails, automatic rollback
      # Rollback configuration
      abortScaleDownDelaySeconds: 30
      maxUnavailable: 1
  # Failure threshold
  revisionHistoryLimit: 5
  progressDeadlineSeconds: 600
  progressDeadlineAbort: true
```

**Manual Rollback Command:**
```bash
# Rollback to previous revision
kubectl argo rollouts undo app-name -n namespace

# Rollback to specific revision
kubectl argo rollouts undo app-name -n namespace --to-revision=3

# Check rollout history
kubectl argo rollouts history app-name -n namespace
```

---

### 6. Multi-Cluster Patterns

#### Hub and Spoke

**Hub Cluster Architecture:**
```yaml
# Hub cluster runs ArgoCD and manages spoke clusters
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: hub-spoke-deployment
  namespace: argocd
spec:
  generators:
    - cluster:
        selector:
          matchLabels:
            cluster-type: spoke
  template:
    metadata:
      name: '{{name}}-app'
      labels:
        cluster: '{{name}}'
        region: '{{metadata.labels.region}}'
    spec:
      project: multi-cluster
      source:
        repoURL: https://github.com/org/app
        targetRevision: HEAD
        path: deploy
        helm:
          parameters:
            - name: cluster.name
              value: '{{name}}'
            - name: cluster.region
              value: '{{metadata.labels.region}}'
            - name: cluster.environment
              value: '{{metadata.labels.environment}}'
      destination:
        server: '{{server}}'
        namespace: applications
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

**Spoke Cluster Registration:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: spoke-cluster-east
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: cluster
    cluster-type: spoke
    region: us-east-1
    environment: production
type: Opaque
stringData:
  name: prod-east
  server: https://spoke-east.example.com
  config: |
    {
      "tlsClientConfig": {
        "insecure": false,
        "caData": "...",
        "certData": "...",
        "keyData": "..."
      }
    }
```

---

#### Fleet Management

**Fleet-Wide Configuration:**
```yaml
# Deploy platform services to all fleet clusters
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: fleet-platform-services
  namespace: argocd
spec:
  generators:
    - cluster:
        selector:
          matchExpressions:
            - key: fleet
              operator: In
              values: [production, staging]
  template:
    metadata:
      name: '{{name}}-platform'
    spec:
      project: platform
      source:
        repoURL: https://github.com/org/platform
        targetRevision: HEAD
        path: 'services/{{metadata.labels.fleet}}'
      destination:
        server: '{{server}}'
        namespace: platform
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

---

#### Cluster Selectors

**Complex Cluster Selection:**
```yaml
spec:
  generators:
    - cluster:
        selector:
          matchExpressions:
            # Production clusters in US regions
            - key: environment
              operator: In
              values: [production]
            - key: region
              operator: In
              values: [us-east-1, us-west-2]
            # With monitoring enabled
            - key: addon
              operator: In
              values: [monitoring]
            # Not in maintenance mode
            - key: maintenance
              operator: NotIn
              values: ["true"]
```

---

#### Network Policies for Multi-Cluster

**Cross-Cluster Network Policy:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: multi-cluster-policy
  namespace: applications
spec:
  podSelector:
    matchLabels:
      app: myapp
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow from hub cluster
    - from:
        - namespaceSelector:
            matchLabels:
              cluster: hub
        - podSelector:
            matchLabels:
              component: controller
  egress:
    # Allow to spoke clusters
    - to:
        - namespaceSelector:
            matchLabels:
              cluster-type: spoke
      ports:
        - protocol: TCP
          port: 443
```

---

## GitOps Best Practices

### 1. Repository Structure

**Monorepo Pattern:**
```
gitops-repo/
├── apps/
│   ├── frontend/
│   ├── backend/
│   └── worker/
├── infrastructure/
│   ├── monitoring/
│   ├── logging/
│   └── ingress/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── clusters/
    ├── dev-cluster/
    ├── staging-cluster/
    └── prod-cluster/
```

**Multi-Repo Pattern:**
```
org/
├── app-manifests/           # Application configurations
├── infrastructure-base/      # Base infrastructure
├── platform-addons/         # Platform services
└── environment-configs/     # Environment-specific overrides
```

---

### 2. Secret Management

**Sealed Secrets Pattern:**
```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  encryptedData:
    database-password: AgBh3...encrypted...
    api-key: AgCx9...encrypted...
```

**External Secrets Operator:**
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: azure-keyvault
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
    - secretKey: database-password
      remoteRef:
        key: app-database-password
    - secretKey: api-key
      remoteRef:
        key: app-api-key
```

---

### 3. Progressive Rollout Strategy

**Production Rollout Sequence:**
```
1. Deploy to Canary (10% traffic)
   ├─ Run smoke tests
   ├─ Monitor metrics (5 min)
   └─ Automated promotion if healthy

2. Increase to 25% traffic
   ├─ Run integration tests
   ├─ Monitor metrics (10 min)
   └─ Automated promotion if healthy

3. Increase to 50% traffic
   ├─ Run full test suite
   ├─ Monitor metrics (15 min)
   └─ Manual approval required

4. Full rollout (100% traffic)
   ├─ Final health check
   ├─ Monitor metrics (30 min)
   └─ Scale down old version
```

---

### 4. Monitoring and Observability

**ArgoCD Metrics:**
```yaml
# ServiceMonitor for ArgoCD metrics
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: argocd-metrics
  namespace: argocd
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: argocd-metrics
  endpoints:
    - port: metrics
      interval: 30s
```

**Key Metrics to Monitor:**
- Sync success rate
- Sync duration
- Application health status
- Rollout progress
- Analysis success rate
- Webhook delivery rate
- Git fetch errors

---

### 5. Disaster Recovery

**Backup Strategy:**
```bash
# Backup ArgoCD applications
kubectl get applications -n argocd -o yaml > argocd-apps-backup.yaml

# Backup ApplicationSets
kubectl get applicationsets -n argocd -o yaml > argocd-appsets-backup.yaml

# Backup ArgoCD configuration
kubectl get configmaps -n argocd -o yaml > argocd-config-backup.yaml
```

**Recovery Procedure:**
```bash
# Restore ArgoCD applications
kubectl apply -f argocd-apps-backup.yaml

# Trigger sync
argocd app sync --all

# Verify health
argocd app list
```

---

## Related Skills

- **template-validation** - Validate GitOps manifests before deployment
- **kubernetes-management** - Manage Kubernetes resources
- **harness-pipeline-management** - Integrate with Harness pipelines
- **monitoring-setup** - Configure observability for GitOps
- **security-scanning** - Scan manifests for security issues

---

## Example Usage Scenarios

### Scenario 1: Multi-Environment Microservices Deployment

```bash
# User: "Set up GitOps for 5 microservices across dev, staging, and prod"

# Claude creates:
# 1. ApplicationSet with List Generator for environments
# 2. Git directory structure for each microservice
# 3. Sync policies with auto-sync for dev, manual for prod
# 4. Health checks and notifications
```

### Scenario 2: Progressive Canary Rollout

```bash
# User: "Deploy new version with canary to production"

# Claude creates:
# 1. Rollout resource with canary strategy
# 2. AnalysisTemplates for error rate and latency
# 3. Istio VirtualService for traffic splitting
# 4. Monitoring dashboards
# 5. Rollback procedures
```

### Scenario 3: Multi-Cluster Fleet Management

```bash
# User: "Deploy monitoring stack to all production clusters in US regions"

# Claude creates:
# 1. ApplicationSet with Cluster Generator
# 2. Cluster selectors for region and environment
# 3. Sync waves for ordered deployment
# 4. Network policies for cross-cluster communication
# 5. Fleet-wide configuration management
```

---

## Success Criteria

A GitOps implementation is successful when:

- ✅ All deployments are driven by Git commits
- ✅ Automated sync policies work correctly
- ✅ Progressive delivery strategies function as expected
- ✅ Health checks accurately detect issues
- ✅ Rollback mechanisms work reliably
- ✅ Multi-cluster deployments are consistent
- ✅ Monitoring and alerting are in place
- ✅ Documentation is comprehensive
- ✅ Team can self-service deployments

---

## Notes

- Always test ApplicationSet generators in non-production first
- Use sync waves to control deployment order
- Implement proper secret management (never commit secrets to Git)
- Monitor sync success rates and deployment health
- Document rollback procedures for each application
- Use preview environments to test changes before production
- Implement RBAC to control who can approve production deployments
- Keep ApplicationSet templates DRY using merge generators
- Use analysis templates to automate promotion decisions
- Establish clear incident response procedures for failed deployments

---

**Version:** 1.0.0
**Last Updated:** 2026-01-19
**Maintainer:** Infrastructure Template Generator Plugin
