---
name: canary-deployment
description: Implement canary deployment strategies to gradually roll out new versions to subset of users with automatic rollback based on metrics.
---

# Canary Deployment

## Overview

Deploy new versions gradually to a small percentage of users, monitor metrics for issues, and automatically rollback or proceed based on predefined thresholds.

## When to Use

- Low-risk gradual rollouts
- Real-world testing with live traffic
- Automatic rollback on errors
- User impact minimization
- A/B testing integration
- Metrics-driven deployments
- High-traffic services

## Implementation Examples

### 1. **Istio-based Canary Deployment**

```yaml
# canary-deployment-istio.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v1
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: v1
  template:
    metadata:
      labels:
        app: myapp
        version: v1
    spec:
      containers:
        - name: myapp
          image: myrepo/myapp:1.0.0
          ports:
            - containerPort: 8080

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-v2
  namespace: production
spec:
  replicas: 1  # Start with minimal replicas for canary
  selector:
    matchLabels:
      app: myapp
      version: v2
  template:
    metadata:
      labels:
        app: myapp
        version: v2
    spec:
      containers:
        - name: myapp
          image: myrepo/myapp:2.0.0
          ports:
            - containerPort: 8080

---
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: myapp
  namespace: production
spec:
  hosts:
    - myapp
  http:
    # Canary: 5% to v2, 95% to v1
    - match:
        - headers:
            user-agent:
              regex: ".*Chrome.*"  # Test with Chrome
      route:
        - destination:
            host: myapp
            subset: v2
          weight: 100
      timeout: 10s

    # Default route with traffic split
    - route:
        - destination:
            host: myapp
            subset: v1
          weight: 95
        - destination:
            host: myapp
            subset: v2
          weight: 5
      timeout: 10s

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: myapp
  namespace: production
spec:
  host: myapp
  trafficPolicy:
    connectionPool:
      http:
        http1MaxPendingRequests: 100
        maxRequestsPerConnection: 2

  subsets:
    - name: v1
      labels:
        version: v1

    - name: v2
      labels:
        version: v2
      trafficPolicy:
        outlierDetection:
          consecutive5xxErrors: 3
          interval: 30s
          baseEjectionTime: 30s

---
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
  namespace: production
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  progressDeadlineSeconds: 300
  service:
    port: 80

  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 5
    stepWeightPromotion: 10

  metrics:
    - name: request-success-rate
      thresholdRange:
        min: 99
      interval: 1m

    - name: request-duration
      thresholdRange:
        max: 500
      interval: 30s

  webhooks:
    - name: acceptance-test
      url: http://flagger-loadtester/
      timeout: 30s
      metadata:
        type: smoke
        cmd: "curl -sd 'test' http://myapp-canary/api/test"

    - name: load-test
      url: http://flagger-loadtester/
      timeout: 5s
      metadata:
        cmd: "hey -z 1m -q 10 -c 2 http://myapp-canary/"
        logCmdOutput: "true"

  # Automatic rollback on failure
  skipAnalysis: false
```

### 2. **Kubernetes Native Canary Script**

