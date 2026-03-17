---
name: cran-extrachecks
description: >
  Prepare R packages for CRAN submission by checking for common ad-hoc requirements not caught by devtools::check(). Use when: (1) Preparing a package for first CRAN release, (2) Preparing a package update for CRAN resubmission, (3) Reviewing a package to ensure CRAN compliance, (4) Responding to CRAN reviewer feedback. Covers documentation requirements, DESCRIPTION field standards, URL validation, examples, and administrative requirements.
---

# CRAN Extra Checks

Help R package developers prepare packages for CRAN submission by systematically checking for common ad-hoc requirements that CRAN reviewers enforce but `devtools::check()` doesn't catch.

## Workflow

1. **Initial Assessment**: Ask user if this is first submission or resubmission
2. **Run Standard Checklist**: Work through each item systematically (see below)
3. **Identify Issues**: As you review files, note specific problems
4. **Propose Fixes**: Suggest specific changes for each issue found
5. **Implement Changes**: Make edits only when user approves
6. **Verify**: Confirm all changes are complete

## Standard CRAN Preparation Checklist

Work through these items systematically:

1. **Create NEWS.md**: Run `usethis::use_news_md()` if not already present
2. **Create cran-comments.md**: Run `usethis::use_cran_comments()` if not already present
3. **Review README**:
   - Ensure it includes install instructions that will be valid when the package is accepted to CRAN (usually `install.packages("pkgname")`).
   - Check that it does not contain relative links. This works on GitHub but will be flagged by CRAN. Use full URLs to package documentation or remove the links.
   - Does the README clearly explain the package purpose and functionality?
   - **Important**: If README.Rmd exists, edit ONLY README.Rmd (README.md will be overwritten), then run `devtools::build_readme()` to re-render README.md
4. **Proofread DESCRIPTION**: Carefully review `Title:` and `Description:` fields (see detailed guidance below)
5. **Check function documentation**: Verify all exported functions have `@return` and `@examples` (see detailed guidance below)
6. **Verify copyright holder**: Check that `Authors@R:` includes a copyright holder with role `[cph]`
7. **Review bundled file licensing**: Check licensing of any included third-party files
8. **Run URL checks**: Use `urlchecker::url_check()` and fix any issues

## Detailed CRAN Checks

### Documentation Requirements

**Return Value Documentation (Strictly Enforced)**

CRAN now strictly requires `@return` documentation for all exported functions. Use the roxygen2 tag `@return` to document what the function returns.

- Required even for functions marked `@keywords internal`
- Required even if function returns nothing - document as `@return None` or similar
- Must be present for every exported function

Example:
```r
# Missing @return - WILL BE REJECTED
#' Calculate sum
#' @export
my_sum <- function(x, y) {
  x + y
}

# Correct - includes @return
#' Calculate sum
#' @param x First number
#' @param y Second number
#' @return A numeric value
#' @export
my_sum <- function(x, y) {
  x + y
}

# For functions with no return value
#' Print message
#' @param msg Message to print
#' @return None, called for side effects
#' @export
print_msg <- function(msg) {
  cat(msg, "\n")
}
```

**Examples for Exported Functions**

If your exported function has a meaningful return value, it will almost definitely require an `@examples` section. Use the roxygen2 tag `@examples`.

- Required even for functions marked `@keywords internal`
- Exceptions exist for functions used purely for side effects (e.g., creating directories)
- Examples must be executable

**Un-exported Functions with Examples**

If you write roxygen examples for un-exported functions, you must either:

1. Call them with `:::` notation: `pkg:::my_fun()`
2. Use `@noRd` tag to suppress `.Rd` file creation

**Using `\dontrun{}` Sparingly**

`\dontrun{}` should only be used if the example really cannot be executed (e.g., missing additional software, API keys, etc.).

- If showing an error, wrap the call in `try()` instead
- Consider custom predicates (e.g., `googlesheets4::sheets_has_token()`) with `if ()` blocks
- Sometimes `interactive()` can be used as the condition
- Lengthy examples (> 5 sec) can use `\donttest{}`

**Never Comment Out Code in Examples**

```r
# BAD - Will be rejected
#' @examples
#' # my_function(x)  # Don't do this!
```

CRAN's guidance: "Examples/code lines in examples should never be commented out. Ideally find toy examples that can be regularly executed and checked."

**Guarding Examples with Suggested Packages**

Use `@examplesIf` for entire example sections requiring suggested packages:

```r
#' @examplesIf rlang::is_installed("dplyr")
#' library(dplyr)
#' my_data %>% my_function()
```

For individual code blocks within examples:
```r
#' @examples
#' if (rlang::is_installed("dplyr")) {
#'   library(dplyr)
#'   my_data %>% my_function()
#' }
```

### DESCRIPTION Title Field

