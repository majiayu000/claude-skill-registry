---
name: validation-automation
description: Automated validation scripts for quality gates
---

# Validation Script

Quick validation script to check all gates after operation implementation.

## Usage

```bash
# Make script executable
chmod +x validate-operation.sh

# Run validation
./validate-operation.sh
```

## Script Content

Save this as `validate-operation.sh` in module root:

```bash
#!/bin/bash
# validate-operation.sh
# Validates that an operation meets all quality gates

echo "🚦 Validating operation completion..."

FAILED=0

# Gate 1: API Spec
echo "Checking Gate 1: API Specification..."

if grep -E "describe[A-Z]" api.yml > /dev/null 2>&1; then
  echo "❌ Gate 1 FAILED: 'describe' found in api.yml"
  FAILED=1
fi

if grep "nullable:" api.yml > /dev/null 2>&1; then
  echo "❌ Gate 1 FAILED: 'nullable' found in api.yml"
  FAILED=1
fi

# Check for schema context separation issues
nested_schemas=$(yq eval '.components.schemas[] | .. | select(type == "string" and test("#/components/schemas/")) | capture("#/components/schemas/(?<schema>.+)").schema' api.yml 2>/dev/null | sort -u)
endpoint_schemas=$(yq eval '.paths.*.*.responses.*.content.*.schema["$ref"]' api.yml 2>/dev/null | grep -o '[^/]*$' | sort -u)
for schema in $nested_schemas; do
  if echo "$endpoint_schemas" | grep -q "^${schema}$"; then
    prop_count=$(yq eval ".components.schemas.${schema}.properties | length" api.yml 2>/dev/null)
    if [ "$prop_count" -gt 10 ] 2>/dev/null; then
      echo "⚠️  WARNING: Schema '${schema}' used in BOTH nested and direct contexts with ${prop_count} properties"
      echo "   Consider creating '${schema}Summary' for nested usage (see api-specification.md Rule #19)"
    fi
  fi
done

# Gate 2: Generation
echo "Checking Gate 2: Type Generation..."

if [ ! -d "generated" ]; then
  echo "❌ Gate 2 FAILED: No generated directory"
  FAILED=1
fi

# Gate 3: Implementation
echo "Checking Gate 3: Implementation..."

if grep "Promise<any>" src/*.ts > /dev/null 2>&1; then
  echo "❌ Gate 3 FAILED: Promise<any> found"
  FAILED=1
fi

# Gate 4: Tests exist
echo "Checking Gate 4: Test Creation..."

if ! find test -name "*Test.ts" | grep -q .; then
  echo "❌ Gate 4 FAILED: No test files"
  FAILED=1
fi

# Gate 4b: No hardcoded test values in integration tests
if [ -d "test/integration" ]; then
  if grep -E "(const|let|var) [a-zA-Z]*[Ii]d = ['\"][0-9]+['\"]" test/integration/*.ts > /dev/null 2>&1; then
    echo "❌ Gate 4 FAILED: Hardcoded test values in integration tests"
    echo "   All test values must be in .env and imported from Common.ts"
    FAILED=1
  fi
fi

# Gate 5: Tests pass
echo "Checking Gate 5: Test Execution..."

if ! npm test > /dev/null 2>&1; then
  echo "❌ Gate 5 FAILED: Tests failing"
  FAILED=1
fi

# Gate 6: Build passes
echo "Checking Gate 6: Build..."

if ! npm run build > /dev/null 2>&1; then
  echo "❌ Gate 6 FAILED: Build failing"
  FAILED=1
fi

# Gate 6b: Shrinkwrap dependencies
if ! npm run shrinkwrap > /dev/null 2>&1; then
  echo "❌ Gate 6 FAILED: Shrinkwrap failing"
  FAILED=1
fi

if [ ! -f "npm-shrinkwrap.json" ]; then
  echo "❌ Gate 6 FAILED: npm-shrinkwrap.json not created"
  FAILED=1
fi

# Final result
if [ $FAILED -eq 0 ]; then
  echo ""
  echo "✅ ALL GATES PASSED - Operation complete!"
  exit 0
else
  echo ""
  echo "🚨 VALIDATION FAILED - Fix issues and re-validate"
  exit 1
fi
```

## Example Output (Success)

```
🚦 Validating operation completion...
Checking Gate 1: API Specification...
Checking Gate 2: Type Generation...
Checking Gate 3: Implementation...
Checking Gate 4: Test Creation...
Checking Gate 5: Test Execution...
Checking Gate 6: Build...

✅ ALL GATES PASSED - Operation complete!
```

## Example Output (Failure)

```
🚦 Validating operation completion...
Checking Gate 1: API Specification...
❌ Gate 1 FAILED: 'describe' found in api.yml
Checking Gate 2: Type Generation...
Checking Gate 3: Implementation...
❌ Gate 3 FAILED: Promise<any> found
Checking Gate 4: Test Creation...
Checking Gate 5: Test Execution...
❌ Gate 5 FAILED: Tests failing
Checking Gate 6: Build...

🚨 VALIDATION FAILED - Fix issues and re-validate
```

## Integration with Agents

Agents can reference this script in their validation steps:

```markdown
## Validation

Run the validation script to verify all gates:

```bash
./validate-operation.sh
```

If validation fails, fix issues and re-run.
```

## Manual Gate Checks

If validation script not available, manually verify each gate using the bash commands documented in:
- @.claude/rules/gate-1-api-spec.md
- @.claude/rules/gate-2-type-generation.md
- @.claude/rules/gate-3-implementation.md
- @.claude/rules/gate-4-test-creation.md
- @.claude/rules/gate-5-test-execution.md
- @.claude/rules/gate-6-build.md
