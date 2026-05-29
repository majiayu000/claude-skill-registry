---
name: best-practices
description: >-
  Transforms vague Claude Code prompts into effective ones by applying five
  principles: add verification criteria, provide specific file paths and context,
  set constraints on scope and approach, structure complex tasks in phases, and
  include rich content like error logs and screenshots. Invoke with /best-practices
  when a prompt needs improvement before execution.
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - Task
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - guide
    - prompting
    - claude-code
    - workflow
    - best-practices
  provenance:
    upstream_source: "best-practices"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:54:13Z"
    generator_version: "1.0.0"
    intent_confidence: 0.58
---

# Best Practices -- Prompt Transformer

Transform prompts by adding what Claude Code needs to succeed.

## Overview

This guide transforms vague or incomplete Claude Code prompts into precise, verifiable instructions. A well-formed prompt gives Claude specific file locations, clear success criteria, explicit constraints, and supporting materials -- reducing correction cycles from 5+ iterations to a single execution.

**What you will learn:**
- The 5 transformation principles ranked by impact
- How to choose between direct transformation and context-first workflows
- Prompt patterns for common task types (bug fix, feature, refactor, test, debug, UI, exploration, migration)
- An evaluation rubric to score prompt quality before execution

**When to use this skill:**
- Before submitting a multi-step prompt to Claude Code
- When a previous prompt led to a correction spiral (2+ failed attempts)
- When reviewing team prompts in shared CLAUDE.md configurations

## Mode Selection

When the user provides a prompt to transform, ask using AskUserQuestion:

- **Question**: "How should I improve this prompt?"
- **Header**: "Mode"
- **Options**:
  1. **Transform directly** -- Apply the 5 principles and output an improved version
  2. **Build context first** -- Gather codebase context and intent analysis first

When the user asks to learn, show the Transformation Principles below.
When the user asks for examples, see `references/transformation-examples.md`.
When the user asks to evaluate a prompt, use the Quality Rubric at the end.

## Learning Path

### Level 1: The Core Rule

**Context is your most valuable resource.** Everything follows from managing the context window effectively.

Claude Code performs dramatically better when it can verify its own work (tests, screenshots, build commands), knows exactly where to look (`src/auth/login.ts:42`), understands what NOT to do (constraints), and receives actual error messages.

### Level 2: The 5 Transformation Principles

Apply in priority order. Each addresses a specific failure mode.

#### Principle 1: Add Verification (Highest Impact)

The single highest-leverage improvement for prompt quality.

| Missing Element | What to Add |
|-----------------|-------------|
| No success criteria | Test cases with specific inputs/outputs |
| UI changes | "take screenshot and compare to design" |
| Bug fixes | "write a failing test, then fix, verify test passes" |
| Build issues | "verify the build succeeds after fixing" |
| Refactoring | "run the test suite after each change" |
| No root cause enforcement | "address root cause, do not suppress error" |

```bash
# BEFORE
implement email validation

# AFTER
write a validateEmail function. test cases:
  user@domain.com -> true
  invalid -> false
  user@.com -> false
run the tests after implementing.
```

#### Principle 2: Provide Specific Context

Replace vague references with precise file paths, function names, line numbers.

| Vague | Specific |
|-------|----------|
| "the code" | `src/auth/login.ts` |
| "the bug" | "users report 500 when order total exceeds 10000" |
| "the API" | "the /api/users endpoint in routes.ts" |
| "that function" | `processPayment()` in `src/billing/charge.ts:142` |

| Strategy | Prompt Fragment |
|----------|----------------|
| Scope the task | "test for `foo.py` covering the logged-out edge case" |
| Point to sources | "`ExecutionFactory` git history for API evolution" |
| Reference patterns | "follow pattern in `HotDogWidget.php` for calendar" |
| Describe symptoms | "login fails after timeout -- check `src/auth/`" |

