---
name: brand-designer
description: Expert in brand identity, logo design, and visual brand systems
version: 1.0.0
tags: [branding, logo-design, identity, visual-identity, brand-guidelines]
---

# Brand Designer Skill

I help you create cohesive brand identities, logos, and visual brand systems.

## What I Do

**Brand Identity:**

- Logo design and variations
- Color palettes
- Typography systems
- Brand guidelines

**Visual Assets:**

- Business cards, letterheads
- Social media templates
- Marketing materials
- Brand presentation decks

**Brand Strategy:**

- Brand positioning
- Target audience definition
- Competitor analysis
- Brand voice and tone

## Logo Design Process

### Step 1: Brand Discovery

**Questions to Answer:**

- What does the company do?
- Who is the target audience?
- What are the brand values?
- What feeling should the logo evoke?
- Any colors/symbols to avoid?

**Example Brief:**

```markdown
## Brand Brief: TechStart

**Industry:** SaaS, developer tools
**Target Audience:** Software developers, 25-40 years old
**Brand Values:** Innovation, simplicity, reliability
**Personality:** Modern, technical, approachable
**Competitors:** GitHub, GitLab, Vercel

**Logo Requirements:**

- Works in monochrome
- Scales from 16px (favicon) to billboard
- Modern, not trendy (should age well)
- Unique, memorable
```

---

### Step 2: Logo Concepts

**Concept 1: Wordmark**

```
Clean, modern typography
Focus on the company name
Example: Google, Facebook, Netflix
```

**Concept 2: Lettermark**

```
Initials in a distinctive way
Good for long company names
Example: IBM, HBO, CNN
```

**Concept 3: Icon + Wordmark**

```
Symbol + company name
Most versatile option
Example: Nike, Apple, Twitter
```

**Example SVG Logo (React Component):**

```typescript
// components/brand/Logo.tsx

interface LogoProps {
  variant?: 'full' | 'icon' | 'wordmark'
  color?: 'primary' | 'white' | 'black'
  size?: number
}

export function Logo({ variant = 'full', color = 'primary', size = 40 }: LogoProps) {
  const colors = {
    primary: '#0066CC',
    white: '#FFFFFF',
    black: '#000000'
  }

  const fillColor = colors[color]

  if (variant === 'icon') {
    return (
      <svg width={size} height={size} viewBox="0 0 40 40" fill="none">
        <circle cx="20" cy="20" r="18" fill={fillColor} />
        <path
          d="M15 20 L25 15 L25 25 Z"
          fill="white"
        />
      </svg>
    )
  }

  if (variant === 'wordmark') {
    return (
      <svg width={size * 4} height={size} viewBox="0 0 160 40" fill="none">
        <text
          x="0"
          y="30"
          fontFamily="Inter, sans-serif"
          fontSize="24"
          fontWeight="700"
          fill={fillColor}
        >
          TechStart
        </text>
      </svg>
    )
  }

  // Full logo (icon + wordmark)
  return (
    <svg width={size * 5} height={size} viewBox="0 0 200 40" fill="none">
      <circle cx="20" cy="20" r="18" fill={fillColor} />
      <path d="M15 20 L25 15 L25 25 Z" fill="white" />
      <text
        x="50"
        y="30"
        fontFamily="Inter, sans-serif"
        fontSize="24"
        fontWeight="700"
        fill={fillColor}
      >
        TechStart
      </text>
    </svg>
  )
}
```

**Usage:**

```typescript
// Different logo variations
<Logo variant="full" />
<Logo variant="icon" size={32} />
<Logo variant="wordmark" color="white" />
```

---

## Color Palette

### Primary Brand Colors

```typescript
// config/brand-colors.ts

export const brandColors = {
  // Primary (main brand color)
  primary: {
    50: '#E6F0FF',
    100: '#CCE0FF',
    200: '#99C2FF',
    300: '#66A3FF',
    400: '#3385FF',
    500: '#0066CC', // Main brand color
    600: '#0052A3',
    700: '#003D7A',
    800: '#002952',
    900: '#001429'
  },

  // Secondary (accent color)
  secondary: {
    50: '#FFF4E6',
    100: '#FFE9CC',
    200: '#FFD399',
    300: '#FFBD66',
    400: '#FFA733',
    500: '#FF9100', // Main accent
    600: '#CC7400',
    700: '#995700',
    800: '#663A00',
    900: '#331D00'
  },

  // Neutral (grays)
  neutral: {
    50: '#F9FAFB',
    100: '#F3F4F6',
    200: '#E5E7EB',
    300: '#D1D5DB',
    400: '#9CA3AF',
    500: '#6B7280',
    600: '#4B5563',
    700: '#374151',
    800: '#1F2937',
    900: '#111827'
  },

  // Semantic colors
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6'
}
```

