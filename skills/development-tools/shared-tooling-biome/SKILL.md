---
name: shared-tooling-biome
description: Biome v2 unified linter, formatter, and import organizer — single Rust-powered tool replacing ESLint + Prettier with 97% Prettier compatibility and 20x faster performance
---

# Biome

> **Quick Guide:** Biome is a unified linter, formatter, and import organizer for JavaScript, TypeScript, JSX, TSX, JSON, CSS, and GraphQL. Single Rust binary replaces ESLint + Prettier with 97% Prettier compatibility. Use `biome.json` for all configuration. Run `biome check --write` to lint, format, and organize imports in one pass. Use `biome ci` in pipelines.
>
> **Current stable version:** Biome v2.4.x (March 2026). Biome v2 introduced type-aware linting, nested configs, and a revamped import organizer.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `biome.json` or `biome.jsonc` for ALL configuration — Biome does not use JavaScript config files)**

**(You MUST pin Biome to an exact version with `--save-exact` — Biome formatting can change between versions)**

**(You MUST use `biome ci` in CI pipelines, NOT `biome check` — `ci` is read-only with no `--write` flag)**

**(You MUST use `biome check --write` for local development — runs linter, formatter, and import organizer in one pass)**

**(You MUST include `$schema` in biome.json for editor autocompletion and validation)**

</critical_requirements>

---

**Auto-detection:** Biome, biome.json, biome.jsonc, @biomejs/biome, biome check, biome lint, biome format, biome ci, biome-ignore, organizeImports, biome migrate

**When to use:**

- Setting up a unified linter + formatter for JavaScript/TypeScript projects
- Replacing ESLint + Prettier with a single, faster tool
- Configuring import organizing with custom group ordering
- Migrating from ESLint and/or Prettier to Biome
- Setting up CI pipelines with `biome ci`
- Configuring pre-commit hooks with Biome's `--staged` flag

**When NOT to use:**

- Projects requiring ESLint plugins with no Biome equivalent (e.g., custom framework-specific plugins)
- Projects needing Markdown, YAML, or TOML formatting (Biome does not support these yet)
- Runtime code (this is build-time tooling only)
- Git hooks framework setup (Husky/Lefthook configuration is a separate concern)
- TypeScript compiler configuration (`tsconfig.json` is a separate concern)

**Key patterns covered:**

- biome.json configuration with formatter, linter, and assist settings
- Linter rule groups (recommended, all, nursery) and severity levels
- Formatter configuration (indent style, line width, quotes, semicolons)
- Import organizer with custom group ordering
- CLI commands: check, format, lint, ci, migrate
- Migration from ESLint + Prettier
- Git hooks integration (Husky, Lefthook, `--staged` flag)
- CI integration with GitHub Actions and GitLab CI
- Editor integration (VS Code, JetBrains)
- Suppression comments (`biome-ignore`, `biome-ignore-all`, range suppressions)
- Nested configuration for monorepos
- Overrides for file-specific settings

---

## Examples

- [Setup & Configuration](examples/core.md) — Installation, biome.json, VS Code, monorepos, framework configs
- [Linting Rules](examples/linting.md) — Rule groups, domains, suppressions, overrides, import ordering
- [Formatting](examples/formatting.md) — Formatter options, Prettier compatibility, option mapping
- [CI & Git Hooks](examples/ci.md) — GitHub Actions, GitLab CI, Husky, Lefthook, staged files
- [Migrating from ESLint/Prettier](examples/migration.md) — Automated migration, rule mapping, package cleanup

**Other resources:**

- [CLI Quick Reference](reference.md) — All CLI commands, flags, and configuration option tables

---

<philosophy>

## Philosophy

Biome unifies linting, formatting, and import organizing into a **single tool with a single configuration file**. Built in Rust, it delivers 20x faster performance than ESLint + Prettier while maintaining 97% Prettier compatibility.

**Core principles:**

