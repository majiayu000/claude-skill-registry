---
name: tdd-execution
description: Execute TDD workflow for user stories - spawn tester agent to write tests (RED), then coder agent to implement (GREEN). Use when executing stories in test-first discipline with parallel wave-based orchestration.
---

# TDD Execution Skill

**Purpose:** Execute test-driven development (TDD) pattern for enriched user stories
**Trigger:** Called by execution-phase or /build during story implementation
**Input:** User stories with acceptance criteria, execution plan with waves
**Output:** Tests written, implementation code, story files updated

**Core Principle:** RED and GREEN phases execute exclusively through agent spawning. The orchestrator spawns tester agent, waits for completion, then spawns coder agent. All test and implementation code is written by agents—never inline in orchestrator.

---

## TDD Pattern Overview

```
Per story:
  RED   → Spawn tester agent to write tests (wait for completion)
  GREEN → Spawn coder agent to implement (wait for completion)
  READY → Story completed with tests passing
```

---

## Workflow Steps

### 1. Per-Story TDD Execution

For each story in the current wave:

**a. RED Phase - Test Writing:**

1. Read story file (extract acceptance criteria, story ID, test path)
2. **SPAWN tester agent** (core-claude-plugin:generic:tester):
   - Write comprehensive test file from acceptance criteria
   - Include passing & failing test scenarios
   - Mock external dependencies
   - Update story: Status → 🧪 Testing
3. **WAIT for tester agent to complete** before proceeding to GREEN phase
4. Verify test file compiles (no passing yet)

**b. GREEN Phase - Implementation:**

1. **SPAWN coder agent** (core-claude-plugin:generic:coder) only after tester agent completes:
   - Read story file (AC, test file path)
   - Implement feature code to pass all tests
   - Update story: Status → 🔄 Implementing
   - Run tests until ALL pass
2. **WAIT for coder agent to complete**
3. Update story: Status → ✅ Complete
4. Record files modified for PM tracking

**c. Production Verification:**

1. Run test file one final time (confirm all pass)
2. Check AC checkboxes marked in story file
3. Mark story verified and ready for validation phase

### 2. Wave-Level Orchestration

- **Waves execute SEQUENTIALLY:** Complete all stories in Wave 1 before Wave 2
- **Stories within wave execute in PARALLEL:** Up to 10 concurrent tester→coder pairs
- **Serialized within story:** Tester completes BEFORE coder starts (RED→GREEN)

### 3. Story File Progress Updates

After each phase, update story file with:

```markdown
## Implementation Status

- Status: [🧪 Testing | 🔄 Implementing | ✅ Complete]
- Assignee: {agent-name}
- Test File: {path}
- Files Modified: {list}
- Tests Passing: {count}/{total}
```

### 4. Error Handling

- On tester failure: Log error, update story Status → ❌ Test Failed, continue
- On coder failure: Log error, update story Status → ❌ Implementation Failed, continue
- Validation phase handles retries and remediation

---

## Execution Logic

```
for each story in current_wave:
  // RED phase - Spawn tester, wait for completion
  tester_agent = spawn(tester, {story, AC})
  test_file = await tester_agent.write_tests()  // ALWAYS wait
  updateStoryFile(story, Status="🧪 Testing", TestFile=test_file)

  // Verify test file before proceeding
  compile_result = verify_test_compiles(test_file)
  ALWAYS_ASSERT(compile_result == success, "Tests must compile")

  // GREEN phase - Spawn coder ONLY after tester completes
  impl_agent = spawn(coder, {story, test_file})
  impl_files = await impl_agent.implement_to_pass_tests()  // ALWAYS wait
  updateStoryFile(story, Status="🔄 Implementing", FilesModified=impl_files)

  // Production verification
  test_result = run_tests(test_file)  // Must all pass
  ALWAYS_ASSERT(test_result == all_pass, "All tests must pass")
  updateStoryFile(story, Status="✅ Complete", Verified="yes")

return {
  story_id: story.id,
  test_file: test_file,
  impl_files: impl_files,
  tests_passed: all_tests_passed,
  status: "complete"
}
```

---

## Agent Spawning Templates

**Tester Agent Spawn (RED Phase):**

