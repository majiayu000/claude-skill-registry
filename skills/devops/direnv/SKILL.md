---
name: direnv
description: Direnv environment management for automatic per-project shell configuration. Use when setting up .envrc files, configuring project-specific environment variables, or integrating direnv with development tools like nix, asdf, pyenv, or nvm.
user-invocable: false
---

# Direnv Skill

This skill provides direnv configuration patterns and best practices for automatic environment management.

## Basic .envrc Structure

```bash
# .envrc - Auto-loaded when entering directory

# Environment variables
export DATABASE_URL="postgresql://localhost:5432/myapp_dev"
export API_KEY="dev-key-only"
export DEBUG=true

# PATH modifications
PATH_add bin
PATH_add scripts

# Source additional files
source_env_if_exists .envrc.local
```

## Security Best Practices

### Never Commit Secrets

```bash
# .envrc - Committed to repo (safe defaults only)
export DATABASE_URL="${DATABASE_URL:-postgresql://localhost:5432/dev}"
export LOG_LEVEL="${LOG_LEVEL:-debug}"

# Load local overrides with real secrets
source_env_if_exists .envrc.local
```

```bash
# .envrc.local - NEVER commit (add to .gitignore)
export DATABASE_URL="postgresql://user:real_password@prod-db:5432/prod"
export API_KEY="sk-real-production-key"
```

### .gitignore Entry

```gitignore
# Always ignore local environment overrides
.envrc.local
.envrc.private
```

## Built-in Functions

### Path Management

```bash
# Add to PATH (prepends)
PATH_add bin
PATH_add node_modules/.bin
PATH_add .venv/bin

# Add to PATH only if directory exists
path_add bin 2>/dev/null || true
```

### Environment Loading

```bash
# Source another envrc if it exists
source_env_if_exists ../.envrc
source_env_if_exists .envrc.local

# Load from .env file
dotenv
dotenv_if_exists .env.local

# Source a file (error if missing)
source_env .envrc.shared
```

### Layout Functions

```bash
# Python virtual environment
layout python
layout python3
layout pyenv 3.11.0

# Node.js
layout node

# Ruby
layout ruby

# Go
layout go
```

## Language-Specific Patterns

### Python Projects

```bash
# .envrc for Python with uv/pip
layout python3

# Or with specific version via pyenv
layout pyenv 3.11

# Environment variables
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Django settings
export DJANGO_SETTINGS_MODULE="config.settings.local"
export DJANGO_DEBUG=true

# Database
export DATABASE_URL="${DATABASE_URL:-postgresql://localhost:5432/myapp_dev}"

# Load secrets from local file
source_env_if_exists .envrc.local
```

### Node.js Projects

```bash
# .envrc for Node.js
layout node

# Use specific Node version with nvm
use nvm 20

# Or with asdf
use asdf

# Add local binaries to path
PATH_add node_modules/.bin

# Environment
export NODE_ENV=development
export PORT=3000

source_env_if_exists .envrc.local
```

### Go Projects

```bash
# .envrc for Go
layout go

# Set Go-specific vars
export CGO_ENABLED=0
export GOFLAGS="-mod=vendor"

source_env_if_exists .envrc.local
```

### Rust Projects

```bash
# .envrc for Rust
export CARGO_HOME="${PWD}/.cargo"
export RUSTUP_HOME="${PWD}/.rustup"
PATH_add target/debug
PATH_add target/release

source_env_if_exists .envrc.local
```

## Integration Patterns

### With asdf Version Manager

```bash
# .envrc with asdf
use asdf

# This reads .tool-versions and sets up all tools
# Ensure .tool-versions exists:
# python 3.11.0
# nodejs 20.10.0
# postgres 15.0
```

### With Nix

```bash
# .envrc with nix-shell
use nix

# Or with flakes
use flake

# With specific nixpkgs
use nix -p python311 nodejs_20
```

### With Docker Compose

```bash
# .envrc for Docker-based development
export COMPOSE_PROJECT_NAME="myapp"
export COMPOSE_FILE="docker-compose.yml:docker-compose.dev.yml"

# Container environment
export DOCKER_BUILDKIT=1

source_env_if_exists .envrc.local
```

## Monorepo Patterns

### Root .envrc

```bash
# /monorepo/.envrc
export MONOREPO_ROOT="${PWD}"
export PATH="${MONOREPO_ROOT}/scripts:${PATH}"

# Shared configuration
export LOG_FORMAT=json
export TZ=UTC
```

### Service .envrc

```bash
# /monorepo/services/api/.envrc

# Inherit from parent
source_env ../.envrc

# Service-specific
export SERVICE_NAME="api"
export PORT=8080

layout python3
```

## Strict Mode Pattern

```bash
# .envrc with strict requirements
strict_env

# Now all required vars must be set
: "${DATABASE_URL:?DATABASE_URL must be set}"
: "${API_KEY:?API_KEY must be set}"

# Or provide defaults
export LOG_LEVEL="${LOG_LEVEL:-info}"
```

## Common Patterns

### Watch and Reload

```bash
# .envrc
watch_file .tool-versions
watch_file requirements.txt
watch_file package.json

# Reload when these files change
```

### Conditional Configuration

```bash
# .envrc with conditional logic
if has python3; then
  layout python3
elif has python; then
  layout python
fi

if [[ -f "package.json" ]]; then
  PATH_add node_modules/.bin
fi
```

### Export Functions

```bash
# .envrc with helper functions
export_function() {
  local name=$1
  local body=$2
  eval "$name() { $body; }"
  export -f "$name"
}

export_function run_tests "pytest tests/ -v"
export_function lint "ruff check . && mypy ."
```

## Anti-Patterns to Avoid

```bash
# ❌ Bad: Hardcoded secrets
export API_KEY="sk-live-abc123"

# ✅ Good: Use local overrides
export API_KEY="${API_KEY:-}"
source_env_if_exists .envrc.local

# ❌ Bad: Absolute paths
export VENV_PATH="/Users/john/projects/myapp/.venv"

# ✅ Good: Relative paths
export VENV_PATH="${PWD}/.venv"

# ❌ Bad: Modifying system paths
export PATH="/usr/local/custom:${PATH}"

# ✅ Good: Use PATH_add for project paths
PATH_add bin
```

## Setup Commands

```bash
# Install direnv (macOS)
brew install direnv

# Install direnv (Ubuntu/Debian)
sudo apt install direnv

# Add to shell (bash)
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

# Add to shell (zsh)
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc

# Add to shell (fish)
echo 'direnv hook fish | source' >> ~/.config/fish/config.fish

# Allow .envrc in current directory
direnv allow

# Reload after changes
direnv reload

# Block .envrc
direnv deny
```
