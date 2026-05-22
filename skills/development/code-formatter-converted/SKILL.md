---
name: code-formatter
description: Formats code files using prettier and eslint. Use when the user wants to format code, fix linting issues, or clean up code style.
allowed-tools:
  - Read
  - Write
  - Bash
---

# Code Formatter Skill

Automatically formats code files using industry-standard tools.

## Capabilities

- Format JavaScript/TypeScript with Prettier
- Fix ESLint issues automatically
- Format JSON, YAML, and Markdown files
- Run format checks before commits

## Usage Examples

**Format a single file:**
```
"Format the src/index.js file"
```

**Format entire directory:**
```
"Format all files in the src/ directory"
```

**Check formatting without changes:**
```
"Check if files in src/ are properly formatted"
```

## Configuration

Set these environment variables for custom configuration:
- `PRETTIER_CONFIG`: Path to prettier config (default: .prettierrc)
- `ESLINT_CONFIG`: Path to eslint config (default: .eslintrc.js)
