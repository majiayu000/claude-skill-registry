---
name: nav-install-multi-claude
description: Install Navigator multi-Claude workflow orchestration scripts. Auto-invokes when user says "install multi-Claude workflows", "set up multi-Claude", or "enable parallel execution".
allowed-tools: Bash, Read, Write
version: 1.0.0
---

# Navigator Multi-Claude Workflow Installer

Install multi-Claude orchestration scripts for parallel AI execution.

## When to Invoke

Auto-invoke when user says:
- "Install multi-Claude workflows"
- "Set up multi-Claude orchestration"
- "Enable parallel execution"
- "Complete Navigator 4.3.0 installation"
- "Install Navigator workflows"

**DO NOT invoke** if:
- Scripts already installed (check with `which navigator-multi-claude.sh`)
- User is just asking about multi-Claude (informational)
- Navigator plugin not installed

## What This Installs

**Scripts installed to `$HOME/bin/`**:
- `navigator-multi-claude.sh` - Full 6-phase workflow orchestration
- `navigator-multi-claude-poc.sh` - Simple 3-phase POC
- `install-multi-claude.sh` - This installer (for future updates)

**Why needed**: Plugin installation only copies skills/templates. Multi-Claude scripts live outside plugin structure and require separate installation.

## Execution Steps

### Step 1: Check if Already Installed

```bash
if command -v navigator-multi-claude.sh &> /dev/null; then
  INSTALLED_PATH=$(which navigator-multi-claude.sh)
  INSTALLED_VERSION=$(grep -o 'VERSION=.*' "$INSTALLED_PATH" | head -1 | cut -d'=' -f2 | tr -d '"' || echo "unknown")

  echo "✅ Multi-Claude workflows already installed"
  echo ""
  echo "Location: $INSTALLED_PATH"
  echo "Version: $INSTALLED_VERSION"
  echo ""
  echo "To reinstall/update:"
  echo "  rm $INSTALLED_PATH"
  echo "  'Install multi-Claude workflows'"

  exit 0
fi
```

### Step 2: Verify Prerequisites

```bash
# Check Claude CLI
if ! command -v claude &> /dev/null; then
  echo "❌ Claude Code CLI not found in PATH"
  echo ""
  echo "Multi-Claude workflows require Claude Code CLI to spawn sub-Claude instances."
  echo ""
  echo "Install Claude Code first, then retry:"
  echo "  https://docs.claude.com/claude-code/installation"
  exit 1
fi

# Check Navigator plugin installed
PLUGIN_PATHS=(
  "$HOME/.claude/plugins/marketplaces/navigator-marketplace"
  "$HOME/.config/claude/plugins/navigator"
  "$HOME/.claude/plugins/navigator"
)

PLUGIN_FOUND=false
for path in "${PLUGIN_PATHS[@]}"; do
  if [ -d "$path" ]; then
    PLUGIN_FOUND=true
    PLUGIN_PATH="$path"
    break
  fi
done

if [ "$PLUGIN_FOUND" = false ]; then
  echo "❌ Navigator plugin not found"
  echo ""
  echo "Install Navigator plugin first:"
  echo "  /plugin marketplace add alekspetrov/navigator"
  echo "  /plugin install navigator"
  exit 1
fi

echo "✅ Prerequisites verified"
echo "   - Claude CLI: $(which claude)"
echo "   - Navigator plugin: $PLUGIN_PATH"
echo ""
```

### Step 3: Download Latest Scripts from GitHub

```bash
echo "📥 Downloading multi-Claude scripts from GitHub..."
echo ""

# Detect installed plugin version
if [ -f "$PLUGIN_PATH/.claude-plugin/plugin.json" ]; then
  PLUGIN_VERSION=$(grep -o '"version": "[^"]*"' "$PLUGIN_PATH/.claude-plugin/plugin.json" | head -1 | cut -d'"' -f4)
  VERSION_TAG="v$PLUGIN_VERSION"
  echo "   Plugin version: $PLUGIN_VERSION"
  echo "   Fetching matching scripts: $VERSION_TAG"
else
  # Fallback to latest stable if version detection fails
  VERSION_TAG="main"
  echo "   ⚠️  Could not detect plugin version"
  echo "   Fetching from: main branch (latest stable)"
fi

echo ""

# Clone repository to temp location
TEMP_DIR="/tmp/navigator-install-$$"
if git clone --depth 1 --branch "$VERSION_TAG" https://github.com/alekspetrov/navigator.git "$TEMP_DIR" 2>&1; then
  echo "✅ Downloaded Navigator repository"
else
  echo "❌ Failed to download from GitHub"
  echo ""
  echo "Possible causes:"
  echo "  - No internet connection"
  echo "  - Version tag $VERSION_TAG doesn't exist"
  echo "  - GitHub rate limit exceeded"
  echo ""
  echo "Retry with main branch? [y/N]"
  exit 1
fi

echo ""
```

### Step 4: Run Installation Script

```bash
echo "📦 Installing multi-Claude scripts..."
echo ""

cd "$TEMP_DIR"

if [ -f "scripts/install-multi-claude.sh" ]; then
  # Run the installer
  chmod +x scripts/install-multi-claude.sh
  ./scripts/install-multi-claude.sh

  INSTALL_EXIT=$?

  if [ $INSTALL_EXIT -eq 0 ]; then
    echo ""
    echo "✅ Multi-Claude workflows installed successfully"
  else
    echo ""
    echo "❌ Installation failed with exit code $INSTALL_EXIT"
    echo ""
    echo "Check the output above for errors."
    exit 1
  fi
else
  echo "❌ install-multi-claude.sh not found in repository"
  echo ""
  echo "This version may not support multi-Claude workflows."
  echo "Upgrade to Navigator v4.3.0+ for multi-Claude features."
  exit 1
fi

echo ""
```

