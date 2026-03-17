---
name: bi-builder
description: Build BI dashboards from databases. Use when creating dashboards, charts, or analytics pages with Next.js + shadcn/ui + Recharts + Prisma.
---

# BI Builder

Build BI dashboards from existing databases, from data exploration to full implementation.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend Framework | Next.js 16 (App Router) |
| UI Components | shadcn/ui + Tailwind CSS |
| Charts | Recharts |
| ORM | Prisma |
| Database | MySQL / PostgreSQL / Supabase / SQLite |

## Core Workflow

```
Database Connection → Schema Exploration → Requirements Dialog → Metrics Design → Chart Planning → Page Implementation
```

### Workflow Flexibility

Skip phases based on project state and user needs:

| Scenario | Skip Phases | Starting Point |
|----------|-------------|----------------|
| Project has `prisma/schema.prisma` | Phase 1 | Go directly to Phase 2 schema analysis |
| User has clear requirements and metrics | Phase 3 | Go directly to Phase 4 metrics design |
| Only need a single chart component | Phases 1-5 | Read recharts-guide.md and implement |
| Only need data query logic | Phases 5-6 | End after metrics design |

**Decision criteria:**
- Check if `prisma/schema.prisma` exists in project
- Ask user "Do you have specific metrics requirements?"
- Ask user "Do you need a full dashboard or just a single chart?"

---

## Phase 1: Database Connection

### 1.1 Check and Install Prisma

First, check if Prisma is already installed in the project:

```bash
# Check if prisma is in package.json dependencies
grep -q '"prisma"' package.json && echo "Prisma installed" || echo "Prisma not installed"
```

If Prisma is not installed, install it:

```bash
# Install Prisma as dev dependency
npm install prisma --save-dev

# Install Prisma Client
npm install @prisma/client
```

### 1.2 Initialize Prisma

```bash
# Initialize Prisma (creates prisma/schema.prisma and .env)
npx prisma init
```

**Note:** If `prisma/schema.prisma` already exists, skip this step.

### 1.3 Create .env with Placeholders

**⚠️ Security Note: Never ask users to share database credentials directly.**

First, ask user which database type they use, then create `.env` file with placeholders:

```
Which database are you using?
1. MySQL
2. PostgreSQL
3. Supabase
4. SQLite
```

**For MySQL:**
```env
# Database Connection
# Please fill in your database credentials below
DATABASE_URL="mysql://YOUR_USERNAME:YOUR_PASSWORD@YOUR_HOST:3306/YOUR_DATABASE"

# Example:
# DATABASE_URL="mysql://root:password123@localhost:3306/myapp_db"
```

**For PostgreSQL:**
```env
# Database Connection
# Please fill in your database credentials below
DATABASE_URL="postgresql://YOUR_USERNAME:YOUR_PASSWORD@YOUR_HOST:5432/YOUR_DATABASE"

# Example:
# DATABASE_URL="postgresql://postgres:password123@localhost:5432/myapp_db"
```

**For Supabase:**
```env
# Supabase Database Connection
# Find your connection string in: Supabase Dashboard → Project Settings → Database → Connection string → URI
DATABASE_URL="postgresql://postgres.YOUR_PROJECT_REF:YOUR_PASSWORD@aws-0-YOUR_REGION.pooler.supabase.com:6543/postgres?pgbouncer=true"

# Direct connection (for migrations)
DIRECT_URL="postgresql://postgres.YOUR_PROJECT_REF:YOUR_PASSWORD@aws-0-YOUR_REGION.pooler.supabase.com:5432/postgres"

# Example:
# DATABASE_URL="postgresql://postgres.abcdefghijkl:MyPassword123@aws-0-us-east-1.pooler.supabase.com:6543/postgres?pgbouncer=true"
```

**For SQLite:**
```env
# Database Connection
DATABASE_URL="file:./dev.db"
```

After creating the file, tell the user:

