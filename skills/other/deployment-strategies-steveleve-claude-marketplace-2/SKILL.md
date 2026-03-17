---
name: Deployment Strategies
description: This skill should be used when the user asks about "deployment", "CI/CD", "continuous integration", "GitHub Actions", "GitLab CI", "environments", "staging", "production", "rollback", "versioning", "gradual rollout", "canary deployment", "blue-green deployment", or discusses deploying Workers, managing multiple environments, or setting up automated deployment pipelines.
version: 0.1.0
---

# Deployment Strategies

## Purpose

This skill provides guidance on deploying Cloudflare Workers, managing multiple environments, implementing CI/CD pipelines, and using deployment best practices. Use this skill when setting up deployment workflows, managing staging and production environments, implementing rollback strategies, or integrating with CI/CD systems.

## Environment Management

### Multi-Environment Configuration

Use wrangler.jsonc environments for staging/production separation:

```jsonc
{
  "name": "my-worker",
  "main": "src/index.ts",

  // Production configuration (default)
  "vars": {
    "ENVIRONMENT": "production"
  },
  "kv_namespaces": [
    { "binding": "CACHE", "id": "prod-kv-id" }
  ],

  // Environment-specific overrides
  "env": {
    "staging": {
      "vars": { "ENVIRONMENT": "staging" },
      "kv_namespaces": [
        { "binding": "CACHE", "id": "staging-kv-id" }
      ]
    },
    "development": {
      "vars": { "ENVIRONMENT": "development" },
      "kv_namespaces": [
        { "binding": "CACHE", "id": "dev-kv-id" }
      ]
    }
  }
}
```

Deploy to specific environment:
```bash
wrangler deploy --env staging
wrangler deploy --env production
```

### Best Practices

1. **Separate resources**: Use different KV namespaces, D1 databases, R2 buckets per environment
2. **Environment variables**: Use `ENVIRONMENT` var to conditionally enable features
3. **Secrets per environment**: `wrangler secret put API_KEY --env staging`
4. **Test in staging**: Always deploy to staging before production
5. **Monitor after deploy**: Use `wrangler tail --env production` after deployment

## CI/CD Integration

### GitHub Actions

**`.github/workflows/deploy.yml`:**
```yaml
name: Deploy Worker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    name: Deploy
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Deploy to staging
        if: github.event_name == 'pull_request'
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: \${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy --env staging

      - name: Deploy to production
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: \${{ secrets.CLOUDFLARE_API_TOKEN }}
          command: deploy --env production
```

**Setup**:
1. Add `CLOUDFLARE_API_TOKEN` to GitHub Secrets
2. Get token from Cloudflare Dashboard → My Profile → API Tokens
3. Create token with "Edit Cloudflare Workers" permissions

### GitLab CI

**`.gitlab-ci.yml`:**
```yaml
stages:
  - test
  - deploy

variables:
  NODE_VERSION: "20"

test:
  stage: test
  image: node:\${NODE_VERSION}
  script:
    - npm ci
    - npm test

deploy_staging:
  stage: deploy
  image: node:\${NODE_VERSION}
  only:
    - merge_requests
  script:
    - npm ci
    - npx wrangler deploy --env staging
  variables:
    CLOUDFLARE_API_TOKEN: \$CLOUDFLARE_API_TOKEN

deploy_production:
  stage: deploy
  image: node:\${NODE_VERSION}
  only:
    - main
  script:
    - npm ci
    - npx wrangler deploy --env production
  variables:
    CLOUDFLARE_API_TOKEN: \$CLOUDFLARE_API_TOKEN
```

## Deployment Workflows

### Pre-Deployment Checklist

```bash
# 1. Run tests
npm test

# 2. Build (if applicable)
npm run build

# 3. Validate configuration
wrangler deploy --dry-run --env production

# 4. Check migrations (D1)
wrangler d1 migrations list DB --remote

# 5. Deploy to staging first
wrangler deploy --env staging

# 6. Test staging
curl https://staging.example.com/health

# 7. Deploy to production
wrangler deploy --env production

# 8. Monitor logs
wrangler tail --env production
```

### Post-Deployment

```bash
# Monitor real-time logs
wrangler tail --env production

# Check for errors
wrangler tail --env production --status error

# Verify deployment
curl https://production.example.com/health

# Check deployment history
wrangler deployments list
```

