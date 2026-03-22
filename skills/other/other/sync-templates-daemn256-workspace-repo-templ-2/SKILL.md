---
name: sync-templates
description: Sync workspace content to template repos via manifest
---

# Sync Templates

Uses **Workspace Configurator** agent. Run the manifest-driven sync to propagate workspace content to template repositories, then validate the results.

**Prerequisites:** `template-manifest.yaml` exists, template repos cloned under `repos/`

---

## Phase 1: Preview

### Dry Run

1. Run `tools/sync-to-templates.sh --dry-run` to preview what will change
2. Review the output — look for:
   - **Copy** operations: files copied verbatim from workspace to template
   - **Scaffold** operations: files sourced from `scaffolds/<target>/` or `scaffolds/common/`
   - **Skipped** files: ignored by manifest (consumer-only content)
3. Flag any unexpected results (files that shouldn't propagate, missing scaffold sources)

### Output

```markdown
## Context Anchors

- **Phase:** 1 — Preview

## Dry Run Summary

| Target | Copies | Scaffolds | Skipped |
| ------ | ------ | --------- | ------- |
| root   | <n>    | <n>       | <n>     |
| repo   | <n>    | <n>       | <n>     |

## Observations

<any unexpected results or concerns>

## Next Step

Approve sync execution.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human approves sync execution.

---

## Phase 2: Execute

### Sync

1. Run `tools/sync-to-templates.sh` (without `--dry-run`)
2. Run `tools/validate-templates.sh` to verify template health
3. Report validation results

### Output

```markdown
## Context Anchors

- **Phase:** 2 — Execute

## Sync Results

<output summary from sync>

## Validation Results

| Check        | Errors | Warnings |
| ------------ | ------ | -------- |
| Completeness | <n>    | <n>      |
| Drift        | <n>    | <n>      |
| Scaffold     | <n>    | <n>      |
| Leakage      | <n>    | <n>      |
| Structure    | <n>    | <n>      |

## Issues Found

<any errors or warnings that need attention>

## Next Step

<commit template changes, fix issues, or re-sync>

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not commit template changes without human approval.

---

## Phase 3: Commit

### Stage and Commit

1. For each template repo that changed:
   - `cd repos/<template-repo>/`
   - `git add -A && git status -s`
   - Commit with message: `chore: sync from workspace via manifest`
2. Return to workspace root

### Output

```markdown
## Context Anchors

- **Phase:** 3 — Commit

## Commits

| Template Repo | Commit | Files Changed |
| ------------- | ------ | ------------- |
| <name>        | <hash> | <n>           |

## Next Step

Push template repos when ready.

**Approval Required:** Yes
```

---

## Error Handling

| Error                    | Recovery                                       |
| ------------------------ | ---------------------------------------------- |
| Sync script fails        | Check template-manifest.yaml for syntax errors |
| Validation reports drift | Review and resolve drift before committing     |
| Repo has uncommitted     | Stash or commit existing changes first         |
| Missing scaffold source  | Create scaffold via /scaffold-file             |
