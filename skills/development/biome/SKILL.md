---
name: biome
description: Biome 2.x linting and formatting patterns. Use when configuring code quality tools, setting up linting rules, formatting code, or integrating with CI/CD. Covers migration from ESLint/Prettier.
---

# Biome 2.x

## Overview

Fast, all-in-one toolchain for linting and formatting JavaScript, TypeScript, JSX, and JSON. Biome 2.x replaces ESLint and Prettier with a single, performant tool written in Rust.

**Install**: `pnpm add -D @biomejs/biome`

**Version**: 2.x (use `biome --version` to verify)

## Workflows

**Initial setup:**
1. [ ] Install Biome: `pnpm add -D @biomejs/biome`
2. [ ] Initialize config: `pnpm biome init`
3. [ ] Configure biome.json with project standards
4. [ ] Install VS Code extension: `biomejs.biome`
5. [ ] Add npm scripts to package.json
6. [ ] Test: `pnpm biome check .`

**Migrating from ESLint/Prettier:**
1. [ ] Run migration helper: `pnpm biome migrate eslint --write`
2. [ ] Review generated biome.json
3. [ ] Remove ESLint/Prettier configs and dependencies
4. [ ] Update pre-commit hooks and CI scripts
5. [ ] Run full check: `pnpm biome check --write .`

**Daily usage:**
1. [ ] Format on save (VS Code integration)
2. [ ] Run `pnpm biome check .` before commits
3. [ ] Fix auto-fixable issues: `pnpm biome check --write .`
4. [ ] Review manual fixes for remaining issues

## Configuration

### biome.json Structure

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "always",
      "trailingCommas": "es5",
      "arrowParentheses": "asNeeded"
    }
  },
  "files": {
    "ignore": [
      "dist",
      "build",
      "node_modules",
      "*.min.js",
      "coverage"
    ]
  }
}
```

### Common Configurations

```json
// Strict TypeScript project
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "error",
        "noImplicitAnyLet": "error"
      },
      "complexity": {
        "noExcessiveCognitiveComplexity": "warn",
        "noUselessFragments": "error"
      },
      "style": {
        "noNonNullAssertion": "warn",
        "useConst": "error",
        "useImportType": "error"
      }
    }
  }
}

// React project
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "a11y": {
        "noBlankTarget": "error",
        "useAltText": "error",
        "useButtonType": "error"
      },
      "correctness": {
        "useExhaustiveDependencies": "warn",
        "useHookAtTopLevel": "error"
      }
    }
  },
  "javascript": {
    "formatter": {
      "jsxQuoteStyle": "double",
      "quoteStyle": "single"
    }
  }
}

// Relaxed formatting (Prettier-like)
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 80
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "semicolons": "always",
      "trailingCommas": "all",
      "arrowParentheses": "always"
    }
  }
}
```

### Rule Categories

```json
{
  "linter": {
    "rules": {
      // Enable all recommended rules
      "recommended": true,

      // Accessibility
      "a11y": {
        "noBlankTarget": "error",
        "useAltText": "error"
      },

      // Code complexity
      "complexity": {
        "noExcessiveCognitiveComplexity": "warn",
        "noBannedTypes": "error"
      },

      // Correctness
      "correctness": {
        "noUnusedVariables": "error",
        "useExhaustiveDependencies": "warn"
      },

      // Performance
      "performance": {
        "noAccumulatingSpread": "warn",
        "noDelete": "error"
      },

      // Security
      "security": {
        "noDangerouslySetInnerHtml": "warn"
      },

      // Style
      "style": {
        "noNonNullAssertion": "warn",
        "useConst": "error",
        "useSingleVarDeclarator": "error"
      },

      // Suspicious patterns
      "suspicious": {
        "noExplicitAny": "error",
        "noDebugger": "error",
        "noConsoleLog": "warn"
      }
    }
  }
}
```

## CLI Commands

### Check (Lint + Format)

```bash
# Check all files
pnpm biome check .

# Check and auto-fix
pnpm biome check --write .

