---
name: vercel-management
description: |
  Use when deploying, managing, or working with Vercel projects without using the dashboard.
  Triggers: "vercel deploy", "manage vercel", "vercel project", "vercel domain", "vercel environment",
  "vercel ci/cd", "vercel promotion", "vercel rollback", "vercel functions", "vercel edge",
  "vercel analytics", "vercel dns", "vercel ssl", "vercel team".
  Provides comprehensive workflows for authentication, deployment, domain management, environment variables,
  team collaboration, and production-ready CI/CD patterns.
---

# Vercel Management

Comprehensive guide for managing Vercel projects entirely via CLI and API, eliminating the need for dashboard access.

## Quick Reference

| Task | Command | Notes |
|------|---------|-------|
| **Deploy** | `vercel --prod` | Production deployment |
| **Deploy preview** | `vercel` | Preview deployment |
| **Link project** | `vercel link` | Link local directory |
| **Pull config** | `vercel pull` | Download settings & env vars |
| **Env add** | `echo "value" \| vercel env add KEY production` | Add environment variable |
| **Env pull** | `vercel env pull .env.local` | Pull dev env vars to file |
| **List deployments** | `vercel list` | Recent deployments |
| **Promote** | `vercel promote <url>` | Make deployment current |
| **Rollback** | `vercel rollback` | Revert to previous |
| **Domain add** | `vercel domains add example.com` | Add custom domain |
| **DNS add** | `vercel dns add example.com www A 1.2.3.4` | Add DNS record |
| **Logs** | `vercel logs <url>` | Stream deployment logs |
| **Team context** | `vercel --team=myteam deploy` | Deploy to team |

## Installation & Authentication

### Install CLI

```bash
# Global installation
npm install -g vercel@latest

# Or use with npx
npx vercel@latest
```

### Authentication

```bash
# Interactive login
vercel login

# Login with email
vercel login user@example.com

# CI/CD authentication (use token)
vercel --token $VERCEL_TOKEN deploy --prod

# Create token at: https://vercel.com/account/tokens
export VERCEL_TOKEN="your-token-here"
```

### Check Authentication

```bash
vercel whoami
# Shows current user or team
```

## Project Management

### Initialize & Link Projects

```bash
# Initialize new project
vercel init nextjs-app

# Link existing directory to Vercel project
vercel link

# Link with specific scope
vercel link --scope=my-team

# Pull project settings and environment variables
vercel pull
vercel pull --environment=production
vercel pull --yes  # Skip prompts
```

### Project Configuration

The `vercel pull` command creates:
- `.vercel/project.json` - Project metadata
- `.vercel/README.txt` - Configuration info
- `.env.local` - Development environment variables

### Open in Dashboard (when necessary)

```bash
vercel open
# Opens current project in browser
```

## Deployment

### Basic Deployment

```bash
# Deploy to preview environment
vercel

# Deploy to production
vercel --prod

# Deploy from specific directory
vercel /path/to/project --prod

# Deploy with custom working directory
vercel --cwd /path/to/project --prod
```

### Advanced Deployment Options

```bash
# Force deployment (skip cache)
vercel --force --prod

# Force with cache retention
vercel --force --with-cache --prod

# Deploy prebuilt output (no build step)
vercel deploy --prebuilt --prod

# Deploy without waiting
vercel --no-wait --prod

# Deploy with build logs
vercel --logs --prod

# Skip auto-assigning production domain
vercel --prod --skip-domain

# Deploy to specific regions (functions)
vercel --regions sfo1,iad1 --prod

# Add metadata to deployment
vercel --meta commit=abc123 --meta branch=main --prod

# Set environment variables at runtime
vercel -e NODE_ENV=production --prod

# Set build-time environment variables
vercel -b API_URL=https://api.example.com --prod

# Archive deployment (for large file counts)
vercel --archive=tgz --prod
```

### Capture Deployment URL

```bash
# Deployment URL always goes to stdout
vercel --prod > deployment-url.txt
url=$(vercel --prod)
echo "Deployed to: $url"

# In CI/CD scripts
if vercel --prod > deployment-url.txt 2> error.txt; then
  DEPLOY_URL=$(cat deployment-url.txt)
  echo "Success: $DEPLOY_URL"
else
  echo "Failed: $(cat error.txt)"
  exit 1
fi
```

