---
name: dashboard-design
description: Design effective dashboards with clear layouts, KPI displays, data grids, and real-time updates. Covers dashboard patterns, information hierarchy, responsive grids, widget design, and admin panel layouts. Use for building analytics dashboards, admin interfaces, and monitoring displays.
---

# Dashboard Design

Create effective, information-rich dashboards that surface key data clearly.

## Instructions

1. **Prioritize information** - Most important metrics at top-left
2. **Use consistent card layouts** - Same styling for similar data types
3. **Design for scanning** - Users glance, not read; make data obvious
4. **Show context** - Compare to previous periods, show trends
5. **Enable action** - Dashboards should lead to decisions

## Dashboard Layout Patterns

### Standard Admin Dashboard

```tsx
function AdminDashboard() {
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      {/* Top Navigation */}
      <header className="sticky top-0 z-50 bg-white dark:bg-gray-800 border-b shadow-sm">
        <div className="flex items-center justify-between h-16 px-6">
          <Logo />
          <div className="flex items-center gap-4">
            <SearchInput />
            <NotificationBell />
            <UserMenu />
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar Navigation */}
        <aside className="hidden lg:block w-64 bg-white dark:bg-gray-800 border-r min-h-[calc(100vh-4rem)] sticky top-16">
          <nav className="p-4 space-y-2">
            <SidebarLink icon={HomeIcon} label="Overview" active />
            <SidebarLink icon={ChartIcon} label="Analytics" />
            <SidebarLink icon={UsersIcon} label="Customers" />
            <SidebarLink icon={SettingsIcon} label="Settings" />
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {/* Page Header */}
          <div className="mb-6">
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
              Dashboard Overview
            </h1>
            <p className="text-gray-500">Welcome back, here's what's happening</p>
          </div>

          {/* KPI Cards Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            <KPICard
              title="Total Revenue"
              value="$45,231"
              change="+12.5%"
              trend="up"
            />
            <KPICard
              title="Active Users"
              value="2,345"
              change="+5.2%"
              trend="up"
            />
            <KPICard
              title="Conversion Rate"
              value="3.2%"
              change="-0.4%"
              trend="down"
            />
            <KPICard
              title="Avg. Order Value"
              value="$127"
              change="+8.1%"
              trend="up"
            />
          </div>

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <ChartCard title="Revenue Over Time">
              <LineChart data={revenueData} />
            </ChartCard>
            <ChartCard title="Sales by Category">
              <BarChart data={categoryData} />
            </ChartCard>
          </div>

          {/* Data Table */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Orders</CardTitle>
              <Button variant="outline" size="sm">View All</Button>
            </CardHeader>
            <DataTable
              columns={orderColumns}
              data={recentOrders}
              pagination
            />
          </Card>
        </main>
      </div>
    </div>
  );
}
```

### KPI Card Component

```tsx
interface KPICardProps {
  title: string;
  value: string | number;
  change?: string;
  trend?: 'up' | 'down' | 'neutral';
  icon?: React.ComponentType;
  subtitle?: string;
}

function KPICard({ title, value, change, trend, icon: Icon, subtitle }: KPICardProps) {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">
            {title}
          </p>
          <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white">
            {value}
          </p>
          {change && (
            <div className="mt-2 flex items-center gap-1">
              {trend === 'up' && (
                <ArrowUpIcon className="w-4 h-4 text-green-500" />
              )}
              {trend === 'down' && (
                <ArrowDownIcon className="w-4 h-4 text-red-500" />
              )}
              <span className={`text-sm font-medium ${
                trend === 'up' ? 'text-green-600' :
                trend === 'down' ? 'text-red-600' :
                'text-gray-500'
              }`}>
                {change}
              </span>
              <span className="text-sm text-gray-400">vs last month</span>
            </div>
          )}
        </div>
        {Icon && (
          <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <Icon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
          </div>
        )}
      </div>
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
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <div>
          <h3 className="font-semibold text-gray-900 dark:text-white">{title}</h3>
          {subtitle && (
            <p className="text-sm text-gray-500">{subtitle}</p>
          )}
        </div>
        {action}
      </div>
      <div className="p-6">
        {children}
      </div>
    </div>
  );
}
```

## Dashboard Grid Patterns

### Responsive Dashboard Grid