```bash
# BEFORE
fix the login bug

# AFTER
users report login fails after session timeout.
check auth flow in src/auth/, especially token refresh
in refresh_token.ts. write a failing test that
reproduces the issue, then fix it.
```

#### Principle 3: Add Constraints

Tell Claude what NOT to do. Prevents over-engineering and scope expansion.

| Constraint Type | Prompt Fragment |
|-----------------|-----------------|
| Dependencies | "no new libraries", "only existing deps" |
| Testing | "avoid mocks", "use real database in tests" |
| Scope | "do not refactor unrelated code" |
| Approach | "address root cause, do not suppress error" |
| Patterns | "follow codebase conventions", "match utils.ts style" |

```bash
# BEFORE
add a calendar widget

# AFTER
implement calendar widget with month selection and year
pagination. follow pattern in HotDogWidget.php. no
libraries beyond what the codebase already uses.
```

#### Principle 4: Structure Complex Tasks in Phases

Separate exploration from implementation for larger tasks:

```bash
# Phase 1 - EXPLORE
read src/auth/ and understand sessions and login.
# Phase 2 - PLAN
design the OAuth flow. what files change? create plan.
# Phase 3 - IMPLEMENT
follow plan. write tests for callback. run after each change.
# Phase 4 - COMMIT
commit with descriptive message.
```

**Use phases when**: uncertain about approach, multi-file change, unfamiliar code.
**Skip phases when**: one-liner change (typo, rename, log line).

#### Principle 5: Include Rich Content

| Content Type | How to Provide |
|--------------|----------------|
| Files | `@filename` syntax |
| Images | Paste screenshots directly |
| Errors | Paste actual error, not description |
| Logs | `cat error.log \| claude` |
| URLs | Link to documentation |

```bash
# BEFORE
the build is failing

# AFTER
build fails with:
  TypeError: Cannot read properties of undefined (reading 'map')
    at OrderList (src/components/OrderList.tsx:42)
fix and verify build succeeds. address root cause.
```

### Level 3: Context-First Workflow

For complex prompts, gather context before transforming. Launch 3 parallel agents via Task tool:

| Agent | Mission | Returns |
|-------|---------|---------|
| task-intent-analyzer | Understand what user is trying to do | Task type, gaps, edge cases |
| best-practices-referencer | Find relevant patterns from references/ | Matching examples, anti-patterns |
| codebase-context-builder | Explore the target codebase | File paths, conventions |

After agents return:
1. Synthesize findings -- combine intent + best practices + codebase context
2. Apply matching patterns -- use examples from referencer as templates
3. Ground in codebase -- add specific file paths from context builder
4. Transform the prompt -- apply all 5 principles with gathered context
5. Output improved prompt with before/after comparison

## Best Practices

### Do
- Start with verification -- highest impact on output quality
- Reference specific files with `@path` syntax
- Provide actual error messages verbatim, not descriptions
- Use `/clear` between unrelated tasks to prevent context pollution
- Scope investigations narrowly: "check `src/auth/`" not "figure out why it is slow"
- Delegate outcomes, not steps -- let Claude choose implementation
- Respect project CLAUDE.md conventions when transforming

### Do Not
- Combine multiple unrelated tasks in one prompt (split with `/clear`)
- Say "getting an error" without pasting the actual error
- Use "make it better" without specific criteria for "better"
- Micromanage file edits -- state the outcome, not the keystrokes
- Continue correcting after 2 failures -- `/clear` and rewrite
- Add try/catch to suppress errors instead of fixing root causes

## Common Questions

### Q: When should I use "Transform directly" vs "Build context first"?
**A**: Use "Transform directly" when you can see what is missing (no verification, vague location). Use "Build context first" when the prompt references unfamiliar code, spans multiple systems, or the approach is uncertain.

### Q: How do I handle prompts that combine multiple tasks?
**A**: Split them. Each prompt should have a single clear objective. After each task, use `/clear` to free context, then submit the next. Compound prompts cause scope creep and make verification ambiguous.

