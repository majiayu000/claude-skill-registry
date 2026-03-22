---
name: frappe-impl-workspace
description: >
  Use when creating or customizing Workspace pages in Frappe v14-v16.
  Covers Workspace DocType structure, shortcuts, number cards, dashboard
  charts, custom HTML blocks, JSON content format, shipping workspaces
  with custom apps, and role-based access control.
  Prevents common mistakes with content/child-table desync and missing fixtures.
  Keywords: workspace, desk, dashboard, number card, chart, shortcut,
  workspace builder, module, fixtures, sidebar.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "3.0"
---

# Frappe Workspace Implementation Workflow

Step-by-step workflows for creating and customizing Workspace pages. Workspaces are the block-based dashboard/navigation pages in Frappe Desk.

**Version**: v14/v15/v16 (version-specific features noted)

---

## Quick Reference

| Concept | Description |
|---------|-------------|
| Workspace | Block-based page with 12-column grid layout |
| Public Workspace | Visible to all permitted users; requires Workspace Manager role to edit |
| Private Workspace | Per-user dashboard under "My Workspaces"; any Desk User can create |
| Content field | JSON array storing the block layout |
| Child tables | 6 tables: charts, shortcuts, links, quick_lists, number_cards, custom_blocks |
| Module association | Primary access control mechanism |

---

## Master Decision: What Do You Need?

```
NEED A WORKSPACE?
│
├─► Default DocType landing page?
│   └─► NO workspace needed — Frappe auto-generates list views
│
├─► Custom dashboard for a module?
│   └─► Create PUBLIC Workspace (Workspace Manager role required)
│
├─► Personal dashboard for a user?
│   └─► Create PRIVATE Workspace (appears under "My Workspaces")
│
└─► Navigation link in sidebar?
    └─► type="Link" (internal) or type="URL" (external)

ADDING COMPONENTS?
│
├─► Key metrics (counts, sums) → Number Cards
├─► Trend / time-series data  → Dashboard Charts
├─► Quick navigation links    → Shortcuts
├─► Grouped link categories   → Link Cards (Card Break + Links)
├─► Custom HTML/JS content    → Custom HTML Blocks
└─► Recent record lists       → Quick Lists
```

---

## Workspace DocType Structure

### Key Fields

| Field | Type | Purpose |
|-------|------|---------|
| `label` | Data | Display name in sidebar |
| `title` | Data | Page title (defaults to label) |
| `module` | Link → Module Def | Associates workspace with a module for access control |
| `parent_page` | Link → Workspace | Nesting under another workspace in sidebar |
| `icon` | Data | Sidebar icon (e.g., `"chart-line"`) |
| `type` | Select | `Workspace` / `Link` / `URL` (v15+) |
| `sequence_id` | Int | Sidebar ordering |
| `content` | JSON | Block layout as JSON array |
| `for_user` | Data | If set, workspace is private to that user |
| `roles` | Table → Has Role | Role-based access restrictions |
| `app` | Data | Owning app identifier (v15+) |
| `indicator_color` | Color | Sidebar indicator dot (v15+) |

### Child Tables (6 total)

| Child Table | DocType | Purpose |
|-------------|---------|---------|
| `charts` | Workspace Chart | Dashboard Chart references |
| `shortcuts` | Workspace Shortcut | DocType/Report/Page/URL shortcuts |
| `links` | Workspace Link | Grouped navigation links |
| `quick_lists` | Workspace Quick List | Recent record lists |
| `number_cards` | Workspace Number Card | Metric card references |
| `custom_blocks` | Workspace Custom Block | HTML block references |

> **CRITICAL**: The `content` JSON and the child tables MUST stay in sync. ALWAYS use the Workspace Builder UI or programmatic API — NEVER manually edit the `content` JSON without updating child tables. See `references/anti-patterns.md`.

---

## Content JSON Format

The `content` field is a JSON array. Each element represents a block in the 12-column grid:

```json
[
  {
    "id": "unique-block-id",
    "type": "header",
    "data": {"text": "Overview", "level": 4, "col": 12}
  },
  {
    "id": "unique-block-id-2",
    "type": "chart",
    "data": {
      "chart_name": "Sales Trends",
      "col": 12
    }
  },
  {
    "id": "unique-block-id-3",
    "type": "number_card",
    "data": {
      "number_card_name": "Open Orders",
      "col": 4
    }
  },
  {
    "id": "unique-block-id-4",
    "type": "shortcut",
    "data": {
      "shortcut_name": "New Sales Order",
      "col": 4
    }
  },
  {
    "id": "unique-block-id-5",
    "type": "spacer",
    "data": {"col": 12}
  }
]
```

