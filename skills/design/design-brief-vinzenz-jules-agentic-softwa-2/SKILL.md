---
name: design-brief
description: Creates contextual design briefs before any visual work begins. Establishes product purpose, user specificity, design principles, and anti-goals. Prevents generic "template" design by requiring specific context.
---

# Contextual Design Brief Skill

You are operating with design brief capabilities. This skill ensures that NO design work begins without a thorough understanding of context. Generic designs happen when context is missing — this skill prevents that.

## Core Philosophy

> "I think people get too focused on the different frameworks and processes, and you start to forget, what are you actually doing?" — Karri Saarinen, Linear

Design without context produces generic output. This skill forces the creation of a design brief that grounds all subsequent decisions in the specific product, users, and goals.

## When to Invoke This Skill

**ALWAYS** invoke before:
- Creating a design system
- Generating logos or brand assets
- Building UI components
- Designing layouts or wireframes
- Any visual design work

**Skip ONLY when:**
- A complete design brief already exists
- Extending an existing, well-documented design system

## Phase 1: Product Definition

Do not accept vague descriptions. Drill down to specifics:

<product_questions>
**The Basics:**
1. What is the product name?
2. What does it DO? (Specific function, not category)
3. What problem does it solve that isn't already solved?
4. What exists today that people use instead?

**The Differentiation:**
5. Why would someone choose this over alternatives?
6. What is this product's "unfair advantage"?
7. What does this product do that competitors refuse to do?

**The Constraints:**
8. What platforms must this run on?
9. What technical constraints exist?
10. What brand constraints exist (if any)?
</product_questions>

<product_definition_output>
```xml
<product_definition>
  <identity>
    <name>Product name</name>
    <tagline>One-sentence description</tagline>
    <category>Market category (for context only)</category>
  </identity>

  <function>
    <primary_action>The main thing users do with this</primary_action>
    <secondary_actions>Other things users can do</secondary_actions>
    <problem_solved>The specific pain point addressed</problem_solved>
  </function>

  <differentiation>
    <vs_competitors>
      <competitor name="competitor-name">
        <their_approach>How they solve the problem</their_approach>
        <our_difference>How we differ</our_difference>
      </competitor>
    </vs_competitors>
    <unfair_advantage>What we do that's hard to copy</unfair_advantage>
  </differentiation>

  <constraints>
    <platforms>Web, iOS, Android, Desktop, CLI, etc.</platforms>
    <technical>Performance requirements, offline needs, etc.</technical>
    <brand>Existing brand elements that must be respected</brand>
  </constraints>
</product_definition>
```
</product_definition_output>

## Phase 2: User Specificity

Generic user descriptions produce generic designs. Be ruthlessly specific:

<user_questions>
**Demographics (surface level):**
1. Job title or role?
2. Industry or domain?
3. Technical expertise level?

**Psychographics (deeper):**
4. What do they value in tools? (Speed? Power? Simplicity?)
5. What frustrates them about current solutions?
6. Are they choosing this tool, or is it chosen for them?

**Context of Use:**
7. When do they use this? (Daily driver vs. occasional)
8. Where do they use this? (Office, mobile, field)
9. How much attention can they give? (Focused vs. distracted)
10. What else are they doing while using this?

**Expertise Gradient:**
11. What does a beginner need?
12. What does a power user need?
13. How do people progress from beginner to power user?
</user_questions>

<user_definition_output>
```xml
<user_definition>
  <primary_user>
    <identity>
      <title>Specific job title or role</title>
      <domain>Industry or field</domain>
      <technical_level>novice/intermediate/expert</technical_level>
    </identity>

    <values>
      <primary_value>What they care most about</primary_value>
      <secondary_values>Other things they value</secondary_values>
      <anti_values>What they actively dislike</anti_values>
    </values>

    <context>
      <frequency>How often they use this</frequency>
      <environment>Where they use it</environment>
      <attention_level>focused/partial/distracted</attention_level>
      <concurrent_tasks>What else they're doing</concurrent_tasks>
    </context>

    <journey>
      <entry_point>How they discover/start using this</entry_point>
      <beginner_needs>What novices require</beginner_needs>
      <power_user_needs>What experts require</power_user_needs>
      <progression_path>How users level up</progression_path>
    </journey>
  </primary_user>

  <secondary_users>
    <!-- Additional user types if applicable -->
  </secondary_users>
</user_definition>
```
</user_definition_output>

## Phase 3: Design Principles

Not generic principles — principles specific to THIS product and THESE users:

<principle_guidelines>
**Good Principles:**
- "Professional to engineers" (Linear) — specific audience, specific tone
- "Simplicity, minimalism, speed" (Vercel) — specific values
- "Developer-centric" (Stripe) — specific audience

**Bad Principles:**
- "User-friendly" — too vague, applies to everything
- "Modern design" — meaningless
- "Clean and intuitive" — every product claims this

**Principle Test:**
A good principle helps you make decisions. If it doesn't rule anything out, it's not useful.
</principle_guidelines>

<principles_output>
```xml
<design_principles>
  <principle name="principle-name" priority="1">
    <statement>The principle in one sentence</statement>
    <meaning>What this actually means in practice</meaning>
    <example_decision>A design decision this would guide</example_decision>
    <rules_out>What this principle says NO to</rules_out>
  </principle>

  <principle name="principle-name" priority="2">
    <!-- ... -->
  </principle>

  <principle name="principle-name" priority="3">
    <!-- ... -->
  </principle>
</design_principles>
```
</principles_output>

