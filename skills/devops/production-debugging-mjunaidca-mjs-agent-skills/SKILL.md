---
name: production-debugging
description: Debug production issues in Kubernetes clusters. Use this skill when investigating 500 errors, missing functionality, silent failures, or service integration issues. Covers systematic log analysis, tracing requests across microservices, and common bug patterns.
---

# Production Debugging

Systematic approach to debugging production issues in Kubernetes microservice environments.

## When to Use

- Investigating HTTP 500 errors
- Debugging missing functionality (feature works locally, fails in production)
- Tracing requests across microservices
- Finding silent failures (no error, but wrong behavior)
- Service-to-service integration issues

## Debugging Methodology

### Step 1: Reproduce and Identify Symptoms

```bash
# What's the user seeing?
# - HTTP 500 error on /workers page
# - No reminder notifications
# - Data saved but logs show errors

# Document the symptom precisely before diving in
```

### Step 2: Check Logs Systematically

```bash
# Start with the failing service
kubectl logs deploy/<service-name> -n <namespace> --tail=100

# Filter for errors
kubectl logs deploy/<service-name> -n <namespace> --tail=200 | grep -i -E "(error|exception|fail|warn)"

# Check specific container in multi-container pod
kubectl logs deploy/<service-name> -n <namespace> -c <container-name> --tail=100

# Common containers:
# - main app container (e.g., "api", "web")
# - daprd (Dapr sidecar)
# - init containers (e.g., "wait-for-db")
```

### Step 3: Trace the Request Path

For microservice issues, trace the full request path:

```bash
# 1. Frontend → API
kubectl logs deploy/web-dashboard -n taskflow --tail=50

# 2. API processing
kubectl logs deploy/taskflow-api -n taskflow --tail=100 | grep -i "endpoint-name"

# 3. API → External service (e.g., Dapr, SSO)
kubectl logs deploy/taskflow-api -n taskflow -c daprd --tail=50

# 4. Downstream service
kubectl logs deploy/notification-service -n taskflow --tail=50
```

### Step 4: Analyze the Error

Common patterns to look for:

| Error Pattern | Likely Cause |
|---------------|--------------|
| `AttributeError: 'X' has no attribute 'Y'` | Model/schema mismatch |
| `404 Not Found` on internal call | Wrong endpoint URL |
| `greenlet_spawn has not been called` | Async SQLAlchemy pattern issue |
| `event_type: None` | Message format/unwrapping issue |
| Times off by hours | Timezone handling bug |

## Quick Commands

### Check All Services Status

```bash
kubectl get pods -n taskflow
kubectl get pods -n taskflow -o wide  # With node info
```

### Check Service Logs

```bash
# Main app logs
kubectl logs deploy/taskflow-api -n taskflow --tail=100

# Dapr sidecar logs
kubectl logs deploy/taskflow-api -n taskflow -c daprd --tail=100

# Follow logs in real-time
kubectl logs deploy/taskflow-api -n taskflow -f

# Logs from specific time
kubectl logs deploy/taskflow-api -n taskflow --since=5m
```

### Check Pod Events

```bash
kubectl describe pod <pod-name> -n taskflow
kubectl get events -n taskflow --sort-by='.lastTimestamp'
```

### Execute Commands in Pod

```bash
# Shell into pod
kubectl exec -it deploy/taskflow-api -n taskflow -- /bin/sh

# Run specific command
kubectl exec deploy/taskflow-api -n taskflow -- env | grep DATABASE
```

## Common Bug Patterns

### 1. Model/Schema Mismatch

**Symptom**: `AttributeError: 'Model' has no attribute 'field'`

**Debug**:
```bash
# Find the error
kubectl logs deploy/taskflow-api -n taskflow --tail=100 | grep -i "attribute"

# Check the model definition
grep -r "class Worker" apps/api/src/
```

**Fix**: Ensure code references match actual model fields.

### 2. Wrong Endpoint URL

**Symptom**: `404 Not Found` on internal service calls

