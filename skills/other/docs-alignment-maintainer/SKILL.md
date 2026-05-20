---
name: docs-alignment-maintainer
description: Check and maintain documentation alignment across repositories in a workspace with a two-pass workflow (audit first, then safe targeted fixes), including language-aware checks for Swift, JavaScript/TypeScript, Python, and Rust. Use when running scheduled automation for repo hygiene, when docs may drift from manifests/tooling, or when you need a Markdown + JSON alignment report with optional bounded auto-fixes.
---

# Docs Alignment Maintainer

Run a deterministic two-pass docs alignment workflow across repositories under a provided workspace root. Detect drift first, then apply only bounded high-confidence fixes when requested.

## Inputs

Pass runtime inputs from the calling prompt:
- `--workspace <path>`
- `--exclude <path>` (repeatable)
- Optional `--exclude-file <path>` with one path per line

Defaults are intentionally not hardcoded in the skill body so automation can control scope per run.

## Workflow

1. Run pass 1 discovery and checks with `scripts/docs_alignment_maintainer.py`.
2. Review unaligned repos and issue categories.
3. If safe remediation is desired, run pass 2 with `--apply-fixes`.
4. Re-check touched repos (handled by the script) and inspect remaining issues.
5. Report results from Markdown and JSON outputs.

## Commands

Audit only:

```bash
python3 scripts/docs_alignment_maintainer.py \
  --workspace ~/Workspace \
  --exclude ~/Workspace/services \
  --print-md \
  --print-json
```

Audit and safe fixes:

```bash
python3 scripts/docs_alignment_maintainer.py \
  --workspace ~/Workspace \
  --exclude ~/Workspace/services \
  --apply-fixes \
  --md-out /tmp/docs-alignment-report.md \
  --json-out /tmp/docs-alignment-report.json
```

Fail the run when unresolved issues remain:

```bash
python3 scripts/docs_alignment_maintainer.py \
  --workspace ~/Workspace \
  --exclude ~/Workspace/services \
  --apply-fixes \
  --fail-on-issues
```

## Safety Rules

- Never commit changes automatically.
- Edit docs only (for example `README.md`, `CONTRIBUTING.md`, `ROADMAP.md`, `docs/*.md`).
- `AGENTS.md` is out-of-scope for this skill and is owned by a dedicated AGENTS maintainer workflow.
- Never edit source code, lockfiles, or manifests.
- Apply only bounded replacements and concise quickstart insertion when evidence is explicit.
- Keep diffs minimal and preserve existing formatting style.

## Output Contract

The script emits:
- Markdown summary with run context, discovery summary, unaligned repos, fixes applied, remaining issues, modified files, and errors.
- JSON report containing:
  - `run_context`
  - `repos_scanned`
  - `unaligned_repos`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`

Use JSON for automation pipelines and Markdown for operator review.

## Automation Templates

Use `$docs-alignment-maintainer` inside automation prompts so Codex reliably loads this skill context.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including guardrails, placeholders, and customization knobs, use:
- `references/automation-prompts.md`

## References

- Common checks and discovery rules: `references/checks-common.md`
- Swift guidance: `references/checks-swift.md`
- JS/TS guidance: `references/checks-js-ts.md`
- Python guidance: `references/checks-python.md`
- Rust guidance: `references/checks-rust.md`
- Safe-fix policy boundaries: `references/fix-policies.md`
- Report schema and section contract: `references/output-contract.md`
- Automation prompt templates: `references/automation-prompts.md`
