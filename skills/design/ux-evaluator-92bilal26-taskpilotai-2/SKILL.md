---
name: ux-evaluator
description: This skill should be used when evaluating UI components against UX best practices. Use for reviewing buttons, navigation elements, spacing, visual hierarchy, or any interface element. Provides a systematic 3-dimension framework (Position, Visual Weight, Spacing) aligned with industry standards (Balsamiq, Nielsen heuristics). Invoke when user asks to "review UX", "check button design", "evaluate layout", or references design guidelines.
---

# UX Evaluator

## Overview

Systematically evaluate UI components against established UX principles using a 3-dimension framework. Transform subjective design feedback into actionable, evidence-based recommendations by comparing against industry conventions and authoritative sources.

**Core Value**: Prevents subjective design debates by grounding decisions in documented best practices.

## When to Use This Skill

**Triggers**:
- User provides UX feedback on a component
- User references external design guidelines (Balsamiq, Nielsen, Material Design)
- User asks to "review", "evaluate", or "check" UI elements
- User questions button labels, spacing, or visual hierarchy
- Before implementing UI changes that affect user interaction

**Do NOT use for**:
- Pure visual aesthetics (colors, fonts) without UX implications
- Backend or non-UI changes
- When user has already made a firm decision and just wants implementation

## Evaluation Framework

### The 3-Dimension Analysis

For ANY UI component, evaluate these three dimensions:

| Dimension | What to Analyze | Key Questions |
|-----------|-----------------|---------------|
| **1. Position** | Where is it located relative to other elements? | Does position follow conventions? Is it discoverable? |
| **2. Visual Weight** | How prominent is it visually? | Does it compete with primary actions? Is hierarchy clear? |
| **3. Spacing** | What's the gap from adjacent elements? | Is there adequate separation? Is spacing consistent? |

### Evaluation Workflow

```
Step 1: GATHER CONTEXT
├── What component is being evaluated?
├── What user feedback or concern triggered this?
├── Is there an external reference (article, guideline)?
└── What is the component's purpose (primary CTA, utility, navigation)?

Step 2: ANALYZE CURRENT STATE
├── Position: Document exact location in layout
├── Visual Weight: Describe styling (filled, ghost, icon-only, etc.)
├── Spacing: Measure gaps from adjacent elements
└── Compare to industry conventions (see references/)

Step 3: PRODUCE VERDICT
├── For each dimension: CORRECT / NEEDS CHANGE / ACCEPTABLE
├── If NEEDS CHANGE: Specific recommendation with rationale
├── Reference authoritative source for each recommendation
└── Prioritize changes (P1: breaks UX, P2: suboptimal, P3: polish)
```

## Component-Specific Guidelines

### Buttons (Action Elements)

**Position**:
- Primary action (Sign Up, Submit, Buy) → RIGHT side
- Secondary action (Cancel, Sign In) → LEFT of primary
- Utility controls (theme, settings) → FAR RIGHT after primary actions

**Visual Weight**:
- Primary: Filled background, brand color, shadow
- Secondary: Ghost/outline, no fill, subtle border
- Utility: Icon-only or minimal text, neutral color

**Spacing**:
- Between button groups: 1.5rem (24px) minimum
- Between buttons in same group: 0.5rem-0.75rem (8-12px)
- Touch targets: 44px minimum height on mobile

**Labels**:
- Use conventional labels: "Sign Up" not "Get Started", "Sign In" not "Login"
- Say exactly what happens: "Delete Account" not "Proceed"
- Verb-first for actions: "Create Project", "Send Message"

### Navigation Elements

**Position**:
- Logo → LEFT
- Primary nav → CENTER or after logo
- Utility items (search, auth, theme) → RIGHT

**Visual Weight**:
- Active state clearly distinguished
- Current page indicator visible
- Don't compete with page content

**Spacing**:
- Group related items visually
- Clear separation between nav groups
- Adequate click/tap targets

### Form Elements

**Position**:
- Labels above or to the left of inputs
- Submit button at bottom, right-aligned or full-width
- Error messages adjacent to field

**Visual Weight**:
- Required fields marked clearly
- Error states prominent (red border/text)
- Success states confirmatory (green checkmark)

**Spacing**:
- Consistent vertical rhythm between fields
- Label-to-input gap: 0.25-0.5rem
- Field-to-field gap: 1-1.5rem

## Industry Conventions Reference

### Button Order (Major Sites)

| Site | Pattern |
|------|---------|
| GitHub | [Sign In] [Sign Up] - secondary left, primary right |
| Stripe | [Sign In] [Start now →] - secondary left, primary right |
| Google | [Sign In] [Create account] - same pattern |
| Notion | [Log in] [Get Notion free] - same pattern |

**Verdict**: Secondary LEFT, Primary RIGHT is the standard.

### Theme Toggle Placement

| Site | Placement |
|------|-----------|
| GitHub | Far right, after user menu |
| VS Code Docs | Far right |
| Stripe Docs | Far right |
| Discord | In settings, not navbar |

**Verdict**: Far right (after auth) or in settings dropdown.

### Utility Control Visual Weight

| Control | Expected Weight |
|---------|-----------------|
| Theme toggle | Icon-only, subtle, doesn't compete with CTAs |
| Search | Icon trigger or compact input, expandable |
| Language selector | Icon or compact dropdown |

**Verdict**: Utilities should be accessible but subordinate to primary actions.

## Output Format

When evaluating a component, produce this structured output:

```markdown
## [Component Name] Evaluation

### Current State
- **Position**: [Description]
- **Visual Weight**: [Description]
- **Spacing**: [Measurements]

### Analysis

| Dimension | Assessment | Rationale |
|-----------|------------|-----------|
| Position | [OK/CHANGE] | [Why, with reference] |
| Visual Weight | [OK/CHANGE] | [Why, with reference] |
| Spacing | [OK/CHANGE] | [Why, with reference] |

### Verdict: [CORRECT / NEEDS CHANGES]

### Recommendations (if any)
| Priority | Change | Rationale |
|----------|--------|-----------|
| P1 | [Specific change] | [Reference to principle] |
| P2 | [Specific change] | [Reference to principle] |
```

## References

See `references/` for detailed UX principles:
- `balsamiq-button-principles.md` - Button design best practices
- `nielsen-heuristics.md` - 10 usability heuristics (to be added)

## Self-Monitoring

Before finalizing evaluation:
- [ ] All 3 dimensions analyzed (Position, Visual Weight, Spacing)
- [ ] Current state documented with specifics (not vague descriptions)
- [ ] Each recommendation references an authoritative source or convention
- [ ] Compared against industry conventions (GitHub, Stripe, etc.)
- [ ] Priorities assigned (P1/P2/P3) based on UX impact
- [ ] Verdict is clear and actionable
