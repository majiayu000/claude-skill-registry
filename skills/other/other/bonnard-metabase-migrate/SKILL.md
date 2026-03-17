---
name: bonnard-metabase-migrate
description: Guide migration from an existing Metabase instance to a Bonnard semantic layer. Use when user says "migrate from metabase", "import metabase", "metabase to semantic layer", or has Metabase data they want to model.
allowed-tools: Bash(bon *)
---

# Migrate from Metabase to Bonnard

This skill guides you through analyzing an existing Metabase instance and
building a semantic layer that replicates its most important metrics.
Walk through each phase in order, confirming progress before moving on.

## Phase 1: Connect to Metabase

Set up a connection to the Metabase instance:

```bash
bon metabase connect
```

This prompts for the Metabase URL and API key. The API key should be created
in Metabase under Admin > Settings > Authentication > API Keys.
An admin-level key gives the richest analysis (permissions, schema access).

## Phase 2: Analyze the Instance

Generate an intelligence report that maps the entire Metabase instance:

```bash
bon metabase analyze
```

This writes a report to `.bon/metabase-analysis.md`. Read it carefully — it
drives every decision in the remaining phases.

### How to interpret each section

| Report Section | What It Tells You | Action |
|----------------|-------------------|--------|
| **Most Referenced Tables** | Tables used most in SQL queries | Create cubes for these first — they are the core of the data model |
| **Top Cards by Activity** | Most-viewed questions/models | `analytical` cards (GROUP BY + aggregation) map to measures; `lookup` cards indicate key filter dimensions; `display` cards can be skipped |
| **Common Filter Variables** | Template vars (`{{var}}`) used across 3+ cards | These must be dimensions on relevant cubes |
| **Foreign Key Relationships** | FK links between tables | Define `joins` between cubes using these relationships |
| **Collection Structure** | How users organize content by business area | Map each top-level collection to a view (one view per business domain) |
| **Dashboard Parameters** | Shared filters across dashboards | The most important shared dimensions — ensure they exist on relevant cubes |
| **Table Inventory** | Field counts and classification per table | Field classification (dims/measures/time) guides each cube definition; tables with 0 refs can be deprioritized |
| **Schema Access** | Which schemas non-admin groups can query | Focus on user-facing schemas — skip admin-only/staging schemas |

## Phase 3: Connect the Data Warehouse

Add a datasource pointing to the same database that Metabase queries.
The database connection details can often be found in Metabase under
Admin > Databases, or in the analysis report header.

```bash
# Non-interactive (preferred for agents)
bon datasource add --name my_warehouse --type postgres \
  --host db.example.com --port 5432 --database mydb --schema public \
  --user myuser --password mypassword

# Import from dbt if available
bon datasource add --from-dbt

# Interactive setup (in user's terminal)
bon datasource add
```

Supported types: `postgres`, `redshift`, `snowflake`, `bigquery`, `databricks`, `duckdb`.

The connection will be tested automatically during `bon deploy`.

## Phase 4: Explore Key Tables

Before writing cubes, drill into the most important tables and cards
identified in Phase 2. Use the explore commands to understand field types
and existing SQL patterns:

```bash
# View table fields with type classification
bon metabase explore table <id>

# View card SQL and columns
bon metabase explore card <id>

# View schemas and tables in a database
bon metabase explore database <id>

# View cards in a collection
bon metabase explore collection <id>
```

### How explore output maps to cube definitions

| Explore Field | Cube Mapping |
|---------------|-------------|
| Field class `pk` | Set `primary_key: true` on dimension |
| Field class `fk` | Join candidate — note the target table |
| Field class `time` | Dimension with `type: time` |
| Field class `measure` | Measure candidate — check card SQL for aggregation type |
| Field class `dim` | Dimension with `type: string` or `type: number` |

### How card SQL maps to measures

Look at the SQL in `analytical` cards to determine measure types:

| Card SQL Pattern | Cube Measure |
|-----------------|-------------|
| `SUM(amount)` | `type: sum`, `sql: amount` |
| `COUNT(*)` | `type: count` |
| `COUNT(DISTINCT user_id)` | `type: count_distinct`, `sql: user_id` |
| `AVG(price)` | `type: avg`, `sql: price` |
| `MIN(date)` / `MAX(date)` | `type: min` / `type: max`, `sql: date` |

Use `bon docs cubes.measures.types` for all 12 measure types.

## Phase 5: Build Cubes

Create cubes for the most-referenced tables (from Phase 2). Start with the
highest-referenced table and work down. Create one file per cube in
`bonnard/cubes/`.

