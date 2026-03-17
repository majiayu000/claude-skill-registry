---
name: secrets-management
description: Manages API keys, credentials, and sensitive configuration using secrets.json patterns with environment variable fallbacks. Use when working with API keys, credentials, .env files, or any sensitive configuration.
---

# Secrets Management Skill

## When to Activate

Activate this skill when:
- Setting up API keys or credentials
- Creating secrets.json files
- Implementing secrets loading patterns
- Working with .env files
- Integrating external APIs requiring authentication
- Ensuring credentials are not committed to git

## Core Principles

### Security Fundamentals
- **NEVER** hardcode API keys in source code
- **ALWAYS** add secrets.json to .gitignore immediately
- **ALWAYS** provide a secrets_template.json for setup reference
- Use environment variable fallbacks for CI/CD compatibility

### Standard File Structure

```
project/
├── secrets.json          # Actual secrets (NEVER commit)
├── secrets_template.json # Template with placeholder values (commit this)
├── .gitignore           # Must include secrets.json
└── .env                 # Alternative for env vars (also gitignored)
```

## Implementation Pattern

### secrets.json Format

```json
{
  "anthropic_api_key": "sk-ant-api03-...",
  "openrouter_api_key": "sk-or-v1-...",
  "openai_api_key": "sk-...",
  "database_url": "postgresql://user:pass@localhost/db",
  "comment": "Add your API keys here. Keep this file private."
}
```

### Python Loading Pattern

```python
import os
import json
from pathlib import Path

def load_secrets():
    """Load secrets from secrets.json with env var fallback."""
    secrets_path = Path(__file__).parent / "secrets.json"
    try:
        with open(secrets_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

SECRETS = load_secrets()

# Use with environment variable fallback
API_KEY = SECRETS.get("anthropic_api_key", os.getenv("ANTHROPIC_API_KEY", ""))
```

## Setup Checklist

1. Create secrets_template.json with placeholder values
2. Copy to secrets.json and add real credentials
3. Add secrets.json to .gitignore
4. Implement secrets loading in application
5. Verify git status shows secrets.json as untracked

## Security Best Practices

### DO ✅
- Store keys in secrets.json
- Add to .gitignore immediately
- Provide template files for setup
- Use environment variable fallbacks
- Rotate keys after team changes

### DON'T ❌
- Hardcode API keys
- Commit actual credentials
- Log full API keys
- Share keys via email/chat

## Key Format Reference

| Provider | Format |
|----------|--------|
| Anthropic | `sk-ant-api03-...` |
| OpenRouter | `sk-or-v1-...` |
| OpenAI | `sk-...` |
| AWS Access | `AKIA...` |

## Related Resources

See `AgentUsage/secrets_management.md` for complete documentation including:
- Advanced loading patterns with validation
- .env file integration
- Automated testing patterns
- Emergency key rotation procedures
- Production deployment strategies
