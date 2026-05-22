---
description: Analyze component screenshots and design artifacts against Northcote
  Curio visual standards. Validate typography (distinctiveness, Victorian craftsmanship),
  color palette (Australian botanical colors), layout (organic spacing, asymmetry),
  and botanical motif integration. Generate compliance assessments and design evolution
  analysis.
name: northcote-visual-audit
---

# Northcote Visual Audit Skill

## Overview

Closes the gap between specification and reality. Uses Claude's vision capabilities to visually analyze component screenshots and validate them against Northcote Curio design standards.

This skill transforms design system management from **specification-heavy and hope-driven** to **visually-grounded and continuously validated**.

## When to Use This Skill

Use this skill when you need to:

- **Audit a component screenshot** against Northcote design standards
- **Validate typography choices** (are fonts distinctive and intentional?)
- **Check color palette adherence** (are colors true to Australian botanical palette?)
- **Assess layout coherence** (is spacing organic or mechanical?)
- **Compare component evolution** (Material Design → Northcote transformation)
- **Generate compliance reports** (pass/fail/needs-refinement assessments)
- **Identify design system drift** (are components becoming more or less Northcote?)

## How It Works

The skill uses Claude's vision capabilities to:

1. **Analyze visual properties** of rendered components
2. **Extract design data** (typography, colors, spacing, motifs)
3. **Validate against spec** (does it match Northcote standards?)
4. **Generate audit report** (structured assessment with pass/fail per criterion)
5. **Suggest refinements** (where and how to improve)

## Audit Criteria

### 1. Typography Audit

**Pass**: Distinctive fonts (Lora, Crimson Text, Fraunces) with clear display+body pairing
**Needs Refinement**: Good fonts but pairing unclear or emotion undefined
**Fail**: Generic fonts (Inter, Arial, Roboto, Space Grotesk) or undefined hierarchy

### 2. Color Audit

**Pass**: Australian botanical palette (sage, terracotta, ochre, gold) with cohesive harmony
**Needs Refinement**: Correct colors but harmony feels off or theme inconsistent
**Fail**: Colors disconnected from botanical inspiration or purple gradients (generic default)

### 3. Layout Audit

**Pass**: Organic spacing, intentional asymmetry, clear visual hierarchy
**Needs Refinement**: Good spacing but feels slightly mechanical or hierarchy ambiguous
**Fail**: Grid-rigid, mechanical patterns or predictable cookie-cutter layouts

### 4. Botanical Elements Audit

**Pass**: Naturalist motifs integrated meaningfully, supporting hierarchy or clarity
**Needs Refinement**: Motifs present but feel slightly ornamental or purpose unclear
**Fail**: No motifs (when expected) or motifs feel decorative/bolted-on

### 5. Overall Aesthetic Coherence

**Pass**: Component clearly embodies Northcote vision; unmistakably intentional
**Needs Refinement**: Good direction but missing some coherence or personalization
**Fail**: Feels generic or like multiple conflicting aesthetic directions

### 6. Microcopy Audit

**Pass**: Copy is immediately understandable; personality enhances without obscuring.
**Needs Refinement**: Personality present but action unclear (e.g., themed label without context).
**Fail**: Copy is so themed that users cannot determine what the element does.

**Key Test**: Can a first-time user understand the action within 2 seconds?

