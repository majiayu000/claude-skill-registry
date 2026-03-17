---
name: sql-translation
description: Guide for adding SQL function translations to dbplyr backends. Use when implementing new database-specific R-to-SQL translations for functions like string manipulation, date/time, aggregates, or window functions.
---

# SQL Translation Skill

Use this skill when adding new SQL function translations for a specific database backend.

## Overview

This skill guides you through adding SQL translations to dbplyr. SQL translations convert R functions to their SQL equivalents for different database backends.

## Workflow

### 1. Research SQL (CRITICAL - ALWAYS FIRST)

Before implementing any SQL translation, you MUST research the SQL syntax and behavior using the **sql-research** skill. See that skill for the complete research workflow.

**Quick summary:**
- Search official documentation for "{dialect} {function}"
- Document findings in `research/{dialect}-{function}.md`
- Include all source URLs
- Only proceed to implementation after completing research

### 2. Identify the backend file

SQL translations are defined in backend-specific files:
- `R/backend-sqlite.R` - SQLite
- `R/backend-postgres.R` - PostgreSQL
- `R/backend-mysql.R` - MySQL
- `R/backend-mssql.R` - MS SQL Server
- etc.

### 3. Add translation

Translations are added to the `sql_translation()` method for the connection class. This method returns a `sql_variant()` with three components:

**Scalar translations** (for mutate/filter):
```r
sql_translator(.parent = base_scalar,
  # Simple function name mapping
  log10 = function(x) sql_expr(log(!!x)),

  # Function with different arguments
  round = function(x, digits = 0L) {
    digits <- as.integer(digits)
    sql_expr(round(((!!x)) %::% numeric, !!digits))
  },

  # Infix operators
  paste0 = sql_paste(""),

  # Complex logic
  grepl = function(pattern, x, ignore.case = FALSE) {
    if (ignore.case) {
      sql_expr(((!!x)) %~*% ((!!pattern)))
    } else {
      sql_expr(((!!x)) %~% ((!!pattern)))
    }
  }
)
```

**Aggregate translations** (for summarise):
```r
sql_translator(.parent = base_agg,
  sd = sql_aggregate("STDEV", "sd"),
  median = sql_aggregate("MEDIAN"),
  quantile = sql_not_supported("quantile")
)
```

**Window translations** (for mutate with groups):
```r
sql_translator(.parent = base_win,
  sd = win_aggregate("STDEV"),
  median = win_absent("median"),
  quantile = sql_not_supported("quantile")
)
```

### 4. Helper functions

Common translation patterns:

- `sql_expr()` - Build SQL expressions with `!!` for interpolation
- `sql_cast(type)` - Type casting (e.g., `sql_cast("REAL")`)
- `sql_aggregate(sql_name, r_name)` - Simple aggregates
- `sql_paste(sep)` - String concatenation
- `sql_not_supported(name)` - Mark unsupported functions
- `win_aggregate(sql_name)` - Window aggregates
- `win_absent(name)` - Window functions not supported

### 5. Test the translation

**Interactive testing:**
```r
Rscript -e "devtools::load_all(); library(dplyr, warn.conflicts = FALSE);
  translate_sql(your_function(x), con = simulate_yourdb())"
```

**Write tests:**
- Tests for `R/{name}.R` go in `tests/testthat/test-{name}.R`
- Place new tests next to similar existing tests
- Keep tests minimal with few comments

Example test:
```r
test_that("backend_name translates function_name correctly", {
  lf <- lazy_frame(x = 1, con = simulate_backend())

  expect_snapshot(
    lf |> mutate(y = your_function(x))
  )
})
```

### 6. Document the translation

**Update backend documentation:**
- Edit the `@description` section in the backend file (e.g., `R/backend-postgres.R`)
- List key translation differences
- Add examples to `@examples` if helpful

**Example:**
```r
#' Backend: PostgreSQL
#'
#' @description
#' See `vignette("translation-function")` and `vignette("translation-verb")` for
#' details of overall translation technology. Key differences for this backend
#' are:
#'
#' * Many stringr functions
#' * lubridate date-time extraction functions
#' * Your new translation
```

### 7. Format and check

```bash
# Format code
air format .

# Run relevant tests
Rscript -e "devtools::test(filter = 'backend-name', reporter = 'llm')"

# Check documentation
Rscript -e "devtools::document()"
```

## Key concepts

**Parent translators:**
- `base_scalar` - Common scalar functions (math, string, logical)
- `base_agg` - Common aggregates (sum, mean, min, max)
- `base_win` - Common window functions

**SQL expression building:**
- Use `sql_expr()` to build SQL
- Use `!!` to interpolate R variables
- Use `%as%` for AS, `%::%` for ::, etc.

**Argument handling:**
- Check arguments with `check_bool()`, `check_unsupported_arg()`
- Convert R types appropriately (e.g., `as.integer()`)
- Handle optional arguments with defaults

## Resources

See also:
- `vignette("translation-function")` - Function translation overview
- `vignette("new-backend")` - Creating new backends
- Existing backend files for examples

## Checklist

Before completing a SQL translation:

- [ ] Researched SQL syntax in official documentation
- [ ] Created research file in `research/{dialect}-{function}.md`
- [ ] Added translation to appropriate `sql_translator()` section
- [ ] Tested translation interactively
- [ ] Added/updated tests
- [ ] Updated backend documentation
- [ ] Ran `air format .`
- [ ] Verified tests pass
