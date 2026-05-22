---
name: define-design-guidelines
description: 'Create a DESIGN_GUIDELINES.md that defines how to design UI/UX for your customer. Requires CUSTOMER.md to exist first. Covers aesthetic direction, design tokens, typography, color, motion, components, and layout patterns. Bakes in frontend-design skill principles to avoid generic AI aesthetics.'
---

# Design Guidelines Skill

Create the DESIGN_GUIDELINES.md document that defines HOW to design interfaces for your customer. This document drives all UI/UX: components, layouts, animations, colors, typography—everything visual.

> **Prerequisite**: CUSTOMER.md must exist. Design without customer definition is just aesthetic preference. The interface must resonate with WHO you're building for.

## Overview

This skill supports both **creating new design guidelines** and **refining existing ones**.

This skill guides you through:
0. **Prerequisite Check** - Verify CUSTOMER.md exists; stop if not
1. **Deep Analysis** - Launch design-research agent to understand ideal design for the customer
2. **Discovery** - Confirm/refine design direction with targeted questions
3. **Generate Document** - Create DESIGN_GUIDELINES.md with full design system
4. **Automatic Alignment Audit** - Opus agent verifies alignment with CUSTOMER.md/BRAND_GUIDELINES.md, fixes issues, repeats until perfect
5. **Finalization** - Add version history once audit passes

## Core Philosophy: Anti-AI-Slop

**CRITICAL**: This skill bakes in the frontend-design skill's principles. Every design guideline must avoid generic AI aesthetics:

### What to AVOID (AI Slop)
- **Generic fonts**: Inter, Roboto, Arial, system fonts, Space Grotesk
- **Cliché colors**: Purple gradients on white, generic blue CTAs, safe gray palettes
- **Predictable layouts**: Cookie-cutter grids, template-looking compositions
- **Safe choices**: Border-radius everywhere, subtle animations, inoffensive everything
- **Generic components**: Bootstrap/MUI defaults without personality

### What to EMBRACE
- **Bold aesthetic commitment**: Pick an extreme and execute with precision
- **Distinctive typography**: Characterful fonts that match the product personality
- **Intentional color**: Dominant colors with sharp accents, not timid even distribution
- **Spatial creativity**: Asymmetry, overlap, diagonal flow, grid-breaking elements
- **Atmospheric details**: Textures, gradients, shadows, effects that create depth

**The test**: Would someone mistake this for a generic template? If yes, it's wrong.

## Workflow

### Phase 0: Prerequisite Check

**CRITICAL**: Before anything else, check for CUSTOMER.md:

1. Use Glob to search for `**/CUSTOMER.md` in the current directory
2. **If NOT found**: Stop immediately and inform the user:

```
"I can't create design guidelines without knowing WHO you're designing for.

Please create your CUSTOMER.md first using /define-customer.

Design without customer definition is just aesthetic preference—it won't resonate with anyone specific."
```

Do NOT proceed. End the workflow here.

