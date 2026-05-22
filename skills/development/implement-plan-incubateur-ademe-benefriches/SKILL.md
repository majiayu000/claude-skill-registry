---
name: implement-plan
description: Implement a feature plan from a spec file, following test-first methodology and tracking all deliverables
user-invocable: true
---

# Implement Plan

Follow the phases below to implement the `Plan`, then `Report` the completed work.

IMPORTANT: If no plan is provided (i.e., $ARGUMENTS is empty or blank), STOP immediately and ask the user to provide one. Example usage: `/implement-plan specs/new-feature.md`

## Plan
$ARGUMENTS

---

## Phase 1: Parse Deliverables

Before writing any code, extract ALL deliverables from the plan:

1. Read the ENTIRE plan from start to finish
2. Find the "Files to Deliver" section (or extract from "Step by Step Tasks" if not present)
3. **Detect database work**: If the plan mentions any of these, use `/create-database-migration` skill:
   - Database migrations (new tables, columns, schema changes)
   - Updates to `tableTypes.d.ts`
   - SQL schema modifications
   - Data migrations
4. Create a structured inventory using TodoWrite:

   **Test Files** (will be implemented first):
   - Create a todo for each test file with format: "Create test: `path/to/file.spec.ts`"
   - Under each test file, note the test cases it must contain

   **Production Files** (will be implemented after tests):
   - Create a todo for each new file: "Create: `path/to/file.ts`"
   - Create a todo for each modification: "Modify: `path/to/file.ts` - <what to change>"

   **Validation**:
   - Create a todo for each validation command from the plan

5. Review the inventory: Does it capture EVERYTHING from the plan? If not, add missing items.

---

## Phase 2: Implement Tests First

For each test file in your inventory:

1. Mark the test todo as `in_progress`
2. Create the test file with ALL test cases described in the plan
3. Tests should initially fail (production code doesn't exist yet) - this is expected
4. Mark the test todo as `completed`

WHY TESTS FIRST:
- Tests act as a contract that forces production code to exist
- Forgotten tests = forgotten functionality (caught immediately)
- Provides deterministic verification that all production code is generated

---

## Phase 3: Implement Production Code

For each production file in your inventory:

1. Mark the file todo as `in_progress`
2. Implement the code following the plan's specifications
3. Run related tests to verify the implementation
4. Tests should now pass - if they don't, fix the implementation
5. Mark the file todo as `completed`

Continue until all production todos are complete AND all tests pass.

---

## Phase 4: Final Verification

Before reporting:

1. Re-read the plan's "Files to Deliver" or "Step by Step Tasks" section
2. Cross-check: Does every listed file exist?
3. Cross-check: Does every listed test case exist and pass?
4. Run ALL validation commands from the plan
5. If anything is missing, go back and complete it

---

## Report

Only after Phase 4 is complete:

1. Summarize the work in a concise bullet point list
2. Show files and lines changed: `git diff --stat`
3. Confirm: "All tests pass" and "All validation commands pass"
