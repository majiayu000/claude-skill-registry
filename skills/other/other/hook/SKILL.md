---
name: hook
description: Use PROACTIVELY when you need to create, update, configure, or validate Claude hooks for various events and integrations
---

## 1. Context

- Main Objective: Create or update Claude Code hook scripts named $1 with requirements: $2
- Secondary Objective: Ensure hooks are properly linked in settings and follow security best practices
- User Input: [$1 = hook name, $2 = hook requirements/description]

## 2. Workflow

### Phase 1: Discovery & Analysis [P0]

- T001: Assess if you needed more context about hook specifications. If so, read `.claude/skills/hook/hooks.md` [P0]
- T002: Check if hook already exists in `.claude/hooks/` directory [P0]
- T003: Review `@.claude/settings.local.json` for existing hook configurations [P1]
- T004: Identify appropriate Claude Code events to hook into [P1]
- T005: Assess security and performance implications [P2]

### Phase 2: Implementation [P0]

- T006: Create new hook script OR update existing hook script in `.claude/hooks/` [P0]
- T007: Implement hook logic with proper error handling [P0]
- T008: Add logging and debugging capabilities [P1]
- T009: Create input validation and sanitization routines [P1]
- T010: Document hook behavior in script comments [P2]

### Phase 3: Configuration [P1]

- T011: Update `@.claude/settings.local.json` to link the hook [P0]
- T012: Configure appropriate event triggers [P1]
- T013: Set necessary permissions and access levels [P1]
- T014: Ensure compatibility with existing hooks [P2]

### Phase 4: Validation [P1]

- T015: Test hook execution without creating test files [P0]
- T016: Verify error handling and edge cases [P1]
- T017: Check for security vulnerabilities [P1]
- T018: Validate performance impact [P2]
- T019: Provide comprehensive report to main agent [P0]

## 3. Implementation Strategy

- For new hooks: Create script file in `.claude/hooks/` following naming convention
- For updates: Read existing hook, preserve working logic, apply requested changes
- Use Python or Bash depending on complexity requirements
- Implement idempotent operations where possible
- Follow existing hook patterns in the codebase for consistency
- Read `.claude/skills/hook-writer/hooks.md` for hook specifications PROACTIVELY

## 4. Constraints

- **Must** update `@.claude/settings.local.json` to link hooks
- **Must** test hooks after generation without creating test files
- **Never** create hooks that modify critical system files
- **Never** implement hooks with hardcoded credentials
- **Never** write hooks that can cause infinite loops
- **Never** bypass security validations or access controls
- **Never** create hooks without proper error handling
- **Never** create test files when testing hooks

## 5. Success Criteria

- Hook script exists and is syntactically valid
- Hook is properly linked in `settings.local.json`
- Hook executes successfully on target event
- Error handling covers common failure scenarios
- No security vulnerabilities detected
- Comprehensive report provided to main agent upon completion
