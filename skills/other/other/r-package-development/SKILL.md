---
name: r-package-development
description: R package development with devtools, testthat, and roxygen2. Use when the user is working on an R package, running tests, writing documentation, or building package infrastructure.
metadata:
  author: Simon P. Couch (@simonpcouch)
  version: "1.1"
---

# R package development

## Key commands

```
# Run code in the package
Rscript -e "devtools::load_all(); code"

# Run all tests
Rscript -e "devtools::test()"

# Run all tests for files starting with {name}
Rscript -e "devtools::test(filter = '^{name}')"

# Run all tests for R/{name}.R
Rscript -e "devtools::test_active_file('R/{name}.R')"

# Run a single test "blah" for R/{name}.R
Rscript -e "devtools::test_active_file('R/{name}.R', desc = 'blah')"

# Redocument the package
Rscript -e "devtools::document()"

# Check pkgdown documentation
Rscript -e "pkgdown::check_pkgdown()"

# Check the package with R CMD check
Rscript -e "devtools::check()"

# Format code
air format .
```

## Coding

* Always run `air format .` after generating code.
* Use the base pipe operator (`|>`) not the magrittr pipe (`%>`).
* Use `\() ...` for single-line anonymous functions. For all other cases, use `function() {...}`.

## Testing

- Tests for `R/{name}.R` go in `tests/testthat/test-{name}.R`.
- All new code should have an accompanying test.
- If there are existing tests, place new tests next to similar existing tests.
- Strive to keep tests minimal with few comments.
- Avoid `expect_true()` and `expect_false()` in favour of a specific expectation which will give a better failure message.
- When testing errors and warnings, don't use `expect_error()` or `expect_warning()`. Instead, use `expect_snapshot(error = TRUE)` for errors and `expect_snapshot()` for warnings because these allow the user to review the full text of the output.

## Documentation

- Every user-facing function should be exported and have roxygen2 documentation.
- Wrap roxygen comments at 80 characters.
- Internal functions should not have roxygen documentation.
- Whenever you add a new (non-internal) documentation topic, also add the topic to `_pkgdown.yml`.
- Always re-document the package after changing a roxygen2 comment.
- Use `pkgdown::check_pkgdown()` to check that all topics are included in the reference index.

## `NEWS.md`

- Every user-facing change should be given a bullet in `NEWS.md`. Do not add bullets for small documentation changes or internal refactorings.
- Each bullet should briefly describe the change to the end user and mention the related issue in parentheses.
- A bullet can consist of multiple sentences but should not contain any new lines (i.e. DO NOT line wrap).
- If the change is related to a function, put the name of the function early in the bullet.
- Order bullets alphabetically by function name. Put all bullets that don't mention function names at the beginning.