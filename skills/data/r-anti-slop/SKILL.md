---
name: r-anti-slop
description: >
  Enforce production-quality R code standards. Prevents generic AI patterns
  through namespace qualification, explicit returns, and tidyverse conventions.
  Use when writing or reviewing R code for data analysis or packages.
applies_to:
  - "**/*.R"
  - "**/*.Rmd"
  - "**/*.qmd"
tags: [r, tidyverse, code-quality, data-science]
related_skills:
  - quarto/anti-slop
  - text/anti-slop
  - external/posit-skills/r-lib/cli
  - external/posit-skills/r-lib/testing
version: 2.0.0
---

# R Programming Anti-Slop Skill

## When to Use This Skill

Use r-anti-slop when:
- ✓ Writing new R code for data analysis or packages
- ✓ Reviewing AI-generated R code before committing
- ✓ Refactoring existing code for production quality
- ✓ Preparing R package for CRAN submission
- ✓ Teaching or enforcing R code standards
- ✓ Cleaning up generic variable names and patterns

Do NOT use when:
- Writing quick exploratory one-offs (though standards still help)
- Working with legacy code that cannot be changed
- Following different established style guides (e.g., Bioconductor)

## Quick Example

**Before (AI Slop)**:
```r
# Load the library
library(dplyr)

# Read the data
df <- read.csv("data.csv")

# Filter the data
result <- df %>% filter(x > 0)
```

**After (Anti-Slop)**:
```r
customer_data <- readr::read_csv("data/customers.csv")

active_customers <- customer_data |>
  dplyr::filter(status == "active", revenue > 0)

return(active_customers)
```

**What changed**:
- ✓ Descriptive names (`customer_data` not `df`)
- ✓ Namespace qualification (`dplyr::`, `readr::`)
- ✓ Native pipe (`|>` not `%>%`)
- ✓ No obvious comments
- ✓ Explicit return

## When to Use What

| If you need to... | Do this | Details |
|-------------------|---------|---------|
| Name variables | Use `snake_case`, no `df`/`data`/`result` | reference/naming.md |
| Call tidyverse functions | Always use `::` (e.g., `dplyr::filter()`) | reference/tidyverse.md |
| Return from function | Always explicit `return()` statement | reference/naming.md |
| Write pipe chains | Use `\|>`, break at 8+ operations | reference/tidyverse.md |
| Document functions | Specific `@param`, `@return`, no circular text | reference/documentation.md |
| Handle missing data | Explicit strategy + report data loss | reference/statistical-rigor.md |
| Validate data | Check assumptions with `stopifnot()` | reference/statistical-rigor.md |
| Format code | Use `styler::style_file()` | reference/tidyverse.md |
| Check code quality | Use `lintr::lint()` | reference/tidyverse.md |

## Core Workflow

### 5-Step Quality Check

1. **Namespace qualification** - All external functions use `::`
   ```r
   # Good
   dplyr::filter(data, x > 0)
   # Bad
   filter(data, x > 0)
   ```

2. **Explicit returns** - Every function has `return()`
   ```r
   # Good
   my_function <- function(x) {
     result <- x + 1
     return(result)
   }
   # Bad
   my_function <- function(x) {
     x + 1
   }
   ```

3. **Naming conventions** - All objects use `snake_case`
   ```r
   # Good
   customer_lifetime_value <- calculate_clv(data)
   # Bad
   df <- calculate_clv(data)
   customerLifetimeValue <- calculate_clv(data)
   ```

4. **Documentation quality** - No generic descriptions
   ```r
   # Good
   #' @param deaths Data frame with `age_group` and `count` columns
   # Bad
   #' @param data The data
   ```

5. **Code formatting** - Run styler and lintr
   ```r
   styler::style_file("script.R")
   lintr::lint("script.R")
   ```

## Quick Reference Checklist

Before committing R code, verify:

