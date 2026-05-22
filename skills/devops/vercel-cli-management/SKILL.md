---
name: vercel-cli-management
description: Manage Vercel deployments, projects, domains, and environment variables using Vercel CLI. Use when deploying Next.js applications, managing production/preview deployments, configuring custom domains, or troubleshooting Vercel-specific issues.
---

# Vercel CLI Management

Skill para gestionar despliegues, proyectos, dominios y variables de entorno en Vercel usando Vercel CLI. Proporciona patrones modernos y mejores prácticas para workflows de desarrollo y producción.

## When to Use This Skill

Use this skill when the user requests:

**Primary Use Cases**

- "Deploy to Vercel" or "Deploy my app"
- "Set up Vercel project" or "Link to Vercel"
- "Configure custom domain on Vercel"
- "Manage environment variables on Vercel"
- "View Vercel logs" or "Debug deployment"

**Secondary Use Cases**

- "Promote preview to production"
- "Remove/delete Vercel deployment"
- "Set up CI/CD with Vercel"
- "Switch Vercel team or scope"
- "Check Vercel project status"

**Do NOT use when**

- Managing environment variables sync (use [vercel-env-sync](../vercel-env-sync/SKILL.md) instead)
- Need automated env var validation (use [vercel-env-sync](../vercel-env-sync/SKILL.md))
- Working with Neon database (use [neon-database-management](../neon-database-management/SKILL.md))

## Prerequisites

### 1. Vercel CLI Installation

The CLI should be installed globally. Verify installation:

```bash
# Check if Vercel CLI is installed
vercel --version

# Expected output: Vercel CLI 37.x.x or higher
```

**If not installed**, install globally:

```bash
# npm
npm install -g vercel

```

**Alternative: Use npx (no installation needed)**

```bash
npx vercel --version
npx vercel --help
```

### 2. Authentication

Verify authentication status:

```bash
vercel whoami

# Output: your-username (success)
# Error: "Error! You must log in first" (needs login)
```

**Login if needed:**

```bash
# Interactive login (opens browser)
vercel login

# Or use token (CI/CD)
vercel login --token <YOUR_TOKEN>
```

### 3. Project Linking

Check if project is linked:

```bash
# Should show .vercel/project.json
ls .vercel/

# View linked project
cat .vercel/project.json
```

**Link if needed:**

```bash
vercel link
```

---

## Step-by-Step Instructions

### Step 1: Environment Verification

Before any Vercel operation, verify the environment:

```bash
# Complete verification script
vercel --version && vercel whoami && test -f .vercel/project.json && echo "Ready" || echo "Needs setup"
```

**Success criteria:**

- CLI version displayed (37.x.x+)
- Username shown (authenticated)
- `.vercel/project.json` exists (linked)

**Troubleshooting:**

- If "command not found": Install CLI (see Prerequisites)
- If "You must log in": Run `vercel login`
- If "No project linked": Run `vercel link`

### Step 2: Project Management

#### Initialize New Project

```bash
# In project directory (creates .vercel/project.json)
vercel

# Follow prompts:
# - Link to existing project? (Y/n)
# - Which scope? (personal/team)
# - Link to existing project or create new?
```

#### Link Existing Project

```bash
# Explicit link command
vercel link

# Force relink
vercel link --yes
```

#### List Projects

```bash
vercel project ls
```

#### Switch Team/Scope

```bash
# List available teams
vercel teams ls

# Switch to team
vercel switch <team-name>

# Or use --scope flag
vercel --scope <team-name> <command>
```

### Step 3: Deployments

#### Deploy to Preview (Default)

```bash
# Deploy current branch to preview URL
vercel

# Output: https://your-project-xxx.vercel.app
```

#### Deploy to Production

```bash
vercel --prod
```

#### Deploy with Options

```bash
# Force rebuild (skip cache)
vercel --force

# Deploy specific directory
vercel ./dist

# With message
vercel --message "Fix: authentication bug"
```

#### List Deployments

```bash
# Recent deployments
vercel ls

# With metadata
vercel ls --meta

# Filter by app
vercel ls <app-name>
```

#### Inspect Deployment

```bash
vercel inspect <deployment-url>

# Example
vercel inspect https://my-app-abc123.vercel.app
```

#### Promote Preview to Production

```bash
vercel promote <deployment-url>

# Example
vercel promote https://my-app-abc123.vercel.app
```

#### Remove Deployment

```bash
# Remove specific deployment
vercel remove <deployment-url>

# Force without confirmation
vercel remove <deployment-url> --yes

# Remove multiple
vercel remove <url1> <url2>
```

### Step 4: Environment Variables

> **Note**: For advanced env var management (sync, validation, audit), use [vercel-env-sync](../vercel-env-sync/SKILL.md).

