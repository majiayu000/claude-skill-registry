---
name: dashboard-design
description: Design effective dashboards with clear layouts, KPI displays, data grids, and real-time updates. Covers dashboard patterns, information hierarchy, responsive grids, widget design, and admin panel layouts. Use for building analytics dashboards, admin interfaces, and monitoring displays.
---

# Dashboard Design

Create effective dashboards that present data clearly and enable quick decision-making.

## Instructions

1. **Prioritize key metrics** - Most important KPIs should be immediately visible
2. **Use consistent card layouts** - Establish a grid system and stick to it
3. **Design for scanning** - Users should grasp status at a glance
4. **Enable drill-down** - Summary to detail progression
5. **Consider real-time needs** - Update frequencies and loading states

## Dashboard Layout Patterns

### KPI Cards

```tsx
interface KPICardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon?: React.ReactNode;
}

function KPICard({ title, value, change, changeLabel, icon }: KPICardProps) {
  const isPositive = change && change > 0;
  const isNegative = change && change < 0;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-500">{title}</span>
        {icon && <span className="text-gray-400">{icon}</span>}
      </div>
      <div className="mt-2">
        <span className="text-3xl font-bold text-gray-900">{value}</span>
      </div>
      {change !== undefined && (
        <div className="mt-2 flex items-center">
          <span
            className={`text-sm font-medium ${
              isPositive ? 'text-green-600' : isNegative ? 'text-red-600' : 'text-gray-500'
            }`}
          >
            {isPositive && '+'}
            {change}%
          </span>
          {changeLabel && (
            <span className="ml-2 text-sm text-gray-500">{changeLabel}</span>
          )}
        </div>
      )}
    </div>
  );
}
```

### Dashboard Grid

```tsx
function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <div className="flex items-center gap-4">
            <DateRangePicker />
            <RefreshButton />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {/* KPI Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <KPICard title="Total Revenue" value="$45,231" change={12.5} changeLabel="vs last month" />
          <KPICard title="Orders" value="1,234" change={-2.3} changeLabel="vs last month" />
          <KPICard title="Customers" value="5,678" change={8.1} changeLabel="vs last month" />
          <KPICard title="Avg. Order" value="$36.70" change={4.2} changeLabel="vs last month" />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <ChartCard title="Revenue Over Time">
            <RevenueChart />
          </ChartCard>
          <ChartCard title="Sales by Category">
            <CategoryChart />
          </ChartCard>
        </div>

        {/* Table Section */}
        <div className="bg-white rounded-lg shadow">
          <DataTable />
        </div>
      </main>
    </div>
  );
}
```

### Chart Card Component

```tsx
interface ChartCardProps {
  title: string;
  subtitle?: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}

function ChartCard({ title, subtitle, action, children }: ChartCardProps) {
  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-gray-900">{title}</h3>
            {subtitle && <p className="text-sm text-gray-500">{subtitle}</p>}
          </div>
          {action}
        </div>
      </div>
      <div className="p-6">{children}</div>
    </div>
  );
}
```

## Data Tables

### Sortable Data Table

```tsx
interface Column<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
}

function DataTable<T extends { id: string }>({
  data,
  columns,
}: {
  data: T[];
  columns: Column<T>[];
}) {
  const [sortKey, setSortKey] = useState<keyof T | null>(null);
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  const sortedData = useMemo(() => {
    if (!sortKey) return data;
    return [...data].sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      const modifier = sortOrder === 'asc' ? 1 : -1;
      return aVal < bVal ? -1 * modifier : aVal > bVal ? 1 * modifier : 0;
    });
  }, [data, sortKey, sortOrder]);

  const handleSort = (key: keyof T) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  };

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((col) => (
              <th
                key={String(col.key)}
                onClick={() => col.sortable && handleSort(col.key)}
                className={`px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider ${
                  col.sortable ? 'cursor-pointer hover:bg-gray-100' : ''
                }`}
              >
                <div className="flex items-center gap-2">
                  {col.header}
                  {col.sortable && sortKey === col.key && (
                    <span>{sortOrder === 'asc' ? '↑' : '↓'}</span>
                  )}
                </div>
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {sortedData.map((row) => (
            <tr key={row.id} className="hover:bg-gray-50">
              {columns.map((col) => (
                <td key={String(col.key)} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {col.render ? col.render(row[col.key], row) : String(row[col.key])}
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

## Real-Time Updates

### Auto-Refresh Hook

```tsx
function useAutoRefresh<T>(
  fetcher: () => Promise<T>,
  intervalMs: number = 30000
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const refresh = useCallback(async () => {
    try {
      const result = await fetcher();
      setData(result);
      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Fetch failed'));
    } finally {
      setLoading(false);
    }
  }, [fetcher]);

  useEffect(() => {
    refresh();
    const interval = setInterval(refresh, intervalMs);
    return () => clearInterval(interval);
  }, [refresh, intervalMs]);

  return { data, loading, error, lastUpdated, refresh };
}
```

### Live Status Indicator

```tsx
function LiveIndicator({ lastUpdated }: { lastUpdated: Date | null }) {
  const [, forceUpdate] = useState({});

  useEffect(() => {
    const interval = setInterval(() => forceUpdate({}), 1000);
    return () => clearInterval(interval);
  }, []);

  if (!lastUpdated) return null;

  const seconds = Math.floor((Date.now() - lastUpdated.getTime()) / 1000);

  return (
    <div className="flex items-center gap-2 text-sm text-gray-500">
      <span className="relative flex h-2 w-2">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500" />
      </span>
      Updated {seconds < 60 ? `${seconds}s ago` : `${Math.floor(seconds / 60)}m ago`}
    </div>
  );
}
```

## Responsive Dashboard

```tsx
function ResponsiveDashboard() {
  return (
    <div className="space-y-6">
      {/* KPIs - Stack on mobile, 4 columns on desktop */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard title="Revenue" value="$45K" />
        <KPICard title="Orders" value="1,234" />
        <KPICard title="Users" value="5,678" />
        <KPICard title="Growth" value="+12%" />
      </div>

      {/* Charts - Full width on mobile, side by side on desktop */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard title="Revenue Trend">
          <LineChart />
        </ChartCard>
        <ChartCard title="Distribution">
          <PieChart />
        </ChartCard>
      </div>

      {/* Table - Horizontal scroll on mobile */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <DataTable />
        </div>
      </div>
    </div>
  );
}
```

## Best Practices

1. **Progressive disclosure** - Show summary first, details on demand
2. **Consistent spacing** - Use a grid system (8px base)
3. **Color coding** - Green for good, red for bad, yellow for warning
4. **Empty states** - Handle zero data gracefully
5. **Loading states** - Skeleton loaders for charts and tables
6. **Error handling** - Show retry options on failure

## When to Use

- Analytics and reporting interfaces
- Admin panels and back-office tools
- Monitoring and operations dashboards
- Business intelligence displays
- Real-time data visualization

## Notes

- Test with real data volumes
- Consider print layouts for reports
- Optimize chart rendering for large datasets
- Provide export functionality for data tables