## Environment Variables

### List Environment Variables

```bash
# List all environment variables
vercel env ls

# List for specific environment
vercel env ls production
vercel env ls preview
vercel env ls development

# List with git branch filter
vercel env ls preview main
```

### Add Environment Variables

```bash
# Add to production (prompts for value)
vercel env add API_KEY production

# Add from stdin
echo "secret-value" | vercel env add API_KEY production

# Add to multiple environments
vercel env add API_KEY production
vercel env add API_KEY preview

# Add sensitive variable (hidden in dashboard)
echo "secret" | vercel env add SECRET production --sensitive

# Add from file
cat cert.pem | vercel env add CERTIFICATE production
```

### Update Environment Variables

```bash
# Update existing variable
vercel env update API_KEY production

# Update from stdin
echo "new-value" | vercel env update API_KEY production

# Update from file
cat ~/.npmrc | vercel env update NPM_RC preview
```

### Remove Environment Variables

```bash
# Remove from specific environment
vercel env rm API_KEY production

# Remove from all environments
vercel env rm API_KEY production
vercel env rm API_KEY preview
vercel env rm API_KEY development
```

### Pull Environment Variables to File

```bash
# Pull development variables to .env.local
vercel env pull .env.local

# Pull production variables
vercel env pull --environment=production .env.production

# Pull preview variables for specific branch
vercel env pull --environment=preview --git-branch=feature-x .env.preview

# Auto-confirm
vercel env pull --yes .env.local
```

### Run Commands with Environment Variables

```bash
# Run command with Vercel environment variables (no file write)
vercel env run -- next dev
vercel env run -- npm test
vercel env run -- node script.js

# Specify environment
vercel env run -e production -- npm run migration
vercel env run -e preview -- npm run seed

# With git branch
vercel env run -e preview --git-branch feature-x -- npm start
```

## Deployment Management

### List Deployments

```bash
# List recent deployments
vercel list
vercel ls

# List for specific project
vercel list my-project

# Filter by environment
vercel list --environment=production
vercel list --environment=preview

# Filter by metadata
vercel list --meta commit=abc123
vercel list --meta branch=main

# Production deployments only
vercel list --prod
```

### Promote Deployments

```bash
# Promote deployment to production
vercel promote https://my-app-xyz123.vercel.app
vercel promote <deployment-id>

# Typical workflow: staged production deployment
vercel --prod --skip-domain > staging-url.txt
# Test the deployment
# If good, promote:
vercel promote $(cat staging-url.txt)
```

### Redeploy

```bash
# Redeploy existing deployment
vercel redeploy https://my-app-xyz123.vercel.app

# Rebuild with latest code
vercel redeploy <deployment-url>
```

### Rollback

```bash
# Rollback to previous production deployment
vercel rollback

# Rollback to specific deployment
vercel rollback https://my-app-xyz123.vercel.app
```

### Remove Deployments

```bash
# Remove specific deployment
vercel remove <deployment-url>
vercel rm <deployment-id>

# Remove with confirmation bypass
vercel remove <deployment-url> --yes
```

### Inspect Deployments

```bash
# Get detailed deployment information
vercel inspect <deployment-url>
vercel inspect <deployment-id>
```

## Domain Management

### List Domains

```bash
vercel domains ls
```

### Add Domain

```bash
# Add domain to current project
vercel domains add example.com

# Vercel will provide DNS configuration instructions
```

### Remove Domain

```bash
vercel domains rm example.com
```

### Inspect Domain

```bash
# Check domain configuration
vercel domains inspect example.com
```

### Aliases

```bash
# List aliases
vercel alias ls

# Set custom alias
vercel alias set <deployment-url> custom.example.com

# Remove alias
vercel alias rm custom.example.com
```

## DNS Management

### List DNS Records

```bash
vercel dns ls

# List for specific domain
vercel dns ls example.com
```

### Add DNS Records

```bash
# Add A record
vercel dns add example.com www A 76.76.21.21

# Add CNAME record
vercel dns add example.com blog CNAME myblog.vercel.app

# Add TXT record (for verification)
vercel dns add example.com @ TXT "verification-code-here"

# Add AAAA record (IPv6)
vercel dns add example.com @ AAAA 2001:0db8:85a3::8a2e:0370:7334

# Add ALIAS record
vercel dns add example.com @ ALIAS target.vercel.app
```

