---
name: r-cli-app
description: Build command-line apps in R using the Rapp package. Use when creating a CLI tool in R, adding argument parsing to an R script, turning an R script into a command-line app, shipping CLIs in an R package, or using Rapp (the alternative Rscript front-end). Also use for shebang scripts, exec/ directory in R packages, or subcommand-based R tools.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.1"
license: MIT
---

# Building CLI Apps with Rapp

Rapp (v0.3.0) is an R package that provides a drop-in replacement for `Rscript`
that automatically parses command-line arguments into R values. It turns simple
R scripts into polished CLI apps with argument parsing, help text, and subcommand
support — with zero boilerplate.

**R ≥ 4.1.0** | **CRAN:** `install.packages("Rapp")` | **GitHub:** `r-lib/Rapp`

After installing, put the `Rapp` launcher on PATH:

```r
Rapp::install_pkg_cli_apps("Rapp")
```

This places the `Rapp` executable in `~/.local/bin` (macOS/Linux) or
`%LOCALAPPDATA%\Programs\R\Rapp\bin` (Windows).

---

## Core Concept: Scripts Are the Spec

Rapp scans **top-level expressions** of an R script and converts specific
patterns into CLI constructs. This means:

1. The same script works identically via `source()` and as a CLI tool.
2. You write normal R code — Rapp infers the CLI from what you write.
3. Default values in your R code become the CLI defaults.

Only top-level assignments are recognized. Assignments inside functions,
loops, or conditionals are not parsed as CLI arguments.

---

## Pattern Recognition: R → CLI Mapping

This table is the heart of Rapp — each R pattern automatically maps to a
CLI surface:

| R Top-Level Expression | CLI Surface | Notes |
|---|---|---|
| `foo <- "text"` | `--foo <value>` | String option |
| `foo <- 1L` | `--foo <int>` | Integer option |
| `foo <- 3.14` | `--foo <float>` | Float option |
| `foo <- TRUE` / `FALSE` | `--foo` / `--no-foo` | Boolean toggle |
| `foo <- NA_integer_` | `--foo <int>` | Optional integer (NA = not set) |
| `foo <- NA_character_` | `--foo <str>` | Optional string (NA = not set) |
| `foo <- NULL` | positional arg | Required by default |
| `foo... <- NULL` | variadic positional | Zero or more values |
| `foo <- c()` | repeatable `--foo` | Multiple values as strings |
| `foo <- list()` | repeatable `--foo` | Multiple values parsed as YAML/JSON |
| `switch("", cmd1={}, cmd2={})` | subcommands | `app cmd1`, `app cmd2` |
| `switch(cmd <- "", ...)` | subcommands | Same; captures command name in `cmd` |

### Type behavior

- **Non-string scalars** are parsed as YAML/JSON at the CLI and coerced to the
  R type of the default. `n <- 5L` means `--n 10` gives integer `10L`.
- **NA defaults** signal optional arguments. Test with `!is.na(myvar)`.
- **Snake case** variable names map to kebab-case: `n_flips` → `--n-flips`.
- **Positional args** always arrive as character strings — convert manually.

---

## Script Structure

### Shebang line

```r
#!/usr/bin/env Rapp
```

Makes the script directly executable on macOS/Linux after `chmod +x`.
On Windows, call `Rapp myscript.R` explicitly.

### Front matter metadata

Hash-pipe comments (`#|`) before any code set script-level metadata:

```r
#!/usr/bin/env Rapp
#| name: my-app
#| title: My App
#| description: |
#|   A short description of what this app does.
#|   Can span multiple lines using YAML block scalar `|`.
```

The `name:` field sets the app name in help output (defaults to filename).

### Per-argument annotations

Place `#|` comments immediately before the assignment they annotate:

```r
#| description: Number of coin flips
#| short: 'n'
flips <- 1L
```

Available annotation fields:

