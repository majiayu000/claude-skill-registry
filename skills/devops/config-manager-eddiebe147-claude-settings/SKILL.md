---
name: config-manager
description: Expert guide for managing application configuration including environment variables, config files, secrets management, and multi-environment setups. Use when handling .env files, config validation, or configuration architecture.
---

# Configuration Manager Skill

## Overview

This skill helps you design and implement robust configuration management for applications. Covers environment variables, config files, secrets management, validation, type safety, and multi-environment deployments.

## Configuration Philosophy

### Twelve-Factor App Principles
1. **Store config in the environment**: Separate config from code
2. **Strict separation**: Config that varies between deploys should be in env vars
3. **No secrets in code**: Ever. Period.

### Configuration Hierarchy
```
Priority (highest to lowest):
1. Command-line arguments
2. Environment variables
3. Environment-specific config files (.env.local)
4. Default config files (.env)
5. Application defaults in code
```

### What Goes Where
- **Environment Variables**: API keys, database URLs, feature flags
- **Config Files**: Non-sensitive defaults, complex structures
- **Secrets Manager**: Production credentials, API tokens
- **Code**: Application logic, never secrets

## Environment Variables

### .env File Structure

```bash
# .env.example - Commit this file as documentation
# Copy to .env and fill in values

# ===================
# Application
# ===================
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000

# ===================
# Database
# ===================
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DATABASE_POOL_SIZE=10

# ===================
# Authentication
# ===================
# Get from Supabase Dashboard > Settings > API
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# ===================
# External Services
# ===================
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx

# ===================
# Email
# ===================
RESEND_API_KEY=re_xxx
EMAIL_FROM=noreply@example.com

# ===================
# Feature Flags
# ===================
ENABLE_ANALYTICS=true
ENABLE_BETA_FEATURES=false
```

### .gitignore Configuration

```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.development.local
.env.test.local
.env.production.local

# Keep example file
!.env.example
```

### Multi-Environment Setup

```bash
# .env.development
NODE_ENV=development
DATABASE_URL=postgresql://localhost:5432/myapp_dev
LOG_LEVEL=debug

# .env.test
NODE_ENV=test
DATABASE_URL=postgresql://localhost:5432/myapp_test
LOG_LEVEL=error

# .env.production
NODE_ENV=production
DATABASE_URL=${DATABASE_URL}  # Set in deployment platform
LOG_LEVEL=info
```

## Type-Safe Configuration

### Zod Schema Validation

```typescript
// src/config/env.ts
import { z } from 'zod';

// Define schema
const envSchema = z.object({
  // Node environment
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),

  // Server
  PORT: z.coerce.number().default(3000),
  APP_URL: z.string().url(),

  // Database
  DATABASE_URL: z.string().url(),
  DATABASE_POOL_SIZE: z.coerce.number().min(1).max(100).default(10),

  // Supabase
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1),

  // Stripe (optional in development)
  STRIPE_SECRET_KEY: z.string().startsWith('sk_').optional(),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith('whsec_').optional(),

  // Feature flags
  ENABLE_ANALYTICS: z.coerce.boolean().default(false),
  ENABLE_BETA_FEATURES: z.coerce.boolean().default(false),
});

// Type export
export type Env = z.infer<typeof envSchema>;

// Parse and validate
function loadEnv(): Env {
  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    console.error('Invalid environment variables:');
    console.error(result.error.format());
    process.exit(1);
  }

  return result.data;
}

// Singleton export
export const env = loadEnv();
```

### Environment Validation at Build Time

```typescript
// src/config/validate-env.ts
import { z } from 'zod';

// Client-side env (exposed to browser)
const clientEnvSchema = z.object({
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  NEXT_PUBLIC_APP_URL: z.string().url(),
});

// Server-side env (never exposed to browser)
const serverEnvSchema = z.object({
  DATABASE_URL: z.string(),
  SUPABASE_SERVICE_ROLE_KEY: z.string(),
  STRIPE_SECRET_KEY: z.string().optional(),
});

// Combined
const envSchema = clientEnvSchema.merge(serverEnvSchema);

export function validateEnv() {
  // Only validate server-side env on server
  if (typeof window !== 'undefined') {
    return clientEnvSchema.parse({
      NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
      NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
      NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
    });
  }

  return envSchema.parse(process.env);
}
```

### T3 Env Pattern (Next.js)

