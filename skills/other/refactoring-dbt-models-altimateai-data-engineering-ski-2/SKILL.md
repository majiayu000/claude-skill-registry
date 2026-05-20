---
name: refactoring-dbt-models
description: |
  Safely refactors dbt models with downstream impact analysis. Use when restructuring dbt models for:
  (1) Task mentions "refactor", "restructure", "extract", "split", "break into", or "reorganize"
  (2) Extracting CTEs to intermediate models or creating macros
  (3) Modifying model logic that has downstream consumers
  (4) Renaming columns, changing types, or reorganizing model dependencies
  Analyzes all downstream dependencies BEFORE making changes.
---

# dbt Refactoring

**Find ALL downstream dependencies before changing. Refactor in small steps. Verify output after each change.**

## Workflow

### 1. Analyze Current Model

```bash
cat models/<path>/<model_name>.sql
```

Identify refactoring opportunities:
- CTEs longer than 50 lines → extract to intermediate model
- Logic repeated across models → extract to macro
- Multiple joins in sequence → split into steps
- Complex WHERE clauses → extract to staging filter

### 2. Find All Downstream Dependencies

**CRITICAL: Never refactor without knowing impact.**

```bash
# Get full dependency tree (model and all its children)
dbt ls --select model_name+ --output list

# Find all models referencing this one
grep -r "ref('model_name')" models/ --include="*.sql"
```

**Report to user:** "Found X downstream models: [list]. These will be affected by changes."

### 3. Check What Columns Downstream Models Use

**BEFORE changing any columns, check what downstream models reference:**

```bash
# For each downstream model, check what columns it uses
cat models/<path>/<downstream_model>.sql | grep -E "model_name\.\w+|alias\.\w+"
```

If downstream models reference specific columns, you MUST ensure those columns remain available after refactoring.

### 4. Plan Refactoring Strategy

| Opportunity | Strategy |
|-------------|----------|
| Long CTE | Extract to intermediate model |
| Repeated logic | Create macro in `macros/` |
| Complex join | Split into intermediate models |
| Multiple concerns | Separate into focused models |

### 5. Execute Refactoring

#### Pattern: Extract CTE to Model

Before:
```sql
-- orders.sql (200 lines)
with customer_metrics as (
    -- 50 lines of complex logic
),
order_enriched as (
    select ...
    from orders
    join customer_metrics on ...
)
select * from order_enriched
```

After:
```sql
-- customer_metrics.sql (new file)
select
    customer_id,
    -- complex logic here
from {{ ref('customers') }}

-- orders.sql (simplified)
with order_enriched as (
    select ...
    from {{ ref('raw_orders') }} orders
    join {{ ref('customer_metrics') }} cm on ...
)
select * from order_enriched
```

#### Pattern: Extract to Macro

Before (repeated in multiple models):
```sql
case
    when amount < 0 then 'refund'
    when amount = 0 then 'zero'
    else 'positive'
end as amount_category
```

After:
```sql
-- macros/categorize_amount.sql
{% macro categorize_amount(column_name) %}
case
    when {{ column_name }} < 0 then 'refund'
    when {{ column_name }} = 0 then 'zero'
    else 'positive'
end
{% endmacro %}

-- In models:
{{ categorize_amount('amount') }} as amount_category
```

### 6. Validate Changes

```bash
# Compile to check syntax
dbt compile --select +model_name+

# Build entire lineage
dbt build --select +model_name+

# Check row counts (manual)
# Before: Record expected counts
# After: Verify counts match
```

### 7. Verify Output Matches Original

**CRITICAL: Refactoring should not change output.**

```bash
# Compare row counts before and after
dbt show --inline "select count(*) from {{ ref('model_name') }}"

# Spot check key values
dbt show --select <model_name> --limit 10
```

### 8. Update Downstream Models

If changing output columns:
1. Update all downstream refs
2. Update schema.yml documentation
3. Re-run downstream tests

## Refactoring Checklist

- [ ] All downstream dependencies identified
- [ ] User informed of impact scope
- [ ] One change at a time
- [ ] Compile passes after each change
- [ ] Build passes after each change
- [ ] Output validated (row counts match)
- [ ] Documentation updated
- [ ] Tests still pass

## Common Refactoring Triggers

| Symptom | Refactoring |
|---------|-------------|
| Model > 200 lines | Extract CTEs to models |
| Same logic in 3+ models | Extract to macro |
| 5+ joins in one model | Create intermediate models |
| Hard to understand | Add CTEs with clear names |
| Slow performance | Split to allow parallelization |

## Anti-Patterns

- Refactoring without checking downstream impact
- Making multiple changes at once
- Not validating output matches after refactoring
- Extracting prematurely (wait for 3+ uses)
- Breaking existing tests without updating them