- [ ] All external functions qualified with `::`
- [ ] All functions have explicit `return()`
- [ ] All objects use `snake_case`
- [ ] No generic names (`df`, `data`, `result`, `temp`)
- [ ] Pipes (`|>`) have space before, end lines
- [ ] Long pipelines (>8 ops) broken into named steps
- [ ] Complex operations have WHY comments
- [ ] Data validated after transformations
- [ ] Seeds set before random operations
- [ ] Uncertainty reported (SE, CI) for statistical models
- [ ] No `attach()` calls
- [ ] No right-hand assignment (`->`)
- [ ] Roxygen documentation is specific
- [ ] Examples are realistic and run

## Common Workflows

### Workflow 1: Clean Up AI-Generated R Script

**Context**: AI generated an analysis script with generic patterns.

**Steps**:

1. **Run detection script**
   ```bash
   Rscript toolkit/scripts/detect_slop.R analysis.R --verbose
   ```

2. **Fix high-priority issues first**
   ```r
   # Replace df, data, result with descriptive names
   # Before
   df <- readr::read_csv("data.csv")
   result <- df %>% filter(x > 0)

   # After
   customer_data <- readr::read_csv("data/customers.csv")
   active_customers <- customer_data |> dplyr::filter(status == "active")
   ```

3. **Add namespace qualification**
   ```r
   # Before
   data %>% filter(x > 0) %>% summarize(mean(y))

   # After
   data |>
     dplyr::filter(x > 0) |>
     dplyr::summarize(mean_y = mean(y))
   ```

4. **Add explicit returns**
   ```r
   # Before
   calculate_rate <- function(numerator, denominator) {
     numerator / denominator
   }

   # After
   calculate_rate <- function(numerator, denominator) {
     rate <- numerator / denominator
     return(rate)
   }
   ```

5. **Break long pipes**
   ```r
   # Before (12 operations in one chain)
   result <- data |>
     filter(...) |> mutate(...) |> group_by(...) |>
     summarize(...) |> arrange(...) |> [7 more ops]

   # After
   clean_data <- data |>
     dplyr::filter(!is.na(value)) |>
     dplyr::mutate(category = categorize(value))

   summary_stats <- clean_data |>
     dplyr::group_by(category) |>
     dplyr::summarize(mean_val = mean(value))
   ```

6. **Format and validate**
   ```r
   styler::style_file("analysis.R")
   lintr::lint("analysis.R")
   ```

**Expected outcome**: Score drops from 60+ to <20

---

### Workflow 2: Fix Generic Package Documentation

**Context**: R package has generic roxygen documentation.

**Steps**:

1. **Identify generic patterns**
   ```r
   # Bad
   #' Process Data
   #'
   #' @description This function processes the data.
   #' @param data The data.
   #' @return The result.
   ```

2. **Make description specific**
   ```r
   # Good
   #' Calculate age-adjusted mortality rates
   #'
   #' Computes mortality rates per 100,000 population, standardized to the
   #' 2000 US Census age distribution using direct standardization.
   ```

3. **Describe parameter structure**
   ```r
   # Good
   #' @param deaths Data frame with columns `age_group` and `count`.
   #' @param population Data frame with columns `age_group` and `pop_size`.
   ```

4. **Specify return value**
   ```r
   # Good
   #' @return A tibble with columns:
   #'   \describe{
   #'     \item{county}{County FIPS code}
   #'     \item{rate}{Age-adjusted rate per 100,000}
   #'     \item{se}{Standard error of the rate}
   #'   }
   ```

5. **Add realistic examples**
   ```r
   # Good
   #' @examples
   #' counties <- data.frame(
   #'   county = c("A", "B"),
   #'   deaths = c(150, 200),
   #'   population = c(50000, 80000)
   #' )
   #'
   #' adjust_rates(counties, rate_per = 100000)
   #' #> # A tibble: 2 x 3
   #' #>   county  rate    se
   #' #> 1 A       312.  25.4
   #' #> 2 B       258.  18.2
   ```

**Expected outcome**: Documentation that teaches, not restates

