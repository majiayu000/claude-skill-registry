---
name: TanStack Table
description: |
  Build headless data tables with TanStack Table v8. Server-side pagination, filtering, sorting, and virtualization for Cloudflare Workers + D1. Prevents 12 documented errors.

  Use when building tables with large datasets, coordinating with TanStack Query, or fixing state management, performance, or React 19+ compatibility issues.
user-invocable: true
---

# TanStack Table

Headless data tables with server-side pagination, filtering, sorting, and virtualization for Cloudflare Workers + D1

---

## Quick Start

**Last Updated**: 2026-01-09
**Versions**: @tanstack/react-table@8.21.3, @tanstack/react-virtual@3.13.18

```bash
npm install @tanstack/react-table@latest
npm install @tanstack/react-virtual@latest  # For virtualization
```

**Basic Setup** (CRITICAL: memoize data/columns to prevent infinite re-renders):
```typescript
import { useReactTable, getCoreRowModel, ColumnDef } from '@tanstack/react-table'
import { useMemo } from 'react'

const columns: ColumnDef<User>[] = [
  { accessorKey: 'name', header: 'Name' },
  { accessorKey: 'email', header: 'Email' },
]

function UsersTable() {
  const data = useMemo(() => [...users], []) // Stable reference
  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() })

  return (
    <table>
      <thead>
        {table.getHeaderGroups().map(group => (
          <tr key={group.id}>
            {group.headers.map(h => <th key={h.id}>{h.column.columnDef.header}</th>)}
          </tr>
        ))}
      </thead>
      <tbody>
        {table.getRowModel().rows.map(row => (
          <tr key={row.id}>
            {row.getVisibleCells().map(cell => <td key={cell.id}>{cell.renderValue()}</td>)}
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

---

## Server-Side Patterns

**Cloudflare D1 API** (pagination + filtering + sorting):
```typescript
// Workers API: functions/api/users.ts
export async function onRequestGet({ request, env }) {
  const url = new URL(request.url)
  const page = Number(url.searchParams.get('page')) || 0
  const pageSize = 20
  const search = url.searchParams.get('search') || ''
  const sortBy = url.searchParams.get('sortBy') || 'created_at'
  const sortOrder = url.searchParams.get('sortOrder') || 'DESC'

  const { results } = await env.DB.prepare(`
    SELECT * FROM users
    WHERE name LIKE ? OR email LIKE ?
    ORDER BY ${sortBy} ${sortOrder}
    LIMIT ? OFFSET ?
  `).bind(`%${search}%`, `%${search}%`, pageSize, page * pageSize).all()

  const { total } = await env.DB.prepare('SELECT COUNT(*) as total FROM users').first()

  return Response.json({
    data: results,
    pagination: { page, pageSize, total, pageCount: Math.ceil(total / pageSize) },
  })
}
```

**Client-Side** (TanStack Query + Table):
```typescript
const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 20 })
const [columnFilters, setColumnFilters] = useState([])
const [sorting, setSorting] = useState([])

// CRITICAL: Include ALL state in query key
const { data, isLoading } = useQuery({
  queryKey: ['users', pagination, columnFilters, sorting],
  queryFn: async () => {
    const params = new URLSearchParams({
      page: pagination.pageIndex,
      search: columnFilters.find(f => f.id === 'search')?.value || '',
      sortBy: sorting[0]?.id || 'created_at',
      sortOrder: sorting[0]?.desc ? 'DESC' : 'ASC',
    })
    return fetch(`/api/users?${params}`).then(r => r.json())
  },
})

const table = useReactTable({
  data: data?.data ?? [],
  columns,
  getCoreRowModel: getCoreRowModel(),
  // CRITICAL: manual* flags tell table server handles these
  manualPagination: true,
  manualFiltering: true,
  manualSorting: true,
  pageCount: data?.pagination.pageCount ?? 0,
  state: { pagination, columnFilters, sorting },
  onPaginationChange: setPagination,
  onColumnFiltersChange: setColumnFilters,
  onSortingChange: setSorting,
})
```

---

## Virtualization (1000+ Rows)

Render only visible rows for performance:
```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

