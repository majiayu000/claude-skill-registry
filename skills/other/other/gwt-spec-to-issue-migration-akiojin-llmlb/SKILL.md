---
name: gwt-spec-to-issue-migration
description: "Migrate existing local SPEC directories (specs/SPEC-*) to GitHub Issue-first specs (gwt-spec label) using the bundled migration script. Use when asked to replace local spec.md/plan.md/tasks.md based workflow with GitHub Issue based management."
---

# gwt Spec to Issue Migration

## Overview

Use this skill only for repositories that still carry legacy local spec trees from a pre-Issue-first workflow.

Migrate local `specs/SPEC-*` directories to GitHub Issues (`gwt-spec` label), then remove the legacy local source of truth.

This skill uses:
- `.gemini/skills/gwt-spec-to-issue-migration/scripts/migrate-specs-to-issues.sh`
- `crates/gwt-core/src/git/issue_spec.rs`

## Preconditions

- Run in repository root
- `gh auth status` is authenticated for target repo
- Branch policy is respected (no branch creation/switching unless user requests)
- `$GWT_PROJECT_ROOT` environment variable is available; prefer it over CWD for repo resolution

## Standard Workflow

1. Inspect source specs directory (auto-detection or explicit `--specs-dir`)
2. Run dry-run and review planned migration count and deletion targets
3. Run actual migration
4. Verify migrated issues exist (`gwt-spec` label)
5. Confirm legacy local spec files were removed on success

## Commands

### Dry-run

```bash
bash ".gemini/skills/gwt-spec-to-issue-migration/scripts/migrate-specs-to-issues.sh" --dry-run
```

### Dry-run with explicit specs directory

```bash
bash ".gemini/skills/gwt-spec-to-issue-migration/scripts/migrate-specs-to-issues.sh" --dry-run --specs-dir "<path-to-specs>"
```

### Execute migration

```bash
bash ".gemini/skills/gwt-spec-to-issue-migration/scripts/migrate-specs-to-issues.sh"
```

### Verify report

```bash
cat migration-report.json
```

Note: `migration-report.json` is deleted automatically after a fully successful migration cleanup. It remains available for dry-run and failure cases.

### Verify created issues

```bash
gh issue list --label gwt-spec --state all --limit 200
```

## Expected Behavior

- Auto-detects local `specs/` under `$GWT_PROJECT_ROOT` or the current repository
- If no `SPEC-*` directory exists, exits successfully with empty report (`[]`)
- Migrates sections from `spec.md`, `plan.md`, `tasks.md` and related artifacts
- Writes per-spec result to `migration-report.json`
- Shows planned deletions during `--dry-run`
- Deletes migrated local spec directories, detected legacy workflow leftovers, and `migration-report.json` after a fully successful cleanup

## Notes

- For safety, always run `--dry-run` first.
- Artifact files in `contracts/` and `checklists/` are migrated as issue comments.
- After migration, ongoing spec updates should use Issue-first operations (`gwt-spec-ops`).
- This skill is for external legacy import only; gwt's normal spec workflow should never recreate repository-local spec bundles.
