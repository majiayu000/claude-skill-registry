---
name: landing-page-guide-v2
description: Create distinctive, high-converting landing pages that combine proven conversion elements with exceptional design quality. Build beautiful, memorable landing pages using Next.js 14+ and ShadCN UI that avoid generic AI aesthetics while following the 11 essential elements framework.
---

# Landing Page Guide V2

## Overview

This skill enables creation of **distinctive, high-converting landing pages** that combine:
- **Proven Conversion Framework**: 11 essential elements from DESIGNNAS for high conversion rates
- **Exceptional Design Quality**: Bold aesthetic choices that create unforgettable brand experiences
- **Production-Ready Code**: Next.js 14+ with ShadCN UI, TypeScript, and performance optimization

**Philosophy**: A landing page must convert visitors AND make them remember your brand. Generic, template-looking pages fail at both. This skill ensures your landing pages are functionally effective and visually extraordinary.

## When to Use This Skill

Use this skill when users request:
- Creation of landing pages, marketing pages, or product pages
- Next.js or React-based promotional websites
- Pages that need to convert visitors into customers AND stand out visually
- Professional marketing pages with exceptional design quality
- Landing pages that avoid generic "template" aesthetics
- Brand experiences that are both conversion-optimized and memorable

## Design Thinking: Before You Code

Before implementing any landing page, commit to a **BOLD aesthetic direction** that aligns with the brand and product:

### 1. Understand Context
- **Purpose**: What problem does this product solve? Who is the target audience?
- **Brand Personality**: Is this brand playful, professional, luxury, minimalist, bold, technical?
- **Industry**: What visual language does this industry expect (or should we break)?
- **Differentiation**: What makes this brand unforgettable? What's the ONE thing visitors will remember?

### 2. Choose an Aesthetic Direction

Pick an extreme direction and commit fully. Examples:

**Minimalist & Refined**
- Brutally clean layouts, generous whitespace
- Sophisticated typography with large scale contrasts
- Monochromatic or limited color palette (2-3 colors max)
- Subtle micro-interactions, elegant transitions
- Examples: Luxury products, professional services, premium SaaS

**Bold & Maximalist**
- Rich, complex visual layers
- Dynamic animations and scroll effects
- Gradient meshes, textures, and overlapping elements
- Vibrant color palettes with high contrast
- Examples: Creative agencies, entertainment, youth brands

**Retro-Futuristic**
- Nostalgic elements with modern execution
- Geometric patterns, neon accents
- Glitch effects, scanlines, grain textures
- Monospace or display fonts with character
- Examples: Gaming, tech startups, creative tools

**Organic & Natural**
- Soft, flowing shapes and gradients
- Nature-inspired colors (earth tones, pastels)
- Smooth animations mimicking natural motion
- Rounded corners, soft shadows
- Examples: Wellness, sustainability, food

**Editorial & Magazine**
- Strong typographic hierarchy
- Grid-breaking asymmetric layouts
- Large, impactful imagery
- Bold use of whitespace and negative space
- Examples: Content platforms, media, education

**Brutalist & Raw**
- Unconventional layouts, intentional "ugly"
- System fonts or deliberately basic typography
- High contrast, limited color
- Minimal or no animations
- Examples: Art, fashion, anti-establishment brands

**CRITICAL**: Choose ONE clear direction. Bold maximalism and refined minimalism both work - the key is **intentionality**, not intensity. Execute your chosen direction with precision and consistency across all 11 elements.

### 3. Define Your Design System

Before coding, define these core decisions:

**Typography Choices**
- **Display Font**: Choose something distinctive and memorable (NOT Inter, Roboto, Arial, or system fonts)
  - Consider: Space Grotesk, Clash Display, Cabinet Grotesk, Syne, DM Serif Display, Zodiak, Fraunces, Archivo Black, Unbounded, Outfit
  - Or use Google Fonts wisely: Playfair Display, Crimson Pro, Libre Baskerville, Epilogue, Plus Jakarta Sans
  - **NEVER** converge on common choices - vary fonts across different projects
