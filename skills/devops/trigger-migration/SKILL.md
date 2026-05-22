---
name: trigger-migration
description: Manually triggers the migration Lambda for deployed environments. Use when migrations need to be run outside of CI/CD.
allowed-tools: Bash(aws lambda invoke:*)
---

# Trigger Migration Lambda

Manually triggers database migrations in deployed environments.

## When to Use

- After manual SST deployment (without CI/CD)
- To re-run failed migrations
- Emergency migration fixes

## Commands

### Development
```bash
aws lambda invoke --function-name template-saas-api-migrate-lambda-dev /dev/null
```

### Production
```bash
aws lambda invoke --function-name template-saas-api-migrate-lambda-prod /dev/null
```

## Prerequisites

1. AWS CLI configured with correct profile/credentials
2. Lambda function deployed (via SST)
3. Database accessible from Lambda

## How It Works

The Migration Lambda:
1. Connects to PostgreSQL using `DbConnStr` secret
2. Runs Alembic migrations via `migration.sh`
3. Returns success/failure status

## Lambda Naming Convention

`{project}-api-migrate-lambda-{stage}`

For this project: `template-saas-api-migrate-lambda-{dev|prod}`

## Checking Migration Status

### View Lambda Logs
```bash
aws logs tail /aws/lambda/template-saas-api-migrate-lambda-dev --follow
```

### Check Current Migration
```bash
# Via Docker locally
docker compose exec back uv run alembic current

# In production, check Lambda logs
```

## CI/CD Integration

Normally, migrations run automatically in CI/CD:
1. Backend deploy job completes
2. Migrate job triggers Migration Lambda
3. Pipeline fails if migration fails

See `.github/workflows/deploy-backend.yml`.

## Manual Production Migration

For production migrations outside of CI/CD:
- Use `.github/workflows/migrate-production.yml`
- Requires typing "migrate-production" to confirm
- Creates audit trail in GitHub Actions

## Troubleshooting

### Lambda Timeout
- Check database connectivity
- Verify `DbConnStr` secret is set
- Check Lambda has VPC access if needed

### Migration Errors
- Check Lambda CloudWatch logs
- Verify migration files are correct
- Test locally first with Docker
