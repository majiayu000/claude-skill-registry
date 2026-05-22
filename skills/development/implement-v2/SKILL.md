---
name: implement
description: Implement features using Test-Driven Development (TDD). Executes red-green-refactor cycle, uses bmad-commands for file operations and testing, verifies acceptance criteria. This skill should be used when implementing new features or functionality from task specifications with test coverage.
acceptance:
  - tests_passing: "All tests must pass"
  - coverage_threshold: "Test coverage >= 80%"
  - no_syntax_errors: "Code must have no syntax errors"
  - task_spec_loaded: "Task specification must be successfully loaded"
  - all_requirements_met: "All acceptance criteria from task spec must be met"
inputs:
  task_id:
    type: string
    required: true
    description: "Task identifier (e.g., task-auth-002)"
    validation: "Must match pattern: task-{component}-{number}"
outputs:
  implementation_complete:
    type: boolean
    description: "Whether implementation is complete and meets all criteria"
  test_coverage_percent:
    type: number
    description: "Test coverage percentage achieved"
  files_modified:
    type: array
    description: "List of files created or modified"
  tests_passed:
    type: boolean
    description: "Whether all tests passed"
telemetry:
  emit: "skill.implement.completed"
  track:
    - task_id
    - test_coverage_percent
    - duration_ms
    - files_modified_count
    - tests_total
    - tests_passed
    - tests_failed
---

# Implement Feature with TDD

## Overview

Implement features following strict Test-Driven Development workflow. Uses bmad-commands for deterministic file and test operations, ensures acceptance criteria are met through automated verification.

**TDD Cycle:**
1. **RED**: Write failing tests
2. **GREEN**: Implement code to pass tests
3. **REFACTOR**: Improve code while keeping tests green

## Prerequisites

- Task specification exists at `workspace/tasks/{task_id}.md`
- bmad-commands skill available at `.claude/skills/bmad-commands/`
- Development environment configured
- Test framework installed (Jest or Pytest)

---

## Workflow

### Step 0: Load Task Specification

**Action:** Use `read_file` command to load task spec.

```bash
python .claude/skills/bmad-commands/scripts/read_file.py \
  --path workspace/tasks/{task_id}.md \
  --output json
```

**Parse Response:**
- Extract `outputs.content` for task specification
- Verify `success == true`
- Parse task spec sections:
  - Objective
  - Acceptance Criteria
  - Technical Specifications
  - Required Files

**Required Sections in Task Spec:**
```markdown
## Objective
[What to build]

## Acceptance Criteria
1. [Testable requirement 1]
2. [Testable requirement 2]

## Technical Specifications
- API endpoints
- Data models
- Dependencies
- File locations

## Required Files
- src/path/to/implementation.ts
- tests/path/to/tests.test.ts
```

**If task spec not found or invalid:**
- Return error with message
- Suggest creating task spec first
- Halt implementation

---

### Step 0.5: Check for External Packages and Fetch Documentation

**CRITICAL STEP:** Before writing any code, identify external packages and fetch current documentation.

**Why This Step is Essential:**
- Training data may be outdated
- Package APIs change between versions
- Prevents using deprecated or removed methods
- Ensures compatibility with installed version

**Action 1: Identify External Packages**

Scan task specification and requirements for package mentions:
- npm packages (JavaScript/TypeScript)
- PyPI packages (Python)
- Go modules
- Maven/Gradle dependencies (Java)
- Crates (Rust)
- NuGet packages (.NET)

**Action 2: Check Installed Versions**

```bash
# JavaScript/TypeScript
cat package.json | grep "package-name"
cat package-lock.json | grep -A 5 "package-name"

# Python
cat requirements.txt | grep package-name
pip show package-name

# Go
cat go.mod | grep package-name

# Rust
cat Cargo.toml | grep package-name
```

**Action 3: Fetch Official Documentation**

Use WebFetch tool to get current documentation:

**JavaScript/TypeScript packages:**
```
WebFetch(
  url: "https://www.npmjs.com/package/{package-name}",
  prompt: "Extract: installation, main API methods, usage examples, version compatibility"
)

# Or check official docs
WebFetch(
  url: "{official-docs-url}",
  prompt: "Extract: API reference for version {version}, method signatures, parameters, return types"
)
```

