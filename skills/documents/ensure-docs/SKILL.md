---
name: ensure-docs
description: Verify documentation coverage and generate missing docs interactively
disable-model-invocation: true
---

# Ensure Documentation Coverage

Verify documentation coverage across a codebase, report gaps, and generate missing docs. **If the agent supports subagents**, dispatch one verifier per detected language in parallel; **otherwise** run the same per-language verification sequentially — the output is identical either way.

## Workflow

Complete steps in order. Do not advance until each step’s **Pass** is satisfied.

1. **Language detection** — Follow Phase 1 (language detection) in [`references/workflow.md`](references/workflow.md).
   - **Pass:** For each language you will verify, you have evidence of at least one matching source file (counts or command output); if none qualify, stop with a short “no applicable languages” message and do not run verifiers.

2. **Load standards** — Read the sections for your detected languages (language standards, verifier prompts, consolidation format) in the same reference file.
   - **Pass:** You can state which standard applies per language (e.g. Google docstrings, JSDoc, GoDoc) before verification begins.

3. **Verification** — Verify each qualifying language using the verifier prompts and JSON output shape in the reference (Phase 2). If the agent supports subagents, run one verifier per language in parallel; otherwise run them sequentially.
   - **Pass:** Each completed verification returns parseable JSON including `language`, `files_scanned`, and `findings` (array, possibly empty).

4. **Consolidated report** — Merge results per Phase 3 (summary table, severity grouping, detailed findings if requested).
   - **Pass:** The user sees the merged report (inline or written to an agreed path) before you claim the audit is done or propose fixes.

5. **Generation** — Only if `--report-only` is not set: offer choices per Phase 4; apply doc edits only after an explicit user choice to generate.
   - **Pass:** No documentation edits for gaps until the user selects an option that includes generation; if they decline or choose report-only behavior, end after the report.

6. **Post-edit verification** — After any generation, run or offer the linter commands in Phase 5 of the reference for languages you changed, when those tools exist in the repo.
   - **Pass:** Linter run completed with output captured, or `N/A` with a one-line reason (e.g. tool not configured); remaining issues are listed or cleared.

## Notes

- Use `--report-only` to skip generation.
- Avoid test files unless they are test helpers.
- Keep report output aligned with the language-specific standards in the reference file.
