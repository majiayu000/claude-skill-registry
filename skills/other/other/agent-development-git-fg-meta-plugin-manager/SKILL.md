---
name: agent-development
description: "Create and audit Claude subagents. Use when building specialized workers with isolated context. Includes frontmatter, allowed-tools, and agent patterns. Not for commands or skills."
---

<mission_control>
<objective>Create and audit agents that follow toolkit standards: proper configuration, tool constraints, and task scope</objective>
<success_criteria>Agent has valid frontmatter, appropriate allowed-tools, and clear task scope</success_criteria>
</mission_control>

## Quick Start

**If you need to create an agent:** Create `.claude/agents/name/` with `agent.md`.

**If you need to audit an agent:** Invoke this skill directly to validate configuration.

**If you need to refine an agent:** Compare against patterns and apply fixes.

## Navigation

| If you need... | Read this section... |
| :------------- | :------------------- |
| Directory structure | ## PATTERN: Directory |
| Frontmatter format | ## PATTERN: Frontmatter |
| allowed-tools | ## PATTERN: Allowed Tools |
| Perfect agent examples | ## PATTERN: Perfect Agent |
| Common failures | ## ANTI-PATTERN: Common Failures |
| Validation checklist | ## Validation Checklist |

## Philosophy

Agents are specialized workers with isolated context. Unlike skills (portable knowledge), agents are configured workers with specific tool access and task scope.

**Key insight:** Agents are "configured workers" - they have specific capabilities defined by their configuration, unlike skills which encode knowledge.

**Why this matters:**
- Agents have isolated context (Task tool spawns subagent)
- Agents can have tool restrictions (allowed-tools)
- Agents are task-specific workers, not general knowledge
- Agent behavior is defined by frontmatter, not SKILL.md

## PATTERN: Directory

Agents use a simple directory structure:

```
.claude/agents/agent-name/
└── agent.md
```

### Directory Structure

| Item | Purpose |
| :--- | :------- |
| `agent.md` | Agent configuration with frontmatter |
| No `references/` | Agents are self-configuring |

### Example Structure

```
.claude/agents/
├── planning-agent/
│   └── agent.md
├── code-review-agent/
│   └── agent.md
└── testing-agent/
    └── agent.md
```

## PATTERN: Frontmatter

Agents use YAML frontmatter for configuration:

```yaml
---
name: agent-name
description: "Brief description, non spoiling of the content. Use when {trigger condition + keywords + key sentences user might say that should lead the agent to be invoked}. Not for {exclusions}."
allowed-tools:
  - Read
  - Write
  - Glob
model: sonnet  # Optional: sonnet, opus, haiku
temperature: 0  # Optional: 0-1
---
```

### Frontmatter Fields

| Field | Required? | Purpose |
| :---- | :-------- | :------- |
| `name` | Yes | Agent identifier |
| `description` | Yes | Auto-discovery |
| `allowed-tools` | No | Tool whitelist |
| `model` | No | Claude model (sonnet/opus/haiku) |
| `temperature` | No | Response creativity (0-1) |

### Description Format

| Element | Purpose | Required? |
| :------ | :------- | :-------- |
| Brief description | Action summary (non-spoiling) | Yes |
| "Use when" | Activation conditions | Yes |
| Keywords/triggers | User phrases that activate | Yes |
| "Not for" | Exclusions | Yes |

### Description Examples

**Basic:**
```yaml
description: "Plan implementation tasks. Use when starting new work or features that need planning."
```

**Intermediate:**
```yaml
description: "Create implementation plans with TDD discipline. Use when starting new features, following test-driven development, or planning complex implementations. Not for bug fixes or quick tasks."
```

**Gold Standard:**
```yaml
description: "Plan implementation using TDD discipline with parallel execution. Use when building new features, following test-driven development, or planning complex implementations. Creates test-first plans with verification gates. Not for bug fixes, hotfixes, or trivial changes."

## PATTERN: Allowed Tools

The `allowed-tools` field restricts which tools the agent can use:

```yaml
---
name: restricted-agent
description: "Agent with limited capabilities."
allowed-tools:
  - Read
  - Write
---
```

### Tool Categories

| Category | Tools |
| :-------- | :----- |
| File Operations | Read, Write, Glob, Grep |
| Code Intelligence | LSP operations |
| Execution | Bash, Task |
| VS Code | All mcp__vscode-* tools |
| Web | WebFetch, WebSearch, mcp__exa-* |
| Orchestration | Skill, AskUserQuestion |

### allowed-tools Best Practices

| Do | Don't |
| :-- | :----- |
| Restrict to minimum needed | Use broad tool access |
| Limit destructive tools | Allow rm, rm -rf without hooks |
| Use for behavior guidance | Use as security (personal project) |
| Document why restrictions exist | Add without reason |

### Example Configurations

**Minimal (Read-only analysis):**
```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
  - LSP
