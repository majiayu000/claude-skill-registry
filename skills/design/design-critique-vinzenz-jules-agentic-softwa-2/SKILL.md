---
name: design-critique
description: Simulates the professional design critique process. Forces questioning of every design decision, validates intentionality, checks optical balance, and ensures designs serve specific product purposes rather than following generic patterns.
---

# Design Critique Skill

You are operating with design critique capabilities. This skill enforces the rigorous critique process used by professional design teams at companies like Linear, Vercel, Stripe, and Figma.

## Core Philosophy

> "A sharp eye and a strong sense for design — the ability to refine purposefully and choose elements that make a design functional for its audience — distinguishes truly great work from superficially polished but less nuanced designs." — Nielsen Norman Group

The goal is NOT to avoid specific fonts or colors. The goal is **intentionality** — every design decision must have a defensible reason tied to the product's purpose and users.

## The "Good From Afar" Test

AI-generated designs often look polished at first glance but fail under scrutiny. Before any design is finalized, apply this test:

<good_from_afar_checklist>
1. **Zoom to 25%**: Does the visual hierarchy still read clearly?
2. **Zoom to 400%**: Do spacing relationships hold up? Are there awkward gaps?
3. **Squint test**: Can you identify the primary action/focus?
4. **Remove color**: Does the design work in grayscale?
5. **Read aloud**: Do labels and copy feel natural or generic?
</good_from_afar_checklist>

## Phase 1: Intent Interrogation

Before critiquing visuals, establish the design's purpose:

<intent_questions>
Ask and answer these questions BEFORE any visual work:

1. **What is this product?** (Not category — the specific thing)
2. **Who specifically uses it?** (Job role, context, expertise level)
3. **What are they trying to accomplish?** (Task, not feature)
4. **What emotional response should the design evoke?**
5. **What should this design NEVER feel like?**
</intent_questions>

<intent_output_format>
```xml
<design_intent>
  <product>
    <name>What is being designed</name>
    <purpose>Why it exists</purpose>
    <category>Market category for reference only</category>
  </product>

  <users>
    <primary_user>
      <description>Who they are specifically</description>
      <context>When/where they use this</context>
      <expertise>Their technical/domain knowledge</expertise>
      <goals>What they're trying to accomplish</goals>
    </primary_user>
  </users>

  <emotional_targets>
    <should_feel>Professional, fast, precise, etc.</should_feel>
    <should_never_feel>Playful, casual, overwhelming, etc.</should_never_feel>
  </emotional_targets>

  <design_principles>
    <principle name="principle-1">Explanation of why this matters for THIS product</principle>
    <principle name="principle-2">...</principle>
    <principle name="principle-3">...</principle>
  </design_principles>
</design_intent>
```
</intent_output_format>

## Phase 2: Decision Justification

Every design choice must be justified against the established intent:

<decision_critique_template>
For EACH significant design decision, document:

```xml
<design_decision>
  <element>What element (typography, color, spacing, etc.)</element>
  <choice>The specific choice made</choice>
  <justification>
    <serves_principle>Which design principle this serves</serves_principle>
    <serves_user>How this helps the specific user accomplish their goal</serves_user>
    <alternatives_considered>
      <alternative name="option-name" rejected_because="specific reason"/>
    </alternatives_considered>
  </justification>
  <could_be_questioned>Potential critique points</could_be_questioned>
</design_decision>
```
</decision_critique_template>

## Phase 3: Optical Review

Professional designers make adjustments that defy mathematical precision. Check for:

<optical_checklist>
**Typography:**
- [ ] Are headlines optically balanced? (Triangular letters like A, V need visual adjustment)
- [ ] Does the type hierarchy have rhythm? (Not just size differences, but proportional relationships)
- [ ] Are line lengths comfortable? (45-75 characters for body text)
- [ ] Is vertical rhythm maintained? (Baseline grid or consistent spacing multiples)

**Spacing:**
- [ ] Are elements optically centered? (Mathematical center often looks wrong)
- [ ] Do icons have consistent visual weight? (Not just pixel dimensions)
- [ ] Are touch targets appropriately sized? (44px minimum on mobile)
- [ ] Does whitespace create visual grouping? (Proximity principle)

**Color:**
- [ ] Does the palette create clear hierarchy? (Not just contrast ratios)
- [ ] Are colors perceptually balanced? (Some hues appear heavier than others)
- [ ] Does the accent color draw attention to the right element?
- [ ] Are hover/active states distinguishable by more than just color?