CRAN enforces strict Title requirements:

**Use Title Case**

Capitalize all words except articles like 'a', 'the'. Use `tools::toTitleCase()` to help format.

**Avoid Redundancy**

Common phrases that get flagged:
- "A Toolkit for" → Remove
- "Tools for" → Remove
- "for R" → Remove

Examples:
```r
# BAD
Title: A Toolkit for the Construction of Modeling Packages for R

# GOOD
Title: Construct Modeling Packages

# BAD
Title: Command Argument Parsing for R

# GOOD
Title: Command Argument Parsing
```

**Quote Software/Package Names**

Put all software and R package names in single quotes:

```r
# GOOD
Title: Interface to 'Tiingo' Stock Price API
```

**Length Limit**

Keep titles under 65 characters.

### DESCRIPTION Description Field

**Never Start With Forbidden Phrases**

CRAN will reject descriptions starting with:
- "This package"
- Package name
- "Functions for"

```r
# BAD
Description: This package provides functions for rendering slides.
Description: Functions for rendering slides to different formats.

# GOOD
Description: Render slides to different formats including HTML and PDF.
```

**Expand to 3-4 Sentences**

Single-sentence descriptions are insufficient. Provide a broader description of:
- What the package does
- Why it may be useful
- Types of problems it helps solve

```r
# BAD (too short)
Description: Render slides to different formats.

# GOOD
Description: Render slides to different formats including HTML and PDF.
    Supports custom themes and progressive disclosure patterns. Integrates
    with 'reveal.js' for interactive presentations. Designed for technical
    presentations and teaching materials.
```

**Quote Software Names, Not Functions**

```r
# BAD
Description: Uses 'case_when()' to process data.

# GOOD
Description: Uses case_when() to process data with 'dplyr'.
```

Software, package, and API names get single quotes (including 'R'). Function names do not.

**Expand All Acronyms**

All acronyms must be fully expanded on first mention:

```r
# BAD
Description: Implements X-SAMPA processing.

# GOOD
Description: Implements Extended Speech Assessment Methods Phonetic
    Alphabet (X-SAMPA) processing.
```

**Publication Titles Only in Double Quotes**

Only use double quotes for publication titles, not for phrases or emphasis:

```r
# BAD
Description: Handles dates like "the first Monday of December".

# GOOD
Description: Handles dates like the first Monday of December.
```

### URL and Link Validation

**All URLs Must Use HTTPS**

CRAN requires `https://` protocol for all URLs. HTTP links will be rejected.

```r
# BAD
URL: http://paleobiodb.org/

# GOOD
URL: https://paleobiodb.org/
```

**No Redirecting URLs**

CRAN rejects URLs that redirect to other locations. Example rejection:

```
Found the following (possibly) invalid URLs:
URL: https://h3geo.org/docs/core-library/coordsystems#faceijk-coordinates
     (moved to https://h3geo.org/docs/core-library/coordsystems/)
```

**Use urlchecker Package**

```r
# Find redirecting URLs
urlchecker::url_check()

# Automatically update to final destinations
urlchecker::url_update()
```

**Ignore URLs That Will Exist After Publication**

Some URLs that don't currently resolve will exist once the package is published on CRAN. These should NOT be changed:

- CRAN badge URLs (e.g., `https://cran.r-project.org/package=pkgname`)
- CRAN status badges (e.g., `https://www.r-pkg.org/badges/version/pkgname`)
- CRAN check results (e.g., `https://cranchecks.info/badges/pkgname`)
- Package documentation URLs on r-universe or pkgdown sites that deploy after release

When `urlchecker::url_check()` flags these URLs, leave them as-is. They are aspirational URLs that will work once the package is on CRAN.

**Check for Invalid File URIs**

Relative links in README must exist after package build. Common issue:

```
Found the following (possibly) invalid file URI:
     URI: CODE_OF_CONDUCT.md
       From: README.md
```

This occurs when files are in `.Rbuildignore`. Solutions:
1. Remove file from `.Rbuildignore`
2. Use `usethis::use_code_of_conduct()` which generates sections without relative links

### Administrative Requirements

**Copyright Holder Role**

Always add `[cph]` role to Authors field, even if you're the only author:

```r
# Required
Authors@R: person("John", "Doe", role = c("aut", "cre", "cph"))
```

**Posit-Supported Packages**

For packages in Posit-related GitHub organizations (posit-dev, rstudio, r-lib, tidyverse, tidymodels) or maintained by someone with a @posit.co email address, include Posit Software, PBC as copyright holder and funder:

```r
Authors@R: c(
  person("Jane", "Doe", role = c("aut", "cre"),
         email = "jane.doe@posit.co"),
  person("Posit Software, PBC", role = c("cph", "fnd"),
         comment = c(ROR = "03wc8by49"))
)
```