1. **One tool, one config** — biome.json replaces .eslintrc, prettier.config, and import sorting plugins
2. **Sensible defaults** — Biome works out of the box with recommended rules enabled; zero-config is a valid setup
3. **Speed as a feature** — Rust-powered binary processes large codebases in milliseconds, not seconds
4. **Unified commands** — `biome check --write` runs everything in one pass (lint + format + organize imports)
5. **Safe by default** — Safe fixes apply automatically; unsafe fixes require explicit `--unsafe` flag

**When to use Biome:**

- Greenfield projects wanting a single, fast tool
- Projects where ESLint + Prettier configuration complexity is a burden
- Large codebases where linting/formatting speed matters
- Teams wanting zero-config or minimal-config setup
- Projects needing JS/TS/JSX/TSX/JSON/CSS/GraphQL support

**When NOT to use Biome:**

- Projects requiring niche ESLint plugins with no Biome equivalent
- Projects needing Markdown, YAML, or TOML formatting
- Projects heavily invested in custom ESLint rules that cannot be replicated
- Teams requiring ESLint's mature plugin ecosystem (accessibility plugins, framework-specific rules)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic biome.json Configuration

Every Biome project starts with a `biome.json` at the project root. Use `biome init` to scaffold one, then customize.

```bash
# Install Biome (always pin exact version)
npm install --save-dev --save-exact @biomejs/biome

# Create default biome.json
npx @biomejs/biome init
```

```jsonc
// biome.json — minimal recommended setup
{
  "$schema": "https://biomejs.dev/schemas/2.4.7/schema.json",
  "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true },
  "formatter": { "indentStyle": "space", "indentWidth": 2, "lineWidth": 100 },
  "linter": { "rules": { "recommended": true } },
  "assist": {
    "enabled": true,
    "actions": { "source": { "organizeImports": "on" } },
  },
}
```

**Why good:** `$schema` enables editor autocompletion, VCS integration respects `.gitignore`, explicit `indentStyle: "space"` avoids Biome's tab default, recommended rules provide a strong baseline

```jsonc
// BAD: No schema, no VCS, relying on defaults that differ from Prettier
{ "linter": { "enabled": true } }
```

**Why bad:** Missing `$schema` loses autocompletion, no VCS means linting node_modules, Biome defaults to tabs which surprises Prettier migrants

> **Full example:** See [examples/core.md](examples/core.md) for a production-ready biome.json with overrides, framework configs, and monorepo setup.

---

### Pattern 2: Linter Rules Configuration

Biome provides 459+ rules across 8 groups. Rules default to `recommended` — a curated subset of safe, stable rules.

#### Rule Groups

| Group           | Purpose                              | Default            |
| --------------- | ------------------------------------ | ------------------ |
| `accessibility` | Prevents a11y problems               | recommended        |
| `complexity`    | Simplifies overly complex code       | recommended        |
| `correctness`   | Detects guaranteed errors            | recommended        |
| `nursery`       | Experimental rules (opt-in required) | off                |
| `performance`   | Catches inefficient patterns         | recommended        |
| `security`      | Identifies security flaws            | recommended        |
| `style`         | Enforces consistent code style       | recommended (warn) |
| `suspicious`    | Flags likely incorrect patterns      | recommended        |

#### Severity Levels

| Level     | Behavior                           |
| --------- | ---------------------------------- |
| `"off"`   | Rule disabled                      |
| `"on"`    | Default severity for that rule     |
| `"info"`  | Informational, no CLI exit impact  |
| `"warn"`  | Non-blocking diagnostic            |
| `"error"` | Blocks CLI with non-zero exit code |

#### Domains (Technology-Specific Rules)

Biome v2 introduces domains that group rules by technology. Domains auto-detect from `package.json` dependencies.

```jsonc
{ "linter": { "domains": { "react": "recommended", "test": "recommended" } } }
```

> **Full examples:** See [examples/linting.md](examples/linting.md) for rule configuration, suppressions, overrides, and import ordering.

---

### Pattern 3: Formatter Configuration

Biome's formatter achieves 97% Prettier compatibility. Global settings apply to all languages; language-specific settings override globals. **Biome defaults to tabs** — set `indentStyle: "space"` explicitly when migrating from Prettier.