### Color Usage Guidelines

```typescript
// Tailwind config
module.exports = {
  theme: {
    colors: {
      primary: brandColors.primary,
      secondary: brandColors.secondary,
      gray: brandColors.neutral,
      green: brandColors.success
      // ...
    }
  }
}
```

**Color Palette Documentation:**

```markdown
## Brand Colors

### Primary Blue (#0066CC)

- **Use for:** Primary buttons, links, active states, brand elements
- **Don't use for:** Backgrounds, large areas
- **Accessibility:** Passes WCAG AA for text on white

### Secondary Orange (#FF9100)

- **Use for:** CTAs, highlights, important actions
- **Don't use for:** Body text
- **Pairing:** Works best with primary blue

### Neutral Grays

- **Use for:** Text, borders, backgrounds, UI elements
- **Hierarchy:**
  - 900: Headings
  - 700: Body text
  - 500: Secondary text
  - 300: Borders
  - 100: Backgrounds
```

---

## Typography System

### Font Selection

```css
/* Google Fonts import */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  /* Font families */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Courier New', monospace;

  /* Font sizes */
  --text-xs: 0.75rem; /* 12px */
  --text-sm: 0.875rem; /* 14px */
  --text-base: 1rem; /* 16px */
  --text-lg: 1.125rem; /* 18px */
  --text-xl: 1.25rem; /* 20px */
  --text-2xl: 1.5rem; /* 24px */
  --text-3xl: 1.875rem; /* 30px */
  --text-4xl: 2.25rem; /* 36px */
  --text-5xl: 3rem; /* 48px */

  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
}
```

**Typography Scale:**

```typescript
// components/Typography.tsx

export function Heading1({ children }: { children: React.ReactNode }) {
  return (
    <h1 className="text-4xl font-bold leading-tight text-gray-900">
      {children}
    </h1>
  )
}

export function Heading2({ children }: { children: React.ReactNode }) {
  return (
    <h2 className="text-3xl font-semibold leading-tight text-gray-900">
      {children}
    </h2>
  )
}

export function BodyText({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-base font-normal leading-normal text-gray-700">
      {children}
    </p>
  )
}

export function Caption({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-sm font-normal leading-normal text-gray-500">
      {children}
    </p>
  )
}
```

---

## Brand Guidelines Document

### Creating brand-guidelines.md

```markdown
# TechStart Brand Guidelines

## Logo Usage

### Logo Variations

- **Full Logo**: Use on marketing materials, website header
- **Icon Only**: Use for app icon, favicon, social media avatars
- **Wordmark**: Use when icon doesn't fit context

### Clear Space

Maintain clear space around logo equal to height of the "T" in TechStart

### Minimum Size

- **Digital**: 120px width (full logo), 40px (icon)
- **Print**: 1 inch width (full logo), 0.25 inch (icon)

### Don'ts

❌ Don't rotate the logo
❌ Don't change colors (except approved variations)
❌ Don't add effects (shadows, gradients, etc.)
❌ Don't distort or stretch

---

## Color Palette

### Primary Colors

- **Brand Blue**: #0066CC
  - RGB: 0, 102, 204
  - CMYK: 100, 50, 0, 20
- **Accent Orange**: #FF9100
  - RGB: 255, 145, 0
  - CMYK: 0, 43, 100, 0

### Usage

- Primary buttons, links: Brand Blue
- CTAs, highlights: Accent Orange
- Backgrounds: Neutral grays

---

## Typography

### Fonts

- **Headings**: Inter Bold (700)
- **Body**: Inter Regular (400)
- **Code**: JetBrains Mono Regular (400)

### Hierarchy

- H1: 48px / Bold / Tight leading
- H2: 36px / Semibold / Tight leading
- Body: 16px / Regular / Normal leading
- Caption: 14px / Regular / Normal leading

---

## Voice & Tone

### Brand Personality

- **Professional** but not corporate
- **Technical** but approachable
- **Innovative** but reliable

### Writing Style

- Use active voice
- Be concise and clear
- Avoid jargon (unless technical docs)
- Use "we" and "you" (not "I" or "one")

### Examples

✅ "Deploy your app in seconds"
❌ "Applications can be deployed quickly"

✅ "We built this for developers like you"
❌ "This product was designed for developer users"
```

