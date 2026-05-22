---
name: kubernetes-manifests
description: |
  Create, validate, and manage Kubernetes and OpenShift YAML manifests. Use this skill when:
  (1) Creating any K8s/OCP resources: Deployments, StatefulSets, DaemonSets, Jobs, CronJobs
  (2) Creating networking resources: Services, Ingress, NetworkPolicies, OCP Routes
  (3) Creating config/storage: ConfigMaps, Secrets, PVCs, PVs, StorageClasses
  (4) Creating RBAC: ServiceAccounts, Roles, RoleBindings, ClusterRoles
  (5) Creating OCP-specific: BuildConfigs, ImageStreams, SCCs, Templates
  (6) Validating or reviewing existing manifests for best practices
  (7) Converting between K8s and OCP resource types
  (8) Generating Helm charts or Kustomize overlays
metadata:
  author: cluster-skills
  version: "1.0.0"
---

# Kubernetes / OpenShift Manifest Generator

Generate production-ready YAML manifests following security best practices and operational excellence.

## Current Versions & CLI (January 2026)

| Platform | Current Version | CLI | Documentation |
|----------|-----------------|-----|---------------|
| **Kubernetes** | 1.31.x | `kubectl` | https://kubernetes.io/docs/ |
| **OpenShift** | 4.17.x | `oc` | https://docs.openshift.com/ |
| **EKS** | 1.31 | `eksctl` | https://docs.aws.amazon.com/eks/ |
| **AKS** | 1.31 | `az aks` | https://learn.microsoft.com/azure/aks/ |
| **GKE** | 1.31 | `gcloud container` | https://cloud.google.com/kubernetes-engine/docs |

## Command Usage Convention

**IMPORTANT**: This skill uses `kubectl` in examples. When working with:
- **OpenShift/ARO clusters**: Replace `kubectl` with `oc`
- **Standard Kubernetes (AKS, EKS, GKE)**: Use `kubectl` as shown

## Core Principles

1. **Security by Default**: Always include security contexts, never run as root
2. **Resource Management**: Always specify resource requests/limits
3. **High Availability**: Multiple replicas with anti-affinity for production
4. **Observability**: Include health probes, annotations for monitoring
5. **GitOps Ready**: Generate manifests suitable for version control

## Manifest Generation Workflow

1. Identify resource type and target platform
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
    app.kubernetes.io/managed-by: cluster-skills
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
      volumes:
        - name: tmp
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

### Ingress (Kubernetes)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
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
```

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ${APP_NAME}-config
  namespace: ${NAMESPACE}
data:
  APP_ENV: "${ENVIRONMENT:-production}"
  LOG_LEVEL: "${LOG_LEVEL:-info}"
```

### Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
type: Opaque
stringData:
  DATABASE_URL: "${DATABASE_URL}"
```

### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ${APP_NAME}-data
  namespace: ${NAMESPACE}
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
      ports:
        - protocol: TCP
          port: ${PORT:-8080}
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: UDP
          port: 53  # DNS
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
```

### ServiceAccount with RBAC

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
automountServiceAccountToken: false
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
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
```

### PodDisruptionBudget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ${APP_NAME}-pdb
  namespace: ${NAMESPACE}
spec:
  minAvailable: ${MIN_AVAILABLE:-1}
  # OR use maxUnavailable
  # maxUnavailable: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: ${APP_NAME}
```

## Best Practices Checklist

### Security
- [ ] `runAsNonRoot: true`
- [ ] `runAsUser` and `runAsGroup` set (non-zero)
- [ ] `allowPrivilegeEscalation: false`
- [ ] `readOnlyRootFilesystem: true`
- [ ] `capabilities.drop: ["ALL"]`
- [ ] `seccompProfile.type: RuntimeDefault`
- [ ] `automountServiceAccountToken: false` (unless needed)

### Reliability
- [ ] Resource requests and limits defined
- [ ] Liveness probe configured
- [ ] Readiness probe configured
- [ ] Startup probe for slow-starting apps
- [ ] PodDisruptionBudget defined
- [ ] Multiple replicas for production

### Observability
- [ ] Standard labels applied (`app.kubernetes.io/*`)
- [ ] Prometheus annotations for metrics
- [ ] Structured logging configured

### Networking
- [ ] NetworkPolicy defined (zero-trust)
- [ ] Service defined for pod exposure
- [ ] Ingress/Route for external access
