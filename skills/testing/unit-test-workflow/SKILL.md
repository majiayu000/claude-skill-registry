---
name: unit-test-workflow
description: Guided multi-phase workflow for designing and generating comprehensive unit tests
category: testing
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Unit Test Generation Workflow

Generate unit tests for given function(s) in a codebase. Work in phases. Output only the requested artifacts.

## Inputs Required
- fileOrFolder: The file or folder path to generate unit tests for
- functionToTest (optional): Specific function to test
- language (optional): Override language detection

## Procedure

### Phase 1 - Detect Language and Environment
1. Identify programming language from file extension
2. Detect testing framework used in the codebase by analyzing dependencies file and existing test files
3. If multiple frameworks detected, choose the one used for unit tests. Prefer the one already present in existing tests file close to fileOrFolder location

### Phase 2 - Locate Placement
4. Search for existing tests covering the target module. Decide if test should be appended to existing file or if new file should be created
5. If creating new file, analyze existing test files to correctly use same naming convention
6. If appending, set up test cases similarly to existing tests. If creating new file, analyze existing test files to correctly set up the testing framework

### Phase 3 - Analyze Code Under Test
7. Parse signatures, inputs, outputs, side effects, expected and exceptional paths, async/await, throw or reverts, edge cases
8. Map branches and guards. Identify boundary values and invariants. Mark non-determinism sources (time, RNG, I/O)

### Phase 4 - Design Cases
9. Create a minimal set for branch coverage. Include happy paths, boundary/edge cases, and failure modes
10. Add security-focused cases: invalid/tainted inputs, injection payloads, path traversal, overflow/underflow, encoding pitfalls, fuzz/property checks for pure functions
11. Define mocking/stubbing plan attempting to follow existing patterns to never hit real network, database, filesystem, clock, or randomness

### Phase 5 - Emit Tests
12. Produce tests consistent with the framework's style and project imports. Keep small, pure helpers. No hidden side effects
13. Add as many tests as seem appropriate to cover all path/security/cases/edge cases
14. Ensure deterministic execution

### Phase 6 - Validate Statically
15. Self-check imports, assertion usage, compilation or type errors and lints. Avoid duplicate tests
16. Output estimated coverage from new tests

### Phase 7 - Run Tests
17. Run tests individually following test framework instructions and make sure they pass

## Language Specifics
- **TypeScript/JavaScript**: Respect tsconfig/moduleResolution. Detect framework in package.json. Use fake timers instead of real time
- **Rust**: Use #[cfg(test)] modules, proptest when property tests enabled

## Constraints
- No original code file writes or schema changes
- Use meaningful test case names
- Prefer pure helpers and table-driven tests
- Analyze only within the given code. Do not invent missing context or external APIs

## Skill Chaining

### After Phase 7 (Run Tests)

| Chain To | Condition |
|----------|-----------|
| property-based-testing | Pure functions, roundtrip patterns detected |
| repo-hygiene | Always (terminal) |

### Chains From

| Source | When |
|--------|------|
| suggest-tests | HIGH risk functions identified |
| tdd | Comprehensive generation needed |

### Testing Pipeline Position

unit-test-workflow is step 3 in the testing pipeline:

```
tdd → suggest-tests → unit-test-workflow → property-based-testing → repo-hygiene
                            ↑
                       (you are here)
```

### Terminal Chain

After all tests pass: **repo-hygiene** (clean temporary test files)