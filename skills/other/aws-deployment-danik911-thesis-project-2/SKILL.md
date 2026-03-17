---
name: aws-deployment
description: Deploys AWS infrastructure with research-first approach. Uses AWS MCP tools for documentation, regional availability, and resource management. ALWAYS searches AWS documentation before writing code, explains services and abbreviations, considers alternatives, maintains organized aws/ folder, and CRITICALLY offers to destroy resources after testing. Use PROACTIVELY for any AWS deployment, Terraform, ECS, Fargate, Lambda, S3, RDS, or cloud infrastructure tasks. MUST BE USED for prototype/learning projects to avoid unexpected costs. (project)
allowed-tools: [
  "Bash", "Read", "Write", "Edit", "Grep", "Glob", "AskUserQuestion", "WebFetch",
  "mcp__aws-knowledge-mcp__aws___search_documentation",
  "mcp__aws-knowledge-mcp__aws___read_documentation",
  "mcp__aws-knowledge-mcp__aws___recommend",
  "mcp__aws-knowledge-mcp__aws___get_regional_availability",
  "mcp__aws-knowledge-mcp__aws___list_regions",
  "mcp__aws-api-mcp__suggest_aws_commands",
  "mcp__aws-api-mcp__call_aws",
  "mcp__aws-ccapi-mcp__check_environment_variables",
  "mcp__aws-ccapi-mcp__get_aws_session_info",
  "mcp__aws-ccapi-mcp__get_resource_schema_information",
  "mcp__aws-ccapi-mcp__list_resources",
  "mcp__aws-ccapi-mcp__get_resource",
  "mcp__aws-ccapi-mcp__generate_infrastructure_code",
  "mcp__aws-ccapi-mcp__explain",
  "mcp__aws-ccapi-mcp__run_checkov",
  "mcp__aws-ccapi-mcp__create_resource",
  "mcp__aws-ccapi-mcp__update_resource",
  "mcp__aws-ccapi-mcp__delete_resource",
  "mcp__aws-ccapi-mcp__get_aws_account_info"
]
---

# AWS Deployment Skill

Deploy and destroy pharma-test-gen ECS/Fargate infrastructure.

## Configuration

| Key | Value |
|-----|-------|
| Project | `pharma-test-gen` |
| Region | `eu-west-2` |
| Account | `275333454012` |
| ECR | `275333454012.dkr.ecr.eu-west-2.amazonaws.com` |

---

## Deploy Workflow

**Full commands:** [reference/quick-commands.md](reference/quick-commands.md)

### 1. ECR Login
```bash
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 275333454012.dkr.ecr.eu-west-2.amazonaws.com
```

### 2. Build & Push Images
```bash
# API
docker buildx build --platform linux/amd64 -f Dockerfile.api.pip -t 275333454012.dkr.ecr.eu-west-2.amazonaws.com/pharma-test-gen-api:staging-latest --push .

# Worker
docker buildx build --platform linux/amd64 -f Dockerfile.worker.pip -t 275333454012.dkr.ecr.eu-west-2.amazonaws.com/pharma-test-gen-worker:staging-latest --push .

# Frontend (needs CLERK key)
docker buildx build --platform linux/amd64 -f Dockerfile.frontend --build-arg NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxx -t 275333454012.dkr.ecr.eu-west-2.amazonaws.com/pharma-test-gen-frontend:staging-latest --push .
```

### 3. Terraform Deploy
```bash
cd aws/terraform && terraform apply -var-file=environments/staging.tfvars -auto-approve
```

### 4. Upload ChromaDB (if missing)
```bash
tar -czvf /tmp/chroma_db.tar.gz -C main chroma_db
aws s3 cp /tmp/chroma_db.tar.gz s3://pharma-test-gen-vectors-staging/chroma_db.tar.gz --region eu-west-2
```

### 5. Force Service Redeployment
```bash
aws ecs update-service --cluster pharma-test-gen-cluster --service pharma-test-gen-api --force-new-deployment --region eu-west-2
aws ecs update-service --cluster pharma-test-gen-cluster --service pharma-test-gen-worker --force-new-deployment --desired-count 1 --region eu-west-2
aws ecs update-service --cluster pharma-test-gen-cluster --service pharma-test-gen-frontend --force-new-deployment --region eu-west-2
```

### 6. Verify Services
```bash
aws ecs describe-services --cluster pharma-test-gen-cluster --services pharma-test-gen-api pharma-test-gen-worker pharma-test-gen-frontend --region eu-west-2 --query 'services[].{name:serviceName,desired:desiredCount,running:runningCount}' --output table
```

---

## Destroy Workflow

### Quick Destroy
```bash
python aws/scripts/destroy.py --yes --skip-ecr
```

### Manual (if script fails)
```bash
cd aws/terraform && terraform destroy -var-file=environments/staging.tfvars -auto-approve
```

### Stop AWS Config (saves ~$3-5/month)
```bash
aws configservice stop-configuration-recorder --configuration-recorder-name pharma --region eu-west-2
```

---

## Troubleshooting

**Full guide:** [reference/troubleshooting.md](reference/troubleshooting.md)

| Symptom | Cause | Fix |
|---------|-------|-----|
| Worker S3 403 Forbidden | ChromaDB tarball deleted | Re-upload: `aws s3 cp chroma_db.tar.gz s3://pharma-test-gen-vectors-staging/` |
| Worker desiredCount=0 | Scaled down during destroy | Scale up: `aws ecs update-service --desired-count 1` |
| `uv: command not found` in WSL | uv not in Ubuntu | Use `python3` directly |
| Terraform state locked | Previous run crashed | `terraform force-unlock <LOCK_ID>` |
| ECR login failed | Token expired | Re-run ECR login command |
| Docker buildx not found | buildx not installed | `docker buildx create --use` |

---

## Health Checks

| Service | Endpoint |
|---------|----------|
| Production (Route 53) | `https://csvgeneration.com/` |
| API Health | `https://csvgeneration.com/health` |
| Frontend | `https://csvgeneration.com/generate` |

### Get ALB DNS (internal)
```bash
aws elbv2 describe-load-balancers --names pharma-test-gen-api-alb pharma-test-gen-frontend-alb --region eu-west-2 --query 'LoadBalancers[].{name:LoadBalancerName,dns:DNSName}' --output table
```

---

## CloudWatch Logs

| Service | Log Group |
|---------|-----------|
| API | `/ecs/pharma-test-gen/api` |
| Worker | `/ecs/pharma-test-gen/worker` |
| Frontend | `/ecs/pharma-test-gen/frontend` |

### View Recent Logs
```bash
aws logs filter-log-events --log-group-name /ecs/pharma-test-gen/worker --start-time $(date -d '5 minutes ago' +%s000) --region eu-west-2 --query 'events[-10:].message' --output text
```

---

## WSL Wrapper (Windows)

All commands need WSL wrapper on Windows:
```powershell
wsl -d Ubuntu -e bash -c "cd /mnt/c/Users/.../thesis_project && <command>"
```

---

## Critical Scripts

| Script | Purpose |
|--------|---------|
| `aws/scripts/deploy.py` | Full deployment orchestrator |
| `aws/scripts/destroy.py` | Clean teardown with S3 emptying |
| `aws/scripts/1_upload_chroma_to_s3.py` | ChromaDB S3 upload (requires boto3) |

---

## Cost Reminder

**Estimated costs while running:**
- Per HOUR: ~$0.75
- Per DAY: ~$18
- Per MONTH: ~$540

**ALWAYS offer to destroy** after testing to avoid unexpected charges.