**For MySQL/PostgreSQL:**
```
I've created .env file with placeholders. Please fill in your actual database credentials:
- YOUR_USERNAME → your database username
- YOUR_PASSWORD → your database password
- YOUR_HOST → database host (e.g., localhost or IP address)
- YOUR_DATABASE → database name

Tip: Use a read-only account for safety.

Let me know when you've filled in the credentials.
```

**For Supabase:**
```
I've created .env file with Supabase placeholders. To get your connection string:

1. Go to Supabase Dashboard → Your Project
2. Click "Project Settings" (gear icon)
3. Go to "Database" section
4. Copy the "Connection string" → "URI" format
5. Replace [YOUR-PASSWORD] with your database password

Let me know when you've filled in the credentials.
```

### 1.4 Configure Prisma Schema

After user confirms .env is configured, update `prisma/schema.prisma`:

**For MySQL/PostgreSQL/SQLite:**
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "mysql"  // or postgresql, sqlite
  url      = env("DATABASE_URL")
}
```

**For Supabase (requires directUrl for migrations):**
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

### 1.5 Pull Database Schema

```bash
# Pull schema from existing database
npx prisma db pull

# Generate Prisma Client
npx prisma generate
```

### 1.6 Error Handling

**When connection fails:**
| Error Message | Possible Cause | Solution |
|---------------|----------------|----------|
| `Can't reach database server` | Network/Firewall | Check host address and port accessibility |
| `Access denied` | Insufficient permissions | Verify username, password, and user privileges |
| `Unknown database` | Database doesn't exist | Confirm database name spelling |
| `SSL connection error` | SSL configuration | Add `?sslmode=require` to DATABASE_URL |

**Post-schema pull checks:**
- If few tables (< 3) → Confirm connection to correct database
- If no relationships → May be legacy database, need manual relationship analysis

---

## Phase 2: Schema Exploration & Analysis

### 2.1 Read Generated Schema

After `prisma db pull`, read `prisma/schema.prisma` and analyze:

- **Table structure**: What tables exist, what fields each has
- **Data types**: Numeric, datetime, categorical fields
- **Relationships**: Table associations (one-to-many, many-to-many)
- **Indexes**: Which fields are indexed, indicating common query dimensions

### 2.2 Identify Metric Potential

Identify buildable metrics by field type:

| Field Type | Metric Potential |
|------------|------------------|
| `Decimal`/`Float`/`Int` (amounts, quantities) | Sum, average, max/min |
| `DateTime` | Time series analysis, YoY/MoM comparisons |
| `Enum`/`String` (status, category) | Group statistics, distribution analysis |
| `@relation` | Join aggregations, multi-dimensional analysis |
| `Boolean` | Conversion rates, completion rates |

### 2.3 Generate Data Overview Report

Present database overview to user:

```markdown
## Database Overview

### Core Tables
- **orders** (Orders table): 12 fields, related to users, products
- **users** (Users table): 8 fields
- **products** (Products table): 10 fields, related to categories

### Available Metrics
**Transaction Metrics**
- Total revenue (orders.total)
- Order count (orders.count)
- Average order value (orders.total / orders.count)

**User Metrics**
- Total users (users.count)
- New users (users.created_at)

**Product Metrics**
- Sales ranking (order_items.quantity)
- Category distribution (categories)

### Time Dimensions
- orders.created_at → Supports daily/weekly/monthly analysis
- users.created_at → Supports user growth analysis
```

---

## Phase 3: Requirements Dialog

### 3.1 Questioning Strategy

**Principle: Ask one question at a time, prefer multiple choice, ask in rounds.**

#### Round 1: Industry Identification (Highest Priority)

```
Question 0: What industry is your business in?
Options: E-commerce/Retail / SaaS Software / Financial Services / Content/Media / Education / Healthcare / Logistics/Supply Chain / Other
```

**Industry determines metric direction:**

