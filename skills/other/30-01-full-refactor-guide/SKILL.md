---
name: 30-01-full-refactor-guide
description: Comprehensive guide for executing large refactors with incremental extraction, agent orchestration, wiring verification, and anti-pattern avoidance.
---

# 30.01 Guide: How To Do A Full Refactor Properly

## Prerequisites

Before starting a large refactor:

1. **Working test suite** - or at minimum, manual test checklist
2. **Clear target architecture** - know where code should end up
3. **Feature list** - every user-facing feature that must work after

## The Golden Rule

> **Refactoring is REPLACING code, not ADDING code alongside it.**

If you create `services/foo.service.ts` and the old inline implementation still exists, you haven't refactored - you've duplicated.

## Phase 1: Analysis

### 1.1 Map Current State

For each file being refactored:
- List every public function/method
- List every export
- List every side effect (scene.add, store updates, API calls)
- List every consumer (who imports this?)

### 1.2 Design Target State

- Where does each function move to?
- What are the new module boundaries?
- What are the dependency relationships?

### 1.3 Create Migration Table

| Function | Current Location | Target Location | Consumers |
|----------|------------------|-----------------|-----------|
| doThing | big-file.ts:450 | thing.service.ts | consumer-a, consumer-b |

## Phase 2: Incremental Extraction

### 2.1 One Function At A Time

For EACH function being moved:

```
1. Create the new location (if needed)
2. Copy the function to new location
3. Export it from new location
4. Update ALL consumers to import from new location
5. DELETE the old function
6. Verify: compiles AND feature works
7. Commit
```

**Critical: Steps 4 and 5 are not optional.**

### 2.2 Wire Services Immediately

If creating a service:

```typescript
// WRONG - creates service, nothing uses it
export function createFooService() { ... }
// consumer.ts - still has its own implementation
const doFoo = () => { ... } // DUPLICATE!
```

```typescript
// RIGHT - creates service AND wires it
export function createFooService() { ... }
// consumer.ts - USES the service
import { createFooService } from '../services/foo.service'
const foo = createFooService(deps)
// OLD doFoo DELETED
```

### 2.3 Verification After Each Step

After EVERY extraction:
1. Typecheck - compiles?
2. Tests - pass?
3. Run the app - feature works?

If any fail, fix before proceeding.

## Phase 3: Analysis Tools (Delphi/Oracle)

### When To Use Delphi

Delphi (parallel oracle consultation) is useful for:
- Understanding a complex codebase before refactoring
- Identifying all the pieces that need to move
- Creating an architecture guide

Delphi is NOT useful for:
- Actually doing the refactor (analysis ≠ implementation)
- Replacing the need for proper agent task design
- Generating code that will be used directly

**Delphi output must be REFERENCED in agent prompts, not just generated and forgotten.**

Bad Delphi usage:
```
1. Run Delphi to analyze codebase
2. Get architecture guide
3. Dispatch agents with vague "refactor this" prompts
4. Agents don't read the guide, do their own thing
```

Good Delphi usage:
```
1. Run Delphi to analyze codebase
2. Get architecture guide with specific function → file mappings
3. Convert guide into specific agent tasks:
   "Move doThing from big-file.ts:450 to thing.service.ts per guide section 4.2"
4. Include guide section reference in each prompt
```

## Phase 4: Subtask Agent Orchestration

A large refactor can use parallel subtask agents, but ONLY if orchestrated correctly.

### 4.1 Worktree Strategy

Create isolated worktrees for parallel work:

```bash
git worktree add .worktrees/services-layer -b refactor/services main
git worktree add .worktrees/features-layer -b refactor/features main
```

**Parallelizable work:**
- Independent modules that don't import each other
- File renames and barrel exports
- New directories/scaffolding

**NOT parallelizable (must be sequential):**
- Service creation AND service wiring (same files)
- Extracting code AND updating consumers (dependencies)
- Any two tasks that touch the same file

### 4.2 Agent Task Structure

Each agent gets ONE worktree and ONE complete unit of work:

```
AGENT TASK: [worktree path]

CONTEXT:
- What exists currently
- What the target state is
- What files this agent owns

REQUIREMENTS:
1. [Specific action]
2. [Specific action]

DELIVERABLES:
- [ ] File X created with functions A, B, C
- [ ] File Y updated to import from X
- [ ] File Y's old implementations DELETED
- [ ] Compiles
- [ ] Function A is called from [specific location]

DO NOT:
- Touch files outside your scope
- Create code that nothing imports
- Leave duplicate implementations
```

### 4.3 The Wiring Problem

WRONG approach:
```
Agent 1: "Create services/ with FooService"
Agent 2: "Create features/ with feature-handler.ts"

Result:
- services/foo.service.ts has doFoo()
- features/feature-handler.ts ALSO has doFoo()
- Nothing connects them
- Services deleted as "dead code"
```