**Supported record types**: A, AAAA, ALIAS, CNAME, TXT

### Remove DNS Records

```bash
# Remove by subdomain
vercel dns rm example.com www

# Remove root domain record
vercel dns rm example.com @
```

## SSL Certificates

### List Certificates

```bash
vercel certs ls
```

### Issue Certificate

```bash
# Issue for single domain
vercel certs add example.com

# Issue for multiple domains (SAN certificate)
vercel certs add example.com www.example.com api.example.com
```

### Remove Certificate

```bash
vercel certs rm <cert-id>
```

**Note**: Vercel automatically manages SSL certificates for domains using Vercel nameservers. Manual certificate management is only needed for external DNS configurations.

## Logs & Monitoring

### Stream Logs

```bash
# Stream runtime logs for deployment
vercel logs <deployment-url>
vercel logs <deployment-id>

# Logs are followed automatically (up to 5 minutes)
```

### JSON Output for Parsing

```bash
# Output logs as JSON
vercel logs <deployment-url> --json

# Filter errors with jq
vercel logs <deployment-url> --json | jq 'select(.level == "error")'

# Extract specific fields
vercel logs <deployment-url> --json | jq '{timestamp: .timestamp, message: .message}'
```

### Build Logs

Build logs are shown during deployment with `--logs` flag:

```bash
vercel deploy --logs --prod
```

## Local Development

### Development Server

```bash
# Start local development server (uses vercel.json)
vercel dev

# Specify port
vercel dev --listen 3000

# Set environment variables
vercel dev --env NODE_ENV=development
```

### Build Locally

```bash
# Build project locally (creates .vercel/output)
vercel build

# Build for production environment
vercel build --prod

# Build for specific environment
vercel build --target=production

# Custom output directory
vercel build --output ./custom-output
```

### Deploy Prebuilt

```bash
# After building, deploy without rebuilding
vercel deploy --prebuilt --prod
```

## Team Management

### List Teams

```bash
vercel teams ls
```

### Switch Team Context

```bash
# Switch default team
vercel switch <team-slug>

# Execute command in team context
vercel --team=my-team deploy --prod
vercel -T team-id list

# Set scope
vercel --scope=my-team link
```

### Invite Team Members

**Note**: Team member management (roles, permissions) requires dashboard access. Use Vercel Dashboard for:
- Inviting members with specific roles
- Configuring member permissions
- Managing team settings

## Advanced Features

### Redirects Configuration

Configure via `vercel.json`:

```json
{
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "statusCode": 301
    },
    {
      "source": "/blog/:slug",
      "destination": "https://blog.example.com/:slug",
      "statusCode": 302
    }
  ]
}
```

### Headers Configuration

Configure via `vercel.json`:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ]
}
```

### Cron Jobs

Configure via `vercel.json`:

```json
{
  "crons": [
    {
      "path": "/api/cron/daily",
      "schedule": "0 5 * * *"
    },
    {
      "path": "/api/cron/hourly",
      "schedule": "0 * * * *"
    }
  ]
}
```

Protect cron endpoints:

```typescript
export async function GET(request: Request) {
  const authHeader = request.headers.get('authorization');
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new Response('Unauthorized', { status: 401 });
  }
  // Cron logic here
}
```

### Edge Config (Feature Flags)

**Note**: Edge Config creation and management requires dashboard access or Vercel API. Use Dashboard for:
- Creating Edge Config stores
- Managing feature flags
- Setting up A/B tests

Access Edge Config in code:

```typescript
import { get } from '@vercel/edge-config';

export async function middleware(request: Request) {
  const isFeatureEnabled = await get('feature-flag');
  // ...
}
```

## CI/CD Best Practices

### GitHub Actions Example

```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Vercel CLI
        run: npm install --global vercel@latest

      - name: Pull Vercel Environment Information
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build Project Artifacts
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy Project Artifacts to Vercel
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### Required Secrets

Create at: https://vercel.com/account/tokens

- `VERCEL_TOKEN` - Authentication token
- `VERCEL_ORG_ID` - Organization/team ID (found in `.vercel/project.json`)
- `VERCEL_PROJECT_ID` - Project ID (found in `.vercel/project.json`)

### Deployment Strategies

#### Strategy 1: Direct Production Deploy

```bash
vercel --prod --token $VERCEL_TOKEN
```

