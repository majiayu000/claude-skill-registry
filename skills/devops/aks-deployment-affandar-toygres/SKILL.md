---
name: aks-deployment
description: Deploying and debugging Toygres on AKS (Azure Kubernetes Service). Use when deploying, debugging pods, viewing logs, troubleshooting SSL, or managing Kubernetes resources.
---

# AKS Deployment & Debugging

## Deployment

```bash
# Full deploy with HTTPS
./deploy/deploy-to-aks.sh --https

# Just restart to pick up new images
kubectl rollout restart deployment/toygres-server -n toygres-system
kubectl rollout status deployment/toygres-server -n toygres-system
```

## Viewing Logs

```bash
# Server logs
kubectl logs -n toygres-system -l app.kubernetes.io/component=server -f

# UI logs
kubectl logs -n toygres-system -l app.kubernetes.io/component=ui -f

# Previous crashed pod
kubectl logs -n toygres-system <pod-name> --previous
```

## Pod Management

```bash
# List pods
kubectl get pods -n toygres-system

# Describe pod (see events, errors)
kubectl describe pod <pod-name> -n toygres-system

# Exec into pod
kubectl exec -it <pod-name> -n toygres-system -- /bin/sh

# Delete pod (will restart)
kubectl delete pod <pod-name> -n toygres-system
```

## Common Issues

### Pod CrashLoopBackOff
```bash
# Check logs for crash reason
kubectl logs <pod-name> -n toygres-system --previous

# Common causes:
# - DATABASE_URL not set or wrong
# - Missing secrets
# - Port already in use
```

### Image Not Updating
```bash
# Force pull latest image
kubectl rollout restart deployment/toygres-server -n toygres-system

# Or delete pod directly
kubectl delete pod -n toygres-system -l app.kubernetes.io/component=server
```

### SSL Certificate Issues
```bash
# Check cert-manager
kubectl get certificate -n toygres-system
kubectl describe certificate toygres-tls -n toygres-system

# Check ingress
kubectl get ingress -n toygres-system
kubectl describe ingress toygres-ingress -n toygres-system
```

### Azure Workload Identity / azcopy 403 Errors

If `azcopy login --identity` succeeds but operations fail with 403 AuthorizationPermissionMismatch:

**Root cause:** `azcopy --identity` uses VM-based managed identity (IMDS), not AKS workload identity.

**Fix:** Use `--login-type=workload` explicitly:
```bash
# Wrong (uses IMDS, fails on AKS)
azcopy login --identity

# Correct (uses federated token)
azcopy login --login-type=workload
```

**Debug workload identity:**
```bash
# Check env vars are injected
kubectl exec <pod> -- env | grep AZURE_

# Should see:
# AZURE_CLIENT_ID=...
# AZURE_TENANT_ID=...
# AZURE_FEDERATED_TOKEN_FILE=/var/run/secrets/azure/tokens/azure-identity-token

# Test with az cli (uses federated token correctly)
az login --federated-token "$(cat $AZURE_FEDERATED_TOKEN_FILE)" \
  --service-principal -u $AZURE_CLIENT_ID -t $AZURE_TENANT_ID
az storage blob list --account-name <acct> --container-name <container> --auth-mode login
```

### Azure LoadBalancer DNS Propagation

**Problem:** Instance provisioning fails at test_connection even though service is created.

**Root cause:** Azure DNS propagation for LoadBalancer services takes 60-90+ seconds after IP is assigned.

**Timeline:**
1. LoadBalancer created → IP assigned (10-30s)
2. DNS record created → DNS propagates (30-60+ additional seconds)
3. Total wait time can be 60-90+ seconds

**Fix:** Use 120s timeout for connection tests, not 60s:

```rust
// In orchestrations
RetryPolicy::new(5)
    .with_timeout(Duration::from_secs(120)) // Not 60s!
```

**Debug DNS propagation:**
```bash
# Check if service has external IP
kubectl get svc -n toygres-managed <svc-name>

# Test DNS resolution
nslookup <dns-label>.westus2.cloudapp.azure.com

# Watch for IP assignment
kubectl get svc -n toygres-managed -w
```

## Local Testing Before Deploy

```bash
# Pause AKS server
kubectl scale deployment toygres-server -n toygres-system --replicas=0

# Run locally
./scripts/start-control-plane.sh

# Test at http://localhost:3000

# Resume AKS
kubectl scale deployment toygres-server -n toygres-system --replicas=1
```
