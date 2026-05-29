---
name: ticket-plan
description: Create detailed implementation plan from an approved design. Converts design document and prototype placeholders into step-by-step tasks for execution by Claude Code agents.
---

# Task Plan Creator

You are creating a detailed implementation plan from an approved design document. The plan will be executed by Claude Code agents via [ralphex](https://github.com/umputun/ralphex), so it must be detailed, unambiguous, and self-contained.

## Prerequisites

Before starting, verify that an approved design exists:

1. Look for `ai/tickets/YYYY-MM-DD-feature-name.md`
2. Check that frontmatter contains `status: approved`

**If no approved design exists:**
```
No approved design found for this feature.
Run /ticket-design first to create and approve a design, or specify the design file path.
```

**If design exists but not approved:**
```
Design exists but status is '[current-status]', not 'approved'.
Run /ticket-design to continue the design process.
```

## Output Location

Write the plan inside the existing design document: `ai/tickets/YYYY-MM-DD-feature-name.md`

Add a new section `# Implementation Plan` at the end of the design document (after `# Context`).

## Plan Structure

Add the following section to the design document:

```markdown
# Implementation Plan

## Overview
[2-4 sentences describing what will be implemented and why - derived from Problem Statement]

## Development Approach
- Complete each task fully before moving to the next
- Make small, focused changes
- **CRITICAL: all tests must pass before starting next task**
- **CRITICAL: update this plan when scope changes**

## Validation Commands
- `[test command]` - Run tests
- `[typecheck command]` - Type checking
- `[lint command]` - Linting (if applicable)

---

## Task 1: [Task Name]
- [ ] [Specific action item]
- [ ] [Another action item]
- [ ] Write/update tests for this task
- [ ] Run `[validation command]` - must pass before next task
- [ ] Stop and request user feedback before proceeding

---

## Task 2: [Task Name]
...

---

## Task [N-1]: Update documentation
- [ ] Update CLAUDE.md with new patterns/conventions (if applicable)
- [ ] Add inline documentation for complex functions
- [ ] Update API documentation (if applicable)

---

## Task [Final]: Cleanup design artifacts
- [ ] Remove all `DESIGN PROTOTYPE: YYYY-MM-DD-feature-name.md` comments from codebase
- [ ] Delete any empty scaffold files that were replaced
- [ ] Update design document status to `implemented`
- [ ] Verify no prototype markers remain: `grep -r "DESIGN PROTOTYPE: YYYY-MM-DD-feature-name" src/`
- [ ] Run `bun test:all` and `bun run typecheck` - final verification

---

## Post-Completion Verification
1. **Functional test**: [Describe how to manually test the feature]
2. **Edge case test**: [Test a specific edge case manually]
3. **Integration check**: [Verify integration with existing features]
4. **No regressions**: All existing tests pass
5. **Cleanup verified**: No DESIGN PROTOTYPE comments remain
```

---

## Your Process

### Phase 1: Load Design Context

1. Read the approved design document completely
2. Read all prototype placeholder files listed in `prototype-files` frontmatter
3. Understand:
   - The problem being solved (from Problem Statement)
   - The chosen approach and rationale (from Proposed Approach, Key Decisions)
   - All affected files (from Affected Components)
   - Technical details (from Technical Details)
   - Edge cases identified (from Edge Cases and Error Handling)
   - Test cases planned (from Test Cases)
   - Review notes (from AI Review Notes)

### Phase 2: Analyze Prototype Placeholders

For each file with `DESIGN PROTOTYPE: <design-file>` markers:

1. Identify what changes are outlined
2. Determine dependencies between changes
3. Note what each prototype outlines and its dependencies
4. Order tasks so dependencies are satisfied

### Phase 3: Read Code Style Guide

Read `.claude/code-style.md` before planning any file/module structure. The style guide governs:
- When to create new files vs. extend existing ones (Separation of Concerns, File Creation rules)
- Module responsibilities and public interface design
- Code formatting and naming conventions

**Every task that creates or restructures files must comply with the code style guide.** If the plan calls for a "shared helpers" file, verify each helper belongs together by responsibility — don't create dump files that mix unrelated concerns.

### Phase 4: Explore the Existing Codebase

You cannot write a good plan from the design document alone. You must understand the actual code that will be modified or extended.

Use Task agents (subagent_type=Explore) to explore in parallel:

1. **Existing patterns**: Read the most similar existing converter/module that the new code will follow. Understand its structure, helper functions, error handling patterns, and test patterns.
2. **Shared infrastructure**: Identify what helper functions, utilities, and types already exist that the new code will reuse. Note which ones need extraction/parameterization.
3. **Types and interfaces**: Check generated types, existing converters, config types — know exactly what exists vs. what needs to be created.
4. **Test infrastructure**: Read an existing test file of the same kind (unit, integration) to understand patterns, helpers, and setup.

This exploration directly informs task granularity. Without it, you'll write vague tasks that bundle unrelated work.

### Phase 5: Create Task Breakdown

Convert the design into discrete, ordered tasks.

**The #1 rule: each task = one reviewable concern.** A task should do ONE thing that a reviewer can evaluate in isolation. If you find yourself writing a task with 3 unrelated bullet points, split it.

**Splitting heuristics**:
- **One file with 3+ distinct changes** (e.g., core fields, conditional fields, identifiers, performers) → split into separate tasks, one per concern
- **Each new preprocessor/handler/converter** → its own task with its own tests
- **Infrastructure** (config, types, routing) → separate task from implementation that uses it
- **Shared code extraction/refactoring** → separate task before tasks that use the shared code
- **Interface/contract definition** → separate task from implementation

**Task sizing target**: 3-7 checkboxes per task. If you have 8+, try to look for a split point.

**It is normal for large features to have 15-30 tasks.** Do not try to compress into fewer tasks. Small, focused tasks are easier to review and easier to implement correctly.

**Task ordering principles:**
- Types/interfaces before implementations
- Shared code extraction before consumers
- Infrastructure (config, routing) before feature code
- Core logic before extensions/edge cases
- Each unit of implementation alongside its tests
- Integration tests after all components exist
- Documentation second-to-last
- Cleanup last

### Phase 6: Write the Implementation Plan

Add `# Implementation Plan` section to `ai/tickets/YYYY-MM-DD-feature-name.md` with:

1. Overview derived from design's Problem Statement
2. Development approach guidelines
3. Validation commands appropriate for this project
4. Detailed tasks with specific checkboxes (one concern per task)
5. Documentation task (second-to-last)
6. Cleanup task to remove prototype placeholders (last)
7. Post-completion verification steps

### Phase 7: Verify Plan Quality

Critically and thoroughly review the plan before presenting to user:

- Plan is written inside the design document under `# Implementation Plan`
- Every affected file from design's Affected Components is covered in tasks
- Every prototype placeholder location has a corresponding task
- Tasks are ordered so dependencies are satisfied
- Each task covers ONE reviewable concern (not multiple unrelated changes)
- Every task ends with validation gate
- Tasks reference design's Technical Details for implementation specifics
- Tasks reference design's Edge Cases for error handling
- Tasks cover ALL test cases mentioned in the design document
- There's a task focused on documentation updates (CLAUDE.md, docs, user guides, inline comments)
- There's a task focused on cleaning up all DESIGN PROTOTYPE markers
- Post-completion verification steps are defined

### Phase 8: Update the document status

Change the design document status to `planned`.

---

## Task Writing Guidelines

### Good Task Structure (focused, one concern)

```markdown
### Task 5: Implement JWT token validation

- [ ] Create `src/middleware/validate-jwt.ts` with `validateJWT()` function
- [ ] Validate token signature and expiration from Authorization header
- [ ] Return structured error with 401 for missing/invalid, 403 for expired
- [ ] Write unit tests: valid token, expired token, malformed token, missing header
- [ ] Run `bun test:all` and `bun run typecheck` - must pass before next task
- [ ] Stop and request user feedback before proceeding
```

```markdown
### Task 6: Wire JWT middleware into protected routes

- [ ] Add `validateJWT` middleware to protected routes in `src/routes/index.ts`
- [ ] Write integration test for protected endpoint (valid token → 200, no token → 401)
- [ ] Run `bun test:all` and `bun run typecheck` - must pass before next task
- [ ] Stop and request user feedback before proceeding
```

### Bad: Too vague

```markdown
### Task 3: Add auth
- [ ] Implement authentication
- [ ] Add tests
```

### Bad: Bundles multiple concerns (should be 3+ tasks)

```markdown
### Task 3: Implement auth middleware, session management, and route protection
- [ ] Create JWT validation function
- [ ] Create session store with Redis
- [ ] Add login/logout endpoints
- [ ] Wire middleware into routes
- [ ] Write 15 unit tests covering all scenarios
- [ ] Write integration tests
```

### Checkbox Guidelines

Each checkbox should be:
- **Specific**: Name exact files, functions, endpoints
- **Verifiable**: Clear success criteria
- **Atomic**: One logical action per checkbox
- **Ordered**: Later checkboxes may depend on earlier ones

Include checkboxes for:
- Implementation steps (reference prototype placeholder locations)
- Test creation/updates
- Error handling (reference design's Edge Cases section)
- Edge case coverage
- Documentation updates (inline comments for complex logic)

---

## Testing Requirements

Every task MUST include testing checkboxes:

```markdown
- [ ] Write unit tests for [specific function/module]
- [ ] Write integration tests for [specific flow]
- [ ] Add test cases for edge cases: [list them]
- [ ] Run `[test command]` - must pass before next task
```

Test coverage should include:
- Happy path scenarios
- Error conditions
- Edge cases (empty inputs, boundary values, concurrent access)
- Integration with adjacent components

---

## Converting Prototype Placeholders to Tasks

### From new file scaffold:

**Prototype:**
```typescript
// ═══════════════════════════════════════════════════════════════════════════
// DESIGN PROTOTYPE: 2026-01-28-feature.md
// ═══════════════════════════════════════════════════════════════════════════
//
// export interface UserSession { ... }
// export function createSession(userId: string): UserSession
// export function validateSession(token: string): boolean
```

**Task:**
```markdown
### Task 2: Implement session management module

- [ ] Replace prototype scaffold in `src/session/manager.ts` with actual implementation
- [ ] Implement `UserSession` interface as specified in design's Technical Details
- [ ] Implement `createSession()` function with JWT generation
- [ ] Implement `validateSession()` function with expiry checking
- [ ] Export all public types and functions
- [ ] Write unit tests in `src/session/manager.test.ts`
- [ ] Run `bun test:all` and `bun run typecheck` - must pass before next task
```

### From inline markers:

**Prototype:**
```typescript
// DESIGN PROTOTYPE: 2026-01-28-feature.md
// Add parameter → mappingType: MappingTypeName = "loinc"
export function generateConceptMapId(sender: SenderContext): string {
```

**Task:**
```markdown
### Task 4: Update generateConceptMapId for multiple mapping types

- [ ] Add `mappingType: MappingTypeName = "loinc"` parameter to `generateConceptMapId()`
- [ ] Import `MappingTypeName` from `src/code-mapping/mapping-types.ts`
- [ ] Use `MAPPING_TYPES[mappingType].conceptMapSuffix` instead of hardcoded `-to-loinc`
- [ ] Update all existing call sites (should work with default parameter)
- [ ] Add unit tests for new parameter with different mapping types
- [ ] Run `bun test:all` and `bun run typecheck` - must pass before next task
```

---

## Validation Commands

Always include commands that verify correctness. Get these from the project's CLAUDE.md or package.json:

```markdown
## Validation Commands
- `bun test:all` - Run all tests
- `bun run typecheck` - Type checking
- `bun run lint` - Linting (if applicable)
- `bun run build` - Verify build succeeds (if applicable)
```

