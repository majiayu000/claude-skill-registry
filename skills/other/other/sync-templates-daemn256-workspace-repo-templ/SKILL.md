---
name: sync-templates
description: Sync workspace content to template repos via manifest.
---

# Sync Templates

The Workspace Configurator drives this workflow. Run the manifest-driven sync to propagate workspace content to template repositories, then validate the results.

**Prerequisites:** `template-manifest.yaml` exists, template repos cloned under `repos/`.

---

## Phase 1: Preview

Dry-run the sync to preview changes.

### Steps

1. Run `tools/sync-to-templates.sh --dry-run`
2. Review output for copy, scaffold, and skip counts
3. Flag unexpected results (files that shouldn't propagate, missing scaffold sources)

### Output

```markdown
## Context Anchors

- **Phase:** Preview

## Dry Run Summary

| Target | Copies | Scaffolds | Skipped |
| ------ | ------ | --------- | ------- |
| root   | <n>    | <n>       | <n>     |
| repo   | <n>    | <n>       | <n>     |

## Next Step

Approve sync execution.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not execute sync without human approval.

---

## Phase 2: Execute

Run the sync and validate.

### Steps

1. Run `tools/sync-to-templates.sh`
2. Run `tools/validate-templates.sh`
3. Report validation results — errors, warnings, checks passed

### Output

```markdown
## Context Anchors

- **Phase:** Execute

## Validation Results

| Check        | Errors | Warnings |
| ------------ | ------ | -------- |
| Completeness | <n>    | <n>      |
| Drift        | <n>    | <n>      |
| Scaffold     | <n>    | <n>      |
| Leakage      | <n>    | <n>      |
| Structure    | <n>    | <n>      |

## Next Step

Commit template changes or fix issues.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not commit without human approval.

---

## Phase 3: Commit

Stage and commit template repo changes.

### Steps

1. For each template repo that changed:
   - Navigate to `repos/<template-repo>/`
   - Stage all changes: `git add -A`
   - Commit: `chore: sync from workspace via manifest`
2. Return to workspace root

### Output

```markdown
## Context Anchors

- **Phase:** Commit

## Commits

| Repo   | Commit | Files |
| ------ | ------ | ----- |
| <name> | <hash> | <n>   |

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
| Missing scaffold source  | Create scaffold via /skill:scaffold-file       |
