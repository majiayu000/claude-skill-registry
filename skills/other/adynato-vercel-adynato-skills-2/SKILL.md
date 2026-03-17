---
name: adynato-vercel
description: Vercel deployment and configuration for Adynato projects. Covers environment variables, vercel.json, project linking, common errors like VERCEL_ORG_ID/VERCEL_PROJECT_ID, and CI/CD setup. Use when deploying to Vercel, configuring builds, or troubleshooting deployment issues.
---

# Vercel Skill

Use this skill when deploying Adynato projects to Vercel or troubleshooting deployment issues.

## Common Errors

### VERCEL_ORG_ID and VERCEL_PROJECT_ID

```
Error: You specified `VERCEL_ORG_ID` but you forgot to specify `VERCEL_PROJECT_ID`.
You need to specify both to deploy to a custom project.
```

**Fix:** Both environment variables must be set together:

```bash
# Get these from Vercel dashboard or .vercel/project.json
export VERCEL_ORG_ID="team_xxxxxx"
export VERCEL_PROJECT_ID="prj_xxxxxx"
```

Or in CI (GitHub Actions):

```yaml
env:
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
```

**Finding your IDs:**

```bash
# After linking a project, check .vercel/project.json
cat .vercel/project.json
# {"orgId":"team_xxx","projectId":"prj_xxx"}
```

### Project Not Linked

```
Error: Your codebase isn't linked to a project on Vercel.
```

**Fix:**

```bash
# Interactive linking
vercel link

# Or with flags for CI
vercel link --yes --project=my-project --scope=my-team
```

### Build Command Failed

```
Error: Command "npm run build" exited with 1
```

**Debug steps:**

1. Check build logs in Vercel dashboard
2. Run build locally: `npm run build`
3. Check for missing environment variables
4. Verify Node.js version matches (`engines` in package.json)

### Environment Variable Not Found

```
Error: Environment variable "DATABASE_URL" not found
```

**Fix:** Add to Vercel dashboard or via CLI:

```bash
# Add single variable
vercel env add DATABASE_URL production

# Pull all env vars locally
vercel env pull .env.local
```

## Project Configuration

### vercel.json

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install",
  "framework": "nextjs",
  "regions": ["iad1"],
  "functions": {
    "app/api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Access-Control-Allow-Origin", "value": "*" }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/blog/:slug",
      "destination": "/posts/:slug"
    }
  ]
}
```

### Framework Presets

Vercel auto-detects, but you can override:

| Framework | `framework` value | Output Directory |
|-----------|-------------------|------------------|
| Next.js | `nextjs` | `.next` |
| Remix | `remix` | `build` |
| Astro | `astro` | `dist` |
| Vite | `vite` | `dist` |
| Create React App | `create-react-app` | `build` |

## Environment Variables

### Scopes

| Scope | When Used |
|-------|-----------|
| `production` | Production deployments (main branch) |
| `preview` | Preview deployments (PRs, other branches) |
| `development` | Local development (`vercel dev`) |

### Managing Env Vars

```bash
# Add variable to all environments
vercel env add SECRET_KEY

# Add to specific environment
vercel env add SECRET_KEY production

# List all variables
vercel env ls

# Remove variable
vercel env rm SECRET_KEY production

# Pull to local .env file
vercel env pull .env.local
```

### Sensitive vs Plain

- **Sensitive:** Encrypted, not visible in dashboard after creation
- **Plain:** Visible, editable in dashboard

```bash
# Add as sensitive (default for secrets)
vercel env add DATABASE_URL --sensitive
```

## CLI Commands

### Deployment

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# Deploy without prompts (CI)
vercel --yes --prod

# Deploy with specific env
vercel --env NODE_ENV=production
```

### Project Management

```bash
# Link to existing project
vercel link

# List projects
vercel projects ls

# Remove project
vercel projects rm my-project

# List deployments
vercel ls

# Inspect deployment
vercel inspect <deployment-url>

# View logs
vercel logs <deployment-url>

# Rollback
vercel rollback <deployment-url>
```

### Domains

```bash
# Add domain
vercel domains add example.com

# List domains
vercel domains ls

# Remove domain
vercel domains rm example.com

# Add domain to project
vercel alias <deployment-url> example.com
```

## CI/CD with GitHub Actions

### Basic Deployment

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

      - name: Install Vercel CLI
        run: npm install -g vercel

      - name: Pull Vercel Environment
        run: vercel pull --yes --environment=production --token=${{ secrets.VERCEL_TOKEN }}
        env:
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

      - name: Build
        run: vercel build --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy
        run: vercel deploy --prebuilt --prod --token=${{ secrets.VERCEL_TOKEN }}
```

### Preview on PR

```yaml
- name: Deploy Preview
  if: github.event_name == 'pull_request'
  run: |
    url=$(vercel deploy --prebuilt --token=${{ secrets.VERCEL_TOKEN }})
    echo "Preview URL: $url"
```

## Monorepo Setup

### Root vercel.json for Monorepo

```json
{
  "projects": [
    { "src": "apps/web", "use": "@vercel/next" },
    { "src": "apps/api", "use": "@vercel/node" }
  ]
}
```

### Deploying Specific App

```bash
# Set root directory in project settings or:
vercel --cwd apps/web
```

### Turborepo Integration

```bash
# vercel.json at root
{
  "buildCommand": "cd ../.. && npx turbo run build --filter=web",
  "installCommand": "cd ../.. && npm install"
}
```

## Troubleshooting

### Check Deployment Status

```bash
# List recent deployments
vercel ls

# Get deployment details
vercel inspect <url>

# Stream logs
vercel logs <url> --follow
```

### Function Timeouts

Default is 10s for Hobby, 60s for Pro. Increase in vercel.json:

```json
{
  "functions": {
    "app/api/slow-endpoint/route.ts": {
      "maxDuration": 60
    }
  }
}
```

### Memory Issues

```json
{
  "functions": {
    "app/api/heavy-compute/route.ts": {
      "memory": 3008
    }
  }
}
```

### Build Cache Issues

```bash
# Force rebuild without cache
vercel --force
```

Or in dashboard: Deployments → Redeploy → "Redeploy with existing Build Cache" unchecked.
