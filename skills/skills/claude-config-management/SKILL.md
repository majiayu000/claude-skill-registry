---
name: claude-config-management
description: Use when configuring, maintaining, troubleshooting, or optimizing Claude Code extensions including skills, commands, hooks, MCP servers, or agents. Provides best practices and prevents common mistakes.
---

# Claude Code Configuration Management

## Critical Constraints

**Context Budget**: MCP servers consume tokens before you work. A single server with 20 tools can use 14,000+ tokens. Keep active servers under 10.

**Precedence Rule**: Deny rules always win over allow rules at any level. More specific settings override broader ones.

**Performance Threshold**: If startup exceeds 30 seconds, clean ~/.claude.json of old project metadata.

## Quick Decision Framework

| I need to...                    | Use        | Not                    |
| ------------------------------- | ---------- | ---------------------- |
| Enforce rules deterministically | Hook       | Skill (probabilistic)  |
| Provide domain expertise        | Skill      | Command (user-invoked) |
| Create user-triggered action    | Command    | Skill (auto-triggered) |
| Connect external service        | MCP Server | Hook                   |
| Orchestrate multi-step tasks    | Agent      | Single command         |

## File Locations

| Content            | Location                       |
| ------------------ | ------------------------------ |
| Project overview   | CLAUDE.md (root)               |
| Team settings      | .claude/settings.json          |
| Personal overrides | .claude/settings.local.json    |
| MCP servers (team) | .mcp.json                      |
| Skills             | .claude/skills/[name]/SKILL.md |
| Commands           | .claude/commands/[name].md     |
| Reference docs     | .claude/docs/                  |

## Anti-Patterns to Avoid

**Skills**: Vague descriptions → Claude can't determine when to activate. Fix: Include trigger conditions.

**Commands**: Complex multi-step workflows → Belongs in skill. Fix: Keep commands simple (3-5 max).

**Hooks**: Complex inline commands → Hard to debug. Fix: Use script files.

**MCP**: Too many servers → Context exhaustion. Fix: Use McPick for selective enabling.

**CLAUDE.md**: Code style rules → Expensive enforcement. Fix: Use linters instead.

## Verification Commands

```bash
/mcp              # MCP server status
/doctor           # Full diagnostics
/context          # Context usage breakdown
claude mcp list   # List configured servers
```

## Maintenance Schedule

- **Weekly**: Review `/context`, clear accumulated sessions
- **Monthly**: Audit CLAUDE.md, check extension updates, clean ~/.claude.json
- **Quarterly**: Full audit, remove unused extensions, update team docs

## Detailed Reference

For complete procedures, checklists, and troubleshooting:
→ Read `.claude/docs/config-management-reference.md`

For finding and evaluating new extensions:
→ Read `.claude/docs/resource-discovery-reference.md` or use `/discover`