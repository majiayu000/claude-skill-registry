---
name: providing-brand-identity
description: Template skill providing the single source of truth for brand guidelines, design tokens, technology choices, and voice/tone. Customize this template for your brand. Use when generating UI components, styling applications, writing copy, or creating user-facing assets to ensure brand consistency.
---

# Brand Identity & Guidelines

> **📋 TEMPLATE SKILL**
> This is a starter template. Copy this folder to your project and customize the resources files with your brand's specific guidelines, design tokens, and voice/tone documentation.

## Setup Instructions

1. Copy this entire `brand-identity-template` folder to your project's `.agent/skills/` directory
2. Rename the folder to `brand-identity`
3. Update the resources files with your brand specifics:
   - `resources/design-tokens.json` - Your colors, fonts, spacing
   - `resources/tech-stack.md` - Your technology choices
   - `resources/voice-tone.md` - Your brand voice and tone
4. Replace `[YOUR BRAND NAME]` below with your actual brand name

---

**Brand Name:** [YOUR BRAND NAME]

This skill defines the core constraints for visual design and technical implementation for the brand. You must adhere to these guidelines strictly to maintain consistency.

## Reference Documentation

Depending on the task you are performing, consult the specific resource files below. Do not guess brand elements; always read the corresponding file.

### For Visual Design & UI Styling

If you need exact colors, fonts, border radii, or spacing values, read:
👉 **[`resources/design-tokens.json`](resources/design-tokens.json)**

### For Coding & Component Implementation

If you are generating code, choosing libraries, or structuring UI components, read the technical constraints here:
👉 **[`resources/tech-stack.md`](resources/tech-stack.md)**

### For Copywriting & Content Generation

If you are writing marketing copy, error messages, documentation, or user-facing text, read the persona guidelines here:
👉 **[`resources/voice-tone.md`](resources/voice-tone.md)**
