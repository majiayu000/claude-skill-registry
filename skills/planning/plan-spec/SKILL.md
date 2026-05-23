---
name: plan-spec
description: Plan specification (enters plan mode)
user-invocable: true
---

# Plan Specification (Plan Mode)

## Prerequisites

Run `/fetch-issue <ALG-XX>` first to fetch issue context and create branch.

## Steps

1. **Enter plan mode**:
   Call the `EnterPlanMode` tool to begin planning.

2. **Analyze fetched issue context** from the conversation:
   - Issue title and description
   - Labels and status
   - Related specs (if any were found)

3. **Ask up to 5 clarifying questions** using `AskUserQuestion`:
   Focus on:
   - Ambiguous or vague requirements
   - Missing acceptance criteria
   - Unclear scope boundaries
   - Priority of different user stories
   - Technical constraints not mentioned

4. **Explore related code** if needed:
   - If related specs were found, read them for patterns
   - Search codebase for relevant existing implementations
   - Understand the domain context

5. **Propose spec structure** in the plan file:
   Write to the plan file (NOT spec.md yet) with:
   - **Summary**: 2-3 sentences from issue description
   - **User Scenarios & Testing**:
     - Multiple user stories with priorities (P1, P2, P3)
     - Each with "Why this priority" explanation
     - Acceptance scenarios in Given/When/Then format
   - **Edge Cases**: Explicit list of edge cases
   - **Functional Requirements**: FR-001, FR-002, etc.
   - **Dependencies**: Links to related specs (e.g., `@specs/alg-14-discover-chat`)
   - **Out of Scope**: Explicit boundaries

6. **Exit plan mode**:
   Call `ExitPlanMode` to get user approval of the proposed spec structure.

7. **After approval**, write the spec file:
   - Get branch info: `git rev-parse --abbrev-ref HEAD`
   - Extract issue number from branch name (e.g., `alg-27-*` -> 27)
   - Write `specs/alg-{NUM}-*/spec.md` with the approved structure
   - Include header:

     ```markdown
     # Feature Specification: {Title}

     **Feature Branch**: `{branch-name}`
     **Created**: {ISO date}
     **Status**: Draft
     **Linear Issue**: [ALG-{NUM}](https://linear.app/algojuke/issue/ALG-{NUM})
     **Input**: {Original issue description}
     ```

8. **Commit the spec**:
   ```bash
   git add specs/alg-{NUM}-*/spec.md
   git commit -m "spec: ALG-{NUM} - initial specification"
   ```

## Spec Template Reference

Follow the structure from existing specs like `specs/alg-14-discover-chat/spec.md`:

- User Scenarios with priorities and acceptance scenarios
- Functional Requirements numbered FR-001, FR-002
- Clear scope boundaries
- Clarifications section for Q&A
