---
name: materialreacttable-mastery
description: Material React Table V3 expert skill. Use when building feature-rich data tables w/ MUI styling, server-side ops, CRUD editing, virtualization, or complex filtering/sorting.
author: George Khananaev
---

# Material React Table Mastery

Build production-grade data tables w/ MRT V3 (TanStack Table V8 + MUI).

## When to Use

- Building data tables with MUI styling
- Server-side pagination/filtering/sorting
- CRUD editing (inline, modal, cell, table)
- Large dataset virtualization (10k+ rows)
- Complex filtering (date range, multi-select, faceted)
- Migrating between MRT versions (V1→V2→V3)
- MUI v7 compatibility issues

## Triggers

- `/mrt-init` - Initialize MRT setup w/ dependencies
- `/mrt-column` - Generate typed column definitions
- `/mrt-crud` - Add CRUD editing capabilities
- `/mrt-server` - Configure server-side pagination/filtering/sorting
- `/mrt-migrate` - Migrate between MRT versions (V1→V2→V3)
- `/mrt-state` - State management, persistence, controlled state
- `/mrt-export` - Data export (CSV, Excel, PDF)
- `/mrt-a11y` - Accessibility & keyboard navigation setup

## Reference Files

| Category | Reference | When to Load |
|----------|-----------|--------------|
| Columns | `references/column_definitions.md` | Accessors, formatters, grouping, aggregation, V1→V2→V3 migration |
| Filtering | `references/filtering_sorting.md` | Filter variants, global search, faceted |
| Pagination | `references/pagination_virtualization.md` | Server-side, infinite scroll, virtualization |
| Editing | `references/editing_crud.md` | Inline, modal, row, cell, validation |
| Selection | `references/row_selection.md` | Multi-select, actions, bulk ops |
| Tree | `references/tree_data.md` | Hierarchical data, expand/collapse |
| Custom | `references/customization.md` | Toolbar, styling, mrtTheme, localization, z-index |
| State | `references/state_management_apis.md` | Table/row/cell APIs, state persistence, events |
| Advanced | `references/advanced_features.md` | A11y, export, drag & drop, click-to-copy |
| Versions | `references/version_compatibility.md` | Version matrix, migrations, prop renames |

## Core Tenets

### 1. TanStack Table Foundation

MRT wraps TanStack Table V8. Use `useMaterialReactTable` hook for full control.

```tsx
import { useMaterialReactTable, MaterialReactTable } from 'material-react-table';

const table = useMaterialReactTable({
  columns,
  data,
  enableColumnFilters: true,
  enableGlobalFilter: true,
  enablePagination: true,
});

return <MaterialReactTable table={table} />;
```

### 2. Column Definitions in useMemo

ALWAYS wrap columns in `useMemo` to prevent unnecessary re-renders.

```tsx
const columns = useMemo<MRT_ColumnDef<Person>[]>(() => [
  { accessorKey: 'name', header: 'Name', size: 200 },
  {
    accessorFn: (row) => `${row.firstName} ${row.lastName}`,
    id: 'fullName',
    header: 'Full Name',
  },
  {
    accessorKey: 'status',
    header: 'Status',
    filterVariant: 'select',
    filterSelectOptions: ['Active', 'Inactive', 'Pending'],
    Cell: ({ cell }) => (
      <Chip
        label={cell.getValue<string>()}
        color={cell.getValue() === 'Active' ? 'success' : 'default'}
      />
    ),
  },
  {
    accessorKey: 'salary',
    header: 'Salary',
    filterVariant: 'range-slider',
    Cell: ({ cell }) => cell.getValue<number>().toLocaleString('en-US', {
      style: 'currency', currency: 'USD',
    }),
    aggregationFn: 'sum',
    AggregatedCell: ({ cell }) => `Total: ${cell.getValue()}`,
  },
], []);
```

### 3. Server-Side Operations

For datasets > 100 rows, use server-side pagination/filtering/sorting.

```tsx
const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 10 });
const [sorting, setSorting] = useState<MRT_SortingState>([]);
const [globalFilter, setGlobalFilter] = useState('');

const { data, isLoading } = useQuery({
  queryKey: ['users', pagination, sorting, globalFilter],
  queryFn: () => fetchUsers({ pagination, sorting, globalFilter }),
});

const table = useMaterialReactTable({
  columns,
  data: data?.rows ?? [],
  rowCount: data?.totalCount ?? 0,
  manualPagination: true,
  manualSorting: true,
  manualFiltering: true,
  state: { pagination, sorting, globalFilter, isLoading },
  onPaginationChange: setPagination,
  onSortingChange: setSorting,
  onGlobalFilterChange: setGlobalFilter,
});
```

### 4. CRUD Editing

Support inline, modal, cell, or table editing modes.

```tsx
const table = useMaterialReactTable({
  columns,
  data,
  enableEditing: true,
  editDisplayMode: 'row', // 'modal' | 'cell' | 'table'
  onEditingRowSave: async ({ values, row, table }) => {
    await updateUser(row.original.id, values);
    table.setEditingRow(null);
  },
  renderRowActions: ({ row, table }) => (
    <Box sx={{ display: 'flex', gap: '1rem' }}>
      <Tooltip title="Edit">
        <IconButton onClick={() => table.setEditingRow(row)}>
          <EditIcon />
        </IconButton>
      </Tooltip>
      <Tooltip title="Delete">
        <IconButton color="error" onClick={() => handleDelete(row.original.id)}>
          <DeleteIcon />
        </IconButton>
      </Tooltip>
    </Box>
  ),
});
```

