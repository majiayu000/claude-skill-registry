---
name: railway-auth
description: Railway authentication and token management. Use when logging into Railway, creating API tokens, setting up CI/CD authentication, or verifying Railway credentials.
---

# Railway Authentication

Manage Railway authentication for CLI, API, and CI/CD workflows.

## Overview

Railway supports multiple authentication methods for different use cases:
- **Interactive Login**: Browser-based OAuth for developers
- **Browserless Login**: Device code flow for SSH/Codespaces/headless
- **API Tokens**: Programmatic access for automation and CI/CD

## When to Use

- Setting up Railway CLI for first time
- Authenticating in CI/CD pipelines
- Creating API tokens for automation
- Verifying authentication status
- Troubleshooting auth issues

---

## Operations

### Operation 1: Interactive Login

Standard browser-based authentication for local development.

**Command**:
```bash
railway login
```

**Process**:
1. Opens browser to Railway OAuth page
2. Authenticate with GitHub/email
3. CLI receives authentication token
4. Token stored in `~/.railway/config.json`

**Verification**:
```bash
railway whoami
# Output: Logged in as: your-email@example.com
```

**Use When**: Local development, first-time setup

---

### Operation 2: Browserless Login

Device code authentication for headless environments.

**Command**:
```bash
railway login --browserless
```

**Process**:
1. CLI generates device code
2. Display URL and code to user
3. User visits URL on any device
4. Enters code to authenticate
5. CLI receives token after approval

**Example Output**:
```
To authenticate, visit: https://railway.app/cli-auth
Enter code: ABCD-1234
Waiting for authentication...
```

**Use When**:
- SSH sessions
- GitHub Codespaces
- Remote servers
- Docker containers
- Any environment without browser

---

### Operation 3: Token-Based Authentication

Use API tokens for programmatic access and CI/CD.

**Token Types**:

| Type | Scope | Header | Use Case |
|------|-------|--------|----------|
| Account Token | All personal + team resources | `Authorization: Bearer <TOKEN>` | Full API access |
| Team Token | Team resources only | `Team-Access-Token: <TOKEN>` | Team automation |
| Project Token | Single environment | `Project-Access-Token: <TOKEN>` | Scoped deployments |

**Creating Tokens**:
1. Visit https://railway.com/account/tokens
2. Click "Create Token"
3. Select token type and scope
4. Copy token (shown only once!)

**CLI Authentication with Token**:
```bash
# For Project Tokens
export RAILWAY_TOKEN=<your-project-token>

# For Account/Team Tokens
export RAILWAY_API_TOKEN=<your-account-or-team-token>

# Verify
railway whoami
```

**API Authentication**:
```bash
# Account Token
curl -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { me { name email } }"}' \
  https://backboard.railway.com/graphql/v2

# Project Token
curl -H "Project-Access-Token: $RAILWAY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { projectToken { projectId } }"}' \
  https://backboard.railway.com/graphql/v2
```

**Use When**: CI/CD pipelines, automation scripts, API integrations

---

### Operation 4: Verify Authentication

Check current authentication status.

**Commands**:
```bash
# Check who you're logged in as
railway whoami

# Check current project context
railway status

# Verify token via API
curl -s -H "Authorization: Bearer $RAILWAY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"query { me { name } }"}' \
  https://backboard.railway.com/graphql/v2
```

**Troubleshooting Auth Issues**:

| Issue | Solution |
|-------|----------|
| "Not logged in" | Run `railway login` |
| "Not Authorized" (API) | Check token type matches header |
| Token expired | Create new token at railway.com/account/tokens |
| Wrong project context | Run `railway link` to re-link project |

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy to Railway
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: railway up --ci
```

**Setup**:
1. Create Project Token in Railway dashboard
2. Add as `RAILWAY_TOKEN` secret in GitHub repo settings
3. Use `--ci` flag for non-interactive deployment

### GitLab CI

```yaml
deploy:
  stage: deploy
  image: node:20
  script:
    - npm install -g @railway/cli
    - railway up --ci
  variables:
    RAILWAY_TOKEN: $RAILWAY_PROJECT_TOKEN
  only:
    - main
```

---

## Token Security Best Practices

1. **Never commit tokens** - Use environment variables or secrets managers
2. **Use minimal scope** - Project tokens for single-project CI/CD
3. **Rotate regularly** - Delete and recreate tokens periodically
4. **Monitor usage** - Check Railway dashboard for unusual activity
5. **Separate environments** - Different tokens for dev/staging/prod

---

## Quick Reference

| Task | Command |
|------|---------|
| Login (browser) | `railway login` |
| Login (headless) | `railway login --browserless` |
| Check auth | `railway whoami` |
| Logout | `railway logout` |
| Set token (CLI) | `export RAILWAY_TOKEN=xxx` |
| API auth header | `Authorization: Bearer <token>` |

---

## References

- [token-types.md](references/token-types.md) - Detailed token comparison and usage
- [token-troubleshooting.md](references/token-troubleshooting.md) - **Common auth issues and fixes**

---

## Related Skills

- [railway-api](../railway-api/SKILL.md) - GraphQL API automation
- [railway-automation](../railway-automation/SKILL.md) - CI/CD patterns
- [railway-project-management](../railway-project-management/SKILL.md) - Project setup
