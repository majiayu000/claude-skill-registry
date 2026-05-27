# Dashboard Scaffold Skill

> **Generate Admin Dashboard**: Sidebar, stats, tables, and charts.

---

## 🎯 Purpose

When user says: "Create an admin dashboard" or "Add dashboard"

Generate a complete dashboard with:
- Sidebar navigation
- Stats cards
- Data tables
- Charts

---

## 📁 Generated Structure

```
src/
├── app/
│   └── dashboard/
│       ├── layout.tsx
│       ├── page.tsx
│       ├── analytics/
│       │   └── page.tsx
│       ├── users/
│       │   └── page.tsx
│       └── settings/
│           └── page.tsx
└── components/
    └── dashboard/
        ├── sidebar.tsx
        ├── header.tsx
        ├── stat-card.tsx
        ├── chart.tsx
        └── data-table.tsx
```

---

## 🏠 Dashboard Layout

```tsx
// app/dashboard/layout.tsx
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { auth } from "@/auth"
import { redirect } from "next/navigation"

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const session = await auth()
  if (!session?.user) redirect("/login")

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header user={session.user} />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
```

---

## 📊 Dashboard Page

```tsx
// app/dashboard/page.tsx
import { StatCard } from "@/components/dashboard/stat-card"
import { RevenueChart } from "@/components/dashboard/charts/revenue-chart"
import { RecentOrders } from "@/components/dashboard/recent-orders"

export default async function DashboardPage() {
  const stats = await getStats()

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Revenue"
          value={`$${stats.revenue.toLocaleString()}`}
          change="+12.5%"
          changeType="positive"
          icon="💰"
        />
        <StatCard
          title="Total Orders"
          value={stats.orders.toLocaleString()}
          change="+8.2%"
          changeType="positive"
          icon="📦"
        />
        <StatCard
          title="Active Users"
          value={stats.users.toLocaleString()}
          change="+3.1%"
          changeType="positive"
          icon="👥"
        />
        <StatCard
          title="Conversion Rate"
          value={`${stats.conversionRate}%`}
          change="-0.5%"
          changeType="negative"
          icon="📈"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <RevenueChart />
        </div>
        <div>
          <RecentOrders />
        </div>
      </div>
    </div>
  )
}
```

---

## 🧭 Sidebar

```tsx
// components/dashboard/sidebar.tsx
"use client"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: "🏠" },
  { name: "Analytics", href: "/dashboard/analytics", icon: "📊" },
  { name: "Users", href: "/dashboard/users", icon: "👥" },
  { name: "Orders", href: "/dashboard/orders", icon: "📦" },
  { name: "Products", href: "/dashboard/products", icon: "🏷️" },
  { name: "Settings", href: "/dashboard/settings", icon: "⚙️" },
]

export function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-64 bg-gray-900 text-white flex flex-col">
      <div className="p-4 border-b border-gray-800">
        <h1 className="text-xl font-bold">Admin Panel</h1>
      </div>

      <nav className="flex-1 p-4 space-y-1">
        {navigation.map((item) => (
          <Link
            key={item.name}
            href={item.href}
            className={cn(
              "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
              pathname === item.href
                ? "bg-gray-800 text-white"
                : "text-gray-400 hover:bg-gray-800 hover:text-white"
            )}
          >
            <span>{item.icon}</span>
            {item.name}
          </Link>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-800">
        <Link href="/dashboard/settings" className="text-sm text-gray-400 hover:text-white">
          Help & Support
        </Link>
      </div>
    </aside>
  )
}
```

---

## 📈 Stat Card

```tsx
// components/dashboard/stat-card.tsx
interface StatCardProps {
  title: string
  value: string
  change: string
  changeType: "positive" | "negative" | "neutral"
  icon: string
}

export function StatCard({ title, value, change, changeType, icon }: StatCardProps) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <span className="text-2xl">{icon}</span>
      </div>
      <p className="mt-2 text-3xl font-bold">{value}</p>
      <p
        className={cn(
          "mt-2 text-sm",
          changeType === "positive" && "text-green-600",
          changeType === "negative" && "text-red-600",
          changeType === "neutral" && "text-gray-600"
        )}
      >
        {change} from last period
      </p>
    </div>
  )
}
```

---

## 📋 Data Table

```tsx
// components/dashboard/data-table.tsx
interface Column<T> {
  key: keyof T
  header: string
  render?: (value: T[keyof T], item: T) => React.ReactNode
}

interface DataTableProps<T> {
  data: T[]
  columns: Column<T>[]
}

export function DataTable<T extends { id: string }>({ data, columns }: DataTableProps<T>) {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((col) => (
              <th key={String(col.key)} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {data.map((row) => (
            <tr key={row.id} className="hover:bg-gray-50">
              {columns.map((col) => (
                <td key={String(col.key)} className="px-6 py-4 whitespace-nowrap">
                  {col.render ? col.render(row[col.key], row) : String(row[col.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

---

**Admin dashboard in minutes!**
