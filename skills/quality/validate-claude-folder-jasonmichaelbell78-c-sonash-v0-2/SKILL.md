---
name: validate-claude-folder
description: Validate .claude folder configuration consistency
---

# Validate Claude Folder

Check the `.claude` folder for configuration consistency, documentation drift,
and missing components.

## When to Use

- After modifying `.claude` folder contents
- During periodic maintenance
- When MCP servers or hooks aren't working as expected
- Before major releases

## Validation Checks

Run these checks and report findings:

### 1. MCP Server Consistency

```bash
# Check .mcp.json exists and is valid JSON
cat .mcp.json | jq . > /dev/null && echo "✅ .mcp.json valid" || echo "❌ .mcp.json invalid"

# List configured servers
cat .mcp.json | jq -r '.mcpServers | keys[]'
```

Compare against COMMAND_REFERENCE.md MCP section - flag any mismatches.

### 2. Hook File Consistency

```bash
# Check all hooks referenced in settings.json exist
for hook in session-start check-mcp-servers check-write-requirements check-edit-requirements pattern-check analyze-user-request; do
  if [ -f ".claude/hooks/${hook}.js" ]; then
    echo "✅ ${hook}.js exists"
  else
    echo "❌ ${hook}.js missing"
  fi
done
```

### 3. Skill/Command Alignment

```bash
# List skills
ls -1 .claude/skills/ | grep -v README

# List commands
ls -1 .claude/commands/*.md | xargs -I {} basename {} .md
```

Verify each command has a corresponding skill.

### 4. Documentation Freshness

Check these files for staleness:

- `.claude/COMMAND_REFERENCE.md` - Version and date
- `.claude/HOOKS.md` - Last Updated date
- `DEVELOPMENT.md` - MCP section accuracy

### 5. Secrets Configuration

```bash
# Check if encrypted secrets exist
[ -f ".env.local.encrypted" ] && echo "✅ Encrypted secrets found" || echo "ℹ️ No encrypted secrets"

# Check if .env.local has tokens (without exposing them)
if [ -f ".env.local" ]; then
  grep -qE "^(GITHUB_TOKEN|SONAR_TOKEN)=.+" .env.local && echo "✅ Tokens configured" || echo "⚠️ Tokens not set"
else
  echo "ℹ️ No .env.local (run decrypt-secrets if needed)"
fi
```

### 6. Agent File Validation

```bash
# Check all agent files have valid frontmatter
for f in .claude/agents/*.md; do
  if head -1 "$f" | grep -q "^---"; then
    echo "✅ $(basename $f) has frontmatter"
  else
    echo "❌ $(basename $f) missing frontmatter"
  fi
done
```

## Output Format

Provide a summary table:

| Check      | Status | Notes   |
| ---------- | ------ | ------- |
| MCP Config | ✅/❌  | Details |
| Hooks      | ✅/❌  | Details |
| Skills     | ✅/❌  | Details |
| Docs       | ✅/❌  | Details |
| Secrets    | ✅/❌  | Details |
| Agents     | ✅/❌  | Details |

## Recommendations

After running checks, provide:

1. List of issues found
2. Specific fix commands or edits needed
3. Files that need updating

## Related

- [COMMAND_REFERENCE.md](../../COMMAND_REFERENCE.md)
- [HOOKS.md](../../HOOKS.md)
- [settings.json](../../settings.json)