| Industry | Core Focus | Typical Metrics |
|----------|------------|-----------------|
| **E-commerce/Retail** | Transaction conversion | GMV, AOV, Repeat purchase rate, Return rate, Inventory turnover |
| **SaaS Software** | User retention | MRR/ARR, Churn Rate, LTV, CAC, DAU/MAU |
| **Financial Services** | Risk & return | AUM, Bad debt rate, Delinquency rate, Approval rate |
| **Content/Media** | Traffic monetization | PV/UV, Session duration, Bounce rate, Ad revenue, Paid conversion |
| **Education** | Learning outcomes | Course completion rate, Renewal rate, Referral rate, Study time |
| **Healthcare** | Service efficiency | Visit volume, Bed turnover, Return visit rate, Satisfaction |
| **Logistics/Supply Chain** | Operational efficiency | Order fulfillment rate, Delivery time, Warehouse cost, Turnover rate |

#### Round 2: Core Metrics Confirmation (Use AskUserQuestion tool)

Based on industry + schema analysis, generate metric options:

```
Question 1: Based on [industry] context and database analysis, which core metrics matter most to you? (Multiple select)
Options: [Combine industry typical metrics + schema-supported metrics]
```

```
Question 2: What's your primary time granularity for analysis?
Options: Daily / Weekly / Monthly / Quarterly
```

#### Round 3: Conditional Follow-ups

Only ask when conditions are met:

| Condition | Follow-up |
|-----------|-----------|
| Schema has category tables | "Do you need category filtering?" |
| User selected multiple metrics | "Do you need metric comparisons (YoY/MoM)?" |
| Data volume may be large | "Do you need export functionality?" |

#### Round 4: Confirmation

Show requirements confirmation template, ask "Is the above understanding correct?"

### 3.2 Data Structure Limitation Handling

**When user requirements don't match data, clearly inform:**

| User Request | Missing Data | Response |
|--------------|--------------|----------|
| Regional distribution analysis | No region field | "Database has no region information, cannot implement. Should we analyze by [available dimension] instead?" |
| Trend analysis | No datetime field | "Missing datetime field, can only do static statistics, cannot show trends." |
| User profiling | Limited user fields | "User data is limited, can only track basic metrics (count, new users)." |

### 3.3 Requirements Confirmation Template

Organize user requirements:

```markdown
## Requirements Confirmation

### Dashboard Name
Sales Analytics Dashboard

### Core Metrics (KPI Cards)
1. Total Revenue - orders.total sum
2. Order Count - orders count
3. AOV - Total Revenue / Order Count
4. New Users - users count (this month)

### Chart Requirements
| Chart | Type | Data Source | Dimension |
|-------|------|-------------|-----------|
| Revenue Trend | Line Chart | orders.total | By day/month |
| Category Sales | Pie Chart | categories | Category distribution |
| Top 10 Products | Bar Chart | products | Sales ranking |
| Order Status | Pie Chart | orders.status | Status distribution |

### Filters
- Date range picker
- Product category dropdown
- Order status multi-select

### Other Requirements
- CSV export support
- Responsive layout
```

---

## Phase 4: Metrics Design

### 4.1 Define Metric Calculation Logic

Based on confirmed requirements, define calculation for each metric:

```typescript
// lib/metrics.ts

// KPI Metrics
export async function getKPIs(startDate: Date, endDate: Date) {
  const [revenue, orders, users] = await Promise.all([
    // Total revenue
    prisma.order.aggregate({
      where: { createdAt: { gte: startDate, lte: endDate }, status: { not: 'CANCELLED' } },
      _sum: { total: true },
    }),
    // Order count
    prisma.order.count({
      where: { createdAt: { gte: startDate, lte: endDate }, status: { not: 'CANCELLED' } },
    }),
    // New users
    prisma.user.count({
      where: { createdAt: { gte: startDate, lte: endDate } },
    }),
  ]);

  return {
    revenue: Number(revenue._sum.total) || 0,
    orders,
    avgOrderValue: orders > 0 ? Number(revenue._sum.total) / orders : 0,
    newUsers: users,
  };
}
```

