---
disable-model-invocation: false
name: cli-just
user-invocable: false
description: This skill should be used when the user asks to "create a justfile", "write just recipes", "configure just settings", "add just modules", "use just attributes", "set up task automation", mentions justfile, just command runner, or task automation with just.
---

# Just Command Runner

## Overview

Expert guidance for Just, a command runner with syntax inspired by make. Use this skill for creating justfiles, writing recipes, configuring settings, and implementing task automation workflows.

**Key capabilities:**

- Create and organize justfiles with proper structure
- Write recipes with attributes, dependencies, and parameters
- Configure settings for shell, modules, and imports
- Use built-in constants for terminal formatting
- Implement check/write patterns for code quality tools

## Quick Reference

### Essential Settings

```just
set allow-duplicate-recipes       # Allow recipes to override imported ones
set allow-duplicate-variables     # Allow variables to override imported ones
set shell := ["bash", "-euo", "pipefail", "-c"]  # Strict bash with error handling
set unstable                      # Enable unstable features (modules, script attribute)
set dotenv-load                   # Auto-load .env file
set positional-arguments          # Pass recipe args as $1, $2, etc.
```

### Common Attributes

| Attribute                 | Purpose                                        |
| ------------------------- | ---------------------------------------------- |
| `[arg("p", long, ...)]`   | Configure parameter as `--flag` option (v1.46) |
| `[arg("p", pattern="…")]` | Constrain parameter to match regex pattern     |
| `[group("name")]`         | Group recipes in `just --list` output          |
| `[no-cd]`                 | Don't change to justfile directory             |
| `[private]`               | Hide from `just --list` (same as `_` prefix)   |
| `[script]`                | Execute recipe as single script block          |
| `[script("interpreter")]` | Use specific interpreter (bash, python, etc.)  |
| `[confirm("prompt")]`     | Require user confirmation before running       |
| `[doc("text")]`           | Override recipe documentation                  |
| `[positional-arguments]`  | Enable positional args for this recipe only    |

### Recipe Argument Flags (v1.46.0+)

The `[arg()]` attribute configures parameters as CLI-style options:

```just
# Long option (--target)
[arg("target", long)]
build target:
    cargo build --target {{ target }}

# Short option (-v)
[arg("verbose", short="v")]
run verbose="false":
    echo "Verbose: {{ verbose }}"

# Combined long + short
[arg("output", long, short="o")]
compile output:
    gcc main.c -o {{ output }}

# Flag without value (presence sets to "true")
[arg("release", long, value="true")]
build release="false":
    cargo build {{ if release == "true" { "--release" } else { "" } }}

# Help string (shown in `just --usage`)
[arg("target", long, help="Build target architecture")]
build target:
    cargo build --target {{ target }}
```

**Usage examples:**

```bash
just build --target x86_64
just build --target=x86_64
just compile -o main
just build --release
just --usage build    # Show recipe argument help
```

Multiple attributes can be combined:

```just
[no-cd, private]
[group("checks")]
recipe:
    echo "hello"
```

### Built-in Constants

Terminal formatting constants are globally available (no definition needed):

| Constant                                            | Description                                |
| --------------------------------------------------- | ------------------------------------------ |
| `CYAN`, `GREEN`, `RED`, `YELLOW`, `BLUE`, `MAGENTA` | Text colors                                |
| `BOLD`, `ITALIC`, `UNDERLINE`, `STRIKETHROUGH`      | Text styles                                |
| `NORMAL`                                            | Reset formatting                           |
| `BG_*`                                              | Background colors (BG_RED, BG_GREEN, etc.) |
| `HEX`, `HEXLOWER`                                   | Hexadecimal digits                         |

Usage:

```just
@status:
    echo -e '{{ GREEN }}Success!{{ NORMAL }}'
    echo -e '{{ BOLD + CYAN }}Building...{{ NORMAL }}'
```

### Key Functions

```just
# Require executable exists (fails recipe if not found)
jq := require("jq")

# Get environment variable with default
log_level := env("LOG_LEVEL", "info")

# Get justfile directory path
root := justfile_dir()
```

## Recipe Patterns

### Status Reporter Pattern

Display formatted status during multi-step workflows:

```just
@_run-with-status recipe *args:
    echo ""
    echo -e '{{ CYAN }}→ Running {{ recipe }}...{{ NORMAL }}'
    just {{ recipe }} {{ args }}
    echo -e '{{ GREEN }}✓ {{ recipe }} completed{{ NORMAL }}'
alias rws := _run-with-status
```

### Check/Write Pattern

Pair check (verify) and write (fix) recipes for code quality tools:

```just
[group("checks")]
@biome-check +globs=".":
    na biome check {{ globs }}
alias bc := biome-check

[group("checks")]
@biome-write +globs=".":
    na biome check --write {{ globs }}
alias bw := biome-write
```

### Full Check/Write Pattern

Aggregate all checks with status reporting:

```just
[group("checks")]
@full-check:
    just _run-with-status biome-check
    just _run-with-status prettier-check
    just _run-with-status tsc-check
    echo ""
    echo -e '{{ GREEN }}All code checks passed!{{ NORMAL }}'
alias fc := full-check

[group("checks")]
@full-write:
    just _run-with-status biome-write
    just _run-with-status prettier-write
    echo ""
    echo -e '{{ GREEN }}All code fixes applied!{{ NORMAL }}'
alias fw := full-write
```

