---
name: scaffold-file
description: Create or update a scaffold file in scaffolds/.
---

# Scaffold File

The Workspace Configurator drives this workflow. Create a new scaffold file or update an existing one, following the manifest's scaffold resolution rules.

**Prerequisites:** `template-manifest.yaml` exists, `scaffolds/` directory exists.

---

## Phase 1: Classify

Determine where the scaffold belongs.

### Steps

1. Identify the consumer-facing file path that needs a scaffold
2. Check `template-manifest.yaml` for an existing rule
3. Determine target scope:
   - **Both targets** → `scaffolds/common/<path>`
   - **Differs by target** → `scaffolds/root/<path>` and/or `scaffolds/repo/<path>`
   - Target-specific overrides common (first match wins)

### Decision Criteria

| Question                              | Yes                 | No                 |
| ------------------------------------- | ------------------- | ------------------ |
| Same content works for root and repo? | `scaffolds/common/` | Target-specific    |
| Root needs multi-repo context?        | `scaffolds/root/`   | Common may suffice |
| Repo needs single-repo context?       | `scaffolds/repo/`   | Common may suffice |
| File contains real consumer data?     | Must be scaffold    | Could be copy      |

### Output

```markdown
## Context Anchors

- **Phase:** Classify
- **File:** <consumer-facing path>

## Classification

- **Placement:** `scaffolds/common/<path>` | target-specific
- **Manifest Change:** Yes | No
- **Rationale:** <why>

## Next Step

Approve scaffold placement.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Await approval.

---

## Phase 2: Create

Write the scaffold file.

### Steps

1. Create scaffold at the determined path
2. Content rules:
   - Placeholder values only — never real consumer data
   - Include comments explaining what to customize
   - Follow the same format/schema as the real file
   - Minimal but complete

### Content Patterns

| Type   | Pattern                                               |
| ------ | ----------------------------------------------------- |
| YAML   | Valid YAML with placeholders and inline comments      |
| MD     | Section headers with `<!-- TODO: ... -->` guidance    |
| JSON   | Valid JSON with descriptive placeholder strings       |
| README | Template structure with `<project-name>` placeholders |

### Output

```markdown
## Context Anchors

- **Phase:** Create
- **File:** <scaffold path>

## Next Step

Verify with dry-run sync.

**Approval Required:** No
```

---

## Phase 3: Verify

Validate the scaffold works correctly.

### Steps

1. Check `template-manifest.yaml` if it was updated
2. Run `tools/sync-to-templates.sh --dry-run` — confirm scaffold appears
3. Run `tools/validate-templates.sh` — check for scaffold issues

### Output

```markdown
## Context Anchors

- **Phase:** Verify

## Verification

- **Dry-run shows scaffold:** Yes | No
- **Validation clean:** Yes | <issues>

## Next Step

Run `/skill:sync-templates` to propagate.

**Approval Required:** No
```

### ⛔ CHECKPOINT

**STOP.** Verify scaffold content and placement before propagating.

---

## Error Handling

| Error                    | Recovery                                    |
| ------------------------ | ------------------------------------------- |
| Manifest rule conflict   | Check existing rules, resolve overlap       |
| Dry-run shows missing    | Verify scaffold path matches manifest       |
| Validation finds leakage | Check for consumer data in scaffold content |
| Template repo not cloned | Clone template repos before syncing         |
