---
name: mcp-check
description: Validate MCP configuration and suggest improvements
user-invocable: true
---

# MCP Configuration Validator

Validate the project's MCP setup for correctness and completeness.

---

## Validation Steps

### 1. Check Configuration Files
- `.claude/settings.json` (project)
- `~/.claude.json` (user, reference)

### 2. Validate Structure
- [ ] Valid JSON format
- [ ] `mcpServers` object exists
- [ ] `enableAllProjectMcpServers: true` is set

### 3. Validate Each MCP
- [ ] `command` is valid
- [ ] `args` properly formatted
- [ ] `env` variables set

### 4. Check Essential MCPs
| MCP | Required? |
|-----|-----------|
| memory | Recommended |
| filesystem | Optional |
| github | If .git exists |

### 5. Security Check
- [ ] No hardcoded secrets
- [ ] Sensitive values use env vars

---

## Output Format

```markdown
## MCP Configuration Report

### Status: VALID / ISSUES / INVALID

### Configuration Summary
| MCP Server | Status | Notes |
|------------|--------|-------|
| memory | OK/FAIL | details |

### Issues Found
1. [Issue and fix]

### Missing Recommended MCPs
- memory: `claude mcp add --scope project memory...`
```

---

## Common Issues

| Issue | Fix |
|-------|-----|
| Invalid JSON | Check trailing commas |
| MCP not loading | `claude mcp reset-project-choices` |
| Missing env vars | Add with `-e KEY=value` |
