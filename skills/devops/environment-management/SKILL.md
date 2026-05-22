---
name: environment-management
description: Auto-activates when user mentions environment variables, .env files, secrets management, configuration, or multi-environment setup. Manages environment configs securely.
category: devops
---

# Environment Management

Manages environment variables, secrets, and multi-environment configurations securely.

## When This Activates

- User says: "setup environment variables", "manage secrets", "create .env"
- User mentions: ".env file", "environment config", "secrets management"
- Files: `.env`, `.env.example`, `.env.local`, `config/*`
- Questions about configuration or environment setup

## Environment File Structure

### .env.example (Template)

```bash
# .env.example - Commit this to git (no secrets!)

# Application
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# DATABASE_URL format: postgresql://USER:PASSWORD@HOST:PORT/DATABASE

# Authentication
JWT_SECRET=your-super-secret-jwt-key-here-min-32-chars
JWT_EXPIRES_IN=7d
SESSION_SECRET=your-session-secret-here

# External APIs
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

SENDGRID_API_KEY=SG....
SENDGRID_FROM_EMAIL=noreply@example.com

# OAuth (optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Feature Flags
ENABLE_ANALYTICS=false
ENABLE_DEBUG_MODE=false

# Redis (optional)
REDIS_URL=redis://localhost:6379
```

### .env (Actual - NEVER commit!)

```bash
# .env - Add to .gitignore!

NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000

DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/myapp_dev

JWT_SECRET=super-secret-jwt-key-change-this-in-production-min-32-characters
JWT_EXPIRES_IN=7d

STRIPE_PUBLIC_KEY=pk_test_51abc123...
STRIPE_SECRET_KEY=sk_test_51xyz789...
```

## Environment Tiers

### Development (.env.development)

```bash
NODE_ENV=development
DEBUG=true
LOG_LEVEL=debug

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379

# Use test/sandbox API keys
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG.test...

# Disable features in dev
ENABLE_ANALYTICS=false
ENABLE_RATE_LIMITING=false
```

### Staging (.env.staging)

```bash
NODE_ENV=staging
DEBUG=false
LOG_LEVEL=info

DATABASE_URL=postgresql://user:pass@staging-db.example.com:5432/myapp_staging
REDIS_URL=redis://staging-redis.example.com:6379

# Staging API keys
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG....

# Enable some features
ENABLE_ANALYTICS=true
ENABLE_RATE_LIMITING=true
```

### Production (.env.production)

```bash
NODE_ENV=production
DEBUG=false
LOG_LEVEL=error

DATABASE_URL=postgresql://user:securepass@prod-db.example.com:5432/myapp_prod
REDIS_URL=redis://prod-redis.example.com:6379

# Production API keys (LIVE!)
STRIPE_SECRET_KEY=sk_live_...
SENDGRID_API_KEY=SG....

# All features enabled
ENABLE_ANALYTICS=true
ENABLE_RATE_LIMITING=true
ENABLE_MONITORING=true
```

## Loading Environment Variables

### Node.js (with dotenv)

```typescript
// config.ts
import 'dotenv/config';
import { z } from 'zod';

// Define schema for validation
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.string().transform(Number),
  APP_URL: z.string().url(),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string(),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  SENDGRID_API_KEY: z.string(),
  REDIS_URL: z.string().url().optional(),
});

// Parse and validate
const env = envSchema.parse(process.env);

export const config = {
  env: env.NODE_ENV,
  port: env.PORT,
  appUrl: env.APP_URL,
  database: {
    url: env.DATABASE_URL,
  },
  jwt: {
    secret: env.JWT_SECRET,
    expiresIn: env.JWT_EXPIRES_IN,
  },
  stripe: {
    secretKey: env.STRIPE_SECRET_KEY,
  },
  sendgrid: {
    apiKey: env.SENDGRID_API_KEY,
  },
  redis: {
    url: env.REDIS_URL,
  },
} as const;

// Type-safe access
export type Config = typeof config;
```

### Next.js (Built-in Support)

```typescript
// next.config.js
module.exports = {
  env: {
    // Public variables (exposed to browser)
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    NEXT_PUBLIC_STRIPE_PUBLIC_KEY: process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY,
  },
  // Server-side only
  serverRuntimeConfig: {
    DATABASE_URL: process.env.DATABASE_URL,
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
  },
};
```

