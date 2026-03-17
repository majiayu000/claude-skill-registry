---
name: web-ui-tanstack-table
description: TanStack Table v8 patterns - useReactTable, column definitions, sorting, filtering, pagination, row selection, virtual scrolling, server-side data
---

# TanStack Table Patterns

> **Quick Guide:** TanStack Table is a headless UI library for building powerful tables and datagrids. Use `useReactTable` hook with `createColumnHelper` for type-safe column definitions. Import only the row models you need (`getSortedRowModel`, `getFilteredRowModel`, etc.) for tree-shaking. Memoize data and columns with `useMemo` to prevent infinite re-renders.

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

**Key patterns covered:**

- useReactTable hook setup with type-safe generics
- Column definitions with columnHelper
- Sorting state and getSortedRowModel
- Filtering with column filters and global filter
- Pagination with client-side and server-side patterns
- Row selection with single/multi-select modes
- Expanding rows and sub-rows
- Virtual scrolling integration
- Column pinning (left/right sticky columns)
- Column resizing with CSS variables for performance

**When NOT to use:**

- Simple tables without interactive features (use plain HTML tables)
- Tables with fewer than 20 rows and no sorting/filtering needs
- Read-only data display without user interaction

**Detailed Resources:**

- For core code examples, see [examples/core.md](examples/core.md)
- For sorting patterns, see [examples/sorting.md](examples/sorting.md)
- For filtering patterns, see [examples/filtering.md](examples/filtering.md)
- For pagination patterns, see [examples/pagination.md](examples/pagination.md)
- For row selection patterns, see [examples/selection.md](examples/selection.md)
- For expandable rows, see [examples/expanding.md](examples/expanding.md)
- For column visibility, see [examples/column-visibility.md](examples/column-visibility.md)
- For server-side data handling, see [examples/server-side.md](examples/server-side.md)
- For virtual scrolling, see [examples/virtualization.md](examples/virtualization.md)
- For column pinning, see [examples/column-pinning.md](examples/column-pinning.md)
- For column resizing, see [examples/column-resizing.md](examples/column-resizing.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

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

### Pattern 1: Basic Table Setup with useReactTable

Set up a type-safe table with the `useReactTable` hook and `createColumnHelper`.

#### Type Definitions

```typescript
// types.ts
export type User = {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  status: "active" | "inactive";
  createdAt: Date;
};
```

#### Column Helper Setup

```typescript
import { createColumnHelper } from "@tanstack/react-table";
import type { User } from "./types";

const columnHelper = createColumnHelper<User>();
```

#### Column Definitions (Memoized)

```typescript
import { useMemo } from "react";
import {
  createColumnHelper,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import type { User } from "./types";

const columnHelper = createColumnHelper<User>();

export function UserTable({ data }: { data: User[] }) {
  // CRITICAL: Memoize columns to prevent infinite re-renders
  const columns = useMemo(
    () => [
      // accessorKey for direct property access
      columnHelper.accessor("firstName", {
        header: "First Name",
        cell: (info) => info.getValue(),
      }),
      columnHelper.accessor("lastName", {
        header: "Last Name",
      }),
      columnHelper.accessor("email", {
        header: "Email",
      }),
      // accessorFn for computed values - MUST include id
      columnHelper.accessor((row) => `${row.firstName} ${row.lastName}`, {
        id: "fullName",
        header: "Full Name",
      }),
      columnHelper.accessor("status", {
        header: "Status",
        cell: (info) => (
          <span data-status={info.getValue()}>{info.getValue()}</span>
        ),
      }),
    ],
    []
  );

  // CRITICAL: Memoize data or define outside component
  const memoizedData = useMemo(() => data, [data]);

  const table = useReactTable({
    data: memoizedData,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th key={header.id}>
                {header.isPlaceholder
                  ? null
                  : flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map((row) => (
          <tr key={row.id}>
            {row.getVisibleCells().map((cell) => (
              <td key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

**Why good:** `createColumnHelper<User>()` provides full type inference for accessors, memoized columns prevent re-render loops, explicit row model imports enable tree-shaking, `accessorFn` with `id` enables computed columns

---

### Pattern 2: Sorting

Enable sorting with `getSortedRowModel` and manage sorting state.

#### Sorting Implementation

```typescript
import { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
} from "@tanstack/react-table";
import type { SortingState } from "@tanstack/react-table";

export function SortableTable({ data }: { data: User[] }) {
  const [sorting, setSorting] = useState<SortingState>([]);

  const columns = useMemo(
    () => [
      columnHelper.accessor("firstName", {
        header: "First Name",
        enableSorting: true, // default is true
      }),
      columnHelper.accessor("email", {
        header: "Email",
        enableSorting: true,
      }),
      columnHelper.accessor("createdAt", {
        header: "Created",
        // Custom sort function for dates
        sortingFn: "datetime",
      }),
      columnHelper.accessor("status", {
        header: "Status",
        enableSorting: false, // Disable sorting for this column
      }),
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map((headerGroup) => (
          <tr key={headerGroup.id}>
            {headerGroup.headers.map((header) => (
              <th
                key={header.id}
                onClick={header.column.getToggleSortingHandler()}
                style={{ cursor: header.column.getCanSort() ? "pointer" : "default" }}
              >
                {flexRender(header.column.columnDef.header, header.getContext())}
                {/* Sort direction indicator */}
                {{
                  asc: " ↑",
                  desc: " ↓",
                }[header.column.getIsSorted() as string] ?? null}
              </th>
            ))}
          </tr>
        ))}
      </thead>
      {/* ... tbody */}
    </table>
  );
}
```

**Why good:** controlled sorting state enables persistence and URL sync, `getSortedRowModel()` handles sorting logic, built-in sort functions for common types (datetime, alphanumeric), column-level `enableSorting` control

---

### Pattern 3: Filtering

Implement column filters and global filter with `getFilteredRowModel`.

#### Column Filtering

```typescript
import { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getFilteredRowModel,
  flexRender,
} from "@tanstack/react-table";
import type { ColumnFiltersState } from "@tanstack/react-table";

export function FilterableTable({ data }: { data: User[] }) {
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState("");

  const columns = useMemo(
    () => [
      columnHelper.accessor("firstName", {
        header: "First Name",
        enableColumnFilter: true,
      }),
      columnHelper.accessor("status", {
        header: "Status",
        // Custom filter function
        filterFn: (row, columnId, filterValue) => {
          return row.getValue(columnId) === filterValue;
        },
      }),
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    state: {
      columnFilters,
      globalFilter,
    },
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
  });

  return (
    <div>
      {/* Global filter input */}
      <input
        type="text"
        value={globalFilter ?? ""}
        onChange={(e) => setGlobalFilter(e.target.value)}
        placeholder="Search all columns..."
      />

      <table>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id}>
                  {flexRender(header.column.columnDef.header, header.getContext())}
                  {/* Column filter input */}
                  {header.column.getCanFilter() && (
                    <input
                      type="text"
                      value={(header.column.getFilterValue() as string) ?? ""}
                      onChange={(e) => header.column.setFilterValue(e.target.value)}
                      placeholder={`Filter ${header.column.id}...`}
                    />
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        {/* ... tbody */}
      </table>
    </div>
  );
}
```

**Why good:** separate state for column and global filters, custom `filterFn` enables complex filtering logic, built-in filter functions available (includesString, equals, etc.)

---

### Pattern 4: Pagination

Implement client-side and server-side pagination with `getPaginationRowModel`.

#### Client-Side Pagination

```typescript
import { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getPaginationRowModel,
  flexRender,
} from "@tanstack/react-table";
import type { PaginationState } from "@tanstack/react-table";

const DEFAULT_PAGE_SIZE = 10;

export function PaginatedTable({ data }: { data: User[] }) {
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

  return (
    <div>
      <table>{/* ... table content */}</table>

      {/* Pagination controls */}
      <div>
        <button
          onClick={() => table.firstPage()}
          disabled={!table.getCanPreviousPage()}
        >
          First
        </button>
        <button
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </button>
        <span>
          Page {table.getState().pagination.pageIndex + 1} of{" "}
          {table.getPageCount()}
        </span>
        <button
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </button>
        <button
          onClick={() => table.lastPage()}
          disabled={!table.getCanNextPage()}
        >
          Last
        </button>
        <select
          value={pagination.pageSize}
          onChange={(e) => table.setPageSize(Number(e.target.value))}
        >
          {[10, 20, 50, 100].map((size) => (
            <option key={size} value={size}>
              Show {size}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
```

**Why good:** controlled pagination state for URL persistence, built-in navigation methods (`firstPage`, `previousPage`, etc.), `getCanPreviousPage`/`getCanNextPage` for button states

---

### Pattern 5: Row Selection

Implement single and multi-row selection with `enableRowSelection`.

#### Multi-Select with Checkboxes

```typescript
import { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";
import type { RowSelectionState } from "@tanstack/react-table";

export function SelectableTable({ data }: { data: User[] }) {
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});

  const columns = useMemo(
    () => [
      // Selection checkbox column
      columnHelper.display({
        id: "select",
        header: ({ table }) => (
          <input
            type="checkbox"
            checked={table.getIsAllRowsSelected()}
            ref={(input) => {
              if (input) {
                input.indeterminate = table.getIsSomeRowsSelected();
              }
            }}
            onChange={table.getToggleAllRowsSelectedHandler()}
          />
        ),
        cell: ({ row }) => (
          <input
            type="checkbox"
            checked={row.getIsSelected()}
            disabled={!row.getCanSelect()}
            onChange={row.getToggleSelectedHandler()}
          />
        ),
      }),
      columnHelper.accessor("firstName", { header: "First Name" }),
      // ... other columns
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    state: { rowSelection },
    onRowSelectionChange: setRowSelection,
    getCoreRowModel: getCoreRowModel(),
    enableRowSelection: true, // Enable selection for all rows
    // Or use a function for conditional selection:
    // enableRowSelection: (row) => row.original.status === "active",
  });

  // Access selected rows
  const selectedRows = table.getSelectedRowModel().rows;

  return (
    <div>
      <p>Selected: {selectedRows.length} rows</p>
      <table>{/* ... table content */}</table>
    </div>
  );
}
```

**Why good:** `display` column for non-data columns like checkboxes, conditional selection with function, `getSelectedRowModel()` provides easy access to selected data

---

### Pattern 6: Column Visibility

Toggle column visibility with visibility state.

#### Visibility Controls

```typescript
import { useState } from "react";
import { useReactTable, getCoreRowModel } from "@tanstack/react-table";
import type { VisibilityState } from "@tanstack/react-table";

export function TableWithColumnVisibility({ data }: { data: User[] }) {
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({
    email: false, // Hide email column by default
  });

  const table = useReactTable({
    data,
    columns,
    state: { columnVisibility },
    onColumnVisibilityChange: setColumnVisibility,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div>
      {/* Column visibility toggles */}
      <div>
        {table.getAllLeafColumns().map((column) => (
          <label key={column.id}>
            <input
              type="checkbox"
              checked={column.getIsVisible()}
              onChange={column.getToggleVisibilityHandler()}
              disabled={!column.getCanHide()}
            />
            {column.id}
          </label>
        ))}
      </div>

      <table>
        {/* Use getVisibleLeafColumns and getVisibleCells */}
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id}>
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

**Why good:** visibility state for persistence, `enableHiding: false` on columns that should always be visible, `getVisibleCells()` automatically respects visibility

---

### Pattern 7: Expanding Rows

Implement expandable rows for hierarchical data or detail views.

#### Expandable Rows

```typescript
import { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getExpandedRowModel,
  flexRender,
  createColumnHelper,
} from "@tanstack/react-table";
import type { ExpandedState } from "@tanstack/react-table";

const columnHelper = createColumnHelper<User>();

export function ExpandableTable({ data }: { data: User[] }) {
  const [expanded, setExpanded] = useState<ExpandedState>({});

  const columns = useMemo(
    () => [
      columnHelper.display({
        id: "expander",
        header: () => null,
        cell: ({ row }) =>
          row.getCanExpand() ? (
            <button
              onClick={row.getToggleExpandedHandler()}
              aria-label={row.getIsExpanded() ? "Collapse row" : "Expand row"}
            >
              {row.getIsExpanded() ? "▼" : "▶"}
            </button>
          ) : null,
      }),
      columnHelper.accessor("firstName", { header: "First Name" }),
      // ... other columns
    ],
    []
  );

  const table = useReactTable({
    data,
    columns,
    state: { expanded },
    onExpandedChange: setExpanded,
    getCoreRowModel: getCoreRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getRowCanExpand: () => true, // All rows can expand
  });

  return (
    <table>
      <tbody>
        {table.getRowModel().rows.map((row) => (
          <>
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
            {/* Expanded content */}
            {row.getIsExpanded() && (
              <tr key={`${row.id}-expanded`}>
                <td colSpan={row.getVisibleCells().length}>
                  <UserDetails user={row.original} />
                </td>
              </tr>
            )}
          </>
        ))}
      </tbody>
    </table>
  );
}
```

**Why good:** controlled expanded state, `getRowCanExpand` for conditional expansion, custom expanded content outside table cells

---

### Pattern 8: Server-Side Data

Handle server-side pagination, sorting, and filtering.

#### Server-Side Implementation

```typescript
import { useState, useMemo } from "react";
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from "@tanstack/react-table";
import type {
  PaginationState,
  SortingState,
  ColumnFiltersState,
} from "@tanstack/react-table";

const DEFAULT_PAGE_SIZE = 20;

export function ServerSideTable() {
  // State for server-side features
  const [pagination, setPagination] = useState<PaginationState>({
    pageIndex: 0,
    pageSize: DEFAULT_PAGE_SIZE,
  });
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);

  // Fetch data from your data fetching solution
  // Pass pagination, sorting, columnFilters as query parameters
  const { data, totalRowCount, isLoading } = useUsersData({
    page: pagination.pageIndex,
    pageSize: pagination.pageSize,
    sortBy: sorting[0]?.id,
    sortOrder: sorting[0]?.desc ? "desc" : "asc",
    filters: columnFilters,
  });

  const table = useReactTable({
    data: data ?? [],
    columns,
    state: {
      pagination,
      sorting,
      columnFilters,
    },
    onPaginationChange: setPagination,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    // CRITICAL: Manual mode for server-side
    manualPagination: true,
    manualSorting: true,
    manualFiltering: true,
    // Tell table the total row count
    rowCount: totalRowCount,
    // Or use pageCount directly:
    // pageCount: Math.ceil(totalRowCount / pagination.pageSize),
  });

  if (isLoading) return <div>Loading...</div>;

  return <table>{/* ... table content */}</table>;
}
```

**Why good:** `manualPagination/Sorting/Filtering: true` disables client-side processing, `rowCount` enables proper page count calculation, state passed to data fetching for server queries

---

### Pattern 9: TypeScript Integration

Leverage TypeScript generics for full type safety.

#### Reusable Table Component

```typescript
import type { ColumnDef } from "@tanstack/react-table";

// Generic table props with dual generics
interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

// Generic table component
export function DataTable<TData, TValue>({
  columns,
  data,
}: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <table>
      {/* ... table content */}
    </table>
  );
}

// Usage with type inference
const userColumns: ColumnDef<User, unknown>[] = [
  { accessorKey: "firstName", header: "First Name" },
  { accessorKey: "email", header: "Email" },
];

<DataTable columns={userColumns} data={users} />
```

#### Custom Row ID

```typescript
const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  // Use database ID instead of index for row identification
  getRowId: (row) => row.id,
});
```

**Why good:** dual generics `<TData, TValue>` for reusable components, `getRowId` enables stable selection state across data updates, `ColumnDef<T>` type ensures column accessors match data shape

</patterns>

---

<integration>

## Integration Guide

TanStack Table is a headless library that integrates with your existing architecture.

**Works with:**

- **React** - `useReactTable` hook for React integration
- **Virtualization** - Combine with `@tanstack/react-virtual` for large datasets

**Boundary clarifications:**

- **TanStack Table handles:** Table state (sorting, filtering, pagination, pinning, sizing), row models, column definitions
- **Your styling solution handles:** Table markup styling, sticky column CSS, cell formatting CSS
- **Your data fetching solution handles:** API calls, caching, loading states for server-side tables
- **Your form solution handles:** Inline editing inputs, validation

**Virtual scrolling note:**

TanStack Table does not include virtualization. For tables with thousands of rows, integrate with `@tanstack/react-virtual`. See [examples/virtualization.md](examples/virtualization.md) for virtual scrolling patterns.

**Column pinning note:**

Column pinning provides state and APIs for pinning columns left/right. You handle the sticky CSS positioning. See [examples/column-pinning.md](examples/column-pinning.md) for patterns.

</integration>

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
