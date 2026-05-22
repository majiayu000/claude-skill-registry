---
name: ui-density
description: Analyze and improve UI density using Matt Ström's 4-dimensional framework. Use when interfaces feel too sparse, too cluttered, or when users complain about efficiency.
---

# UI Density Analysis

**Core formula:** `Value Density = User Value ÷ (Time + Space)`

Density is NOT about visual crowding. Sparse can be low-value. Dense can be high-value. Google's 2001 homepage beat Yahoo's portal because value density > visual density.

## When This Activates

- "This feels too sparse/empty"
- "This feels cluttered"
- "Users say it takes too long"
- Dashboard or data-heavy interface design

## The Four Dimensions

### 1. Visual Density
What users *perceive*. Unreliable—same elements arranged differently feel different.

Determine whether the perception is a real problem or a grouping problem.

### 2. Information Density
Tufte's data-ink ratio applied to UI.

Point to every element. Verify it communicates something the user needs RIGHT NOW.

### 3. Design Density
How many explicit design decisions (borders, labels, colors) vs implicit ones (Gestalt doing the work).

Check whether proximity/similarity can replace borders. Check whether convention can replace labels.

### 4. Temporal Density
Value delivered per unit of time.

| Delay | Strategy |
|-------|----------|
| <100ms | No animation (adds perceived latency) |
| 100ms–1s | Transition to bridge the gap |
| 1–10s | Spinner |
| 10s–1min | Progress bar |
| >1min | Background task + notification |

Identify where users wait. Determine whether partial results can show earlier.

## Examples

**Low visual density, LOW value density:**
```
Landing page with giant hero image, one headline, scroll to see anything useful.
Problem: Whitespace isn't communicating. User scrolls to find value.
Fix: Put key info above fold. Space should separate, not hide.
```

**High visual density, HIGH value density:**
```
Bloomberg Terminal: Every pixel shows tradeable information.
Why it works: Users need all of it. Instant load. No decoration.
```

**High visual density, LOW value density:**
```
Dashboard showing 20 metrics when user only acts on 3.
Problem: Cognitive load without proportional value.
Fix: Show the 3 actionable metrics prominently. Hide rest behind "more."
```

## Analysis Process

Identify the primary failing dimension first. Then address secondary issues.

```
1. Identify which dimension is the main problem:
   - Visual (perception mismatch)
   - Information (wrong content)
   - Design (inefficient decisions)
   - Temporal (too slow)

2. Determine the specific failure.

3. Define the fix.
```

## Output Format

```
UI DENSITY ANALYSIS

PRIMARY ISSUE: [dimension]
[One sentence describing the specific failure]

VISUAL: [cluttered/balanced/sparse] — [matches reality? if no, why]
INFORMATION: [missing: X] [excess: Y]
DESIGN: [Gestalt opportunities if any]
TEMPORAL: [wait points and feedback gaps]

VALUE DENSITY: [low/medium/high]
FIX: [specific recommendation]
```

## Reference

[UI Density](https://mattstromawn.com/writing/ui-density/) — Matt Ström
