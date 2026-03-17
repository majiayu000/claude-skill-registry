---
name: pyenv-activation
description: Guide for activating pyenv virtual environments with troubleshooting for common issues
---

# Pyenv Activation Skill

This skill should be used when activating pyenv virtual environments or troubleshooting pyenv activation issues.

## Purpose

Activate pyenv virtual environments reliably, with fallbacks when standard activation methods fail.

## Activation Methods

### Method 1: Standard Activation (Preferred)

```bash
pyenv activate <env-name>
```

This requires pyenv-virtualenv to be loaded into the shell.

### Method 2: Shell Re-initialization

If pyenv-virtualenv is not loaded:

```bash
eval "$(pyenv init -)" && eval "$(pyenv virtualenv-init -)" && pyenv activate <env-name>
```

### Method 3: Direct Virtual Environment Activation

When pyenv activation fails or shell integration is not enabled, activate the virtual environment directly using its path:

```bash
source /Users/alexismanuel/.pyenv/versions/<python-version>/envs/<env-name>/bin/activate
```

To find the correct path:
1. Run `pyenv versions` to list available environments
2. Note the Python version and environment name
3. Construct the path: `~/.pyenv/versions/<version>/envs/<env-name>/bin/activate`

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "pyenv-virtualenv has not been loaded" | pyenv-virtualenv plugin not initialized | Use Method 2 |
| "shell integration not enabled" | pyenv shell integration not configured | Use Method 3 |
| Activation appears to work but wrong Python version | Environment not properly activated | Verify with `python --version` and `which python` |

## Verification

After activation, always verify the environment is active:

```bash
python --version
which python
```

Expected output should show the Python version from the pyenv environment and a path under `~/.pyenv/versions/`.