### 4.2 Time Series Metrics

```typescript
// Aggregate by time granularity
export async function getRevenueTrend(
  startDate: Date,
  endDate: Date,
  granularity: 'day' | 'week' | 'month'
) {
  const format = {
    day: '%Y-%m-%d',
    week: '%Y-%u',
    month: '%Y-%m',
  }[granularity];

  return prisma.$queryRaw`
    SELECT
      DATE_FORMAT(created_at, ${format}) as period,
      SUM(total) as revenue,
      COUNT(*) as orders
    FROM orders
    WHERE created_at BETWEEN ${startDate} AND ${endDate}
      AND status != 'CANCELLED'
    GROUP BY period
    ORDER BY period
  `;
}
```

### 4.3 Grouped Metrics

```typescript
// Category distribution
export async function getCategoryDistribution(startDate: Date, endDate: Date) {
  return prisma.$queryRaw`
    SELECT
      c.name as category,
      SUM(oi.quantity * oi.price) as revenue,
      SUM(oi.quantity) as quantity
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    JOIN categories c ON p.category_id = c.id
    JOIN orders o ON oi.order_id = o.id
    WHERE o.created_at BETWEEN ${startDate} AND ${endDate}
      AND o.status != 'CANCELLED'
    GROUP BY c.id, c.name
    ORDER BY revenue DESC
  `;
}
```

