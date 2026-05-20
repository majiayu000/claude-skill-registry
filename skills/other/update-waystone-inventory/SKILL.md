---
name: update-waystone-inventory
description: Update the waystone (contextual help marker) inventory when waystones are added or removed. Use when adding new waystones, after code reviews flag inventory mismatches, or periodically to ensure docs match reality.
---

# Update Waystone Inventory Skill

## When to Activate

Activate this skill when:

- Adding new `<Waystone>` components to any Grove package
- Removing waystones from pages
- The waystone-inventory CI check fails
- You want to verify the inventory matches actual codebase usage
- After merging PRs that add/remove waystones

## Files Involved

| File                                                                | Purpose                                 |
| ------------------------------------------------------------------- | --------------------------------------- |
| `.github/waystone-inventory.json`                                   | Source of truth for waystone placements |
| `packages/engine/src/lib/ui/components/ui/waystone/Waystone.svelte` | Component source                        |
| `docs/specs/waystone-spec.md`                                       | Waystone system specification           |

## Inventory Structure

The inventory tracks waystones by slug, with each slug containing its instances:

```json
{
  "waystones": {
    "total": 15,
    "breakdown": {
      "engine": 15,
      "login": 0,
      "landing": 0
    },
    "bySlugs": 10
  },
  "slugs": [
    {
      "slug": "what-is-rings",
      "usageCount": 2,
      "instances": [
        {
          "file": "packages/engine/src/routes/arbor/analytics/+page.svelte",
          "label": "Learn about Rings",
          "placement": "page-header",
          "size": "sm"
        }
      ]
    }
  ]
}
```

## Placement Types

When adding instances, use the appropriate placement type:

| Type             | Description                                      |
| ---------------- | ------------------------------------------------ |
| `page-header`    | Beside `<h1>` titles on major pages              |
| `section-header` | Beside `<h2>` section titles within pages        |
| `feature-card`   | Inside feature showcase cards                    |
| `inline-help`    | Inline with paragraph text for contextual hints  |
| `error-context`  | Within error messages linking to troubleshooting |
| `panel-header`   | In panel or control headers                      |
| `auth-context`   | Near auth-related UI for trust building          |

## Step-by-Step Process

### 1. Find All Waystone Usages

```bash
# Search for <Waystone in all Svelte files across ALL packages
rg '<Waystone' --type svelte -l

# Get slug and label details
rg '<Waystone' --type svelte -A 3
```

### 2. Compare with Inventory

```bash
# Read current inventory
cat .github/waystone-inventory.json | jq '.waystones.total'

# Count actual usages
rg '<Waystone' --type svelte | wc -l
```

### 3. Identify Discrepancies

Look for:

- **New waystones**: `<Waystone>` tags in code but not in inventory
- **Removed waystones**: Instances in inventory whose files no longer contain the waystone
- **Changed metadata**: Slug, label, or placement changed

### 4. Update Inventory JSON

Edit `.github/waystone-inventory.json`:

1. **Update counts**:

   ```json
   "waystones": {
     "total": <new total instances>,
     "breakdown": {
       "engine": <count in engine>,
       "login": <count in login>,
       ...
     },
     "bySlugs": <number of distinct slugs>
   }
   ```

2. **Add/update slug entries** — add new slugs to the `slugs` array, or add instances to existing slugs

3. **Update metadata**:
   ```json
   "lastUpdated": "YYYY-MM-DD",
   "lastAuditedBy": "claude/<context>"
   ```

### 5. Commit Changes

```bash
gw git commit --write -m "docs: update waystone inventory

- Add <slug> waystone to <package>
- Update total: X -> Y
- Update package breakdown"
```

## Quick Reference Commands

```bash
# Count all waystone instances across all packages
rg '<Waystone' packages/ --type svelte | wc -l

# List all unique slugs in use
rg 'slug="([^"]+)"' packages/ --type svelte -o -r '$1' | sort -u

# Count instances per package
for pkg in engine login landing plant meadow; do
  count=$(rg '<Waystone' "packages/$pkg" --type svelte 2>/dev/null | wc -l | tr -d ' ')
  echo "$pkg: $count"
done

# Find waystones with specific placement patterns
rg '<Waystone' packages/ --type svelte -B 2 -A 2
```

## Adding a New Waystone (Full Checklist)

When adding a new waystone:

- [ ] Add `<Waystone>` component to the target file with appropriate slug, label, and size
- [ ] Ensure the file imports Waystone (from `$lib/ui` in engine, or `@autumnsgrove/groveengine/ui` in other packages)
- [ ] Add the instance to `.github/waystone-inventory.json`
- [ ] If it's a new slug, add a new entry to the `slugs` array
- [ ] If the slug already exists, add an instance to the existing entry
- [ ] Update `waystones.total` count
- [ ] Update `waystones.breakdown.<package>` count
- [ ] Update `waystones.bySlugs` if a new slug was added
- [ ] Update `lastUpdated` and `lastAuditedBy`
- [ ] Verify the KB article exists (or note it needs to be created)

## CI Integration

The `.github/workflows/waystone-inventory.yml` workflow:

- Runs on PRs touching `**/*.svelte` files
- Counts `<Waystone` occurrences across all packages
- Compares to inventory total
- Comments on PRs when there's a mismatch
- Creates issues for drift on scheduled runs (Thursdays)

When CI fails, run this skill to fix the mismatch.

## Checklist

Before finishing:

- [ ] All `<Waystone>` instances in code have entries in inventory
- [ ] All inventory instances still exist in code
- [ ] `total` equals sum of all `breakdown` values
- [ ] `bySlugs` equals the length of the `slugs` array
- [ ] Each slug's `usageCount` matches its `instances` array length
- [ ] `lastUpdated` date is today
- [ ] Changes committed with descriptive message
