---
name: lifecycle
description: >
  Guidance for managing R package lifecycle according to tidyverse principles
  using the lifecycle package. Use when: (1) Setting up lifecycle
  infrastructure in a package, (2) Deprecating functions or arguments,
  (3) Renaming functions or arguments, (4) Superseding functions, (5) Marking
  functions as experimental, (6) Understanding lifecycle stages (stable,
  experimental, deprecated, superseded), or (7) Writing deprecation helpers for
  complex scenarios.
---

# R Package Lifecycle Management

Manage function and argument lifecycle using tidyverse conventions and the lifecycle package.

## Setup

Check if lifecycle is configured by looking for `lifecycle-*.svg` files in `man/figures/`.

If not configured, run:

```r
usethis::use_lifecycle()
```

This:

- Adds lifecycle to `Imports` in DESCRIPTION
- Adds `@importFrom lifecycle deprecated` to the package documentation file
- Copies badge SVGs to `man/figures/`

## Lifecycle Badges

Insert badges in roxygen2 documentation:

```r
#' @description
#' `r lifecycle::badge("experimental")`
#' `r lifecycle::badge("deprecated")`
#' `r lifecycle::badge("superseded")`
```

For arguments:

```r
#' @param old_arg `r lifecycle::badge("deprecated")` Use `new_arg` instead.
```

Only badge functions/arguments whose stage differs from the package's overall stage.

## Deprecating a Function

1. Add badge and explanation to `@description`:

```r
#' Do something
#'
#' @description
#' `r lifecycle::badge("deprecated")`
#'
#' `old_fun()` was deprecated in mypkg 1.0.0. Use [new_fun()] instead.
#' @keywords internal
```

2. Add `deprecate_warn()` as first line of function body:

```r
old_fun <- function(x) {

lifecycle::deprecate_warn("1.0.0", "old_fun()", "new_fun()")
new_fun(x)
}
```

3. Show migration in examples:

```r
#' @examples
#' old_fun(x)
#' # ->
#' new_fun(x)
```

## Deprecation Functions

| Function           | When to Use                                             |
| ------------------ | ------------------------------------------------------- |
| `deprecate_soft()` | First stage; warns only direct users and during tests   |
| `deprecate_warn()` | Standard deprecation; warns once per 8 hours            |
| `deprecate_stop()` | Final stage before removal; errors with helpful message |

**Deprecation workflow for major releases:**

1. Search `deprecate_stop()` - consider removing function entirely
2. Replace `deprecate_warn()` with `deprecate_stop()`
3. Replace `deprecate_soft()` with `deprecate_warn()`

## Renaming a Function

Move implementation to new name, call from old name with deprecation:

```r
#' @description
#' `r lifecycle::badge("deprecated")`
#'
#' `add_two()` was renamed to `number_add()` for API consistency.
#' @keywords internal
#' @export
add_two <- function(x, y) {
lifecycle::deprecate_warn("1.0.0", "add_two()", "number_add()")
number_add(x, y)
}

#' Add two numbers
#' @export
number_add <- function(x, y) {
x + y
}
```

## Deprecating an Argument

Use `deprecated()` as default value with `is_present()` check:

```r
#' @param path `r lifecycle::badge("deprecated")` Use `file` instead.
write_file <- function(x, file, path = deprecated()) {
  if (lifecycle::is_present(path)) {
    lifecycle::deprecate_warn("1.4.0", "write_file(path)", "write_file(file)")
    file <- path
  }
  # ... rest of function
}
```

## Renaming an Argument

```r
add_two <- function(x, y, na_rm = TRUE, na.rm = deprecated()) {
  if (lifecycle::is_present(na.rm)) {
    lifecycle::deprecate_warn("1.0.0", "add_two(na.rm)", "add_two(na_rm)")
    na_rm <- na.rm
  }
  sum(x, y, na.rm = na_rm)
}
```

## Superseding a Function

For functions with better alternatives that shouldn't be removed:

```r
#' Gather columns into key-value pairs
#'
#' @description
#' `r lifecycle::badge("superseded")`
#'
#' Development on `gather()` is complete. For new code, use [pivot_longer()].
#'
#' `df %>% gather("key", "value", x, y, z)` is equivalent to
#' `df %>% pivot_longer(c(x, y, z), names_to = "key", values_to = "value")`.
```

No warning needed - just document the preferred alternative.

## Marking as Experimental

```r
#' @description
#' `r lifecycle::badge("experimental")`
cool_function <- function() {
  lifecycle::signal_stage("experimental", "cool_function()")
  # ...
}
```

## Testing Deprecations

Test that deprecated functions work and warn appropriately:

```r
test_that("old_fun is deprecated", {
  expect_snapshot({
    x <- old_fun(1)
    expect_equal(x, expected_value)
  })
})
```

Suppress warnings in existing tests:

```r
test_that("old_fun returns correct value", {
  withr::local_options(lifecycle_verbosity = "quiet")
  expect_equal(old_fun(1), expected_value)
})
```

## Deprecation Helpers

For deprecations affecting many functions (e.g., removing a common argument), create an internal helper:

```r
warn_for_verbose <- function(
  verbose = TRUE,
  env = rlang::caller_env(),
  user_env = rlang::caller_env(2)
) {
  if (!lifecycle::is_present(verbose) || isTRUE(verbose)) {
    return(invisible())
  }

  lifecycle::deprecate_warn(
    when = "2.0.0",
    what = I("The `verbose` argument"),
    details = c(
      "Set `options(mypkg_quiet = TRUE)` to suppress messages.",
      "The `verbose` argument will be removed in a future release."
    ),
    user_env = user_env
  )

  invisible()
}
```

Then use in affected functions:

```r
my_function <- function(..., verbose = deprecated()) {
  warn_for_verbose(verbose)
  # ...
}
```

## Custom Deprecation Messages

For non-standard deprecations, use `I()` to wrap custom text:

```r
lifecycle::deprecate_warn(
  when = "1.0.0",
  what = I('Setting option "pkg.opt" to "foo"'),
  with = I('"pkg.new_opt"')
)
```

The `what` fragment must work with "was deprecated in..." appended.

## Reference

See `references/lifecycle-stages.md` for detailed stage definitions and transitions.
