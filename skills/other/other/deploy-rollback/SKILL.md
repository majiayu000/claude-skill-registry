---
name: deploy__rollback
description: Rollback a failed deployment to the previous working version. Use this when a deployment causes issues in Azure or Kubernetes.
---

Use this guide to rollback a failed deployment to restore service quickly.

## Related Skills

**Prerequisites**:
- You must have deployed using one of:
  - `/deploy__azure_container_apps` - Azure Container Apps
  - `/deploy__kubernetes_cluster` - Kubernetes cluster

**Debugging**:
- `/frontend__debug_sse` - If rollback was due to SSE issues
- `/cache__debug_cache` - If rollback was due to caching issues
- `/ops__doctor_check` - Check environment after rollback

**Verification**:
- `/test__verify_feature` - Verify application health after rollback

## When to Rollback

- ✗ Application crashes after deployment
- ✗ Critical functionality broken
- ✗ Performance degradation
- ✗ Database migration failure
- ✗ Unacceptable user-facing errors

## Azure Deployment Rollback

### Using Azure Developer CLI (azd)

```bash
# View deployment history
azd show

# Get previous deployment details
az deployment group list \
  --resource-group <rg-name> \
  --query "[].{name:name, timestamp:properties.timestamp, state:properties.provisioningState}" \
  --output table

# Rollback to previous deployment
# Note: azd doesn't have direct rollback, deploy previous version instead

# Get previous version tag
git log --oneline -n 10

# Checkout previous version
git checkout <previous-commit>

# Deploy previous version
azd up
```

### Using Azure Portal

1. Navigate to Azure Container Apps
2. Select the BookStore API or Web app
3. Go to "Revisions"
4. Find the last working revision
5. Click "Activate" on the previous revision
6. Deactivate the failing revision

### Using Azure CLI

```bash
# List revisions for API service
az containerapp revision list \
  --name bookstore-api \
  --resource-group <rg-name> \
  --query "[].{name:name, active:properties.active, created:properties.createdTime}" \
  --output table

# Activate previous revision
az containerapp revision activate \
  --name bookstore-api \
  --resource-group <rg-name> \
  --revision <previous-revision-name>

# Deactivate current (failing) revision
az containerapp revision deactivate \
  --name bookstore-api \
  --resource-group <rg-name> \
  --revision <current-revision-name>

# Repeat for Web frontend
az containerapp revision activate \
  --name bookstore-web \
  --resource-group <rg-name> \
  --revision <previous-revision-name>
```

## Kubernetes Deployment Rollback

### Using kubectl Rollback Command

```bash
# Check rollout status
kubectl rollout status deployment/bookstore-api
kubectl rollout status deployment/bookstore-web

# View rollout history
kubectl rollout history deployment/bookstore-api
kubectl rollout history deployment/bookstore-web

# Rollback to previous version
kubectl rollout undo deployment/bookstore-api
kubectl rollout undo deployment/bookstore-web

# Rollback to specific revision
kubectl rollout undo deployment/bookstore-api --to-revision=2

# Watch rollback progress
kubectl rollout status deployment/bookstore-api -w
```

### Manual Rollback (Image Tag)

```bash
# Get current image
kubectl get deployment bookstore-api -o jsonpath='{.spec.template.spec.containers[0].image}'

# Set to previous image tag
kubectl set image deployment/bookstore-api \
  bookstore-api=<registry>/bookstore-api:v1.0.0

# Or edit deployment directly
kubectl edit deployment bookstore-api
# Change image tag in the spec, save and exit

# Verify pods are restarting
kubectl get pods -w
```

### Using Helm (if using Helm charts)

```bash
# List releases
helm list

# View history
helm history bookstore

# Rollback to previous release
helm rollback bookstore

# Rollback to specific version
helm rollback bookstore 2
```

## Database Migration Rollback

If the deployment included database migrations:

### Marten Projection Rollback

```bash
# Connect to database
kubectl exec -it deployment/bookstore-api -- bash

# Or from local with port-forward
kubectl port-forward service/postgres 5432:5432

# Connect to PostgreSQL
psql -h localhost -U postgres -d bookstore

# Check projection versions
SELECT name, status, position FROM mt_projections;

# Stop async projections if needed
# (handled programmatically or restart pods)
```

**For breaking schema changes**:
1. Deploy database-compatible version first
2. Run migration forward
3. Deploy new application version
4. **Never rollback migrations** - deploy a new "forward" migration

### Manual Migration Rollback (Emergency Only)

```sql
-- ⚠️ DANGEROUS - Only if absolutely necessary
BEGIN;

-- Reverse the migration manually
DROP TABLE IF EXISTS new_table;
-- Restore previous state...

-- Verify
SELECT * FROM mt_events LIMIT 5;

COMMIT;  -- Or ROLLBACK if issues
```

## Verification After Rollback

### Health Checks

