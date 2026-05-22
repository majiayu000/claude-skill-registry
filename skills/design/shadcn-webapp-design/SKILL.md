---
name: shadcn-webapp-design
description: Build production-grade Next.js web applications with shadcn/ui, Tailwind CSS, and Framer Motion. Use when building React components, pages, dashboards, landing pages, or any web UI that should use the shadcn/ui component library. Triggers on requests involving shadcn components, Tailwind styling, Framer Motion animations, or when the user wants polished, non-generic UI that avoids "vibecoded" aesthetics.
---

# shadcn/ui Webapp Design

Build distinctive, production-grade web interfaces using **Next.js 14 + Tailwind CSS + shadcn/ui + Framer Motion**. This skill guides creation of interfaces that avoid generic "AI slop" aesthetics with exceptional attention to aesthetic details and creative choices.

## Design Thinking

Before coding, understand the context and commit to a **BOLD** aesthetic direction:

- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian. Use these for inspiration but design one true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is intentionality, not intensity.

## Frontend Aesthetics Guidelines

### Typography
Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt for distinctive choices that elevate aesthetics. Pair a distinctive display font with a refined body font.

### Color & Theme
Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

### Motion
Use Framer Motion for effects and micro-interactions. Focus on high-impact moments: one well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.

### Spatial Composition
Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.

### Backgrounds & Visual Details
Create atmosphere and depth rather than defaulting to solid colors. Apply creative forms: gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, grain overlays.

## Anti-Patterns: Never Use

- Overused font families (Inter, Roboto, Arial, Space Grotesk, system fonts)
- Cliched color schemes (purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design lacking context-specific character
- Generic rounded cards with subtle shadows
- Stock gradient buttons

**Match implementation complexity to aesthetic vision.** Maximalist designs need elaborate code with extensive animations. Minimalist designs need restraint, precision, and careful attention to spacing and typography.

---

## Core Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Framework | Next.js 14 (App Router) | Server components, routing, optimization |
| Styling | Tailwind CSS | Utility-first styling with design tokens |
| Components | shadcn/ui | Accessible, customizable component primitives |
| Animation | Framer Motion | Declarative animations and gestures |

## Setup

### New Project

```bash
# Create Next.js with Tailwind
npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd my-app

# Initialize shadcn/ui
npx shadcn@latest init

# Install Framer Motion
npm install framer-motion

# Install common shadcn components
npx shadcn@latest add button card input label dialog dropdown-menu tabs toast
```

### Existing Project

```bash
# Verify dependencies
grep -E "next|tailwindcss|framer-motion" package.json
cat components.json  # shadcn config

# Install missing pieces
npm install framer-motion              # if missing
npx shadcn@latest init                 # if missing
npx shadcn@latest add [component-name] # as needed
```

## Design System First

Before writing code, read the project's design tokens:

```bash
cat tailwind.config.ts
cat app/globals.css
cat components.json
```

Use established tokens—never invent new colors or spacing.

## Component Usage

Always import from the project's component directory:

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
```

Check what's installed: `ls components/ui/`

If a component doesn't exist:
```bash
npx shadcn@latest add [component-name]
```

## Animation Quick Reference

```tsx
import { motion } from "framer-motion"

// Fade up on enter
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
/>

// Stagger children
<motion.div
  initial="hidden"
  animate="visible"
  variants={{
    hidden: {},
    visible: { transition: { staggerChildren: 0.1 } }
  }}
>
  {items.map(item => (
    <motion.div
      key={item.id}
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
      }}
    />
  ))}
</motion.div>

// Hover interaction
<motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} />
```

## Workflow

1. **Read existing code** - Understand the project's patterns
2. **Check design tokens** - Use established colors/spacing
3. **Commit to aesthetic direction** - Bold and intentional
4. **Use shadcn components** - Never recreate primitives
5. **Add Framer Motion** - For meaningful interactions
6. **Test responsiveness** - Mobile-first with Tailwind breakpoints

## Reference Files

- **[references/shadcn-components.md](references/shadcn-components.md)** - Component patterns and composition
- **[references/framer-motion-patterns.md](references/framer-motion-patterns.md)** - Animation recipes
- **[references/design-tokens.md](references/design-tokens.md)** - Token system and theming
