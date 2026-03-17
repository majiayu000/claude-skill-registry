---
name: test-runner-java-gradle
description: a definition of tests and testing in a Java project using Gradle and JUnit 5
---

# Skill: Project Test Runner (Java + Gradle, macOS, JUnit 5 Only)

This skill defines what a "test" is and how tests are executed for this Java project.
It is designed to be used together with a TDD skill that determines *when* tests must run.

Language: Java
Test framework: JUnit 5 (Jupiter)
Detailed test output: XML files under `build/test-results/<testType>/TEST-*.xml`

IMPORTANT: NEVER write test scripts that use `gradlew bootRun`. Direct testing of Java applications done using `./gradlew test/check` only.

---

## 1. Test Types and Source Sets

This project uses multiple test types with separate source sets, executed in order:

| Test Type | Task | Source Directory | Purpose |
|-----------|------|------------------|---------|
| Unit | `./gradlew test` | `src/test/java` | Fast, isolated tests with mocked dependencies |
| Integration | `./gradlew integrationTest` | `src/integrationTest/java` | Tests with real external systems (databases, message brokers) via testcontainers |
| Component | `./gradlew componentTest` | `src/componentTest/java` | Single service tested as a Docker container |
| End-to-End | `./gradlew endToEndTest` | `src/endToEndTest/java` | Full application with multiple services |

### Execution Order

```
test → integrationTest → componentTest → endToEndTest
```

All test types are wired to the `check` task. Running `./gradlew check` executes all test types in order.

### When to Use Each Test Type

- **Unit tests**: Business logic, domain objects, service methods with mocked dependencies
- **Integration tests**: Repository tests with real database, Kafka producer/consumer with real broker
- **Component tests**: HTTP API tests against a containerized service, service behavior verification
- **End-to-end tests**: Cross-service workflows, user journey tests

---

## 2. Definition of a Test

A test in this project is:

- A Java method annotated with `@org.junit.jupiter.api.Test`
- Located in the appropriate source directory for its test type
- Part of a test class following normal JUnit 5 structure

Examples of valid test locations:
- `src/test/java/com/example/MyServiceTest.java` (unit test)
- `src/integrationTest/java/com/example/MyRepositoryIntegrationTest.java` (integration test)
- `src/componentTest/java/com/example/MyServiceComponentTest.java` (component test)
- `src/endToEndTest/java/com/example/OrderWorkflowE2ETest.java` (end-to-end test)

JUnit 5 assertions (e.g., `Assertions.assertEquals`, `assertThrows`) should be used.

No Kotlin and no JUnit 4 are present in this project.

---

## 3. Running Tests

### Incremental Testing Workflow

Tests are run incrementally, progressing from fast/isolated to slow/integrated:

1. **TDD Loop**: Run unit tests frequently during development
   ```
   ./gradlew test
   ```

2. **After unit tests pass**: Run integration tests
   ```
   ./gradlew integrationTest
   ```

3. **After integration tests pass**: Run component tests
   ```
   ./gradlew componentTest
   ```

4. **Before commit/PR**: Run all tests
   ```
   ./gradlew check
   ```

This progression provides fast feedback during development while ensuring full coverage before committing.

### Specific Test Types

```
./gradlew test              # Unit tests only
./gradlew integrationTest   # Integration tests only
./gradlew componentTest     # Component tests only
./gradlew endToEndTest      # End-to-end tests only
./gradlew check             # All test types in order
```

All commands must be run from the project root (the directory containing `gradlew`).

### Gradle Daemon

Do not use the `--no-daemon` flag with Gradle commands unless specifically troubleshooting daemon issues. The Gradle daemon improves build performance by keeping the JVM warm between builds.

### Avoid Clean Builds

Use `./gradlew build`, not `./gradlew clean build`. Gradle's incremental build correctly detects changes. Only use `clean` when:
- Explicitly debugging build cache issues
- User specifically requests it

### Gradle Wrapper

When creating a standalone Gradle project, use the `gradle wrapper` command to generate wrapper files instead of copying them from another project:

```bash
cd new-project-directory
gradle wrapper --gradle-version 8.11.1
```

This is cleaner than copying `gradle/`, `gradlew`, and `gradlew.bat` files and avoids permission issues.

### Output Filtering

Do not use output filtering with Gradle commands (no `| tail`, `| head`, or `2>&1` redirection). Gradle's console output is already concise - just task names and pass/fail status. Verbose test output (Hibernate SQL, Spring Boot logs, etc.) is captured in `TEST-*.xml` files, not streamed to the console.

### Test Verification Commands

- Use `./gradlew check` to verify changes - this runs all test types (unit, integration, component tests)
- Use `./gradlew test` only when specifically running unit tests in a TDD loop
- `./gradlew test` only runs unit tests and misses integration/component tests
- NEVER just compile tests to verify they work - always run them