### Python (with python-dotenv)

```python
# config.py
from dotenv import load_dotenv
import os
from pydantic import BaseSettings, Field, PostgresDsn

load_dotenv()

class Settings(BaseSettings):
    app_name: str = "MyApp"
    debug: bool = Field(False, env='DEBUG')
    database_url: PostgresDsn
    jwt_secret: str = Field(..., min_length=32)
    stripe_secret_key: str
    
    class Config:
        env_file = '.env'
        case_sensitive = False

settings = Settings()
```

## Secrets Management

### Using Environment Variables in CI/CD

#### GitHub Actions

```yaml
# .github/workflows/deploy.yml
- name: Deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    JWT_SECRET: ${{ secrets.JWT_SECRET }}
    STRIPE_SECRET_KEY: ${{ secrets.STRIPE_SECRET_KEY }}
  run: npm run deploy
```

#### Docker Compose

```yaml
# docker-compose.yml
services:
  app:
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET=${JWT_SECRET}
    env_file:
      - .env
```

### Cloud Providers

#### Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Add secrets
vercel env add DATABASE_URL
vercel env add JWT_SECRET

# Pull environment variables
vercel env pull .env.local
```

#### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Link project
railway link

# Add variables
railway variables set DATABASE_URL=...
```

#### AWS Systems Manager (Parameter Store)

```bash
# Store parameter
aws ssm put-parameter \
  --name "/myapp/prod/DATABASE_URL" \
  --value "postgresql://..." \
  --type "SecureString"

# Retrieve parameter
aws ssm get-parameter \
  --name "/myapp/prod/DATABASE_URL" \
  --with-decryption \
  --query "Parameter.Value"
```

## Security Best Practices

### 1. Never Commit Secrets

```bash
# .gitignore
.env
.env.local
.env.*.local
.env.production
*.pem
*.key
secrets/
```

### 2. Use Secret Scanning

```bash
# Install git-secrets
git secrets --install
git secrets --register-aws

# Scan for secrets
git secrets --scan

# Pre-commit hook
git secrets --install ~/.git-templates/git-secrets
git config --global init.templateDir ~/.git-templates/git-secrets
```

### 3. Rotate Secrets Regularly

```typescript
// secret-rotation.ts
import { scheduleJob } from 'node-schedule';

// Rotate JWT secret weekly
scheduleJob('0 0 * * 0', async () => {
  const newSecret = generateSecureSecret();
  await updateSecret('JWT_SECRET', newSecret);
  await notifyAdmins('JWT secret rotated');
});
```

### 4. Validate Environment Variables

```typescript
// startup.ts
const requiredEnvVars = [
  'DATABASE_URL',
  'JWT_SECRET',
  'STRIPE_SECRET_KEY',
];

for (const varName of requiredEnvVars) {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
}
```

## Environment Detection

```typescript
// env.ts
export const isDevelopment = process.env.NODE_ENV === 'development';
export const isStaging = process.env.NODE_ENV === 'staging';
export const isProduction = process.env.NODE_ENV === 'production';
export const isTest = process.env.NODE_ENV === 'test';

// Feature flags based on environment
export const features = {
  analytics: isProduction || isStaging,
  debugMode: isDevelopment,
  rateLimiting: isProduction || isStaging,
  verboseLogging: isDevelopment || isStaging,
};
```

## Migration Guide

```bash
# 1. Create .env.example from current .env (remove values)
cat .env | sed 's/=.*/=/' > .env.example

# 2. Verify no secrets in .env.example
grep -E "(secret|password|key)" .env.example

# 3. Add .env to .gitignore
echo ".env" >> .gitignore

# 4. Remove .env from git history (if committed)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all
```

## Checklist

- [ ] .env.example created (no secrets!)
- [ ] .env added to .gitignore
- [ ] All secrets in environment variables (not hardcoded)
- [ ] Environment variables validated at startup
- [ ] Separate configs for dev/staging/prod
- [ ] Secrets management tool configured (GitHub Secrets, etc.)
- [ ] Type-safe environment variable access
- [ ] Documentation of all required variables
- [ ] Secret rotation plan in place
- [ ] Git secrets scanning enabled

**Generate environment configs, present to user, create files with approval.**
