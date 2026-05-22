---
name: environment-config
description: Centralized environment variable management with validation. Fail fast at startup if config is invalid. Supports multi-environment setups (dev/staging/prod) with type-safe access.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: foundations
  time: 2h
  source: drift-masterguide
---

# Environment Configuration

Centralized, validated environment variables that fail fast at startup.

## When to Use This Skill

- Starting a new project that needs env var management
- Environment variables scattered across codebase
- Missing vars causing runtime crashes
- Need different configs for dev/staging/prod
- Want type-safe access to configuration

## Core Concepts

1. **Centralized config** - Single source of truth for all env vars
2. **Fail fast** - Validate at startup, not when first accessed
3. **Type safety** - Full TypeScript/Python typing for all config values
4. **Environment separation** - Clear distinction between dev/staging/prod

## File Structure

```
project/
├── .env                    # Local development (gitignored)
├── .env.example            # Template (committed)
├── .env.production         # Production overrides (gitignored or in CI)
├── .env.local              # Local overrides (gitignored)
└── src/
    └── lib/
        └── env.ts          # Validation and exports
```

## TypeScript Implementation

### With Zod Validation

```typescript
// lib/env.ts
import { z } from 'zod';

/**
 * Server-side environment variables.
 * These are NOT exposed to the browser.
 */
const serverSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  
  // Database
  DATABASE_URL: z.string().url(),
  
  // External services
  API_URL: z.string().url().default('http://localhost:8787'),
  REDIS_URL: z.string().url().optional(),
  
  // Feature flags
  ENABLE_ANALYTICS: z.coerce.boolean().default(false),
  ENABLE_RATE_LIMITING: z.coerce.boolean().default(true),
  
  // Secrets
  JWT_SECRET: z.string().min(32),
  
  // Logging
  LOG_LEVEL: z.enum(['debug', 'info', 'warn', 'error']).default('info'),
});

/**
 * Client-side environment variables.
 * MUST be prefixed with NEXT_PUBLIC_ (Next.js) or VITE_ (Vite)
 */
const clientSchema = z.object({
  NEXT_PUBLIC_API_URL: z.string().url(),
  NEXT_PUBLIC_APP_URL: z.string().url().optional(),
});

// Validate at module load time
const serverEnv = serverSchema.safeParse(process.env);
const clientEnv = clientSchema.safeParse(process.env);

if (!serverEnv.success) {
  console.error('❌ Invalid server environment variables:');
  console.error(JSON.stringify(serverEnv.error.flatten().fieldErrors, null, 2));
  throw new Error('Invalid server environment configuration');
}

if (!clientEnv.success) {
  console.error('❌ Invalid client environment variables:');
  console.error(JSON.stringify(clientEnv.error.flatten().fieldErrors, null, 2));
  throw new Error('Invalid client environment configuration');
}

/**
 * Type-safe server environment.
 * Use this in API routes and server components.
 */
export const env = serverEnv.data;

/**
 * Type-safe client environment.
 * Use this in client components.
 */
export const publicEnv = clientEnv.data;

// Type exports
export type Env = z.infer<typeof serverSchema>;
export type PublicEnv = z.infer<typeof clientSchema>;
```

### Without Dependencies (Lightweight)

```typescript
// lib/env.ts - No external dependencies

function requireEnv(key: string): string {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value;
}

function optionalEnv(key: string, defaultValue: string): string {
  return process.env[key] || defaultValue;
}

function boolEnv(key: string, defaultValue: boolean): boolean {
  const value = process.env[key];
  if (value === undefined) return defaultValue;
  return value === 'true' || value === '1';
}

function intEnv(key: string, defaultValue: number): number {
  const value = process.env[key];
  if (value === undefined) return defaultValue;
  const parsed = parseInt(value, 10);
  if (isNaN(parsed)) {
    throw new Error(`Environment variable ${key} must be a number`);
  }
  return parsed;
}

export const env = {
  // Required
  DATABASE_URL: requireEnv('DATABASE_URL'),
  JWT_SECRET: requireEnv('JWT_SECRET'),
  
  // Optional with defaults
  API_URL: optionalEnv('API_URL', 'http://localhost:8787'),
  LOG_LEVEL: optionalEnv('LOG_LEVEL', 'info'),
  PORT: intEnv('PORT', 3000),
  
  // Booleans
  ENABLE_ANALYTICS: boolEnv('ENABLE_ANALYTICS', false),
  ENABLE_RATE_LIMITING: boolEnv('ENABLE_RATE_LIMITING', true),
  
  // Computed
  isDev: process.env.NODE_ENV === 'development',
  isProd: process.env.NODE_ENV === 'production',
  isTest: process.env.NODE_ENV === 'test',
} as const;

// Validate on import
Object.keys(env); // Triggers all getters
```

## Python Implementation

### With Pydantic

