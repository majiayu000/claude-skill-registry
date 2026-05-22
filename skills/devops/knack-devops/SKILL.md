---
name: Knack DevOps
description: Manages automated build, deployment, environment sync, and monitoring for HTI's Knack-Vercel integration. Ensures dashboard uptime, data sync relia...
allowed-tools: Read
---

# Knack DevOps

## Purpose
Manages automated build, deployment, environment sync, and monitoring for HTI's Knack-Vercel integration. Ensures dashboard uptime, data sync reliability, and performance optimization.

## Core Functions

### trigger_vercel_build
**Purpose**: Programmatically deploy updated dashboard code

**Parameters**:
- `vercel_url` (string, optional): Deployment URL (default: production)
- `trigger` (string, optional): "push" | "webhook" | "api" (default: "api")

**Example**:
```javascript
const deployment = await trigger_vercel_build({
  vercel_url: process.env.VERCEL_PROJECT_URL,
  trigger: "api"
});

// Output:
// {
//   deployment_id: "dpl_abc123",
//   status: "building",
//   url: "https://hubdash-git-main.vercel.app",
//   estimated_completion: "2025-04-15T14:35:00Z"
// }
```

**Implementation**:
```javascript
import { Vercel } from '@vercel/sdk';

async function trigger_vercel_build({ vercel_url }) {
  const vercel = new Vercel({ bearerToken: process.env.VERCEL_TOKEN });

  const deployment = await vercel.deployments.create({
    name: 'hubdash',
    gitSource: {
      type: 'github',
      ref: 'main'
    }
  });

  return {
    deployment_id: deployment.id,
    status: deployment.status,
    url: deployment.url
  };
}
```

### monitor_latency
**Purpose**: Track API and dashboard response times

**Parameters**:
- `api_url` (string, required): Endpoint to monitor
- `interval_seconds` (integer, optional): Check frequency (default: 300 = 5 min)
- `alert_threshold_ms` (integer, optional): Latency threshold for alerts (default: 2000)

**Example**:
```javascript
const monitor = await monitor_latency({
  api_url: "https://hubdash.vercel.app/api/metrics",
  interval_seconds: 300,
  alert_threshold_ms: 2000
});
```

**Implementation**:
```javascript
import axios from 'axios';

async function monitor_latency({ api_url, interval_seconds, alert_threshold_ms }) {
  setInterval(async () => {
    const start = Date.now();

    try {
      await axios.get(api_url);
      const latency = Date.now() - start;

      console.log(`Latency: ${latency}ms`);

      if (latency > alert_threshold_ms) {
        await alert_team({
          severity: "warning",
          message: `Dashboard latency high: ${latency}ms (threshold: ${alert_threshold_ms}ms)`
        });
      }

      // Log to metrics system
      await log_metric({
        metric: "api_latency",
        value: latency,
        timestamp: new Date()
      });
    } catch (error) {
      await alert_team({
        severity: "critical",
        message: `Dashboard unreachable: ${api_url}`,
        error: error.message
      });
    }
  }, interval_seconds * 1000);
}
```

### sync_environment
**Purpose**: Keep Knack credentials and config in sync across environments

**Environments**:
- **Development**: Local testing with sandbox Knack instance
- **Staging**: Pre-production testing with production data copy
- **Production**: Live HTI dashboard with real grant data

**Example**:
```javascript
await sync_environment({
  source: "production",
  target: "staging",
  include: ["knack_credentials", "api_endpoints"],
  exclude: ["user_tokens", "sensitive_keys"]
});
```

**Implementation**:
```javascript
async function sync_environment({ source, target, include, exclude }) {
  // Fetch config from source
  const source_config = await get_env_config(source);

  // Filter based on include/exclude
  const filtered_config = Object.keys(source_config)
    .filter(key => include.includes(key) && !exclude.includes(key))
    .reduce((obj, key) => {
      obj[key] = source_config[key];
      return obj;
    }, {});

  // Apply to target environment
  await update_env_config(target, filtered_config);

  return {
    synced_keys: Object.keys(filtered_config),
    source: source,
    target: target
  };
}
```

