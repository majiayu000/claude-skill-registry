---
name: biome-configuration
description: Use when biome configuration including biome.json setup, schema versions, VCS integration, and project organization.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Biome Configuration

Master Biome configuration including biome.json setup, schema versions, VCS integration, and project organization for optimal JavaScript/TypeScript tooling.

## Overview

Biome is a fast, modern toolchain for JavaScript and TypeScript projects that combines linting and formatting in a single tool. It's designed as a performant alternative to ESLint and Prettier, written in Rust for maximum speed.

## Installation and Setup

### Basic Installation

Install Biome in your project:

```bash
npm install --save-dev @biomejs/biome
# or
pnpm add -D @biomejs/biome
# or
yarn add -D @biomejs/biome
```

### Initialize Configuration

Create a basic biome.json configuration:

```bash
npx biome init
```

This creates a `biome.json` file in your project root.

## Configuration File Structure

### Basic biome.json

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": []
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 80
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "es5"
    }
  }
}
```

### Schema Versioning

Always use the correct schema version matching your Biome installation:

```bash
# Check Biome version
npx biome --version

# Migrate configuration to current version
npx biome migrate --write
```

The `$schema` field enables IDE autocomplete and validation:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.6/schema.json"
}
```

### VCS Integration

Configure version control integration to respect .gitignore:

```json
{
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true,
    "defaultBranch": "main"
  }
}
```

Options:

- `enabled`: Enable VCS integration
- `clientKind`: "git" for Git repositories
- `useIgnoreFile`: Respect .gitignore patterns
- `defaultBranch`: Default branch name for operations

## File Management

### File Patterns

Control which files Biome processes:

```json
{
  "files": {
    "ignoreUnknown": false,
    "ignore": [
      "**/node_modules/**",
      "**/dist/**",
      "**/.next/**",
      "**/build/**",
      "**/.cache/**"
    ],
    "include": ["src/**/*.ts", "src/**/*.tsx"]
  }
}
```

### Common Ignore Patterns

```json
{
  "files": {
    "ignore": [
      "**/node_modules/",
      "**/dist/",
      "**/build/",
      "**/.next/",
      "**/.cache/",
      "**/coverage/",
      "**/*.min.js",
      "**/*.log"
    ]
  }
}
```

## Formatter Configuration

### Basic Formatter Settings

```json
{
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineEnding": "lf",
    "lineWidth": 80
  }
}
```

Options:

- `enabled`: Enable/disable formatter
- `formatWithErrors`: Format even with syntax errors
- `indentStyle`: "space" or "tab"
- `indentWidth`: Number of spaces (2 or 4 recommended)
- `lineEnding`: "lf", "crlf", or "cr"
- `lineWidth`: Maximum line length

### Language-Specific Formatting

#### JavaScript/TypeScript

```json
{
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "quoteProperties": "asNeeded",
      "trailingCommas": "all",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSpacing": true,
      "bracketSameLine": false
    }
  }
}
```

#### JSON

```json
{
  "json": {
    "formatter": {
      "enabled": true,
      "indentStyle": "space",
      "indentWidth": 2,
      "lineWidth": 80,
      "trailingCommas": "none"
    }
  }
}
```

## Linter Configuration

### Enable Recommended Rules

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

### Rule Categories

Configure specific rule groups:

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "a11y": {
        "recommended": true
      },
      "complexity": {
        "recommended": true
      },
      "correctness": {
        "recommended": true
      },
      "performance": {
        "recommended": true
      },
      "security": {
        "recommended": true
      },
      "style": {
        "recommended": true
      },
      "suspicious": {
        "recommended": true
      }
    }
  }
}
```

### Fine-Grained Rule Control

Enable or disable specific rules:

```json
{
  "linter": {
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "error",
        "noConsoleLog": "warn"
      },
      "style": {
        "useConst": "error",
        "noVar": "error"
      }
    }
  }
}
```

Rule levels:

- `"off"`: Disable rule
- `"warn"`: Show warning
- `"error"`: Fail check

## Monorepo Configuration

### Root Configuration

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.6/schema.json",
  "extends": [],
  "files": {
    "ignore": ["**/node_modules/", "**/dist/"]
  },
  "formatter": {
    "enabled": true,
    "indentWidth": 2
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

### Package-Specific Overrides

Each package can have its own biome.json:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.3.6/schema.json",
  "extends": ["../../biome.json"],
  "linter": {
    "rules": {
      "suspicious": {
        "noConsoleLog": "off"
      }
    }
  }
}
```

## Best Practices

1. **Use Schema URLs** - Always include `$schema` for IDE support
2. **Version Management** - Run `biome migrate` after updates
3. **VCS Integration** - Enable VCS to respect .gitignore
4. **Consistent Formatting** - Set clear formatter rules across team
5. **Rule Documentation** - Document why specific rules are disabled
6. **Monorepo Strategy** - Use extends for shared configuration
7. **CI Integration** - Run `biome ci` in continuous integration
8. **Pre-commit Hooks** - Validate code before commits
9. **Editor Integration** - Install Biome VSCode/IDE extensions
10. **Regular Updates** - Keep Biome updated for new features

## Common Pitfalls

1. **Schema Mismatch** - Using outdated schema version
2. **Missing Migration** - Not running migrate after updates
3. **Overly Strict** - Enabling all rules without team agreement
4. **No VCS Integration** - Not respecting gitignore patterns
5. **Inconsistent Config** - Different settings across packages
6. **Ignored Warnings** - Dismissing warnings that indicate issues
7. **No Editor Setup** - Missing IDE integration for real-time feedback
8. **Large Line Width** - Setting lineWidth too high reduces readability
9. **Mixed Quotes** - Not enforcing consistent quote style
10. **No CI Enforcement** - Not running checks in CI pipeline

## Advanced Topics

### Overrides Per Path

```json
{
  "overrides": [
    {
      "include": ["scripts/**/*.js"],
      "linter": {
        "rules": {
          "suspicious": {
            "noConsoleLog": "off"
          }
        }
      }
    },
    {
      "include": ["**/*.test.ts"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "off"
          }
        }
      }
    }
  ]
}
```

### Custom Scripts

Add to package.json:

```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write .",
    "ci": "biome ci ."
  }
}
```

### CI/CD Integration

```bash
# CI mode (fails on warnings)
biome ci .

# Check without fixing
biome check .

# Fix automatically
biome check --write .

# Format only
biome format --write .
```

## When to Use This Skill

- Setting up Biome in new projects
- Migrating from ESLint/Prettier to Biome
- Configuring Biome for monorepos
- Customizing linting and formatting rules
- Troubleshooting Biome configuration issues
- Integrating Biome with CI/CD pipelines
- Establishing team code standards
- Optimizing Biome performance

## Troubleshooting

### Schema Version Mismatch

```bash
# Error: Schema version doesn't match CLI version
npx biome migrate --write
```

### Files Not Being Checked

Check:

1. VCS integration and .gitignore
2. `files.ignore` patterns
3. `files.include` if specified
4. File extensions supported by Biome

### Rules Not Applying

Verify:

1. `linter.enabled` is true
2. Rule category is enabled
3. Rule name is correct
4. No overrides disabling the rule

### Performance Issues

Optimize:

1. Use `files.ignore` for large directories
2. Enable VCS integration
3. Exclude generated files
4. Update to latest Biome version