### Standard Alias Conventions

| Recipe         | Alias | Recipe         | Alias |
| -------------- | ----- | -------------- | ----- |
| full-check     | fc    | full-write     | fw    |
| biome-check    | bc    | biome-write    | bw    |
| prettier-check | pc    | prettier-write | pw    |
| mdformat-check | mc    | mdformat-write | mw    |
| tsc-check      | tc    | ruff-check     | rc    |
| test           | t     | build          | b     |

## Inline Scripts

Just supports inline scripts in any language via two methods:

### Script Attribute (Recommended)

Use `[script("interpreter")]` for cross-platform compatibility:

```just
[script("node")]
fetch-data:
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    console.log(data);

[script("python3")]
analyze:
    import json
    with open('package.json') as f:
        pkg = json.load(f)
    print(f"Package: {pkg['name']}@{pkg['version']}")

[script("bash")]
deploy:
    set -e
    npm run build
    aws s3 sync dist/ s3://bucket/
```

### Shebang Method

Use `#!/usr/bin/env interpreter` at the recipe start:

```just
node-script:
    #!/usr/bin/env node
    console.log(`Node ${process.version}`);
    console.log(JSON.stringify(process.env, null, 2));

python-script:
    #!/usr/bin/env python3
    import sys
    print(f"Python {sys.version}")

bash-script:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Running on $(uname -s)"
```

**When to use which:**

- `[script()]` - Better cross-platform support, cleaner syntax
- Shebang - Traditional Unix approach, works without `set unstable`

## Modules & Imports

### Import Pattern

Include recipes from another file:

```just
import "./just/settings.just"
import "./just/base.just"
import? "./local.just"    # Optional (no error if missing)
```

### Module Pattern

Load submodule (requires `set unstable`):

```just
mod foo                   # Loads foo.just or foo/justfile
mod bar "path/to/bar"     # Custom path
mod? optional             # Optional module

# Call module recipes
just foo::build
```

### Devkit Import Pattern

For projects using `@sablier/devkit`:

```just
import "./node_modules/@sablier/devkit/just/base.just"
import "./node_modules/@sablier/devkit/just/npm.just"
```

## Section Organization

Standard section header format:

```just
# ---------------------------------------------------------------------------- #
#                                 DEPENDENCIES                                 #
# ---------------------------------------------------------------------------- #
```

Common sections (in order):

1. **DEPENDENCIES** - Required tools with URLs
2. **CONSTANTS** - Glob patterns, environment vars
3. **RECIPES / COMMANDS** - Main entry points
4. **CHECKS** - Code quality recipes
5. **UTILITIES / INTERNAL HELPERS** - Private helpers

## Default Recipe

Always define a default recipe:

```just
# Show available commands
default:
    @just --list
```

## Dependencies Declaration

Document required tools at the top:

```just
# ---------------------------------------------------------------------------- #
#                                 DEPENDENCIES                                 #
# ---------------------------------------------------------------------------- #

# Bun: https://bun.sh
bun := require("bun")

# Ni: https://github.com/antfu-collective/ni
na := require("na")
ni := require("ni")
nlx := require("nlx")

# Usage: invoke directly in recipes (not with interpolation)
build:
    bun next build
```

**Note:** `require()` validates the tool exists at recipe evaluation time. Use the variable name directly (e.g., `bun`), not with interpolation (`{{ bun }}`).

## Context7 Fallback

For Just features not covered in this skill (new attributes, advanced functions, edge cases), fetch the latest documentation:

```
Use context7 MCP with library ID `/websites/just_systems-man` to get up-to-date Just documentation.
```

Example topics to search:

- `modules import mod` - Module system details
- `settings` - All available settings
- `attributes` - Recipe attributes
- `functions` - Built-in functions
- `script recipes` - Script block syntax

## Additional Resources

### Reference Files

For detailed patterns and comprehensive coverage, consult:

- **[`references/settings.md`](references/settings.md)** - Settings configuration and module system
- **[`references/recipes.md`](references/recipes.md)** - Recipe attributes, parameters, dependencies, and prefixes
- **[`references/syntax.md`](references/syntax.md)** - Constants, functions, variables, and CLI options
- **[`references/patterns.md`](references/patterns.md)** - Established conventions, section organization, helper patterns

### Example Templates

Working justfile templates in `examples/`:

- **[`devkit.just`](examples/devkit.just)** - Minimal template importing @sablier/devkit
- **[`standalone.just`](examples/standalone.just)** - Full standalone template with all patterns

### External Documentation

- **Official Manual**: https://just.systems/man/en/
- **GitHub Repository**: https://github.com/casey/just
- **Context7 Library ID**: `/websites/just_systems-man`

## Tips

1. Use `@` prefix to suppress command echo: `@echo "quiet"`
2. Use `+` for variadic parameters: `test +args`
3. Use `*` for optional variadic: `build *flags`
4. Quote glob patterns in variables: `GLOBS := "\"**/*.json\""`
5. Use `[no-cd]` in monorepos to stay in current directory
6. Private recipes start with `_` or use `[private]`
7. Always define aliases after recipe names for discoverability
