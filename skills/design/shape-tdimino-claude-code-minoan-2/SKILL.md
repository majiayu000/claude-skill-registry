---
name: shape
description: "Plan the UX and UI for a feature before writing code. Runs a structured discovery interview, then produces a design brief that guides implementation. This skill should be used during the planning phase to establish design direction, constraints, and strategy before any code is written. Use when the user says 'plan the design,' 'design brief,' 'shape the UX,' or 'before we build.'"
argument-hint: "[feature to shape]"
---

Shape the UX and UI for a feature before any code is written. This skill produces a **design brief** — a structured artifact that guides implementation through discovery, not guesswork.

**Scope**: Design planning only. This skill produces design briefs, not code.

## Preparation

Read `~/.claude/skills/minoan-frontend-design/SKILL.md` for aesthetic principles and anti-pattern guidance. These inform the design direction but should not constrain the discovery interview.

Check for existing design context: `.design-context.md` in the project root, or a `## Design Context` section in CLAUDE.md. If either exists, use it as a starting point — don't re-ask questions it already answers.

## Phase 1: Discovery Interview

Do NOT make any design decisions during this phase. Understand the feature deeply enough to make excellent decisions later.

Ask these questions conversationally — adapt based on answers, don't dump them all at once:

### Purpose & Context
- What is this feature for? What problem does it solve?
- Who specifically will use it? (Role, context, frequency — not just "users")
- What does success look like? How will you know this feature is working?
- What's the user's state of mind when they reach this? (Rushed? Exploring? Anxious?)

### Content & Data
- What content or data does this feature display or collect?
- What are the realistic ranges? (Minimum, typical, maximum — e.g., 0 items, 5 items, 500 items)
- What are the edge cases? (Empty state, error state, first-time use, power user)

### Design Goals
- What's the single most important thing a user should do or understand here?
- What should this feel like? (Fast/efficient? Calm/trustworthy? Fun/playful? Premium/refined?)
- Are there existing patterns in the product this should be consistent with?
- Any reference sites or apps that capture what you're going for? What specifically about them?

### Constraints
- Technical constraints? (Framework, performance budget, browser support)
- Content constraints? (Localization, dynamic text length, user-generated content)
- Mobile/responsive requirements?
- Accessibility requirements beyond WCAG AA?

### Anti-Goals
- What should this NOT be? What would be a wrong direction?
- What's the biggest risk of getting this wrong?

## Phase 2: Design Brief

After the interview, synthesize everything into a structured design brief. Present it to the user for confirmation before considering this skill complete.

**1. Feature Summary** (2-3 sentences)
What this is, who it's for, what it needs to accomplish.

**2. Primary User Action**
The single most important thing a user should do or understand here.

**3. Design Direction**
How this should feel. What aesthetic approach fits. Reference the project's design context if available and explain how this feature should express it. Set DESIGN_VARIANCE, MOTION_INTENSITY, and VISUAL_DENSITY (1-10 each) based on discovery answers. Consult `~/.claude/skills/minoan-frontend-design/references/design-dials.md`.

**4. Layout Strategy**
High-level spatial approach: what gets emphasis, what's secondary, how information flows. Describe the visual hierarchy and rhythm, not specific CSS.

**5. Key States**
List every state the feature needs: default, empty, loading, error, success, edge cases. For each, note what the user needs to see and feel.

**6. Interaction Model**
How users interact with this feature. What happens on click, hover, scroll? What feedback do they get? What's the flow from entry to completion?

**7. Content Requirements**
What copy, labels, empty state messages, error messages, and microcopy are needed. Note any dynamic content and its realistic ranges.

**8. Open Questions**
Anything unresolved that the implementer should resolve during build.

**9. Implementation Skills**
Consult `references/design-media-catalog.md`. Based on discovery answers, recommend which skills the implementer should invoke beyond `/minoan-frontend-design`. Only list skills that match actual needs discovered — don't enumerate the full catalog.

---

Get explicit confirmation of the brief before finishing. If the user disagrees with any part, revisit the relevant discovery questions.

Once confirmed, write the brief to `.design-context.md` in the project root (or update the existing file). The user can then hand it to `/minoan-frontend-design` or use it to guide any other implementation approach.