# Check specific files
pnpm biome check src/components/*.tsx

# Check with specific configurations
pnpm biome check --formatter-enabled=false .
pnpm biome check --linter-enabled=false .

# Dry run (show what would change)
pnpm biome check --write --dry-run .
```

### Lint Only

```bash
# Lint all files
pnpm biome lint .

# Lint and auto-fix
pnpm biome lint --write .

# Show applied fixes
pnpm biome lint --write --verbose .

# Lint with specific rules
pnpm biome lint --only=suspicious/noExplicitAny .
```

### Format Only

```bash
# Format all files
pnpm biome format .

# Format and write changes
pnpm biome format --write .

# Format with custom line width
pnpm biome format --line-width=120 .

# Format specific file types
pnpm biome format --json-formatter-enabled=true .
```

### Other Commands

```bash
# Initialize configuration
pnpm biome init

# Migrate from ESLint
pnpm biome migrate eslint --write

# Migrate from Prettier
pnpm biome migrate prettier --write

# Print configuration
pnpm biome rage

# Print effective configuration for a file
pnpm biome explain src/App.tsx

# Check configuration validity
pnpm biome check --config-path=./biome.json
```

## Package.json Scripts

```json
{
  "scripts": {
    "lint": "biome lint .",
    "format": "biome format --write .",
    "check": "biome check .",
    "fix": "biome check --write .",
    "typecheck": "tsc --noEmit",
    "quality": "pnpm lint && pnpm typecheck && pnpm build"
  }
}
```

## VS Code Integration

### settings.json

```json
{
  // Enable Biome as default formatter
  "editor.defaultFormatter": "biomejs.biome",

  // Format on save
  "editor.formatOnSave": true,

  // Organize imports on save
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  },

  // Disable conflicting extensions
  "eslint.enable": false,
  "prettier.enable": false,

  // File associations
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[json]": {
    "editor.defaultFormatter": "biomejs.biome"
  }
}
```

### Workspace Settings

```json
{
  "biome.lspBin": "./node_modules/@biomejs/biome/bin/biome",
  "biome.enabled": true,
  "biome.rename": true
}
```

## Ignoring Files

### Via biome.json

```json
{
  "files": {
    "ignore": [
      // Build outputs
      "dist",
      "build",
      "out",
      ".next",

      // Dependencies
      "node_modules",
      "vendor",

      // Generated files
      "*.generated.ts",
      "**/*.min.js",

      // Coverage
      "coverage",
      ".nyc_output",

      // Temp files
      "tmp",
      "temp"
    ],
    "include": [
      "src/**/*.ts",
      "src/**/*.tsx"
    ]
  }
}
```

### Via Comments

```typescript
// biome-ignore lint/suspicious/noExplicitAny: legacy code
function legacy(param: any) {
  return param;
}

// biome-ignore format: preserve formatting
const matrix = [
  1, 0, 0,
  0, 1, 0,
  0, 0, 1
];

// Multiple ignores
// biome-ignore lint/complexity/noExcessiveCognitiveComplexity: complex business logic
// biome-ignore lint/suspicious/noConsoleLog: debugging required
function complexFunction() {
  console.log('Debug info');
  // ... complex logic
}
```

### Per-File Configuration

```json
{
  "overrides": [
    {
      "include": ["tests/**/*.ts"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "off"
          }
        }
      }
    },
    {
      "include": ["scripts/**/*.js"],
      "formatter": {
        "lineWidth": 120
      }
    }
  ]
}
```

## Git Hooks Integration

### Using Husky + lint-staged

```bash
# Install dependencies
pnpm add -D husky lint-staged

# Initialize Husky
pnpm husky init
```

**.husky/pre-commit**
```bash
#!/usr/bin/env sh
pnpm lint-staged
```

**package.json**
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx,json}": [
      "biome check --write --no-errors-on-unmatched"
    ]
  }
}
```

### Using Lefthook

**lefthook.yml**
```yaml
pre-commit:
  parallel: true
  commands:
    biome:
      glob: "*.{js,ts,jsx,tsx,json}"
      run: biome check --write --no-errors-on-unmatched {staged_files}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v4
        with:
          version: 10

      - uses: actions/setup-node@v4
        with:
          node-version: '24'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run Biome
        run: pnpm biome check .

      - name: Type check
        run: pnpm typecheck
```

### GitLab CI

