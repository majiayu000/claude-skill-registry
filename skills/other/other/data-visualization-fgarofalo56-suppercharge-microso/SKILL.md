---
name: data-visualization
description: Create effective data visualizations with React charting libraries. Covers chart selection, Recharts, Chart.js, D3.js basics, real-time data, accessible charts, and color palettes. Use for charts, graphs, dashboards, and data-driven displays.
---

# Data Visualization

Create clear, informative, and accessible data visualizations.

## Instructions

1. **Choose the right chart type** - Match visualization to data story
2. **Keep it simple** - Remove chartjunk, focus on data
3. **Use color meaningfully** - Semantic colors, accessible palettes
4. **Provide context** - Labels, legends, tooltips, annotations
5. **Make it accessible** - Alt text, patterns, screen reader support

## Chart Selection Guide

| Data Type | Best Charts |
|-----------|-------------|
| Trends over time | Line, Area |
| Comparisons | Bar, Column |
| Parts of whole | Pie, Donut (max 5-7 segments) |
| Distribution | Histogram, Box plot |
| Correlation | Scatter, Bubble |
| Hierarchies | Treemap, Sunburst |
| Geographic | Choropleth, Pin map |

## Recharts (Recommended for React)

### Line Chart

```tsx
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const data = [
  { month: 'Jan', revenue: 4000, users: 2400 },
  { month: 'Feb', revenue: 3000, users: 1398 },
  { month: 'Mar', revenue: 5000, users: 3800 },
  { month: 'Apr', revenue: 4500, users: 3908 },
  { month: 'May', revenue: 6000, users: 4800 },
  { month: 'Jun', revenue: 5500, users: 3800 },
];

function RevenueChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
        <XAxis
          dataKey="month"
          tick={{ fill: '#6b7280' }}
          axisLine={{ stroke: '#e5e7eb' }}
        />
        <YAxis
          tick={{ fill: '#6b7280' }}
          axisLine={{ stroke: '#e5e7eb' }}
          tickFormatter={(value) => `$${value / 1000}k`}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#fff',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
          }}
          formatter={(value: number) => [`$${value.toLocaleString()}`, 'Revenue']}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="revenue"
          stroke="#2563eb"
          strokeWidth={2}
          dot={{ fill: '#2563eb', strokeWidth: 2 }}
          activeDot={{ r: 6, fill: '#2563eb' }}
        />
        <Line
          type="monotone"
          dataKey="users"
          stroke="#10b981"
          strokeWidth={2}
          dot={{ fill: '#10b981', strokeWidth: 2 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Bar Chart

```tsx
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';

const data = [
  { name: 'Electronics', value: 4000 },
  { name: 'Clothing', value: 3000 },
  { name: 'Food', value: 2000 },
  { name: 'Books', value: 2780 },
  { name: 'Home', value: 1890 },
];

const COLORS = ['#2563eb', '#7c3aed', '#db2777', '#ea580c', '#16a34a'];

function CategoryChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data} layout="vertical" margin={{ left: 80 }}>
        <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
        <XAxis type="number" tickFormatter={(v) => `$${v / 1000}k`} />
        <YAxis type="category" dataKey="name" />
        <Tooltip
          formatter={(value: number) => [`$${value.toLocaleString()}`, 'Sales']}
        />
        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
          {data.map((entry, index) => (
            <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
```

### Donut Chart

```tsx
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const data = [
  { name: 'Direct', value: 400 },
  { name: 'Organic', value: 300 },
  { name: 'Referral', value: 200 },
  { name: 'Social', value: 100 },
];

const COLORS = ['#2563eb', '#10b981', '#f59e0b', '#ef4444'];

function TrafficDonut() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={100}
          paddingAngle={2}
          dataKey="value"
          label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
        >
          {data.map((entry, index) => (
            <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip formatter={(value: number) => [value.toLocaleString(), 'Visitors']} />
        <Legend />
      </PieChart>
    </ResponsiveContainer>
  );
}
```

### Area Chart with Gradient

```tsx
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

function GradientAreaChart({ data }: { data: DataPoint[] }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
          </linearGradient>
        </defs>
        <XAxis dataKey="date" hide />
        <YAxis hide />
        <Tooltip />
        <Area
          type="monotone"
          dataKey="value"
          stroke="#2563eb"
          strokeWidth={2}
          fill="url(#colorValue)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

## Sparklines

```tsx
// Mini inline charts for KPI cards
function Sparkline({ data, color = '#2563eb', height = 40 }: {
  data: number[];
  color?: string;
  height?: number;
}) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;

  const points = data
    .map((value, i) => {
      const x = (i / (data.length - 1)) * 100;
      const y = 100 - ((value - min) / range) * 100;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <svg width="100%" height={height} viewBox="0 0 100 100" preserveAspectRatio="none">
      <polyline
        points={points}
        fill="none"
        stroke={color}
        strokeWidth="2"
        vectorEffect="non-scaling-stroke"
      />
    </svg>
  );
}

// Usage in KPI card
<div className="flex items-end gap-4">
  <div>
    <p className="text-3xl font-bold">$45,231</p>
    <p className="text-sm text-green-600">+12.5%</p>
  </div>
  <div className="w-24 h-12">
    <Sparkline data={[10, 15, 12, 20, 18, 25, 30, 28, 35]} color="#10b981" />
  </div>
</div>
```

## Accessible Charts

### Providing Alternatives

```tsx
function AccessibleChart({ data, title }: { data: ChartData[]; title: string }) {
  return (
    <figure>
      <figcaption className="font-semibold mb-4">{title}</figcaption>

      {/* Visual chart */}
      <div aria-hidden="true">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            {/* ... chart config ... */}
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Accessible data table (can be visually hidden) */}
      <table className="sr-only">
        <caption>{title} Data Table</caption>
        <thead>
          <tr>
            <th scope="col">Category</th>
            <th scope="col">Value</th>
          </tr>
        </thead>
        <tbody>
          {data.map(item => (
            <tr key={item.name}>
              <td>{item.name}</td>
              <td>{item.value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </figure>
  );
}
```

### Colorblind-Safe Palettes

```tsx
// Okabe-Ito colorblind-safe palette
const COLORBLIND_SAFE = [
  '#0077BB', // Blue
  '#33BBEE', // Cyan
  '#009988', // Teal
  '#EE7733', // Orange
  '#CC3311', // Red
  '#EE3377', // Magenta
  '#BBBBBB', // Grey
];

// Use patterns in addition to colors
const PATTERNS = [
  'url(#pattern-dots)',
  'url(#pattern-lines)',
  'url(#pattern-crosses)',
  'url(#pattern-squares)',
];
```

## Real-Time Charts

```tsx
import { useState, useEffect, useRef } from 'react';

function RealTimeChart() {
  const [data, setData] = useState<DataPoint[]>([]);
  const maxPoints = 30;

  useEffect(() => {
    const ws = new WebSocket('wss://api.example.com/metrics');

    ws.onmessage = (event) => {
      const newPoint = JSON.parse(event.data);
      setData(prev => {
        const updated = [...prev, newPoint];
        // Keep only last N points for performance
        return updated.slice(-maxPoints);
      });
    };

    return () => ws.close();
  }, []);

  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <Line
          type="monotone"
          dataKey="value"
          stroke="#2563eb"
          strokeWidth={2}
          dot={false}
          isAnimationActive={false} // Disable animation for real-time
        />
        <YAxis domain={['dataMin - 10', 'dataMax + 10']} />
        <XAxis dataKey="timestamp" hide />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

## Chart.js Alternative

```tsx
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function ChartJSExample() {
  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: true, text: 'Monthly Revenue' },
    },
    scales: {
      y: { beginAtZero: true },
    },
  };

  const data = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Revenue',
        data: [4000, 3000, 5000, 4500, 6000, 5500],
        borderColor: 'rgb(37, 99, 235)',
        backgroundColor: 'rgba(37, 99, 235, 0.5)',
        tension: 0.3,
      },
    ],
  };

  return (
    <div style={{ height: '400px' }}>
      <Line options={options} data={data} />
    </div>
  );
}
```

## Best Practices

1. **Start Y-axis at zero** for bar charts (context matters for line charts)
2. **Limit pie segments** - Max 5-7 slices, group small values into "Other"
3. **Use consistent colors** - Same color = same metric across charts
4. **Add context** - Show comparison periods, targets, benchmarks
5. **Responsive design** - Charts should resize gracefully
6. **Performance** - Virtualize large datasets, debounce updates

## When to Use

- Building analytics dashboards
- Creating reports and data presentations
- Displaying KPIs and metrics
- Monitoring real-time data
- Making data-driven applications

## Notes

- Recharts is best for React (declarative, composable)
- Chart.js offers more chart types out of the box
- D3.js for custom/complex visualizations
- Always provide data table alternative for accessibility
