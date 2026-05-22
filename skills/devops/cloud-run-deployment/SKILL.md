---
name: cloud-run-deployment
version: "1.0"
description: >
  Deploy and manage Google Cloud Run services with traffic management and scaling.
  PROACTIVELY activate for: (1) deploying containers to Cloud Run, (2) configuring blue-green or canary deployments, (3) managing traffic splits and rollbacks.
  Triggers: "cloud run", "deploy", "traffic split"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Cloud Run Deployment Skill

## Metadata (Tier 1)

**Keywords**: cloud run, deploy, gcloud run, scaling, concurrency, health check, traffic split, blue-green, canary, revision

**File Patterns**: service.yaml, cloudrun.yaml, *-deployment.sh

**Modes**: cloud_run_dev, deployment

**Activation**: When user mentions Cloud Run deployment, service configuration, or traffic management.

---

## Instructions (Tier 2)

### Core Deployment Patterns

#### 1. Basic Deployment
```bash
gcloud run deploy SERVICE \
  --image=IMAGE_URL \
  --region=REGION \
  --service-account=SA_EMAIL \
  --no-allow-unauthenticated
```

#### 2. Blue-Green Deployment
Deploy new revision without traffic, validate, then switch:
```bash
# Deploy with --no-traffic
gcloud run deploy SERVICE --image=NEW_IMAGE --no-traffic --tag=blue

# Validate health check
curl -f https://blue---SERVICE-xxx.run.app/health

# Shift traffic
gcloud run services update-traffic SERVICE --to-tags=blue=100
```

#### 3. Canary Deployment
Gradual traffic shift:
```bash
# Deploy canary
gcloud run deploy SERVICE --image=NEW_IMAGE --no-traffic --tag=canary

# 10% traffic
gcloud run services update-traffic SERVICE \
  --to-revisions=CANARY_REV=10,LATEST=90

# Monitor, then increase to 50%, 100%
```

### Scaling Configuration

- **min-instances**: Set >0 for latency-sensitive (eliminates cold starts)
- **max-instances**: Limit to control costs
- **concurrency**: Default 80, tune based on workload (lower for CPU-intensive, higher for I/O)

```bash
gcloud run deploy SERVICE \
  --min-instances=2 \
  --max-instances=50 \
  --concurrency=80
```

### Health Checks (MANDATORY)

Use service.yaml for startup and liveness probes:

```yaml
spec:
  template:
    spec:
      containers:
      - startupProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          failureThreshold: 3
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          periodSeconds: 10
```

### Traffic Management

- **--to-latest**: Send 100% to latest revision
- **--to-tags=TAG=PERCENT**: Tag-based routing
- **--to-revisions=REV1=50,REV2=50**: Revision-based split

### Instant Rollback

```bash
PREVIOUS=$(gcloud run revisions list --service=SERVICE --limit=2 --format='value(metadata.name)' | tail -n 1)
gcloud run services update-traffic SERVICE --to-revisions=$PREVIOUS=100
```

### Anti-Patterns
- No health checks
- Direct to 100% traffic for critical services
- Using --allow-unauthenticated by default
- Ignoring startup probe failures