RIGHT approach:
```
Agent 1: "Create services/ with FooService"
Agent 1: "Update feature-handler.ts to IMPORT and USE FooService"
Agent 1: "DELETE inline doFoo from feature-handler.ts"
```

**Rule: The agent that creates a service MUST also wire it in the same task.**

### 4.4 Sequential Dependency Chain

For dependent work, use a chain:

```
TASK 1 (Agent A):
- Create data-layer.ts with state Maps
- Wire: app.ts imports and uses data-layer Maps
- DELETE Maps from app.ts
- Commit

TASK 2 (Agent B, AFTER Task 1 completes):
- Create subscription-manager.ts
- Import data-layer Maps
- Move handlers from app.ts
- DELETE handlers from app.ts
- Commit
```

Each task: creates, wires, deletes, leaves codebase in working state.

### 4.5 Reviewer Agent Protocol

After implementation agents complete, dispatch SEPARATE reviewer agents:

```
REVIEWER TASK:

VERIFY:
1. Every new file is imported somewhere
   - rg "from.*[filename]" src/
   - If 0 results: FAIL - code not wired

2. No duplicate implementations
   - If found in both: FAIL - duplication

3. Old code deleted
   - If still present: FAIL - incomplete extraction

4. Features work
   - If broken: FAIL - regression

VERDICT: PASS / FAIL with specific issues
```

**Critical: "not imported" means SEND BACK TO WIRE, not "delete as dead code".**

### 4.6 The "10/10 Review" Trap

Agents rating their own work will give 10/10 if code compiles and follows patterns. They will NOT catch: code that's never imported, duplicate implementations, missing integration, broken features.

**Solution:** Review criteria must include:

```
HARD REQUIREMENTS (fail if not met):
- [ ] Every new file has at least 1 import (grep proof required)
- [ ] No function exists in both old and new location
- [ ] Application starts and [specific feature] works
```

## Phase 5: Integration Verification

### 5.1 Import Graph Verification

Every new file must be reachable from an entry point:

```bash
for f in src/services/*.ts; do
  imports=$(rg -c "from.*$(basename $f .ts)" src/ || echo 0)
  echo "$f: $imports imports"
done
```

If imports = 0 and it's new code, it's not wired.

### 5.2 Signs The Refactor Is Going Wrong

**ABORT if you see:**

1. **Multiple implementations appearing** - two agents created the same function
2. **New files with 0 imports** - wiring not happening
3. **Original file not shrinking** - code was copied, not moved
4. **Agents asking "should I proceed?"** - task was unclear
5. **Review scores are 10/10 but wiring is 0%** - reviews aren't checking integration

### 5.3 Rollback Strategy

```bash
# Worktrees make rollback easy
git worktree remove .worktrees/failed-refactor --force
git branch -D refactor/failed

# Or revert last N commits
git revert HEAD~N..HEAD
```

**Never:** Delete code that took significant compute to produce without understanding WHY it's not working.

## Phase 6: Session Handoff

If refactor spans multiple sessions:

```markdown
## Refactor State: YYYY-MM-DD HH:MM

COMPLETED:
- data-layer.ts created and wired (app.ts imports it)
- subscription-manager.ts created and wired

IN PROGRESS:
- feature-handler.ts created but NOT YET WIRED
- app.ts still has inline feature functions (lines 800-1100)

NEXT STEPS:
1. Wire feature-handler into app.ts
2. Delete lines 800-1100 from app.ts
3. Run app and test feature

DO NOT:
- Delete feature-handler.ts (it's not dead code, it's unfinished)
- Merge to main (not ready)
```

## Anti-Patterns

### 1. Scaffold Theater
Creating directory structures and empty/stub files without actual implementation or wiring.

### 2. Duplicate-And-Forget
Copying code to new location but leaving old code in place.

### 3. Review By Compilation
Assuming code works because it compiles.

### 4. Dead Code Confusion
Treating unfinished new code as dead code and deleting it.

### 5. Parallel Divergence
Multiple agents creating different implementations of the same thing.

## Checklist Before Declaring "Done"

```
[ ] Every function in migration table has been moved
[ ] Every old location has been updated or deleted
[ ] Every new file is imported by something
[ ] Compiles
[ ] Tests pass (if they exist)
[ ] Manual testing of all features passes
[ ] No duplicate implementations exist
[ ] git diff shows net REDUCTION in total code (or justified increase)
```

## Recovery From Failed Refactor

If refactor fails mid-way:

1. **Don't delete new code** - it may be unfinished, not dead
2. **Identify what's wired vs not** - grep for imports
3. **Complete the wiring** - update consumers to use new code
4. **Then delete old code** - only after wiring is complete
5. **Verify features work** - run the actual application
