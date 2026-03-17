---
name: docker-k8s
description: Master containerization and orchestration with security-first approach. Expert in Docker multi-stage builds, Kubernetes zero-trust deployments, security hardening, GitOps workflows, and production-ready patterns for cloud-native applications. Includes 2025 best practices from CNCF and major cloud providers.
license: MIT
---

# Containerization & Kubernetes with Security Hardening

This skill provides comprehensive patterns for containerizing applications and deploying to Kubernetes in 2025, focusing on zero-trust security, multi-stage optimization, production hardening, and cloud-native best practices that work across different cloud providers.

## When to Use This Skill

Use this skill when you need to:
- Create secure multi-stage Docker builds
- Deploy applications to Kubernetes with security hardening
- Implement zero-trust security patterns
- Set up GitOps workflows with ArgoCD/Flux
- Optimize container images for production
- Configure cluster security with Pod Security Standards
- Implement secure networking with service meshes
- Set up monitoring and observability
- Deploy to multiple cloud providers (AWS, GCP, Azure, DO)

## Secure Multi-Stage Docker Builds

### 1. Security-First Multi-Stage Builds

```dockerfile
# Dockerfile with security hardening
# Build stage
FROM python:3.11-slim AS builder

# Set build-time security arguments
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBCONF_NONINTERACTIVE_SEEN=true
ARG BUILDPLATFORM
ARG TARGETPLATFORM

# Install build dependencies with security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        ca-certificates \
        curl \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    truncate -s 0 /var/log/apt/history.log

# Create non-root user for build
RUN groupadd -r builder && \
    useradd -r -g builder builder

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies in virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -U pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim AS production

# Security labels
LABEL maintainer="security-team@company.com" \
      version="1.0.0" \
      security.scan="enabled" \
      org.opencontainers.image.vendor="Company"

# Install runtime dependencies with security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        libpq5 \
        ca-certificates \
        curl \
        dumb-init \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    truncate -s 0 /var/log/apt/history.log

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user for runtime
RUN groupadd -r appuser && \
    useradd -r -g appuser -s /bin/sh appuser

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser alembic/ ./alembic/
COPY --chown=appuser:appuser alembic.ini .

# Set permissions
RUN chmod -R 755 /app && \
    chmod -x /app/alembic.ini

# Switch to non-root user
USER appuser

# Set PATH
ENV PATH="/opt/venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Security scan before running
RUN python -c "import urllib.request; urllib.request.urlopen('https://security-scan.example.com/scan')"

# Expose port
EXPOSE 8000

# Use dumb-init as PID 1
ENTRYPOINT ["dumb-init", "--"]

# Run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers=4", "--access-log=-"]
```

### 2. Docker Security Best Practices

```dockerfile
# Dockerfile.security
# Base security hardening
FROM python:3.11-slim AS base

# Kernel security settings
RUN sysctl -w net.ipv4.ip_forward=1 && \
    sysctl -w net.ipv6.conf.all.forwarding=1 && \
    sysctl -w net.ipv4.conf.all.send_redirects=0 && \
    sysctl -w net.ipv4.conf.default_accept_source_route=0 && \
    sysctl -w kernel.dmesg_restrict=1

# Remove setuid/setgid binaries
RUN find / -type f -perm /6000 -exec chmod a-s {} \; || true && \
    find / -type f -perm /4000 -exec chmod a+r {} \; || true

# Security scanning
RUN apt-get update && \
    apt-get install -y trivy && \
    trivy image --severity HIGH,CRITICAL python:3.11-slim

# Production application with security
FROM base AS production

# Add security labels
LABEL \
    security.stack.linux.docker.image-version="1" \
    security.stack.linux.docker.kernel-version="6.x" \
    security.stack.linux.docker.os-version="Debian 12" \
    security.stack.cis.docker.version="1.6.0"

# Implement runtime security
RUN apt-get update && \
    apt-get install -y \
        apparmor-profiles \
        fail2ban \
        rkhunter \
        chkrootkit \
    && \
    apt-get clean

# Configure fail2ban
COPY fail2ban.conf /etc/fail2ban/jail.local

# Configure AppArmor
COPY apparmor-profiles /etc/apparmor.d/

# Security runtime checks
RUN python -c "
import subprocess
import sys

# Check for vulnerable packages
result = subprocess.run(['apt', 'list', '--upgradable'],
                        capture_output=True, text=True)
if result.stdout.strip():
    print('WARNING: Packages need updates:', result.stdout.strip())
    sys.exit(1)
"
```

