---
name: doctor
description: Diagnose and fix oh-my-gemini installation issues
---

# Doctor Skill

## Task: Run Installation Diagnostics

You are the OMC Doctor - diagnose and fix installation issues.

### Step 1: Check Plugin Version

```bash
# Get installed version
INSTALLED=$(ls ~/.gemini-cli/plugins/cache/omc/oh-my-gemini/ 2>/dev/null | sort -V | tail -1)
echo "Installed: $INSTALLED"

# Get latest from npm
LATEST=$(npm view oh-my-claude-sisyphus version 2>/dev/null)
echo "Latest: $LATEST"
```

**Diagnosis**:
- If no version installed: CRITICAL - plugin not installed
- If INSTALLED != LATEST: WARN - outdated plugin
- If multiple versions exist: WARN - stale cache

### Step 2: Check for Legacy Hooks in settings.json

Read `~/.gemini-cli/settings.json` and check if there's a `"hooks"` key with entries like:
- `bash $HOME/.gemini-cli/hooks/keyword-detector.sh`
- `bash $HOME/.gemini-cli/hooks/persistent-mode.sh`
- `bash $HOME/.gemini-cli/hooks/session-start.sh`

**Diagnosis**:
- If found: CRITICAL - legacy hooks causing duplicates

### Step 3: Check for Legacy Bash Hook Scripts

```bash
ls -la ~/.gemini-cli/hooks/*.sh 2>/dev/null
```

**Diagnosis**:
- If `keyword-detector.sh`, `persistent-mode.sh`, `session-start.sh`, or `stop-continuation.sh` exist: WARN - legacy scripts (can cause confusion)

### Step 4: Check GEMINI.md

```bash
# Check if GEMINI.md exists
ls -la ~/.gemini-cli/GEMINI.md 2>/dev/null

# Check for OMC marker
grep -q "oh-my-gemini Multi-Agent System" ~/.gemini-cli/GEMINI.md 2>/dev/null && echo "Has OMC config" || echo "Missing OMC config"
```

**Diagnosis**:
- If missing: CRITICAL - GEMINI.md not configured
- If missing OMC marker: WARN - outdated GEMINI.md

### Step 5: Check for Stale Plugin Cache

```bash
# Count versions in cache
ls ~/.gemini-cli/plugins/cache/omc/oh-my-gemini/ 2>/dev/null | wc -l
```

**Diagnosis**:
- If > 1 version: WARN - multiple cached versions (cleanup recommended)

### Step 6: Check for Legacy Curl-Installed Content

Check for legacy agents, commands, and skills installed via curl (before plugin system):

```bash
# Check for legacy agents directory
ls -la ~/.gemini-cli/agents/ 2>/dev/null

# Check for legacy commands directory
ls -la ~/.gemini-cli/commands/ 2>/dev/null

# Check for legacy skills directory
ls -la ~/.gemini-cli/skills/ 2>/dev/null
```

**Diagnosis**:
- If `~/.gemini-cli/agents/` exists with oh-my-gemini-related files: WARN - legacy agents (now provided by plugin)
- If `~/.gemini-cli/commands/` exists with oh-my-gemini-related files: WARN - legacy commands (now provided by plugin)
- If `~/.gemini-cli/skills/` exists with oh-my-gemini-related files: WARN - legacy skills (now provided by plugin)

Look for files like:
- `architect.md`, `researcher.md`, `explore.md`, `executor.md`, etc. in agents/
- `ultrawork.md`, `deepsearch.md`, etc. in commands/
- Any oh-my-gemini-related `.md` files in skills/

---

## Report Format

After running all checks, output a report:

```
## OMC Doctor Report

### Summary
[HEALTHY / ISSUES FOUND]

### Checks

| Check | Status | Details |
|-------|--------|---------|
| Plugin Version | OK/WARN/CRITICAL | ... |
| Legacy Hooks (settings.json) | OK/CRITICAL | ... |
| Legacy Scripts (~/.gemini-cli/hooks/) | OK/WARN | ... |
| GEMINI.md | OK/WARN/CRITICAL | ... |
| Plugin Cache | OK/WARN | ... |
| Legacy Agents (~/.gemini-cli/agents/) | OK/WARN | ... |
| Legacy Commands (~/.gemini-cli/commands/) | OK/WARN | ... |
| Legacy Skills (~/.gemini-cli/skills/) | OK/WARN | ... |

### Issues Found
1. [Issue description]
2. [Issue description]

### Recommended Fixes
[List fixes based on issues]
```

---

## Auto-Fix (if user confirms)

If issues found, ask user: "Would you like me to fix these issues automatically?"

If yes, apply fixes:

### Fix: Legacy Hooks in settings.json
Remove the `"hooks"` section from `~/.gemini-cli/settings.json` (keep other settings intact)

### Fix: Legacy Bash Scripts
```bash
rm -f ~/.gemini-cli/hooks/keyword-detector.sh
rm -f ~/.gemini-cli/hooks/persistent-mode.sh
rm -f ~/.gemini-cli/hooks/session-start.sh
rm -f ~/.gemini-cli/hooks/stop-continuation.sh
```

### Fix: Outdated Plugin
```bash
rm -rf ~/.gemini-cli/plugins/cache/oh-my-gemini
echo "Plugin cache cleared. Restart Gemini CLI to fetch latest version."
```

### Fix: Stale Cache (multiple versions)
```bash
# Keep only latest version
cd ~/.gemini-cli/plugins/cache/omc/oh-my-gemini/
ls | sort -V | head -n -1 | xargs rm -rf
```

### Fix: Missing/Outdated GEMINI.md
Fetch latest from GitHub and write to `~/.gemini-cli/GEMINI.md`:
```
WebFetch(url: "https://raw.githubusercontent.com/Yeachan-Heo/oh-my-gemini/main/docs/GEMINI.md", prompt: "Return the complete raw markdown content exactly as-is")
```

### Fix: Legacy Curl-Installed Content

Remove legacy agents, commands, and skills directories (now provided by plugin):

```bash
# Backup first (optional - ask user)
# mv ~/.gemini-cli/agents ~/.gemini-cli/agents.bak
# mv ~/.gemini-cli/commands ~/.gemini-cli/commands.bak
# mv ~/.gemini-cli/skills ~/.gemini-cli/skills.bak

# Or remove directly
rm -rf ~/.gemini-cli/agents
rm -rf ~/.gemini-cli/commands
rm -rf ~/.gemini-cli/skills
```

**Note**: Only remove if these contain oh-my-gemini-related files. If user has custom agents/commands/skills, warn them and ask before removing.

---

## Post-Fix

After applying fixes, inform user:
> Fixes applied. **Restart Gemini CLI** for changes to take effect.
