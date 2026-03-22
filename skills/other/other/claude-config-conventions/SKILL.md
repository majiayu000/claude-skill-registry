---
name: claude-config-conventions
description: "Conventions for Claude Code configuration files (agents, commands, rules, skills). Use when creating, reviewing, or modifying .claude/ configuration. Do NOT use for general application configuration (webpack, tsconfig, etc.) -- this is for Claude Code's own .claude/ directory only."
durability: encoded-preference
---

# Claude Config Conventions

## Architecture Layers

| Layer | Location | Loading | Purpose |
|-------|----------|---------|---------|
| Rules | `.claude/rules/` | Always loaded (main session only) | Lightweight principles, language-agnostic |
| Skills | `.claude/skills/` | Conditionally loaded by description match | Principles and patterns (WHAT) |
| Agents | `.claude/agents/` | Invoked explicitly | Workflow and process (HOW) |

## Content Placement Rules

- Skills define principles (WHAT). Agents define workflow (HOW). Never duplicate between them.
- Agents do NOT auto-inherit Rules or Skills -- declare skills in frontmatter (always-load) or in agent body with Skill tool (on-demand). See Skill Loading Strategy.
- Content needed in both main session and agents --> put in Skill (not Rule).
- When modifying an agent, check ALL skills it loads for consistency.

## Scope Purity

A skill's content must match the scope declared by its name and description.

When creating a new skill:
1. Can the principles be abstracted to be platform-independent?
   - **Yes** -- Generic-scoped SKILL.md (principles only) + platform-specific content in `references/` or dedicated skills
   - **No** -- Platform-scoped SKILL.md with specific content directly. Name must include the platform (e.g., `postgresql-patterns`, `react-patterns`)

Review checks:
- Generic-named skills must not contain platform-specific content
- Platform-named skills must not contain content for other platforms

**references/ vs dedicated skill decision:**
If the content is used independently without the parent skill -- dedicated skill. If always loaded together with the parent -- references/. When uncertain, start with references/ and promote to dedicated skill when independent usage emerges.

## Naming Conventions

**Agent naming: `{scope}-{role}`**
- `{scope}` matches the command's `{object}` keyword for discoverability
- `{role}` conveys the agent's persona (designer, planner, reviewer, etc.)
- Examples: `ux-planner`, `how-planner`, `adr-architect`, `build-fixer`, `code-reviewer`

**Command naming: `{verb}-{object}`**
- Verb-first for action clarity
- Examples: `/plan-ux`, `/plan-how`, `/fix-build`, `/code-review`

**Mapping rule: Agent `{scope}` = Command `{object}`**

| Command | Object | Agent(s) | Scope |
|---------|--------|----------|-------|
| `/plan-ux` | `ux` | `ux-planner`, `ux-critic`, `ux-optimizer`, `ux-synthesizer` | `ux` |
| `/plan-how` | `how` | `how-planner`, `how-critic`, `how-optimizer`, `how-synthesizer` | `how` |
| `/plan-claude-config` | `claude-config` | `claude-config-planner`, `-critic`, `-optimizer`, `-synthesizer` | `claude-config` |
| `/create-architecture-decision` | `architecture-decision` (long) | `adr-architect` | `adr` |
| `/fix-build` | `build` | `build-fixer` | `build` |
| `/code-review` | `code-review` | `code-reviewer` | `code` |

**Exact match exception**: When the command name is short and unambiguous, the agent can match exactly (e.g., `/commit` -> `commit` agent, `/push-to-remote` -> `push-to-remote` agent).

## Agent Conventions

**Frontmatter (required fields):**
- `name` -- kebab-case identifier
- `description` -- clear purpose and when to use
- `tools` -- list of required tools
- `skills` -- list skills the agent always needs (see Skill Loading Strategy). Optional if the agent needs no skills.

**`model:` field:**
- Optional. If omitted, inherits from caller.
- Plans must NOT specify model selection for agents they create -- model choice is the user's decision.
- **Exception -- Agent Team teammates**: Commands that define Agent Team teammates MAY specify `model:` to control cost. Teammates use standard Opus (not 1M context) since they process focused subtasks, while the main session uses Opus 1M for full project context. This is a cost optimization, not a quality downgrade.
- Do not downgrade to cheaper models (sonnet, haiku) without explicit user instruction.