```jsonc
{
  "formatter": { "indentStyle": "space", "indentWidth": 2, "lineWidth": 100 },
  "javascript": {
    "formatter": { "quoteStyle": "double", "semicolons": "always" },
  },
  "json": { "formatter": { "trailingCommas": "none" } },
  "css": { "formatter": { "enabled": true } },
}
```

> **Full reference:** See [examples/formatting.md](examples/formatting.md) for all options, Prettier mapping, and language-specific settings.

---

### Pattern 4: Import Organizer

Biome v2 revamped the import organizer with custom group ordering. Configure under `assist.actions.source.organizeImports`.

```jsonc
{
  "assist": {
    "actions": {
      "source": {
        "organizeImports": {
          "level": "on",
          "options": {
            "groups": [
              [":BUN:", ":NODE:"],
              ":PACKAGE:",
              ":BLANK_LINE:",
              ["@company/**"],
              ":BLANK_LINE:",
              ":ALIAS:",
              ":PATH:",
              ":BLANK_LINE:",
              { "type": true },
            ],
            "identifierOrder": "natural",
          },
        },
      },
    },
  },
}
```

**Key options:** `identifierOrder` controls named import sorting — `"natural"` (default, e.g. `var1, var2, var11`) or `"lexicographic"` (strict alphabetical). Groups accept predefined matchers, glob patterns (`"@my/lib/**"`), object matchers (`{ "type": true, "source": ["@my/lib"] }`), or arrays combining any of these.

#### Predefined Groups

| Group                     | Matches                                    |
| ------------------------- | ------------------------------------------ |
| `:NODE:`                  | Node.js built-ins and `node:` protocol     |
| `:BUN:`                   | Bun-specific modules                       |
| `:PACKAGE:`               | Scoped and bare npm packages               |
| `:PACKAGE_WITH_PROTOCOL:` | Packages with a protocol prefix            |
| `:ALIAS:`                 | Aliased imports (`@/`, `#`, `~`, `$`, `%`) |
| `:PATH:`                  | Absolute and relative path imports         |
| `:URL:`                   | HTTP/HTTPS imports                         |
| `:BLANK_LINE:`            | Visual separator between groups            |

