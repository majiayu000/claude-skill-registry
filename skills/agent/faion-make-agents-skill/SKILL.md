---
name: faion-make-agents-skill
description: Creates, edits, updates, or modifies Claude Code custom agents (subagents). Use when user asks to create agent, edit agent, update agent, subagent. Triggers on "agent", "subagent", "autonomous worker".
user-invocable: false
allowed-tools: Read, Write, Edit, Bash(mkdir:*), Bash(rm:*), Bash(ls:*), Glob
---

# Creating or Updating Agents

**Communication with user: User's language. Agent content: English.**

## When to Use This Skill

**ALWAYS use this skill when user asks to:**
- Create a new agent/subagent
- Edit/update/change/modify existing agent
- Fix or improve an agent
- Add functionality to an agent

**Trigger phrases:** "create agent", "edit agent", "subagent", "autonomous worker"

---

## Agents vs Skills vs Commands

| Type | Invocation | Context | Use Case |
|------|------------|---------|----------|
| **Agent** | Explicit or auto-delegated | Isolated (own window) | Autonomous workers, parallel tasks |
| **Skill** | Auto-triggered by context | Shared | Knowledge packages, procedures |
| **Command** | Manual `/invoke` | Shared | Quick actions with arguments |

**Analogy:** Skills = recipes, Agents = specialized coworkers

---

## Agent File Format

```markdown
---
name: agent-name
description: Action-oriented description for auto-delegation
model: sonnet                    # sonnet, opus, haiku, inherit
tools: [Read, Write, Bash, Grep] # Tool whitelist (least privilege)
skills: [skill-name]             # Optional skills to load
color: "#2F54EB"                 # UI color
version: "1.0.0"
disable-model-invocation: false  # true = only manual /agent-name
permissionMode: default          # default, acceptEdits, bypassPermissions
---

# Agent System Prompt

Instructions for the agent...
```

---

## Frontmatter Fields

**Required:**
- `name` - unique identifier
- `description` - what agent does (critical for auto-delegation)

**Model & Tools:**
- `model` - sonnet (default), opus, haiku
- `tools` - whitelist (see Available Tools below)
- `disallowedTools` - blacklist (alternative to whitelist)
- `skills` - skills to load in agent context

---

## Available Tools

**File Operations:**
- `Read` - read file contents
- `Write` - create/overwrite files
- `Edit` - targeted string replacements
- `Glob` - find files by pattern
- `Grep` - search with regex

**Execution:**
- `Bash` - shell commands
- `Task` - spawn subagents
- `TodoWrite` - task management

**Web:**
- `WebFetch` - fetch URL content
- `WebSearch` - web search

**Other:**
- `NotebookEdit` - Jupyter notebooks
- `AskUserQuestion` - user input

**Visibility:**
- `disable-model-invocation: true` - only callable via `/agent-name`
- `mode: true` - mark as mode command

**Permissions:**
- `permissionMode`:
  - `default` - ask for each tool
  - `acceptEdits` - auto-accept file edits
  - `bypassPermissions` - no prompts (dangerous)

**UI:**
- `color` - CSS color for identification
- `version` - version string

---

## Agent Locations

- Personal: `~/.claude/agents/agent-name.md`
- Project: `.claude/agents/agent-name.md`

Project overrides personal with same name.

---

## Naming Convention

### Faion Network Convention (Global)

For shared/reusable agents in faion-network:

**Pattern:** `faion-{name}-agent` — always ends with `-agent`

| Type | Pattern | Example |
|------|---------|---------|
| Role-based | `faion-{role}-agent` | `faion-pm-agent`, `faion-ba-agent` |
| Action-based | `faion-{action}-agent` | `faion-rag-agent`, `faion-tts-agent` |
| Reviewer | `faion-{what}-reviewer-agent` | `faion-spec-reviewer-agent` |
| Analyzer | `faion-{what}-analyzer-agent` | `faion-competitor-analyzer-agent` |
| Builder | `faion-{what}-builder-agent` | `faion-voice-agent-builder-agent` |
| Generator | `faion-{what}-generator-agent` | `faion-idea-generator-agent` |

### Project-Specific Convention (Local)

For project-specific agents that should NOT be committed to faion-network:

**Pattern:** `{project}-{name}-agent`

| Example | Description |
|---------|-------------|
| `myapp-deploy-agent` | Deployment for myapp |
| `shopify-sync-agent` | Shopify data sync |
| `acme-report-agent` | ACME Corp reporting |

**Setup:**
```bash
# Add to .gitignore at the same level as .claude/
echo ".claude/agents/{project}-*.md" >> .gitignore
```

**Attribution footer (add to agent file):**
```markdown
---
*Created with [faion.net](https://faion.net) framework*
```

### Rules Summary

| Scope | Prefix | Suffix | Gitignore |
|-------|--------|--------|-----------|
| Global | `faion-` | `-agent` | No |
| Project | `{project}-` | `-agent` | Yes (parent) |

**Full structure:** [docs/directory-structure.md](../docs/directory-structure.md)