## Phase 4: Emotional Targets

Define the emotional response the design should evoke:

<emotional_spectrum>
For each dimension, place where this product should land:

**Tone Spectrum:**
```
Playful ←————————————→ Serious
Casual ←————————————→ Professional
Friendly ←————————————→ Authoritative
Warm ←————————————→ Cool
```

**Energy Spectrum:**
```
Calm ←————————————→ Energetic
Minimal ←————————————→ Dense
Subtle ←————————————→ Bold
Quiet ←————————————→ Loud
```

**Complexity Spectrum:**
```
Simple ←————————————→ Powerful
Guided ←————————————→ Flexible
Opinionated ←————————————→ Customizable
```
</emotional_spectrum>

<emotional_output>
```xml
<emotional_targets>
  <should_feel>
    <emotion name="emotion-1" intensity="high/medium/low">
      <why>Why this emotion serves our users</why>
    </emotion>
  </should_feel>

  <should_never_feel>
    <emotion name="emotion-1">
      <why>Why this would be wrong for our product</why>
    </emotion>
  </should_never_feel>

  <spectrum_positions>
    <dimension name="playful-serious" position="0.8">Lean serious</dimension>
    <dimension name="casual-professional" position="0.9">Very professional</dimension>
    <!-- ... -->
  </spectrum_positions>
</emotional_targets>
```
</emotional_output>

## Phase 5: Reference Audit

Study real products — but extract principles, don't copy aesthetics:

<reference_guidelines>
**Good Reference Usage:**
- "Linear uses dark mode because their users (engineers) prefer coding environments"
- "Stripe's documentation is exemplary because developers need to scan quickly"

**Bad Reference Usage:**
- "Let's do dark mode like Linear" (copying without understanding)
- "Make it look like Stripe" (aesthetic theft)

**Reference Selection Criteria:**
- Serves similar users (not just same industry)
- Solves similar problems (not just looks nice)
- Has documented design reasoning (not just pretty)
</reference_guidelines>

<reference_output>
```xml
<reference_audit>
  <reference name="Product Name">
    <why_relevant>Why this is a good reference for us</why_relevant>
    <serves_similar_users>How their users overlap with ours</serves_similar_users>

    <principles_to_extract>
      <principle>What principle they demonstrate</principle>
      <how_they_execute>How they implement it</how_they_execute>
      <how_we_might_apply>How we could apply this (differently)</how_we_might_apply>
    </principles_to_extract>

    <what_not_to_copy>
      <element>What we should NOT copy</element>
      <why>Why it wouldn't work for us</why>
    </what_not_to_copy>
  </reference>
</reference_audit>
```
</reference_output>

## Phase 6: Anti-Goals

What this design should explicitly NOT be:

<anti_goals_guidelines>
Anti-goals prevent scope creep and maintain focus. They should be specific and sometimes controversial.

**Good Anti-Goals:**
- "Not for beginners" — accepts expertise requirement
- "Not customizable" — values opinion over flexibility
- "Not visually flashy" — substance over style

**Bad Anti-Goals:**
- "Not ugly" — too obvious
- "Not bad" — not specific
</anti_goals_guidelines>

<anti_goals_output>
```xml
<anti_goals>
  <anti_goal>
    <statement>What we explicitly will NOT do</statement>
    <why>Why this constraint helps us</why>
    <trade_off>What we're giving up (and why it's worth it)</trade_off>
  </anti_goal>
</anti_goals>
```
</anti_goals_output>

## Complete Design Brief Output

<complete_brief_format>
```xml
<design_brief>
  <metadata>
    <created>Date</created>
    <version>1.0</version>
    <author>Who created this</author>
  </metadata>

  <product_definition>
    <!-- From Phase 1 -->
  </product_definition>

  <user_definition>
    <!-- From Phase 2 -->
  </user_definition>

  <design_principles>
    <!-- From Phase 3 -->
  </design_principles>

  <emotional_targets>
    <!-- From Phase 4 -->
  </emotional_targets>

  <reference_audit>
    <!-- From Phase 5 -->
  </reference_audit>

  <anti_goals>
    <!-- From Phase 6 -->
  </anti_goals>

  <decision_framework>
    <when_in_doubt>
      When facing a design decision, ask:
      1. Does this serve [primary user]'s [primary goal]?
      2. Does this align with principle [highest priority principle]?
      3. Does this feel [target emotion]?
      4. Would [reference product] do this? Why or why not?
    </when_in_doubt>
  </decision_framework>
</design_brief>
```
</complete_brief_format>

## Validation Checklist

Before considering the brief complete:

<validation_checklist>
- [ ] Product definition is specific enough to differentiate from competitors
- [ ] User definition describes a real person, not a demographic segment
- [ ] Each design principle rules something out (not just describes good design)
- [ ] Emotional targets create a clear personality (not "professional yet friendly")
- [ ] References are analyzed for principles, not just aesthetics
- [ ] Anti-goals are genuinely controversial (someone might disagree)
- [ ] The decision framework actually helps make decisions
</validation_checklist>

## Using the Brief

Once complete, this brief should be:
1. **Referenced in every design decision** — "Per the brief, our users value X, so..."
2. **Updated when assumptions change** — Briefs are living documents
3. **Shared with all contributors** — Everyone should know the context
4. **Used in critiques** — "Does this align with principle #2?"

The brief is not bureaucracy — it's the foundation that makes intentional design possible.
