---
name: fnox-configuration
description: Use when configuring Fnox secrets management with fnox.toml. Covers file structure, secrets definition, profiles, and hierarchical configurations.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Fnox - Configuration

Configuring secrets management with Fnox using fnox.toml files for secure, version-controlled secret storage.

## Basic Configuration

### Initialize Project

```bash
# Create fnox.toml in current directory
fnox init

# Initialize with specific provider
fnox init --provider age
```

### Basic fnox.toml Structure

```toml
# fnox.toml
[providers.age]
type = "age"
public_keys = ["age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"]

[secrets]
DATABASE_URL = { provider = "age", value = "age[...]" }
API_KEY = { provider = "age", value = "age[...]", description = "Production API key" }
```

## Secrets Definition

### Simple Secret

```toml
[secrets]
DATABASE_URL = "postgresql://localhost/myapp"  # Plain text (dev only)
```

### Encrypted Secret

```toml
[secrets]
DATABASE_URL = {
  provider = "age",
  value = "age1encrypted-value-here",
  description = "Production database connection string"
}
```

### Secret with Default

```toml
[secrets]
DEBUG_MODE = {
  provider = "age",
  value = "age[...]",
  default = "false",
  description = "Enable debug logging"
}
```

### Secret Behavior Options

```toml
[secrets]
OPTIONAL_API_KEY = {
  provider = "age",
  value = "age[...]",
  if_missing = "warn"  # Options: "error", "warn", "ignore"
}

REQUIRED_SECRET = {
  provider = "age",
  value = "age[...]",
  if_missing = "error"  # Fail if missing (default)
}
```

## Configuration Hierarchy

### File Locations (Priority Order)

1. `fnox.local.toml` - Local overrides (gitignored)
2. `fnox.$FNOX_PROFILE.toml` - Profile-specific
3. `fnox.toml` - Project configuration
4. Parent directory `fnox.toml` files (recursive)
5. `~/.config/fnox/config.toml` - Global configuration

### Global Configuration

```toml
# ~/.config/fnox/config.toml
[providers.age]
type = "age"
identity = "~/.config/fnox/keys/identity.txt"

[settings]
if_missing = "warn"  # Global default for missing secrets
```

### Project Configuration

```toml
# project/fnox.toml
[providers.age]
public_keys = ["age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"]

[secrets]
DATABASE_URL = { provider = "age", value = "age[...]" }
APP_NAME = "myapp"
```

### Local Overrides

```toml
# project/fnox.local.toml (gitignored)
[secrets]
DATABASE_URL = "postgresql://localhost/myapp_dev"  # Override for local dev
DEBUG = "true"
```

## Profiles

### Define Profiles

```toml
# fnox.toml
[secrets]
DATABASE_URL = "postgresql://localhost/myapp"  # Default

[profiles.production]
[profiles.production.secrets]
DATABASE_URL = { provider = "aws-sm", value = "prod/database-url" }

[profiles.staging]
[profiles.staging.secrets]
DATABASE_URL = { provider = "aws-sm", value = "staging/database-url" }
```

### Use Profiles

```bash
# Set profile via environment variable
export FNOX_PROFILE=production
fnox get DATABASE_URL

# Or use flag
fnox --profile staging get DATABASE_URL
fnox -p production exec -- node app.js
```

### Profile-Specific Files

```toml
# fnox.production.toml
[providers.aws-sm]
type = "aws-sm"
region = "us-east-1"

[secrets]
DATABASE_URL = { provider = "aws-sm", value = "prod/database-url" }
API_KEY = { provider = "aws-sm", value = "prod/api-key" }
```

```bash
# Use profile-specific file
export FNOX_PROFILE=production
fnox get DATABASE_URL  # Loads from fnox.production.toml
```

## Configuration Imports

### Import Other Configurations

```toml
# fnox.toml
import = ["shared-secrets.toml", "../common/fnox.toml"]

[secrets]
APP_SPECIFIC_SECRET = { provider = "age", value = "age[...]" }
```

### Shared Configuration

```toml
# shared-secrets.toml
[providers.age]
public_keys = ["age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p"]

[secrets]
SHARED_API_KEY = { provider = "age", value = "age[...]" }
```

## Validation

### Check Configuration

```bash
# Show diagnostic information
fnox doctor

# Verify secrets can be retrieved
fnox get DATABASE_URL

# List all configured secrets
fnox list

# Test specific provider
fnox provider test age
```

### Common Validation Errors

```toml
# Error: Missing provider definition
[secrets]
API_KEY = { provider = "nonexistent", value = "..." }

# Error: Invalid provider configuration
[providers.age]
# Missing required fields

# Error: Circular import
import = ["other.toml"]  # other.toml imports this file
```

## Best Practices

### Separate Public and Private Config

```toml
# fnox.toml (committed)
[providers.age]
public_keys = ["age1ql3z..."]  # Public key safe to commit

[secrets]
DATABASE_URL = { provider = "age", value = "age[...]" }
API_KEY = { provider = "age", value = "age[...]" }

# fnox.local.toml (gitignored)
[providers.age]
identity = "~/.ssh/age-identity.txt"  # Private key, never commit

[secrets]
DATABASE_URL = "postgresql://localhost/dev"  # Local override
```