```bash
#!/bin/bash
# canary-rollout.sh - Canary deployment with k8s native tools

set -euo pipefail

NAMESPACE="${1:-production}"
DEPLOYMENT="${2:-myapp}"
NEW_VERSION="${3:-latest}"
CANARY_WEIGHT=10
MAX_WEIGHT=100
STEP_WEIGHT=10
CHECK_INTERVAL=60
MAX_ERROR_RATE=0.05

echo "Starting canary deployment for $DEPLOYMENT with version $NEW_VERSION"

# Get current replicas
CURRENT_REPLICAS=$(kubectl get deployment $DEPLOYMENT -n "$NAMESPACE" \
  -o jsonpath='{.spec.replicas}')
CANARY_REPLICAS=$((CURRENT_REPLICAS / 10 + 1))

echo "Current replicas: $CURRENT_REPLICAS, Canary replicas: $CANARY_REPLICAS"

# Create canary deployment
kubectl set image deployment/${DEPLOYMENT}-canary \
  ${DEPLOYMENT}=myrepo/${DEPLOYMENT}:${NEW_VERSION} \
  -n "$NAMESPACE"

# Scale up canary gradually
CURRENT_WEIGHT=$CANARY_WEIGHT
while [ $CURRENT_WEIGHT -le $MAX_WEIGHT ]; do
  echo "Setting traffic to canary: ${CURRENT_WEIGHT}%"

  # Update ingress or service to split traffic
  kubectl patch virtualservice ${DEPLOYMENT} -n "$NAMESPACE" --type merge \
    -p '{"spec":{"http":[{"route":[{"destination":{"host":"'${DEPLOYMENT}-stable'"},"weight":'$((100-CURRENT_WEIGHT))'},{"destination":{"host":"'${DEPLOYMENT}-canary'"},"weight":'${CURRENT_WEIGHT}'}]}]}}'

  # Wait and check metrics
  echo "Monitoring metrics for ${CHECK_INTERVAL}s..."
  sleep $CHECK_INTERVAL

  # Check error rate
  ERROR_RATE=$(kubectl exec -it deployment/${DEPLOYMENT}-canary -n "$NAMESPACE" -- \
    curl -s http://localhost:8080/metrics | grep http_requests_total | \
    awk '{print $2}' || echo "0")

  if (( $(echo "$ERROR_RATE > $MAX_ERROR_RATE" | bc -l) )); then
    echo "ERROR: Error rate exceeded threshold: $ERROR_RATE"
    echo "Rolling back canary deployment..."
    kubectl patch virtualservice ${DEPLOYMENT} -n "$NAMESPACE" --type merge \
      -p '{"spec":{"http":[{"route":[{"destination":{"host":"'${DEPLOYMENT}-stable'"},"weight":100}]}]}}'
    exit 1
  fi

  CURRENT_WEIGHT=$((CURRENT_WEIGHT + STEP_WEIGHT))
done

# Promote canary to stable
echo "Canary deployment successful! Promoting to stable..."
kubectl set image deployment/${DEPLOYMENT} \
  ${DEPLOYMENT}=myrepo/${DEPLOYMENT}:${NEW_VERSION} \
  -n "$NAMESPACE"

kubectl rollout status deployment/${DEPLOYMENT} -n "$NAMESPACE" --timeout=5m

echo "Canary deployment complete!"
```

### 3. **Metrics-Based Canary Analysis**

```yaml
# canary-monitoring.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: canary-analysis
  namespace: production
data:
  analyze.sh: |
    #!/bin/bash
    set -euo pipefail

    CANARY_DEPLOYMENT="${1:-myapp-canary}"
    STABLE_DEPLOYMENT="${2:-myapp-stable}"
    THRESHOLD="${3:-0.05}"  # 5% error rate threshold
    NAMESPACE="production"

    echo "Analyzing canary metrics..."

    # Query Prometheus for metrics
    CANARY_ERROR_RATE=$(curl -s 'http://prometheus:9090/api/v1/query' \
      --data-urlencode 'query=rate(http_requests_total{status=~"5..",deployment="'${CANARY_DEPLOYMENT}'"}[5m])' | \
      jq -r '.data.result[0].value[1]' || echo "0")

    STABLE_ERROR_RATE=$(curl -s 'http://prometheus:9090/api/v1/query' \
      --data-urlencode 'query=rate(http_requests_total{status=~"5..",deployment="'${STABLE_DEPLOYMENT}'"}[5m])' | \
      jq -r '.data.result[0].value[1]' || echo "0")

    CANARY_LATENCY=$(curl -s 'http://prometheus:9090/api/v1/query' \
      --data-urlencode 'query=histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{deployment="'${CANARY_DEPLOYMENT}'"}[5m]))' | \
      jq -r '.data.result[0].value[1]' || echo "0")

    STABLE_LATENCY=$(curl -s 'http://prometheus:9090/api/v1/query' \
      --data-urlencode 'query=histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{deployment="'${STABLE_DEPLOYMENT}'"}[5m]))' | \
      jq -r '.data.result[0].value[1]' || echo "0")

    echo "Canary Error Rate: $CANARY_ERROR_RATE"
    echo "Stable Error Rate: $STABLE_ERROR_RATE"
    echo "Canary P95 Latency: ${CANARY_LATENCY}s"
    echo "Stable P95 Latency: ${STABLE_LATENCY}s"

    # Check if canary is within acceptable range
    if (( $(echo "$CANARY_ERROR_RATE > $THRESHOLD" | bc -l) )); then
      echo "FAIL: Canary error rate exceeds threshold"
      exit 1
    fi

    if (( $(echo "$CANARY_LATENCY > $STABLE_LATENCY * 1.2" | bc -l) )); then
      echo "FAIL: Canary latency is 20% higher than stable"
      exit 1
    fi

    echo "PASS: Canary meets quality criteria"
    exit 0

---
apiVersion: batch/v1
kind: Job
metadata:
  name: canary-analysis
  namespace: production
spec:
  template:
    spec:
      containers:
        - name: analyzer
          image: curlimages/curl:latest
          command:
            - sh
            - -c
            - |
              apk add --no-cache bc jq
              bash /scripts/analyze.sh
          volumeMounts:
            - name: scripts
              mountPath: /scripts
      volumes:
        - name: scripts
          configMap:
            name: canary-analysis
      restartPolicy: Never
```

