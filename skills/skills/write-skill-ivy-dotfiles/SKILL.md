---
name: write-skill
description: Use when the user wants to create a new Claude Code skill. Guides skill creation with playbook patterns.
argument-hint: "[global|local] [skill-name] [purpose...]"
{{- template "bedrock-model" (dict "tier" "opus" "root" .) }}
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash(chezmoi apply:*)
  - Bash(chezmoi diff:*)
  - Bash(chezmoi status:*)
  - Bash(chezmoi source-path:*)
  - Bash(ls:*)
---

# Skill Creation Playbook

**CRITICAL: Before deploying any skill, spawn a reviewer agent with REVIEW.md to audit `allowed-tools`. Overly permissive tool access (e.g., `Bash(git:*)`) can cause data loss or leak secrets.**

Create skills as flexible playbooks, not rigid scripts.

## Arguments

```
$ARGUMENTS
```

## Pre-computed Context

The following paths and listings were computed before this skill was invoked:

**Chezmoi source path:** !`chezmoi source-path 2>/dev/null || echo "(chezmoi not available)"`
**Global skills source:** !`chezmoi source-path 2>/dev/null`/dot_claude/skills
**Global skills deployed:** ~/.claude/skills

## Process

### 0. Determine Scope

Check if arguments specify `global` or `local`:
- **`global`** or **`in ~/.claude/skills/`** → Skill goes in dotfiles via chezmoi, available everywhere
- **`local`** or **`in .claude/skills/`** → Skill goes in current project's `.claude/skills/`, scoped to this repo

If scope is unclear, ask:
> "Should this skill be **global** (available in all projects via dotfiles) or **local** (scoped to this project only)?"

### 1. No Arguments? Extract from Conversation

If arguments are empty, the user wants to codify the task just performed:

1. Analyze the conversation for the repeatable pattern
2. Identify: trigger conditions, tools used, decision points, inputs/outputs
3. Propose a skill name and description based on what was done
4. Ask about scope (global vs local)
5. Draft the skill capturing the workflow as a playbook
6. Ask user to confirm or refine before writing

### 2. Gather Context (when args provided)

If unclear, ask:
- Trigger? (user/auto/always)
- Tools needed?
- Fork context? (noisy output)
- Side effects? (commits/deploys/APIs)

### 3. Draft Skill

**For global skills:** Create `$(chezmoi source-path)/dot_claude/skills/<name>/SKILL.md.tmpl` (note `.tmpl` extension)

**For local skills:** Create `.claude/skills/<name>/SKILL.md` in the current working directory (plain `.md`, no template)

**Global skill template** (`.md.tmpl`):
```yaml
---
name: <kebab-case>
description: <When to use + what it does>
argument-hint: <flexible, use brackets>
{{ "{{-" }} template "bedrock-model" (dict "tier" "<haiku|sonnet|opus>" "root" .) {{ "}}" }}
disable-model-invocation: <true if user-only>
context: <fork if output not needed>
allowed-tools: <minimal safe subset>
---
```

**Local skill template** (plain `.md`):
```yaml
---
name: <kebab-case>
description: <When to use + what it does>
argument-hint: <flexible, use brackets>
# model: omit to inherit session default, or use plain: model: sonnet
disable-model-invocation: <true if user-only>
context: <fork if output not needed>
allowed-tools: <minimal safe subset>
---
```

Both follow the same body structure:

```markdown
# <Title>

## Arguments
\`\`\`
\$ARGUMENTS
\`\`\`

## Instructions
<Decision-tree playbook>

## Examples
<Varied inputs and outcomes>
```

**For global skills:** After writing, run:
- `chezmoi diff` to preview
- `chezmoi apply ~/.claude/skills/<name>` to deploy
- `chezmoi status` to verify

**For local skills:** No deployment needed - the skill is immediately available in the project.

### 4. Principles

**Frontmatter:**
- `description`: "Use when..." for auto-invoke
- `context: fork`: noisy output that won't inform follow-up
- `disable-model-invocation: true`: side-effect skills
- `allowed-tools`: tools that run WITHOUT user approval (omitted tools still work but prompt user)

**Arguments:**
- Free-form: `[package | url...]` not `<package>`
- Show varied inputs in examples
- Parse flexibly, not strictly

**Content:**
- Decision trees, not linear scripts
- <60 lines; externalize reference material
- Refer to "arguments" after the Arguments section
- `\${CLAUDE_SESSION_ID}` for session-specific context

### 5. Review (REQUIRED)

**Spawn a reviewer agent** with this skill's `REVIEW.md` file to audit:
- `allowed-tools` against red flags (reject `Bash(git:*)`, `Bash(npm:*)`, etc.)
- Narrowing principle: most specific pattern used?
- Publication risks: commands that send data externally?
- Deletion risks: commands that remove data?

Also check verbosity, edge cases, and invocation clarity.

## Quick Reference

| Goal | Frontmatter |
|------|-------------|
| User-only trigger | `disable-model-invocation: true` |
| Auto-invoke | `description` with "Use when..." |
| Hidden from `/` menu | `user-invocable: false` |
| Isolate context | `context: fork` |
| Specific agent | `context: fork` + `agent: Explore` |
| Right-size capability | `model: haiku\|sonnet\|opus` |

## Supplementary Docs

- **REVIEW.md** - **REQUIRED** checklist for auditing `allowed-tools` before deployment
- **MODEL-SELECTION.md** - When to use haiku vs sonnet vs opus
- **SHIM-PATTERN.md** - Wrapper scripts for enforcing constraints (advanced)

| Safe | Unsafe |
|------|--------|
| `Bash(git status:*)` | `Bash(git:*)` |
| `Bash(npm test:*)` | `Bash(npm:*)` |
| `Read, Grep, Glob` | `Bash(rm:*)` |

## Examples

```
/write-skill                              → extract skill from current conversation (will ask about scope)
/write-skill global deploy                → global skill for deployments (via chezmoi)
/write-skill local lint-fix               → project-local skill for this repo only
/write-skill in ~/.claude/skills/ search  → global skill (explicit path)
/write-skill in .claude/skills/ format    → local skill (explicit path)
```

## Scope Decision Guide

| Choose **global** when... | Choose **local** when... |
|---------------------------|--------------------------|
| Skill is useful across many projects | Skill is specific to this codebase |
| General-purpose workflow (git, testing) | Project-specific conventions |
| You want it in your dotfiles | Collaborators should have it too |
| Personal preference/style | Team or repo-specific process |

## Anti-patterns

- Strict positional arguments
- Broad tool access
- Verbose prose over terse bullets
- Missing `context: fork` for noisy ops
- Hardcoded paths vs arguments
- Global skill for project-specific logic
- Local skill for personal workflows you'd want everywhere
