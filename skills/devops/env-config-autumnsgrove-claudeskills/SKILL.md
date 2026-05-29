---
name: env-config
description: Environment configuration and secrets management skill using UV for Python projects. Handles .env files, environment variables, secrets encryption, multi-environment setups, and secure configuration patterns. Use when setting up project environments, managing API keys, or implementing configuration best practices.
---

# Environment Configuration Skill

## Overview

This skill provides comprehensive guidance for managing environment configurations, secrets, and environment variables in Python projects using UV (the modern Python package and project manager). It covers secure configuration patterns, multi-environment setups, .env file management, and secrets handling with encryption support.

Environment configuration is critical for separating configuration from code (12-factor app principles), managing secrets securely across environments, preventing credential leaks, and supporting team collaboration.

## When to Use This Skill

Use this skill when you need to:
- Set up environment configuration for a new Python project
- Implement secure secrets management
- Configure multi-environment setups (dev/staging/prod)
- Migrate from hardcoded configs to environment variables
- Audit existing configuration for security issues
- Standardize configuration across team projects
- Set up UV-based Python project with proper config management

## Core Principles

### 1. Never Hardcode Secrets
- All API keys, passwords, tokens go in environment variables or encrypted secrets
- Configuration files with secrets must be in .gitignore
- Use templates for sharing structure, not actual secrets

### 2. Separate by Environment
- Different configurations for development, staging, production
- Environment-specific .env files (.env.development, .env.production)
- Clear naming conventions for environment variables

### 3. Fail Securely
- Validate required environment variables on startup
- Provide clear error messages for missing configuration
- Use sensible defaults only for non-sensitive values

### 4. Use UV for Dependency Management
- UV provides fast, reliable Python package management
- Replaces pip, pip-tools, virtualenv, and more
- Ensures reproducible environments across machines

### 5. Document Everything
- Template files show structure without exposing secrets
- README explains required variables and how to set them
- Comments describe purpose and format of variables

## UV Setup

### Installing UV

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with pip
pip install uv

# Verify installation
uv --version
```

### Initialize UV Project

```bash
# Create new project
uv init my-project
cd my-project

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Add dependencies
uv add python-dotenv cryptography pydantic

# Add dev dependencies
uv add --dev pytest pytest-env black ruff
```

## Environment Configuration Workflow

### Phase 1: Project Setup

**1. Create Project Structure**

```bash
# Initialize UV project
uv init your-project-name
cd your-project-name
uv venv
source .venv/bin/activate
```

**2. Install Configuration Dependencies**

```bash
uv add python-dotenv      # For .env file loading
uv add cryptography       # For secrets encryption (optional)
uv add pydantic          # For config validation (optional)
uv add --dev pytest pytest-env
```

**3. Create Configuration Files**

Essential files to create:
- `.env.template` - Template showing required variables (commit this)
- `.env` - Actual secrets (add to .gitignore)
- `.env.development` - Development-specific config
- `.env.production` - Production-specific config
- `config.py` - Configuration loading module

**4. Update .gitignore**

```bash
# Add to .gitignore
cat >> .gitignore << 'EOF'
# Environment files
.env
.env.local
.env.*.local
secrets.json

# UV
.venv/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/
EOF
```

### Phase 2: Create Configuration Templates

**1. Create .env.template**

```bash
# .env.template - Commit this file
# Copy to .env and fill in actual values

# Application Settings
APP_NAME=MyApp
APP_ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_POOL_SIZE=5

# API Keys (Replace with actual keys)
ANTHROPIC_API_KEY=sk-ant-api03-xxx
OPENAI_API_KEY=sk-xxx
OPENROUTER_API_KEY=sk-or-v1-xxx

# Security
SECRET_KEY=generate-random-secret-key-here
JWT_SECRET=another-random-secret

# Feature Flags
ENABLE_ANALYTICS=false
ENABLE_CACHING=true
```

**2. Create Config Loading Module**

Create `config.py` - see `references/api-reference.md` for complete implementation:

```python
import os
from pathlib import Path
from dotenv import load_dotenv


