---
name: skill-check
description: Validate skill/command file format and structure
user-invocable: true
---

# Skill File Validator

Validate skill files for correct format.

---

## Validation Target

- With argument: validate specific file
- Without: validate all `.claude/skills/*/SKILL.md`

---

## Required Frontmatter

```yaml
---
name: skill-name              # Required: lowercase, hyphenated
description: What it does     # Required: shown in / menu
version: 0.1.0              # Optional: semantic version
user-invocable: true          # Optional: default true
model: sonnet               # Optional: inherit, haiku, sonnet, opus, best, sonnet[1m], opus[1m], opusplan
allowed-tools:                # Optional: restrict tools (YAML list)
  - Read
  - Write
  - Bash
context: fork                 # Optional: isolated context
agent: agent-name             # Optional: run as specific agent
argument-hint: "<hint>"       # Optional: hint for arguments
when_to_use: Description of when this skill should be used  # Optional: underscore format
arguments:                    # Optional: structured argument definitions
  - name: arg-name
    description: What the argument does
    required: true
disable-model-invocation: false  # Optional: prevent programmatic invocation
hooks:                        # Optional: lifecycle hooks
  pre_tool_call:
    command: ./scripts/pre-check.sh
    once: false
  post_tool_call:
    command: ./scripts/post-check.sh
    once: false
  Stop:
    command: ./scripts/verify.sh
    once: false
---
```

### Valid Tools (for allowed-tools)
```
Read, Write, Edit, Bash, Grep, Glob, Task,
WebFetch, WebSearch, TodoWrite, NotebookEdit
```

---

## Validation Checklist

### Required Fields
- [ ] `name` exists (lowercase, hyphenated)
- [ ] `description` exists

### Optional Field Validation
- [ ] `allowed-tools` are valid tool names (if specified)
- [ ] `allowed-tools` uses YAML list format (if specified)
- [ ] `agent` references existing agent file (if specified)
- [ ] `version` is valid semver format (if specified)
- [ ] `model` is valid value: inherit, haiku, sonnet, opus, best, sonnet[1m], opus[1m], opusplan (if specified)
- [ ] `context` is valid value: fork (if specified)
- [ ] `argument-hint` is a string (if specified)
- [ ] `when_to_use` is a descriptive string (if specified)
- [ ] `arguments` is a valid array with name/description/required entries (if specified)
- [ ] `disable-model-invocation` is boolean (if specified)
- [ ] `hooks` has valid structure (if specified)

### Content Structure
- [ ] Clear instructions
- [ ] Uses `$ARGUMENTS` if expecting input
- [ ] Step-by-step process if complex

---

## Output Format

```markdown
## Skill Validation Report

### Files Checked
| File | Status | Issues |
|------|--------|--------|
| workflow/SKILL.md | OK | None |
| my-skill/SKILL.md | WARN | Missing description |

### Summary
- Total: [N]
- Valid: [N]
- Needs fixes: [N]
```

---

## Auto-Fix

- Add missing `name` from directory name
- Add missing `description`
- Convert bracket array tools to YAML list format
- Remove invalid frontmatter fields
- Add `$ARGUMENTS` handling
