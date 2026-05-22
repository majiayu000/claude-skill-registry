---
name: plotly-dash-dashboard
description: Builds production-ready, beautiful Plotly Dash dashboards with consistent theming, intuitive layouts, performant callbacks, and thorough documentation. Use when the user asks for a dashboard/data app, interactive analytics, Plotly charts, Dash UI, or a well-formatted shareable web dashboard.
---

# Plotly Dash Dashboard Builder

This Skill is a **battle-tested workflow** for building dashboards that are:
- **Intuitive** (clear hierarchy, obvious interactions, readable charts)
- **Beautiful** (cohesive typography + spacing + color, consistent chart styling)
- **Fast** (responsive UI; expensive work cached or offloaded)
- **Maintainable** (clean structure, small callbacks, documented data/assumptions)

## Quick start

### 1) Start by choosing the “dashboard type”
Pick the simplest thing that satisfies the request:

- **Single “report” page**: few KPIs + trends + breakdowns, light filtering
- **Multi-page app**: several workflows (overview → drilldown → details)
- **Exploration app**: many filters, cross-filtering, large tables

If the user is unsure, default to **single-page report + drilldown page**.

### 2) Choose a styling stack
Pick one (don’t mix unless required):

- **Dash Bootstrap Components (dbc)**: quickest path to clean layout + responsive grid.
- **Dash Mantine Components (dmc)**: modern UI components + built-in theming; great for polished apps.
- **Pure CSS + Dash HTML components**: when you need full control.

### 3) Always create a single source of truth for styling
- A **UI theme** (CSS variables or component library theme)
- A **Plotly figure template** (fonts, colors, margins, grid, hover, etc.)

See:
- [STYLE_GUIDE.md](STYLE_GUIDE.md)
- [FIGURE_STYLE.md](FIGURE_STYLE.md)
- [PALETTES.md](PALETTES.md)

---

## Intake (ask these before building)

Capture answers in the README so the app stays maintainable.

1) **Audience & decisions**
- Who uses this? What decisions should the dashboard help them make?
- What are the top 3 questions they’ll ask every time?

2) **Data**
- Data sources? Size? Update frequency? Latency expectations?
- Any definitions that must match existing reports (e.g., “Active user”)?

3) **Scope**
- Must-have views (KPIs, trends, breakdowns, table export)?
- Required filters (date, region, product, segment)?
- Need multi-user auth or just local/internal?

4) **Constraints**
- Deployment target (local, internal server, Dash Enterprise, container)?
- Performance expectations (p95 interaction < 300ms?) and data volume?

---

## Workflow

### Step 1 — Create the dashboard “story”
Write a 5–10 line narrative:
- “This dashboard helps **{persona}** monitor **{system}** to decide **{action}**.”
- “Success means they can answer **Q1/Q2/Q3** in under 30 seconds.”

Then decide the layout hierarchy:
- **Top**: KPIs + last updated + key filters
- **Middle**: primary trends / “what changed”
- **Bottom**: drivers, breakdowns, and details table

### Step 2 — Pick a layout pattern
Use one of these patterns (keep it consistent):

- **Header + filter bar + grid of cards** (default)
- **Left rail filters + main content** (lots of filters)
- **Tabbed sections** (few filters, many views)
- **Overview → drilldown pages** (best for complex apps)

### Step 3 — Choose a theme + palette
- Choose **one** font family and set it everywhere.
- Choose a palette for categorical colors + a sequential/diverging scale.

See [PALETTES.md](PALETTES.md) for ready-to-use palettes and guidance.

### Step 4 — Define the figure template (non-negotiable)
Every figure must inherit from a template (no one-off styling).

See [FIGURE_STYLE.md](FIGURE_STYLE.md) for a “drop-in” template + helper functions.

### Step 5 — Build the layout skeleton first
Before writing callbacks:
- Implement **Header**, **Filters**, **Main grid**, **Footer**
- Put placeholder charts (empty figures), placeholders for tables

This prevents “callback-driven UI design” (which usually becomes messy).

### Step 6 — Implement interactivity with maintainable callbacks
Rules of thumb:
- **One callback = one user intent**.
- Keep callbacks small; extract data transforms into `utils/`.
- Use `dcc.Store` for shared intermediate results.
- Use `prevent_initial_call=True` where appropriate.
- Use `PreventUpdate` / `no_update` when inputs are incomplete.

See [DASH_ARCHITECTURE.md](DASH_ARCHITECTURE.md).

### Step 7 — Make it fast (early)
If any callback takes > ~300ms:
- Cache the expensive part (memoize / store pre-aggregations)
- Or run it as a **background callback** (job queue)
- Or compute once and reuse results across charts

See [PERFORMANCE.md](PERFORMANCE.md).

### Step 8 — Add UX polish
Must-have polish for intuitive dashboards:
- Clear chart titles (“Revenue by Region — last 30 days”)
- Consistent hover tooltips (units, formatting, short labels)
- Loading states for expensive updates
- Empty-state messaging (“No data for this filter set”)
- “Last updated” timestamp and data source footnote

### Step 9 — QA with a checklist
Run through [QA_CHECKLIST.md](QA_CHECKLIST.md) before delivery.

### Step 10 — Documentation and handoff (required)
Deliver these artifacts:
- `README.md` with purpose, run instructions, config/env, screenshots
- `data_dictionary.md` (definitions + caveats)
- `architecture.md` (file tree + callback/data flow diagram)
- “Design decisions” notes (palette + template + layout rationale)

---

## Output contract (what this Skill should produce)

When asked to “build a dashboard”, produce:

1) A **project skeleton** with:
- `app.py` (entry point)
- `pages/` (if multi-page)
- `components/`, `callbacks/`, `utils/`, `assets/`
- `requirements.txt` or `pyproject.toml`

2) A **cohesive theme**:
- CSS variables or component library theme
- A Plotly template applied everywhere

3) A **demo dataset path** or loader stub:
- If data is unknown, include a clean interface with a sample dataset + TODO.

4) Clear **run instructions**:
- `python app.py`
- optional: `gunicorn app:server`

---

## References (2025–2026 sources used for this Skill)

- Anthropic Skill authoring best practices (format, progressive disclosure): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Dash design principles (typography, spacing, hierarchy): https://dash-resources.com/a-guide-to-beautiful-dashboards-basic-design-principles/ (2025)
- Dash callback maintainability patterns: https://dash-resources.com/dash-callbacks-best-practices-with-examples/ (updated 2025)
- Dash docs: Pages / multi-page apps: https://dash.plotly.com/urls
- Dash docs: Advanced callbacks (`PreventUpdate`, `no_update`, `running`, `prevent_initial_call`): https://dash.plotly.com/advanced-callbacks
- Dash docs: Background callbacks / job queues: https://dash.plotly.com/background-callbacks
- Plotly Python: theming & templates: https://plotly.com/python/templates/
- Learn UI Design: Data visualization palette generator (equidistant palettes): https://www.learnui.design/tools/data-color-picker.html
- Dash Mantine Components (modern UI library; 2026 release noted): https://pypi.org/project/dash-mantine-components/