```tsx
// 12-column grid system
<div className="grid grid-cols-12 gap-6">
  {/* Full width */}
  <div className="col-span-12">
    <PageHeader />
  </div>

  {/* 4 equal KPI cards */}
  <div className="col-span-12 sm:col-span-6 lg:col-span-3">
    <KPICard />
  </div>
  <div className="col-span-12 sm:col-span-6 lg:col-span-3">
    <KPICard />
  </div>
  <div className="col-span-12 sm:col-span-6 lg:col-span-3">
    <KPICard />
  </div>
  <div className="col-span-12 sm:col-span-6 lg:col-span-3">
    <KPICard />
  </div>

  {/* 2/3 + 1/3 layout */}
  <div className="col-span-12 lg:col-span-8">
    <MainChart />
  </div>
  <div className="col-span-12 lg:col-span-4">
    <SidePanel />
  </div>

  {/* 50/50 split */}
  <div className="col-span-12 md:col-span-6">
    <ChartA />
  </div>
  <div className="col-span-12 md:col-span-6">
    <ChartB />
  </div>
</div>
```

## Real-Time Dashboard

```tsx
function RealTimeDashboard() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  useEffect(() => {
    // WebSocket for real-time updates
    const ws = new WebSocket('wss://api.example.com/metrics');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMetrics(data);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="space-y-6">
      {/* Live indicator */}
      <div className="flex items-center gap-2">
        <span className="relative flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
          <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500" />
        </span>
        <span className="text-sm text-gray-500">Live</span>
        <span className="text-sm text-gray-400">
          Updated {formatRelativeTime(metrics?.timestamp)}
        </span>
      </div>

      {/* Real-time metrics */}
      <div className="grid grid-cols-4 gap-4">
        <LiveMetric
          label="Active Users"
          value={metrics?.activeUsers}
          sparkline={metrics?.userHistory}
        />
        <LiveMetric
          label="Requests/sec"
          value={metrics?.requestsPerSecond}
          unit="req/s"
        />
        <LiveMetric
          label="Avg Response"
          value={metrics?.avgResponseTime}
          unit="ms"
        />
        <LiveMetric
          label="Error Rate"
          value={metrics?.errorRate}
          unit="%"
          alert={metrics?.errorRate > 1}
        />
      </div>
    </div>
  );
}
```

## Data Table for Dashboards

```tsx
interface DataTableProps<T> {
  columns: ColumnDef<T>[];
  data: T[];
  pagination?: boolean;
  searchable?: boolean;
  actions?: (row: T) => React.ReactNode;
}

function DataTable<T>({ columns, data, pagination, searchable }: DataTableProps<T>) {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const pageSize = 10;

  const filteredData = useMemo(() => {
    if (!search) return data;
    return data.filter(row =>
      Object.values(row).some(val =>
        String(val).toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [data, search]);

  const paginatedData = useMemo(() => {
    if (!pagination) return filteredData;
    const start = (page - 1) * pageSize;
    return filteredData.slice(start, start + pageSize);
  }, [filteredData, page, pagination]);

  return (
    <div>
      {searchable && (
        <div className="mb-4">
          <input
            type="search"
            placeholder="Search..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="px-4 py-2 border rounded-lg w-full max-w-sm"
          />
        </div>
      )}

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-gray-50 dark:bg-gray-800">
            <tr>
              {columns.map(col => (
                <th key={col.key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
            {paginatedData.map((row, i) => (
              <tr key={i} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                {columns.map(col => (
                  <td key={col.key} className="px-6 py-4 whitespace-nowrap text-sm">
                    {col.render ? col.render(row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {pagination && (
        <Pagination
          page={page}
          totalPages={Math.ceil(filteredData.length / pageSize)}
          onPageChange={setPage}
        />
      )}
    </div>
  );
}
```

## Best Practices

1. **5-second rule** - Key metrics should be understood in 5 seconds
2. **Above the fold** - Critical data visible without scrolling
3. **Consistent time ranges** - All charts use same time period
4. **Progressive disclosure** - Summary → details on demand
5. **Empty states** - Show meaningful content when no data
6. **Loading states** - Skeleton screens while loading

## When to Use

- Building admin panels and back-office tools
- Creating analytics dashboards
- Monitoring systems and real-time displays
- Data-heavy business applications
- Internal tools and management interfaces

## Notes

- Consider user role - executives vs analysts have different needs
- Mobile dashboards need different layouts, not just responsive
- Performance matters - virtualize long lists, lazy load charts
- Allow customization - users can arrange their own dashboards
