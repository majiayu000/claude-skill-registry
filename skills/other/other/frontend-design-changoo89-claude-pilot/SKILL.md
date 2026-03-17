---
name: frontend-design
description: Production-grade frontend design skill for distinctive, non-generic UI development. Avoids "AI slop" aesthetics through specific aesthetic direction guidelines.
license: MIT
---

# Frontend Design Skill

> **Purpose**: Create production-grade, distinctive UI that stands out from generic AI-generated designs

---

## Quick Start

### When to Use

- Building web UI components, pages, or applications
- Creating dashboard interfaces, landing pages, or marketing sites
- Styling React components, HTML/CSS layouts, or design systems

### Quick Reference

| Category | Key Principle | Action |
|----------|---------------|--------|
| **Fonts** | Avoid defaults | Never use Inter as default |
| **Colors** | Avoid gradients | No purple-to-blue gradients |
| **Layout** | Embrace asymmetry | Break from rigid grids |
| **Details** | Add texture | Use noise, patterns, borders |

## Core Principles

### 1. Choose an Aesthetic Direction

| Direction | Characteristics | Examples |
|-----------|----------------|----------|
| **Minimalist** | Clean, sparse, purposeful | Stripe, Linear |
| **Maximalist** | Bold, expressive, layered | Brutalist sites |
| **Warm/Human** | Organic textures, soft edges | Notion, Gumroad |
| **Technical/Precise** | Sharp edges, monospace | Vercel, GitHub |
| **Playful** | Bright colors, rounded | Discord, Slack |

**Action**: Start with "I'll use a **[direction]** aesthetic for this."

### 2. Make Every Detail Intentional

- **Default fonts** → Never accept Inter as the default
- **Gradients** → Purple-to-blue is the most overused gradient
- **Center alignment** → Explore asymmetry and interesting layouts
- **Flat colors** → Add texture, noise, patterns, or subtle borders

### 3. Be Specific, Not Generic

**Bad**: "Use a nice color scheme" | **Good**: "Use a warm palette with coral (#FF6B6B) as primary, cream (#FFF8F0) background"

## Typography & Color

### Font Selection

**⚠️ NEVER use Inter as the default font**

| Category | Font Families | When to Use |
|----------|---------------|-------------|
| **Serif** | GT Super, Charter, Georgia | Editorial, premium |
| **Sans-Serif** | Geist, Satoshi, System UI | Clean, modern (not Inter!) |
| **Monospace** | Geist Mono, JetBrains Mono | Technical, code |
| **Display** | Clash Display, Syne | Headlines, personality |

**Typography Hierarchy**: Headlines: 40-72px, tight tracking (-1% to -3%) | Body: 16-18px, loose tracking (0% to +2%)

### Color Strategy

**⚠️ Anti-Pattern**: `background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);` (purple-to-blue is everywhere)

**Moods**: Warm (coral, peach, cream) | Cool (teal, sage, slate) | Bold (red, yellow, black) | Muted (olive, rust, navy)

**Palette example**:
```css
:root {
  --primary: #FF6B6B;      /* Coral */
  --background: #FFF8F0;   /* Cream */
  --text: #2D3436;
  --border: #E8E8E8;
}
```

**Usage rules**:
- Backgrounds: Off-white, cream, or dark (never pure #FFF)
- Borders: Subtle (opacity 0.1-0.2) or sharp black/white
- Gradients: Subtle, same-hue shifts (no purple-to-blue!)

## Motion & Layout

### Animation Principles

- **Duration**: 200-300ms for micro-interactions
- **Easing**: `ease-out` for entry, `ease-in` for exit
- **Spring physics**: `cubic-bezier(0.34, 1.56, 0.64, 1)`
- **Examples**: Hover: Scale up (1.02) | Click: Scale down (0.98) | Entry: Fade in + slide up (20px)

### ⚠️ Anti-Pattern: Over-Animation

**Avoid**: Spinning loaders, bounce effects, slow fade-ins (>500ms)

### Layout Strategy

- Explore asymmetric layouts
- Use grid systems creatively
- Generous padding = premium feel

**Component Spacing**: Section (80-120px) | Component (24-32px) | Element (8-16px)

## Anti-Patterns: The "AI Slop" Checklist

- [ ] **Inter font** default → Change
- [ ] **Purple-to-blue gradient** → Different scheme
- [ ] **Perfectly centered** → Explore asymmetry
- [ ] **Pure white (#FFF)** → Add texture
- [ ] **Generic shadows** → Use subtle
- [ ] **No borders** → Add separation
- [ ] **Rounded-xl everywhere** → Vary radius
- [ ] **No texture/noise** → Add interest

## Implementation Tips

### Tailwind CSS

```jsx
/* Good: Specific values */
className="text-[17px] leading-[1.6] text-[#2D3436]"

/* Bad: Generic defaults */
className="text-base leading-normal text-gray-900"
```

### React Components

```jsx
const theme = { colors: { primary: '#FF6B6B' } };
<button style={{ backgroundColor: theme.colors.primary }} />
```

## Further Reading

**Internal**: @.claude/skills/frontend-design/REFERENCE.md - Detailed examples, patterns, case studies

**External**: [Refactoring UI](https://www.refactoringui.com/)
