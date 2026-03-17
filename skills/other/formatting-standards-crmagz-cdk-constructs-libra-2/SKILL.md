---
name: formatting-standards
description: Formatting and linting standards using GTS, ESLint, and Prettier. Use when writing or formatting TypeScript code in this project.
---

# Formatting Standards

## Tools

This repository uses:

- **ESLint** for code quality (extends GTS)
- **Prettier** for formatting (extends GTS)
- **GTS** (Google TypeScript Style) for TypeScript style

## Configuration Files

- `.eslintrc.json` - ESLint configuration (extends GTS)
- `.prettierrc.js` - Prettier configuration (extends GTS)
- `.eslintignore` - Files to ignore for linting
- `.prettierignore` - Files to ignore for formatting

## Formatting Rules

Based on GTS and project configuration:

- **Indentation**: 4 spaces (not tabs)
- **Line Width**: 160 characters
- **Import Spacing**: Spaces around braces: `{ Item }` not `{Item}`
- **Function Signatures**: Multi-line when they exceed print width
- **Arrow Functions**: Parentheses around single parameters: `(x) =>` not `x =>`
- **Quotes**: Single quotes (from GTS)
- **Semicolons**: Required (from GTS)
- **Trailing Commas**: ES5 style (from GTS)

## Running Formatting

```bash
# Format all files
npm run format

# Check formatting without writing
npm run format:check

# Format and fix linting issues
npm run format:fix
```

## VS Code Integration

Format on save is configured in `.vscode/settings.json`:

- Prettier is the default formatter
- ESLint auto-fix on save
- Format on save enabled for TypeScript, JavaScript, JSON

## Before Committing

Always run:

```bash
npm run format:fix
```

This ensures:

- Code is formatted according to GTS/Prettier rules
- Linting issues are automatically fixed
- Consistent code style across the repository
