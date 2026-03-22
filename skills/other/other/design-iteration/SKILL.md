---
name: design-iteration
description: "Refine and improve designs based on feedback, testing, and evolving requirements through iterative cycles. Use for: incorporating feedback, A/B testing results, user testing insights, stakeholder revisions, and continuous improvement."
---

# Design Iteration

## Description

Design Iteration is the systematic process of improving designs based on review findings and score gaps. This skill ensures each iteration moves closer to the 9/10 quality target through focused, prioritized changes.

## When to Use

- After design review identifies issues
- When score is below 9/10
- To address specific feedback
- During refinement phase
- Before final handoff

---

## Instructions for AI Agents

### Step 1: Prioritize Issues

**Impact/Effort matrix:**

```markdown
## Issue Prioritization

### High Impact, Low Effort (Do First) 🟢
[Issues that significantly improve quality with minimal work]

1. [Issue]: [Impact description] | Effort: [X hours]
2. [Issue]: [Impact description] | Effort: [X hours]

### High Impact, High Effort (Schedule) 🟡
[Issues that are important but require significant work]

1. [Issue]: [Impact description] | Effort: [X hours]

### Low Impact, Low Effort (Quick Wins) 🟢
[Small improvements that polish the design]

1. [Issue]: [Impact description] | Effort: [X hours]

### Low Impact, High Effort (Defer) 🔴
[Consider if worth the effort, may skip]

1. [Issue]: [Impact description] | Effort: [X hours]
```

### Step 2: Plan Iteration

**Iteration plan template:**

```markdown
## Iteration Plan: V[X] → V[X+1]

### Goal
Move from [current score] to [target score]

### Scope
**In Scope**:
- [Change 1]
- [Change 2]
- [Change 3]

**Out of Scope** (next iteration):
- [Deferred item 1]
- [Deferred item 2]

### Checklist

#### Visual Design Improvements
- [ ] [Specific change 1]
- [ ] [Specific change 2]

#### UX Improvements
- [ ] [Specific change 1]
- [ ] [Specific change 2]

#### Consistency Fixes
- [ ] [Specific change 1]
- [ ] [Specific change 2]

#### Accessibility Fixes
- [ ] [Specific change 1]

### Expected Outcome
- Score improvement: +[X] points
- Target score: [X]/10
```

### Step 3: Execute Changes

**For each change, document:**

```markdown
## Change Log: V[X]

### Change 1: [Title]
**Category**: [Visual/UX/Consistency/Accessibility/Brand]
**Issue**: [What was wrong]
**Solution**: [What was changed]
**Before**: [Description or reference]
**After**: [Description or reference]

### Change 2: [Title]
...
```

### Step 4: Validate Changes

**Post-iteration checklist:**

```markdown
## Iteration Validation

### Issue Resolution
- [ ] Issue 1: Verified fixed
- [ ] Issue 2: Verified fixed
- [ ] Issue 3: Verified fixed

### No Regressions
- [ ] Previous strengths maintained
- [ ] No new issues introduced
- [ ] Consistency not broken

### Quality Check
- [ ] Quick visual scan passes
- [ ] Primary flows still work
- [ ] Responsive behavior intact

### Ready for Re-scoring
- [ ] All planned changes complete
- [ ] Documentation updated
- [ ] Ready for `design_scoring.md`
```

---

## Example Input/Output

### Example Input

```markdown
**Current Version**: TaskFlow v2
**Current Score**: 7.74/10
**Target**: 9.0/10
**Key Issues from Review**:
1. Typography line-height too tight
2. Shadow inconsistencies
3. Focus states need enhancement
4. Mobile task list needs refinement
5. Empty states lack personality
```

### Example Output

```markdown
## Iteration Plan: TaskFlow V2 → V3

### Goal
Move from 7.74/10 to 8.5+/10

### Priority Matrix

#### Do First (High Impact, Low Effort)
1. **Fix typography line-heights** | +0.1 impact | 1 hour
   - Body: 1.5 → 1.6
   - Headings: 1.2 → 1.3
   
2. **Standardize shadows** | +0.05 impact | 30 min
   - Define: shadow-sm, shadow-md, shadow-lg
   - Apply consistently to all cards

3. **Enhance focus states** | +0.1 impact | 1 hour
   - Add visible focus ring (3px violet-200)
   - Ensure all interactive elements covered

#### Schedule (High Impact, High Effort)
4. **Mobile task list redesign** | +0.15 impact | 3 hours
   - Convert to swipeable cards
   - Larger touch targets
   - Pull to refresh

5. **Empty states with personality** | +0.1 impact | 2 hours
   - Add illustrations
   - Friendly copy
   - Clear CTAs

#### Quick Wins (Low Impact, Low Effort)
6. **Border radius consistency** | +0.02 | 15 min
7. **Button hover state refinement** | +0.02 | 15 min

---

### Iteration Scope

**V3 Scope** (This iteration - Target: 8.5/10):
- Typography line-heights ✓
- Shadow standardization ✓
- Focus states ✓
- Mobile task list ✓
- Quick wins ✓

**V4 Scope** (Next iteration - Target: 9.0/10):
- Empty states
- Micro-interactions
- Final accessibility audit
- Edge case handling

---

### Detailed Changes

#### 1. Typography Line-Heights

**Before:**
```css
body { line-height: 1.5; }
h1 { line-height: 1.1; }
h2 { line-height: 1.1; }
```

**After:**
```css
body { line-height: 1.6; }
h1 { line-height: 1.2; }
h2 { line-height: 1.25; }
h3 { line-height: 1.3; }
```

**Impact**: Improved readability, especially in dense content areas.

---

#### 2. Shadow Standardization

**Before**: Mix of values
- Card A: `box-shadow: 0 1px 3px rgba(0,0,0,0.1)`
- Card B: `box-shadow: 0 2px 4px rgba(0,0,0,0.15)`
- Card C: `box-shadow: 0 1px 2px rgba(0,0,0,0.08)`

**After**: Consistent scale
```css
--shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px rgba(0,0,0,0.07);
--shadow-lg: 0 10px 15px rgba(0,0,0,0.1);