### Document Secrets

```toml
[secrets]
DATABASE_URL = {
  provider = "age",
  value = "age[...]",
  description = "PostgreSQL connection string for production database"
}

STRIPE_API_KEY = {
  provider = "age",
  value = "age[...]",
  description = "Stripe secret key for payment processing"
}

SENDGRID_API_KEY = {
  provider = "age",
  value = "age[...]",
  description = "SendGrid API key for transactional emails"
}
```

### Use Meaningful Names

```toml
# Good: Clear, descriptive names
[secrets]
POSTGRES_CONNECTION_STRING = { provider = "age", value = "age[...]" }
STRIPE_SECRET_KEY = { provider = "age", value = "age[...]" }
JWT_SIGNING_SECRET = { provider = "age", value = "age[...]" }

# Avoid: Vague names
[secrets]
DB = { provider = "age", value = "age[...]" }
KEY1 = { provider = "age", value = "age[...]" }
SECRET = { provider = "age", value = "age[...]" }
```

### Set Appropriate Defaults

```toml
[secrets]
# Good: Sensible defaults for non-sensitive config
LOG_LEVEL = { default = "info" }
CACHE_TTL = { default = "3600" }

# Avoid: Defaults for sensitive data
API_KEY = { default = "unsafe-default-key" }  # Bad!
```

## Common Patterns

### Multi-Environment Setup

```toml
# fnox.toml - Base configuration
[providers.age]
public_keys = ["age1ql3z..."]

[secrets]
APP_NAME = "myapp"

# fnox.development.toml
[secrets]
DATABASE_URL = "postgresql://localhost/myapp_dev"
DEBUG = "true"

# fnox.production.toml
[providers.aws-sm]
type = "aws-sm"
region = "us-east-1"

[secrets]
DATABASE_URL = { provider = "aws-sm", value = "prod/db-url" }
DEBUG = "false"
```

### Feature Flags

```toml
[secrets]
FEATURE_NEW_DASHBOARD = { default = "false" }
FEATURE_BETA_API = { default = "false" }
FEATURE_ROLLOUT_PERCENTAGE = { default = "0" }
```

### Service Configuration

```toml
[secrets]
# Database
DATABASE_HOST = { provider = "age", value = "age[...]" }
DATABASE_PORT = { default = "5432" }
DATABASE_NAME = { default = "myapp" }
DATABASE_USER = { provider = "age", value = "age[...]" }
DATABASE_PASSWORD = { provider = "age", value = "age[...]" }

# Redis
REDIS_HOST = { provider = "age", value = "age[...]" }
REDIS_PORT = { default = "6379" }
REDIS_PASSWORD = { provider = "age", value = "age[...]" }
```

## Anti-Patterns

### Don't Commit Private Keys

```toml
# Bad: Private key in committed config
[providers.age]
identity = "AGE-SECRET-KEY-..."  # NEVER DO THIS

# Good: Reference gitignored location
[providers.age]
identity = "~/.config/fnox/keys/identity.txt"
```

### Don't Use Plain Text for Sensitive Data

```toml
# Bad: Sensitive data in plain text
[secrets]
DATABASE_PASSWORD = "super-secret-password"  # Committed to git!

# Good: Encrypted
[secrets]
DATABASE_PASSWORD = { provider = "age", value = "age[...]" }
```

### Don't Duplicate Secrets

```toml
# Bad: Same secret defined multiple times
[secrets]
API_KEY = { provider = "age", value = "age[...]" }
STRIPE_KEY = { provider = "age", value = "age[...]" }  # Same as API_KEY

# Good: Use one secret, reference from code
[secrets]
STRIPE_API_KEY = { provider = "age", value = "age[...]" }
```

### Don't Mix Concerns

```toml
# Bad: Secrets mixed with non-secret config
[secrets]
DATABASE_PASSWORD = { provider = "age", value = "age[...]" }
APP_NAME = "myapp"  # Not a secret!
LOG_LEVEL = "info"  # Not a secret!

# Good: Only secrets in fnox.toml
[secrets]
DATABASE_PASSWORD = { provider = "age", value = "age[...]" }

# Use separate config file for non-secrets
# app.config.toml
APP_NAME = "myapp"
LOG_LEVEL = "info"
```

## Advanced Patterns

### Template Values

```toml
[secrets]
DATABASE_HOST = { provider = "age", value = "age[...]" }
DATABASE_NAME = { default = "myapp" }
DATABASE_USER = { provider = "age", value = "age[...]" }
DATABASE_PASSWORD = { provider = "age", value = "age[...]" }

# Constructed in application code from components above
# DATABASE_URL = postgresql://{USER}:{PASSWORD}@{HOST}/{NAME}
```

### Conditional Secrets

```toml
[secrets]
# Base secrets always loaded
API_KEY = { provider = "age", value = "age[...]" }

[profiles.ci]
[profiles.ci.secrets]
# Additional secrets only for CI
CI_TOKEN = { provider = "age", value = "age[...]" }
DEPLOY_KEY = { provider = "age", value = "age[...]" }
```

## Related Skills

- **providers**: Configuring encryption and secret storage providers
- **security-best-practices**: Security guidelines for secrets management
