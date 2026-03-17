---
name: plugin-checker
description: >-
  Use this skill when asked to "validate plugin", "check plugin structure",
  "verify plugin", "audit plugin", "is my plugin correct", "plugin issues",
  or when troubleshooting plugin problems.
---

# Plugin Checker Skill

This skill provides comprehensive validation guidelines for Claude Code plugins, helping identify structural issues, misconfigurations, and best practice violations.

## Validation Checklist

### 1. Plugin Manifest Validation

Check `.claude-plugin/plugin.json`:

**Required:**
- [ ] File exists at `.claude-plugin/plugin.json`
- [ ] Valid JSON syntax
- [ ] `name` field present and valid

**Name validation:**
- [ ] Uses kebab-case (lowercase letters, numbers, hyphens)
- [ ] Length between 3-50 characters
- [ ] No spaces or special characters
- [ ] Starts with a letter

**Optional fields (if present):**
- [ ] `version` follows semver (X.Y.Z)
- [ ] `description` is a non-empty string
- [ ] `author` has `name` field (string)
- [ ] `author.email` is valid email format (if present)

### 2. Directory Structure Validation

**Required structure:**
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json    ← REQUIRED
```

**Valid optional directories:**
- [ ] `agents/` - Contains `.md` files only
- [ ] `skills/` - Contains subdirectories with `SKILL.md`
- [ ] `commands/` - Contains `.md` files only
- [ ] `hooks/` - Contains `hooks.json`
- [ ] `scripts/` - Contains executable scripts

**Invalid patterns to flag:**
- ❌ `AGENTS.md` at root (should be `agents/*.md`)
- ❌ `SKILL.md` at root (should be `skills/*/SKILL.md`)
- ❌ Nested `.claude-plugin/` directories
- ❌ Files directly in `skills/` (should be in subdirs)

### 3. Agent File Validation

For each file in `agents/*.md`:

**Frontmatter checks:**
- [ ] File starts with `---`
- [ ] Valid YAML frontmatter
- [ ] `name` field present
- [ ] `description` field present

**Name field:**
- [ ] Lowercase letters, numbers, hyphens only
- [ ] 3-50 characters
- [ ] Matches filename (recommended)

**Description field:**
- [ ] Contains trigger conditions
- [ ] Has at least one `<example>` block (recommended)
- [ ] Example has `user:`, `assistant:`, `<commentary>`

**Model field (if present):**
- [ ] Valid value: `inherit`, `sonnet`, `opus`, `haiku`

**Color field (if present):**
- [ ] Valid value: `blue`, `cyan`, `green`, `yellow`, `magenta`, `red`

**Tools field (if present):**
- [ ] Is an array
- [ ] Contains valid tool names

**Content check:**
- [ ] Has system prompt after frontmatter
- [ ] System prompt is substantial (>20 chars)

### 4. Skill Directory Validation

For each directory in `skills/*/`:

**Structure:**
- [ ] Contains `SKILL.md` file
- [ ] `SKILL.md` has YAML frontmatter

**Frontmatter:**
- [ ] `name` field present
- [ ] `description` field present with trigger phrases

**Optional subdirectories:**
- [ ] `references/` - Additional documentation
- [ ] `examples/` - Working examples
- [ ] `scripts/` - Utility scripts

### 5. Command File Validation

For each file in `commands/*.md`:

**Frontmatter:**
- [ ] `description` field present
- [ ] `argument-hint` is string (if present)
- [ ] `allowed-tools` is array (if present)

**Naming:**
- [ ] Filename is kebab-case
- [ ] No spaces or special characters

### 6. Hooks Validation

For `hooks/hooks.json`:

**JSON structure:**
- [ ] Valid JSON syntax
- [ ] Has `hooks` object at root (or in `description` + `hooks`)

**Event names (if present):**
- [ ] `PreToolUse`
- [ ] `PostToolUse`
- [ ] `Stop`
- [ ] `SubagentStop`
- [ ] `SessionStart`
- [ ] `SessionEnd`
- [ ] `UserPromptSubmit`
- [ ] `PreCompact`
- [ ] `Notification`
- [ ] `PermissionRequest`

**Hook entries:**
- [ ] `matcher` field present (for tool events)
- [ ] `hooks` array present
- [ ] Each hook has `type` ("command" or "prompt")
- [ ] Command hooks have `command` field
- [ ] Prompt hooks have `prompt` field

**Path portability:**
- [ ] Uses `${CLAUDE_PLUGIN_ROOT}` for plugin paths
- [ ] No hardcoded absolute paths

**Script references:**
- [ ] Referenced scripts exist
- [ ] Scripts are executable (have shebang)

### 7. Security Checks

**Credentials:**
- [ ] No hardcoded API keys or tokens
- [ ] No passwords in configuration
- [ ] Environment variables used for secrets

**URLs:**
- [ ] MCP servers use HTTPS/WSS (not HTTP/WS)

**Scripts:**
- [ ] No obvious command injection vulnerabilities
- [ ] Input validation present
- [ ] Variables properly quoted

## Common Issues and Fixes

### Issue: "plugin not found"
**Cause:** Missing or invalid plugin.json
**Fix:** Create `.claude-plugin/plugin.json` with valid JSON and `name` field

### Issue: "agents not loading"
**Cause:** Agents not in correct location
**Fix:** Move to `agents/` directory with `.md` extension

### Issue: "skill not triggering"
**Cause:** Weak trigger description or wrong structure
**Fix:**
- Ensure `skills/{name}/SKILL.md` structure
- Add specific trigger phrases to description

### Issue: "hooks not running"
**Cause:** Invalid hooks.json or script permissions
**Fix:**
- Validate JSON syntax
- Make scripts executable: `chmod +x scripts/*.sh`
- Use `${CLAUDE_PLUGIN_ROOT}` in paths

### Issue: "command not appearing"
**Cause:** Missing frontmatter or wrong location
**Fix:** Ensure `commands/*.md` with `description` in frontmatter

## Validation Commands

Quick structure check:
```bash
# Check plugin.json exists and is valid
jq . my-plugin/.claude-plugin/plugin.json

# List all components
find my-plugin -name "*.md" -o -name "*.json" | head -20

# Check hooks.json
jq . my-plugin/hooks/hooks.json 2>/dev/null || echo "No hooks.json"
```

Test plugin locally:
```bash
claude --plugin-dir /path/to/my-plugin
```

Debug mode:
```bash
claude --debug --plugin-dir /path/to/my-plugin
```

## Validation Report Format

When reporting validation results:

```
## Plugin Validation Report

### Plugin: [name]
Location: [path]

### Summary
[PASS/FAIL] - [brief assessment]

### Critical Issues (must fix)
- [ ] `path/to/file` - [issue] - [fix]

### Warnings (should fix)
- [ ] `path/to/file` - [issue] - [recommendation]

### Components Found
- Agents: [count] files
- Skills: [count] directories
- Commands: [count] files
- Hooks: [present/not present]

### Positive Findings
- [What's done correctly]

### Recommendations
1. [Priority fix]
2. [Improvement suggestion]
```

## Quick Validation Script

```bash
#!/bin/bash
# validate-plugin.sh <plugin-dir>

PLUGIN_DIR="${1:-.}"

echo "=== Plugin Validation ==="

# Check plugin.json
if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
  echo "✓ plugin.json exists"
  NAME=$(jq -r '.name' "$PLUGIN_DIR/.claude-plugin/plugin.json" 2>/dev/null)
  if [ -n "$NAME" ] && [ "$NAME" != "null" ]; then
    echo "✓ name: $NAME"
  else
    echo "✗ ERROR: name field missing or invalid"
  fi
else
  echo "✗ CRITICAL: .claude-plugin/plugin.json not found"
fi

# Check agents
if [ -d "$PLUGIN_DIR/agents" ]; then
  AGENT_COUNT=$(find "$PLUGIN_DIR/agents" -name "*.md" | wc -l)
  echo "✓ agents/: $AGENT_COUNT files"
fi

# Check skills
if [ -d "$PLUGIN_DIR/skills" ]; then
  SKILL_COUNT=$(find "$PLUGIN_DIR/skills" -name "SKILL.md" | wc -l)
  echo "✓ skills/: $SKILL_COUNT SKILL.md files"
fi

# Check commands
if [ -d "$PLUGIN_DIR/commands" ]; then
  CMD_COUNT=$(find "$PLUGIN_DIR/commands" -name "*.md" | wc -l)
  echo "✓ commands/: $CMD_COUNT files"
fi

# Check hooks
if [ -f "$PLUGIN_DIR/hooks/hooks.json" ]; then
  if jq empty "$PLUGIN_DIR/hooks/hooks.json" 2>/dev/null; then
    echo "✓ hooks/hooks.json: valid JSON"
  else
    echo "✗ hooks/hooks.json: invalid JSON"
  fi
fi

echo "=== Validation Complete ==="
```

## References

- Plugin structure: https://code.claude.com/docs/en/plugins-reference
- Hooks reference: https://code.claude.com/docs/en/hooks
- Official examples: https://github.com/anthropics/claude-code/tree/main/plugins
