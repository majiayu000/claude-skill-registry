---
name: vs-design
description: High-quality UI design. Mode Collapse prevention, Low-Typicality selection. Use for component, page, dashboard design.
---

# VS Design Diverge (Meeting Context Hub)

## Phase 0: Context Discovery (MANDATORY)

Explore following dimensions via AskUserQuestion:
1. **Emotional Tone**: Trust? Edgy? Calm?
2. **Target Audience**: Who uses it? Technical level?
3. **Reference/Anti-Reference**: What to reference, what to avoid
4. **Business Context**: What problem to solve?

## Phase 1: Identify the Mode (Generic Baseline)

State the most predictable (P~0.95) design. This is NOT to be selected.

Meeting Context Hub default patterns (AI-slop):
- Inter font, purple gradient
- F-pattern layout, white background
- 8px border-radius uniformly

## Phase 2: Sample the Long-Tail (3 Directions)

| Direction | T-Score | Description |
|-----------|---------|-------------|
| A | ~0.7 | Modern/Clean but safe |
| B | ~0.4 | Distinctive/Characterful |
| C | <0.2 | Experimental/Bold |

T-Score justification required for each direction.

## Phase 3: Commit to Low-Typicality

Select lowest T-Score that satisfies Quality Guardrails:
- Visual Hierarchy
- Contrast & Legibility (WCAG AA)
- Internal Consistency
- Functional Clarity

## Meeting Context Hub Design Tone

**Professional + Calm + Organized**
- Keywords: Productivity, team collaboration, information organization
- Colors: Neutral tones (slate, zinc) + accents (blue, green)
- Typography: JetBrains Mono (code), Pretendard (body)

## Domain Components

| Component | Aesthetic Direction |
|-----------|---------------------|
| MeetingCard | Tag badges, date meta |
| PRDSummary | Problem/Goal/Scope sections |
| ActionItemList | Checkboxes, assignee avatars |
| TagSelector | Chip style, autocomplete |
| ContextTimeline | Timeline/grid toggle |

## Final Validation

1. **Intentionality**: Can all decisions be justified?
2. **Consistency**: Internal logic consistent?
3. **Guardrails**: Hierarchy/legibility/clarity?
4. **Surprise**: Stands out in AI-generated lineup?
