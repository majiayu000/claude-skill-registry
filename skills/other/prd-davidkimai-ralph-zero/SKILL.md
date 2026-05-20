---
name: prd
description: "Generate structured Product Requirements Documents through guided questions. Creates well-formed PRDs with user stories, acceptance criteria, and technical approach. Use when planning new features, creating specifications, or when user asks to create/generate a PRD."
license: MIT
metadata:
  parent_skill: ralph-zero
  version: "0.1.0"
---

# PRD Generation Skill

Generate comprehensive, structured Product Requirements Documents (PRDs) through an interactive question-and-answer workflow optimized for autonomous development.

## When to Use

Use this skill when:
- User asks to "create a PRD" or "generate requirements"
- Planning a new feature before implementation
- Need to document requirements for Ralph Zero
- Want to break down complex features into implementable stories

## Workflow

This skill follows a structured 5-step process to create production-ready PRDs.

### Step 1: Get Feature Description

Ask the user for a high-level description:

```
What feature would you like to build? Please provide a brief description.
```

### Step 2: Ask Clarifying Questions

Ask these essential questions with **letter options** for quick responses:

#### 1. Problem & Goals
```
1. What problem does this feature solve?
   A. User pain point / friction
   B. Business requirement
   C. Technical debt / refactoring
   D. Competitive feature parity
   E. Other: [specify]
```

#### 2. Target Users
```
2. Who will use this feature?
   A. End users only
   B. Admin users only
   C. All users
   D. Developers / internal team
   E. External integrations
```

#### 3. Scope
```
3. What is the desired scope?
   A. Minimal viable version (fastest path)
   B. Full-featured implementation
   C. Backend/API only (no UI)
   D. Frontend/UI only (mock backend)
```

#### 4. Technical Constraints
```
4. Any technical constraints or requirements?
   A. Must integrate with existing system X
   B. Performance requirements (specify)
   C. Security/compliance requirements
   D. No special constraints
```

#### 5. Success Measurement
```
5. How will you measure success?
   A. User metrics (engagement, retention)
   B. Business metrics (conversion, revenue)
   C. Technical metrics (performance, quality)
   D. Simply: feature works as specified
```

**Allow user to respond:** `1A, 2C, 3A, 4D, 5D` for efficient iteration.

### Step 3: Generate PRD

Based on answers, generate a PRD using this structure:

```markdown
# [Feature Name]

## Executive Summary
[2-3 sentence overview]

## Problem Statement
[What problem are we solving and why]

## Goals
- Goal 1: [Specific, measurable]
- Goal 2: [Specific, measurable]
- Goal 3: [Specific, measurable]

## User Stories

For each story, use this format:

### US-001: [Story Title]
**Description:** As a [user type], I want to [action], so that [benefit].

**Acceptance Criteria:**
- [ ] Specific, verifiable criterion 1
- [ ] Specific, verifiable criterion 2
- [ ] Typecheck passes
- [ ] [UI stories only] Verify in browser using dev-browser skill

**Priority:** 1

**Notes:** [Any implementation hints or context]

## Functional Requirements

- FR-1: The system must [specific requirement]
- FR-2: When [condition], the system must [behavior]
- FR-3: [Specific, testable requirement]

## Non-Goals (Out of Scope)

- What we're explicitly NOT doing
- Features deferred to future iterations
- Edge cases intentionally not handled

## Technical Approach

### Architecture
[High-level technical approach]

### Data Model
[Key schema changes or data structures]

### APIs/Inte grations
[External systems, endpoints needed]

## Success Metrics

- Metric 1: [target value]
- Metric 2: [target value]

## Timeline & Milestones

- Phase 1: [description] - [timeframe]
- Phase 2: [description] - [timeframe]

## Dependencies

- Dependency 1: [what and why]
- Dependency 2: [what and why]

## Open Questions

- Question 1
- Question 2
```

### Step 4: Save PRD

Save to `tasks/prd-[feature-name-kebab-case].md`

Examples:
- "User Authentication" → `tasks/prd-user-authentication.md`
- "Task Priority System" → `tasks/prd-task-priority.md`

### Step 5: Next Steps

After saving, inform the user:

```
✅ PRD saved to tasks/prd-[feature-name].md

Next steps:
1. Review and refine the PRD as needed
2. Convert to prd.json: Load ralph-convert skill and convert tasks/prd-[feature-name].md to prd.json
3. Run Ralph Zero: ralph-zero run --max-iterations 50
```

## Best Practices

### Keep Stories Atomic

Each user story should be:
- **Specific**: Clear about what needs to be done
- **Testable**: Can be verified when complete
- **Independent**: Minimal dependencies on other stories
- **Small**: Completable in one iteration (30min - 2hrs)

### Write Verifiable Acceptance Criteria

✅ **Good criteria (specific, testable):**
- "Add status column to tasks table ('pending' | 'in_progress' | 'done')"
- "Badge shows green for done, blue for in_progress, gray for pending"
- "Clicking delete shows confirmation dialog with Cancel/Confirm buttons"

❌ **Bad criteria (vague, untestable):**
- "Status works correctly"
- "Good UX"
- "User can easily do X"
- "Handles all edge cases"

### Order Stories by Dependency

Stories should execute in dependency order:

**Correct order:**
1. Schema/database changes
2. Backend logic/server actions
3. UI components
4. Dashboard/aggregation views

**Wrong order:**
- UI component at priority 1 that needs schema from priority 3

### Always Include Quality Checks

Every story must have:
- `Typecheck passes` as final criterion
- `Tests pass` if testable logic
- `Verify in browser using dev-browser skill` if UI changes

## Example Interaction

**User:** "Create a PRD for adding task priority levels"

**Agent (you):**
```
I'll help you create a PRD for task priority levels. Let me ask some clarifying questions:

1. What problem does this feature solve?
   A. User pain point / friction
   B. Business requirement
   C. Technical debt / refactoring
   D. Competitive feature parity
   E. Other: [specify]

[User: 1A]

2. Who will use this feature?
   A. End users only
   B. Admin users only
   C. All users
   D. Developers / internal team
   E. External integrations

[User: 2C]

...

[After gathering all answers]

Great! Here's your PRD:

# Task Priority System

## Executive Summary
Add priority levels (high, medium, low) to tasks so users can focus on what matters most...

[Generate complete PRD]

✅ PRD saved to tasks/prd-task-priority.md

Next steps:
1. Review the PRD
2. Convert to prd.json using ralph-convert skill
3. Run Ralph Zero
```

## Customization

For project-specific templates, create:
```
skills/prd/references/CUSTOM_TEMPLATE.md
```

Then reference it:
```
Use the custom PRD template from references/CUSTOM_TEMPLATE.md
```

## Common Pitfalls

### Avoid Vague Requirements
❌ "Make the UI better"
✅ "Add visual feedback on hover (scale to 1.05, show shadow)"

### Avoid Mixing Concerns
❌ "Add authentication and dashboard"
✅ Split into: Auth schema, Auth UI, Dashboard

### Avoid Future-Proofing
❌ "Design for eventual multi-tenant support"
✅ "Implement single-tenant, document extension points"

## Related Skills

- **ralph-convert**: Convert this PRD to prd.json
- **ralph-zero**: Run autonomous development loop

## See Also

- [PRD Template](references/TEMPLATE.md)
- [PRD Best Practices](references/BEST_PRACTICES.md)
- [Story Sizing Guide](references/STORY_SIZING.md)
