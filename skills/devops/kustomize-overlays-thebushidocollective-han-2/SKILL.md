---
name: kustomize-overlays
description: Use when managing environment-specific Kubernetes configurations with Kustomize overlays and patches.
allowed-tools: [Bash, Read]
---

# Kustomize Overlays

Master environment-specific Kubernetes configuration management using Kustomize overlays, strategic merge patches, and JSON patches for development, staging, and production environments.

## Overview

Overlays enable environment-specific customization of Kubernetes resources without duplicating configuration. Each overlay references a base configuration and applies environment-specific patches, transformations, and resource adjustments.

## Basic Overlay Structure

```
myapp/
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
    │   └── namespace.yaml
    ├── staging/
    │   ├── kustomization.yaml
    │   ├── replica-patch.yaml
    │   ├── resource-patch.yaml
    │   └── namespace.yaml
    └── production/
        ├── kustomization.yaml
        ├── replica-patch.yaml
        ├── resource-patch.yaml
        ├── hpa.yaml
        └── namespace.yaml
```

## Base Configuration

### Base Kustomization

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

metadata:
  name: myapp-base

# Resources to include
resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
  - ingress.yaml

# Common labels applied to all resources
commonLabels:
  app: myapp
  managed-by: kustomize

# Common annotations
commonAnnotations:
  version: "1.0.0"
  team: platform

# Name prefix for all resources
namePrefix: myapp-

# Default namespace (can be overridden in overlays)
namespace: default

# Image transformations
images:
  - name: myapp
    newName: registry.example.com/myapp
    newTag: latest
```

### Base Deployment

```yaml
# base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment
spec:
  replicas: 1
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
        image: myapp:latest
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: config
              key: log-level
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Base Service

```yaml
# base/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: service
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: http
    protocol: TCP
    name: http
  selector:
    app: myapp
```

### Base ConfigMap

```yaml
# base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: config
data:
  log-level: "info"
  cache-enabled: "true"
  timeout: "30"
```

### Base Ingress

```yaml
# base/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
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

## Development Overlay

### Development Kustomization

```yaml
# overlays/development/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

# Reference the base
resources:
  - ../../base
  - namespace.yaml

# Override namespace
namespace: development

# Development-specific labels
commonLabels:
  environment: development
  cost-center: engineering

# Development-specific annotations
commonAnnotations:
  deployed-by: ci-cd
  environment: dev

# Name suffix for development resources
nameSuffix: -dev

# Image overrides for development
images:
  - name: myapp
    newName: registry.example.com/myapp
    newTag: dev-latest

# ConfigMap overrides
configMapGenerator:
  - name: config
    behavior: merge
    literals:
      - log-level=debug
      - cache-enabled=false
      - debug-mode=true

# Replica overrides
replicas:
  - name: myapp-deployment
    count: 1

# Strategic merge patches
patches:
  - path: replica-patch.yaml
    target:
      kind: Deployment
      name: myapp-deployment

# Inline patches
patchesStrategicMerge:
  - |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: deployment
    spec:
      template:
        spec:
          containers:
          - name: myapp
            env:
            - name: ENVIRONMENT
              value: development
            - name: DEBUG
              value: "true"
```

### Development Namespace

```yaml
# overlays/development/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: development
  labels:
    environment: development
    team: platform
```

### Development Replica Patch

```yaml
# overlays/development/replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: myapp
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
```

## Staging Overlay

### Staging Kustomization

```yaml
# overlays/staging/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base
  - namespace.yaml

namespace: staging

commonLabels:
  environment: staging
  cost-center: engineering

commonAnnotations:
  deployed-by: ci-cd
  environment: staging

nameSuffix: -staging

images:
  - name: myapp
    newName: registry.example.com/myapp
    newTag: staging-v1.2.3

configMapGenerator:
  - name: config
    behavior: merge
    literals:
      - log-level=info
      - cache-enabled=true
      - cache-ttl=300

replicas:
  - name: myapp-deployment
    count: 2

patches:
  - path: replica-patch.yaml
    target:
      kind: Deployment
      name: myapp-deployment
  - path: resource-patch.yaml
    target:
      kind: Deployment
      name: myapp-deployment

patchesStrategicMerge:
  - |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: deployment
    spec:
      template:
        metadata:
          annotations:
            prometheus.io/scrape: "true"
            prometheus.io/port: "8080"
        spec:
          containers:
          - name: myapp
            env:
            - name: ENVIRONMENT
              value: staging
            - name: METRICS_ENABLED
              value: "true"
          affinity:
            podAntiAffinity:
              preferredDuringSchedulingIgnoredDuringExecution:
              - weight: 100
                podAffinityTerm:
                  labelSelector:
                    matchExpressions:
                    - key: app
                      operator: In
                      values:
                      - myapp
                  topologyKey: kubernetes.io/hostname
```

### Staging Replica Patch

```yaml
# overlays/staging/replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
```

### Staging Resource Patch

```yaml
# overlays/staging/resource-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment
spec:
  template:
    spec:
      containers:
      - name: myapp
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Production Overlay