### 5. Virtualization for Large Data

Enable row virtualization for 10,000+ rows.

```tsx
const table = useMaterialReactTable({
  columns,
  data: largeDataset,
  enableRowVirtualization: true,
  rowVirtualizerOptions: { overscan: 5 },
  muiTableBodyRowProps: { sx: { height: 53 } }, // Fixed height for perf
});
```

## Decision Tree

```
Dataset size?
├─ < 100 rows → Client-side (default)
├─ 100-10,000 rows → Server-side pagination
└─ > 10,000 rows → Virtualization + server-side
```

## Common Configurations

| Use Case | Configuration |
|----------|---------------|
| Basic display | `enableColumnFilters: false, enablePagination: false` |
| Editable | `enableEditing: true, editDisplayMode: 'row'` |
| Selection | `enableRowSelection: true, enableMultiRowSelection: true` |
| Expandable | `enableExpanding: true, renderDetailPanel: ({row}) => <Details />` |
| Tree data | `enableExpanding: true, getSubRows: (row) => row.children` |
| Server-side | `manualPagination: true, manualFiltering: true, manualSorting: true` |

## Customization

### Toolbar

```tsx
renderTopToolbar: ({ table }) => (
  <Box sx={{ display: 'flex', gap: 2, p: 2 }}>
    <MRT_GlobalFilterTextField table={table} />
    <ExportButton data={data} />
  </Box>
),
```

### Row Styling

```tsx
muiTableBodyRowProps: ({ row }) => ({
  sx: { backgroundColor: row.original.isHighlighted ? 'action.hover' : undefined },
}),
```

### Localization

```tsx
import { MRT_Localization_ES } from 'material-react-table/locales/es';

localization: MRT_Localization_ES,
```

## Filter Variants

| Type | Variant | Use Case |
|------|---------|----------|
| Text | `'text'` (default) | Free text search |
| Select | `'select'` | Enum/status fields |
| Multi-select | `'multi-select'` | Tags, categories |
| Range | `'range'` | Numeric ranges |
| Range Slider | `'range-slider'` | Price, age |
| Date | `'date'` | Date fields |
| Date Range | `'date-range'` | Date ranges |
| Autocomplete | `'autocomplete'` | Large option sets |
| Checkbox | `'checkbox'` | Boolean fields |

## React Query Integration

```tsx
function UsersTable() {
  const [columnFilters, setColumnFilters] = useState<MRT_ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');
  const [sorting, setSorting] = useState<MRT_SortingState>([]);
  const [pagination, setPagination] = useState({ pageIndex: 0, pageSize: 10 });

  const { data, isLoading, isError } = useQuery({
    queryKey: ['users', columnFilters, globalFilter, pagination, sorting],
    queryFn: () => fetchUsers({ columnFilters, globalFilter, pagination, sorting }),
    placeholderData: keepPreviousData,
  });

  const table = useMaterialReactTable({
    columns,
    data: data?.users ?? [],
    rowCount: data?.meta?.totalRowCount ?? 0,
    manualFiltering: true,
    manualPagination: true,
    manualSorting: true,
    state: { columnFilters, globalFilter, isLoading, pagination, showAlertBanner: isError, sorting },
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    onPaginationChange: setPagination,
    onSortingChange: setSorting,
  });

  return <MaterialReactTable table={table} />;
}
```

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Recreate columns on every render | Wrap in `useMemo` |
| Fetch all data for server-side | Implement backend pagination |
| Skip virtualization for 10k+ rows | Enable `enableRowVirtualization` |
| Custom filter UI for common cases | Use built-in `filterVariant` |
| Ignore loading states | Use `isLoading` state prop |
| Inline column definitions | Define outside component or `useMemo` |
| Hardcode table text | Use `localization` prop |

## Dependencies

```bash
npm install material-react-table @mui/material @mui/x-date-pickers @mui/icons-material @emotion/react @emotion/styled @tanstack/react-query
```

## Version Compatibility

| MRT | MUI | React | Notes |
|-----|-----|-------|-------|
| V3 | 6+ (v7 experimental) | 18+ | Current - keyboard nav default |
| V2 | 5.11+ | 17+ | Maintenance |
| V1 | 5.0+ | 17+ | Deprecated |

**MUI v7 Status**: ⚠️ Not officially supported yet. Known issues: dark mode broken, TypeScript errors. Use `--legacy-peer-deps` if required. Track [GitHub #1401](https://github.com/KevinVandy/material-react-table/issues/1401).

**Key V2→V3 changes**: `text` → `label` in select options, keyboard nav enabled by default.

## Checklist

- [ ] Columns wrapped in `useMemo`
- [ ] Proper accessors (`accessorKey` | `accessorFn` + `id`)
- [ ] `filterVariant` set per column type
- [ ] Server-side for > 100 rows
- [ ] Virtualization for > 10k rows
- [ ] `isLoading` state connected
- [ ] Error states handled (`showAlertBanner`)
- [ ] Validation in `onEditingRowSave`
- [ ] Row actions labeled for a11y
- [ ] `LocalizationProvider` if using date filters
- [ ] Version-appropriate props (V1→V2→V3 renames)
- [ ] z-index handled if table in modal/drawer