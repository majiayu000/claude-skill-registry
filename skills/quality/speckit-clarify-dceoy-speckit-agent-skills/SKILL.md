---
name: speckit-clarify
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
handoffs:
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
---

# Spec-Kit Clarify

Detect and reduce ambiguity in feature specifications through targeted questioning. Optional step between speckit-specify and speckit-plan.

## When to Use

- After creating spec.md with `speckit-specify`
- Spec contains vague terms ("fast", "intuitive", "robust")
- Missing decision points or placeholders (TODO, ???)
- Before planning when requirements seem incomplete

## Execution Workflow

This workflow runs BEFORE `/speckit.plan`. If user explicitly skips clarification, warn that downstream rework risk increases.

**CRITICAL LIMITS:**

- **Maximum 5 questions** per session (total asked)
- **ONE question at a time** - never batch questions
- **Provide recommendations** for all questions based on best practices
- **User can reply "yes"** to accept recommendation

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` once to get FEATURE_DIR and FEATURE_SPEC
2. **Load spec** and perform structured ambiguity scan across 11 categories:
   - Functional Scope & Behavior
   - Domain & Data Model
   - Interaction & UX Flow
   - Non-Functional Quality Attributes
   - Integration & External Dependencies
   - Edge Cases & Failure Handling
   - Constraints & Tradeoffs
   - Terminology & Consistency
   - Completion Signals
   - Misc/Placeholders
3. **Generate prioritized queue** of candidate clarification questions (max 5):
   - Prioritize by (Impact × Uncertainty) heuristic
   - High impact: security/auth, data model, API contracts, performance, acceptance criteria
   - High uncertainty: vague adjectives, multiple approaches, missing constraints, undefined terms
   - Skip low-priority: stylistic preferences, implementation details, already answered
4. **Sequential questioning loop** (interactive):
   - Present EXACTLY ONE question at a time
   - For multiple-choice: Analyze all options, recommend the best one with reasoning
   - For short-answer: Provide suggested answer based on best practices
   - User can reply "yes"/"recommended"/"suggested" to accept recommendation
   - After answer: Record in working memory, move to next question
   - Stop when: critical ambiguities resolved, user signals completion, or 5 questions reached
5. **Integration after EACH accepted answer** (incremental update - NOT batched):
   - **CRITICAL**: Update spec file after EACH answer, not at the end
   - Maintain in-memory spec representation
   - First answer: Create/ensure `## Clarifications` section with `### Session YYYY-MM-DD` subheading
   - Append bullet: `- Q: <question> → A: <final answer>`
   - Apply clarification to appropriate section (Functional Requirements, NFRs, Data Model, etc.)
   - Replace vague statement instead of duplicating
   - **Save spec file immediately** AFTER each integration (atomic overwrite prevents context loss)
6. **Validation** after each write:
   - One bullet per accepted answer in Clarifications
   - No duplicate entries or contradictory statements
   - Updated sections clear and specific
   - Markdown structure valid
7. **Report completion**:
   - Number of questions asked & answered
   - Path to updated spec
   - Sections touched
   - Coverage summary table (Resolved/Deferred/Clear/Outstanding)
   - Suggest next command (`/speckit.plan` or run `/speckit.clarify` again)

## Key Points

- **Maximum 5 questions** per session (total asked)
- **ONE question at a time** - never batch
- **Provide recommendations** for all questions based on best practices
- **Accept "yes"** to use recommendation
- **Integrate answers immediately** after each acceptance
- **Constitution is non-negotiable** - constitution conflicts are always CRITICAL
- **Limit to 3 clarifications in specify** - this is for additional refinement
- **Skip if low-impact** - only ask questions that materially change implementation/validation
- **Early termination allowed** - user can say "stop", "done", "proceed"

## Next Steps

After clarification:

- **Plan** with `speckit-plan` - Create technical design
- **Re-clarify** if new ambiguities emerge during planning

## See Also

- `speckit-specify` - Create feature specifications
- `speckit-plan` - Create technical implementation strategy