### automated_backup
**Purpose**: Regular backups of Knack data for disaster recovery

**Example**:
```javascript
// Daily backup of all Knack objects
cron.schedule('0 2 * * *', async () => {
  const backup = await automated_backup({
    objects: ["object_1", "object_2", "object_training"],
    destination: "s3://hti-backups/knack",
    retention_days: 90
  });

  console.log(`Backup complete: ${backup.records_backed_up} records`);
});
```

**Implementation**:
```javascript
import AWS from 'aws-sdk';

async function automated_backup({ objects, destination, retention_days }) {
  const s3 = new AWS.S3();
  const timestamp = new Date().toISOString().split('T')[0];
  let total_records = 0;

  for (const object_key of objects) {
    // Fetch all records
    const records = await fetch_all_pages(object_key);
    total_records += records.length;

    // Save to S3
    await s3.putObject({
      Bucket: 'hti-backups',
      Key: `knack/${object_key}_${timestamp}.json`,
      Body: JSON.stringify(records, null, 2),
      ContentType: 'application/json'
    }).promise();
  }

  // Clean up old backups (>90 days)
  await cleanup_old_backups({ bucket: 'hti-backups', retention_days });

  return { records_backed_up: total_records, timestamp };
}
```

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy HTI Dashboard

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Validate Knack connection
        run: npm run test:knack-api
        env:
          KNACK_APP_ID: ${{ secrets.KNACK_APP_ID }}
          KNACK_API_KEY: ${{ secrets.KNACK_API_KEY }}

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'

      - name: Notify deployment
        run: |
          curl -X POST https://hooks.slack.com/services/${{ secrets.SLACK_WEBHOOK }} \
          -d '{"text": "✅ HTI Dashboard deployed to production"}'
```

### Pre-Deployment Checks
```javascript
async function pre_deployment_checks() {
  const checks = {
    knack_api: await test_knack_connection(),
    data_integrity: await validate_production_data(),
    cache_warm: await warm_cache(),
    env_vars: await verify_env_vars(),
    build_size: await check_bundle_size()
  };

  const all_passed = Object.values(checks).every(c => c.passed);

  if (!all_passed) {
    throw new Error(`Pre-deployment checks failed: ${JSON.stringify(checks)}`);
  }

  return checks;
}

// Run before every production deploy
async function test_knack_connection() {
  try {
    const response = await get_records("object_1", { rows_per_page: 1 });
    return { passed: true, message: "Knack API accessible" };
  } catch (error) {
    return { passed: false, message: `Knack API error: ${error.message}` };
  }
}
```

## Monitoring & Alerting

### Uptime Monitoring
```javascript
// Use Vercel Analytics or external service (Pingdom, UptimeRobot)
async function setup_uptime_monitoring() {
  // Vercel Analytics (automatic)
  // https://vercel.com/docs/analytics

  // Or external monitoring
  const monitor = await createUptimeCheck({
    url: "https://hubdash.vercel.app",
    interval: 300, // 5 minutes
    alert_contacts: ["admin@hubzonetech.org"]
  });

  return monitor;
}
```

### Error Tracking
```javascript
// Sentry integration
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV,
  tracesSampleRate: 1.0,

  beforeSend(event) {
    // Don't send test data errors
    if (event.request?.url?.includes('localhost')) {
      return null;
    }
    return event;
  }
});

// Log Knack API errors
try {
  await get_records("object_1");
} catch (error) {
  Sentry.captureException(error, {
    tags: { service: "knack_api" },
    extra: { object_key: "object_1" }
  });
}
```

### Performance Monitoring
```javascript
// Web Vitals tracking
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

function send_to_analytics(metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    id: metric.id
  });

  fetch('/api/analytics', { method: 'POST', body });
}