/* All cards use shadow-md */
.card { box-shadow: var(--shadow-md); }
```

**Impact**: Visual consistency, professional appearance.

---

#### 3. Focus States

**Before**: Browser default (often invisible)

**After**:
```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 3px var(--violet-200);
}

/* Buttons */
.btn:focus-visible {
  box-shadow: 0 0 0 3px var(--violet-200);
}

/* Inputs */
.input:focus {
  border-color: var(--violet-500);
  box-shadow: 0 0 0 3px var(--violet-100);
}
```

**Impact**: Accessibility improvement, WCAG compliance.

---

#### 4. Mobile Task List Redesign

**Before**:
```
┌────────────────────┐
│ ○ Task name      > │  <- Small touch target
│   Due today       │
└────────────────────┘
```

**After**:
```
┌───────────────────────┐
│  ┌───┐                │
│  │   │  Task name     │  <- 48px touch target
│  │ ○ │                │
│  │   │  Acme • Today   │
│  └───┘                │
└───────────────────────┘
    ↑
    Swipe left to complete/delete
```

Changes:
- Larger card padding (16px → 20px)
- Checkbox area: 48×48px touch target
- Swipe actions for complete/delete
- Pull-to-refresh at top
- Clearer visual separation between tasks

---

#### 5-6. Quick Wins

**Border radius standardized**:
- All cards: 12px
- All buttons: 8px
- All inputs: 8px
- All modals: 16px

**Button hover refined**:
```css
.btn-primary:hover {
  background: var(--violet-400);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}
```

---

### Expected Score Impact

| Category | V2 | V3 Expected | Change |
|----------|-----|-------------|--------|
| Visual | 7.6 | 8.2 | +0.6 |
| UX | 8.0 | 8.2 | +0.2 |
| Consistency | 7.7 | 8.5 | +0.8 |
| Responsiveness | 7.7 | 8.3 | +0.6 |
| Accessibility | 7.7 | 8.5 | +0.8 |
| Brand | 7.5 | 7.8 | +0.3 |

**Projected V3 Score**: 8.3/10

---

### Validation Checklist

- [ ] Line-heights feel more comfortable
- [ ] Shadows consistent across all cards
- [ ] Tab through interface shows clear focus
- [ ] Mobile task list easier to use
- [ ] Border radius consistent
- [ ] Hover states refined
- [ ] No regressions in other areas
- [ ] Ready for V3 scoring
```

---

## Prompts Library

### Iteration Planning
```
Plan iteration from [CURRENT SCORE] to [TARGET SCORE]:

Given these issues:
[ISSUE LIST]

Create:
1. Priority matrix
2. Scope for this iteration
3. What to defer
4. Expected score impact
```

### Change Implementation
```
Implement this design change:
- Issue: [ISSUE]
- Goal: [DESIRED OUTCOME]

Provide:
1. Before state
2. After state (detailed spec)
3. CSS/design token changes
4. Verification criteria
```

### Iteration Review
```
Review iteration V[X] → V[X+1]:

1. Were all planned changes made?
2. What improved?
3. Any regressions?
4. Ready for re-scoring?
5. Remaining work estimate?
```

---

## Success Criteria

### Minimum Requirements
- [ ] High-impact issues addressed
- [ ] Changes documented
- [ ] No regressions introduced
- [ ] Ready for re-scoring

### Quality Indicators
- [ ] Score improved as expected
- [ ] Changes align with design system
- [ ] Iteration moves toward 9/10
- [ ] Sustainable pace (not rushed)

---

## Related Skills

- **Previous**: `design_scoring.md` - Know what to improve
- **Next**: `design_review.md` - Validate improvements
- **Loop**: Continue until 9/10 achieved
