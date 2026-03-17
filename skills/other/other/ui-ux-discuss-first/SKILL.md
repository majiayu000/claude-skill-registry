---
name: ui-ux-discuss-first
description: Consultative UI/UX planning workflow that forces design discussion and explicit approval before implementation. Use when users ask to design, redesign, improve, or build UI and want to explore style directions, color systems, typography, and project-fit tradeoffs first. Run UI optioning with ui-ux-pro-max, then implement only after approval; use frontend-design and frontend-development as secondary skills after direction is locked.
---

# UI UX Discuss First

## Overview

Enforce a discuss-first workflow for UI work. Extract project context, present multiple style directions with tradeoffs, iterate with the user, and block implementation until explicit approval.

## Workflow

### Step 1: Build Project Context Before Asking Style Questions

1. Read `README.md` and `docs/*` if present.
2. Inspect existing frontend code for:
- Current color tokens and typography tokens.
- Existing component style language.
- Constraints from framework/design system.
3. Summarize context in 5-8 bullets before proposing any visual direction.
4. Use this summary to tailor questions; do not ask generic style questions without project grounding.

Use `references/project-discovery-questions.md` for question batches.

### Step 2: Run Discovery Dialog in Rounds

1. Ask concise batches (3-5 questions per round), not a single giant questionnaire.
2. Focus on:
- Product goal and business outcome.
- Target audience and tone.
- Brand references and anti-references.
- Color direction and contrast expectations.
- Motion density and accessibility requirements.
3. Keep asking follow-up questions until enough detail exists to produce confident options.

### Step 3: Generate Option Pack With UI Pro Max

1. Generate one baseline design system:

```bash
python .codex/skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <style_keywords>" --design-system -p "<Project Name>"
```

2. Generate supporting evidence:

```bash
python .codex/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain style
python .codex/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain color
python .codex/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain typography
python .codex/skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain ux
```

3. Present 2-4 concrete options using `references/style-option-template.md`.
4. For each option, include:
- Style name and product fit.
- Primary/secondary/background/text/CTA colors.
- Typography pairing.
- Interaction and motion profile.
- Risks, anti-patterns, and why this option may fail.

### Step 4: Discussion and Convergence (Mandatory)

1. Ask user to choose:
- Option A, B, C, or a hybrid.
2. If hybrid, restate exact merged rules (colors, typography, motion, layout).
3. Repeat until explicit approval exists.
4. Do not implement code before approval.

Use `references/approval-gate.md` to verify readiness.

### Step 5: Implement Only After Explicit Approval

1. Freeze final brief in chat:
- Chosen style direction.
- Color palette and type scale.
- Accessibility and motion constraints.
- Components/pages in scope.
2. Load `frontend-design` for visual execution quality.
3. Load `frontend-development` for code architecture/pattern compliance.
4. Implement strictly within approved scope.

## Hard Rules

1. Do not skip discussion and jump to coding.
2. Do not provide only one option unless user explicitly asks for one.
3. Do not lock colors/typography without user confirmation.
4. Do not broaden scope beyond requested pages/components.
5. Keep every recommendation tied to project context discovered in Step 1.

## Quick Trigger Examples

- "Design this landing page, but discuss style options first."
- "Help me choose visual direction before coding UI."
- "I want to explore 3 color and typography directions for this product."
- "Do not implement yet; first debate the design approach."

## References

- `references/project-discovery-questions.md`
- `references/style-option-template.md`
- `references/approval-gate.md`
