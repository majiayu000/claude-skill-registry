---
name: sst-deployment
description: Configure or update SST v3 infrastructure resources for AWS deployment. Use when adding new AWS resources, modifying Lambda configurations, or updating domain settings.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# SST Deployment Skill

This skill helps you configure and deploy infrastructure using SST v3 in `infra/`.

## When to Use This Skill

- Deploying applications to AWS
- Adding new Lambda functions or API routes
- Configuring environment variables per stage
- Setting up custom domains
- Adding AWS resources (S3, DynamoDB, etc.)
- Debugging deployment failures
- Managing multiple environments (dev, staging, prod)

## SST Architecture

```
infra/
├── sst.config.ts           # SST configuration
├── api.ts                  # API Lambda configuration
├── web.ts                  # Next.js web app configuration
├── dns.ts                  # Domain and DNS configuration
└── database.ts             # Database resources (optional)
```

## SST Configuration

### Main Config File

```typescript
// infra/sst.config.ts
import { SSTConfig } from "sst";
import { API } from "./api";
import { Web } from "./web";
import { DNS } from "./dns";

export default {
  config(_input) {
    return {
      name: "sgcarstrends",
      region: "ap-southeast-1", // Singapore
      profile: "default",
    };
  },
  stacks(app) {
    app.stack(DNS).stack(API).stack(Web);
  },
} satisfies SSTConfig;
```

## Environment Management

### Stage-Based Configuration

```typescript
// infra/sst.config.ts
export default {
  config(input) {
    return {
      name: "sgcarstrends",
      region: "ap-southeast-1",
      profile: input.stage === "production" ? "prod" : "default",
    };
  },
  stacks(app) {
    // Set default removal policy based on stage
    app.setDefaultRemovalPolicy(
      app.stage === "production" ? "retain" : "destroy"
    );

    app.stack(DNS).stack(API).stack(Web);
  },
} satisfies SSTConfig;
```

### Environment-Specific Settings

```typescript
// infra/api.ts
import { StackContext, Function } from "sst/constructs";

export function API({ stack, app }: StackContext) {
  const stage = app.stage;

  // Stage-specific configuration
  const config = {
    dev: {
      memory: 512,
      timeout: "30 seconds",
      runtime: "nodejs20.x",
    },
    staging: {
      memory: 1024,
      timeout: "60 seconds",
      runtime: "nodejs20.x",
    },
    production: {
      memory: 2048,
      timeout: "120 seconds",
      runtime: "nodejs20.x",
    },
  }[stage] || {
    memory: 512,
    timeout: "30 seconds",
    runtime: "nodejs20.x",
  };

  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    ...config,
    environment: {
      NODE_ENV: stage === "production" ? "production" : "development",
      DATABASE_URL: process.env.DATABASE_URL!,
      UPSTASH_REDIS_REST_URL: process.env.UPSTASH_REDIS_REST_URL!,
      UPSTASH_REDIS_REST_TOKEN: process.env.UPSTASH_REDIS_REST_TOKEN!,
    },
  });

  stack.addOutputs({
    ApiUrl: api.url,
  });

  return { api };
}
```

## Lambda Configuration

### API Lambda

