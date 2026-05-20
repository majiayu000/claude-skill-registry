---
name: brand-guidelines
description: Apply OpenEd's visual brand identity to presentations, websites, and digital materials. Specifies colors, typography, spacing, and design specifications for consistent visual branding across all OpenEd materials.
---

# OpenEd Visual Brand Guidelines

This skill provides OpenEd's visual brand specifications for presentations, websites, digital materials, and design assets. Use this when you need color palettes, typography standards, spacing guidelines, and responsive design specifications.

## When to Use This Skill

Use this skill when:
- Creating PowerPoint presentations for OpenEd
- Designing digital materials with OpenEd branding
- Building websites or digital assets requiring brand consistency
- Specifying colors, fonts, and layout standards
- Creating templates or design systems for OpenEd

**For messaging, voice, narrative framework, and strategic content direction, see the `opened-identity` skill.**

---

## Visual Identity

### Color Palette

| Purpose | Color Name | Hex Value | RGB | Usage |
|---------|-----------|-----------|-----|-------|
| Primary Orange | Thought | #f24915 | rgb(242, 73, 21) | Thought category badges, accent elements, icons |
| Primary Blue | Trend | #03a4ea | rgb(3, 164, 234) | Trend category badges, links, buttons, hover states |
| Dark Gray | Tool | #141a1f | rgb(20, 26, 31) | Tool category badges, primary text, dark elements |
| Light Gray | Border | #e0e0e0 | rgb(224, 224, 224) | Borders, dividers, subtle backgrounds |
| Background | Off-White | #fafaf6 | rgb(250, 250, 246) | Page background, light backgrounds |
| Text | Dark | #333333 | rgb(51, 51, 51) | Primary text content |

**Color Usage Guidelines:**
- **Orange (#f24915)**: Draws attention, used for primary calls-to-action and "Thought" category content
- **Blue (#03a4ea)**: Conveys trust and forward momentum, used for "Trend" content and secondary CTAs
- **Dark Gray (#141a1f)**: Professional authority, used for "Tool" category and primary text
- **Light Gray (#e0e0e0)**: Creates visual hierarchy and separation without harshness
- **Off-White (#fafaf6)**: Reduces eye strain, perfect for backgrounds and large content areas

### Typography

| Element | Font | Weight | Size | Line Height | Color | Usage |
|---------|------|--------|------|------------|-------|-------|
| Headings (H1-H2) | Inter | 700 | 24-32px | 1.2 | #333 | Newsletter titles, major section headers |
| Subheadings (H3-H4) | Inter | 600 | 18-22px | 1.3 | #333 | Article titles, card headings |
| Body Text | Playfair | Regular | 16px | 1.6 | #333 | Long-form content, article text |
| Small Text | Inter | 400 | 12-14px | 1.5 | #666 | Metadata, timestamps, captions |
| Category Labels | Inter | Bold | 12px | 1.4 | White | Badge labels for content categories |

**Font Stack Guidelines:**
- **Headings (Inter)**: System font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`
- **Body (Playfair)**: Serif stack: `Georgia, "Times New Roman", Times, serif`

**Typography Principles:**
- Inter is modern, clean, and scannable—perfect for headlines and navigation
- Playfair provides warmth and readability for longer-form content
- Maintain 1.6 line height for body text for optimal readability
- Use font-weight 600-700 for headings to create clear hierarchy

### Spacing & Layout

| Element | Padding/Margin | Max Width | Notes |
|---------|----------------|-----------|-------|
| Container | 20px (desktop), 15px (mobile) | 600px | Primary content width for emails/newsletters |
| Article Cards | 20px padding, 30px margin-bottom | N/A | White background with 1px border, 5px radius, shadow |
| Section Headers | 0 padding, 30px margin-bottom | N/A | Clear separation between content blocks |
| Icon Circles | 40px (diameter) | N/A | Positioned above cards, -20px top offset |
| Border Radius | 5px | N/A | Applied to cards, buttons, inputs |

### Shadow & Depth

- **Card Shadow**: `0 4px 8px rgba(0,0,0,0.1)` (default)
- **Card Shadow on Hover**: `0 6px 12px rgba(0,0,0,0.15)` (interactive)
- **Icon Shadow**: `0 2px 4px rgba(0,0,0,0.2)` (subtle depth)

### Responsive Breakpoints

- **Desktop**: 600px+ (standard)
- **Mobile**: < 600px (media query adjustments)
- **Small Mobile**: < 480px (additional scaling)

**Mobile Adjustments:**
- Reduce heading size to 24px (from 28px)
- Reduce padding to 15px (from 20px)
- Scale icons to 0.9x
- Maintain 600px max-width constraint

