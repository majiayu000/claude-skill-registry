---
name: update-ui-inventory
description: Update the UI component inventory and documentation when components are added or removed. Use when adding new components, after code reviews flag inventory mismatches, or periodically to ensure docs match reality.
---

# Update UI Inventory Skill

## When to Activate

Activate this skill when:
- Adding new UI components to the engine
- Removing or deprecating components
- The component-inventory CI check fails
- You want to verify docs match the actual component count
- After merging PRs that add/remove components

## Files Involved

| File | Purpose |
|------|---------|
| `.github/component-inventory.json` | Source of truth for component counts |
| `docs/design-system/COMPONENT-REFERENCE.md` | User-facing component documentation |
| `packages/engine/src/lib/ui/components/` | Actual component source files |

## Inventory Structure

The inventory tracks 13 component categories:

```json
{
  "components": {
    "total": 186,
    "breakdown": {
      "primitives": 45,
      "nature": 64,
      "ui": 29,
      "typography": 11,
      "chrome": 6,
      "terrarium": 7,
      "gallery": 4,
      "charts": 4,
      "content": 4,
      "states": 4,
      "forms": 3,
      "indicators": 3,
      "icons": 2
    }
  }
}
```

## Step-by-Step Process

### 1. Count Components in Each Category

Run these commands to get actual counts:

```bash
# Count .svelte files in each category
for dir in primitives nature ui typography chrome terrarium gallery charts content states forms indicators icons; do
  count=$(find packages/engine/src/lib/ui/components/$dir -name "*.svelte" 2>/dev/null | wc -l | tr -d ' ')
  echo "$dir: $count"
done
```

### 2. Compare with Inventory

Read the current inventory and compare:

```bash
cat .github/component-inventory.json
```

### 3. Identify Discrepancies

Look for:
- **New components**: Files exist but aren't in the count
- **Removed components**: Count includes files that no longer exist
- **Moved components**: Component relocated to different category

### 4. Update Inventory JSON

Edit `.github/component-inventory.json`:

```json
{
  "lastUpdated": "YYYY-MM-DD",
  "lastAuditedBy": "claude/<context>",
  "components": {
    "total": <sum of all categories>,
    "breakdown": {
      "<category>": <new count>,
      ...
    }
  }
}
```

### 5. Update Component Reference

Edit `docs/design-system/COMPONENT-REFERENCE.md`:

1. **Update the intro line**:
   ```markdown
   > 186 components organized by category...
   ```

2. **Update Quick Links** (the anchor links include counts):
   ```markdown
   - [ui/ - Core UI Components](#ui---core-ui-components-29)
   ```

3. **Update section headers**:
   ```markdown
   ## ui/ - Core UI Components (29)
   ```

4. **Add new component to relevant table** (if significant):
   For Glass components, add to "Other Glass Components" table:
   ```markdown
   | `GlassNewComponent` | Description of what it does |
   ```

5. **Update the last updated date** at the bottom:
   ```markdown
   *Last updated: YYYY-MM-DD*
   ```

### 6. Commit Changes

```bash
git add .github/component-inventory.json docs/design-system/COMPONENT-REFERENCE.md
git commit -m "docs: update component inventory

- Update <category> count: X -> Y
- Add <ComponentName> to COMPONENT-REFERENCE.md
- Bump total: A -> B"
```

## Quick Reference: Counting Commands

```bash
# Single category count
find packages/engine/src/lib/ui/components/ui -name "*.svelte" | wc -l

# List all files in a category (to identify new ones)
ls packages/engine/src/lib/ui/components/ui/*.svelte

# Find Glass components specifically
ls packages/engine/src/lib/ui/components/ui/ | grep -i glass

# Total across all categories
find packages/engine/src/lib/ui/components -name "*.svelte" | wc -l
```

## Documentation Guidelines

When adding components to COMPONENT-REFERENCE.md:

### Glass Components (Always Document)
Glass components define Grove's visual language - always add them to the "Other Glass Components" table with a clear description.

### Standard Components
Add to the "Standard Components" table if it's a general-purpose wrapper.

### Specialized Components
For category-specific components (nature, charts, etc.), add to the appropriate section if it's significant or has unique props worth documenting.

## Example: Adding a New Glass Component

After adding `GlassStatusWidget.svelte`:

1. **Count confirms ui went from 28 to 29**

2. **Update inventory**:
   ```json
   "ui": 29,
   "total": 186,
   "lastUpdated": "2026-01-21"
   ```

3. **Update COMPONENT-REFERENCE.md**:
   - Line 3: `> 186 components...`
   - Line 13: `- [ui/ - Core UI Components](#ui---core-ui-components-29)`
   - Line 74: `## ui/ - Core UI Components (29)`
   - After line 209, add to table:
     ```markdown
     | `GlassStatusWidget` | Real-time status widget with auto-refresh |
     ```
   - Last line: `*Last updated: 2026-01-21*`

## CI Integration

The `.github/workflows/component-inventory.yml` workflow:
- Runs on PRs touching `packages/engine/src/lib/ui/components/**`
- Counts actual components vs inventory
- Fails if there's a mismatch
- Provides helpful output showing discrepancies

When CI fails, run this skill to fix the mismatch.

## Checklist

Before finishing:

- [ ] All category counts match actual file counts
- [ ] Total equals sum of all categories
- [ ] `lastUpdated` date is today
- [ ] COMPONENT-REFERENCE.md counts match inventory
- [ ] New significant components added to appropriate documentation table
- [ ] Quick Links anchors updated if section headers changed
- [ ] Changes committed with descriptive message
