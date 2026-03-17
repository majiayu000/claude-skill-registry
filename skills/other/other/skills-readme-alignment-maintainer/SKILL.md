---
name: skills-readme-alignment-maintainer
description: Audit and maintain README standards across *-skills repositories with a two-pass workflow (audit first, optional bounded fixes second). Use when running Codex App or CLI automations for skills-repo documentation consistency, profile-aware section schemas, command integrity checks, and discoverability baseline enforcement.
---

# Skills README Alignment Maintainer

Run deterministic README standards maintenance for `*-skills` repositories in a workspace.

## Inputs

Pass runtime inputs from the calling prompt:

- `--workspace <path>`
- `--repo-glob <pattern>` (default: `*-skills`)
- `--exclude <path>` (repeatable)
- optional `--apply-fixes`
- optional `--md-out`, `--json-out`

## Workflow

1. Run pass 1 audit with `scripts/readme_alignment_maintainer.py`.
2. Review profile assignments and issue categories.
3. If bounded remediation is desired, run pass 2 with `--apply-fixes`.
4. Re-check touched repos (handled by script).
5. Report Markdown and JSON outputs.

## Commands

Audit only:

```bash
python3 scripts/readme_alignment_maintainer.py \
  --workspace ~/Workspace \
  --repo-glob '*-skills' \
  --print-md \
  --print-json
```

Audit and bounded fixes:

```bash
python3 scripts/readme_alignment_maintainer.py \
  --workspace ~/Workspace \
  --repo-glob '*-skills' \
  --apply-fixes \
  --md-out /tmp/readme-alignment-report.md \
  --json-out /tmp/readme-alignment-report.json
```

Fail when unresolved issues remain:

```bash
python3 scripts/readme_alignment_maintainer.py \
  --workspace ~/Workspace \
  --repo-glob '*-skills' \
  --apply-fixes \
  --fail-on-issues
```

## Safety Rules

- Never commit changes automatically.
- Edit README files only.
- Never edit source code, manifests, lockfiles, CI files, or AGENTS.md.
- Apply only bounded heading/schema/discoverability insertions and bootstrap README creation.
- Keep diffs minimal and preserve existing style where possible.

## Profile Model

Use `references/profile-model.md`:

- public curated repos: enforce full schema and discoverability sections
- private/internal repos: keep concise, omit growth-only sections
- bootstrap repos: allow initial README creation with minimal complete structure

## Output Contract

The script emits:

- Markdown summary of run context, profile assignments, issues, fixes, remaining issues, and errors.
- JSON report containing:
  - `run_context`
  - `repos_scanned`
  - `profile_assignments`
  - `schema_violations`
  - `command_integrity_issues`
  - `fixes_applied`
  - `post_fix_status`
  - `errors`

Use JSON for automation integration and Markdown for operator review.

## Automation Templates

Use `$skills-readme-alignment-maintainer` in automation prompts.

For ready-to-fill Codex App and Codex CLI templates, use:

- `references/automation-prompts.md`

## References

- Profile mapping: `references/profile-model.md`
- Required sections by profile: `references/section-schema.md`
- Voice and style rules: `references/style-rules.md`
- Discoverability requirements: `references/discoverability-rules.md`
- Verification checklist: `references/verification-checklist.md`
- Seed standards artifacts: `references/seed-artifacts.md`
- Automation prompt templates: `references/automation-prompts.md`
