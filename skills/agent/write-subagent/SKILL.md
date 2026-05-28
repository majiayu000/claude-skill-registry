---
name: write-subagent
description: Use when the user wants to create a new Claude Code subagent. Guides subagent creation with focused prompts and constrained tool access.
argument-hint: "[global|local] [subagent-name] [purpose...]"
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
---

# Subagent Creation Playbook

**CRITICAL: Before deploying any subagent, spawn a reviewer agent with REVIEW.md to audit `tools`. Overly permissive tool access can cause data loss or leak secrets.**

Create subagents as focused specialists, not general-purpose assistants.

## Arguments

```
$ARGUMENTS
```

## Process

### 0. Determine Scope

Check if arguments specify `global` or `local`:
- **`global`** or **`in ~/.claude/agents/`** → Subagent goes in dotfiles via chezmoi, available everywhere
- **`local`** or **`in .claude/agents/`** → Subagent goes in current project's `.claude/agents/`, scoped to this repo

If scope is unclear, ask:
> "Should this subagent be **global** (available in all projects via dotfiles) or **local** (scoped to this project only)?"

### 1. No Arguments? Extract from Conversation

If arguments are empty, the user wants to codify a delegatable task:

1. Analyze the conversation for patterns that would benefit from isolated context
2. Identify: task type, tools needed, decision points, success criteria
3. Propose a subagent name and description based on what was done
4. Ask about scope (global vs local)
5. Draft the subagent with focused system prompt
6. Ask user to confirm or refine before writing

### 2. Gather Context (when args provided)

If unclear, ask:
- Primary task type?
- Tools needed? (prefer minimal set)
- Should it run in background? (noisy/long-running)
- Permission mode? (default/acceptEdits/dontAsk/plan)
- Skills to preload?

### 3. Draft Subagent

**For global subagents:** Create `$(chezmoi source-path)/dot_claude/agents/<name>.md.tmpl` (note `.tmpl` extension)

**For local subagents:** Create `.claude/agents/<name>.md` in the current working directory (plain `.md`, no template)

**Global subagent template** (`.md.tmpl`):
```yaml
---
name: <kebab-case>
description: <When Claude should delegate + what it does. Use "proactively" for auto-use.>
tools: <minimal subset - see REVIEW.md>
disallowedTools: <explicit denials if inheriting>
{{ "{{-" }} template "bedrock-model" (dict "tier" "<haiku|sonnet|opus>" "root" .) {{ "}}" }}
permissionMode: <default|acceptEdits|dontAsk|plan>
skills: <list of skills to preload>
hooks: <optional lifecycle hooks>
---

<System prompt: Who the subagent is, what it does, how it works>
```

**Local subagent template** (plain `.md`):
```yaml
---
name: <kebab-case>
description: <When Claude should delegate + what it does. Use "proactively" for auto-use.>
tools: <minimal subset - see REVIEW.md>
disallowedTools: <explicit denials if inheriting>
# model: omit to inherit, or use plain: model: sonnet
permissionMode: <default|acceptEdits|dontAsk|plan>
---

<System prompt: Who the subagent is, what it does, how it works>
```

**For global subagents:** After writing, run:
- `chezmoi diff` to preview
- `chezmoi apply ~/.claude/agents/<name>.md` to deploy
- `chezmoi status` to verify

**For local subagents:** Restart Claude Code or run `/agents` to load immediately.

### 4. Principles

**Frontmatter:**
- `description`: Include "proactively" or "Use immediately after..." for auto-delegation
- `tools`: Minimal subset—subagents inherit all tools by default, so use `disallowedTools` to restrict
- `model`: Match to task complexity (see MODEL-SELECTION.md)
- `permissionMode`: Use `dontAsk` for read-only, `acceptEdits` for trusted modification

**System Prompt (body):**
- Define role clearly: "You are a..."
- Specify when to activate: "When invoked..."
- List concrete steps or checklist
- Describe output format
- Keep under 50 lines—focused specialists, not generalists

**Key Differences from Skills:**
- Subagents run in isolated context (separate from main conversation)
- Cannot spawn other subagents (no nesting)
- Use `tools`/`disallowedTools` instead of `allowed-tools`
- Body is the system prompt, not playbook instructions

### 5. Review (REQUIRED)

**Spawn a reviewer agent** with this skill's `REVIEW.md` file to audit:
- `tools` against red flags (reject broad patterns like all tools when minimal set needed)
- Is `disallowedTools` used to restrict inherited capabilities?
- Permission mode appropriate for the task?
- System prompt clear and focused?

## Quick Reference

| Goal | Frontmatter |
|------|-------------|
| Auto-delegation | `description` with "proactively" |
| Read-only | `disallowedTools: Write, Edit` or `tools: Read, Glob, Grep` |
| Fast/cheap | `model: haiku` |
| Capable | `model: sonnet` or `model: opus` |
| Skip prompts | `permissionMode: dontAsk` (auto-deny) or `acceptEdits` |
| Exploration | `permissionMode: plan` |
| Inject knowledge | `skills: [skill-name, ...]` |
| Validate operations | `hooks: { PreToolUse: [...] }` |

## Supplementary Docs

- **REVIEW.md** - **REQUIRED** checklist for auditing `tools` before deployment
- **MODEL-SELECTION.md** - When to use haiku vs sonnet vs opus
- **HOOKS.md** - Adding lifecycle hooks to subagents

## Examples

```
/write-subagent                              → extract subagent from current conversation (will ask about scope)
/write-subagent global code-reviewer         → global subagent for code review (via chezmoi)
/write-subagent local db-query               → project-local subagent for database queries
/write-subagent in ~/.claude/agents/ search  → global subagent (explicit path)
/write-subagent in .claude/agents/ lint      → local subagent (explicit path)
```

## Scope Decision Guide

| Choose **global** when... | Choose **local** when... |
|---------------------------|--------------------------|
| Subagent is useful across many projects | Subagent uses project-specific conventions |
| General-purpose task (review, debug, test) | Requires project-specific tools/config |
| You want it in your dotfiles | Team members should have it too |
| Personal workflow preference | Repo-specific domain knowledge |

## Anti-patterns

- Inheriting all tools when minimal set suffices
- Missing `disallowedTools` for write operations on read-only agents
- Verbose system prompts (over 50 lines)
- Generic descriptions that don't help Claude decide when to delegate
- Using subagents for tasks that need main conversation context
- Global subagent for project-specific logic
