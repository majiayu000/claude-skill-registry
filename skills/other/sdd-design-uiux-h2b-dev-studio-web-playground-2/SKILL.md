---
name: sdd-design-uiux
description: |
  Design layout, responsive behavior, interactions, and accessibility.
  Use when: sdd-design assigns UI/UX Design section.
  Triggers: "design layout", "responsive design", "accessibility", "interaction design"
---

# SDD Design UI/UX

Write the UI/UX Design section of a design document.

## Scope

| Responsible For | Not Responsible For |
|-----------------|---------------------|
| Layout structure | Component hierarchy (→ frontend) |
| Responsive breakpoints | State management (→ frontend) |
| Interaction patterns | Data flow (→ frontend) |
| Accessibility (a11y) | Security validation (→ security) |
| Visual hierarchy | Bundle size (→ perf) |
| Loading states design | Loading implementation (→ frontend) |

## Cross-Cutting Roles

> **Note:** Cross-cutting concerns are an extension to `docs/sdd-guidelines.md` for specialist coordination. See sdd-design for full mapping.

UI/UX is:
- **Primary owner:** Accessibility, Loading states
- **Reviewer for:** Error handling (owned by frontend)

## Instructions

### Step 1: Read Context

1. Design skeleton (from sdd-design)
2. All REQs in your section's `@derives`
3. Foundation anchors (especially `SCOPE-*`, `CONSTRAINT-*`, audience)

### Step 2: Analyze Requirements

For each assigned REQ, extract UI/UX implications:

| REQ | User Goal | UX Elements Needed |
|-----|-----------|-------------------|
| | | |

**Tip:** Focus on user goals and experience, not implementation.

### Step 3: Design Layout Structure

Define spatial organization:

```
┌─────────────────────────────────┐
│           {Region}              │
├─────────────┬───────────────────┤
│  {Region}   │    {Region}       │
│             │                   │
└─────────────┴───────────────────┘
```

**Principles:**
- Content hierarchy reflects user priorities
- Related elements grouped
- Primary actions prominent

Document layout decisions with `@derives` linking to REQ.

### Step 4: Define Responsive Strategy

Based on REQ viewport requirements:

| Breakpoint | Width | Layout Changes | Rationale |
|------------|-------|----------------|-----------|
| Desktop | ≥{X}px | | REQ says "..." |
| Tablet | {X}-{Y}px | | REQ says "..." |
| Mobile | <{X}px | | REQ says "..." |

**Decision points:**
- Adaptive (different layouts) vs Responsive (fluid)?
- What collapses/hides at each breakpoint?
- Touch targets for mobile?

### Step 5: Design Interaction Patterns

For each user action in REQs:

| Action | Trigger | Feedback | Duration | @derives |
|--------|---------|----------|----------|----------|
| | | | | REQ-XXX |

**Feedback types:**
- Immediate: button states, hover
- Progress: loading, spinners
- Completion: success/error states

### Step 6: Design Accessibility

Map REQ features to a11y requirements:

| Feature | Keyboard | Screen Reader | Visual |
|---------|----------|---------------|--------|
| {from REQ} | Tab order, shortcuts | ARIA labels, announcements | Focus, contrast |

**WCAG checklist:**
- [ ] All interactive elements keyboard accessible
- [ ] Focus visible and logical
- [ ] Color not sole indicator
- [ ] Text contrast ≥4.5:1

### Step 7: Define Visual Hierarchy

Prioritize content per REQs:

1. **Primary:** {what REQ emphasizes most}
2. **Secondary:** {supporting content}
3. **Tertiary:** {optional/advanced}

**If REQ doesn't specify priority:**
- User's primary task → Primary
- Supporting info → Secondary
- Edge cases/advanced features → Tertiary

Document with `@derives` linking to REQ.

### Step 8: Design Loading States

For async operations in REQs:

| Operation | Skeleton/Spinner | Placement | @derives |
|-----------|------------------|-----------|----------|
| | | | REQ-XXX |

### Step 9: Write Section

```markdown
## UI/UX Design

@derives: {REQ-IDs}

### Layout Structure
### Responsive Breakpoints
### Interaction Patterns
### Accessibility
### Visual Hierarchy
### Loading States

**Status:** draft
```

### Step 10: Add Decisions

For non-obvious choices:

```markdown
| ID | Decision | Rationale | Owner |
|----|----------|-----------|-------|
| DEC-00x | {what} | {why — connect to REQ} | uiux |
```

### Step 11: Handoff

Per `docs/sdd-guidelines.md` §4.3 and §10.6.

#### 1. Update Section Status

```markdown
**Status:** verified
```

#### 2. Update State File

```yaml
# .sdd/state.yaml
documents:
  design:
    sections:
      uiux: verified
```

#### 3. Create Handoff Record

```yaml
# .sdd/handoffs/{timestamp}-uiux.yaml
from: sdd-design-uiux
to: sdd-design
timestamp: {ISO-8601}

completed:
  - design.uiux: verified

in_progress: []

blocked: []

gaps: []

next_steps:
  - sdd-design-frontend: Review accessibility — verify components support a11y props
  - sdd-design-perf: Review loading states for performance impact
```

#### 4. Cross-Cutting Status

| Concern | Primary | Reviewer | Status |
|---------|---------|----------|--------|
| Accessibility | uiux | frontend | `ready-for-review` |
| Loading states | uiux | perf | `ready-for-review` |

## @derives Judgment

**A layout/interaction `@derives` from a REQ when:**

| Criterion | Example |
|-----------|---------|
| Directly addresses REQ's UX need | Responsive layout → REQ's "works on mobile" |
| Enables REQ's user action | Interaction pattern → REQ's "user can toggle" |
| Satisfies REQ's constraint | Breakpoints → REQ's viewport requirements |

**NOT @derives:**
- Generic UX best practices not tied to REQ
- Aesthetic choices without REQ basis

## Verification

- [ ] All assigned REQs have @derives coverage
- [ ] Layout supports all REQ features
- [ ] Breakpoints match REQ viewport requirements
- [ ] Interactions defined for all user actions in REQs
- [ ] Accessibility covers all interactive elements
- [ ] Loading states for all async operations
- [ ] Decisions logged with rationale
- [ ] Cross-cutting items flagged for reviewers

## References

| File | Content |
|------|---------|
| [reference/responsive-strategy.md](reference/responsive-strategy.md) | REQ-based responsive decisions |
| [reference/a11y-checklist.md](reference/a11y-checklist.md) | Accessibility verification for SDD |

## Examples

| File | Content |
|------|---------|
| [examples/react-sample.md](examples/react-sample.md) | Complete example for react-sample package |
