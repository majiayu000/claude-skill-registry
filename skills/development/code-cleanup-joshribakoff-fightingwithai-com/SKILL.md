# Code Cleanup Skill

## When to Use

After iterating on code with multiple changes, reversals, or simplifications - technical debt accumulates. Use this skill to systematically identify and clean it up.

**Triggers:**
- "clean up the code"
- "look for technical debt"
- "we iterated a lot, what can we simplify"
- After any feature that went through multiple revisions

## Process

### Phase 1: Audit (Don't Change Code Yet)

1. **Identify files touched** - What files were modified during iteration?

2. **Look for these patterns:**

   | Pattern | Description | Example |
   |---------|-------------|---------|
   | **Duplicated code** | Same logic/styles in multiple files | CSS copied across 3 pages |
   | **Dead code** | Unused functions, props, variables | `prev` prop passed but never used |
   | **Vestigial code** | Leftovers from removed features | `extractDescription()` for deleted UI |
   | **Inconsistent patterns** | Same thing done different ways | `flex` vs `text-align` for alignment |
   | **Over-abstraction** | Complexity added then never used | Interface with 5 fields, 2 used |
   | **Under-abstraction** | Copy-paste that should be shared | 3 nearly-identical page templates |
   | **Nested ternaries** | Complex conditional rendering inline | 20-line ternary in layout template |
   | **Hardcoded variants** | Multiple files differing only in config values | 3 index pages with different titles |
   | **Repeated inline logic** | Same operation duplicated across files | `.sort((a, b) => ...)` in 5 places |

3. **Prioritize by impact:**
   - **High**: Dead code, unused props (easy wins, remove confusion)
   - **Medium**: Duplicated code (DRY violations, maintenance burden)
   - **Low**: Inconsistencies (style issues, not bugs)

4. **Create a summary** - List issues with line counts and fix complexity before touching code.

### Phase 2: Checkpoint

Before making cleanup changes:
1. Commit current working state
2. Use a clear message like "checkpoint before cleanup" or "feature complete, cleanup pending"

This ensures you can always get back to working code if cleanup introduces issues.

### Phase 3: Fix (In Order)

1. **Quick wins first** - Delete dead code, remove unused props
2. **Then consolidation** - Extract shared components/styles
3. **Finally polish** - Fix inconsistencies

After each logical chunk, verify the app still works.

## Common Cleanup Patterns

### Extracting Nested Ternaries

Nested ternaries in Astro/JSX are hard to read and modify. Extract to components when you see:
- Multiple conditions determining what to render
- Same HTML structure repeated with slight variations
- Logic mixing with markup in confusing ways

```astro
<!-- Before: nested ternary spanning 20+ lines -->
{conditionA && conditionB ? (
  <nav>
    {subCondition ? <a href="/">{x}</a> : <span>{x}</span>}
    <span>{y}</span>
  </nav>
) : conditionA ? (
  <nav>
    <span>{x}</span>
  </nav>
) : (
  <span>Fallback</span>
)}

<!-- After: clean component usage -->
<MyBreadcrumbs
  sectionName={sectionName}
  sectionSlug={sectionSlug}
  pageTitle={pageTitle}
/>
```

The component encapsulates the logic with clear variable names at the top:
```astro
---
const hasFullPath = currentSection && pageTitle;
const hasSectionOnly = currentSection && !pageTitle;
---
{hasFullPath ? (...) : hasSectionOnly ? (...) : (...)}
```

This moves complexity to one place and makes the parent template scannable.

### Consolidating Hardcoded Variants

When you see multiple files that are nearly identical with only small differences (title, description, sort method), consolidate into a single dynamic file with configuration.

**Signs of this problem:**
- 3+ files with same structure, different hardcoded values
- Copy-paste when adding new variants
- Changes need to be made in multiple places

```astro
<!-- Before: 3 separate files (concepts/index, patterns/index, failure-modes/index) -->
<!-- Each 30+ lines, differing only in: collection name, title, description, sort method -->

<!-- After: ONE dynamic [collection]/index.astro + config -->
```

**The fix pattern:**
1. Create a config object with all variant-specific values
2. Create one dynamic page that reads from config
3. Delete the hardcoded files

```typescript
// src/utils/collections-config.ts
export const COLLECTION_CONFIG = {
  "concepts": { displayName: "Concepts", sortMethod: "dependency", description: "..." },
  "failure-modes": { displayName: "Failure Modes", sortMethod: "alphabetical", description: "..." },
  // ...
};

// src/pages/[collection]/index.astro
const config = COLLECTION_CONFIG[collection];
```

### Separating Pure Functions from Framework Code

When testing fails because of framework imports (`astro:content`, `next/router`, etc.), split into two files:

```
collections-config.ts  ← Pure TypeScript, testable
collections.ts         ← Re-exports config + adds framework-specific functions
```

The test imports from the `-config` file, production code imports from the main file.

### Removing Dead Props

```typescript
// Before: prop accepted but never used
interface Props {
  prev: Item | null;  // ← dead
  next: Item | null;
}
const { prev, next } = Astro.props;
// prev never referenced...

// After: remove from interface and callers
interface Props {
  next: Item | null;
}
```

### Extracting Shared Styles

```astro
<!-- Before: duplicated in 3 files -->
<style>
  .nav { text-align: right; padding-top: var(--space-4); ... }
</style>

<!-- After: shared component or global styles -->
<NavFooter href="/next/" label="Next Item" />
```

### Removing Vestigial Functions

Look for functions that:
- Are defined but never called
- Return values that are stored but never used
- Compute things for UI elements that were removed

## Checklist

- [ ] Read all modified files
- [ ] List dead code (unused functions, props, variables)
- [ ] List duplicated code (same logic in multiple places)
- [ ] List inconsistencies (different approaches to same problem)
- [ ] Prioritize fixes
- [ ] Commit checkpoint before changes
- [ ] Make changes in priority order
- [ ] Verify app works after each chunk
- [ ] Final commit with cleanup summary

## Anti-Patterns to Avoid

- **Don't refactor while cleaning** - Cleanup removes debt, refactoring changes structure. Do one at a time.
- **Don't add features during cleanup** - Keep the diff focused on removal/consolidation.
- **Don't skip the checkpoint** - You'll regret it when cleanup breaks something subtle.