function VirtualizedTable() {
  const containerRef = useRef<HTMLDivElement>(null)
  const table = useReactTable({ data: largeDataset, columns, getCoreRowModel: getCoreRowModel() })
  const { rows } = table.getRowModel()

  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => containerRef.current,
    estimateSize: () => 50, // Row height px
    overscan: 10,
  })

  return (
    <div ref={containerRef} style={{ height: '600px', overflow: 'auto' }}>
      <table style={{ height: `${rowVirtualizer.getTotalSize()}px` }}>
        <tbody>
          {rowVirtualizer.getVirtualItems().map(virtualRow => {
            const row = rows[virtualRow.index]
            return (
              <tr key={row.id} style={{ position: 'absolute', transform: `translateY(${virtualRow.start}px)` }}>
                {row.getVisibleCells().map(cell => <td key={cell.id}>{cell.renderValue()}</td>)}
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
```

### Warning: Hidden Containers (Tabs/Modals)

**Known Issue**: When using virtualization inside tabbed content or modals that hide inactive content with `display: none`, the virtualizer continues performing layout calculations while hidden, causing:
- Infinite re-render loops (large datasets: 50k+ rows)
- Incorrect scroll position when tab becomes visible
- Empty table or reset scroll (small datasets)

**Source**: [GitHub Issue #6109](https://github.com/TanStack/table/issues/6109)

**Prevention**:
```typescript
const rowVirtualizer = useVirtualizer({
  count: rows.length,
  getScrollElement: () => containerRef.current,
  estimateSize: () => 50,
  overscan: 10,
  // Disable when container is hidden to prevent infinite re-renders
  enabled: containerRef.current?.getClientRects().length !== 0,
})

// OR: Conditionally render instead of hiding with CSS
{isVisible && <VirtualizedTable />}
```

---

## Column/Row Pinning

Pin columns or rows to keep them visible during horizontal/vertical scroll:

```typescript
import { useReactTable, getCoreRowModel } from '@tanstack/react-table'

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  // Enable pinning
  enableColumnPinning: true,
  enableRowPinning: true,
  // Initial pinning state
  initialState: {
    columnPinning: {
      left: ['select', 'name'],  // Pin to left
      right: ['actions'],        // Pin to right
    },
  },
})

// Render with pinned columns
function PinnedTable() {
  return (
    <div className="flex">
      {/* Left pinned columns */}
      <div className="sticky left-0 bg-background z-10">
        {table.getLeftHeaderGroups().map(/* render left headers */)}
        {table.getRowModel().rows.map(row => (
          <tr>{row.getLeftVisibleCells().map(/* render cells */)}</tr>
        ))}
      </div>

      {/* Center scrollable columns */}
      <div className="overflow-x-auto">
        {table.getCenterHeaderGroups().map(/* render center headers */)}
        {table.getRowModel().rows.map(row => (
          <tr>{row.getCenterVisibleCells().map(/* render cells */)}</tr>
        ))}
      </div>

      {/* Right pinned columns */}
      <div className="sticky right-0 bg-background z-10">
        {table.getRightHeaderGroups().map(/* render right headers */)}
        {table.getRowModel().rows.map(row => (
          <tr>{row.getRightVisibleCells().map(/* render cells */)}</tr>
        ))}
      </div>
    </div>
  )
}

// Toggle pinning programmatically
column.pin('left')   // Pin column to left
column.pin('right')  // Pin column to right
column.pin(false)    // Unpin column
row.pin('top')       // Pin row to top
row.pin('bottom')    // Pin row to bottom
```

### Warning: Column Pinning with Column Groups

**Known Issue**: Pinning parent group columns (created with `columnHelper.group()`) causes incorrect positioning and duplicated headers. `column.getStart('left')` returns wrong values for group headers.

**Source**: [GitHub Issue #5397](https://github.com/TanStack/table/issues/5397)

**Prevention**:
```typescript
// Disable pinning for grouped columns
const isPinnable = (column) => !column.parent

// OR: Pin individual columns within group, not the group itself
table.getColumn('firstName')?.pin('left')
table.getColumn('lastName')?.pin('left')
// Don't pin the parent group column
```

---

## Row Expanding (Nested Data)

Show/hide child rows or additional details:

```typescript
import { useReactTable, getCoreRowModel, getExpandedRowModel } from '@tanstack/react-table'

// Data with nested children
const data = [
  {
    id: 1,
    name: 'Parent Row',
    subRows: [
      { id: 2, name: 'Child Row 1' },
      { id: 3, name: 'Child Row 2' },
    ],
  },
]

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getExpandedRowModel: getExpandedRowModel(),  // Required for expanding
  getSubRows: row => row.subRows,               // Tell table where children are
})

// Render with expand button
function ExpandableTable() {
  return (
    <tbody>
      {table.getRowModel().rows.map(row => (
        <>
          <tr key={row.id}>
            <td>
              {row.getCanExpand() && (
                <button onClick={row.getToggleExpandedHandler()}>
                  {row.getIsExpanded() ? '▼' : '▶'}
                </button>
              )}
            </td>
            {row.getVisibleCells().map(cell => (
              <td key={cell.id} style={{ paddingLeft: `${row.depth * 20}px` }}>
                {cell.renderValue()}
              </td>
            ))}
          </tr>
        </>
      ))}
    </tbody>
  )
}

// Control expansion programmatically
table.toggleAllRowsExpanded()     // Expand/collapse all
row.toggleExpanded()              // Toggle single row
table.getIsAllRowsExpanded()      // Check if all expanded
```

**Detail Rows** (custom content, not nested data):

```typescript
function DetailRow({ row }) {
  if (!row.getIsExpanded()) return null

  return (
    <tr>
      <td colSpan={columns.length}>
        <div className="p-4 bg-muted">
          Custom detail content for row {row.id}
        </div>
      </td>
    </tr>
  )
}
```

---

## Row Grouping

Group rows by column values:

```typescript
import { useReactTable, getCoreRowModel, getGroupedRowModel } from '@tanstack/react-table'

const table = useReactTable({
  data,
  columns,
  getCoreRowModel: getCoreRowModel(),
  getGroupedRowModel: getGroupedRowModel(),    // Required for grouping
  getExpandedRowModel: getExpandedRowModel(),  // Groups are expandable
  initialState: {
    grouping: ['status'],  // Group by 'status' column
  },
})

// Column with aggregation
const columns = [
  {
    accessorKey: 'status',
    header: 'Status',
  },
  {
    accessorKey: 'amount',
    header: 'Amount',
    aggregationFn: 'sum',                      // Sum grouped values
    aggregatedCell: ({ getValue }) => `Total: ${getValue()}`,
  },
]

// Render grouped table
function GroupedTable() {
  return (
    <tbody>
      {table.getRowModel().rows.map(row => (
        <tr key={row.id}>
          {row.getVisibleCells().map(cell => (
            <td key={cell.id}>
              {cell.getIsGrouped() ? (
                // Grouped cell - show group header with expand toggle
                <button onClick={row.getToggleExpandedHandler()}>
                  {row.getIsExpanded() ? '▼' : '▶'} {cell.renderValue()} ({row.subRows.length})
                </button>
              ) : cell.getIsAggregated() ? (
                // Aggregated cell - show aggregation result
                cell.renderValue()
              ) : cell.getIsPlaceholder() ? null : (
                // Regular cell
                cell.renderValue()
              )}
            </td>
          ))}
        </tr>
      ))}
    </tbody>
  )
}

// Built-in aggregation functions
// 'sum', 'min', 'max', 'extent', 'mean', 'median', 'unique', 'uniqueCount', 'count'
```

### Warning: Performance Bottleneck with Grouping (Community-sourced)

**Known Issue**: The grouping feature causes significant performance degradation on medium-to-large datasets. With grouping enabled, render times can increase from <1 second to 30-40 seconds on 50k rows due to excessive memory usage in `createRow` calculations.

**Source**: [Blog Post (JP Camara)](https://jpcamara.com/2023/03/07/making-tanstack-table.html) | [GitHub Issue #5926](https://github.com/TanStack/table/issues/5926)

**Verified**: Community testing + GitHub issue report

**Prevention**:
```typescript
// 1. Use server-side grouping for large datasets
// 2. Implement pagination to limit rows per page
// 3. Disable grouping for 10k+ rows
const shouldEnableGrouping = data.length < 10000

// 4. OR: Use React.memo on row components
const MemoizedRow = React.memo(TableRow)
```

---

## Known Issues & Solutions

**Issue #1: Infinite Re-Renders**
- **Error**: Table re-renders infinitely, browser freezes
- **Cause**: `data` or `columns` references change on every render
- **Fix**: Use `useMemo(() => [...], [])` or define data/columns outside component

**Issue #2: Query + Table State Mismatch**
- **Error**: Query refetches but pagination state not synced, stale data
- **Cause**: Query key missing table state (pagination, filters, sorting)
- **Fix**: Include ALL state in query key: `queryKey: ['users', pagination, columnFilters, sorting]`

**Issue #3: Server-Side Features Not Working**
- **Error**: Pagination/filtering/sorting doesn't trigger API calls
- **Cause**: Missing `manual*` flags
- **Fix**: Set `manualPagination: true`, `manualFiltering: true`, `manualSorting: true` + provide `pageCount`

**Issue #4: TypeScript "Cannot Find Module"**
- **Error**: Import errors for `createColumnHelper`
- **Fix**: Import from `@tanstack/react-table` (NOT `@tanstack/table-core`)

**Issue #5: Sorting Not Working Server-Side**
- **Error**: Clicking sort headers doesn't update data
- **Cause**: Sorting state not in query key/API params
- **Fix**: Include `sorting` in query key, add sort params to API call, set `manualSorting: true` + `onSortingChange`

**Issue #6: Poor Performance (1000+ Rows)**
- **Error**: Table slow/laggy with large datasets
- **Fix**: Use TanStack Virtual for client-side OR implement server-side pagination

**Issue #7: React Compiler Incompatibility (React 19+)**
- **Error**: `"Table doesn't re-render when data changes"` (with React Compiler enabled)
- **Source**: [GitHub Issue #5567](https://github.com/TanStack/table/issues/5567)
- **Why It Happens**: React Compiler's automatic memoization conflicts with table core instance, preventing re-renders when data/state changes
- **Prevention**: Add `"use no memo"` directive at top of components using `useReactTable`:

```typescript
"use no memo"

function TableComponent() {
  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() })
  // Now works correctly with React Compiler
}
```

**Note**: This issue also affects column visibility and row selection. Full fix coming in v9.

**Issue #8: Server-Side Pagination Row Selection Bug**
- **Error**: `toggleAllRowsSelected(false)` only deselects current page, not all pages
- **Source**: [GitHub Issue #5929](https://github.com/TanStack/table/issues/5929)
- **Why It Happens**: Selection state persists across pages (intentional for server-side use cases), but header checkbox state is calculated incorrectly
- **Prevention**: Manually clear selection state when toggling off:

```typescript
const toggleAllRows = (value: boolean) => {
  if (!value) {
    table.setRowSelection({}) // Clear entire selection object
  } else {
    table.toggleAllRowsSelected(true)
  }
}
```

**Issue #9: Client-Side onPaginationChange Returns Incorrect pageIndex**
- **Error**: `onPaginationChange` always returns `pageIndex: 0` instead of current page
- **Source**: [GitHub Issue #5970](https://github.com/TanStack/table/issues/5970)
- **Why It Happens**: Client-side pagination mode has state tracking bug (only occurs in client mode, works correctly in server/manual mode)
- **Prevention**: Switch to manual pagination for correct behavior:

```typescript
// Instead of relying on client-side pagination
const table = useReactTable({
  data,
  columns,
  manualPagination: true, // Forces correct state tracking
  pageCount: Math.ceil(data.length / pagination.pageSize),
  state: { pagination },
  onPaginationChange: setPagination,
})
```

**Issue #10: Row Selection Not Cleaned Up When Data Removed**
- **Error**: Selected rows that no longer exist in data remain in selection state
- **Source**: [GitHub Issue #5850](https://github.com/TanStack/table/issues/5850)
- **Why It Happens**: Intentional behavior to support server-side pagination (where rows disappear from current page but should stay selected)
- **Prevention**: Manually clean up selection when removing data:

```typescript
const removeRow = (idToRemove: string) => {
  // Remove from data
  setData(data.filter(row => row.id !== idToRemove))

  // Clean up selection if it was selected
  const { rowSelection } = table.getState()
  if (rowSelection[idToRemove]) {
    table.setRowSelection((old) => {
      const filtered = Object.entries(old).filter(([id]) => id !== idToRemove)
      return Object.fromEntries(filtered)
    })
  }
}

