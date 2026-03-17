---
name: vercel-preview
description: Resolve Vercel preview deployment URL for the current git branch. Invoked by browser-verification when deployment.enabled is true, or directly to check deployment status. Use to check deployment status or when browser verification needs a URL.
---

# Vercel Preview URL Resolution Skill

Resolve the Vercel preview deployment URL for the current git branch. Used by
browser-verification and phase-checkpoint to run E2E tests against production-like
environments instead of localhost.

## When This Skill Runs

- Invoked by `browser-verification` skill when `deployment.enabled` is true
- Invoked by `phase-checkpoint` for browser-based acceptance criteria
- Can be invoked directly to check deployment status

## Prerequisites

- Project must be linked to Vercel (`.vercel/project.json` exists)
- Vercel CLI must be installed (`vercel` command available)
- Git repository with current branch

## Inputs

From `.claude/verification-config.json`:

```json
{
  "deployment": {
    "enabled": true,
    "service": "vercel",
    "waitForDeployment": true,
    "deploymentTimeout": 300,
    "tokenVar": "VERCEL_TOKEN"
  }
}
```

## Workflow Overview

Copy this checklist and track progress:

```
Vercel Preview Progress:
- [ ] Step 1: Get git context (branch, commit)
- [ ] Step 2: Check Vercel project linking
- [ ] Step 3: Query deployments for branch
- [ ] Step 4: Wait for deployment (if configured)
- [ ] Step 5: Return URL or error guidance
```

## Step 1: Get Git Context

```bash
# Get current branch name
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Get current commit SHA (short)
COMMIT=$(git rev-parse --short HEAD)

# Get full commit SHA for exact matching
COMMIT_FULL=$(git rev-parse HEAD)
```

**Branch name sanitization:** Vercel sanitizes branch names for URLs (replaces `/` with `-`,
removes special characters). The `vercel ls` command handles this automatically via metadata
matching.

## Step 2: Check Vercel Project Linking

Verify the project is linked to Vercel:

```bash
# Check for Vercel project config
if [ -f ".vercel/project.json" ]; then
  PROJECT_ID=$(jq -r '.projectId' .vercel/project.json)
  ORG_ID=$(jq -r '.orgId' .vercel/project.json)
  echo "Vercel project: $PROJECT_ID (org: $ORG_ID)"
else
  echo "ERROR: Project not linked to Vercel"
  echo "Run 'vercel link' to connect this project"
  exit 1
fi
```

## Step 3: Query Deployments

Use `vercel ls` with metadata filtering to find deployments for the current branch:

```bash
# List deployments for this branch (most reliable method)
vercel ls --json -m gitBranch="$BRANCH" --status READY 2>/dev/null | head -1
```

**Why this approach:**
- `gitBranch` metadata is set automatically by Vercel's GitHub integration
- Handles sanitized branch names correctly
- `--status READY` filters to only completed deployments
- Returns most recent matching deployment

### Validate Response Before Parsing

```bash
RESPONSE=$(vercel ls --json -m gitBranch="$BRANCH" --status READY 2>/dev/null)
if ! echo "$RESPONSE" | jq empty 2>/dev/null; then
  echo "ERROR: vercel ls returned invalid JSON"
  # Return error status, don't attempt to parse
fi
```

### Parse Response

```bash
# Extract URL from JSON response
DEPLOYMENT_URL=$(vercel ls --json -m gitBranch="$BRANCH" --status READY 2>/dev/null | \
  jq -r '.[0].url // empty')

if [ -z "$DEPLOYMENT_URL" ]; then
  echo "No ready deployment found for branch: $BRANCH"
  # Check if deployment exists but is still building
  BUILDING=$(vercel ls --json -m gitBranch="$BRANCH" --status BUILDING 2>/dev/null | \
    jq -r '.[0].url // empty')
  if [ -n "$BUILDING" ]; then
    echo "Deployment in progress: $BUILDING"
  fi
fi
```

## Step 4: Wait for Deployment (Optional)

If `waitForDeployment` is enabled and no ready deployment exists:

```bash
# Get the latest deployment (any status) for the branch
LATEST=$(vercel ls --json -m gitBranch="$BRANCH" 2>/dev/null | jq -r '.[0].url // empty')

if [ -z "$LATEST" ]; then
  echo "No deployments found for branch: $BRANCH"
  echo "Possible causes:"
  echo "  - Branch has not been pushed to remote"
  echo "  - Vercel project is not linked (run: vercel link)"
  echo "  - Branch name doesn't match Vercel's git integration"
  # Return empty result, let caller decide how to handle
fi

if [ -n "$LATEST" ]; then
  echo "Waiting for deployment to be ready: $LATEST"

  # Use vercel inspect --wait with timeout
  TIMEOUT=${DEPLOYMENT_TIMEOUT:-300}
  vercel inspect "$LATEST" --wait --timeout "${TIMEOUT}s"

  if [ $? -eq 0 ]; then
    DEPLOYMENT_URL="https://$LATEST"
    echo "Deployment ready: $DEPLOYMENT_URL"
  else
    echo "Deployment did not become ready within ${TIMEOUT}s"
  fi
fi
```

