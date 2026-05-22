---
name: brand-identity
description: Provides the single source of truth for brand guidelines, design tokens, technology choices, and voice/tone. Use this skill whenever generating UI components, styling applications, writing copy, or creating user-facing assets to ensure brand consistency.
---

# Brand Identity System

## When to use this skill
- When starting a new project.
- When the user asks to "make it look like [Brand X]".
- When a UI component needs specific colors/fonts.
- When writing copy, to ensure the correct "Voice".

## Workflow
1.  **Extraction**: Ask the user for their brand attributes (or analyze existing files).
    - *Visuals*: Colors, Typography, Spacing, Radius.
    - *Voice*: Tone, Persona, Vocabulary constraints.
    - *Tech Constraints*: Accessibility Level (WCAG), Framework preferences.
2.  **Definition**: Create a single source of truth.
    - `docs/BRAND_GUIDELINES.md`: The high-level rules.
    - `src/theme/design-tokens.ts`: The code implementation (Tailwind config, CSS Variables).
3.  **Application**: Instruct `designing-ui` to use these tokens.

## Instructions

### 1. The Brand DNA (Template)
Create or update `docs/BRAND_GUIDELINES.md`:

```markdown
# Brand: [Name]

## 1. Visual Identity
- **Primary Color**: Neo-Mint (`#00FCA8`) - Used for CTAs.
- **Background**: Deep Space (`#0B0C15`).
- **Typography**: 
    - Headers: 'Space Grotesk' (Bold, Uppercase).
    - Body: 'Inter' (Clean, readable).
- **Radius**: `0px` (Sharp, Brutalist).
- **Icons**: Lucide React (Stroke width 1.5).

## 2. Voice & Tone
- **Persona**: The "Rebel Techie".
- **Do's**: Use punchy sentences. Emojis allowed (🚀).
- **Don'ts**: No corporate jargon ("synergy"). "User" -> "Hacker".

## 3. Tech & Accessibility
- **Stack**: Next.js + Tailwind + Framer Motion.
- **Accessibility**: strict WCAG AA compliance.
- **Dark Mode**: Forced Dark Mode (no light switch).
```

### 2. Tech Stack Alignment
- Ensure the chosen `designing-ui` library supports these tokens.
    - *Tailwind*: Generate `tailwind.config.js` with these colors.
    - *MUI*: Generate `createTheme()` with this palette.

## Self-Correction Checklist
- "Am I guessing the hex code?" -> STOP. Check Brand Guidelines.
- "Is this font available?" -> Use Google Fonts import.
- "Does this copy sound like the persona?" -> Rewrite if generic.
