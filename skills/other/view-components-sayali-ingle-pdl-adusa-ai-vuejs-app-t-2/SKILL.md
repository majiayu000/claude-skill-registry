---
name: view-components
description: Generates initial view components with mandatory unit tests. Creates HomeView.vue, PageNotFoundView.vue, and their .spec.ts test files (4 files total).
---

# View Components Skill

## Purpose
Generate initial view components for the application **WITH UNIT TESTS**. Each component MUST have a corresponding .spec.ts file created at the same time as the component.

**CRITICAL**: This skill requires creating BOTH the .vue component file AND its .spec.ts test file. Do not skip test file creation.

## 🚨 MANDATORY FILE COUNT
**Total Required: 4 files**
- HomeView.vue (1 file) + HomeView.spec.ts (1 file) = 2 files
- PageNotFoundView.vue (1 file) + PageNotFoundView.spec.ts (1 file) = 2 files

**If you create fewer than 4 files, you have FAILED this skill.**

## Output
Create the files:
- `src/views/Home/Home.vue`
- `src/views/Home/Home.spec.ts` ⚠️ **REQUIRED**
- `src/views/PageNotFoundView/PageNotFoundView.vue`
- `src/views/PageNotFoundView/PageNotFoundView.spec.ts` ⚠️ **REQUIRED**

## Execution Order (Test-Driven Development)
**IMPORTANT**: Follow this order strictly to ensure tests are never forgotten:

1. **Create HomeView.spec.ts FIRST** with failing tests
2. **Then create HomeView.vue** to make tests pass
3. **Create PageNotFoundView.spec.ts FIRST** with failing tests
4. **Then create PageNotFoundView.vue** to make tests pass

This TDD approach ensures you never create a component without its test.

## Requirements
- Home view displays a welcome message
- PageNotFoundView provides a 404 error page
- **Each component MUST have a unit test file within its directory**
- Unit tests MUST cover:
  - Component rendering
  - Props (if any)
  - Events/emits (if any)
  - Methods and computed properties
  - Lifecycle hooks (created, mounted, etc.)
  - User interactions (clicks, inputs, etc.)
  - Conditional rendering
- Both components use theme variables for styling
- Components are placed in their own directories for organization

## Test Coverage Requirements
Each .spec.ts file should include:
- Basic rendering test
- DOM element verification (headings, paragraphs, links, etc.)
- Text content verification
- CSS class verification
- Router/navigation tests (if applicable)
- Minimum 80% code coverage for each component

## Execution Checklist
Use this checklist to ensure all required files are created:
- [ ] Create `src/views/Home/Home.spec.ts` with comprehensive tests **FIRST**
- [ ] Create `src/views/Home/Home.vue` component
- [ ] Create `src/views/PageNotFoundView/PageNotFoundView.spec.ts` with comprehensive tests **FIRST**
- [ ] Create `src/views/PageNotFoundView/PageNotFoundView.vue` component  
- [ ] Verify all 4 files exist in correct directories
- [ ] Run unit test to ensure tests pass
- [ ] Verify test output shows tests for both components

## 🛑 BLOCKING VALIDATION CHECKPOINT
**STOP AND VERIFY before proceeding to the next skill:**

### Automated Verification
Run this command to verify all test files exist:
```bash
# Check for missing test files
for vue_file in src/views/*/*.vue; do
  test_file="${vue_file%.vue}.spec.ts"
  if [ ! -f "$test_file" ]; then
    echo "❌ MISSING: $test_file"
    exit 1
  fi
done
echo "✅ All test files present"
```

### Manual Verification
1. ✓ Count files: Must be exactly 4 files (2 .vue + 2 .spec.ts)
2. ✓ Both .vue files exist in correct directories
3. ✓ Both .spec.ts files exist alongside their respective components
4. ✓ Running unit test confirms all tests pass
5. ✓ Test output shows at least 3-5 tests per component
6. ✓ No test files are skipped or marked as pending

### If Validation Fails
**DO NOT PROCEED** to the next skill. Go back and create the missing test files immediately.

## Validation
After creating all files, validate:
1. ✓ Both .vue files exist in correct directories
2. ✓ Both .spec.ts files exist alongside their respective components
3. ✓ Running unit test confirms all tests pass
4. ✓ Test output shows at least 3-5 tests per component
5. ✓ No test files are skipped or marked as pending
