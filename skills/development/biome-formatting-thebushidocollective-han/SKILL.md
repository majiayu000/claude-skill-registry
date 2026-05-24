---
name: biome-formatting
description: Use when formatting JavaScript/TypeScript code with Biome's fast formatter including patterns, options, and code style management.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Biome Formatting

Master Biome's fast code formatter for JavaScript, TypeScript, JSON, and other supported languages with consistent style enforcement.

## Overview

Biome's formatter provides opinionated, fast code formatting similar to Prettier but with better performance. It's written in Rust and designed to format code consistently across teams.

## Core Commands

### Basic Formatting

```bash
# Format files and write changes
biome format --write .

# Format specific files
biome format --write src/**/*.ts

# Check formatting without fixing
biome format .

# Format stdin
echo "const x={a:1}" | biome format --stdin-file-path="example.js"
```

### Combined Operations

```bash
# Lint and format together
biome check --write .

# Only format (skip linting)
biome format --write .

# CI mode (check both lint and format)
biome ci .
```

## Formatter Configuration

### Global Settings

```json
{
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineEnding": "lf",
    "lineWidth": 80,
    "attributePosition": "auto"
  }
}
```

Options:

- `enabled`: Enable/disable formatter (default: true)
- `formatWithErrors`: Format even with syntax errors (default: false)
- `indentStyle`: "space" or "tab" (default: "tab")
- `indentWidth`: Number of spaces, typically 2 or 4 (default: 2)
- `lineEnding`: "lf", "crlf", or "cr" (default: "lf")
- `lineWidth`: Maximum line length (default: 80)
- `attributePosition`: "auto" or "multiline" for HTML/JSX

### Recommended Configuration

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineEnding": "lf",
    "lineWidth": 100
  }
}
```

## Language-Specific Formatting

### JavaScript/TypeScript

```json
{
  "javascript": {
    "formatter": {
      "enabled": true,
      "quoteStyle": "single",
      "jsxQuoteStyle": "double",
      "quoteProperties": "asNeeded",
      "trailingCommas": "all",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSpacing": true,
      "bracketSameLine": false,
      "attributePosition": "auto"
    }
  }
}
```

#### Quote Styles

```json
{
  "javascript": {
    "formatter": {
      "quoteStyle": "single",      // 'string' vs "string"
      "jsxQuoteStyle": "double"     // <div attr="value">
    }
  }
}
```

Examples:

```javascript
// quoteStyle: "single"
const message = 'Hello, world!';
const name = 'Alice';

// quoteStyle: "double"
const message = "Hello, world!";
const name = "Alice";

// jsxQuoteStyle: "double"
<button onClick={handleClick} label="Submit" />

// jsxQuoteStyle: "single"
<button onClick={handleClick} label='Submit' />
```

#### Trailing Commas

```json
{
  "javascript": {
    "formatter": {
      "trailingCommas": "all"  // "all", "es5", or "none"
    }
  }
}
```

Examples:

```javascript
// "all"
const obj = {
  a: 1,
  b: 2,
};

function fn(
  arg1,
  arg2,
) {}

// "es5"
const obj = {
  a: 1,
  b: 2,
};

function fn(
  arg1,
  arg2  // No comma (not ES5)
) {}

// "none"
const obj = {
  a: 1,
  b: 2
};
```

#### Semicolons

```json
{
  "javascript": {
    "formatter": {
      "semicolons": "always"  // "always" or "asNeeded"
    }
  }
}
```

Examples:

```javascript
// "always"
const x = 1;
const y = 2;

// "asNeeded"
const x = 1
const y = 2
```

#### Arrow Parentheses

```json
{
  "javascript": {
    "formatter": {
      "arrowParentheses": "always"  // "always" or "asNeeded"
    }
  }
}
```

Examples:

```javascript
// "always"
const fn = (x) => x * 2;
const single = (item) => item;

