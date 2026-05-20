---
name: frontend-design
description: Create distinctive, production-grade frontend interfaces. USE THIS whenever the user asks to build web components, pages, dashboards, landing pages, React/Next/Vue components, HTML/CSS layouts, or when styling/beautifying any UI. Also use when creating posters, visual artifacts, or any web interface. This generates creative, polished code that prioritizes minimalist aesthetics with carefully crafted 3D effects and smooth interactions.
---

# Frontend Design Skill

Your primary purpose is to create **production-grade, high-quality frontend interfaces** that stand out. You prioritize clean code, modern design patterns, and distinctive visual appeal.

## Your Tech Stack

### Frameworks
- **Primary**: React & Next.js
- **Secondary**: Vue.js (as needed)
- Use the framework that best fits the project context

### Styling & Components
- **Tailwind CSS** - for utility-first styling
- **shadcn/ui** - for accessible, composable components
- **Chakra UI** - for flexible, themeable components
- When to use which:
  - **shadcn/ui**: Default choice for modern, minimal designs with accessibility baked in
  - **Chakra UI**: When you need theme flexibility or rapid prototyping
  - **Tailwind alone**: For custom, unique designs where pre-built components would feel restrictive

### Design Philosophy
- **Aesthetic**: Well-crafted, minimalist, clean
- **Visual Effects**: Strategic use of 3D transforms and depth
- **Interactions**: Smooth animations and micro-interactions
- **Spacing**: Generous whitespace, clear hierarchy
- **Typography**: Careful font pairing, excellent readability

## When to Use This Skill

✓ Building web components or pages  
✓ Creating dashboards or data visualizations  
✓ Designing landing pages or marketing sites  
✓ Styling/beautifying existing UIs  
✓ Creating React/Next/Vue applications  
✓ Building HTML/CSS layouts  
✓ Creating visual artifacts or posters  
✓ Any request involving web interface design  

**Invoke directly**: Use `/frontend-design` if Claude doesn't auto-trigger this skill.

## Your Design Approach

### 1. Component Architecture
- Break designs into small, reusable components
- Use composition over inheritance
- Keep components focused and single-purpose
- Export components that are easy to test and iterate on

### 2. Styling Strategy
```
Priority Order:
1. shadcn/ui components (accessible defaults + customizable)
2. Custom Tailwind utilities (for unique styling)
3. CSS modules (for complex scoped styles)
4. Inline styles (rarely, only for dynamic values)
```

### 3. Minimalist 3D Effects
- Use CSS transforms sparingly for visual interest
- `perspective`, `rotateX`, `rotateY` for subtle depth
- Hover states that respond with elevation or subtle motion
- Layer depth with shadows (use Tailwind's shadow utilities strategically)
- Never let 3D effects compromise readability or usability

### 4. Interaction & Animation
- Smooth transitions between states (150-300ms for most interactions)
- Use `framer-motion` for complex animations (if available)
- Micro-interactions that provide feedback
- Purposeful motion that guides user attention
- Keep animations under 400ms for responsive feel

### 5. Color & Typography
- Limit palette to 3-5 colors + neutrals
- High contrast for accessibility
- Careful font hierarchy (typically 2-3 font families max)
- Use system fonts when possible for performance
- Dark mode support as standard

## Code Quality Standards

### React/Next.js
```javascript
// Use functional components with hooks
// Proper TypeScript types when available
// Component organization:
//   1. Imports
//   2. Type definitions
//   3. Component function
//   4. Exports
```

### Tailwind Best Practices
- Use `@apply` rarely (prefer composition)
- Consistent spacing scale (use Tailwind's default 4px units)
- Dark mode variant: `dark:` prefix for dark mode styles
- Responsive prefixes: `sm:`, `md:`, `lg:` for responsive design

### Accessibility
- Semantic HTML (`<button>`, `<nav>`, `<main>`, etc.)
- ARIA labels where needed
- Sufficient color contrast (WCAG AA minimum)
- Keyboard navigation support
- Focus indicators on interactive elements

### Performance
- Lazy load images (`loading="lazy"`)
- Minimize layout shifts (use `aspect-ratio` for media containers)
- Optimize font loading
- Code-split components when needed in Next.js

## Output Format

When creating interfaces, deliver:

1. **Clean, commented code** - self-documenting and easy to modify
2. **Component structure** - organized and scalable
3. **Tailwind classes** - properly ordered and minimal
4. **Responsive design** - mobile-first approach
5. **Interactive states** - hover, focus, active feedback
6. **Dark mode** - included by default
7. **Accessibility considerations** - noted in comments

## Common Patterns

### Card Component (shadcn/ui base)
```jsx
// Minimalist, with subtle 3D on hover
<div className="rounded-lg border border-gray-200 bg-white p-6 
  shadow-sm hover:shadow-md transition-shadow duration-200
  dark:border-gray-800 dark:bg-gray-950">
  {children}
</div>
```

### Interactive Button (with 3D effect)
```jsx
// Responds to interaction with subtle depth
<button className="px-4 py-2 rounded-lg bg-blue-600 text-white
  hover:shadow-lg hover:scale-105 transition-all duration-200
  active:scale-95 focus:outline-none focus:ring-2 focus:ring-blue-400">
  {label}
</button>
```

### Gradient Text
```jsx
<h1 className="bg-gradient-to-r from-blue-600 to-purple-600 
  bg-clip-text text-transparent font-bold text-4xl">
  Gradient Heading
</h1>
```

## Pro Tips

1. **Start with the grid** - Mental Models: desktop-first wireframe, then add responsive variants
2. **Typography first** - Great typography makes any design look polished
3. **Whitespace is content** - Don't fill every pixel
4. **Test on mobile early** - Responsive design is non-negotiable
5. **Use design tokens** - Tailor Tailwind config for consistent sizing/spacing
6. **Focus on depth, not chaos** - 3D effects should enhance, never distract
7. **Animate with purpose** - Every animation should serve a function

## Tools & Dependencies

- **React 18+** / **Next.js 13+** / **Vue 3+**
- **Tailwind CSS 3+**
- **shadcn/ui** (optional but recommended)
- **Chakra UI** (optional alternative)
- **framer-motion** (for complex animations)
- **TypeScript** (strongly recommended)

## Quick Start Template

```jsx
// pages/example.jsx (Next.js) or App.jsx (React)
import { Button } from '@/components/ui/button'

export default function Example() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-950 dark:to-gray-900">
      <div className="max-w-7xl mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold mb-4 dark:text-white">
          Your Title Here
        </h1>
        <p className="text-lg text-gray-600 dark:text-gray-400 mb-8">
          Your description
        </p>
        <Button>Get Started</Button>
      </div>
    </div>
  )
}
```

## Troubleshooting

- **Components look generic?** → Add strategic 3D transforms and custom shadows
- **No responsive feel?** → Ensure mobile-first breakpoints are applied
- **Performance issues?** → Check for unused Tailwind classes, lazy load images
- **Accessibility concerns?** → Use semantic HTML, test keyboard nav, check contrast
- **Not hitting the aesthetic?** → Increase whitespace, refine typography, simplify colors

---

**Remember**: Great frontend design is about balancing aesthetics with functionality. Every visual element should serve a purpose. When in doubt, choose minimalism with carefully considered highlights.
