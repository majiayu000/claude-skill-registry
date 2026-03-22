---
name: lovable-dashboard-pro
description: "Generate data-rich, interactive analytics dashboards in Lovable with advanced chart layouts, real-time patterns, KPI cards, and intuitive navigation."
homepage: https://lovable.dev
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"📊"}}
---

# Lovable Dashboard Pro

## Purpose

Generate professional-grade dashboard UIs in Lovable for analytics, admin panels, CRM, monitoring, or any data-heavy application. Produces proper data component hierarchy, interactive chart elements, efficient navigation, and responsive layouts that go beyond basic table-and-sidebar defaults.

> **Platform context**: Lovable generates React + TypeScript + Tailwind CSS + shadcn/ui apps. Charts should use Recharts (available in Lovable). Data tables should use shadcn's Table or TanStack Table. Icons from Lucide React.

## Inputs

| Parameter        | Required | Values                                                                                     | Default             |
|------------------|----------|--------------------------------------------------------------------------------------------|---------------------|
| `domain`         | yes      | marketing_analytics, financial_reporting, project_management, devops_monitoring, crm, healthcare, sales, hr | — |
| `dashboard_type` | no       | overview, analytical, operational, detail                                                   | overview            |
| `density`        | no       | compact, balanced, spacious                                                                 | balanced            |
| `theme`          | no       | light-professional, dark-operational, high-contrast                                         | light-professional  |

## Workflow

### 1. Classify Dashboard Type

Determine layout pattern based on `dashboard_type`:

| Type        | Layout                                                                 | Purpose                      |
|-------------|------------------------------------------------------------------------|------------------------------|
| overview    | KPI cards (top) → primary charts (2-col middle) → data table (bottom) | Quick status at a glance     |
| analytical  | Filter bar (top) → bento chart grid (3-col) → drill-down panel        | Data exploration, comparison |
| operational | Status banner (top) → real-time metrics (3-col) → timeline + log      | Live monitoring              |
| detail      | Entity header → tabbed content → action panel                         | Deep dive into single record |

### 2. Build Layout Architecture

**Sidebar Navigation**:
- Collapsible: 240px expanded (icon + label), 64px collapsed (icon only).
- Toggle button at bottom. Sections grouped with subtle dividers.
- Active item: primary color background or left border accent.

**Top Bar**:
- Height 56px. Breadcrumb trail (left), search with ⌘K hint (center), notification bell + avatar (right).
- On scroll: `backdrop-filter: blur(10px)`, subtle bottom border.

**Content Grid** (CSS Grid, responsive):
- Desktop (1280px+): Full sidebar + multi-column grid.
- Tablet (768–1279px): Collapsed sidebar + 2-column grid.
- Mobile (<768px): Hidden sidebar (hamburger) + single column.

**Widget Containers**:
- Card with theme-appropriate `border-radius`, subtle 1px border, optional header (title + action menu).
- Padding: 16px (compact), 20px (balanced), 28px (spacious).

### 3. Design Data Components

**KPI Cards**:
- Large primary number (2rem+, tabular numerals / monospace).
- Trend indicator: up/down arrow, green for positive, red for negative.
- Percentage change, sparkline (40px height), comparison period label.
- Hover: lifts 2px with tooltip showing detailed breakdown.

**Charts** (Recharts):
- Clean axis labels (0.75rem, muted color). Grid lines at 0.08 opacity.
- Data points with 6px radius on line charts. Smooth 600ms entrance animation.
- Interactive tooltip on hover. Crosshair guide lines. Maximum 5 data series colors.

**Data Tables** (shadcn Table):
- Sortable column headers with arrow indicators. Alternating row backgrounds.
- Row hover highlight. Inline action buttons on hover. Pagination with page size selector.