#### List Variables

```bash
# All environments
vercel env ls

# Specific environment
vercel env ls production
vercel env ls preview
vercel env ls development
```

#### Add Variable

```bash
# Interactive (recommended for sensitive values)
vercel env add <NAME>

# Non-interactive (CI/CD)
echo "value" | vercel env add MY_VAR production

# Multiple environments
echo "value" | vercel env add MY_VAR production preview development

# Mark as sensitive
echo "secret" | vercel env add API_SECRET production --sensitive
```

#### Update Variable (Modern)

```bash
# Update existing variable (Vercel CLI 33+)
echo "new-value" | vercel env update MY_VAR production --yes

# Update with sensitive flag
echo "new-secret" | vercel env update API_SECRET production --sensitive --yes
```

#### Remove Variable

```bash
vercel env rm MY_VAR production

# Force without confirmation
vercel env rm MY_VAR production --yes
```

#### Pull Variables (Local Development)

```bash
# Pull development variables to .env.local
vercel env pull

# Pull specific environment
vercel env pull .env.production --environment=production

# Pull with git branch
vercel env pull .env.preview --environment=preview --git-branch=feature-x
```

⚠️ **IMPORTANT**: Add `.env*.local` to `.gitignore`

#### Run Commands with Vercel Env

```bash
# Run dev server with Vercel environment
vercel env run -- pnpm dev

# Run with specific environment
vercel env run -e production -- pnpm build

# Run tests with preview env
vercel env run -e preview -- pnpm test
```

### Step 5: Domains

#### List Domains

```bash
vercel domains ls
```

#### Add Domain

```bash
# Add domain to current project
vercel domains add example.com

# Add with project
vercel domains add example.com --project=my-project
```

#### Verify Domain

```bash
vercel domains inspect example.com

# Force re-verification
vercel domains verify example.com
```

#### Remove Domain

```bash
vercel domains rm example.com
```

#### Create Alias (Legacy)

```bash
# Assign custom domain to deployment
vercel alias set <deployment-url> example.com

# List aliases
vercel alias ls

# Remove alias
vercel alias rm example.com
```

### Step 6: Logs and Debugging

#### View Logs

```bash
# Production logs
vercel logs --prod

# Specific deployment
vercel logs <deployment-url>

# Follow (real-time)
vercel logs --prod --follow

# Filter by function
vercel logs --prod --function=api/hello

# Filter by status code
vercel logs --prod --status=500
```

#### Local Development

```bash
# Simulate Vercel environment locally
vercel dev

# With custom port
vercel dev --port 3001

# With specific env file
vercel dev --env .env.local
```

#### Local Build

```bash
# Build as Vercel would
vercel build

# Production build
vercel build --prod

# Deploy prebuilt
vercel deploy --prebuilt
```

---

## Advanced Usage

### CI/CD Integration

#### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install dependencies
        run: pnpm install

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}

      - name: Build Project
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy to Vercel
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

#### Required GitHub Secrets

```
VERCEL_TOKEN      # From https://vercel.com/account/tokens
VERCEL_ORG_ID     # From .vercel/project.json
VERCEL_PROJECT_ID # From .vercel/project.json
```

### vercel.json Configuration

#### Basic Structure

```json
{
  "version": 2,
  "name": "my-project",
  "framework": "nextjs",
  "buildCommand": "pnpm build",
  "devCommand": "pnpm dev",
  "installCommand": "pnpm install"
}
```

#### Redirects

```json
{
  "redirects": [
    {
      "source": "/old-path",
      "destination": "/new-path",
      "permanent": true
    },
    {
      "source": "/blog/:slug",
      "destination": "/news/:slug",
      "permanent": false
    }
  ]
}
```

#### Rewrites

```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.external.com/:path*"
    }
  ]
}
```

#### Headers

```json
{
  "headers": [
    {
      "source": "/api/:path*",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

---

## Examples

### Example 1: First-Time Project Setup

**User request**: "Set up my Next.js project on Vercel"

**Actions**:

```bash
# 1. Verify CLI
vercel --version

# 2. Login (if needed)
vercel login

# 3. Link project
vercel link

# 4. Deploy to preview
vercel

# 5. Deploy to production
vercel --prod
```

**Expected result**: Project deployed to Vercel with both preview and production URLs.

### Example 2: Deploy with Environment Variables

**User request**: "Deploy and set up env vars"

**Actions**:

```bash
# 1. Deploy
vercel --prod

# 2. Add environment variables
echo "https://myapp.com" | vercel env add NEXT_PUBLIC_APP_URL production
echo "secret-key" | vercel env add API_SECRET production --sensitive

