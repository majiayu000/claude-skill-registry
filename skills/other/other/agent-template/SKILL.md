---
name: agent-template
description: Generate custom agent from template
user-invocable: true
---

# Agent Template Generator

Generate a custom agent file based on requirements.

**Usage**: `/agent-template [agent-name] [purpose]`

---

## Templates

| Purpose | Template | Tools | Color | Model |
|---------|----------|-------|-------|-------|
| Review/Audit | Reviewer | Read, Grep, Glob, Bash | yellow | sonnet |
| Generate/Create | Generator | Read, Write, Grep, Glob | cyan | sonnet |
| Fix/Modify | Fixer | Read, Write, Edit, Bash, Grep | red | sonnet |
| Test/Validate | Tester | Read, Bash, Grep, Glob | green | sonnet |
| Document | Documenter | Read, Write, Grep, Glob | cyan | sonnet |
| Orchestrate | Orchestrator | Read, Write, Bash, Grep, Glob, Task | cyan | haiku |

---

## Process

1. **Gather Requirements**
   - Agent name (lowercase, hyphenated)
   - Purpose
   - Tools needed
   - Model (haiku/sonnet/opus)
   - Linked skill (if any)

2. **Select Template** based on purpose

3. **Generate File** at `.claude/agents/[name].md`

4. **Validate** with `/agent-check`

---

## Frontmatter Reference

```yaml
---
name: agent-name            # Required: lowercase, hyphenated, 3-50 chars
description: Brief desc     # Required: triggering conditions + <example> blocks
color: cyan                 # Required: yellow, red, green, blue, magenta, cyan
tools:                      # Optional: YAML list (omit = all tools)
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - WebFetch
  - WebSearch
  - TodoWrite
  - NotebookEdit
model: sonnet               # Required: inherit, haiku, sonnet, opus, best, sonnet[1m], opus[1m], opusplan
# forkContext: "true"        # Optional: context isolation (string, not boolean)
# maxTurns: 20              # Optional: max agentic turns before stopping
skills:                     # Optional: skills to auto-load (array)
  - linked-skill
# memory:                   # Optional: CLAUDE.md access (array)
#   - user
#   - project
#   - local
# mcpServers:               # Optional: MCP servers (string ref or inline config)
#   - memory
#   - name: custom-server
#     type: stdio
#     command: npx
#     args: ["-y", "@example/server"]
hooks:                      # Optional: agent-scoped lifecycle hooks
  PreToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: ./scripts/validate.sh
  PostToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: ./scripts/log.sh
  Stop:
    - hooks:
        - type: command
          command: ./scripts/check.sh
          once: true
permissionMode: default     # Optional: default, acceptEdits, bypassPermissions, plan, delegate, dontAsk
disallowedTools:            # Optional: explicit tool blocking
  - NotebookEdit
---
```

---

## Reviewer Template Structure

```markdown
---
name: [name]
description: [brief purpose]
color: yellow
tools:
  - Read
  - Grep
  - Glob
  - Bash
model: sonnet
skills:
  - linked-skill
---

# [Name] Agent

## Activation
When to trigger

## Review Checklist
- [ ] Check items

## Output Format
Report structure
```

---

## Example

```
/agent-template security-scanner "scan code for vulnerabilities"

Output: Created .claude/agents/security-scanner.md
```
