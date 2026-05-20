---
name: agent-validate-config
description: "Validate agent YAML frontmatter and configuration. Use before committing agent changes or in CI."
mcp_fallback: none
category: agent
user-invocable: false
---

# Agent Configuration Validation

Verify agent configurations meet ML Odyssey requirements.

## When to Use

- Creating or modifying agent configurations
- Before committing agent config changes
- CI/CD validation before merge
- Troubleshooting agent loading issues

## Quick Reference

```bash
# Validate all agents
python3 tests/agents/validate_configs.py .claude/agents/

# Validate single agent
./scripts/validate_agent.sh .claude/agents/agent-name.md
```

## Validation Checklist

Required YAML frontmatter fields:

```yaml
---
name: agent-name              # kebab-case identifier
description: "Brief desc"     # One sentence purpose
mcp_fallback: none
category: agent               # Classification
level: 0-5                    # Hierarchy level
phase: Plan|Test|Implementation|Package|Cleanup
---
```

Validation includes:

- YAML syntax correctness
- All required fields present
- Correct field types and values
- Valid tool names (Read, Write, Bash, Grep, Glob)
- Valid agent references in delegates_to/escalates_to
- Correct directory structure

## Error Handling

| Error | Fix |
|-------|-----|
| No YAML frontmatter | Ensure file starts/ends with `---` |
| Invalid phase value | Use: Plan, Test, Implementation, Package, Cleanup |
| Delegation target not found | Verify agent name or create referenced agent |
| Duplicate keys | Remove duplicate entries in frontmatter |
| Wrong level type | Must be integer 0-5, not string |

## References

- `/agents/templates/` - Agent configuration templates
- `.claude/agents/` - All agent configurations
- `CLAUDE.md` - Agent system guidelines
