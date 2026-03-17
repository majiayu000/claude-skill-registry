---
name: ultimate-frontend
description: Create production-ready, gorgeous frontend interfaces with expert design guidance, modern component patterns, animations, and extensive templates. Combines design principles, component libraries (React/shadcn/ui/Tailwind), animation techniques (CSS/Framer Motion/p5.js), and 10 pre-built themes. Use this skill when building landing pages, web applications, dashboards, or any frontend project requiring high design quality and modern best practices.
---

# Ultimate Frontend Design

## Overview

Create distinctive, production-ready frontend interfaces that avoid generic AI aesthetics. This skill provides comprehensive guidance, templates, and resources for building gorgeous web experiences using modern technologies (React, Tailwind CSS, shadcn/ui, Framer Motion, p5.js).

## When to Use This Skill

Invoke this skill when:
- Building landing pages, marketing sites, or portfolios
- Creating web applications or dashboards
- Implementing animations or interactive elements
- Applying professional design themes
- Need component patterns and best practices
- Want to avoid generic, AI-looking designs

## Core Capabilities

### 1. Design Excellence

Follow anti-generic-AI design principles to create original, distinctive interfaces:

**Read `references/design-principles.md` for:**
- Anti-generic-AI aesthetics (what to avoid)
- Production-ready standards (accessibility, performance, responsive design)
- Design systems approach (color, typography, spacing, components)
- Contemporary trends (2024-2025)
- Unique design inspiration and differentiation strategies

**Key Principles:**
- Avoid gradient overload, geometric blobs, and generic SaaS layouts
- Use consistent spacing scales and typographic hierarchy
- Ensure WCAG AA accessibility (4.5:1 contrast minimum)
- Implement mobile-first responsive design
- Create originality through custom illustrations, unexpected colors, and asymmetric layouts

### 2. Modern Component Patterns

Build with React, Tailwind CSS, and shadcn/ui following industry best practices:

**Read `references/component-patterns.md` for:**
- Project structure recommendations
- shadcn/ui component installation and usage patterns
- Layout patterns (hero sections, bento grids, navigation)
- State management patterns (useState, React Query, Zustand)
- Animation patterns (Framer Motion, Tailwind animations)
- Performance optimization (code splitting, image optimization)
- Dark mode implementation

**Common Patterns:**
```tsx
// Button with variants
<Button variant="outline" size="lg">Click me</Button>

// Card structure
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>

// Form with validation
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
```

### 3. Animations & Interactions

Create smooth, performant animations that delight users:

**Read `references/animation-guide.md` for:**
- CSS animations and transitions
- Tailwind CSS animation utilities
- Framer Motion patterns (variants, gestures, scroll-triggered)
- p5.js for generative/algorithmic art
- Micro-interactions (button ripples, loading skeletons, toasts)
- Performance best practices

**Performance Rule:** Only animate `transform`, `opacity`, and sparingly `filter` for 60fps.

### 4. Professional Themes

Apply one of 10 pre-built professional color themes:

**Read `references/theme-library.md` for:**
- 10 complete color themes with CSS variables
- Typography scales (modern sans, elegant serif, tech monospace)
- Theme application methods (CSS variables, Tailwind config)
- Dark mode variants

**Available Themes:**
1. Ocean Depth - Professional blue tones
2. Forest Twilight - Natural greens
3. Sunset Blaze - Warm oranges and reds
4. Midnight Purple - Bold purples
5. Minimal Mono - Clean black/white
6. Pastel Dream - Soft, airy colors
7. Corporate Blue - Traditional business
8. Earthy Terracotta - Warm browns
9. Neon Cyber - Futuristic brights
10. Vintage Sepia - Classic sepia tones

### 5. Template Library

Start projects quickly with pre-built templates:

**Available in `assets/templates/`:**
- `landing-page/` - SaaS landing page (HTML + Tailwind)
- `react-dashboard/` - Admin dashboard (React + shadcn/ui)
- `portfolio/` - Portfolio site (HTML + Tailwind)
- `react-app-shell/` - Full React app boilerplate

**Use the setup script:**
```bash
python3 scripts/setup-project.py \
  --template landing-page \
  --theme ocean-depth \
  --output ./my-project
```

## Workflow Decision Tree

### Starting a New Project

**1. Determine Project Type:**
- Simple landing page or portfolio? → Use HTML templates
- Complex web application? → Use React templates
- Generative art or animations? → Use p5.js patterns

**2. Choose Template (if applicable):**
- Run `scripts/setup-project.py` with desired template and theme
- Customize the generated files

**3. Apply Design Principles:**
- Read `references/design-principles.md`
- Choose color theme from `references/theme-library.md`
- Ensure accessibility and responsive design

**4. Implement Components:**
- Read `references/component-patterns.md` for patterns
- Use shadcn/ui components for React projects
- Follow layout patterns (hero, bento grid, etc.)

**5. Add Animations:**
- Read `references/animation-guide.md`
- Implement micro-interactions
- Ensure performance (transform/opacity only)

### Enhancing Existing Projects

**1. Improve Design Quality:**
- Review against anti-generic-AI principles in `references/design-principles.md`
- Check for generic patterns (gradient overload, blobs, etc.)
- Improve typography hierarchy and spacing consistency

