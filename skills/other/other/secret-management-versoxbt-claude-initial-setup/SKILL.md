---
name: secret-management
description: >
  Manage secrets, API keys, and sensitive configuration securely. Activate whenever the user
  handles API keys, passwords, tokens, database credentials, .env files, CI/CD pipelines,
  or any configuration that contains sensitive values. Also activate when the user asks about
  secret rotation, vault integration, or gitignore setup.
---

# Secret Management

Secure handling of API keys, passwords, tokens, and sensitive configuration across
development, CI/CD, and production environments. Never hardcode secrets; always use
environment variables, secret managers, or vault solutions.

## When to Use
- Setting up a new project that needs API keys or database credentials
- Configuring CI/CD pipelines with secrets
- Reviewing code that may contain hardcoded secrets
- Setting up .env files and .gitignore
- Integrating with secret management services (Vault, AWS Secrets Manager)
- Rotating compromised or expired credentials

## Core Patterns

### Environment Variables and .env Files

Use .env files for local development, never commit them to version control.

```bash
# .env (NEVER committed to git)
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
JWT_SECRET=your-256-bit-secret-here
REDIS_URL=redis://localhost:6379

# .env.example (committed to git, no real values)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
OPENAI_API_KEY=sk-proj-your-key-here
JWT_SECRET=generate-a-secure-random-string
REDIS_URL=redis://localhost:6379
```

```gitignore
# .gitignore - ALWAYS include these
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
service-account.json
```

### Loading and Validating Secrets

Always validate that required secrets exist at startup, not at first use.

```typescript
import { z } from 'zod';
import dotenv from 'dotenv';

dotenv.config();

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  OPENAI_API_KEY: z.string().startsWith('sk-'),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  PORT: z.coerce.number().default(3000),
});

function loadConfig() {
  const result = envSchema.safeParse(process.env);
  if (!result.success) {
    const missing = result.error.issues.map(i => i.path.join('.'));
    throw new Error(`Missing or invalid env vars: ${missing.join(', ')}`);
  }
  return result.data;
}

export const config = loadConfig();
```

```python
# Python equivalent with Pydantic
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    jwt_secret: str
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

### HashiCorp Vault Integration

Use Vault for production secret management with automatic rotation.

```typescript
import Vault from 'node-vault';

const vault = Vault({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,
});

async function getSecret(path: string): Promise<string> {
  try {
    const result = await vault.read(`secret/data/${path}`);
    return result.data.data.value;
  } catch (error) {
    throw new Error(`Failed to read secret at ${path}: ${error.message}`);
  }
}

// Usage
const dbPassword = await getSecret('production/database');
```

### CI/CD Secret Configuration

Configure secrets in CI/CD without exposing them in logs or artifacts.

```yaml
# GitHub Actions - use repository secrets
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          # Never echo secrets
          npm run deploy

      # WRONG: This exposes secrets in logs
      # - run: echo ${{ secrets.API_KEY }}

      # WRONG: This exposes secrets in artifacts
      # - run: env > debug.txt
```

```yaml
# GitLab CI - use protected variables
deploy:
  stage: deploy
  variables:
    DATABASE_URL: $DATABASE_URL  # Set in GitLab CI/CD settings
  script:
    - npm run deploy
  only:
    - main
```

### Secret Rotation

Implement graceful secret rotation without downtime.

```typescript
interface SecretProvider {
  getCurrent(): Promise<string>;
  getPrevious(): Promise<string | null>;
}

// Accept both current and previous secrets during rotation window
async function validateApiKey(
  key: string,
  provider: SecretProvider
): Promise<boolean> {
  const current = await provider.getCurrent();
  if (key === current) return true;

  const previous = await provider.getPrevious();
  if (previous && key === previous) return true;

  return false;
}

// Rotate JWT secrets gracefully
function verifyToken(token: string): JwtPayload {
  try {
    return jwt.verify(token, config.JWT_SECRET) as JwtPayload;
  } catch {
    if (config.JWT_SECRET_PREVIOUS) {
      return jwt.verify(token, config.JWT_SECRET_PREVIOUS) as JwtPayload;
    }
    throw new Error('Invalid token');
  }
}
```

## Anti-Patterns
- Hardcoding secrets directly in source code (`const apiKey = "sk-..."`)
- Committing .env files to version control
- Logging secret values, even in debug mode
- Passing secrets as command-line arguments (visible in process listings)
- Storing secrets in frontend/client-side code (always exposed to users)
- Using the same secrets across all environments (dev, staging, production)
- Sharing secrets via Slack, email, or other unencrypted channels
- Not rotating secrets after team member departure or suspected compromise

## Quick Reference

| Context | Solution |
|---------|----------|
| Local development | .env files + dotenv, validated at startup |
| CI/CD pipelines | Platform secret storage (GitHub Secrets, GitLab Variables) |
| Production | Vault, AWS Secrets Manager, GCP Secret Manager |
| Rotation | Dual-key acceptance window, then revoke old key |
| Frontend | Never store secrets; proxy through backend API |
| Git protection | .gitignore, pre-commit hooks, git-secrets scanner |
| Validation | Zod/Pydantic schema at app startup |
