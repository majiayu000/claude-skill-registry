---
name: kubernetes-deployment-patterns
description: Kubernetes deployment strategies and workload patterns for production-grade applications. Use when deploying to Kubernetes, implementing rollout strategies, or designing cloud-native application architectures.
---

# Kubernetes Deployment Patterns

Expert guidance for production-grade Kubernetes deployments covering deployment strategies, workload types, configuration management, resource optimization, and autoscaling patterns for cloud-native applications.

## When to Use This Skill

- Implementing deployment strategies (rolling updates, blue-green, canary releases)
- Choosing appropriate workload types (Deployment, StatefulSet, DaemonSet, Job)
- Designing rollout strategies for zero-downtime deployments
- Implementing configuration management with ConfigMaps and Secrets
- Setting up resource management and autoscaling (HPA, VPA)
- Configuring health checks and probe strategies
- Designing highly available applications on Kubernetes
- Implementing batch processing and scheduled jobs

## Core Concepts

### Deployment Strategies

**Rolling Update:** Gradually replace old pods with new ones (zero-downtime, default)
**Recreate:** Terminate all old pods before creating new ones (brief downtime)
**Blue-Green:** Run two environments, switch traffic instantly (2x resources)
**Canary:** Gradually shift traffic to new version while monitoring (risk mitigation)

### Workload Types

**Deployment:** Stateless applications (web servers, APIs, microservices)
**StatefulSet:** Stateful applications (databases, message queues)
**DaemonSet:** Node-level services (log collectors, monitoring agents)
**Job:** One-time tasks (batch processing, migrations)
**CronJob:** Scheduled tasks (backups, periodic reports)

### Resource Management

**Requests:** Guaranteed resources for scheduling
**Limits:** Maximum resources enforced by kubelet
**HPA:** Horizontal Pod Autoscaler (scale replicas based on metrics)
**VPA:** Vertical Pod Autoscaler (adjust resource requests/limits)

## Quick Reference

| Task | Load reference |
| --- | --- |
| Deployment strategies (rolling, blue-green, canary) | `skills/kubernetes-deployment-patterns/references/deployment-strategies.md` |
| Workload types (Deployment, StatefulSet, DaemonSet, Job) | `skills/kubernetes-deployment-patterns/references/workload-types.md` |
| Configuration management (ConfigMaps, Secrets) | `skills/kubernetes-deployment-patterns/references/configuration-management.md` |
| Resource management and autoscaling (HPA, VPA) | `skills/kubernetes-deployment-patterns/references/resource-management.md` |
| Production best practices and security | `skills/kubernetes-deployment-patterns/references/production-best-practices.md` |

## Workflow

### 1. Choose Deployment Strategy

```yaml
# Rolling update for standard deployments
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0

# Recreate for incompatible versions
strategy:
  type: Recreate
```

### 2. Select Workload Type

- **Stateless?** → Use Deployment
- **Stateful with persistent identity?** → Use StatefulSet
- **One pod per node?** → Use DaemonSet
- **Run to completion?** → Use Job
- **Run on schedule?** → Use CronJob

### 3. Configure Resources

```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"
  limits:
    memory: "512Mi"
    cpu: "1000m"
```

### 4. Add Configuration

```yaml
# ConfigMap for non-sensitive config
envFrom:
- configMapRef:
    name: app-config

# Secret for sensitive data
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-credentials
      key: password
```

### 5. Implement Health Checks

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

### 6. Enable Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Common Mistakes

1. **Using `latest` tag:** Always use specific version tags for reproducibility
2. **No resource limits:** Can cause resource starvation and cluster instability
3. **Missing health checks:** Kubernetes can't manage pod health without probes
4. **Single replica in production:** No high availability or resilience
5. **Secrets in ConfigMaps:** Use Secrets for sensitive data, not ConfigMaps
6. **No update strategy:** Leads to unpredictable deployment behavior
7. **Running as root:** Security vulnerability, violates least privilege
8. **No monitoring:** Can't detect or debug issues in production

## Resources

- **Official Docs:** https://kubernetes.io/docs/concepts/workloads/
- **Deployment Strategies:** https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- **StatefulSets:** https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- **Autoscaling:** https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- **Configuration:** https://kubernetes.io/docs/concepts/configuration/
- **Best Practices:** https://kubernetes.io/docs/concepts/configuration/overview/