### Production Kustomization

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../base
  - namespace.yaml
  - hpa.yaml
  - pdb.yaml
  - network-policy.yaml

namespace: production

commonLabels:
  environment: production
  cost-center: product
  compliance: pci

commonAnnotations:
  deployed-by: ci-cd
  environment: production
  backup: "true"

nameSuffix: -prod

images:
  - name: myapp
    newName: registry.example.com/myapp
    newTag: v1.2.3
    digest: sha256:abc123...

configMapGenerator:
  - name: config
    behavior: merge
    literals:
      - log-level=warn
      - cache-enabled=true
      - cache-ttl=600
      - rate-limit-enabled=true

replicas:
  - name: myapp-deployment
    count: 5

patches:
  - path: replica-patch.yaml
    target:
      kind: Deployment
      name: myapp-deployment
  - path: resource-patch.yaml
    target:
      kind: Deployment
      name: myapp-deployment
  - path: security-patch.yaml
    target:
      kind: Deployment
      name: myapp-deployment

patchesStrategicMerge:
  - |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: deployment
    spec:
      template:
        metadata:
          annotations:
            prometheus.io/scrape: "true"
            prometheus.io/port: "8080"
            vault.hashicorp.com/agent-inject: "true"
            vault.hashicorp.com/role: "myapp"
        spec:
          containers:
          - name: myapp
            env:
            - name: ENVIRONMENT
              value: production
            - name: METRICS_ENABLED
              value: "true"
            - name: TRACING_ENABLED
              value: "true"
          affinity:
            podAntiAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
              - labelSelector:
                  matchExpressions:
                  - key: app
                    operator: In
                    values:
                    - myapp
                topologyKey: kubernetes.io/hostname
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                  - key: node.kubernetes.io/instance-type
                    operator: In
                    values:
                    - m5.xlarge
                    - m5.2xlarge

patchesJson6902:
  - target:
      group: networking.k8s.io
      version: v1
      kind: Ingress
      name: myapp-ingress
    patch: |-
      - op: replace
        path: /spec/rules/0/host
        value: myapp.production.example.com
      - op: add
        path: /metadata/annotations/cert-manager.io~1cluster-issuer
        value: letsencrypt-prod
      - op: add
        path: /spec/tls
        value:
        - hosts:
          - myapp.production.example.com
          secretName: myapp-tls
```

### Production Replica Patch

```yaml
# overlays/production/replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 0
  minReadySeconds: 30
```

### Production Resource Patch

```yaml
# overlays/production/resource-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment
spec:
  template:
    spec:
      containers:
      - name: myapp
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

### Production Security Patch

```yaml
# overlays/production/security-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: myapp
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

### Production HPA

```yaml
# overlays/production/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp-deployment-prod
  minReplicas: 5
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 30
      - type: Pods
        value: 2
        periodSeconds: 30
      selectPolicy: Max
```

### Production PDB

```yaml
# overlays/production/pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb-prod
spec:
  minAvailable: 3
  selector:
    matchLabels:
      app: myapp
      environment: production
```

### Production Network Policy

```yaml
# overlays/production/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: myapp-network-policy-prod
spec:
  podSelector:
    matchLabels:
      app: myapp
      environment: production
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    - podSelector:
        matchLabels:
          app: prometheus
    ports:
    - protocol: TCP
      port: 8080
  egress:
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
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

## JSON Patch Examples

### Replace Operations

```yaml
patchesJson6902:
  - target:
      group: apps
      version: v1
      kind: Deployment
      name: myapp-deployment
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 10
      - op: replace
        path: /spec/template/spec/containers/0/image
        value: registry.example.com/myapp:v2.0.0
```

### Add Operations

```yaml
patchesJson6902:
  - target:
      group: apps
      version: v1
      kind: Deployment
      name: myapp-deployment
    patch: |-
      - op: add
        path: /spec/template/spec/containers/0/env/-
        value:
          name: NEW_FEATURE_FLAG
          value: "true"
      - op: add
        path: /spec/template/metadata/annotations/sidecar.istio.io~1inject
        value: "true"
```

### Remove Operations

```yaml
patchesJson6902:
  - target:
      group: apps
      version: v1
      kind: Deployment
      name: myapp-deployment
    patch: |-
      - op: remove
        path: /spec/template/spec/containers/0/env/2
      - op: remove
        path: /spec/template/metadata/annotations/deprecated-annotation
```

## Advanced Patch Techniques

### Conditional Patches

```yaml
# overlays/production/kustomization.yaml
patches:
  - target:
      kind: Deployment
      labelSelector: "tier=frontend"
    patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: not-used
      spec:
        template:
          spec:
            containers:
            - name: myapp
              resources:
                limits:
                  memory: "2Gi"
```

### Multi-Resource Patches

```yaml
patches:
  - target:
      kind: Deployment|StatefulSet
      name: myapp-.*
    patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: not-used
        annotations:
          monitoring: "enabled"
```

### Patch with Options

```yaml
patches:
  - path: cpu-patch.yaml
    target:
      kind: Deployment
    options:
      allowNameChange: true
      allowKindChange: false
```

## Multi-Environment Configuration

