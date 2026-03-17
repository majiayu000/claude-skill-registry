---
name: landing-page-guide
description: Comprehensive guide for creating effective landing pages using Next.js or React. This skill should be used when users request to create landing pages, marketing pages, or product pages that require the 11 essential elements for high-converting landing pages. Specifically designed for Next.js 14+ App Router with ShadCN UI components.
---

# Landing Page Guide

## Overview

This skill enables creation of professional, high-converting landing pages following the 11 essential elements framework from DESIGNNAS. It provides complete implementation patterns for Next.js 14+ and React with ShadCN UI integration, ensuring every landing page includes proper SEO optimization, accessibility standards, and conversion-focused design.

## When to Use This Skill

Use this skill when users request:
- Creation of landing pages, marketing pages, or product pages
- Next.js or React-based promotional websites
- Pages that need to convert visitors into customers
- Professional marketing pages with SEO optimization
- Landing pages following industry best practices

## The 11 Essential Elements Framework

Every effective landing page must include these 11 essential elements. These are based on DESIGNNAS's proven framework for high-converting landing pages:

1. **URL with Keywords** - SEO-optimized, descriptive URL structure
2. **Company Logo** - Brand identity placed prominently (top-left)
3. **SEO-Optimized Title and Subtitle** - Clear value proposition with keywords
4. **Primary CTA** - Main call-to-action button in hero section
5. **Social Proof** - Reviews, ratings, user statistics
6. **Images or Videos** - Visual demonstration of product/service
7. **Core Benefits/Features** - 3-6 key advantages with icons
8. **Customer Testimonials** - 4-6 authentic reviews with photos
9. **FAQ Section** - 5-10 common questions with accordion UI
10. **Final CTA** - Bottom call-to-action for second chance conversion
11. **Contact Information/Legal Pages** - Footer with complete information

**Critical:** All 11 elements must be included in every landing page. No exceptions.

For detailed explanations of each element, refer to `references/11-essential-elements.md`.

## Technology Stack Requirements

When creating landing pages, always use:

### Required Technologies
- **Next.js 14+** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **ShadCN UI** for all UI components

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

### Why ShadCN UI?
- **Accessibility**: WCAG-compliant components
- **Customizable**: Fully customizable with Tailwind CSS
- **Type-safe**: Written in TypeScript
- **Performance**: Copy only what you need, minimal bundle size
- **Consistency**: Built-in design system

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

### Step 1: Setup Metadata (SEO)

Always start with proper SEO metadata in `layout.tsx` or `page.tsx`:

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

### Step 2: Create Component Structure

Build components in this order to ensure proper flow:

1. **Header** with logo (Element 2)
2. **Hero** section with title, subtitle, primary CTA, and social proof (Elements 3-5)
3. **MediaSection** with product images/videos (Element 6)
4. **Benefits** section with 3-6 feature cards (Element 7)
5. **Testimonials** with customer reviews (Element 8)
6. **FAQ** with accordion (Element 9)
7. **FinalCTA** at bottom (Element 10)
8. **Footer** with contact and legal links (Element 11)

### Step 3: Use ShadCN UI Components

Map each section to appropriate ShadCN components:

- **Hero CTA**: Use `Button` component with size="lg"
- **Benefits**: Use `Card`, `CardHeader`, `CardTitle`, `CardContent`
- **Testimonials**: Use `Card`, `Avatar`, `Badge`
- **FAQ**: Use `Accordion`, `AccordionItem`, `AccordionTrigger`, `AccordionContent`
- **Final CTA**: Use `Button` and `Card`
- **Footer**: Use `Separator`, `Input` for newsletter

### Step 4: Implement Responsive Design

Ensure mobile-first responsive design:

- Use Tailwind responsive prefixes: `sm:`, `md:`, `lg:`, `xl:`
- Test all breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- Minimum touch target size: 44x44px for buttons
- Base font size: minimum 16px on mobile

### Step 5: Optimize Performance

- Use Next.js `Image` component for all images
- Add `priority` prop to above-the-fold images
- Implement lazy loading for below-the-fold content
- Use dynamic imports for heavy components if needed

### Step 6: Ensure Accessibility

- Use semantic HTML5 elements (`<header>`, `<main>`, `<section>`, `<footer>`)
- Add ARIA labels where needed
- Ensure keyboard navigation works
- Provide alt text for all images
- Maintain sufficient color contrast (WCAG AA minimum)

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

Before completing any landing page, verify:

**11 Essential Elements:**
- [ ] 1. URL with keywords
- [ ] 2. Company logo (top-left)
- [ ] 3. SEO-optimized title and subtitle
- [ ] 4. Primary CTA in hero
- [ ] 5. Social proof (reviews, stats)
- [ ] 6. Images or videos
- [ ] 7. Benefits/features section (3-6 items)
- [ ] 8. Customer testimonials (4-6 items)
- [ ] 9. FAQ section (5-10 questions)
- [ ] 10. Final CTA at bottom
- [ ] 11. Footer with contact and legal links

**Technical Requirements:**
- [ ] Next.js 14+ with App Router
- [ ] TypeScript types defined
- [ ] Tailwind CSS styling
- [ ] ShadCN UI components used
- [ ] Metadata configured for SEO
- [ ] Images optimized with Next.js Image
- [ ] Responsive design implemented
- [ ] Accessibility standards met
- [ ] Performance optimized

## Best Practices

### Content Guidelines
- Write clear, benefit-focused copy
- Use action-oriented language in CTAs
- Keep sections scannable with proper headings
- Include specific numbers and statistics
- Use authentic testimonials with real names

### Design Guidelines
- Maintain visual hierarchy throughout
- Use consistent color palette
- Ensure adequate whitespace
- Choose readable fonts (16px+ base size)
- Design for mobile-first

### SEO Optimization
- Include keywords naturally in content
- Use proper heading tag structure (H1 → H2 → H3)
- Add alt text to all images
- Optimize page load speed
- Create descriptive meta tags

### Conversion Optimization
- Place CTAs strategically (hero + bottom minimum)
- Reduce friction in user journey
- Highlight trust signals prominently
- Use contrasting colors for CTAs
- Test different CTA copy variations

## Common Patterns

### SaaS Product Landing Page
Focus on: Free trial CTA, feature comparisons, pricing clarity, security badges

### E-commerce Product Landing Page
Focus on: Product images, pricing, shipping info, return policy, urgency

### Service/Agency Landing Page
Focus on: Portfolio/case studies, process explanation, team credentials, contact form

### Event/Webinar Landing Page
Focus on: Date/time prominence, speaker profiles, agenda, registration form, countdown timer

## Resources

### references/
This skill includes detailed reference documentation:

- `11-essential-elements.md` - In-depth explanation of each of the 11 essential elements with principles, implementation tips, and examples
- `component-examples.md` - Complete, production-ready component code using ShadCN UI for all major sections

Load these references as needed when implementing specific sections or when you need detailed guidance on any element.

## Notes

- This framework is based on DESIGNNAS's "11 Essential Landing Page Elements"
- Adapt to brand guidelines and target audience as needed
- Use A/B testing to continuously improve conversion rates
- All implementations should prioritize user experience and conversion optimization
