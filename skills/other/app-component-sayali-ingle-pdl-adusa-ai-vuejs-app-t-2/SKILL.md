---
name: app-component
description: Generates src/App.vue root component with unit test. Creates both App.vue and App.spec.ts files.
---

# App Component Skill

## Purpose
Generate the `src/App.vue` root component **WITH UNIT TEST**. The component MUST have a corresponding .spec.ts file created at the same time.

**CRITICAL**: This skill requires creating BOTH the App.vue component file AND its App.spec.ts test file. Do not skip test file creation.

## 🚨 MANDATORY FILE COUNT
**Total Required: 2 files**
- `src/App.vue` (1 file) + `src/App.spec.ts` (1 file) = 2 files

**If you create fewer than 2 files, you have FAILED this skill.**

## Output
- Create the file: `src/App.vue`
- Create the unit test file: `src/App.spec.ts` ⚠️ **REQUIRED**

## Execution Order (Test-Driven Development)
**IMPORTANT**: Follow this order strictly to ensure tests are never forgotten:

1. **Create `src/App.spec.ts` FIRST** with failing tests
2. **Then create `src/App.vue`** to make tests pass

This TDD approach ensures you never create a component without its test.

## Requirements
- Simple root component with router-view
- The `id` attribute should use the `appId` constant from global constants
- Imports theme variables for global styling
- No scoped styles to allow global CSS
- Component should be minimal and serve as a container for the router view
- **MUST have a unit test file in the same directory**
- Unit tests MUST cover:
  - Component rendering
  - Router-view presence
  - Props (if any)
  - Methods and computed properties (if any)
  - Lifecycle hooks (created, mounted, etc.)
  - Global store initialization (if applicable)

## Test Coverage Requirements
The App.spec.ts file should include:
- Basic rendering test
- Router-view component verification
- DOM element verification (root div with correct id)
- Lifecycle hook execution tests
- Store initialization tests (if using Pinia/Vuex)
- Minimum 80% code coverage

## Execution Checklist
Use this checklist to ensure all required files are created:
- [ ] Create `src/App.spec.ts` with comprehensive tests **FIRST**
- [ ] Create `src/App.vue` component
- [ ] Verify both files exist in src/ directory
- [ ] Run unit test to ensure tests pass
- [ ] Verify test output shows tests for App component

## 🛑 BLOCKING VALIDATION CHECKPOINT
**STOP AND VERIFY before proceeding to the next skill:**

### Automated Verification
Run this command to verify test file exists:
```bash
# Check for App.spec.ts
if [ ! -f "src/App.spec.ts" ]; then
  echo "❌ MISSING: src/App.spec.ts"
  exit 1
fi
echo "✅ App.spec.ts present"
```

### Manual Verification
1. ✓ Count files: Must be exactly 2 files (App.vue + App.spec.ts)
2. ✓ `src/App.vue` exists in src/ directory
3. ✓ `src/App.spec.ts` exists alongside `src/App.vue`
4. ✓ Running `npm test` confirms all tests pass
5. ✓ Test output shows at least 3-5 tests for App component
6. ✓ No test files are skipped or marked as pending

### If Validation Fails
**DO NOT PROCEED** to the next skill. Go back and create the missing test file immediately.

## Validation
After creating all files, validate:
1. ✓ App.vue exists in src/ directory
2. ✓ App.spec.ts exists alongside App.vue
3. ✓ Running unit test confirms all tests pass
4. ✓ Test output shows at least 3-5 tests for App component
5. ✓ No test files are skipped or marked as pending
