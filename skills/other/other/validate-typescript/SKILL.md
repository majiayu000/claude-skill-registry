---
name: validate-typescript
description: Run TypeScript compiler type-checking (tsc --noEmit) to validate type safety and catch type errors. Works with any TypeScript project. Returns structured output with error counts, categories (type/syntax/import errors), and affected files. Used for quality gates and pre-commit validation.
---

# Validate TypeScript

## Purpose

Execute TypeScript compiler in type-check mode to validate type safety without emitting JavaScript files, catching type errors before runtime. Works with any TypeScript/JavaScript project using TypeScript.

## When to Use

- Quality gate validation (before commit/PR)
- Pre-refactor validation
- After TypeScript code changes
- As part of `quality-gate` skill
- Conductor Phase 3 (Quality Assurance)

## Instructions

### Step 1: Check TypeScript Available

```bash
if ! command -v tsc &>/dev/null; then
  if ! command -v npx &>/dev/null; then
    echo "❌ Error: TypeScript not available"
    exit 1
  else
    # Use npx if tsc not in PATH
    TSC_CMD="npx tsc"
  fi
else
  TSC_CMD="tsc"
fi

echo "Using: $TSC_CMD"
```

### Step 2: Run Type Check

```bash
echo "→ Running TypeScript type check..."

# Run tsc --noEmit (no files emitted, just type checking)
if $TSC_CMD --noEmit 2>&1 | tee .claude/validation/tsc-output.txt; then
  TS_STATUS="passing"
  TS_EXIT_CODE=0
  echo "✅ TypeScript validation passed"
else
  TS_STATUS="failing"
  TS_EXIT_CODE=$?
  echo "❌ TypeScript validation failed"
fi
```

### Step 3: Parse Errors

```bash
if [ "$TS_STATUS" = "failing" ]; then
  # Count errors
  ERROR_COUNT=$(grep -c 'error TS' .claude/validation/tsc-output.txt || echo "0")

  echo "   Errors: $ERROR_COUNT"

  # Categorize errors
  TYPE_ERRORS=$(grep -c 'error TS2' .claude/validation/tsc-output.txt || echo "0")
  SYNTAX_ERRORS=$(grep -c 'error TS1' .claude/validation/tsc-output.txt || echo "0")
  IMPORT_ERRORS=$(grep -c 'error TS2307' .claude/validation/tsc-output.txt || echo "0")

  echo "   Type errors: $TYPE_ERRORS"
  echo "   Syntax errors: $SYNTAX_ERRORS"
  echo "   Import errors: $IMPORT_ERRORS"

  # Extract error files
  ERROR_FILES=$(grep 'error TS' .claude/validation/tsc-output.txt | \
    cut -d'(' -f1 | \
    sort -u | \
    jq -R -s -c 'split("\n") | map(select(length > 0))')
else
  ERROR_COUNT=0
  TYPE_ERRORS=0
  SYNTAX_ERRORS=0
  IMPORT_ERRORS=0
  ERROR_FILES="[]"
fi
```

### Step 4: Return Structured Output

```json
{
  "status": "$([ "$TS_STATUS" = "passing" ] && echo 'success' || echo 'error')",
  "typescript": {
    "status": "$TS_STATUS",
    "errors": {
      "total": $ERROR_COUNT,
      "type": $TYPE_ERRORS,
      "syntax": $SYNTAX_ERRORS,
      "import": $IMPORT_ERRORS
    },
    "files": $ERROR_FILES
  },
  "canProceed": $([ "$TS_STATUS" = "passing" ] && echo 'true' || echo 'false')
}
```

## Output Format

### All Types Valid

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

### Type Errors Found

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
      "src/context/WorldContext.tsx",
      "src/types/index.ts"
    ]
  },
  "canProceed": false,
  "details": "12 TypeScript errors must be fixed before proceeding"
}
```

## Integration with Quality Gate

Used in `quality-gate` skill:

```markdown
### Step 5: TypeScript Type Checking

Use `validate-typescript` skill:

Expected result:
- Status: passing
- Errors: 0

If TypeScript errors found:
  ❌ BLOCK - Quality gate fails
  → Fix type errors
  → Re-run quality gate

If TypeScript passes:
  ✅ Continue to next check
```

## Common Error Categories

### TS2xxx - Type Errors

```
error TS2322: Type 'string' is not assignable to type 'number'
error TS2339: Property 'foo' does not exist on type 'Bar'
error TS2345: Argument of type 'X' is not assignable to parameter of type 'Y'
```

**Action**: Fix type mismatches

### TS1xxx - Syntax Errors

```
error TS1005: ',' expected
error TS1128: Declaration or statement expected
```

**Action**: Fix syntax issues

### TS2307 - Import Errors

```
error TS2307: Cannot find module './foo' or its corresponding type declarations
```

**Action**: Fix import paths or install missing types

## Related Skills

- `quality-gate` - Uses this for TypeScript validation
- `record-quality-baseline` - Records TypeScript error count

## Error Handling

### TypeScript Not Installed

```json
{
  "status": "error",
  "error": "TypeScript not available",
  "suggestion": "Install TypeScript: npm install --save-dev typescript"
}
```

### tsconfig.json Missing

```bash
if [ ! -f tsconfig.json ]; then
  echo "⚠️ Warning: tsconfig.json not found - using default config"
fi
```

## Best Practices

1. **Always check before commit** - Prevents type errors in production
2. **Fix errors incrementally** - Don't accumulate type debt
3. **Use strict mode** - Enable strict type checking in tsconfig.json
4. **No `any` types** - Avoid bypassing type system
5. **Save output** - Keep error logs for debugging

## Notes

- Uses `--noEmit` flag (no files generated)
- Respects tsconfig.json configuration
- Exit code 0 = no errors, non-zero = errors found
- Output saved to `.claude/validation/tsc-output.txt`
