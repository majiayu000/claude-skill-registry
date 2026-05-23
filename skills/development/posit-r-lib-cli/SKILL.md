---
name: cli
description: >
  Comprehensive R package for command-line interface styling, semantic messaging,
  and user communication. Use this skill when working with R code that needs to:
  (1) Format console output with inline markup and colors,
  (2) Display errors, warnings, or messages with cli_abort/cli_warn/cli_inform,
  (3) Show progress indicators for long-running operations,
  (4) Create semantic CLI elements (headers, lists, alerts, code blocks),
  (5) Apply themes and customize output styling,
  (6) Handle pluralization in user-facing text,
  (7) Work with ANSI strings, hyperlinks, or custom containers.
  Also use when migrating from base R message/warning/stop, debugging cli code,
  or improving existing cli usage.
---

# CLI for R Packages

## When to Use What

task: Display error with context and formatting
use: `cli_abort()` with inline markup and bullet lists

task: Show warning with formatting
use: `cli_warn()` with inline markup

task: Display informative message
use: `cli_inform()` with inline markup

task: Show progress for counted operations
use: `cli_progress_bar()` with total count

task: Show simple progress steps
use: `cli_progress_step()` with status messages

task: Format code or function names
use: `{.code ...}` or `{.fn package::function}`

task: Format file paths
use: `{.file path/to/file}`

task: Format package names
use: `{.pkg packagename}`

task: Format variable names
use: `{.var variable_name}`

task: Format values
use: `{.val value}`

task: Handle singular/plural text
use: `{?s}` or `{?y/ies}` with pluralization

task: Create headers
use: `cli_h1()`, `cli_h2()`, `cli_h3()`

task: Create alerts
use: `cli_alert_success()`, `cli_alert_danger()`, `cli_alert_warning()`, `cli_alert_info()`

task: Create lists
use: `cli_ul()`, `cli_ol()`, `cli_dl()` with `cli_li()`

## Inline Markup Essentials

Use inline markup with `{.class content}` syntax to format text:

```r
# Basic formatting
cli_text("Function {.fn mean} calculates averages")
cli_text("Install package {.pkg dplyr}")
cli_text("See file {.file ~/.Rprofile}")
cli_text("{.var x} must be numeric, not {.obj_type_of {x}}")
cli_text("Got value {.val {x}}"))

# Code formatting
cli_text("Use {.code sum(x, na.rm = TRUE)}")

# Paths and arguments
cli_text("Reading from {.path /data/file.csv}")
cli_text("Set {.arg na.rm} to TRUE")

# Types and classes
cli_text("Object is {.cls data.frame}")

# Emphasis
cli_text("This is {.emph important}")
cli_text("This is {.strong critical}")

# Fields
cli_text("The {.field name} field is required")
```

### Vector Collapsing

Vectors are automatically collapsed with commas and "and":

```r
pkgs <- c("dplyr", "tidyr", "ggplot2")
cli_text("Installing packages: {.pkg {pkgs}}")
#> Installing packages: dplyr, tidyr, and ggplot2

files <- c("data.csv", "script.R")
cli_text("Found {length(files)} file{?s}: {.file {files}}")
#> Found 2 files: data.csv and script.R
```

### Escaping Braces

Use double braces `{{` and `}}` to escape literal braces:

```r
cli_text("Use {{variable}} syntax in glue")
#> Use {variable} syntax in glue
```

**For complete markup reference**: See [references/inline-markup.md](references/inline-markup.md) for all 50+ inline classes, edge cases, nesting rules, and advanced patterns.

## Pluralization Basics

Use `{?}` for pluralization with three patterns:

### Single Alternative

```r
nfile <- 1
cli_text("Found {nfile} file{?s}")
#> Found 1 file

nfile <- 3
cli_text("Found {nfile} file{?s}")
#> Found 3 files
```

### Two Alternatives

```r
ndir <- 1
cli_text("Found {ndir} director{?y/ies}")
#> Found 1 directory

ndir <- 5
cli_text("Found {ndir} director{?y/ies}")
#> Found 5 directories
```

