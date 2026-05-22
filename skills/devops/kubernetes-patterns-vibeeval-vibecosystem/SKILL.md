---
name: kubernetes-patterns
description: Pod design patterns, sidecar containers, init containers, config management, rolling updates, and resource limits.
---

# Kubernetes Patterns

Production-grade Kubernetes deployment and pod design patterns.

## Pod Design Patterns

```yaml
# Sidecar Pattern: log collector alongside main app
apiVersion: v1
kind: Pod
metadata:
  name: app-with-sidecar
spec:
  containers:
    - name: app
      image: myapp:v1.2.0
      ports:
        - containerPort: 8080
      volumeMounts:
        - name: logs
          mountPath: /var/log/app

    - name: log-collector
      image: fluentd:v1.16
      volumeMounts:
        - name: logs
          mountPath: /var/log/app
          readOnly: true

  volumes:
    - name: logs
      emptyDir: {}
```

## Init Containers

```yaml
# Run setup tasks before main container starts
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 3
  template:
    spec:
      initContainers:
        # Wait for database to be ready
        - name: wait-for-db
          image: busybox:1.36
          command: ['sh', '-c', 'until nc -z postgres-svc 5432; do sleep 2; done']

        # Run database migrations
        - name: run-migrations
          image: myapp:v1.2.0
          command: ['npx', 'prisma', 'migrate', 'deploy']
          envFrom:
            - secretRef:
                name: db-credentials

      containers:
        - name: api
          image: myapp:v1.2.0
          ports:
            - containerPort: 3000
```

## Resource Limits and Requests

```yaml
containers:
  - name: api
    image: myapp:v1.2.0
    resources:
      requests:          # Scheduler uses this to place pods
        cpu: 250m        # 0.25 CPU cores
        memory: 256Mi    # 256 MB
      limits:            # OOM kill / CPU throttle beyond this
        cpu: 500m        # 0.5 CPU cores
        memory: 512Mi    # 512 MB

    # Liveness: restart container if health check fails
    livenessProbe:
      httpGet:
        path: /healthz
        port: 3000
      initialDelaySeconds: 15
      periodSeconds: 10
      failureThreshold: 3

    # Readiness: remove from service if not ready (no traffic)
    readinessProbe:
      httpGet:
        path: /ready
        port: 3000
      initialDelaySeconds: 5
      periodSeconds: 5

    # Startup: disable liveness/readiness until app starts
    startupProbe:
      httpGet:
        path: /healthz
        port: 3000
      failureThreshold: 30    # 30 * 10s = 5 min max startup
      periodSeconds: 10
```

## ConfigMap and Secrets

```yaml
# ConfigMap for non-sensitive config
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"
  FEATURE_NEW_UI: "true"

---
# Secret for sensitive data (base64 encoded, use sealed-secrets in prod)
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
type: Opaque
stringData:        # stringData auto-encodes to base64
  DATABASE_URL: "postgresql://user:pass@postgres:5432/mydb"
  JWT_SECRET: "super-secret-key"

---
# Mount in deployment
spec:
  containers:
    - name: api
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: db-credentials
```

## Rolling Update Strategy

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1          # At most 5 pods during update (4+1)
      maxUnavailable: 0    # All 4 must stay available (zero downtime)

  template:
    spec:
      terminationGracePeriodSeconds: 30

      containers:
        - name: api
          image: myapp:v1.2.0
          lifecycle:
            preStop:
              exec:
                # Allow in-flight requests to complete
                command: ["/bin/sh", "-c", "sleep 5"]
```

## Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-server
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70    # Scale up when CPU > 70%
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300   # Wait 5 min before scaling down
      policies:
        - type: Percent
          value: 25                     # Max 25% reduction per period
          periodSeconds: 60
```

## Network Policy

```yaml
# Only allow traffic from specific namespaces/pods
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-network-policy
spec:
  podSelector:
    matchLabels:
      app: api-server
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              env: production
        - podSelector:
            matchLabels:
              role: frontend
      ports:
        - port: 3000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
```

## Checklist

- [ ] Resource requests AND limits set for every container
- [ ] Liveness, readiness, and startup probes configured
- [ ] Rolling update with maxUnavailable: 0 for zero-downtime deploys
- [ ] preStop hook with sleep for graceful connection draining
- [ ] Pod Disruption Budget (minAvailable: 50%) for maintenance windows
- [ ] Network policies restrict ingress/egress to required paths only
- [ ] Secrets managed via sealed-secrets or external-secrets, not plain YAML
- [ ] HPA configured with scale-down stabilization window

## Anti-Patterns

- No resource limits: single pod can starve the entire node
- Liveness probe hitting a heavy endpoint: cascading restarts under load
- Using `latest` tag: no rollback capability, unpredictable deployments
- Storing secrets in ConfigMaps: no encryption at rest
- Single replica for stateful services: no availability during updates
- Missing PodDisruptionBudget: node drain kills all pods simultaneously
