---
name: design-guide
description: Professional design methodology for building modern, premium interfaces with client branding. Use for ALL client work and non-AICA projects. Applies glassforium logic, cinematic polish, and intentional design principles while adapting to client colors and brand identity. For Kelvin's personal AICA brand (black glass + gold), use the 'aica' skill instead.
---

# Professional Design Guide

Apply these principles to every client project, UI component, webpage, or interface you build.

## When to Use This Skill

**Use design-guide for:**
- ALL client work (regardless of brand/colors)
- Non-AICA projects
- General UI components
- Any design work that needs YOUR quality but THEIR branding

**DO NOT use this for:**
- Kelvin's personal AICA brand projects (use `aica` skill instead)
- kelvingarr.com or AICA-branded sites

## Philosophy

This is YOUR professional design approach applied to client work:
- **Your methodology**: Glassforium logic, cinematic lighting, intentional motion
- **Your quality**: Clean execution, thoughtful hierarchy, premium polish
- **Their identity**: Adapt to their colors, fonts, and brand guidelines

You give them what they want, but with your caliber and flavor.

## Core Design Principles

### 1. Clean and Minimal
- Embrace white space—it's not wasted space, it's breathing room
- Avoid clutter—every element should have a purpose
- Remove unnecessary decorative elements
- Keep layouts simple and focused

### 2. Color Palette
- **Base colors**: Use grays (e.g., #f8f9fa, #e9ecef, #6c757d) and off-whites
- **Accent color**: Choose ONE accent color and use it sparingly for CTAs and highlights
- **NEVER use**: Generic purple/blue gradients, rainbow gradients, or multiple competing accent colors
- **Example palette**: 
  - Background: #ffffff, #f8f9fa
  - Text: #212529, #6c757d
  - Borders: #dee2e6
  - Accent: #10b981 (or similar single color)

### 3. Spacing System (8px Grid)
Use consistent spacing based on 8px increments:
- **8px**: Tight spacing (icon to text, form field padding)
- **16px**: Default spacing (between related elements)
- **24px**: Medium spacing (between sections within a card)
- **32px**: Large spacing (between distinct sections)
- **48px**: Extra large spacing (major section breaks)
- **64px**: Maximum spacing (page-level separations)

Apply this system to: padding, margins, gaps, and positioning.

### 4. Typography
- **Minimum body text**: 16px (never smaller)
- **Maximum fonts**: 2 font families per design
- **Clear hierarchy**:
  - H1: 32-48px, bold
  - H2: 24-32px, semibold
  - H3: 20-24px, semibold
  - Body: 16px, regular
  - Small text: 14px, regular (use sparingly)
- **Line height**: 1.5-1.6 for body text, 1.2-1.3 for headings
- **Recommended fonts**: Inter, Roboto, System UI for sans-serif; avoid mixing serif and sans-serif

### 5. Shadows
- Use subtle shadows, not heavy or dramatic
- **Light shadow**: `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1)`
- **Medium shadow**: `box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1)`
- **Never**: Multiple stacked shadows or dark/heavy shadows

### 6. Rounded Corners
- Use rounded corners selectively, not on everything
- **Buttons**: 6-8px border-radius
- **Cards**: 8-12px border-radius
- **Form inputs**: 6-8px border-radius
- **Small elements** (badges, tags): 4-6px border-radius
- **Consider**: Some elements (data tables, code blocks) look better with sharp corners

### 7. Interactive States
Always define clear states for interactive elements:
- **Default**: Base appearance
- **Hover**: Subtle color shift or shadow increase
- **Active/Focus**: Clear visual feedback (border, background change)
- **Disabled**: Reduced opacity (0.5-0.6) and cursor: not-allowed
- **Example**: Button hover increases shadow slightly and darkens background by 5-10%

### 8. Mobile-First Approach
- Design for mobile screens first, then enhance for larger screens
- Use responsive units (rem, %, vw/vh) over fixed pixels
- Ensure touch targets are minimum 44x44px
- Test layouts at 320px, 768px, 1024px, and 1440px

## Component-Specific Guidelines

### Buttons
✅ **Good**:
- Padding: 12px 24px (or 16px 32px for large)
- Subtle shadow: `0 1px 3px rgba(0, 0, 0, 0.1)`
- Hover: Slightly darker background + increased shadow
- Border-radius: 6-8px
- No gradients

❌ **Bad**:
- Gradient backgrounds
- Heavy shadows
- Tiny padding
- Inconsistent sizing across button types

### Cards
✅ **Good**:
- Choose EITHER clean border (1px #e5e7eb) OR subtle shadow
- Never both border and shadow
- Padding: 24px or 32px
- Border-radius: 8-12px
- White or subtle gray background

❌ **Bad**:
- Both heavy borders and shadows
- Gradients
- Inconsistent padding
- Too many nested cards

### Forms
✅ **Good**:
- Labels above inputs, 8px spacing
- Input padding: 12px 16px
- Clear error states with red accent and error message
- Spacing between fields: 24px
- Success states with green accent
- Disabled inputs at 0.6 opacity

❌ **Bad**:
- Tiny unreadable labels
- Inputs without padding
- No clear error/success feedback
- Inconsistent field spacing
- No focus states

### Data Tables
✅ **Good**:
- Header row with subtle background (#f8f9fa)
- Row hover state (slight background change)
- Adequate cell padding: 12px 16px
- Borders: subtle horizontal dividers only
- Proper column alignment (numbers right, text left)

❌ **Bad**:
- Heavy borders everywhere
- No hover states
- Cramped cells
- Poor alignment

## Accessibility Checklist
- Color contrast ratio minimum 4.5:1 for text
- All interactive elements keyboard accessible
- Focus indicators visible
- Text scalable to 200% without breaking layout
- Sufficient spacing between clickable elements (8px minimum)

## Anti-Patterns to Avoid
- ❌ Rainbow gradients everywhere
- ❌ Text smaller than 14px
- ❌ Inconsistent spacing (mixing arbitrary values)
- ❌ Every element a different color
- ❌ Heavy drop shadows
- ❌ Too many font families
- ❌ Overly rounded corners on everything
- ❌ No visual hierarchy
- ❌ Missing interactive states

## Quick Reference
When building any UI, ask:
1. Is this clean and minimal with adequate white space?
2. Am I using only grays/off-whites + one accent color?
3. Are all spacing values from the 8px grid (8, 16, 24, 32, 48, 64)?
4. Is text at least 16px with clear hierarchy?
5. Are shadows subtle?
6. Do interactive elements have hover/focus/disabled states?
7. Does this work on mobile?

## Advanced: Premium Glass Framework

For cinematic, premium, or emotionally-driven client designs, layer in the glass methodology:

**Read this file**: `references/glass-methodology.md`

**When to use**:
- Client requests "premium," "cinematic," or "glass" aesthetic
- Building hero sections, landing pages, or marketing sites
- Emotional connection is critical to project success
- Project benefits from elevated visual polish

**How to integrate**:
1. Start with standard Design Guide principles (above) as foundation
2. Read glass methodology for depth, lighting, and motion techniques
3. Answer the 3 creative questions before designing
4. Choose appropriate glass material mode (soft/hard/matte/metal/liquid)
5. **Adapt to client colors**: Use their brand palette, not AICA's
6. Layer in cinematic lighting with their color scheme
7. Apply physics-based motion
8. Document your reasoning

**Result**: Clean foundation + premium cinematic polish with CLIENT branding

This methodology enhances client brand guidelines with depth, emotion, and intelligence—never overrides them.
