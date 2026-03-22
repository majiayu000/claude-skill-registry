---
name: r-guide
description: |
  R language guardrails, patterns, and best practices for AI-assisted development.
  Use when working with R files (.R, .Rmd, .qmd), DESCRIPTION, or when the user mentions R/RStudio.
  Provides tidyverse conventions, vectorization patterns, R Markdown guidelines,
  and testing standards specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: r
  extensions: ".R,.Rmd,.qmd,.Rproj"
---

# R Guide

> Applies to: R 4.1+, Statistical Computing, Data Analysis, R Packages, Shiny Apps

## Core Principles

1. **Tidyverse First**: Use tidyverse conventions for data manipulation, visualization, and functional programming; fall back to base R only when performance demands it
2. **Vectorize Everything**: Prefer vectorized operations and `purrr::map()` over explicit `for` loops; R is optimized for vector operations
3. **Reproducibility**: Every analysis must be reproducible -- use `renv` for dependency management, `set.seed()` for stochastic operations, and R Markdown/Quarto for literate programming
4. **Functional Style**: Write pure functions with no side effects; avoid modifying global state or relying on `.GlobalEnv`
5. **Explicit Over Implicit**: No reliance on partial matching, implicit type coercion, or positional argument passing for non-trivial functions

## Guardrails

### Version & Dependencies

- Target R 4.1+ (native pipe `|>`, lambda shorthand `\(x)`)
- Manage dependencies with `renv` -- always commit `renv.lock`
- For packages, declare all dependencies in `DESCRIPTION` (`Imports:`, `Suggests:`)
- Pin CRAN snapshot dates in `renv` for full reproducibility
- Audit new dependencies: check CRAN status, reverse dependencies, license (GPL compatibility)

### Code Style