### Block Types

| Type | `data` fields | Description |
|------|---------------|-------------|
| `header` | `text`, `level`, `col` | Section heading (h3/h4/h5) |
| `chart` | `chart_name`, `col` | References a Dashboard Chart doc |
| `number_card` | `number_card_name`, `col` | References a Number Card doc |
| `shortcut` | `shortcut_name`, `col` | References a Workspace Shortcut child |
| `card` | `card_name`, `col` | Card break for grouped links |
| `quick_list` | `quick_list_name`, `col` | Recent records for a DocType |
| `custom_block` | `custom_block_name`, `col` | References a Custom HTML Block doc |
| `text` | `body`, `col` | Rich text / Markdown block |
| `spacer` | `col` | Empty vertical space |
| `onboarding` | `onboarding_name`, `col` | Module onboarding widget |

> `col` values MUST be 1-12 and represent grid column width. Blocks in the same row MUST sum to ≤ 12.

---

## Implementation Workflows

### Workflow 1: Create a Public Workspace via UI

1. Navigate to `/app/workspace` → click **+ New Workspace**
2. Set **Label** (appears in sidebar), **Module**, **Icon**
3. Use the Workspace Builder to drag-and-drop blocks
4. Add components: Charts, Number Cards, Shortcuts, Links
5. Click **Save** → workspace appears in sidebar for permitted users
6. In developer mode: JSON auto-exports to your app directory

### Workflow 2: Create a Workspace Programmatically

```python
import frappe
import json

workspace = frappe.new_doc("Workspace")
workspace.label = "Project Dashboard"
workspace.module = "Projects"
workspace.icon = "project"
workspace.type = "Workspace"
workspace.sequence_id = 10

# Build content blocks
workspace.content = json.dumps([
    {
        "id": frappe.generate_hash(length=10),
        "type": "header",
        "data": {"text": "Project Overview", "level": 4, "col": 12}
    },
    {
        "id": frappe.generate_hash(length=10),
        "type": "number_card",
        "data": {"number_card_name": "Active Projects", "col": 4}
    },
    {
        "id": frappe.generate_hash(length=10),
        "type": "chart",
        "data": {"chart_name": "Project Status", "col": 12}
    }
])

# Add child table entries (MUST match content JSON)
workspace.append("number_cards", {
    "number_card_name": "Active Projects"
})
workspace.append("charts", {
    "chart_name": "Project Status"
})

# Role restrictions (optional)
workspace.append("roles", {"role": "Projects Manager"})

workspace.insert(ignore_permissions=True)
frappe.db.commit()
```

> **ALWAYS** add corresponding child-table rows when setting `content` JSON programmatically.

### Workflow 3: Create Supporting Documents First

Before adding components to a workspace, create the referenced documents:

**Number Card:**
```python
card = frappe.new_doc("Number Card")
card.label = "Active Projects"
card.document_type = "Project"
card.function = "Count"
card.filters_json = json.dumps([["Project", "status", "=", "Open"]])
card.is_public = 1
card.insert(ignore_permissions=True)
```

**Dashboard Chart:**
```python
chart = frappe.new_doc("Dashboard Chart")
chart.chart_name = "Project Status"
chart.chart_type = "Group By"
chart.document_type = "Project"
chart.group_by_type = "Count"
chart.group_by_based_on = "status"
chart.type = "Donut"
chart.is_public = 1
chart.insert(ignore_permissions=True)
```

**Shortcut:**
Shortcuts are child-table entries on the Workspace, not standalone docs:
```python
workspace.append("shortcuts", {
    "label": "New Project",
    "type": "DocType",
    "link_to": "Project",
    "color": "Blue",
    "format": "{} Active",
    "stats_filter": json.dumps([["Project", "status", "=", "Open"]])
})
```

See `references/workspace-components.md` for complete component reference.

---

## Permission Model

### Three Layers of Access Control

