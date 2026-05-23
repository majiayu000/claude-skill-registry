---
name: create-prd
description: Plan features interactively. Asks clarifying questions, then generates a detailed PRD document.
---

# Create PRD

Generate a Product Requirements Document through interactive planning.

## Process

### 1. Understand the Feature

Read the user's feature request. If unclear, ask for a brief description.

### 2. Ask Clarifying Questions

Ask 3-5 clarifying questions to understand scope and requirements.

Format with lettered options:
```
1. Who is the primary user?
   A) Logged-in users only
   B) All visitors
   C) Admin users

2. Should this persist across sessions?
   A) Yes, save to database
   B) No, session only
```

User can respond with combinations like "1A, 2B".

### 3. Generate PRD

After answers, create a detailed PRD with these sections:

```md
# PRD: [Feature Name]

## Introduction
Brief overview of the feature and why it's needed.

## Goals
- Primary goal
- Secondary goals

## User Stories
### [Story Title]
**Description:** As a [user], I want [action] so that [benefit].
**Acceptance Criteria:**
- [ ] Specific, verifiable criterion
- [ ] Another criterion
- [ ] Typecheck passes
- [ ] (UI changes) Verify in browser

## Functional Requirements
1. Requirement one
2. Requirement two

## Non-Goals
What this feature explicitly won't do.

## Design Considerations
UI/UX notes, mockup descriptions.

## Technical Considerations
Architecture notes, dependencies, potential challenges.

## Success Metrics
How to measure if this feature is successful.

## Open Questions
Any unresolved decisions.
```

### 4. Save PRD

Save to `prds/[feature-name].md` (create `prds/` directory if needed).

```
PRD saved to prds/[feature-name].md

Next: Run /create-prd-json to convert to executable format.
```

## Guidelines

- Be explicit and unambiguous
- Write for junior developers and AI agents
- Avoid jargon
- Number requirements for easy reference
- Acceptance criteria must be verifiable, not vague
  - Good: "Button displays 'Save' text"
  - Bad: "Button looks good"
