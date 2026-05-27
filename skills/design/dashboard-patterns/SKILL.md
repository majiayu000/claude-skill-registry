---
name: dashboard-patterns
description: Dashboard UI patterns with widget composition, real-time data updates, responsive grid layouts, and data tables for React applications. Use when building dashboards, widgets, or data tables.
tags: [dashboard, widgets, data-grid, real-time, layout, admin, tanstack-table, sse]
context: fork
agent: frontend-ui-developer
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Dashboard Patterns

Dashboard UI patterns for building admin panels, analytics dashboards, and data-driven interfaces with React.

## Layout Patterns

### Responsive Dashboard Grid

```tsx
function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-muted/40">
      <aside className="fixed inset-y-0 left-0 z-10 w-64 border-r bg-background">
        <Sidebar />
      </aside>
      <main className="pl-64">
        <header className="sticky top-0 z-10 border-b bg-background px-6 py-4">
          <DashboardHeader />
        </header>
        <div className="p-6">
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">{children}</div>
        </div>
      </main>
    </div>
  );
}

function DashboardGrid() {
  return (
    <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
      <StatCard title="Revenue" value="$45,231" change="+12%" />
      <StatCard title="Users" value="2,350" change="+5.2%" />
      <StatCard title="Orders" value="1,245" change="+18%" />
      <StatCard title="Conversion" value="3.2%" change="-0.4%" />
      <div className="col-span-1 sm:col-span-2"><RevenueChart /></div>
      <div className="col-span-1 sm:col-span-2"><TrafficChart /></div>
      <div className="col-span-full"><RecentOrdersTable /></div>
    </div>
  );
}
```

## Widget Components

### Stat Card Widget

```tsx
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon?: React.ReactNode;
}

function StatCard({ title, value, change, changeType = 'neutral', icon }: StatCardProps) {
  return (
    <div className="rounded-xl border bg-card p-6">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        {icon && <div className="text-muted-foreground">{icon}</div>}
      </div>
      <div className="mt-2 flex items-baseline gap-2">
        <p className="text-3xl font-bold">{value}</p>
        {change && (
          <span className={cn(
            'flex items-center text-sm font-medium',
            changeType === 'positive' && 'text-green-600',
            changeType === 'negative' && 'text-red-600',
          )}>
            {changeType === 'positive' && <TrendingUp className="h-4 w-4" />}
            {changeType === 'negative' && <TrendingDown className="h-4 w-4" />}
            {change}
          </span>
        )}
      </div>
    </div>
  );
}
```

### Widget Registry Pattern

```tsx
type WidgetType = 'stat' | 'chart' | 'table' | 'list';

interface WidgetConfig {
  id: string;
  type: WidgetType;
  title: string;
  span?: number;
  props: Record<string, unknown>;
}

const widgetRegistry: Record<WidgetType, React.ComponentType<any>> = {
  stat: StatCard,
  chart: ChartCard,
  table: DataTable,
  list: ListWidget,
};

function DashboardWidget({ config }: { config: WidgetConfig }) {
  const Component = widgetRegistry[config.type];
  if (!Component) return null;

  return (
    <div style={{ gridColumn: config.span ? `span ${config.span}` : undefined }}>
      <Component title={config.title} {...config.props} />
    </div>
  );
}
```

## Real-Time Data Patterns

### TanStack Query + SSE

```tsx
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';

function useRealtimeMetrics() {
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: fetchMetrics,
  });

  useEffect(() => {
    const eventSource = new EventSource('/api/metrics/stream');
    eventSource.onmessage = (event) => {
      const update = JSON.parse(event.data);
      queryClient.setQueryData(['metrics'], (old: Metrics | undefined) => ({
        ...old,
        ...update,
      }));
    };
    eventSource.onerror = () => {
      eventSource.close();
      queryClient.invalidateQueries({ queryKey: ['metrics'] });
    };
    return () => eventSource.close();
  }, [queryClient]);

  return { data, isLoading };
}
```

## Data Table (TanStack Table)

```tsx
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
  type ColumnDef,
  type SortingState,
} from '@tanstack/react-table';

const columns: ColumnDef<Order>[] = [
  { accessorKey: 'id', header: 'Order ID' },
  { accessorKey: 'customer', header: 'Customer' },
  { accessorKey: 'amount', header: 'Amount', cell: ({ getValue }) => `$${getValue<number>().toLocaleString()}` },
  { accessorKey: 'status', header: 'Status', cell: ({ getValue }) => <StatusBadge status={getValue()} /> },
];

function OrdersTable({ data }: { data: Order[] }) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const table = useReactTable({
    data,
    columns,
    state: { sorting, globalFilter },
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
  });

  return (
    <div>
      <input
        value={globalFilter}
        onChange={(e) => setGlobalFilter(e.target.value)}
        placeholder="Search orders..."
        className="mb-4 rounded border px-3 py-2"
      />
      <table className="w-full">
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th key={header.id} onClick={header.column.getToggleSortingHandler()} className="cursor-pointer px-4 py-2 text-left">
                  {flexRender(header.column.columnDef.header, header.getContext())}
                  {header.column.getIsSorted() === 'asc' && ' ↑'}
                  {header.column.getIsSorted() === 'desc' && ' ↓'}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id} className="border-t">
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-4 py-2">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4 flex items-center gap-2">
        <button onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>Previous</button>
        <span>Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}</span>
        <button onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>Next</button>
      </div>
    </div>
  );
}
```

## Skeleton Loading

```tsx
function DashboardSkeleton() {
  return (
    <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
      {[...Array(4)].map((_, i) => (
        <div key={i} className="rounded-xl border bg-card p-6">
          <div className="h-4 w-24 animate-pulse rounded bg-muted" />
          <div className="mt-2 h-8 w-32 animate-pulse rounded bg-muted" />
        </div>
      ))}
      <div className="col-span-full rounded-xl border bg-card p-6">
        <div className="mt-4 space-y-2">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-12 animate-pulse rounded bg-muted" />
          ))}
        </div>
      </div>
    </div>
  );
}
```

## Anti-Patterns (FORBIDDEN)

```tsx
// NEVER: Fetch data in every widget independently (duplicated queries)
// NEVER: Re-render entire dashboard on single metric change
// NEVER: Hardcoded dashboard layout (not responsive)
// NEVER: Polling without intervals (infinite loop)
// NEVER: Missing loading states (flash of empty state)
// NEVER: Real-time updates without debounce (100 re-renders/sec)
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Layout | **CSS Grid** for 2D dashboard layouts |
| Real-time | **SSE** for server->client, **WebSocket** for bidirectional |
| Data table | **TanStack Table** for features |
| State | **TanStack Query** with granular keys |
| Loading | **Skeleton** for content areas |

## Related Skills

- `recharts-patterns` - Chart components for dashboards
- `tanstack-query-advanced` - Data fetching patterns
- `streaming-api-patterns` - SSE and WebSocket implementation
