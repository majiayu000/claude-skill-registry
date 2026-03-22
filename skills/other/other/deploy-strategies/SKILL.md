---
name: deploy-strategies
description: >
  Guide for deployment strategies including blue-green, canary, rolling updates, feature flags,
  and rollback procedures. Use when the user asks about deployment patterns, zero-downtime
  deployments, release strategies, or rollback plans. Trigger whenever deployment, release
  management, or production rollout is discussed.
---

# Deploy Strategies

Implement safe, zero-downtime deployment strategies with proper rollback procedures,
traffic shifting, and health monitoring.

## When to Use
- User asks about zero-downtime deployments
- User needs to choose between deployment strategies
- User asks about canary releases or blue-green deploys
- User implements feature flags for gradual rollout
- User needs rollback procedures

## Core Patterns

### Blue-Green Deployment

Maintain two identical production environments. Route traffic to the new one after
verification, keep the old one as instant rollback.

```yaml
# Kubernetes blue-green with service switching
apiVersion: v1
kind: Service
metadata:
  name: api
spec:
  selector:
    app: api
    version: green      # Switch to "blue" for rollback
  ports:
    - port: 80
      targetPort: 3000
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
      version: green
  template:
    metadata:
      labels:
        app: api
        version: green
    spec:
      containers:
        - name: api
          image: myapp:2.0.0
          readinessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
```

```bash
# Blue-green deploy script
deploy_blue_green() {
  local NEW_VERSION=$1
  local CURRENT=$(kubectl get svc api -o jsonpath='{.spec.selector.version}')
  local TARGET=$( [ "$CURRENT" = "blue" ] && echo "green" || echo "blue" )

  # Deploy new version to inactive slot
  kubectl set image "deployment/api-${TARGET}" "api=myapp:${NEW_VERSION}"
  kubectl rollout status "deployment/api-${TARGET}" --timeout=300s

  # Run smoke tests against new deployment
  kubectl run smoke-test --rm -i --image=curlimages/curl -- \
    curl -f "http://api-${TARGET}.default.svc/health"

  # Switch traffic
  kubectl patch svc api -p "{\"spec\":{\"selector\":{\"version\":\"${TARGET}\"}}}"
  echo "Traffic switched to ${TARGET} (v${NEW_VERSION})"
}
```

### Canary Deployment

Route a small percentage of traffic to the new version, monitor metrics, then gradually
increase if healthy.

```yaml
# Nginx Ingress canary annotation
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "10"
spec:
  rules:
    - host: api.myapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-canary
                port:
                  number: 80
```

```bash
# Progressive canary rollout
canary_deploy() {
  local WEIGHTS=(5 10 25 50 100)

  for weight in "${WEIGHTS[@]}"; do
    echo "Setting canary weight to ${weight}%"
    kubectl annotate ingress api-canary \
      nginx.ingress.kubernetes.io/canary-weight="${weight}" --overwrite

    # Monitor error rate for 5 minutes
    sleep 300
    ERROR_RATE=$(curl -s "http://prometheus:9090/api/v1/query?query=rate(http_errors_total[5m])" \
      | jq '.data.result[0].value[1]' -r)

    if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
      echo "Error rate ${ERROR_RATE} exceeds threshold, rolling back"
      kubectl annotate ingress api-canary \
        nginx.ingress.kubernetes.io/canary-weight="0" --overwrite
      exit 1
    fi
  done
  echo "Canary promotion complete"
}
```

### Rolling Update

Replace instances gradually with built-in Kubernetes rollout controls.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 6
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2           # Create 2 extra pods during rollout
      maxUnavailable: 1     # At most 1 pod unavailable
  template:
    spec:
      containers:
        - name: api
          image: myapp:2.0.0
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 5
            failureThreshold: 3
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 30
            periodSeconds: 10
      terminationGracePeriodSeconds: 60
```

```bash
# Monitor and auto-rollback
kubectl rollout status deployment/api --timeout=600s || kubectl rollout undo deployment/api
```

### Feature Flags for Gradual Rollout

Decouple deployment from release. Ship code behind flags and enable for specific users
or percentages.

```typescript
interface FeatureFlag {
  readonly name: string
  readonly enabled: boolean
  readonly percentage: number
  readonly allowlist: readonly string[]
}

function isFeatureEnabled(flag: FeatureFlag, userId: string): boolean {
  if (!flag.enabled) return false
  if (flag.allowlist.includes(userId)) return true
  const hash = hashCode(`${flag.name}:${userId}`)
  return (hash % 100) < flag.percentage
}
```

### Rollback Procedures

Every deployment must have a tested rollback path. Automate rollback triggers based
on health metrics.

```bash
#!/bin/bash
# Deploy and auto-rollback on health check failure
kubectl set image "deployment/api" "api=myapp:${NEW_VERSION}"
kubectl rollout status "deployment/api" --timeout=300s

# Verify health, rollback if failing
for i in 1 2 3; do
  curl -sf "https://api.myapp.com/health" && break
  [ "$i" -eq 3 ] && { kubectl rollout undo deployment/api; exit 1; }
  sleep 10
done
```

## Anti-Patterns

- **No health checks**: Without readiness probes, traffic reaches pods before they are ready, causing errors during deployment.
- **Big bang releases**: Deploying all changes at once to 100% of traffic. Always use gradual rollout for significant changes.
- **No rollback plan**: If you cannot roll back in under 5 minutes, your deployment process is not production-ready.
- **Database-coupled deploys**: Schema changes that break the old version prevent rollback. Use backwards-compatible migrations.
- **Manual deployments**: One-off SSH deployments are error-prone and unrepeatable. Automate everything.
- **Ignoring drain and graceful shutdown**: Killing pods without draining connections drops in-flight requests. Use `preStop` hooks and `terminationGracePeriodSeconds`.

## Quick Reference

| Strategy | Zero Downtime | Rollback Speed | Resource Cost | Complexity |
|---|---|---|---|---|
| Blue-Green | Yes | Instant (switch) | 2x (two envs) | Medium |
| Canary | Yes | Fast (shift to 0%) | 1.1x | High |
| Rolling | Yes | Medium (rollback) | 1.2x | Low |
| Feature Flag | Yes | Instant (toggle) | 1x | Medium |
| Recreate | No | Slow (redeploy) | 1x | Low |
