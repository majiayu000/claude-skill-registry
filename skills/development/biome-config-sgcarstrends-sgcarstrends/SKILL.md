---
name: biome-config
description: Update Biome linting rules, formatting configs, and import organization settings. Use when adding new lint rules, customizing code style, or fixing workspace-specific linting issues.
allowed-tools: Read, Edit, Bash, Grep, Glob
---

# Biome Configuration Skill

This skill helps you configure and customize Biome for linting and formatting across the monorepo.

## When to Use This Skill

- Adding new linting rules
- Customizing code formatting
- Configuring import organization
- Fixing linting errors across the codebase
- Setting up workspace-specific rules
- Debugging Biome configuration issues
- Migrating from ESLint/Prettier

## Biome Overview

Biome is an all-in-one toolchain for web projects that provides:
- **Linting**: Fast, opinionated linting
- **Formatting**: Consistent code formatting
- **Import Organization**: Automatic import sorting

The project uses Biome instead of ESLint and Prettier for better performance.

## Configuration Structure

```
sgcarstrends/
├── biome.json                 # Root Biome config
├── apps/
│   ├── api/
│   │   └── biome.json        # API-specific config (extends root)
│   └── web/
│       └── biome.json        # Web-specific config (extends root)
└── packages/
    └── database/
        └── biome.json        # Database-specific config
```

## Root Configuration

```json
// biome.json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true,
    "defaultBranch": "main"
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": [
      "node_modules",
      "dist",
      "build",
      ".next",
      ".turbo",
      "coverage",
      ".sst"
    ]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf"
  },
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "complexity": {
        "noExtraBooleanCast": "error",
        "noMultipleSpacesInRegularExpressionLiterals": "error",
        "noUselessCatch": "error",
        "noUselessConstructor": "error",
        "noUselessEmptyExport": "error",
        "noWith": "error"
      },
      "correctness": {
        "noConstAssign": "error",
        "noConstantCondition": "error",
        "noEmptyCharacterClassInRegex": "error",
        "noEmptyPattern": "error",
        "noGlobalObjectCalls": "error",
        "noInvalidConstructorSuper": "error",
        "noInvalidNewBuiltin": "error",
        "noNonoctalDecimalEscape": "error",
        "noPrecisionLoss": "error",
        "noSelfAssign": "error",
        "noSetterReturn": "error",
        "noSwitchDeclarations": "error",
        "noUndeclaredVariables": "error",
        "noUnreachable": "error",
        "noUnreachableSuper": "error",
        "noUnsafeFinally": "error",
        "noUnsafeOptionalChaining": "error",
        "noUnusedLabels": "error",
        "noUnusedVariables": "error",
        "useIsNan": "error",
        "useValidForDirection": "error",
        "useYield": "error"
      },
      "security": {
        "noDangerouslySetInnerHtml": "error",
        "noDangerouslySetInnerHtmlWithChildren": "error"
      },
      "style": {
        "noArguments": "error",
        "noVar": "error",
        "useConst": "error",
        "useTemplate": "error"
      },
      "suspicious": {
        "noAsyncPromiseExecutor": "error",
        "noCatchAssign": "error",
        "noClassAssign": "error",
        "noCommentText": "error",
        "noCompareNegZero": "error",
        "noDebugger": "error",
        "noDoubleEquals": "error",
        "noDuplicateCase": "error",
        "noDuplicateClassMembers": "error",
        "noDuplicateObjectKeys": "error",
        "noDuplicateParameters": "error",
        "noEmptyBlockStatements": "error",
        "noExplicitAny": "warn",
        "noExtraNonNullAssertion": "error",
        "noFallthroughSwitchClause": "error",
        "noFunctionAssign": "error",
        "noGlobalAssign": "error",
        "noImportAssign": "error",
        "noMisleadingCharacterClass": "error",
        "noMisleadingInstantiator": "error",
        "noPrototypeBuiltins": "error",
        "noRedeclare": "error",
        "noShadowRestrictedNames": "error",
        "noUnsafeDeclarationMerging": "error",
        "noUnsafeNegation": "error",
        "useGetterReturn": "error",
        "useValidTypeof": "error"
      }
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "double",
      "jsxQuoteStyle": "double",
      "quoteProperties": "asNeeded",
      "trailingCommas": "es5",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSpacing": true,
      "bracketSameLine": false
    }
  }
}
```

