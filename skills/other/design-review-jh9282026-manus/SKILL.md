---
name: design-review
description: "Facilitate design critiques and reviews with stakeholders, team members, and users to gather feedback. Use for: design presentations, stakeholder reviews, team critiques, client feedback sessions, and collaborative design evaluation."
---

# Design Review

## Description

Design Review systematically evaluates designs against established criteria, user needs, and quality standards. This skill identifies strengths to maintain and weaknesses to address, driving the iterative improvement process.

## When to Use

- After completing a design phase
- Before handoff to development
- When iterating toward 9/10 quality
- During design critiques
- When validating design decisions

---

## Instructions for AI Agents

### Step 1: Establish Review Framework

**Review dimensions:**

```markdown
## Review Checklist

### 1. Visual Design (25%)
- [ ] Color harmony and contrast
- [ ] Typography hierarchy and readability
- [ ] Layout alignment and grid usage
- [ ] Visual hierarchy effectiveness
- [ ] Polish and attention to detail

### 2. User Experience (25%)
- [ ] Clarity of purpose on each screen
- [ ] Intuitive navigation
- [ ] Clear call-to-actions
- [ ] Logical user flows
- [ ] Error prevention and handling

### 3. Consistency (15%)
- [ ] Component reuse
- [ ] Pattern consistency
- [ ] Spacing consistency
- [ ] Interaction consistency

### 4. Responsiveness (15%)
- [ ] Mobile layout quality
- [ ] Breakpoint transitions
- [ ] Touch target sizes
- [ ] Content priority on small screens

### 5. Accessibility (10%)
- [ ] Color contrast compliance
- [ ] Focus states
- [ ] Touch targets
- [ ] Screen reader considerations

### 6. Brand & Polish (10%)
- [ ] Brand alignment
- [ ] Professional appearance
- [ ] Memorable elements
- [ ] Emotional resonance
```

### Step 2: Conduct Visual Inspection

**Systematic review process:**

```markdown
## Visual Inspection Checklist

### Overall Impression
1. Take 5 seconds to look at the design
2. Note first impression (positive/negative/neutral)
3. Identify what draws attention first
4. Assess if primary action is clear

### Element-by-Element Review

#### Typography
- [ ] Is body text readable (16px+)?
- [ ] Is heading hierarchy clear (3+ levels)?
- [ ] Is line length comfortable (60-75 chars)?
- [ ] Is line height appropriate (1.5-1.7 for body)?
- [ ] Are fonts loading correctly?

#### Color
- [ ] Does palette feel cohesive?
- [ ] Is there sufficient contrast?
- [ ] Is color used meaningfully (not decoratively)?
- [ ] Are semantic colors correct (green=success)?
- [ ] Would it work for colorblind users?

#### Layout
- [ ] Is grid usage consistent?
- [ ] Is alignment precise?
- [ ] Is whitespace intentional?
- [ ] Is visual balance achieved?
- [ ] Does layout guide the eye?

#### Components
- [ ] Are all states designed?
- [ ] Are components consistent?
- [ ] Are interactive elements clear?
- [ ] Is feedback adequate?
```

### Step 3: UX Evaluation

**User-centered review:**

```markdown
## UX Evaluation

### Task Completion
For each key user task:
1. Can user identify where to start?
2. Is the path to completion clear?
3. Is progress communicated?
4. Is completion confirmed?

### Cognitive Load
- Is information chunked appropriately?
- Are users overloaded with options?
- Is important info prioritized?
- Can users focus on one task?

### Wayfinding
- Is current location clear?
- Can users navigate to any section?
- Are breadcrumbs/back paths available?
- Is search available if needed?

### Error Handling
- Are potential errors prevented?
- Are error messages helpful?
- Can users recover easily?
- Is data preserved on errors?
```

### Step 4: Document Findings

**Review report template:**

