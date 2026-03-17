---
name: atlan-app-scaffold-standard
description: Scaffold new Atlan apps from CLI templates as the default behavior when users ask for a new app, then align files to sample-app standards.
---

# Atlan App Scaffold Standard

When a user asks to create a new app, treat CLI bootstrap as implicit. Do not require users to mention CLI commands.

## Workflow
1. Interpret user intent:
   - If request is "create/build/new app" (even without technical detail), trigger this skill first.
2. Resolve app path and slug from user request.
3. Ask clarifying questions when high-impact requirements are missing:
   - Ask 1-3 short questions for business behavior only (input source, expected output, critical constraints).
   - Do not ask users to specify CLI commands or low-level scaffolding details.
   - If unanswered, proceed with sane defaults and state the assumptions.
4. Choose quality tier before implementation:
   - default: `quickstart-utility`
   - use `connector-standard` when request requires connector behavior comparable to postgres/redshift patterns.
   - follow `../_shared/references/app-quality-bar.md`.
5. Run progressive discovery before coding (no repo-wide sweep):
   - `quickstart-utility`: read only skill references + one representative quickstart app (main/workflow/activity/pyproject + one e2e test), target <= 12 reads.
   - `connector-standard`: read skill references + one postgres-style and one redshift-style reference slice, target <= 20 reads.
   - Expand beyond budget only when blocked by missing facts.
   - Do not run recursive wildcard scans (for example full-tree `Search(\"**\")`) in first pass.
6. Enforce CLI-first bootstrap:
   - Check `atlan` availability (`command -v atlan`).
   - If available: use `atlan app init -o <app_path> -t generic -y` (or `-s <sample>` when requested).
   - If missing: invoke `atlan-cli-install-configure`, then continue scaffold.
   - Do not begin by searching for a local `atlan-cli` repository.
   - Re-verify with `command -v atlan && atlan --help`.
   - If network/install is blocked, stop and ask the user to enable installation or provide an existing CLI binary path.
7. Verify template/sample choices only when needed:
   - `atlan app template list`
   - `atlan app sample list`
8. After scaffold, apply mode-specific structure from `references/scaffold-matrix.md`:
   - `postgres-minimal` by default.
   - `redshift-custom` only when requirements demand custom auth/preflight/miner behavior.
9. If behavior-critical decisions are unclear, run `atlan-fact-verification-gate`.
10. Continue implementation on scaffolded project files; do not hand-create base tree.
11. Before declaring completion, hand off to `atlan-cli-run-test-loop` to run at least:
   - unit tests
   - e2e tests (or record a concrete infrastructure blocker)
   and summarize results.

## Hard Rules
- Do not manually create baseline app skeleton when CLI scaffold is available.
- Do not copy another quickstart folder as a substitute for scaffold.
- Keep SDK/CLI repositories read-only.
- Keep outputs portable; no machine-local absolute paths.

## References
- Scaffold matrix: `references/scaffold-matrix.md`
- Quality bar: `../_shared/references/app-quality-bar.md`
- Shared verification map: `../_shared/references/verification-sources.md`
- CLI install/config: `../atlan-cli-install-configure/SKILL.md`
