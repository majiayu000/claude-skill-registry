---
name: deployment-guide
description: Эксперт по deployment документации. Используй для гайдов по деплою, CI/CD и release processes.
---

# Deployment Guide Creator

Эксперт по созданию production-ready документации для деплоя.

## Core Principles

### Structure & Organization
- Prerequisites listed first
- Environment-specific instructions
- Verification steps after each phase
- Rollback procedures documented
- Operational readiness covered

### Documentation Standards
- Imperative tone for instructions
- Exact commands with expected outputs
- Version specifications for all tools
- Context explaining why each step matters
- Estimated execution times per phase

## Standard Guide Structure

```markdown
# Deployment Guide: [Application Name]

## Overview
- Application description
- Deployment strategy (blue-green, rolling, canary)
- Architecture diagram
- Key contacts

## Prerequisites

### System Requirements
- OS: Ubuntu 22.04 LTS
- RAM: 8GB minimum
- Disk: 50GB SSD
- Network: 100Mbps

### Required Tools
| Tool | Version | Purpose |
|------|---------|---------|
| Docker | 24.0+ | Containerization |
| kubectl | 1.28+ | Kubernetes CLI |
| Helm | 3.12+ | Package management |

### Access Requirements
- [ ] SSH access to jump server
- [ ] Kubernetes cluster credentials
- [ ] Container registry credentials
- [ ] Secrets management access

### Security Checklist
- [ ] VPN connection established
- [ ] MFA configured
- [ ] SSH keys rotated (< 90 days)
```

## Pre-Deployment Checklist

```markdown
## Pre-Deployment Checklist

### Code Readiness
- [ ] All tests passing in CI
- [ ] Code review approved
- [ ] Security scan completed
- [ ] Documentation updated

### Environment Checks
- [ ] Target cluster healthy
- [ ] Database backups verified
- [ ] Monitoring alerts silenced
- [ ] Maintenance window scheduled

### Rollback Preparation
- [ ] Previous version tagged
- [ ] Rollback procedure tested
- [ ] Data migration reversible
- [ ] Communication plan ready
```

## Deployment Phases

### Phase 1: Infrastructure Prep

```bash
# Estimated time: 10 minutes

# 1. Verify cluster connectivity
kubectl cluster-info
# Expected: Kubernetes control plane is running

# 2. Check node readiness
kubectl get nodes
# Expected: All nodes in "Ready" state

# 3. Verify namespace exists
kubectl get namespace production
# If not exists:
kubectl create namespace production
```

### Phase 2: Application Deployment

```bash
# Estimated time: 15 minutes

# 1. Pull latest configuration
git pull origin main
cd deployment/kubernetes

# 2. Update image tag in values
export IMAGE_TAG=v1.2.3
sed -i "s/tag: .*/tag: ${IMAGE_TAG}/" values.yaml

# 3. Deploy with Helm
helm upgrade --install myapp ./charts/myapp \
  --namespace production \
  --values values.yaml \
  --wait \
  --timeout 10m

# Expected output:
# Release "myapp" has been upgraded. Happy Helming!
```

### Phase 3: Database Migration

```bash
# Estimated time: 5-30 minutes (depends on data size)

# 1. Create backup before migration
kubectl exec -n production deploy/myapp -- \
  pg_dump -Fc > backup_$(date +%Y%m%d_%H%M%S).dump

# 2. Run migrations
kubectl exec -n production deploy/myapp -- \
  npm run migrate

# 3. Verify migration status
kubectl exec -n production deploy/myapp -- \
  npm run migrate:status
```

## Kubernetes Deployment Example

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  namespace: production
  labels:
    app: myapp
    version: v1.2.3
spec:
  replicas: 3
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
    spec:
      containers:
        - name: myapp
          image: registry.example.com/myapp:v1.2.3
          ports:
            - containerPort: 8080
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: NODE_ENV
              value: "production"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-url
```

## Post-Deployment Verification

```markdown
## Verification Checklist

### Health Checks
- [ ] All pods running: `kubectl get pods -n production`
- [ ] Endpoints healthy: `curl -s https://api.example.com/health`
- [ ] Database connected: Check application logs

### Performance Validation
- [ ] Response time < 200ms (p95)
- [ ] Error rate < 0.1%
- [ ] Memory usage stable

### Security Checks
- [ ] TLS certificates valid
- [ ] No sensitive data in logs
- [ ] Rate limiting active
```

### Verification Script

```bash
#!/bin/bash
# verify-deployment.sh

echo "=== Deployment Verification ==="