getCLS(send_to_analytics);
getFID(send_to_analytics);
getFCP(send_to_analytics);
getLCP(send_to_analytics);
getTTFB(send_to_analytics);
```

## Environment Management

### Development Environment
```bash
# .env.development
KNACK_APP_ID=dev_app_id
KNACK_API_KEY=dev_api_key
VERCEL_ENV=development
CACHE_TTL=30 # Shorter cache for testing
DEBUG_MODE=true
```

### Production Environment
```bash
# .env.production (in Vercel dashboard)
KNACK_APP_ID=prod_app_id
KNACK_API_KEY=prod_api_key
VERCEL_ENV=production
CACHE_TTL=300 # 5 minutes
DEBUG_MODE=false
SENTRY_DSN=https://...
```

### Secrets Management
```javascript
// Store secrets in Vercel Environment Variables
// Never commit secrets to Git

// Access in code:
const knack_api_key = process.env.KNACK_API_KEY;

// Rotate secrets quarterly (align with grant reporting)
async function rotate_secrets() {
  // 1. Generate new API key in Knack dashboard
  // 2. Update Vercel environment variables
  // 3. Trigger redeployment
  // 4. Verify new keys work
  // 5. Revoke old keys
}
```

## Performance Optimization

### Bundle Size Analysis
```javascript
// Run during CI/CD
import { readFileSync } from 'fs';

async function check_bundle_size() {
  const bundle_stats = JSON.parse(readFileSync('.next/analyze/client.json'));

  const total_size = bundle_stats.reduce((sum, bundle) => sum + bundle.size, 0);
  const max_size = 1_000_000; // 1MB

  if (total_size > max_size) {
    console.warn(`Bundle size ${total_size} exceeds ${max_size}`);
    return { passed: false, size: total_size };
  }

  return { passed: true, size: total_size };
}
```

### Cache Warming
```javascript
// Warm cache after deployment
async function warm_cache() {
  const critical_endpoints = [
    "/api/metrics",
    "/api/county-breakdown",
    "/api/quarterly-report"
  ];

  for (const endpoint of critical_endpoints) {
    await fetch(`https://hubdash.vercel.app${endpoint}`);
  }

  return { warmed: critical_endpoints.length };
}
```

## Disaster Recovery

### Database Recovery
```javascript
async function restore_from_backup({ backup_date, objects }) {
  const s3 = new AWS.S3();

  for (const object_key of objects) {
    // Fetch backup
    const backup = await s3.getObject({
      Bucket: 'hti-backups',
      Key: `knack/${object_key}_${backup_date}.json`
    }).promise();

    const records = JSON.parse(backup.Body.toString());

    // Restore to Knack (batch insert)
    console.log(`Restoring ${records.length} records to ${object_key}`);
    // Implementation depends on Knack's batch API
  }
}
```

### Rollback Procedure
```javascript
// Rollback to previous Vercel deployment
async function rollback_deployment() {
  const vercel = new Vercel({ bearerToken: process.env.VERCEL_TOKEN });

  // Get previous deployment
  const deployments = await vercel.deployments.list({
    projectId: process.env.VERCEL_PROJECT_ID,
    limit: 2
  });

  const previous = deployments[1];

  // Promote to production
  await vercel.deployments.update(previous.id, {
    target: 'production'
  });

  console.log(`Rolled back to ${previous.id}`);
}
```

## Integration Points

- **knack_reader**: Monitor API health
- **knack_cache_optimizer**: Cache invalidation on deploy
- **knack_realtime**: Webhook endpoint health checks
- **knack_reporting_sync**: Automated report generation triggers
- **knack_dashboard_ai**: Performance metrics collection

## Best Practices

1. **Automate everything**: No manual deployments
2. **Test before deploy**: CI/CD checks gate production
3. **Monitor continuously**: Uptime + performance + errors
4. **Backup daily**: 90-day retention
5. **Document runbooks**: Incident response procedures
6. **Rotate secrets quarterly**: Align with grant reporting cycle

## Incident Response

### Runbook: Dashboard Down
1. Check Vercel status page
2. Verify Knack API connectivity
3. Review recent deployments
4. Check error logs in Sentry
5. If needed, rollback deployment
6. Notify stakeholders
7. Post-incident review

### Runbook: Slow Dashboard
1. Check API latency metrics
2. Review cache hit rates
3. Analyze bundle size
4. Check Knack rate limits
5. Optimize queries if needed
6. Consider CDN configuration
