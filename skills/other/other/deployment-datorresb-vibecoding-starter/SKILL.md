---
name: deployment
description: Safe, repeatable deployment strategies for applications across environments. Use when setting up deployment pipelines, deploying to production, planning deployment strategies, implementing rollback procedures, or zero-downtime deployments.
---

# Deployment Skill

## Core Principle

**Deploy early, deploy often, deploy safely. Automate everything.**

Deployment should be boring, predictable, and reversible. Every deployment should follow the same process, whether to development or production. Manual deployments are error-prone—automation is reliability.

---

## When to Use

Use this skill when:
- Setting up deployment pipelines for new applications
- Deploying changes to production environments
- Planning deployment strategies for complex systems
- Implementing zero-downtime deployment patterns
- Creating rollback procedures
- Troubleshooting failed deployments
- Migrating between deployment strategies
- Implementing continuous deployment workflows
- Setting up multi-environment deployments

---

## Deployment Strategies

### 1. Blue-Green Deployment

**Two identical environments, instant switch.**

```
┌─────────────┐     ┌─────────────┐
│    BLUE     │     │    GREEN    │
│  (Current)  │     │    (New)    │
│   v1.0      │     │    v1.1     │
└──────┬──────┘     └──────┬──────┘
       │                   │
       └────────┬──────────┘
                │
          ┌─────▼─────┐
          │   Router  │ ← Switch traffic instantly
          │           │
          └───────────┘
```

**Process:**
1. Deploy new version to Green environment
2. Test Green thoroughly (smoke tests, health checks)
3. Switch router/load balancer to Green
4. Monitor for issues
5. Keep Blue running as instant rollback option

**Benefits:**
- Zero downtime
- Instant rollback (switch back to Blue)
- Full testing before traffic switch
- Clean separation between versions

**Drawbacks:**
- Requires 2x infrastructure
- Database migrations need special handling
- Stateful applications require session management

**When to Use:**
- Mission-critical applications
- High-traffic systems
- When instant rollback is essential
- When you can afford 2x infrastructure

---

### 2. Canary Deployment

**Gradual rollout to subset of users.**

```
Version 1.0: ████████████████████ 100% → 90% → 50% → 0%
Version 1.1: ░░░░░░░░░░░░░░░░░░░░   0% → 10% → 50% → 100%

Timeline: 0min  →  15min  →  30min  →  60min

Monitor metrics at each stage:
- Error rate
- Response time
- Business metrics
- User feedback
```

**Process:**
1. Deploy new version alongside old version
2. Route 5-10% of traffic to new version
3. Monitor metrics for 15-30 minutes
4. If metrics are good: increase to 25%
5. Continue gradual increase: 50%, 75%, 100%
6. If metrics degrade: route all traffic back to old version

**Benefits:**
- Limits blast radius of bugs
- Real-world production testing
- Data-driven rollout decisions
- Early detection of issues

**Drawbacks:**
- Requires sophisticated routing
- Longer deployment time
- Need good monitoring and metrics
- Complex rollback decision-making

**When to Use:**
- High-risk changes
- User-facing applications
- When you have good monitoring
- When gradual validation is important

**Canary with Feature Flags:**
```javascript
// Combine canary with feature flags for fine-grained control
function getFeatureFlag(userId, feature) {
  if (isInCanaryGroup(userId, 10)) {
    return newFeatureImplementation();
  }
  return oldFeatureImplementation();
}
```

---

### 3. Rolling Deployment

**Update instances one at a time.**

```
┌─────────────────────────────────┐
│  Load Balancer                  │
└────┬─────┬──────┬──────┬────────┘
     │     │      │      │
     v     v      v      v
   ┌───┐ ┌───┐ ┌───┐ ┌───┐
   │ 1 │ │ 2 │ │ 3 │ │ 4 │  Instances
   └───┘ └───┘ └───┘ └───┘

Step 1: │v1.1│ v1.0  v1.0  v1.0  ← Update instance 1
Step 2: │v1.1││v1.1│ v1.0  v1.0  ← Update instance 2
Step 3: │v1.1││v1.1││v1.1│ v1.0  ← Update instance 3
Step 4: │v1.1││v1.1││v1.1││v1.1│ ← Update instance 4
```