**Pros**: Simple, fast  
**Cons**: No testing window

#### Strategy 2: Staged Production Deploy

```bash
# Deploy without assigning production domain
vercel --prod --skip-domain --token $VERCEL_TOKEN > deployment-url.txt

# Run tests against staging URL
npm run e2e:test $(cat deployment-url.txt)

# If tests pass, promote
if [ $? -eq 0 ]; then
  vercel promote $(cat deployment-url.txt) --token $VERCEL_TOKEN
else
  echo "Tests failed, deployment not promoted"
  exit 1
fi
```

**Pros**: Safe, testable  
**Cons**: More complex

#### Strategy 3: Preview → Manual Promotion

```bash
# Deploy to preview
vercel --token $VERCEL_TOKEN > preview-url.txt

# Manual testing, then:
vercel promote $(cat preview-url.txt) --token $VERCEL_TOKEN
```

**Pros**: Maximum control  
**Cons**: Requires manual step

## Global Options

Available for all commands:

| Option | Description |
|--------|-------------|
| `--cwd <path>` | Set working directory |
| `--debug` / `-d` | Enable verbose output |
| `--global-config <dir>` / `-Q` | Path to global config |
| `--help` / `-h` | Show help |
| `--local-config <file>` / `-A` | Path to vercel.json |
| `--no-color` | Disable color output |
| `--scope <scope>` / `-S` | Team or user scope |
| `--token <token>` / `-t` | Auth token |
| `--team <team>` / `-T` | Team slug or ID |
| `--version` / `-v` | Show CLI version |
| `--yes` / `-y` | Skip confirmation prompts |

## Dashboard-Only Features

Some features require dashboard access:

- **Analytics**: View detailed analytics (no CLI equivalent)
- **Webhooks**: Configure deployment webhooks
- **Edge Config**: Create and manage Edge Config stores
- **Team Settings**: Advanced team permissions and roles
- **Billing**: Spending limits and payment settings
- **Log Drains**: Configure log forwarding
- **Protection Rules**: Advanced deployment protection

For these features, use the Vercel Dashboard or REST API (see `references/api-reference.md`).

## Common Workflows

### Initial Project Setup

```bash
# 1. Authenticate
vercel login

# 2. Link project
cd my-project
vercel link

# 3. Pull configuration
vercel pull --environment=production --yes

# 4. Deploy
vercel --prod
```

### Environment Variable Sync

```bash
# Development workflow
vercel env pull .env.local
# Edit .env.local locally
# When ready, push changes:
vercel env add NEW_VAR development < .env.local
vercel env add NEW_VAR production < .env.prod
```

### Zero-Downtime Deployment

```bash
# 1. Deploy without assigning production domain
vercel --prod --skip-domain > staging-url.txt

# 2. Run health checks
curl $(cat staging-url.txt)/api/health

# 3. If healthy, promote
vercel promote $(cat staging-url.txt)
```

### Emergency Rollback

```bash
# Quick rollback to previous deployment
vercel rollback

# Or rollback to specific deployment
vercel list --prod  # Find deployment ID
vercel rollback <deployment-id>
```

## Troubleshooting

### Authentication Issues

```bash
# Check current user
vercel whoami

# Re-authenticate
vercel logout
vercel login
```

### Deployment Failures

```bash
# Deploy with logs
vercel --logs --prod

# Check build output
vercel build --debug

# Inspect failed deployment
vercel inspect <deployment-id>
```

### Environment Variables Not Loading

```bash
# Pull latest environment variables
vercel env pull --environment=production --yes

# Verify variables are set
vercel env ls production

# Check that vercel.json is not overriding
cat vercel.json
```

### Domain Not Working

```bash
# Inspect domain configuration
vercel domains inspect example.com

# Check DNS records
vercel dns ls example.com

# Verify SSL certificate
vercel certs ls
```

## Version Information

**CLI Version**: 50.4.5  
**Skill Version**: 1.0.0  
**Last Updated**: 2026-01-17

## Additional Resources

- **Official Documentation**: https://vercel.com/docs/cli
- **API Reference**: See `references/api-reference.md`
- **Advanced Workflows**: See `references/advanced-workflows.md`
- **GitHub Actions**: https://github.com/vercel/actions
- **REST API**: https://vercel.com/docs/rest-api