### Polling Fallback

If `vercel inspect --wait` is unavailable, use polling:

```bash
MAX_ATTEMPTS=$((DEPLOYMENT_TIMEOUT / 10))
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  STATUS=$(vercel ls --json -m gitBranch="$BRANCH" 2>/dev/null | \
    jq -r '.[0].readyState // "UNKNOWN"')

  if [ "$STATUS" = "READY" ]; then
    DEPLOYMENT_URL=$(vercel ls --json -m gitBranch="$BRANCH" 2>/dev/null | \
      jq -r '"https://" + .[0].url')
    echo "Deployment ready: $DEPLOYMENT_URL"
    break
  fi

  echo "Deployment status: $STATUS (attempt $((ATTEMPT + 1))/$MAX_ATTEMPTS)"
  sleep 10
  ATTEMPT=$((ATTEMPT + 1))
done
```

## Step 5: Return Result

### Success Response

```
VERCEL PREVIEW URL RESOLVED
===========================
Branch: feature/user-auth
Commit: a1b2c3d
URL: https://my-app-abc123-team.vercel.app
Status: READY
Age: 5 minutes ago

Ready for browser verification.
```

### Fallback Response (No Deployment)

```
VERCEL PREVIEW URL NOT FOUND
============================
Branch: feature/user-auth
Commit: a1b2c3d

No ready deployment found. Possible causes:
1. Push has not triggered a deployment yet
2. Deployment is still building
3. Branch name doesn't match Vercel's git integration

Checked:
- Ready deployments: 0
- Building deployments: 1 (https://my-app-xyz-team.vercel.app)

Options:
1. Wait for deployment (run with waitForDeployment: true)
2. Fall back to local dev server
3. Trigger deployment manually: vercel --prod
```

### Error Response

```
VERCEL PREVIEW URL ERROR
========================
Error: {error message}

Troubleshooting:
- Verify Vercel CLI is installed: npm i -g vercel
- Verify project is linked: vercel link
- Check authentication: vercel whoami
- Check VERCEL_TOKEN environment variable (if using CI)
```

## Authentication

### Local Development

Vercel CLI uses stored credentials from `vercel login`. No additional configuration
needed for local use.

### CI/CD Environment

Set `VERCEL_TOKEN` environment variable:

```bash
# In CI, use token auth
export VERCEL_TOKEN="${VERCEL_TOKEN}"
vercel ls --token "$VERCEL_TOKEN" --json -m gitBranch="$BRANCH"
```

The skill reads `deployment.tokenVar` from config to determine which env var to use.

## Integration with Browser Verification

When browser-verification invokes this skill:

1. **URL Found:** Return URL, browser-verification uses it as BASE_URL
2. **URL Not Found + fallbackToLocal:** Return null with warning, browser-verification uses localhost
3. **URL Not Found + NO fallback:** Return error, browser-verification blocks

```
# Example integration output
PREVIEW_RESOLUTION
==================
Deployment: Vercel
Branch: main
URL: https://my-app.vercel.app (or null)
Fallback: http://localhost:3000 (if enabled)
Action: USE_PREVIEW | USE_FALLBACK | BLOCK
```

## Troubleshooting

### "No deployments found"

1. Check if branch was pushed: `git log origin/$BRANCH`
2. Check Vercel dashboard for deployment status
3. Verify GitHub/GitLab integration is enabled in Vercel project settings

### "Authentication failed"

1. Run `vercel login` to re-authenticate
2. For CI, ensure `VERCEL_TOKEN` is set correctly
3. Check token has access to the project

### "Project not linked"

1. Run `vercel link` in project directory
2. Select the correct Vercel project
3. Verify `.vercel/project.json` was created

### "Deployment never becomes ready"

1. Check Vercel dashboard for build errors
2. Review build logs: `vercel logs <deployment-url>`
3. Increase `deploymentTimeout` in verification-config.json

## When Preview Cannot Be Resolved

**If Vercel CLI is not installed and cannot be installed:**
- Report: "Vercel CLI unavailable"
- Provide fallback: Use local dev server at `devServer.url`
- If `fallbackToLocal` is disabled: BLOCK with clear message
- Suggest: Install Vercel CLI for preview deployment support

**If all deployments are failing:**
- Report the deployment status and error summary
- Do NOT wait indefinitely
- After timeout: Fall back to local if enabled, otherwise BLOCK
- Provide: Direct link to Vercel dashboard for manual investigation

**If branch has never been deployed:**
- Report: "No deployments found for branch '{branch}'"
- Check if this is a new branch that hasn't been pushed
- Suggest: Push branch to trigger deployment
- Fall back to local if enabled

**If timeout reached while waiting:**
- Stop waiting immediately
- Report: "Deployment wait timeout ({N}s) exceeded"
- Show current deployment state (if known)
- Ask user: "Continue with local fallback?" or "Abort verification?"