### Definition of Done for Code Changes

For any code modification task (refactoring, bug fixes, new features):
- Compilation passing is a prerequisite, not success
- Success = `./gradlew build` passes (includes all tests)

### Test Coverage for Refactoring

When performing refactoring tasks (renaming classes, methods, moving files, changing signatures), always run the full test suite (`./gradlew check`) without excluding any test categories. Refactoring can break:

- Integration tests that reference renamed classes in configuration
- Component tests that verify service interactions
- End-to-end tests that may have references to renamed elements

Only exclude test categories when explicitly instructed by the user or when debugging a specific test failure.

Exit code meaning:
- Exit code 0 → all tests passed
- Non-zero exit code → tests failed or tests could not run due to build errors

The console output of Gradle indicates only overall success or failure, not individual test results.

### Build Success Is Authoritative

When `./gradlew build` succeeds (BUILD SUCCESSFUL), that is authoritative proof that all tests passed. Do not:
- Read TEST*.xml files to "verify" results
- Parse build/reports for confirmation
- Run additional commands to check test outcomes

TEST*.xml and HTML reports are for human debugging, not for Claude verification.

---

## 4. Detailed Test Results (XML)

Detailed per-test results are located in test-type-specific directories:

```
build/test-results/test/TEST-*.xml              # Unit tests
build/test-results/integrationTest/TEST-*.xml   # Integration tests
build/test-results/componentTest/TEST-*.xml     # Component tests
build/test-results/endToEndTest/TEST-*.xml      # End-to-end tests
```

Each XML file corresponds to a test class and contains:
- `<testsuite>` metadata such as total tests and failures
- `<testcase classname="..." name="...">` elements
- Optional `<failure>` elements that contain the failure message and stack trace snippet

The agent must extract:
- The first failing test class name
- The failing test method name
- The failure message text
- A useful stack trace snippet if present

This information must be used to explain why tests failed and guide the next RED → GREEN change.

---

## 5. Evidence Integration (for the TDD skill)

The TDD skill uses an Evidence block with fields:
- `tests: pass | fail | not-run`
- `last_output: <text>`

This Test Runner skill defines how to populate those fields.

When tests pass:
- `tests: pass`
- `last_output` should mention that `./gradlew test` exited with code 0

When tests fail:
- `tests: fail`
- `last_output` should mention that `./gradlew test` exited with a non-zero code
- The agent must parse XML files (from `build/test-results/test/`) and describe the failing test(s)

When tests cannot run (environment error):
- `tests: not-run`
- `last_output` should say that Gradle could not be executed
- The agent must enter the BLOCKED state (as defined by the TDD skill)

---

## 6. Rules for the Coding Agent

1. Follow the incremental testing workflow: unit → integration → component
2. Before committing, run all tests using: `./gradlew check`
3. The agent must not guess test results from reading code
4. The agent must never claim tests passed without real Gradle output
5. The agent must parse XML under `build/test-results/<testType>` to identify failing tests
6. If Gradle cannot be run, the agent must enter BLOCKED and request user-provided output
7. The agent must not move to GREEN, VERIFY, or COMPLETE without real evidence

## 7. Tests Are Sacred

NEVER delete or remove tests to make a build pass. If tests fail:
1. Investigate why they fail
2. Fix the underlying issue (missing dependencies, configuration, etc.)
3. If a test is genuinely obsolete, discuss with the user before removal

Deleting tests hides broken functionality and is never an acceptable solution.

## 8. Test Failure Investigation

NEVER ignore test failures. When tests fail:

- **STOP** and investigate the cause before proceeding
- **Do NOT assume** the cause based on error message alone (e.g., "TimeoutException means Kafka isn't running")
- **Do NOT dismiss** failures as "infrastructure not running" without verification
- **Do NOT proceed** with commits or other work until failures are understood and resolved
- **Check test infrastructure** - many tests use testcontainers which auto-start dependencies

### After Fixing a Failing Test

When a test fails (whether from pre-commit hook, CI, or manual run):

1. Fix the test or the code causing the failure
2. Run the specific failing test to verify the fix
3. Only after the test passes, proceed with staging and committing

Never assume a fix is correct without running the test to verify.

---

## 9. Summary

- Tests are JUnit 5 `@Test` methods in Java only
- Four test types: unit, integration, component, end-to-end
- TDD loop uses `./gradlew test` (unit tests only)
- Full verification uses `./gradlew check` (all test types)
- Test execution order: test → integrationTest → componentTest → endToEndTest
- Detailed failures live in `build/test-results/<testType>/TEST-*.xml`
- The agent must never guess test results and must always rely on real output

# End of Java + Gradle Test Runner Skill