**2. Apply Theme:**
- Choose theme from `references/theme-library.md`
- Update CSS variables or Tailwind config
- Ensure consistent color usage

**3. Add Components:**
- Review `references/component-patterns.md`
- Install shadcn/ui components as needed
- Follow established patterns

**4. Enhance Animations:**
- Review `references/animation-guide.md`
- Add micro-interactions for better UX
- Optimize for 60fps performance

## Implementation Guidelines

### For Landing Pages

1. Start with hero section (clear value proposition, 2 CTAs)
2. Features section (3 columns, icons, concise descriptions)
3. Social proof (testimonials or logos)
4. Pricing (3-tier structure)
5. FAQ section (details/summary elements)
6. Footer (links, copyright)

**Template:** Use `assets/templates/landing-page/`

### For Web Applications

1. Set up React + TypeScript + Vite + Tailwind
2. Install shadcn/ui components (`npx shadcn-ui@latest add`)
3. Implement routing (React Router)
4. Add state management (Zustand for global, React Query for server)
5. Create layout (header, sidebar, main content)
6. Build feature components following patterns
7. Add dark mode support

**Template:** Use `assets/templates/react-app-shell/`

### For Dashboards

1. Sidebar navigation with sections
2. Data tables with sorting/filtering
3. Charts and visualizations (Chart.js)
4. Form components with validation
5. Modal dialogs for actions
6. Responsive layout (collapsible sidebar on mobile)

**Template:** Use `assets/templates/react-dashboard/`

### For Animations

**CSS Animations:**
- Simple transitions: Use Tailwind utilities (`transition`, `hover:scale-105`)
- Keyframe animations: Define in CSS, apply with `animate-*` classes

**Framer Motion:**
- Install: `npm install framer-motion`
- Use variants for reusable animation sets
- Implement stagger children for list animations
- Add scroll-triggered animations with `useScroll`

**p5.js (Generative Art):**
- Use seeded randomness for reproducibility
- Implement particle systems for organic movement
- Create flow fields for natural patterns
- Export as canvas or save frames

## Best Practices

### Design
- Avoid generic AI patterns (see `references/design-principles.md`)
- Use consistent spacing scale (4, 8, 16, 24, 32, 48, 64px)
- Ensure WCAG AA contrast ratios (4.5:1 minimum)
- Test on multiple devices and screen sizes

### Code
- Follow semantic HTML structure
- Use Tailwind CSS for styling (avoid custom CSS unless necessary)
- Implement proper TypeScript types for React components
- Use React Hook Form + Zod for form validation
- Code split large components with React.lazy()

### Performance
- Optimize images (WebP, lazy loading, responsive srcset)
- Only animate transform/opacity for 60fps
- Minimize JavaScript bundle size
- Use server-side rendering or static generation when possible
- Implement proper loading states

### Accessibility
- Use semantic HTML elements
- Add ARIA labels where needed
- Ensure keyboard navigation works
- Test with screen readers
- Respect prefers-reduced-motion

## Resources

### scripts/
- `setup-project.py` - Initialize projects with templates and themes

### references/
- `design-principles.md` - Comprehensive design guidance and anti-patterns
- `component-patterns.md` - React/Tailwind/shadcn/ui patterns and examples
- `animation-guide.md` - CSS, Framer Motion, and p5.js animation techniques
- `theme-library.md` - 10 pre-built color themes and typography scales

### assets/
- `templates/landing-page/` - HTML + Tailwind landing page
- `templates/react-dashboard/` - React dashboard with charts
- `templates/portfolio/` - Personal portfolio site
- `templates/react-app-shell/` - Full React app boilerplate

## Quick Start Examples

### Example 1: Create a Landing Page
```bash
# Initialize with template and theme
python3 scripts/setup-project.py \
  --template landing-page \
  --theme midnight-purple \
  --output ./my-landing-page

# Open and customize
cd my-landing-page
open index.html
```

### Example 2: Build a React Dashboard
1. Read `references/component-patterns.md` for setup
2. Copy `assets/templates/react-dashboard/` as starting point
3. Install dependencies: `npm install`
4. Add shadcn/ui components: `npx shadcn-ui@latest add button card`
5. Read `references/design-principles.md` for design guidance
6. Apply theme from `references/theme-library.md`

### Example 3: Add Animations
1. Read `references/animation-guide.md`
2. For simple animations: Use Tailwind (`transition`, `hover:scale-105`)
3. For complex animations: Install Framer Motion, use variants pattern
4. For generative art: Implement p5.js particle system or flow field

## Tips for Success

1. **Start with Design Principles** - Read `references/design-principles.md` first to avoid generic patterns
2. **Use Templates** - Don't start from scratch, customize existing templates
3. **Follow Patterns** - Reference `references/component-patterns.md` for proven solutions
4. **Choose Theme Early** - Apply a theme from `references/theme-library.md` at project start
5. **Test Across Devices** - Ensure responsive design works on mobile, tablet, desktop
6. **Prioritize Performance** - Follow animation best practices (transform/opacity only)
7. **Accessibility Matters** - Check contrast, keyboard nav, and screen reader support
