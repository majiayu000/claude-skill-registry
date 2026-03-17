---
name: using-nuqs
description: Manage React state in URL query parameters with nuqs. Covers Suspense boundaries, parsers, clearing state, and deep-linkable dialogs.
---

# Working with nuqs

Manage React state in URL query parameters with nuqs. Covers Suspense boundaries, parsers, clearing state, and deep-linkable dialogs.

## Implement Working with nuqs

Manage React state in URL query parameters with nuqs for shareable filters, search, and deep-linkable dialogs.

**See:**

- Resource: `using-nuqs` in Fullstack Recipes
- URL: https://fullstackrecipes.com/recipes/using-nuqs

---

### Suspense Boundary Pattern

nuqs uses `useSearchParams` behind the scenes, requiring a Suspense boundary. Wrap nuqs-using components with Suspense via a wrapper component to keep the boundary colocated:

```typescript
import { Suspense } from "react";

type SearchInputProps = {
  placeholder?: string;
};

// Public component with built-in Suspense
export function SearchInput(props: SearchInputProps) {
  return (
    <Suspense fallback={<input placeholder={props.placeholder} disabled />}>
      <SearchInputClient {...props} />
    </Suspense>
  );
}
```

```typescript
"use client";

import { useQueryState, parseAsString } from "nuqs";

// Internal client component that uses nuqs
function SearchInputClient({ placeholder = "Search..." }: SearchInputProps) {
  const [search, setSearch] = useQueryState("q", parseAsString.withDefault(""));

  return (
    <input
      value={search}
      onChange={(e) => setSearch(e.target.value || null)}
      placeholder={placeholder}
    />
  );
}
```

This pattern allows consuming components to use `SearchInput` without adding Suspense themselves.

### State to URL Query Params

Replace `useState` with `useQueryState` to sync state to the URL:

```typescript
"use client";

import {
  useQueryState,
  parseAsString,
  parseAsBoolean,
  parseAsArrayOf,
} from "nuqs";

// String state (search, filters)
const [search, setSearch] = useQueryState("q", parseAsString.withDefault(""));

// Boolean state (toggles)
const [showArchived, setShowArchived] = useQueryState(
  "archived",
  parseAsBoolean.withDefault(false),
);

// Array state (multi-select)
const [tags, setTags] = useQueryState(
  "tags",
  parseAsArrayOf(parseAsString).withDefault([]),
);
```

### Clear State

Set to `null` to remove from URL:

```typescript
// Clear single param
setSearch(null);

// Clear all filters
function clearFilters() {
  setSearch(null);
  setTags(null);
  setShowArchived(null);
}
```

When using `.withDefault()`, setting to `null` clears the URL param but returns the default value.

### Deep-Linkable Dialogs

Control dialog visibility with URL params for shareable links:

```typescript
import { Suspense } from "react";

type DeleteDialogProps = {
  onDelete: (id: string) => Promise<void>;
};

// Public component with built-in Suspense
export function DeleteDialog(props: DeleteDialogProps) {
  return (
    <Suspense fallback={null}>
      <DeleteDialogClient {...props} />
    </Suspense>
  );
}
```

```typescript
"use client";

import { useQueryState, parseAsString } from "nuqs";
import { AlertDialog, AlertDialogContent } from "@/components/ui/alert-dialog";

function DeleteDialogClient({ onDelete }: DeleteDialogProps) {
  const [deleteId, setDeleteId] = useQueryState("delete", parseAsString);

  async function handleDelete() {
    if (!deleteId) return;
    await onDelete(deleteId);
    setDeleteId(null);
  }

  return (
    <AlertDialog open={!!deleteId} onOpenChange={(open) => !open && setDeleteId(null)}>
      <AlertDialogContent>
        {/* Confirmation UI */}
        <Button onClick={handleDelete}>Delete</Button>
      </AlertDialogContent>
    </AlertDialog>
  );
}
```

Open the dialog programmatically:

```typescript
// Open delete dialog for specific item
setDeleteId("item-123");

// Deep link: /items?delete=item-123
```

### Opening Dialogs from Buttons

Use a trigger button to open the dialog:

```typescript
function ItemRow({ item }: { item: Item }) {
  const [, setDeleteId] = useQueryState("delete", parseAsString);

  return (
    <Button variant="ghost" onClick={() => setDeleteId(item.id)}>
      Delete
    </Button>
  );
}
```

---

## References

- [nuqs Documentation](https://nuqs.47ng.com/)
- [nuqs Parsers](https://nuqs.47ng.com/docs/parsers)