```
Layer 1: Module Access (PRIMARY)
└─► User must have access to the workspace's module
    └─► Controlled via "Module Def" and user's "Block Modules" list

Layer 2: Role Restrictions (OPTIONAL)
└─► workspace.roles child table
    └─► If populated: ONLY users with listed roles see the workspace
    └─► If empty: ALL users with module access see it

Layer 3: Workspace Manager Role
└─► Required to create/edit PUBLIC workspaces
└─► NOT required for private workspaces
```

### Rules

- ALWAYS set `module` on public workspaces — without it, the workspace is visible to ALL Desk users
- ALWAYS add role restrictions for sensitive dashboards (financial, HR)
- NEVER set `for_user` on workspaces shipped with an app — it creates a private workspace

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| Workspace Builder UI | Basic | Redesigned (drag-drop grid) | Incremental fixes |
| `type` field (Workspace/Link/URL) | Not available | Added | Available |
| `app` field | Not available | Added | Available |
| `indicator_color` | Not available | Added | Available |
| Name collision protection | Manual | Manual | Auto-deduplicate |
| Welcome header config | Not available | Not available | Added |
| Content JSON format | Same | Same | Same |

### Migration Notes

- v14 → v15: Workspace Builder UI changed significantly; existing JSON content remains compatible
- v15 → v16: Minor field additions; no breaking changes to workspace structure
- ALWAYS test workspace rendering after major version upgrades

---

## Shipping Workspaces with a Custom App

### Directory Structure

```
myapp/
└── mymodule/
    └── workspace/
        └── my_workspace/
            └── my_workspace.json
```

### Export Process

1. Enable **Developer Mode** (`frappe.conf.developer_mode = 1`)
2. Create/edit workspace via Workspace Builder UI
3. On save, Frappe auto-exports to the app directory above
4. Commit the JSON file to version control

### CRITICAL: Ship Dependencies Too

A workspace JSON alone is NOT sufficient. You MUST also ship:

| Component | How to Ship |
|-----------|-------------|
| Number Cards | fixtures in hooks.py OR `myapp/fixtures/` |
| Dashboard Charts | fixtures in hooks.py OR `myapp/fixtures/` |
| Custom HTML Blocks | fixtures in hooks.py OR `myapp/fixtures/` |
| Linked Reports | Already shipped via report directory structure |
| Linked Pages | Already shipped via page directory structure |

```python
# hooks.py
fixtures = [
    {"dt": "Number Card", "filters": [["module", "=", "My Module"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "My Module"]]},
    {"dt": "Custom HTML Block", "filters": [["name", "in", ["My Block"]]]},
]
```

See `references/shipping-with-app.md` for complete shipping guide.

---

## Common Patterns

### Pattern 1: Module Dashboard with KPIs

```
[Header: "Key Metrics"]
[Number Card: Open Orders (col=3)] [Number Card: Revenue (col=3)]
[Number Card: Pending (col=3)]     [Number Card: Overdue (col=3)]
[Spacer]
[Header: "Trends"]
[Chart: Monthly Revenue (col=12)]
[Header: "Quick Access"]
[Shortcut: New Order (col=4)] [Shortcut: Reports (col=4)] [Shortcut: Settings (col=4)]
```

### Pattern 2: Role-Based Workspace

```python
# Sales Manager sees full dashboard; Sales User sees limited view
# Option A: Two separate workspaces with different role restrictions
# Option B: One workspace — use Number Card/Chart permissions to filter

# Option A implementation:
ws_manager = frappe.get_doc({"doctype": "Workspace", "label": "Sales Management", ...})
ws_manager.append("roles", {"role": "Sales Manager"})

ws_user = frappe.get_doc({"doctype": "Workspace", "label": "Sales Overview", ...})
ws_user.append("roles", {"role": "Sales User"})
```

### Pattern 3: Sidebar Hierarchy

```python
# Parent workspace
parent = frappe.get_doc({"doctype": "Workspace", "label": "CRM", "module": "CRM"})

# Child workspaces (nested in sidebar)
child = frappe.get_doc({
    "doctype": "Workspace",
    "label": "Lead Pipeline",
    "module": "CRM",
    "parent_page": "CRM"  # References parent workspace label
})
```

---

## Reference Files

| File | Content |
|------|---------|
| `references/workspace-components.md` | Number Cards, Dashboard Charts, Shortcuts, Custom Blocks — full API |
| `references/shipping-with-app.md` | JSON format, fixtures, module structure, install hooks |
| `references/anti-patterns.md` | Common workspace mistakes and how to avoid them |