```
CONSTITUTION: 1) Change only what must change 2) Fix root cause 3) Read first
4) Verify before done 5) Do exactly what asked

ROLE: Tester Agent (TDD RED Phase)
TASK: Write tests from acceptance criteria

STORY: {story_id}
AC (Acceptance Criteria):
  {acceptance_criteria_list}

DELIVERABLE: Test file at {test_file_path}
  - Mock passing scenarios
  - Mock failing scenarios
  - Cover all AC points
  - No implementation code yet (RED phase)

VERIFY: Test file compiles and runs (no tests passing yet)
```

**Coder Agent Spawn (GREEN Phase):**

```
CONSTITUTION: 1) Change only what must change 2) Fix root cause 3) Read first
4) Verify before done 5) Do exactly what asked

ROLE: Coder Agent (TDD GREEN Phase)
TASK: Implement to pass all tests

STORY: {story_id}
AC (Acceptance Criteria):
  {acceptance_criteria_list}

TESTS: Must pass {test_file_path}
  - Run tests continuously
  - All tests MUST pass
  - Implement minimal code to pass
  - No over-engineering

DELIVERABLE: Implementation code at {impl_file_paths}
  - Code implements AC
  - All tests passing
  - List files modified

VERIFY: Run test file - confirm 100% passing
```

---

## Parallel Execution Limits

| Constraint     | Value | Rationale                      |
| -------------- | ----- | ------------------------------ |
| Max concurrent | 10    | Prevent resource exhaustion    |
| Wave batching  | Yes   | Control complexity             |
| Tester→Coder   | Seq   | RED before GREEN (TDD pattern) |
| Story→Story    | Par   | Parallelism within wave        |

---

## Output Format

```json
{
  "story_id": "prj-epc-001",
  "wave": 1,
  "tester_agent": "tester",
  "test_file": "src/__tests__/feature.test.ts",
  "tests_passed": true,
  "test_count": 8,
  "coder_agent": "coder",
  "impl_status": "success",
  "files_modified": ["src/feature.ts", "src/feature.spec.ts"],
  "ac_complete": true,
  "verified": true
}
```

---

## Wave Execution Example

```
Wave 1: Story prj-epc-001 (Authentication)
  1. Tester writes auth.test.ts (RED)
     - Mock User model
     - Mock login scenarios
     - Test passing & failing cases
  2. Coder implements AuthService (GREEN)
     - Read auth.test.ts
     - Implement login/logout
     - All 12 tests pass
  3. Production check: tests still passing

Wave 2: prj-epc-002 + prj-epc-003 (Parallel)
  Stories prj-epc-002 (Database) and prj-epc-003 (API) run in parallel:

  prj-epc-002:
    1. Tester writes db.test.ts (RED)
    2. Coder implements Repository (GREEN)

  prj-epc-003:
    1. Tester writes api.test.ts (RED)
    2. Coder implements Routes (GREEN)

  Both stories complete before Wave 3 starts
```

---

## Story File Integration

Story files (`prj-epc-001-add-authentication.md`) track progress:

```markdown
# prj-epc-001: Add Authentication

## Acceptance Criteria

- [ ] User can login with email + password
- [ ] User can logout
- [ ] Invalid credentials rejected

## Implementation Status

- Status: ✅ Complete
- Assignee: coder-agent
- Test File: src/**tests**/auth.test.ts
- Tests Passing: 12/12
- Files Modified: src/auth.ts, src/services/AuthService.ts
- Verified: yes

## Completion

- Tester: auth.test.ts written (8 tests)
- Coder: AuthService + login routes (4 files)
- Coverage: 95% (lines)
```

---

## Integration

**Called by:** execution-phase, /build command
**Calls:** Tester agent (core-claude-plugin:generic:tester), Coder agent (core-claude-plugin:generic:coder)
**Next:** Story file updates for validation-phase

---

## Success Criteria

- **ALWAYS spawn tester agent** to write all tests from acceptance criteria
- **ALWAYS wait for tester agent to complete** before spawning coder agent (RED → GREEN sequence)
- **ALWAYS spawn coder agent** to implement all feature code
- **ALWAYS wait for coder agent to complete** before marking story complete
- All tests passing after implementation
- Story files updated with progress
- Files modified tracked for PM
- Production verification passed
- **ALWAYS verify:** All tests written by spawned tester agent before any implementation code written
- **ALWAYS verify:** All implementation code written by spawned coder agent
- **ALWAYS verify:** Tester agent completes before coder agent spawns (sequential, never parallel)