**Status Indicators**:
- Green (#22c55e), yellow (#eab308), red (#ef4444). Only red gets subtle pulse animation.
- Always include text label alongside color dot (accessibility).

**Activity/Event Feed**:
- Monospace timestamp + event icon + description. New items fade in from top.
- Scrollable container with max-height.

### 4. Inject Dashboard Interactions

**Date Range Picker**:
- Preset buttons: Today, 7d, 30d, 90d, YTD, Custom.
- Custom opens calendar popover. Selection triggers skeleton loading on widgets.

**Filter System**:
- Filter button opens dropdown panel. Active filters as removable chips.
- Chip removal animates out (200ms). Filters trigger skeleton loading (300ms min).

**Chart Interactions**:
- Click bar/pie segment to filter related widgets (300ms cross-fade).
- Hover tooltip with 150ms delay.

**Widget Controls**:
- Three-dot menu: expand full-screen (400ms ease-out), export, refresh, configure.
- Refresh icon rotates 360° over 600ms.

**Global Refresh**:
- Button in top bar. Icon rotates. All widgets show skeleton loading. Data fades in (300ms).

### 5. Apply Typography and Color

**Numeric values**: Tabular numerals — use `font-variant-numeric: tabular-nums` or monospace font (Geist Mono, JetBrains Mono).

**Section labels**: 0.75rem, uppercase, `letter-spacing: 0.05em`, muted color.

**Chart color palettes**:

| Theme             | Colors                                        |
|-------------------|-----------------------------------------------|
| light-professional | #3b82f6, #8b5cf6, #06b6d4, #f59e0b, #10b981 |
| dark-operational   | #60a5fa, #a78bfa, #22d3ee, #fbbf24, #34d399 |
| high-contrast      | #2563eb, #7c3aed, #0891b2, #d97706, #059669 |

**Background hierarchy**: Sidebar slightly darker → content area → widget cards slightly lighter. Creates depth without heavy shadows.

### 6. Apply Density Settings

| Setting  | Widget Padding | Row Height | Font Adjustment | Widget Gap |
|----------|---------------|------------|-----------------|------------|
| compact  | 12px          | 36px       | -1 step         | 8px        |
| balanced | 20px          | 44px       | standard        | 16px       |
| spacious | 28px          | 52px       | +1 step         | 24px       |

## Output Format

Complete dashboard layout with sidebar, top bar, and content area populated with domain-appropriate data components. All widgets include interactive states, loading states, and responsive behavior. Uses Recharts for charts, shadcn Table for data tables, Lucide icons, and Tailwind CSS.

## Guardrails

- Never use more than 5 colors in a single chart. Group smaller categories into "Other."
- All numeric data must use tabular/monospace numerals.
- Status colors must be consistent: green=success, yellow=warning, red=critical, blue=info.
- Tables must include sortable headers and row hover states.
- Loading states must use skeleton placeholders matching content shape. Never use centered spinners.
- Charts must have `aria-label` describing the data trend.
- Never display raw timestamps — format as "2 hours ago" or "Mar 15, 2025."
- Dashboard must work at 1024px minimum without horizontal scroll.
- Use Recharts for all chart components. Do not introduce Chart.js, D3, or other chart libraries.

## Failure Handling

| Problem | Follow-up Prompt |
|---------|-----------------|
| Flat KPI cards | "Restructure KPI cards: large metric (2rem, tabular font), trend arrow (green/red), percentage change, sparkline (40px height), comparison text. Hover tooltip with breakdown." |
| Non-interactive charts | "Add Recharts tooltips on hover (150ms delay). Add crosshair guide lines. Add 600ms ease-out entrance animation. Make segments clickable to filter." |
| Single column layout | "Use CSS Grid: top row 4-col KPIs, middle 2-col charts (60/40), bottom full-width table. Collapsible sidebar (240px/64px)." |
| Missing loading states | "Add skeleton placeholders matching widget shapes. Rectangular for charts, row-shaped for tables, card-shaped for KPIs. Min 300ms display." |
| Sidebar not collapsible | "Make sidebar collapsible: 240px expanded with icon+label, 64px collapsed with icon only. Toggle button at bottom. Persist state." |

## Examples

### Example 1: Marketing Analytics Overview

**Input**: `domain=marketing_analytics`, `dashboard_type=overview`, `density=balanced`, `theme=light-professional`

**Prompt to Lovable**:
```
Build a marketing analytics dashboard:

LAYOUT: Left sidebar (collapsible 240px/64px) with nav items: Overview, Campaigns, Audiences, Content, Reports, Settings. Top bar with breadcrumbs, search input (Cmd+K hint), notification bell, avatar. Main content in CSS Grid.

TOP ROW (4 KPI cards): Total Visitors (sparkline), Conversion Rate (trend arrow), Revenue (comparison to last period), Active Campaigns (status count). Numbers in tabular-nums monospace. Cards lift on hover.

MIDDLE (2-column, 60/40): Left — line chart showing traffic over 30 days with 3 series (organic, paid, referral) using Recharts. Right — donut chart of traffic sources. Interactive tooltips on hover.

BOTTOM (full-width): Campaign performance table with columns: Name, Status (color dot + label), Impressions, Clicks, CTR, Spend, ROAS. Sortable headers, row hover highlight, pagination.

Date range picker at top: Today, 7d, 30d, 90d, Custom. Changing triggers skeleton loading.

Colors: #3b82f6, #8b5cf6, #06b6d4, #f59e0b, #10b981 for chart series.
```

### Example 2: DevOps Monitoring Operational

**Input**: `domain=devops_monitoring`, `dashboard_type=operational`, `density=compact`, `theme=dark-operational`

**Prompt to Lovable**:
```
Build a DevOps monitoring dashboard with dark theme:

LAYOUT: Dark background (slate-950). Collapsed sidebar (64px icons). Top bar with system status indicator and global refresh.

TOP BANNER: System health — green/yellow/red status with uptime percentage. Only red gets pulse animation.

METRICS ROW (3 cards): CPU Usage (gauge chart), Memory Usage (bar), Active Connections (counter with sparkline). Compact 12px padding, tabular monospace numbers.

MAIN (2-column split): Left — time-series chart (request latency p50/p95/p99 over 1 hour, auto-refreshing). Right — event log (scrollable, monospace timestamps, color-coded severity icons, new items fade in from top).

All widgets: 8px gaps, dark card backgrounds (slate-900), subtle borders (slate-800). Chart colors: #60a5fa, #a78bfa, #22d3ee, #fbbf24, #34d399.
```

## Security & Privacy

This skill generates text prompts only. It does not access external endpoints, transmit data, or execute code. All output is prompt text intended for the Lovable.dev platform.

## Trust Statement

This skill contains no executable scripts. It produces Lovable-compatible dashboard generation prompts. It does not access the filesystem, network, or any external service.