# Check pod status
echo "Checking pods..."
READY_PODS=$(kubectl get pods -n production -l app=myapp \
  -o jsonpath='{.items[*].status.containerStatuses[0].ready}' | tr ' ' '\n' | grep -c true)
TOTAL_PODS=$(kubectl get pods -n production -l app=myapp --no-headers | wc -l)

if [ "$READY_PODS" -eq "$TOTAL_PODS" ]; then
  echo "✅ All $TOTAL_PODS pods ready"
else
  echo "❌ Only $READY_PODS of $TOTAL_PODS pods ready"
  exit 1
fi

# Check endpoints
echo "Checking health endpoint..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://api.example.com/health)
if [ "$HTTP_CODE" -eq 200 ]; then
  echo "✅ Health endpoint returning 200"
else
  echo "❌ Health endpoint returning $HTTP_CODE"
  exit 1
fi

# Check logs for errors
echo "Checking for errors in logs..."
ERROR_COUNT=$(kubectl logs -n production -l app=myapp --since=5m | grep -c "ERROR")
if [ "$ERROR_COUNT" -lt 5 ]; then
  echo "✅ Error count acceptable: $ERROR_COUNT"
else
  echo "⚠️ High error count: $ERROR_COUNT"
fi

echo "=== Verification Complete ==="
```

## Rollback Procedures

### Automatic Rollback Triggers
- Health check failures > 3 consecutive
- Error rate > 5% for 5 minutes
- P99 latency > 2 seconds for 5 minutes

### Manual Rollback Steps

```bash
# Estimated time: 5 minutes

# 1. Identify previous release
helm history myapp -n production

# 2. Rollback to previous version
helm rollback myapp [REVISION] -n production --wait

# 3. Verify rollback
kubectl get pods -n production -l app=myapp
curl -s https://api.example.com/health

# 4. If database migration needs reversal
kubectl exec -n production deploy/myapp -- \
  npm run migrate:down
```

### Data Recovery

```bash
# Restore from backup if needed
kubectl exec -n production deploy/myapp -- \
  pg_restore -d myapp_production backup_20240101_120000.dump
```

## Troubleshooting

### Common Issues

```markdown
## Issue: Pods stuck in ImagePullBackOff

**Symptoms:**
- Pods show ImagePullBackOff status
- Events show "Failed to pull image"

**Resolution:**
1. Verify image exists: `docker pull registry.example.com/myapp:v1.2.3`
2. Check registry credentials: `kubectl get secret regcred -n production`
3. Recreate secret if needed:
   ```bash
   kubectl create secret docker-registry regcred \
     --docker-server=registry.example.com \
     --docker-username=user \
     --docker-password=pass \
     -n production
   ```

## Issue: Health checks failing

**Symptoms:**
- Pods restarting frequently
- Readiness probe failures in events

**Resolution:**
1. Check application logs: `kubectl logs -n production deploy/myapp`
2. Verify environment variables: `kubectl exec -n production deploy/myapp -- env`
3. Test health endpoint manually: `kubectl port-forward deploy/myapp 8080:8080`
4. Increase probe timeouts if startup is slow
```

### Log Locations

```markdown
| Log Type | Location | Command |
|----------|----------|---------|
| Application | Pod stdout | `kubectl logs deploy/myapp` |
| Ingress | Ingress controller | `kubectl logs -n ingress deploy/nginx` |
| Events | Kubernetes events | `kubectl get events -n production` |
| Audit | Cluster audit logs | `/var/log/kubernetes/audit.log` |
```

### Emergency Contacts

```markdown
| Role | Name | Contact |
|------|------|---------|
| On-call Engineer | PagerDuty | #ops-escalation |
| Database Admin | DBA Team | dba@example.com |
| Security | Security Team | security@example.com |
```

## CI/CD Integration

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy with Helm
        run: |
          helm upgrade --install myapp ./charts/myapp \
            --namespace production \
            --set image.tag=${{ github.ref_name }} \
            --wait \
            --timeout 10m

      - name: Verify deployment
        run: ./scripts/verify-deployment.sh

      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {"text": "⚠️ Deployment failed for ${{ github.ref_name }}"}
```

## Лучшие практики

1. **Test rollback** — регулярно тестируйте процедуры отката
2. **Incremental deploys** — начинайте с малого % трафика
3. **Feature flags** — разделяйте deploy и release
4. **Monitoring first** — настройте мониторинг до деплоя
5. **Document everything** — все шаги должны быть воспроизводимы
6. **Automate verification** — скрипты вместо ручных проверок
