---
name: feature-dev
description: Feature development workflow with exploration, architecture, implementation, and review phases. Use for implementing new features or significant changes.
dependencies:
  - architecture-patterns
  - code-quality
  - changelog-format
  - deep-analysis (core-tools)
  - language-patterns (core-tools)
  - technical-diagrams (core-tools)
---

# Feature Development Workflow

Execute a structured 7-phase feature development workflow. This workflow guides you through understanding, exploring, designing, implementing, and reviewing a feature.

## Phase Overview

Execute these phases in order:

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

1. Analyze the feature description from `$ARGUMENTS`:
   - What is the core functionality?
   - What are the expected inputs and outputs?
   - Are there any constraints mentioned?
   - What success criteria can you infer?

2. Summarize your understanding to the user. Prompt the user to confirm if your understanding is correct before proceeding.

---

## Phase 2: Codebase Exploration

**Goal:** Understand the relevant parts of the codebase.

1. **Run deep-analysis workflow:**
   - Refer to the **deep-analysis** skill (from the core-tools package) and follow its workflow
   - Pass the feature description from Phase 1 as the analysis context
   - This handles reconnaissance, team planning, parallel exploration, and synthesis
   - Deep-analysis may return cached results if a valid exploration cache exists. When invoked by another skill, cache hits are auto-accepted to avoid redundant exploration.

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

1. **Load reference skills for this phase:**
   - Refer to the **architecture-patterns** skill for pattern guidance
   - Refer to the **language-patterns** skill (from the core-tools package) for language-specific patterns
   - Refer to the **technical-diagrams** skill (from the core-tools package) for Mermaid diagram styling rules in architecture proposals

2. **Launch architecture agents:**

   Spawn 2-3 architecture design agents with different approaches:
   - Agent 1: Design a minimal, focused approach prioritizing simplicity
   - Agent 2: Design a flexible, extensible approach prioritizing future changes
   - Agent 3: Design an approach optimized for the project's existing patterns (if applicable)

   Refer to the **code-architect** agent (from the core-tools package) for this role.

   Each agent receives:
   - Feature description
   - Design approach emphasis
   - Summary of relevant files and patterns from codebase exploration
   - Instructions to list files to create/modify, describe changes, explain data flow, and identify risks

3. **Present approaches:**
   - Summarize each approach
   - Compare trade-offs (simplicity, flexibility, performance, maintainability)
   - Make a recommendation with justification

4. **User chooses approach:**
   Prompt the user to select an approach or request modifications.

5. **Generate ADR artifact:**

   Create an Architecture Decision Record documenting:
   - Context: Why this feature is needed
   - Decision: The chosen approach
   - Consequences: Trade-offs and implications
   - Alternatives: Other approaches considered

   **ADR Template:**

   ```markdown
   # ADR-NNNN: [Title]

   **Date:** YYYY-MM-DD
   **Status:** Accepted
   **Feature:** [Feature name/description]

   ## Context

   [Describe the situation: what problem, what constraints, what driving forces]

   ## Decision

   [What approach, key architectural choices, technologies/patterns selected]

   ## Consequences

   ### Positive
   - [Benefits]

   ### Negative
   - [Tradeoffs]

   ### Risks
   - [Risk and mitigation]

   ## Alternatives Considered

   ### Alternative 1: [Name]
   [Brief description]
   - **Pros:** [List]
   - **Cons:** [List]
   - **Why rejected:** [Reason]

   ## Implementation Notes

   [Key files, patterns, integration points]
   ```

   - Determine the next ADR number by checking existing files in `internal/docs/adr/`
   - Save to `internal/docs/adr/NNNN-[feature-slug].md` (create directory if needed)
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

1. **Load reference skill for this phase:**
   - Refer to the **code-quality** skill for review criteria

2. **Launch code-reviewer agents:**

   Spawn 3 code-reviewer agents with different focuses:
   - Agent 1: Review for correctness and edge cases
   - Agent 2: Review for security and error handling
   - Agent 3: Review for maintainability and code quality

   Each agent receives:
   - Review focus area
   - List of files modified/created
   - Instructions to report issues with confidence scores (0-100), suggestions, and positive observations
   - Only report issues with confidence >= 80

3. **Aggregate findings:**
   - Collect results from all reviewers
   - Deduplicate similar issues
   - Prioritize by severity and confidence

4. **Present findings:**
   Show the user:
   - Critical issues (must fix)
   - Moderate issues (should fix)
   - Minor suggestions (nice to have)

5. **User decides:**
   Prompt the user:
   - "Fix all issues now"
   - "Fix critical issues only"
   - "Proceed without fixes"
   - "I'll fix manually later"

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

   Create an entry under the `[Unreleased]` section following Keep a Changelog guidelines:

   **Changelog Entry Template:**

   ```markdown
   ### Added
   - Add [feature name] with [key capability]

   ### Changed
   - Update [component] to [new behavior]

   ### Fixed
   - Fix [issue description]
   ```

   **Instructions:**
   - Locate CHANGELOG.md in the repository root (create if it doesn't exist)
   - Find the `[Unreleased]` section
   - Choose the appropriate category (Added, Changed, Fixed, etc.)
   - Use imperative mood ("Add feature" not "Added feature")
   - Focus on user-facing changes, one line per distinct change
   - Reference related ADRs if applicable (e.g., "Add JWT-based authentication (see ADR-0003)")

   Refer to the **changelog-format** skill for additional Keep a Changelog guidelines.

   **Categories Reference:**

   | Category | Use For |
   |----------|---------|
   | **Added** | New features |
   | **Changed** | Changes to existing functionality |
   | **Deprecated** | Features that will be removed in future |
   | **Removed** | Features that were removed |
   | **Fixed** | Bug fixes |
   | **Security** | Security improvements |

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

## Agent Coordination

Exploration and synthesis agent coordination is handled by the deep-analysis skill in Phase 2, which manages parallel exploration agents and a synthesis agent. Deep-analysis performs reconnaissance, composes a team plan, assembles the team, and manages the exploration/synthesis lifecycle.

When launching other parallel agents (code-architect from core-tools, code-reviewer):
- Give each agent a distinct focus area
- Wait for all agents to complete before proceeding
- Handle agent failures gracefully (continue with partial results)

---

## Integration Notes
**What this component does:** Orchestrates a complete 7-phase feature development lifecycle: discovery, codebase exploration (via deep-analysis), clarifying questions, architecture design with multiple proposals, implementation, quality review, and summary with changelog update.
**Capabilities needed:** Shell execution, file reading/writing/editing, pattern search, sub-agent spawning (code-architect from core-tools, code-reviewer, deep-analysis from core-tools), user interaction.
**Adaptation guidance:** This skill depends heavily on sub-agent coordination. Phase 2 delegates to deep-analysis (core-tools). Phase 4 spawns architecture agents. Phase 6 spawns reviewer agents. Adapt agent spawning to your platform's sub-task mechanism. The ADR template and changelog entry template are inlined in this skill.
**Sub-agent capabilities:** Code-architect agents (from core-tools) need read-only file access and search for producing architecture proposals. Code-reviewer agents need read-only file access and search for producing review reports with confidence-scored findings.
