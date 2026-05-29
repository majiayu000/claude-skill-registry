---
name: k8s-manifests
description: |
  Create, validate, and manage Kubernetes and OpenShift YAML manifests. Use this skill when:
  (1) Creating any K8s/OCP resources: Deployments, StatefulSets, DaemonSets, Jobs, CronJobs, Pods
  (2) Creating networking resources: Services, Ingress, NetworkPolicies, OCP Routes
  (3) Creating config/storage: ConfigMaps, Secrets, PVCs, PVs, StorageClasses
  (4) Creating RBAC: ServiceAccounts, Roles, RoleBindings, ClusterRoles, ClusterRoleBindings
  (5) Creating OCP-specific: DeploymentConfigs, BuildConfigs, ImageStreams, SCCs, Templates
  (6) Validating or reviewing existing manifests for best practices
  (7) Converting between K8s and OCP resource types
  (8) Generating Helm charts or Kustomize overlays
---

# Kubernetes / OpenShift Manifest Generator

## Current Versions & CLI Documentation (January 2026)

| Platform | Current Version | CLI | Documentation |
|----------|-----------------|-----|---------------|
| **Kubernetes** | 1.31.x | `kubectl` | https://kubernetes.io/docs/ |
| **OpenShift** | 4.17.x | `oc` | https://docs.openshift.com/ |
| **EKS** | 1.31 | `aws eks`, `eksctl` | https://docs.aws.amazon.com/eks/ |
| **AKS** | 1.31 | `az aks` | https://learn.microsoft.com/azure/aks/ |
| **GKE** | 1.31 | `gcloud container` | https://cloud.google.com/kubernetes-engine/docs |
| **ARO** | 4.17 | `az aro`, `oc` | https://learn.microsoft.com/azure/openshift/ |
| **ROSA** | 4.17 | `rosa`, `oc` | https://docs.openshift.com/rosa/ |

### CLI Installation Quick Reference

```bash
# kubectl (latest stable)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/$(uname -s | tr '[:upper:]' '[:lower:]')/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/
# OR
brew install kubectl

# oc (OpenShift CLI) - download from mirror.openshift.com or:
brew install openshift-cli

# eksctl (AWS EKS)
brew install eksctl
# OR
curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz"

# Azure CLI + AKS
brew install azure-cli
az extension add --name aks-preview

# Google Cloud SDK + GKE
brew install google-cloud-sdk
gcloud components install gke-gcloud-auth-plugin

# ROSA CLI
rosa download cli
```

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` as the primary command in all examples. When working with:
- **OpenShift/ARO clusters**: Replace all `kubectl` commands with `oc`
- **Standard Kubernetes clusters (AKS, EKS, GKE, etc.)**: Use `kubectl` as shown

The agent will automatically detect the cluster type and use the appropriate command.

Generate production-ready YAML manifests following security best practices and operational excellence.

## Core Principles

1. **Security by Default**: Always include security contexts, never run as root unless explicitly required
2. **Resource Management**: Always specify resource requests/limits
3. **High Availability**: Default to multiple replicas with anti-affinity for production
4. **Observability**: Include health probes, annotations for monitoring
5. **GitOps Ready**: Generate manifests suitable for version control and GitOps workflows

## Manifest Generation Workflow

1. Identify resource type and target platform (K8s vanilla, OCP, EKS, GKE, AKS)
2. Gather requirements (replicas, resources, networking, storage)
3. Apply security best practices
4. Generate YAML with appropriate labels and annotations
5. Validate against best practices checklist

## Resource Templates

### Deployment (Production-Ready)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/instance: ${INSTANCE}
    app.kubernetes.io/version: "${VERSION}"
    app.kubernetes.io/component: ${COMPONENT}
    app.kubernetes.io/part-of: ${PART_OF}
    app.kubernetes.io/managed-by: cluster-code
  annotations:
    description: "${DESCRIPTION}"
spec:
  replicas: ${REPLICAS:-3}
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
      app.kubernetes.io/instance: ${INSTANCE}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${APP_NAME}
        app.kubernetes.io/instance: ${INSTANCE}
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "${METRICS_PORT:-8080}"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: ${SERVICE_ACCOUNT:-default}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: ${APP_NAME}
                topologyKey: kubernetes.io/hostname
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: ScheduleAnyway
          labelSelector:
            matchLabels:
              app.kubernetes.io/name: ${APP_NAME}
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}:${TAG}
          imagePullPolicy: IfNotPresent
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          ports:
            - name: http
              containerPort: ${PORT:-8080}
              protocol: TCP
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          envFrom:
            - configMapRef:
                name: ${APP_NAME}-config
                optional: true
            - secretRef:
                name: ${APP_NAME}-secrets
                optional: true
          resources:
            requests:
              cpu: ${CPU_REQUEST:-100m}
              memory: ${MEMORY_REQUEST:-128Mi}
            limits:
              cpu: ${CPU_LIMIT:-500m}
              memory: ${MEMORY_LIMIT:-512Mi}
          livenessProbe:
            httpGet:
              path: /healthz
              port: http
            initialDelaySeconds: 15
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          startupProbe:
            httpGet:
              path: /healthz
              port: http
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 30
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /var/cache
      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}
      terminationGracePeriodSeconds: 30
```

### Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  type: ${SERVICE_TYPE:-ClusterIP}
  ports:
    - name: http
      port: ${SERVICE_PORT:-80}
      targetPort: http
      protocol: TCP
  selector:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/instance: ${INSTANCE}
```

### Ingress (K8s)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    cert-manager.io/cluster-issuer: ${CLUSTER_ISSUER:-letsencrypt-prod}
spec:
  ingressClassName: ${INGRESS_CLASS:-nginx}
  tls:
    - hosts:
        - ${HOST}
      secretName: ${APP_NAME}-tls
  rules:
    - host: ${HOST}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: ${APP_NAME}
                port:
                  name: http
```

### OpenShift Route

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
  annotations:
    haproxy.router.openshift.io/timeout: 60s
spec:
  host: ${HOST}
  to:
    kind: Service
    name: ${APP_NAME}
    weight: 100
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
  wildcardPolicy: None
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-config
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
data:
  # Application configuration
  APP_ENV: "${ENVIRONMENT:-production}"
  LOG_LEVEL: "${LOG_LEVEL:-info}"
  # Add application-specific config here
```

### Secret (Template - values should be base64 encoded or use stringData)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
type: Opaque
stringData:
  # Use stringData for plain text (auto-encoded)
  # Use data: for pre-encoded base64 values
  DATABASE_URL: "${DATABASE_URL}"
```

### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ${APP_NAME}-data
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  accessModes:
    - ${ACCESS_MODE:-ReadWriteOnce}
  storageClassName: ${STORAGE_CLASS:-standard}
  resources:
    requests:
      storage: ${STORAGE_SIZE:-10Gi}
```

### StatefulSet

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  serviceName: ${APP_NAME}-headless
  replicas: ${REPLICAS:-3}
  podManagementPolicy: Parallel
  updateStrategy:
    type: RollingUpdate
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ${APP_NAME}
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}:${TAG}
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          ports:
            - name: http
              containerPort: ${PORT:-8080}
          resources:
            requests:
              cpu: ${CPU_REQUEST:-100m}
              memory: ${MEMORY_REQUEST:-256Mi}
            limits:
              cpu: ${CPU_LIMIT:-1000m}
              memory: ${MEMORY_LIMIT:-1Gi}
          volumeMounts:
            - name: data
              mountPath: /data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes:
          - ReadWriteOnce
        storageClassName: ${STORAGE_CLASS:-standard}
        resources:
          requests:
            storage: ${STORAGE_SIZE:-10Gi}
```

### NetworkPolicy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ${APP_NAME}-netpol
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: ${INGRESS_NAMESPACE:-ingress-nginx}
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: ${ALLOWED_APP}
      ports:
        - protocol: TCP
          port: ${PORT:-8080}
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: ${EGRESS_TARGET}
      ports:
        - protocol: TCP
          port: ${EGRESS_PORT}
```

### HorizontalPodAutoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ${APP_NAME}
  minReplicas: ${MIN_REPLICAS:-2}
  maxReplicas: ${MAX_REPLICAS:-10}
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: ${CPU_TARGET:-70}
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: ${MEMORY_TARGET:-80}
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
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

### ServiceAccount with RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: ${APP_NAME}
subjects:
  - kind: ServiceAccount
    name: ${APP_NAME}
    namespace: ${NAMESPACE}
```

### CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ${JOB_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${JOB_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  schedule: "${SCHEDULE}"
  concurrencyPolicy: ${CONCURRENCY:-Forbid}
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  startingDeadlineSeconds: 300
  jobTemplate:
    spec:
      backoffLimit: 3
      activeDeadlineSeconds: ${TIMEOUT:-3600}
      template:
        spec:
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
            seccompProfile:
              type: RuntimeDefault
          restartPolicy: OnFailure
          containers:
            - name: ${JOB_NAME}
              image: ${IMAGE}:${TAG}
              securityContext:
                allowPrivilegeEscalation: false
                readOnlyRootFilesystem: true
                capabilities:
                  drop:
                    - ALL
              resources:
                requests:
                  cpu: ${CPU_REQUEST:-100m}
                  memory: ${MEMORY_REQUEST:-128Mi}
                limits:
                  cpu: ${CPU_LIMIT:-500m}
                  memory: ${MEMORY_LIMIT:-512Mi}
              command: ${COMMAND}
              args: ${ARGS}
```

### PodDisruptionBudget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  minAvailable: ${MIN_AVAILABLE:-1}
  # OR use maxUnavailable: ${MAX_UNAVAILABLE:-1}
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
```

## OpenShift-Specific Resources

### SecurityContextConstraints (Cluster-Admin)

```yaml
apiVersion: security.openshift.io/v1
kind: SecurityContextConstraints
metadata:
  name: ${SCC_NAME}
  labels:
    app.kubernetes.io/managed-by: cluster-code
allowHostDirVolumePlugin: false
allowHostIPC: false
allowHostNetwork: false
allowHostPID: false
allowHostPorts: false
allowPrivilegeEscalation: false
allowPrivilegedContainer: false
allowedCapabilities: null
defaultAddCapabilities: null
fsGroup:
  type: MustRunAs
  ranges:
    - min: 1000
      max: 65534
priority: null
readOnlyRootFilesystem: true
requiredDropCapabilities:
  - ALL
runAsUser:
  type: MustRunAsRange
  uidRangeMin: 1000
  uidRangeMax: 65534
seLinuxContext:
  type: MustRunAs
supplementalGroups:
  type: MustRunAs
  ranges:
    - min: 1000
      max: 65534
users: []
groups: []
volumes:
  - configMap
  - downwardAPI
  - emptyDir
  - persistentVolumeClaim
  - projected
  - secret
```

### BuildConfig (S2I)

```yaml
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  source:
    type: Git
    git:
      uri: ${GIT_URI}
      ref: ${GIT_REF:-main}
    contextDir: ${CONTEXT_DIR:-/}
  strategy:
    type: Source
    sourceStrategy:
      from:
        kind: ImageStreamTag
        namespace: openshift
        name: ${BUILDER_IMAGE:-python:3.11-ubi8}
      env:
        - name: APP_ENV
          value: ${ENVIRONMENT:-production}
  output:
    to:
      kind: ImageStreamTag
      name: ${APP_NAME}:latest
  triggers:
    - type: ConfigChange
    - type: ImageChange
    - type: GitHub
      github:
        secret: ${WEBHOOK_SECRET}
  resources:
    limits:
      cpu: "1"
      memory: 2Gi
    requests:
      cpu: 500m
      memory: 1Gi
```

### ImageStream

```yaml
apiVersion: image.openshift.io/v1
kind: ImageStream
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  labels:
    app.kubernetes.io/name: ${APP_NAME}
    app.kubernetes.io/managed-by: cluster-code
spec:
  lookupPolicy:
    local: true
  tags:
    - name: latest
      annotations:
        description: Latest build of ${APP_NAME}
```

## Best Practices Checklist

Before finalizing any manifest, verify:

### Security
- [ ] `runAsNonRoot: true` in securityContext
- [ ] `allowPrivilegeEscalation: false`
- [ ] `readOnlyRootFilesystem: true` (with emptyDir for temp/cache)
- [ ] `capabilities.drop: [ALL]`
- [ ] `seccompProfile.type: RuntimeDefault`
- [ ] ServiceAccount with minimal RBAC permissions
- [ ] NetworkPolicy restricting ingress/egress
- [ ] Secrets not hardcoded, using Secret resources or external secrets operator

### Reliability
- [ ] Resource requests AND limits defined
- [ ] Liveness, readiness, and startup probes configured
- [ ] PodDisruptionBudget for HA workloads
- [ ] Anti-affinity rules for multi-replica deployments
- [ ] TopologySpreadConstraints for zone distribution

