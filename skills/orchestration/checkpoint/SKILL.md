---
name: checkpoint
description: |
  Meta-cognitive decision support that analyzes current context and surfaces intelligent next-step options to the user. Use this skill when: (1) User explicitly invokes /checkpoint, (2) Significant work has been completed and a checkpoint is valuable, (3) Uncertainty or ambiguity exists about requirements or approach, (4) Task complexity has expanded beyond initial scope, (5) Before finalizing or committing to ensure nothing is missed. This skill pauses execution, assesses the situation holistically, and presents 2-5 contextually-appropriate options via AskUserQuestion, with a recommended option and rationale.
---

# Checkpoint

Pause, assess, and surface intelligent next-step options to the user.

## When to Trigger Proactively

Suggest this skill (without being asked) when detecting:

- **Completion signal**: A feature, fix, or milestone just finished
- **Uncertainty signal**: Requirements unclear, multiple valid paths, or low confidence in current direction
- **Complexity signal**: Scope expanded, unexpected dependencies emerged, or task is taking longer than expected
- **Drift signal**: Work may have diverged from user's original intent
- **Quality signal**: Code works but may benefit from review, testing, or refactoring

## Workflow

### 1. Context Assessment

Silently evaluate the current state across these dimensions (do not output this analysis):

- **Progress**: What has been accomplished? What remains?
- **Quality**: Is the work solid, or are there rough edges?
- **Alignment**: Does recent work match what the user actually wants?
- **Uncertainty**: What assumptions were made? What's unclear?
- **Risk**: What could go wrong? What hasn't been tested?
- **Efficiency**: Is there a better path forward?

### 2. Generate Options

Based on assessment, generate 2-5 contextually-appropriate options. Draw from (but don't limit to) these archetypes:

| Archetype | When Relevant |
|-----------|---------------|
| **Commit progress** | Meaningful progress made, good stopping point |
| **Systems audit** | Complex changes, potential for bugs or regressions |
| **Prioritize/plan** | Multiple pending tasks, unclear what matters most |
| **Re-evaluate decisions** | Low confidence in recent choices, new information available |
| **Clarify with user** | Assumptions made, requirements ambiguous |
| **Test/verify** | Code works but edge cases untested |
| **Refactor/clean up** | Code functional but messy |
| **Document** | Complex logic that needs explanation |
| **Step back** | May be overcomplicating or missing simpler solution |
| **Continue current path** | Clear next step, no reason to pause |

**Option generation principles:**
- Options should be meaningfully different, not variations of the same thing
- Include at least one "continue forward" option when momentum is valuable
- Include at least one "pause and verify" option when risk is present
- Avoid analysis paralysis - fewer sharp options beat many vague ones

### 3. Select Recommendation

Choose one option as recommended. The recommendation should reflect:

- What would a thoughtful senior engineer do here?
- What reduces risk of wasted effort or rework?
- What serves the user's underlying goals (not just stated requests)?

### 4. Present via AskUserQuestion

Use AskUserQuestion with this structure:

```
Question: "What would you like to do next?"
Header: "Next step" (or contextually appropriate 1-2 words)
Options: [generated options with descriptions]
```

**Option format:**
- `label`: Action verb phrase (e.g., "Commit current progress", "Run systems audit")
- `description`: 1 sentence explaining what this involves and why it might be valuable

**Recommendation:**
- Place recommended option FIRST in the list
- Append "(Recommended)" to its label
- Include rationale in the description

### Example Output

For a scenario where a feature was just implemented but with some shortcuts:

```
AskUserQuestion:
  question: "Feature implementation complete. What would you like to do next?"
  header: "Next step"
  options:
    - label: "Review and refactor (Recommended)"
      description: "Clean up the shortcuts taken during implementation before they become technical debt. The core logic works but could be more maintainable."
    - label: "Add test coverage"
      description: "Write tests for the new feature to catch edge cases and prevent regressions."
    - label: "Commit and move on"
      description: "The feature works - commit it and tackle the next task. Can refactor later if needed."
    - label: "Walk me through what was built"
      description: "Explain the implementation so you can verify it matches your expectations before proceeding."
```

## Anti-Patterns

- **Don't overthink**: This skill should take seconds, not minutes
- **Don't list every possible option**: Curate the most valuable 2-5
- **Don't recommend "ask user" when the situation is clear**: Have a point of view
- **Don't trigger too frequently**: Reserve for genuine decision points, not every minor step
- **Don't explain the assessment process**: Just present the options naturally
