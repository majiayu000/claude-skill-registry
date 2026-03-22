---
name: design-scoring
description: "Evaluate and score designs against objective criteria including usability, aesthetics, accessibility, and business goals. Use for: design quality assessment, comparing design alternatives, measuring design effectiveness, and making data-driven design decisions."
---

# Design Scoring

## Description

Design Scoring applies the comprehensive rubric to objectively measure design quality on a 1-10 scale. This enables tracking progress across iterations and provides clear targets for improvement.

## When to Use

- After each design iteration
- To measure progress toward 9/10 goal
- During design reviews
- To identify specific weak areas
- Before declaring design "complete"

**Critical Rule**: All designs must achieve **9/10 or higher** before delivery.

---

## Instructions for AI Agents

### Step 1: Prepare for Scoring

**Pre-scoring checklist:**
```markdown
Before scoring, confirm:
- [ ] Design is complete enough to evaluate
- [ ] All key screens are available
- [ ] Responsive versions exist (or can be inferred)
- [ ] Component states are defined
- [ ] Have access to rubric criteria
```

### Step 2: Apply Rubric Categories

**Score each category (1-10):**

```markdown
## Scoring Worksheet

### Category 1: Visual Aesthetics (25% weight)

#### 1.1 Color Usage (5%)
Score: _/10
Rationale: 

#### 1.2 Typography (5%)
Score: _/10
Rationale: 

#### 1.3 Layout & Composition (5%)
Score: _/10
Rationale: 

#### 1.4 Visual Hierarchy (5%)
Score: _/10
Rationale: 

#### 1.5 Polish & Detail (5%)
Score: _/10
Rationale: 

**Category Score**: (avg of above) = _/10

---

### Category 2: User Experience (25% weight)

#### 2.1 Usability (10%)
Score: _/10
Rationale: 

#### 2.2 Information Architecture (5%)
Score: _/10
Rationale: 

#### 2.3 User Flow (5%)
Score: _/10
Rationale: 

#### 2.4 Content Clarity (5%)
Score: _/10
Rationale: 

**Category Score**: _/10

---

### Category 3: Consistency & Systems (15% weight)

#### 3.1 Design System Adherence (5%)
Score: _/10
Rationale: 

#### 3.2 Component Consistency (5%)
Score: _/10
Rationale: 

#### 3.3 Spacing & Rhythm (5%)
Score: _/10
Rationale: 

**Category Score**: _/10

---

### Category 4: Responsiveness (15% weight)

#### 4.1 Mobile Design (5%)
Score: _/10
Rationale: 

#### 4.2 Tablet/Desktop Adaptation (5%)
Score: _/10
Rationale: 

#### 4.3 Cross-Platform Consistency (5%)
Score: _/10
Rationale: 

**Category Score**: _/10

---

### Category 5: Accessibility (10% weight)

#### 5.1 Color Accessibility (4%)
Score: _/10
Rationale: 

#### 5.2 Interactive Accessibility (3%)
Score: _/10
Rationale: 

#### 5.3 Content Accessibility (3%)
Score: _/10
Rationale: 

**Category Score**: _/10

---

### Category 6: Brand & Identity (10% weight)

#### 6.1 Brand Expression (5%)
Score: _/10
Rationale: 

#### 6.2 Emotional Design (5%)
Score: _/10
Rationale: 

**Category Score**: _/10
```

### Step 3: Calculate Final Score

**Weighted calculation:**

```markdown
## Final Score Calculation

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Visual Aesthetics | _/10 | × 0.25 | = _ |
| User Experience | _/10 | × 0.25 | = _ |
| Consistency | _/10 | × 0.15 | = _ |
| Responsiveness | _/10 | × 0.15 | = _ |
| Accessibility | _/10 | × 0.10 | = _ |
| Brand & Identity | _/10 | × 0.10 | = _ |
| **FINAL SCORE** | | | **_/10** |

### Quality Level
| Score Range | Level | Action |
|-------------|-------|--------|
| 9.0-10.0 | ✅ Excellent | Ready for delivery |
| 8.0-8.9 | Good | Minor polish needed |
| 7.0-7.9 | Average | Focused improvements |
| 6.0-6.9 | Below Average | Significant revision |
| <6.0 | Poor | Major rework required |

**Current Level**: [Level]
**Ready for Delivery**: [Yes/No]
```

