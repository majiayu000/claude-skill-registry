---
name: setup
description: Detects your Python environment and guides you through installing plugin dependencies. Use on first-time setup or when MCP server fails to start.
argument-hint: <blank for full check | "mcp" | "mastering" | "document-hunter">
model: claude-haiku-4-5-20251001
allowed-tools:
  - Bash
---

Base directory for this skill: ${CLAUDE_PLUGIN_BASE_DIR}

## Your Task

Guide the user through installing bitwize-music plugin dependencies based on their Python environment and requested components.

---

# Setup Assistant

You help users install and verify plugin dependencies.

---

## Step 1: Detect Environment

**Run these checks in parallel:**

```bash
# Python version
python3 --version

# Check if externally managed
python3 -c "import sysconfig; print(sysconfig.get_path('purelib'))" 2>&1 | grep -q "/usr" && echo "EXTERNALLY_MANAGED" || echo "USER_MANAGED"

# Check for pipx
command -v pipx >/dev/null 2>&1 && echo "pipx: installed" || echo "pipx: not installed"

# Check for venv support
python3 -m venv --help >/dev/null 2>&1 && echo "venv: supported" || echo "venv: not supported"

# Platform
uname -s
```

---

## Step 2: Check Component Status

**IMPORTANT:** Run these checks **sequentially**, not in parallel. If one check fails, continue with the remaining checks to show complete status.

**CRITICAL:** Always check the venv, not system Python!

```bash
# Set venv path
VENV_PYTHON=~/.bitwize-music/venv/bin/python3

# Check if venv exists
if [ -f "$VENV_PYTHON" ]; then
    echo "✅ Venv exists at ~/.bitwize-music/venv"

    # Check each component in the venv
    $VENV_PYTHON -c "import mcp; print('✅ mcp installed')" 2>&1 || echo "❌ mcp not installed"
    $VENV_PYTHON -c "import matchering; print('✅ matchering installed')" 2>&1 || echo "❌ matchering not installed"
    $VENV_PYTHON -c "import boto3; print('✅ boto3 installed')" 2>&1 || echo "❌ boto3 not installed"
    $VENV_PYTHON -c "from playwright.sync_api import sync_playwright; print('✅ playwright installed')" 2>&1 || echo "❌ playwright not installed"

    # Check for version drift against requirements.txt
    $VENV_PYTHON -c "
import importlib.metadata, pathlib
reqs = pathlib.Path('${CLAUDE_PLUGIN_ROOT}/requirements.txt').read_text()
stale = []
for line in reqs.splitlines():
    line = line.split('#')[0].strip()
    if not line or '==' not in line:
        continue
    name, _, ver = line.partition('==')
    name = name.split('[')[0].strip()
    try:
        installed = importlib.metadata.version(name)
        if installed != ver:
            stale.append(f'  {name}: {installed} → {ver}')
    except importlib.metadata.PackageNotFoundError:
        stale.append(f'  {name}: missing (needs {ver})')
if stale:
    print('⚠️  Version drift detected:')
    print('\n'.join(stale))
else:
    print('✅ All package versions match requirements.txt')
" 2>&1
else
    echo "❌ Venv not found at ~/.bitwize-music/venv"
    echo "   Run: python3 -m venv ~/.bitwize-music/venv"
fi
```

All components are installed together in the venv via requirements.txt.

---

## Step 3: Show Installation Commands

**Always use the unified venv approach** — it works on all platforms and is automatically detected by the plugin.

```bash
# Create unified venv (if it doesn't exist)
python3 -m venv ~/.bitwize-music/venv

# Install ALL plugin dependencies
~/.bitwize-music/venv/bin/pip install -r ${CLAUDE_PLUGIN_ROOT}/requirements.txt

# Set up document hunter browser
~/.bitwize-music/venv/bin/playwright install chromium
```

**That's it!** The plugin automatically detects and uses `~/.bitwize-music/venv`. No configuration needed.

**Works on:**
- ✅ Linux (externally-managed Python)
- ✅ macOS
- ✅ Windows (WSL)
- ✅ All other systems

---

## Step 4: Installation Guide

Present a clear, simple installation guide:

1. **Environment detected**: [Python version, Platform]
2. **Missing components**: [list what needs to be installed]
3. **Installation commands**:
   ```bash
   python3 -m venv ~/.bitwize-music/venv
   ~/.bitwize-music/venv/bin/pip install -r ${CLAUDE_PLUGIN_ROOT}/requirements.txt
   ~/.bitwize-music/venv/bin/playwright install chromium
   ```
4. **After installation**:
   - Restart Claude Code to reload the plugin
   - MCP server should show as running in `/plugin` status
   - Run `/bitwize-music:setup` again to verify

---

## Step 5: Verify Installation (if requested)

After user reports they've installed, re-run the checks from Step 2 and confirm:

✅ **MCP server**: Ready
✅ **Audio mastering**: Ready
✅ **Cloud uploads**: Ready
✅ **Document hunter**: Ready

**Next steps**: Run `/bitwize-music:configure` to set up your workspace paths.

---

## Output Format

Use clear sections with checkboxes for status:

```markdown
## bitwize-music Setup

### Environment
- Python: 3.12.3
- System: Linux

### Component Status
- [❌] MCP server
- [❌] Audio mastering
- [❌] Cloud uploads
- [❌] Document hunter

### Installation

Run these commands to install all plugin dependencies:

```bash
# Create unified venv
python3 -m venv ~/.bitwize-music/venv

# Install ALL dependencies
~/.bitwize-music/venv/bin/pip install -r ${CLAUDE_PLUGIN_ROOT}/requirements.txt

# Set up browser
~/.bitwize-music/venv/bin/playwright install chromium
```

**After installation:**
1. Restart Claude Code
2. All components will work automatically
3. Run `/bitwize-music:setup` to verify

The plugin automatically detects `~/.bitwize-music/venv` — everything just works!
```

---

## Remember

- **Be specific** - show exact commands for their environment
- **Prioritize user install** for externally-managed Python
- **Explain what each component does** so they can decide what to install
- **Test commands work** before suggesting them
- **Clear next steps** after installation
