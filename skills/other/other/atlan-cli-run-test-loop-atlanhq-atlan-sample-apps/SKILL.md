---
name: atlan-cli-run-test-loop
description: Run Atlan app execution loops using CLI-first commands with automatic CLI availability checks and safe fallbacks.
---

# Atlan CLI Run Test Loop

Execute run/test/fix loops that a developer would expect from a normal app request.

## Workflow
1. Resolve target app path.
2. Verify CLI availability first:
   - Check `command -v atlan`.
   - If missing, invoke `atlan-cli-install-configure` before run/test.
   - Do not begin by searching for a local `atlan-cli` repository.
   - Re-verify with `command -v atlan && atlan --help`.
   - If network/install is blocked, stop and ask the user to enable installation or provide an existing CLI binary path.
3. Verify infra prerequisites before run/e2e:
   - `uv`, `temporal`, `dapr` are available.
   - Dapr runtime initialization is present (config path exists and sidecar can start).
   - If missing, run `atlan app init tools` first; if issue persists, apply manual Dapr recovery and record it.
4. Use CLI-first commands:
   - `atlan app run -p <app_path>`
   - `atlan app test -p <app_path> -t unit`
   - `atlan app test -p <app_path> -t e2e`
5. Use fallback commands only when CLI path is unavailable or mismatched:
   - `uv run poe start-deps`
   - `uv run main.py`
   - `uv run pytest`
6. Record each cycle in `loop_report.md` using `../_shared/assets/loop_report.md`.
7. If command behavior is unclear or conflicting, verify against CLI docs/code and run `atlan-fact-verification-gate`.
8. If a CLI mismatch appears, append proposal to `../_shared/references/cli-change-proposals.md`.

## Loop Contract
- Capture commands, failures, root cause, patch plan, and rerun result.
- Prefer deterministic command sequences and explicit paths.
- Treat `ATLAN-CLI-APP-0012` / dependency startup failures as infra blockers; collect logs and apply the run-matrix recovery steps.
- Do not imply or perform CLI repo edits.

## References
- Run matrix: `references/run-matrix.md`
- CLI proposal log: `../_shared/references/cli-change-proposals.md`
- CLI install/config: `../atlan-cli-install-configure/SKILL.md`
