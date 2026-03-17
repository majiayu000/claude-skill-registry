---
name: design-vision
description: Transform design inspiration into implemented code through deep analysis, interactive vision discovery, planning, and checkpoint-based execution. Use when you have a screenshot/reference and want to build something similar while understanding and preserving the design intent.
---

# Design Vision

Transform design inspiration into implemented code by deeply understanding both the visual and your intent.

## The Problem This Solves

Traditional approach:
- Look at screenshot → Extract colors/fonts → Implement → Lose the original "feel"

This skill:
- Analyze screenshot deeply → Understand YOUR intent → Plan with vision → Implement with checkpoints → Verify against original

## Workflow Phases

### Phase 1: Deep Visual Analysis (Silent)

**Input:** Screenshot path, URL, or image file

**Process:**
1. Use `ai-multimodal` skill to analyze the image deeply
2. Extract ALL visual elements:
   - Color palette (primary, secondary, accent, neutrals) with hex codes
   - Typography (font families, sizes, weights, line heights)
   - Spacing system (margins, padding patterns)
   - Layout structure (grid, flex patterns, breakpoints)
   - Component patterns (cards, buttons, forms, navigation)
   - Visual effects (shadows, borders, gradients, blur)
   - Micro-interactions implied by the design
3. Interpret the design:
   - Design style classification (Minimalism, Glassmorphism, Neo-brutalism, etc.)
   - Emotional tone (calm, energetic, professional, playful)
   - What principles make this design effective
   - What creates the "feel" of the design

**Output:** Internal analysis object (NOT shown to user yet - used to inform questions)

### Phase 2: Vision Discovery (Interactive)

**Purpose:** Understand what the USER wants, not just what's visible

**Process:**
1. Generate contextual questions BASED on Phase 1 analysis
2. Use `AskUserQuestion` to gather intent

**Smart Questions (informed by analysis):**

Context questions:
- "What are you building? (app type, purpose, audience)"
- "What drew you to this design? What specifically appeals to you?"

Analysis-informed questions (examples):
- If analysis found heavy whitespace: "This design uses generous spacing for a calm feel - is that breathing room important, or are you more interested in the layout structure?"
- If analysis found muted colors: "The color palette is quite subdued - do you want similar tones, or different energy?"
- If analysis found complex animations: "This appears to have sophisticated animations - how important is motion to your project?"
- If analysis found specific typography: "The typography uses [detected font] which creates [effect] - do you want to match this, or have different type preferences?"

Adaptation questions:
- "What should feel DIFFERENT from this reference?"
- "Any constraints? (tech stack, existing design system, accessibility requirements)"

**Output:** User intent data

### Phase 3: Vision Synthesis

**Purpose:** Create a source-of-truth document for all subsequent work

**Process:**
1. Combine analysis + user answers into Vision Document
2. Categorize elements:
   - **KEEP**: Elements to preserve exactly as in reference
   - **ADAPT**: Elements to modify for user's context
   - **IGNORE**: Elements not relevant to user's needs
3. Define goals:
   - Emotional goals (how it should feel)
   - Functional goals (what it needs to do)
   - Constraints (tech, accessibility, etc.)

**Present to user for confirmation:**
```markdown
## Vision Summary

**Building:** [what they're building]
**Inspired by:** [reference description]
**Target feel:** [emotional goals]

### Keep from reference:
- [element 1]
- [element 2]

### Adapt for your context:
- [element 1] → [how to adapt]

### Your additions:
- [requirements not in reference]

Does this capture your vision?
```

**Use `AskUserQuestion`:**
- header: "Vision"
- options:
  - "Yes, this is right" - Proceed to planning
  - "Needs adjustment" - Let me clarify
  - "Start over" - Re-do discovery

**Output:** Approved Vision Document

### Phase 4: Planning

**Purpose:** Convert vision into concrete implementation plan

**Process:**
1. Invoke `writing-plans` skill OR use `EnterPlanMode`
2. Plan should include:
   - Component breakdown (what to build)
   - Implementation order (dependencies)
   - File structure
   - Technical decisions (libraries, patterns)
   - Checkpoints for vision verification

**Present plan for approval before any code**

**Output:** Approved implementation plan

### Phase 5: Implementation with Checkpoints