### Q: What if the prompt is already well-formed?
**A**: Score it against the Quality Rubric below. If it scores 6+ out of 8, it is ready. Focus on verification criteria and specific file locations -- these two principles account for most of prompt effectiveness.

## Examples

### Example 1: Bug Fix

```
BEFORE: fix the login bug

AFTER: users report login fails after session timeout.
check auth flow in src/auth/, especially token refresh
in refresh_token.ts. write a failing test that reproduces
the issue, then fix it. run the auth test suite after.

ADDED: symptom, location, verification (failing test), suite run
```

### Example 2: Feature Implementation

```
BEFORE: add a search feature

AFTER: implement search for products page. look at filtering
in ProductList.tsx for the pattern. search by name and category.
tests: empty query returns all, partial match works, no results
shows message. no external search libraries.

ADDED: location, reference pattern, test cases, constraint
```

### Example 3: Refactoring

```
BEFORE: make the code better

AFTER: refactor utils.js to ES2024: convert callbacks to
async/await, use optional chaining, add TypeScript types.
run the existing test suite after each change to ensure
nothing breaks. do not change public API signatures.

ADDED: specific changes, incremental verification, constraint
```

### Example 4: Debugging

```
BEFORE: the API is slow

AFTER: /api/orders takes 3+ seconds for large orders.
profile database queries in OrderService.ts. look for
N+1 queries or missing indexes. fix and verify response
time is under 500ms with 1000+ order items.

ADDED: endpoint, location, what to look for, measurable target
```

## Transformation Output Format

When transforming a prompt, output in this structure:

```markdown
**Original:** [user prompt]

**Improved:**
[transformed prompt in code block]

**Added:**
- [what was missing and added]
- [another improvement]
```

## Quality Rubric

Rate the prompt against these 4 dimensions (0-2 each, max 8):

| Dimension | 0 (Missing) | 1 (Partial) | 2 (Complete) |
|-----------|-------------|-------------|--------------|
| **Verification** | None | "test it" | Specific test cases + report |
| **Location** | "the code" | "auth module" | `src/auth/login.ts:42` |
| **Constraints** | None | Implied | "no X, root cause only" |
| **Scope** | Vague | Partial | Single clear task |

**Quick assessment:** 0-3 needs significant work, 4-5 needs some improvements, 6-8 good to go.

## Transformation Checklist

Before outputting, verify the improved prompt has:

- [ ] **Verification** -- How to know it worked (tests, screenshot, output)
- [ ] **Location** -- Specific files, functions, or areas
- [ ] **Constraints** -- What NOT to do
- [ ] **Single task** -- Not compound (split if needed)
- [ ] **Phases** -- If complex, structured as explore then plan then implement
- [ ] **Root cause** -- For bugs: "address root cause, do not suppress"
- [ ] **CLAUDE.md** -- Respects project conventions if they exist

## Anti-Patterns Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| "fix the bug" | Add symptom + location + verification |
| "make it better" | Specify exact changes (perf? types? style?) |
| "add tests" | Specify file, cases, edge cases, pattern |
| "getting an error" | Paste full error + file:line + repro steps |
| "review my code" | Specify focus: security? perf? edge cases? |
| Fix + style + refactor | Split tasks, `/clear` between each |
| "do what we discussed" | Restate the decision explicitly |

## Session Management

- **`/clear`** between unrelated tasks to free context
- After 2 failed corrections, `/clear` + write a better prompt
- Use subagents (Task tool) for investigation in separate context
- **`Esc`** to stop current operation, **`Esc+Esc`** to rewind
- `claude --continue` / `--resume` for persistent sessions

## References

- [references/prompt-patterns.md](references/prompt-patterns.md) -- Templates, anti-patterns, task-type prompt recipes
- [references/transformation-examples.md](references/transformation-examples.md) -- Extended before/after examples for all task types