**Process:**
1. Remove instance 1 from load balancer
2. Update instance 1 to new version
3. Run health checks on instance 1
4. Add instance 1 back to load balancer
5. Wait for health confirmation
6. Repeat for next instance
7. If health check fails: stop and rollback

**Benefits:**
- No downtime (if > 1 instance)
- Resource efficient (no extra infrastructure)
- Automatic rollback on health check failure
- Simple to understand and implement

**Drawbacks:**
- Slower than blue-green
- Mixed versions running temporarily
- Need good health checks
- Rollback means updating all instances back

**When to Use:**
- Standard web applications
- When infrastructure budget is limited
- When you have reliable health checks
- For gradual, controlled updates

**Kubernetes Rolling Update:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max extra pods during update
      maxUnavailable: 1  # Max pods that can be down
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:v1.1
```

---

### 4. Recreate Deployment

**Stop all old, then start all new.**

```
Old Version: ████████ → ░░░░░░░░ (stopped)
              ↓ Downtime ↓
New Version: ░░░░░░░░ → ████████ (started)
```

**Process:**
1. Stop all old version instances
2. Deploy new version
3. Start all new version instances
4. Verify new version is working

**Benefits:**
- Simple to understand
- No version compatibility issues
- Clean state transition
- Resource efficient

**Drawbacks:**
- Downtime (critical issue for most apps)
- All-or-nothing approach
- Rollback requires full redeployment

**When to Use:**
- Development/staging environments
- Maintenance windows are acceptable
- Applications with infrequent releases
- Non-critical internal tools
- When version compatibility is complex

---

### 5. Feature Flags / Dark Launches

**Deploy code inactive, enable gradually.**

```
Deploy v1.1 with new feature DISABLED
      ↓
Feature flag: 0% of users
      ↓
Enable for: Internal team (1%)
      ↓
Enable for: Beta users (10%)
      ↓
Enable for: All users (100%)
```

**Process:**
1. Deploy new code with feature behind flag (off by default)
2. Enable for internal testing (0.1% - internal IPs)
3. Enable for beta users (1-5%)
4. Monitor metrics and feedback
5. Gradually increase percentage: 10%, 25%, 50%, 100%
6. Once stable at 100%: remove flag, clean up code

**Benefits:**
- Decouple deployment from release
- Fine-grained control over rollout
- Easy rollback (toggle flag off)
- A/B testing capabilities
- Dark launching (deployed but invisible)

**Drawbacks:**
- Code complexity (flag conditionals)
- Technical debt if flags aren't cleaned up
- Testing complexity (multiple flag states)

**When to Use:**
- High-risk features
- Gradual rollouts needed
- A/B testing scenarios
- When separating deploy from release
- For premium/beta features

**Implementation Example:**
```python
# Feature flag service
def is_feature_enabled(feature_name, user_id):
    rollout_percentage = get_rollout_percentage(feature_name)
    return hash(user_id) % 100 < rollout_percentage

# Usage in code
if is_feature_enabled("new_checkout_flow", user.id):
    return new_checkout_flow()
else:
    return old_checkout_flow()
```

**Popular Feature Flag Tools:**
- LaunchDarkly
- Split.io
- Unleash (open source)
- AWS AppConfig
- Flagsmith (open source)

---

## Pre-Deployment Checklist

Before every deployment, verify:

### 1. Code Readiness
- [ ] All tests passing (unit, integration, e2e)
- [ ] Code reviewed and approved
- [ ] CI/CD pipeline green
- [ ] Security scans completed
- [ ] Performance tests passed (if applicable)
- [ ] Changelog updated
- [ ] Version number incremented

### 2. Environment Readiness
- [ ] Target environment identified (dev/staging/prod)
- [ ] Infrastructure capacity verified
- [ ] Required secrets/configs available
- [ ] Database migrations prepared
- [ ] Feature flags configured
- [ ] Monitoring and alerting active

### 3. Communication
- [ ] Team notified of deployment
- [ ] Deployment window scheduled
- [ ] On-call engineer identified
- [ ] Rollback plan documented
- [ ] Stakeholders informed (if production)

### 4. Dependencies
- [ ] External services notified (if API changes)
- [ ] Database backups completed
- [ ] Dependent services compatible
- [ ] Third-party integrations tested
- [ ] Rate limits and quotas checked

---

## Deployment Process

### Standard Deployment Flow

```
1. Pre-Deployment
   ↓
