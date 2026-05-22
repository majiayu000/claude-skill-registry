---
name: mise-environment-management
description: Use when managing environment variables and project settings with Mise. Covers env configuration, direnv replacement, and per-directory settings.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Mise - Environment Management

Managing environment variables, project settings, and directory-specific configuration with Mise.

## Basic Environment Variables

### Defining Environment Variables

```toml
# mise.toml
[env]
NODE_ENV = "production"
DATABASE_URL = "postgresql://localhost/myapp"
API_KEY = "development-key"
LOG_LEVEL = "info"
```

### Loading Environment

```bash
# Activate mise environment
mise activate bash  # Or zsh, fish

# Or use mise exec
mise exec -- node app.js

# Or mise run
mise run start
```

## Advanced Environment Configuration

### Template Variables

```toml
[env]
PROJECT_ROOT = "{{ config_root }}"
DATA_DIR = "{{ config_root }}/data"
LOG_FILE = "{{ config_root }}/logs/app.log"
```

### Environment File Loading

```toml
[env]
_.file = ".env"
_.file = [".env", ".env.local"]
```

### Conditional Environment Variables

```toml
[env]
# Set based on other variables
DATABASE_URL = "postgresql://{{ env.DB_HOST | default(value='localhost') }}/{{ env.DB_NAME }}"
```

## Path Management

### Adding to PATH

```toml
[env]
_.path = [
  "{{ config_root }}/bin",
  "{{ config_root }}/scripts",
  "/usr/local/bin"
]
```

### Library Paths

```toml
[env]
LD_LIBRARY_PATH = "{{ config_root }}/lib:$LD_LIBRARY_PATH"
DYLD_LIBRARY_PATH = "{{ config_root }}/lib:$DYLD_LIBRARY_PATH"
```

## Tool-Specific Environments

### Python Virtual Environment

```toml
[tools]
python = "3.12"

[env]
_.python.venv = { path = ".venv", create = true }
VIRTUAL_ENV = "{{ config_root }}/.venv"
```

### Node.js Environment

```toml
[tools]
node = "20.10.0"

[env]
NODE_ENV = "development"
NODE_OPTIONS = "--max-old-space-size=4096"
NPM_CONFIG_PREFIX = "{{ config_root }}/.npm-global"
```

### Go Environment

```toml
[tools]
go = "1.21"

[env]
GOPATH = "{{ config_root }}/.go"
GOBIN = "{{ config_root }}/.go/bin"
GO111MODULE = "on"
```

## Replacing direnv

### Basic direnv Replacement

```toml
# Instead of .envrc
# export DATABASE_URL=postgresql://localhost/myapp
# export NODE_ENV=development

# Use mise.toml
[env]
DATABASE_URL = "postgresql://localhost/myapp"
NODE_ENV = "development"
```

### Allowed Directories

```toml
# mise.toml - mark as trusted
[settings]
experimental_monorepo_root = true  # Trust subdirectories
```

### Watch File Changes

Mise automatically reloads when mise.toml changes, similar to direnv.

## Hierarchical Configuration

### Global Settings

```toml
# ~/.config/mise/config.toml
[env]
EDITOR = "code"
GIT_AUTHOR_NAME = "Your Name"
GIT_AUTHOR_EMAIL = "you@example.com"
```

### Project Settings

```toml
# ~/projects/myapp/mise.toml
[env]
PROJECT_NAME = "myapp"
DATABASE_URL = "postgresql://localhost/myapp"
```

### Local Overrides

```toml
# ~/projects/myapp/mise.local.toml (gitignored)
[env]
DATABASE_URL = "postgresql://localhost/myapp-dev"
DEBUG = "true"
```

## Sensitive Data

### Environment Files

```toml
# mise.toml
[env]
_.file = ".env.local"  # Gitignored file with secrets
```

```bash
# .env.local (add to .gitignore)
API_KEY=secret-key-here
DATABASE_PASSWORD=secret-password
```

### Using System Environment

```toml
[env]
# Reference existing environment variables
API_KEY = "$API_KEY"
DATABASE_URL = "$DATABASE_URL"
```

### Secure Secrets Management

```bash
# Don't commit secrets to mise.toml
# Instead, reference from external secret managers

# Example with 1Password CLI
mise exec -- op run -- node app.js

# Or load from encrypted file
mise exec -- sops exec-env .env.encrypted -- node app.js
```

## Mise Environment Variables

### Built-in Variables

Mise provides these variables automatically:

```bash
$MISE_ORIGINAL_CWD      # Directory where mise was invoked
$MISE_CONFIG_ROOT       # Directory containing mise.toml
$MISE_PROJECT_ROOT      # Project root directory
$MISE_DATA_DIR          # Mise data directory
$MISE_CACHE_DIR         # Mise cache directory
```

### Using in Configuration

```toml
[env]
PROJECT_ROOT = "{{ env.MISE_PROJECT_ROOT }}"
CONFIG_FILE = "{{ env.MISE_CONFIG_ROOT }}/config.yaml"
```

## Configuration Validation

### Check Current Environment

```bash
# Show current environment
mise env

# Show specific variable
mise env DATABASE_URL

# Export as shell commands
mise env -s bash > .env.sh
source .env.sh
```

