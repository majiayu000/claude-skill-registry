---
name: tanstack-table
description: Build TanStack Table components using the meta field pattern for cell callbacks instead of closures. Use when creating data tables, implementing sorting, or adding inline editing.
user-invocable: false
metadata:
  author: BastiDood <basti@casperstudios.xyz>
---

## Documentation

Use `context7` for the latest documentation. Use `deepwiki` to ask questions about the library's implementation.

- GitHub Repository: https://github.com/TanStack/table
- DeepWiki Repository: `TanStack/table`
- Context7 Library ID: `/tanstack/table`

# TanStack Table Patterns

This skill covers TanStack Table library patterns with the `meta` field for passing behavior to cells.

## Core Pattern: Hoisted Columns with Meta

```typescript
// 1. Extend TableMeta for type safety
declare module '@tanstack/react-table' {
	interface TableMeta<TData extends RowData> {
		onEdit?: (id: string) => void;
		onDelete?: (id: string) => void;
	}
}

// 2. Hoist column definitions outside component
const columnHelper = createColumnHelper<Job>();

const columns = [
	columnHelper.accessor('name', {
		header: 'Name',
		cell: info => info.getValue(),
	}),
	columnHelper.display({
		id: 'actions',
		cell: ({ row, table }) => (
			<Button onClick={() => table.options.meta?.onEdit?.(row.original.id)}>Edit</Button>
		),
	}),
];

// 3. Pass callbacks via meta
function DataTable({ data, onEdit, onDelete }: Props) {
	const table = useReactTable({
		data,
		columns,
		getCoreRowModel: getCoreRowModel(),
		meta: { onEdit, onDelete },
	});

	return <Table>...</Table>;
}
```

## Why Meta Over Closures?

Closures in column definitions cause re-renders:

```typescript
// Bad - new column array every render
const columns = useMemo(() => [
  {
    cell: ({ row }) => (
      <Button onClick={() => onEdit(row.original.id)}>Edit</Button>
    ),
  },
], [onEdit]); // Invalidates when onEdit changes

// Good - stable columns, dynamic meta
const columns = [...]; // Hoisted, never changes

const table = useReactTable({
  meta: { onEdit }, // Only meta changes
});
```

## References

- For column definition patterns, see [column-definitions.md](references/column-definitions.md)
- For meta field type safety, see [meta-field.md](references/meta-field.md)