| Field | Purpose |
|---|---|
| `description:` | Help text shown in `--help` |
| `title:` | Display title (for subcommands and front matter) |
| `short:` | Single-letter alias, e.g. `'n'` → `-n` |
| `required:` | `true`/`false` — for positional args only |
| `val_type:` | Override type: `string`, `integer`, `float`, `bool`, `any` |
| `arg_type:` | Override CLI type: `option`, `switch`, `positional` |
| `action:` | For repeatable options: `replace` or `append` |

Add `#| short:` for frequently-used options — users expect single-letter
shortcuts for common flags like verbose (`-v`), output (`-o`), or count (`-n`).

---

## Named Options

Scalar literal assignments become named options:

```r
name <- "world"          # --name <value>    (string, default "world")
count <- 1L              # --count <int>     (integer, default 1)
threshold <- 0.5         # --threshold <flt> (float, default 0.5)
seed <- NA_integer_      # --seed <int>      (optional, NA if omitted)
output <- NA_character_  # --output <str>    (optional, NA if omitted)
```

For optional arguments, test whether the user supplied them:

```r
seed <- NA_integer_
if (!is.na(seed)) set.seed(seed)
```

## Boolean Switches

`TRUE`/`FALSE` assignments become toggles:

```r
verbose <- FALSE   # --verbose or --no-verbose
wrap <- TRUE       # --wrap (default) or --no-wrap
```

Values `yes`/`true`/`1` set TRUE; `no`/`false`/`0` set FALSE.

## Repeatable Options

```r
pattern <- c()     # --pattern '*.csv' --pattern 'sales-*'  → character vector
threshold <- list() # --threshold 5 --threshold '[10,20]'   → list of parsed values
```

## Positional Arguments

Assign `NULL` for positional args (required by default):

```r
#| description: The input file to process.
input_file <- NULL
```

Make optional with `#| required: false`. Test with `is.null(myvar)`.

### Variadic positional args

Use `...` suffix to collect multiple positional values:

```r
pkgs... <- c()
# install-pkgs dplyr ggplot2 tidyr → pkgs... = c("dplyr", "ggplot2", "tidyr")
```

---

## Subcommands

Use `switch()` with a string first argument to declare subcommands.
Options before the `switch()` are global; options inside branches are
local to that subcommand.

```r
switch(
  command <- "",

  #| title: Display the todos
  list = {
    #| description: Max entries to display (-1 for all).
    limit <- 30L
    # ... list implementation
  },

  #| title: Add a new todo
  add = {
    #| description: Task description to add.
    task <- NULL
    # ... add implementation
  },

  #| title: Mark a task as completed
  done = {
    #| description: Index of the task to complete.
    index <- 1L
    # ... done implementation
  }
)
```

Help is scoped: `myapp --help` lists commands; `myapp list --help` shows
list-specific options plus globals. Subcommands can nest by placing another
`switch()` inside a branch.

---

## Built-in Help

Every Rapp automatically gets `--help` (human-readable) and `--help-yaml`
(machine-readable). These work with subcommands too.

---

## Development and Testing

### Interactive Development

Use `Rapp::run()` to test scripts from an R session:

```r
Rapp::run("path/to/myapp.R", c("--help"))
Rapp::run("path/to/myapp.R", c("--name", "Alice", "--count", "5"))
```

It returns the evaluation environment (invisibly) for inspection, and
supports `browser()` for interactive debugging.

### Testing CLI Apps in Packages

Use `Rapp::run()` with `testthat` snapshot testing. Test computed values by
accessing the returned environment, and test output with `expect_snapshot()`.