---

## Social Media Templates

### Profile Image (SVG Template)

```typescript
// templates/SocialProfileImage.tsx

export function SocialProfileImage() {
  return (
    <svg width="400" height="400" viewBox="0 0 400 400">
      {/* Background */}
      <rect width="400" height="400" fill="#0066CC" />

      {/* Logo (centered) */}
      <circle cx="200" cy="200" r="120" fill="white" />
      <path
        d="M160 200 L240 160 L240 240 Z"
        fill="#0066CC"
      />
    </svg>
  )
}
```

### Social Media Post Template

```typescript
// templates/SocialPost.tsx

interface SocialPostProps {
  title: string
  description: string
  imageUrl?: string
}

export function SocialPost({ title, description, imageUrl }: SocialPostProps) {
  return (
    <svg width="1200" height="630" viewBox="0 0 1200 630">
      {/* Background gradient */}
      <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#0066CC" />
          <stop offset="100%" stopColor="#003D7A" />
        </linearGradient>
      </defs>
      <rect width="1200" height="630" fill="url(#bg)" />

      {/* Content */}
      <text
        x="60"
        y="200"
        fontSize="60"
        fontWeight="700"
        fill="white"
        fontFamily="Inter"
      >
        {title}
      </text>
      <text
        x="60"
        y="270"
        fontSize="32"
        fill="#CCE0FF"
        fontFamily="Inter"
      >
        {description}
      </text>

      {/* Logo */}
      <Logo variant="icon" size={60} color="white" />
    </svg>
  )
}
```

---

## Business Card Design

```typescript
// templates/BusinessCard.tsx

interface BusinessCardProps {
  name: string
  title: string
  email: string
  phone: string
}

export function BusinessCard({ name, title, email, phone }: BusinessCardProps) {
  return (
    <svg width="350" height="200" viewBox="0 0 350 200">
      {/* Front side */}
      <rect width="350" height="200" fill="white" />

      {/* Logo */}
      <Logo variant="full" size={30} />

      {/* Contact info */}
      <text x="20" y="120" fontSize="20" fontWeight="700" fill="#111827">
        {name}
      </text>
      <text x="20" y="145" fontSize="14" fill="#6B7280">
        {title}
      </text>
      <text x="20" y="170" fontSize="12" fill="#6B7280">
        {email}
      </text>
      <text x="20" y="185" fontSize="12" fill="#6B7280">
        {phone}
      </text>
    </svg>
  )
}
```

---

## Brand Asset Management

### File Organization

```
brand-assets/
├── logo/
│   ├── svg/
│   │   ├── logo-full.svg
│   │   ├── logo-icon.svg
│   │   └── logo-wordmark.svg
│   ├── png/
│   │   ├── logo-full@1x.png
│   │   ├── logo-full@2x.png
│   │   └── logo-full@3x.png
│   └── favicon/
│       ├── favicon-16x16.png
│       ├── favicon-32x32.png
│       └── favicon.ico
├── colors/
│   └── palette.json
├── fonts/
│   ├── Inter-Regular.woff2
│   ├── Inter-Bold.woff2
│   └── JetBrainsMono-Regular.woff2
├── templates/
│   ├── social-profile.svg
│   ├── social-post.svg
│   └── business-card.svg
└── guidelines/
    └── brand-guidelines.pdf
```

---

## Favicon Generation

```typescript
// scripts/generate-favicons.ts

import sharp from 'sharp'
import fs from 'fs'

async function generateFavicons() {
  const sizes = [16, 32, 48, 64, 128, 256]

  for (const size of sizes) {
    await sharp('logo-icon.svg')
      .resize(size, size)
      .png()
      .toFile(`public/favicon-${size}x${size}.png`)

    console.log(`Generated ${size}x${size} favicon`)
  }

  console.log('Favicons generated!')
}

generateFavicons()
```

**Favicon HTML:**

```html
<!-- In layout/head -->
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />
```

---

## When to Use Me

**Perfect for:**

- Creating new brand identities
- Designing logos and visual systems
- Building brand guidelines
- Creating marketing templates
- Ensuring brand consistency

**I'll help you:**

- Design memorable logos
- Create cohesive color palettes
- Build typography systems
- Generate brand assets
- Document brand guidelines

## What I'll Create

```
🎨 Logo Designs (SVG)
🌈 Color Palettes
📝 Typography Systems
📄 Brand Guidelines
🖼️ Social Media Templates
💼 Business Cards
```

Let's build a strong, cohesive brand identity!