2. Database Migrations (if needed)
   ↓
3. Deploy Application Code
   ↓
4. Health Checks
   ↓
5. Smoke Tests
   ↓
6. Traffic Routing
   ↓
7. Monitoring
   ↓
8. Post-Deployment Verification
```

---

### Database Migrations

**Critical: Migrations must be backward compatible.**

#### Forward-Compatible Migration Pattern

**Problem:** Deploy new code that requires new DB schema.

**Solution:** Three-phase deployment

**Phase 1: Add (backward compatible)**
```sql
-- Add new column, nullable initially
ALTER TABLE users ADD COLUMN email_verified BOOLEAN DEFAULT FALSE;

-- Deploy application v1.1 (uses new column)
```

**Phase 2: Migrate Data**
```sql
-- Backfill existing data
UPDATE users SET email_verified = TRUE WHERE email_confirmed_at IS NOT NULL;
```

**Phase 3: Enforce (after old code retired)**
```sql
-- Make column non-nullable (only after v1.0 is fully retired)
ALTER TABLE users ALTER COLUMN email_verified SET NOT NULL;
```

#### Migration Anti-Patterns

❌ **Don't: Breaking change in one deployment**
```sql
-- Bad: This breaks old code immediately
ALTER TABLE users DROP COLUMN old_email_field;
ALTER TABLE users ADD COLUMN new_email_field VARCHAR(255) NOT NULL;
```

✅ **Do: Add new, deprecate old, remove old**
```sql
-- Phase 1: Add new column
ALTER TABLE users ADD COLUMN new_email_field VARCHAR(255);

-- Phase 2: Migrate data + deploy new code using new column
UPDATE users SET new_email_field = old_email_field;

-- Phase 3: After old code retired, remove old column
ALTER TABLE users DROP COLUMN old_email_field;
```

---

### Health Checks

**Every service must expose health endpoints.**

#### Basic Health Check
```python
# Python Flask example
@app.route('/health')
def health():
    return {'status': 'healthy'}, 200
```

#### Comprehensive Health Check
```python
@app.route('/health')
def health():
    checks = {
        'database': check_database_connection(),
        'redis': check_redis_connection(),
        'disk_space': check_disk_space(),
        'memory': check_memory_usage(),
    }

    if all(checks.values()):
        return {'status': 'healthy', 'checks': checks}, 200
    else:
        return {'status': 'unhealthy', 'checks': checks}, 503
```

#### Readiness vs Liveness

**Liveness:** Is the process alive?
- Restart if failing
- Example: `/health/live`

**Readiness:** Is the service ready to receive traffic?
- Remove from load balancer if failing
- Example: `/health/ready`

```yaml
# Kubernetes health checks
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 5
```

---

### Smoke Tests

**Post-deployment validation that critical paths work.**

```bash
#!/bin/bash
# smoke-tests.sh

echo "Running smoke tests..."

# Test 1: Health endpoint
curl -f http://myapp.com/health || exit 1

# Test 2: Critical API endpoint
curl -f http://myapp.com/api/users/1 || exit 1

# Test 3: Authentication
TOKEN=$(curl -X POST http://myapp.com/auth/login \
  -d '{"username":"test","password":"test"}' | jq -r .token)
[ -z "$TOKEN" ] && exit 1

# Test 4: Database connectivity
curl -f http://myapp.com/api/status | grep -q "database.*ok" || exit 1

echo "All smoke tests passed!"
```

---

## Platform-Specific Deployment

### Kubernetes Deployment

#### Basic Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
  labels:
    app: myapp
spec:
  replicas: 3
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
        image: myapp:1.1.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

#### Deploy with kubectl
```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Check rollout status
kubectl rollout status deployment/myapp

# View deployment history
kubectl rollout history deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=2

# Scale deployment
kubectl scale deployment/myapp --replicas=5

# Update image
kubectl set image deployment/myapp myapp=myapp:1.2.0
```

---

### AWS Deployment

#### AWS ECS (Elastic Container Service)
```bash
# Register new task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Update service to use new task definition
aws ecs update-service \
  --cluster production \
  --service myapp \
  --task-definition myapp:42 \
  --desired-count 3

