---
name: eslint-config
# prettier-ignore
description: Use when configuring ESLint - covers flat config, TypeScript integration, and custom rules
---

# ESLint Configuration Best Practices

## Quick Start (Flat Config)

```javascript
// eslint.config.js
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["src/**/*.ts"],
    rules: {
      "@typescript-eslint/no-unused-vars": ["error", { argsIgnorePattern: "^_" }],
    },
  },
  {
    ignores: ["dist/", "node_modules/"],
  }
);
```

## Core Configuration

### TypeScript Integration

```javascript
import tseslint from "typescript-eslint";

export default tseslint.config(
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        project: "./tsconfig.json",
      },
    },
  }
);
```

### Custom Rules

```javascript
{
  rules: {
    // Disallow console in production
    "no-console": "warn",

    // Require explicit return types
    "@typescript-eslint/explicit-function-return-type": "error",

    // Prefer const
    "prefer-const": "error",

    // No floating promises
    "@typescript-eslint/no-floating-promises": "error",
  }
}
```

### File-Specific Rules

```javascript
export default [
  {
    files: ["src/**/*.ts"],
    rules: { /* production rules */ }
  },
  {
    files: ["**/*.test.ts", "__tests__/**/*.ts"],
    rules: {
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-non-null-assertion": "off",
    }
  },
  {
    files: ["scripts/**/*.ts"],
    rules: {
      "no-console": "off",
    }
  }
];
```

## Common Patterns for Language Projects

### Parser/Interpreter Specific

```javascript
{
  rules: {
    // Allow switch fallthrough for token parsing
    "no-fallthrough": ["error", { commentPattern: "falls?\\s*through" }],

    // Allow bitwise for flags
    "no-bitwise": "off",

    // Complex functions in interpreters
    "complexity": ["warn", 20],
    "max-depth": ["warn", 5],
  }
}
```

### Naming Conventions

```javascript
{
  rules: {
    "@typescript-eslint/naming-convention": [
      "error",
      { selector: "interface", format: ["PascalCase"] },
      { selector: "typeAlias", format: ["PascalCase"] },
      { selector: "enum", format: ["PascalCase"] },
      { selector: "enumMember", format: ["UPPER_CASE"] },
    ]
  }
}
```

## Migration from Legacy Config

```javascript
// Old: .eslintrc.json
{
  "extends": ["eslint:recommended"],
  "rules": { "semi": "error" }
}

// New: eslint.config.js
import eslint from "@eslint/js";
export default [
  eslint.configs.recommended,
  { rules: { semi: "error" } }
];
```

## Scripts

```json
{
  "scripts": {
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix"
  }
}
```

## Reference Files

- [references/rules.md](references/rules.md) - Common rule configurations
- [references/plugins.md](references/plugins.md) - Popular plugins
