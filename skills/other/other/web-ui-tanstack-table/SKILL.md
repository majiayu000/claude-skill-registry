---
name: web-ui-tanstack-table
description: TanStack Table v8 patterns - useReactTable, column definitions, sorting, filtering, pagination, row selection, virtual scrolling, server-side data
---

# TanStack Table Patterns

> **Quick Guide:** TanStack Table is a headless UI library for building powerful tables and datagrids. Use `useReactTable` hook with `createColumnHelper` for type-safe column definitions. Import only the row models you need (`getSortedRowModel`, `getFilteredRowModel`, etc.) for tree-shaking. Memoize data and columns with `useMemo` to prevent infinite re-renders. Set `manualPagination`, `manualSorting`, `manualFiltering` to `true` for server-side data.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST memoize data and columns with `useMemo` - unstable references cause infinite re-renders)**

**(You MUST use `createColumnHelper<TData>()` for type-safe column definitions with proper TValue inference)**

**(You MUST import row models explicitly - `getSortedRowModel`, `getFilteredRowModel`, etc. - for tree-shaking)**

**(You MUST use `accessorKey` for direct property access and `accessorFn` with explicit `id` for computed values)**

**(You MUST set `manualPagination`, `manualSorting`, `manualFiltering` to `true` for server-side data)**

</critical_requirements>

---

**Auto-detection:** TanStack Table, @tanstack/react-table, useReactTable, createColumnHelper, getCoreRowModel, getSortedRowModel, getFilteredRowModel, getPaginationRowModel, ColumnDef, column definitions, table state

**When to use:**

- Building data tables with sorting, filtering, and pagination
- Implementing server-side data tables with API integration
- Creating tables with row selection and expansion
- Building virtual scrolling tables for large datasets
- Implementing column visibility controls and column ordering

**When NOT to use:**

- Simple tables without interactive features (use plain HTML tables)
- Tables with fewer than 20 rows and no sorting/filtering needs
- Read-only data display without user interaction

**Key patterns covered:**

- useReactTable hook setup with type-safe generics
- Column definitions with columnHelper
- Sorting, filtering, pagination (client-side and server-side)
- Row selection, expanding rows, column visibility
- Virtual scrolling, column pinning, column resizing

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Basic table setup, column definitions, type safety
- [examples/sorting.md](examples/sorting.md) - Column sorting with custom sort functions
- [examples/filtering.md](examples/filtering.md) - Column and global filtering
- [examples/pagination.md](examples/pagination.md) - Client-side pagination
- [examples/selection.md](examples/selection.md) - Row selection with bulk actions
- [examples/expanding.md](examples/expanding.md) - Expandable rows with sub-content
- [examples/column-visibility.md](examples/column-visibility.md) - Column visibility toggles
- [examples/server-side.md](examples/server-side.md) - Server-side data handling
- [examples/virtualization.md](examples/virtualization.md) - Virtual scrolling for large datasets
- [examples/column-pinning.md](examples/column-pinning.md) - Sticky pinned columns (left/right)
- [examples/column-resizing.md](examples/column-resizing.md) - Performant column resizing with CSS variables
- [reference.md](reference.md) - Decision frameworks, checklists, anti-patterns

---

<philosophy>

## Philosophy

TanStack Table is a **headless UI library** - it provides the logic for tables without any markup or styles. This gives you complete control over rendering while the library handles complex state management for sorting, filtering, pagination, and more.

**Core Principles:**

1. **Headless Architecture** - No pre-built components. You own the markup and styling.
2. **Type Safety** - Full TypeScript support with generics for data types.
3. **Tree-Shakable** - Import only what you use. Each feature is a separate row model.
4. **Framework Agnostic** - Same API works across React, Vue, Solid, and Svelte.
5. **Performant** - Optimized for large datasets with virtualization support.

**Why Headless?**

The headless approach means TanStack Table handles the hard parts (state management, sorting algorithms, pagination logic) while you control presentation. This is ideal when:

- You need custom table designs that don't fit pre-built components
- You're integrating with an existing design system
- You need maximum performance control

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Table Setup

