---
name: write-plan
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive impelemntation plans assuming the developer has no expierence with the codebase. Document everything you think they need to know: which files
to touch for each task, applicable design patterns, reference documentation and how it should be tested. Produce a plan split into small bite-size tasks.

Follow DRY, YAGNI and TDD principles.

Commit early, commit often.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

## Bite-Sized Tasks

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Structure

**Save plans to:** `./plans/YYYY-MM-DD-<feature-name>.md`

```markdown
# [Feature Name] Implementation Plan

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Technology:** [Languages, frameworks and core technology]

## Tasks

### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.ts`
- Modify: `exact/path/to/existing.ts:123-145`
- Test: `tests/exact/path/to/test.ts`

1. **Step 1**, Write the failing test:
    ```typescript
    describe('test suite', () => {
        it('method under test should pass', async () => {
            // Arrange
            const params = ['a', '1', '2'];

            // Act
            const result = await methodUnderTest(param)

            // Assert
            expect(result).toBeDefined();
            expect(result).toBe('success');
        });
    });
    ```
2. **Step 2**, Run test to verify it fails:
    Run: `vitest path/to/specific.test.ts`
    Expected: FAIL

3. **Step 3**, Write minimal implementation:
    ```python
    function methodUnderTest(param: string[])
    {
        return 'success';
    }
    ```
4. **Step 4**, Run test to verify it passes:
    Run: `vitest path/to/specific.test.ts`
    Expected: PASS

5. **Step 5**, Commit:
    Commit the changes to git.

    ```bash
    git add tests/path/test.py src/path/file.py
    git commit -m "feat: add specific feature"
    ```

    Follow conventional commits message formatting (feat:, fix:, chore:, docs:, etc.)
```

## Common Mistakes

| Mistake                                                      | Solution                                                                                      |
|--------------------------------------------------------------|-----------------------------------------------------------------------------------------------|
| Not being specific about what file to edit, create or modify | Always use exact file paths                                                                   |
| Instructions are vague                                       | Always provide complete code in the plan (not "add validation" or non-specific instrtuctions) |
| Commands don't work, or contain syntax errors                | Always test shell commands for validity                                                       |
| Quality of generated code is low                             | Follow DRY, YAGNI, TDD with frequent commits                                                  |
