---
name: feature-dev
description: Feature development workflow with exploration, architecture, implementation, and review phases. Use for implementing new features or significant changes.
argument-hint: <feature-description> [--teams]
model: inherit
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

# Feature Development Workflow

Execute a structured 7-phase feature development workflow. This workflow guides you through understanding, exploring, designing, implementing, and reviewing a feature.

**CRITICAL: Complete ALL 7 phases.** The workflow is not complete until Phase 7: Summary is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Phase Overview

Execute these phases in order, completing ALL of them:

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

2. Summarize your understanding to the user. Use AskUserQuestion to confirm if your understanding is correct before proceeding.

---

## Phase 2: Codebase Exploration

**Goal:** Understand the relevant parts of the codebase.

1. **Run deep-analysis workflow:**
   - Check if the original `$ARGUMENTS` contains `--teams` flag
   - If `--teams` is present:
     - Read `${CLAUDE_PLUGIN_ROOT}/skills/teams-deep-analysis/SKILL.md` and follow its workflow
     - Remove `--teams` from the analysis context passed to the skill
   - Otherwise:
     - Read `${CLAUDE_PLUGIN_ROOT}/skills/deep-analysis/SKILL.md` and follow its workflow (default)
   - Pass the feature description from Phase 1 as the analysis context
   - This handles exploration (parallel code-explorer agents) and synthesis (codebase-synthesizer agent)

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
   Use AskUserQuestion to get answers for critical unknowns. Only ask questions that would significantly impact the implementation.

   If no clarifying questions are needed, inform the user and proceed.

---

## Phase 4: Architecture Design

**Goal:** Design the implementation approach.

1. **Load skills for this phase:**
   - Read `${CLAUDE_PLUGIN_ROOT}/skills/architecture-patterns/SKILL.md` and apply its guidance
   - Read `${CLAUDE_PLUGIN_ROOT}/skills/language-patterns/SKILL.md` and apply its guidance

2. **Launch code-architect agents:**

   Launch 2-3 code-architect agents (Opus) with different approaches:
   ```
   Agent 1: Design a minimal, focused approach prioritizing simplicity
   Agent 2: Design a flexible, extensible approach prioritizing future changes
   Agent 3: Design an approach optimized for the project's existing patterns (if applicable)
   ```

   Use the Task tool with `subagent_type: "claude-alchemy-tools:code-architect"`:
   ```
   Feature: [feature description]
   Design approach: [specific approach for this agent]

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
   Use AskUserQuestion to let the user select an approach or request modifications.

5. **Generate ADR artifact:**
   - Read the ADR template from `${CLAUDE_PLUGIN_ROOT}/skills/feature-dev/references/adr-template.md`
   - Create an ADR documenting:
     - Context: Why this feature is needed
     - Decision: The chosen approach
     - Consequences: Trade-offs and implications
     - Alternatives: Other approaches considered
   - Determine the next ADR number by checking existing files in `internal/docs/adr/`
   - Save to `internal/docs/adr/NNNN-[feature-slug].md` (create `internal/docs/adr/` if needed)
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
   - Update existing files using Edit tool
   - Add appropriate error handling
   - Include inline comments only where logic isn't obvious

4. **Test if applicable:**
   - If the project has tests, add tests for the new functionality
   - Run existing tests to ensure nothing broke

5. **IMPORTANT: Proceed immediately to Phase 6.**
   Do NOT stop here. Do NOT wait for user input. Implementation is complete, but the workflow requires Quality Review and Summary phases. Continue directly to Phase 6 now.

---

## Phase 6: Quality Review

**Goal:** Review the implementation for issues.

1. **Load skills for this phase:**
   - Read `${CLAUDE_PLUGIN_ROOT}/skills/code-quality/SKILL.md` and apply its guidance

2. **Launch code-reviewer agents:**

   Launch 3 code-reviewer agents (Opus) with different focuses:
   ```
   Agent 1: Review for correctness and edge cases
   Agent 2: Review for security and error handling
   Agent 3: Review for maintainability and code quality
   ```

   Use the Task tool with `subagent_type: "claude-alchemy-tools:code-reviewer"`:
   ```
   Review focus: [specific focus for this agent]

   Files to review:
   [List of files modified/created]

   Review the implementation and report:
   - Issues found with confidence scores (0-100)
   - Suggestions for improvement
   - Positive observations

   Only report issues with confidence >= 80.
   ```

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
   Use AskUserQuestion:
   - "Fix all issues now"
   - "Fix critical issues only"
   - "Proceed without fixes"
   - "I'll fix manually later"

6. If fixing: make the changes and re-review if needed.

7. **IMPORTANT: Proceed immediately to Phase 7.**
   Do NOT stop here. The workflow requires a Summary phase to document accomplishments and update the CHANGELOG. Continue directly to Phase 7 now.

---

## Phase 7: Summary

**Goal:** Document and celebrate accomplishments.

1. **Summarize accomplishments:**
   Present to the user:
   - What was built
   - Key files created/modified
   - Architecture decisions made
   - Any known limitations or future work

2. **Update CHANGELOG.md:**
   - Read the entry template from `${CLAUDE_PLUGIN_ROOT}/skills/feature-dev/references/changelog-entry-template.md`
   - Load the `changelog-format` skill for Keep a Changelog guidelines
   - Create an entry under the `[Unreleased]` section with:
     - Appropriate category (Added, Changed, Fixed, etc.)
     - Concise description of the feature
   - If `CHANGELOG.md` doesn't exist, create it with proper header
   - Add the entry to the appropriate section under `[Unreleased]`
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

## Agent Coordination

Exploration and synthesis agent coordination is handled by the `deep-analysis` skill in Phase 2. See that skill for agent model tiers and failure handling details.

When launching other parallel agents (code-architect, code-reviewer):
- Give each agent a distinct focus area
- Wait for all agents to complete before proceeding
- Handle agent failures gracefully (continue with partial results)

When calling Task tool for agents:
- Use `model: "opus"` for code-architect and code-reviewer agents
- Code-explorer and codebase-synthesizer models are managed by deep-analysis

## Additional Resources

- For ADR template, see [references/adr-template.md](references/adr-template.md)
- For changelog entry format, see [references/changelog-entry-template.md](references/changelog-entry-template.md)