```typescript
// src/env.mjs
import { createEnv } from '@t3-oss/env-nextjs';
import { z } from 'zod';

export const env = createEnv({
  /**
   * Server-side environment variables
   */
  server: {
    DATABASE_URL: z.string().url(),
    NODE_ENV: z.enum(['development', 'test', 'production']),
    SUPABASE_SERVICE_ROLE_KEY: z.string(),
    STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
  },

  /**
   * Client-side environment variables (exposed to browser)
   * Prefix with NEXT_PUBLIC_
   */
  client: {
    NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
    NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string(),
    NEXT_PUBLIC_APP_URL: z.string().url(),
  },

  /**
   * Runtime values
   */
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    NODE_ENV: process.env.NODE_ENV,
    SUPABASE_SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY,
    STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
  },

  /**
   * Skip validation in certain environments
   */
  skipValidation: !!process.env.SKIP_ENV_VALIDATION,
});
```

## Configuration Files

### JSON Configuration

```typescript
// config/default.json
{
  "app": {
    "name": "My Application",
    "version": "1.0.0"
  },
  "server": {
    "port": 3000,
    "host": "localhost"
  },
  "cache": {
    "ttl": 3600,
    "maxSize": 1000
  },
  "features": {
    "darkMode": true,
    "betaFeatures": false
  }
}

// config/production.json (overrides default)
{
  "server": {
    "host": "0.0.0.0"
  },
  "cache": {
    "ttl": 86400
  }
}
```

### Config Loader

```typescript
// src/config/loader.ts
import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { z } from 'zod';

const configSchema = z.object({
  app: z.object({
    name: z.string(),
    version: z.string(),
  }),
  server: z.object({
    port: z.number(),
    host: z.string(),
  }),
  cache: z.object({
    ttl: z.number(),
    maxSize: z.number(),
  }),
  features: z.object({
    darkMode: z.boolean(),
    betaFeatures: z.boolean(),
  }),
});

type Config = z.infer<typeof configSchema>;

function deepMerge(target: any, source: any): any {
  const result = { ...target };

  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
      result[key] = deepMerge(result[key] || {}, source[key]);
    } else {
      result[key] = source[key];
    }
  }

  return result;
}

export function loadConfig(): Config {
  const env = process.env.NODE_ENV || 'development';
  const configDir = join(process.cwd(), 'config');

  // Load default config
  const defaultPath = join(configDir, 'default.json');
  let config = JSON.parse(readFileSync(defaultPath, 'utf-8'));

  // Merge environment-specific config
  const envPath = join(configDir, `${env}.json`);
  if (existsSync(envPath)) {
    const envConfig = JSON.parse(readFileSync(envPath, 'utf-8'));
    config = deepMerge(config, envConfig);
  }

  // Merge local overrides (not committed)
  const localPath = join(configDir, 'local.json');
  if (existsSync(localPath)) {
    const localConfig = JSON.parse(readFileSync(localPath, 'utf-8'));
    config = deepMerge(config, localConfig);
  }

  // Validate
  return configSchema.parse(config);
}

export const config = loadConfig();
```

## Secrets Management

### Local Development Secrets

```bash
# Use a secrets manager locally too
# Option 1: 1Password CLI
op read "op://Development/MyApp/API_KEY"

# Option 2: Doppler
doppler secrets download --no-file --format env > .env

# Option 3: AWS SSM (for local AWS dev)
aws ssm get-parameter --name "/myapp/dev/api-key" --with-decryption --query "Parameter.Value"
```

### Production Secrets with Vercel

```bash
# Add secrets via CLI
vercel env add STRIPE_SECRET_KEY production
vercel env add DATABASE_URL production

# Pull secrets to local .env
vercel env pull .env.local
```

### Secrets in Docker

```yaml
# docker-compose.yml
version: '3.8'
services:
  app:
    build: .
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true  # From Docker Swarm/secrets manager
```

### AWS Secrets Manager Integration

```typescript
// src/config/secrets.ts
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

interface AppSecrets {
  database_url: string;
  stripe_secret_key: string;
  jwt_secret: string;
}

let cachedSecrets: AppSecrets | null = null;

export async function getSecrets(): Promise<AppSecrets> {
  if (cachedSecrets) {
    return cachedSecrets;
  }

  const secretId = process.env.AWS_SECRET_ID || 'myapp/production/secrets';

  const command = new GetSecretValueCommand({ SecretId: secretId });
  const response = await client.send(command);

  if (!response.SecretString) {
    throw new Error('Secret not found');
  }

  cachedSecrets = JSON.parse(response.SecretString);
  return cachedSecrets!;
}

// Usage
async function connectDatabase() {
  const secrets = await getSecrets();
  return createConnection(secrets.database_url);
}
```

## Feature Flags

### Simple Feature Flag System