**See [references/advanced.md](references/advanced.md#testing-cli-apps)** for
detailed testing patterns, including:

- Accessing computed values via the evaluation environment
- Snapshot testing for help output and formatted text
- Testing file side effects and state changes

---

## Complete Example: Coin Flipper

```r
#!/usr/bin/env Rapp
#| name: flip-coin
#| description: |
#|   Flip a coin.

#| description: Number of coin flips
#| short: 'n'
flips <- 1L

sep <- " "
wrap <- TRUE

seed <- NA_integer_
if (!is.na(seed)) {
  set.seed(seed)
}

cat(sample(c("heads", "tails"), flips, TRUE), sep = sep, fill = wrap)
```

```sh
flip-coin            # heads
flip-coin -n 3       # heads tails heads
flip-coin --seed 42 -n 5
flip-coin --help
```

Generated help:
```
Usage: flip-coin [OPTIONS]

Flip a coin.

Options:
  -n, --flips <FLIPS>  Number of coin flips [default: 1] [type: integer]
      --sep <SEP>      [default: " "] [type: string]
      --wrap / --no-wrap  [default: true]
      --seed <SEED>    [default: NA] [type: integer]
```

## Complete Example: Todo Manager (Subcommands)

```r
#!/usr/bin/env Rapp
#| name: todo
#| description: Manage a simple todo list.

#| description: Path to the todo list file.
#| short: s
store <- ".todo.yml"

switch(
  command <- "",

  list = {
    #| description: Max entries to display (-1 for all).
    limit <- 30L

    tasks <- if (file.exists(store)) yaml::read_yaml(store) else list()
    if (!length(tasks)) {
      cat("No tasks yet.\n")
    } else {
      if (limit >= 0L) tasks <- head(tasks, limit)
      writeLines(sprintf("%2d. %s\n", seq_along(tasks), tasks))
    }
  },

  add = {
    #| description: Task description to add.
    task <- NULL

    tasks <- if (file.exists(store)) yaml::read_yaml(store) else list()
    tasks[[length(tasks) + 1L]] <- task
    yaml::write_yaml(tasks, store)
    cat("Added:", task, "\n")
  },

  done = {
    #| description: Index of the task to complete.
    #| short: i
    index <- 1L

    tasks <- if (file.exists(store)) yaml::read_yaml(store) else list()
    task <- tasks[[as.integer(index)]]
    tasks[[as.integer(index)]] <- NULL
    yaml::write_yaml(tasks, store)
    cat("Completed:", task, "\n")
  }
)
```

```sh
todo add "Write quarterly report"
todo list
todo list --limit 5
todo done 1
todo --store /tmp/work.yml list
```

---

## Shipping CLIs in an R Package

Place CLI scripts in `exec/` and add `Rapp` to `Imports` in DESCRIPTION:

```
mypkg/
├── DESCRIPTION
├── R/
├── exec/
│   ├── myapp       # script with #!/usr/bin/env Rapp shebang
│   └── myapp2
└── man/
```

Users install the CLI launchers after installing the package:

```r
Rapp::install_pkg_cli_apps("mypkg")
```

Expose a convenience installer so users don't need to know about Rapp:

```r
#' Install mypkg CLI apps
#' @export
install_mypkg_cli <- function(destdir = NULL) {
  Rapp::install_pkg_cli_apps(package = "mypkg", destdir = destdir)
}
```

By default, launchers set `--default-packages=base,<pkg>`, so only `base`
and the package are auto-loaded. Use `library()` for other dependencies.

---

## Quick Reference: Common Patterns

### NA vs NULL for optional arguments

- **NA** (`NA_integer_`, `NA_character_`) → optional **named option**.
  Test: `!is.na(x)`.
- **NULL** + `#| required: false` → optional **positional arg**.
  Test: `!is.null(x)`.

### stdin/stdout

```r
input_file <- NA_character_
con <- if (is.na(input_file)) file("stdin") else file(input_file, "r")
lines <- readLines(con)
writeLines(lines, stdout())
```

### Exit codes and stderr

```r
message("Error: something went wrong")   # writes to stderr
cat("Error:", msg, "\n", file = stderr()) # also stderr
quit(status = 1)                          # non-zero exit
```

### Error handling

```r
tryCatch({
  result <- do_work()
}, error = function(e) {
  cat("Error:", conditionMessage(e), "\n", file = stderr())
  quit(status = 1)
})
```

---

## Additional Reference

For less common topics — launcher customization (`#| launcher:` front matter),
detailed `Rapp::install_pkg_cli_apps()` API options, and more complete examples
(deduplication filter, variadic install-pkg, interactive fallback) — read
`references/advanced.md`.