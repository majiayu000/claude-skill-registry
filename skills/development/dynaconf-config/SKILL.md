---
name: dynaconf-config
description: Automatically applies when adding configuration settings. Ensures proper dynaconf pattern with @env, @int, @bool type casting in settings.toml and environment-specific overrides.
---

# Dynaconf Configuration Pattern Enforcer

When adding new configuration to `settings.toml`, always follow the dynaconf pattern.

## ✅ Correct Pattern

```toml
# settings.toml

[default]
# Base configuration with type casting
api_base_url = "@env API_BASE_URL|http://localhost:8080"
api_timeout = "@int 30"
feature_enabled = "@bool true"
max_retries = "@int 3"

# API endpoints (no @ prefix for strings)
api_endpoint = "/api/v1/endpoint"

[dev_local]
# Override for local development
api_base_url = "@env API_BASE_URL|http://localhost:8080"

[dev_remote]
# Override for remote development
api_base_url = "@env API_BASE_URL|http://gateway-service"

[production]
# Production overrides
api_base_url = "@env API_BASE_URL|https://api.production.com"
api_timeout = "@int 60"
```

## Type Casting Directives

**Use appropriate prefixes:**
- `@env VAR|default` - Environment variable with fallback
- `@int 123` - Cast to integer
- `@bool true` - Cast to boolean
- `@float 1.5` - Cast to float
- `@path ./dir` - Convert to Path object
- No prefix - String value

## Environment Variable Override

**Pattern:** `APPNAME_SETTING_NAME`

Example:
```toml
# In settings.toml
api_timeout = "@int 30"

# Override via environment
export APP_API_TIMEOUT=60
```

## Configuration Access

```python
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    load_dotenv=True,
)

timeout = settings.api_timeout  # Returns int 30
url = settings.api_base_url     # Returns string
```

## Common Patterns

**API Configuration:**
```toml
service_api_base_url = "@env SERVICE_API_URL|http://localhost:8080"
service_endpoint = "/api/v1/endpoint/{param}"
service_timeout = "@int 30"
```

**Feature Flags:**
```toml
feature_enabled = "@bool true"
feature_beta_mode = "@bool false"
```

**Database Paths:**
```toml
db_path = "@path data/database.db"
```

**Secrets Management:**
```toml
# settings.toml (checked into git)
api_key = "@env API_KEY"

# .secrets.toml (gitignored)
api_key = "actual-secret-key"
```

## ❌ Anti-Patterns

```toml
# ❌ Don't hardcode secrets
api_key = "sk-1234567890"

# ❌ Don't forget type casting for numbers
timeout = "30"  # Will be string, not int

# ❌ Don't mix environments in same section
[default]
api_url = "https://production.com"  # Should be in [production]
```

## Best Practices Checklist

- ✅ Add to `[default]` section first
- ✅ Use appropriate `@` type casting
- ✅ Add environment variable overrides with `@env`
- ✅ Add to environment-specific sections as needed
- ✅ Document in comments what the setting does
- ✅ Keep secrets in `.secrets.toml` (gitignored)
- ✅ Use consistent naming conventions (snake_case)
- ✅ Provide sensible defaults

## Auto-Apply

When adding configuration:
1. Add to `[default]` section first
2. Use appropriate `@` type casting
3. Add environment variable overrides
4. Add to environment-specific sections as needed
5. Document in comments what the setting does

## Related Skills

- structured-errors - For validation errors
- pydantic-models - For settings validation with Pydantic