```typescript
// src/config/features.ts
import { env } from './env';

export const features = {
  analytics: env.ENABLE_ANALYTICS,
  betaFeatures: env.ENABLE_BETA_FEATURES,
  darkMode: true,  // Always enabled

  // Computed flags
  get isProduction() {
    return env.NODE_ENV === 'production';
  },

  get enableDebugLogs() {
    return env.NODE_ENV === 'development' || env.DEBUG === 'true';
  },
} as const;

// Type-safe feature checking
export function isEnabled(feature: keyof typeof features): boolean {
  return Boolean(features[feature]);
}

// Usage
if (isEnabled('analytics')) {
  initAnalytics();
}
```

### Environment-Aware Feature Flags

```typescript
// src/config/feature-flags.ts
type Environment = 'development' | 'staging' | 'production';

interface FeatureConfig {
  enabled: boolean | Environment[];
  description: string;
}

const featureFlags: Record<string, FeatureConfig> = {
  newCheckout: {
    enabled: ['development', 'staging'],
    description: 'New checkout flow',
  },
  aiAssistant: {
    enabled: true,
    description: 'AI assistant feature',
  },
  experimentalApi: {
    enabled: ['development'],
    description: 'Experimental API endpoints',
  },
};

export function isFeatureEnabled(
  feature: keyof typeof featureFlags
): boolean {
  const config = featureFlags[feature];
  const currentEnv = process.env.NODE_ENV as Environment;

  if (typeof config.enabled === 'boolean') {
    return config.enabled;
  }

  return config.enabled.includes(currentEnv);
}
```

## Configuration Patterns

### Singleton Configuration

```typescript
// src/config/index.ts
import { env } from './env';
import { loadConfig } from './loader';
import { features } from './features';

class AppConfig {
  private static instance: AppConfig;

  public readonly env = env;
  public readonly features = features;
  public readonly settings = loadConfig();

  private constructor() {
    // Freeze to prevent modifications
    Object.freeze(this);
  }

  static getInstance(): AppConfig {
    if (!AppConfig.instance) {
      AppConfig.instance = new AppConfig();
    }
    return AppConfig.instance;
  }

  // Helper methods
  get isDevelopment(): boolean {
    return this.env.NODE_ENV === 'development';
  }

  get isProduction(): boolean {
    return this.env.NODE_ENV === 'production';
  }

  get databaseUrl(): string {
    return this.env.DATABASE_URL;
  }
}

export const config = AppConfig.getInstance();
```

### Runtime Configuration Updates

```typescript
// src/config/runtime.ts
import { EventEmitter } from 'events';

class RuntimeConfig extends EventEmitter {
  private values: Map<string, any> = new Map();

  get<T>(key: string, defaultValue?: T): T | undefined {
    return this.values.get(key) ?? defaultValue;
  }

  set<T>(key: string, value: T): void {
    const oldValue = this.values.get(key);
    this.values.set(key, value);
    this.emit('change', { key, oldValue, newValue: value });
  }

  // Subscribe to changes
  onChange(callback: (change: { key: string; oldValue: any; newValue: any }) => void) {
    this.on('change', callback);
    return () => this.off('change', callback);
  }
}

export const runtimeConfig = new RuntimeConfig();

// Usage: Update config at runtime
runtimeConfig.set('maintenanceMode', true);

// Usage: React to changes
runtimeConfig.onChange(({ key, newValue }) => {
  if (key === 'maintenanceMode' && newValue) {
    showMaintenanceBanner();
  }
});
```

## Validation Checklist

### Environment Setup
- [ ] `.env.example` with all variables documented
- [ ] `.gitignore` excludes all `.env` files except example
- [ ] Validation runs at application startup
- [ ] Helpful error messages for missing/invalid config
- [ ] Type definitions for all config values

### Security
- [ ] No secrets in version control
- [ ] Secrets use appropriate secrets manager
- [ ] Production secrets rotated regularly
- [ ] Minimal exposure of sensitive values in logs
- [ ] NEXT_PUBLIC_ prefix only for truly public values

### Developer Experience
- [ ] Easy local setup (copy `.env.example`)
- [ ] Clear documentation of each variable
- [ ] Defaults for development environment
- [ ] Config validation gives actionable errors
- [ ] IDE autocomplete for config values

### Multi-Environment
- [ ] Separate configs for dev/staging/production
- [ ] Environment-specific overrides work correctly
- [ ] Feature flags for gradual rollouts
- [ ] Easy switching between environments

## When to Use This Skill

Invoke this skill when:
- Setting up configuration for a new project
- Adding new environment variables
- Implementing secrets management
- Creating feature flag systems
- Debugging configuration issues
- Setting up multi-environment deployments
- Migrating configuration between providers
- Implementing runtime configuration changes