---

### Workflow 3: Prepare Package for CRAN

**Context**: Final checks before CRAN submission.

**Steps**:

1. **Run all quality checks**
   ```r
   # Standard checks
   devtools::check()

   # Anti-slop checks
   lapply(list.files("R", full.names = TRUE), function(f) {
     system(paste("Rscript toolkit/scripts/detect_slop.R", f))
   })
   ```

2. **Fix documentation**
   - Check all `@param` descriptions are specific
   - Verify `@examples` run and are realistic
   - Ensure `@return` describes structure

3. **Validate code quality**
   ```r
   # Format all files
   styler::style_dir("R/")

   # Check lints
   lintr::lint_package()
   ```

4. **Check CRAN-specific requirements**
   - Use external/posit-skills/r-lib/cran-extrachecks skill
   - Validate URLs in DESCRIPTION and documentation
   - Check examples run in < 5 seconds

**Expected outcome**: Clean `R CMD check` with no slop patterns

## Mandatory Rules Summary

### 1. Namespace Qualification
**ALWAYS use `::` for external packages**

Exceptions (don't need `::`):
- Base R: `mean()`, `sum()`, `log()`, etc.
- stats: `lm()`, `glm()`, `t.test()`, etc.
- utils: `head()`, `tail()`, `str()`, etc.

### 2. Explicit Returns
**ALWAYS use `return()` - never implicit**

### 3. Naming: snake_case
**All objects use `snake_case`**
- Variables: `customer_data` not `customerData` or `df`
- Functions: `calculate_rate` not `calculateRate`
- Arguments: `input_data` not `inputData`

### 4. Native Pipe
**Prefer `|>` over `%>%`** (unless R < 4.1)

### 5. No Generic Names
**Never use**: `df`, `data`, `result`, `temp`, `x`, `n` (except standard math notation)

## Tidyverse Philosophy

Follow [Tidyverse Style Guide](https://style.tidyverse.org/) as primary reference:

1. **Design for humans** - Code should be readable and intuitive
2. **Reuse existing data structures** - Work with tibbles and data frames
3. **Compose simple functions with pipes** - Build complexity through composition
4. **Embrace functional programming** - Functions are first-class objects

See **reference/tidyverse.md** for complete tidyverse conventions.

## Resources & Advanced Topics

### Reference Files

- **[reference/naming.md](reference/naming.md)** - Complete naming conventions and forbidden patterns
- **[reference/tidyverse.md](reference/tidyverse.md)** - Pipe conventions, formatting, ggplot2 standards
- **[reference/documentation.md](reference/documentation.md)** - Roxygen2, vignettes, README quality
- **[reference/statistical-rigor.md](reference/statistical-rigor.md)** - Validation, uncertainty, reproducibility
- **[reference/forbidden-patterns.md](reference/forbidden-patterns.md)** - Complete antipattern catalog

### Related Skills

- **external/posit-skills/r-lib/cli** - Error message formatting with cli package
- **external/posit-skills/r-lib/testing** - Test structure and best practices
- **external/posit-skills/r-lib/cran-extrachecks** - CRAN submission requirements
- **text/anti-slop** - For cleaning prose in documentation

### Tools

- `styler::style_file()` - Auto-format code
- `lintr::lint()` - Check code quality
- `Rscript toolkit/scripts/detect_slop.R` - Detect AI patterns

## Integration with Posit Skills

This skill focuses on **code quality and avoiding generic patterns**.

Use together with Posit skills for complete coverage:

| Task | Use This Skill | + Posit Skill |
|------|----------------|---------------|
| Write error messages | r/anti-slop (quality) | + r-lib/cli (structure) |
| Write tests | r/anti-slop (code quality) | + r-lib/testing (test patterns) |
| Prepare for CRAN | r/anti-slop (no slop) | + r-lib/cran-extrachecks (requirements) |
| Document lifecycle | r/anti-slop (doc quality) | + r-lib/lifecycle (deprecation) |
