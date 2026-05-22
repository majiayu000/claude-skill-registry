---
name: fix-spacing
description: This skill should be used when elements feel disconnected, cards float like islands, or groupings are unclear. Applies Law of Proximity, Law of Common Region, and Law of Uniform Connectedness.
---

# Fix Spacing Issues

## Purpose

This skill diagnoses and fixes spacing issues that make interfaces feel disconnected or unclear. It applies three fundamental perceptual laws to create proper visual grouping and hierarchy through strategic use of whitespace, boundaries, and visual connections.

Applies these laws from lawsofux.com:
- **Law of Proximity**: Objects near each other appear grouped
- **Law of Common Region**: Elements sharing a boundary appear related
- **Law of Uniform Connectedness**: Visually connected elements seem more related

## When to Use

- "Cards feel like islands"
- "Everything is the same distance apart"
- "Elements feel disconnected"
- "Groupings are unclear"
- "No visual rhythm"

## The Laws

### Law of Proximity

> Objects that are near each other tend to be grouped together.

**Application:**
```
Space WITHIN groups < Space BETWEEN groups

Card padding < Gap between cards < Section gap
```

**Violation test:**
```
Proximity Ratio = internal spacing / external spacing
PASS: ratio < 1.0
FAIL: ratio ≥ 1.0
```

### Law of Common Region

> Elements tend to be perceived as groups if they share a clearly defined boundary.

**Application:**
- Add backgrounds, borders, or containers to create regions
- Don't rely on proximity alone for complex groupings
- Nested regions show hierarchy

### Law of Uniform Connectedness

> Elements that are visually connected are perceived as more related than elements with no connection.

**Application:**
- Lines, arrows, or shared colors connect related items
- Timelines, flowcharts, breadcrumbs use this
- Stronger than proximity for showing relationships

## Diagnosis

For each group of elements, check:

```
1. PROXIMITY: Is internal < external spacing?
2. REGION: Do related items share a boundary?
3. CONNECTION: Are sequential items visually linked?
```

## Output Format

```
SPACING DIAGNOSIS

Law of Proximity:
WHERE: [component]
Ratio: [internal]px / [external]px = [X]
Violation: [Yes/No]
FIX: [change]

Law of Common Region:
WHERE: [component]
Issue: [missing boundary / competing regions]
FIX: [add container / adjust]

Law of Uniform Connectedness:
WHERE: [component]
Issue: [disconnected sequence]
FIX: [add connector]
```

## Quick Reference

| Spacing | Tailwind | Use for |
|---------|----------|---------|
| 4px | gap-1, p-1 | Tight inline elements |
| 8px | gap-2, p-2 | Related items in a group |
| 16px | gap-4, p-4 | Items within a card |
| 24px | gap-6, p-6 | Cards in a grid |
| 32px | gap-8 | Between sections |
| 48-64px | py-12/16 | Major section breaks |

**Rule:** Each level should be ~1.5-2x the previous.