### 3. Zero-Trust Kubernetes Deployment

```yaml
# manifests/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    name: production
    security-tier: "high"
    environment: "production"
  annotations:
    pod-security.kubernetes.io/enforce: "restricted"
    pod-security.kubernetes.io/audit: "restricted"
    pod-security.kubernetes.io/warn: "restricted"

---
# manifests/rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: production-apps
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets", "daemonsets"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["networking.k8s.io"]
  resources: ["networkpolicies"]
  verbs: ["get", "list", "create", "update", "patch"]

---
apiVersion: rbac.authorization.kubernetes.io/v1
kind: ClusterRoleBinding
metadata:
  name: production-apps-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: production-apps
subjects:
- kind: ServiceAccount
  name: default
  namespace: production

---
# manifests/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress
  # Deny all ingress and egress by default

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Egress
  egress:
  - to: []
    ports:
    - protocol: UDP
      port: 53
    - protocol: TCP
      port: 53
  - to: []
    ports:
    - protocol: TCP
      port: 443
    - protocol: TCP
      port: 53

---
# manifests/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  namespace: production
  labels:
    app: secure-app
    tier: application
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
      tier: application
      version: v1
      security.stack.company.com/container-security-level: "high"
      security.stack.company.com/network-segment: "application"
    annotations:
      container.security.kubernetes.io/scc: "restricted"
      seccomp.security.kubernetes.io/profile: "runtime/default"
      kubernetes.io/psp: "restricted"
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
        readOnlyRootFilesystem: false
        capabilities:
          drop:
          - ALL
          add:
            - NET_BIND_SERVICE
      containers:
      - name: app
        image: your-registry/secure-app:v1.0.0
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
          protocol: TCP
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
          requests:
            cpu: "100m"
            memory: "128Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
          successThreshold: 1
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
          successThreshold: 1
        startupProbe:
          httpGet:
            path: /health
            port: 8000
          failureThreshold: 30
          periodSeconds: 10
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: false
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /cache
      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
      imagePullSecrets:
      - name: registry-secret
      serviceAccountName: restricted-sa
      automountServiceAccountToken: false

---
# manifests/service-account.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: restricted-sa
  namespace: production
  annotations:
    iam.gke.io/gcp-service-account: "production-sa@your-project.iam.gserviceaccount.com"
    eks.amazonaws.com/role-arn: "arn:aws:iam::123456789012:role/production-role"

---
# manifests/pod-security-policy.yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted-psp
  namespace: production
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    'downwardAPI'
    'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
```

### 4. Service Mesh with Istio

