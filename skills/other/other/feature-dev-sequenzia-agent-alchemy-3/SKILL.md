---
name: feature-dev
description: Feature development workflow with exploration, architecture, implementation, and review phases. Use for implementing new features or significant changes.
dependencies:
  - deep-analysis
  - architecture-patterns
  - language-patterns
  - technical-diagrams
  - code-quality
  - code-architect
  - code-reviewer
  - changelog-format
---

# Feature Development Workflow

Execute a structured 7-phase feature development workflow. This workflow guides you through understanding, exploring, designing, implementing, and reviewing a feature.

## Phase Overview

Execute these phases in order, completing all of them:

1. **Discovery** - Understand the feature requirements
2. **Codebase Exploration** - Map relevant code areas
3. **Clarifying Questions** - Resolve ambiguities
4. **Architecture Design** - Design the implementation approach
5. **Implementation** - Build the feature
6. **Quality Review** - Review for issues
7. **Summary** - Document accomplishments

---

## Phase 1: Discovery

**Goal:** Understand what the user wants to build.

1. Analyze the feature description from the provided inputs:
   - What is the core functionality?
   - What are the expected inputs and outputs?
   - Are there any constraints mentioned?
   - What success criteria can you infer?

2. Summarize your understanding to the user. Prompt the user to confirm your understanding is correct before proceeding.

---

## Phase 2: Codebase Exploration

**Goal:** Understand the relevant parts of the codebase.

1. **Run the deep-analysis workflow:**
   - Refer to the **deep-analysis** skill (from the core-tools package) for codebase exploration
   - Pass the feature description from Phase 1 as the analysis context
   - This handles reconnaissance, team planning, parallel exploration, and synthesis
   - The deep-analysis skill may return cached results if a valid exploration cache exists. When invoked by another skill, cache hits are auto-accepted.

2. Present the synthesized analysis to the user.

---

## Phase 3: Clarifying Questions

**Goal:** Resolve any ambiguities before designing.

1. Review the feature requirements and exploration findings.

2. Identify underspecified aspects:
   - Edge cases not covered
   - Technical decisions that could go multiple ways
   - Integration points that need clarification
   - Performance or scale requirements

3. **Ask clarifying questions:**
   Prompt the user to get answers for critical unknowns. Only ask questions that would significantly impact the implementation.

   If no clarifying questions are needed, inform the user and proceed.

---

## Phase 4: Architecture Design

**Goal:** Design the implementation approach.

1. **Load skills for this phase:**
   - Refer to the **architecture-patterns** skill for architectural pattern guidance
   - Refer to the **language-patterns** skill (from the core-tools package) for language-specific patterns
   - Refer to the **technical-diagrams** skill (from the core-tools package) for Mermaid diagram styling rules

2. **Design 2-3 architecture approaches:**

   Delegate to architecture specialists (refer to the **code-architect** skill from core-tools) with different design philosophies:
   ```
   Approach 1: Design a minimal, focused approach prioritizing simplicity
   Approach 2: Design a flexible, extensible approach prioritizing future changes
   Approach 3: Design an approach optimized for the project's existing patterns (if applicable)
   ```

   For each approach, provide:
   ```
   Feature: [feature description]
   Design approach: [specific approach]

   Based on the codebase exploration:
   [Summary of relevant files and patterns]

   Design an implementation that:
   - Lists files to create/modify
   - Describes the changes needed in each file
   - Explains the data flow
   - Identifies risks and mitigations

   Return a detailed implementation blueprint.
   ```

3. **Present approaches:**
   - Summarize each approach
   - Compare trade-offs (simplicity, flexibility, performance, maintainability)
   - Make a recommendation with justification

4. **User chooses approach:**
   Prompt the user to select an approach or request modifications.

5. **Generate ADR artifact:**

   Create an Architecture Decision Record using this template:

   ```markdown
   # ADR-NNNN: [Title]

   **Date:** YYYY-MM-DD
   **Status:** Accepted
   **Feature:** [Feature name/description]

   ## Context

   [Describe the situation that led to this decision. Include:]
   - What problem are we solving?
   - What constraints do we have?
   - What are the driving forces?

   ## Decision

   [State the decision clearly and concisely. Include:]
   - What approach are we taking?
   - Key architectural choices made
   - Technologies/patterns selected

   ## Consequences

   ### Positive
   - [Benefit 1]
   - [Benefit 2]
   - [Benefit 3]

   ### Negative
   - [Tradeoff 1]
   - [Tradeoff 2]

   ### Risks
   - [Risk 1 and mitigation]
   - [Risk 2 and mitigation]

   ## Alternatives Considered

   ### Alternative 1: [Name]
   [Brief description]
   - **Pros:** [List]
   - **Cons:** [List]
   - **Why rejected:** [Reason]

   ### Alternative 2: [Name]
   [Brief description]
   - **Pros:** [List]
   - **Cons:** [List]
   - **Why rejected:** [Reason]

   ## Implementation Notes

   [Any specific implementation guidance:]
   - Key files to create/modify
   - Important patterns to follow
   - Integration points

   ## References

   - [Link to related docs]
   - [Link to similar implementations]
   ```

   Usage:
   - Determine the next ADR number by checking existing files in `internal/docs/adr/`
   - If no ADRs exist, start with 0001
   - Save to `internal/docs/adr/NNNN-[feature-slug].md` (create the directory if needed)
   - Inform the user of the saved ADR location