// OR: Use table.resetRowSelection(true) to clear all
```

**Issue #11: Performance Degradation with React DevTools Open**
- **Error**: Table performance significantly degrades with React DevTools open (development only)
- **Why It Happens**: DevTools inspects table instance and row models on every render, especially noticeable with 500+ rows
- **Fix**: Close React DevTools during performance testing. This is not a production issue.

**Issue #12: TypeScript getValue() Type Inference with Grouped Columns**
- **Error**: `getValue()` returns `unknown` instead of accessor's actual type inside `columnHelper.group()`
- **Source**: [GitHub Issue #5860](https://github.com/TanStack/table/issues/5860)
- **Fix**: Manually specify type or use `renderValue()`:

```typescript
// Option 1: Type assertion
cell: (info) => {
  const value = info.getValue() as string
  return value.toUpperCase()
}

// Option 2: Use renderValue() (better type inference)
cell: (info) => {
  const value = info.renderValue()
  return typeof value === 'string' ? value.toUpperCase() : value
}
```

---

**Related Skills**: tanstack-query (data fetching), cloudflare-d1 (database backend), tailwind-v4-shadcn (UI styling)

---

**Last verified**: 2026-01-21 | **Skill version**: 2.0.0 | **Changes**: Added 7 new known issues from TIER 1-2 research findings (React 19 Compiler, server-side row selection, virtualization in hidden containers, client-side pagination bug, column pinning with groups, row selection cleanup, DevTools performance, TypeScript getValue). Error count: 6 → 12.