### Step 4: Gap Analysis

**Identify improvement path:**

```markdown
## Gap Analysis

### Current State
- **Score**: [X/10]
- **Target**: 9.0/10
- **Gap**: [Y points]

### Weakest Categories (Focus Here)

1. **[Category with lowest score]**: [Score]/10
   - Why it's low: [Explanation]
   - To reach 9: [Specific improvements needed]
   - Estimated effort: [Hours]

2. **[Second lowest category]**: [Score]/10
   - Why it's low: [Explanation]
   - To reach 9: [Specific improvements needed]
   - Estimated effort: [Hours]

### Strongest Categories (Maintain)

1. **[Highest category]**: [Score]/10
   - Keep: [What's working]
   - Avoid: [What could reduce this]

### Impact Analysis

To reach 9.0:
- If we improve [Category 1] from [X] to 9: Final = [new score]
- If we improve [Category 2] from [X] to 9: Final = [new score]
- Most efficient path: [Which categories to focus on]
```

---

## Example Input/Output

### Example Input

```markdown
**Design**: TaskFlow Dashboard v2
**Context**: Second iteration after addressing critical issues
```

### Example Output

```markdown
## Design Score Card: TaskFlow v2

**Date**: Current
**Iteration**: 2
**Previous Score**: 6.5/10

---

### Category Scores

#### Visual Aesthetics (25%)
| Subcategory | Score | Notes |
|-------------|-------|-------|
| Color Usage | 8/10 | Good palette, minor contrast issue in one badge |
| Typography | 7/10 | Improved hierarchy, line-height still tight |
| Layout | 8/10 | Grid now consistent, good whitespace |
| Hierarchy | 8/10 | Clear primary actions, good focal points |
| Polish | 7/10 | Much improved, some shadow inconsistencies |
| **Average** | **7.6/10** | |

#### User Experience (25%)
| Subcategory | Score | Notes |
|-------------|-------|-------|
| Usability | 8/10 | Flows are clear, one confusing state |
| Information Arch | 8/10 | Navigation logical, labels clear |
| User Flow | 8/10 | Task completion smooth |
| Content Clarity | 8/10 | Good copywriting, scannable |
| **Average** | **8.0/10** | |

#### Consistency (15%)
| Subcategory | Score | Notes |
|-------------|-------|-------|
| Design System | 8/10 | Following established patterns |
| Components | 8/10 | Cards consistent, buttons unified |
| Spacing | 7/10 | Mostly 8px scale, one section off |
| **Average** | **7.7/10** | |

#### Responsiveness (15%)
| Subcategory | Score | Notes |
|-------------|-------|-------|
| Mobile | 7/10 | Good but task list needs work |
| Desktop/Tablet | 8/10 | Well adapted |
| Cross-Platform | 8/10 | Consistent feel |
| **Average** | **7.7/10** | |

#### Accessibility (10%)
| Subcategory | Score | Notes |
|-------------|-------|-------|
| Color | 8/10 | Passes WCAG AA |
| Interactive | 7/10 | Focus states need enhancement |
| Content | 8/10 | Good semantics planned |
| **Average** | **7.7/10** | |

#### Brand & Identity (10%)
| Subcategory | Score | Notes |
|-------------|-------|-------|
| Brand Expression | 8/10 | Violet brand clear, differentiates |
| Emotional Design | 7/10 | Professional but could be warmer |
| **Average** | **7.5/10** | |

---

### Final Score Calculation

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Visual Aesthetics | 7.6 | × 0.25 | 1.90 |
| User Experience | 8.0 | × 0.25 | 2.00 |
| Consistency | 7.7 | × 0.15 | 1.16 |
| Responsiveness | 7.7 | × 0.15 | 1.16 |
| Accessibility | 7.7 | × 0.10 | 0.77 |
| Brand & Identity | 7.5 | × 0.10 | 0.75 |
| **FINAL SCORE** | | | **7.74/10** |

### Quality Assessment

**Score**: 7.74/10 (+1.24 from v1)
**Level**: Average (approaching Good)
**Ready for Delivery**: ❌ No (target: 9.0)
**Gap to Target**: 1.26 points

---

### Gap Analysis

#### Progress Made 📈
- Visual hierarchy improved significantly
- Mobile design now exists
- Consistency much better
- Loading states added

#### Remaining Gaps to 9.0

**Priority 1: Brand & Identity (7.5 → 9.0)**
- Impact: +0.15 to final score
- Actions needed:
  - Add warmer illustration/imagery
  - Include delightful micro-interactions
  - Strengthen empty states with personality
- Effort: 4 hours

**Priority 2: Visual Polish (7.6 → 9.0)**
- Impact: +0.35 to final score
- Actions needed:
  - Fix typography line-heights
  - Standardize all shadows
  - Perfect border radius consistency
- Effort: 3 hours

**Priority 3: Accessibility (7.7 → 9.0)**
- Impact: +0.13 to final score
- Actions needed:
  - Enhance focus states
  - Add skip links
  - Verify all touch targets
- Effort: 2 hours

**Priority 4: Responsiveness (7.7 → 9.0)**
- Impact: +0.20 to final score
- Actions needed:
  - Refine mobile task list
  - Test tablet landscape
- Effort: 3 hours

---

### Path to 9.0

**If all priorities addressed:**
- Visual: 7.6 → 9.0 (+1.4 × 0.25 = +0.35)
- Brand: 7.5 → 9.0 (+1.5 × 0.10 = +0.15)
- Accessibility: 7.7 → 9.0 (+1.3 × 0.10 = +0.13)
- Responsiveness: 7.7 → 9.0 (+1.3 × 0.15 = +0.20)

**Projected Score**: 7.74 + 0.83 = **8.57/10**

To reach 9.0, also need:
- UX improvements (+0.25 × 1.0 = +0.25)
- Consistency improvements (+0.15 × 1.3 = +0.20)

**Estimated total effort**: 12 hours

---

### Recommendation

**Next Iteration Focus** (Iteration 3):
1. Visual polish (biggest impact)
2. Responsiveness refinement
3. Accessibility enhancement

**Expected Score After Iteration 3**: 8.5-9.0/10
```

---

## Prompts Library

### Quick Score
```
Score this design quickly (1-10):
[DESIGN]

Provide:
- Overall score with one-line rationale
- Strongest category
- Weakest category
- One action to improve most
```

### Category Deep-Dive
```
Score [DESIGN] deeply on [CATEGORY]:

For each subcategory:
1. Score (1-10)
2. Evidence/rationale
3. Specific improvement to reach 9
```

### Progress Comparison
```
Compare scores between [VERSION 1] and [VERSION 2]:

1. Score comparison table
2. Improvements made
3. Regressions (if any)
4. Remaining work to 9/10
```

---

## Success Criteria

### Minimum Requirements
- [ ] All categories scored
- [ ] Final weighted score calculated
- [ ] Rationale provided for each score
- [ ] Gap to 9/10 identified

### Quality Indicators
- [ ] Scores are calibrated consistently
- [ ] Rationale is specific, not vague
- [ ] Path to improvement is clear
- [ ] Effort estimates included

---

## Related Skills

- **Reference**: `design_rubric.md` - Full scoring criteria
- **Previous**: `design_review.md` - Qualitative review
- **Next**: `design_iteration.md` - Act on score gaps