- **Body Font**: Refined, readable choice that complements display font
  - Consider: DM Sans, General Sans, Switzer, Geist, Manrope, Karla, Work Sans
- **Scale**: Establish clear hierarchy (e.g., H1: 4rem → H2: 3rem → H3: 2rem → Body: 1rem)

**Color Palette**
- **Dominant Color**: Your primary brand color (60% usage)
- **Accent Color**: High-contrast color for CTAs (10% usage)
- **Neutral Palette**: Grays or earth tones (30% usage)
- **Background Strategy**: Solid, gradient, texture, or pattern?
- Define as CSS variables for consistency

**Motion Strategy**
- **Page Load**: Staggered reveals with animation-delay for hero elements
- **Scroll Interactions**: Fade-ups, parallax, or scroll-triggered animations?
- **Hover States**: Subtle scale, color shift, or dramatic transformations?
- **CTA Animations**: How do buttons attract attention without being annoying?

**Spatial Approach**
- **Layout Style**: Centered and symmetric? Asymmetric and dynamic? Grid-breaking?
- **Spacing System**: Tight and dense? Generous and airy?
- **Section Flow**: Traditional stacked? Diagonal? Overlapping?

## The 11 Essential Elements Framework

Every effective landing page must include these 11 essential elements. These are based on DESIGNNAS's proven framework for high-converting landing pages.

**Each element has TWO requirements:**
1. **Functional requirement** (for conversion) - Must be included
2. **Design excellence** (for memorability) - Must be distinctive and beautiful

### Element-by-Element Design Guide

#### 1. URL with Keywords
**Functional**: SEO-optimized, descriptive URL structure
**Design**: N/A (SEO-focused)

#### 2. Company Logo (Header)
**Functional**: Brand identity placed prominently (top-left)
**Design Excellence**:
- Consider animated logo on page load
- Sticky header with smooth scroll transitions
- Logo mark variation for different scroll states
- Header background: transparent → solid with backdrop blur
- Navigation typography that matches your display font choice

#### 3. SEO-Optimized Title and Subtitle (Hero)
**Functional**: Clear value proposition with keywords
**Design Excellence**:
- **Typography**: Make this MASSIVE and unforgettable (4rem-6rem+)
- Use your distinctive display font here
- Consider gradient text, outlined text, or text shadows for impact
- Animate title words with staggered fade-in (animation-delay)
- Subtitle should be 50% the size of title, different weight or font
- Add visual rhythm with line breaks and spacing

#### 4. Primary CTA (Hero)
**Functional**: Main call-to-action button in hero section
**Design Excellence**:
- Make it IMPOSSIBLE to miss: size, color contrast, position
- Avoid boring rectangles: consider pill shapes, unique borders, or geometric shapes
- Add micro-interactions: hover scale, shadow expansion, color shift
- Consider dual CTAs with primary/secondary hierarchy
- Entrance animation that draws the eye (delay after title)
- Add visual cues: arrows, icons, or pulsing effects

#### 5. Social Proof (Hero)
**Functional**: Reviews, ratings, user statistics
**Design Excellence**:
- Numbers should be HUGE and animated on load (count-up effect)
- Statistics cards with gradient backgrounds or subtle borders
- Customer avatars in overlapping circles
- Star ratings with custom styling (not default yellow stars)
- "As featured in" logos with proper spacing and opacity treatment
- Consider rotating testimonials or animated social proof carousel

#### 6. Images or Videos (Media Section)
**Functional**: Visual demonstration of product/service
**Design Excellence**:
- **CRITICAL**: Never use placeholder or generic images
- Product screenshots with device mockups (laptop/phone frames)
- Add depth: shadows, reflections, 3D tilt effects
- Consider: Floating screenshots, parallax scroll effects, video backgrounds
- Image reveal animations on scroll (fade-up, slide-in)
- For videos: Custom play button design, ambient background glow
- Grid layouts: Asymmetric, overlapping, or bento box style

