---
name: kubernetes-deployment
description: Deploy, manage, and scale applications on Kubernetes clusters using manifests, Helm charts, and autoscaling configurations. Use when the user requests kubernetes deployment or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Kubernetes Deployment

This skill enables the agent to deploy and manage applications on Kubernetes clusters. The agent can generate deployment manifests, services, ingress rules, Helm charts, and autoscaling configurations. It handles the full lifecycle from initial deployment through scaling, rolling updates, and troubleshooting, following production best practices for resource management, security, and reliability.

## Workflow

1. **Configure Cluster Access:** The agent verifies that `kubectl` is configured with the correct cluster context and namespace. It checks connectivity with `kubectl cluster-info` and confirms that the user has sufficient RBAC permissions to create and manage resources in the target namespace. If a kubeconfig is not present, the agent guides the user through authentication (e.g., `aws eks update-kubeconfig`, `gcloud container clusters get-credentials`).

2. **Define Deployment Manifests:** The agent creates Kubernetes deployment manifests specifying the container image, replica count, resource requests and limits, environment variables, liveness and readiness probes, and pod anti-affinity rules. Labels and annotations are applied consistently for service discovery, monitoring, and operations. The agent uses specific image tags (never `latest`) and sets `imagePullPolicy` appropriately.

3. **Configure Services and Ingress:** The agent creates Service resources to expose deployments within the cluster (ClusterIP) or externally (LoadBalancer, NodePort). For HTTP workloads, the agent configures Ingress resources with TLS termination using cert-manager, path-based routing, and rate limiting annotations. The agent selects the appropriate service type based on the deployment environment and traffic requirements.

4. **Apply Manifests and Verify Rollout:** The agent applies manifests using `kubectl apply -f` and monitors the rollout with `kubectl rollout status`. It verifies that all pods reach the Running state, health checks pass, and the service endpoints are registered. If a rollout stalls, the agent checks pod events with `kubectl describe pod` and logs with `kubectl logs` to diagnose the issue, and can execute `kubectl rollout undo` to revert to the previous version.

5. **Configure Autoscaling:** The agent sets up Horizontal Pod Autoscalers (HPA) to scale the replica count based on CPU utilization, memory usage, or custom metrics. It defines minimum and maximum replica counts, scale-up and scale-down behavior, and stabilization windows to prevent thrashing. For workloads with variable resource needs, the agent can also configure Vertical Pod Autoscalers (VPA).

6. **Manage with Helm Charts:** For complex applications with multiple environments, the agent packages Kubernetes manifests into Helm charts with templated values. Helm enables versioned releases, atomic upgrades with automatic rollback on failure, and environment-specific value overrides. The agent uses `helm upgrade --install` for idempotent deployments and `helm diff` to preview changes before applying.

## Supported Technologies

- **Orchestration:** Kubernetes (EKS, GKE, AKS, self-managed), k3s, kind, minikube
- **Package Management:** Helm 3, Kustomize
- **Autoscaling:** HPA, VPA, KEDA, Cluster Autoscaler
- **Networking:** Nginx Ingress Controller, Traefik, Istio, Cilium
- **Certificate Management:** cert-manager, Let's Encrypt
- **CI/CD Integration:** ArgoCD, Flux, GitHub Actions, GitLab CI

## Usage

Provide the agent with your application's container image, resource requirements, desired replica count, and target Kubernetes cluster details.

**Example prompt:**

```
Deploy my app to the production EKS cluster:
- Image: myregistry.io/myapp:v2.1.0
- 3 replicas with CPU/memory limits
- Liveness and readiness probes on /health
- Expose via Ingress at api.example.com with TLS
- HPA scaling between 3-10 replicas based on CPU
```

## Examples

### Example 1: Production Deployment with Service and Ingress

**deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    version: v2.1.0
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
        version: v2.1.0
    spec:
      serviceAccountName: myapp
      terminationGracePeriodSeconds: 60
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app
                      operator: In
                      values: [myapp]
                topologyKey: kubernetes.io/hostname
      containers:
        - name: myapp
          image: myregistry.io/myapp:v2.1.0
          ports:
            - containerPort: 3000
              name: http
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
          resources:
            requests:
              cpu: 250m
              memory: 256Mi
            limits:
              cpu: "1"
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
          lifecycle:
            preStop:
              exec:
                command: ["/bin/sh", "-c", "sleep 15"]