**Python packages:**
```
WebFetch(
  url: "https://pypi.org/project/{package-name}/",
  prompt: "Extract: installation, API reference, examples for version {version}"
)

WebFetch(
  url: "https://{package}.readthedocs.io/en/stable/",
  prompt: "Extract: API documentation, class methods, function signatures"
)
```

**Go modules:**
```
WebFetch(
  url: "https://pkg.go.dev/{module-path}",
  prompt: "Extract: package documentation, function signatures, examples"
)
```

**Action 4: Verify API Compatibility**

Compare fetched documentation with task requirements:
- Confirm method names exist
- Verify parameter types match
- Check return types
- Note any deprecated methods
- Identify breaking changes from older versions

**Action 5: Document Findings**

Add comments in code referencing documentation:
```typescript
// Using axios@1.6.0
// Docs: https://axios-http.com/docs/api_intro
// Method: axios.get(url, config) returns Promise<AxiosResponse>
import axios from 'axios';
```

**If Package is Unfamiliar:**
- Spend 5-10 minutes reviewing documentation
- Understand core concepts and patterns
- Review example code
- Note common pitfalls
- Prefer official examples over training data

**Common Documentation Sources:**

| Language | Primary Source | Secondary Source |
|----------|---------------|------------------|
| JavaScript/TS | npmjs.com, official docs | TypeScript definitions |
| Python | PyPI, Read the Docs | Official package docs |
| Go | pkg.go.dev | godoc |
| Java | Maven Central | Javadoc |
| Rust | docs.rs | crates.io |
| .NET | NuGet | Microsoft Docs |

**If Documentation Not Found:**
- Check package repository (GitHub, GitLab)
- Look for README.md
- Check CHANGELOG for version-specific changes
- Search for migration guides
- Escalate to user if critical package lacks documentation

---

### Step 1: Analyze Requirements

**Action:** Break down acceptance criteria into test cases.

For each acceptance criterion:
1. Identify what needs to be tested
2. Determine test type (unit/integration/e2e)
3. Plan test structure
4. Identify edge cases

**Example:**
```
Acceptance Criterion: "User can log in with valid credentials"

Test Cases:
- [Unit] Should return user object when credentials valid
- [Unit] Should return null when email not found
- [Unit] Should return null when password incorrect
- [Integration] Should create session when login successful
- [Integration] Should not create session when login fails
```

Reference `references/tdd-workflow.md` for detailed TDD patterns and best practices.

---

### Step 2: RED Phase - Write Failing Tests

**Action:** Write tests that cover all acceptance criteria.

**Test Structure:**
```typescript
// tests/auth/login.test.ts
describe('AuthService.login', () => {
  // Happy path
  it('should return user when credentials valid', async () => {
    // Arrange
    // Act
    // Assert
  });

  // Error cases
  it('should return null when email not found', async () => {
    // ...
  });

  it('should return null when password incorrect', async () => {
    // ...
  });

  // Edge cases
  it('should handle empty email', async () => {
    // ...
  });
});
```

**Run Tests:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Verify RED Phase:**
- Tests should fail (NOT pass)
- Failures should be for the right reason (not syntax errors)
- Parse response: `outputs.passed == false`

**If tests pass in RED phase:**
- Tests are not valid (already passing code exists)
- Refine tests to be more specific
- Verify testing the right functionality

---

### Step 3: GREEN Phase - Implement Code

**Action:** Write minimum code to make tests pass.

**Focus on:**
- Making tests pass (not elegance)
- Implementing simplest solution
- Following TDD cycle strictly

**Implementation Pattern:**
```typescript
// src/auth/login.ts
export class AuthService {
  async login(email: string, password: string): Promise<User | null> {
    // Step 1: Find user
    const user = await this.userRepository.findByEmail(email);
    if (!user) return null;

    // Step 2: Verify password
    const valid = await this.passwordService.verify(password, user.passwordHash);
    if (!valid) return null;

    // Step 3: Return user
    return user;
  }
}
```

**Run Tests:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Verify GREEN Phase:**
- Parse response: `outputs.passed == true`
- Check `outputs.coverage_percent >= 80`
- Verify `outputs.failed_tests == 0`

