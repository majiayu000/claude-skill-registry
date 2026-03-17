---
description: Interactive design wizard that guides through a complete frontend design process with discovery, aesthetic selection, and code generation. Use for creating distinctive, production-ready UI.
allowed-tools:
  - Read
  - Write
  - AskUserQuestion
  - Skill
---

# Design Wizard

An interactive wizard that guides you through creating distinctive, production-ready frontend designs.

## Purpose

This skill orchestrates the complete design process:
1. Discovery - Understanding what to build
2. Research - Analyzing trends and inspiration
3. Direction - Selecting aesthetic approach
4. Colors - Choosing color palette
5. Typography - Selecting fonts
6. Implementation - Generating code
7. Review - Validating quality

## Process Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Discovery  │ ──▶ │  Research   │ ──▶ │  Moodboard  │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
┌─────────────┐     ┌─────────────┐           ▼
│   Review    │ ◀── │  Generate   │ ◀── ┌─────────────┐
└─────────────┘     └─────────────┘     │ Colors/Type │
                                        └─────────────┘
```

## Step 1: Discovery Questions

Ask the user about their project:

### Question 1: What are you building?
- Landing page
- Dashboard
- Blog/Content site
- E-commerce
- Portfolio
- SaaS application
- Mobile app UI
- Other (describe)

### Question 2: Project context
- Personal project
- Startup/new product
- Established brand
- Client work
- Redesign of existing

### Question 3: Target audience
- Developers/technical
- Business professionals
- Creative/designers
- General consumers
- Young/Gen-Z
- Luxury/premium market

### Question 4: Background style preference
- Pure white (#ffffff)
- Off-white/warm (#faf8f5)
- Light tinted (use lightest palette color)
- Dark/moody (use darkest palette color)
- Let me decide based on aesthetic

### Question 5: Any specific inspiration?
- URLs to analyze
- Aesthetic keywords
- Specific requirements
- Skip (use trend research)

## Step 2: Research Phase

Based on answers, optionally invoke:
- `trend-researcher` - For current design trends
- `inspiration-analyzer` - For specific URLs provided

## Step 3: Moodboard Phase

Invoke `moodboard-creator` to:
- Synthesize research into direction
- Present options to user
- Iterate until approved

## Step 4: Aesthetic Selection

Based on discovery and moodboard, suggest aesthetics from catalog:

**For Modern/Premium:**
- Dark & Premium - Sophisticated, high-contrast
- Glassmorphism - Layered, translucent
- Bento Grid - Structured, modular

**For Bold/Distinctive:**
- Neobrutalism - Raw, impactful
- Statement Hero - Typography-focused
- Editorial - Magazine-inspired

**For Minimal/Clean:**
- Scandinavian - Warm minimal
- Swiss Typography - Grid-based clarity
- Single-Page Focus - Concentrated impact

**For Playful/Creative:**
- Y2K/Cyber - Retro-futuristic
- Memphis - Colorful geometric
- Kawaii - Cute, rounded

See `references/aesthetics-catalog.md` for full catalog.

## Step 5: Color & Typography

Invoke specialized skills:
- `color-curator` - Browse Coolors or select from fallbacks
- `typography-selector` - Browse Google Fonts or use pairings

Map selections to Tailwind config.

## Step 6: Code Generation

Generate single HTML file with:

### Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Project Title]</title>

  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=[Font1]&family=[Font2]&display=swap" rel="stylesheet">

  <!-- Tailwind CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            // Custom colors from palette
          },
          fontFamily: {
            // Custom fonts
          }
        }
      }
    }
  </script>

  <style>
    /* Custom animations */
    /* Focus states */
    /* Reduced motion */
  </style>
</head>
<body>
  <!-- Semantic HTML structure -->
</body>
</html>
```

### Requirements
- Mobile-responsive (Tailwind breakpoints)
- Semantic HTML (header, main, nav, footer, section)
- Accessible (ARIA labels, focus states, contrast)
- No Lorem ipsum (realistic placeholder content)
- Animations respect prefers-reduced-motion
- Keyboard navigable

## Step 7: Self-Review

Check against `references/anti-patterns.md`:
- [ ] No hero badges/pills
- [ ] No generic fonts (Inter, Roboto, Arial)
- [ ] No purple/blue gradients on white
- [ ] No generic blob shapes
- [ ] No excessive rounded corners
- [ ] No predictable templates

Check `references/design-principles.md`:
- [ ] Clear visual hierarchy
- [ ] Proper alignment
- [ ] Sufficient contrast
- [ ] Appropriate white space
- [ ] Consistent spacing

Check `references/accessibility-guidelines.md`:
- [ ] 4.5:1 contrast ratio for text
- [ ] Visible focus states
- [ ] Semantic HTML
- [ ] Alt text for images
- [ ] Form labels

## Output Format

Deliver:
1. Final HTML file
2. Brief explanation of design choices
3. List of fonts used (for reference)
4. Color palette summary

## Iteration

If user requests changes:
1. Note specific feedback
2. Make targeted adjustments
3. Re-run self-review
4. Present updated version

Maximum 3 major iterations, then consolidate feedback.

## References

- `references/design-principles.md` - Core design principles with code
- `references/aesthetics-catalog.md` - Full aesthetic catalog
- `references/anti-patterns.md` - What NOT to do
- `references/accessibility-guidelines.md` - WCAG compliance
