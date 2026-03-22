---
name: deploy-staging
description: Deploy to staging workflow — build, deploy to staging environment, run smoke tests, verify. Use after feature completion before production deployment.
disable-model-invocation: true
argument-hint: [service-name]
---

# Deploy to Staging

Structured workflow for deploying to staging environment. Builds the application, deploys, runs smoke tests, and verifies the deployment.

## 1. Pre-Deployment Checks

### 1a. Verify Branch State

```
// turbo
git branch --show-current
```

```
// turbo
git status --short
```

- Working directory must be clean
- Branch should be `main` or a release branch

### 1b. Run Tests

Invoke `/run-tests` sub-workflow. All tests must pass before deploying.

### 1c. Identify Deployment Method

Read `CLAUDE.md` and project config to determine:

| Signal | Method |
|---|---|
| `Dockerfile` + K8s manifests | Container → Kubernetes |
| `Dockerfile` + `docker-compose` | Container → Docker Compose |
| Helm charts | Container → Helm |
| Terraform | Infrastructure as Code |
| Serverless config (serverless.yml, SAM) | Serverless deployment |
| Static site (Next.js, Vite) | CDN / static hosting |
| Platform config (Netlify, Vercel, Railway) | Platform deployment |

## 2. Build

Build the application artifact:

| Stack | Command |
|---|---|
| Node.js | `npm run build` or `pnpm build` |
| Java | `./mvnw clean package -DskipTests` |
| Python | `docker build -t <image>:<tag> .` |
| Go | `go build -o bin/app ./cmd/api` |
| .NET | `dotnet publish -c Release` |

### Container Build (if applicable)

```
docker build -t <registry>/<image>:<tag> .
```

Tag with git SHA or version:
```
docker tag <image> <registry>/<image>:<git-sha>
```

## 3. Deploy to Staging

**⚠️ Present deployment plan and request APPROVE before executing.**

### 3a. Kubernetes / Helm

```
helm upgrade --install <release> <chart> \
  -n staging \
  -f values-staging.yaml \
  --set image.tag=<tag> \
  --dry-run
```

After APPROVE:
```
helm upgrade --install <release> <chart> \
  -n staging \
  -f values-staging.yaml \
  --set image.tag=<tag>
```

### 3b. Docker Compose

```
docker compose -f docker-compose.staging.yml up -d
```

### 3c. Platform (Netlify, Vercel, etc.)

Follow platform-specific CLI or git-based deployment.

## 4. Verify Deployment

### 4a. Health Check

```
// turbo
kubectl get pods -n staging -o wide
```

Or curl health endpoint:
```
curl -s <staging-url>/health
```

### 4b. Smoke Tests

Run critical path smoke tests:
- Application starts and responds
- Health endpoint returns 200
- Authentication flow works
- Core API endpoints respond correctly
- Database connectivity verified

### 4c. Monitor Logs

```
// turbo
kubectl logs -n staging -l app=<app-name> --tail=50
```

Check for errors, warnings, or unexpected behavior in the first 2–5 minutes.

## 5. Summary

```
## Staging Deployment Summary
- **Version**: [version/tag]
- **Branch**: [branch name]
- **Environment**: staging
- **Method**: [K8s/Helm/Docker/Platform]
- **Build**: [success/fail]
- **Deploy**: [success/fail]
- **Health check**: [pass/fail]
- **Smoke tests**: [pass/fail]
- **Staging URL**: [url]
- **Next steps**: [QA testing / production deploy]
```

If all checks pass, suggest:
- Run full QA testing on staging
- When ready: `/deploy-production`

## Integration

- **Preceded by**: `/pre-commit`, `/create-pr` (code ready)
- **Followed by**: `/deploy-production`
- **Roles**: `Agent(devops-engineer)`, `Agent(devops-architect)` (deployment strategy design)
