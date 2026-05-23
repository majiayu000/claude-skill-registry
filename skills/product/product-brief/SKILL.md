---
name: product-brief
description: Extract product ideas through guided questions and generate PRD
---

## Purpose

Extract product ideas from your head through guided questioning, then generate a detailed Product Requirements Document (PRD). Designed for product people who have a vision but need help articulating it clearly.

## The Problem This Solves

You have an idea for a product or feature in your mind, but struggle to explain it comprehensively. This command acts as your product thought partner — asking the right questions to extract what you're envisioning, then structuring it into a PRD ready for a team to execute.

## Usage

```
/product-brief [initial idea]
```

**Examples:**
- `/product-brief Add a notification system to our app`
- `/product-brief Build a customer feedback portal`
- `/product-brief Create an onboarding flow for new users`
- `/product-brief` (prompts you for the idea)

---

## Process Flow

### Phase 1: Capture Initial Idea

**If no idea is provided:**
Ask: "What product or feature are you thinking about?"
- Wait for their description (1 sentence to several paragraphs)
- Capture it as the starting point

**If idea is provided:**
Start with whatever the user provides:
- Could be 1 sentence or 5 paragraphs
- Capture it as the starting point
- Don't judge, just absorb

Display:

```markdown
## Initial Idea

[User's description]

---

**Next:** I'll ask a few questions to understand this better.
```

---

### Phase 2: Clarifying Questions (Conversational)

**Important:** Ask questions conversationally, not as a survey. 2-3 questions at a time, then wait for answers before asking more.

**Question Strategy:**

**Round 1 (Critical Context):**
- What problem does this solve?
- Who is this for?
- What success looks like?

**Round 2 (Constraints & Scope):**
Based on Round 1 answers, ask about:
- Timeline expectations
- Technical constraints
- Existing systems to integrate with
- What's explicitly out of scope

**Round 3 (User Experience):**
- How do users discover this?
- What's the core user journey?
- What actions should be easy vs hard?

**Round 4 (Success & Validation):**
- How will we know this succeeded?
- What are we assuming that needs validation?
- What dependencies exist?

**Adaptive questioning:** If user mentions stakeholders, budget, or other context early, adjust questions accordingly. Don't ask what you already know.

After each round, acknowledge answers briefly and transition naturally:
> "Got it. That helps me understand [X]. A few more questions about [Y]..."

---

### Phase 3: Understanding Summary

Before moving forward, confirm you captured the vision correctly:

```markdown
## What I Heard

**The Problem:**
[Synthesized problem statement]

**Target Users:**
[Who this is for]

**Core Value:**
[The main benefit/outcome]

**Key Constraints:**
[Timeline, technical, scope boundaries]

**Assumptions to Validate:**
[Things we're assuming but should test]

---

**Does this capture your vision? Type "yes" to continue or correct anything above.**
```

If user corrects, update and re-confirm.

---

### Phase 4: Spec Doc

User triggers with: `spec doc` or `create spec`

Generate structured product spec:

```markdown
# Product Spec: [Feature/Product Name]

**Date:** YYYY-MM-DD
**Owner:** [User's name]
**Status:** Draft

---

## Executive Summary

[2-3 sentence pitch: what this is and why it matters]

---

## Problem Statement

### Current Situation
[What exists today]

### Pain Points
- [Specific pain 1]
- [Specific pain 2]
- [Specific pain 3]

### Impact of Inaction
[What happens if we don't build this]

---

## Target Audience

### Primary Users
[Who will use this most]

### Secondary Users
[Who else benefits]

### User Characteristics
- [Key trait 1]
- [Key trait 2]
- [Key trait 3]

---

## Solution Overview

[High-level description of what we're building]

---

## Key Features & Functionality

### Must Have (MVP)
1. **[Feature 1]**
   - Description
   - Why it's critical
   
2. **[Feature 2]**
   - Description
   - Why it's critical

### Should Have (Phase 2)
1. **[Feature 3]**
   - Description
   - Why it's valuable

### Nice to Have (Future)
1. **[Feature 4]**
   - Description
   - Why it's desirable

---

## Success Metrics

### Primary Metric
[The one number that matters most]

### Secondary Metrics
- [Metric 2]
- [Metric 3]

### Leading Indicators
[Early signals of success/failure]

---

## Assumptions & Risks

### Key Assumptions
1. [Assumption 1]
   - How to validate: [Test method]
   
2. [Assumption 2]
   - How to validate: [Test method]

### Risks
1. **[Risk 1]** — [Mitigation strategy]
2. **[Risk 2]** — [Mitigation strategy]

---

## Dependencies

### Technical
- [System/API/service dependency]

### Team
- [Who needs to be involved]

### External
- [Third-party dependencies]

---

## Out of Scope

Explicitly not included:
- [Thing 1]
- [Thing 2]
- [Thing 3]

---

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]
- [ ] [Question 3]

---

**Next Steps:**

- Type `prioritize` to rank features by effort/impact
- Type `design flows` to create detailed user flows
- Type `create prd` to generate final PRD
- Type `back` to revise anything above
```

---

### Phase 5: Prioritization (Optional)

User triggers with: `prioritize`

Create effort/impact matrix:

```markdown
## Feature Prioritization

| Feature | Impact | Effort | Priority | Rationale |
|---------|--------|--------|----------|-----------|
| [Feature 1] | High | Low | P0 | [Why] |
| [Feature 2] | High | Medium | P0 | [Why] |
| [Feature 3] | Medium | Low | P1 | [Why] |
| [Feature 4] | Low | High | P2 | [Why] |

### Recommended MVP Scope

Based on high impact + reasonable effort:
1. [Feature 1]
2. [Feature 2]
3. [Feature 3]

**Estimated Effort:** [X weeks/sprints]

---

**Next:**
- Type `design flows` to create user flows
- Type `create prd` to generate final PRD
- Type `back` to revise spec
```

---

### Phase 6: Design Flows (Optional)

User triggers with: `design flows`

Create detailed user flows and screen specs:

```markdown
## User Flows & Screen Specifications

### Flow 1: [Primary User Journey]

**Entry Point:** [How user arrives]

**Steps:**

#### Step 1: [Screen Name]

**Layout:**
- [Header elements]
- [Main content area]
- [Actions/buttons]

**User Actions:**
- Click [X] → [Outcome]
- Enter [Y] → [Validation rules]
- Cancel → [State change]

**Navigation:**
- Success → [Next screen]
- Error → [Error state]
- Back → [Previous screen]

**Validation Rules:**
- [Field 1]: [Rules]
- [Field 2]: [Rules]

**States:**
- Default: [Description]
- Loading: [What user sees]
- Error: [Error message]
- Success: [Confirmation]

---

#### Step 2: [Next Screen]

[Same structure as Step 1]

---

### Flow 2: [Secondary Journey]

[Same structure as Flow 1]

---

**Next:**
- Type `create prd` to generate final PRD
- Type `back` to revise flows
```

---

### Phase 7: Final PRD

User triggers with: `create prd` or `generate prd`

Generate comprehensive PRD combining all previous phases:

```markdown
# Product Requirements Document
## [Product/Feature Name]

**Author:** [User name]
**Date:** YYYY-MM-DD
**Status:** Draft
**Last Updated:** YYYY-MM-DD

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | YYYY-MM-DD | [Name] | Initial draft |

---

## Executive Summary

[2-3 paragraphs covering: what, why, who, success]

---

## Background & Context

### Current State
[What exists today]

### Problem Statement
[The problem we're solving]

### Opportunity
[Why now, why us]

---

## Goals & Success Metrics

### Primary Objective
[The main goal]

### Success Metrics

**Primary:**
- [Metric 1]: [Target]

**Secondary:**
- [Metric 2]: [Target]
- [Metric 3]: [Target]

**Leading Indicators:**
- [Early signal 1]
- [Early signal 2]

---

## Target Users

### Primary Audience
[Detailed description]

### Use Cases
1. **[Use Case 1]**
   - As a [user type]
   - I want to [action]
   - So that [benefit]

2. **[Use Case 2]**
   - As a [user type]
   - I want to [action]
   - So that [benefit]

---

## Solution Overview

[Comprehensive description of what we're building]

---

## Functional Requirements

### Must Have (P0)

#### Requirement 1: [Name]
- **Description:** [What it does]
- **Acceptance Criteria:**
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]
  - [ ] [Criterion 3]
- **User Story:** As a [X], I want [Y], so that [Z]

#### Requirement 2: [Name]
[Same structure]

### Should Have (P1)

[Same structure as Must Have]

### Nice to Have (P2)

[Same structure as Must Have]

---

## User Experience

### User Flows
[Reference to flows from Phase 6, or create if skipped]

### Key Screens
[High-level screen descriptions]

### Interaction Patterns
[How users interact with the feature]

---

## Technical Requirements

### Performance
- [Requirement 1]
- [Requirement 2]

### Security
- [Requirement 1]
- [Requirement 2]

### Integration Points
- [System 1]: [What needs to connect]
- [System 2]: [What needs to connect]

### Data Requirements
- [What data is collected]
- [Where it's stored]
- [How it's used]

---

## Design Requirements

### Visual Design
- [Style guide compliance]
- [Responsive requirements]
- [Accessibility standards]

### Content Requirements
- [Copy needs]
- [Translation needs]
- [Asset requirements]

---

## Dependencies & Constraints

### Dependencies
- **Technical:** [List]
- **Team:** [Who needs to be involved]
- **External:** [Third parties]

### Constraints
- **Timeline:** [Dates/milestones]
- **Budget:** [If applicable]
- **Technical:** [Platform limitations]

---

## Assumptions & Risks

### Assumptions
1. [Assumption 1]
   - **Validation method:** [How to test]
   - **Impact if wrong:** [Consequence]

2. [Assumption 2]
   - **Validation method:** [How to test]
   - **Impact if wrong:** [Consequence]

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Strategy] |

---

## Out of Scope

Explicitly not included in this version:
- [Item 1] — [Why/when it might be included]
- [Item 2] — [Why/when it might be included]
- [Item 3] — [Why/when it might be included]

---

## Open Questions

- [ ] [Question 1] — Owner: [Name], Due: [Date]
- [ ] [Question 2] — Owner: [Name], Due: [Date]
- [ ] [Question 3] — Owner: [Name], Due: [Date]

---

## Timeline & Milestones

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| PRD Complete | [Date] | In Progress |
| Design Complete | [Date] | Not Started |
| Dev Complete | [Date] | Not Started |
| QA Complete | [Date] | Not Started |
| Launch | [Date] | Not Started |

---

## Stakeholders

| Name | Role | Involvement |
|------|------|-------------|
| [Name] | [Role] | [What they do] |
| [Name] | [Role] | [What they do] |

---

## Appendix

### Research
[Link to user research, competitive analysis, etc.]

### Design Mockups
[Links to designs when available]

### Technical Specs
[Links to technical documentation]

---

**Document Status:** Ready for Review

**Next Actions:**
- [ ] Review with stakeholders
- [ ] Refine based on feedback
- [ ] Get approval to proceed
- [ ] Hand off to design/engineering

---

*This PRD was generated using the /product-brief command. Update as needed.*
```

---

### Phase 8: Save & Integration

After generating the PRD:

1. **Save the document:**
   - Create folder: `04-Projects/[Product Name]/`
   - Save as: `04-Projects/[Product Name]/PRD.md`

2. **Create person pages** (if stakeholders mentioned):
   - For each stakeholder mentioned, check if person page exists
   - Create/update pages in `People/Internal/` or `People/External/`
   - Add note in their page referencing this project

3. **Link to 03-Tasks/Tasks.md:**
   - If user mentioned any immediate actions, suggest creating tasks
   - Link tasks to the project

