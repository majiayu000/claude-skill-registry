---
name: bonnard-build-dashboard
description: Guide a user through building and deploying a markdown dashboard. Use when user says "build a dashboard", "create a chart", "visualize data", or wants to create a dashboard.
allowed-tools: Bash(bon *), Write, Edit, Read
---

# Build & Deploy a Markdown Dashboard

This skill guides you through creating a markdown dashboard with built-in
chart components and deploying it to Bonnard.

## Phase 1: Explore Available Data

Discover what measures and dimensions are available to query:

```bash
# List all views and their fields
bon schema

# Inspect a specific view's measures and dimensions
bon schema <view_name>

# Query a specific view to see what data looks like
bon query '{"measures": ["view_name.measure"], "dimensions": ["view_name.dimension"], "limit": 5}'

# Or use SQL format
bon query --sql "SELECT MEASURE(total_revenue), date FROM sales_performance LIMIT 5"
```

Ask the user what data they want to visualize. Match their request to
available views and measures.

## Phase 2: Learn the Format

Review the dashboard format docs for reference:

```bash
bon docs dashboards              # Overview + format
bon docs dashboards.components   # Chart components (BigValue, LineChart, BarChart, etc.)
bon docs dashboards.queries      # Query block syntax
bon docs dashboards.inputs       # Interactive filters (DateRange, Dropdown)
bon docs dashboards.examples     # Complete examples
```

## Phase 3: Build the Markdown File

Create a `.md` file with three parts:

1. **YAML frontmatter** — title and optional description
2. **Query blocks** — ` ```query name ` code fences with YAML query options
3. **Components** — `<BigValue />`, `<LineChart />`, `<BarChart />`, etc.

Key points:
- All field names must be fully qualified: `orders.total_revenue`, not `total_revenue`
- Each component references a query by name: `data={query_name}`
- Consecutive `<BigValue>` components auto-group into a row
- Use `<Grid cols="2">` to place charts side by side
- Use `<DateRange>` and `<Dropdown>` for interactive filters
- BigValue supports `comparison` prop for ▲/▼ delta indicators (e.g. actual vs target)
- Charts support `y2` for secondary y-axis (combo charts: bars + line, dual scales)
- For DataTable formatting, use `<Column>` children instead of the `fmt` prop (avoids comma ambiguity with Excel format codes):
  ```
  <DataTable data={sales}>
    <Column field="orders.total_revenue" header="Revenue" fmt="eur2" />
    <Column field="orders.count" header="Orders" fmt="num0" />
  </DataTable>
  ```

Example structure:

```markdown
---
title: Revenue Dashboard
description: Key revenue metrics and trends
---

` ``query total_revenue
measures: [orders.total_revenue]
` ``

` ``query order_count
measures: [orders.count]
` ``

<BigValue data={total_revenue} value="orders.total_revenue" title="Revenue" fmt="eur2" />
<BigValue data={order_count} value="orders.count" title="Orders" />

## Trend

` ``query monthly
measures: [orders.total_revenue, orders.count]
timeDimension:
  dimension: orders.created_at
  granularity: month
` ``

<BarChart data={monthly} x="orders.created_at" y="orders.total_revenue" y2="orders.count" yFmt="eur" y2Fmt="num0" y2SeriesType="line" title="Revenue & Orders" />
```

Save the file (e.g., `dashboard.md`).

## Phase 4: Preview Locally (Required)

**Always preview before deploying.** Open a local dev server with live reload:

```bash
bon dashboard dev dashboard.md
```

This opens a browser with the rendered dashboard. Edit the `.md` file and
the preview updates automatically. Queries run against the deployed
semantic layer using the user's credentials.

Requires `bon login` — no API key needed.

Ask the user to review the preview and confirm it looks correct before
moving to Phase 5. Do not skip this step — deploying without previewing
often results in layout issues, missing data, or wrong chart types that
are easy to catch locally.

## Phase 5: Deploy

Once the user has confirmed the preview looks good, deploy the dashboard:

```bash
bon dashboard deploy dashboard.md
```

This will:
- Upload the markdown content
- Assign a slug (derived from filename, or use `--slug`)
- Extract the title from frontmatter
- Print the URL where the dashboard is accessible

Options:
- `--slug <slug>` — custom URL slug (default: derived from filename)
- `--title <title>` — override frontmatter title

## Theming (Optional)

Customize colors and palettes:

- **Per-dashboard**: Add `theme:` to frontmatter (e.g. `theme: { palette: observable }`)
- **Org-wide**: Create a `theme.yml` and run `bon theme set theme.yml`
- **Preview locally**: `bon dashboard dev dashboard.md --theme theme.yml`

See `bon docs dashboards.theming` for palette names, color tokens, and examples.

## Phase 6: View Live

Open the deployed dashboard in the browser:

```bash
bon dashboard open dashboard
```

## Iteration

To update, edit the `.md` file and redeploy:

```bash
bon dashboard deploy dashboard.md
```

Each deploy increments the version. Use `bon dashboard list` to see all
deployed dashboards with their versions and URLs.

To remove a dashboard:

```bash
bon dashboard remove dashboard
```
