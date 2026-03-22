---
name: harness-engineering-playbook
description: Implement OpenAI Harness Engineering practices in any repository. Use when setting up or refactoring agent-first workflows, writing or upgrading AGENTS.md and PLANS.md, creating deterministic smoke/test/lint/typecheck harness commands, defining strict architecture boundaries and data-shape contracts, wiring observability from day 1, and adding entropy-control checks plus CI automation for reliable autonomous runs.
---

# Harness Engineering Playbook

Use this skill to operationalize the practices from OpenAI's Harness Engineering guide in a repo that agents can run against repeatedly and safely.

## What To Load

- Use `references/openai-harness-practices.md` for the full practice-to-artifact mapping.
- Use `references/rollout-checklist.md` for phased adoption in active repos.
- Use `references/wizard-cli.md` for Typer wizard command flows.
- Use `assets/templates/` when creating or updating harness files.

## Inputs

- Target repository path.
- Existing command surface (`make`, `npm`, `cargo`, `pytest`, etc.).
- Existing CI workflows and branch protections.

## Workflow

1. Baseline the repo and detect existing workflows.
2. Bootstrap harness artifacts and templates.
3. Apply all nine Harness Engineering practices.
4. Run harness audit checks and repair gaps.
5. Iterate after real agent runs.

## Step 1: Baseline The Repo

- Identify language/toolchain and canonical entrypoints.
- Inventory existing checks, scripts, and CI jobs.
- Record current pain points for agent runs: setup drift, unclear docs, flaky tests, missing trace IDs, slow loops.

Use a short baseline note inside `PLANS.md` so decisions remain durable.

## Step 2: Bootstrap Harness Artifacts

Preferred entrypoint:

```bash
python3 scripts/harness_wizard.py init <repo-path> --profile control
```

Profiles:

- `baseline`: only core harness artifacts.
- `control`: baseline + control-system primitives.
- `full`: control + entropy controls (nightly audit + entropy checks).

Direct shell fallback:

Run:

```bash
./scripts/bootstrap_harness.sh <repo-path>
```

This script installs safe defaults from `assets/templates/`:

- `AGENTS.md`
- `PLANS.md`
- `docs/ARCHITECTURE.md`
- `docs/OBSERVABILITY.md`
- `Makefile.harness` (+ `-include Makefile.harness` in `Makefile`)
- `scripts/audit_harness.sh`
- `scripts/harness/{smoke,test,lint,typecheck}.sh`
- `.github/workflows/harness.yml`

By default, existing files are not overwritten. Pass `--force` to replace template-managed files.

## Step 3: Apply The Nine Practices

Implement each practice directly in repo artifacts.

### 1. Make Easy To Do Hard Thing

- Ensure hard, high-value tasks are one command away (`make smoke`, `make check`, `make ci`).
- Keep setup and cleanup scripted.
- Make smoke checks cheap enough for frequent use.

### 2. Communicate Actionable Constraints With Compact Docs

- Keep `AGENTS.md` short, concrete, and command-first.
- Document non-obvious constraints and guardrails.
- Keep docs close to code and update with behavior changes.

### 3. Structure Codebase With Strict Boundaries And Flow

- Define module boundaries in `docs/ARCHITECTURE.md`.
- Parse and validate data at boundaries; use typed contracts for internal flow.
- Prefer one abstraction per module and one clear ownership path.

### 4. Build Observability In From Day 1

- Emit structured logs/events with correlation IDs.
- Capture key transitions in long-running workflows.
- Define minimum observable fields in `docs/OBSERVABILITY.md`.

### 5. Optimize For Agent Flow, Not Human Flow

- Treat context as a first-class system dependency.
- Use `PLANS.md` for multi-step/multi-hour tasks.
- Front-load durable context (scope, constraints, checkpoints) so restarts stay cheap.

### 6. Bring Your Own Harness

- Standardize repo-local wrappers (`Makefile.harness`, `scripts/harness/`).
- Wrap local infra actions in deterministic scripts.
- Make agent behavior reproducible across machines and runs.

### 7. Prototype In Natural Language First

- Draft logic and tests in prose before coding.
- Review edge cases in prose and lock acceptance criteria.
- Translate approved prose into code and tests.

### 8. Invest In Static Analysis And Linting

- Pin formatter/linter/typechecker versions where practical.
- Enforce checks in both local workflow and CI.
- Run static checks before long tests to shorten failure loops.

### 9. Manage Entropy

- Add periodic audits for docs drift, flaky checks, and dead scripts.
- Keep templates synchronized with real workflows.
- Remove stale abstractions quickly to keep agent context clean.

For a detailed artifact matrix, load `references/openai-harness-practices.md`.

## Step 4: Validate

Run:

```bash
python3 scripts/harness_wizard.py audit <repo-path>
```

Treat any `MISSING` or `FAIL` result as blocking before calling harness setup complete.

## Step 5: Iterate On Real Runs

- Observe one full agent run from clean checkout to merged change.
- Patch harness gaps immediately.
- Re-run audit.
- Keep `AGENTS.md`, `PLANS.md`, and architecture docs aligned with current behavior.

## Adaptation Rules

- Preserve existing project conventions and replace templates incrementally.
- Do not overwrite user-authored files without explicit approval.
- Keep command names stable; change internals behind wrappers.
- Favor deterministic, scriptable workflows over ad-hoc interactive steps.
