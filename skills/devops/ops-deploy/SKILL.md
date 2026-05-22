---
name: ops-deploy
description: Deploy Expo frontend (EAS Update/Build) or serverless backend (Serverless Framework) to dev, staging, or production environments.
allowed-tools:
  - Bash
  - Read
---

# Ops: Deploy

Deploy the application to remote environments.

**Argument**: `$ARGUMENTS` — environment (`dev`, `staging`, `production`) and optional target (`frontend`, `backend`, `both`; default: `both`)

## Path Convention

- **Frontend**: Current project directory (`.`)
- **Backend**: `${BACKEND_DIR:-../backend-v2}` — set `BACKEND_DIR` in `.claude/settings.local.json` if your backend is elsewhere

## Safety

**CRITICAL**: Production deployments require explicit human confirmation before proceeding. Always ask for confirmation when `$ARGUMENTS` contains `production`.

## Discovery

1. Read backend `package.json` to discover `deploy:*`, `aws:signin:*` scripts
2. Read frontend `package.json` to discover available scripts
3. Read `.env.{environment}` files to find GraphQL URLs for post-deploy verification

## CI/CD Path (Preferred)

The standard deployment path is via CI/CD — pushing to environment branches triggers auto-deploy. Manual deployment instructions below are for when CI/CD is not suitable.

## Frontend Deployment

### EAS Update (OTA — over-the-air JavaScript update)

Use for JS-only changes (no native module changes).

1. Verify EAS CLI:
   ```bash
   eas whoami
   ```
   If not authenticated: `eas login`

2. Copy environment file:
   ```bash
   cp .env.{environment} .env
   ```

3. Deploy OTA update:
   ```bash
   STAGE={env} NODE_OPTIONS="--max-old-space-size=8192" eas update --auto --channel={env} --message="Manual update"
   ```

4. Verify deployment:
   ```bash
   eas update:list --branch {env} --limit 3
   ```

### EAS Build (Native binary — only when `app.config.ts` or native modules change)

1. ```bash
   eas build --platform all --non-interactive --no-wait --profile={profile}
   ```

2. Check build status:
   ```bash
   eas build:list --limit 5
   ```

## Backend Deployment

### Full Deploy (Serverless Framework)

1. AWS signin (discover script name from backend `package.json`):
   ```bash
   cd "${BACKEND_DIR:-../backend-v2}"
   bun run aws:signin:{env}
   ```

2. Deploy all functions:
   ```bash
   cd "${BACKEND_DIR:-../backend-v2}"
   bun run deploy:{env}
   ```

3. Verify (use the GraphQL URL from `.env.{environment}`):
   ```bash
   curl -sf {graphql-url} -X POST \
     -H "Content-Type: application/json" \
     -d '{"query":"{ __typename }"}' \
     -w "\nHTTP %{http_code} in %{time_total}s\n"
   ```

### Single Function Deploy

Discover available function names from backend `package.json` `deploy:function:*` scripts:

```bash
cd "${BACKEND_DIR:-../backend-v2}"
FUNCTION_NAME={fn} bun run deploy:function:{env}
```

## Post-Deploy Verification

After any deployment:

1. **Health check** the deployed environment (use `ops-verify-health` skill)
2. **Check logs** for errors in the first 5 minutes (use `ops-check-logs` skill)
3. **Monitor Sentry** for new issues (use `ops-monitor-errors` skill)
4. **Run browser UAT smoke test** against the deployed environment (use `ops-browser-uat` skill)

Report deployment result as a table:

| Target | Environment | Method | Status | Verification |
|--------|-------------|--------|--------|-------------|
| Frontend | dev | EAS Update | SUCCESS/FAIL | URL responds |
| Backend | dev | Serverless | SUCCESS/FAIL | GraphQL responds |
