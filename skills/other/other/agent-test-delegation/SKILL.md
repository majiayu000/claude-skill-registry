---
name: agent-test-delegation
description: "Test agent delegation patterns to verify hierarchy and escalation paths. Use after modifying agent structure."
mcp_fallback: none
category: agent
user-invocable: false
---

# Agent Delegation Testing

Verify agent hierarchy, delegation chains, and escalation paths.

## When to Use

- After modifying agent hierarchy
- Verifying escalation paths work correctly
- Troubleshooting delegation issues
- CI/CD validation before merge

## Quick Reference

```bash
# Test all delegation patterns
python3 tests/agents/test_delegation.py .claude/agents/

# Test specific agent delegation
./scripts/test_agent_delegation.sh implementation-specialist

# Visualize delegation tree
./scripts/visualize_delegation.sh
```

## What Gets Tested

**Hierarchy levels**: Agents delegate to lower levels, escalate to higher levels

**Delegation chains**: L0 → L1 → L2 → L3 → L4 (proper tree structure)

**Circular dependencies**: Detect A → B → C → A patterns

**Reference validity**: All delegates_to/escalates_to targets exist

**Level consistency**: Level values correct and levels don't skip improperly

## Validation Rules

| Rule | Example ✅ | Wrong ❌ |
|------|-----------|---------|
| Delegate downward | L2 → L3 | L3 → L2 |
| Escalate upward | L3 → L2 | L3 → L4 |
| No circles | A → B, A → C | A → B → A |
| Valid refs | Existing agent | Nonexistent agent |

## Common Issues

**Circular dependency**: Agent A → Agent B → Agent A

- **Fix**: Break circle by restructuring delegation

**Skip-level delegation**: L2 → L4 (skips L3)

- **Fix**: Document exception in agent description

**Orphaned agent**: No other agent delegates to it

- **Fix**: Add delegation or remove if unused

## References

- `/agents/delegation-rules.md` - Complete delegation guidelines
- `.claude/agents/` - All agent configurations
- `CLAUDE.md` - Hierarchy documentation
