---
name: coding-guidelines-gen
description: Generate nested AGENTS.md coding guidelines per module (monorepo-aware), detect languages/tooling, ask architecture preferences, and set up missing formatters/linters (Spotless for JVM). Use when the user wants module-scoped AGENTS.md coding guidelines or to set up missing formatters/linters.
---

# Coding guidelines generator

## Goal
Create **nested** `AGENTS.md` files (not repo root) that define:
- architecture preferences + boundaries (high level)
- formatting/lint/testing commands (runnable)
- a small **verifiable** config block the verifier skill can execute

## Minimal questions to ask (don’t skip)
- Where are the module roots? (Confirm the folders that should each get an `AGENTS.md`; avoid repo root unless explicitly requested.)
- Architecture style: layered / hex / clean (pick one) and any hard boundaries (e.g., `domain/` must not import `infra/`).
- OK to add tooling when missing? (default: yes; Spotless for Java/Kotlin)
- Default commands: format / lint / test for each module (changed-files-first where practical).

## Workflow (monorepo-aware)
1) Scan for candidate modules and languages.
   - Use `scripts/scan_modules.py` to produce a quick inventory.
   - If `python` is not available or the script fails, tell the user and ask whether to install Python or proceed with a manual module scan.
2) Propose the **nested** `AGENTS.md` placement(s) and get confirmation.
   - If the only detected module is repo root, suggest a subdir (e.g., `src/`, `apps/<name>/`, `packages/<name>/`) or ask the user where the code “starts”.
3) For each confirmed module root:
   - Create/update `<module>/AGENTS.md` using `references/agents-template.md`.
   - Fill the `codex-guidelines` JSON block (schema: `references/verifiable-block.md`) with runnable commands.
4) Ensure formatting + linting exist (prefer existing; otherwise add best-practice defaults).
   - JVM (Gradle/Maven): add/configure Spotless (see `references/spotless.md`).
   - Others: pick a minimal, common default and wire commands into `AGENTS.md` (see `references/language-defaults.md`).

## Deliverable
Provide:
- The list of module roots covered and each `AGENTS.md` created/updated.
- The `codex-guidelines` command block per module (format/lint/test).
- Any tooling/config changes added (e.g., Spotless) and where they live.