```

**Standard (Read-write):**
```yaml
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - LSP
```

**Full access:**
```yaml
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Task
  - LSP
  - WebFetch
  - WebSearch
```

## PATTERN: Perfect Agent

### Simple Agent (Analysis)

```yaml
---
name: analysis-agent
description: "Analyze code and find patterns. Use when exploring codebase. Includes pattern matching and file discovery. Not for modifications."
allowed-tools:
  - Read
  - Glob
  - Grep
  - LSP
model: sonnet
---
```

### Medium Agent (with Task delegation)

```yaml
---
name: planning-agent
description: "Create implementation plans with TDD. Use when starting features. Creates test-first plans with verification. Not for bug fixes."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Task
  - Skill
model: sonnet
---
```

### Complex Agent (Full capabilities)

```yaml
---
name: full-agent
description: "Complete development workflow agent. Use for autonomous development. Includes planning, implementation, testing. Not for research tasks."
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Task
  - Skill
  - LSP
  - WebFetch
  - WebSearch
  - mcp__vscode-*
model: opus
temperature: 0.7
---
```

## ANTI-PATTERN: Common Failures

### Anti-Pattern: Overly Broad allowed-tools

```yaml
❌ Wrong:
allowed-tools:
  - Read
  - Write
  - Bash
  - Task
  - Skill
  - ALL_TOOLS  # Never do this
```

**Fix:** Restrict to minimum needed:
```yaml
✅ Correct:
allowed-tools:
  - Read
  - Glob
  - Grep
```

### Anti-Pattern: Missing Task Scope

```yaml
❌ Wrong:
---
name: planning-agent
description: "Plan tasks."
---
```

**Fix:** Define clear scope in description:
```yaml
✅ Correct:
---
name: planning-agent
description: "Create implementation plans with TDD. Use when starting features. Not for modifications."
---
```

### Anti-Pattern: No Model Specification

```yaml
❌ Wrong:
---
name: analysis-agent
description: "Deep analysis."
---
```

**Fix:** Specify model for specialized tasks:
```yaml
✅ Correct:
---
name: analysis-agent
description: "Deep analysis. Use for complex investigations."
model: opus
---
```

### Anti-Pattern: Wrong Directory Structure

```
❌ Wrong:
.claude/agents/planning-agent/
├── agent.md
└── references/
    └── patterns.md

✅ Correct:
.claude/agents/planning-agent/
└── agent.md

Or use a Skill if references are needed:
.claude/skills/planning/
├── SKILL.md
└── references/
    └── patterns.md
```

### Anti-Pattern: Agent References Slash Commands

```yaml
❌ Wrong:
description: "Run /meta:refine:all operations."
```

**Fix:** Never reference slash commands:
```yaml
✅ Correct:
description: "Run refinement operations. Use when improving multiple components. Orchestrates all refine operations."
```

## Validation Checklist

Before claiming agent authoring complete:

**Structure:**
- [ ] Agent in `.claude/agents/name/` directory
- [ ] Single `agent.md` file
- [ ] No `references/` folder

**Frontmatter:**
- [ ] Valid `name` field
- [ ] Description uses "Use when" format
- [ ] Clear task scope defined
- [ ] Exclusions documented if applicable

**Configuration:**
- [ ] `allowed-tools` defined (or omitted for defaults)
- [ ] Model specified for specialized tasks
- [ ] Temperature set for creative tasks

**Best Practices:**
- [ ] Tools restricted to minimum needed
- [ ] No reference to slash commands
- [ ] Task scope clearly defined
- [ ] Behavior guidance via allowed-tools

---

## Recognition Questions

| Question | Answer Should Be... |
| :------- | :------------------ |
| Does agent use directory structure? | Yes, `.claude/agents/name/` |
| Does agent have frontmatter? | Yes, with name and description |
| Does allowed-tools exist? | Yes, restricted to minimum |
| Does agent reference /meta? | No, never references slash commands |
| Is task scope clear? | Yes, description defines scope |
| Is model specified? | Yes, for specialized tasks |

---

<critical_constraint>
**Portability:**

1. Agents MUST reference skills by name only, never by path
2. Agents never know about commands that trigger them
3. Agent logic must be self-documenting
4. Never use relative paths pointing outside the skill itself. When referencing other components, use: "invoke `skill-name`" or "invoke `skill-name` and read its file"

**Self-Contained:**

1. All agent configuration MUST be in frontmatter
2. No external dependencies for validation
3. Fork isolation (works in vacuum)

**Configuration:**

1. allowed-tools guides behavior (removes options from availability)
2. Hooks can enforce (block operations via exit codes)
3. Tools should be restricted to minimum needed
4. Model and temperature affect agent creativity
</critical_constraint>