### Three Alternatives (zero/one/many)

```r
nfile <- 0
cli_text("Found {nfile} file{?s}: {?no/the/the} file{?s}")
#> Found 0 files: no files

nfile <- 1
cli_text("Found {nfile} file{?s}: {?no/the/the} file{?s}")
#> Found 1 file: the file

nfile <- 3
cli_text("Found {nfile} file{?s}: {?no/the/the} file{?s}")
#> Found 3 files: the files
```

### Helpers: qty() and no()

Use `no()` to display "no" instead of zero:

```r
nfile <- 0
cli_text("Found {no(nfile)} file{?s}")
#> Found no files
```

Use `qty()` to set quantity explicitly:

```r
nupd <- 3
ntotal <- 10
cli_text("{nupd}/{ntotal} {qty(nupd)} file{?s} {?needs/need} updates")
#> 3/10 files need updates
```

**For advanced pluralization**: See [references/inline-markup.md](references/inline-markup.md) for edge cases and complex patterns.

## CLI Conditions: Core Patterns

Use cli conditions instead of base R for better formatting:

### cli_abort() - Formatted Errors

```r
# Before (base R)
stop("File not found: ", path)

# After (cli)
cli_abort("File {.file {path}} not found")

# With bullets for context
check_file <- function(path) {
  if (!file.exists(path)) {
    cli_abort(c(
      "File not found",
      "x" = "Cannot read {.file {path}}",
      "i" = "Check that the file exists"
    ))
  }
}
```

### cli_warn() - Formatted Warnings

```r
# Before (base R)
warning("Column ", col, " has missing values")

# After (cli)
cli_warn("Column {.field {col}} has missing values")

# With context
cli_warn(c(
  "Data quality issues detected",
  "!" = "Column {.field {col}} has {n_missing} missing value{?s}",
  "i" = "Consider using {.fn tidyr::drop_na}"
))
```

### cli_inform() - Formatted Messages

```r
# Before (base R)
message("Processing ", n, " files")

# After (cli)
cli_inform("Processing {n} file{?s}")

# With structure
cli_inform(c(
  "v" = "Successfully loaded {.pkg dplyr}",
  "i" = "Version {packageVersion('dplyr')}"
))
```

### Bullet Types

- `"x"` - Error/problem (red X)
- `"!"` - Warning (yellow !)
- `"i"` - Information (blue i)
- `"v"` - Success (green checkmark)
- `"*"` - Bullet point
- `">"` - Arrow/pointer

**For advanced error design**: See [references/conditions.md](references/conditions.md) for error design principles, rlang integration, testing strategies, and real-world patterns.

## Basic Progress Indicators

### Simple Progress Steps

```r
process_data <- function() {
  cli_progress_step("Loading data")
  data <- load_data()

  cli_progress_step("Cleaning data")
  clean <- clean_data(data)

  cli_progress_step("Analyzing data")
  analyze(clean)
}
```

### Basic Progress Bar

```r
process_files <- function(files) {
  cli_progress_bar("Processing files", total = length(files))

  for (file in files) {
    process_file(file)
    cli_progress_update()
  }
}
```

### Auto-Cleanup

Progress bars auto-close when the function exits:

```r
process <- function() {
  cli_progress_bar("Working", total = 100)
  for (i in 1:100) {
    Sys.sleep(0.01)
    cli_progress_update()
  }
  # No need to call cli_progress_done() - auto-closes
}
```

**For advanced progress**: See [references/progress.md](references/progress.md) for nested progress, custom formats, parallel processing, all progress variables, and Shiny integration.

## Semantic CLI Elements

### Headers

```r
cli_h1("Main Section")
cli_h2("Subsection")
cli_h3("Detail")
```

### Alerts

```r
cli_alert_success("Operation completed successfully")
cli_alert_danger("Critical error occurred")
cli_alert_warning("Potential issue detected")
cli_alert_info("Additional information available")
```

### Text and Code