Set up a type-safe table with `useReactTable` and `createColumnHelper`. See [examples/core.md](examples/core.md) for complete implementation.

```typescript
const columnHelper = createColumnHelper<User>();

const columns = useMemo(
  () => [
    columnHelper.accessor("firstName", { header: "First Name" }),
    // accessorFn for computed values - MUST include id
    columnHelper.accessor((row) => `${row.firstName} ${row.lastName}`, {
      id: "fullName",
      header: "Full Name",
    }),
  ],
  [],
);

const data = useMemo(() => users, [users]);

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getRowId: (row) => row.id,
});
```

**Critical:** Memoize both `columns` and `data` - unstable references cause infinite re-renders.

---

### Pattern 2: Sorting

Enable sorting with `getSortedRowModel` and controlled state. See [examples/sorting.md](examples/sorting.md).

```typescript
const [sorting, setSorting] = useState<SortingState>([]);

const table = useReactTable({
  data,
  columns,
  state: { sorting },
  onSortingChange: setSorting,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
});

// In column def:
columnHelper.accessor("createdAt", {
  header: "Created",
  sortingFn: "datetime", // Required for Date objects
});
```

**Gotcha:** Dates don't sort correctly with default sort. Use `sortingFn: "datetime"` for Date columns.

---

### Pattern 3: Filtering

Column filters and global filter with `getFilteredRowModel`. See [examples/filtering.md](examples/filtering.md).

```typescript
const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
const [globalFilter, setGlobalFilter] = useState("");

const table = useReactTable({
  data,
  columns,
  state: { columnFilters, globalFilter },
  onColumnFiltersChange: setColumnFilters,
  onGlobalFilterChange: setGlobalFilter,
  getCoreRowModel: getCoreRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
});
```

**Gotcha:** Multiple column filters combine with AND logic, not OR. Use global filter or custom logic for OR behavior.

---

### Pattern 4: Pagination

Client-side and server-side pagination with `getPaginationRowModel`. See [examples/pagination.md](examples/pagination.md).

```typescript
const DEFAULT_PAGE_SIZE = 10;

const [pagination, setPagination] = useState<PaginationState>({
  pageIndex: 0,
  pageSize: DEFAULT_PAGE_SIZE,
});

const table = useReactTable({
  data,
  columns,
  state: { pagination },
  onPaginationChange: setPagination,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
});
```

**Gotcha:** `pageIndex` is 0-based internally, but many APIs are 1-based. Add 1 when sending to server.

---

### Pattern 5: Row Selection

Single and multi-row selection. See [examples/selection.md](examples/selection.md).

```typescript
const [rowSelection, setRowSelection] = useState<RowSelectionState>({});

const table = useReactTable({
  data,
  columns,
  state: { rowSelection },
  onRowSelectionChange: setRowSelection,
  getCoreRowModel: getCoreRowModel(),
  enableRowSelection: true,
  getRowId: (row) => row.id, // CRITICAL: Stable IDs for selection
});
```

**Critical:** Without `getRowId`, selection uses array indices which break when data is re-ordered or filtered.

---

### Pattern 6: Server-Side Data

Handle server-side pagination, sorting, and filtering. See [examples/server-side.md](examples/server-side.md).

```typescript
const table = useReactTable({
  data: apiData ?? [],
  columns,
  state: { pagination, sorting, columnFilters },
  onPaginationChange: setPagination,
  onSortingChange: setSorting,
  onColumnFiltersChange: setColumnFilters,
  getCoreRowModel: getCoreRowModel(),
  // CRITICAL: All three manual flags for server-side
  manualPagination: true,
  manualSorting: true,
  manualFiltering: true,
  rowCount: totalFromApi,
});
```

**Critical:** Do NOT import client-side row models (`getSortedRowModel`, etc.) with `manual*: true` - they are redundant.

---

### Pattern 7: Column Visibility

Toggle column visibility. See [examples/column-visibility.md](examples/column-visibility.md).