```bash
# Azure Container Apps
az containerapp show \
  --name bookstore-api \
  --resource-group <rg-name> \
  --query "properties.configuration.ingress.fqdn"

curl https://<fqdn>/health

# Kubernetes
kubectl get pods
kubectl get services

# Get external IP
kubectl get service bookstore-web-lb

curl http://<external-ip>/health
```

### Application Verification

```bash
# Test critical endpoints
curl https://<host>/api/books
curl https://<host>/api/authors

# Check logs for errors
# Azure
az containerapp logs show \
  --name bookstore-api \
  --resource-group <rg-name> \
  --tail 50

# Kubernetes
kubectl logs -l app=bookstore-api --tail=50
```

### Monitor Metrics

```bash
# Azure - Application Insights
# View in Azure Portal → Application Insights → Failures

# Kubernetes
kubectl top pods
kubectl top nodes

# Check for errors
kubectl get events --sort-by=.metadata.creationTimestamp | grep -i error
```

## Rollback Communication

After rollback, communicate with stakeholders:

1. **Status Update**:
   - Service has been rolled back to previous stable version
   - Current version: `<tag>`
   - Rollback reason: `<description>`

2. **Impact Assessment**:
   - Downtime duration: `<X minutes>`
   - Affected features: `<list>`
   - Data integrity: `Verified/Investigating`

3. **Next Steps**:
   - Root cause analysis scheduled
   - Fix being developed
   - New deployment planned for: `<datetime>`

## Post-Rollback Actions

### 1. Identify Root Cause

```bash
# Review deployment logs
# Azure
az containerapp logs show --name bookstore-api -g <rg> --tail 200 > rollback-logs.txt

# Kubernetes
kubectl logs -l app=bookstore-api --previous > rollback-logs.txt

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp > events.txt

# Analyze
grep -i error rollback-logs.txt
grep -i exception rollback-logs.txt
```

### 2. Document the Incident

Create incident report:
- Deployment timestamp
- First error detected
- Rollback initiated
- Service restored
- Root cause
- Prevention measures

### 3. Fix and Redeploy

```bash
# Create hotfix branch
git checkout -b hotfix/deployment-issue

# Apply fix
# ... code changes ...

# Test locally
dotnet test

# Test in staging environment
azd deploy --environment staging

# Verify fix
curl https://staging.bookstore.com/health

# Deploy to production
azd deploy --environment production

# Monitor closely
watch kubectl get pods
```

## Preventing Rollbacks

### Blue-Green Deployment

```bash
# Deploy new version alongside old
kubectl apply -f deploy/k8s/deployments-v2.yaml

# Test new version
kubectl port-forward deployment/bookstore-api-v2 8080:80

# Switch traffic gradually
kubectl patch service bookstore-api -p '{"spec":{"selector":{"version":"v2"}}}'

# If issues, switch back immediately
kubectl patch service bookstore-api -p '{"spec":{"selector":{"version":"v1"}}}'
```

### Canary Deployment

```bash
# Deploy canary with 10% traffic
# (requires service mesh like Istio or Linkerd)

# Monitor canary metrics
# If errors increase, rollback canary
# If stable, increase to 50%, then 100%
```

### Health Checks

Ensure proper health checks:

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 80
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health
    port: 80
  initialDelaySeconds: 5
  periodSeconds: 5
```

## Emergency Contacts

- **DevOps Lead**: [Contact]
- **Database Admin**: [Contact]
- **On-Call Engineer**: [PagerDuty/etc]

## Rollback Checklist

Before rolling back:
- [ ] Confirm deployment is actually failing (not transient)
- [ ] Check if auto-scaling or restart might resolve
- [ ] Identify last known good version
- [ ] Verify rollback won't cause data loss
- [ ] Notify team of pending rollback

During rollback:
- [ ] Execute rollback commands
- [ ] Monitor health checks
- [ ] Verify critical functionality
- [ ] Check database integrity
- [ ] Monitor error rates

After rollback:
- [ ] Notify stakeholders of restoration
- [ ] Collect logs and diagnostics
- [ ] Document incident
- [ ] Schedule post-mortem
- [ ] Plan fix and redeployment

## Related Skills

**Prerequisites**:
- You must have deployed using one of:
  - `/deploy__azure_container_apps` - Azure Container Apps
  - `/deploy__kubernetes_cluster` - Kubernetes cluster

**Debugging**:
- `/frontend__debug_sse` - If rollback was due to SSE issues
- `/cache__debug_cache` - If rollback was due to caching issues
- `/ops__doctor_check` - Check environment after rollback

**After Fix**:
- `/test__verify_feature` - Verify application health after rollback
- `/deploy__azure_container_apps` or `/deploy__kubernetes_cluster` - Redeploy fixed version

**See Also**:
- [aspire-deployment-guide](../../../docs/guides/aspire-deployment-guide.md) - Deployment documentation
- [aspire-guide](../../../docs/guides/aspire-guide.md) - Aspire orchestration
- AppHost AGENTS.md - Aspire orchestration configuration
