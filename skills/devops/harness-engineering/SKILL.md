---
name: harness-engineering-playbook
description: Implement OpenAI Harness Engineering practices in any repository — AGENTS.md, PLANS.md, deterministic smoke/test/lint harness commands, strict architecture boundaries, observability from day 1, and entropy-control audits for reliable autonomous agent runs.
---

# Harness Engineering Playbook

A skills.sh-compatible skill that operationalizes the practices from OpenAI's Harness Engineering guide. Use it to set up or refactor agent-first workflows so that autonomous runs are repeatable, observable, and safe.

## Install

```bash
npx skills add broomva/harness-engineering-skill --skill harness-engineering-playbook
```

## What It Does

- Bootstraps harness artifacts: `AGENTS.md`, `PLANS.md`, `docs/ARCHITECTURE.md`, `docs/OBSERVABILITY.md`, `Makefile.harness`, and CI workflows.
- Wraps deterministic commands behind `make smoke`, `make check`, `make ci` so agents can run them reliably.
- Enforces strict module boundaries and data-shape contracts.
- Wires structured observability (correlation IDs, key transitions) from day 1.
- Adds entropy-control audits and nightly harness checks to prevent docs drift and flaky scripts.

## Workflow

1. **Baseline** the target repo — detect language, toolchain, and existing CI.
2. **Bootstrap** harness artifacts from templates (interactive wizard or shell script).
3. **Apply** the nine Harness Engineering practices across repo artifacts.
4. **Validate** with `audit` — treat any `MISSING` or `FAIL` as blocking.
5. **Iterate** after real agent runs — patch gaps and re-audit.

## Quick Start

```bash
# Interactive wizard (recommended)
python3 .agents/skills/harness-engineering-playbook/scripts/harness_wizard.py init <repo-path> --profile control

# Shell fallback
./scripts/bootstrap_harness.sh <repo-path>

# Audit
python3 .agents/skills/harness-engineering-playbook/scripts/harness_wizard.py audit <repo-path>
```

## Profiles

| Profile    | Scope                                              |
|------------|----------------------------------------------------|
| `baseline` | Core harness artifacts only                        |
| `control`  | Baseline + control-system primitives               |
| `full`     | Control + entropy controls, nightly audit, CI      |

## Source

OpenAI Harness Engineering guide: <https://openai.com/index/harness-engineering/>

## License

MIT
