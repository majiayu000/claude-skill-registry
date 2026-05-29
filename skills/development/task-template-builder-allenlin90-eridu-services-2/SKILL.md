---
name: task-template-builder
description: Provides guidelines for the Task Template Builder architecture, including Schema alignment, Draft storage, Drag-and-Drop, and Validation logic.
---

# Task Template Builder Pattern

This skill documents the architecture of the Task Template Builder in `erify_studios`.

## Core Architecture

### 1. Schema Alignment (Single Source of Truth)

The Task Template Builder uses a **Shared Zod Schema** to ensure frontend and backend are always in sync.

- **Source**: `packages/api-types/src/task-management/template-definition.schema.ts`
- **Frontend Usage**: `import { FieldItemSchema } from '@eridu/api-types/task-management'`
- **Backend Usage**: `import { TemplateSchemaValidator } from '@eridu/api-types/task-management'`

> **Crucial Rule**: Never duplicate validation logic. If you need a new field or rule, update `api-types` first.

### 2. Draft Storage (IndexedDB)

To prevent data loss, drafts are saved to **IndexedDB** using `idb-keyval`.

**Why IndexedDB over localStorage?**
- **Capacity**: Task templates can be large (HTML descriptions, many fields). localStorage (5MB) runs out quickly.
- **Async**: Prevents blocking the main thread during auto-save of large objects.

**Implementation**:
```typescript
const DRAFT_KEY = 'task_template_draft';

// Load
useEffect(() => {
  get(DRAFT_KEY).then(saved => setTemplate(saved || defaultTemplate));
}, []);

// Save (Debounced)
const debouncedSave = useDebounceCallback((data) => {
  set(DRAFT_KEY, data);
}, 1000);
```

### 3. Drag and Drop (@dnd-kit)

We use `@dnd-kit/core` and `@dnd-kit/sortable` for the field list.

**Key Components**:
- `DndContext`: Wraps the list.
- `SortableContext`: Wraps the items.
- `SortableFieldItem`: Individual item component using `useSortable`.

**Constraint**:
- `dnd-kit` requires a stable `id` for every item.
- We generate a frontend-only `id` (`crypto.randomUUID()`) for every field.
- **IMPORTANT**: This `id` must be **stripped** before sending to the backend!

### 4. Advanced Validation Logic (`require_reason`)

The builder supports complex conditional validation based on field type.

**Structure**:
```typescript
require_reason: z.union([
  z.enum(['always', 'on-true', 'on-false']), // Primitive (checkbox)
  z.array(z.object({                         // Complex (number, date, select)
    op: z.enum(['lt', 'eq', 'in', ...]),
    value: z.any()
  }))
])
```

**Supported Operators per Type**:
- **Number**: `lt`, `lte`, `gt`, `gte`, `eq`, `neq`
- **Date/Datetime**: `lt` (Before), `gt` (After), `eq` (On)
- **Select**: `eq` (Is), `neq` (Is Not)
- **Multiselect**: `in` (Is One Of), `not_in` (Is Not One Of)

### 5. Payload Transformation

Before submitting to the API, the frontend payload must be transformed:

1. **Include IDs**: Keep the stable `id` fields as they are part of the shared schema.
2. **Nest Items**: specific API structure requires `{ schema: { items: [...] } }`.
3. **Filter Empty**: Remove empty options or invalid rules.

```typescript
const payload = {
  name: data.name,
  schema: {
    items: data.items.map((item) => ({
      ...item,
      options: item.options?.filter(o => o.value)
    }))
  }
};
```
