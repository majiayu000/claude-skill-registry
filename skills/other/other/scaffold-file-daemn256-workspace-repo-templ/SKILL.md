---
name: scaffold-file
description: Create or update a scaffold file in scaffolds/
---

# Scaffold File

Uses **Workspace Configurator** agent. Create a new scaffold file or update an existing one, following the manifest's scaffold resolution rules.

**Prerequisites:** `template-manifest.yaml` exists, `scaffolds/` directory exists

---

## Phase 1: Classify

### Determine Scaffold Placement

1. Identify which file needs a scaffold (the path as it appears in a consumer workspace)
2. Check `template-manifest.yaml` for an existing rule:
   - If a `scaffold` rule already exists for this path, this is an **update**
   - If the file is currently unlisted or set to `copy`, a manifest change may be needed
3. Determine target scope:
   - **Both targets** → place in `scaffolds/common/<path>`
   - **Differs by target** → place in `scaffolds/root/<path>` and/or `scaffolds/repo/<path>`
   - Target-specific files override common (first match wins)

### Decision Criteria

| Question                                           | If Yes                  | If No               |
| -------------------------------------------------- | ----------------------- | ------------------- |
| Same example content works for root and repo?      | Use `scaffolds/common/` | Use target-specific |
| Root workspace needs multi-repo context?           | Needs `scaffolds/root/` | Common may suffice  |
| Repo workspace needs single-repo context?          | Needs `scaffolds/repo/` | Common may suffice  |
| File contains real consumer data (IDs, keys, etc)? | Must be scaffold        | Could be copy       |

### Output

```markdown
## Context Anchors

- **Phase:** 1 — Classify
- **File:** <consumer-facing path>

## Classification

- **Action:** scaffold
- **Placement:** `scaffolds/common/<path>` | `scaffolds/root/<path>` + `scaffolds/repo/<path>`
- **Manifest Change:** Yes (add rule) | No (rule exists)
- **Rationale:** <why this placement>

## Next Step

Approve scaffold placement before creating the file.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Await approval for scaffold placement.

---

## Phase 2: Create

### Write the Scaffold

1. Create the scaffold file at the determined path
2. Content guidelines:
   - Use **placeholder values** — never real consumer data
   - Include **comments** explaining what to customize
   - Follow the same format/schema as the real file
   - Keep it minimal but complete enough to be useful
3. If updating an existing scaffold, preserve the structure and update relevant sections

### Scaffold Content Patterns

| File Type    | Pattern                                                     |
| ------------ | ----------------------------------------------------------- |
| YAML config  | Valid YAML with placeholder values and inline comments      |
| Markdown doc | Section headers with `<!-- TODO: ... -->` guidance          |
| JSON config  | Valid JSON with descriptive placeholder strings             |
| README       | Template structure with `<project-name>` style placeholders |

### Output

```markdown
## Context Anchors

- **Phase:** 2 — Create
- **File:** <scaffold path created>

## Scaffold Content

<summary of what was created>

## Next Step

Update manifest if needed, then verify with dry-run sync.

**Approval Required:** No
```

---

## Phase 3: Verify

### Validate the Scaffold

1. If manifest was updated, check `template-manifest.yaml` for correctness
2. Run `tools/sync-to-templates.sh --dry-run` to confirm the scaffold appears in output
3. Run `tools/validate-templates.sh` to check for scaffold-related issues

### Output

```markdown
## Context Anchors

- **Phase:** 3 — Verify

## Verification

- **Dry-run shows scaffold:** Yes | No
- **Validation clean:** Yes | <issues found>

## Next Step

Scaffold is ready. Run `/sync-templates` to propagate.

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
