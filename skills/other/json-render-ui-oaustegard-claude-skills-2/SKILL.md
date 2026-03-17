---
name: json-render-ui
description: Generate guardrailed UI from natural language. Claude emits constrained JSON, skill runtime renders via Preact. Use when user provides json and requests: Dashboards with metrics, charts, tables; Admin panels; Data visualization interfaces; Form-based applications
metadata:
  version: 0.0.1
---

# JSON Render UI

## Overview

Transform natural language UI requests into working dashboards and applications. Claude acts as the translation layer (prompt → JSON), the skill provides the rendering runtime (JSON → UI).

**Architecture:**
```
User prompt → Claude (constrained by catalog) → UITree JSON → Preact renderer → UI
```

## Output Format

Claude emits a **UITree** structure:

```json
{
  "root": "main",
  "elements": {
    "main": {
      "key": "main",
      "type": "Grid",
      "props": { "columns": 2, "gap": "md" },
      "children": ["metric1", "metric2"]
    },
    "metric1": {
      "key": "metric1",
      "type": "Metric",
      "props": {
        "label": "Revenue",
        "valuePath": "/revenue",
        "format": "currency"
      }
    },
    "metric2": {
      "key": "metric2",
      "type": "Metric",
      "props": {
        "label": "Growth",
        "valuePath": "/growth",
        "format": "percent"
      }
    }
  },
  "data": {
    "revenue": 125000,
    "growth": 0.15
  }
}
```

## Component Catalog

Claude can ONLY use these components. This is the guardrail.

### Layout Components

| Component | Props | Children | Description |
|-----------|-------|----------|-------------|
| `Card` | `title?`, `description?`, `padding?: sm\|md\|lg` | Yes | Container with optional header |
| `Grid` | `columns?: 1-4`, `gap?: sm\|md\|lg` | Yes | CSS grid layout |
| `Stack` | `direction?: horizontal\|vertical`, `gap?: sm\|md\|lg`, `align?: start\|center\|end\|stretch` | Yes | Flexbox stack |

### Data Display

| Component | Props | Children | Description |
|-----------|-------|----------|-------------|
| `Metric` | `label`, `valuePath`, `format?: number\|currency\|percent`, `trend?: up\|down\|neutral`, `trendValue?` | No | Single KPI display |
| `Chart` | `type: bar\|line\|pie\|area`, `dataPath`, `title?`, `height?` | No | Data visualization |
| `Table` | `dataPath`, `columns: [{key, label, format?: text\|currency\|date\|badge}]` | No | Tabular data |
| `List` | `dataPath`, `emptyMessage?` | Yes | Rendered list from array |

### Interactive

| Component | Props | Children | Description |
|-----------|-------|----------|-------------|
| `Button` | `label`, `action`, `variant?: primary\|secondary\|danger\|ghost`, `size?: sm\|md\|lg`, `disabled?` | No | Clickable action |
| `Select` | `label?`, `bindPath`, `options: [{value, label}]`, `placeholder?` | No | Dropdown select |
| `DatePicker` | `label?`, `bindPath`, `placeholder?` | No | Date input |

### Typography

| Component | Props | Children | Description |
|-----------|-------|----------|-------------|
| `Heading` | `text`, `level?: h1\|h2\|h3\|h4` | No | Section heading |
| `Text` | `content`, `variant?: body\|caption\|label`, `color?: default\|muted\|success\|warning\|danger` | No | Text paragraph |

### Status

| Component | Props | Children | Description |
|-----------|-------|----------|-------------|
| `Badge` | `text`, `variant?: default\|success\|warning\|danger\|info` | No | Status indicator |
| `Alert` | `type: info\|success\|warning\|error`, `title`, `message?`, `dismissible?` | No | Notification banner |

### Special

| Component | Props | Children | Description |
|-----------|-------|----------|-------------|
| `Divider` | `label?` | No | Visual separator |
| `Empty` | `title`, `description?`, `action?`, `actionLabel?` | No | Empty state |

## Data Binding

Props ending in `Path` (e.g., `valuePath`, `dataPath`, `bindPath`) reference the data model using JSON Pointer syntax:

- `/revenue` → `data.revenue`
- `/users/0/name` → `data.users[0].name`
- `/filters/dateRange` → `data.filters.dateRange`

## Visibility Conditions

Any element can have a `visible` property:

```json
{
  "type": "Alert",
  "props": { "type": "error", "title": "Error" },
  "visible": { "path": "/hasError" }
}
```

Visibility expressions:
- `true` / `false` — Static
- `{ "path": "/some/path" }` — Truthy check
- `{ "and": [...] }` — All conditions true
- `{ "or": [...] }` — Any condition true
- `{ "not": {...} }` — Negation
- `{ "eq": [a, b] }` — Equality

## Generating Output

### Step 1: Emit UITree JSON

Analyze the user's request and emit a UITree structure. Include sample data that matches the schema.

### Step 2: Create Artifact

Create an HTML artifact that:
1. Embeds the UITree JSON
2. Imports the renderer from `assets/renderer.js` (inline it)
3. Renders the UI

Use the template in `assets/template.html`.

## Constraints

**DO:**
- Use only catalog components
- Provide realistic sample data
- Use semantic component choices (Metric for KPIs, Table for tabular data)
- Keep trees flat (no deep nesting beyond 3 levels)

**DO NOT:**
- Invent new component types
- Use arbitrary HTML/CSS
- Omit required props
- Create deeply nested structures

## Example

**User:** "Create a sales dashboard with revenue, orders, and a chart showing monthly trends"

**Claude outputs:**

```json
{
  "root": "dashboard",
  "elements": {
    "dashboard": {
      "key": "dashboard",
      "type": "Stack",
      "props": { "direction": "vertical", "gap": "lg" },
      "children": ["header", "metrics", "chartCard"]
    },
    "header": {
      "key": "header",
      "type": "Heading",
      "props": { "text": "Sales Dashboard", "level": "h1" }
    },
    "metrics": {
      "key": "metrics",
      "type": "Grid",
      "props": { "columns": 3, "gap": "md" },
      "children": ["revenue", "orders", "avgOrder"]
    },
    "revenue": {
      "key": "revenue",
      "type": "Card",
      "props": { "padding": "md" },
      "children": ["revenueMetric"]
    },
    "revenueMetric": {
      "key": "revenueMetric",
      "type": "Metric",
      "props": {
        "label": "Total Revenue",
        "valuePath": "/revenue",
        "format": "currency",
        "trend": "up",
        "trendValue": "12%"
      }
    },
    "orders": {
      "key": "orders",
      "type": "Card",
      "props": { "padding": "md" },
      "children": ["ordersMetric"]
    },
    "ordersMetric": {
      "key": "ordersMetric",
      "type": "Metric",
      "props": {
        "label": "Orders",
        "valuePath": "/orders",
        "format": "number"
      }
    },
    "avgOrder": {
      "key": "avgOrder",
      "type": "Card",
      "props": { "padding": "md" },
      "children": ["avgMetric"]
    },
    "avgMetric": {
      "key": "avgMetric",
      "type": "Metric",
      "props": {
        "label": "Avg Order Value",
        "valuePath": "/avgOrderValue",
        "format": "currency"
      }
    },
    "chartCard": {
      "key": "chartCard",
      "type": "Card",
      "props": { "title": "Monthly Trends", "padding": "md" },
      "children": ["chart"]
    },
    "chart": {
      "key": "chart",
      "type": "Chart",
      "props": {
        "type": "line",
        "dataPath": "/monthlyData",
        "height": 300
      }
    }
  },
  "data": {
    "revenue": 284500,
    "orders": 1247,
    "avgOrderValue": 228,
    "monthlyData": [
      { "month": "Jan", "value": 18000 },
      { "month": "Feb", "value": 22000 },
      { "month": "Mar", "value": 28000 },
      { "month": "Apr", "value": 24000 },
      { "month": "May", "value": 32000 }
    ]
  }
}
```

Then wrap in the artifact template from `assets/template.html`.

## Files

- `assets/template.html` — Complete artifact template with embedded renderer
- `assets/catalog.json` — Machine-readable component schemas
- `references/uitree-format.md` — Detailed UITree specification
