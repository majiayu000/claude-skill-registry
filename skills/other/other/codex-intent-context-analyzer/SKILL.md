---
name: codex-intent-context-analyzer
description: Analyze code-change prompts into structured intent JSON with goal, constraints, missing info, normalized prompt, complexity, and confirmation gating. Use before implementation for build, fix, debug, review, and docs tasks.
load_priority: always
---

## TL;DR
Parse user request into structured intent JSON (goal, constraints, complexity). Trigger Socratic Gate for complex/ambiguous scope. Wait for explicit confirmation before implementation. For large repos: read index files first, max 20 files deep-read per task.

# Intent and Context Analyzer

## Activation

1. Activate for any request that implies code or documentation changes.
2. Skip for purely informational questions with no requested edits.

## Output Contract

Always return a fenced JSON block in conversation:

```json
{
  "intent": "build | fix | review | debug | docs | refactor | deploy | handoff | other",
  "goal": "One-sentence description",
  "pain_points": ["Problems extracted from the prompt"],
  "constraints": ["Technical or business constraints"],
  "missing_info": ["Information needed but not provided"],
  "normalized_prompt": "Clean rewrite of the user request",
  "complexity": "simple | complex",
  "needs_confirmation": true
}
```

## Socratic Gate

Trigger Socratic Gate for `complexity: complex` or ambiguous scope.

### Trigger Conditions

- Build/create requests with vague requirements.
- Multi-file or architecture-level work.
- Requests with missing constraints or success criteria.
- "Just do it" requests with unclear scope.

### Mandatory Questions

Ask at least 3 questions covering:

1. Purpose: what problem is being solved.
2. Users: who is affected.
3. Scope: must-have vs nice-to-have.

### Question Quality Rules

- Generate questions dynamically for this task (do not reuse static boilerplate).
- Tie each question to an implementation decision.
- Present trade-offs and a default assumption.

Format:

- Question: ...
- Why it matters: ...
- Options: A vs B ...
- Default if unspecified: ...

### Special Cases

- If user already gave stack/tooling, ask edge-case and trade-off questions.
- If user says "just do it", still ask 2 short boundary questions.

## Confirmation Rule

- Keep `needs_confirmation` true by default.
- Present analysis first and wait for explicit confirmation.
- Do not start implementation until confirmed.

## Fallback

If `intent` is `other`, ask user to rephrase or choose one of:
`build`, `fix`, `review`, `debug`, `docs`, `refactor`, `deploy`, `handoff`.

## Script Invocation Discipline

1. When this workflow calls helper scripts from other skills, run `--help` first.
2. Treat helper scripts as black-box tools and execute by contract before reading source.
3. Read script source only when customization or bug-fixing is required.

## Repo Comprehension Protocol

For repositories with more than 50 files:

1. Read index files first: `ARCHITECTURE.md`, `CODEBASE.md`, `README.md`.
2. Build a lightweight map:
   - top-level directories (depth <= 2)
   - likely entry points (`main`, `index`, `app`, `server`)
   - config files (`package.json`, `tsconfig.json`, `pyproject.toml`, etc.)
3. Load by scope, not globally:
   - fix: target module + related tests/docs
   - build: target area + nearby tests/docs
4. Use progressive disclosure:
   - outline first (exports/functions/classes)
   - deep-read only directly relevant files
5. Deep-read budget: max 20 files per task unless user approves expansion.
6. If uncertain scope, ask user before broad exploration.