3. **If found**: Read the CUSTOMER.md and extract key context:
   - ICP definition (who they are)
   - What they value (speed? precision? fun? simplicity?)
   - Behavioral traits (patient? impatient? technical? casual?)
   - Anti-personas (who they're NOT)
   - Any visual/experience hints

**IMPORTANT - Pre-fill Recommendations**: Use CUSTOMER.md to infer recommended options for all questions:

| If CUSTOMER.md says... | Recommend... |
|------------------------|--------------|
| ICP values "speed", "efficiency", "no patience" | Terminal/utilitarian aesthetic, fast animations, dense UI |
| ICP is technical (developers, engineers) | Monospace typography, dark theme, information-dense |
| ICP values "data", "statistics", "precision" | Data terminal aesthetic, clinical colors, sharp geometry |
| ICP is "fun-seekers", "casual players", "beginners" | Playful/soft aesthetic, rounded corners, inviting colors |
| ICP is "professionals", "executives" | Refined/luxury aesthetic, premium typography, restrained palette |
| ICP values "creativity", "expression" | Bold/maximalist aesthetic, unexpected layouts, strong personality |
| Anti-persona is "corporate" or "enterprise" | Avoid generic SaaS look, embrace distinctive character |

The goal: **User should be able to accept all recommended defaults** and get a design system that resonates with their ICP.

Then check for existing DESIGN_GUIDELINES.md:

```
header: "Existing Design Guidelines Found"
question: "I found existing DESIGN_GUIDELINES.md. What would you like to do?"
options:
  - "Refine it - update based on new insights"
  - "Start fresh - create new design guidelines"
  - "Review it - just read through what's there"
```

### Phase 1: Deep Analysis

**BEFORE asking any questions**, launch the `design-research` agent to deeply analyze the customer profile and determine the ideal design direction.

**Launch the Design Research Agent:**

```
Launch Task agent (subagent_type: design-research) with prompt:

"Analyze the customer profile to determine ideal UI/UX design direction.

CUSTOMER.md path: [path found in Phase 0]

Provide your full design analysis covering:
1. Customer Design Psychology
2. Recommended Aesthetic Direction
3. Typography Recommendation
4. Color Direction
5. Geometry & Motion
6. Signature Elements
7. Anti-Patterns for This ICP
8. Design Reference Products

Be specific and decisive. This analysis will inform the entire design system."
```

The agent will:
1. Read CUSTOMER.md and BRAND_GUIDELINES.md (if exists)
2. Research industry design patterns and competitors
3. Provide comprehensive design analysis with specific recommendations

**After agent completes**, extract the analysis and use it to:
1. Pre-fill ALL question recommendations with high confidence
2. Present a summary to the user before discovery questions

**Present Analysis Summary:**

```
header: "Design Analysis"
question: "Based on your customer profile, here's my recommended design direction. Does this feel right?"
[Display: Aesthetic direction, typography, theme, key signature elements]
options:
  - "Yes - this direction feels right, let's refine details (Recommended)"
  - "Mostly - good direction but some things feel off"
  - "No - I have a different vision"
```

If "Yes" or "Mostly", proceed to Phase 2 with agent recommendations as defaults.
If "No", ask what's different and adjust recommendations.

### Phase 2: Discovery

Use AskUserQuestion for all questions. **Put the recommended option FIRST** with "(Recommended)" suffix. **Use the opus agent's analysis to inform ALL recommendations.**

**Question 1: Aesthetic Direction**

This is the most important question. The entire design system flows from this choice.

**Use the opus agent's recommendation as the default.** The agent has already analyzed CUSTOMER.md deeply.

```
header: "Aesthetic Direction"
question: "What aesthetic direction fits your product and customer?"
options:
  - "[Inferred from CUSTOMER.md] (Recommended)"
  - "Data terminal - clinical, sharp, information-dense (Bloomberg, trading apps)"
  - "Brutally minimal - stark, essential, no decoration"
  - "Industrial utilitarian - functional, raw, tool-like"
  - "Luxury/refined - premium, elegant, restrained"
  - "Editorial/magazine - typographic, editorial, sophisticated"
  - "Brutalist/raw - bold, unapologetic, confrontational"
  - "Retro-futuristic - nostalgic tech, synthwave, neon"
  - "Playful/toy-like - fun, colorful, delightful"
  - "Soft/pastel - gentle, approachable, calming"
  - "Art deco/geometric - structured, ornamental, patterns"
  - "Organic/natural - flowing, earthy, warm"
```

**Question 2: Theme Preference**

**Use the opus agent's color direction analysis.**

```
header: "Theme"
question: "What's your primary theme?"
options:
  - "[Inferred] (Recommended)"
  - "Dark theme - dark backgrounds, light text (more distinctive)"
  - "Light theme - light backgrounds, dark text (more accessible)"
  - "Both - design for both with theme switching"
```

**Question 3: Typography Character**

**Use the opus agent's typography recommendation.**

```
header: "Typography"
question: "What typographic character fits your brand?"
options:
  - "[Inferred] (Recommended)"
  - "Monospace-forward - technical, precise, data-focused (JetBrains Mono, Fira Code)"
  - "Elegant serif - premium, editorial, sophisticated (Playfair, Cormorant)"
  - "Bold geometric - strong, modern, impactful (Clash Display, Satoshi)"
  - "Rounded/friendly - approachable, soft, inviting (Nunito, Quicksand)"
  - "Editorial mix - display headlines with refined body (custom pairing)"
  - "Clean sans - neutral but NOT generic (Geist, DM Sans - not Inter/Roboto)"
```

**Question 4: Geometry & Shape**

**Use the opus agent's geometry & motion analysis.**

```
header: "Geometry"
question: "What geometric character defines your UI?"
options:
  - "[Inferred] (Recommended)"
  - "Sharp zero-radius - all corners sharp, no exceptions (precision, clinical)"
  - "Minimal/subtle - small radius (4-6px) for polish without softness"
  - "Rounded/soft - generous radius (8-16px) for friendliness"
  - "Pill shapes - fully rounded buttons/badges for playfulness"
  - "Mixed - sharp containers, rounded interactive elements"
```

**Question 5: Information Density**

**Use the opus agent's analysis of ICP technical level and patience.**

```
header: "Density"
question: "How dense should information be?"
options:
  - "[Inferred] (Recommended)"
  - "Dense - information-rich, minimal whitespace (power users)"
  - "Balanced - comfortable density with clear hierarchy"
  - "Spacious - generous whitespace, breathing room"
  - "Editorial - dramatic spacing, statement pieces"
```

**Question 6: Motion Philosophy**

**Use the opus agent's motion philosophy recommendation.**

```
header: "Motion"
question: "What's your animation philosophy?"
options:
  - "[Inferred] (Recommended)"
  - "Instant - <100ms, no unnecessary animation (respects time)"
  - "Functional - fast, purposeful, feedback-focused"
  - "Subtle - refined micro-interactions, polished feel"
  - "Delightful - playful animations, personality-forward"
  - "Dramatic - bold transitions, statement animations"
```

**Question 7: Primary Color Direction**

```
header: "Primary Color"
question: "What color family anchors your palette?"
options:
  - "[Inferred if clear signal] (Recommended)"
  - "Orange/amber - energy, action, warmth"
  - "Blue - trust, calm, professional"
  - "Green - growth, success, nature"
  - "Purple - creativity, premium, unique"
  - "Red/coral - bold, urgent, passionate"
  - "Teal/cyan - modern, tech, fresh"
  - "Neutral - black/white/gray dominant, accent secondary"
  - "Custom - I have specific brand colors"
```

**Question 7b: Brand Colors (If "Custom" selected)**

```
header: "Brand Colors"
question: "What are your brand colors?"
freeText: true
placeholder: "e.g., 'Primary: #F97316 (orange), Secondary: #3B82F6 (blue), Background: #0A0A0B'"
```

**Question 8: Technical Constraints**

```
header: "Tech Stack"
question: "What's your frontend tech stack?"
options:
  - "React + Tailwind (Recommended - most flexible)"
  - "React + CSS-in-JS (styled-components, emotion)"
  - "React + CSS Modules"
  - "Vue + Tailwind"
  - "Vanilla HTML/CSS/JS"
  - "Other framework"
multiSelect: false
```

**Question 9: Signature Elements**

```
header: "Signature"
question: "What should be immediately recognizable about your UI? (Select 2-3)"
options:
  - "[Inferred from aesthetic] (Recommended)"
  - "Zero border-radius everywhere"
  - "Monospace typography for data"
  - "Single dominant accent color"
  - "Heavy use of negative space"
  - "Custom cursor or micro-interactions"
  - "Unique loading states"
  - "Distinctive iconography"
  - "Gradient treatments"
  - "Texture or grain overlays"
  - "Bold asymmetric layouts"
multiSelect: true
```

**Question 10: Product Context** (Free text)

```
header: "Product Context"
question: "Describe your product briefly - what does it do and what's the primary interface?"
freeText: true
placeholder: "e.g., 'Chess analysis tool - main screen shows a chess board with win percentage overlay. Data-heavy stats pages.'"
```

**Question 11: References** (Optional, free text)

```
header: "References"
question: "Any products or websites whose design you admire? (Optional)"
freeText: true
placeholder: "e.g., 'Linear's clean interface, Stripe's documentation, Notion's typography'"
```

**Question 12+: Gap-Filling**

After core questions, verify you have clarity on:
- Aesthetic direction (specific, not vague)
- Typography approach
- Color palette direction
- Geometry decisions
- Motion philosophy
- Signature elements

Keep asking until confident enough to generate a distinctive design system.

### Phase 3: Generate Document

Based on the design-research agent's analysis and user's confirmed preferences, generate `DESIGN_GUIDELINES.md`.

The document should include:

1. **Identity** - User, problem, aesthetic direction, "We Are / We Are NOT", signature elements, core principles
2. **Design Tokens** - Colors (surfaces, text, accent, status, borders), typography (fonts, sizes, weights), spacing, geometry, shadows, animation timings, breakpoints
3. **Voice & Copy** - UI tone, bad/good examples, state copy
4. **Components** - Cards, buttons, inputs, toasts with specific specs
5. **Layout Patterns** - Primary layout philosophy, visual hierarchy
6. **Motion** - Philosophy, orchestrated reveals, loading states
7. **Anti-Patterns** - AI slop to avoid, brand violations, customer-ignoring mistakes
8. **Ship Checklist** - Pre-ship verification items

**Incorporate the design-research agent's full analysis** into the document—especially the anti-patterns, signature elements, and reference products.

Write `DESIGN_GUIDELINES.md` to the current working directory.

### Phase 4: Automatic Alignment Audit

After generating the document, **automatically** audit it against CUSTOMER.md and BRAND_GUIDELINES.md to ensure perfect alignment. This is NOT optional—run at least one audit cycle.

**Launch the Design Quality Auditor Agent:**

```
Launch Task agent (subagent_type: design-quality-auditor) with prompt:

"Audit DESIGN_GUIDELINES.md for alignment with customer profile and brand guidelines.

Document paths:
- DESIGN_GUIDELINES.md: [path]
- CUSTOMER.md: [path]
- BRAND_GUIDELINES.md: [path] (if exists)

Perform your full audit protocol and report results."
```

The agent will:
1. Read all three documents
2. Check customer alignment, brand alignment, internal consistency, completeness
3. Report `✅ AUDIT PASSED` or `⚠️ ISSUES FOUND` with specific fixes

**After audit completes:**

1. **If AUDIT PASSED**: Proceed to finalization
2. **If ISSUES FOUND**:
   - Apply all suggested fixes to DESIGN_GUIDELINES.md
   - Run the audit again
   - Repeat until AUDIT PASSED (max 3 cycles to prevent infinite loops)

**Example audit issue and fix:**
```
ISSUE: Customer Alignment - ICP values "zero patience" but motion philosophy
specifies 300ms animations which feels slow for this audience.
FIX: Change base animation duration to 100ms, reserve 300ms only for
celebratory moments like score reveals.
```

### Phase 5: Finalization

Once audit passes, add version history:

```markdown
---

## Version History

- **v1.0** - [Date] - Initial creation (audit passed)

## Usage

Reference this document for ALL UI work. The test: Would your ICP feel this UI was made for them?
```

## Key Principles

### Grounded in Customer
- Every design choice should resonate with the ICP
- Reference CUSTOMER.md values when making decisions
- If the ICP values speed, the UI must be fast
- If the ICP is technical, the UI can be dense

### Anti-AI-Slop is Non-Negotiable
- Every design system must be distinctive
- Generic choices are wrong by default
- If it looks like a template, it fails
- Bold commitment beats safe mediocrity

### Actionable Over Abstract
- Don't just say "be bold" - specify the border-radius
- Every guideline needs exact values
- Ship checklist catches drift

### Aesthetic Coherence
- All tokens must serve the chosen direction
- Typography, color, motion, geometry align
- Signature elements appear consistently
- Deviations are intentional, not accidental

### Reduce Cognitive Load
- ALWAYS use AskUserQuestion tool when available
- **Put recommended option FIRST** with "(Recommended)" suffix
- **Pre-fill recommendations from agent analysis** - user should be able to accept defaults
- Present multi-choice questions to minimize typing

## Output Location

Write `DESIGN_GUIDELINES.md` to the current working directory (or user-specified path).