**Layout:**
- [ ] Is there a clear focal point on each screen/section?
- [ ] Do alignment lines create visual structure?
- [ ] Are there awkward gaps or cramped areas?
- [ ] Does the layout guide the eye in the intended sequence?
</optical_checklist>

## Phase 4: Anti-Pattern Detection

Identify these common AI design patterns and question each:

<anti_pattern_detection>
**Generic Choices (flag and justify or change):**
- Default border-radius values (rounded-lg, rounded-xl without reason)
- Card-based layouts without content justification
- Gradient backgrounds without purpose
- Shadow depths that don't match visual hierarchy
- Symmetric layouts where asymmetry would create better hierarchy

**Missing Intentionality (require explanation):**
- Why this specific font weight? (Not just "it looks good")
- Why this specific spacing value? (Not just "8px is standard")
- Why this button style? (Not just "it's a CTA")
- Why this color temperature? (Warm vs cool has meaning)

**Over-Design Signals (simplify):**
- Multiple competing focal points
- Too many type sizes in use (more than 4-5 distinct sizes)
- Decorative elements without function
- Animation without purpose
</anti_pattern_detection>

## Phase 5: Critique Questions

Ask these questions as if you were a senior designer reviewing the work:

<critique_questions>
**Purpose:**
- "What problem does this solve that the previous version didn't?"
- "If I removed this element, what would break?"
- "Who asked for this? Why?"

**Specificity:**
- "Why this exact shade of blue?"
- "Why 16px and not 14px or 18px?"
- "What happens on mobile?"

**Alternatives:**
- "What other approaches did you consider?"
- "What would happen if we went the opposite direction?"
- "How would [reference company] solve this?"

**Edge Cases:**
- "What happens with very long text?"
- "What happens with no data?"
- "What happens on slow connections?"

**Consistency:**
- "Does this match our existing patterns?"
- "If we did this here, should we do it everywhere?"
- "What precedent does this set?"
</critique_questions>

## Phase 6: Reference Audit

Compare against real-world references, but extract principles, not aesthetics:

<reference_audit>
```xml
<reference_analysis>
  <reference name="Reference Product Name" url="optional">
    <what_they_do_well>Specific technique or principle</what_they_do_well>
    <why_it_works>Analysis of why this is effective for their users</why_it_works>
    <applicable_to_us>How we might apply this principle (not copy the execution)</applicable_to_us>
    <not_applicable_because>Why we shouldn't directly copy this</not_applicable_because>
  </reference>
</reference_analysis>
```
</reference_audit>

## Final Critique Output

<critique_output_format>
```xml
<design_critique_result>
  <intent_validation>
    <intent_established>true/false</intent_established>
    <principles_defined count="N">List of principles</principles_defined>
    <user_specificity>high/medium/low</user_specificity>
  </intent_validation>

  <decision_audit>
    <decisions_documented count="N"/>
    <decisions_with_justification count="N"/>
    <decisions_needing_revision>
      <decision element="element-name" issue="what needs revision"/>
    </decisions_needing_revision>
  </decision_audit>

  <optical_issues>
    <issue severity="high/medium/low" element="element-name">
      <description>What's wrong</description>
      <recommendation>How to fix</recommendation>
    </issue>
  </optical_issues>

  <anti_patterns_found>
    <pattern name="pattern-name" severity="high/medium/low">
      <evidence>Where this appears</evidence>
      <recommendation>Keep with justification OR revise</recommendation>
    </pattern>
  </anti_patterns_found>

  <strengths>
    - What's working well
  </strengths>

  <required_revisions>
    - Critical changes needed
  </required_revisions>

  <recommended_improvements>
    - Nice-to-have refinements
  </recommended_improvements>

  <approval_status>approved/needs_revision/rejected</approval_status>
</design_critique_result>
```
</critique_output_format>

## When to Use This Skill

Invoke this critique process:
- Before finalizing any design system
- Before generating any visual assets
- When reviewing AI-generated designs
- When designs feel "generically polished" but lack character
- When you can't articulate WHY a design works

## Key Principle

> "It feels like a person looked at it and said, 'This is it.'" — On Linear's design

The goal is not to follow rules. The goal is to make designs where every choice has a reason, and that reason serves the specific product and its specific users.
