---
name: composable-step-design
description: Design Plan/Build/Review/Fix workflow steps for ADWs. Use when creating composable workflow primitives, defining step contracts, or implementing step isolation patterns.
allowed-tools: Read, Grep, Glob
---

# Composable Step Design

Design the four composable workflow steps (Plan/Build/Review/Fix) that form the backbone of AI Developer Workflows.

## When to Use

- Creating new workflow step primitives
- Defining step input/output contracts
- Implementing step isolation patterns
- Designing step composition strategies
- Building ADW workflow variations

## Prerequisites

- Understanding of @composable-steps.md memory file
- Familiarity with @adw-framework.md patterns
- Knowledge of deterministic vs non-deterministic execution

## SDK Requirement

> **Implementation Note**: Full step orchestration requires Claude Agent SDK. This skill provides step design patterns and contracts.

## The Four Steps

| Step | Type | Output | Characteristic |
| --- | --- | --- | --- |
| `/plan` | Deterministic output | Spec file | Known path, structured content |
| `/build` | Non-deterministic | Code changes | Creative, adaptive |
| `/review` | Deterministic output | PASS/FAIL report | Structured, parseable |
| `/fix` | Non-deterministic | Targeted fixes | Focused, corrective |

## Step Design Process

### Step 1: Define the Contract

Each step needs a clear contract:

```python
# Plan Step Contract
class PlanContract:
    inputs = {
        "task_description": str,      # What to implement
        "issue_context": str | None,  # Optional context
        "project_path": str           # Where to work
    }
    outputs = {
        "spec_file_path": str,        # Path to generated spec
        "success": bool
    }
```text

### Step 2: Ensure Isolation

Each step must be runnable independently:

**Isolation Requirements:**

1. Accept inputs via arguments or file paths (not workflow state)
2. Produce outputs to known, predictable locations
3. Not depend on other steps having run
4. Complete or fail cleanly (no partial states)
5. Be testable in isolation

### Step 3: Define Success Criteria

Each step needs clear success indicators:

**Plan Step:**

- [ ] Spec file created at expected path
- [ ] Spec includes acceptance criteria
- [ ] Scope is bounded and achievable
- [ ] Technical approach defined

**Build Step:**

- [ ] All spec requirements addressed
- [ ] Code compiles/lints
- [ ] Tests pass (if exist)
- [ ] Changes committed

**Review Step:**

- [ ] All code reviewed against spec
- [ ] Issues categorized by severity
- [ ] Clear PASS/FAIL determination
- [ ] Actionable issue descriptions

**Fix Step:**

- [ ] All flagged issues addressed
- [ ] No new issues introduced
- [ ] Changes committed

### Step 4: Design Error Handling

Plan failure modes and recovery:

| Step | Failure Mode | Recovery |
| --- | --- | --- |
| Plan | Can't generate spec | Retry with more context |
| Build | Build errors | Return to plan |
| Review | Critical issues | Proceed to fix |
| Fix | Can't fix | Escalate to human |

### Step 5: Define Composition Rules

How steps chain together:

```text
plan_build:
  Plan → Build

plan_build_review:
  Plan → Build → Review

plan_build_review_fix:
  Plan → Build → Review → [if FAIL] → Fix → [loop until PASS or max]
```text

## Step Templates

### Plan Step Template

```markdown
# /plan

You are a planning agent. Create an implementation specification.

## Inputs

- Task: $ARGUMENTS
- Project: $PROJECT_PATH

## Output

Create a spec file at: specs/{type}-{id}-{description}.md

## Spec Structure

1. **Summary**: One paragraph overview
2. **Requirements**: Numbered list of what must be done
3. **Acceptance Criteria**: How to verify completion
4. **Technical Approach**: How to implement
5. **Files to Modify**: List of affected files

## Success Criteria

- [ ] Spec file created
- [ ] All sections complete
- [ ] Scope is achievable
```text

### Build Step Template

```markdown
# /build

You are an implementation agent. Execute the plan.

## Inputs

- Plan: $ARGUMENTS (path to spec file)
- Project: $PROJECT_PATH

## Process

1. Read the spec file
2. Implement each requirement
3. Run tests if they exist
4. Commit changes with "build: " prefix

## Success Criteria

- [ ] All requirements addressed
- [ ] Code compiles
- [ ] Tests pass
- [ ] Changes committed
```text

### Review Step Template

```markdown
# /review

You are a review agent. Validate the implementation.

## Inputs

- Project: $PROJECT_PATH
- Spec: $SPEC_PATH (optional)

## Output

Structured review report:

STATUS: PASS | FAIL

ISSUES (if FAIL):
- [severity] description

## Severity Levels

- CRITICAL: Must fix before merge
- HIGH: Should fix before merge
- MEDIUM: Consider fixing
- LOW: Optional improvement

## Success Criteria

- [ ] All code reviewed
- [ ] Issues categorized
- [ ] Clear PASS/FAIL status
```text

### Fix Step Template

```markdown
# /fix

You are a fix agent. Resolve review issues.

## Inputs

- Issues: $ARGUMENTS (from review output)
- Project: $PROJECT_PATH

## Process

1. Parse issue list
2. Fix each issue in priority order
3. Verify fix doesn't introduce new issues
4. Commit with "fix: " prefix

## Success Criteria

- [ ] All issues addressed
- [ ] No new issues introduced
- [ ] Changes committed
```text

## Loop Limit Pattern

Prevent infinite fix loops:

```python
MAX_FIX_ATTEMPTS = 3

for attempt in range(MAX_FIX_ATTEMPTS):
    review = await run_review()
    if review.status == "PASS":
        break
    await run_fix(review.issues)
else:
    # Max attempts reached
    escalate_to_human("Max fix attempts reached")
```text

## Output Format

```markdown
## Step Design Specification

### Step: [Name]

**Type:** Deterministic Output | Non-Deterministic

**Purpose:** [What this step accomplishes]

### Contract

**Inputs:**
| Name | Type | Required | Description |
| --- | --- | --- | --- |
| [input] | [type] | [yes/no] | [description] |

**Outputs:**
| Name | Type | Description |
| --- | --- | --- |
| [output] | [type] | [description] |

### Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
...

### Error Handling

| Failure Mode | Recovery Action |
| --- | --- |
| [mode] | [action] |

### Template

```markdown
[Slash command template]
```text

### Composition Rules

[How this step chains with others]

```text

## Design Checklist

- [ ] Contract inputs defined
- [ ] Contract outputs defined
- [ ] Isolation verified (standalone runnable)
- [ ] Success criteria specified
- [ ] Error handling planned
- [ ] Composition rules documented
- [ ] Template created
- [ ] Tests designed

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Coupled steps | Can't run independently | Pass data via files |
| Unbounded loops | Infinite fix attempts | MAX_FIX_ATTEMPTS |
| Undefined contracts | Unpredictable I/O | Explicit contracts |
| Missing success criteria | Can't verify completion | Define criteria |
| No error handling | Silent failures | Plan recovery actions |

## Cross-References

- @composable-steps.md - Step memory file
- @composable-primitives.md - General primitives
- @adw-framework.md - ADW overview
- @template-engineering.md - Template patterns

## Version History

- **v1.0.0** (2026-01-01): Initial release (Lesson 14)

---

## Last Updated

**Date:** 2026-01-01
**Model:** claude-opus-4-5-20251101