```markdown
## Design Review Report

**Project**: [Name]
**Date**: [Date]
**Reviewer**: [AI Agent/Name]
**Design Version**: [Version number]

---

### Summary

**Overall Score**: [X/10]
**Quality Level**: [Poor/Below Average/Average/Good/Excellent]
**Ready for**: [Next phase / Iteration / Development]

### Key Findings

#### Strengths (Keep These)
1. **[Strength 1]**: [Why it works well]
2. **[Strength 2]**: [Why it works well]
3. **[Strength 3]**: [Why it works well]

#### Areas for Improvement (Address These)
1. **[Issue 1]**: [Description]
   - Impact: [High/Medium/Low]
   - Fix: [Recommendation]
   
2. **[Issue 2]**: [Description]
   - Impact: [High/Medium/Low]
   - Fix: [Recommendation]

#### Critical Issues (Must Fix)
1. **[Critical Issue]**: [Description]
   - Why critical: [Reason]
   - Required fix: [Action]

---

### Detailed Scores

| Category | Score | Notes |
|----------|-------|-------|
| Visual Design | _/10 | |
| User Experience | _/10 | |
| Consistency | _/10 | |
| Responsiveness | _/10 | |
| Accessibility | _/10 | |
| Brand & Polish | _/10 | |

---

### Screen-by-Screen Notes

#### [Screen 1 Name]
- **What's working**: [Notes]
- **Issues**: [Notes]
- **Suggestions**: [Notes]

#### [Screen 2 Name]
- **What's working**: [Notes]
- **Issues**: [Notes]
- **Suggestions**: [Notes]

---

### Recommended Next Steps

1. [ ] [Priority action 1]
2. [ ] [Priority action 2]
3. [ ] [Priority action 3]

### Timeline Estimate
- Critical fixes: [X hours]
- Improvements: [X hours]
- Polish: [X hours]
```

---

## Example Input/Output

### Example Input

```markdown
**Design**: TaskFlow Dashboard v1
**Screens**: Dashboard, Project List, Task Detail
**Stage**: First draft visual design
```

### Example Output

