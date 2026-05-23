---
name: frontend-analyzer
description: Analyze React/Next.js components to extract typography, colors, layout, fonts, spacing systems, and design tokens. Identifies accessibility issues, responsive breakpoints, and component hierarchies.
---

# Frontend Analyzer

Analisa e identifica tipografia, cores, layout, fontes e elementos de design system em componentes frontend.

## Overview

The Frontend Analyzer skill provides deep inspection of frontend code, design elements, and visual properties. It extracts typography, color palettes, spacing systems, component hierarchies, and accessibility attributes from React/Next.js applications.

## Core Capabilities

### 1. **Visual Element Analysis**

#### 🔤 Typography Detection
- Font families (system fonts, Google Fonts, custom fonts)
- Font sizes and scaling systems (rem, px, %)
- Font weights (100-900)
- Line heights and letter spacing
- Text decorations and text transforms
- Font loading strategies (WOFF2, variable fonts)

#### 🎨 Color Palette Extraction
- Primary, secondary, accent colors
- Background and text colors
- Semantic colors (success, error, warning, info)
- Opacity/alpha values
- Color space (RGB, HSL, hex, CSS variables)
- Dark mode variants

#### 📐 Layout & Spacing
- Grid systems (CSS Grid, Flexbox)
- Spacing scale (gaps, margins, padding)
- Breakpoints and responsive behavior
- Container queries and fluid sizing
- Z-index hierarchy
- Positioning strategies

#### 🧩 Component Architecture
- Component hierarchy and nesting
- Reusable component patterns
- Props and TypeScript interfaces
- State management patterns
- Custom hooks usage
- Styled components vs CSS modules

### 2. **Analysis Categories**

1. **Visual Inspection** - Screenshots and visual differences
2. **Code Inspection** - Component code structure
3. **Design System** - Design token usage
4. **Accessibility (A11y)** - WCAG AA/AAA compliance
5. **Performance** - Font loading optimization

## Analysis Output Structure

```markdown
## 🎨 VISUAL ELEMENTS DETECTED

### Typography System
- Primary Font: [Font family, source, fallback]
- Heading Scale: H1-H6 sizes and weights
- Body Text: Default size, line-height, letter-spacing
- Monospace: Code/terminal fonts

### Color Palette
- Primary: #XXXXXX (RGB, HSL, CSS var)
- Semantic: Success, error, warning colors
- Dark Mode: Color scheme variants
- Contrast Ratios: WCAG AA/AAA compliance

### Layout System
- Grid: [Columns, gap, max-width]
- Breakpoints: [Mobile, tablet, desktop specs]
- Spacing Scale: [Base unit, multipliers]
```

## Usage Examples

### Example 1: Extract Design Tokens
Input: "Analise tipografia de ofertachina.com"
Output: All fonts used, sizes, weights, loading strategy

### Example 2: Color Palette Analysis
Input: "Extraia paleta de cores do ProductCard"
Output: Exact colors, WCAG compliance, dark mode variants

### Example 3: Component Deep Dive
Input: "Analise estrutura de ProductCard"
Output: JSX structure, props, styling approach, accessibility

### Example 4: Design System Audit
Input: "Audite design system compliance"
Output: % compliance, violations, refactoring recommendations

## Accessibility (WCAG)

- Contrast ratios: Pass/Fail by element
- Font sizes: Minimum sizes met
- Interactive elements: Size compliance
- Semantic HTML: Structure quality

## Performance Metrics

- Font file sizes and optimization
- Image optimization status
- CSS bundle size
- Component render efficiency

## Integrations

### With Playwright
- Automated visual analysis
- Color & typography extraction
- Accessibility testing

### With Prompt Improver
- Design tokens inform prompt creation
- UI patterns documented in instructions

## Tools & Technologies Reference

- **CSS Analysis:** PostCSS, cssstats
- **Typography:** Google Fonts API, Font loading APIs
- **Color:** Chroma.js, ntc.js (color naming)
- **Accessibility:** axe-core, WAVE
- **React Inspection:** React DevTools, Storybook
- **Design Systems:** Figma API, Design tokens parser

## References

- [Google Fonts](https://fonts.google.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [WCAG Color Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [CSS-Tricks](https://css-tricks.com/)
- [MDN Web Docs](https://developer.mozilla.org/)
- [Figma Design System](https://www.figma.com/design-systems/)

## Changelog

- **v1.0** (2025-12-19): Initial release with typography, color, layout, component, and accessibility analysis