```

**service.yaml:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
  namespace: production
spec:
  selector:
    app: myapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: http
  type: ClusterIP
```

**ingress.yaml:**

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp
  namespace: production
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: myapp-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: myapp
                port:
                  number: 80
```

### Example 2: Horizontal Pod Autoscaler with Helm Deployment

**Install or upgrade using Helm with custom values:**

```bash
helm upgrade --install myapp ./charts/myapp \
  --namespace production \
  --set image.tag=v2.1.0 \
  --set replicaCount=3 \
  --set autoscaling.enabled=true \
  --values values-production.yaml \
  --wait --timeout 5m \
  --atomic
```

**hpa.yaml** — Horizontal Pod Autoscaler:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 3
  maxReplicas: 10
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
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 25
          periodSeconds: 120
```

**Deployment steps:**

1. `kubectl create namespace production` (if it does not exist)
2. `kubectl apply -f deployment.yaml -f service.yaml -f ingress.yaml`
3. `kubectl apply -f hpa.yaml`
4. `kubectl rollout status deployment/myapp -n production`
5. `kubectl get hpa myapp -n production` to verify autoscaler targets

## Best Practices

- **Always set resource requests and limits:** Every container should define CPU and memory requests (for scheduling) and limits (to prevent noisy-neighbor issues). Without requests, the scheduler cannot make informed placement decisions, and without limits, a single pod can consume all node resources.
- **Configure liveness and readiness probes:** Liveness probes allow Kubernetes to restart containers that are stuck or deadlocked. Readiness probes prevent traffic from being routed to pods that are not yet ready to serve requests. Set appropriate `initialDelaySeconds` to avoid killing pods during startup.
- **Use namespaces for isolation:** Separate environments (dev, staging, production) and teams into distinct namespaces. Apply ResourceQuotas and LimitRanges per namespace to prevent any single team or environment from consuming excessive cluster resources.
- **Implement RBAC with least privilege:** Create service accounts with minimal permissions for each application. Avoid using the `default` service account or granting `cluster-admin` to workloads. Use Roles and RoleBindings scoped to the namespace rather than ClusterRoles when possible.
- **Use Helm for repeatable deployments:** Helm charts package manifests with templated values, enabling consistent deployments across environments. Use `--atomic` for automatic rollback on failure and `--wait` to block until resources are healthy.
- **Set pod disruption budgets:** Define PodDisruptionBudgets (PDBs) to ensure a minimum number of replicas remain available during voluntary disruptions like node drains and cluster upgrades. For example, `minAvailable: 2` ensures at least 2 pods are running at all times.

## Edge Cases

- **CrashLoopBackOff:** A pod repeatedly crashes and Kubernetes applies exponential backoff delays between restart attempts. Diagnose with `kubectl logs <pod> --previous` to see the crash output and `kubectl describe pod <pod>` for events. Common causes include misconfigured environment variables, missing secrets, or failed database connections.
- **ImagePullBackOff:** The container runtime cannot pull the specified image. This occurs when the image tag does not exist, the registry requires authentication, or there is a network issue. Verify the image exists with `docker pull`, check `imagePullSecrets` on the pod spec, and ensure the node has network access to the registry.
- **Pod eviction under node pressure:** When a node runs low on memory or disk, the kubelet evicts pods starting with those exceeding their resource requests (BestEffort pods first, then Burstable). Set appropriate resource requests to ensure critical pods are categorized as Guaranteed QoS class and are evicted last.
- **Stuck rollouts and deadlines:** A deployment rollout can stall if new pods fail readiness checks. The default `progressDeadlineSeconds` is 600 seconds, after which Kubernetes marks the rollout as failed. Use `kubectl rollout undo deployment/myapp` to revert immediately rather than waiting for the deadline.
- **DNS resolution failures in new namespaces:** Pods in newly created namespaces may experience temporary DNS resolution failures if CoreDNS has not yet updated its internal records. Application containers should implement retry logic with backoff for initial service discovery calls.
- **Helm release conflicts:** If a previous `helm upgrade` was interrupted (e.g., by a timeout), the release may be in a `pending-upgrade` or `failed` state. Use `helm history myapp` to inspect the state and `helm rollback myapp <revision>` to recover before attempting another upgrade.