#### 7. Core Benefits/Features
**Functional**: 3-6 key advantages with icons
**Design Excellence**:
- **Icons**: Custom designed or carefully selected (NOT generic line icons)
- Consider: Gradient fills, animated icons on hover, 3D-style illustrations
- Card design variations: glassmorphism, neumorphism, gradient borders, subtle shadows
- Staggered animation as user scrolls to this section
- Asymmetric layout instead of boring 3-column grid
- Background elements: subtle patterns, gradients, or decorative shapes
- Typography: Feature titles in your display font, bold and prominent

#### 8. Customer Testimonials
**Functional**: 4-6 authentic reviews with photos
**Design Excellence**:
- Photo treatment: Circular avatars with gradient borders or unique shapes
- Card backgrounds: Subtle gradients, frosted glass, or elevated shadows
- Quote marks: Oversized, decorative, or custom styled
- Layout: Masonry grid, carousel, or staggered vertical
- Rating stars: Custom colors matching brand palette
- Hover effects: Lift up, expand, or glow
- Customer names and titles: Refined typography

#### 9. FAQ Section
**Functional**: 5-10 common questions with accordion UI
**Design Excellence**:
- Accordion animations: Smooth expand/collapse with easing
- Icons: Custom chevrons or plus/minus signs with rotation
- Hover states on questions
- Typography: Questions in bold or different font weight
- Consider: Two-column layout on desktop, side-by-side Q&A pairs
- Background: Subtle color shift from previous section
- Spacing: Generous padding inside accordion items

#### 10. Final CTA
**Functional**: Bottom call-to-action for second chance conversion
**Design Excellence**:
- **Make it a HERO moment**: This is the last chance
- Full-width section with dramatic background (gradient, pattern, or color)
- CTA button even BIGGER than hero CTA
- Add urgency: Countdown timers, limited spots, scarcity indicators
- Surround with compelling copy and micro-benefits
- Animation: Parallax background, floating elements, or scroll-triggered effects
- Consider: Email input + button combo for newsletter/waitlist

#### 11. Contact Information/Legal Pages (Footer)
**Functional**: Footer with complete information, legal links
**Design Excellence**:
- Multi-column layout with clear information hierarchy
- Social icons: Hover effects (color shift, scale, or rotate)
- Newsletter signup: Styled input with inline button
- Typography: Smaller but still readable (14-16px)
- Background: Darker than body or distinct color
- Separator from content: Subtle gradient line or decorative divider
- Bottom bar: Copyright and legal links with proper spacing

**Critical:** All 11 elements must be included in every landing page. No exceptions.

For detailed explanations of each element, refer to `references/11-essential-elements.md`.

## Design Aesthetics Guidelines

### Typography Excellence
- **NEVER** use generic fonts: Inter, Roboto, Arial, Helvetica, system-ui
- **Display fonts** should be distinctive and memorable
- **Pair wisely**: Display font for headings + refined body font for text
- **Scale dramatically**: Create clear hierarchy with size jumps (not subtle differences)
- **Letter spacing**: Adjust for display fonts (often needs tighter tracking)
- **Line height**: Display = 1.1-1.2, Body = 1.6-1.8

### Color & Visual Coherence
- **Define CSS variables** for all colors (maintain consistency)
- **Dominant color** should appear throughout (not just CTAs)
- **Accent colors** must have sufficient contrast for accessibility (WCAG AA minimum)
- **Avoid**: Purple gradients on white (overused AI aesthetic)
- **Backgrounds**: Create atmosphere with gradients, meshes, patterns, or textures
  - Gradient meshes: Multi-color smooth gradients
  - Noise textures: Subtle grain for depth
  - Geometric patterns: Dots, lines, or shapes at low opacity
  - Layered transparencies: Overlapping colored sections

