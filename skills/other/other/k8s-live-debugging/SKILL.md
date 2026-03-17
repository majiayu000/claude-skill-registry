---
name: k8s:live-debugging
description: Iterative debugging workflow for fixing issues on a running cluster
---

# Live Cluster Debugging Workflow

Iterative debugging workflow for fixing issues on a running HyperShift cluster.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Workflow](#workflow)
- [Common Debugging Scenarios](#common-debugging-scenarios)
- [Environment Variable Quick Reference](#environment-variable-quick-reference)
- [Useful One-Liners](#useful-one-liners)
- [After Debugging](#after-debugging)

## Overview

When tests fail on a deployed cluster, use this workflow to:
1. Diagnose the root cause
2. Make targeted fixes
3. Verify the fix without full redeployment

## Prerequisites

```bash
# Set the kubeconfig for your cluster
export KUBECONFIG=~/clusters/hcp/kagenti-hypershift-custom-<suffix>/auth/kubeconfig

# Verify connection
kubectl get nodes
```

## Workflow

### 1. Check Test Results

```bash
# View test results XML
cat test-results/e2e-results.xml

# Or re-run failing test with verbose output
pytest kagenti/tests/e2e/common/test_mlflow_traces.py -v -s
```

### 2. Check Pod Status

```bash
# Get all pods in relevant namespace
kubectl get pods -n kagenti-system

# Check specific component
kubectl get pods -n kagenti-system -l app=otel-collector

# Describe problematic pod
kubectl describe pod -n kagenti-system <pod-name>
```

### 3. Check Logs

```bash
# Get recent logs
kubectl logs -n kagenti-system deployment/otel-collector --tail=100

# Stream logs in real-time
kubectl logs -n kagenti-system deployment/otel-collector -f

# Filter for errors
kubectl logs -n kagenti-system deployment/otel-collector --tail=200 | grep -iE "(error|fail|403|401)"
```

### 4. Check Configuration

```bash
# View ConfigMap contents
kubectl get configmap otel-collector-config -n kagenti-system -o yaml

# Check Secret contents (decoded)
kubectl get secret mlflow-oauth-secret -n kagenti-system -o jsonpath='{.data.OIDC_CLIENT_ID}' | base64 -d

# View rendered Helm values
helm get values kagenti-deps -n kagenti-system > /tmp/kagenti-deps-values.yaml
cat /tmp/kagenti-deps-values.yaml
```

### 5. Check Authorization

```bash
# View AuthorizationPolicy
kubectl get authorizationpolicy -n kagenti-system -o yaml

# Check waypoint proxy
kubectl get gateway -n kagenti-system

# Check service labels
kubectl get svc mlflow -n kagenti-system -o yaml | grep -A5 labels
```

### 6. Make Chart Changes

```bash
# Edit the chart template
vim charts/kagenti-deps/templates/otel-collector.yaml

# Apply the change
helm upgrade kagenti-deps charts/kagenti-deps -n kagenti-system \
  -f /tmp/kagenti-deps-values.yaml
```

### 7. Restart Affected Pods

```bash
# Rollout restart to pick up ConfigMap changes
kubectl rollout restart deployment/otel-collector -n kagenti-system

# Wait for rollout to complete
kubectl rollout status deployment/otel-collector -n kagenti-system --timeout=60s
```

### 8. Generate Test Data

```bash
# Get route to weather service
ROUTE_HOST=$(kubectl get route weather-service -n team1 -o jsonpath='{.spec.host}')

# Send test request
curl -sk -X POST "https://$ROUTE_HOST/" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"message/send","params":{"message":{"messageId":"test-123","parts":[{"kind":"text","text":"What is the weather?"}],"role":"user"}}}'
```

### 9. Verify Fix

```bash
# Check logs after test request
kubectl logs -n kagenti-system deployment/otel-collector --tail=50

# Run the specific failing test
pytest kagenti/tests/e2e/common/test_mlflow_traces.py::test_mlflow_has_traces -v
```

## Common Debugging Scenarios

### OAuth/Authentication Issues

```bash
# Check if OAuth extension started
kubectl logs -n kagenti-system deployment/otel-collector | grep oauth2client

# Test token acquisition
KEYCLOAK_HOST=$(kubectl get route keycloak -n keycloak -o jsonpath='{.spec.host}')
CLIENT_ID=$(kubectl get secret mlflow-oauth-secret -n kagenti-system -o jsonpath='{.data.OIDC_CLIENT_ID}' | base64 -d)
CLIENT_SECRET=$(kubectl get secret mlflow-oauth-secret -n kagenti-system -o jsonpath='{.data.OIDC_CLIENT_SECRET}' | base64 -d)

curl -sk -X POST "https://$KEYCLOAK_HOST/realms/master/protocol/openid-connect/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET"
```

### Mesh/Istio Issues

```bash
# Check Istiod logs for authorization warnings
kubectl logs -n istio-system deployment/istiod --tail=100 | grep -i authorization

# Check if pods are in ambient mode
kubectl get pod -n kagenti-system -l app=otel-collector -o jsonpath='{.items[0].metadata.annotations}'

# Verify trust domain
kubectl get configmap istio -n istio-system -o jsonpath='{.data.mesh}' | grep trustDomain
```

### Trace Export Issues

```bash
# Add debug exporter to pipeline (in otel-collector.yaml)
# exporters: [ debug, otlphttp/mlflow ]

# Check debug output for traces
kubectl logs -n kagenti-system deployment/otel-collector | grep "Span #"

# Check for export errors
kubectl logs -n kagenti-system deployment/otel-collector | grep -i "drop\|error\|fail"
```

## Environment Variable Quick Reference

```bash
# Weather service check
kubectl get pod -n team1 -l app=weather-service -o jsonpath='{.items[0].spec.containers[0].env}' | jq

# OTEL collector environment
kubectl get pod -n kagenti-system -l app=otel-collector -o jsonpath='{.items[0].spec.containers[0].env}' | jq
```

## Useful One-Liners

```bash
# Get all routes
kubectl get routes -A

# Check all deployments ready
kubectl get deployments -n kagenti-system

# Watch pod status
watch kubectl get pods -n kagenti-system

# Quick port-forward for testing
kubectl port-forward -n kagenti-system svc/mlflow 5000:5000
```

## After Debugging

Once the fix is verified:

1. **Run full test suite**: `pytest kagenti/tests/e2e/ -v`
2. **Commit changes**: `git add -A && git commit -m "fix: <description>"`
3. **Document findings**: Update relevant skills or CLAUDE.md

## Related Skills

- `tdd:hypershift`
- `testing:kubectl-debugging`