> **Full examples:** See [examples/linting.md](examples/linting.md#custom-import-ordering) for import ordering with results.

---

### Pattern 5: CLI Commands

Use `check` locally, `ci` in pipelines. Key commands:

```bash
npx biome check --write .          # Lint + format + organize imports (auto-fix)
npx biome ci .                     # CI mode (read-only, optimized for pipelines)
npx biome check --staged --write . # Pre-commit hooks (only staged files)
npx biome check --changed --since=main .  # Changed files only
```

> **Full reference:** See [examples/ci.md](examples/ci.md) for complete CLI usage, filtering, and reporting options.

---

### Pattern 6: Suppression Comments

Biome uses `biome-ignore` comments with required explanations.

```typescript
// biome-ignore lint/suspicious/noDebugger: needed for local debugging
debugger;

// biome-ignore-all lint/style/noDefaultExport: framework requires default export (top of file only)

// biome-ignore-start lint/suspicious/noDoubleEquals: legacy section
// biome-ignore-end lint/suspicious/noDoubleEquals: legacy section
```

| Type        | Syntax                                 | Scope                        |
| ----------- | -------------------------------------- | ---------------------------- |
| Inline      | `// biome-ignore <spec>: reason`       | Next line                    |
| File-wide   | `// biome-ignore-all <spec>: reason`   | Entire file (must be at top) |
| Range start | `// biome-ignore-start <spec>: reason` | Until matching end           |
| Range end   | `// biome-ignore-end <spec>: reason`   | Ends matching range          |

> **Full examples:** See [examples/linting.md](examples/linting.md#suppression-comments) for inline, file-level, and range suppressions.

---

### Pattern 7: Nested Configuration (Monorepos)

Biome v2 supports nested `biome.json` files. Each subdirectory can override the root config.

```jsonc
// packages/my-app/biome.json — inherits from root
{ "$schema": "https://biomejs.dev/schemas/2.4.7/schema.json", "extends": "//" }
```

```jsonc
// packages/legacy-lib/biome.json — relaxes rules
{
  "$schema": "https://biomejs.dev/schemas/2.4.7/schema.json",
  "root": false,
  "linter": { "rules": { "suspicious": { "noExplicitAny": "off" } } },
}
```

**Why good:** `"extends": "//"` shorthand inherits root config, `"root": false` marks as child, each package can relax or tighten rules independently

> **Full examples:** See [examples/core.md](examples/core.md#monorepo-nested-configuration) for root + child config patterns.

---

### Pattern 8: Overrides (File-Specific Rules)

Use `overrides` for file-pattern-specific configuration without nested config files.

```jsonc
{
  "overrides": [
    {
      "includes": ["**/*.test.ts", "**/*.test.tsx"],
      "linter": { "rules": { "suspicious": { "noExplicitAny": "off" } } },
    },
    {
      "includes": ["**/app/**/page.tsx", "**/app/**/layout.tsx"],
      "linter": { "rules": { "style": { "noDefaultExport": "off" } } },
    },
  ],
}
```

**Why good:** Overrides eliminate suppression comments in every file, test files get relaxed rules, framework conventions handled declaratively

> **Full examples:** See [examples/linting.md](examples/linting.md#overrides-file-specific-rules) for test, config, and generated file overrides.

</patterns>

---

<performance>

## Performance

Biome is written in Rust and processes files in parallel, making it significantly faster than JavaScript-based alternatives.

| Tool              | Format Time (1000 files) | Lint Time (1000 files) |
| ----------------- | ------------------------ | ---------------------- |
| Biome             | ~100ms                   | ~200ms                 |
| Prettier          | ~2000ms                  | N/A                    |
| ESLint            | N/A                      | ~3000ms                |
| ESLint + Prettier | ~5000ms                  | ~5000ms                |

_Approximate benchmarks. Actual performance varies by project size and rule configuration._

**Performance Tips:**

- **Use `biome check`** instead of running `biome format` and `biome lint` separately — single pass is faster
- **Enable VCS integration** to automatically skip ignored files (`.gitignore`)
- **Use `--staged` or `--changed`** in hooks and CI to process only affected files
- **Be selective with nursery rules** — some experimental rules may impact performance
- **Use `--profile-rules`** (v2.4+) to identify slow lint rules in your configuration

**Type-Aware Linting Performance:**

Biome v2 introduced type-aware linting without the TypeScript compiler. Enable selectively:

- **Default scan** discovers nested configs only (fast)
- **Project domain scan** indexes the full module graph (slower, but still faster than tsc)
- **Types domain scan** adds type inference (most comprehensive, most expensive)

</performance>

---

<decision_framework>

## Decision Framework

### Biome vs ESLint + Prettier

```
Need linting and formatting?
|-- Greenfield project?
|   |-- Want simplest possible setup? -> Biome (one tool, one config)
|   |-- Need niche ESLint plugins? -> ESLint + Prettier
|   +-- Speed is important? -> Biome (20x faster)
|-- Existing ESLint + Prettier project?
|   |-- Happy with current setup? -> Stay with ESLint + Prettier
|   |-- Config complexity is a pain? -> Migrate to Biome
|   |-- Need ESLint plugins without Biome equivalents? -> Stay
|   +-- Want faster CI/pre-commit hooks? -> Biome (or hybrid)
+-- Monorepo?
    |-- Need per-package lint configs? -> Biome v2 nested configs or ESLint 10
    +-- Speed bottleneck in CI? -> Biome
```

### Configuration Complexity

```
How to configure Biome?
|-- Just starting out? -> Run `biome init`, use defaults with recommended: true
|-- Migrating from ESLint? -> Run `biome migrate eslint --write`
|-- Migrating from Prettier? -> Run `biome migrate prettier --write`
|-- Need per-file rules?
|   |-- Different rules for test files? -> Use `overrides` in biome.json
|   +-- Different rules per package? -> Use nested biome.json with "root": false
+-- Need custom import ordering? -> Configure organizeImports.options.groups
```

> **Full migration decision tree:** See [examples/migration.md](examples/migration.md#full-migration-vs-hybrid-approach).

</decision_framework>

---

<integration>

## Integration Guide

**Works with:**

- **React/Next.js/Remix**: Full JSX/TSX support, domain-specific rules for React
- **TypeScript**: Type-aware linting without tsc dependency (Biome v2+)
- **CSS**: Linting enabled by default, formatting opt-in
- **JSON/JSONC**: Full support including tsconfig.json, package.json
- **GraphQL**: Linting enabled by default, formatting opt-in
- **Vue/Svelte/Astro**: Experimental support via `html.experimentalFullSupportEnabled` (v2.4+)

**Replaces / Conflicts with:**

- **ESLint**: Biome replaces ESLint for linting (or use hybrid approach)
- **Prettier**: Biome replaces Prettier for formatting
- **eslint-plugin-import**: Biome's import organizer replaces import sorting plugins
- **eslint-config-prettier**: Not needed — Biome has no formatter/linter conflicts

> **CI/editor integration:** See [examples/ci.md](examples/ci.md) and [examples/core.md](examples/core.md#vs-code-integration).

</integration>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `biome check` in CI instead of `biome ci` (`check` allows `--write` which is dangerous in pipelines; `ci` is read-only)
- Not pinning Biome version with `--save-exact` (formatting can change between minor versions, causing diff noise)
- Missing `$schema` in biome.json (loses editor autocompletion, validation, and discoverability)
- Using JavaScript config files instead of biome.json (Biome only supports JSON/JSONC configuration)
- Running `biome format` and `biome lint` separately when `biome check` does both (wastes time, parses files twice)

**Medium Priority Issues:**

- Forgetting to set `indentStyle: "space"` when migrating from Prettier (Biome defaults to tabs)
- Not enabling VCS integration (without it, Biome may process node_modules and dist)
- Using `--unsafe` without reviewing changes (unsafe fixes can alter program behavior)
- Not including `--no-errors-on-unmatched` in git hooks (causes failures when no matching files are staged)
- Enabling all nursery rules (they are experimental and may have bugs or performance issues)

**Common Mistakes:**

- Using `"root": true` in a nested config (this is the default; use `"root": false` for child configs)
- Expecting Markdown/YAML formatting support (Biome does not support these languages yet)
- Not running `biome migrate --write` when upgrading major versions (config schema changes between v1 and v2)
- Suppression comments without explanations (`biome-ignore lint:` requires text after the colon)

**Gotchas & Edge Cases:**

- Biome defaults to tabs, not spaces — always set `indentStyle` explicitly when migrating from Prettier
- CSS and GraphQL formatting is disabled by default — must opt in with `"formatter": { "enabled": true }`
- `biome-ignore-all` must be at the top of the file — placing it mid-file triggers an unused suppression warning
- Import organizer is part of `assist`, not `linter` — configure under `assist.actions.source.organizeImports`
- The `--staged` flag makes lint-staged unnecessary for Biome-only setups (since Biome v1.7.0+)
- Type-aware linting (project/types domains) triggers file scanning which can slow down first runs on large projects
- `biome migrate eslint --write` does not migrate inspired rules by default — use `--include-inspired` to include them
- Range suppressions (`biome-ignore-start`/`biome-ignore-end`) must have matching rule specifiers
- Biome treats all JS/TS/JSX/TSX under the `javascript` config key — there is no separate `typescript` section
- Configuration files named `.biome.json` (with leading dot) are also discovered (v2.4+)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `biome.json` or `biome.jsonc` for ALL configuration — Biome does not use JavaScript config files)**

**(You MUST pin Biome to an exact version with `--save-exact` — Biome formatting can change between versions)**

**(You MUST use `biome ci` in CI pipelines, NOT `biome check` — `ci` is read-only with no `--write` flag)**

**(You MUST use `biome check --write` for local development — runs linter, formatter, and import organizer in one pass)**

**(You MUST include `$schema` in biome.json for editor autocompletion and validation)**

**Failure to follow these rules will cause inconsistent formatting, broken CI pipelines, and missed lint errors.**

</critical_reminders>
