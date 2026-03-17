---
name: data-visualizer
description: Expert in creating charts, dashboards, and data visualizations using modern libraries
version: 1.0.0
tags: [data-viz, charts, dashboards, d3, recharts, analytics]
---

# Data Visualizer Skill

I help you build beautiful, interactive data visualizations and dashboards.

## What I Do

**Chart Creation:**

- Line charts, bar charts, pie charts
- Area charts, scatter plots, heatmaps
- Complex visualizations (Sankey, treemaps, network graphs)

**Dashboard Building:**

- KPI cards and metrics
- Real-time data dashboards
- Interactive filters and drill-downs
- Responsive layouts

**Data Presentation:**

- Data storytelling
- Color schemes and accessibility
- Animation and interactions
- Export capabilities

## Library Selection Guide

### Recharts (Recommended for React)

**Best for:**

- Quick, simple charts
- React/Next.js projects
- Standard chart types
- Responsive design

**Example:**

```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

const data = [
  { month: 'Jan', revenue: 4000, expenses: 2400 },
  { month: 'Feb', revenue: 3000, expenses: 1398 },
  { month: 'Mar', revenue: 2000, expenses: 9800 },
]

function RevenueChart() {
  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="month" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
      <Line type="monotone" dataKey="expenses" stroke="#82ca9d" />
    </LineChart>
  )
}
```

---

### Chart.js (Recommended for Vue/Angular)

**Best for:**

- Framework-agnostic
- Simple API
- Good documentation
- Standard chart types

**Example:**

```typescript
import { Chart } from 'chart.js/auto'

const ctx = document.getElementById('myChart')
const chart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Sales',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor: 'rgba(54, 162, 235, 0.5)'
      }
    ]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Monthly Sales' }
    }
  }
})
```

---

### D3.js (Advanced)

**Best for:**

- Custom visualizations
- Complex interactions
- Full control over rendering
- Data-driven documents

**When to use:**

- Need custom chart type
- Complex data transformations
- Advanced interactions
- Publication-quality graphics

**Example:**

```typescript
import * as d3 from 'd3'

function createBarChart(data: Array<{ name: string; value: number }>) {
  const width = 600
  const height = 400
  const margin = { top: 20, right: 20, bottom: 30, left: 40 }

  const svg = d3.select('#chart').append('svg').attr('width', width).attr('height', height)

  const x = d3
    .scaleBand()
    .domain(data.map(d => d.name))
    .range([margin.left, width - margin.right])
    .padding(0.1)

  const y = d3
    .scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([height - margin.bottom, margin.top])

  svg
    .selectAll('rect')
    .data(data)
    .join('rect')
    .attr('x', d => x(d.name))
    .attr('y', d => y(d.value))
    .attr('height', d => y(0) - y(d.value))
    .attr('width', x.bandwidth())
    .attr('fill', 'steelblue')

  // Add axes
  svg
    .append('g')
    .attr('transform', `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))

  svg.append('g').attr('transform', `translate(${margin.left},0)`).call(d3.axisLeft(y))
}
```

---

## Dashboard Patterns

### Pattern 1: KPI Dashboard

**Use case:** Executive dashboard with key metrics

```typescript
// components/KPIDashboard.tsx
import { Card } from '@/components/ui/card'

interface KPICardProps {
  title: string
  value: string | number
  change: number
  trend: 'up' | 'down'
}

function KPICard({ title, value, change, trend }: KPICardProps) {
  const trendColor = trend === 'up' ? 'text-green-600' : 'text-red-600'
  const trendIcon = trend === 'up' ? '↑' : '↓'

  return (
    <Card className="p-6">
      <h3 className="text-sm font-medium text-gray-600">{title}</h3>
      <div className="mt-2 flex items-baseline">
        <p className="text-3xl font-semibold">{value}</p>
        <span className={`ml-2 text-sm ${trendColor}`}>
          {trendIcon} {Math.abs(change)}%
        </span>
      </div>
    </Card>
  )
}

export default function Dashboard() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <KPICard title="Total Revenue" value="$45,231" change={12.5} trend="up" />
      <KPICard title="Active Users" value="2,350" change={-5.2} trend="down" />
      <KPICard title="Conversion Rate" value="3.24%" change={8.1} trend="up" />
      <KPICard title="Avg Order Value" value="$158" change={2.3} trend="up" />
    </div>
  )
}
```

---

### Pattern 2: Real-Time Dashboard

**Use case:** Live data monitoring

```typescript
// components/RealtimeDashboard.tsx
'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

interface DataPoint {
  time: string
  value: number
}