**If tests still failing:**
- Review failure messages
- Fix implementation
- Re-run tests
- Repeat until GREEN

---

### Step 4: REFACTOR Phase

**Action:** Improve code quality while keeping tests green.

**Refactoring Targets:**
- Remove duplication
- Improve naming
- Extract functions/methods
- Simplify conditionals
- Add type safety
- Improve error handling

**After Each Refactor:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Verify tests stay green:**
- `outputs.passed == true` after each refactor
- If tests break, revert refactor
- Only commit refactors that keep tests green

Reference `references/refactoring-patterns.md` for common refactoring patterns and techniques.

---

### Step 5: Verify Acceptance Criteria

**Action:** Check that all acceptance criteria from task spec are met.

For each acceptance criterion:
1. Identify corresponding tests
2. Verify tests pass
3. Verify behavior matches requirement
4. Check edge cases covered

**Automated Verification:**
```bash
# Run full test suite
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Check:**
- `outputs.passed == true`
- `outputs.coverage_percent >= 80`
- `outputs.total_tests >= expected_count`
- All acceptance criteria have corresponding passing tests

**Manual Verification:**
- Review code against technical specifications
- Verify API contracts match
- Check data models are correct
- Ensure error handling is complete

---

### Step 6: Final Validation

**Action:** Run comprehensive checks before completion.

**Checks:**
1. All tests passing
2. Coverage >= 80%
3. No syntax errors
4. No linting errors
5. All files created as specified
6. Code follows project standards

**Run Tests One Final Time:**
```bash
python .claude/skills/bmad-commands/scripts/run_tests.py \
  --path . \
  --framework auto \
  --output json
```

**Acceptance Criteria Verification:**
- ✅ `tests_passing`: `outputs.passed == true`
- ✅ `coverage_threshold`: `outputs.coverage_percent >= 80`
- ✅ `no_syntax_errors`: No syntax errors in output
- ✅ `task_spec_loaded`: Task spec was successfully loaded in Step 0
- ✅ `all_requirements_met`: All acceptance criteria verified in Step 5

---

## Output

Return structured output with telemetry:

```json
{
  "implementation_complete": true,
  "test_coverage_percent": 87,
  "files_modified": [
    "src/auth/login.ts",
    "tests/auth/login.test.ts"
  ],
  "tests_passed": true,
  "telemetry": {
    "skill": "implement",
    "task_id": "task-auth-002",
    "duration_ms": 45000,
    "files_modified_count": 2,
    "tests_total": 12,
    "tests_passed": 12,
    "tests_failed": 0,
    "coverage_percent": 87
  }
}
```

---

## Error Handling

If any step fails:

1. **Task Spec Not Found:**
   - Error: "Task specification not found at workspace/tasks/{task_id}.md"
   - Action: Create task spec first

2. **Tests Failing:**
   - Error: "Tests failing after implementation"
   - Action: Review test failures, fix code, re-run

3. **Coverage Below Threshold:**
   - Error: "Test coverage {actual}% below threshold 80%"
   - Action: Add more tests to increase coverage

4. **Syntax Errors:**
   - Error: "Syntax errors detected in implementation"
   - Action: Fix syntax errors, re-run tests

---

## References

Detailed documentation in `references/`:

- **tdd-workflow.md**: Complete TDD workflow with patterns
- **refactoring-patterns.md**: Common refactoring techniques
- **testing-best-practices.md**: Testing patterns and anti-patterns
- **acceptance-criteria-guide.md**: Writing good acceptance criteria

---

## Using This Skill

**From James subagent:**
```bash
@james *implement task-auth-002
```

**Directly:**
```bash
Use .claude/skills/development/implement-v2/SKILL.md with input {task_id: "task-auth-002"}
```

**With Orchestrator:**
Orchestrator calls this skill automatically during delivery workflow.

---

## Philosophy

This skill embodies BMAD's 3-layer architecture:

- **Uses Commands**: bmad-commands for read_file, run_tests
- **Provides Composition**: Sequences commands into TDD workflow
- **Enables Orchestration**: Called by James subagent with routing

By using commands, this skill is:
- **Observable**: Telemetry at every step
- **Testable**: Commands have known contracts
- **Composable**: Can be used by other workflows
- **Reliable**: Deterministic command behavior