### Motion & Animation
- **Page load**: One well-orchestrated entrance with staggered reveals
  - Hero title words fade in sequentially (animation-delay: 0ms, 100ms, 200ms)
  - Subtitle follows (delay: 300ms)
  - CTA appears last (delay: 500ms) with emphasis
- **Scroll animations**: Sections fade up as they enter viewport
  - Use Intersection Observer API or Framer Motion's scroll triggers
  - Cards stagger in (each with incremental delay)
- **Hover states**: Surprise and delight
  - Buttons: Scale up, shadow expand, color shift
  - Cards: Lift effect with shadow
  - Images: Subtle zoom or parallax
- **Performance**: Prefer CSS animations over JavaScript
  - Use `transform` and `opacity` (GPU-accelerated)
  - Avoid animating `width`, `height`, `top`, `left`

### Spatial Composition & Layout
- **Break the grid**: Don't default to centered, symmetric layouts
- **Asymmetry**: One side larger text, other side visual
- **Overlapping elements**: Layer sections for depth
- **Diagonal flow**: Angled dividers between sections
- **Generous whitespace** OR controlled density (pick one and commit)
- **Z-axis thinking**: Use shadows, blur, and layering for depth

### AVOID Generic AI Aesthetics
These patterns make landing pages look "AI-generated" and forgettable:

**DON'T:**
- ❌ Inter/Roboto/Arial fonts
- ❌ Purple gradients on white backgrounds
- ❌ Perfectly centered, symmetric layouts every time
- ❌ Generic line icons
- ❌ Default yellow star ratings
- ❌ Boring rectangular buttons with no personality
- ❌ White background with no visual interest
- ❌ Cookie-cutter three-column feature grids
- ❌ Stock photos of people pointing at laptops

**DO:**
- ✅ Choose distinctive fonts that match brand personality
- ✅ Commit to a unique color palette (not always purple!)
- ✅ Create unexpected layouts with asymmetry
- ✅ Design or select characterful icons
- ✅ Custom-style all UI elements to match aesthetic
- ✅ Add background textures, gradients, or patterns
- ✅ Vary layouts across sections
- ✅ Use product screenshots, custom illustrations, or authentic photography

## Technology Stack Requirements

When creating landing pages, always use:

### Required Technologies
- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **ShadCN UI** for all UI components (customize heavily!)
- **Framer Motion** (optional) for advanced animations

### ShadCN UI Components to Install

Before creating any landing page, ensure these components are installed:

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add accordion
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add avatar
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add input
```

**IMPORTANT**: ShadCN components are STARTING POINTS, not final designs. Customize them heavily:
- Modify default styles in component files
- Add custom variants in Tailwind config
- Override with className props
- Create wrapper components for brand-specific styling

### Why ShadCN UI?
- **Accessibility**: WCAG-compliant components (maintain this!)
- **Customizable**: Fully customizable with Tailwind CSS (leverage this!)
- **Type-safe**: Written in TypeScript
- **Performance**: Copy only what you need, minimal bundle size
- **Ownership**: You own the code, modify freely

## Project Structure

Create landing pages with this structure:

```
landing-page/
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Main landing page
│   └── globals.css         # Global styles
├── components/
│   ├── Header.tsx          # Logo & Navigation (Element 2)
│   ├── Hero.tsx            # Title, CTA, Social Proof (Elements 3-5)
│   ├── MediaSection.tsx    # Images/Videos (Element 6)
│   ├── Benefits.tsx        # Core Benefits (Element 7)
│   ├── Testimonials.tsx    # Customer Reviews (Element 8)
│   ├── FAQ.tsx             # FAQ Accordion (Element 9)
│   ├── FinalCTA.tsx        # Bottom CTA (Element 10)
│   └── Footer.tsx          # Contact & Legal (Element 11)
├── public/
│   └── images/             # Optimized images
└── package.json
```

## Implementation Workflow

### Step 1: Design First (CRITICAL)
**Before writing ANY code**, complete the Design Thinking section:
1. Understand the brand, audience, and purpose
2. Choose your aesthetic direction (minimalist, maximalist, retro, etc.)
3. Define your design system:
   - Display font + body font
   - Color palette (dominant, accent, neutral)
   - Motion strategy (page load, scroll, hover)
   - Spatial approach (layout style, spacing)

Document these decisions in comments at the top of your main component file.

### Step 2: Setup Design System (CSS Variables)

Create `globals.css` or `app.css` with your design system:

```css
@import url('https://fonts.googleapis.com/css2?family=Your+Display+Font&family=Your+Body+Font&display=swap');