# Wait for deployment to complete
aws ecs wait services-stable \
  --cluster production \
  --services myapp
```

#### AWS Lambda
```bash
# Update function code
aws lambda update-function-code \
  --function-name myapp \
  --zip-file fileb://function.zip

# Publish new version
VERSION=$(aws lambda publish-version \
  --function-name myapp \
  --query 'Version' \
  --output text)

# Update alias to point to new version
aws lambda update-alias \
  --function-name myapp \
  --name production \
  --function-version $VERSION
```

#### AWS Elastic Beanstalk
```bash
# Create application version
aws elasticbeanstalk create-application-version \
  --application-name myapp \
  --version-label v1.1.0 \
  --source-bundle S3Bucket=mybucket,S3Key=myapp-v1.1.0.zip

# Deploy to environment
aws elasticbeanstalk update-environment \
  --environment-name myapp-production \
  --version-label v1.1.0
```

---

### Azure Deployment

#### Azure App Service
```bash
# Deploy via Azure CLI
az webapp deployment source config-zip \
  --resource-group myapp-rg \
  --name myapp \
  --src ./myapp.zip

# Deploy specific slot (for blue-green)
az webapp deployment source config-zip \
  --resource-group myapp-rg \
  --name myapp \
  --slot staging \
  --src ./myapp.zip

# Swap slots (staging → production)
az webapp deployment slot swap \
  --resource-group myapp-rg \
  --name myapp \
  --slot staging \
  --target-slot production
```

#### Azure Kubernetes Service (AKS)
```bash
# Get credentials
az aks get-credentials --resource-group myapp-rg --name myapp-cluster

# Deploy using kubectl (same as Kubernetes section)
kubectl apply -f deployment.yaml
```

---

### GCP Deployment

#### Google Cloud Run
```bash
# Deploy container
gcloud run deploy myapp \
  --image gcr.io/myproject/myapp:1.1.0 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Deploy with traffic splitting (canary)
gcloud run services update-traffic myapp \
  --to-revisions=myapp-v2=10,myapp-v1=90
```

#### Google Kubernetes Engine (GKE)
```bash
# Get credentials
gcloud container clusters get-credentials myapp-cluster --region us-central1

# Deploy using kubectl
kubectl apply -f deployment.yaml
```

---

### Docker Swarm

```bash
# Deploy stack
docker stack deploy -c docker-compose.yml myapp

# Update service
docker service update \
  --image myapp:1.1.0 \
  myapp_web

# Scale service
docker service scale myapp_web=5

# Rollback service
docker service rollback myapp_web
```

---

## Zero-Downtime Deployment

### Key Principles

1. **Graceful Shutdown**
   - Stop accepting new requests
   - Finish processing in-flight requests
   - Close connections cleanly

2. **Health Checks**
   - Remove unhealthy instances from load balancer
   - Don't route traffic to instances being updated

3. **Rolling Updates**
   - Update one instance at a time
   - Verify health before moving to next

4. **Database Compatibility**
   - New code works with old schema
   - Old code works with new schema

---

### Graceful Shutdown Pattern

```python
# Python example with signal handling
import signal
import sys
import time

shutdown_requested = False

def signal_handler(signum, frame):
    global shutdown_requested
    print("Shutdown signal received, finishing requests...")
    shutdown_requested = True

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# In request handler
def handle_request():
    if shutdown_requested:
        return "Service unavailable", 503
    # Process request normally
    return process_request()

# Graceful shutdown
while shutdown_requested:
    if no_active_requests():
        break
    time.sleep(0.1)

print("All requests finished, exiting...")
sys.exit(0)
```

```javascript
// Node.js example
const server = app.listen(3000);

process.on('SIGTERM', () => {
  console.log('SIGTERM received, closing server gracefully...');

  server.close(() => {
    console.log('Server closed, exiting...');
    process.exit(0);
  });

  // Force exit after 30 seconds
  setTimeout(() => {
    console.error('Forced shutdown after timeout');
    process.exit(1);
  }, 30000);
});
```

---

## Rollback Procedures

### When to Rollback

Rollback immediately if:
- Error rate increases significantly (>2x baseline)
- Critical functionality broken
- Data corruption detected
- Performance degradation (>50% slower)
- Security vulnerability introduced

### Rollback Decision Tree

```
Deployment Issue Detected
         ↓
    Can it be hotfixed in <5 minutes?
    ↙              ↘
  YES               NO
   ↓                 ↓
