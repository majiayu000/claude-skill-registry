---
document_name: "user-flows.skill.md"
location: ".claude/skills/user-flows.skill.md"
codebook_id: "CB-SKILL-USERFLOW-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for user flow design"
skill_metadata:
  category: "design"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "UX fundamentals"
    - "User research awareness"
category: "skills"
status: "active"
tags:
  - "skill"
  - "design"
  - "ux"
  - "flow"
ai_parser_instructions: |
  This skill defines procedures for user flow design.
  Used by UX Designer agent.
---

# User Flows Skill

=== PURPOSE ===

Procedures for designing and documenting user flows.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(ux-designer) @ref(CB-AGENT-UXDESIGN-001) | Primary skill for flows |

=== PROCEDURE: Flow Types ===

**User Flow:** Single task, start to completion
```
Start → Action → Action → Success
```

**User Journey:** End-to-end experience across touchpoints
```
Awareness → Consideration → Purchase → Onboarding → Usage → Advocacy
```

**Task Flow:** Specific steps without decision points
```
Click button → Fill form → Submit → Confirmation
```

=== PROCEDURE: Flow Notation ===

**Symbols:**
```
┌─────────┐
│  Start  │     Entry point (rounded rectangle)
└─────────┘

┌─────────┐
│ Screen  │     Screen/page (rectangle)
└─────────┘

    ◇           Decision point (diamond)
   / \
  /   \

   ──→          Flow direction (arrow)

┌─────────┐
│   End   │     Exit point (rounded rectangle)
└─────────┘
```

**Example Flow:**
```
┌───────────┐
│  Landing  │
└─────┬─────┘
      │
      ▼
┌───────────┐
│   Login   │
└─────┬─────┘
      │
      ◇ Valid?
     / \
    /   \
   ▼     ▼
┌────┐ ┌─────┐
│Home│ │Error│
└────┘ └──┬──┘
          │
          └──→ (back to Login)
```

=== PROCEDURE: Flow Documentation ===

**Template:**
```markdown
# [Feature Name] User Flow

## Overview
**Goal:** What the user wants to accomplish
**Persona:** Primary user type
**Entry points:** How users arrive
**Success criteria:** What defines completion

## Prerequisites
- User is logged in
- Has required permissions
- etc.

## Flow Diagram
[ASCII or embedded diagram]

## Detailed Steps

### Step 1: [Screen/Action Name]
**URL/Screen:** /path/to/screen
**User sees:**
- Element 1
- Element 2

**User actions:**
- Primary: Click "Submit"
- Secondary: Click "Cancel"

**System response:**
- On success: Navigate to Step 2
- On error: Show validation message

### Step 2: [Screen/Action Name]
...

## Error Handling
| Error | Display | Recovery |
|-------|---------|----------|
| Network failure | Toast message | Retry button |
| Validation error | Inline message | Fix and resubmit |

## Edge Cases
- [ ] User loses connection mid-flow
- [ ] Session expires
- [ ] Required data is missing
- [ ] User navigates away

## Metrics
- Completion rate target: 80%
- Time to complete target: < 2 minutes
- Drop-off monitoring points: Step 2, Step 4
```

=== PROCEDURE: Flow Analysis ===

**Questions to Ask:**
1. What is the user's goal?
2. Where does the user come from?
3. What's the shortest path to success?
4. What can go wrong at each step?
5. How does the user recover from errors?
6. What if the user abandons midway?

**Red Flags:**
- More than 5-7 steps for simple tasks
- Redundant information requests
- Dead ends without recovery
- Forced linear paths without shortcuts
- No progress indication

=== PROCEDURE: Flow Optimization ===

**Reduce Steps:**
```
Before: Login → Verify email → Set password → Accept terms → Profile → Home
After:  Login (social) → Accept terms → Home (profile optional)
```

**Progressive Disclosure:**
```
Show only what's needed at each step
Collect optional info later
Offer "skip" where possible
```

**Smart Defaults:**
```
Pre-fill known information
Remember previous choices
Use sensible defaults
```

=== PROCEDURE: Wireframe Integration ===

**Flow-to-Wireframe Mapping:**
```markdown
## Screen Inventory

| Flow Step | Screen | Wireframe | Status |
|-----------|--------|-----------|--------|
| Step 1 | Landing | wireframes/landing.png | Done |
| Step 2 | Login | wireframes/login.png | Done |
| Step 3 | Dashboard | wireframes/dashboard.png | In progress |
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(usability-review) | Flow validation |
| @skill(accessibility) | A11y in flows |
