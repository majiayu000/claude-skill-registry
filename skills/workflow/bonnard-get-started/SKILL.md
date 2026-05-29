---
name: bonnard-get-started
description: Guide a user through setting up their first semantic layer after bon init. Use when user says "get started", "what next", "help me set up", or has just run bon init.
allowed-tools: Bash(bon *)
---

# Get Started with Bonnard

This skill guides you through building and deploying a semantic layer.
The user has already run `bon init`. Walk through each phase in order,
confirming progress before moving on.

## Phase 1: Connect a Data Source

Ask the user if they have a warehouse to connect, or want to try a demo dataset first:

```bash
# Option A: Use demo data (no warehouse needed)
bon datasource add --demo

# Option B: Import from dbt (if they use it)
bon datasource add --from-dbt

# Option C: Add manually, non-interactive (preferred for agents)
bon datasource add --name my_warehouse --type postgres \
  --host db.example.com --port 5432 --database mydb --schema public \
  --user myuser --password mypassword

# Option D: Add manually, interactive (in user's terminal)
bon datasource add
```

Supported types: `postgres`, `redshift`, `snowflake`, `bigquery`, `databricks`, `duckdb`.

The demo option adds a read-only Contoso retail dataset with tables like
`fact_sales`, `dim_product`, `dim_store`, and `dim_customer`.

The connection will be tested automatically during `bon deploy`.

## Phase 2: Explore the Data

Before creating cubes, understand what tables and columns are available in your warehouse.

**Important:** `bon query` is for querying the **deployed semantic layer** — it does NOT
access your database directly. Use your warehouse's native tools to explore tables.

**Options for exploring your data:**
- Use your database CLI (e.g., `psql` for Postgres/Redshift, `snowsql` for Snowflake, `bq` for BigQuery) to list tables and columns
- Check your dbt docs or existing documentation for table schemas
- Ask the user for table names and column details if you don't have direct database access
- For the demo dataset, the tables are: `contoso.fact_sales`, `contoso.dim_product`, `contoso.dim_store`, `contoso.dim_customer`

Note the table names, column names, and data types — you'll use these in Phase 3.

## Phase 3: Create Your First Cube

Based on what you found in Phase 2, create a file in `bonnard/cubes/` for
the most important table. A cube maps directly to a database table — define
measures for the metrics you want to track and dimensions for the attributes
you want to filter and group by. **Use the actual table and column names from
Phase 2, not placeholder names.**

Example using demo data — `bonnard/cubes/sales.yaml`:

```yaml
cubes:
  - name: sales
    sql_table: contoso.fact_sales
    data_source: contoso_demo

    measures:
      - name: count
        type: count
        description: Total number of sales transactions

      - name: total_revenue
        type: sum
        sql: sales_amount
        description: Sum of sales revenue

      - name: total_cost
        type: sum
        sql: total_cost
        description: Sum of product costs

      # Filtered measures — match what users actually see on dashboards
      - name: return_count
        type: count
        description: >-
          Sales transactions with returns only (return_quantity > 0).
          For all transactions, use count.
        filters:
          - sql: "{CUBE}.return_quantity > 0"

    dimensions:
      - name: sales_key
        type: number
        sql: sales_key
        primary_key: true

      - name: date
        type: time
        sql: date_key
        description: Sale date

      - name: sales_quantity
        type: number
        sql: sales_quantity
        description: Number of units sold
```

Key rules:
- Every cube needs a `primary_key` dimension — **it must be unique**. If no column is naturally unique, use `sql` with `ROW_NUMBER()` instead of `sql_table` and add a synthetic key. Non-unique PKs cause dimension queries to silently return empty results.
- Every measure and dimension should have a `description` — descriptions are how AI agents discover and choose metrics (see `/bonnard-design-guide`)
- **Add filtered measures** for any metric users track with filters (e.g., "online revenue" vs "total revenue"). If a dashboard card has a WHERE clause beyond a date range, that filter should be a filtered measure.
- Measure descriptions should say what's **included and excluded** — e.g., "Online channel only. For all channels, use total_revenue."
- Dimension descriptions should include **example values** for categorical fields — e.g., "Sales channel (values: Online, Store, Reseller)"
- Set `data_source` to match the datasource name from Phase 1
- Use `sql_table` with the full `schema.table` path
- Use `sql_table` for simple table references, `sql` for complex queries

