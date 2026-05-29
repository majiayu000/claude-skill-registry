# Content Collections & Ordering

## Overview

Content is organized into collections in `src/content/`. The single source of truth for collection order is `COLLECTION_NAMES` in `src/utils/collections-config.ts`.

| Collection | Path | Purpose |
|------------|------|---------|
| Concepts | `src/content/concepts/` | Foundational knowledge for AI-assisted work |
| Prompt Engineering | `src/content/prompt-engineering/` | How you write and structure prompts |
| Context Engineering | `src/content/context-engineering/` | What info AI has access to and when |
| Workflow & Guardrails | `src/content/workflow-guardrails/` | How you guide AI through a task |
| Failure Modes | `src/content/failure-modes/` | What goes wrong |
| Tools | `src/content/tools/` | AI coding assistants |

## Ordering: Linked List via `dependsOn`

Instead of numerical ordering (`order: 1, 2, 3`), content uses a **linked list** approach where each item points to its prerequisite.

### Schema

```typescript
// src/content/config.ts
schema: z.object({
  title: z.string(),
  dependsOn: z.string().optional(), // slug of prerequisite
})
```

### Example Chain

```yaml
# large-language-models.md (HEAD - no dependsOn)
---
title: Large Language Models
---

# context.md
---
title: Context
dependsOn: large-language-models
---

# tools.md
---
title: Tools
dependsOn: context
---
```

**Result:** LLMs → Context → Tools

### Why Linked Lists?

1. **Insert anywhere** - Add new content by pointing to predecessor, update successor
2. **No renumbering** - Unlike `order: 1, 2, 3` where inserting means updating all subsequent items
3. **Semantic** - `dependsOn` documents prerequisites, not just position

## Sorting Implementation

The sorting logic lives in `src/utils/sortByDependency.ts`:

```typescript
import { sortCollectionByDependency } from '../utils/sortByDependency';

const concepts = sortCollectionByDependency(await getCollection("concepts"));
```

**Algorithm:** Topological sort - finds items with no `dependsOn` (heads), then walks the chain.

## Adding New Content

1. Create the markdown file in the appropriate collection folder
2. Set `dependsOn` to the slug of what should come before it
3. If inserting between A and B: set new item's `dependsOn` to A, update B's `dependsOn` to new item

## Adding New Collections

To add a new collection:

1. Create the directory: `src/content/new-collection/`
2. Add to `src/content/config.ts` schema
3. Add to `COLLECTION_NAMES` array in `src/utils/collections-config.ts` (this controls order)
4. Add to `COLLECTION_CONFIG` in the same file (display name, description, sort method)
5. Add to `AnyCollectionEntry` type in `src/utils/collections.ts`

Everything else (sidebar, pages, navigation) will automatically pick up the new collection.

## Tests

Run `npm test` - the sorting logic has 22 tests covering:
- Empty/single items
- Simple chains
- Multiple independent chains
- Missing dependencies (treated as heads)
- Cycle handling
- Deterministic ordering

## Files

| File | Purpose |
|------|---------|
| `src/content/config.ts` | Schema definitions |
| `src/utils/collections-config.ts` | Collection names, order, and metadata |
| `src/utils/collections.ts` | Astro integration and fetching |
| `src/utils/sortByDependency.ts` | Sorting utility |
| `src/utils/sortByDependency.test.ts` | Test suite |
| `src/layouts/Layout.astro` | Uses sorting for nav |
