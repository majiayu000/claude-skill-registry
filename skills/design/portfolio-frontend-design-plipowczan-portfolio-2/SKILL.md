---
name: portfolio-frontend-design
description: Frontend design system dla projektu portfolio Pawla Lipowczana (React 19 + Vite 7 + Tailwind CSS 3 + Framer Motion 12). Uzyj przy tworzeniu nowych komponentow, stron, sekcji lub modyfikacji UI w portfolio. Zawiera palete kolorow (green accent #00ff9d, dark backgrounds #0a0e1a), typografie (Inter/Poppins), wzorce animacji Framer Motion, efekty hover (scale 1.05 + green glow), glassmorphism cards, gradient text effects. Zapewnia spojnosc z istniejacym design language i architektura projektu.
license: Apache-2.0
---

# Portfolio Frontend Design System

Design system i wytyczne dla projektu portfolio Pawla Lipowczana. Zapewnia spojnosc wizualna przy tworzeniu nowych komponentow, stron i sekcji.

## Quick Reference

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| Primary Accent | `#00ff9d` | Buttons, CTAs, hover states, highlights |
| Accent Hover | `#00ffa3` | Hover variants |
| Cyan | `#00b8ff` | Gradient secondary color |
| Background Dark | `#0a0e1a` | Main page background |
| Background Darker | `#050810` | Deep sections, cards |
| Text Primary | `#ffffff` | Headings, important text |
| Text Secondary | `#e5e7eb` | Body text, descriptions |
| Text Muted | `#9ca3af` | Less important text |

### Gradient Definitions

```css
/* Primary text gradient */
background: linear-gradient(to right, #00ff9d, #00b8ff, #00ffa3);
-webkit-background-clip: text;
background-clip: text;
color: transparent;

/* Tailwind equivalent */
className="bg-gradient-to-r from-green-400 via-cyan-400 to-green-300 bg-clip-text text-transparent"
```

### Typography

| Element | Font | Tailwind Classes |
|---------|------|------------------|
| Headings | Inter/Poppins | `font-bold` |
| Body | Inter | `font-normal` |
| Code | Fira Code | `font-mono` |
| Hero Title | Inter | `text-6xl md:text-8xl font-bold uppercase` |

### Core Tailwind Class Combinations

```jsx
// Primary Button
className="px-6 py-3 bg-green-500 hover:bg-green-400 text-black font-semibold rounded-lg transition-all duration-300 hover:scale-105 hover:shadow-[0_0_30px_rgba(0,255,157,0.3)]"

// Secondary/Outline Button
className="px-6 py-3 border border-green-500 text-green-500 hover:bg-green-500/10 rounded-lg transition-all duration-300"

// Glassmorphism Card
className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-xl p-6 hover:border-green-500/30 transition-all duration-300"

// Section Container
className="relative min-h-screen py-20 px-4 md:px-8 lg:px-16"

// Gradient Text
className="bg-gradient-to-r from-green-400 via-cyan-400 to-green-300 bg-clip-text text-transparent"
```

## Component Creation Workflow

1. **Determine component type** - Section (homepage), Page (route), or UI component
2. **Copy appropriate template** from `assets/templates/`
3. **Apply design tokens** from `references/design-tokens.md`
4. **Add animations** following `references/animation-patterns.md`
5. **Verify accessibility** using `references/accessibility-checklist.md`
6. **Place in correct directory** (see Integration section)

## Design Principles

### Visual Identity

Portfolio uzywa ciemnego motywu z zielonymi/cyan akcentami, tworzac nowoczesna, techniczna estetykę:

- **Dark theme only** - Ciemne tla (#0a0e1a, #050810) z jasnym tekstem
- **Green/Cyan accents** - Wszystkie interaktywne elementy uzywaja zielonego (#00ff9d)
- **Gradient effects** - Naglowki z gradient text, dekoracyjne elementy
- **Glassmorphism** - Karty z backdrop-blur i polprzezroczystymi tlami
- **Network/Tech aesthetic** - Canvas particle background, geometric patterns

### Hover & Interaction Effects

Wszystkie interaktywne elementy musza miec efekty hover:

```jsx
// Standard card hover - lift + glow
whileHover={{ y: -10 }}
className="hover:shadow-[0_0_30px_rgba(0,255,157,0.15)] hover:border-green-500/30"

// Button hover - scale + glow
className="hover:scale-105 hover:shadow-[0_0_30px_rgba(0,255,157,0.3)]"

// Link hover - color change
className="hover:text-green-400 transition-colors"

// Image hover - zoom
className="group-hover:scale-105 transition-transform duration-500"
```

### Animation Timing

| Type | Duration | Easing |
|------|----------|--------|
| Hover transitions | 300ms | ease |
| Page transitions | 500ms | easeOut |
| Stagger children | 100ms delay | - |
| Entry animations | 600ms | easeOut |

## Component Patterns

### Section Structure

Kazda sekcja strony glownej powinna miec:

```jsx
<section
  id="section-name"  // dla smooth scroll
  className="relative min-h-screen py-20 px-4 md:px-8 lg:px-16"
>
  {/* Decorative background blurs */}
  <div className="absolute inset-0 overflow-hidden pointer-events-none">
    <div className="absolute top-1/4 -left-20 w-72 h-72 bg-green-500/10 rounded-full blur-3xl" />
  </div>

  <div className="relative max-w-7xl mx-auto">
    {/* Section header */}
    <motion.div className="text-center mb-16">
      <h2 className="text-4xl md:text-5xl font-bold">
        <span className="bg-gradient-to-r from-green-400 via-cyan-400 to-green-300 bg-clip-text text-transparent">
          Section Title
        </span>
      </h2>
      <p className="text-gray-400 text-lg mt-4">Description</p>
    </motion.div>

    {/* Content grid */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      {/* Items */}
    </div>
  </div>
</section>
```

### Card Component

Karty uzywaja glassmorphism z hover effects:

```jsx
<motion.div
  whileHover={{ y: -10 }}
  className="
    bg-white/5 backdrop-blur-sm
    border border-white/10
    rounded-xl overflow-hidden
    transition-all duration-300
    hover:border-green-500/30
    hover:shadow-[0_0_30px_rgba(0,255,157,0.15)]
  "
>
  <img className="w-full aspect-video object-cover" />
  <div className="p-6">
    <h3 className="text-xl font-semibold text-white group-hover:text-green-400">
      Title
    </h3>
    <p className="text-gray-400 mt-2">Description</p>
    {/* Tags */}
    <div className="flex gap-2 mt-4">
      <span className="px-2 py-1 text-xs bg-green-500/10 text-green-400 rounded-full border border-green-500/20">
        Tag
      </span>
    </div>
  </div>
</motion.div>
```

### Navigation

Sticky header z backdrop blur:

```jsx
<header className="
  fixed top-0 left-0 right-0 z-50
  bg-[#0a0e1a]/80 backdrop-blur-md
  border-b border-white/5
">
  <nav className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
    {/* Logo */}
    {/* Desktop menu */}
    {/* Mobile hamburger */}
  </nav>
</header>
```

### Buttons

```jsx
// Primary CTA
<button className="
  px-6 py-3 bg-green-500 hover:bg-green-400
  text-black font-semibold rounded-lg
  transition-all duration-300
  hover:scale-105 hover:shadow-[0_0_30px_rgba(0,255,157,0.3)]
">
  Primary Action
</button>

// Secondary/Outline
<button className="
  px-6 py-3 border border-green-500 text-green-500
  hover:bg-green-500/10 rounded-lg
  transition-all duration-300
">
  Secondary Action
</button>

// Ghost/Link
<a className="text-gray-400 hover:text-green-400 transition-colors">
  Link Text
</a>
```

## Integration with Architecture

### Directory Structure

Place components in correct directories:

| Type | Directory | Example |
|------|-----------|---------|
| Layout | `src/components/layout/` | Navigation, Footer, Layout |
| Sections | `src/components/sections/` | Hero, About, Projects, Skills, Contact |
| UI | `src/components/ui/` | CookieBanner, Breadcrumbs, Card |
| Animations | `src/components/animations/` | NetworkBackground |
| SEO | `src/components/seo/` | SEO, StructuredData |
| Pages | `src/pages/` | Home, Blog, BlogPostPage |

### Required Imports

```jsx
// Animation
import { motion } from 'framer-motion';

// SEO (for pages)
import { Helmet } from 'react-helmet-async';

// Routing
import { Link, useNavigate } from 'react-router-dom';

// Icons
import { FaGithub, FaLinkedin, FaTwitter } from 'react-icons/fa';

// Constants
import { SITE_CONFIG } from '../utils/constants';
```

### SEO Requirements

Kazda nowa strona musi miec:

```jsx
<Helmet>
  <title>Page Title - {SITE_CONFIG.name}</title>
  <meta name="description" content="..." />
  <meta property="og:title" content="..." />
  <meta property="og:description" content="..." />
  <meta property="og:image" content={`${SITE_CONFIG.url}/images/og/page.webp`} />
  <link rel="canonical" href={`${SITE_CONFIG.url}/page-slug`} />
</Helmet>
```

Nowe routes musza byc dodane do:
- `src/App.jsx` - routing
- `scripts/prerender.mjs` - prerendering dla SEO
- `public/sitemap.xml` - sitemap

## Resources

### References

Szczegolowe specyfikacje znajduja sie w:

- **[design-tokens.md](references/design-tokens.md)** - Kompletna paleta kolorow, typografia, spacing, shadows
- **[animation-patterns.md](references/animation-patterns.md)** - Framer Motion variants, CSS transitions, scroll effects
- **[accessibility-checklist.md](references/accessibility-checklist.md)** - WCAG 2.1 AA checklist

### Templates

Gotowe szablony do kopiowania:

- **[section-component.jsx](assets/templates/section-component.jsx)** - Szablon sekcji homepage
- **[page-component.jsx](assets/templates/page-component.jsx)** - Szablon nowej strony/route
- **[card-component.jsx](assets/templates/card-component.jsx)** - Szablon karty glassmorphism

### Project Documentation

Pelna dokumentacja projektu:

- `docs/portfolio/SRS.md` - Specyfikacja techniczna
- `docs/portfolio/PRD.md` - Wymagania produktowe
- `docs/portfolio/blog/BLOG_WORKFLOW.md` - Workflow dla blogow

### Related Skills

- **portfolio-code-review** - Code review checklist dla portfolio
