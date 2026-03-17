---
description: Sync living docs for an increment. Generates or updates spec files in .specweave/docs/internal/specs/. Use when saying "sync docs", "update living docs", or "sync-docs".
argument-hint: "<increment-id> [--review]"
---

# Sync Living Docs

## Project Overrides

!`s="sync-docs"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

Sync living documentation for an increment. This generates or updates feature specs and user story files under `.specweave/docs/internal/specs/`.

## Usage

```
/sw:sync-docs <increment-id>           # Sync living docs for increment
/sw:sync-docs <increment-id> --review  # Dry-run: validate sync without modifying files
```

## Workflow

### Step 1: Resolve Increment

1. Parse the increment ID argument (required)
2. Find the increment directory: `.specweave/increments/NNNN-*/`
3. Load `spec.md` and `metadata.json`

### Step 2: Detect Mode

- If `--review` argument present: set `dryRun = true`
- Otherwise: set `dryRun = false`

### Step 3: Execute Sync

Run the living docs sync via CLI:

```bash
# Normal mode
specweave sync-living-docs <increment-id>

# If CLI command not available, use Node.js directly:
node -e "
  const { LivingDocsSync } = require('./dist/src/core/living-docs/living-docs-sync.js');
  const sync = new LivingDocsSync(process.cwd());
  sync.syncIncrement('<increment-id>').then(r => console.log(JSON.stringify(r, null, 2)));
"
```

### Step 4: Report Results

Display a summary:

```
Living Docs Sync Results:
- Feature spec: created/updated/unchanged
- User story files: N created, M updated, K unchanged
- Total files affected: X
```

In review mode, prefix with: `[DRY RUN] No files were modified.`

### Step 5: Error Handling

If sync fails:
- Display the error message
- Suggest: "Check that spec.md has valid frontmatter and user stories are properly formatted"
- Suggest: "Run `/sw:progress-sync` for full external tool sync"
