---
name: python-env
description: Python environment variable management using .env files and python-dotenv for simple projects
---

# Python Environment Variable Management

**Focus**: Managing environment variables in Python projects using `.env` files

**Source**: Patterns extracted from Google Sheets automation project, ss-automation, and general Python best practices

---

## When to Use This Skill

Use python-env when:
- ✓ Starting a new Python project that needs configuration
- ✓ Simple projects without enterprise secret management (no Doppler/Vault)
- ✓ Open-source projects where contributors can't access your secret manager
- ✓ Local development environment setup
- ✓ Quick prototypes needing configuration

**DO NOT use for:**
- ✗ Production secrets with compliance requirements (use Doppler/Vault/AWS Secrets Manager)
- ✗ Multi-team projects with shared secrets (use centralized secret manager)
- ✗ Projects already using Doppler (see CLAUDE.md Principle #13)

---

## Two-Tier Architecture

| Project Type | Configuration Approach | When to Use |
|--------------|----------------------|-------------|
| **Simple** | `.env` + `python-dotenv` | Solo/small team, no compliance needs |
| **Complex** | Doppler + `doppler run` | Team secrets, AWS, production |

**Decision tree**:
```
Does project have compliance requirements (SOC2, HIPAA, etc.)?
├── YES → Use Doppler/Vault (see CLAUDE.md Principle #13)
└── NO → Continue...
         Does project have team-shared secrets?
         ├── YES → Use Doppler (shared secrets need single source)
         └── NO → Use .env pattern (this skill)
```

---

## Core Principles

### 1. Single Load Point

Load environment variables **once** at application entry point, not scattered throughout code.

```python
# ✅ GOOD: Single load point
# src/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # Load once

DATABASE_URL = os.environ['DATABASE_URL']
API_KEY = os.environ['API_KEY']

# ❌ BAD: Scattered loading
# src/database.py
from dotenv import load_dotenv
load_dotenv()  # Loading again!

# src/api.py
from dotenv import load_dotenv
load_dotenv()  # And again!
```

### 2. Validate at Startup (Fail Fast)

Validate ALL required environment variables at application startup, not when first used.

```python
# src/config.py
from dotenv import load_dotenv
import os

load_dotenv()

REQUIRED_VARS = [
    'DATABASE_URL',
    'API_KEY',
    'SECRET_KEY',
]

def validate_config():
    """Validate required configuration at startup."""
    missing = [var for var in REQUIRED_VARS if not os.environ.get(var)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {missing}\n"
            f"Copy .env.example to .env and fill in values."
        )

# Call at import time
validate_config()

# Export validated config
DATABASE_URL = os.environ['DATABASE_URL']
API_KEY = os.environ['API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
```

### 3. File Hierarchy

Use hierarchical `.env` files for different contexts:

```
project/
├── .env.example     # Template (committed to git)
├── .env             # Shared defaults (gitignored, optional)
├── .env.local       # Personal overrides (gitignored, highest priority)
└── .env.test        # Test environment (gitignored)
```

**Priority order** (highest to lowest):
1. `.env.local` - Personal settings (API keys, local paths)
2. `.env` - Shared defaults
3. `.env.example` - Documentation only (committed)

**Loading pattern**:
```python
from dotenv import load_dotenv

# Load in reverse priority (last loaded wins with override=True)
load_dotenv('.env')           # Base defaults
load_dotenv('.env.local', override=True)  # Personal overrides
```

### 4. Gitignore Security

**Always** gitignore actual `.env` files:

```gitignore
# Environment variables
.env
.env.local
.env.*.local
.env.test

# Keep example (documentation)
!.env.example
```

### 5. Document with .env.example

Create `.env.example` as documentation and template:

```bash
# .env.example - Copy to .env and fill in values

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# API Keys (get from: https://example.com/api-keys)
API_KEY=your-api-key-here
SECRET_KEY=generate-with-openssl-rand-hex-32

# Optional Configuration
DEBUG=false
LOG_LEVEL=INFO
```

**Best practices for .env.example**:
- Use placeholder values that clearly need replacing
- Add comments explaining where to get values
- Group related variables with headers
- Mark optional vs required variables

---

## Quick Start

### 1. Install python-dotenv

```bash
pip install python-dotenv
```

### 2. Create .env.example

```bash
# .env.example
DATABASE_URL=postgresql://localhost/mydb
API_KEY=your-api-key-here
DEBUG=false
```

### 3. Create src/config.py

```python
"""
Application configuration.

Load environment variables from .env files and validate required configuration.
"""
from pathlib import Path
from dotenv import load_dotenv
import os

# Determine project root
PROJECT_ROOT = Path(__file__).parent.parent

# Load environment variables (order matters: later overrides earlier)
load_dotenv(PROJECT_ROOT / '.env')
load_dotenv(PROJECT_ROOT / '.env.local', override=True)

# Required variables (fail fast if missing)
REQUIRED = ['DATABASE_URL', 'API_KEY']

def _validate():
    missing = [v for v in REQUIRED if not os.environ.get(v)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {missing}\n"
            f"Copy .env.example to .env and fill in values:\n"
            f"  cp .env.example .env"
        )

_validate()

# Export configuration
DATABASE_URL = os.environ['DATABASE_URL']
API_KEY = os.environ['API_KEY']
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
```

### 4. Update .gitignore

```gitignore
# Environment variables
.env
.env.local
.env.*.local
!.env.example
```

### 5. Copy template and configure

```bash
cp .env.example .env
# Edit .env with your values
```

---

## Patterns

### Pattern 1: Type-Safe Configuration

Convert string environment variables to proper types:

```python
# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Boolean
DEBUG = os.environ.get('DEBUG', 'false').lower() in ('true', '1', 'yes')

# Integer
PORT = int(os.environ.get('PORT', '8000'))
TIMEOUT = int(os.environ.get('TIMEOUT', '30'))

# Float
RATE_LIMIT = float(os.environ.get('RATE_LIMIT', '1.0'))

# List (comma-separated)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# Optional (with explicit None)
OPTIONAL_API_KEY = os.environ.get('OPTIONAL_API_KEY')  # None if not set
```

### Pattern 2: Configuration Class

Organize related configuration into classes:

```python
# src/config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class DatabaseConfig:
    host: str = os.environ.get('DB_HOST', 'localhost')
    port: int = int(os.environ.get('DB_PORT', '5432'))
    user: str = os.environ.get('DB_USER', 'postgres')
    password: str = os.environ.get('DB_PASSWORD', '')
    database: str = os.environ.get('DB_NAME', 'mydb')

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

@dataclass(frozen=True)
class APIConfig:
    key: str = os.environ.get('API_KEY', '')
    secret: str = os.environ.get('API_SECRET', '')
    timeout: int = int(os.environ.get('API_TIMEOUT', '30'))

# Singleton instances
db = DatabaseConfig()
api = APIConfig()

# Usage: from config import db, api
# print(db.url)
# print(api.key)
```

### Pattern 3: Environment-Specific Loading

Load different configurations based on environment:

```python
# src/config.py
import os
from dotenv import load_dotenv

# Determine environment
ENV = os.environ.get('ENV', 'development')

# Load base config
load_dotenv('.env')

# Load environment-specific config
if ENV == 'production':
    load_dotenv('.env.production', override=True)
elif ENV == 'test':
    load_dotenv('.env.test', override=True)
else:
    load_dotenv('.env.local', override=True)

# Always override with local (for development)
if ENV != 'production':
    load_dotenv('.env.local', override=True)
```

### Pattern 4: Credential File Paths

For credentials stored in files (like Google Service Account):

```python
# .env
GOOGLE_CREDENTIALS_PATH=credentials.json
SHEET_NAME=My Dashboard

# src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent

# Resolve path relative to project root
GOOGLE_CREDENTIALS_PATH = PROJECT_ROOT / os.environ.get(
    'GOOGLE_CREDENTIALS_PATH',
    'credentials.json'
)

def validate_files():
    """Validate required files exist."""
    if not GOOGLE_CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            f"Credentials file not found: {GOOGLE_CREDENTIALS_PATH}\n"
            f"See docs/GOOGLE_SETUP.md for setup instructions."
        )

validate_files()

SHEET_NAME = os.environ.get('SHEET_NAME', 'Dashboard')
```

---

## Anti-Patterns

### 1. Loading .env in Multiple Places

```python
# ❌ BAD: Multiple load points cause confusion
# database.py
from dotenv import load_dotenv
load_dotenv()

# api.py
from dotenv import load_dotenv
load_dotenv()  # Which .env file? What order?

# ✅ GOOD: Single config module
# database.py
from config import DATABASE_URL

# api.py
from config import API_KEY
```

### 2. Silent Fallbacks for Required Variables

```python
# ❌ BAD: Silent fallback hides missing config
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
# What if someone forgot to set DATABASE_URL? Uses wrong database!

# ✅ GOOD: Fail fast for required variables
DATABASE_URL = os.environ['DATABASE_URL']  # Raises KeyError if missing

# Or with explicit validation
if not os.environ.get('DATABASE_URL'):
    raise ValueError("DATABASE_URL is required")
DATABASE_URL = os.environ['DATABASE_URL']
```

### 3. Committing .env Files

```bash
# ❌ BAD: Secrets in git history
git add .env
git commit -m "Add configuration"
# Now API keys are in git history forever!

# ✅ GOOD: Gitignore before first commit
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Ignore .env files"
```

### 4. Not Documenting Configuration

```bash
# ❌ BAD: No .env.example
# New developers: "What environment variables do I need?"

# ✅ GOOD: Self-documenting .env.example
# .env.example
# Database connection (required)
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# API key from https://example.com/api (required)
API_KEY=your-key-here

# Debug mode (optional, default: false)
DEBUG=false
```

---

## Testing with .env

### Pattern: Test-Specific Environment

```python
# conftest.py
import os
import pytest
from dotenv import load_dotenv

@pytest.fixture(scope='session', autouse=True)
def load_test_env():
    """Load test environment variables."""
    # Load test-specific .env
    load_dotenv('.env.test', override=True)

    # Or set test values directly
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['API_KEY'] = 'test-key'
```

### Pattern: Mock Environment Variables

```python
# test_config.py
import os
import pytest

def test_config_validates_required_vars(monkeypatch):
    """Test that missing required vars raise error."""
    # Remove required variable
    monkeypatch.delenv('API_KEY', raising=False)

    # Should raise on import
    with pytest.raises(ValueError, match="Missing required"):
        import importlib
        import config
        importlib.reload(config)

def test_config_uses_defaults(monkeypatch):
    """Test that optional vars have defaults."""
    monkeypatch.delenv('DEBUG', raising=False)

    from config import DEBUG
    assert DEBUG == False  # Default value
```

---

## File Organization

```
.claude/skills/python-env/
├── SKILL.md              # This file (entry point)
├── PATTERNS.md           # Additional patterns (if needed)
└── examples/
    ├── simple_config.py  # Basic configuration example
    └── typed_config.py   # Type-safe configuration class
```

---

## Integration with CLAUDE.md

This skill complements CLAUDE.md Principle #13 (Secret Management Discipline):

| Scenario | Use This Skill | Use Doppler (Principle #13) |
|----------|---------------|---------------------------|
| Simple project | ✅ | ❌ |
| Team secrets | ❌ | ✅ |
| Production | ❌ | ✅ |
| Local development | ✅ | ✅ (via `doppler run`) |
| Open-source | ✅ | ❌ (contributors can't access) |

**Principle overlap**:
- Both emphasize **fail fast** validation
- Both use **single source of truth** (one config file/service)
- Both require **gitignore for secrets**

---

## References

- [python-dotenv documentation](https://github.com/theskumar/python-dotenv)
- [12-Factor App: Config](https://12factor.net/config)
- CLAUDE.md Principle #1 (Defensive Programming - validate at startup)
- CLAUDE.md Principle #13 (Secret Management Discipline - for complex projects)