Hotfix        ROLLBACK
   ↓                 ↓
Test          Investigate
   ↓           Fix in dev
Deploy        Redeploy
```

---

### Kubernetes Rollback

```bash
# Check current status
kubectl rollout status deployment/myapp

# View rollout history
kubectl rollout history deployment/myapp

# Rollback to previous version
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=3

# Pause rollout (stop updating remaining instances)
kubectl rollout pause deployment/myapp

# Resume rollout
kubectl rollout resume deployment/myapp
```

---

### Blue-Green Rollback

```bash
# Simply switch router back to blue environment
# AWS Example (updating target group)
aws elbv2 modify-listener \
  --listener-arn $LISTENER_ARN \
  --default-actions Type=forward,TargetGroupArn=$BLUE_TARGET_GROUP

# Instant rollback!
```

---

### Canary Rollback

```bash
# Route all traffic back to stable version
# Example with Istio
kubectl apply -f - <<EOF
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: myapp
spec:
  hosts:
  - myapp
  http:
  - route:
    - destination:
        host: myapp
        subset: v1
      weight: 100
    - destination:
        host: myapp
        subset: v2
      weight: 0
EOF
```

---

## Deployment Security

### 1. Secrets Management

❌ **Never do this:**
```yaml
# Bad: Secrets in code
env:
- name: DATABASE_PASSWORD
  value: "super_secret_password"
```

✅ **Do this:**
```yaml
# Good: Secrets from secret management system
env:
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: myapp-secrets
      key: database-password
```

#### Secret Management Tools

- **Kubernetes Secrets** (for K8s deployments)
- **AWS Secrets Manager** / **AWS Systems Manager Parameter Store**
- **Azure Key Vault**
- **Google Cloud Secret Manager**
- **HashiCorp Vault** (cross-platform)
- **Doppler** (developer-friendly)

#### Accessing Secrets at Runtime

```python
# Python with AWS Secrets Manager
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
db_config = get_secret('production/database')
db_password = db_config['password']
```

---

### 2. Environment Isolation

**Separate environments with clear boundaries:**

```
Development  → Developers can deploy anytime
     ↓
Staging      → Auto-deploy on merge to main
     ↓
Production   → Manual approval + restricted access
```

**Access Control:**
- Development: All developers
- Staging: Developers + QA
- Production: Ops team + tech leads only

---

### 3. Audit Logging

**Log all deployments:**

```json
{
  "timestamp": "2025-01-10T14:30:00Z",
  "event": "deployment",
  "environment": "production",
  "service": "myapp",
  "version": "1.1.0",
  "deployed_by": "jane.doe@example.com",
  "commit_sha": "abc123def456",
  "rollback": false,
  "status": "success"
}
```

---

### 4. Deployment Permissions

**Principle of least privilege:**

```yaml
# Example: Kubernetes RBAC for deployment
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "update", "patch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
```

---

## Deployment Automation (GitOps)

### GitOps Principles

1. **Git as single source of truth**
2. **Declarative configuration**
3. **Automated deployment on git changes**
4. **Reconciliation loops** (actual state → desired state)

### ArgoCD Example

```yaml
# Application definition
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp-config
    targetRevision: HEAD
    path: k8s/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

**Workflow:**
1. Developer commits config change to git
2. ArgoCD detects change
3. ArgoCD applies changes to cluster
4. ArgoCD monitors and reconciles continuously

---

## Deployment Monitoring

### Key Metrics to Monitor

**During Deployment:**
- Error rate (should not increase)
- Response time (should not degrade)
- Request rate (should remain stable)
- Instance health (all instances healthy)

**Post-Deployment:**
- Application logs (check for errors)
- Business metrics (conversions, signups, etc.)
- Resource usage (CPU, memory)
- Dependency health (database, cache, APIs)

### Monitoring Checklist

- [ ] Error rate dashboard visible
- [ ] Response time dashboard visible
- [ ] Alerts configured for anomalies
- [ ] Logs aggregated and searchable
- [ ] On-call engineer has access to dashboards
- [ ] Rollback runbook accessible

---

## Troubleshooting Failed Deployments

### Common Issues