**LICENSE Year**

Update LICENSE year to current submission year:

```r
# If LICENSE shows 2024 but submitting in 2026
# Update: 2024 → 2026
```

**Method References**

CRAN may ask:

> If there are references describing the methods in your package, please add these in the description field...

If there are no references, reply to the email explaining this. Consider adding a preemptive note in `cran-comments.md`:

```markdown
## Method References

There are no published references describing the methods in this package.
The package implements original functionality for [brief description].
```

## Key Files to Review

Work through these files systematically:

- **DESCRIPTION**: Title, Description, Authors@R, URLs, License year
- **R/*.R**: Function documentation (`@return`, `@examples`, `@examplesIf`, `@noRd`)
- **README.Rmd** (if exists): Edit this file (NOT README.md), then run `devtools::build_readme()`
- **README.md**: Review for install instructions, relative links, URLs. Only edit directly if no README.Rmd exists
- **cran-comments.md**: Preemptive notes for reviewers
- **NEWS.md**: Version notes for this release
- **.Rbuildignore**: Files referenced in README

## Common Fix Patterns

**DESCRIPTION Title:**
```r
# Before
Title: A Toolkit for the Construction of Modeling Packages for R

# After
Title: Construct Modeling Packages
```

**DESCRIPTION Description:**
```r
# Before
Description: This package provides functions for rendering slides.

# After
Description: Render slides to different formats including HTML and PDF.
    Supports custom themes and progressive disclosure. Integrates with
    'reveal.js' for interactive presentations.
```

**Function Documentation:**
```r
# Before - Missing @return
#' Calculate total
#' @param x Values
#' @export
calc_total <- function(x) sum(x)

# After - Complete documentation
#' Calculate total
#' @param x Numeric values to sum
#' @return A numeric value representing the sum
#' @examples
#' calc_total(1:10)
#' @export
calc_total <- function(x) sum(x)
```

## Useful Tools

- `tools::toTitleCase()` - Format titles with proper capitalization
- `urlchecker::url_check()` - Find problematic URLs
- `urlchecker::url_update()` - Fix redirecting URLs
- `usethis::use_news_md()` - Create NEWS.md
- `usethis::use_cran_comments()` - Create cran-comments.md
- `devtools::build_readme()` - Re-render README.md from README.Rmd
- `usethis::use_code_of_conduct()` - Add CoC without relative links
- `usethis::use_build_ignore()` - Ignore files in R package build
- `usethis::use_package()` - Add a package dependency to DESCRIPTION
- `usethis::use_tidy_description()` - Tidy up DESCRIPTION formatting

## Final Verification Checklist

Use this checklist to ensure nothing is missed before submission:

### Files and Structure
- [ ] `NEWS.md` exists and documents changes for this version
- [ ] `cran-comments.md` exists with submission notes
- [ ] If README.Rmd exists, it was edited (not README.md) and `devtools::build_readme()` was run
- [ ] README includes valid install instructions (`install.packages("pkgname")`)
- [ ] README has no relative links (all links are full URLs or removed)

### DESCRIPTION File
- [ ] `Title:` uses title case
- [ ] `Title:` has no redundant phrases ("A Toolkit for", "Tools for", "for R")
- [ ] `Title:` quotes all software/package names in single quotes
- [ ] `Title:` is under 65 characters
- [ ] `Description:` does NOT start with "This package", package name, or "Functions for"
- [ ] `Description:` is 3-4 sentences explaining purpose and utility
- [ ] `Description:` quotes software/package/API names (including 'R') but NOT function names
- [ ] `Description:` expands all acronyms on first mention
- [ ] `Description:` uses double quotes only for publication titles
- [ ] `Authors@R:` includes copyright holder with `[cph]` role
- [ ] For Posit packages: Includes `person("Posit Software, PBC", role = c("cph", "fnd"), comment = c(ROR = "03wc8by49"))`
- [ ] LICENSE year matches current submission year

### Function Documentation
- [ ] All exported functions have `@return` documentation
- [ ] All exported functions with meaningful returns have `@examples`
- [ ] No example sections use commented-out code
- [ ] Examples avoid `\dontrun{}` unless truly necessary
- [ ] Examples requiring suggested packages use `@examplesIf` or `if` guards
- [ ] Un-exported functions with examples use `:::` notation or `@noRd`

### URLs and Links
- [ ] `urlchecker::url_check()` was run
- [ ] All URLs use https protocol (no http links)
- [ ] No redirecting URLs (except aspirational CRAN badge URLs)
- [ ] Aspirational URLs (CRAN badges, etc.) are left as-is
- [ ] No relative links in README that reference `.Rbuildignore` files

### Optional but Recommended
- [ ] If concerns about method references, added preemptive note to `cran-comments.md`
- [ ] Reviewed bundled file licensing if including third-party files
