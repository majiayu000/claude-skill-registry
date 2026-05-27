---
name: component-patterns
description: Guidelines for organizing React components in Shadow Master. Use when creating new components, deciding between single-file vs subfolder structure, or adding character creation cards.
allowed-tools: Read, Grep, Glob
---

# Component Organization Patterns

Guidelines for structuring React components in the Shadow Master codebase.

## Decision Flowchart

```
Does the component have modals?
├─ Yes → Create subfolder, extract modals
└─ No → Does it have reusable Row/ListItem components?
        ├─ Yes, used elsewhere → Create subfolder
        └─ No → Keep as single file with internal helpers
```

---

## When to Use a Subfolder

Create a subfolder with `index.ts` when:

- Component has one or more **modals** (selection dialogs, forms, etc.)
- Component has **reusable row/list item** components used in multiple places
- Component exceeds ~600 lines with clear separable concerns
- Component has distinct UI pieces that could be tested independently

**Subfolder structure:**

```
/components/creation/qualities/
├── QualitiesCard.tsx        # Main card component
├── QualityModal.tsx         # Selection/edit modal
├── QualityRow.tsx           # Optional: if row is complex/reusable
├── index.ts                 # Re-exports public components
```

**Index file pattern:**

```typescript
// index.ts - export only public API
export { QualitiesCard } from "./QualitiesCard";
export { QualityModal } from "./QualityModal"; // Only if used externally
```

---

## When to Keep as Single File

Keep as a single file when:

- Component is self-contained with only **internal helper components**
- Internal components are tightly coupled and only make sense within the parent
- Component is under ~400 lines with straightforward structure
- No modals or independently reusable pieces

---

## Creation Component Subfolders

Current organization (15 directories, 89 total components):

| Folder                 | Components | Pattern                                |
| ---------------------- | ---------- | -------------------------------------- |
| `/armor`               | 4          | Panel + Row + PurchaseModal + ModModal |
| `/augmentations`       | 4          | 4 specialized modals                   |
| `/contacts`            | 2          | Card + Modal + support files           |
| `/foci`                | 2          | Card + Modal                           |
| `/gear`                | 4          | Panel + Row + 2 Modals                 |
| `/identities`          | 6          | Card + 3 modal types                   |
| `/knowledge-languages` | 5          | Card + 2 Row types + 2 Modals          |
| `/magic-path`          | 2          | Card + Modal + utilities               |
| `/matrix-gear`         | 3          | Card + 2 specialized modals            |
| `/metatype`            | 2          | Card + Modal + support files           |
| `/qualities`           | 3          | Card + SelectionModal + DetailCard     |
| `/shared`              | 10         | Reusable utilities and hooks           |
| `/skills`              | 5          | 5 specialized modals                   |
| `/vehicles`            | 4          | 4 specialized modals                   |
| `/weapons`             | 4          | Row + 3 Modals                         |

---

## Adding a New Character Creation Card

1. **Determine if card needs subfolder** (see decision flowchart above)
   - Has modals? → Create subfolder with `index.ts`
   - Simple with internal helpers? → Single file is fine

2. **Create card component** in `/components/creation/` or `/components/creation/{feature}/`

3. **Follow the `CreationCard` wrapper pattern** from `/components/creation/shared/`

4. **Add to `SheetCreationLayout.tsx`** in the appropriate column

5. **Update `CreationState` type** in `/lib/types/creation.ts` if needed

6. **Export from `/components/creation/index.ts`**

---

## Adding a New API Endpoint

1. Create `/app/api/{path}/route.ts`
2. Export HTTP method handlers (GET, POST, PUT, DELETE)
3. Follow authentication pattern (getSession → validate user)
4. Call storage layer functions
5. Return JSON responses

---

## Adding a New Ruleset Module

1. Define module type in `/lib/types/edition.ts`
2. Add module to book payload in `/data/editions/{editionCode}/`
3. Update merge logic in `/lib/rules/merge.ts` if special handling needed
4. Create hook in `RulesetContext.tsx` for easy access

---

## Key Reference Files

- `components/creation/shared/CreationCard.tsx` - Card wrapper pattern
- `components/creation/SkillsCard.tsx` - Modal-based editing example
- `components/creation/AugmentationsCard.tsx` - Category tabs + list
- `app/characters/create/sheet/components/SheetCreationLayout.tsx` - Three-column layout