### 4. **Automated Canary Promotion**

```bash
#!/bin/bash
# promote-canary.sh - Automatically promote successful canary

set -euo pipefail

NAMESPACE="${1:-production}"
DEPLOYMENT="${2:-myapp}"
MAX_DURATION="${3:-600}"  # Max 10 minutes for canary

start_time=$(date +%s)

echo "Starting automated canary promotion for $DEPLOYMENT"

while true; do
  current_time=$(date +%s)
  elapsed=$((current_time - start_time))

  if [ $elapsed -gt $MAX_DURATION ]; then
    echo "ERROR: Canary exceeded max duration"
    exit 1
  fi

  # Check canary health
  CANARY_REPLICAS=$(kubectl get deployment ${DEPLOYMENT}-canary -n "$NAMESPACE" \
    -o jsonpath='{.status.readyReplicas}')
  CANARY_DESIRED=$(kubectl get deployment ${DEPLOYMENT}-canary -n "$NAMESPACE" \
    -o jsonpath='{.spec.replicas}')

  if [ "$CANARY_REPLICAS" -ne "$CANARY_DESIRED" ]; then
    echo "Waiting for canary pods to be ready..."
    sleep 10
    continue
  fi

  # Run analysis
  if bash /scripts/analyze.sh "$DEPLOYMENT-canary" "$DEPLOYMENT-stable"; then
    echo "Canary analysis passed! Promoting to stable..."

    # Merge canary into stable
    kubectl set image deployment/${DEPLOYMENT} \
      ${DEPLOYMENT}=myrepo/${DEPLOYMENT}:$(kubectl get deployment ${DEPLOYMENT}-canary -n "$NAMESPACE" \
        -o jsonpath='{.spec.template.spec.containers[0].image}' | cut -d: -f2) \
      -n "$NAMESPACE"

    kubectl rollout status deployment/${DEPLOYMENT} -n "$NAMESPACE" --timeout=5m

    echo "Canary promoted successfully!"
    exit 0
  else
    echo "Canary analysis failed. Rolling back..."
    exit 1
  fi
done
```

## Canary Best Practices

### ✅ DO
- Start with small traffic percentage (5-10%)
- Monitor key metrics continuously
- Increase gradually based on metrics
- Implement automatic rollback
- Run load tests on canary
- Test with real user traffic
- Set appropriate thresholds
- Document rollback procedures

### ❌ DON'T
- Rush through canary phases
- Ignore metrics
- Mix canary and stable versions
- Deploy to all users at once
- Skip rollback testing
- Use artificial load only
- Set unrealistic thresholds
- Deploy unvalidated changes

## Metrics to Monitor

- **Error Rate**: 5xx errors increase
- **Latency**: P95/P99 response time
- **Throughput**: Requests per second
- **Resource Usage**: CPU, memory
- **Business Metrics**: Conversion rate, revenue
- **User Experience**: Session duration, bounce rate

## Resources

- [Flagger Canary Deployments](https://flagger.app/)
- [Istio Traffic Management](https://istio.io/latest/docs/concepts/traffic-management/)
- [Kubernetes Canary Pattern](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy)