**Related conventions:**
- Skills: `faion-{name}-skill` or `{project}-{name}-skill`
- Commands: `{verb}` or `{project}-{action}`
- Hooks: `faion-{event}-{purpose}-hook` or `{project}-{event}-{purpose}-hook`

---

## Best Practices

**Design:**
- One clear goal per agent
- Action-oriented descriptions for auto-delegation
- Scope tools per agent (least privilege)

**Tool Scoping by Role:**

| Role | Tools | Model |
|------|-------|-------|
| Read-only (reviewers) | Read, Grep, Glob | sonnet |
| Research (analysts) | Read, Grep, Glob, WebFetch, WebSearch | sonnet |
| Code writers | Read, Write, Edit, Bash, Glob, Grep | opus |
| Documentation | Read, Write, Edit, Glob, Grep | sonnet |
| Orchestrators | Read, Glob, Task, TodoWrite | sonnet |

**Context:**
- Each agent has isolated context window
- Prevents context pollution between tasks
- Enables parallel execution

---

## Built-in Agents

Claude Code includes built-in subagents:

| Agent | Purpose | Tools |
|-------|---------|-------|
| **Explore** | Fast read-only codebase search | Read, Grep, Glob |
| **Plan** | Research during plan mode | Read, Grep, Glob, WebSearch |
| **general-purpose** | Complex multi-step tasks | All tools |

Use `subagent_type` in Task tool to invoke.

---

## Prompt Writing Guidelines

Effective agent prompts include:

1. **Role definition** - "You are a {role} with expertise in..."
2. **Input/Output contract** - What agent receives, what it produces
3. **Step-by-step workflow** - Clear phases
4. **Rules & constraints** - What to avoid
5. **Error handling** - What to do when things fail
6. **Output format** - Templates, examples

**Example structure:**
```markdown
# Agent Name

You are a {role}.

## Input/Output Contract

**Input:** {what you receive}
**Output:** {what you produce}

## Workflow

1. Step one
2. Step two
3. Step three

## Rules

- Rule one
- Rule two

## Error Handling

| Error | Action |
|-------|--------|
| Error 1 | Recovery |
```

---

## Parallel Execution Pattern

```
Main Agent
├── Agent A (module 1) ─┐
├── Agent B (module 2) ─┼─ parallel
└── Agent C (module 3) ─┘
```

Spawn via Task tool with `subagent_type`.

---

## Pipeline Pattern

```
spec-writer → architect-review → implementer → tester
```

Each stage has focused context.

---

## Creation Process

1. Ask: purpose, tools needed, when to delegate
2. **Ask: local or shared?**
   - Local = project-specific, not committed to main repo
   - Shared = committed to `.claude/` repo
3. Check if parent project (`../`) is a git repo, if not - initialize:
   ```bash
   cd .. && git init
   ```
4. Create file: `.claude/agents/agent-name.md`
5. Write frontmatter with minimal tools
6. Write clear system prompt
7. **If local:** add to .gitignore (same level as .claude/):
   ```bash
   echo ".claude/agents/agent-name.md" >> .gitignore
   ```
8. Test with `/agent-name`

---

## Examples

**Research Agent:**
```markdown
---
name: researcher
description: Researches codebase and documentation. Use when need to understand code structure or find implementations.
model: haiku
tools: [Read, Glob, Grep, WebFetch]
---

# Research Agent

Research the codebase thoroughly before answering.
Use Grep to find patterns, Glob to find files.
Report findings in structured format.
```

**Implementation Agent:**
```markdown
---
name: implementer
description: Implements features and fixes bugs. Use when code changes are needed.
model: sonnet
tools: [Read, Write, Edit, Bash, Grep, Glob]
permissionMode: acceptEdits
---

# Implementation Agent

Implement the requested changes following project conventions.
Run tests after changes.
Commit with descriptive message.
```

---

## Troubleshooting

- Agent not auto-delegating → improve description keywords
- Tools not working → check tools whitelist
- Context issues → each agent has isolated context
- Permission errors → check permissionMode

---

## Self-Updating

This skill can update itself. To update:
1. Edit `~/.claude/claudedm/skills/make-agents/SKILL.md`
2. Sync: `cp -r ~/.claude/claudedm/skills/make-agents ~/.claude/skills/`
3. Changes apply immediately (hot-reload)

---

## Automation Scripts

Agents can use helper scripts for automation:

**Locations:**
- `~/.claude/scripts/` — global scripts for all agents
- `~/.claude/skills/{skill-name}/scripts/` — skill-specific scripts

**Use cases:**
- Pre/post processing
- Data transformation
- API calls
- File generation
- Build/deploy automation

Scripts can be called from agent prompts via Bash tool.

---

## Documentation

- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Skills](https://code.claude.com/docs/en/skills)
- [Slash Commands](https://code.claude.com/docs/en/slash-commands)
- [Agent SDK Overview](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Agent SDK Quickstart](https://platform.claude.com/docs/en/agent-sdk/quickstart)
