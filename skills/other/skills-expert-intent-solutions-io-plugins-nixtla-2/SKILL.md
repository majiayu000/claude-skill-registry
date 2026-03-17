---
name: skills-expert
description: "Provide expert guidance on skills architecture, YAML frontmatter, tool permissions, and debugging. Use when creating, troubleshooting, or validating skills. Trigger with \"skill not loading\", \"frontmatter\", or \"allowed-tools\"."
allowed-tools: Read,Write,Glob,Grep,Edit
version: 1.0.0
author: Jeremy Longshore <jeremy@intentsolutions.io>
license: MIT
---

# Skills Expert

Provide expert guidance on Claude Code skills development, validation, and troubleshooting.

## Overview

This skill transforms Claude into a Claude Skills architecture expert. Use when:
- Creating new skills
- Debugging skill discovery/invocation issues
- Validating YAML frontmatter
- Understanding tool permissions
- Optimizing skill descriptions for selection

## Prerequisites

- Access to skill files in `.claude/skills/` or `skills-pack/.claude/skills/`
- Understanding of target skill's purpose

## Claude Skills Architecture

### YAML Frontmatter Fields

#### Required Fields

| Field | Max Length | Purpose |
|-------|------------|---------|
| `name` | 64 chars | Identifier used as `command` in Skill tool invocation |
| `description` | 1024 chars | Primary signal Claude uses to decide when to invoke skill |

#### Optional Fields

| Field | Type | Purpose |
|-------|------|---------|
| `allowed-tools` | CSV string | Pre-approved tools during skill execution |
| `model` | string | Override model (`"inherit"` or model ID) |
| `version` | string | Semantic versioning (e.g., `"1.0.0"`) |
| `license` | string | License metadata |
| `mode` | boolean | `true` = appears in Mode Commands section |
| `disable-model-invocation` | boolean | `true` = requires manual `/skill-name` |

#### Undocumented but Functional

| Field | Behavior |
|-------|----------|
| `when_to_use` | Appends to description with hyphen separator |

**Critical Rule**: Skill MUST have `description` OR `when_to_use` or it's filtered out.

### Directory Structure

```
skill-name/
├── SKILL.md              # Core prompt + frontmatter (required)
├── scripts/              # Python/Bash executables
├── references/           # Documentation loaded via Read tool
└── assets/               # Templates, static files (referenced by path)
```

### {baseDir} Variable

Template variable resolving to skill installation directory:

```markdown
## Resources
- Skill standard: `{baseDir}/references/skill-standard.md`
```

**Never hardcode absolute paths.**

### Tool Permission Scoping

Permissions in `allowed-tools` are scoped to skill execution only:

```yaml
# Granular scoping examples
allowed-tools: "Bash(git:*),Read,Grep"     # Only git commands
allowed-tools: "Bash(npm:*),Read,Write"    # Only npm commands
allowed-tools: "Read,Glob,Grep"            # Read-only audit
```

### Skill Selection Mechanism

Claude decides skill invocation through pure language understanding:

1. Claude receives Skill tool with `<available_skills>` section
2. Each skill formatted as: `"skill-name": description`
3. Claude's transformer matches user intent to descriptions
4. Claude invokes Skill tool with matching `command`

**No embeddings, regex, or classifiers** - pure LLM reasoning.

### Execution Flow

1. User request matches skill description
2. Claude invokes `Skill` tool with `command: "skill-name"`
3. Two messages injected:
   - **Visible**: `<command-message>The "skill-name" skill is loading</command-message>`
   - **Hidden**: Full SKILL.md content (isMeta: true)
4. Tool permissions scoped to `allowed-tools`
5. Skill prompt expands into conversation context

### Token Budget

- Default skill description budget: **15,000 characters**
- Typical skill prompt: 500-5,000 words

### Discovery Priority

Skills loaded in order (later overrides earlier):
1. User settings (`~/.config/claude/skills/`)
2. Project settings (`.claude/skills/`)
3. Plugin-provided skills
4. Built-in skills

### Critical Gotchas