## Rollback Strategies

### Quick Rollback

```bash
# List recent deployments
wrangler deployments list

# Rollback to previous deployment
wrangler rollback <deployment-id>

# Verify rollback
wrangler deployments list
```

### Version Pinning

```javascript
// Add version to response headers
export default {
  async fetch(request, env) {
    const response = await handleRequest(request, env);
    response.headers.set('X-Worker-Version', env.VERSION || 'unknown');
    return response;
  }
};
```

Set version in wrangler.jsonc:
```jsonc
{
  "vars": {
    "VERSION": "1.2.3"
  }
}
```

### Canary Deployments

Not natively supported; use percentage-based routing:

```javascript
export default {
  async fetch(request, env) {
    const random = Math.random();

    // 10% canary traffic
    if (random < 0.1) {
      return await newVersionHandler(request, env);
    }

    return await stableVersionHandler(request, env);
  }
};
```

## Database Migrations

### D1 Migration Workflow

```bash
# 1. Create migration
wrangler d1 migrations create DB add_users_table

# 2. Write SQL in migrations/0001_add_users_table.sql
#    CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);

# 3. Apply locally
wrangler d1 migrations apply DB

# 4. Test locally
wrangler dev

# 5. Apply to staging
wrangler d1 migrations apply DB --env staging --remote

# 6. Test staging
# ... test ...

# 7. Apply to production
wrangler d1 migrations apply DB --env production --remote

# 8. Deploy Worker
wrangler deploy --env production
```

**Important**: Always apply migrations before deploying Worker code that depends on them.

## Secrets Management

### Deployment Secrets

```bash
# Set secrets per environment
wrangler secret put API_KEY --env staging
wrangler secret put API_KEY --env production

# Different values per environment
wrangler secret put DATABASE_URL --env staging
# Enter staging database URL

wrangler secret put DATABASE_URL --env production
# Enter production database URL

# List secrets
wrangler secret list --env production
```

### Secret Rotation

```bash
# 1. Add new secret with different name
wrangler secret put API_KEY_NEW --env production

# 2. Update Worker code to try new secret first, fall back to old
# 3. Deploy updated Worker
wrangler deploy --env production

# 4. Verify new secret works
# 5. Delete old secret
wrangler secret delete API_KEY --env production
```

## Monitoring and Observability

### Real-Time Monitoring

```bash
# All logs
wrangler tail --env production

# Errors only
wrangler tail --env production --status error

# Specific method
wrangler tail --env production --method POST

# Search logs
wrangler tail --env production --search "user-id-123"
```

### Health Checks

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === '/health') {
      // Check dependencies
      try {
        await env.DB.prepare('SELECT 1').first();
        await env.CACHE.get('health-check');

        return new Response(JSON.stringify({
          status: 'healthy',
          version: env.VERSION,
          environment: env.ENVIRONMENT
        }), {
          headers: { 'Content-Type': 'application/json' }
        });
      } catch (error) {
        return new Response(JSON.stringify({
          status: 'unhealthy',
          error: error.message
        }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

    // Regular request handling
    return await handleRequest(request, env);
  }
};
```

## Best Practices

1. **Always test in staging** before production
2. **Use semantic versioning** for releases
3. **Automate deployments** with CI/CD
4. **Monitor after every deployment**
5. **Have rollback plan** ready
6. **Apply database migrations** before code
7. **Use environment-specific resources**
8. **Keep secrets out of code** (use wrangler secret)
9. **Tag releases** in git for tracking
10. **Document deployment process**

## Troubleshooting

**Issue**: "Deployment failed - binding not found"
- **Solution**: Ensure all bindings (KV, D1, R2) are created and IDs match wrangler.jsonc

**Issue**: "Migration failed"
- **Solution**: Check SQL syntax, ensure migrations run in order, verify database exists

**Issue**: "Secrets not working after deployment"
- **Solution**: Re-set secrets after creating new environment: `wrangler secret put KEY --env ENV`

**Issue**: "Changes not reflecting"
- **Solution**: Clear browser cache, check deployment logs, verify correct environment deployed

For the latest deployment documentation, use the cloudflare-docs-specialist agent.