class ConfigError(Exception):
    """Raised when required configuration is missing."""
    pass


class Config:
    """Application configuration from environment variables."""

    def __init__(self, env: str = None):
        self.env = env or os.getenv('APP_ENV', 'development')
        self._load_env_file()
        self._validate_required()

    def _load_env_file(self):
        """Load appropriate .env file based on environment."""
        env_file = Path(f'.env.{self.env}')
        if env_file.exists():
            load_dotenv(env_file, override=True)
        if Path('.env').exists():
            load_dotenv('.env', override=False)

    @property
    def app_name(self) -> str:
        return os.getenv('APP_NAME', 'MyApp')

    @property
    def debug(self) -> bool:
        return os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes')

    # Add more properties as needed...


# Global config instance
config = Config()
```

For complete Config class with all properties and validation, see `references/api-reference.md`.

**3. Use Config in Application**

```python
from config import config

def main():
    print(f"Starting {config.app_name} in {config.app_env} mode")

    if config.anthropic_api_key:
        # Use API key
        print("✓ API key loaded")
```

### Phase 3: Multi-Environment Setup

**1. Create Environment-Specific Files**

`.env.development`:
```bash
APP_ENV=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://localhost:5432/myapp_dev
```

`.env.production`:
```bash
APP_ENV=production
DEBUG=false
LOG_LEVEL=WARNING
DATABASE_URL=postgresql://prod-host:5432/myapp_prod
SECRET_KEY=super-secure-random-key
```

**2. Switch Between Environments**

```bash
# Development (default)
uv run python main.py

# Production
export APP_ENV=production
uv run python main.py
```

### Phase 4: Secrets Management

**1. Using JSON Secrets (Alternative Pattern)**

Create `secrets_template.json`:
```json
{
  "anthropic_api_key": "sk-ant-api03-xxx",
  "openai_api_key": "sk-xxx",
  "database_password": "your-password-here",
  "comment": "Copy to secrets.json and fill in real values"
}
```

**2. Load JSON Secrets**

See `references/api-reference.md` for complete implementation:

```python
import json
from pathlib import Path

def load_secrets(secrets_file: str = 'secrets.json') -> dict:
    """Load secrets from JSON with fallback to env vars."""
    if Path(secrets_file).exists():
        return json.load(open(secrets_file))
    # Fallback to environment variables
    return {
        'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', '')
    }
```

**3. Encrypted Secrets**

For encryption utilities and advanced secrets management, see:
- `references/advanced-topics.md` - Encryption, rotation, auditing
- `scripts/env_helper.py` - Encryption/decryption utilities

## Configuration Validation

### Using Pydantic for Type-Safe Config

```python
from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    app_name: str = Field(default='MyApp', env='APP_NAME')
    app_env: str = Field(default='development', env='APP_ENV')
    database_url: str = Field(..., env='DATABASE_URL')  # Required

    @validator('app_env')
    def validate_env(cls, v):
        allowed = ['development', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f'app_env must be one of {allowed}')
        return v

    class Config:
        env_file = '.env'


settings = Settings()
```

For complete Pydantic configuration examples, see `references/api-reference.md`.

## Security Best Practices

### 1. .gitignore Configuration

Always add to `.gitignore`:
```
.env
.env.local
.env.*.local
secrets.json
.env.production
.venv/
```

### 2. Secret Rotation

Implement regular API key rotation:
```python
def rotate_api_key(old_key: str, new_key: str):
    """Rotate API key gracefully with backup."""
    # Implementation in references/advanced-topics.md
```

### 3. Environment Auditing

Regular security audits:
```python
def audit_environment():
    """Check for security issues in environment variables."""
    # Implementation in references/advanced-topics.md
```

For complete security implementations, see `references/advanced-topics.md`.

## Testing Configuration

### Basic Test Setup

```python
# conftest.py
import pytest
import os


