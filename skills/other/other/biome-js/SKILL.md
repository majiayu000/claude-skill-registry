---
disable-model-invocation: false
name: biome-js
user-invocable: false
description: This skill should be used when the user asks to "configure Biome", "extend biome config", "set up BiomeJS", "add biome overrides", "biome lint-staged", "fix biome errors", or mentions biome.jsonc, Biome linting, or Biome formatting configuration.
---

# BiomeJS Skill

Quick guidance for BiomeJS configuration based on Sablier project patterns.

## Core Concepts

### Extending Shared Configs

Extend shared configs via npm package exports. The consuming project must always provide its own `files.includes`:

```jsonc
{
  "$schema": "./node_modules/@biomejs/biome/configuration_schema.json",
  "extends": ["@sablier/devkit/biome"],
  "files": {
    "includes": ["**/*.{js,json,jsonc,ts}", "!node_modules/**/*"]
  }
}
```

For UI projects, extend both base and ui configs:

```jsonc
{
  "extends": ["@sablier/devkit/biome/base", "@sablier/devkit/biome/ui"],
  "files": {
    "includes": ["**/*.{css,js,jsx,json,jsonc,ts,tsx}"]
  }
}
```

### Monorepo Inheritance

In monorepos, workspace configs inherit from root using `"//"`:

```jsonc
// packages/my-package/biome.jsonc
{
  "extends": ["//"],
  "overrides": [
    // package-specific overrides
  ]
}
```

### File Includes Pattern

Always specify `files.includes` explicitly. Common patterns:

| Project Type | Pattern                                       |
| ------------ | --------------------------------------------- |
| Library      | `**/*.{js,json,jsonc,ts}`                     |
| UI/Frontend  | `**/*.{css,js,jsx,json,jsonc,ts,tsx}`         |
| With GraphQL | `**/*.{css,graphql,js,jsx,json,jsonc,ts,tsx}` |

Exclusions: `!node_modules/**/*`, `!**/generated`, `!dist`

## Common Overrides

### Test Files

Relax strict rules in test files:

```jsonc
{
  "overrides": [
    {
      "includes": ["**/tests/**/*.ts", "**/*.test.ts"],
      "linter": {
        "rules": {
          "style": {
            "noNonNullAssertion": "off"
          },
          "suspicious": {
            "noExplicitAny": "off"
          }
        }
      }
    }
  ]
}
```

### Generated/ABI Files

Disable sorting and compact formatting for generated code:

```jsonc
{
  "overrides": [
    {
      "includes": ["**/abi/**/*.ts", "**/generated/**/*.ts"],
      "assist": {
        "actions": {
          "source": {
            "useSortedKeys": "off"
          }
        }
      },
      "javascript": {
        "formatter": {
          "expand": "never"
        }
      }
    }
  ]
}
```

### Import Restrictions

Enforce barrel imports for specific modules:

```jsonc
{
  "overrides": [
    {
      "includes": ["src/**/*.{ts,tsx}"],
      "linter": {
        "rules": {
          "correctness": {
            "noRestrictedImports": {
              "level": "error",
              "options": {
                "paths": {
                  "@/core": "Import from @/core (barrel) instead of subpaths"
                }
              }
            }
          }
        }
      }
    }
  ]
}
```

## Key Rules Reference

| Rule                      | Default              | Rationale                               |
| ------------------------- | -------------------- | --------------------------------------- |
| `noFloatingPromises`      | error                | Floating promises cause bugs            |
| `noUnusedImports`         | off                  | Allow during dev, enforce in pre-commit |
| `noUnusedVariables`       | error                | Keep code clean                         |
| `useImportType`           | warn (separatedType) | Explicit type imports                   |
| `useSortedKeys`           | on                   | Consistent object ordering              |
| `useSortedClasses`        | warn (UI)            | Tailwind class sorting                  |
| `useFilenamingConvention` | kebab/camel/Pascal   | Flexible naming                         |
| `noVoid`                  | off                  | Useful for useEffect callbacks          |
| `useTemplate`             | off                  | Allow string concatenation              |

## Git Hooks Integration

### Lint-Staged Configuration

Standard pattern for pre-commit hooks:

```javascript
// .lintstagedrc.js
module.exports = {
  "*.{json,jsonc,ts,tsx}": "bun biome check --write",
  "*.{md,yml,yaml}": "bun prettier --cache --write",
  "*.{ts,tsx}": "bun biome check --write --only=correctness/noUnusedImports",
};
```

The separate `noUnusedImports` pass enforces import cleanup only at commit time, not during development.

## UI-Specific Configuration

For frontend projects with Tailwind CSS:

```jsonc
{
  "css": {
    "parser": {
      "tailwindDirectives": true
    }
  },
  "assist": {
    "actions": {
      "source": {
        "useSortedAttributes": "on"
      }
    }
  },
  "linter": {
    "rules": {
      "nursery": {
        "useSortedClasses": {
          "fix": "safe",
          "level": "warn",
          "options": {
            "attributes": ["classList"],
            "functions": ["clsx", "cva", "cn", "tv", "tw"]
          }
        }
      }
    }
  }
}
```

Biome `v2.4.0+` auto-enables CSS Modules parsing for `*.module.css`, so explicit
`"cssModules": true` is usually unnecessary unless your project needs non-standard behavior.

## Biome v2.4+ Notes

- `biome check` and `biome ci` now support `--only` and `--skip` for targeted rule/action runs.
- `biome check --write` now also applies formatting when applying fixes.
- Config lookup now also supports hidden files: `.biome.json` and `.biome.jsonc`.
- Config lookup now also supports user config directories (for example, `$HOME/.config/biome` on Linux/macOS equivalents).
- New formatter option `formatter.trailingNewline` can disable trailing newline insertion.
- HTML formatter behavior changed significantly in `v2.4.0`; expect larger diffs in HTML/Vue/Svelte/Astro if formatter support is enabled.

## Troubleshooting

### Common Issues

**"No files matched"**: Check `files.includes` patterns match your file structure.

**Conflicting rules**: Overrides are applied in order; later overrides take precedence.

**Schema errors**: Use local schema reference for IDE support:

```jsonc
"$schema": "./node_modules/@biomejs/biome/configuration_schema.json"
```

### Biome vs Prettier

Biome handles JS/TS/JSON/CSS formatting. Use Prettier for:

- Markdown (`.md`, `.mdx`)
- YAML (`.yml`, `.yaml`)

## Additional Resources

### Examples

Working examples in `./examples/`:

- **`./examples/base-config.jsonc`** - Minimal library configuration
- **`./examples/ui-config.jsonc`** - Frontend project with Tailwind
- **`./examples/lint-staged.js`** - Pre-commit hook configuration

### Full Documentation

For advanced features, migrations, or complete rule reference, consult the official Biome documentation via Context7 MCP:

```
Use context7 to fetch Biome documentation for [specific topic]
```

The official docs at biomejs.dev should be consulted as a last resort for features not covered here.