#### 1. Health Checks Failing

**Symptoms:** New instances fail health checks, removed from load balancer

**Debug:**
```bash
# Check instance logs
kubectl logs deployment/myapp

# Describe pod for events
kubectl describe pod myapp-xxx

# Test health endpoint manually
curl http://pod-ip:8080/health
```

**Common Causes:**
- Application startup too slow (increase initialDelaySeconds)
- Missing dependencies (database, cache)
- Configuration errors
- Port mismatch

---

#### 2. Database Migration Failure

**Symptoms:** Migration script fails during deployment

**Debug:**
```bash
# Check migration logs
kubectl logs migration-job

# Connect to database and check schema
psql -h $DB_HOST -U $DB_USER -d $DB_NAME
\dt  # List tables
\d table_name  # Describe table
```

**Recovery:**
- Rollback code
- Investigate migration failure
- Fix migration script
- Test in staging
- Redeploy

---

#### 3. Out of Memory (OOM) Errors

**Symptoms:** Pods/instances crash during deployment

**Debug:**
```bash
# Check resource limits
kubectl describe pod myapp-xxx | grep -A 5 "Limits"

# Check actual resource usage
kubectl top pod myapp-xxx
```

**Fix:**
- Increase memory limits in deployment config
- Investigate memory leaks
- Optimize application memory usage

---

#### 4. Image Pull Errors

**Symptoms:** Cannot pull container image

**Debug:**
```bash
kubectl describe pod myapp-xxx | grep -A 10 "Events"
# Look for: "Failed to pull image" or "ImagePullBackOff"
```

**Common Causes:**
- Image tag doesn't exist
- Registry authentication failed
- Image registry unreachable
- Typo in image name

**Fix:**
```bash
# Verify image exists
docker pull myapp:1.1.0

# Check secret for registry auth
kubectl get secret regcred -o yaml
```

---

## Integration with Other Skills

### With CI/CD
- CI builds and tests code
- CD deploys passing builds
- Deployment is final stage of pipeline
- Automated deployment to dev/staging
- Manual approval gate for production

### With Infrastructure (IaC)
- Terraform provisions infrastructure
- Deployment tools deploy applications
- Infrastructure changes deployed before app changes
- Version infrastructure alongside application

### With Monitoring
- Monitoring watches deployment metrics
- Alerts trigger if deployment causes issues
- Dashboards show before/after comparison
- Logs help troubleshoot failed deployments

### With Git Hygiene
- Deployment tags mark released versions
- Commit SHAs tracked in deployments
- Rollback references previous commits
- Deployment history in git log

---

## Quick Reference

### Deployment Strategy Comparison

| Strategy | Downtime | Rollback Speed | Infrastructure Cost | Complexity | Best For |
|----------|----------|----------------|---------------------|------------|----------|
| **Blue-Green** | None | Instant | 2x (high) | Medium | Mission-critical |
| **Canary** | None | Fast | 1.1x (low) | High | High-risk changes |
| **Rolling** | None | Slow | 1x (none) | Low | Standard apps |
| **Recreate** | Yes | Medium | 1x (none) | Very Low | Dev/staging |
| **Feature Flags** | None | Instant | 1x (none) | High | Gradual rollouts |

---

### Deployment Commands Quick Reference

```bash
# Kubernetes
kubectl apply -f deployment.yaml
kubectl rollout status deployment/myapp
kubectl rollout undo deployment/myapp
kubectl scale deployment/myapp --replicas=5

# Docker
docker service update --image myapp:1.1.0 myapp_web
docker service rollback myapp_web

# AWS ECS
aws ecs update-service --cluster prod --service myapp --task-definition myapp:42

# Azure
az webapp deployment source config-zip --name myapp --src app.zip

# GCP Cloud Run
gcloud run deploy myapp --image gcr.io/project/myapp:1.1.0
```

---

### Pre-Deployment Checklist (Short)

- [ ] Tests passing
- [ ] Code reviewed
- [ ] Database migrations ready
- [ ] Secrets configured
- [ ] Monitoring active
- [ ] Rollback plan documented
- [ ] Team notified

---

**Remember:** Deployment is not just pushing code—it's a controlled, monitored, reversible process. Automate everything. Test in staging. Monitor in production. Always have a rollback plan. Boring deployments are successful deployments.
