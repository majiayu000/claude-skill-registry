---
name: agent-builder
type: standard
depth: base
description: >-
  Creates Claude Code agent files (.claude/agents/*.md) with YAML frontmatter, tool
  permissions, and system prompts. Use when building new agents, configuring agent
  frontmatter, writing agent system prompts, or setting agent tool permissions.
---

# [H1][AGENT-BUILDER]
>**Dictum:** *Structured frontmatter and scoped tools enable discoverable agents.*

<br>

Specialized execution contexts for Claude Code subagent delegation. Frontmatter controls discovery and capabilities; markdown body encodes behavior.

**Location:** `.claude/agents/` (project) or `~/.claude/agents/` (user). Higher priority wins: CLI flag > project > user > plugin.

**Tasks:**
1. Read [index.md](./index.md) — Reference file listing for navigation.
2. Read [frontmatter.md](./references/frontmatter.md) — Complete schema (11 fields), triggers, syntax.
3. Read [prompt.md](./references/prompt.md) — Structure patterns, constraint markers.
4. Read [workflow.md](./references/workflow.md) — 5-phase creation process.
5. (prose) Load `style-standards` skill — Voice, formatting, constraints.
6. Execute per workflow — UNDERSTAND, ACQUIRE, RESEARCH, AUTHOR, VALIDATE.
7. Validate — Quality gate; see §VALIDATION.

**Templates:** [→agent.template.md](./templates/agent.template.md) — Standard agent scaffold.

[REFERENCE]: [index.md](./index.md) — Complete reference file listing.

---
## [1][FRONTMATTER]
>**Dictum:** *Metadata enables discovery before load.*

<br>

```yaml
---
name: agent-name
description: >-
  Capability statement. Use when scenario-1, scenario-2, or scenario-3.
tools: Read, Glob, Grep
model: sonnet
skills:
  - style-standards
memory: user
---
```

| [INDEX] | [FIELD]           | [TYPE] | [REQ] | [CONSTRAINT]                                                                 |
| :-----: | ----------------- | ------ | :---: | ---------------------------------------------------------------------------- |
|   [1]   | `name`            | string |  Yes  | Kebab-case, max 64 chars, match filename                                     |
|   [2]   | `description`     | string |  Yes  | Third person, active voice, "Use when" clause                                |
|   [3]   | `tools`           | list   |  No   | Comma-separated allowlist; omit = inherit all                                |
|   [4]   | `disallowedTools` | list   |  No   | Denylist; removed from inherited/allowed tools                               |
|   [5]   | `model`           | enum   |  No   | `haiku`, `sonnet`, `opus`, `inherit`                                         |
|   [6]   | `permissionMode`  | enum   |  No   | `default`, `acceptEdits`, `delegate`, `dontAsk`, `bypassPermissions`, `plan` |
|   [7]   | `maxTurns`        | number |  No   | Maximum agentic turns before subagent stops                                  |
|   [8]   | `skills`          | list   |  No   | Full skill content preloaded at startup                                      |
|   [9]   | `mcpServers`      | object |  No   | MCP servers available to this subagent                                       |
|  [10]   | `hooks`           | object |  No   | Scoped lifecycle hooks (all 14 events supported)                             |
|  [11]   | `memory`          | enum   |  No   | `user`, `project`, or `local` persistent scope                               |


[IMPORTANT] Agent background color set interactively via `/agents` UI — not frontmatter field.

---
## [2][DISCOVERY]
>**Dictum:** *Description quality determines invocation accuracy.*

<br>

Reasoning matches description directly — no embeddings, no keyword matching.

| [INDEX] | [PATTERN]           | [EXAMPLE]                            | [MECHANISM]                |
| :-----: | ------------------- | ------------------------------------ | -------------------------- |
|   [1]   | "Use when" clause   | `Use when building MCP servers`      | Direct activation signal   |
|   [2]   | Proactive trigger   | `Use proactively after code changes` | Encourages auto-invocation |
|   [3]   | Imperative emphasis | `MUST BE USED before committing`     | Strong delegation signal   |
|   [4]   | Enumerated list     | `(1) creating, (2) modifying`        | Parallel pattern matching  |
|   [5]   | Technology embed    | `Python (FastMCP) or TypeScript`     | Framework-specific match   |

[CRITICAL]:
- [NEVER] Hedging words: `might`, `could`, `should`, `probably`.
- [ALWAYS] Include "Use when" clause — 3+ trigger scenarios.
- [ALWAYS] Third person, active voice, present tense.

---
## [3][TOOLS]
>**Dictum:** *Tool declarations scope permissions.*

<br>

| [INDEX] | [PATTERN]     | [TOOLS]                          | [USE_CASE]         |
| :-----: | ------------- | -------------------------------- | ------------------ |
|   [1]   | Read-only     | `Read, Glob, Grep`               | Analysis, review   |
|   [2]   | Write-capable | `Read, Edit, Write, Glob, Bash`  | Implementation     |
|   [3]   | Orchestration | `Task(worker, researcher), Read` | Agent dispatch     |
|   [4]   | Full access   | *(omit field)*                   | Inherits all tools |

**Task restriction:** `Task(agent_type)` limits spawnable subagent types (main thread only).
**Denylist:** `disallowedTools: Write, Edit` removes tools from inherited or allowed set.

---
## [4][MODELS]
>**Dictum:** *Model selection balances capability against latency and cost.*

<br>

| [INDEX] | [MODEL] | [STRENGTH]              | [LATENCY] | [COST]  |
| :-----: | ------- | ----------------------- | :-------: | :-----: |
|   [1]   | opus    | Complex reasoning       |   High    |  High   |
|   [2]   | sonnet  | Balanced performance    |  Medium   | Medium  |
|   [3]   | haiku   | Fast, simple tasks      |    Low    |   Low   |
|   [4]   | inherit | Match main conversation |  Session  | Session |

---
## [5][SYSTEM_PROMPT]
>**Dictum:** *Structured prompts constrain execution.*

<br>

Markdown body follows frontmatter. Body encodes agent behavior; structure determines effectiveness. Subagents receive only this system prompt (plus environment details), NOT full Claude Code system prompt.

---
## [6][NAMING]
>**Dictum:** *Naming conventions enable discovery.*

<br>

| [INDEX] | [PATTERN]       | [EXAMPLE]            | [USE_CASE]            |
| :-----: | --------------- | -------------------- | --------------------- |
|   [1]   | Role-based      | `code-reviewer`      | Specialized function  |
|   [2]   | Action-based    | `generating-commits` | Gerund form preferred |
|   [3]   | Domain-specific | `react-specialist`   | Technology expertise  |

[CRITICAL]:
- [NEVER] Generic names: `helper`, `processor`, `agent`.
- [ALWAYS] Kebab-case — lowercase, hyphens only. Filename matches `name` field.

---
## [7][VALIDATION]
>**Dictum:** *Validation gates prevent incomplete artifacts.*

<br>

[VERIFY] Completion:
- [ ] Workflow: All 5 phases executed (UNDERSTAND → VALIDATE).
- [ ] Frontmatter: Valid YAML, description with "Use when" clause.
- [ ] Tools: Matches type gate (readonly|write|orchestrator|full).
- [ ] Prompt: Role line + H2 sections + constraint markers.
- [ ] Quality: Kebab-case naming, filename matches `name` field.

[REFERENCE] Operational checklist: [→validation.md](./references/validation.md).