## Workspace-Specific Configuration

### Apps Configuration

```json
// apps/web/biome.json
{
  "extends": ["../../biome.json"],
  "linter": {
    "rules": {
      "suspicious": {
        "noExplicitAny": "off"  // Allow 'any' in web app for flexibility
      }
    }
  }
}
```

### Test Files Configuration

```json
// Override for test files (if needed)
{
  "overrides": [
    {
      "include": ["**/__tests__/**", "**/*.test.ts", "**/*.spec.ts"],
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

## Common Commands

### Check Code

```bash
# Check all files
pnpm biome check .

# Check specific directory
pnpm biome check apps/web

# Check and apply safe fixes
pnpm biome check --write .

# Check only linting
pnpm biome lint .

# Check only formatting
pnpm biome format .
```

### Format Code

```bash
# Format all files
pnpm biome format --write .

# Format specific files
pnpm biome format --write apps/web/src/**/*.ts

# Check formatting without writing
pnpm biome format .
```

### Organize Imports

```bash
# Organize imports
pnpm biome check --organize-imports-enabled=true --write .
```

### CI Mode

```bash
# Check without modifying files (for CI)
pnpm biome ci .
```

## Linting Rules

### Enabling/Disabling Rules

**Disable a rule globally:**
```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "noExplicitAny": "off"
      }
    }
  }
}
```

**Change severity:**
```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "noExplicitAny": "warn"  // error, warn, off
      }
    }
  }
}
```

**Disable inline:**
```typescript
// biome-ignore lint/suspicious/noExplicitAny: Legacy code needs refactoring
function legacy(data: any) {
  // ...
}
```

**Disable for entire file:**
```typescript
/* biome-ignore lint/suspicious/noExplicitAny: Test file */
```

### Recommended Rules

**Enable all recommended:**
```json
{
  "linter": {
    "rules": {
      "recommended": true
    }
  }
}
```

**Enable specific categories:**
```json
{
  "linter": {
    "rules": {
      "recommended": false,
      "correctness": {
        "recommended": true
      },
      "security": {
        "recommended": true
      },
      "performance": {
        "recommended": true
      }
    }
  }
}
```

## Formatting Configuration

### JavaScript/TypeScript

```json
{
  "javascript": {
    "formatter": {
      "quoteStyle": "double",           // "single" or "double"
      "jsxQuoteStyle": "double",
      "quoteProperties": "asNeeded",    // "asNeeded" or "preserve"
      "trailingCommas": "es5",          // "none", "es5", or "all"
      "semicolons": "always",           // "always" or "asNeeded"
      "arrowParentheses": "always",     // "always" or "asNeeded"
      "bracketSpacing": true,
      "bracketSameLine": false
    }
  }
}
```

### Line Width and Indentation

```json
{
  "formatter": {
    "indentStyle": "space",    // "space" or "tab"
    "indentWidth": 2,          // Number of spaces
    "lineWidth": 100,          // Max line length
    "lineEnding": "lf"         // "lf", "crlf", or "cr"
  }
}
```

## Import Organization

### Configuration

```json
{
  "organizeImports": {
    "enabled": true
  }
}
```

### Import Groups

Biome automatically organizes imports into groups:
1. Built-in modules (e.g., `fs`, `path`)
2. External modules (e.g., `react`, `next`)
3. Internal modules (e.g., `@/components`, `~/utils`)
4. Relative imports (e.g., `./utils`, `../types`)

Example:
```typescript
// Before
import { Button } from "./components/button";
import { useState } from "react";
import path from "path";
import { db } from "@/lib/db";

// After
import path from "path";

import { useState } from "react";

import { db } from "@/lib/db";

