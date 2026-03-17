---
name: deploy-component
description: Deploys a component (frontend, backend, or landing) using SST. Use when deploying to AWS, pushing to dev or prod environments.
allowed-tools: Read, Bash(npx sst:*), Bash(cd:*)
---

# Deploy Component

Deploys individual components (frontend, backend, landing) using SST to AWS.

## Prerequisites

1. AWS credentials configured
2. SST secrets set for the stage
3. For backend: ECR image must be built (CI/CD handles this)

## Deployment Commands

### Backend
```bash
cd back && npx sst deploy --stage dev
cd back && npx sst deploy --stage prod
```

### Frontend
```bash
cd front && npx sst deploy --stage dev
cd front && npx sst deploy --stage prod
```

### Landing
```bash
cd landing && npx sst deploy --stage dev
cd landing && npx sst deploy --stage prod
```

## Stages

| Stage | Branch | Domain Pattern |
|-------|--------|----------------|
| `dev` | `develop` | `*-dev.{domain}` |
| `prod` | `main` | `*.{domain}` |

## Domain Structure

| Component | Dev | Prod |
|-----------|-----|------|
| Landing | `dev.questloghq.com` | `questloghq.com` |
| Frontend | `app-dev.questloghq.com` | `app.questloghq.com` |
| Backend | `api-dev.questloghq.com` | `api.questloghq.com` |

## View Deployed Resources

```bash
npx sst console --stage dev
```

## Common Issues

### Missing Secrets
```bash
# Check if secrets are set
npx sst secret list --stage dev

# Set missing secret
npx sst secret set SecretName "value" --stage dev
```

### Route 53 Record Exists
The SST configs use `allowOverwrite: true` / `override: true` for idempotent deploys.

### Build Errors (Frontend)
Ensure all environment variables are set:
```bash
npx sst secret set ClerkPublishableKey "pk_..." --stage dev
npx sst secret set ClerkSecretKey "sk_..." --stage dev
```

## CI/CD

Deployments are typically handled by GitHub Actions:
- Backend: `.github/workflows/deploy-backend.yml`
- Frontend: `.github/workflows/deploy-frontend.yml`
- Landing: `.github/workflows/deploy-landing.yml`

Manual deployment should only be needed for debugging or emergency fixes.
