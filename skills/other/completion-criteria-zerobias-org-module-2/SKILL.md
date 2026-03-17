---
name: completion-criteria
description: Completion checklist - when is a task truly done
---

## ✅ Completion Checklist

Task is ONLY complete when ALL items checked:

### API Specification Phase
- [ ] Operation added to api.yml
- [ ] Operation name follows pattern (get/list/search/create/update/delete)
- [ ] Summary uses "Retrieve" for get/list operations
- [ ] Description added from vendor documentation
- [ ] NO error responses (only 200/201)
- [ ] Properties are camelCase
- [ ] Nested objects use $ref

### Code Generation Phase
- [ ] Ran `npm run clean && npm run generate`
- [ ] Generation succeeded without errors
- [ ] New types created in generated/
- [ ] No InlineResponse types generated

### Implementation Phase
- [ ] Method added to producer class
- [ ] Using generated types (NO Promise<any>)
- [ ] Mappers implemented for field conversions
- [ ] Error handling using core types
- [ ] No TypeScript compilation errors

### Testing Phase
- [ ] Unit test file created/updated
- [ ] Integration test file created/updated
- [ ] At least 3 test cases for the operation
- [ ] Success case tested
- [ ] Error cases tested
- [ ] Mocks properly configured

### Validation Phase
- [ ] All tests passing (`npm test`)
- [ ] No regression in existing tests
- [ ] Build successful (`npm run build`)
- [ ] Dependencies locked (`npm run shrinkwrap`)
- [ ] npm-shrinkwrap.json created
- [ ] No linting errors

### Documentation Phase
- [ ] Operation documented in code
- [ ] Test names descriptive
- [ ] Any special behavior noted

## 🚫 Immediate Failure Conditions

Task FAILS if:

1. **Operation name contains 'describe'**
   - STOP immediately, use 'get' instead

2. **API spec contains 4xx or 5xx responses**
   - DELETE all error responses
   - Framework handles errors automatically

3. **Skipped generation step**
   - TASK FAILED - must run `npm run clean && npm run generate`

4. **No tests written**
   - TASK FAILED - tests are mandatory

5. **Tests not run**
   - TASK FAILED - must execute `npm test`

6. **Build not verified**
   - TASK FAILED - must execute `npm run build`

7. **Dependencies not locked**
   - TASK FAILED - must execute `npm run shrinkwrap`

8. **Used `Promise<any>` in signatures**
   - TASK FAILED - use generated types

9. **Stopped before Gate 6**
   - TASK INCOMPLETE - continue working

10. **Schema used in both nested and direct contexts without separation**
   - If schema has 10+ properties AND is referenced by other schemas AND has its own endpoint
   - CREATE separate `{Schema}Summary` for nested usage
   - See api-specification.md Rule #19

11. **Hardcoded test values in integration tests**
   - ALL test values (IDs, names, etc.) MUST be in .env
   - Export from test/integration/Common.ts
   - Import and use in integration tests
   - NEVER hardcode: `const userId = '12345'` ❌
   - ALWAYS use .env: `const userId = TEST_USER_ID` ✅
   - See testing.md Rule #7

## Red Flags (Incomplete Work)

Watch for these signs:

1. **No mention of tests** - MAJOR red flag
2. **"I've added the operation"** without test confirmation
3. **No `npm test` output shown**
4. **No build validation**
5. **Jumping to "done" after implementation**

## User Should NEVER Have To Say

- "Now write tests"
- "Did you test it?"
- "Run the tests"
- "Does it build?"
- "You forgot the tests"

If user has to remind about tests: **TASK HAS FAILED**

## Complete Execution Example

```
✅ OPERATION COMPLETE: getAccessToken

Gate 1 - API Specification: ✅
- Operation: getAccessToken (uses 'get', not 'describe')
- Summary: "Retrieve an access token"
- Description from vendor docs included
- Response: 200 only (no error codes)
- All properties camelCase

Gate 2 - Type Generation: ✅
- Ran: npm run clean && npm run generate
- Generated: AccessToken interface
- No InlineResponse types
- Exit code: 0

Gate 3 - Implementation: ✅
- Added to AccessTokenProducer
- Signature: Promise<AccessToken> (not any)
- Mappers handle snake_case → camelCase
- Error handling uses core errors

Gate 4 - Test Creation: ✅
- Unit tests: test/AccessTokenProducerTest.ts (4 cases)
- Integration: test/integration/AccessTokenIntegrationTest.ts (2 cases)
- Mock responses configured

Gate 5 - Test Execution: ✅
- Ran: npm test
- Result: 6 passing
- No regressions
- Exit code: 0

Gate 6 - Build: ✅
- Ran: npm run build
- Result: Success
- No errors
- Exit code: 0
- Ran: npm run shrinkwrap
- npm-shrinkwrap.json created
- Dependencies locked

Operation is fully implemented, tested, and verified.
```

## Enforcement Rules Summary

| Rule | Violation = Task Failure |
|------|--------------------------|
| NEVER use 'describe' prefix | ✅ Yes |
| ONLY 200/201 responses | ✅ Yes |
| ALWAYS run generate after API changes | ✅ Yes |
| ALWAYS write tests | ✅ Yes |
| ALWAYS run tests | ✅ Yes |
| ALWAYS build and verify | ✅ Yes |
| ALWAYS run shrinkwrap | ✅ Yes |
| NO `Promise<any>` types | ✅ Yes |

## Quick Validation Script

```bash
#!/bin/bash
# validate-operation.sh

echo "🚦 Validating operation completion..."

FAILED=0

# Gate 1: API Spec
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
if [ ! -d "generated" ]; then
  echo "❌ Gate 2 FAILED: No generated directory"
  FAILED=1
fi

# Gate 3: Implementation
if grep "Promise<any>" src/*.ts > /dev/null 2>&1; then
  echo "❌ Gate 3 FAILED: Promise<any> found"
  FAILED=1
fi

# Gate 4: Tests exist
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
if ! npm test > /dev/null 2>&1; then
  echo "❌ Gate 5 FAILED: Tests failing"
  FAILED=1
fi

# Gate 6: Build passes
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

if [ $FAILED -eq 0 ]; then
  echo "✅ ALL GATES PASSED - Operation complete!"
else
  echo "🚨 FAILED - Fix issues and re-validate"
  exit 1
fi
```

## Remember

**GATES ARE NOT OPTIONAL**

Every operation MUST pass through ALL gates sequentially.
No shortcuts. No exceptions. Complete or fail.