Use `bon docs cubes` for the full reference, `bon docs cubes.measures.types`
for all 12 measure types, `bon docs cubes.dimensions.types` for dimension types.

## Phase 4: Create a View

Views expose a curated subset of measures and dimensions for specific
audiences. **Name views by what they answer** (e.g., `sales_performance`),
not by what table they wrap (e.g., `sales_view`). A view can combine
measures and dimensions from multiple cubes via `join_path`.

The view **description** is critical — it's how AI agents decide which view
to query. It should answer: what's in here, when to use it, and when to
use something else instead. Include key dimension values where helpful.

Example using demo data — `bonnard/views/sales_performance.yaml`:

```yaml
views:
  - name: sales_performance
    description: >-
      Retail sales metrics — revenue, cost, and transaction counts by product,
      store, and date. Default view for sales questions. Includes return_count
      for return analysis. For customer demographics, use customer_insights
      instead.
    cubes:
      - join_path: sales
        includes:
          - count
          - total_revenue
          - return_count
          - total_cost
          - date
          - sales_quantity
```

Use `bon docs views` for the full reference. See `/bonnard-design-guide`
for principles on naming, descriptions, and view structure.

## Phase 5: Validate

Check for errors:

```bash
bon validate
```

Fix any errors before proceeding. Common issues:
- Missing required fields (`name`, `type`, `sql`)
- Unknown measure/dimension types (e.g., `text` should be `string`)
- Bad YAML indentation

Validate also warns about:
- **Missing descriptions** — descriptions help AI agents and analysts discover metrics
- **Missing `data_source`** — cubes without an explicit `data_source` use the default warehouse, which can cause issues when multiple warehouses are configured

## Phase 6: Deploy

Log in (if not already) and deploy:

```bash
bon login
bon deploy -m "Initial semantic layer with sales cube and overview view"
```

Deploy requires a `-m` message describing the changes. It validates, tests
connections, uploads cubes/views, and syncs datasource credentials (encrypted)
to Bonnard.

After deploying, the output shows what changed (added/modified/removed) and
flags any breaking changes. Use `bon deployments` to see history and
`bon diff <id>` to review changes from any deployment.

## Phase 7: Test with Queries

Verify the deployment works using the **view name** from Phase 4:

```bash
# Simple count
bon query '{"measures": ["sales_performance.count"]}'

# With a dimension
bon query '{"measures": ["sales_performance.total_revenue"], "dimensions": ["sales_performance.date"]}'

# SQL format
bon query --sql "SELECT MEASURE(total_revenue) FROM sales_performance"
```

**Test with natural language too.** If you've set up MCP (Phase 8), ask
an AI agent questions like "what's our total revenue?" and check whether
it picks the right view and measure. If it picks the wrong view, the issue
is usually the view description — see `/bonnard-design-guide` Principle 4.

## Phase 8: Connect AI Agents (Optional)

Set up MCP so AI agents can query the semantic layer:

```bash
bon mcp
```

This shows setup instructions for Claude Desktop, ChatGPT, Cursor, VS Code,
and other MCP clients. The MCP URL is `https://mcp.bonnard.dev/mcp`.

## Next Steps

After the first cube is working:

- **Iterate on descriptions** — test with real questions via MCP, fix agent mistakes by improving view descriptions and adding filtered measures (`/bonnard-design-guide`)
- Add more cubes for other tables
- Add joins between cubes (`bon docs cubes.joins`)
- Build audience-centric views that combine multiple cubes — e.g., a `management` view that pulls from `sales`, `users`, and `products` cubes
- Add calculated measures (`bon docs cubes.measures.calculated`)
- Add segments for common filters (`bon docs cubes.segments`)