```python
# config/settings.py
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Literal
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # Environment
    environment: Literal["development", "production", "test"] = "development"
    debug: bool = False
    
    # Database
    database_url: str = Field(..., description="PostgreSQL connection string")
    
    # External services
    api_url: str = "http://localhost:8787"
    redis_url: str | None = None
    
    # Feature flags
    enable_analytics: bool = False
    enable_rate_limiting: bool = True
    
    # Secrets
    jwt_secret: str = Field(..., min_length=32)
    
    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    
    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith(("postgresql://", "postgres://")):
            raise ValueError("database_url must be a PostgreSQL connection string")
        return v
    
    @property
    def is_dev(self) -> bool:
        return self.environment == "development"
    
    @property
    def is_prod(self) -> bool:
        return self.environment == "production"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance. Call once at startup."""
    return Settings()


# Validate on import
settings = get_settings()
```

### Without Dependencies

```python
# config/settings.py
import os
from dataclasses import dataclass
from typing import Optional


class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass


def require_env(key: str) -> str:
    """Get required environment variable or raise."""
    value = os.getenv(key)
    if not value:
        raise ConfigError(f"Missing required environment variable: {key}")
    return value


def optional_env(key: str, default: str) -> str:
    """Get optional environment variable with default."""
    return os.getenv(key, default)


def bool_env(key: str, default: bool) -> bool:
    """Get boolean environment variable."""
    value = os.getenv(key)
    if value is None:
        return default
    return value.lower() in ("true", "1", "yes")


def int_env(key: str, default: int) -> int:
    """Get integer environment variable."""
    value = os.getenv(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        raise ConfigError(f"Environment variable {key} must be an integer")


@dataclass(frozen=True)
class Settings:
    """Immutable application settings."""
    
    # Required
    database_url: str
    jwt_secret: str
    
    # Optional
    api_url: str
    log_level: str
    port: int
    
    # Feature flags
    enable_analytics: bool
    enable_rate_limiting: bool
    
    # Computed
    is_dev: bool
    is_prod: bool
    is_test: bool


def load_settings() -> Settings:
    """Load and validate settings from environment."""
    return Settings(
        database_url=require_env("DATABASE_URL"),
        jwt_secret=require_env("JWT_SECRET"),
        api_url=optional_env("API_URL", "http://localhost:8787"),
        log_level=optional_env("LOG_LEVEL", "INFO"),
        port=int_env("PORT", 8000),
        enable_analytics=bool_env("ENABLE_ANALYTICS", False),
        enable_rate_limiting=bool_env("ENABLE_RATE_LIMITING", True),
        is_dev=os.getenv("ENVIRONMENT", "development") == "development",
        is_prod=os.getenv("ENVIRONMENT") == "production",
        is_test=os.getenv("ENVIRONMENT") == "test",
    )


# Validate on import
settings = load_settings()
```

## Usage Examples

### TypeScript

```typescript
// In API routes
import { env } from '@/lib/env';

export async function GET() {
  if (env.ENABLE_ANALYTICS) {
    await trackEvent('api_call');
  }
  
  const response = await fetch(`${env.API_URL}/data`);
  return Response.json(await response.json());
}

// In client components
import { publicEnv } from '@/lib/env';

const apiClient = createClient(publicEnv.NEXT_PUBLIC_API_URL);
```

### Python

```python
# In FastAPI
from config.settings import settings

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "environment": settings.environment,
        "debug": settings.debug,
    }

# In services
from config.settings import settings

async def process_data():
    if settings.enable_analytics:
        await track_event("data_processed")
```

## .env.example Template

```bash
# =============================================================================
# Required - App will not start without these
# =============================================================================
DATABASE_URL=postgresql://user:pass@localhost:5432/myapp
JWT_SECRET=your-secret-key-at-least-32-characters-long

# =============================================================================
# External Services
# =============================================================================
API_URL=http://localhost:8787
REDIS_URL=redis://localhost:6379

# =============================================================================
# Feature Flags
# =============================================================================
ENABLE_ANALYTICS=false
ENABLE_RATE_LIMITING=true

# =============================================================================
# App Config
# =============================================================================
NODE_ENV=development
LOG_LEVEL=debug
PORT=3000
```

## .gitignore

```gitignore
# Environment files
.env
.env.local
.env.*.local
.env.production
.env.staging

# Keep the example
!.env.example
```

## Docker Integration

```dockerfile
# Build args for client-side vars (baked into bundle)
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Runtime vars set via docker-compose or k8s
```

```yaml
# docker-compose.yml
services:
  app:
    build: .
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET=${JWT_SECRET}
    env_file:
      - .env.production
```

## Best Practices

1. **Validate at startup** - Never let invalid config reach runtime
2. **Use typed access** - No raw `process.env` calls in business logic
3. **Separate client/server** - Client vars need special prefixes
4. **Default sensibly** - Dev-friendly defaults, prod requires explicit config
5. **Document everything** - `.env.example` is your config documentation

## Common Mistakes

- Committing `.env` files with secrets
- Using `process.env` directly throughout codebase
- Not validating at startup (crashes at 3am instead)
- Exposing server secrets to client bundle
- Missing `.env.example` (new devs can't onboard)

## Related Skills

- [Feature Flags](../feature-flags/)
- [Error Handling](../error-handling/)
