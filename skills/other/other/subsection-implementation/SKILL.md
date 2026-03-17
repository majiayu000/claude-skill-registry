---
name: subsection-implementation
description: Complete workflow for implementing a single subsection from the implementation plan. Orchestrates all project skills to ensure consistent, high-quality implementation with full test coverage. Use when implementing any subsection (e.g., 5.1.1, 5.2.3) to automate the entire workflow from requirements to commit.
license: MIT
metadata:
  version: "1.0.0"
  orchestrates: ["phase-implementation", "test-writing", "commit-format", "error-handling", "api-endpoint-implementation", "pre-commit-validation"]
  workflow: "clear-context → read-subsection → plan → implement → test → validate → document → commit"
---

# Subsection Implementation Workflow

This skill provides a complete, automated workflow for implementing a single subsection from `docs/implementation-plan.md`. It orchestrates all project skills to ensure consistent, high-quality implementation.

## Quick Start

To implement a subsection (e.g., 5.1.1):

```
/subsection-implementation 5.1.1
```

This will execute the entire workflow automatically.

## Complete Workflow

### Step 0: Clear Context (Fresh Start)

**Goal**: Start with a clean slate to avoid context pollution and ensure focused implementation.

**Actions**:
- Summarize current conversation state if needed
- Clear conversation history
- Focus only on the subsection to implement
- Load only relevant documentation and code

**Why**: Long conversations accumulate context that may interfere with focused implementation. Starting fresh ensures clarity.

---

### Step 1: Read Subsection Requirements

**Goal**: Understand what needs to be implemented.

**Actions**:
1. Read `docs/implementation-plan.md` for the specified subsection
2. Extract:
   - Subsection title and description
   - Implementation notes
   - Files to create/modify
   - Subsection tests (acceptance criteria)
   - Spec references
3. Identify dependencies on previous subsections
4. Verify prerequisites are complete

**Output**: Clear understanding of requirements and test expectations.

---

### Step 2: Create Implementation Plan

**Goal**: Break down the subsection into actionable tasks.

**Actions**:
1. Use `TaskCreate` to track implementation tasks:
   ```
   - Read and understand requirements
   - Implement code changes
   - Write subsection tests
   - Run quality checks
   - Update documentation
   - Commit and push
   ```
2. Mark tasks as `in_progress` when starting
3. Mark tasks as `completed` when done

**Pattern**: Follow `@skills/phase-implementation/SKILL.md` workflow

---

### Step 3: Implement Code

**Goal**: Write production code following project patterns.

**Actions**:
1. Create/modify files as specified in subsection
2. Follow project conventions:
   - Type hints on all functions
   - Docstrings (Google style)
   - Error handling with custom error codes (see `@skills/error-handling/SKILL.md`)
   - API endpoints follow pattern (see `@skills/api-endpoint-implementation/SKILL.md`)
3. Import required dependencies
4. Handle edge cases
5. Add logging where appropriate

**Patterns**:
- Domain models: Use Pydantic v2
- Services: Return `Result[T]` types with error codes
- API endpoints: Use FastAPI with proper status codes
- Error handling: Follow `@skills/error-handling/SKILL.md`

**Update task**: Mark "Implement code changes" as `completed`

---

### Step 4: Write Tests

**Goal**: Verify implementation meets all subsection test requirements.

**Actions**:
1. Read subsection tests from implementation plan
2. Write tests following `@skills/test-writing/SKILL.md`:
   - Test file: `tests/unit/<module>/test_<component>.py`
   - Test class: `class Test<ComponentName>`
   - Test method format: `def test_subsection_X_Y_Z_requirement(self) -> None:`
   - Include type annotations: `-> None`
3. Cover all subsection test cases listed in plan
4. Test success paths and error cases
5. Use descriptive test names
6. Follow Arrange-Act-Assert pattern

**Example**:
```python
def test_subsection_5_1_1_calls_llm_when_enabled(self) -> None:
    """Test subsection 5.1.1: Scout calls LLM when enabled."""
    # Arrange
    scout = ScoutAgent(llm_enabled=True)
    game_state = create_test_game_state()

    # Act
    result = scout.analyze(game_state)

    # Assert
    assert result.success is True
    assert result.data.llm_used is True
```

**Update task**: Mark "Write subsection tests" as `completed`

---

### Step 5: Run Quality Checks

**Goal**: Ensure code meets all quality standards before committing.

**Actions**:
1. Run linters:
   ```bash
   ruff check src/ tests/
   black --check src/ tests/
   ```
2. Run type checker:
   ```bash
   mypy --strict --explicit-package-bases src/
   ```
