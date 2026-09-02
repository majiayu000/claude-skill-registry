---
name: sync-docs
description: 'Use when a behavioral diff may have left docs or CHANGELOG stale. Detects docs-vs-code drift and applies only safe fixes. Also handles stale code comments when tidy targets them. Not for roadmap drift — use drift-detect. Don''t use for remote or irreversible changes.'
---

# Sync docs

## Contract

| Field | Bound contract |
|---|---|
| Trigger | User says 'sync docs' or 'update changelog' after a behavioral change. |
| Authority | Reversible local writes only. Edit named local doc files and write a fix ledger. Rollback reverts the edited files to their pre-edit content. |
| Side effect | Applies only safe fixes (version bump plus CHANGELOG Unreleased entry) and writes a fix ledger with before/after evidence. |
| Done | Safe fixes are applied or explicitly unavailable, and all residual drift is flagged with file:line evidence and reasons. |

## Inputs

- Mode: `report` (default) or `apply`. `apply` still edits only safe-fix issues.
- Scope: `recent` (changed files from current branch or last few commits), `before-pr` (branch diff against PR base), or `all` (all tracked code and docs).
- Base: explicit base ref preferred. If absent, resolve the default branch, then fall back to `HEAD~5` for `recent`.

## Refusal

- No diff or empty scope: stop. Report the resolved base and scope; do not fabricate drift.
- Ambiguous base ref: stop. List candidate refs and ask the user.
- Manifest parse failure: skip the version-bump safe fix for that manifest; flag the file as MEDIUM with reason.
- Post-edit read mismatch: revert the edit; reclassify the issue as flag-only with `reasonFlagOnly`.
- Codegraph unavailable: use syntax fallback; downgrade confidence to MEDIUM for symbol-dependent claims.

## Procedure

1. **Pick scope and base.** Refuse ambiguous review scope when the user expects PR readiness. Resolve the base ref and compute the changed-file list. In ODIN tool mode, use `bash` only for git commands; use `find`, `search`, `read`, `lsp`, `ast_grep`, and `edit` for everything else. Done when: the scope and base are resolved and the changed-file list is computed.
2. **Compute changed code.** Keep only source/config/package files that can change docs. Exclude pure docs, vendored/generated paths, lockfiles unless version docs mention package manager output, and deleted files that were never public. Done when: the changed-code file list is filtered.
3. **Extract coupling terms.** For each changed code file derive filename stem, full path, import strings from the diff, and exported/public symbols via codegraph when indexed or syntax fallback. Load `references/doc-issues.md` for the full detection recipe. Done when: coupling terms are extracted for every changed file.
4. **Discover related docs.** Search live doc surfaces: `README.md`, `CHANGELOG.md`, `docs/**/*.md`, `*.md` at repo root. For each coupling term, search docs and record `doc`, `line`, `term`, `referenceType`. Done when: every coupling term is searched against docs.
5. **Classify issues.** Load `references/doc-issues.md` for the severity taxonomy, safe-fix boundary, and default ignore list. Classify each finding as HIGH, MEDIUM, or LOW. Ignore generated docs unless explicitly in scope, vendored docs, changelog append-only entries, and versioned snapshots unless in scope. Done when: every finding is classified with severity and safe-fix eligibility.
6. **Apply safe fixes only** (in `apply` mode). Safe fixes are: version bump (replace stale semver in docs with the manifest version when the line clearly labels a version) and CHANGELOG `## [Unreleased]` entry (insert a minimal bullet citing commit/file evidence). Load `references/detection-recipes.md` for per-ecosystem manifest version fields and changelog evidence commands. Do not auto-edit removed exports, import paths, examples, undocumented exports, dead-code docs, or doc-drift prose. Those require human intent. Done when: safe fixes are applied or confirmed unavailable.
7. **Flag the rest.** Emit a compact report sorted by severity then file path. Done when: every non-safe-fix finding is flagged with file:line evidence and reason.
8. **Return fix ledger.** For every edit record `file`, `line`, `type`, `before`, `after`, and evidence source. For every flag-only item record `reasonFlagOnly`. Done when: the fix ledger is complete.

## Failure modes

- Partial results: if some coupling terms resolve and others do not, report resolved issues and flag unresolved terms. Never widen scope to compensate for missing evidence.
- Rollback: revert any edited file to its pre-edit content. The fix ledger records before/after for every edit.

## Output

A JSON fix ledger: `opCell`, `scope`, `base`, `changedCode` array, `relatedDocs` array, `fixesApplied` array, `flagged` array. Completion means safe fixes are applied or explicitly unavailable, and all remaining drift is flagged. A clean report with no edits is valid only after the diff-to-doc mapping and taxonomy pass ran.