**Debug**:
```bash
# Check what URL is being called
kubectl logs deploy/taskflow-api -n taskflow -c daprd --tail=100 | grep "404"

# Check what endpoints exist
kubectl exec deploy/taskflow-api -n taskflow -- curl localhost:8000/openapi.json | jq '.paths | keys'
```

**Fix**: Match the callback URL to what the service exposes.

### 3. Timezone Bugs

**Symptom**: Scheduled jobs fire at wrong times (hours off)

**Debug**:
```bash
# Check when job was scheduled vs when it should fire
kubectl logs deploy/taskflow-api -n taskflow | grep -i "scheduled"

# Compare times
# If local time 23:00 but scheduled for 23:00 UTC → timezone bug
```

**Fix**: Convert to UTC before storing/scheduling.

### 4. Message Format Issues

**Symptom**: Handler receives data but can't find expected fields

**Debug**:
```bash
# Add logging to see raw message
kubectl logs deploy/notification-service -n taskflow | grep -i "raw"

# Check message structure
# CloudEvent wraps payload in "data" field
```

**Fix**: Unwrap CloudEvent: `event = raw.get("data", raw)`

### 5. Async SQLAlchemy Errors

**Symptom**: `greenlet_spawn has not been called`

**Debug**:
```bash
# Find the line that crashes
kubectl logs deploy/notification-service -n taskflow | grep -A 20 "greenlet"
```

**Fix**: Add `await session.refresh(obj)` after commit before accessing attributes.

## Debugging Dapr Specifically

### Check Dapr Sidecar

```bash
# Dapr scheduler connection
kubectl logs deploy/taskflow-api -n taskflow -c daprd | grep -i "scheduler"

# Dapr API calls
kubectl logs deploy/taskflow-api -n taskflow -c daprd | grep "HTTP API Called"

# Dapr pub/sub
kubectl logs deploy/taskflow-api -n taskflow -c daprd | grep -i "publish"
```

### Check Dapr Subscriptions

```bash
# What subscriptions are registered?
kubectl exec deploy/notification-service -n taskflow -- curl localhost:8001/dapr/subscribe
```

### Test Dapr Pub/Sub

```bash
# Publish test event from inside cluster
kubectl exec deploy/taskflow-api -n taskflow -- curl -X POST \
  http://localhost:3500/v1.0/publish/taskflow-pubsub/test-topic \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

## Debugging Checklist

When investigating a production issue:

- [ ] Reproduce the issue (what exactly fails?)
- [ ] Check pod status (`kubectl get pods`)
- [ ] Check main app logs for errors
- [ ] Check sidecar logs (daprd, etc.)
- [ ] Trace request path across services
- [ ] Identify error pattern (see table above)
- [ ] Verify fix locally before deploying
- [ ] Deploy and verify in production

## CI/CD Integration

### Check Deployment Status

```bash
# GitHub Actions
gh run list --limit 5

# Check specific run
gh run view <run-id>

# Watch deployment
gh run watch
```

### Verify Deployment

```bash
# Check pod restart count (should be 0 for healthy pods)
kubectl get pods -n taskflow

# Check pod age (recent = just deployed)
kubectl get pods -n taskflow -o wide

# Verify new code is running
kubectl logs deploy/taskflow-api -n taskflow --tail=10 | head -5
```

## Prevention

### Add Logging at Key Points

```python
logger.info("[SERVICE] Received request: %s", request_summary)
logger.info("[SERVICE] Processing: step=%s, data=%s", step, safe_data)
logger.info("[SERVICE] Completed: result=%s", result_summary)
logger.error("[SERVICE] Failed: error=%s, context=%s", error, context)
```

### Include Correlation IDs

```python
import uuid

@router.post("/tasks")
async def create_task(request: Request):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    logger.info("[%s] Creating task", correlation_id)
    # ... processing ...
    logger.info("[%s] Task created: %d", correlation_id, task.id)
```

### Test Error Paths

```python
def test_handles_missing_field():
    """Ensure graceful handling of missing data."""
    response = client.post("/tasks", json={})  # Missing required field
    assert response.status_code == 422  # Not 500!
```