```typescript
// infra/api.ts
import { StackContext, Function, use } from "sst/constructs";
import { DNS } from "./dns";

export function API({ stack, app }: StackContext) {
  const { hostedZone } = use(DNS);

  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    runtime: "nodejs20.x",
    architecture: "arm64", // Graviton2 - cheaper and faster
    memory: 1024,
    timeout: "60 seconds",
    nodejs: {
      esbuild: {
        minify: app.stage === "production",
        sourcemap: app.stage !== "production",
      },
    },
    environment: {
      DATABASE_URL: process.env.DATABASE_URL!,
      UPSTASH_REDIS_REST_URL: process.env.UPSTASH_REDIS_REST_URL!,
      UPSTASH_REDIS_REST_TOKEN: process.env.UPSTASH_REDIS_REST_TOKEN!,
      GOOGLE_GEMINI_API_KEY: process.env.GOOGLE_GEMINI_API_KEY!,
      QSTASH_TOKEN: process.env.QSTASH_TOKEN!,
      DISCORD_WEBHOOK_URL: process.env.DISCORD_WEBHOOK_URL!,
      TELEGRAM_BOT_TOKEN: process.env.TELEGRAM_BOT_TOKEN!,
      TELEGRAM_CHAT_ID: process.env.TELEGRAM_CHAT_ID!,
    },
    url: {
      // Custom domain for API
      domain: {
        domainName: `api.${app.stage === "production" ? "" : `${app.stage}.`}sgcarstrends.com`,
        hostedZone: hostedZone.zoneName,
      },
    },
  });

  stack.addOutputs({
    ApiUrl: api.url,
    ApiDomain: api.url,
  });

  return { api };
}
```

### Next.js Web App

```typescript
// infra/web.ts
import { StackContext, NextjsSite, use } from "sst/constructs";
import { DNS } from "./dns";

export function Web({ stack, app }: StackContext) {
  const { hostedZone } = use(DNS);

  const web = new NextjsSite(stack, "web", {
    path: "apps/web",
    buildCommand: "pnpm build",
    environment: {
      NEXT_PUBLIC_API_URL: `https://api.${app.stage === "production" ? "" : `${app.stage}.`}sgcarstrends.com`,
      DATABASE_URL: process.env.DATABASE_URL!,
      UPSTASH_REDIS_REST_URL: process.env.UPSTASH_REDIS_REST_URL!,
      UPSTASH_REDIS_REST_TOKEN: process.env.UPSTASH_REDIS_REST_TOKEN!,
    },
    customDomain: {
      domainName: app.stage === "production"
        ? "sgcarstrends.com"
        : `${app.stage}.sgcarstrends.com`,
      hostedZone: hostedZone.zoneName,
    },
  });

  stack.addOutputs({
    WebUrl: web.url,
    WebDomain: web.customDomainUrl,
  });

  return { web };
}
```

## DNS and Domains

### Hosted Zone Configuration

```typescript
// infra/dns.ts
import { StackContext } from "sst/constructs";
import * as route53 from "aws-cdk-lib/aws-route53";

export function DNS({ stack }: StackContext) {
  // Import existing hosted zone
  const hostedZone = route53.HostedZone.fromLookup(stack, "HostedZone", {
    domainName: "sgcarstrends.com",
  });

  stack.addOutputs({
    HostedZoneId: hostedZone.hostedZoneId,
    HostedZoneName: hostedZone.zoneName,
  });

  return { hostedZone };
}
```

### Domain Mapping

Environment-specific domains:
- **Production**: `sgcarstrends.com`, `api.sgcarstrends.com`
- **Staging**: `staging.sgcarstrends.com`, `api.staging.sgcarstrends.com`
- **Dev**: `dev.sgcarstrends.com`, `api.dev.sgcarstrends.com`

## Deployment Commands

### Deploy to Environments

```bash
# Development
pnpm deploy:dev
# or
cd infra && npx sst deploy --stage dev

# Staging
pnpm deploy:staging
# or
cd infra && npx sst deploy --stage staging

# Production
pnpm deploy:prod
# or
cd infra && npx sst deploy --stage production
```

### Deploy Specific Stack

```bash
# Deploy only API
cd infra && npx sst deploy --stage dev API

# Deploy only Web
cd infra && npx sst deploy --stage dev Web
```

### Remove Stack

```bash
# Remove dev stack
cd infra && npx sst remove --stage dev