### Region-Specific Overlays

```
overlays/
├── us-east-1/
│   ├── development/
│   ├── staging/
│   └── production/
└── eu-west-1/
    ├── development/
    ├── staging/
    └── production/
```

### Regional Production Overlay

```yaml
# overlays/us-east-1/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - ../../../overlays/production

commonLabels:
  region: us-east-1

configMapGenerator:
  - name: config
    behavior: merge
    literals:
      - region=us-east-1
      - s3-bucket=myapp-prod-us-east-1
      - cdn-url=https://us-east-1.cdn.example.com

patchesStrategicMerge:
  - |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: deployment
    spec:
      template:
        spec:
          affinity:
            nodeAffinity:
              requiredDuringSchedulingIgnoredDuringExecution:
                nodeSelectorTerms:
                - matchExpressions:
                  - key: topology.kubernetes.io/region
                    operator: In
                    values:
                    - us-east-1
```

## When to Use This Skill

Use the kustomize-overlays skill when you need to:

1. Manage multiple environments (dev, staging, production) with different configurations
2. Apply environment-specific patches to base Kubernetes resources
3. Override resource limits, replicas, or environment variables per environment
4. Maintain a single source of truth with environment-specific variations
5. Apply strategic merge patches or JSON patches to resources
6. Manage region-specific or tenant-specific configurations
7. Implement progressive delivery with canary or blue-green deployments
8. Apply security policies and network policies per environment
9. Configure autoscaling differently across environments
10. Manage image tags and versions across multiple environments
11. Apply conditional patches based on labels or resource types
12. Implement cost optimization by varying resources per environment
13. Configure monitoring and observability settings per environment
14. Manage ingress rules and certificates per environment
15. Apply compliance and regulatory requirements to specific environments

## Best Practices

1. Keep base configurations minimal and environment-agnostic
2. Use strategic merge patches for simple modifications
3. Use JSON patches for precise, surgical changes
4. Organize overlays by environment, then by region if needed
5. Use commonLabels to track resources by environment
6. Apply nameSuffix or namePrefix to avoid resource conflicts
7. Pin image tags with digests in production overlays
8. Use configMapGenerator with behavior: merge to override specific keys
9. Test overlay output with kustomize build before applying
10. Use kustomize edit commands for programmatic updates
11. Leverage replicas field for quick replica count overrides
12. Apply security contexts progressively from dev to production
13. Use HPA in production, fixed replicas in development
14. Document patch rationale in comments within kustomization.yaml
15. Use version control to track overlay changes over time
16. Validate patches don't inadvertently remove critical settings
17. Use namespace field consistently across all overlays
18. Apply resource quotas and limits progressively
19. Use podDisruptionBudgets only in production environments
20. Test disaster recovery by applying production overlays to staging
21. Use labelSelector in patches for conditional application
22. Avoid hardcoding environment-specific values in base
23. Use generators for ConfigMaps and Secrets instead of static files
24. Apply network policies in production for security
25. Use affinity rules to distribute pods across nodes in production

## Common Pitfalls

1. Duplicating entire resources in overlays instead of patching
2. Hardcoding environment-specific values in base configurations
3. Not using namespace field consistently across overlays
4. Forgetting to update image tags in production overlays
5. Over-patching - making too many changes in overlays
6. Not testing overlay output before applying to clusters
7. Using incorrect patch paths in JSON patches
8. Forgetting to escape tildes in JSON patch paths
9. Not using behavior: merge with configMapGenerator
10. Applying production-grade resources to development environments
11. Not validating that patches actually apply successfully
12. Using replicas in kustomization.yaml and deployment patches simultaneously
13. Not organizing overlays in a clear directory structure
14. Forgetting to add new resources to kustomization.yaml
15. Using absolute paths instead of relative paths in resources
16. Not documenting why specific patches are necessary
17. Applying breaking patches without testing
18. Not using version control for overlay changes
19. Forgetting to apply security contexts in production
20. Using mutable image tags in production overlays
21. Not considering resource consumption differences across environments
22. Applying patches that conflict with each other
23. Not validating JSON patch syntax before committing
24. Using strategic merge for complex changes better suited to JSON patch
25. Not cleaning up obsolete patches and overlay resources
26. Forgetting to update overlay references when restructuring
27. Not using labelSelector for conditional patches
28. Hardcoding secrets in overlays instead of using external secret management
29. Not testing overlay changes in lower environments first
30. Applying network policies without understanding connectivity requirements

## Resources

- [Kustomize Official Documentation](https://kustomize.io/)
- [Kubernetes SIG-CLI Kustomize](https://github.com/kubernetes-sigs/kustomize)
- [Kustomize Feature List](https://kubectl.docs.kubernetes.io/references/kustomize/)
- [Strategic Merge Patch](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-api-machinery/strategic-merge-patch.md)
- [JSON Patch RFC 6902](https://tools.ietf.org/html/rfc6902)
- [Kubectl Apply with Kustomize](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- [Kustomize Best Practices](https://kubectl.docs.kubernetes.io/guides/config_management/)
- [GitOps with Kustomize](https://www.gitops.tech/)