### Verify Configuration

```bash
# Check loaded config files
mise config

# Show resolved settings
mise settings
```

## Best Practices

### Separate Public and Private Config

```toml
# mise.toml (committed)
[env]
NODE_ENV = "development"
LOG_LEVEL = "info"
API_URL = "https://api.example.com"

# mise.local.toml (gitignored)
[env]
API_KEY = "secret-key"
DATABASE_PASSWORD = "secret-password"
```

### Use Descriptive Variable Names

```toml
# Good: Clear, descriptive names
[env]
DATABASE_CONNECTION_POOL_SIZE = "10"
API_REQUEST_TIMEOUT_MS = "5000"
FEATURE_FLAG_NEW_UI = "true"

# Avoid: Vague abbreviations
[env]
DB_POOL = "10"
TIMEOUT = "5000"
FLAG = "true"
```

### Document Required Variables

```toml
# mise.toml
[env]
# Database configuration (required)
DATABASE_URL = "postgresql://localhost/myapp"

# API keys (set in mise.local.toml)
# API_KEY = "your-key-here"

# Optional feature flags
FEATURE_ANALYTICS = "false"
```

### Use Templates for Paths

```toml
# Good: Relative to config root
[env]
DATA_DIR = "{{ config_root }}/data"
LOGS_DIR = "{{ config_root }}/logs"

# Avoid: Hardcoded paths
[env]
DATA_DIR = "/Users/me/project/data"
```

## Common Patterns

### Multi-Environment Setup

```toml
# mise.toml - base configuration
[env]
APP_NAME = "myapp"
LOG_FORMAT = "json"

# mise.development.toml
[env]
NODE_ENV = "development"
DEBUG = "true"
DATABASE_URL = "postgresql://localhost/myapp_dev"

# mise.production.toml
[env]
NODE_ENV = "production"
DEBUG = "false"
DATABASE_URL = "postgresql://prod-server/myapp"
```

```bash
# Switch environments
ln -sf mise.development.toml mise.local.toml
# Or
ln -sf mise.production.toml mise.local.toml
```

### Database Configuration

```toml
[env]
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "myapp"
DATABASE_USER = "postgres"
DATABASE_URL = "postgresql://{{ env.DATABASE_USER }}:{{ env.DATABASE_PASSWORD }}@{{ env.DATABASE_HOST }}:{{ env.DATABASE_PORT }}/{{ env.DATABASE_NAME }}"
```

### Feature Flags

```toml
[env]
# Feature toggles
FEATURE_NEW_DASHBOARD = "true"
FEATURE_BETA_API = "false"
FEATURE_EXPERIMENTAL_CACHE = "true"

# Feature rollout percentages
FEATURE_NEW_CHECKOUT_ROLLOUT = "25"
```

### CI/CD Environment

```toml
# mise.toml
[env]
NODE_ENV = "{{ env.CI | default(value='development') }}"
SKIP_PREFLIGHT_CHECK = "{{ env.CI | default(value='false') }}"
```

## Anti-Patterns

### Don't Commit Secrets

```toml
# Bad: Secrets in committed file
[env]
API_KEY = "sk-secret-key-12345"
DATABASE_PASSWORD = "password123"

# Good: Reference from secure location
[env]
_.file = ".env.local"  # Gitignored
```

### Don't Duplicate Global Config

```toml
# Bad: Repeating global settings in every project
# ~/project-a/mise.toml
[env]
EDITOR = "code"
GIT_AUTHOR_NAME = "Your Name"

# ~/project-b/mise.toml
[env]
EDITOR = "code"
GIT_AUTHOR_NAME = "Your Name"

# Good: Use global config
# ~/.config/mise/config.toml
[env]
EDITOR = "code"
GIT_AUTHOR_NAME = "Your Name"
```

### Don't Hardcode Environment Names

```toml
# Bad: Hardcoded check
[tasks.deploy]
run = '''
if [ "$NODE_ENV" = "production" ]; then
  ./deploy-prod.sh
fi
'''

# Good: Use configuration
[tasks.deploy]
env = { DEPLOYMENT_TARGET = "production" }
run = "./deploy.sh"
```

## Advanced Patterns

### Dynamic Environment Loading

```toml
[env]
# Load environment based on git branch
BRANCH = "{{ exec(command='git branch --show-current') }}"
DEPLOY_ENV = "{{ env.BRANCH | replace(from='main', to='production') | replace(from='develop', to='staging') }}"
```

### Computed Variables

```toml
[env]
PROJECT_NAME = "myapp"
NAMESPACE = "{{ env.PROJECT_NAME }}-{{ env.ENVIRONMENT }}"
REDIS_URL = "redis://{{ env.NAMESPACE }}-redis:6379"
```

### Environment Inheritance

```toml
# Base configuration
[env]
LOG_LEVEL = "info"
CACHE_TTL = "3600"

# Override in specific contexts
[env.production]
LOG_LEVEL = "warn"
CACHE_TTL = "7200"
```

## Related Skills

- **task-configuration**: Using environment variables in tasks
- **tool-management**: Tool-specific environment configuration