export default function RealtimeDashboard() {
  const [data, setData] = useState<DataPoint[]>([])

  useEffect(() => {
    // Fetch initial data
    fetch('/api/metrics/realtime')
      .then(res => res.json())
      .then(setData)

    // Subscribe to real-time updates
    const eventSource = new EventSource('/api/metrics/stream')

    eventSource.onmessage = (event) => {
      const newDataPoint = JSON.parse(event.data)

      setData(prev => {
        const updated = [...prev, newDataPoint]
        // Keep last 20 data points
        return updated.slice(-20)
      })
    }

    return () => eventSource.close()
  }, [])

  return (
    <div className="p-6 bg-white rounded-lg shadow">
      <h2 className="text-xl font-bold mb-4">Live Traffic</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#8884d8"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
```

**API Route for SSE:**

```typescript
// app/api/metrics/stream/route.ts
export async function GET(req: Request) {
  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      const interval = setInterval(async () => {
        const value = Math.floor(Math.random() * 100)
        const time = new Date().toLocaleTimeString()

        const data = `data: ${JSON.stringify({ time, value })}\n\n`
        controller.enqueue(encoder.encode(data))
      }, 1000)

      // Cleanup on close
      req.signal.addEventListener('abort', () => {
        clearInterval(interval)
        controller.close()
      })
    }
  })

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      Connection: 'keep-alive'
    }
  })
}
```

---

### Pattern 3: Interactive Dashboard with Filters

```typescript
// components/SalesDashboard.tsx
'use client'

import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

type Period = '7d' | '30d' | '90d'
type Region = 'all' | 'us' | 'eu' | 'asia'

export default function SalesDashboard() {
  const [period, setPeriod] = useState<Period>('30d')
  const [region, setRegion] = useState<Region>('all')

  const { data, loading } = useSalesData({ period, region })

  return (
    <div className="space-y-6">
      {/* Filters */}
      <div className="flex gap-4">
        <select
          value={period}
          onChange={(e) => setPeriod(e.target.value as Period)}
          className="px-4 py-2 border rounded"
        >
          <option value="7d">Last 7 days</option>
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
        </select>

        <select
          value={region}
          onChange={(e) => setRegion(e.target.value as Region)}
          className="px-4 py-2 border rounded"
        >
          <option value="all">All Regions</option>
          <option value="us">United States</option>
          <option value="eu">Europe</option>
          <option value="asia">Asia</option>
        </select>
      </div>

      {/* Chart */}
      {loading ? (
        <div>Loading...</div>
      ) : (
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="sales" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}

// Custom hook for data fetching
function useSalesData({ period, region }: { period: Period, region: Region }) {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    fetch(`/api/sales?period=${period}&region=${region}`)
      .then(res => res.json())
      .then(data => {
        setData(data)
        setLoading(false)
      })
  }, [period, region])

  return { data, loading }
}
```

---

## Chart Types Guide

### Line Chart

**Best for:** Trends over time, continuous data

```typescript
<LineChart data={data}>
  <Line type="monotone" dataKey="value" stroke="#8884d8" />
</LineChart>
```

**Use when:**

- Stock prices, temperature, website traffic
- Showing change over time
- Multiple data series comparison

---

### Bar Chart

**Best for:** Comparing categories

```typescript
<BarChart data={data}>
  <Bar dataKey="value" fill="#8884d8" />
</BarChart>
```

**Use when:**

- Sales by product, users by country
- Discrete categories
- Ranking/comparison

---

### Pie/Donut Chart

**Best for:** Part-to-whole relationships

```typescript
<PieChart>
  <Pie data={data} dataKey="value" nameKey="name" fill="#8884d8" />
</PieChart>
```

**Use when:**

- Market share, budget allocation
- Proportions (max 5-7 slices)
- Simple percentages

⚠️ **Avoid when:**

- Too many categories (> 7)
- Precise comparison needed (use bar chart)

---

### Area Chart

**Best for:** Volume over time

```typescript
<AreaChart data={data}>
  <Area type="monotone" dataKey="value" fill="#8884d8" />
</AreaChart>
```

**Use when:**

- Cumulative totals
- Filled regions show magnitude
- Stacked categories

---

### Scatter Plot

**Best for:** Correlation between variables

```typescript
<ScatterChart>
  <Scatter data={data} fill="#8884d8" />
</ScatterChart>
```

**Use when:**

- Finding correlations
- Outlier detection
- Distribution analysis

---

### Heatmap

**Best for:** Intensity across two dimensions

```typescript
// Using D3
const colorScale = d3.scaleSequential(d3.interpolateBlues).domain([0, d3.max(data)])

svg
  .selectAll('rect')
  .data(data)
  .join('rect')
  .attr('fill', d => colorScale(d.value))
```

**Use when:**

- Time-based patterns (day/hour)
- Geographic intensity
- Matrix data

---

## Responsive Design

### Pattern: Mobile-Friendly Charts

```typescript
'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, ResponsiveContainer } from 'recharts'

export default function ResponsiveChart({ data }) {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768)
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  return (
    <ResponsiveContainer width="100%" height={isMobile ? 200 : 400}>
      <LineChart data={data}>
        <Line
          dataKey="value"
          stroke="#8884d8"
          strokeWidth={isMobile ? 1 : 2}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
```

---

## Color Schemes

### Accessible Colors

```typescript
// colors.ts
export const chartColors = {
  // WCAG AA compliant
  primary: '#0066CC', // Blue
  success: '#007A3D', // Green
  warning: '#C87000', // Orange
  danger: '#D32F2F', // Red

  // Multi-series (colorblind-safe)
  series: [
    '#0066CC', // Blue
    '#CC6600', // Orange
    '#7A00CC', // Purple
    '#00CC66', // Green
    '#CC0066' // Magenta
  ]
}
```

**Colorblind-Safe Palettes:**

```typescript
// For up to 5 data series
const colorblindSafe = [
  '#000000', // Black
  '#E69F00', // Orange
  '#56B4E9', // Sky Blue
  '#009E73', // Green
  '#F0E442' // Yellow
]
```

---

## Data Formatting

### Number Formatting

```typescript
// utils/formatters.ts

export function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value)
}