:root {
  /* Typography */
  --font-display: 'Your Display Font', sans-serif;
  --font-body: 'Your Body Font', sans-serif;

  /* Colors */
  --color-primary: #your-dominant-color;
  --color-accent: #your-accent-color;
  --color-neutral: #your-neutral-color;
  --color-background: #your-bg-color;

  /* Spacing */
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 2rem;
  --spacing-lg: 4rem;
  --spacing-xl: 6rem;

  /* Animation timing */
  --duration-fast: 150ms;
  --duration-medium: 300ms;
  --duration-slow: 500ms;
  --easing: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Apply fonts */
h1, h2, h3, h4, h5, h6 {
  font-family: var(--font-display);
}

body {
  font-family: var(--font-body);
}
```

Update `tailwind.config.ts` to use your design system:

```typescript
export default {
  theme: {
    extend: {
      fontFamily: {
        display: ['var(--font-display)'],
        body: ['var(--font-body)'],
      },
      colors: {
        primary: 'var(--color-primary)',
        accent: 'var(--color-accent)',
        // ... etc
      },
    },
  },
}
```

### Step 3: Setup Metadata (SEO)

Configure proper SEO metadata in `layout.tsx` or `page.tsx`:

```typescript
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'SEO Optimized Title with Keywords | Brand Name',
  description: 'Compelling description with main keywords',
  keywords: ['keyword1', 'keyword2', 'keyword3'],
  openGraph: {
    title: 'OG Title',
    description: 'OG Description',
    images: ['/og-image.jpg'],
  },
}
```

### Step 4: Create Component Structure with Design

Build components in this order, applying your aesthetic direction to each:

1. **Header** - Sticky navigation with smooth transitions
2. **Hero** - MASSIVE typography, staggered animations, bold CTA
3. **MediaSection** - Showcase with depth (shadows, 3D effects)
4. **Benefits** - Asymmetric layout, custom icons, animated on scroll
5. **Testimonials** - Unique card design, custom avatars
6. **FAQ** - Smooth accordion with custom styling
7. **FinalCTA** - Dramatic full-width section
8. **Footer** - Multi-column with refined typography

### Step 5: Customize ShadCN Components

Map sections to ShadCN components and **customize heavily**:

**Hero CTA Example:**
```tsx
<Button
  size="lg"
  className="bg-accent hover:bg-accent/90 text-white px-12 py-6 text-xl font-display rounded-full shadow-2xl hover:shadow-accent/50 hover:scale-105 transition-all duration-300"
>
  Get Started →
</Button>
```

**Benefits Card Example:**
```tsx
<Card className="border-2 border-primary/10 hover:border-primary/30 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 bg-gradient-to-br from-white to-primary/5">
  {/* Custom content */}
</Card>
```

### Step 6: Implement Animations

Add entrance animations and scroll effects:

```tsx
// Hero title with staggered animation
<h1 className="text-6xl font-display font-bold">
  <span className="inline-block animate-fade-in" style={{ animationDelay: '0ms' }}>
    Beautiful
  </span>{' '}
  <span className="inline-block animate-fade-in" style={{ animationDelay: '100ms' }}>
    Landing
  </span>{' '}
  <span className="inline-block animate-fade-in" style={{ animationDelay: '200ms' }}>
    Pages
  </span>