```markdown
## Design Review Report: TaskFlow Dashboard v1

**Date**: Current
**Design Version**: 1.0 (First Draft)

---

### Summary

**Overall Score**: 6.5/10
**Quality Level**: Average to Good
**Ready for**: Iteration (1-2 more rounds recommended)

The design shows good foundational work with a clear structure and appropriate color palette. However, it needs work on visual hierarchy, consistency, and some UX improvements before reaching production quality.

---

### Key Findings

#### Strengths (Keep These) ✅

1. **Color palette is well-chosen**
   - Violet primary feels modern and premium
   - Good differentiation from competitors
   - Accessible contrast ratios

2. **Navigation structure is clear**
   - Sidebar organization makes sense
   - User can find main sections easily
   - Icons support labels well

3. **Card-based layout works well**
   - Information is chunked appropriately
   - Visual hierarchy within cards is good
   - Consistent card treatment throughout

---

#### Areas for Improvement (Address These) ⚠️

1. **Typography hierarchy needs work**
   - Issue: H2 and H3 look too similar
   - Impact: Medium - reduces scanability
   - Fix: Increase size difference (H2: 28px, H3: 22px) or add weight contrast

2. **Inconsistent spacing**
   - Issue: Card padding varies (16px, 20px, 24px)
   - Impact: Medium - looks unpolished
   - Fix: Standardize to 20px for all cards

3. **Stat cards lack visual hierarchy**
   - Issue: Number and label are similar weight
   - Impact: Low - data is readable but could be clearer
   - Fix: Make numbers bolder (700) and larger (32px)

4. **Project cards missing status indicator**
   - Issue: Can't quickly see project health
   - Impact: Medium - key information missing
   - Fix: Add colored dot or badge for status

5. **Search bar too subtle**
   - Issue: Low contrast, hard to notice
   - Impact: Low - discoverable but not prominent
   - Fix: Add subtle border or darker background

---

#### Critical Issues (Must Fix) 🚨

1. **No loading states designed**
   - Why critical: Users won't know if system is working
   - Fix: Design skeleton loaders for dashboard, task list
   - Estimate: 2 hours

2. **Mobile navigation not resolved**
   - Why critical: Tab bar items undefined, overflow not handled
   - Fix: Design complete mobile nav with all states
   - Estimate: 3 hours

---

### Detailed Scores

| Category | Score | Notes |
|----------|-------|-------|
| Visual Design | 7/10 | Good colors, needs hierarchy work |
| User Experience | 6/10 | Clear but missing states |
| Consistency | 5/10 | Spacing inconsistencies |
| Responsiveness | 5/10 | Mobile incomplete |
| Accessibility | 7/10 | Good contrast, needs focus states |
| Brand & Polish | 6/10 | Solid foundation, needs refinement |

**Weighted Total: 6.5/10**

---

### Screen-by-Screen Notes

#### Dashboard
**Working**: Layout structure, stat cards concept, color usage
**Issues**: 
- Stat cards need stronger number emphasis
- "Welcome" message feels generic
- No time context ("Today is Monday")
**Suggestions**:
- Add personalization to welcome (time-based greeting)
- Consider showing "quick actions" section

#### Project List
**Working**: Card layout, filtering concept
**Issues**:
- Cards look identical - hard to scan
- No visual indicator of project priority
- Grid spacing uneven
**Suggestions**:
- Add color-coded priority/status
- Consider list view as alternative
- Add project thumbnail/color stripe

#### Task Detail (Modal)
**Working**: Information organization
**Issues**:
- Close button too small
- No clear primary action
- Comments section undefined
**Suggestions**:
- Add "Mark Complete" as primary CTA
- Design empty state for no comments
- Add activity log

---

### Recommended Next Steps

**Iteration 1 (Critical)** - Target: 7.5/10
1. [ ] Design loading/skeleton states
2. [ ] Complete mobile navigation design
3. [ ] Add focus states to all interactive elements

**Iteration 2 (Important)** - Target: 8.5/10
1. [ ] Refine typography hierarchy
2. [ ] Standardize spacing to 8px scale
3. [ ] Add project status indicators
4. [ ] Design empty states

**Iteration 3 (Polish)** - Target: 9/10
1. [ ] Micro-interaction specifications
2. [ ] Edge cases (error states, long content)
3. [ ] Final accessibility audit

---

### Timeline Estimate

| Phase | Hours | Priority |
|-------|-------|----------|
| Critical fixes | 5h | High |
| Important improvements | 6h | Medium |
| Polish | 4h | Low |
| **Total** | **15h** | |
```

---

## Prompts Library

### Quick Review
```
Provide a rapid design review of [DESIGN/SCREEN]:

1. First impression (1-10)
2. Top 3 strengths
3. Top 3 issues
4. Most critical fix needed
5. Estimated quality level
```

### Focused Review
```
Review [DESIGN] specifically for [ASPECT]:
- Typography / Color / Layout / UX / Accessibility

Provide:
1. Current state assessment
2. Specific issues found
3. Recommended fixes
4. Priority level
```

### Comparative Review
```
Compare [DESIGN A] vs [DESIGN B]:

1. Which is stronger overall?
2. What does A do better?
3. What does B do better?
4. Recommended elements to combine
```

---

## Success Criteria

### Minimum Requirements
- [ ] All review dimensions addressed
- [ ] Specific issues identified (not vague)
- [ ] Actionable recommendations provided
- [ ] Priority levels assigned
- [ ] Score/rating given

### Quality Indicators
- [ ] Review is balanced (strengths and weaknesses)
- [ ] Issues are specific and verifiable
- [ ] Recommendations are actionable
- [ ] Timeline estimates included
- [ ] Path to 9/10 is clear

---

## Related Skills

- **Next**: `design_scoring.md` - Apply rubric for objective score
- **Next**: `design_iteration.md` - Act on review findings
- **Related**: `accessibility_review.md` - Deep accessibility review
