---
name: fix-hierarchy
description: This skill should be used to fix visual hierarchy when everything looks equally important, CTAs don't stand out, or users miss key information. Applies Von Restorff Effect, Serial Position Effect, and Law of Prägnanz.
---

# Fix Visual Hierarchy

Applies these laws from lawsofux.com:
- **Von Restorff Effect**: Distinctive items among similar ones are remembered
- **Serial Position Effect**: First and last items are most memorable
- **Law of Prägnanz**: People interpret complex images in the simplest way

## When to Use

- "Everything looks the same"
- "CTA doesn't stand out"
- "Users miss important info"
- "Page feels flat"
- "Too much competing for attention"

## How to Use

1. Analyze the interface against the three laws (Von Restorff, Serial Position, Prägnanz)
2. Identify hierarchy violations in the diagnosis
3. Apply the recommended fixes from the output format
4. Verify that exactly ONE element stands out and hierarchy is immediately clear

## The Laws

### Von Restorff Effect (Isolation Effect)

> When multiple similar objects are present, the one that differs from the rest is most likely to be remembered.

**Application:**
```
Make ONE thing visually distinct:
- Different color (only CTA is blue)
- Different size (hero text 2x larger)
- Different weight (only headline is bold)
- Different treatment (only CTA has shadow)
```

**Violation:** Multiple elements using the "special" treatment.

### Serial Position Effect

> Users best remember the first and last items in a series.

**Application:**
```
FIRST position: Most important action/info
LAST position: Secondary important action
MIDDLE: Supporting content (will be skimmed)
```

**For navigation:** Home (first), CTA (last)
**For forms:** Key field (first), Submit (last)
**For lists:** Critical items at ends

### Law of Prägnanz (Simplicity)

> People perceive and interpret ambiguous or complex images as the simplest form possible.

**Application:**
```
Reduce to minimum elements needed:
- Remove decorative complexity
- Use simple shapes over complex ones
- Clear figure/ground relationship
- Obvious visual hierarchy
```

**Test:** Can a user describe the page in one sentence?

## Diagnosis

```
1. VON RESTORFF: Is exactly ONE element isolated/distinct?
2. SERIAL POSITION: Are key items at start/end?
3. PRÄGNANZ: Is hierarchy immediately obvious?
```

## Output Format

```
HIERARCHY DIAGNOSIS

Von Restorff Effect:
Primary element: [what should stand out]
Currently isolated: [what actually stands out]
Competing elements: [list of things fighting for attention]
FIX: [make X distinct, reduce prominence of Y]

Serial Position Effect:
First position: [what's there] → [what should be]
Last position: [what's there] → [what should be]
FIX: [reorder]

Law of Prägnanz:
Complexity score: [high/medium/low]
Can describe in one sentence: [Yes/No]
FIX: [simplify by...]
```

## Quick Fixes

| Problem | Law | Fix |
|---------|-----|-----|
| CTA invisible | Von Restorff | Make it the ONLY colored/bold element |
| Users skip content | Serial Position | Move to first or last position |
| Page overwhelming | Prägnanz | Remove 30% of elements |
| Everything bold | Von Restorff | Unbold everything except ONE |
| Nav items equal | Serial Position | Emphasize first and last |