3. Run tests:
   ```bash
   pytest tests/ -v
   ```
4. Check coverage (if applicable):
   ```bash
   pytest tests/ --cov=src --cov-report=term-missing
   ```

**CRITICAL**: All checks must pass before proceeding. If any fail:
- Fix the issues immediately
- Re-run all checks
- Do not proceed until everything is green ✅

**Pattern**: Follow `@skills/pre-commit-validation/SKILL.md`

**Update task**: Mark "Run quality checks" as `completed`

---

### Step 6: Update Documentation

**Goal**: Mark subsection as complete and document implementation.

**Actions**:
1. Update `docs/implementation-plan.md`:
   - Add ✅ to subsection title
   - Add **Implementation Notes** section with key details:
     ```markdown
     **Implementation Notes:**
     - [Key implementation detail 1]
     - [Key implementation detail 2]
     - [Any deviations from plan]
     ```
   - Add **Subsection Tests** section with ✅:
     ```markdown
     **Subsection Tests** ✅:
     - ✅ [Test 1 description]
     - ✅ [Test 2 description]
     ```
   - Add **Test Coverage** section:
     ```markdown
     **Test Coverage** ✅:
     - **Subsection Tests**: ✅ X tests implemented and passing
     - **Test File**: ✅ `tests/unit/<module>/test_<component>.py`
     ```
2. Update any related documentation (API docs, architecture docs, etc.)

**Update task**: Mark "Update documentation" as `completed`

---

### Step 7: Commit and Push

**Goal**: Save work with a clear, descriptive commit message.

**Actions**:
1. Stage all changes:
   ```bash
   git add <files>
   ```
2. Create commit following `@skills/commit-format/SKILL.md`:
   ```
   <type>(<scope>): <Subsection X.Y.Z> - <description>

   - [Implementation detail 1]
   - [Implementation detail 2]

   Tests:
   - [List of subsection tests added]

   Files:
   - <file1>: <description>
   - <file2>: <description>
   ```
3. Common commit types:
   - `feat`: New feature/functionality
   - `fix`: Bug fix
   - `test`: Test-only changes
   - `refactor`: Code restructuring
   - `docs`: Documentation only

**Example**:
```
feat(agents): Subsection 5.1.1 - Scout LLM enhancement

- Integrate Pydantic AI for board analysis
- Add LLM fallback to rule-based logic
- Implement retry mechanism (3 attempts with exponential backoff)
- Add LLM call metadata logging

Tests:
- ✅ 8 subsection tests covering LLM integration
- ✅ Test LLM calls, fallback, retries, and logging

Files:
- src/agents/scout.py: Add LLM integration with fallback
- tests/unit/agents/test_scout_llm.py: Add subsection tests
- docs/implementation-plan.md: Mark 5.1.1 as complete
```

4. Push to remote:
   ```bash
   git push origin main
   ```

**CRITICAL**: Only commit after:
- ✅ All tests pass
- ✅ All linters pass
- ✅ Type checker passes
- ✅ Documentation updated
- ✅ Implementation verified to work

**Update task**: Mark "Commit and push" as `completed`

---

## Workflow Summary

```
1. Clear Context       → Start fresh
2. Read Requirements   → Understand subsection
3. Create Plan         → Track with TaskCreate
4. Implement Code      → Follow project patterns
5. Write Tests         → Verify requirements
6. Run Quality Checks  → Ensure standards (MUST PASS)
7. Update Docs         → Mark complete with notes
8. Commit & Push       → Save work with clear message
```

## Subsection Format

Subsections are identified by their numbering in the implementation plan:

- **Phase.Section.Subsection**: e.g., `5.1.1`, `5.2.3`, `6.0.1`
- **Title**: Descriptive name (e.g., "Scout LLM Enhancement")
- **Tests**: Listed as "Subsection Tests" in the plan
- **Implementation Notes**: Key details about implementation

## Quality Gates

**Before committing, all of these MUST be ✅:**

1. ✅ All subsection tests pass
2. ✅ All existing tests still pass (no regressions)
3. ✅ Linters pass (ruff, black)
4. ✅ Type checker passes (mypy --strict)
5. ✅ Documentation updated with ✅ markers
6. ✅ Implementation notes added to plan
7. ✅ Commit message follows format

**If any quality gate fails**: Fix issues and re-validate. Do not proceed.

## Best Practices

