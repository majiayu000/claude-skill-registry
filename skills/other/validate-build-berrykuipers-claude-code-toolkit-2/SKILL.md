---
name: validate-build
description: Run production build validation (npm run build, vite build, tsc) to ensure code compiles and builds successfully. Returns structured output with build status, duration, size metrics, and error details. Used for quality gates and deployment readiness checks.
---

# Validate Build

## Purpose

Execute production build process to validate that code compiles and bundles successfully, ensuring deployment readiness.

## When to Use

- Quality gate validation (before PR)
- Deployment readiness check
- After significant code changes
- Conductor Phase 3 (Quality Assurance)
- CI/CD pipeline validation

## Supported Build Tools

- **Vite**: Modern bundler for frontend
- **TypeScript**: tsc --build
- **Webpack**: Production webpack builds
- **esbuild/Rollup**: Modern bundlers
- Works with any `npm run build` script

## Instructions

### Step 1: Detect Build Command

```bash
# Check package.json for build script
if grep -q '"build"' package.json; then
  BUILD_CMD="npm run build"
  echo "Using npm script: npm run build"

# Check for vite
elif command -v vite &>/dev/null || [ -f node_modules/.bin/vite ]; then
  BUILD_CMD="npx vite build"
  echo "Using vite build"

# Check for tsc
elif command -v tsc &>/dev/null || [ -f node_modules/.bin/tsc ]; then
  BUILD_CMD="npx tsc --build"
  echo "Using tsc --build"

else
  echo "❌ Error: No build command available"
  echo "Add 'build' script to package.json"
  exit 1
fi
```

### Step 2: Run Build

```bash
echo "→ Running production build..."

# Record start time
START_TIME=$(date +%s)

# Run build (with timeout to prevent hanging)
if timeout 300 $BUILD_CMD 2>&1 | tee .claude/validation/build-output.txt; then
  BUILD_STATUS="passing"
  BUILD_EXIT_CODE=0
  echo "✅ Build succeeded"
else
  BUILD_STATUS="failing"
  BUILD_EXIT_CODE=$?
  echo "❌ Build failed"
fi

# Calculate duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
DURATION_STR="${DURATION}s"
```

### Step 3: Measure Build Output

```bash
if [ "$BUILD_STATUS" = "passing" ]; then
  # Check for common build output directories
  BUILD_DIR=""
  if [ -d "dist" ]; then
    BUILD_DIR="dist"
  elif [ -d "build" ]; then
    BUILD_DIR="build"
  elif [ -d "out" ]; then
    BUILD_DIR="out"
  fi

  if [ -n "$BUILD_DIR" ]; then
    # Calculate total output size
    OUTPUT_SIZE=$(du -sh "$BUILD_DIR" | cut -f1)
    echo "   Build output: $OUTPUT_SIZE in $BUILD_DIR/"

    # List main bundle files
    BUNDLE_FILES=$(find "$BUILD_DIR" -name "*.js" -o -name "*.css" | head -5)
  else
    OUTPUT_SIZE="unknown"
  fi
else
  OUTPUT_SIZE="N/A"
fi
```

### Step 4: Parse Build Errors

```bash
if [ "$BUILD_STATUS" = "failing" ]; then
  # Extract error messages
  BUILD_ERRORS=$(grep -A 3 'error\|Error\|ERROR' .claude/validation/build-output.txt | \
    head -20 | \
    jq -R -s -c 'split("\n") | map(select(length > 0))')

  # Count errors
  ERROR_COUNT=$(echo "$BUILD_ERRORS" | jq 'length')

  # Check for warnings too
  WARNING_COUNT=$(grep -c 'warning\|Warning' .claude/validation/build-output.txt || echo "0")

  echo "   Errors: $ERROR_COUNT"
  echo "   Warnings: $WARNING_COUNT"
else
  BUILD_ERRORS="[]"
  ERROR_COUNT=0
  WARNING_COUNT=0
fi
```

### Step 5: Return Structured Output

```json
{
  "status": "$([ "$BUILD_STATUS" = "passing" ] && echo 'success' || echo 'error')",
  "build": {
    "status": "$BUILD_STATUS",
    "duration": "$DURATION_STR",
    "outputSize": "$OUTPUT_SIZE",
    "errors": $BUILD_ERRORS,
    "errorCount": $ERROR_COUNT,
    "warnings": $WARNING_COUNT
  },
  "canProceed": $([ "$BUILD_STATUS" = "passing" ] && echo 'true' || echo 'false')
}
```

## Output Format

### Build Succeeds

```json
{
  "status": "success",
  "build": {
    "status": "passing",
    "duration": "12.3s",
    "outputSize": "245.8 kB",
    "errors": [],
    "errorCount": 0,
    "warnings": 0
  },
  "canProceed": true
}
```

### Build Fails

```json
{
  "status": "error",
  "build": {
    "status": "failing",
    "duration": "5.2s",
    "outputSize": "N/A",
    "errors": [
      "src/components/Settings.tsx(42,15): error TS2339: Property 'user' does not exist on type 'AppState'",
      "Build failed with 1 error(s)"
    ],
    "errorCount": 1,
    "warnings": 2
  },
  "canProceed": false,
  "details": "Build failed with 1 error(s)"
}
```

## Integration with Quality Gate

Used in `quality-gate` skill:

```markdown
### Step 5: Build Validation

Use `validate-build` skill:

Expected result:
- Status: passing
- No build errors
- Reasonable build time (<2 min)

If build fails:
  ❌ BLOCK - Quality gate fails
  → Fix build errors
  → Re-run quality gate

If build passes:
  ✅ Quality gate complete
```

## Common Build Errors

### TypeScript Errors

```
error TS2322: Type 'string' is not assignable to type 'number'
error TS2339: Property 'foo' does not exist
```

**Action**: Fix TypeScript errors (run `validate-typescript` first)

### Module Resolution

```
Error: Cannot find module './component'
Module not found: Can't resolve 'package-name'
```

**Action**: Fix import paths or install missing dependencies

### Syntax Errors

```
SyntaxError: Unexpected token
ParseError: Invalid syntax
```

**Action**: Check for JavaScript/TypeScript syntax errors

## Build Optimization

Monitor build performance:
- **Duration**: Aim for <60s for medium projects
- **Output Size**: Track bundle size trends
- **Warnings**: Address build warnings over time

## Related Skills

- `quality-gate` - Uses this for final validation
- `validate-typescript` - Should pass before build
- `validate-lint` - Code quality before build

## Error Handling

### No Build Script

```json
{
  "status": "error",
  "error": "No build command available",
  "suggestion": "Add 'build' script to package.json"
}
```

### Build Timeout

```bash
# Build exceeds 5 minutes (300s timeout)
if [ $BUILD_EXIT_CODE -eq 124 ]; then
  echo "⚠️ Build timeout - exceeds 5 minutes"
fi
```

## Best Practices

1. **Always build before PR** - Catches build errors early
2. **Monitor build time** - Optimize if exceeding thresholds
3. **Check output size** - Watch for bundle bloat
4. **Clean builds** - Remove build dir before validation
5. **Save output** - Keep logs for debugging

## Notes

- Build runs with production environment settings
- Output saved to `.claude/validation/build-output.txt`
- Timeout set to 5 minutes (300s) to prevent hanging
- Respects `.gitignore` and build tool configs