</h1>

// Add to globals.css
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in var(--duration-slow) var(--easing) both;
}
```

For scroll animations, use Intersection Observer or Framer Motion.

### Step 7: Implement Responsive Design

Ensure mobile-first responsive design with brand consistency:

- Use Tailwind responsive prefixes: `sm:`, `md:`, `lg:`, `xl:`
- Test all breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- Minimum touch target size: 44x44px for buttons
- Base font size: minimum 16px on mobile
- **Maintain design system** across breakpoints (colors, fonts stay consistent)
- Adjust layouts: Stack on mobile, side-by-side on desktop

### Step 8: Optimize Performance

- Use Next.js `Image` component for all images
- Add `priority` prop to above-the-fold images (hero section)
- Implement lazy loading for below-the-fold content
- Optimize fonts: Use `font-display: swap` for web fonts
- Use CSS animations over JavaScript when possible
- Minimize bundle size: Tree-shake unused ShadCN components

### Step 9: Ensure Accessibility

- Use semantic HTML5 elements (`<header>`, `<main>`, `<section>`, `<footer>`)
- Add ARIA labels for icon-only buttons
- Ensure keyboard navigation works (test with Tab key)
- Provide descriptive alt text for all images
- Maintain sufficient color contrast (WCAG AA minimum: 4.5:1 for text)
- Test animations for users who prefer reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Component Examples

For complete, production-ready component implementations using ShadCN UI, refer to `references/component-examples.md`.

This reference file includes:
- Hero section with Button, Badge, and Image optimization
- Benefits section with Card components
- Testimonials with Avatar and Card
- FAQ with Accordion
- Final CTA with Card and Button
- Footer with Separator and links

Load this reference when implementing components to follow best practices.

## Validation Checklist

Before completing any landing page, verify ALL items:

### Design Quality ⭐
- [ ] **Aesthetic direction chosen** and executed consistently
- [ ] **Typography**: Distinctive display font (NOT Inter/Roboto/Arial)
- [ ] **Typography**: Clear hierarchy with dramatic scale differences
- [ ] **Color palette**: Defined CSS variables, cohesive throughout
- [ ] **Backgrounds**: NOT plain white - has texture/gradient/pattern
- [ ] **Animations**: Staggered page load, scroll-triggered reveals
- [ ] **Layout**: Not generic centered grid - has unique composition
- [ ] **ShadCN customization**: Components heavily customized, not default
- [ ] **NO generic AI aesthetics**: Passes the "does this look AI-generated?" test

### 11 Essential Elements (Conversion) ✅
- [ ] 1. URL with keywords
- [ ] 2. Company logo (top-left, animated)
- [ ] 3. SEO-optimized title and subtitle (MASSIVE typography)
- [ ] 4. Primary CTA in hero (distinctive design, micro-interactions)
- [ ] 5. Social proof (reviews, stats, animated)
- [ ] 6. Images or videos (with depth effects, not placeholders)
- [ ] 7. Benefits/features section (3-6 items, custom icons, unique layout)
- [ ] 8. Customer testimonials (4-6 items, styled cards)
- [ ] 9. FAQ section (5-10 questions, smooth accordion)
- [ ] 10. Final CTA at bottom (dramatic, full-width)
- [ ] 11. Footer with contact and legal links (multi-column, refined)

### Technical Requirements 🔧
- [ ] Next.js 14+ with App Router
- [ ] TypeScript types defined
- [ ] Tailwind CSS styling
- [ ] ShadCN UI components installed and customized
- [ ] Metadata configured for SEO (title, description, OG tags)
- [ ] Images optimized with Next.js Image component
- [ ] Responsive design implemented (mobile-first)
- [ ] Accessibility standards met (WCAG AA)
- [ ] Performance optimized (lazy loading, font optimization)
- [ ] Reduced motion support for animations

### Final Polish 💎
- [ ] All fonts loaded correctly (check browser DevTools)
- [ ] Color contrast tested (use browser DevTools)
- [ ] Tested on mobile, tablet, desktop
- [ ] Keyboard navigation works
- [ ] Hover states feel delightful
- [ ] No Lorem Ipsum or placeholder content
- [ ] Brand feels unique and memorable

## Best Practices

### Design-First Approach
- **Always start with design thinking** before coding
- Document your aesthetic direction in comments
- Create a mood board or reference images before implementing
- Don't default to "safe" choices - push creative boundaries
- Remember: Conversions come from trust, and trust comes from professionalism + distinctiveness

### Content Guidelines
- Write clear, benefit-focused copy that matches your brand voice
- Use action-oriented language in CTAs (verb + benefit)
- Keep sections scannable with proper headings
- Include specific numbers and statistics (builds credibility)
- Use authentic testimonials with real names and photos
- **Match tone to aesthetic**: Playful design → playful copy, Professional design → authoritative copy

### Typography Best Practices
- **Never compromise on typography** - it's 80% of design
- Use display fonts at large sizes (4rem+) where they shine
- Maintain consistent line heights across sections
- Use font weights strategically (light for elegance, bold for impact)
- Test readability on actual devices, not just dev tools
- Load fonts efficiently: Only weights you actually use

### Color & Visual Consistency
- Define ALL colors as CSS variables upfront
- Use your primary color in at least 3-4 places (not just logo)
- Accent color should be high contrast and used sparingly
- Test color contrast with browser DevTools or online checkers
- Dark text on light backgrounds should be near-black (#1a1a1a), not pure black
- Consider color psychology: Blue = trust, Green = growth, Red = urgency, Purple = creativity

### Animation & Motion Guidelines
- **Less is more**: One great page entrance > scattered micro-animations
- Use `animation-delay` to create rhythm and flow
- Respect `prefers-reduced-motion` - always
- Test on actual devices - animations feel different on 60Hz vs 120Hz screens
- Avoid animations that distract from CTAs
- Use easing functions: `cubic-bezier(0.4, 0, 0.2, 1)` is smooth and professional

### SEO Optimization
- Include keywords naturally in H1, H2, and first paragraph
- Use proper heading tag structure (H1 → H2 → H3), only one H1
- Add descriptive alt text to all images (SEO + accessibility)
- Optimize page load speed (Core Web Vitals matter)
- Create compelling meta tags that encourage clicks
- Schema markup for business/product info

### Conversion Optimization
- **Primary CTA**: Above the fold, impossible to miss
- **Final CTA**: Last chance conversion, make it dramatic
- Reduce friction: Minimize form fields, clear value proposition
- Highlight trust signals: Reviews, testimonials, "As seen in" logos
- Use contrasting colors for CTAs (should stand out)
- Test CTA copy variations: "Start Free Trial" vs "Try Free for 14 Days"
- Add urgency where appropriate: Limited spots, time-sensitive offers
- Show human faces: Testimonials with real photos convert better

### Performance Best Practices
- Optimize images: WebP format, proper sizing, lazy loading
- Font loading strategy: `font-display: swap` to avoid FOIT (Flash of Invisible Text)
- Minimize JavaScript: Use CSS animations when possible
- Code splitting: Dynamic imports for heavy components
- Prefetch critical resources
- Target: LCP < 2.5s, FID < 100ms, CLS < 0.1

## Common Patterns & Aesthetic Recommendations

Each landing page type has different conversion goals AND can express unique aesthetics:

### SaaS Product Landing Page
**Conversion Focus**: Free trial CTA, feature comparisons, pricing clarity, security badges
**Aesthetic Recommendations**:
- **Minimalist & Professional**: Clean layout, lots of whitespace, sophisticated typography
- **Tech-Forward**: Gradient backgrounds, subtle animations, modern sans-serif fonts
- **Bold & Confident**: Large typography, high-contrast CTAs, dynamic hover states
**Avoid**: Generic blue gradients, stock photos of laptops in coffee shops

### E-commerce Product Landing Page
**Conversion Focus**: Product images, pricing, shipping info, return policy, urgency
**Aesthetic Recommendations**:
- **Luxury/Premium**: Elegant serif fonts, monochrome palette, generous whitespace
- **Energetic/Youth**: Bold colors, playful fonts, dynamic layouts, vibrant CTAs
- **Natural/Sustainable**: Earth tones, organic shapes, soft shadows, rounded corners
**Avoid**: Cluttered layouts, too many competing visual elements

### Service/Agency Landing Page
**Conversion Focus**: Portfolio/case studies, process explanation, team credentials, contact form
**Aesthetic Recommendations**:
- **Creative/Bold**: Asymmetric layouts, unique typography, portfolio as hero
- **Editorial**: Magazine-style layouts, large imagery, strong typographic hierarchy
- **Minimalist/Portfolio**: Grid of work, minimal text, let work speak for itself
**Avoid**: Generic "professional" templates, stock photography

### Event/Webinar Landing Page
**Conversion Focus**: Date/time prominence, speaker profiles, agenda, registration form, countdown timer
**Aesthetic Recommendations**:
- **Exciting/Dynamic**: Animated countdown, gradient backgrounds, energetic colors
- **Professional/Conference**: Clean layout, speaker headshots with borders, agenda timeline
- **Community/Friendly**: Warm colors, circular avatars, social proof emphasis
**Avoid**: Boring bullet-point agendas, generic conference aesthetics

### Mobile App Landing Page
**Conversion Focus**: App Store badges, screenshots in device frames, feature highlights, demo video
**Aesthetic Recommendations**:
- **Modern/Sleek**: Device mockups with 3D tilt, floating screenshots, smooth animations
- **Playful/Fun**: Bright colors, illustrated icons, character mascots
- **Screenshot-Forward**: Large phone mockups as hero, minimal text, visual storytelling
**Avoid**: Tiny screenshots, generic app icons

## Resources

### references/
This skill includes detailed reference documentation:

- `11-essential-elements.md` - In-depth explanation of each of the 11 essential elements with principles, implementation tips, and examples
- `component-examples.md` - Complete, production-ready component code using ShadCN UI for all major sections

Load these references as needed when implementing specific sections or when you need detailed guidance on any element.

## Notes & Philosophy

### Core Principles
1. **Conversion + Memorability**: A landing page must both convert and be memorable
2. **Intentional Design**: Every aesthetic choice should be deliberate, not default
3. **No Generic AI Aesthetics**: Avoid the "AI-generated" look that makes brands forgettable
4. **Design System First**: Define fonts, colors, motion before coding
5. **Customize Everything**: ShadCN is a starting point, not the final design

### Framework Origins
- **11 Essential Elements** based on DESIGNNAS's proven conversion framework
- **Design Excellence** principles adapted from high-quality frontend design practices
- Combined to create landing pages that are functionally effective AND visually extraordinary

### Adaptation Guidelines
- Adapt to specific brand guidelines and target audience
- Use A/B testing to continuously improve conversion rates
- Balance conversion optimization with creative expression
- When in doubt, be bold - generic pages don't convert OR impress

### Success Metrics
**Conversion metrics:**
- Click-through rate on CTAs
- Form submission rate
- Scroll depth (are users reaching all 11 elements?)
- Bounce rate and time on page

**Brand metrics:**
- User feedback on design quality
- Social sharing of the landing page
- Brand recall in user surveys
- Differentiation from competitors

### Remember
Every landing page is an opportunity to make an unforgettable first impression. The 11 essential elements ensure conversions. Exceptional design ensures they remember your brand. Never sacrifice one for the other.

**The best landing pages convert AND inspire.**
