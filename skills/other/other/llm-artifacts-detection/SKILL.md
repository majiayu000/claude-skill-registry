---
name: llm-artifacts-detection
description: Detects common LLM coding agent artifacts in codebases. Identifies test quality issues, dead code, over-abstraction, and verbose LLM style patterns. Use when cleaning up AI-generated code or reviewing for agent-introduced cruft.
---

# LLM Artifacts Detection

Detect and flag common patterns introduced by LLM coding agents that reduce code quality.

## Detection Categories

| Category | Reference | Key Issues |
|----------|-----------|------------|
| Tests | [references/tests-criteria.md](references/tests-criteria.md) | DRY violations, library testing, mock boundaries |
| Dead Code | [references/dead-code-criteria.md](references/dead-code-criteria.md) | Unused code, TODO/FIXME, backwards compat cruft |
| Abstraction | [references/abstraction-criteria.md](references/abstraction-criteria.md) | Over-abstraction, copy-paste drift, over-configuration |
| Style | [references/style-criteria.md](references/style-criteria.md) | Obvious comments, defensive overkill, unnecessary types |

## Agent Prompts

Use these prompts to spawn focused detection agents:

### Tests Agent

```
Analyze the test files for LLM-introduced test quality issues:

1. **DRY Violations**: Look for setup/teardown code repeated across multiple test functions instead of using fixtures or shared helpers. Flag patterns like:
   - Identical object creation in multiple tests
   - Repeated mock configurations
   - Copy-pasted database setup

2. **Library Testing**: Identify tests that validate standard library or framework behavior rather than application code. Signs:
   - No imports from the application codebase
   - Testing built-in functions or third-party library methods
   - Assertions about stdlib behavior

3. **Mock Boundaries**: Flag mocking that's too deep or too shallow:
   - Too deep: Mocking internal implementation details, private methods
   - Too shallow: Mocking at the wrong layer, missing integration points
   - Wrong level: Unit test mocks in integration tests or vice versa

For each issue found, report: [FILE:LINE] ISSUE_TITLE
```

### Dead Code Agent

```
Scan the codebase for dead code and cleanup opportunities:

1. **Unused Code**: Find functions, classes, and variables with no references:
   - Functions never called
   - Classes never instantiated
   - Module-level variables never read
   - Unreachable code after returns

2. **TODO/FIXME Comments**: Flag all TODO, FIXME, HACK, XXX comments that indicate incomplete work

3. **Backwards Compat Cruft**: Look for patterns suggesting removed features:
   - Variables renamed with _unused, _old, _deprecated suffixes
   - Re-exports only for backwards compatibility
   - Comments like "# removed", "# legacy", "# deprecated"
   - Empty functions/classes kept "for compatibility"

4. **Orphaned Tests**: Tests for code that no longer exists:
   - Test files with no corresponding source
   - Test functions testing deleted features

For each issue found, report: [FILE:LINE] ISSUE_TITLE
```

### Abstraction Agent

```
Review the codebase for over-engineering introduced by LLM agents:

1. **Over-Abstraction**: Identify unnecessary abstraction layers:
   - Wrapper classes that just delegate to one method
   - Interfaces/protocols with only one implementation
   - Abstract base classes with single concrete class
   - Factory functions that always return the same type

2. **Copy-Paste Drift**: Find 3+ similar code blocks that should be parameterized:
   - Nearly identical functions with minor variations
   - Repeated patterns that could be a single function with parameters
   - Similar class methods across multiple classes

3. **Over-Configuration**: Flag configuration for non-configurable things:
   - Feature flags that are never toggled
   - Environment variables always set to one value
   - Config options with no production variation
   - Overly generic code for single use case

For each issue found, report: [FILE:LINE] ISSUE_TITLE
```

### Style Agent

```
Check for verbose LLM-style patterns that reduce code clarity:

1. **Obvious Comments**: Comments that restate what the code clearly does:
   - "# increment counter" above counter += 1
   - "# return the result" above return result
   - Docstrings that repeat the function name

2. **Over-Documentation**: Excessive documentation on trivial code:
   - Full docstrings on simple getters/setters
   - Parameter descriptions for obvious args
   - Return value docs for self-evident returns

3. **Defensive Overkill**: Unnecessary defensive programming:
   - try/except around code that cannot fail
   - Null checks on values that can't be null
   - Type checks after type hints guarantee the type
   - Validation of already-validated inputs

4. **Unnecessary Type Hints**: Type hints that add no value:
   - Type hints on obvious literal assignments
   - Redundant hints on variables immediately clear from context
   - Over-annotated internal/local variables

For each issue found, report: [FILE:LINE] ISSUE_TITLE
```

## Usage

1. Load this skill when reviewing AI-generated code
2. Spawn agents for specific detection categories as needed
3. Use reference files for detailed criteria and examples
4. Report issues in format: `[FILE:LINE] ISSUE_TITLE`

## When to Apply

- Cleaning up code written by AI coding agents
- Post-generation code review
- Reducing code bloat from iterative AI generation
- Identifying patterns that reduce maintainability
