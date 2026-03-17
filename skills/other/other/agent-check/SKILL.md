---
name: agent-check
description: Validate custom agent file format and structure
user-invocable: true
---

# Agent File Validator

Validate agent files in `.claude/agents/` for correct format.

---

## Validation Target

- With argument: validate specific file
- Without: validate all `.claude/agents/*.md`

---

## Required Frontmatter

```yaml
---
name: agent-name          # Required: lowercase, hyphenated
description: Brief desc   # Required: under 100 chars
color: cyan               # Required: yellow, red, green, blue, magenta, cyan
tools:                    # Required: YAML list format
  - Read
  - Write
  - Grep
model: sonnet             # Required: inherit, haiku, sonnet, opus, best, sonnet[1m], opus[1m], opusplan
# forkContext: "true"     # Optional: run in forked context (string "true"/"false")
# maxTurns: 20            # Optional: max conversation turns (positive integer)
skills:                    # Optional: auto-load skills (array)
  - linked-skill
memory:                    # Optional: memory scopes to load (array)
  - user
  - project
  - local
mcpServers:                # Optional: MCP server refs or objects (array)
  - server-name
hooks:                     # Optional: agent-scoped lifecycle hooks
  PreToolUse:
    - matcher: Write
      command: ./validate.sh
  PostToolUse:
    - matcher: Bash
      command: ./log.sh
permissionMode: default    # Optional: permission handling
disallowedTools:           # Optional: explicit tool blocking
  - NotebookEdit
---
```

### Valid Tools
```
Read, Write, Edit, Bash, Grep, Glob, Task,
WebFetch, WebSearch, TodoWrite, NotebookEdit
```

### Valid Colors
```
yellow, red, green, blue, magenta, cyan
```

### Valid Models
```
inherit, haiku, sonnet, opus, best, sonnet[1m], opus[1m], opusplan
```

---

## Validation Checklist

### Required Fields
- [ ] `name` exists (lowercase, hyphenated)
- [ ] `description` exists (under 100 chars)
- [ ] `tools` exists (YAML list format, not bracket array)
- [ ] `color` is set (valid color name)
- [ ] `model` is set (inherit/haiku/sonnet/opus/best/sonnet[1m]/opus[1m]/opusplan)

### Optional Fields
- [ ] `skills` references existing skills (array, if set)
- [ ] `forkContext` is string "true" or "false" (if set)
- [ ] `maxTurns` is positive integer (if set)
- [ ] `memory` is valid array of: user, project, local (if set)
- [ ] `mcpServers` is valid array of string refs or objects (if set)
- [ ] `hooks` has valid structure (if set)
- [ ] `permissionMode` is valid value (if set)
- [ ] `disallowedTools` are valid tool names (if set)

### Content Structure
- [ ] `# Agent Name` heading
- [ ] `## Activation` section
- [ ] Process/workflow description
- [ ] Output format definition

### Format Rules
- [ ] `tools` uses YAML list format (not `[Read, Write]` bracket array)
- [ ] No duplicate tools in list
- [ ] All tools are valid tool names

---

## Output Format

```markdown
## Agent Validation Report

### Files Checked
| File | Status | Issues |
|------|--------|--------|
| code-reviewer.md | OK | None |
| my-agent.md | WARN | Missing color, model |

### Summary
- Total: [N]
- Valid: [N]
- Needs fixes: [N]
```

---

## Auto-Fix

- Convert bracket array tools to YAML list format
- Convert string skills to YAML array
- Add missing `color` field (default: cyan)
- Add missing `model` field (default: inherit)
- Convert boolean forkContext to string
- Convert scalar memory to array format
- Remove invalid tools
- Add recommended sections
