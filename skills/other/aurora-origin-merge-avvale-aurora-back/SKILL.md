---
name: aurora-origin-merge
description: >
  Handles .origin.ts file merges after Aurora CLI regeneration. Provides
  step-by-step workflow to surgically merge new schema code into files with
  custom modifications, preserving all business logic.
  Trigger: After aurora load back module creates .origin files, or when merging
  regenerated code with custom modifications.
license: MIT
metadata:
  author: aurora
  version: '1.2'
  auto_invoke: 'origin file merge, .origin.ts, merge after regeneration'
  scope: back
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Task
---

## When to Use

Use this skill when:

- Aurora CLI creates `.origin.ts` files after regeneration
- You need to merge new schema-generated code into files with custom modifications
- The CLI prompts "Do you want to manage origin files? (Y/n)"
- You find `.origin.ts` files in the codebase after running `aurora load back module`

**Always combine with:**

- `aurora-cli` skill (triggers the regeneration)
- `aurora-cqrs` skill (understand editable zones vs generated zones)
- `prettier` skill (format after merge)

## Detailed References

- [Merge Rules by File Type](merge-rules.md) — Mapper, handler, aggregate, model, API handler, resolver, DTO, event, seeder rules + conflict resolution scenarios

---

## Critical Concept: Why .origin Files Exist

Aurora tracks every generated file via SHA1 hash in `*-lock.json` files. When you regenerate:

```
File hash matches lock?
    │
    YES → Overwrite safely (no custom code)
    │
    NO  → File has custom modifications
         └→ Create filename.origin.ts (new generated version)
            Keep filename.ts intact (your custom code)
```

---

## Step-by-Step Merge Workflow

### Step 0: Detect YAML Schema Delta (CRITICAL)

**Before touching any `.origin` file, you MUST determine what changed in the YAML schema.**

```bash
# Check if YAML has uncommitted changes
git diff HEAD -- cliter/<bc>/<module>.aurora.yaml
```

- **If diff exists** → YAML changed, not yet committed → compare against `HEAD`
- **If no diff** → YAML already committed → compare against previous commit

```bash
# Flujo A: YAML not committed yet
git show HEAD:cliter/<bc>/<module>.aurora.yaml > /tmp/old-schema.yaml

# Flujo B: YAML already committed
PREV_COMMIT=$(git log -2 --format="%H" -- cliter/<bc>/<module>.aurora.yaml | tail -1)
git show $PREV_COMMIT:cliter/<bc>/<module>.aurora.yaml > /tmp/old-schema.yaml
```

```bash
# Compare to get delta
diff /tmp/old-schema.yaml cliter/<bc>/<module>.aurora.yaml
```

| Delta | Action |
| --- | --- |
| New field in YAML | Merge from `.origin` into existing files |
| Removed field in YAML | Remove from existing files |
| Changed field type/properties | Update in existing files |
| No change for a field | DO NOT touch |

**GOLDEN RULE: Only merge code related to fields that CHANGED in the YAML delta. Never touch code for fields that didn't change.**

### Step 1: Find All .origin Files

```bash
fd ".origin.ts"
```

### Step 2: For EACH .origin File

Read BOTH files side by side:
1. **Existing file** (has custom code + old schema)
2. **Origin file** (has NO custom code + new schema)

### Step 3: Merge Using the YAML Delta

For each change identified in Step 0, apply the appropriate merge rule. See [Merge Rules by File Type](merge-rules.md) for detailed rules per file type.

### Step 4: Preserve ALL Custom Code

- Custom class properties remain untouched
- Custom logic in method bodies is preserved
- Custom helper methods are kept
- Custom imports are retained
- Intentionally removed fields stay removed

### Step 5: Delete the .origin File

```bash
rm path/to/file.origin.ts
```

### Step 6: Verify No .origin Files Remain

```bash
fd ".origin.ts"
# Should return empty
```

---

## Handling Parameter Order

**CRITICAL:** Aurora generates parameters in the EXACT order defined in `.aurora.yaml`. When merging, the new field MUST be inserted in the correct position.

This order MUST be reflected in:
1. `register()` parameters in Aggregate
2. `register()` arguments in Mapper's `makeAggregate()`
3. `Response` constructor parameters
4. `Response` constructor arguments in Mapper's `makeResponse()`
5. Command/Query payload fields
6. Event properties

**How to determine position:** Look at the `.origin` file — Aurora already generated the correct order.

---

## Post-Merge Checklist

- [ ] No `.origin.ts` files remain (`fd ".origin.ts"` returns empty)
- [ ] All new imports are added (no missing Value Objects)
- [ ] Parameter order matches `.aurora.yaml` field order
- [ ] All custom logic is preserved (no overwrites)
- [ ] Eager loading blocks include new relationships (if any)
- [ ] Run Prettier to format (`npx prettier --write <files>`)
- [ ] TypeScript compiles without errors (`npx tsc --noEmit`)

---

## Common Mistakes

| Mistake | Prevention |
| --- | --- |
| Skipping YAML delta detection | ALWAYS diff YAML before merging |
| Adding intentionally removed fields | Check YAML delta — if field is NOT new, don't add it |
| Replacing entire file with .origin | Always compare first |
| Forgetting new imports | Check .origin imports section |
| Wrong parameter order | Match YAML field order |
| Leaving .origin files in codebase | Always delete after merge |
| Not running Prettier after merge | Run prettier on modified files |

---

## Decision Tree: How Complex Is This Merge?

```
How many .origin files?
    │
    1 file ─────────────── Simple merge
    │
    2-5 files ──────────── Medium merge (review each)
    │
    5+ files ───────────── Complex merge (plan first)

Does the existing file have custom logic?
    │
    NO (just stale hash) → Replace entirely with .origin content
    │
    YES, simple → Quick surgical merge
    │
    YES, complex (50+ lines) → Careful line-by-line merge
    │
    YES, very complex (500+ lines) → Read ENTIRE file, merge minimally
```

---

## Commands

```bash
fd ".origin.ts"                          # Find all .origin files
code -d path/to/file.ts path/to/file.origin.ts  # Compare side by side
fd ".origin.ts" -x rm {}                 # Delete all after merge
npx tsc --noEmit                         # Check TypeScript compiles
npx prettier --write "src/@app/**/*.ts"  # Format merged files
```

---

## Related Skills

| Skill | When to Use Together |
| --- | --- |
| `aurora-cli` | Triggers regeneration that creates .origin files |
| `aurora-cqrs` | Understand editable zones vs generated zones |
| `aurora-schema` | Understanding YAML field order for parameter positioning |
| `prettier` | Format files after merge |
| `conventional-commits` | Commit after successful merge |
