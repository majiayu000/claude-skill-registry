---
name: api-credentials
description: Securely manages API credentials for multiple providers (Anthropic Claude, Google Gemini, GitHub). Use when skills need to access stored API keys for external service invocations.
metadata:
  version: 0.0.3
---

# API Credentials Management

**🚨 DEPRECATED: This skill is no longer needed for hosted skills environments.**

**New approach:** Skills now read credentials directly from project knowledge files:
- `ANTHROPIC_API_KEY.txt`, `GOOGLE_API_KEY.txt`, `GITHUB_API_KEY.txt` (recommended)
- Or `API_CREDENTIALS.json` (combined file)

See updated skill documentation:
- [orchestrating-agents](../orchestrating-agents/SKILL.md#setup)
- [invoking-gemini](../invoking-gemini/SKILL.md#setup)
- [invoking-github](../invoking-github/SKILL.md#quick-start)

**Legacy use only:** This skill may still be useful for local development environments or backward compatibility.

---

**⚠️ WARNING: This is a PERSONAL skill - DO NOT share or commit with actual credentials!**

This skill provides secure storage and retrieval of API credentials for multiple providers. It serves as a dependency for other skills that need to invoke external APIs programmatically.

## Supported Providers

- **Anthropic** (Claude API)
- **Google** (Gemini API, Vertex AI, etc.)
- **GitHub** (GitHub API, Personal Access Tokens)
- Extensible for additional providers

## Purpose

- Centralized credential storage for multiple API providers
- Secure retrieval methods for dependent skills
- Clear error messages when credentials are missing
- Support for multiple credential sources (config file, environment variables)

## Usage by Other Skills

Skills that need to invoke APIs should reference this skill:

### Anthropic Claude API

```python
import sys
sys.path.append('/home/user/claude-skills/api-credentials/scripts')
from credentials import get_anthropic_api_key

try:
    api_key = get_anthropic_api_key()
    # Use api_key for Claude API calls
except ValueError as e:
    print(f"Error: {e}")
```

### Google Gemini API

```python
import sys
sys.path.append('/home/user/claude-skills/api-credentials/scripts')
from credentials import get_google_api_key

try:
    api_key = get_google_api_key()
    # Use api_key for Gemini API calls
except ValueError as e:
    print(f"Error: {e}")
```

### GitHub API

```python
import sys
sys.path.append('/home/user/claude-skills/api-credentials/scripts')
from credentials import get_github_api_key

try:
    api_key = get_github_api_key()
    # Use api_key for GitHub API calls
except ValueError as e:
    print(f"Error: {e}")
```

## Setup Instructions

### Option 1: Configuration File (Recommended)

1. Copy the example config:
```bash
cp /home/user/claude-skills/api-credentials/assets/config.json.example \
   /home/user/claude-skills/api-credentials/config.json
```

2. Edit `config.json` and add your API keys:
```json
{
  "anthropic_api_key": "sk-ant-api03-...",
  "google_api_key": "AIzaSy...",
  "github_api_key": "ghp_..."
}
```

3. Ensure the config file is in `.gitignore` (already configured)

### Option 2: Environment Variables

Set environment variables for the providers you need:

```bash
# Anthropic Claude
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Google Gemini
export GOOGLE_API_KEY="AIzaSy..."

# GitHub
export GITHUB_TOKEN="ghp_..."
# or
export GITHUB_API_KEY="ghp_..."
```

Add to your shell profile (~/.bashrc, ~/.zshrc) to persist.

## Priority

Credential retrieval follows this priority for each provider:
1. `config.json` in the skill directory (highest priority)
2. Environment variable (ANTHROPIC_API_KEY or GOOGLE_API_KEY)
3. ValueError raised if neither is available

## Security Notes

- **Never commit config.json with real credentials**
- The config.json file should be in .gitignore
- Only config.json.example should be version controlled
- Consider using environment variables in shared/production environments
- Rotate API keys regularly
- Skills should never log or display full API keys

## File Structure

```
api-credentials/
├── SKILL.md              # This file
├── config.json           # YOUR credentials (gitignored)
├── scripts/
│   └── credentials.py    # Credential retrieval module
└── assets/
    └── config.json.example  # Template for users
```

## Error Handling

When credentials are not found, the module raises `ValueError` with clear guidance:
- Where to place config.json
- How to set environment variables
- Links to provider consoles for key generation

Skills should catch `ValueError` exceptions and handle appropriately.

## Available Functions

**get_anthropic_api_key()** → str
- Returns Anthropic API key
- Raises ValueError if not configured

**get_google_api_key()** → str
- Returns Google API key
- Raises ValueError if not configured

**get_github_api_key()** → str
- Returns GitHub API token (Personal Access Token)
- Raises ValueError if not configured

**get_api_key_masked(api_key)** → str
- Returns masked version for safe logging
- Example: "sk-ant-...xyz"

**verify_credential(provider)** → bool
- Checks if provider is configured
- Returns True/False without raising exceptions
- Providers: 'anthropic', 'google', 'github'

## Adding New Providers

To support additional providers:

1. Add field to `assets/config.json.example`
2. Add getter function to `scripts/credentials.py`:
   ```python
   def get_provider_api_key() -> str:
       # Follow existing pattern with config file + env var
       pass
   ```
3. Add to `verify_credential()` mapping
4. Update this documentation

## Token Efficiency

This skill uses ~300 tokens when loaded but saves repeated credential management code across multiple skills that invoke external APIs. It provides a single, consistent pattern for all credential handling.
