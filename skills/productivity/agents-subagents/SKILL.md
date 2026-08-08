---
name: agents-subagents
description: Create AI coding agent subagents with YAML frontmatter and least-privilege tools. Use when designing delegation, tool selection, or safety rules.
---

# Claude Code Agents

Create and maintain Claude Code agents/subagents with predictable behavior, least-privilege tools, and explicit delegation contracts.

## Quick Start

1. Create an agent file at `.claude/agents/<agent-name>.md` (kebab-case filename).
2. Add YAML frontmatter (required: `name`, `description`; optional: `tools`, `model`, `permissionMode`, `skills`, `hooks`).
3. Write the agent prompt: responsibilities, workflow, and an output contract.
4. Minimize tools: start read-only, then add only what the agent truly needs.
5. Test on a real task and iterate.

Minimal template:

```markdown
---
name: sql-optimizer
description: Optimize SQL queries, explain tradeoffs, and propose safe indexes
tools: Read, Grep, Glob
model: sonnet
---

# SQL Optimizer

## Responsibilities
- Diagnose bottlenecks using query shape and plans when available
- Propose optimizations with risks and expected impact

## Workflow
1. Identify the slow path and data volume assumptions
2. Propose changes (query rewrite, indexes, stats) with rationale
3. Provide a verification plan

## Output Contract
- Summary (1–3 bullets)
- Recommendations (ordered)
- Verification (commands/tests to run)
```

## Workflow (2026)

1. Define the agent’s scope and success criteria.
2. Choose a model based on risk, latency, and cost (default to `sonnet` for most work).
3. Choose tools via least privilege; avoid granting `Edit`/`Write` unless required.
4. If delegating with `Task`, define a handoff contract (inputs, constraints, output format).
5. Add safety rails for destructive actions and secrets.
6. Add a verification step (checklist, tests, or a dedicated verifier agent).

## Frontmatter Fields (Summary)

- `name` (REQUIRED): kebab-case; match filename (without `.md`).
- `description` (REQUIRED): state when to invoke + what it does; include keywords users will say.
- `tools` (OPTIONAL): explicit allow-list; prefer small, purpose-built sets.
- `model` (OPTIONAL): `haiku` for fast checks, `sonnet` for most tasks, `opus` for high-stakes reasoning, `inherit` to match parent.
- `permissionMode` (OPTIONAL): prefer defaults; change only with a clear reason and understand the tradeoffs.
- `skills` (OPTIONAL): preload skill packs for domain expertise; keep the list minimal.
- `hooks` (OPTIONAL): automate guardrails; prefer using the hooks skill for patterns and safety.

For full tool semantics and permission patterns, use `references/agent-tools.md`. For orchestration and anti-patterns, use `references/agent-patterns.md`.

## 2026 Best Practices (Domain Expertise)

- Use small, specialized agents; avoid “god agents”.
- Keep agent prompts short; put repo conventions in `CLAUDE.md`/project memory and domain knowledge in skills.
- Budget context: pass file paths, minimal snippets, and constraints; avoid dumping long logs/code.
- Use explicit handoffs for subagents: “Goal / Constraints / Inputs / Output Contract”.
- Add a verifier step for risky changes (security, migrations, infra, auth).
- Treat CLI fields/features as moving; verify against official docs in `data/sources.json`.

## Validation Checklist

- Frontmatter: `name` matches filename; `description` is single-line and trigger-oriented; tools are minimal; model fits risk.
- Prompt: responsibilities are concrete; workflow is actionable; output contract is explicit.
- Delegation: subagent briefs are specific and bounded; orchestrator verifies integration.
- Safety: confirm destructive ops; avoid secrets/PII; follow repository policies.

## Navigation

- `frameworks/shared-skills/skills/agents-subagents/references/agent-patterns.md`
- `frameworks/shared-skills/skills/agents-subagents/references/agent-tools.md`
- `frameworks/shared-skills/skills/agents-subagents/references/subagent-interruption-recovery.md`
- `frameworks/shared-skills/skills/agents-subagents/data/sources.json`
- `frameworks/shared-skills/skills/agents-skills/SKILL.md`
- `frameworks/shared-skills/skills/agents-hooks/SKILL.md`

