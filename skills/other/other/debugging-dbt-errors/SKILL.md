---
name: debugging-dbt-errors
description: |
  Debugs and fixes dbt errors systematically. Use when working with dbt errors for:
  (1) Task mentions "fix", "error", "broken", "failing", "debug", "wrong", or "not working"
  (2) Compilation Error, Database Error, or test failures occur
  (3) Model produces incorrect output or unexpected results
  (4) Need to troubleshoot why a dbt command failed
  Reads full error, checks upstream first, runs dbt build (not just compile) to verify fix.
---

# dbt Troubleshooting

**Read the full error. Check upstream first. ALWAYS run `dbt build` after fixing.**

## Critical Rules

1. **ALWAYS run `dbt build` after fixing** - compile is NOT enough to verify the fix
2. **If fix fails 3+ times**, stop and reassess your entire approach
3. **Verify data after build** - build passing doesn't mean output is correct

## Workflow

### 1. Get the Full Error

```bash
dbt compile --select <model_name>
# or
dbt build --select <model_name>
```

Read the COMPLETE error message. Note the file, line number, and specific error.

### 2. Inspect Actual Data (For Data Issues)

**Before fixing "wrong output" or "incorrect results", query the actual data:**

```bash
# Preview current output
dbt show --select <model_name> --limit 20

# Check specific values with inline query
dbt show --inline "select * from {{ ref('model_name') }} where <condition>" --limit 10

# Compare with expected - look for patterns
dbt show --inline "select column, count(*) from {{ ref('model_name') }} group by 1 order by 2 desc" --limit 10
```

**Understand what's wrong before attempting to fix it.**

### 3. Read Compiled SQL

```bash
cat target/compiled/<project>/<path>/<model_name>.sql
```

See the actual SQL that will run.

### 4. Analyze Error Type

| Error Type | Look For |
|------------|----------|
| Compilation Error | Jinja syntax, missing refs, YAML issues |
| Database Error | Column not found, type mismatch, SQL syntax |
| Dependency Error | Missing model, circular reference |

### 5. Check Upstream Models

```bash
# Find what this model references
grep -E "ref\(|source\(" models/<path>/<model_name>.sql

# Read upstream model to verify columns
cat models/<path>/<upstream_model>.sql
```

Many errors come from upstream changes, not the current model.

### 6. Apply Fix

Common fixes:

| Error | Fix |
|-------|-----|
| Column not found | Check upstream model's output columns |
| Ambiguous column | Add table alias: `table.column` |
| Type mismatch | Add explicit `CAST()` |
| Division by zero | Use `NULLIF(divisor, 0)` |
| Jinja error | Check matching `{{ }}` and `{% %}` |

### 7. Rebuild (MANDATORY)

```bash
dbt build --select <model_name>
```

**3-Failure Rule**: If build fails 3+ times, STOP. Step back and:
1. Re-read the original error
2. Check if your entire approach is wrong
3. Consider alternative solutions

### 8. Verify Fix

```bash
# Preview the data
dbt show --select <model_name> --limit 10

# Run tests
dbt test --select <model_name>
```

### 9. Re-review Logic Against Requirements

**After fixing, re-read the original request and verify:**
- Does the output match what the user asked for?
- Are the column names exactly as requested?
- Is the calculation logic correct per the requirements?
- Did you solve the actual problem, not just make the error go away?

### 10. Check Downstream Impact

```bash
# Find downstream models
grep -r "ref('<model_name>')" models/ --include="*.sql"

# Rebuild downstream
dbt build --select <model_name>+
```

## Error Categories

### Compilation Errors
- Check Jinja syntax: matching `{{ }}` and `{% %}`
- Verify macro arguments
- Check YAML indentation

### Database Errors
- Read compiled SQL in `target/compiled/`
- Check column names against upstream
- Verify data types

### Test Failures
- Read the test SQL to understand what it checks
- Compare your model output to expected behavior
- Check column names, data types, NULL handling

## Anti-Patterns

- Making random changes without understanding the error
- Assuming the current model is wrong before checking upstream
- Not reading the FULL error message
- Declaring "fixed" without running build
- Getting stuck making small tweaks instead of reassessing
