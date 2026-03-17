---
name: validate-typescript
description: Run TypeScript compiler type-checking (tsc --noEmit) to validate type safety and catch type errors. Returns structured output with error counts, categories (type/syntax/import errors), and affected files. Used for quality gates and pre-commit validation.
---

# Validate TypeScript

Executes TypeScript compiler in type-check mode to validate type safety without emitting files.

## Usage

This skill runs `tsc --noEmit` and returns structured validation results.

## Output Format

### Success (No Errors)

```json
{
  "status": "success",
  "typescript": {
    "status": "passing",
    "errors": {
      "total": 0,
      "type": 0,
      "syntax": 0,
      "import": 0
    },
    "files": []
  },
  "canProceed": true
}
```

### Errors Found

```json
{
  "status": "error",
  "typescript": {
    "status": "failing",
    "errors": {
      "total": 12,
      "type": 8,
      "syntax": 2,
      "import": 2
    },
    "files": [
      "src/components/Settings.tsx",
      "src/context/WorldContext.tsx"
    ]
  },
  "canProceed": false,
  "details": "12 TypeScript errors must be fixed before proceeding"
}
```

## Error Categories

- **TS2xxx**: Type errors (type mismatches, missing properties)
- **TS1xxx**: Syntax errors
- **TS2307**: Import/module errors

## When to Use

- Quality gate validation (before commit/PR)
- Pre-refactor validation
- After TypeScript code changes
- Conductor Phase 3 (Quality Assurance)

## Requirements

- TypeScript installed (via npm or npx)
- tsconfig.json in project root (optional, uses defaults if missing)
