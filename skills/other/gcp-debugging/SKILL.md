---
name: gcp-debugging
description: GCP debugging and investigation patterns. Use when checking Cloud Logging, debugging Cloud Run services, investigating production issues, verifying deployments, or checking Cloud Build status.
---

# GCP Debugging Patterns

## Cloud Logging

**Tail Cloud Run logs (live):**
```bash
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=gh-pr-linear-issue-linker" \
  --project=your-project-id \
  --format=json
```

**Filter logs by severity:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND severity>=ERROR" \
  --project=your-project-id \
  --limit=50 \
  --format=json
```

**Search logs with filters:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND textPayload=~'webhook'" \
  --project=your-project-id \
  --freshness=1h \
  --limit=100
```

**Query specific time range:**
```bash
gcloud logging read "resource.type=cloud_run_revision" \
  --project=your-project-id \
  --format=json \
  --freshness=2h
```

## Cloud Run Service Verification

**Get service details:**
```bash
gcloud run services describe gh-pr-linear-issue-linker \
  --region=us-central1 \
  --project=your-project-id \
  --format=yaml
```

**Check service status:**
```bash
gcloud run services list --project=your-project-id --region=us-central1
```

**Get recent revisions:**
```bash
gcloud run revisions list \
  --service=gh-pr-linear-issue-linker \
  --region=us-central1 \
  --project=your-project-id
```

**View environment variables:**
```bash
gcloud run services describe gh-pr-linear-issue-linker \
  --region=us-central1 \
  --project=your-project-id \
  --format="yaml(spec.template.spec.containers[0].env)"
```

## Cloud Build Investigation

**List recent builds:**
```bash
gcloud builds list \
  --project=your-project-id \
  --limit=10 \
  --format="table(id,status,createTime,duration)"
```

**Get build logs:**
```bash
gcloud builds log {build-id} --project=your-project-id
```

**Check build status:**
```bash
gcloud builds describe {build-id} \
  --project=your-project-id \
  --format=json
```

## Artifact Registry

**List container images:**
```bash
gcloud artifacts docker images list \
  us-central1-docker.pkg.dev/your-project-id/gh-pr-linear-issue-linker \
  --project=your-project-id
```

**Get image details:**
```bash
gcloud artifacts docker images describe \
  us-central1-docker.pkg.dev/your-project-id/gh-pr-linear-issue-linker/app:latest \
  --project=your-project-id
```

## Secret Manager

**List secrets:**
```bash
gcloud secrets list --project=your-project-id
```

**Get secret metadata:**
```bash
gcloud secrets describe {secret-name} --project=your-project-id
```

**Access secret value (for debugging):**
```bash
gcloud secrets versions access latest \
  --secret={secret-name} \
  --project=your-project-id
```

## Testing Webhook Locally

**Send test webhook:**
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256=..." \
  -d @test-payload.json
```

**Check service health:**
```bash
curl https://gh-pr-linear-issue-linker-xxxxx.run.app/health
```

## Investigation Methodology

### Phase 1: Context
- When does it occur?
- Which PRs/users are affected?
- Frequency (intermittent vs consistent)?

### Phase 2: Evidence Collection
- Cloud Logging for error messages and traces
- Cloud Run revision history
- Cloud Build logs for deployment failures
- Webhook payload inspection (from GitHub delivery logs)

### Phase 3: Proof Generation
Produce one of:
1. **Reproduced Test Case**: pytest test that fails
2. **Log Evidence**: Cloud Logging with stack trace and Logfire trace ID
3. **Webhook Payload**: GitHub webhook delivery logs showing malformed data
4. **CI/CD Output**: Cloud Build logs showing build/deploy failure

### Always Specify
- `--project=your-project-id` for all gcloud commands
- `--region=us-central1` for regional resources (Cloud Run)
- `--format=json` for programmatic parsing
