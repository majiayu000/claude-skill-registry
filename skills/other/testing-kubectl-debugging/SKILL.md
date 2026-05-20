---
name: testing:kubectl-debugging
description: Common kubectl commands for debugging Kagenti components
---

# Kubectl Debugging Patterns

Common kubectl commands for debugging Kagenti components.

## Table of Contents

- [Setting Up Environment](#setting-up-environment)
- [Helm Debugging](#helm-debugging)
- [ConfigMap and Secret Inspection](#configmap-and-secret-inspection)
- [Pod Debugging](#pod-debugging)
- [Service Debugging](#service-debugging)
- [Keycloak Client Verification](#keycloak-client-verification)
- [Job Debugging](#job-debugging)
- [Istio Debugging](#istio-debugging)
- [Events](#events)
- [Quick Reference](#quick-reference)

## Setting Up Environment

### Using Correct Kubeconfig

```bash
# HyperShift cluster
export KUBECONFIG=~/clusters/hcp/kagenti-hypershift-custom-mlflow/auth/kubeconfig

# Kind cluster
export KUBECONFIG=~/.kube/config
kubectl config use-context kind-kagenti
```

### Verify Connection

```bash
kubectl cluster-info
kubectl get nodes
```

## Helm Debugging

### Check Rendered Values

```bash
helm get values kagenti-deps -n kagenti-system
```

### Check All Values (Including Defaults)

```bash
helm get values kagenti-deps -n kagenti-system -a
```

### Template Without Installing

```bash
helm template kagenti-deps charts/kagenti-deps -n kagenti-system \
  -f /tmp/values.yaml > /tmp/rendered.yaml
```

### Check Release Status

```bash
helm list -n kagenti-system
helm history kagenti-deps -n kagenti-system
```

## ConfigMap and Secret Inspection

### Extract ConfigMap Content

```bash
kubectl get configmap otel-collector-config -n kagenti-system -o yaml
```

### Extract Specific Key

```bash
kubectl get configmap otel-collector-config -n kagenti-system \
  -o jsonpath='{.data.otel-collector-config\.yaml}'
```

### Decode Secret

```bash
kubectl get secret mlflow-oauth-secret -n kagenti-system \
  -o jsonpath='{.data.MLFLOW_CLIENT_ID}' | base64 -d
```

### List All Secret Keys

```bash
kubectl get secret mlflow-oauth-secret -n kagenti-system \
  -o jsonpath='{.data}' | jq 'keys'
```

## Pod Debugging

### Check Pod Environment Variables

```bash
kubectl get pod otel-collector-xxx -n kagenti-system \
  -o jsonpath='{.spec.containers[0].env}' | jq
```

### Check Pod Status

```bash
kubectl describe pod otel-collector-xxx -n kagenti-system
```

### Get Pod Logs

```bash
kubectl logs -n kagenti-system otel-collector-xxx
kubectl logs -n kagenti-system otel-collector-xxx --previous  # After crash
kubectl logs -n kagenti-system otel-collector-xxx -f          # Follow
```

### Exec Into Pod

```bash
kubectl exec -it otel-collector-xxx -n kagenti-system -- /bin/sh
```

### Check Mounted Files

```bash
kubectl exec -it otel-collector-xxx -n kagenti-system -- \
  ls -la /etc/pki/ca-trust/extracted/pem/
```

## Service Debugging

### Check Service Endpoints

```bash
kubectl get endpoints mlflow -n kagenti-system
```

### Check Service Labels

```bash
kubectl get svc mlflow -n kagenti-system --show-labels
```

### Port Forward

```bash
kubectl port-forward svc/mlflow 5000:5000 -n kagenti-system
```

## Keycloak Client Verification

### Get Token

```bash
# Set variables
KEYCLOAK_URL="http://keycloak-service.keycloak.svc.cluster.local:8080"
CLIENT_ID="mlflow-client"
CLIENT_SECRET=$(kubectl get secret mlflow-oauth-secret -n kagenti-system \
  -o jsonpath='{.data.MLFLOW_CLIENT_SECRET}' | base64 -d)

# Get token
curl -X POST "$KEYCLOAK_URL/realms/master/protocol/openid-connect/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET"
```

### Test From Inside Cluster

```bash
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl -X POST "http://keycloak-service.keycloak.svc.cluster.local:8080/realms/master/protocol/openid-connect/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=mlflow-client" \
  -d "client_secret=<secret>"
```

## Job Debugging

### Check Job Status

```bash
kubectl get jobs -n keycloak
kubectl describe job mlflow-oauth-secret -n keycloak
```

### Get Job Pod Logs

```bash
kubectl logs -n keycloak -l job-name=mlflow-oauth-secret
```

### Rerun Failed Job

```bash
kubectl delete job mlflow-oauth-secret -n keycloak
# Job will be recreated by Helm if still in chart
```

## Istio Debugging

### Check Waypoint Status

```bash
kubectl get gateway -n kagenti-system
kubectl describe gateway mlflow-waypoint -n kagenti-system
```

### Check AuthorizationPolicy

```bash
kubectl get authorizationpolicy -n kagenti-system
kubectl describe authorizationpolicy mlflow-traces-from-otel -n kagenti-system
```

### Check Pod Identity

```bash
istioctl proxy-config secret otel-collector-xxx -n kagenti-system
```

### Check ztunnel Logs

```bash
kubectl logs -n istio-system -l app=ztunnel --tail=100
```

## Events

### Namespace Events

```bash
kubectl get events -n kagenti-system --sort-by='.lastTimestamp'
```

### Pod Events

```bash
kubectl get events -n kagenti-system --field-selector involvedObject.name=otel-collector-xxx
```

## Resource Usage

### Pod Resources

```bash
kubectl top pods -n kagenti-system
```

### Describe Resource Limits

```bash
kubectl get pod otel-collector-xxx -n kagenti-system \
  -o jsonpath='{.spec.containers[0].resources}'
```

## Quick Reference

| Task | Command |
|------|---------|
| Get all pods | `kubectl get pods -n kagenti-system` |
| Get logs | `kubectl logs -n kagenti-system <pod>` |
| Describe pod | `kubectl describe pod -n kagenti-system <pod>` |
| Exec shell | `kubectl exec -it <pod> -n kagenti-system -- /bin/sh` |
| Port forward | `kubectl port-forward svc/<svc> <port>:<port> -n kagenti-system` |
| Get events | `kubectl get events -n kagenti-system --sort-by='.lastTimestamp'` |
| Helm values | `helm get values kagenti-deps -n kagenti-system` |

## Related Skills

- `tdd:hypershift`
- `k8s:live-debugging`
- `istio:ambient-waypoint`
