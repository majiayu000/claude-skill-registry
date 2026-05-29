---
name: clickup-setup-guide
description: Complete setup and installation guide for the ClickUp Framework CLI with troubleshooting
tags: [clickup, installation, setup, configuration]
---

# ClickUp Framework Setup Guide

Complete guide to installing and configuring the ClickUp Framework CLI.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for installation from repository)
- ClickUp API Token ([Get one here](https://app.clickup.com/settings/apps))

## Installation

### Method 1: Install from GitHub (Recommended)

Install the latest version directly from GitHub:

```bash
pip install --upgrade --force-reinstall git+https://github.com/SOELexicon/clickup_framework.git
```

**Flags explained:**
- `--upgrade`: Upgrade if already installed
- `--force-reinstall`: Force reinstall even if up-to-date
- `git+https://...`: Install from Git repository

### Method 2: Install in Virtual Environment (Recommended for Development)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate     # On Windows

# Install the framework
pip install git+https://github.com/SOELexicon/clickup_framework.git
```

### Method 3: Development Installation

If you're developing the framework itself:

```bash
# Clone the repository
git clone https://github.com/SOELexicon/clickup_framework.git
cd clickup_framework

# Install in editable mode
pip install -e .

# Use the module directly
python -m clickup_framework.cli --help
```

## Configuration

### 1. Get Your ClickUp API Token

1. Go to [ClickUp Settings > Apps](https://app.clickup.com/settings/apps)
2. Click "Generate" under "API Token"
3. Copy your token (it looks like: `pk_12345678_ABCDEFGHIJKLMNOPQRSTUVWXYZ`)

### 2. Set Environment Variable

**Linux/Mac (Temporary - current session only):**
```bash
export CLICKUP_API_TOKEN="pk_your_token_here"
```

**Linux/Mac (Permanent - add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export CLICKUP_API_TOKEN="pk_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
$env:CLICKUP_API_TOKEN="pk_your_token_here"

# Or permanently:
[System.Environment]::SetEnvironmentVariable('CLICKUP_API_TOKEN', 'pk_your_token_here', 'User')
```

### 3. Verify Installation

```bash
# Check if command is available
cum --version
# or
clickup --version

# Test with demo mode (no token required)
cum demo

# Test with your token
cum show
```

### 4. Set Up Context

Set your default workspace and list for easier command usage:

```bash
# Set workspace (find ID in ClickUp URL or use cum demo)
cum set workspace <workspace_id>

# Set default list
cum set list <list_id>

# Set default assignee (your user ID)
cum set assignee <user_id>

# Verify context
cum show
```

## Optional: Enable Tab Completion

### Bash

```bash
# Install argcomplete if not already installed
pip install argcomplete

# Add to ~/.bashrc
echo 'eval "$(register-python-argcomplete cum)"' >> ~/.bashrc
source ~/.bashrc
```

### Zsh

```bash
# Install argcomplete if not already installed
pip install argcomplete

# Add to ~/.zshrc
echo 'eval "$(register-python-argcomplete cum)"' >> ~/.zshrc
source ~/.zshrc
```

## Verification Checklist

Run these commands to verify everything is working:

```bash
# 1. Command is available
which cum
# Should show: /usr/local/bin/cum or similar

# 2. Token is set
echo $CLICKUP_API_TOKEN
# Should show: pk_...

# 3. Can connect to API
cum show
# Should show: Current context (even if empty)

# 4. Can view tasks
cum a
# Should show: Your assigned tasks

# 5. Context is working
cum set workspace <workspace_id>
cum show
# Should show: Current workspace ID
```

## Troubleshooting

### Issue: `command not found: cum`

**Solution 1:** Reinstall the package
```bash
pip install --upgrade --force-reinstall git+https://github.com/SOELexicon/clickup_framework.git
```

**Solution 2:** Use the module directly
```bash
python -m clickup_framework.cli --help
```

**Solution 3:** Check your PATH
```bash
# Find where pip installs executables
pip show clickup_framework | grep Location

# Add to PATH if needed (in ~/.bashrc or ~/.zshrc)
export PATH="$PATH:$HOME/.local/bin"
```

### Issue: `401 Unauthorized` or API errors

**Causes:**
- Token not set
- Token expired or invalid
- Token doesn't have required permissions

**Solution:**
```bash
# Check if token is set
echo $CLICKUP_API_TOKEN

# If empty, set it
export CLICKUP_API_TOKEN="pk_your_token_here"

# Test the token
cum show

# If still failing, regenerate token in ClickUp settings
```

### Issue: Permission denied or pip warnings

**Symptom:**
```
WARNING: The directory '/root/.cache/pip' or its parent directory is not owned...
WARNING: Running pip as the 'root' user...
```

**Solution:** Use a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate
pip install git+https://github.com/SOELexicon/clickup_framework.git
```

### Issue: Python version too old

**Symptom:**
```
ERROR: Package requires Python '>=3.8'
```

**Solution:** Upgrade Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10

# Mac (using Homebrew)
brew install python@3.10

# Verify
python3 --version
```

### Issue: SSL Certificate errors

**Symptom:**
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Solution:**
```bash
# Update certificates (Mac)
/Applications/Python\ 3.x/Install\ Certificates.command

# Or upgrade certifi
pip install --upgrade certifi

# Or temporarily disable (not recommended for production)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org git+https://github.com/SOELexicon/clickup_framework.git
```

### Issue: Commands are slow

**Causes:**
- Network latency
- Large task lists
- Complex hierarchies

**Solutions:**
```bash
# Use minimal preset for faster rendering
cum h current --preset minimal

# Filter to specific status
cum fil current --status "in progress"

# Disable colors if terminal is slow
cum ansi disable

# Use flat view instead of hierarchy
cum f current
```

## Updating

### Update to Latest Version

```bash
pip install --upgrade --force-reinstall git+https://github.com/SOELexicon/clickup_framework.git
```

### Check Current Version

```bash
cum --version
```

### Update in Virtual Environment

```bash
# Activate venv
source venv/bin/activate

# Update
pip install --upgrade --force-reinstall git+https://github.com/SOELexicon/clickup_framework.git
```

## Uninstallation

```bash
# Uninstall the package
pip uninstall clickup_framework

# Remove configuration (optional)
rm ~/.clickup_context.json

# Remove environment variable (remove from ~/.bashrc or ~/.zshrc)
# Then reload shell:
source ~/.bashrc
```

## Docker Installation (Advanced)

Create a Dockerfile for containerized usage:

```dockerfile
FROM python:3.10-slim

# Install ClickUp Framework
RUN pip install --no-cache-dir git+https://github.com/SOELexicon/clickup_framework.git

# Set token via environment
ENV CLICKUP_API_TOKEN=""

# Default command
CMD ["cum", "--help"]
```

Build and run:

```bash
# Build
docker build -t clickup-cli .

# Run (pass token)
docker run -e CLICKUP_API_TOKEN="pk_your_token" clickup-cli cum a
```

## Next Steps

After installation:

1. **Set up context:** Run `cum set workspace <id>` and `cum set list <id>`
2. **View your tasks:** Run `cum a` to see assigned tasks
3. **Learn the workflow:** See the Workflow skill or run `/workflow` in Claude Code
4. **Explore commands:** Run `/cum` for complete CLI reference
5. **Enable tab completion:** Follow the optional steps above

## Getting Help

```bash
# General help
cum --help

# Command-specific help
cum <command> --help

# Demo mode (no token required)
cum demo

# Show current context
cum show
```

## Resources

- **GitHub Repository:** https://github.com/SOELexicon/clickup_framework
- **ClickUp API Docs:** https://clickup.com/api
- **Get API Token:** https://app.clickup.com/settings/apps

---

For command reference: See the CLI Reference skill or run `/cum` in Claude Code.
For workflow guide: See the Workflow skill or run `/workflow` in Claude Code.