1. **Skills are NOT concurrency-safe** - Multiple simultaneous skill invocations cause context conflicts
2. **Skills don't live in system prompts** - They're in the `tools` array as part of Skill meta-tool
3. **`when_to_use` is undocumented/experimental** - Safer to rely on detailed `description`
4. **Hardcoded paths break portability** - Always use `{baseDir}`

### Three-Stage Execution Pipeline

```
1. VALIDATION
   - Syntax checking
   - Skill existence verification
   - Frontmatter parsing

2. PERMISSION EVALUATION
   - Deny rules checked first (blocking patterns)
   - Allow rules checked second (pre-approved)
   - Default: prompt user for approval

3. LOADING & INJECTION
   - SKILL.md content loaded
   - Two messages injected (visible + hidden)
   - Context modifier applied
   - Tool permissions scoped
```

### Where Skills Actually Live

Skills are NOT in system prompts. They're bundled in the `tools` array:

```javascript
tools: [
  { name: "Read", ... },
  { name: "Write", ... },
  {
    name: "Skill",           // Meta-tool
    inputSchema: { command: string },
    prompt: "<available_skills>..." // Dynamic, contains all skill descriptions
  }
]
```

This enables dynamic loading without system prompt manipulation.

## Instructions

### When Creating Skills

1. **Write action-oriented descriptions** that explicitly state use cases
2. **Keep descriptions under 1024 chars** - be concise
3. **Use minimal tool permissions** - principle of least privilege
4. **Use {baseDir}** for all path references
5. **Include all four directories** (scripts/, references/, assets/) even if empty
6. **Test discovery** by asking Claude "what skills do you have?"

### When Debugging Skills

1. Check YAML frontmatter syntax (no tabs, proper quoting)
2. Verify `description` or `when_to_use` exists
3. Check skill directory is in correct location
4. Verify SKILL.md filename (case-insensitive)
5. Check for `disable-model-invocation: true` blocking auto-discovery

### When Validating Compliance

```yaml
# Nixtla Standard Checklist
- [ ] name: lowercase + hyphens, matches folder name
- [ ] description: action-oriented, <1024 chars
- [ ] version: semver format
- [ ] allowed-tools: minimal necessary
- [ ] NO deprecated fields (author, priority, audience)
- [ ] mode: true ONLY for mode skills
- [ ] disable-model-invocation: true ONLY for infra/dangerous skills
```

## Output

- Validated SKILL.md frontmatter
- Corrected skill configurations
- Debugging recommendations
- Skill architecture explanations

## Error Handling

| Issue | Solution |
|-------|----------|
| Skill not discovered | Check description/when_to_use exists |
| Tools not working | Verify allowed-tools syntax |
| Wrong skill invoked | Improve description specificity |
| Skill filtered out | Add required frontmatter fields |

## Examples

- Diagnose why a skill does not auto-trigger, then propose an updated `description` that includes both “Use when …” and “Trigger with …”.
- Audit a skill for minimal `allowed-tools` and scoped `Bash(...)` usage.

## Resources

- Project validator: `004-scripts/validate_skills_v2.py`
- Project skills: `003-skills/.claude/skills/`

## Examples

### Example 1: Minimal Skill

```yaml
---
name: my-skill
description: Generate reports from CSV data. Use when user has CSV files and needs analysis.
allowed-tools: "Read,Write,Glob"
version: "1.0.0"
---
```

### Example 2: Mode Skill

```yaml
---
name: expert-mode
description: Transform Claude into domain expert for extended session.
mode: true
allowed-tools: "Read,Write,Glob,Grep,Edit,Bash"
version: "1.0.0"
---
```

### Example 3: Infrastructure Skill

```yaml
---
name: deploy-skill
description: Deploy application to production. Dangerous - requires explicit invocation.
disable-model-invocation: true
allowed-tools: "Bash(deploy:*),Read,Glob"
version: "1.0.0"
---
```

## Resources

- Skill standard: `{baseDir}/references/skill-standard.md`
- Deep dive source: https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/