**Before writing complex queries → Must read [data-layer.md#data-aggregation-queries](references/data-layer.md#data-aggregation-queries)**

---

## Phase 5: Chart Planning

### 5.1 Visualization Type Selection

| Data Type | Recommended Component | Reason |
|-----------|----------------------|--------|
| Time trends | LineChart / AreaChart | Show change over time |
| Distribution | PieChart | Intuitive proportion display |
| Rankings | BarChart (horizontal) | Easy comparison and reading |
| Multi-metric comparison | ComposedChart | Combine bar and line charts |
| Status distribution | PieChart / BarChart | Show counts per status |
| Detailed records | DataTable | Sortable, filterable, paginated list |
| Transaction logs | DataTable | Search, filter, export capabilities |
| Item listings | DataTable | With actions (view, edit, delete) |

### 5.2 Layout Type Selection

Ask user about their dashboard purpose to recommend a layout:

```
What is the primary purpose of this dashboard?
1. Executive Overview - High-level KPIs for quick decision-making
2. Operations Monitoring - Real-time data and alerts
3. Deep Analysis - Multi-dimensional filtering and exploration
4. Period Comparison - YoY/MoM comparison and benchmarking
```

| Layout Type | Best For | Key Features |
|-------------|----------|--------------|
| Executive Dashboard | C-level, managers | KPI cards + main trend + distribution |
| Operational Dashboard | Operations team | Real-time status + live table + alerts |
| Analytical Dashboard | Analysts | Sidebar filters + drill-down + detailed table |
| Comparison Dashboard | Strategy, planning | Period selector + dual charts + change analysis |

**Before implementing layout → Must read [dashboard-patterns.md#common-bi-layout-patterns](references/dashboard-patterns.md#common-bi-layout-patterns)**

### 5.3 Layout Structure

Default Executive Dashboard layout:

```
┌─────────────────────────────────────────────────────────┐
│ Filter Bar: [Date Range] [Category] [Status] [Apply]    │
├─────────┬─────────┬─────────┬───────────────────────────┤
│ KPI 1   │ KPI 2   │ KPI 3   │ KPI 4                     │
│ Revenue │ Orders  │ AOV     │ New Users                 │
├─────────────────────────────┬───────────────────────────┤
│                             │                           │
│   Revenue Trend (Line)      │   Category Dist (Pie)     │
│   lg:col-span-2             │                           │
│                             │                           │
├─────────────────────────────┴───────────────────────────┤
│                                                         │
│              Top 10 Products (Bar Chart)                │
│                                                         │
├─────────────────────────────────────────────────────────┤
│              Order Details (DataTable)                  │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 6: Page Implementation

### 6.1 Directory Structure

```
app/dashboard/
├── page.tsx              # Main page
├── loading.tsx           # Loading skeleton
└── components/
    ├── kpi-cards.tsx         # KPI cards
    ├── revenue-chart.tsx     # Revenue trend chart
    ├── category-pie.tsx      # Category pie chart
    ├── top-products.tsx      # Product ranking
    ├── data-table.tsx        # Reusable DataTable component
    ├── columns.tsx           # Table column definitions
    ├── filters.tsx           # Filters
    └── export-button.tsx     # Export button

lib/
├── prisma.ts             # Prisma client
└── metrics.ts            # Metric calculation functions

app/api/dashboard/
├── route.ts              # Combined data API
├── kpi/route.ts          # KPI API
├── revenue/route.ts      # Revenue trend API
└── categories/route.ts   # Category data API
```

### 6.2 Implementation Order

1. **Prisma client** → `lib/prisma.ts`
2. **Metric functions** → `lib/metrics.ts`
3. **API routes** → `app/api/dashboard/`
4. **KPI cards** → Simplest, verify data flow first
5. **Chart components** → Implement one by one
6. **Filters** → Add interactivity
7. **Export functionality** → Complete last

### 6.3 Component Implementation

Chart components must use `"use client"` and `ResponsiveContainer`:

```tsx
"use client";

import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from "recharts";

export function RevenueChart({ data }: { data: { period: string; revenue: number }[] }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="period" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="revenue" stroke="hsl(var(--primary))" />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

**Before creating chart components → Must read [recharts-guide.md](references/recharts-guide.md) for the corresponding chart type**

**Before creating DataTable components → Must read [table-patterns.md](references/table-patterns.md)**

**Before implementing page layout → Must read [dashboard-patterns.md](references/dashboard-patterns.md)**

**Before implementing export functionality → Must read [export-patterns.md](references/export-patterns.md)**

---

## Quick Reference

### Prisma Commands

```bash
npx prisma db pull      # Pull schema from database
npx prisma generate     # Generate Prisma Client
npx prisma studio       # Open database management UI
```

### Chart Color Scheme

```tsx
const CHART_COLORS = [
  "hsl(221, 83%, 53%)",  // blue
  "hsl(142, 71%, 45%)",  // green
  "hsl(38, 92%, 50%)",   // amber
  "hsl(0, 84%, 60%)",    // red
  "hsl(262, 83%, 58%)",  // purple
];
```

### Responsive Breakpoints

```tsx
// KPI row
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">

// Main chart area
<div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
  <div className="lg:col-span-2">{/* Large chart */}</div>
  <div>{/* Small chart */}</div>
</div>
```

## Reference Document Usage Rules

**⚠️ Do not read all documents upfront. Only load on-demand when entering the corresponding phase.**

### Required Reading Triggers

| Trigger Timing | Must Read | Section |
|----------------|-----------|---------|
| Entering Phase 4 (before writing Prisma queries) | data-layer.md | `#data-aggregation-queries` |
| Entering Phase 5 (when selecting chart types) | recharts-guide.md | Corresponding chart type section |
| Entering Phase 6 (before implementing page layout) | dashboard-patterns.md | `#responsive-grid-layout` `#kpi-card-component` |
| When user needs DataTable | table-patterns.md | Full document |
| When user needs export functionality | export-patterns.md | Full document |

### Document Index

- [data-layer.md](references/data-layer.md) - Prisma queries, Schema analysis, API design
- [recharts-guide.md](references/recharts-guide.md) - Chart code examples by type
- [table-patterns.md](references/table-patterns.md) - DataTable with sorting, filtering, pagination
- [dashboard-patterns.md](references/dashboard-patterns.md) - Page layouts, KPI cards, filters
- [export-patterns.md](references/export-patterns.md) - CSV export, image export