import { Button } from "./components/button";
```

## Git Integration

### Git Hooks with Husky

Biome integrates with git hooks:

```json
// .husky/pre-commit
pnpm biome check --write --staged
```

### Git-Aware Processing

```json
{
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true,     // Respect .gitignore
    "defaultBranch": "main"
  }
}
```

## Ignoring Files

### Via Configuration

```json
{
  "files": {
    "ignore": [
      "node_modules",
      "dist",
      "build",
      ".next",
      ".turbo",
      "coverage",
      ".sst",
      "**/*.config.js",
      "migrations/**"
    ]
  }
}
```

### Via .gitignore

With `useIgnoreFile: true`, Biome respects `.gitignore`.

### Inline Ignore

```typescript
// biome-ignore format: Auto-generated code
const generated = "...";
```

## Package.json Scripts

```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "format": "biome format --write .",
    "format:check": "biome format .",
    "biome:ci": "biome ci ."
  }
}
```

## VS Code Integration

### Install Extension

1. Install "Biome" extension
2. Configure as default formatter

### Settings

```json
// .vscode/settings.json
{
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  },
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  },
  "[javascriptreact]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  },
  "[json]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  },
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  }
}
```

## Migration from ESLint/Prettier

### 1. Remove Old Tools

```bash
# Remove ESLint
pnpm remove -r eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Remove Prettier
pnpm remove -r prettier

# Remove config files
rm .eslintrc.json .prettierrc .prettierignore
```

### 2. Install Biome

```bash
# Already installed in project
pnpm add -D -w @biomejs/biome
```

### 3. Migrate Configuration

Convert ESLint rules to Biome:
- Check Biome documentation for equivalent rules
- Some rules may not have direct equivalents
- Use `biome migrate eslint` for automated migration

```bash
npx @biomejs/biome migrate eslint --write
```

### 4. Update Scripts

Replace in `package.json`:
```json
{
  "scripts": {
    "lint": "biome check .",      // was: eslint .
    "format": "biome format --write ."  // was: prettier --write .
  }
}
```

## Troubleshooting

### Rule Conflicts

**Issue**: Rule seems to contradict another
**Solution**: Check rule documentation, disable one if needed

### Performance Issues

**Issue**: Biome is slow on large codebase
**Solutions**:
1. Check `files.ignore` is properly set
2. Run on specific directories
3. Use `--max-diagnostics` to limit output

### Format Not Applied

**Issue**: Files not formatting on save
**Solutions**:
1. Check VS Code extension is installed
2. Verify `editor.defaultFormatter` is set to Biome
3. Check `biome.json` is in workspace root

### Import Organization Not Working

**Issue**: Imports not organizing
**Solutions**:
1. Verify `organizeImports.enabled: true`
2. Run explicitly: `biome check --organize-imports-enabled=true --write .`
3. Check for syntax errors in file

## Advanced Configuration

### Per-File Overrides

```json
{
  "overrides": [
    {
      "include": ["**/*.config.ts"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "off"
          }
        }
      }
    },
    {
      "include": ["apps/api/**/*.ts"],
      "formatter": {
        "lineWidth": 120
      }
    }
  ]
}
```

### Custom Rule Severity

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "noUnusedVariables": "error"
      },
      "style": {
        "useConst": "warn"
      },
      "suspicious": {
        "noExplicitAny": "off"
      }
    }
  }
}
```

## CI Integration

### GitHub Actions

```yaml
# .github/workflows/lint.yml
name: Lint

on: [push, pull_request]

jobs:
  biome:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"
      - run: pnpm install
      - run: pnpm biome ci .
```

## References

- Biome Documentation: https://biomejs.dev
- Migration Guide: https://biomejs.dev/guides/migrate-eslint-prettier
- Rules Reference: https://biomejs.dev/linter/rules
- Related files:
  - `biome.json` - Root configuration
  - Root CLAUDE.md - Code style guidelines

## Best Practices

1. **Use Root Config**: Define common rules in root `biome.json`
2. **Extend in Workspaces**: Extend root config for workspace-specific rules
3. **Git Integration**: Enable VCS integration for `.gitignore` support
4. **Pre-commit Hooks**: Run Biome on staged files
5. **CI Checks**: Use `biome ci` in continuous integration
6. **Inline Ignores**: Use sparingly and with clear comments
7. **Consistent Formatting**: Apply formatting across entire codebase
8. **Regular Updates**: Keep Biome updated for new rules and fixes