```yaml
quality:
  image: node:24
  cache:
    paths:
      - node_modules/
  before_script:
    - npm install -g pnpm
    - pnpm install --frozen-lockfile
  script:
    - pnpm biome check .
    - pnpm typecheck
  only:
    - merge_requests
    - main
```

### Docker

```dockerfile
FROM node:24-alpine

WORKDIR /app

# Install pnpm
RUN npm install -g pnpm

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy source
COPY . .

# Run checks
RUN pnpm biome check .
RUN pnpm typecheck
RUN pnpm build
```

## Migration from ESLint/Prettier

### Step-by-Step Migration

```bash
# 1. Install Biome
pnpm add -D @biomejs/biome

# 2. Run migration (reads .eslintrc/.prettierrc)
pnpm biome migrate eslint --write
pnpm biome migrate prettier --write

# 3. Review generated biome.json
cat biome.json

# 4. Remove old configs
rm .eslintrc.json .prettierrc.json .eslintignore .prettierignore

# 5. Remove old dependencies
pnpm remove eslint prettier \
  @typescript-eslint/parser \
  @typescript-eslint/eslint-plugin \
  eslint-config-prettier \
  eslint-plugin-react

# 6. Update package.json scripts
# Replace "eslint ." with "biome lint ."
# Replace "prettier --write ." with "biome format --write ."

# 7. Update pre-commit hooks
# Replace eslint/prettier with biome check --write

# 8. Update CI/CD
# Replace eslint/prettier commands with biome check

# 9. Update VS Code settings
# Disable ESLint/Prettier extensions
# Enable Biome extension

# 10. Run full check
pnpm biome check --write .
```

### ESLint Rule Equivalents

| ESLint Rule | Biome Rule |
|-------------|------------|
| `no-unused-vars` | `correctness/noUnusedVariables` |
| `@typescript-eslint/no-explicit-any` | `suspicious/noExplicitAny` |
| `react-hooks/exhaustive-deps` | `correctness/useExhaustiveDependencies` |
| `no-console` | `suspicious/noConsoleLog` |
| `prefer-const` | `style/useConst` |
| `no-var` | `style/noVar` |
| `jsx-a11y/alt-text` | `a11y/useAltText` |
| `react/jsx-no-target-blank` | `a11y/noBlankTarget` |

## Best Practices

- **Use recommended ruleset** as baseline, then customize specific rules
- **Enable format-on-save** in VS Code for seamless workflow
- **Run check before commits** using git hooks (Husky/Lefthook)
- **Use biome check** (not lint + format separately) for unified workflow
- **Ignore generated files** in biome.json, not inline comments
- **Use overrides** for different rules in tests vs source
- **Commit biome.json** to version control for team consistency
- **Document custom rules** in comments explaining why they're needed
- **Leverage --write** for auto-fixing in CI (with separate review step)
- **Use biome explain** to understand why a file fails checks

## Anti-Patterns

- ❌ Running lint and format separately (use `check` instead)
- ❌ Disabling recommended rules without justification
- ❌ Using biome-ignore excessively (fix the underlying issue)
- ❌ Not committing biome.json to version control
- ❌ Mixing ESLint and Biome in the same project
- ❌ Ignoring files via comments instead of configuration
- ❌ Not testing migration thoroughly before removing ESLint/Prettier
- ❌ Skipping pre-commit hooks for "quick fixes"
- ❌ Using outdated schema version in biome.json
- ❌ Not organizing imports (disable organizeImports)

## Feedback Loops

**Check formatting:**
```bash
# See what would change without modifying files
pnpm biome format --write --dry-run .
```

**Validate configuration:**
```bash
# Print effective config and diagnostics
pnpm biome rage

# Explain rules for specific file
pnpm biome explain src/App.tsx
```

**Performance benchmark:**
```bash
# Compare Biome vs ESLint/Prettier speed
time pnpm biome check .
time pnpm eslint . && pnpm prettier --check .
# Biome typically 10-100x faster
```

**CI integration test:**
```bash
# Test CI checks locally
pnpm biome check . --error-on-warnings
echo $? # Should be 0 for success
```

**Editor integration:**
```
# Verify VS Code extension is active
# Open Command Palette → "Biome: Show Output Channel"
# Should show Biome LSP server logs
```