**Purpose:** Build while staying true to the vision

**Process:**
1. Invoke `executing-plans` skill with vision context
2. Implement in stages:
   - **Stage 1: Structure** - Layout, routing, basic components
   - **Stage 2: Core UI** - Main components with styling
   - **Stage 3: Details** - Typography, colors, spacing refinement
   - **Stage 4: Polish** - Micro-interactions, animations, edge cases

3. At each stage checkpoint, ask:
   ```
   Stage [N] complete. Here's what I built: [summary]

   Comparing to your vision:
   - [what matches]
   - [what might differ]

   Should I continue, adjust, or show you the current state?
   ```

**Output:** Implemented code

### Phase 6: Vision Verification

**Purpose:** Ensure final result matches original intent

**Process:**
1. Use `ai-multimodal` to compare:
   - Original reference screenshot
   - Current implementation (via `chrome-devtools` screenshot)
2. Evaluate alignment with Vision Document
3. Present comparison to user:
   ```
   ## Vision Check

   **Original reference:** [key characteristics]
   **Your implementation:** [how it compares]
   **Vision alignment:** [what matches, what differs]

   Are you satisfied, or should we refine?
   ```

**Output:** User approval or refinement requests

## Modes

| Mode | Phases | When to Use |
|------|--------|-------------|
| `full` | All 6 phases | Complete design-to-code with maximum alignment |
| `quick` | 1, 2 (brief), 4, 5 | Faster, fewer questions, still vision-aware |
| `analyze-only` | 1, 2, 3 | Just create vision document, no implementation |
| `implement` | 4, 5, 6 | Already have vision, just need to build |

**To specify mode:** User can say "quick mode" or skill can ask:
```
How thorough should the vision discovery be?
- Full (deep analysis, multiple questions, checkpoints)
- Quick (brief questions, faster to code)
- Analyze only (just create vision doc)
```

## Skills Integration

This skill orchestrates:

| Phase | Skills Used |
|-------|-------------|
| Analysis | `ai-multimodal` |
| Discovery | `AskUserQuestion` tool, `brainstorming` patterns |
| Synthesis | `AskUserQuestion` tool |
| Planning | `writing-plans` or `EnterPlanMode` |
| Implementation | `executing-plans`, `frontend-design`, `aesthetic` |
| Verification | `ai-multimodal`, `chrome-devtools` |

## Context Persistence

Maintain throughout execution:
```
vision_context = {
  original_reference: [image path/description],
  analysis: [Phase 1 output],
  user_intent: [Phase 2 answers],
  vision_document: [Phase 3 output],
  plan: [Phase 4 output],
  checkpoints: [Phase 5 progress],
  current_stage: [where we are]
}
```

Pass this context to each skill invocation so they all work toward the same vision.

## Example Flow

**User:** "Build me a dashboard like this" [attaches screenshot]

**Phase 1:** [Silent analysis extracts: dark theme, glassmorphism cards, SF Pro font, purple accent, lots of data visualization, sidebar nav]

**Phase 2:**
- "What kind of dashboard is this for?" → "Analytics for my SaaS"
- "I notice the glassmorphism card style - is that frosted glass effect important to you?" → "Yes, love that"
- "The dark theme with purple accents - keep those colors or different?" → "Keep dark, but blue instead of purple"
- "What should feel different from this?" → "Less cluttered, I have fewer metrics"

**Phase 3:**
```
Vision Summary:
Building: SaaS analytics dashboard
Keep: Dark theme, glassmorphism cards, sidebar nav
Adapt: Purple → Blue accents, fewer metrics (cleaner)
Goals: Professional, modern, easy to scan
```

**Phase 4:** [Plan: 5 components, start with layout, then cards, then charts...]

**Phase 5:** [Build with checkpoints at each stage]

**Phase 6:** [Compare final to original, verify vision alignment]

## Rules

1. **Never skip vision discovery** - Even in quick mode, ask at least 2 contextual questions
2. **Analysis informs questions** - Don't ask generic questions; make them specific to what was detected
3. **Vision document is source of truth** - Reference it throughout implementation
4. **Checkpoints prevent drift** - Verify alignment before moving to next stage
5. **User can always adjust** - Provide modification options at every phase
6. **Pass context forward** - Every skill invocation should know the full vision context
