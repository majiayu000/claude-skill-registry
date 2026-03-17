---
description: Write minimal code to make failing tests pass. Use when saying "TDD green", "make tests pass", or "implement for tests".
---

# TDD Green Phase - Make Tests Pass

## Project Overrides

!`s="tdd-green"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

Implement minimal code to make failing tests pass in TDD green phase.

## Implementation Process

Use Task tool with subagent_type="general-purpose" to implement minimal passing code.

Prompt: "Implement MINIMAL code to make these failing tests pass: $ARGUMENTS. Follow TDD green phase principles:

1. **Pre-Implementation Analysis**
   - Review all failing tests and their error messages
   - Identify the simplest path to make tests pass
   - Avoid premature optimization or over-engineering

2. **Implementation Strategy**
   - **Fake It**: Return hard-coded values when appropriate
   - **Obvious Implementation**: When solution is trivial and clear
   - **Triangulation**: Generalize only when multiple tests require it
   - One test at a time — don't try to pass all at once

3. **Code Guidelines**
   - Write the minimal code that could possibly work
   - Avoid adding functionality not required by tests
   - Defer architectural decisions until refactor phase
   - Don't add error handling unless tests require it

4. **Progressive Implementation**
   - Make first test pass with simplest possible code
   - Run tests after each change to verify progress
   - Add just enough code for next failing test
   - Keep track of technical debt for refactor phase

5. **Anti-Patterns to Avoid**
   - Gold plating or adding unrequested features
   - Implementing design patterns prematurely
   - Refactoring during implementation
   - Ignoring test failures to move forward

Output:
- Complete implementation code
- Test execution results showing all green
- List of shortcuts taken for later refactoring"

## Post-Implementation Checks

1. Run full test suite — confirm all tests pass
2. Verify no existing tests were broken
3. Document areas needing refactoring
4. Check implementation is truly minimal

## Recovery

If tests still fail: review test requirements carefully, check for misunderstood assertions, add minimal code to address specific failures.

Tests to make pass: $ARGUMENTS