```r
# Regular text with markup
cli_text("This is formatted text with {.emph emphasis}")

# Code blocks
cli_code(c(
  "library(dplyr)",
  "mtcars %>% filter(mpg > 20)"
))

# Verbatim text (no formatting)
cli_verbatim("This is displayed exactly as-is: {not interpolated}")
```

### Lists

```r
# Unordered list
cli_ul()
cli_li("First item")
cli_li("Second item")
cli_end()

# Ordered list
cli_ol()
cli_li("First step")
cli_li("Second step")
cli_end()

# Definition list
cli_dl()
cli_li(c(name = "The name field"))
cli_li(c(email = "The email address"))
cli_end()
```

## Common Workflows

### Base R to CLI Migration

```r
# Before: Base R error handling
validate_input <- function(x, y) {
  if (!is.numeric(x)) {
    stop("x must be numeric")
  }
  if (length(y) == 0) {
    stop("y cannot be empty")
  }
  if (length(x) != length(y)) {
    stop("x and y must have the same length")
  }
}

# After: CLI error handling
validate_input <- function(x, y) {
  if (!is.numeric(x)) {
    cli_abort(c(
      "{.arg x} must be numeric",
      "x" = "You supplied a {.cls {class(x)}} vector",
      "i" = "Use {.fn as.numeric} to convert"
    ))
  }

  if (length(y) == 0) {
    cli_abort(c(
      "{.arg y} cannot be empty",
      "i" = "Provide at least one element"
    ))
  }

  if (length(x) != length(y)) {
    cli_abort(c(
      "{.arg x} and {.arg y} must have the same length",
      "x" = "{.arg x} has length {length(x)}",
      "x" = "{.arg y} has length {length(y)}"
    ))
  }
}
```

### Error Message with Rich Context

```r
check_required_columns <- function(data, required_cols) {
  actual_cols <- names(data)
  missing_cols <- setdiff(required_cols, actual_cols)

  if (length(missing_cols) > 0) {
    cli_abort(c(
      "Required column{?s} missing from data",
      "x" = "Missing {length(missing_cols)} column{?s}: {.field {missing_cols}}",
      "i" = "Data has {length(actual_cols)} column{?s}: {.field {actual_cols}}",
      "i" = "Add the missing column{?s} or check for typos"
    ))
  }

  invisible(data)
}
```

### Function with Progress Bar

```r
process_files <- function(files, verbose = TRUE) {
  n <- length(files)

  if (verbose) {
    cli_progress_bar(
      format = "Processing {cli::pb_bar} {cli::pb_current}/{cli::pb_total} [{cli::pb_eta}]",
      total = n
    )
  }

  results <- vector("list", n)

  for (i in seq_along(files)) {
    results[[i]] <- process_file(files[[i]])

    if (verbose) {
      cli_progress_update()
    }
  }

  results
}
```

## Resources & Advanced Topics

### Reference Files

- **[references/inline-markup.md](references/inline-markup.md)** - Complete catalog of inline classes organized by category, advanced patterns, nesting rules, and real-world examples

- **[references/conditions.md](references/conditions.md)** - Advanced error design patterns, rlang integration, testing with testthat snapshots, migration guide, and anti-patterns

- **[references/progress.md](references/progress.md)** - Nested progress bars, custom formats, all progress variables, parallel processing, Shiny integration, and debugging

- **[references/themes.md](references/themes.md)** - Complete theming system with CSS-like selectors, container functions, color palettes, custom themes, and accessibility

- **[references/ansi-operations.md](references/ansi-operations.md)** - ANSI string operations (align, columns, nchar, etc.), hyperlinks, color detection, testing CLI output, and troubleshooting

### External Resources

- [cli package documentation](https://cli.r-lib.org)
- [cli GitHub repository](https://github.com/r-lib/cli)
- [Building a semantic CLI (article)](https://cli.r-lib.org/articles/semantic-cli.html)

### Related Packages

- **rlang** - Condition handling and error objects integrate with cli
- **glue** - String interpolation powers cli's `{}` syntax
- **testthat** - Snapshot testing for cli output
