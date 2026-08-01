---
name: argocd
description: '| ID | cicd-argocd |'
---

# 🔄 Skill: ArgoCD GitOps Deployment

## 📋 Metadata

| Atributo | Valor |
|----------|-------|
| **ID** | `cicd-argocd` |
| **Nivel** | 🔴 Avanzado |
| **Versión** | 1.0.0 |
| **Keywords** | `argocd`, `gitops`, `kubernetes`, `cd`, `continuous-deployment` |
| **Referencia** | [ArgoCD Docs](https://argo-cd.readthedocs.io/) |

## 🔑 Keywords para Invocación

- `argocd`
- `gitops`
- `continuous-deployment`
- `k8s-deployment`
- `@skill:argocd`

### Ejemplos de Prompts

```
Configura ArgoCD para deployment de backend Flutter
```

```
Implementa GitOps con ArgoCD para monorepo
```

```
@skill:argocd - Setup continuous deployment

 Kubernetes
```

## 📖 Descripción

ArgoCD implementa GitOps para Kubernetes, sincronizando automáticamente el estado del cluster con repositorios Git. Ideal para deployments declarativos de backends Flutter y microservicios en un monorepo.

### ✅ Cuándo Usar Este Skill

- Deployments a Kubernetes
- GitOps workflow
- Múltiples ambientes (dev/staging/prod)
- Rollbacks automáticos
- Audit trail completo
- Self-healing applications

### ❌ Cuándo NO Usar Este Skill

- No usas Kubernetes
- Deployments muy simples
- Preferencia por CI/CD tradicional

## 🏗️ Estructura del Proyecto

```
my-app-monorepo/
├── k8s/
│   ├── argocd/
│   │   ├── applications/
│   │   │   ├── backend-dev.yaml
│   │   │   ├── backend-staging.yaml
│   │   │   └── backend-prod.yaml
│   │   ├── app-of-apps.yaml
│   │   └── projects.yaml
│   │
│   ├── base/
│   │   ├── backend/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   ├── ingress.yaml
│   │   │   └── kustomization.yaml
│   │   └── frontend/
│   │
│   └── overlays/
│       ├── dev/
│       │   ├── backend/
│       │   │   ├── kustomization.yaml
│       │   │   └── patches/
│       │   └── configmap.yaml
│       ├── staging/
│       └── production/
│
└── backend/
    └── Dockerfile
```

## 💻 Implementación

### 1. ArgoCD Installation

```bash
# Create argocd namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Expose ArgoCD Server
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Login with CLI
argocd login <ARGOCD_SERVER>

# Change password
argocd account update-password
```

### 2. Project Configuration

```yaml
# k8s/argocd/projects.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: myapp
  namespace: argocd
spec:
  description: My Flutter App Backend Project

  sourceRepos:
    - 'https://github.com/myorg/myapp-monorepo.git'

  destinations:
    - namespace: 'myapp-*'
      server: https://kubernetes.default.svc
    - namespace: production
      server: https://kubernetes.default.svc

  clusterResourceWhitelist:
    - group: ''
      kind: Namespace

  namespaceResourceWhitelist:
    - group: 'apps'
      kind: Deployment
    - group: 'apps'
      kind: StatefulSet
    - group: ''
      kind: Service
    - group: ''
      kind: ConfigMap
    - group: ''
      kind: Secret
    - group: 'networking.k8s.io'
      kind: Ingress

  roles:
    - name: developer
      description: Developers can sync apps
      policies:
        - p, proj:myapp:developer, applications, sync, myapp/*, allow
        - p, proj:myapp:developer, applications, get, myapp/*, allow

    - name: admin
      description: Admin access
      policies:
        - p, proj:myapp:admin, applications, *, myapp/*, allow
```

### 3. Application Configuration (Backend)

```yaml
# k8s/argocd/applications/backend-prod.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: backend-prod
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: myapp

  source:
    repoURL: https://github.com/myorg/myapp-monorepo.git
    targetRevision: main
    path: k8s/overlays/production/backend

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false

    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true

    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  revisionHistoryLimit: 10

  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas
```

### 4. App of Apps Pattern

```yaml
# k8s/argocd/app-of-apps.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp-apps
  namespace: argocd
spec:
  project: myapp

  source:
    repoURL: https://github.com/myorg/myapp-monorepo.git
    targetRevision: main
    path: k8s/argocd/applications

  destination:
    server: https://kubernetes.default.svc
    namespace: argocd

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 5. Kustomize Base

```yaml
# k8s/base/backend/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  labels:
    app: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: myorg/backend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: production
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: backend-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5

---
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: backend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: ClusterIP

---
# k8s/base/backend/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - ingress.yaml

commonLabels:
  app: backend
  managed-by: argocd
```

### 6. Kustomize Overlays (Production)

```yaml
# k8s/overlays/production/backend/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production

bases:
  - ../../../base/backend

commonLabels:
  environment: production

replicas:
  - name: backend
    count: 5

images:
  - name: myorg/backend
    newTag: v1.2.3

configMapGenerator:
  - name: backend-config
    literals:
      - LOG_LEVEL=info
      - API_TIMEOUT=30000

secretGenerator:
  - name: backend-secrets
    envs:
      - secrets.env

patches:
  - path: patches/resources.yaml
  - path: patches/hpa.yaml

---
# k8s/overlays/production/backend/patches/resources.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  template:
    spec:
      containers:
      - name: backend
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"

---
# k8s/overlays/production/backend/patches/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 7. ArgoCD CLI Commands

```bash
# List applications
argocd app list

# Get application details
argocd app get backend-prod

# Sync application
argocd app sync backend-prod

# Rollback to previous version
argocd app rollback backend-prod

# Set image
argocd app set backend-prod --kustomize-image myorg/backend:v1.2.4

# Delete application
argocd app delete backend-prod

# Create application from file
argocd app create -f k8s/argocd/applications/backend-prod.yaml

# Watch sync status
argocd app wait backend-prod --sync

# View logs
argocd app logs backend-prod

# Terminal access to pod
argocd app terminal backend-prod
```

### 8. Sync Waves and Hooks

```yaml
# Order of deployment with sync waves
apiVersion: v1
kind: ConfigMap
metadata:
  name: database-config
  annotations:
    argocd.argoproj.io/sync-wave: "0"  # Deploy first

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  annotations:
    argocd.argoproj.io/sync-wave: "1"  # Deploy after ConfigMap

---
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
  annotations:
    argocd.argoproj.io/hook: PreSync  # Run before sync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
```

### 9. Notifications

```yaml
# argocd-notifications-cm ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-notifications-cm
  namespace: argocd
data:
  service.slack: |
    token: $slack-token

  template.app-deployed: |
    message: |
      Application {{.app.metadata.name}} is now running new version.

  trigger.on-deployed: |
    - description: Application is synced and healthy
      send:
        - app-deployed
      when: app.status.operationState.phase in ['Succeeded'] and app.status.health.status == 'Healthy'
```

## 🎯 Mejores Prácticas

### 1. GitOps Workflow

```bash
# Desarrollador hace cambios
git checkout -b feature/new-endpoint
# ... hace cambios en código ...
git commit -m "Add new endpoint"
git push origin feature/new-endpoint

# PR es revisado y merged a main

# CI/CD build imagen y actualiza manifest
# (GitHub Actions actualiza image tag en k8s/overlays/*/kustomization.yaml)

# ArgoCD detecta cambios y sincroniza automáticamente
```

### 2. Environment Promotion

```yaml
# Promote from dev to staging
argocd app set backend-staging --kustomize-image myorg/backend:v1.2.3

# Promote from staging to production (manual approval)
argocd app set backend-prod --kustomize-image myorg/backend:v1.2.3
```

### 3. Disaster Recovery

```bash
# Backup ArgoCD
kubectl get applications -n argocd -o yaml > argocd-apps-backup.yaml

# Restore
kubectl apply -f argocd-apps-backup.yaml
```

## 📚 Recursos Adicionales

- [ArgoCD Documentation](https://argo-cd.readthedocs.io/)
- [Kustomize Documentation](https://kustomize.io/)
- [GitOps Principles](https://opengitops.dev/)

## 🔗 Skills Relacionados

- [Terraform](../terraform/SKILL.md) - Infrastructure provisioning
- [Kubernetes](../kubernetes/SKILL.md) - Container orchestration
- [GitHub Actions](../github-actions/SKILL.md) - CI/CD

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025