**Content rules:**
- Agent = workflow/process (HOW). Never duplicate content from skills it loads.
- Do not include general knowledge Claude already knows (standard library usage, basic syntax, general concepts).
- Include a "When Invoked" section describing the execution flow. For Agent Team teammates, "Teammate Protocol" is an accepted alternative that describes the agent's role in the team debate workflow.
- Include output format specification if the agent produces structured output.

## Skill Loading Strategy

Subagent skills in `skills:` frontmatter are fully preloaded at startup -- there is no conditional loading by description match. Use this decision framework:

| Category | Where to declare | When |
|----------|-----------------|------|
| **Always-load** | `skills:` frontmatter | Skills the agent needs on every invocation regardless of task |
| **On-demand** | Agent body text + `Skill` tool | Domain-specific skills needed only when the task involves that domain |

Always-load examples: `review-severity-format` (every review needs it), `pcos-debate` (every PCOS teammate needs it), `ears-format` (how-planner always writes EARS)

On-demand examples: `postgresql-patterns` (only when task involves PostgreSQL), `cicd-patterns` (only when task involves CI/CD)

To enable on-demand loading, add `Skill` to the agent's `tools:` list and include invocation guidance in the agent body:

```
## On-Demand Skills

Load these skills when the task involves their domain:
- `/database-patterns` -- database schema or query design
- `/cicd-patterns` -- CI/CD pipeline configuration
```

**Reliability trade-off**: On-demand loading depends on the agent's judgment to invoke the skill. Use always-load for skills whose absence causes incorrect output (e.g., review-severity-format for reviewers). Use on-demand for domain-specific skills whose absence degrades quality but does not cause wrong behavior.

Review check: if a skill in `skills:` frontmatter is only relevant to a subset of the agent's tasks, consider moving it to on-demand loading.

## Command Conventions

**Frontmatter (required fields):**
- `description` -- concise, starts with a verb (used for matching/triggering)

**Content rules:**
- Body is expanded in the main session context (not inside a subagent).
- Delegate to a subagent for actual work, UNLESS:
  - Interactive: requires back-and-forth dialogue with the user during execution (e.g., `/investigate`)
  - Trivial: a few simple operations where subagent overhead exceeds the work itself (e.g., `/verify`)
- Include a "Next Commands" section when the command has natural follow-up steps in a workflow.
- Include a "Prerequisites" section if the command requires prior state.

## Rule Conventions

- Always loaded in main session only (not in agents).
- Lightweight principles, language-agnostic.
- Content needed in both main session and agents --> put in a Skill instead of a Rule.

## Agent Responsibility Boundaries

Reviewers have non-overlapping responsibilities:

| Agent | Scope |
|-------|-------|
| `code-reviewer` | Code quality: integrity, readability, comments, best practices |
| `security-reviewer` | All security and OWASP concerns |
| `performance-reviewer` | Algorithmic complexity, memory, rendering, bundle size, caching, network optimization |
| `sre-reviewer` | Observability, resilience, health checks, resource limits, blast radius, incident readiness |
| `database-reviewer` | SQL queries, ORM usage, schema design |
| `dead-code-reviewer` | Unused code, imports, dependencies |
| `claude-config-reviewer` | Claude Code configuration quality and consistency |
| `test-quality-reviewer` | Test coverage analysis, uncovered paths, test-to-code ratio |
| `accessibility-reviewer` | WCAG 2.2 compliance, ARIA correctness, keyboard navigation, screen reader compatibility |

## Reviewer Integration Checklist

When a new reviewer agent is added to the `/code-review` pipeline, ALL of the following must be updated:

- Agent file created in `.claude/agents/` with boundary definitions
- Skill file created in `.claude/skills/` (if the reviewer needs domain-specific patterns)
- `/code-review` command: reviewer table, reviewer count, issue ID prefix
- `review-severity-format` skill: issue ID prefix added
- `claude-config-conventions` skill: Agent Responsibility Boundaries table updated
- `CLAUDE.md`: reviewer count and any workflow descriptions updated

