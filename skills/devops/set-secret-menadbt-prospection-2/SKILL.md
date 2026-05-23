---
name: set-secret
description: Sets SST secrets for deployed environments. Use when configuring Clerk, database, Stripe, or webhook secrets.
allowed-tools: Bash(npx sst secret:*)
---

# Set SST Secret

Manages secrets stored in AWS SSM Parameter Store for SST deployments.

## Commands

### Set a Secret
```bash
npx sst secret set <SecretName> "<value>" --stage <stage>
```

### List Secrets
```bash
npx sst secret list --stage dev
```

### Remove a Secret
```bash
npx sst secret remove <SecretName> --stage dev
```

## Required Secrets by Component

### Backend (`back/sst.config.ts`)

| Secret | Description | Example |
|--------|-------------|---------|
| `DbConnStr` | PostgreSQL connection string | `postgresql://user:pass@host:5432/db` |
| `ClerkSecretKey` | Clerk backend secret | `sk_test_...` or `sk_live_...` |
| `ClerkWebhookSecret` | Clerk webhook signing secret | `whsec_...` |
| `StripeSecretKey` | Stripe API key (if using Stripe) | `sk_test_...` |
| `StripeWebhookSecret` | Stripe webhook signing secret | `whsec_...` |

```bash
# Set backend secrets
npx sst secret set DbConnStr "postgresql://user:pass@host:5432/db" --stage dev
npx sst secret set ClerkSecretKey "sk_test_..." --stage dev
npx sst secret set ClerkWebhookSecret "whsec_..." --stage dev
```

### Frontend (`front/sst.config.ts`)

| Secret | Description | Example |
|--------|-------------|---------|
| `ClerkPublishableKey` | Clerk frontend key | `pk_test_...` or `pk_live_...` |
| `ClerkSecretKey` | Clerk backend secret (for SSR) | `sk_test_...` |

```bash
# Set frontend secrets
npx sst secret set ClerkPublishableKey "pk_test_..." --stage dev
npx sst secret set ClerkSecretKey "sk_test_..." --stage dev
```

## Environment-Specific Values

### Development (`--stage dev`)
- Use Clerk **test** keys (`pk_test_*`, `sk_test_*`)
- Use Stripe **test** keys
- Connect to development database

### Production (`--stage prod`)
- Use Clerk **live** keys (`pk_live_*`, `sk_live_*`)
- Use Stripe **live** keys
- Connect to production database

## Secret Storage

Secrets are stored in AWS SSM Parameter Store:
- Path: `/sst/{app}/{stage}/{secret}`
- Encrypted with AWS KMS

## Accessing Secrets in Code

Secrets are declared in `sst.config.ts`:

```typescript
const dbConnStr = new sst.Secret('DbConnStr');
const clerkSecretKey = new sst.Secret('ClerkSecretKey');

// Use in Lambda environment
environment: {
  DATABASE_URL: dbConnStr.value,
  CLERK_SECRET_KEY: clerkSecretKey.value,
}
```

## Security Notes

- **Never** commit secrets to git
- **Never** log secret values
- Use different values for dev and prod
- Rotate secrets periodically
- Clerk keys: test vs live determine environment
