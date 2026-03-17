---
name: deploy-stack
description: Deploys multiple components to an environment. Use for coordinated deployments of backend, frontend, and landing.
allowed-tools: Bash(npx sst:*), Bash(cd:*), Bash(aws:*)
---

# Deploy Stack

Deploys multiple components to an environment in the correct order.

## Deployment Order

For a full stack deployment:

1. **Backend** (first - frontend depends on API)
2. **Frontend** (after backend API is available)
3. **Landing** (independent, can be parallel)

## Commands

### Deploy All to Dev

```bash
# 1. Backend
cd back && npx sst deploy --stage dev

# 2. Frontend (after backend completes)
cd ../front && npx sst deploy --stage dev

# 3. Landing (can run in parallel with frontend)
cd ../landing && npx sst deploy --stage dev
```

### Deploy All to Production

```bash
# 1. Backend
cd back && npx sst deploy --stage prod

# 2. Run migrations
aws lambda invoke --function-name template-saas-api-migrate-lambda-prod /dev/null

# 3. Frontend
cd ../front && npx sst deploy --stage prod

# 4. Landing
cd ../landing && npx sst deploy --stage prod
```

## Pre-Deployment Checklist

### Secrets

Ensure all secrets are set for the target stage:

**Backend:**
```bash
npx sst secret set DbConnStr "..." --stage <stage>
npx sst secret set ClerkSecretKey "..." --stage <stage>
npx sst secret set ClerkWebhookSecret "..." --stage <stage>
```

**Frontend:**
```bash
npx sst secret set ClerkPublishableKey "..." --stage <stage>
npx sst secret set ClerkSecretKey "..." --stage <stage>
```

### Quality Checks

Run quality checks before deployment:
```bash
# Backend
cd back && task format && task tests

# Frontend
cd front && pnpm type-check && pnpm lint && pnpm build

# Landing
cd landing && pnpm type-check && pnpm lint && pnpm build
```

## CI/CD Alternative

Manual stack deployment should only be needed for:
- Initial setup
- Emergency fixes
- Development testing

For normal deployments, use CI/CD:
- Push to `develop` → deploys to `dev` stage
- Push to `main` → deploys to `prod` stage

## Rollback

If deployment fails:

1. Check SST console for errors:
   ```bash
   npx sst console --stage <stage>
   ```

2. Check CloudWatch logs for Lambda errors

3. For frontend: Previous CloudFront distribution remains until new deploy succeeds

4. For backend: Revert code and redeploy

## Domain Verification

After deployment, verify domains are accessible:

| Component | Dev | Prod |
|-----------|-----|------|
| Landing | `dev.{domain}` | `{domain}` |
| Frontend | `app-dev.{domain}` | `app.{domain}` |
| Backend | `api-dev.{domain}/health` | `api.{domain}/health` |