For each cube:
1. Set `sql_table` to the full `schema.table` path
2. Set `data_source` to the datasource name from Phase 3
3. Add a `primary_key` dimension — **must be unique**. If no column is naturally unique, use `sql` with `ROW_NUMBER()` instead of `sql_table` and add a synthetic key
4. Add time dimensions for date/datetime columns
5. Add measures based on card SQL patterns (Phase 4)
6. **Add filtered measures** for every card with a WHERE clause beyond date range — e.g., "active offers" (status != cancelled). This is the #1 way to match dashboard numbers.
7. Add dimensions for columns used as filters (template vars from Phase 2)
8. Add `description` to every measure and dimension — descriptions should say what's **included and excluded**. Dimension descriptions should include **example values** for categorical fields.

Example — `bonnard/cubes/orders.yaml`:

```yaml
cubes:
  - name: orders
    sql_table: public.orders
    data_source: my_warehouse
    description: Order transactions

    measures:
      - name: count
        type: count
        description: Total number of orders

      - name: total_revenue
        type: sum
        sql: amount
        description: Sum of order amounts

    dimensions:
      - name: id
        type: number
        sql: id
        primary_key: true

      - name: created_at
        type: time
        sql: created_at
        description: Order creation timestamp

      - name: status
        type: string
        sql: status
        description: Order status (pending, completed, cancelled)
```

### Adding joins

Use FK relationships from the analysis report to define joins between cubes:

```yaml
    joins:
      - name: customers
        sql: "{CUBE}.customer_id = {customers.id}"
        relationship: many_to_one
```

Use `bon docs cubes.joins` for the full reference.

## Phase 6: Build Views

Map Metabase collections to views. Each top-level collection (business domain)
from the analysis report becomes a view that composes the relevant cubes.
**Name views by what they answer** (e.g., `sales_pipeline`), not by what
table they wrap (e.g., `orders_view`).

Create one file per view in `bonnard/views/`.

The view **description** is critical — it's how AI agents decide which view
to query. It should answer: what's in here, when to use it, and when to use
something else instead. Cross-reference related views to prevent agents from
picking the wrong one.

Example — `bonnard/views/sales_analytics.yaml`:

```yaml
views:
  - name: sales_analytics
    description: >-
      Sales team view — order revenue, counts, and status breakdowns with
      customer region. Default view for revenue and order questions. Use the
      status dimension (values: pending, completed, cancelled) to filter.
      For customer-level analysis, use customer_insights instead.
    cubes:
      - join_path: orders
        includes:
          - count
          - total_revenue
          - created_at
          - status

      - join_path: orders.customers
        prefix: true
        includes:
          - name
          - region
```

Use `bon docs views` for the full reference. See `/bonnard-design-guide`
for principles on view naming, descriptions, and structure.

## Phase 7: Validate and Deploy

Validate the semantic layer:

```bash
bon validate
```

Fix any errors. Common issues:
- Missing `primary_key` dimension
- Unknown measure/dimension types
- Undefined cube referenced in a view join path
- Missing `data_source`

Then deploy:

```bash
bon login
bon deploy -m "Migrate semantic layer from Metabase"
```

## Phase 8: Verify

Compare results from the semantic layer against Metabase card outputs.
Pick 3-5 important `analytical` cards from the analysis report and run
equivalent queries:

```bash
# Run a semantic layer query
bon query '{"measures": ["sales_analytics.total_revenue"], "dimensions": ["sales_analytics.status"]}'

# SQL format
bon query --sql "SELECT status, MEASURE(total_revenue) FROM sales_analytics GROUP BY 1"
```

Compare the numbers with the corresponding Metabase card. If they don't match:
- Check the SQL in the card (`bon metabase explore card <id>`) for filters or transformations
- Ensure the measure type matches the aggregation (SUM vs COUNT vs AVG)
- Check for WHERE clauses that should be filtered measures (not segments)

**Test with natural language too.** Set up MCP (`bon mcp`) and ask an agent
the same questions your Metabase dashboards answer. Check whether it picks
the right **view** and **measure** — most failures are description problems,
not data problems. See `/bonnard-design-guide` Principle 6.

## Next Steps

After the core migration is working:

- **Iterate on descriptions** — test with real questions via MCP, fix agent mistakes by improving view descriptions and adding filtered measures (`/bonnard-design-guide`)
- Add remaining tables as cubes (work down the reference count list)
- Build audience-centric views that combine multiple cubes — match how Metabase collections organize data by business domain
- Add calculated measures for complex card SQL (`bon docs cubes.measures.calculated`)
- Set up MCP for AI agent access (`bon mcp`)
- Review and iterate with `bon deployments` and `bon diff <id>`