## Subagent Interruption Recovery Protocol

Interruptions are normal in multi-agent runs. Treat them as recoverable state transitions, not total failures.

### Recovery Loop

1. Capture partial output from interrupted agent.
2. Classify interruption cause (`manual redirect`, `timeout`, `context overflow`, `tool error`).
3. Decide resume strategy:
   - resume same agent with narrowed scope, or
   - spawn replacement agent with explicit handoff from checkpoint.
4. Prevent duplicate work by marking completed subtasks before rerun.
5. Re-verify integration assumptions after recovery.

### Required Checkpoint Fields

- completed work
- pending work
- owned files
- unresolved blocker
- next exact command/task

### Anti-Pattern

Do not restart full fan-out blindly after one interruption. Resume the smallest affected unit first.

## Operational Guardrails: Subagent Orchestration

Use these defaults unless the user explicitly asks for wider fan-out.

### Worktree Isolation

For parallel subagent execution, use one Git worktree per agent to prevent file conflicts and index lock contention. See **[AI Agent Worktrees](../dev-git-workflow/references/ai-agent-worktrees.md)** for setup, directory conventions, safety patterns, and cleanup.

### Hard Limits

- Keep active subagents <= 3.
- Keep each subagent scope to one responsibility and a bounded file set.
- Do not let multiple subagents edit the same file in parallel.
- Use one worktree per subagent when running parallel agents locally.

### Handoff Template (Standard)

```text
Goal:
Constraints:
Owned files:
Do-not-touch files:
Output format:
Definition of done:
```

### Context-Rich Handoff Template (For Parallel/Swarm Execution)

When dispatching multiple subagents from a plan, front-load each agent with structured context. This reduces token usage, tool calls, and drift.

```text
## Context
- Plan: [plan filename or path]
- Goals: [relevant overview from plan — what this task achieves]
- Dependencies: [prerequisite tasks + their outputs/files]
- Related tasks: [sibling tasks and their function]

## Scope
- Files to create/modify: [full paths]
- Files to read (not modify): [paths for reference only]
- Do-not-touch: [files owned by other agents]

## Acceptance Criteria
- [Criterion 1]
- [Criterion 2]
- [Test/verification command]

## Implementation Steps
1. Read the plan at [path] for full context
2. [Concrete step]
3. [Concrete step]
4. Verify: [specific check]
```

**Why this works:** Subagents have no prior context. Without front-loaded detail, they spend tokens rediscovering the codebase. With it, they execute focused work immediately.

### Wave Dispatch Protocol

When executing plans with dependency graphs, use waves:

1. Read the dependency graph from the plan.
2. Identify all tasks with no unmet dependencies (Wave 1).
3. Launch one subagent per unblocked task (using context-rich handoff template).
4. Wait for all agents in the wave to complete.
5. Validate each agent's output before proceeding.
6. Identify newly unblocked tasks → launch next wave.
7. Repeat until all tasks complete.

**Single-wave shortcut:** If only one task is unblocked, launch one agent. Don't force parallelism.

### Merge Discipline

1. Wait for subagent outputs.
2. Review for overlap/conflicts.
3. Integrate one subagent result at a time.
4. Run verification gates before final synthesis.

### Conflict Resolution (Parallel Outputs)

When parallel agents produce conflicting changes:

1. **Detect**: Check for overlapping file edits, incompatible interface changes, or divergent assumptions.
2. **Prioritize**: The agent working on the dependency (upstream task) takes priority for shared interfaces.
3. **Resolve**: The orchestrator (not subagents) reconciles conflicts — it has the full plan context.
4. **Re-run if needed**: If conflict resolution invalidates a task's output, re-dispatch that single task with updated context.
5. **Document**: Record the conflict and resolution in the plan for traceability.

### Stop Conditions

Stop and re-plan when:
- two subagents propose conflicting edits to same module,
- repeated retries happen without new evidence,
- context window starts dropping prior decisions,
- conflict resolution would require re-running more than half the completed tasks.

## Fact-Checking

- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.
