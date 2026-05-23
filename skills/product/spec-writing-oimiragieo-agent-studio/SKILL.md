---
name: spec-writing
description: 'Specification document creation from gathered requirements and context. Use when requirements are gathered and you need to create a comprehensive spec.'
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Synthesize context into actionable specification
  - Be specific about files and patterns
  - Include QA criteria for validation
error_handling: graceful
streaming: supported
source: auto-claude
---

# Specification Writing Skill

## Overview

Transform gathered requirements and codebase context into a comprehensive, actionable specification document. The spec is the contract between planning and implementation.

**Core principle:** Synthesize context into actionable spec. No user interaction needed during writing.

## When to Use

**Always:**

- After requirements gathering is complete
- When you have codebase context available
- Before implementation planning begins

**Exceptions:**

- Simple changes that don't need formal specs
- Exploratory work without clear requirements

## The Iron Law

```
NO IMPLEMENTATION WITHOUT A COMPLETE SPEC FIRST
```

A spec must have ALL required sections before implementation can begin.

## Inputs Required

Before writing a spec, ensure you have:

1. **Requirements document** - What needs to be built
2. **Project context** - Tech stack, structure, patterns
3. **Files to modify** - Identified from codebase analysis
4. **Files to reference** - Patterns to follow

## Workflow

### Phase 1: Load All Context

Read all input files to understand the full picture:

```bash
# Read requirements
cat .claude/context/requirements/[task-name].md

# Read project context
cat .claude/context/product.md
cat .claude/context/tech-stack.md

# Read any analysis results
cat .claude/context/analysis/[task-name].json 2>/dev/null
```

Extract from these files:

- **From requirements**: Task description, workflow type, acceptance criteria
- **From project context**: Services, tech stacks, patterns
- **From analysis**: Files to modify, files to reference, patterns

### Phase 2: Analyze Context

Before writing, think about:

**Implementation Strategy:**

- What's the optimal order of implementation?
- Which area should be built first?
- What are the dependencies between components?

**Risk Assessment:**

- What could go wrong?
- What edge cases exist?
- Any security considerations?

**Pattern Synthesis:**

- What patterns from reference files apply?
- What utilities can be reused?
- What's the code style?

### Phase 3: Write Specification Document

Create the spec with ALL required sections:

````markdown
# Specification: [Task Name]

## Overview

[One paragraph: What is being built and why]

## Workflow Type

**Type**: [feature|refactor|investigation|migration|simple]

**Rationale**: [Why this workflow type fits the task]

## Task Scope

### Areas Involved

- **[area-name]** (primary) - [role from context analysis]
- **[area-name]** (integration) - [role from context analysis]

### This Task Will:

- [ ] [Specific change 1]
- [ ] [Specific change 2]
- [ ] [Specific change 3]

### Out of Scope:

- [What this task does NOT include]

## Technical Context

### Tech Stack

- Language: [from project context]
- Framework: [from project context]
- Key directories: [from project context]

### How to Run

```bash
[commands from project context]
```
````

## Files to Modify

| File     | Purpose   | What to Change           |
| -------- | --------- | ------------------------ |
| `[path]` | [purpose] | [specific change needed] |

## Files to Reference

These files show patterns to follow:

| File     | Pattern to Copy                  |
| -------- | -------------------------------- |
| `[path]` | [what pattern this demonstrates] |

## Patterns to Follow

### [Pattern Name]

From `[reference file path]`:

```[language]
[code snippet or description]
```

**Key Points:**

- [What to notice about this pattern]
- [What to replicate]

## Requirements

### Functional Requirements

1. **[Requirement Name]**
   - Description: [What it does]
   - Acceptance: [How to verify]

2. **[Requirement Name]**
   - Description: [What it does]
   - Acceptance: [How to verify]

### Edge Cases

1. **[Edge Case]** - [How to handle it]
2. **[Edge Case]** - [How to handle it]

## Implementation Notes

### DO

- Follow the pattern in `[file]` for [thing]
- Reuse `[utility/component]` for [purpose]
- [Specific guidance based on context]

### DON'T

- Create new [thing] when [existing thing] works
- [Anti-pattern to avoid based on context]

## Development Environment

### Start Services

```bash
[commands from project context]
```

### Required Environment Variables

- `VAR_NAME`: [description]

## Success Criteria

The task is complete when:

1. [ ] [From requirements acceptance_criteria]
2. [ ] [From requirements acceptance_criteria]
3. [ ] No console errors
4. [ ] Existing tests still pass
5. [ ] New functionality verified

## QA Acceptance Criteria

**CRITICAL**: These criteria must be verified by QA before sign-off.

### Unit Tests

| Test        | File             | What to Verify                 |
| ----------- | ---------------- | ------------------------------ |
| [Test Name] | `[path/to/test]` | [What this test should verify] |

### Integration Tests

| Test        | Areas             | What to Verify            |
| ----------- | ----------------- | ------------------------- |
| [Test Name] | [area-a + area-b] | [API contract, data flow] |

### End-to-End Tests

| Flow        | Steps               | Expected Outcome  |
| ----------- | ------------------- | ----------------- |
| [User Flow] | 1. [Step] 2. [Step] | [Expected result] |

### QA Sign-off Requirements

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] No regressions in existing functionality
- [ ] Code follows established patterns
- [ ] No security vulnerabilities introduced

````

### Phase 4: Verify Spec

After creating, verify the spec has all required sections:

```bash
# Check required sections exist
grep -E "^##? Overview" spec.md && echo "Overview present"
grep -E "^##? Workflow Type" spec.md && echo "Workflow Type present"
grep -E "^##? Task Scope" spec.md && echo "Task Scope present"
grep -E "^##? Success Criteria" spec.md && echo "Success Criteria present"
grep -E "^##? QA Acceptance" spec.md && echo "QA Criteria present"

# Check file length (should be substantial)
wc -l spec.md
````

If any section is missing, add it immediately.

### Phase 5: Save and Signal Completion

Save the spec to the appropriate location:

```bash
# Save to context directory
cat > .claude/context/specs/[task-name]-spec.md << 'EOF'
[Spec content]
EOF
```

## Verification Checklist

Before completing spec writing:

- [ ] Overview section present and clear
- [ ] Workflow type determined with rationale
- [ ] Task scope defined with in/out of scope
- [ ] Files to modify listed with specific changes
- [ ] Files to reference listed with patterns
- [ ] Functional requirements documented
- [ ] Edge cases identified
- [ ] Implementation notes included
- [ ] Success criteria defined
- [ ] QA acceptance criteria complete

## Common Mistakes

### Generic Content

**Why it's wrong:** "Implement the feature" is not actionable.

**Do this instead:** Be specific to this project and task. Use exact file paths.

### Missing Tables

**Why it's wrong:** Empty tables provide no guidance.

**Do this instead:** Fill in tables with data from context analysis.

### No QA Criteria

**Why it's wrong:** QA agent needs clear criteria to validate.

**Do this instead:** Include unit, integration, and E2E test expectations.

## Integration with Other Skills

This skill works well with:

- **spec-gathering**: Provides the requirements input
- **spec-critique**: Reviews the spec for issues
- **complexity-assessment**: Determines spec complexity for planning

## Memory Protocol

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
