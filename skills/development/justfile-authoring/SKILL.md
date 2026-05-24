---
name: justfile-authoring
description: Create, edit, or review justfiles for the just command runner. Use when adding or modifying recipes, parameters, dependencies, settings, attributes, aliases, or shebang scripts; fixing invocation or working-directory behavior; or documenting tasks for `just --list` output.
---

# Justfile Authoring

## Follow existing conventions

- Locate the nearest `justfile` or `.justfile` to the working directory and edit in place.
- Preserve naming style, indentation, and grouping conventions.
- Keep diffs minimal; avoid renaming recipes unless requested.

## Edit workflow

1. Read the existing `justfile` top to bottom; note `set` directives, variables, aliases, and groups.
2. Add or update recipes using the same structure and indentation.
3. Ensure dependencies and parameters are correct and consistent.
4. If a recipe should be hidden from listings, mark it private or prefix with `_`.

## Syntax essentials

- **Recipe:**

  ```just
  build target="app": clean
      cargo build --release --bin {{target}}
  ```

- **Dependencies:** run before the recipe body; parameterized deps are wrapped in parentheses.

  ```just
  rebuild: clean build
  build arch: (clean arch)
      cargo build --target {{arch}}
  ```

- **Parameters:** defaults supported; variadics use `*` (zero or more) or `+` (one or more).

  ```just
  test suite="all":
      cargo test --tests {{suite}}

  backup *files:
      tar czf backup.tar.gz {{files}}
  ```

- **Exported parameters:** prefix with `$` to pass as environment variables.

  ```just
  test-with-env $TEST_MODE:
      echo "$TEST_MODE"
  ```

- **Variables and interpolation:**

  ```just
  app := "myapp"
  build:
      echo "{{app}}"
  ```

- **Default recipe:** place first if you want it to run with `just`.

  ```just
  default:
      @just --list
  ```

## Settings

Use `set` to configure behavior globally.

```just
set dotenv-load := true
set shell := ["bash", "-eo", "pipefail", "-c"]
set working-directory := "ios"
```

## Attributes and helpers

Common attributes:

- `[group('name')]` or `[group: 'name']` to categorize recipes in listings.
- `[working-directory('path')]` to override the cwd for one recipe.
- `[private]` to hide a recipe or alias from `just --list`.
- `[doc('description')]` to control list output text.
- `[confirm('prompt')]` to request confirmation.
- `[linux]`, `[macos]`, `[windows]` for platform-specific recipes.
- `[no-cd]` to run in the invoking directory instead of the justfile directory.
- `[positional-arguments]` for positional-argument recipes.

Aliases:

```just
alias b := build
```

## Shebang recipes

For multi-line scripts, start the body with a shebang.

```just
release:
    #!/usr/bin/env bash
    set -euo pipefail
    ./scripts/release.sh
```

## Editing checklist

- Keep indentation consistent (spaces or tabs, not both, within a recipe).
- Use `@` on a line (or `@` before the recipe name) to suppress command echoing.
- Prefer `group` and `doc` attributes for clarity in `just --list`.
- Avoid unused variables, aliases, or recipes.
- For repo-specific paths, anchor to the existing `working-directory` conventions.