---

## Phase 5: Implementation

**Goal:** Build the feature.

1. **Require explicit approval:**
   Ask the user: "Ready to begin implementation of [feature] using [chosen approach]?"
   Wait for confirmation before proceeding.

2. **Read all relevant files:**
   Before making any changes, read the complete content of every file you'll modify.

3. **Implement the feature:**
   - Follow the chosen architecture design
   - Match existing code patterns and conventions
   - Create new files as needed
   - Update existing files
   - Add appropriate error handling
   - Include inline comments only where logic isn't obvious

4. **Test if applicable:**
   - If the project has tests, add tests for the new functionality
   - Run existing tests to ensure nothing broke

5. Proceed immediately to Phase 6.

---

## Phase 6: Quality Review

**Goal:** Review the implementation for issues.

1. **Load skills for this phase:**
   - Refer to the **code-quality** skill for quality principles

2. **Delegate to code review specialists:**

   Delegate to the **code-reviewer** skill with 3 different focuses:
   ```
   Reviewer 1: Review for correctness and edge cases
   Reviewer 2: Review for security and error handling
   Reviewer 3: Review for maintainability and code quality
   ```

   For each review:
   ```
   Review focus: [specific focus]

   Files to review:
   [List of files modified/created]

   Review the implementation and report:
   - Issues found with confidence scores (0-100)
   - Suggestions for improvement
   - Positive observations

   Only report issues with confidence >= 80.
   ```

3. **Aggregate findings:**
   - Collect results from all reviews
   - Deduplicate similar issues
   - Prioritize by severity and confidence

4. **Present findings:**
   Show the user:
   - Critical issues (must fix)
   - Moderate issues (should fix)
   - Minor suggestions (nice to have)

5. **User decides:**
   Prompt the user:
   - **"Fix all issues now"**
   - **"Fix critical issues only"**
   - **"Proceed without fixes"**
   - **"I'll fix manually later"**

6. If fixing: make the changes and re-review if needed.

7. Proceed immediately to Phase 7.

---

## Phase 7: Summary

**Goal:** Document and celebrate accomplishments.

1. **Summarize accomplishments:**
   Present to the user:
   - What was built
   - Key files created/modified
   - Architecture decisions made
   - Architecture diagram (Mermaid flowchart showing the implemented structure)
   - Any known limitations or future work

2. **Update CHANGELOG.md:**

   Refer to the **changelog-format** skill for Keep a Changelog guidelines.

   Entry format:
   ```markdown
   ### Added
   - Add [feature name] with [key capability]

   ### Changed
   - Update [component] to [new behavior]

   ### Fixed
   - Fix [issue description]
   ```

   Steps:
   - Find the project's `CHANGELOG.md` in the repository root
   - If it doesn't exist, create it with the standard Keep a Changelog header
   - Create an entry under the `[Unreleased]` section with:
     - Appropriate category (Added, Changed, Fixed, etc.)
     - Concise, user-focused description using imperative mood
   - Inform the user of the update

3. **Final message:**
   Congratulate the user and offer next steps:
   - Commit the changes
   - Create a PR
   - Additional testing suggestions

---

## Error Handling

If any phase fails:
1. Explain what went wrong
2. Ask the user how to proceed:
   - Retry the phase
   - Skip to next phase
   - Abort the workflow

---

## Coordination Notes

- **Phase 2**: Codebase exploration is handled by the deep-analysis skill, which coordinates parallel exploration and synthesis.
- **Phase 4**: Architecture design benefits from delegating to multiple specialists with different design philosophies. Give each a distinct approach; wait for all to complete before presenting.
- **Phase 6**: Code review benefits from delegating to multiple specialists with different focus areas. Handle failures gracefully — continue with partial results.

---

## Integration Notes

This skill was converted from the dev-tools plugin package. It orchestrates a complete feature development lifecycle across 7 phases. Dependencies span both the dev-tools and core-tools packages: deep-analysis, architecture-patterns, language-patterns, technical-diagrams (from core-tools); code-quality, code-reviewer, changelog-format (from dev-tools); and code-architect (from core-tools). The ADR template and changelog entry template have been inlined.