// "asNeeded"
const fn = x => x * 2;
const single = item => item;
const multi = (a, b) => a + b;  // Still needs parens
```

#### Bracket Spacing

```json
{
  "javascript": {
    "formatter": {
      "bracketSpacing": true  // true or false
    }
  }
}
```

Examples:

```javascript
// bracketSpacing: true
const obj = { a: 1, b: 2 };

// bracketSpacing: false
const obj = {a: 1, b: 2};
```

#### Bracket Same Line

```json
{
  "javascript": {
    "formatter": {
      "bracketSameLine": false  // true or false
    }
  }
}
```

Examples:

```jsx
// bracketSameLine: false
<Button
  onClick={handleClick}
  label="Submit"
>
  Click me
</Button>

// bracketSameLine: true
<Button
  onClick={handleClick}
  label="Submit">
  Click me
</Button>
```

#### Quote Properties

```json
{
  "javascript": {
    "formatter": {
      "quoteProperties": "asNeeded"  // "asNeeded" or "preserve"
    }
  }
}
```

Examples:

```javascript
// "asNeeded"
const obj = {
  validIdentifier: 1,
  'invalid-identifier': 2,
  'needs quotes': 3,
};

// "preserve"
const obj = {
  'validIdentifier': 1,
  'invalid-identifier': 2,
  'needs quotes': 3,
};
```

### JSON Formatting

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

Note: JSON doesn't support trailing commas, so always use "none".

### CSS Formatting

```json
{
  "css": {
    "formatter": {
      "enabled": true,
      "indentStyle": "space",
      "indentWidth": 2,
      "lineWidth": 80,
      "quoteStyle": "double"
    }
  }
}
```

## Common Configurations

### Prettier-like Configuration

```json
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
      "trailingCommas": "es5",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSpacing": true,
      "bracketSameLine": false
    }
  }
}
```

### Standard/XO Style

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "none",
      "semicolons": "asNeeded",
      "arrowParentheses": "asNeeded",
      "bracketSpacing": true
    }
  }
}
```

### Google Style

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 80
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "all",
      "semicolons": "always",
      "arrowParentheses": "always"
    }
  }
}
```

### Airbnb Style

```json
{
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "jsxQuoteStyle": "double",
      "trailingCommas": "all",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSpacing": true
    }
  }
}
```

## Ignoring Formatting

### Ignore Blocks

```javascript
// biome-ignore format: Preserve specific formatting
const matrix = [
  [1, 0, 0],
  [0, 1, 0],
  [0, 0, 1]
];

// biome-ignore format: ASCII art
const banner = `
  ╔═══════════════╗
  ║   Welcome!    ║
  ╚═══════════════╝
`;
```

### Ignore Files

In biome.json:

```json
{
  "formatter": {
    "ignore": [
      "**/generated/**",
      "**/*.min.js",
      "**/dist/**"
    ]
  }
}
```

Or use files.ignore for both linting and formatting:

```json
{
  "files": {
    "ignore": [
      "**/node_modules/",
      "**/dist/",
      "**/*.min.js"
    ]
  }
}
```

## Line Width Strategies

### Conservative (80 columns)

Good for code review, side-by-side diffs:

```json
{
  "formatter": {
    "lineWidth": 80
  }
}
```

### Balanced (100-120 columns)

Modern standard for most projects:

```json
{
  "formatter": {
    "lineWidth": 100
  }
}
```

### Relaxed (120+ columns)

For teams with large screens:

```json
{
  "formatter": {
    "lineWidth": 120
  }
}
```

## Indentation Strategies

### Spaces (Recommended)

```json
{
  "formatter": {
    "indentStyle": "space",
    "indentWidth": 2  // or 4
  }
}
```

Pros:

- Consistent across all editors
- Better for code review
- Standard in JavaScript ecosystem

### Tabs

```json
{
  "formatter": {
    "indentStyle": "tab"
  }
}
```

Pros:

- Users can set preferred width
- Smaller file sizes
- Accessibility benefits

## Migration from Prettier

### Compare Configuration

Prettier `.prettierrc.json`:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 80
}
```

Equivalent Biome config:

```json
{
  "formatter": {
    "indentWidth": 2,
    "lineWidth": 80
  },
  "javascript": {
    "formatter": {
      "semicolons": "always",
      "quoteStyle": "single",
      "trailingCommas": "all"
    }
  }
}
```

### Migration Steps

1. **Install Biome**:

```bash
npm install -D @biomejs/biome
```

1. **Create Config**:

```bash
npx biome init
```

1. **Match Prettier Settings**: Update biome.json with equivalent config

2. **Format Codebase**:

```bash
npx biome format --write .
```

1. **Update Scripts**:

```json
{
  "scripts": {
    "format": "biome format --write .",
    "format:check": "biome format ."
  }
}
```

1. **Remove Prettier** (after validation):

```bash
npm uninstall prettier
rm .prettierrc.json .prettierignore
```

## Best Practices

1. **Consistent Configuration** - Same settings across all packages
2. **Line Width Balance** - 80-120 based on team preference
3. **Use Spaces** - More consistent than tabs for JavaScript
4. **Enable in CI** - Check formatting in pipelines
5. **Pre-commit Hooks** - Auto-format before commit
6. **Document Choices** - Explain config decisions to team
7. **Ignore Generated Files** - Don't format build output
8. **Format Incrementally** - Use `--changed` for large codebases
9. **Editor Integration** - Install Biome extension for IDE
10. **Review Diffs** - Check formatting changes before commit

## Common Pitfalls

1. **Conflicting Configs** - Multiple configs with different settings
2. **Formatting Generated Code** - Wasting time on build output
3. **Too Strict Line Width** - 60 or less is too restrictive
4. **Mixing Tabs and Spaces** - Inconsistent indentation
5. **No CI Check** - Not enforcing formatting in pipeline
6. **Wrong File Patterns** - Ignoring files that should be formatted
7. **No Editor Setup** - Manually running format commands
8. **Large Commits** - Formatting entire codebase at once
9. **Ignoring Errors** - formatWithErrors hides syntax issues
10. **No Team Agreement** - Individual preferences cause conflicts

## Advanced Topics

### Per-Language Overrides

```json
{
  "formatter": {
    "indentWidth": 2
  },
  "overrides": [
    {
      "include": ["**/*.json"],
      "formatter": {
        "lineWidth": 120
      }
    },
    {
      "include": ["**/*.md"],
      "formatter": {
        "lineWidth": 80
      }
    }
  ]
}
```

### Conditional Formatting

Format only changed files:

```bash
# Git changed files
biome format --write --changed

# Specific commit range
biome format --write --since=main
```

### Editor Integration

VS Code settings.json:

```json
{
  "editor.defaultFormatter": "biomejs.biome",
  "editor.formatOnSave": true,
  "[javascript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome"
  },
  "[json]": {
    "editor.defaultFormatter": "biomejs.biome"
  }
}
```

### Monorepo Setup

Root biome.json:

```json
{
  "formatter": {
    "enabled": true,
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "all"
    }
  }
}
```

Package-specific override:

```json
{
  "extends": ["../../biome.json"],
  "formatter": {
    "lineWidth": 120
  }
}
```

## Troubleshooting

### Files Not Being Formatted

Check:

1. `formatter.enabled` is true
2. File extension is supported
3. File not in ignore patterns
4. VCS integration not excluding it

### Formatting Conflicts

If formatting keeps changing:

1. Ensure single biome.json source of truth
2. Update all team members' Biome version
3. Run `biome migrate` to update config
4. Clear editor cache and restart

### Performance Issues

Speed up formatting:

1. Use `--changed` for large repos
2. Ignore node_modules and dist
3. Update to latest Biome version
4. Use VCS integration

## When to Use This Skill

- Setting up code formatting for projects
- Migrating from Prettier to Biome
- Establishing team code style standards
- Configuring formatter for specific frameworks
- Troubleshooting formatting issues
- Optimizing formatting performance
- Integrating formatting into CI/CD
- Training teams on code style
