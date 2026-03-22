---
name: deploy
description: |
  Use this skill to help deploy code to an environment. Triggered by
  "deploy", "deploy to staging", "deploy to production", "ship it".
argument-hint: "[environment: staging|production|preview]"
allowed-tools: "Bash, Read"
disable-model-invocation: true
---

# Deployment Helper

Safely deploy to `$ARGUMENTS` (defaults to `staging` if not specified).

## Pre-Deploy Checklist

!`git status && echo "---" && git log --oneline -3`

### 1. Environment Confirmation

**Target:** $ARGUMENTS

⚠️  If deploying to **production**, I will explicitly confirm with you before running any deploy commands.

### 2. Pre-flight Checks

```bash
# Ensure clean working tree
git status

# Run tests
npm test

# Run linter
npm run lint

# Check for security issues
npm audit --audit-level=high

# Build
npm run build
```

### 3. Deploy Steps

Depending on your setup, deploy with one of:

```bash
# Vercel
vercel --prod   # production
vercel          # preview

# Railway
railway up

# Fly.io
fly deploy

# AWS (via CDK or SAM)
cdk deploy
sam deploy

# Kubernetes
kubectl apply -f k8s/ --namespace=production

# Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Heroku
git push heroku main

# GitHub Actions (trigger workflow)
gh workflow run deploy.yml --ref main -f environment=$ARGUMENTS
```

### 4. Post-Deploy Verification

```bash
# Check health endpoint
curl -f https://your-app.com/health

# Tail logs for errors
# vercel logs --follow
# fly logs
# kubectl logs -f deployment/app-name
```

### 5. Rollback (if needed)

```bash
# Vercel: revert to previous deployment in dashboard
# Fly.io:    fly releases list; fly deploy --image <old-image>
# Kubernetes: kubectl rollout undo deployment/app-name
# Git:        git revert HEAD && git push
```

## Rules

- Always run tests before deploying
- Always confirm before deploying to production
- Keep a rollback plan ready
- Monitor error rates for 10 minutes post-deploy

$ARGUMENTS
