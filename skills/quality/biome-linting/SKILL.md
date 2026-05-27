---
name: biome-linting
description: Use when applying Biome's linting capabilities, rule categories, and code quality enforcement to JavaScript/TypeScript projects.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Biome Linting

Expert knowledge of Biome's linting capabilities, rule categories, and code quality enforcement for JavaScript and TypeScript projects.

## Overview

Biome's linter provides fast, comprehensive code quality checks with a focus on correctness, performance, security, and best practices. It's designed to catch common bugs and enforce consistent code patterns.

## Core Commands

### Basic Linting

```bash
# Check files without fixing
biome check .

# Check and auto-fix
biome check --write .

# Check specific files
biome check src/**/*.ts

# CI mode (strict, fails on warnings)
biome ci .
```

### Command Options

```bash
# Verbose output
biome check --verbose .

# JSON output
biome check --json .

# Only lint (skip formatting)
biome lint .

# Apply safe fixes only
biome check --write --unsafe=false .
```

## Rule Categories

### Accessibility (a11y)

Rules for web accessibility and WCAG compliance:

```json
{
  "linter": {
    "rules": {
      "a11y": {
        "recommended": true,
        "noAccessKey": "error",
        "noAriaHiddenOnFocusable": "error",
        "noAutofocus": "warn",
        "noBlankTarget": "error",
        "noPositiveTabindex": "error",
        "useAltText": "error",
        "useAnchorContent": "error",
        "useButtonType": "error",
        "useValidAriaProps": "error"
      }
    }
  }
}
```

Common violations:

- Missing alt text on images
- Autofocus on form elements
- Positive tabindex values
- Links without content
- Invalid ARIA properties

### Complexity

Rules to reduce code complexity:

```json
{
  "linter": {
    "rules": {
      "complexity": {
        "recommended": true,
        "noBannedTypes": "error",
        "noExcessiveCognitiveComplexity": "warn",
        "noExtraBooleanCast": "error",
        "noMultipleSpacesInRegularExpressionLiterals": "error",
        "noUselessCatch": "error",
        "noUselessConstructor": "error",
        "noUselessEmptyExport": "error",
        "noUselessFragments": "error",
        "noUselessLabel": "error",
        "noUselessRename": "error",
        "noUselessSwitchCase": "error",
        "noWith": "error"
      }
    }
  }
}
```

### Correctness

Rules for code correctness and bug prevention:

```json
{
  "linter": {
    "rules": {
      "correctness": {
        "recommended": true,
        "noChildrenProp": "error",
        "noConstAssign": "error",
        "noConstantCondition": "error",
        "noConstructorReturn": "error",
        "noEmptyPattern": "error",
        "noGlobalObjectCalls": "error",
        "noInnerDeclarations": "error",
        "noInvalidConstructorSuper": "error",
        "noNewSymbol": "error",
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
      }
    }
  }
}
```

Critical rules:

- `noUndeclaredVariables`: Catch undeclared variables
- `noUnusedVariables`: Remove unused code
- `noConstAssign`: Prevent const reassignment
- `noUnreachable`: Detect unreachable code
- `useIsNan`: Use isNaN() for NaN checks

### Performance

Rules for performance optimization:

```json
{
  "linter": {
    "rules": {
      "performance": {
        "recommended": true,
        "noAccumulatingSpread": "warn",
        "noDelete": "error"
      }
    }
  }
}
```

### Security

Rules for security best practices:

```json
{
  "linter": {
    "rules": {
      "security": {
        "recommended": true,
        "noDangerouslySetInnerHtml": "error",
        "noDangerouslySetInnerHtmlWithChildren": "error",
        "noGlobalEval": "error"
      }
    }
  }
}
```

Critical security rules:

- Prevent XSS via innerHTML
- Block eval() usage
- Detect security vulnerabilities

### Style

Code style and consistency rules:

```json
{
  "linter": {
    "rules": {
      "style": {
        "recommended": true,
        "noArguments": "error",
        "noCommaOperator": "error",
        "noImplicitBoolean": "warn",
        "noNegationElse": "warn",
        "noNonNullAssertion": "warn",
        "noParameterAssign": "error",
        "noRestrictedGlobals": "error",
        "noShoutyConstants": "warn",
        "noUnusedTemplateLiteral": "error",
        "noVar": "error",
        "useBlockStatements": "warn",
        "useCollapsedElseIf": "warn",
        "useConst": "error",
        "useDefaultParameterLast": "error",
        "useEnumInitializers": "warn",
        "useExponentiationOperator": "error",
        "useFragmentSyntax": "error",
        "useNumericLiterals": "error",
        "useSelfClosingElements": "error",
        "useShorthandArrayType": "error",
        "useSingleVarDeclarator": "error",
        "useTemplate": "warn",
        "useWhile": "error"
      }
    }
  }
}
```

Key style rules:

- `noVar`: Use let/const instead of var
- `useConst`: Prefer const for immutable bindings
- `noNonNullAssertion`: Avoid ! assertions in TypeScript
- `useTemplate`: Prefer template literals

### Suspicious

Rules for suspicious code patterns:

```json
{
  "linter": {
    "rules": {
      "suspicious": {
        "recommended": true,
        "noArrayIndexKey": "warn",
        "noAssignInExpressions": "error",
        "noAsyncPromiseExecutor": "error",
        "noCatchAssign": "error",
        "noClassAssign": "error",
        "noCommentText": "error",
        "noCompareNegZero": "error",
        "noConsoleLog": "warn",
        "noControlCharactersInRegex": "error",
        "noDebugger": "error",
        "noDoubleEquals": "error",
        "noDuplicateCase": "error",
        "noDuplicateClassMembers": "error",
        "noDuplicateObjectKeys": "error",
        "noDuplicateParameters": "error",
        "noEmptyBlockStatements": "warn",
        "noExplicitAny": "warn",
        "noExtraNonNullAssertion": "error",
        "noFallthroughSwitchClause": "error",
        "noFunctionAssign": "error",
        "noGlobalAssign": "error",
        "noImportAssign": "error",
        "noLabelVar": "error",
        "noMisleadingCharacterClass": "error",
        "noPrototypeBuiltins": "error",
        "noRedeclare": "error",
        "noSelfCompare": "error",
        "noShadowRestrictedNames": "error",
        "noUnsafeNegation": "error",
        "useDefaultSwitchClauseLast": "error",
        "useGetterReturn": "error",
        "useValidTypeof": "error"
      }
    }
  }
}
```

Critical suspicious patterns:

- `noExplicitAny`: Avoid any in TypeScript
- `noConsoleLog`: Remove console.log in production
- `noDebugger`: Remove debugger statements
- `noDoubleEquals`: Use === instead of ==
- `noDuplicateObjectKeys`: Catch duplicate keys

## Rule Configuration Patterns

### Strict Configuration

Maximum strictness for high-quality codebases:

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "a11y": { "recommended": true },
      "complexity": { "recommended": true },
      "correctness": { "recommended": true },
      "performance": { "recommended": true },
      "security": { "recommended": true },
      "style": { "recommended": true },
      "suspicious": {
        "recommended": true,
        "noExplicitAny": "error",
        "noConsoleLog": "error"
      }
    }
  }
}
```

### Gradual Adoption

Start lenient and progressively tighten:

```json
{
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "suspicious": {
        "noExplicitAny": "warn",
        "noConsoleLog": "warn"
      },
      "style": {
        "noVar": "error",
        "useConst": "warn"
      }
    }
  }
}
```

### Framework-Specific

React configuration example:

```json
{
  "linter": {
    "rules": {
      "recommended": true,
      "a11y": { "recommended": true },
      "correctness": {
        "recommended": true,
        "noChildrenProp": "error"
      },
      "security": {
        "noDangerouslySetInnerHtml": "error"
      },
      "suspicious": {
        "noArrayIndexKey": "error"
      }
    }
  }
}
```

## Ignoring Violations

### Inline Comments

Suppress specific violations:

```javascript
// biome-ignore lint/suspicious/noExplicitAny: Legacy code
function legacyFunction(data: any) {
  return data;
}

