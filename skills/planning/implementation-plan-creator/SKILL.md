---
name: implementation-plan-creator
description: Create feature implementation plans before development. Captures requirements, acceptance criteria, non-goals, risks, and implementation complexity in structured markdown. Use when starting a new feature to ensure scope clarity and implementation guidance.
license: MIT
allowed-tools: Bash(git:*) Read Bash(ls:*)
metadata:
  generated-at: "2026-01-09T00:00:00Z"
  group: "development"
  category: "planning"
  difficulty: "intermediate"
  step-count: "3"
---

# Implementation Plan Creator

## What You'll Do
- 📋 Gather planning details (scope, requirements, non-goals, risks, and implementation complexity)
- ✍️ Generate a structured markdown implementation plan file
- ✅ Ensure the plan lives in a `plans/` directory with proper naming convention

---

## Concept Introduction

An **implementation plan** is a specification-driven markdown document that captures everything needed to develop a feature: what the feature does, what success looks like, how it will be built, and who will build it. Creating a clear implementation plan before coding ensures:

- **Scope clarity**: Everyone understands what's being built, why, and what's NOT being built
- **Specification completeness**: Feature requirements and acceptance criteria are documented upfront
- **Risk awareness**: Potential challenges and dependencies are identified early
- **Implementation guidance**: Approach and technical considerations guide development decisions
- **Complexity clarity**: Key factors affecting implementation are documented upfront
- **Progress tracking**: Acceptance criteria serve as a checklist during development

Implementation plans live in a `plans/` directory with filenames following the pattern: `YYYY-MM-DD-feature-short-name.md`

Key sections: **Overview** → **Requirements** → **Non-Goals** → **Acceptance Criteria** → **Implementation Complexity** → **Implementation** → **Risks** → **Dependencies** → **References**

---

## When to Use This Skill

Use this skill when you're:
- ✅ Starting development on a new feature
- ✅ Adding new capability or user-facing functionality
- ✅ Need to document scope, requirements, and success criteria before coding

**Do NOT use** if you're:
- ❌ Fixing bugs or issues
- ❌ Completing technical chores (refactoring, dependencies, infrastructure)
- ❌ Making minor fixes or documentation updates
- ❌ Working on quick, well-defined tasks without planning needs

**Decision Point:** Is this a new feature or user-facing capability?

- **YES** → Proceed to Phase 1. You're in the right place.
- **NO** → This skill is not a good fit. Focus on the work without a plan.

---

## Phase 1: 📋 ANALYSIS - Understand the Feature

**What you're doing:** Gathering the information needed to create a comprehensive feature implementation plan.

**Decision Point:** How much detail do you already have?

- **Full details** (requirements, risks, implementation approach) → Skip to Phase 2 to create the plan directly.
- **Partial info** (some details missing) → Work through Phase 1 sections to fill gaps.
- **High-level only** (just the idea) → Work through Phase 1 comprehensively to understand the feature fully.

For guidance on what questions to ask at each mode, see [references/agent-modes.md](./references/agent-modes.md).

**Now clarify these aspects of your feature:**

### 1. Title & Overview
Define what you're building:
- **Title**: Short, clear name (e.g., "Add dark mode toggle", "Implement two-factor authentication", "Create user profile editor")
- **Overview**: 1-2 sentences explaining what the feature does and why it matters

**Example:**

```text
Title: Add Dark Mode Toggle
Overview: Enable users to switch between light and dark themes with preference persistence across sessions. This improves usability for users working in low-light environments.
```

### 2. Requirements
List 3-5 specific requirements that must be true:
- **What capabilities** does this feature provide?
- **What must work** across different scenarios?
- **What systems or data** does it interact with?

**Example requirements:**

```markdown
- Users can toggle dark mode from Settings page
- Dark mode preference persists across browser sessions
- All UI elements remain readable in both light and dark modes
- Dark mode works consistently on mobile and desktop
- Theme applies instantly without page reload
```

### 3. Acceptance Criteria
Define testable criteria that verify the feature is complete:
- **What will be true** when this feature is done?
- **What can be tested** to verify success?
- **What edge cases** should be handled?

### 4. Non-Goals
Clarify what will NOT be built to keep scope focused.

### 5. Risks & Mitigations
Identify potential issues and how you'll address them.

### 6. Dependencies
List external services, libraries, approvals, or team dependencies required.

### 7. Implementation Complexity
Document factors affecting implementation complexity (dependencies, integration points, testing needs, potential challenges).

**Verification Checklist:**