```yaml
# istio/istio-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio-config
  namespace: istio-system
data:
  meshConfig: |
    accessLogFile: /dev/stdout
    defaultConfig:
      concurrency: 3
      circuitBreakers:
        consecutive5xxErrors: 5
        timeout: 30s
        maxConnections: 1000
        maxRequestsPerConnection: 500
      connectionPoolSettings:
        tcp:
          maxConnections: 100
          connectTimeout: 10s
        http:
          http2MaxRequests: 100
          maxRequestsPerConnection: 10
          maxRetries: 3
      outlierDetection:
        consecutiveGatewayErrors: 5
        interval: 30s
        baseEjectionTime: 30s
        maxEjectionPercent: 100
      proxyStatsMatcher: "-x"
      telemetry:
        v2:
          prometheus:
            enabled: true
            customTags:
              app: "secure-app"
              version: "v1"

---
# istio/destination-rule.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: secure-app
  namespace: production
spec:
  host: secure-app
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
      clientCertificate:
        - /etc/istio/destination-client-certs
    connectionPool:
      tcp:
        maxConnections: 100
        connectTimeout: 30s
        keepAlive:
          time: 7200s
          requests: 10000
      http:
        http2MaxRequests: 1000
        maxRequestsPerConnection: 100
        maxRetries: 3
        idleTimeout: 120s
        h2UpgradePolicy: RFC
        keepAlive:
          time: 7200s
          requests: 100
    loadBalancer:
      simple: LEAST_CONN
    circuitBreaker:
      consecutiveErrors: 7
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 100
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 30s
      maxEjectionPercent: 10
    retryOn:
      - connect-failure
      - refused-stream
      - canceled
      - timeout
      - retriable-status
    retryOff:
      - overloaded
      - deadline-exceeded
      - unknown
    timeout: 300s
    tls:
      mode: ISTIO_MUTUAL
  subsets:
  - name: v1
    labels:
      version: v1
    trafficPolicy:
      loadBalancer:
        leastRequestConn: 100
      connectionPool:
        tcp:
          maxConnections: 10
          connectTimeout: 10s
          keepAlive:
            time: 300s
        http:
          http1MaxPendingRequests: 10
          maxRequestsPerConnection: 2
          maxRetries: 2
          idleTimeout: 60s
      outlierDetection:
        consecutiveErrors: 3
        interval: 15s
        baseEjectionTime: 15s
        maxEjectionPercent: 10
      timeout: 60s

---
# istio/virtual-service.yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: secure-app
  namespace: production
spec:
  hosts:
  - secure-app.production.company.com
  gateways:
  - istio-system/ingressgateway
  http:
  - match:
    - uri:
        prefix: /
    retries:
      attempts: 3
      perTryTimeout: 2s
      retryOn: [5xx, connect-failure, refused-stream]
    fault:
      delay:
        percentage:
          value: 0
        fixedDelay: 0s
    timeout: 300s
    route:
    - destination:
        host: secure-app
        subset: v1
    mirror:
      host: secure-app
      subset: v1
      mirrorPercentage:
        value: 5
    http:
    - match:
      - headers:
          canary: "true"
      route:
      - destination:
          host: secure-app
          subset: canary
      weight: 10
    http:
    - route:
      - destination:
          host: secure-app
          subset: v1
      weight: 90
```

### 5. ArgoCD GitOps Configuration

```yaml
# argocd/application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: secure-app
  namespace: argocd
  finalizers:
  - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/company/secure-app-k8s
    targetRevision: HEAD
    path: kubernetes/production
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
    - PruneLast=false
    - PrunePropagationPolicy=foreground
    retry:
      limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
  ignoreDifferences:
    - JSONPath: '.spec.template.spec.replicas'
  revisionHistoryLimit: 10
  plugins:
  - name: argocd-image-updater
    args:
      - image-updater
      - allow-tags
      - kwok='image-tag: "*"'
  - name: argocd-notifications
    args:
      - notifications
      - service: slack
      - slack-token: $SLACK_TOKEN
  - name: argocd-cm
    args:
      - cm
      - configMapName: argocd-cm
      - configMapKey: config.yaml
```

### 6. Monitoring and Observability