- Follow the [tidyverse style guide](https://style.tidyverse.org/)
- Run `styler::style_pkg()` and `lintr::lint_package()` before every commit
- Naming: `snake_case` for functions/variables, `PascalCase` for R6/S4 classes
- Max line length: 80 characters
- Use `<-` for assignment (not `=` outside function arguments)
- Explicit `library()` at top of scripts; never use `require()`
- Always use `TRUE`/`FALSE` (never `T`/`F` -- they can be overwritten)
- No `attach()` or `setwd()` -- use `here::here()` for project-relative paths

### Vectorization

- Prefer vectorized operations: `x * 2` not `for (i in seq_along(x)) x[i] * 2`
- Use `dplyr::mutate()` / `dplyr::summarise()` for column-wise transformations
- Use `purrr::map()` family for list iteration (`map_dbl()`, `map_chr()`, `map_dfr()`)
- Use `dplyr::across()` for applying functions to multiple columns
- Reserve `for` loops for side effects only (writing files, API calls)
- Use `vapply()` over `sapply()` when base R is required (explicit return type)

### Error Handling

- Use `rlang::abort()` / `cli::cli_abort()` over `stop()` for structured conditions
- Validate inputs at the start of every exported function
- Use `stopifnot()` or `rlang::arg_match()` for argument validation
- Never use `try()` -- always `tryCatch()` or `purrr::safely()`

```r
validate_dataframe <- function(df, required_cols) {
  if (!is.data.frame(df)) {
    cli::cli_abort("{.arg df} must be a data frame, not {.obj_type_friendly {df}}.")
  }
  missing_cols <- setdiff(required_cols, names(df))
  if (length(missing_cols) > 0) {
    cli::cli_abort(
      "Missing required column{?s}: {.field {missing_cols}}.",
      class = "validation_error"
    )
  }
  invisible(df)
}
```

### Reproducibility

- Always use `set.seed()` before stochastic operations; document the seed
- Use `renv::snapshot()` after adding or updating packages
- Never use absolute paths -- use `here::here()` for project-relative paths
- Use R Markdown (`.Rmd`) or Quarto (`.qmd`) for analysis reports
- Include `sessioninfo::session_info()` at the end of reports

## Project Structure

```
mypackage/                          myanalysis/
├── R/             # Source files   ├── R/             # Reusable functions
│   ├── data-clean.R                ├── analysis/      # Rmd/Quarto (numbered)
│   └── utils.R                     │   ├── 01-exploration.Rmd
├── tests/                          │   └── 02-modeling.qmd
│   ├── testthat.R  # Runner        ├── data/
│   └── testthat/                   │   ├── raw/       # Immutable input
│       └── test-data-clean.R       │   └── processed/ # Generated output
├── man/            # roxygen2      ├── output/        # Figures, reports
├── vignettes/                      ├── tests/testthat/
├── data-raw/       # Data scripts  ├── renv.lock
├── DESCRIPTION                     └── README.md
├── NAMESPACE       # roxygen2
├── renv.lock
└── README.md
```

- Use `roxygen2` for all docs; never edit `man/` or `NAMESPACE` by hand
- Raw data is immutable -- store in `data/raw/`, process into `data/processed/`

## Key Patterns

### Tidyverse Pipe Chains

```r
# Prefer native pipe |> (R 4.1+) over magrittr %>%
result <- raw_data |>
  dplyr::filter(year >= 2020, !is.na(revenue)) |>
  dplyr::mutate(
    revenue_m = revenue / 1e6,
    growth = (revenue - dplyr::lag(revenue)) / dplyr::lag(revenue)
  ) |>
  dplyr::summarise(
    mean_revenue = mean(revenue_m, na.rm = TRUE),
    .by = region
  )
```

### Tidy Evaluation

```r
# Use {{ }} (embrace) for column names passed as arguments
summarise_by <- function(df, group_col, value_col) {
  df |>
    dplyr::summarise(
      mean_val = mean({{ value_col }}, na.rm = TRUE),
      n = dplyr::n(),
      .by = {{ group_col }}
    )
}

# Use .data pronoun for string column references
filter_column <- function(df, col_name, threshold) {
  df |> dplyr::filter(.data[[col_name]] > threshold)
}

# Use across() for multiple columns
standardize_numeric <- function(df) {
  df |>
    dplyr::mutate(dplyr::across(
      where(is.numeric),
      \(x) (x - mean(x, na.rm = TRUE)) / sd(x, na.rm = TRUE)
    ))
}
```

### ggplot2 Grammar of Graphics

```r
plot_distribution <- function(df, x_col, fill_col = NULL) {
  ggplot2::ggplot(df, ggplot2::aes(x = {{ x_col }})) +
    ggplot2::geom_histogram(ggplot2::aes(fill = {{ fill_col }}), bins = 30, alpha = 0.7) +
    ggplot2::labs(title = "Distribution", x = NULL, y = "Count") +
    ggplot2::theme_minimal(base_size = 14)
}
```

### Functional Programming with purrr

```r
# Type-stable map variants -- read and combine CSV files
results <- purrr::map_dfr(file_paths, \(path) {
  readr::read_csv(path, show_col_types = FALSE) |>
    dplyr::mutate(source_file = basename(path))
})

# Safe execution -- capture errors without stopping
safe_read <- purrr::safely(readr::read_csv)
reads <- purrr::map(file_paths, safe_read)
successes <- purrr::map(purrr::keep(reads, \(x) is.null(x$error)), "result")
```

## Testing

### Standards

- Use `testthat` 3rd edition (`Config/testthat/edition: 3` in `DESCRIPTION`)
- Test files: `test-*.R` (mirror source: `data-clean.R` -> `test-data-clean.R`)
- Test names describe behavior: `test_that("filter_active removes inactive users", ...)`
- Coverage target: >80% for business logic, >60% overall (measured with `covr`)
- Use snapshot tests (`expect_snapshot()`) for complex output (plots, printed tables)
- No test interdependencies -- each `test_that()` block is self-contained
- Use `withr::local_*()` for temporary state changes (env vars, options, files)

### testthat Examples

```r
test_that("summarise_by computes correct group means", {
  df <- tibble::tibble(
    region = c("east", "east", "west", "west"),
    revenue = c(100, 200, 300, 400)
  )
  result <- summarise_by(df, region, revenue)
  expect_equal(nrow(result), 2)
  expect_equal(result$mean_val[result$region == "east"], 150)
})

test_that("validate_dataframe errors on missing columns", {
  df <- tibble::tibble(a = 1, b = 2)
  expect_error(validate_dataframe(df, c("a", "c")), class = "validation_error")
})
```

## Tooling

### Essential Commands

```bash
Rscript -e 'styler::style_pkg()'        # Format package code
Rscript -e 'lintr::lint_package()'       # Lint package
Rscript -e 'devtools::test()'            # Run tests
Rscript -e 'covr::package_coverage()'    # Coverage report
Rscript -e 'devtools::check()'           # Full R CMD check
Rscript -e 'renv::snapshot()'            # Lock dependencies
Rscript -e 'devtools::document()'        # Rebuild roxygen2 docs
quarto render analysis/report.qmd        # Render Quarto document
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- dplyr pipelines, ggplot2 recipes, purrr functional patterns

## External References

- [Tidyverse Style Guide](https://style.tidyverse.org/)
- [R for Data Science (2e)](https://r4ds.hadley.nz/)
- [Advanced R (2e)](https://adv-r.hadley.nz/)
- [R Packages (2e)](https://r-pkgs.org/)
- [Tidy Evaluation](https://rlang.r-lib.org/reference/topic-data-mask.html)
- [testthat 3e Documentation](https://testthat.r-lib.org/)
- [ggplot2 Documentation](https://ggplot2.tidyverse.org/)
- [renv Documentation](https://rstudio.github.io/renv/)
- [Quarto Guide](https://quarto.org/docs/guide/)
- [lintr Documentation](https://lintr.r-lib.org/)
