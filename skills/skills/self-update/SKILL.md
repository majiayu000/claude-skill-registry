---
name: self-update
description: "Update the AGENTS.md system when its components change. Use when modifying agents, skills, or instructions files."
event: system-change
auto_trigger: true
priority: high
version: "2.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - changed_component
  - change_type (create|modify|delete)
  - affected_files
output: system_update_report
output_format: "List of updated system files"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "system-change"
    - "agent-modified"
    - "skill-modified"
    - "instruction-modified"
  file_patterns:
    - ".github/agents/*.agent.md"
    - ".github/skills/*/skill.md"
    - ".github/instructions/*.instructions.md"
    - "docs/templates/*.md"
  conditions:
    - "agent file created/modified/deleted"
    - "skill file created/modified/deleted"
    - "instruction file created/modified/deleted"

# Validation
validation_rules:
  - "all agents listed in AGENTS.md"
  - "all skills listed in README"
  - "routing keywords match agent keywords"
  - "version numbers consistent"

# Chaining
chain_after: []
chain_before: []
is_meta: true

# Agent Association
called_by: ["@Architect", "@Scribe"]
mcp_tools:
  - read_file
  - replace_string_in_file
  - list_dir
---

# Self-Update Meta Skill

> **Purpose:** Automatically update the AGENTS.md system when its components change. Keeps routing tables, README files, and documentation in sync.

## Trigger

**When:** Any agent, skill, or instruction file is created, modified, or deleted
**Context Needed:** Changed file, change type, current system state
**MCP Tools:** `read_file`, `replace_string_in_file`, `list_dir`

## Watched Paths

| Path                                     | Component Type | Updates                             |
| :--------------------------------------- | :------------- | :---------------------------------- |
| `.github/agents/*.agent.md`              | Subagent       | AGENTS.md routing, agents/README.md |
| `.github/skills/*/skill.md`              | Skill          | skills/README.md, trigger tables    |
| `.github/instructions/*.instructions.md` | Instruction    | instructions/README.md              |
| `docs/templates/*.md`                    | Template       | Documentation workflow              |

## Update Chains

### New Agent Added

```
Security.agent.md created
    ↓
1. Update agents/README.md (add to table)
2. Update AGENTS.md (add routing keywords)
3. Update copilot-instructions.md (if major)
```

### New Skill Added

```
new-skill/skill.md created
    ↓
1. Update skills/README.md (add to table)
2. Update trigger events table
3. Link to relevant agents
```

### Agent Modified

```
Backend.agent.md modified
    ↓
1. Check if keywords changed → update AGENTS.md
2. Check if tools changed → update README MCP section
3. Bump version in agent file
```

## Auto-Update Fields

### In Agent/Skill Files

```yaml
version: "1.0.0" # Bump on changes
last_updated: "YYYY-MM-DD" # Set to today
```

### In README Files

```markdown
| Agent | File | Domain | Primary MCP Tools |

# Re-scan directory and rebuild table
```

### In AGENTS.md

```markdown
## Agent Routing

| Keywords | Route To |

# Re-scan agent keywords and rebuild
```

## Version Bumping Rules

| Change Type                  | Version Bump  |
| :--------------------------- | :------------ |
| Fix typo, comment            | No bump       |
| Update tools, workflow       | Patch (0.0.X) |
| Add section, change behavior | Minor (0.X.0) |
| Breaking change              | Major (X.0.0) |

## Consistency Checks

After any update:

- [ ] All agents in README table
- [ ] All skills in README table
- [ ] AGENTS.md routing matches agent keywords
- [ ] No duplicate agent_ids or skill_ids
- [ ] All file references resolve

## Changelog Maintenance

When system changes, add to AGENTS.md changelog:

```markdown
## Change Log

| Version | Date       | Changes                                                        |
| :------ | :--------- | :------------------------------------------------------------- |
| 4.0.0   | 2026-01-26 | Added @Security, @DataArchitect, @SyncEngineer, @DevOps agents |
```

## Workflow

1. **Detect change** - What file changed?
2. **Parse metadata** - Read YAML frontmatter
3. **Identify updates** - What else needs changing?
4. **Apply updates** - Modify affected files
5. **Validate** - Run consistency checks
6. **Report** - List all changes made

## Output Report

```json
{
  "trigger": "Security.agent.md created",
  "updates": [
    { "file": "agents/README.md", "action": "add_row" },
    { "file": "AGENTS.md", "action": "add_routing" },
    { "file": "copilot-instructions.md", "action": "add_to_mcp_table" }
  ],
  "validation": "passed"
}
```

## Reference

- [AGENTS.md](/AGENTS.md)
- [agents/README.md](../agents/README.md)
- [skills/README.md](../skills/README.md)
