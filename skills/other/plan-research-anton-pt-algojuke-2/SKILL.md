---
name: plan-research
description: Plan technical research (enters plan mode)
argument-hint: "[guidelines]"
user-invocable: true
---

# Plan Research (Plan Mode)

## Input

Optional implementation guidelines: $ARGUMENTS
Examples:

- "Focus on SSE streaming patterns"
- "Use React Query for data fetching"
- "Based on the pattern from ALG-14"

## Steps

1. **Enter plan mode**:
   Call the `EnterPlanMode` tool to begin planning.

2. **Get current feature from branch**:

   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   # Extract: alg-27-feature-name -> 27
   NUM=$(echo "$BRANCH" | grep -oE 'alg-([0-9]+)' | grep -oE '[0-9]+')
   ```

3. **Read the spec**:
   - Read `specs/alg-${NUM}-*/spec.md`
   - Extract user stories, requirements, and scope

4. **Incorporate user guidelines** (if `$ARGUMENTS` provided):
   - Parse the implementation guidance
   - Use as constraints for technology choices
   - Note any specific patterns or libraries mentioned

5. **Explore codebase** to identify:
   - Existing patterns to follow (search for similar implementations)
   - Files that will need modification
   - Technologies currently in use
   - External documentation to reference

6. **Propose research plan** in the plan file:
   Write to the plan file (NOT research.md yet) with:
   - **Key Decisions** to make (numbered 1, 2, 3...)
   - **Technologies** to evaluate
   - **Codebase Patterns** to examine
   - **Files** likely to be modified
   - **External Resources** to consult

7. **Exit plan mode**:
   Call `ExitPlanMode` to get user approval of the research plan.

8. **After approval**, conduct research:
   - Make the key decisions with rationale
   - Document alternatives considered
   - Extract relevant code patterns from codebase
   - Reference external documentation

9. **Write research.md**:

   ```markdown
   # Research: {Feature Title}

   **Date**: {ISO date}
   **Feature**: ALG-{NUM}
   **Implementation Guidance**: {$ARGUMENTS if provided}

   ## Executive Summary

   {Brief overview of key decisions}

   ## Key Decisions

   ### 1. {Decision Title}

   **Decision**: {What was decided}
   **Rationale**: {Why this approach}
   **Alternatives Considered**:

   - {Alternative 1}: {Why rejected}
   - {Alternative 2}: {Why rejected}

   ## Implementation Patterns

   {Code snippets from codebase showing patterns to follow}

   ## Files to Modify

   - `path/to/file.ts`: {What changes}
   ```

10. **Commit the research**:
    ```bash
    git add specs/alg-${NUM}-*/research.md
    git commit -m "spec: ALG-${NUM} - research and decisions"
    ```

## Notes

- Research should validate decisions against existing codebase patterns
- Include actual code snippets showing how similar things are done
- Reference specific file paths for implementation guidance