# 3. Redeploy to apply env vars
vercel --prod
```

**Expected result**: App deployed with environment variables configured.

### Example 3: Promote Preview to Production

**User request**: "Make my preview deployment live"

**Actions**:

```bash
# 1. List recent deployments
vercel ls

# 2. Promote specific deployment to production
vercel promote https://my-app-abc123.vercel.app

# Or simply redeploy current to production
vercel --prod
```

**Expected result**: Preview deployment now serves production traffic.

### Example 4: Debug Failed Deployment

**User request**: "My deployment failed, help me debug"

**Actions**:

```bash
# 1. Get deployment URL from recent deployments
vercel ls

# 2. View logs
vercel logs <deployment-url>

# 3. Inspect deployment details
vercel inspect <deployment-url>

# 4. Try local build with Vercel env
vercel env pull .env.local
vercel build
```

**Expected result**: Root cause identified from logs or build output.

---

## Error Handling

### Common Errors

| Error                            | Cause                        | Solution                                          |
| -------------------------------- | ---------------------------- | ------------------------------------------------- |
| `command not found: vercel`      | CLI not installed            | `npm install -g vercel` or use `npx vercel`       |
| `You must log in`                | Not authenticated            | `vercel login`                                    |
| `No project linked`              | Missing .vercel/project.json | `vercel link`                                     |
| `Project not found`              | Wrong scope or project name  | `vercel switch <team>` or `vercel --scope <team>` |
| `Environment variable not found` | Variable not set             | `vercel env add VAR_NAME production`              |
| `Build failed`                   | Build error in code          | Check `vercel logs`, test `vercel build` locally  |
| `Domain already in use`          | Domain assigned elsewhere    | Remove from other project first                   |

### Debugging Tips

```bash
# Enable verbose output
vercel --debug <command>

# Check authentication
vercel whoami && vercel teams ls

# Verify project config
cat .vercel/project.json

# Test build locally
vercel build

# Check all env vars
vercel env ls
```

---

## Best Practices

### DO

1. **Verify CLI installation** before operations
2. **Use `vercel env run`** for local development with latest env vars
3. **Test with `vercel build`** locally before deploying
4. **Use preview deployments** for testing before production
5. **Add `.vercel/` to `.gitignore`** (except project.json if team-shared)
6. **Use `--yes` flag** in CI/CD to skip prompts
7. **Document env vars** in `.env.example`
8. **Use `vercel env update`** instead of rm+add pattern

### DON'T

1. **Don't commit secrets** in `vercel.json`
2. **Don't share `VERCEL_TOKEN`** publicly
3. **Don't deploy directly to production** without testing
4. **Don't use deprecated `vercel secrets`** (use `vercel env`)
5. **Don't ignore failed builds** - check logs immediately

---

## Quick Reference

### Essential Commands

```bash
# Verify setup
vercel --version && vercel whoami

# Deploy
vercel              # Preview
vercel --prod       # Production

# Environment
vercel env ls                              # List all vars
vercel env add NAME production             # Add var
vercel env update NAME production --yes    # Update var
vercel env pull                            # Pull to .env.local
vercel env run -- pnpm dev                 # Run with Vercel env

# Logs
vercel logs --prod          # Production logs
vercel logs --prod --follow # Real-time logs

# Domains
vercel domains ls                    # List domains
vercel domains add example.com       # Add domain
vercel alias set <url> example.com   # Create alias

# Project
vercel link                 # Link project
vercel inspect              # Inspect current deployment
vercel ls                   # List deployments
vercel remove <url>         # Remove deployment
```

### NPM Scripts

```json
{
  "scripts": {
    "deploy": "vercel",
    "deploy:prod": "vercel --prod",
    "env:pull": "vercel env pull .env.local",
    "env:ls": "vercel env ls",
    "logs": "vercel logs --prod",
    "vercel:build": "vercel build",
    "vercel:dev": "vercel dev"
  }
}
```

---

## Related Skills

- **[vercel-env-sync](../vercel-env-sync/SKILL.md)** - Advanced environment variable synchronization
- **[neon-database-management](../neon-database-management/SKILL.md)** - Neon database integration with Vercel
- **[nextjs16-proxy-middleware](../nextjs16-proxy-middleware/SKILL.md)** - Middleware configuration

---

## Resources

- [Vercel CLI Documentation](https://vercel.com/docs/cli)
- [Environment Variables](https://vercel.com/docs/environment-variables)
- [Deploying with Git](https://vercel.com/docs/deployments/git)
- [Vercel REST API](https://vercel.com/docs/rest-api)
- [Agent Skills Standard](https://agentskills.io/)

---

**Last Updated**: January 31, 2026  
**Version**: 3.0  
**Compatibility**: Vercel CLI 37.0+, Node.js 18+