_See [DOC-006 Voice Tier System](file:///Users/okgoogle13/Desktop/careercopilot/docs/archive/atomic-v2/DOC-006_Voice_and_Microcopy.md) for voice guidelines._

## Usage Examples

### Example 1: Basic Component Audit

"Audit this Pebble button screenshot against Northcote standards"

Upload screenshot. Claude will:

1. Identify fonts, colors, spacing
2. Assess against each criterion
3. Generate pass/fail for each dimension
4. Provide specific recommendations
5. Return structured JSON report

### Example 2: Comparative Analysis

"Compare this Material Design button to the Northcote version and document the evolution"

Upload both screenshots. Claude will:

1. Analyze original (Material Design aesthetics)
2. Analyze updated (Northcote aesthetic)
3. Document typography transformation
4. Assess color palette shift
5. Evaluate overall aesthetic evolution
6. Tell the story of the design transformation

### Example 3: Batch Component Auditing

"Audit all components in this directory screenshot collection against Northcote standards"

Multiple screenshots. Claude will:

1. Audit each component individually
2. Generate pass/fail for each
3. Identify patterns (what's working, what's not)
4. Summarize compliance across portfolio
5. Highlight priority refinement targets

### Example 4: Design Evolution Tracking

"Show me how this component has evolved through versions toward Northcote coherence"

Historical screenshots. Claude will:

1. Analyze progression across versions
2. Identify where aesthetic solidified
3. Note when intentionality increased
4. Document visual maturity trajectory
5. Assess current alignment with Northcote

## The Audit Report Format

Structured JSON output for integration with compliance dashboards:

```json
{
  "audit": {
    "component_name": "Pebble Button",
    "audit_date": "2026-01-28T...",
    "overall_status": "pass|needs_refinement|fail",
    "compliance_score": 0-100,

    "dimensions": {
      "typography": {
        "status": "pass|needs_refinement|fail",
        "findings": "Lora display + Crimson Text body established",
        "specifics": {
          "display_font": "Lora",
          "body_font": "Crimson Text",
          "hierarchy_clarity": "clear",
          "distinctiveness": "high"
        }
      },
      "color": {
        "status": "pass|needs_refinement|fail",
        "findings": "Sage primary, terracotta accent, within botanical palette",
        "palette_adherence": "100%",
        "theme_consistency": "light_mode_cohesive"
      },
      "layout": {
        "status": "pass|needs_refinement|fail",
        "findings": "Organic spacing with intentional asymmetry",
        "spacing_quality": "organic",
        "hierarchy_clarity": "strong"
      },
      "botanical_elements": {
        "status": "pass|needs_refinement|fail",
        "findings": "Subtle sage motif supports visual weight",
        "integration_quality": "meaningful",
        "ornamental_risk": "low"
      }
    },

    "assessment": "Component strongly embodies Northcote vision",
    "recommendations": [
      "Consider slightly warmer undertone in accent color",
      "Botanical motif could be slightly more prominent without becoming decorative"
    ],

    "design_narrative": "This button demonstrates intentional design mastery..."
  }
}
```

## Key Capabilities

### Visual Data Extraction

Claude can identify:

- Actual fonts rendered (not what you hoped)
- Exact color usage (hex values or descriptions)
- Spacing patterns (organic vs. mechanical)
- Visual hierarchy establishment
- Botanical motif presence and integration

### Comparative Analysis

Can compare:

- Before/after (Material Design → Northcote)
- Multiple variants (design iterations)
- Component families (consistency across types)
- Historical progression (maturity tracking)

### Pattern Recognition

Identifies:

- What's working well across components
- Where standards are being violated
- Edge cases needing attention
- Trends (improving or diverging?)

## Integration with Other Skills

### With Northcote-Typography-Strategy

Validates that typography choices made are actually rendering as intended.

### With Frontend-Design

Assesses whether components match aesthetic direction established in design phase.

### With Compliance-Dashboard

Audit results feed into dashboard for continuous tracking.

### With Brand-Brief-Optimizer

Reveals where brief language is clear (audits consistent) vs. vague (audits inconsistent).

## Important Limitations

This skill:

✅ Analyzes rendered visual output with high accuracy
✅ Identifies design intent through visual analysis
✅ Detects patterns across multiple components
✅ Provides structured assessment for automation

❌ Cannot measure pixel-perfect specifications
❌ Cannot validate accessibility (beyond visual appearance)
❌ Cannot assess performance or rendering speed
❌ Judgments should be human-verified for high-stakes decisions

## Best Practices

1. **Provide context**: Tell Claude the component name and purpose
2. **Screenshot quality**: Use clean, well-lit screenshots for accuracy
3. **Multiple images**: For complex components, screenshot different states
4. **Human verification**: Audit results should feed into human review loop
5. **Iteration**: Use feedback to refine both components and brief language

## Execution & Validation Checklist

Before checking off an asset as audit-complete, ensure it passes the **Northcote Visual Audit**:

- [ ] **Palette Compliance:** Is the red _Waratah Crimson_ (#C45C4B)? Is the gold _Wattle Gold_ (#D4A84B)? **Are there any forbidden blues/purples?**
- [ ] **Anatomical Geometry:** Does the Echidna spine cluster look mathematical? Does the Banksia pod show a spiral?
- [ ] **Lighting:** Is the background pure black (#1A1714)? Is there dramatic contrast?
- [ ] **Typology:** If text is present, is it a cream serif font (e.g., "Fig. II")?

## Validation Questions

Before deploying audit results, verify:

- Does the audit capture what you see visually?
- Are the findings specific and actionable?
- Do the recommendations improve the component?
- Is the assessment repeatable (would someone else agree)?
- Does this feed meaningful signal into your compliance dashboard?

If yes to all, the audit is reliable.

## Related Documentation

See `references/northcote-visual-spec.md` for complete audit criteria.
See `references/component-examples.md` for exemplary passing/failing components.
See `references/design-evolution-tracking.md` for how to document visual transformation over time.

---

_Vision audit transforms design system management from specification-only to visually-validated. This closes the loop between intention and implementation._