# Remove specific stack
cd infra && npx sst remove --stage dev API
```

## Environment Variables

### Local Development

```bash
# .env.local (not committed)
DATABASE_URL=postgresql://...
UPSTASH_REDIS_REST_URL=https://...
UPSTASH_REDIS_REST_TOKEN=...
GOOGLE_GEMINI_API_KEY=...
QSTASH_TOKEN=...
```

### SST Secrets

Use SST secrets for sensitive values:

```bash
# Set secret for specific stage
npx sst secrets set DATABASE_URL "postgresql://..." --stage production

# List secrets
npx sst secrets list --stage production

# Remove secret
npx sst secrets remove DATABASE_URL --stage production
```

Access secrets in code:

```typescript
import { Config } from "sst/node/config";

export function handler() {
  const databaseUrl = Config.DATABASE_URL;
  // Use secret...
}
```

### Parameter Store

```typescript
// infra/api.ts
import { StringParameter } from "aws-cdk-lib/aws-ssm";

export function API({ stack }: StackContext) {
  // Store parameter
  const param = new StringParameter(stack, "DatabaseUrl", {
    parameterName: `/sgcarstrends/${stack.stage}/database-url`,
    stringValue: process.env.DATABASE_URL!,
  });

  const api = new Function(stack, "api", {
    handler: "apps/api/src/index.handler",
    environment: {
      DATABASE_URL: param.stringValue,
    },
  });
}
```

## Adding AWS Resources

### S3 Bucket

```typescript
// infra/storage.ts
import { StackContext, Bucket } from "sst/constructs";

export function Storage({ stack, app }: StackContext) {
  const bucket = new Bucket(stack, "uploads", {
    cors: [
      {
        allowedMethods: ["GET", "PUT", "POST", "DELETE", "HEAD"],
        allowedOrigins: ["*"],
        allowedHeaders: ["*"],
      },
    ],
  });

  stack.addOutputs({
    BucketName: bucket.bucketName,
  });

  return { bucket };
}
```

### DynamoDB Table

```typescript
// infra/database.ts
import { StackContext, Table } from "sst/constructs";

export function Database({ stack }: StackContext) {
  const table = new Table(stack, "sessions", {
    fields: {
      userId: "string",
      sessionId: "string",
    },
    primaryIndex: { partitionKey: "userId", sortKey: "sessionId" },
    timeToLiveAttribute: "expiresAt",
  });

  stack.addOutputs({
    TableName: table.tableName,
  });

  return { table };
}
```

### EventBridge Cron

```typescript
// infra/cron.ts
import { StackContext, Cron, use } from "sst/constructs";
import { API } from "./api";

export function Cron({ stack }: StackContext) {
  const { api } = use(API);

  new Cron(stack, "DataUpdateCron", {
    schedule: "rate(1 hour)",
    job: {
      function: {
        handler: "apps/api/src/cron/update-data.handler",
        environment: {
          API_URL: api.url,
        },
      },
    },
  });
}
```

## Debugging Deployments

### Check Deployment Status

```bash
# List all stacks
npx sst stacks list --stage dev

# Get stack info
npx sst stacks info API --stage dev
```

### View Logs

```bash
# Tail logs for API function
npx sst logs --stage dev --function api

# Tail logs with filter
npx sst logs --stage dev --function api --filter "ERROR"
```

### Console Access

```bash
# Open SST console
npx sst console --stage dev
```

### Check Outputs

```bash
# Get stack outputs
npx sst outputs --stage dev
```

## Common Issues

### Deployment Failures

**Issue**: Deployment fails with timeout
**Solution**: Increase Lambda timeout or check network issues

```typescript
const api = new Function(stack, "api", {
  timeout: "120 seconds", // Increase from 30s
});
```

**Issue**: Out of memory errors
**Solution**: Increase memory allocation

```typescript
const api = new Function(stack, "api", {
  memory: 2048, // Increase from 1024
});
```

**Issue**: Domain not working
**Solution**: Verify DNS propagation and Route53 configuration

```bash
# Check DNS records
dig sgcarstrends.com
dig api.sgcarstrends.com