export function formatPercent(value: number): string {
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: 1,
    maximumFractionDigits: 1,
  }).format(value / 100)
}

export function formatNumber(value: number): string {
  if (value >= 1000000) {
    return `${(value / 1000000).toFixed(1)}M`
  }
  if (value >= 1000) {
    return `${(value / 1000).toFixed(1)}K`
  }
  return value.toFixed(0)
}

// Usage in chart
<YAxis tickFormatter={formatCurrency} />
```

---

## Export Functionality

### Export Chart as PNG

```typescript
'use client'

import html2canvas from 'html2canvas'

export function ExportableChart({ children }) {
  const chartRef = useRef<HTMLDivElement>(null)

  const exportToPNG = async () => {
    if (!chartRef.current) return

    const canvas = await html2canvas(chartRef.current)
    const link = document.createElement('a')
    link.download = 'chart.png'
    link.href = canvas.toDataURL()
    link.click()
  }

  return (
    <div>
      <button onClick={exportToPNG} className="mb-4 px-4 py-2 bg-blue-600 text-white rounded">
        Export as PNG
      </button>
      <div ref={chartRef}>
        {children}
      </div>
    </div>
  )
}
```

### Export Data as CSV

```typescript
export function exportToCSV(data: any[], filename: string) {
  const headers = Object.keys(data[0])
  const csv = [
    headers.join(','),
    ...data.map(row => headers.map(h => row[h]).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const link = document.createElement('a')
  link.download = `${filename}.csv`
  link.href = URL.createObjectURL(blob)
  link.click()
}

// Usage
<button onClick={() => exportToCSV(data, 'sales-data')}>
  Export to CSV
</button>
```

---

## Performance Optimization

### Lazy Loading Charts

```typescript
// Lazy load chart libraries (reduce initial bundle)
import dynamic from 'next/dynamic'

const LineChart = dynamic(
  () => import('recharts').then(mod => mod.LineChart),
  { ssr: false }
)

export default function ChartPage() {
  return <LineChart data={data} />
}
```

### Virtualization for Large Datasets

```typescript
import { useVirtualizer } from '@tanstack/react-virtual'

export function LargeDataTable({ data }: { data: any[] }) {
  const parentRef = useRef<HTMLDivElement>(null)

  const virtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50,
  })

  return (
    <div ref={parentRef} className="h-96 overflow-auto">
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div key={virtualRow.index} className="py-2 border-b">
            {data[virtualRow.index].name}: {data[virtualRow.index].value}
          </div>
        ))}
      </div>
    </div>
  )
}
```

---

## Animation Best Practices

### Smooth Transitions

```typescript
<LineChart data={data}>
  <Line
    type="monotone"
    dataKey="value"
    stroke="#8884d8"
    animationDuration={500}
    animationEasing="ease-in-out"
  />
</LineChart>
```

### Disable Animation for Real-Time

```typescript
// For real-time dashboards, disable animation
<Line
  dataKey="value"
  isAnimationActive={false}
/>
```

---

## Common Patterns

### Pattern: Drill-Down Chart

```typescript
'use client'

import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis } from 'recharts'

export default function DrillDownChart() {
  const [level, setLevel] = useState<'year' | 'month' | 'day'>('year')
  const [selectedYear, setSelectedYear] = useState<number | null>(null)

  const handleBarClick = (data: any) => {
    if (level === 'year') {
      setSelectedYear(data.year)
      setLevel('month')
    } else if (level === 'month') {
      setLevel('day')
    }
  }

  const goBack = () => {
    if (level === 'day') setLevel('month')
    else if (level === 'month') {
      setLevel('year')
      setSelectedYear(null)
    }
  }

  return (
    <div>
      {level !== 'year' && (
        <button onClick={goBack} className="mb-4">← Back</button>
      )}

      <BarChart data={getData(level, selectedYear)} width={600} height={300}>
        <Bar dataKey="value" fill="#8884d8" onClick={handleBarClick} />
        <XAxis dataKey="name" />
        <YAxis />
      </BarChart>
    </div>
  )
}
```

---

## When to Use Me

**Perfect for:**

- Building analytics dashboards
- Creating interactive charts
- Data storytelling
- Real-time monitoring
- Visualizing complex datasets

**I'll help you:**

- Choose the right chart type
- Implement responsive layouts
- Add interactivity
- Optimize performance
- Ensure accessibility

## What I'll Create

```
📊 Charts and Visualizations
📈 KPI Dashboards
🎨 Custom Color Schemes
📱 Responsive Layouts
⚡ Real-Time Updates
💾 Export Functionality
```

Let's make your data beautiful and understandable!
