---
name: generic-ux-designer
description: Professional UX expertise for any project type. Covers user research, design thinking, interaction patterns, accessibility, and design critique. Use when designing new features, improving UX, conducting design reviews, or evaluating user flows. For visual UI work, combine with ui-research skill.
---

# Generic UX Designer

Professional UX expertise adapting to any project's constraints.

## Combine with Research for Visual Work

For UI/visual design decisions, also use:

```
Skill(ui-research)  # Research inspiration first
```

**References:**

- [UX Principles](../_shared/UX_PRINCIPLES.md) - UX methodology
- [UI Inspiration Sources](../_shared/UI_INSPIRATION_SOURCES.md) - Visual research

## When to Use This Skill

**Use for:**

- Designing new features or flows
- Improving existing user experience
- Conducting design reviews/critiques
- Evaluating user flows and interactions
- Making accessibility decisions
- Choosing between design alternatives

**Don't use when:**

- Visual styling/tokens → use `generic-design-system`
- Code architecture → use `generic-feature-developer`
- Code quality review → use `generic-code-reviewer`

## Design Thinking Process

1. **Empathize** - Understand user needs, pain points, journeys
2. **Define** - Problem statements, personas, success metrics
3. **Ideate** - Brainstorm solutions, explore alternatives
4. **Prototype** - Low-fidelity first, test assumptions
5. **Test** - Usability testing, iterate on data

## Research Decision Guide

### When to Research vs Ship

| Situation            | Action                               |
| -------------------- | ------------------------------------ |
| New product/feature  | Full research (interviews + testing) |
| Incremental change   | Quick critique (heuristic review)    |
| Bug fix              | No research needed                   |
| A/B decision         | Analytics + small test               |
| Controversial design | Stakeholder alignment first          |

### Method Selection

- Need user motivation? → Interviews
- Need usability feedback? → Testing
- Need quick quality check? → Heuristic evaluation
- Need quantitative data? → Surveys/Analytics
- Have no users yet? → Competitor analysis + proto-personas

### Research Scope by Confidence

| Confidence Level           | Action         |
| -------------------------- | -------------- |
| High (established pattern) | Skip research  |
| Medium (some uncertainty)  | Quick critique |
| Low (new territory)        | Full research  |

**Reference:** See UX_PRINCIPLES.md for detailed method frameworks

## User Psychology Applied

### Cognitive Load

- Reduce choices (Hick's Law)
- Chunk information (Miller's Law)
- Progressive disclosure
- Minimize memory load

### Visual Hierarchy

- Size indicates importance
- Contrast draws attention
- Whitespace groups elements
- F-pattern/Z-pattern reading

## Interaction Patterns

### Navigation

| Pattern    | Use Case                    |
| ---------- | --------------------------- |
| Top nav    | Simple sites, < 7 items     |
| Side nav   | Complex apps, many sections |
| Bottom nav | Mobile apps, < 5 items      |
| Tabs       | Related content sections    |

### Forms

- Single column layout
- Inline validation
- Smart defaults
- Progress indicators

### Feedback

| Pattern  | Use Case            |
| -------- | ------------------- |
| Toast    | Non-blocking info   |
| Modal    | Blocking/important  |
| Inline   | Contextual feedback |
| Skeleton | Loading states      |

## Mobile Considerations

- Touch targets: 44x44px minimum
- 8px spacing between targets
- Thumb-friendly placement
- Bottom sheets for actions

## Accessibility (UX Perspective)

| Aspect    | Approach                         |
| --------- | -------------------------------- |
| Vision    | High contrast, scalable text     |
| Motor     | Large targets, keyboard nav      |
| Cognitive | Simple language, clear structure |
| Hearing   | Captions, visual indicators      |

## Heuristic Evaluation in Practice

### Quick Scan (5 minutes)

| Heuristic        | Quick Check                          |
| ---------------- | ------------------------------------ |
| Visibility       | Is current state obvious?            |
| Feedback         | Does every action have response?     |
| Consistency      | Do similar things look/work similar? |
| Error Prevention | Can user easily make mistakes?       |
| Recovery         | Can user undo/fix errors?            |

### Common Violations to Flag

- Hidden system state (loading with no indicator)
- Silent failures (action with no feedback)
- Inconsistent patterns (different buttons for same action)
- Destructive without confirm (delete with no undo)
- Jargon in user-facing text

### Presenting Findings

```
Issue: [What's wrong]
Heuristic: [Which violated]
Impact: [User consequence]
Suggestion: [How to fix]
Priority: P0/P1/P2
```

## Design Critique Framework

| Aspect        | Questions                     |
| ------------- | ----------------------------- |
| Usability     | Can users complete tasks?     |
| Clarity       | Is purpose immediately clear? |
| Consistency   | Follows established patterns? |
| Hierarchy     | Most important stands out?    |
| Feedback      | Users know system state?      |
| Accessibility | Works for everyone?           |

## UX Patterns

### Empty States

1. Explain what goes here
2. Guide to first action
3. Show example content

### Loading States

1. Skeleton screens > spinners
2. Progress for long operations
3. Optimistic UI when safe

### Error States

1. Explain what happened
2. Suggest how to fix
3. Don't blame user

## UX Output Checklist

Before presenting UX recommendation:

- [ ] User problem clearly defined
- [ ] Solution addresses root cause (not symptom)
- [ ] Accessibility considered
- [ ] Edge cases identified
- [ ] Implementation complexity noted
- [ ] Success metrics defined

## Design Review Checklist

- [ ] Primary task achievable
- [ ] Clear visual hierarchy
- [ ] Keyboard navigable
- [ ] Touch targets sized
- [ ] Copy clear and helpful

## See Also

- [UX Principles](./../_shared/UX_PRINCIPLES.md) - Research methods, heuristics, psychology
- [Design Patterns](./../_shared/DESIGN_PATTERNS.md) - Visual patterns and components
- `generic-design-system` - For tokens, styling, visual consistency
- `generic-feature-developer` - For implementation architecture
- Project `CLAUDE.md` - Project-specific constraints

**READ UX_PRINCIPLES.md for:**

- Full research method frameworks → methods section
- Complete Nielsen heuristics → evaluation section
- Quick critique workflow → critique section
