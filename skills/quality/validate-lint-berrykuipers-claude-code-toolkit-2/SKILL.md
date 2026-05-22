---
name: validate-lint
description: Run ESLint and Prettier validation to check code style, formatting, and linting rules. Works with any TypeScript/JavaScript project using ESLint/Prettier. Returns structured output with error/warning counts, rule violations, and affected files.
---

# Validate Lint

## Purpose

Execute ESLint and Prettier to validate code style, formatting standards, and linting rules across the project.

## When to Use

- Quality gate validation (before commit/PR)
- During conductor Phase 3 (Quality Assurance)
- Pre-refactor validation
- Real-time validation during development
- As part of `quality-gate` skill

## Supported Linters

- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- Detects via:
  - npm scripts (`npm run lint`)
  - Direct commands (`eslint .`)
  - npx execution (`npx eslint .`)

## Instructions

### Step 1: Detect Lint Command

```bash
# Check package.json for lint script
if grep -q '"lint"' package.json; then
  LINT_CMD="npm run lint"
  echo "Using npm script: npm run lint"

# Check for eslint in node_modules
elif [ -f node_modules/.bin/eslint ]; then
  LINT_CMD="npx eslint ."
  echo "Using npx eslint"

# Use global eslint
elif command -v eslint &>/dev/null; then
  LINT_CMD="eslint ."
  echo "Using global eslint"

else
  echo "❌ Error: ESLint not available"
  echo "Install: npm install --save-dev eslint"
  exit 1
fi
```

### Step 2: Run Lint Check

```bash
echo "→ Running lint validation..."

# Run linter and capture output
if $LINT_CMD 2>&1 | tee .claude/validation/lint-output.txt; then
  LINT_STATUS="passing"
  LINT_EXIT_CODE=0
  echo "✅ Lint validation passed"
else
  LINT_STATUS="failing"
  LINT_EXIT_CODE=$?
  echo "❌ Lint validation failed"
fi
```

### Step 3: Parse Errors and Warnings

```bash
if [ "$LINT_STATUS" = "failing" ]; then
  # Count errors and warnings
  ERROR_COUNT=$(grep -c 'error  ' .claude/validation/lint-output.txt || echo "0")
  WARNING_COUNT=$(grep -c 'warning  ' .claude/validation/lint-output.txt || echo "0")

  echo "   Errors: $ERROR_COUNT"
  echo "   Warnings: $WARNING_COUNT"

  # Extract affected files
  AFFECTED_FILES=$(grep -oP '^/.+\.tsx?(?=\s)' .claude/validation/lint-output.txt | \
    sort -u | \
    jq -R -s -c 'split("\n") | map(select(length > 0))')

  # Parse rule violations (top offenders)
  RULE_VIOLATIONS=$(grep -oP '\w+/[\w-]+(?=\s+)' .claude/validation/lint-output.txt | \
    sort | uniq -c | sort -rn | head -5 | \
    awk '{print "{\"rule\": \"" $2 "\", \"count\": " $1 "}"}' | \
    jq -s -c '.')

else
  ERROR_COUNT=0
  WARNING_COUNT=0
  AFFECTED_FILES="[]"
  RULE_VIOLATIONS="[]"
fi
```

### Step 4: Return Structured Output

```json
{
  "status": "$([ "$LINT_STATUS" = "passing" ] && echo 'success' || echo 'error')",
  "lint": {
    "status": "$LINT_STATUS",
    "errors": $ERROR_COUNT,
    "warnings": $WARNING_COUNT,
    "files": $AFFECTED_FILES,
    "ruleViolations": $RULE_VIOLATIONS
  },
  "canProceed": $([ "$LINT_STATUS" = "passing" ] && echo 'true' || echo 'false')
}
```

## Output Format

### All Checks Pass

```json
{
  "status": "success",
  "lint": {
    "status": "passing",
    "errors": 0,
    "warnings": 0,
    "files": [],
    "ruleViolations": []
  },
  "canProceed": true
}
```

### Lint Errors Found

```json
{
  "status": "error",
  "lint": {
    "status": "failing",
    "errors": 15,
    "warnings": 8,
    "files": [
      "src/components/Settings.tsx",
      "src/utils/helpers.ts"
    ],
    "ruleViolations": [
      {"rule": "react/prop-types", "count": 5},
      {"rule": "@typescript-eslint/no-explicit-any", "count": 4},
      {"rule": "prettier/prettier", "count": 3}
    ]
  },
  "canProceed": false,
  "details": "15 lint errors must be fixed before proceeding"
}
```

## Integration with Quality Gate

Used in `quality-gate` skill:

```markdown
### Step 2: Lint Validation

Use `validate-lint` skill:

Expected result:
- Status: passing
- Errors: 0
- Warnings: acceptable (configurable)

If lint errors found:
  ❌ BLOCK - Quality gate fails
  → Fix linting errors
  → Re-run quality gate

If lint passes:
  ✅ Continue to next check
```

## Common Rule Violations

### React/TypeScript Rules

```
react/prop-types          - Missing prop type validation
@typescript-eslint/no-explicit-any - Using 'any' type
react-hooks/exhaustive-deps - Missing hook dependencies
```

**Action**: Fix according to project style guide

### Prettier Formatting

```
prettier/prettier - Formatting inconsistencies
```

**Action**: Run `npm run format` or `prettier --write .`

### Import/Export Rules

```
import/no-unresolved - Cannot resolve import
import/order - Incorrect import ordering
```

**Action**: Fix import paths and organize imports

## Auto-Fix Support

Many linting issues can be auto-fixed:

```bash
# Auto-fix ESLint issues
eslint --fix .

# Auto-format with Prettier
prettier --write .

# Combined (if configured)
npm run lint:fix
```

## Related Skills

- `quality-gate` - Uses this for lint validation
- `validate-typescript` - Type checking (separate from linting)

## Error Handling

### ESLint Not Installed

```json
{
  "status": "error",
  "error": "ESLint not available",
  "suggestion": "Install ESLint: npm install --save-dev eslint"
}
```

### No ESLint Config

```bash
if [ ! -f .eslintrc.json ] && [ ! -f .eslintrc.js ] && [ ! -f eslint.config.js ]; then
  echo "⚠️ Warning: No ESLint config found - using default rules"
fi
```

## Best Practices

1. **Fix errors before committing** - Don't accumulate lint debt
2. **Warnings are acceptable** - Configure thresholds in quality-gate
3. **Use auto-fix when safe** - Speeds up fixing formatting issues
4. **Consistent config** - Share ESLint config across team
5. **Save output** - Keep logs for debugging

## Notes

- Warnings don't block quality gate by default (configurable)
- Errors always block
- Output saved to `.claude/validation/lint-output.txt`
- Respects `.eslintignore` and `.prettierignore`
