---
name: feature-dev
description: Develop a feature from documentation or a feature brief by reading AGENTS.md context, detecting the relevant stack, implementing the change, and verifying it with tests.
---

# Feature Development

Implement a feature end to end using repository context and the relevant stack patterns.

## 1. Parse the Requirement

Extract:

- Goal
- Requirements
- Acceptance criteria
- Constraints
- Out-of-scope items

If the requirement is incomplete, infer from local docs and code before asking the user.

## 2. Detect Stack and Scope

Read:

1. Root `AGENTS.md`
2. Relevant scoped `AGENTS.md`
3. Relevant configs such as `package.json`, `pom.xml`, `pyproject.toml`, `go.mod`

Identify which engineering perspective applies:

- Frontend
- Java backend
- Python backend
- DevOps or infrastructure
- Database
- Data or ML

## 3. Analyze Existing Code

Understand:

- Affected modules
- Existing patterns
- Integration points
- Test layout

List files to create and modify before editing.

## 4. Plan the Change

Break the work into ordered steps with tests interleaved.

Prefer:

- Minimal blast radius
- Existing patterns
- Root-cause fixes

## 5. Implement

For each step:

1. Make the smallest coherent change
2. Keep naming and structure aligned with the existing codebase
3. Add or update tests for behavior changes
4. Verify syntax or compile health as soon as practical

## 6. Verify

Run the most relevant checks available:

- Build or type-check
- Lint if configured
- Targeted tests first
- Broader regression tests when the change warrants it

## 7. Report

Summarize:

- Stack and scope
- Files changed
- Verification performed
- Remaining risks or follow-up items

## Integration

- Planning: `feature-plan`
- Verification: `run-tests`, `pre-commit`
- Companion skills: `testing-procedures`, `code-review`, `context-engineering`