## PCOS Agent Team Pattern

The PCOS (Planner-Critic-Optimizer-Synthesizer) pattern uses Agent Teams for structured debate before implementation.

**Four roles:**

| Role | Hat | Responsibility |
|------|-----|---------------|
| Planner | Blue/White | Drafts the plan based on analysis of existing files |
| Critic | Black | Finds problems -- missing edge cases, anti-patterns, conflicts |
| Optimizer | Green | Proposes improvements and breaks deadlocks between Planner and Critic |
| Synthesizer | -- | Converges debate into final plan with Critique Log |

**When to use PCOS:**
- Configuration changes that affect multiple interconnected files (agents, skills, commands)
- Changes where trade-offs need structured evaluation (e.g., architecture layer decisions)
- NOT for trivial single-file edits or mechanical updates

**PCOS-enabled commands:**

| Command | Team | Domain |
|---------|------|--------|
| `/plan-ux` | ux-planner, ux-critic, ux-optimizer, ux-synthesizer | UX plans (user stories, Gherkin) |
| `/plan-how` | how-planner, how-critic, how-optimizer, how-synthesizer | Implementation plans (EARS, ADR) |
| `/plan-claude-config` | claude-config-planner, -critic, -optimizer, -synthesizer | Config changes (.claude/) |

All PCOS-enabled commands include a complexity gate: simple requests bypass the team debate and delegate to the Planner agent directly.

**Debate flow:**
1. Planner drafts plan and shares with Critic and Optimizer
2. Critic sends challenges, then Optimizer sends proposals incorporating Critic's input (both to Planner)
3. Planner accepts/rejects/defers each item, sends revised version to Critic, Optimizer, AND Synthesizer
4. Critic and Optimizer send final assessments to Synthesizer
5. Synthesizer converges debate, writes output files, and sends Critique Log to team lead
6. Team lead presents plan to user

**Pre-implementation vs post-implementation review:**
- **PCOS Critic** (pre-implementation): Reviews the *plan* during PCOS debate, before any files are created or modified. Catches architectural issues early. Exists in all PCOS teams (ux-critic, how-critic, claude-config-critic).
- **Post-implementation reviewer** (post-implementation): Reviews *implemented file changes* after the plan has been executed. Catches issues that only appear in actual file content (e.g., config-reviewer for config changes, code-reviewer for code changes).

These are different stages with different inputs -- no responsibility overlap.

## Subagent Constraints

- Subagents return text results only -- no structured data (task IDs, etc.)
- Subagents must NOT use TaskCreate -- task creation is the main session's responsibility. Subagents that use TaskCreate pollute the task list with intermediate work items
- If a command needs tasks created from subagent results, specify this in the command body (e.g., "After the subagent returns, create TaskCreate entries for each action item")
- Subagents cannot spawn other subagents (no nested Task tool usage)

## No Personal or Company Information in Git

This repository is a public dotfiles repo. Git-tracked files must NEVER contain:
- Real names (use `[user]` placeholder or store in `memory/` which is git-ignored)
- Company names, workspace URLs, or internal channel names
- Email addresses, Slack user IDs, or employee identifiers
- API tokens, OAuth secrets, or credentials

Personal/company-specific values go in `memory/` (e.g., `memory/slack-profile.md`) or `settings.local.json`.

## Anti-Patterns

- Putting workflow steps in a skill (belongs in agent)
- Putting shared principles in an agent (belongs in skill)
- Putting agent-needed content in a rule (rules are main-session only)
- Duplicating content between a skill and the agents that load it
- Downgrading model (sonnet, haiku) in plans or agent definitions without user instruction (Agent Team teammate model selection is allowed -- see model field rules)
- Omitting skills entirely (neither frontmatter nor on-demand) when the agent's responsibilities require them
- Commands doing substantial work directly instead of delegating to a subagent
- Giving subagents TaskCreate/TaskUpdate tools -- causes intermediate task pollution
- Hardcoding personal names, company names, or usernames in git-tracked config files
