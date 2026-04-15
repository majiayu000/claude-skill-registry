---
name: color-system
description: Use when the user needs help choosing, evaluating, fixing, extending, or operationalizing colors for any interface. Trigger on requests about palettes, color grading, themes, semantic roles, contrast, tokens, visual tone, muddy or washed-out UI, dark mode, light mode, state colors, or making colors feel right. Use this skill to teach flexible color judgment and, when useful, support that judgment with small deterministic helper scripts.
argument-hint: [color problem, interface context, or palette goal]
---

color_goal = $ARGUMENTS

Design color as a living system, not a bag of swatches.

The job is to understand what the interface should feel like, what color must communicate, and how those choices survive real components, states, themes, and content. Good color work mixes judgment and measurement.

This applies to product UIs, dashboards, content-heavy interfaces, marketing surfaces, brand-led screens, and hybrids. Semantic state colors are useful when the interface truly needs them; they are not mandatory for every system.

For deeper methods, review loops, and helper-script ideas:
!references/color-method.md

## Core Orientation

**Color is relational.** No color is good on its own. Judge it by what it sits on, what it sits next to, what text it carries, and what state it represents.

**Start from the product, not from palette templates.** Infer the desired feeling, trust level, energy, clarity, and emphasis pattern from the actual task. Do not force the work into canned categories.

**Fit beats theory.** A color strategy is strong when it feels appropriate to this product, audience, and moment of use. A theoretically elegant palette that feels wrong in context is still wrong.

**Think in lightness, chroma, and hue.** Use perceptual reasoning when possible.
- lightness shapes hierarchy and legibility
- chroma shapes intensity and restraint
- hue shapes temperature, meaning, and emotional direction

**Separate taste from math.** Let the model decide the intent, relationships, and direction. Use deterministic helpers only for the parts where math is more reliable than intuition.

**Scripts are instruments, not authors.** If a script helps generate ramps, test contrast, pair foregrounds, or compare variants, use it. Do not let the script choose the design direction for you.

**Differentiate on purpose.** Sometimes the right move is to fit category expectations; sometimes it is to claim visual territory others are not using. Make that choice consciously.

**Observe in context.** A palette that looks good in a list of values but fails on buttons, badges, forms, charts, tables, or dark mode is unfinished.

**Passing contrast is necessary, not sufficient.** Accessibility checks matter, but a color system can pass contrast and still feel generic, noisy, flat, or emotionally wrong.

## What This Skill Is For

Use it for any color task, including:
- palette brainstorming
- repairing muddy, flat, loud, or incoherent color systems
- extending an existing palette without fragmenting it
- turning taste-level direction into semantic roles or tokens
- refining light and dark themes
- evaluating component states and foreground/background pairings
- deciding when to write a small helper script instead of trusting pretraining

## Working Model

Do not begin by asking "what palette category is this?" Begin by understanding the color problem.

Match depth to stage. Early exploration needs interpretation and direction more than token architecture. Later refinement may need deterministic helpers, tokens, and validation.

### 1. Read the situation

Figure out:
- what should feel quiet, stable, sharp, soft, urgent, premium, technical, warm, or neutral
- where attention should accumulate and where it should not
- whether color carries status, brand, navigation, category, selection, or all of the above
- which parts of the interface must stay readable under stress, speed, density, or poor displays
- what a 2-second first impression should communicate
- what the surrounding category or competitor set tends to do, and whether matching or differentiating serves the product better
- what already exists: brand cues, current tokens, screenshots, code, component library, user complaints

### 2. Form a color hypothesis

Describe the system before choosing values:
- what the neutral backbone should feel like
- where emphasis should live
- how far semantic colors should separate from each other
- how state changes should move: lighter, darker, duller, sharper, warmer, cooler
- how light and dark themes should relate, if both exist
- what should be avoided because it would make the interface feel generic, mismatched, noisy, or off-brand

### 3. Explore when the space is open

If the user is still searching, propose a few meaningfully different directions. Vary the emotional logic and hierarchy strategy, not just the accent hue.

For each direction, explain:
- what it feels like
- what it makes easy
- what it makes risky
- whether it fits, differentiates, or both
- what to avoid if using that direction
- where it would likely fail if pushed too far

### 4. Choose anchors and relationships

Once the direction is clear, define:
- the neutral backbone
- action/emphasis colors
- role families only when the interface truly needs them
- special colors such as selection, focus, overlays, charts, or illustrations when relevant
- how components inherit color behavior instead of improvising locally

At this stage, define relationships first. Full ramps and token tables can come later.

### 5. Use deterministic helpers where they help

For early direction work or small critiques, stay in plain-language reasoning first. Reach for scripts mainly after the anchors and behavior are clear, or when consistency, comparison, or validation at scale matters.

Write or use small helper scripts only when they reduce guesswork. Good uses include:
- generating tonal ramps from chosen anchors
- testing contrast and pairing likely foregrounds
- deriving hover, active, disabled, or selected variants
- checking collision between primary, info, success, and selected states
- comparing alternate variants side by side
- auditing an existing codebase for hardcoded or drifting colors
- attaching usage metadata to formalized tokens or roles, such as intended use, avoid cases, contrast requirements, and likely component bindings

Bad use: giving the script full authority over the color direction.

### 6. Observe the result in real UI context

Start with a first-impression pass before the detailed audit.

Ask:
- what draws the eye first
- what emotional tone lands in the first few seconds
- whether that matches the product intent

Review the system on actual surfaces and with realistic content:
- primary surfaces and text blocks
- buttons, links, and focus treatment
- inputs, validation, alerts, and badges
- tables, cards, navigation, and selected states
- charts and annotations when relevant
- light theme, dark theme, or both

### 7. Iterate intelligently

When something feels wrong, diagnose the class of failure before changing colors blindly.

Typical causes include:
- weak lightness structure
- too much chroma everywhere
- semantic collisions
- accent overuse
- dark-theme over-saturation
- components bypassing the intended system

Fix the root pattern, not only the most visible symptom.

## Heuristics

- Most palette failures are structure failures before they are hue failures.
- Neutrals usually do more product work than accents.
- Emphasis becomes stronger when it is rare and deliberate.
- Brand color is not automatically the right choice for backgrounds, borders, or semantic states.
- Consistency compounds over time; a simpler system that can be applied faithfully often outperforms a clever but fragile one.
- State changes should usually move first by lightness and chroma before making dramatic hue jumps.
- Gradients, glows, and tinted shadows are part of the color system if they materially affect perception.
- Tokens are useful when the interface needs a shared language, but token naming should follow meaning, not appearance.
- If the output starts looking like a generic agent palette, stop and restate the intended feeling in plain language.

## Output

Produce the smallest useful artifact for the moment.

Possible outputs include:
- a short color critique with root-cause diagnosis
- a first-impression read plus deeper color diagnosis
- 2-4 distinct directions with tradeoffs
- a palette brief describing anchors and relationships
- semantic roles or token recommendations
- a helper script plan for deterministic ramp generation or validation
- a migration plan for repairing an existing system

When structure helps, include:
- the intended feeling
- the core color relationships
- what should remain neutral
- where emphasis should live
- what the helper script should compute versus what should stay human/LLM-directed

If editing an existing system, prefer changing shared color logic before adding one-off exceptions.

If context is thin, inspect what exists first and ask at most one targeted question only when the answer would materially change the direction.
