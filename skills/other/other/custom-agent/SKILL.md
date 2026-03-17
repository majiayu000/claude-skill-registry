---
name: custom-agent
description: '[AI & Tools] Create, verify, or enhance Claude Code custom agents (.claude/agents/*.md). Triggers on: create agent, new agent, agent schema, audit agent, verify agent, review agent, enhance agent, refactor agent, agent quality, custom agent.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Create new custom agents, audit existing agent quality, or enhance agent definitions.

**Workflow:** Detect mode (Create/Audit/Enhance) from `$ARGUMENTS` → Execute → Validate

**Key Rules:**
- Agent files: `.claude/agents/{name}.md` with YAML frontmatter + markdown body as system prompt
- Agent does NOT inherit Claude Code system prompt — write complete instructions
- Minimize tools to only what the agent needs
- System prompt structure: `## Role` → `## Workflow` → `## Key Rules` → `## Output`

## Modes

| Mode | Trigger | Action |
|------|---------|--------|
| **Create** | `$ARGUMENTS` describes a new agent | Create agent file |
| **Audit** | mentions verify, audit, review, check, quality | Audit existing agents |
| **Enhance** | mentions refactor, enhance, improve, optimize | Improve existing agent |

## Mode 1: Create Agent

1. **Clarify** — `AskUserQuestion`: purpose, read-only vs read-write, model preference, memory needs
2. **Check Existing** — Glob `.claude/agents/*.md` for similar agents. Avoid duplication.
3. **Scaffold** — Create `.claude/agents/{name}.md` using frontmatter template below
4. **Write System Prompt** — Structure: `## Role` → `## Workflow` → `## Key Rules` → `## Output`
5. **Validate** — Run audit checklist below

## Mode 2: Audit Agents

1. **Discover** — Glob `.claude/agents/*.md`
2. **Parse** — Read first 30 lines of each, extract frontmatter
3. **Validate** — Check each audit rule below
4. **Report** — Issues grouped by severity (Error > Warning > Info), include quality scores
5. **Fix** — If user confirms, fix Error-level issues automatically

## Mode 3: Enhance Agent

1. **Read** — Load specified agent file
2. **Analyze** — Check against best practices and audit checklist
3. **Recommend** — List improvements with rationale
4. **Apply** — If user confirms, apply enhancements

---

## Agent Frontmatter Schema

```yaml
---
# REQUIRED
name: my-agent                    # Lowercase + hyphens only
description: >-                   # Claude uses this to decide when to delegate
  Use this agent when [specific trigger scenarios].

# OPTIONAL — Tools
tools: Read, Grep, Glob, Bash     # Allowlist (omit both → inherits all)
disallowedTools: Write, Edit      # Denylist (removes from inherited set)
# Task(agent1, agent2) restricts spawnable subagents

# OPTIONAL — Model
model: inherit                    # inherit | sonnet | opus | haiku

# OPTIONAL — Permissions
permissionMode: default           # default | acceptEdits | dontAsk | bypassPermissions | plan

# OPTIONAL — Limits
maxTurns: 30                      # Prevents runaway agents

# OPTIONAL — Skills (content injected at startup)
skills:
  - skill-name

# OPTIONAL — MCP Servers
mcpServers:
  - server-name

# OPTIONAL — Hooks (scoped to this agent)
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"

# OPTIONAL — Memory (MEMORY.md auto-injected, Read/Write/Edit auto-added)
memory: project                   # user (~/.claude/agent-memory/) | project (.claude/agent-memory/) | local (gitignored)

# OPTIONAL — Execution
background: false                 # true = always background task
isolation: worktree               # Run in temporary git worktree
---
```

## Tool Restriction Patterns

| Agent Type | Recommended `tools` |
|---|---|
| Explorer/Scout | `Read, Grep, Glob, Bash` |
| Reviewer (read-only) | `Read, Grep, Glob` |
| Writer/Implementer | `Read, Write, Edit, Grep, Glob, Bash` |
| Researcher | `Read, Grep, Glob, WebFetch, WebSearch` |
| Orchestrator | `Read, Grep, Glob, Task(sub1, sub2)` |

Available tools: Read, Write, Edit, MultiEdit, Glob, Grep, Bash, WebFetch, WebSearch, Task, NotebookRead, NotebookEdit, TaskCreate, TaskUpdate, AskUserQuestion, + MCP tools.

## Model Selection

| Model | Best For |
|---|---|
| `haiku` | Fast read-only: scanning, search, file listing |
| `sonnet` | Balanced: code review, debugging, analysis |
| `opus` | High-stakes: architecture, complex implementation |
| `inherit` | Default — match parent's model |

## Description Best Practices

```yaml
# BAD — too vague, Claude won't auto-delegate
description: Reviews code

# GOOD — specific trigger conditions
description: >-
  Use this agent for comprehensive code review after implementing features,
  before merging PRs, or when assessing code quality and technical debt.
```

- Include "Use this agent when..." phrasing with concrete scenarios
- Add "use proactively" to encourage auto-invocation

## Common Anti-Patterns

| Anti-Pattern | Fix |
|---|---|
| No tool restrictions | Add `tools` allowlist |
| Vague description | Write specific trigger conditions |
| Giant system prompt | Keep concise, use `skills` for detail |
| No `maxTurns` | Set 20-30 to prevent runaway |
| Recursive subagents | Restrict `Task` in tools |
| Windows long prompts (>8191 chars) | Use file-based agents, not `--agents` CLI |

## Context Passing

- Agent receives ONLY its system prompt + task prompt — NOT parent conversation
- Parent receives ONLY agent's final result — NOT intermediate tool calls
- This isolation is the primary context management benefit

## Audit Checklist

| # | Check | Rule | Severity |
|---|-------|------|----------|
| 1 | Frontmatter exists | Must have `---` delimiters | Error |
| 2 | Name present & valid | Lowercase + hyphens only | Error |
| 3 | Description present | Non-empty, >20 chars | Error |
| 4 | No duplicate names | Unique across all agent files | Error |
| 5 | Description quality | Specific trigger scenarios | Warning |
| 6 | Tools minimal | Only what agent needs | Warning |
| 7 | Prompt structure | Has `## Role` + `## Workflow` | Warning |
| 8 | Model set | When task differs from default | Info |
| 9 | maxTurns set | Recommended 20-30 | Info |

**Quality Score:** Valid frontmatter (20) + Description >50 chars (20) + Tools restricted (15) + Role section (15) + Workflow section (10) + Model set (10) + maxTurns set (10) = 100. Rating: 80+ Excellent, 60-79 Good, 40-59 Needs Work, <40 Poor.

## File Priority (highest first)

1. `--agents` CLI flag (session only)
2. `.claude/agents/*.md` (project)
3. `~/.claude/agents/*.md` (user)
4. Plugin `agents/` directory

Same `name` across levels: higher-priority wins. Use `claude agents` CLI to list all.

## Requirements

<user-prompt>$ARGUMENTS</user-prompt>

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always break work into small todo tasks
- Always add a final review todo task