### Operations
- [ ] Standard Kubernetes labels (app.kubernetes.io/*)
- [ ] Prometheus annotations for metrics scraping
- [ ] Appropriate terminationGracePeriodSeconds
- [ ] RevisionHistoryLimit set (default 5)
- [ ] RollingUpdate strategy with maxSurge/maxUnavailable

### Observability
- [ ] Logging to stdout/stderr
- [ ] Metrics endpoint exposed
- [ ] Health check endpoints (/healthz, /ready)
- [ ] Resource annotations for monitoring dashboards

## Common Patterns

### Sidecar Container Pattern
Add sidecars for logging, monitoring, or service mesh:
```yaml
containers:
  - name: app
    # main application
  - name: sidecar
    image: sidecar-image
    resources:
      requests:
        cpu: 10m
        memory: 32Mi
      limits:
        cpu: 50m
        memory: 64Mi
```

### Init Container Pattern
For initialization, migrations, or waiting on dependencies:
```yaml
initContainers:
  - name: wait-for-db
    image: busybox
    command: ['sh', '-c', 'until nc -z ${DB_HOST} 5432; do sleep 2; done']
  - name: migrations
    image: ${IMAGE}:${TAG}
    command: ['./migrate.sh']
```

### External Secrets Pattern
For HashiCorp Vault, AWS Secrets Manager, etc.:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: ${APP_NAME}-secrets
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: ${APP_NAME}-secrets
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: ${VAULT_PATH}
        property: database_url
```

## Platform-Specific Notes

### EKS (AWS) - v1.31

**CLI Commands:**
```bash
# Create cluster with eksctl
eksctl create cluster --name ${CLUSTER} --region ${REGION} \
  --version 1.31 --nodegroup-name standard \
  --node-type m6i.large --nodes 3 --nodes-min 1 --nodes-max 5 \
  --managed --spot

# Get kubeconfig
aws eks update-kubeconfig --name ${CLUSTER} --region ${REGION}

# Check add-ons
aws eks list-addons --cluster-name ${CLUSTER}

# Install EKS Pod Identity (replaces IRSA in 1.31+)
eksctl create podidentityassociation --cluster ${CLUSTER} \
  --namespace ${NS} --service-account-name ${SA} \
  --role-arn arn:aws:iam::${ACCOUNT}:role/${ROLE}
```

**Key Features (1.31):**
- EKS Pod Identity (simplified IAM for pods, replaces IRSA complexity)
- EKS Auto Mode (automatic node management)
- EBS CSI driver for gp3 volumes (default)
- AWS Load Balancer Controller v2.9+ for ALB/NLB
- Karpenter v1.0+ for autoscaling

**Manifest Annotations:**
```yaml
# ALB Ingress (AWS Load Balancer Controller)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS13-1-2-2021-06
    alb.ingress.kubernetes.io/certificate-arn: ${ACM_CERT_ARN}
    alb.ingress.kubernetes.io/healthcheck-path: /healthz
    alb.ingress.kubernetes.io/wafv2-acl-arn: ${WAF_ARN}  # Optional WAF

# NLB Service
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: nlb
    service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing
    service.beta.kubernetes.io/aws-load-balancer-nlb-target-type: ip
    service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
```

### GKE (Google Cloud) - v1.31

**CLI Commands:**
```bash
# Create Autopilot cluster (recommended)
gcloud container clusters create-auto ${CLUSTER} \
  --region ${REGION} \
  --release-channel regular

# Create Standard cluster
gcloud container clusters create ${CLUSTER} \
  --region ${REGION} \
  --num-nodes 3 \
  --machine-type e2-standard-4 \
  --enable-autoscaling --min-nodes 1 --max-nodes 10 \
  --workload-pool=${PROJECT}.svc.id.goog \
  --enable-dataplane-v2  # Cilium-based networking

# Get credentials
gcloud container clusters get-credentials ${CLUSTER} --region ${REGION}

# Check GKE version
gcloud container get-server-config --region ${REGION}
```

**Key Features (1.31):**
- Autopilot mode (fully managed nodes)
- GKE Dataplane V2 (Cilium-based eBPF networking)
- Workload Identity Federation (replaces node SA)
- Gateway API support (standard)
- Config Connector for GCP resource management

**Manifest Annotations:**
```yaml
# GCE Ingress with Google-managed cert
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: gce
    kubernetes.io/ingress.global-static-ip-name: ${STATIC_IP}
    networking.gke.io/managed-certificates: ${MANAGED_CERT}
    networking.gke.io/v1beta1.FrontendConfig: ${FRONTEND_CONFIG}

# NEG for container-native load balancing (recommended)
apiVersion: v1
kind: Service
metadata:
  annotations:
    cloud.google.com/neg: '{"ingress": true}'
    cloud.google.com/backend-config: '{"default": "${BACKEND_CONFIG}"}'
```

### AKS (Azure) - v1.31

**CLI Commands:**
```bash
# Create AKS cluster
az aks create --resource-group ${RG} --name ${CLUSTER} \
  --kubernetes-version 1.31 \
  --node-count 3 --node-vm-size Standard_D4s_v5 \
  --enable-managed-identity \
  --enable-workload-identity \
  --enable-oidc-issuer \
  --network-plugin azure \
  --network-plugin-mode overlay \
  --network-dataplane cilium \
  --enable-addons monitoring

# Get credentials
az aks get-credentials --resource-group ${RG} --name ${CLUSTER}

# Check cluster
az aks show --resource-group ${RG} --name ${CLUSTER}

# Enable addons
az aks enable-addons --addons azure-keyvault-secrets-provider \
  --resource-group ${RG} --name ${CLUSTER}
```

**Key Features (1.31):**
- Azure CNI Overlay with Cilium (eBPF networking)
- Workload Identity (Azure AD pod identity replacement)
- KEDA add-on (event-driven autoscaling)
- Azure Key Vault Secrets Provider (CSI driver)
- Automatic image cleaner and node autoprovision

**Manifest Annotations:**
```yaml
# Azure Application Gateway Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: azure/application-gateway
    appgw.ingress.kubernetes.io/ssl-redirect: "true"
    appgw.ingress.kubernetes.io/use-private-ip: "false"
    appgw.ingress.kubernetes.io/backend-path-prefix: "/"
    appgw.ingress.kubernetes.io/waf-policy-for-path: ${WAF_POLICY_ID}

# Azure Internal Load Balancer
apiVersion: v1
kind: Service
metadata:
  annotations:
    service.beta.kubernetes.io/azure-load-balancer-internal: "true"
    service.beta.kubernetes.io/azure-load-balancer-internal-subnet: ${SUBNET}
    service.beta.kubernetes.io/azure-pls-create: "true"  # Private Link
```

### OpenShift / ARO / ROSA - v4.17

**CLI Commands:**
```bash
# OpenShift CLI basics
oc login ${API_URL} --token=${TOKEN}
oc project ${NAMESPACE}
oc new-project ${PROJECT}

# ARO (Azure Red Hat OpenShift)
az aro create --resource-group ${RG} --name ${CLUSTER} \
  --vnet ${VNET} --master-subnet ${MASTER_SUBNET} \
  --worker-subnet ${WORKER_SUBNET} \
  --pull-secret @pull-secret.txt

az aro show --resource-group ${RG} --name ${CLUSTER} --query consoleProfile.url
az aro list-credentials --resource-group ${RG} --name ${CLUSTER}

# ROSA (Red Hat OpenShift on AWS)
rosa create cluster --cluster-name ${CLUSTER} \
  --region ${REGION} \
  --sts --mode auto \
  --hosted-cp  # Hosted control plane (HCP) for faster provisioning

rosa describe cluster --cluster ${CLUSTER}
rosa create admin --cluster ${CLUSTER}
```

**Key Features (4.17):**
- OVN-Kubernetes (default CNI with eBPF)
- ROSA with Hosted Control Planes (HCP)
- SecurityContextConstraints (SCC) with Pod Security Admission
- OpenShift GitOps (ArgoCD) and Pipelines (Tekton) operators
- Service Mesh 3.0 (Istio-based)
- OpenShift AI (machine learning platform)

**OpenShift-specific Resources:**
```yaml
# Route (instead of Ingress)
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: ${APP_NAME}
  annotations:
    haproxy.router.openshift.io/timeout: 60s
    haproxy.router.openshift.io/rate-limit-connections: "true"
    haproxy.router.openshift.io/rate-limit-connections.rate-http: "100"
spec:
  host: ${HOST}
  to:
    kind: Service
    name: ${APP_NAME}
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
    certificate: |
      ${CERT}
    key: |
      ${KEY}
```