@pytest.fixture
def test_env():
    """Set up test environment variables."""
    original = os.environ.copy()
    os.environ['APP_ENV'] = 'testing'
    os.environ['DEBUG'] = 'true'
    yield
    os.environ.clear()
    os.environ.update(original)


@pytest.fixture
def config(test_env):
    from config import Config
    return Config(env='testing')
```

### Example Tests

```python
def test_config_loading(config):
    assert config.app_env == 'testing'
    assert config.debug is True


def test_missing_required_var():
    from config import ConfigError
    with pytest.raises(ConfigError):
        Config()  # Missing required vars
```

For comprehensive testing guide, see `references/testing-guide.md`.

## UV Commands Reference

```bash
# Dependency management
uv sync                    # Install all dependencies
uv add requests           # Add dependency
uv add --dev pytest       # Add dev dependency
uv remove requests        # Remove dependency

# Environment management
uv venv                   # Create virtual environment
uv lock --upgrade         # Update dependencies

# Running scripts
uv run python main.py     # Run with UV environment
uv run pytest            # Run tests

# Compatibility
uv pip compile pyproject.toml -o requirements.txt
```

## Helper Scripts

This skill provides utility scripts in `scripts/`:

- `env_helper.py` - Core utilities for env management
  - Parse and validate .env files
  - Check for missing variables
  - Encrypt/decrypt secrets files
  - Compare environments
  - Generate .env templates

Usage:
```bash
# Validate .env file
python scripts/env_helper.py validate .env

# Encrypt secrets
python scripts/env_helper.py encrypt secrets.json secrets.encrypted

# Compare environments
python scripts/env_helper.py compare .env.development .env.production
```

## Quick Reference

### Setup Checklist

- [ ] Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Create project: `uv init project-name`
- [ ] Create virtual env: `uv venv`
- [ ] Add dependencies: `uv add python-dotenv`
- [ ] Create `.env.template` from examples
- [ ] Copy to `.env` and fill in secrets
- [ ] Add `.env` to `.gitignore`
- [ ] Create `config.py` module
- [ ] Test configuration loading
- [ ] Set up environment-specific configs
- [ ] Implement validation
- [ ] Add tests for configuration

### Environment Variable Naming

Use consistent naming:
- `APP_*` - Application settings
- `DATABASE_*` - Database configuration
- `*_API_KEY` - API keys and tokens
- `*_SECRET` - Secret keys
- `ENABLE_*` - Feature flags
- `*_URL` - Service endpoints

### Security Checklist

- [ ] No secrets in version control
- [ ] `.env` in `.gitignore`
- [ ] Production secrets separate from dev
- [ ] Required variables validated on startup
- [ ] Secrets encrypted at rest (if needed)
- [ ] Regular secret rotation
- [ ] Team training on secure practices

## Additional Resources

### Documentation in This Skill

- **`references/api-reference.md`** - Complete Config class implementation, Pydantic validation, JSON secrets loading
- **`references/advanced-topics.md`** - Encryption, secret rotation, auditing, multi-tenant config, cloud integration
- **`references/testing-guide.md`** - pytest setup, mocking, validation testing, CI/CD examples
- **`references/troubleshooting.md`** - Common issues, environment-specific problems, debugging techniques

### Examples Directory

- `.env.example` - Comprehensive .env template
- `pyproject.toml` - UV project configuration
- `secrets_template.json` - JSON secrets template

### External Resources

- **UV Documentation**: https://docs.astral.sh/uv/
- **python-dotenv**: https://github.com/theskumar/python-dotenv
- **Pydantic**: https://docs.pydantic.dev/
- **12-Factor App Config**: https://12factor.net/config

## Troubleshooting

For common issues and solutions, see `references/troubleshooting.md`:

- Environment variables not loading
- Wrong environment loaded
- UV sync failures
- Import errors
- Secrets decryption issues
- Performance optimization
- Security issues and remediation
- Docker integration problems

Quick debug:
```python
from dotenv import load_dotenv
load_dotenv(verbose=True)  # Shows loading process
```
