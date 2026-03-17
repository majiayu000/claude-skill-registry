---
name: writing-slash-commands
description: Use when creating or editing slash commands - applies TDD to slash command documentation by testing with SlashCommand tool and subagents before deployment, preventing inverted logic and untested conditionals
---

# Writing Slash Commands

## Overview

**Writing slash commands IS Test-Driven Development applied to command documentation.**

You write test cases (arguments to test), watch them fail (wrong logic), fix the logic, watch tests pass, and refactor.

**Core principle:** If you didn't watch the slash command execute with the SlashCommand tool, you don't know if the logic works.

**REQUIRED BACKGROUND:** You MUST understand **`writing-skills`** skill before using this. This skill adapts TDD methodology to slash commands.

## TDD Mapping for Slash Commands

| TDD Concept | Slash Command Creation |
|-------------|------------------------|
| **Test case** | SlashCommand tool call with specific arguments |
| **Production code** | Slash command markdown file |
| **Test fails (RED)** | Command output wrong for given input |
| **Test passes (GREEN)** | Command handles all inputs correctly |
| **Refactor** | Fix edge cases, maintain correctness |
| **Write test first** | Test command with SlashCommand BEFORE deploying |
| **Watch it fail** | Document exact wrong outputs |
| **Minimal code** | Fix logic to pass those specific tests |
| **Watch it pass** | Verify all test cases now work |

## The Iron Law

```text
NO SLASH COMMAND WITHOUT TESTING WITH SlashCommand TOOL FIRST
```

**Mental simulation ≠ actual testing.** The SlashCommand tool is the ONLY way to verify logic.

## When to Use

**Create slash command:**
- [ ] Test with SlashCommand tool for each argument combination
- [ ] Watch it fail/succeed for each input
- [ ] Fix logic until all tests pass

**Edit existing slash command:**
- [ ] Test current behavior (RED - document what's wrong)
- [ ] Fix logic (GREEN - make tests pass)
- [ ] Test edge cases (REFACTOR - handle new scenarios)

## Common Failures (From Baseline Testing)

### Failure 1: Inverted Conditional Logic

**Baseline behavior:**

```bash
# With NO argument
Output: "Creating commit for $1 branch" ❌
Expected: "Warning: No feature branch provided"

# With argument "my-feature"
Output: "Warning: No feature branch provided" ❌
Expected: "Creating commit for my-feature branch"
```

**Root cause:** IF/ELSE conditions backwards, not tested

**Solution:** Test BOTH branches with SlashCommand tool

### Failure 2: Untested Variable Substitution

**Baseline behavior:**
- Output shows literal "$1" instead of argument value

**Root cause:** Assumed $N substitution works without testing

**Solution:** Verify variables substitute correctly in output

### Failure 3: Unverified Path References

**Baseline behavior:**
- Command references `git-and-github/create-git-commit` skill
- Actual path: `.claude/skills/create-git-commit/SKILL.md`

**Root cause:** Trust mental model of paths without verification

**Solution:** Verify all referenced paths exist before deploying

## Testing Workflow (RED-GREEN-REFACTOR)

### RED: Document Current Behavior

Use subagent with SlashCommand tool to test:

```text
Task: Test the slash command at [path] with these arguments:
1. No arguments
2. One argument: "test-value"
3. Multiple arguments: "arg1" "arg2"

Document EXACT output for each test.
```

### GREEN: Fix Logic to Pass Tests

Fix the slash command logic based on RED phase findings.

### REFACTOR: Test Edge Cases

Add tests for:
- Empty strings
- Special characters
- Missing vs empty arguments
- Extra unexpected arguments

## Required Tests Before Deploying

**For every slash command, test:**

- [ ] **No arguments** (if optional)
- [ ] **One argument** (if single arg expected)
- [ ] **All arguments** (if multiple args expected)
- [ ] **Each conditional branch** (test IF and ELSE separately)
- [ ] **Variable substitution** (verify $1, $2, etc. show actual values)
- [ ] **Referenced paths** (verify skills/files exist)

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Logic is simple, don't need to test" | Baseline showed inverted IF/ELSE. Test it. |
| "I know how variables work" | $1 appeared literally in output. Verify it. |
| "I remember the path" | Wrong path in baseline. Check it exists. |
| "Mental simulation is good enough" | Mental simulation missed all 4 baseline bugs. Use SlashCommand tool. |
| "Testing is overkill for one command" | One untested command = 4 bugs in production. Test it. |
| "Cache is stale, I'll verify by inspection" | File inspection = mental simulation. Can't verify? Can't deploy. |

## Red Flags - STOP and Test

- Writing conditional logic without testing both branches
- Assuming variable substitution works
- Referencing paths without verifying
- "This is simple, no need to test"
- Deploying without using SlashCommand tool

**All of these mean: Stop. Test with SlashCommand tool.**

## Slash Command Testing Checklist

**Before deploying ANY slash command:**

- [ ] Used subagent with SlashCommand tool to test
- [ ] Tested with NO arguments (documented behavior)
- [ ] Tested WITH arguments (documented behavior)
- [ ] Tested EACH conditional branch (IF, ELSE, ELSE IF)
- [ ] Verified variable substitution ($1, $2) works correctly
- [ ] Verified all referenced paths/skills exist
- [ ] Fixed any bugs found during testing
- [ ] Re-tested after fixes to confirm resolution

## The Bottom Line

**Mental simulation found ZERO bugs.**
**SlashCommand tool testing found FOUR bugs.**

Test with SlashCommand tool. Every time. No exceptions.