- [ ] Feature title is clear and descriptive
- [ ] Overview explains the feature (what and why)
- [ ] 3-5 requirements documented
- [ ] Non-goals are explicit
- [ ] Acceptance criteria are testable
- [ ] Risks and mitigations identified
- [ ] Dependencies listed
- [ ] Implementation complexity factors documented

### ✅ PHASE 1 COMPLETE

All items checked? Great! You're ready for Phase 2. Your feature is well-understood and scoped. Now you'll create the actual implementation plan file.

---

## Phase 2: ✍️ COMPOSITION - Create the Implementation Plan

**What you're doing:** Generating the markdown implementation plan file in the `plans/` directory with proper formatting and structure.

### File Creation
Generate a markdown file with:
- **Filename**: `YYYY-MM-DD-feature-short-name.md` (e.g., `2026-01-09-dark-mode-toggle.md`)
- **Location**: `plans/` directory (created automatically if needed)
- **Format**: Markdown with sections below

### Implementation Plan Template Structure

```markdown
# [Feature Title]

## Overview
[What the feature does and why it matters - 1-2 sentences]

## Requirements
- Requirement 1
- Requirement 2
- Requirement 3
- Requirement 4
- Requirement 5

## Non-Goals
- Non-goal 1
- Non-goal 2
- Non-goal 3

## Acceptance Criteria
- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2
- [ ] Acceptance criterion 3
- [ ] Acceptance criterion 4
- [ ] Acceptance criterion 5

## Implementation Complexity
**Factors:** [Key factors affecting complexity - dependencies, integration points, testing scope, known challenges]

## Implementation

### Approach
[High-level strategy and technology choices]

### Implementation Steps
1. **[Step title]** - `path/to/file.ts`
   - What to do and why
   - Suggested code snippet based on existing codebase patterns:
   ```typescript
   // Example implementation
   ```

2. **[Step title]** - `path/to/file2.ts`
   - What to do and why
   - Suggested code snippet based on existing codebase patterns:
   ```typescript
   // Example implementation
   ```

## Risks
- Risk 1
  - Mitigation: [How to address]
- Risk 2
  - Mitigation: [How to address]

## Dependencies
- Dependency 1 (version X)
- Dependency 2 (version Y)
- External requirement (description)

## References
[Links to relevant documentation, issues, or related code]
```

### Creation Steps

1. **Prepare directory** - Ensure `plans/` directory exists
   ```bash
   ./scripts/ensure-plans-dir.sh
   ```

2. **Generate filename** - Use today's date + short feature name
   - Today's date: YYYY-MM-DD format
   - Feature short name: 2-4 words, lowercase, hyphenated
   - Example: `2026-01-09-user-authentication.md`

3. **Populate sections** - Fill in each section from Phase 1 analysis
   - Keep descriptions concise
   - Use checkboxes for criteria
   - Be specific about file modifications

**Verification Checklist:**

- [ ] File created in `plans/` directory
- [ ] Filename follows correct pattern
- [ ] All required sections present
- [ ] Requirements are specific
- [ ] Acceptance criteria are testable
- [ ] Implementation notes are clear
- [ ] No placeholder text in any section

### ✅ PHASE 2 COMPLETE

All items checked? Excellent! Your implementation plan markdown is written and structured. Now you'll verify it's complete and ready for use.

---

## Phase 3: ✅ VALIDATION - Finalize the Plan

**What you're doing:** Verifying the implementation plan is complete, clear, and ready for development.

### Quality Checks

1. **Completeness**
   - [ ] All sections filled in (no "TBD" or empty sections)
   - [ ] Requirements and acceptance criteria are specific
   - [ ] Implementation notes provide actionable direction

2. **Clarity**
   - [ ] Title clearly describes what's being built
   - [ ] Description can be understood by someone unfamiliar with the work
   - [ ] Acceptance criteria are unambiguous

3. **Actionability**
   - [ ] Implementation notes identify specific files to modify
   - [ ] Approach is clear enough to guide development
   - [ ] Challenges and mitigations are documented

4. **File Structure**
   - [ ] File is in `plans/` directory
   - [ ] Filename matches convention: `YYYY-MM-DD-feature-short-name.md`
   - [ ] Markdown is properly formatted

### Decision Point: Is the plan ready?

- **YES** (all validation checks pass) → Plan is complete and ready to use
- **NO** (missing sections or unclear requirements) → Return to Phase 1 or 2 to refine

**When the plan is ready:**
- Share with team/stakeholders for feedback
- Use as reference while implementing
- Check off acceptance criteria during development
- Close the plan when work is complete

### ✅ PHASE 3 COMPLETE

All quality checks passed? Perfect! Your implementation plan is complete, validated, and ready for development. You have a clear roadmap for building this feature with documented requirements, success criteria, estimated effort, and identified risks.