### Step 5: Verify Installation

```bash
echo "🔍 Verifying installation..."
echo ""

# Check if scripts are in PATH
if command -v navigator-multi-claude.sh &> /dev/null; then
  INSTALLED_PATH=$(which navigator-multi-claude.sh)
  echo "✅ navigator-multi-claude.sh: $INSTALLED_PATH"
else
  echo "⚠️  navigator-multi-claude.sh not in PATH"
  echo "   May need to restart terminal or run:"
  echo "   export PATH=\"\$HOME/bin:\$PATH\""
fi

if command -v navigator-multi-claude-poc.sh &> /dev/null; then
  INSTALLED_PATH=$(which navigator-multi-claude-poc.sh)
  echo "✅ navigator-multi-claude-poc.sh: $INSTALLED_PATH"
else
  echo "⚠️  navigator-multi-claude-poc.sh not in PATH"
fi

echo ""
```

### Step 6: Cleanup and Next Steps

```bash
# Cleanup temp directory
rm -rf "$TEMP_DIR"
echo "🧹 Cleaned up temporary files"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Multi-Claude Workflows Ready"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Test with simple task:"
echo "  navigator-multi-claude-poc.sh \"Add hello world function\""
echo ""
echo "Full 6-phase workflow:"
echo "  navigator-multi-claude.sh \"Implement user authentication\""
echo ""
echo "Documentation:"
echo "  - Release notes: RELEASE-NOTES-v4.3.0.md"
echo "  - POC learnings: scripts/POC-LEARNINGS.md"
echo ""
echo "Status: Experimental (30% success rate)"
echo "Recommendation: Use for simple features, monitor output closely"
echo ""
```

## Error Handling

### Git Clone Fails

```
❌ Failed to download from GitHub

Possible causes:
  - No internet connection
  - Version tag v4.3.1 doesn't exist
  - GitHub rate limit exceeded

Manual installation:
  1. Download: https://github.com/alekspetrov/navigator/archive/refs/heads/main.zip
  2. Extract and cd to directory
  3. Run: ./scripts/install-multi-claude.sh
```

### Version Mismatch

```
⚠️  Plugin version: 4.3.1
    Latest release: 4.3.0
    Installing from: main branch

This may include unreleased changes.
Continue? [y/N]
```

### Already Installed

```
✅ Multi-Claude workflows already installed

Location: /Users/username/bin/navigator-multi-claude.sh
Version: 4.3.0

To reinstall/update:
  rm /Users/username/bin/navigator-multi-claude.sh
  'Install multi-Claude workflows'
```

### Permission Denied

```
❌ Permission denied: /usr/local/bin/

Installation requires write access to:
  - $HOME/bin/ (recommended)
  - /usr/local/bin/ (requires sudo)

Fix:
  mkdir -p $HOME/bin
  export PATH="$HOME/bin:$PATH"

Then retry: 'Install multi-Claude workflows'
```

## Success Criteria

Installation successful when:
- [ ] Scripts downloaded from GitHub
- [ ] install-multi-claude.sh executed without errors
- [ ] Scripts added to PATH (verified with `which`)
- [ ] Version matches plugin version (or explicit override)
- [ ] User can invoke `navigator-multi-claude-poc.sh --help`

## Rollback Procedure

If installation fails or causes issues:

```bash
# Remove installed scripts
rm -f $HOME/bin/navigator-multi-claude.sh
rm -f $HOME/bin/navigator-multi-claude-poc.sh
rm -f $HOME/bin/install-multi-claude.sh

# Verify removal
which navigator-multi-claude.sh
# Should output: navigator-multi-claude.sh not found
```

## Notes

**Why separate installation**:
- Plugin system only copies skills/templates from `.claude-plugin/`
- Multi-Claude scripts are executable Bash files that need to be in PATH
- Installation location varies by system ($HOME/bin vs /usr/local/bin)
- Scripts need `chmod +x` for execution

**Version matching**:
- Always fetches scripts matching installed plugin version
- Prevents version drift (v4.3.1 plugin with v4.3.0 scripts)
- Falls back to main branch if version tag doesn't exist

**What gets installed**:
```
$HOME/bin/
├── navigator-multi-claude.sh         # Full 6-phase workflow
├── navigator-multi-claude-poc.sh     # 3-phase POC
└── install-multi-claude.sh           # Reinstaller
```

## Related Skills

- **nav-start**: Detects missing workflows and prompts installation
- **nav-upgrade**: Updates plugin (workflows need separate reinstall)
- **nav-stats**: Shows multi-Claude workflow efficiency metrics

## Examples

### Example 1: Fresh Installation

User: "Install multi-Claude workflows"

Assistant executes:
1. Checks prerequisites (Claude CLI, Navigator plugin)
2. Downloads from GitHub (v4.3.1 tag)
3. Runs install-multi-claude.sh
4. Verifies installation
5. Shows test commands

Output:
```
✅ Multi-Claude Workflows Ready

Test with simple task:
  navigator-multi-claude-poc.sh "Add hello world function"
```

### Example 2: Already Installed

User: "Set up multi-Claude"

Assistant checks:
```bash
which navigator-multi-claude.sh
# Found at: /Users/alex/bin/navigator-multi-claude.sh
```

Output:
```
✅ Multi-Claude workflows already installed

Location: /Users/alex/bin/navigator-multi-claude.sh
Version: 4.3.0

Already ready to use!
```

### Example 3: After Plugin Update

User updates plugin 4.3.0 → 4.3.1, then:
"Install multi-Claude workflows"