// biome-ignore lint/suspicious/noConsoleLog: Debug logging
console.log('Debug info');

// Multiple rules
// biome-ignore lint/suspicious/noExplicitAny lint/style/useConst: Migration
var config: any = {};
```

### File-Level Ignores

Ignore entire file:

```javascript
/* biome-ignore-file */

// Legacy file, skip all linting
```

### Configuration Ignores

Ignore patterns in biome.json:

```json
{
  "files": {
    "ignore": [
      "**/generated/**",
      "**/*.config.js",
      "**/vendor/**"
    ]
  }
}
```

## Best Practices

1. **Enable Recommended Rules** - Start with `"recommended": true`
2. **Progressive Enhancement** - Add stricter rules gradually
3. **Document Exceptions** - Explain why rules are disabled
4. **Use Inline Ignores Sparingly** - Prefer fixing over ignoring
5. **Security First** - Never disable security rules
6. **CI Enforcement** - Use `biome ci` in pipelines
7. **Pre-commit Hooks** - Catch issues before commit
8. **Team Agreement** - Discuss rule changes with team
9. **Regular Review** - Periodically review disabled rules
10. **Fix Warnings** - Don't let warnings accumulate

## Common Pitfalls

1. **Ignoring Errors** - Using biome-ignore instead of fixing
2. **Disabling Security** - Turning off security rules
3. **No CI Check** - Not enforcing in continuous integration
4. **Too Lenient** - Setting everything to "warn"
5. **No Documentation** - Not explaining disabled rules
6. **Inconsistent Config** - Different rules per package
7. **Ignoring Warnings** - Treating warnings as optional
8. **Wrong Rule Names** - Typos in rule configuration
9. **Overly Strict** - Blocking team productivity
10. **No Migration Plan** - Enabling all rules at once

## Advanced Topics

### Custom Rule Sets

Create shared rule sets for organization:

```json
{
  "extends": ["@company/biome-config"],
  "linter": {
    "rules": {
      "suspicious": {
        "noConsoleLog": "error"
      }
    }
  }
}
```

### Per-Directory Rules

Use overrides for different code areas:

```json
{
  "overrides": [
    {
      "include": ["src/**/*.ts"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "error"
          }
        }
      }
    },
    {
      "include": ["scripts/**/*.js"],
      "linter": {
        "rules": {
          "suspicious": {
            "noConsoleLog": "off"
          }
        }
      }
    }
  ]
}
```

### Migration Strategy

Migrating from ESLint:

1. **Install Biome**: `npm install -D @biomejs/biome`
2. **Initialize**: `npx biome init`
3. **Run Check**: `npx biome check .` to see violations
4. **Fix Automatically**: `npx biome check --write .`
5. **Address Remaining**: Fix issues that can't auto-fix
6. **Tune Rules**: Adjust rules based on team needs
7. **Update CI**: Replace ESLint with Biome
8. **Remove ESLint**: After validation period

## Integration Patterns

### Package.json Scripts

```json
{
  "scripts": {
    "lint": "biome check .",
    "lint:fix": "biome check --write .",
    "lint:ci": "biome ci ."
  }
}
```

### Pre-commit Hook

Using husky:

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "biome check --write --changed"
    }
  }
}
```

### GitHub Actions

```yaml
- name: Run Biome
  run: npx biome ci .
```

## Troubleshooting

### False Positives

If rule triggers incorrectly:

1. Verify rule is appropriate for your code
2. Check if bug in Biome (report upstream)
3. Use biome-ignore with explanation
4. Consider disabling rule if widespread

### Performance Issues

If linting is slow:

1. Update to latest Biome version
2. Use VCS integration
3. Ignore large generated directories
4. Check for file pattern issues

### Rules Not Applied

Verify:

1. Linter is enabled in config
2. Rule category is enabled
3. Rule name is spelled correctly
4. No overrides disabling it
5. Files are not ignored

## When to Use This Skill

- Setting up linting for new projects
- Migrating from ESLint to Biome
- Configuring rule sets for teams
- Troubleshooting linting errors
- Optimizing code quality checks
- Establishing code standards
- Training team on Biome linting
- Integrating linting into CI/CD