```typescript
const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({
  email: false, // Hide by default
});

// In column def - prevent hiding required columns:
columnHelper.accessor("id", { enableHiding: false });
```

---

### Pattern 8: Expanding Rows

Expandable rows for hierarchical data or detail views. See [examples/expanding.md](examples/expanding.md).

```typescript
const [expanded, setExpanded] = useState<ExpandedState>({});

const table = useReactTable({
  data,
  columns,
  state: { expanded },
  onExpandedChange: setExpanded,
  getCoreRowModel: getCoreRowModel(),
  getExpandedRowModel: getExpandedRowModel(),
  getRowCanExpand: () => true,
});
```

---

### Pattern 9: Reusable Generic Table Component

Leverage TypeScript generics for a reusable table component. See [examples/core.md](examples/core.md).

```typescript
interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export function DataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });
  // ... render table
}
```

---

### Pattern 10: Column Pinning

Keep columns visible during horizontal scroll. See [examples/column-pinning.md](examples/column-pinning.md).

```typescript
const [columnPinning, setColumnPinning] = useState<ColumnPinningState>({
  left: ["id"],
  right: ["actions"],
});
```

**Critical:** Pinning provides state only. You must apply `position: sticky` and background CSS yourself to prevent content overlap.

---

### Pattern 11: Column Resizing

User-adjustable column widths. See [examples/column-resizing.md](examples/column-resizing.md).

```typescript
const table = useReactTable({
  data,
  columns,
  columnResizeMode: "onChange", // or "onEnd" for simpler, more performant
  enableColumnResizing: true,
});
```

**Critical:** `columnResizeMode: "onChange"` requires CSS variables pattern and memoized table body for 60fps performance. Use `"onEnd"` for simpler cases.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Missing useMemo on columns/data** - Columns or data defined inline without memoization cause infinite re-renders. Must be memoized or defined outside the component.
- **accessorFn without id** - Using `accessorFn` without providing an `id` causes runtime errors.
- **Missing manualPagination for server-side** - Forgetting `manualPagination: true` when using server-side data causes the table to paginate already-paginated data.
- **Returning JSX from accessorFn** - Accessors return primitive values for sorting/filtering. Use the `cell` option for JSX rendering.

**Medium Priority Issues:**

- **Not providing rowCount for server-side** - Without `rowCount` or `pageCount`, the table cannot calculate correct page count.
- **Missing getRowId with selection** - Without `getRowId`, row selection uses array indices which break on sort/filter.
- **Not using flexRender** - Manually rendering header/cell values breaks when columnDef uses a function for header/cell.

**Gotchas & Edge Cases:**

- Date sorting requires `sortingFn: "datetime"` - JavaScript dates don't sort correctly by default
- Column filters are AND, not OR - Multiple column filters combine with AND logic
- `pageIndex` is 0-based - Many APIs use 1-based; add 1 when sending to server
- `autoResetPageIndex` defaults to `true` - Page resets to 0 when data changes; set to `false` for server-side
- Column pinning requires sticky CSS - TanStack Table provides state only, you apply CSS
- `columnResizeMode: "onChange"` needs CSS variables + memoized body for performance
- Attach `getResizeHandler` to both `onMouseDown` and `onTouchStart` for mobile support
- Pinning affects column order - Pinning, column ordering, and grouping all reorder columns; pinning happens first
- Pinned cells need background color - Otherwise scrolling content shows through

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST memoize data and columns with `useMemo` - unstable references cause infinite re-renders)**

**(You MUST use `createColumnHelper<TData>()` for type-safe column definitions with proper TValue inference)**

**(You MUST import row models explicitly - `getSortedRowModel`, `getFilteredRowModel`, etc. - for tree-shaking)**

**(You MUST use `accessorKey` for direct property access and `accessorFn` with explicit `id` for computed values)**

**(You MUST set `manualPagination`, `manualSorting`, `manualFiltering` to `true` for server-side data)**

**Failure to follow these rules will cause infinite re-renders, TypeScript errors, and incorrect server-side behavior.**

</critical_reminders>