# Check certificate status in AWS Console
```

### Environment Variable Issues

**Issue**: Environment variables not available
**Solution**: Check they're set in SST config

```typescript
environment: {
  DATABASE_URL: process.env.DATABASE_URL!,
  // Ensure all required vars are listed
}
```

**Issue**: Secrets not found
**Solution**: Set secrets for the correct stage

```bash
npx sst secrets set DATABASE_URL "value" --stage production
```

## Monitoring

### CloudWatch Metrics

SST automatically creates CloudWatch metrics for:
- Lambda invocations
- Errors
- Duration
- Throttles
- Concurrent executions

Access in AWS Console: CloudWatch → Metrics → Lambda

### Alarms

```typescript
// infra/monitoring.ts
import { StackContext, use } from "sst/constructs";
import { Alarm } from "aws-cdk-lib/aws-cloudwatch";
import { API } from "./api";

export function Monitoring({ stack }: StackContext) {
  const { api } = use(API);

  new Alarm(stack, "ApiErrorAlarm", {
    metric: api.metricErrors(),
    threshold: 10,
    evaluationPeriods: 1,
    alarmDescription: "Alert when API has more than 10 errors",
  });
}
```

## Cost Optimization

### Use ARM Architecture

```typescript
const api = new Function(stack, "api", {
  architecture: "arm64", // 20% cheaper than x86
});
```

### Appropriate Memory

```typescript
// Don't over-provision
const api = new Function(stack, "api", {
  memory: 1024, // Start here, adjust based on metrics
});
```

### Enable Minification

```typescript
const api = new Function(stack, "api", {
  nodejs: {
    esbuild: {
      minify: app.stage === "production",
    },
  },
});
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy-prod.yml
name: Deploy Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ap-southeast-1

      - name: Deploy to production
        run: pnpm deploy:prod
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          UPSTASH_REDIS_REST_URL: ${{ secrets.UPSTASH_REDIS_REST_URL }}
          UPSTASH_REDIS_REST_TOKEN: ${{ secrets.UPSTASH_REDIS_REST_TOKEN }}
```

## Rollback Strategy

### Rollback Deployment

```bash
# List recent deployments
aws cloudformation describe-stacks --stack-name sgcarstrends-api-production

# Rollback to previous version
npx sst deploy --stage production --rollback
```

### Manual Rollback

1. Identify last good deployment
2. Checkout that commit
3. Redeploy

```bash
git log --oneline
git checkout <commit-hash>
npx sst deploy --stage production
```

## Best Practices

### Resource Naming

```typescript
// ✅ Good - clear, scoped names
new Function(stack, "ApiHandler", { ... });
new Bucket(stack, "UserUploads", { ... });

// ❌ Bad - generic names
new Function(stack, "Function1", { ... });
new Bucket(stack, "Bucket", { ... });
```

### Environment Management

```typescript
// ✅ Good - environment-specific config
const config = getConfigForStage(app.stage);

// ❌ Bad - hardcoded values
const config = { memory: 1024 };
```

### Outputs

```typescript
// ✅ Good - add useful outputs
stack.addOutputs({
  ApiUrl: api.url,
  BucketName: bucket.bucketName,
});
```

## References

- SST Documentation: https://docs.sst.dev
- AWS CDK: https://docs.aws.amazon.com/cdk
- Related files:
  - `infra/` - All infrastructure code
  - `infra/CLAUDE.md` - Infrastructure documentation
  - Root CLAUDE.md - Project documentation

## Best Practices

1. **Use Stages**: Separate dev/staging/prod environments
2. **Secrets Management**: Use SST secrets for sensitive data
3. **Monitoring**: Set up CloudWatch alarms
4. **Cost Optimization**: Use ARM, appropriate memory
5. **Naming**: Use clear, descriptive resource names
6. **Outputs**: Export useful values for reference
7. **Removal Policy**: Retain production data
8. **Testing**: Test deployments in staging first
