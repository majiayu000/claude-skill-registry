---
name: update-graft-inventory
description: Update the graft (feature flag) inventory when flags are added or removed. Use when adding new grafts via migrations, after CI flags inventory mismatches, or periodically to ensure docs match production D1.
---

# Update Graft Inventory Skill

## When to Activate

Activate this skill when:
- Adding new feature flags via SQL migrations
- Removing or deprecating grafts
- The graft-inventory CI check fails
- You want to verify inventory matches production D1
- After applying migrations that add grafts

## Files Involved

| File | Purpose |
|------|---------|
| `.github/graft-inventory.json` | Source of truth for graft counts and metadata |
| `packages/engine/migrations/*.sql` | Migration files that define grafts |
| `packages/engine/src/lib/feature-flags/grafts.ts` | Type definitions (`KnownGraftId`) |
| `docs/guides/adding-grafts-and-flags.md` | Developer guide |

## Inventory Structure

The inventory tracks grafts with full metadata:

```json
{
  "grafts": {
    "total": 10,
    "breakdown": {
      "platform": 8,
      "greenhouse": 2
    },
    "byType": {
      "boolean": 9,
      "number": 1
    }
  },
  "flags": [
    {
      "id": "fireside_mode",
      "name": "Fireside Mode",
      "type": "boolean",
      "greenhouseOnly": true,
      "migration": "040_fireside_scribe_grafts.sql",
      "description": "AI-assisted writing prompts"
    }
  ]
}
```

## Step-by-Step Process

### 1. List Grafts from Migrations

```bash
# Extract all flag IDs from migration INSERT statements
grep -hoP "INSERT OR IGNORE INTO feature_flags.*?VALUES\s*\(\s*'\K[a-z_]+" packages/engine/migrations/*.sql | sort -u
```

### 2. Query Production D1

```bash
# Get actual flags from production database
npx wrangler d1 execute grove-engine-db --remote --command="SELECT id, name, flag_type, greenhouse_only, enabled FROM feature_flags ORDER BY id;"
```

### 3. Compare with Inventory

```bash
# Read current inventory
cat .github/graft-inventory.json | jq '.flags[].id' | sort
```

### 4. Identify Discrepancies

Look for:
- **New grafts**: In migrations/D1 but not in inventory
- **Removed grafts**: In inventory but not in D1
- **Changed metadata**: Type, greenhouse_only, or description changed

### 5. Update Inventory JSON

Edit `.github/graft-inventory.json`:

1. **Update counts**:
   ```json
   "grafts": {
     "total": <new count>,
     "breakdown": {
       "platform": <non-greenhouse count>,
       "greenhouse": <greenhouse_only count>
     }
   }
   ```

2. **Add/remove flag entries**:
   ```json
   "flags": [
     {
       "id": "new_flag_id",
       "name": "Human Readable Name",
       "type": "boolean",
       "greenhouseOnly": false,
       "migration": "XXX_migration_name.sql",
       "description": "What this flag controls"
     }
   ]
   ```

3. **Update metadata**:
   ```json
   "lastUpdated": "YYYY-MM-DD",
   "lastAuditedBy": "claude/<context>"
   ```

### 6. Update KnownGraftId Type

Edit `packages/engine/src/lib/feature-flags/grafts.ts`:

```typescript
export type KnownGraftId =
  | "fireside_mode"
  | "scribe_mode"
  | "meadow_access"
  | "jxl_encoding"
  | "jxl_kill_switch"
  | "new_flag_id";  // Add new flag
```

### 7. Commit Changes

```bash
git add .github/graft-inventory.json packages/engine/src/lib/feature-flags/grafts.ts
git commit -m "docs: update graft inventory

- Add <flag_id> to inventory
- Update total: X -> Y
- Update KnownGraftId type"
```

## Quick Reference Commands

```bash
# Count grafts in migrations
grep -c "INSERT OR IGNORE INTO feature_flags" packages/engine/migrations/*.sql | awk -F: '{sum+=$2} END {print sum}'

# List all flag IDs
grep -hoP "INSERT OR IGNORE INTO feature_flags.*?VALUES\s*\(\s*'\K[a-z_]+" packages/engine/migrations/*.sql | sort -u

# Count greenhouse-only grafts
npx wrangler d1 execute grove-engine-db --remote --command="SELECT COUNT(*) FROM feature_flags WHERE greenhouse_only = 1;"

# Full flag details from production
npx wrangler d1 execute grove-engine-db --remote --command="SELECT * FROM feature_flags ORDER BY id;"

# Check which migrations haven't been applied
# Compare migration file flag IDs vs production D1 flag IDs
```

## Adding a New Graft (Full Checklist)

When adding a new graft:

- [ ] Create migration file: `packages/engine/migrations/XXX_name.sql`
- [ ] Apply migration: `npx wrangler d1 execute grove-engine-db --remote --file=...`
- [ ] Add to `KnownGraftId` type in `grafts.ts`
- [ ] Add entry to `.github/graft-inventory.json` flags array
- [ ] Update inventory counts (total, breakdown.platform/greenhouse, byType)
- [ ] Update `lastUpdated` and `lastAuditedBy`
- [ ] Commit all changes together

## Verifying Production Sync

After updating, verify production matches:

```bash
# Expected count
jq '.grafts.total' .github/graft-inventory.json

# Actual count in production
npx wrangler d1 execute grove-engine-db --remote --command="SELECT COUNT(*) as count FROM feature_flags;"
```

If they don't match, migrations may need to be applied:

```bash
# Apply a specific migration
npx wrangler d1 execute grove-engine-db --remote --file=packages/engine/migrations/XXX_name.sql
```

## CI Integration

The `.github/workflows/graft-inventory.yml` workflow:
- Runs on PRs touching `packages/engine/migrations/*.sql`
- Runs on PRs touching `packages/engine/src/lib/feature-flags/**`
- Parses migrations for INSERT statements
- Compares count to inventory
- Comments on PRs when there's a mismatch
- Creates issues for drift on scheduled runs (Wednesdays)

When CI fails, run this skill to fix the mismatch.

## Checklist

Before finishing:

- [ ] Production D1 graft count matches inventory `total`
- [ ] All flags in D1 have entries in inventory `flags` array
- [ ] `KnownGraftId` type includes all flag IDs
- [ ] `lastUpdated` date is today
- [ ] Counts add up: `total = platform + greenhouse`
- [ ] Type breakdown is accurate
- [ ] Changes committed with descriptive message
