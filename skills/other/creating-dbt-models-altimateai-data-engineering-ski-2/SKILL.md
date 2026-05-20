---
name: creating-dbt-models
description: |
  Creates dbt models following project conventions. Use when working with dbt models for:
  (1) Creating new models (any layer - discovers project's naming conventions first)
  (2) Task mentions "create", "build", "add", "write", "new", or "implement" with model, table, or SQL
  (3) Modifying existing model logic, columns, joins, or transformations
  (4) Implementing a model from schema.yml specs or expected output requirements
  Discovers project conventions before writing. Runs dbt build (not just compile) to verify.
---

# dbt Model Development

**Read before you write. Build after you write. Verify your output.**

## Critical Rules

1. **ALWAYS run `dbt build`** after creating/modifying models - compile is NOT enough
2. **ALWAYS verify output** after build using `dbt show` - don't assume success
3. **If build fails 3+ times**, stop and reassess your entire approach

## Workflow

### 1. Understand the Task Requirements

- What columns are needed? List them explicitly.
- What is the grain of the table (one row per what)?
- What calculations or aggregations are required?

### 2. Discover Project Conventions

```bash
cat dbt_project.yml
find models/ -name "*.sql" | head -20
```

Read 2-3 existing models to learn naming, config, and SQL patterns.

### 3. Find Similar Models

```bash
# Find models with similar purpose
find models/ -name "*agg*.sql" -o -name "*fct_*.sql" | head -5
```

Learn from existing models: join types, aggregation patterns, NULL handling.

### 4. Check Upstream Data

```bash
# Preview upstream data if needed
dbt show --select <upstream_model> --limit 10
```

### 5. Write the Model

Follow discovered conventions. Match the required columns exactly.

### 6. Compile (Syntax Check)

```bash
dbt compile --select <model_name>
```

### 7. BUILD - MANDATORY

**This step is REQUIRED. Do NOT skip it.**

```bash
dbt build --select <model_name>
```

If build fails:
1. Read the error carefully
2. Fix the specific issue
3. Run build again
4. **If fails 3+ times, step back and reassess approach**

### 8. Verify Output (CRITICAL)

**Build success does NOT mean correct output.**

```bash
# Check the table was created and preview data
dbt show --select <model_name> --limit 10
```

Verify:
- Column names match requirements exactly
- Row count is reasonable
- Data values look correct
- No unexpected NULLs

### 9. Verify Calculations Against Sample Data

**For models with calculations, verify correctness manually:**

```bash
# Pick a specific row and verify calculation by hand
dbt show --inline "
  select *
  from {{ ref('model_name') }}
  where <primary_key> = '<known_value>'
" --limit 1

# Cross-check aggregations
dbt show --inline "
  select count(*), sum(<column>)
  from {{ ref('model_name') }}
"
```

For example, if calculating `total_revenue = quantity * price`:
1. Pick one row from output
2. Look up the source quantity and price
3. Manually calculate: does it match?

### 10. Re-review Against Requirements

**Before declaring done, re-read the original request:**
- Did you implement what was asked, not what you assumed?
- Are column names exactly as specified?
- Is the calculation logic correct per the requirements?
- Does the grain (one row per what?) match what was requested?

## Anti-Patterns

- Declaring done after compile without running build
- Not verifying output data after build
- Getting stuck in compile/build error loops
- Assuming table exists just because model file exists
- Writing SQL without checking existing model patterns first