1. **One subsection at a time**: Never implement multiple subsections in one session
2. **Clear context first**: Always start fresh to avoid confusion
3. **Follow the plan**: Implement exactly what's specified in the subsection
4. **Test thoroughly**: Cover all listed subsection tests
5. **Document clearly**: Add implementation notes explaining key decisions
6. **Verify before commit**: Run all quality checks and ensure they pass
7. **Commit atomically**: One subsection = one commit
8. **Push immediately**: Share work with team right away

## Common Edge Cases

### When Subsection Tests Fail

1. Review test expectations in implementation plan
2. Debug implementation vs. requirements
3. Fix code or update requirements (if plan was wrong)
4. Document any deviations in Implementation Notes
5. Re-run all tests
6. Only proceed when all tests pass

### When Implementation Differs from Plan

1. Update the implementation plan to match reality
2. Document why the change was necessary in Implementation Notes
3. Ensure subsection tests still cover the requirements
4. Verify acceptance criteria are still met

### When Tests Reveal Design Issues

1. Fix the design issue first
2. Update implementation plan if requirements change
3. Update tests to match new design
4. Document lessons learned in Implementation Notes

### When Prerequisites Are Missing

1. Stop immediately
2. Identify which previous subsections must be completed first
3. Implement prerequisites in order
4. Return to original subsection after prerequisites are done

## Skills Integration

This skill orchestrates these existing skills:

- **@skills/phase-implementation/SKILL.md**: Overall implementation workflow
- **@skills/test-writing/SKILL.md**: Test patterns and conventions
- **@skills/commit-format/SKILL.md**: Commit message format
- **@skills/error-handling/SKILL.md**: Error handling patterns
- **@skills/api-endpoint-implementation/SKILL.md**: API endpoint patterns
- **@skills/pre-commit-validation/SKILL.md**: Quality checks before commit

Follow all patterns from these skills during implementation.

## Example: Complete Workflow for Subsection 5.1.1

**User**: `/subsection-implementation 5.1.1`

**AI Response**:

### Step 0: Clear Context
"Starting fresh implementation of subsection 5.1.1..."

### Step 1: Read Requirements
"Reading docs/implementation-plan.md section 5.1.1..."
- Title: Scout LLM Enhancement
- Files: src/agents/scout.py
- Tests: 8 subsection tests listed

### Step 2: Create Plan
"Creating task list..."
[Creates TaskCreate with 6 tasks]

### Step 3: Implement Code
"Implementing Scout LLM enhancement..."
[Modifies src/agents/scout.py with LLM integration]

### Step 4: Write Tests
"Writing subsection tests..."
[Creates tests/unit/agents/test_scout_llm.py with 8 tests]

### Step 5: Run Quality Checks
```bash
ruff check src/ tests/          # ✅ Pass
black --check src/ tests/       # ✅ Pass
mypy --strict src/              # ✅ Pass
pytest tests/ -v                # ✅ 8/8 passed
```

### Step 6: Update Documentation
[Updates docs/implementation-plan.md]:
- Adds ✅ to subsection 5.1.1
- Adds Implementation Notes
- Marks Subsection Tests as ✅

### Step 7: Commit & Push
```bash
git add src/agents/scout.py tests/unit/agents/test_scout_llm.py docs/implementation-plan.md
git commit -m "feat(agents): Subsection 5.1.1 - Scout LLM enhancement

- Integrate Pydantic AI for board analysis
- Add LLM fallback to rule-based logic
- Implement retry mechanism (3 attempts)
- Add LLM call metadata logging

Tests:
- ✅ 8 subsection tests covering LLM integration

Files:
- src/agents/scout.py: Add LLM integration with fallback
- tests/unit/agents/test_scout_llm.py: Add subsection tests
- docs/implementation-plan.md: Mark 5.1.1 as complete"

git push origin main
```

✅ **Subsection 5.1.1 Complete!**

---

## Usage

### Basic Usage

Implement a specific subsection:
```
/subsection-implementation 5.1.1
```

### Advanced Usage

With specific branch:
```
/subsection-implementation 5.1.1 --branch feature/scout-llm
```

With dry-run (show plan without executing):
```
/subsection-implementation 5.1.1 --dry-run
```

## Troubleshooting

### "Subsection not found"
- Check that subsection exists in `docs/implementation-plan.md`
- Ensure proper format (e.g., `5.1.1`, not `5-1-1`)

### "Prerequisites not complete"
- Check that previous subsections are marked ✅
- Implement prerequisites first

### "Tests failing"
- Review subsection test requirements in plan
- Debug implementation vs. requirements
- Fix issues before proceeding

### "Quality checks failing"
- Run checks individually to identify issue
- Fix linting/type errors
- Re-run until all checks pass