```yaml
# monitoring/prometheus.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: monitoring
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
      evaluation_interval: 15s

    rule_files:
      - "/etc/prometheus/rules/*.yml"

    scrape_configs:
      - job_name: 'kubernetes-pods'
        kubernetes_sd_configs:
          - role: pod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_name]
            target_label: pod
          - source_labels: [__meta_kubernetes_namespace]
            target_label: namespace
          - source_labels: [__meta_kubernetes_pod_label_app]
            target_label: app
          - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
            action: keep
            regex: true
            source_label: __meta_kubernetes_pod_annotation_prometheus_io_scrape
            target_label: __meta_kubernetes_pod_annotation_prometheus_io_scrape
        metric_relabel_configs:
          - source_labels: [__name__]
            regex: 'instance_.*'
            target_label: instance
          - action: labelmap
            regex: 'pod_.*'
            target_label: pod
          - source_labels: [__name__]
            regex: 'namespace_.*'
            target_label: namespace
          - source_labels: [__name__]
            regex: 'workload_.*'
            target_label: workload
      - job_name: 'kubernetes-services'
        kubernetes_sd_configs:
          - role: service
        relabel_configs:
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
            action: keep
            regex: true
            source_label: __meta_kubernetes_service_annotation_prometheus_io_scrape
            target_label: __meta_kubernetes_service_annotation_prometheus_io_scrape
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scheme]
            action: keep
            regex: true
            source_label: __meta_kubernetes_service_annotation_prometheus_io_scheme
            target_label: __meta_kubernetes_service_annotation_prometheus_io_scheme
          - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_path]
            action: keep
            regex: true
            source_label: __meta_kubernetes_service_annotation_prometheus_io_path
            target_label: __meta_kubernetes_service_annotation_prometheus_io_path
          - source_labels: [__meta_kubernetes_service_name]
            target_label: kubernetes_name
          - source_labels: [__meta_kubernetes_namespace]
            target_label: kubernetes_namespace
          - source_labels: [__meta_kubernetes_service_label]
            target_label: kubernetes_name

# Security rules
---
apiVersion: v1
kind: Secret
metadata:
  name: prometheus-rules
  namespace: monitoring
type: Opaque
stringData:
  security-alerts.yml: |
    groups:
    - name: security.rules
      rules:
        - alert: HighErrorRate
          expr: rate(http_requests_total{job="kubernetes-pods",status="5xx"}[5m]) > 0.1
          for: 5m
          labels:
            severity: "critical"
          annotations:
            summary: "High error rate detected"
            description: "Error rate is above 10% for 5 minutes"
            runbook_url: "https://runbooks.company.com/high-error-rate"
        - alert: UnauthorizedAccess
          expr: rate(http_requests_total{status="401"}[5m]) > 5
          for: 5m
          labels:
            severity: "warning"
          annotations:
            summary: "Unauthorized access attempts"
            description: "More than 5 unauthorized requests per minute"
            runbook_url: "https://runbooks.company.com/unauthorized-access"
        - alert: ContainerRestarts
          expr: rate(kube_pod_container_status_restarts_total[15m]) > 3
          for: 15m
          labels:
            severity: "warning"
          annotations:
            summary: "Container restarts detected"
            description: "Container has restarted more than 3 times in 15 minutes"
            runbook_url: "https://runbooks.company.com/container-restarts"
```

### 7. Production Deployment Checklist

```yaml
# deployment/production-checklist.yaml
security:
  container_security:
    minimal_base_image: true
    minimal_packages: true
    security_scanning: true
    vulnerability_scanning: true
    sbom_generation: true

  runtime_security:
    non_root_user: true
    readonly_filesystem: false
    capabilities_dropped_all: true
    seccomp_enabled: true
    apparmor_enabled: true
    selinux_enabled: true

  network_security:
    network_policies: true
    service_mesh: true
    mtls_enabled: true
    tls_version: "1.3"
    certificate_rotation: true

  secrets_management:
    encrypted_secrets: true
    key_rotation: true
    secret_versioning: true
    access_control: true

  rbac:
    principle_of_least_privilege: true
    service_accounts_limited: true
    token_min_ttl: true
    token_autorenewal: false

  compliance:
    cis_benchmark: true
    pod_security_standards: true
    nist_controls: true
    pci_dss: true
    hipaa: true

observability:
  monitoring:
    metrics_collection: true
    custom_metrics: true
    alerting_enabled: true
    dashboard_creation: true

  logging:
    structured_logging: true
    log_aggregation: true
    log_retention: true
    sensitive_data_redaction: true

  tracing:
    distributed_tracing: true
    span_sampling: true
    performance_tracking: true
    error_tracking: true

  auditing:
    api_audit_logging: true
    system_event_logging: true
    security_event_logging: true
    compliance_reporting: true

performance:
  resource_management:
    resource_limits: true
    resource_quotas: true
    hpa_enabled: true
    cluster_autoscaling: true

  optimization:
    image_optimization: true
    caching_enabled: true
    compression: true
    connection_pooling: true
    batch_processing: true

disaster_recovery:
  backup_strategy:
    automated_backups: true
    backup_encryption: true
    cross_region_backup: true
    restore_testing: true

  high_availability:
    multi_zone_deployment: true
    health_checks: true
    auto_healing: true
    graceful_shutdown: true
    rolling_updates: true

  testing:
  security_testing:
    penetration_testing: true
    vulnerability_scanning: true
    compliance_testing: true
    chaos_testing: true

  performance_testing:
    load_testing: true
    stress_testing: true
    scalability_testing: true
    reliability_testing: true
```

This comprehensive Docker/Kubernetes skill provides security-first containerization and deployment patterns for 2025, including zero-trust architectures, service mesh integration, GitOps workflows, and production-ready security hardening that works across different cloud providers and meets modern compliance standards.