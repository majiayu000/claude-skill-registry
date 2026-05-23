---
name: eslint-prettier
description: >-
  Configures and uses ESLint and Prettier for JavaScript/TypeScript formatting. Activates when fixing
  lint errors, formatting JS/TS code, configuring ESLint rules, or when user mentions eslint, prettier,
  lint, format, code style, or JavaScript formatting.
---

# ESLint & Prettier Development

## When to Apply

Activate this skill when:

- Fixing ESLint errors or warnings
- Formatting JavaScript/TypeScript code
- Configuring ESLint or Prettier rules
- Resolving conflicts between ESLint and Prettier
- Setting up linting for new file types

## Running Formatters

### Check for Issues

```bash
# Run ESLint
npx eslint .

# Check specific files
npx eslint "src/**/*.{js,ts,vue}"

# Check Prettier formatting
npx prettier --check .
```

### Fix Issues

```bash
# Auto-fix ESLint issues
npx eslint . --fix

# Format with Prettier
npx prettier --write .

# Format specific files
npx prettier --write "src/**/*.{js,ts,vue}"
```

## ESLint 9 Flat Config

ESLint 9 uses flat config format (`eslint.config.js`):

<code-snippet name="ESLint Flat Config" lang="javascript">
// eslint.config.js
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import vue from 'eslint-plugin-vue';
import prettier from 'eslint-config-prettier';

export default [
    js.configs.recommended,
    ...vue.configs['flat/recommended'],
    prettier,
    {
        files: ['**/*.{ts,tsx,vue}'],
        languageOptions: {
            parser: tsParser,
            parserOptions: {
                ecmaVersion: 'latest',
                sourceType: 'module',
            },
        },
        plugins: {
            '@typescript-eslint': typescript,
        },
        rules: {
            '@typescript-eslint/no-unused-vars': 'error',
        },
    },
    {
        ignores: ['node_modules/', 'dist/', 'vendor/'],
    },
];
</code-snippet>

## Prettier Configuration

<code-snippet name="Prettier Config" lang="javascript">
// prettier.config.js
export default {
    semi: true,
    singleQuote: true,
    tabWidth: 4,
    trailingComma: 'all',
    printWidth: 120,
    plugins: ['prettier-plugin-tailwindcss'],
};
</code-snippet>

## Common ESLint Rules

<code-snippet name="Common Rules" lang="javascript">
rules: {
    // TypeScript
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/no-explicit-any': 'warn',

    // Vue
    'vue/multi-word-component-names': 'off',
    'vue/require-default-prop': 'off',

    // General
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'prefer-const': 'error',
}
</code-snippet>

## VS Code Integration

<code-snippet name="VS Code Settings" lang="json">
// .vscode/settings.json
{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
        "source.fixAll.eslint": "explicit"
    },
    "[vue]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode"
    }
}
</code-snippet>

## Package.json Scripts

<code-snippet name="NPM Scripts" lang="json">
{
    "scripts": {
        "lint": "eslint .",
        "lint:fix": "eslint . --fix",
        "format": "prettier --write .",
        "format:check": "prettier --check ."
    }
}
</code-snippet>

## Ignoring Files

<code-snippet name="Ignore Patterns" lang="text">
// .prettierignore
node_modules/
dist/
vendor/
public/build/
*.min.js
</code-snippet>

## Common Issues and Fixes

### ESLint/Prettier Conflicts

Use `eslint-config-prettier` to disable conflicting ESLint rules:

```bash
npm install -D eslint-config-prettier
```

Add as last item in ESLint config to override conflicting rules.

### Vue Single File Components

Ensure Vue plugin is configured for `.vue` files:

```bash
npm install -D eslint-plugin-vue
```

### TypeScript Support

```bash
npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

## Common Pitfalls

- Not running formatters before committing
- ESLint and Prettier conflicting on formatting rules
- Missing parser configuration for TypeScript/Vue files
- Using legacy `.eslintrc` format with ESLint 9
- Not ignoring build output directories
- Forgetting to install required ESLint plugins