---

## Phase 4: 🎯 POST-EXECUTION - Verify Best Practices

**What you're doing:** Validating the implementation plan against best practices before it's ready for use.

After completing Phase 3, verify the plan follows these best practices:

### Best Practices Checklist

- [ ] **Specific, not vague** - Requirements and criteria use concrete language ("Users can...", "The button will..."), not "system should improve"
- [ ] **Non-goals are explicit** - At least 3 things clarified as NOT being built
- [ ] **Risks identified** - Every risk has a documented mitigation strategy
- [ ] **Complexity factors documented** - Key factors affecting implementation are clearly explained
- [ ] **Implementation is actionable** - Each step identifies specific files and includes code patterns
- [ ] **One feature per plan** - Scope is focused, not trying to build multiple features
- [ ] **No placeholders** - No "TBD", "[example]", or incomplete sections
- [ ] **Acceptance criteria are testable** - Each criterion can be verified without ambiguity
- [ ] **Dependencies are listed** - All external requirements, libraries, and approvals documented

**Decision:** Are all best practices met?

- **YES** → Plan is complete, validated, and ready for development
- **NO** → Return to appropriate phase and refine before proceeding

### ✅ PHASE 4 COMPLETE

All best practices validated? Excellent! Your implementation plan meets quality standards and is ready to guide development.

---

## Reference Section: What Goes In Each Part

**Requirements** (capabilities the feature must provide) vs. **Acceptance Criteria** (testable conditions proving success)

- Requirements: Capability-focused ("Users can toggle dark mode")
- Acceptance Criteria: Test-focused ("[ ] Toggle button works and saves preference")

**Implementation** section: Include approach (strategy and tech choices), then step-by-step implementation steps. Each step should have: file path, what to do and why, and suggested code snippet based on reading the codebase patterns matching your feature.

---

## Examples

See [references/examples.md](./references/examples.md) for detailed examples and tips.

**Decision Point:** Do you need to see examples before writing your plan?

- **YES** → Review the examples file to understand structure and patterns.
- **NO** → Skip to Best Practices or LLM Output Format sections.

---

## Best Practices

**Do**: Be specific, keep it focused (one feature per plan), define non-goals explicitly, identify risks with mitigations, document implementation complexity factors.

**Don't**: Use vague language, skip non-goals or risks, leave placeholders, over-engineer the plan (aim for 1-2 pages).

---

## LLM Output Format

When generating an implementation plan markdown file, use this exact structure:

```markdown
# [Feature Title]

## Overview
[What the feature does and why it matters - 1-2 sentences]

## Requirements
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]
- [Specific requirement 4]
- [Specific requirement 5]

## Non-Goals
- [What will NOT be built - justification]
- [What's deferred to future - why]
- [What's explicitly out of scope - rationale]

## Acceptance Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]
- [ ] [Testable criterion 4]
- [ ] [Testable criterion 5]

## Implementation Complexity
**Factors:** [Key factors affecting complexity - dependencies, integration points, testing scope, known challenges]

## Implementation

### Approach
[High-level strategy and technology choices]

### Files to Create/Modify
- `path/to/file1.ts` (description of change)
- `path/to/file2.tsx` (description of change)

## Risks
- Risk: [Description]
  Mitigation: [How to address]
- Risk: [Description]
  Mitigation: [How to address]

## Dependencies
- [Dependency name and version if applicable]
- [External service or approval required]
- [Team or infrastructure dependency]

## References
[Links or related information]
```

See [references/examples.md](./references/examples.md) for complete examples showing good vs. poor patterns and detailed guidance on each section.

---

## Agent Behavior Guidelines

For guidance on operating modes, clarification questions, and when to ask for more information, see [references/agent-modes.md](./references/agent-modes.md).

---

## Preconditions

Before using this skill:
- ✅ Git repository exists (or local project directory)
- ✅ `plans/` directory will be created automatically if it doesn't exist
- ✅ You're working on a new feature (not a bug fix or chore)
- ✅ You have a clear understanding of what the feature should do
- ✅ You have initial thoughts on requirements and success criteria

---

## Quick Reference

**File naming:** `YYYY-MM-DD-feature-short-name.md` (e.g., `2026-01-09-dark-mode-toggle.md`) in `plans/` directory

**Template order:** Title → Overview → Requirements → Non-Goals → Acceptance Criteria → Implementation Complexity → Implementation (Approach + Step-by-Step Steps with Code) → Risks → Dependencies → References

**Key point:** Be specific, define non-goals explicitly, identify risks with mitigations, document implementation complexity factors. See [references/agent-modes.md](./references/agent-modes.md) for operating modes and clarification questions.
