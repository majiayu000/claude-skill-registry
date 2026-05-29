---
name: 'artefact-logger'
description: 'Log access to Claude configuration artefacts (CLAUDE.md, rules, skills, commands, agents). This skill should be invoked automatically after reading configuration files to track usage.'
---

# Artefact Logger

Log access to Claude configuration artefacts for usage tracking.

## When to Use

Invoke this skill after reading:

- `CLAUDE.md` files
- `.claude/rules/**` files
- `.claude/skills/**` files
- `.skills/commands/**` files
- `.claude/agents/**` files (custom agents only, not internal Task tool agents)

## How to Log

Run the script with required arguments:

```bash
.claude/skills/artefact-logger/scripts/log-artefact.sh "<name>" "<path>" "<type>"
```

### Arguments

| Argument | Description                  | Valid Values                                     |
| -------- | ---------------------------- | ------------------------------------------------ |
| `name`   | Filename or skill/agent name | Any string                                       |
| `path`   | Relative path or identifier  | Any path string                                  |
| `type`   | Artefact type                | `claude_md`, `rule`, `skill`, `command`, `agent` |

### Examples

```bash
# Log CLAUDE.md access
.claude/skills/artefact-logger/scripts/log-artefact.sh "CLAUDE.md" "CLAUDE.md" "claude_md"

# Log rule access
.claude/skills/artefact-logger/scripts/log-artefact.sh "standard-changelog.md" ".claude/rules/packmind/standard-changelog.md" "rule"

# Log skill invocation
.claude/skills/artefact-logger/scripts/log-artefact.sh "signal-capture" "signal-capture" "skill"
```

## Notes

- Do NOT log internal Task tool agents (Explore, Plan, Bash, general-purpose, etc.)
- Only log custom agents defined in `.claude/agents/**`
- The script creates `.claude/artefacts.yaml` if missing
- Each access is logged with an ISO 8601 timestamp