4. **Confirm completion:**

```markdown
## ✅ PRD Created

**Saved to:** `04-Projects/[Product Name]/PRD.md`

**Next Steps:**
1. Review and refine the PRD
2. Share with stakeholders for feedback
3. Use `/project-health` to track progress
4. Create tasks in 03-Tasks/Tasks.md when ready to execute

**Want to:**
- Revise any section → Just tell me what to change
- Create tasks from this PRD → Say "create tasks"
- Share with stakeholders → I can draft an email
```

---

## Navigation Commands

At any phase, users can:

- `back` or `previous` — Return to previous phase
- `skip to prd` — Jump directly to final PRD
- `revise [section]` — Edit specific section
- `start over` — Begin from scratch
- `save` — Save current progress

---

## Conversational Style

- **Be a thought partner, not an interrogator**
- Ask follow-up questions when answers reveal gaps
- Challenge assumptions constructively
- Suggest alternatives when you spot potential issues
- Keep momentum — don't let the process feel like homework

**Good:**
> "Interesting. If this is for enterprise customers, how do we handle single sign-on? Or is that something we're punting to Phase 2?"

**Bad:**
> "Question 7: Please describe your authentication strategy."

---

## Tips for Effectiveness

### For the User
- Start with whatever you have — even 1 sentence is enough
- Don't worry about being comprehensive upfront
- The questions will extract what's in your head
- You can always revise and refine

### For Dex
- Listen for what's NOT being said
- If scope sounds too big, flag it early
- Connect this feature to their strategic pillars if relevant
- Update person pages for stakeholders mentioned
- Link to existing projects if this builds on something

---

## Example Session

**User:** `/product-brief Add notifications to our app`

**Dex:**

```markdown
## Initial Idea

Add notifications to our app

---

Great, let's flesh this out. A few questions to start:

1. What type of notifications are we talking about — push notifications, in-app alerts, email, or all three?
2. What specific events should trigger notifications?
3. Who are these notifications for — all users, or specific roles?
```

**User:** "Push notifications for now. We want to notify sales reps when a lead takes an action in the product."

**Dex:**

```markdown
Got it — push notifications for sales reps when leads are active. That helps narrow it.

A few more questions:

1. What actions count as notification-worthy? (e.g., login, feature usage, upgrade intent)
2. Should there be any filtering or preferences? Like "only notify me about my accounts"?
3. What's the business outcome we're driving here — faster response time, more engagement, closing deals faster?
```

[Conversation continues through phases until PRD is complete]

---

## Integration with Dex System

- **Pillars:** Link PRD to relevant strategic pillar
- **Quarter Goals:** If this supports a quarterly goal, note it
- **Week Priorities:** Suggest adding "finalize PRD" to this week if urgent
- **People pages:** Auto-update stakeholders mentioned in the PRD
- **Tasks:** Offer to create tasks from the PRD's next steps

---

## When to Use This Command

**Use `/product-brief` when:**
- You have a product idea but struggle to articulate it
- You need to write a PRD and want help structuring it
- You're pitching an idea and need to flesh it out
- You want to validate your thinking with good questions

**Don't use it for:**
- Simple feature requests (just describe them normally)
- Already-written PRDs that need editing
- Technical implementation details (that's engineering's job)

---

## Refinement After Creation

The PRD isn't set in stone. After creation:

- Say "refine the success metrics section" to iterate
- Say "add a section on localization" to expand
- Say "this scope is too big, help me cut it down" to trim

Dex will update the PRD file directly and maintain version history.

---

## Output Quality Checks

Before finalizing the PRD, verify:

- [ ] Clear problem statement
- [ ] Specific target audience
- [ ] Measurable success metrics
- [ ] Prioritized feature list (MVP vs later)
- [ ] Explicit out-of-scope items
- [ ] Key assumptions identified
- [ ] Dependencies called out
- [ ] Open questions captured

If any are missing, prompt user to fill gaps before finalizing.
