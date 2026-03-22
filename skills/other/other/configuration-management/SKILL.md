---
name: configuration-management
description: Manage configuration properly - environment variables, config files, secrets
category: DevOps Operations
---

# Skill: configuration-management

## What I do

I manage application settings, environment variables, secrets, and environment-specific configuration. I follow the Twelve-Factor App approach, keeping configuration strictly separate from code while maintaining security, auditability, and ease of use across multiple environments.

## When to use me

- Managing environment-specific behaviour (dev, staging, prod).
- Handling database credentials, API keys, and sensitive tokens securely.
- Configuring third-party integrations and feature toggles.
- Setting up CI/CD pipelines and Kubernetes ConfigMaps/Secrets.
- Ensuring configuration validation at application startup.

## Core principles

1. **Configuration in Environment** - Store config in environment variables, never in code (12-Factor).
2. **Never Commit Secrets** - Secrets must never enter version control; use secure vaults or secret managers.
3. **Environment Parity** - Keep environments as similar as possible, differing only in configuration.
4. **Validation at Startup** - Validate all required settings on boot; fail fast if configuration is missing or invalid.
5. **Immutable Configuration** - Once loaded, configuration should not change; restart to apply updates.

## Patterns & examples

**Pattern: Go Startup Validation**

```go
func Load() (*Config, error) {
    cfg := &Config{
        DatabaseURL: os.Getenv("DATABASE_URL"),
        JWTSecret:   os.Getenv("JWT_SECRET"),
    }
    if cfg.DatabaseURL == "" || cfg.JWTSecret == "" {
        return nil, fmt.Errorf("missing required configuration")
    }
    return cfg, nil
}
```

**Pattern: Kubernetes Secret Usage**

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-url
```

**Pattern: Environment Files (.env.example)**

```bash
# .env.example - Commit to Git
PORT=8080
DATABASE_URL=postgres://localhost:5432/db
JWT_SECRET=changeme # Example only
```

## Anti-patterns

- ❌ **Hardcoded Configuration** - Embedding settings in source code requiring rebuilds for changes.
- ❌ **Committing Secrets** - Storing passwords or keys in `.env` files that are committed to Git.
- ❌ **Configuration Sprawl** - Scattered settings across dozens of files without a central registry.
- ❌ **Logging Secrets** - Printing configuration to logs without sanitising sensitive values.
- ❌ **Default Production Secrets** - Using "development" or "changeme" secrets in production.


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/Configuration Management.md`

## Related skills

- `security` - Secure handling of sensitive data.
- `devops` - Configuration management in CI/CD pipelines.
- `docker` - Passing configuration to containerised applications.
- `infrastructure-as-code` - Declarative management of configuration state.

