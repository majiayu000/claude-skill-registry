---
name: webconsulting-branding
description: Enforces webconsulting.at design system, color palettes, typography, and MDX component structures for frontend development.
version: 1.0.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - frontend
  - design
  - branding
  - ui
  - components
  - styling
---

# webconsulting Design System

## 1. Brand Identity & Voice

**Persona**: Innovative, Technical, Professional ("Senior Solutions Architect")

**Tone**: Clear, concise, authoritative. Avoid marketing fluff.

**Language**: German (Primary) / English (Technical documentation)

## 2. Visual Design Tokens (Strict Adherence)

### Color Palette

| Token | Hex Value | Tailwind Class | Usage |
|-------|-----------|----------------|-------|
| Primary Teal | `#14b8a6` | `text-teal-500` | Links, primary buttons, active states |
| Primary Cyan | `#06b6d4` | `text-cyan-600` | Hover states, secondary highlights |
| Accent Amber | `#f59e0b` | `text-amber-500` | Warnings, highlights, specialized icons |
| Neutral Dark | `#334155` | `text-slate-700` | Body text, standard paragraphs |
| Deep Black | `#0a0a0a` | `bg-neutral-950` | Footers, dark mode backgrounds |
| Hero Gradient Start | `#667eea` | `from-[#667eea]` | Hero section gradient start |
| Hero Gradient End | `#764ba2` | `to-[#764ba2]` | Hero section gradient end |

### Hero Gradient Usage

```css
.hero-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

```html
<div class="bg-gradient-to-r from-[#667eea] to-[#764ba2]">
  <!-- Hero content -->
</div>
```

### Typography

| Element | Font Family | Weight | Usage |
|---------|-------------|--------|-------|
| Headings | Raleway | 600, 700 | H1-H3, titles |
| Body | Open Sans | 400, 500 | Paragraphs, UI elements |
| Code | JetBrains Mono | 400 | Code blocks, inline code |
| Fallback | Calibri | - | System fallback only |

### Font Import

```css
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@600;700&family=Open+Sans:wght@400;500&family=JetBrains+Mono&display=swap');
```

## 3. MDX Component Architecture

When generating content or frontend components, use the following structure. **Do NOT use raw HTML**.

### Interactive Tabs

Use for version comparisons (e.g., TYPO3 v11 vs v12 vs v13 vs v14):

```jsx
<Tabs defaultValue="v14">
  <TabsList>
    <TabsTrigger value="v13">TYPO3 v13</TabsTrigger>
    <TabsTrigger value="v14">TYPO3 v14</TabsTrigger>
  </TabsList>
  <TabsContent value="v13">
    Content for v13...
  </TabsContent>
  <TabsContent value="v14">
    Content for v14 (preferred)...
  </TabsContent>
</Tabs>
```

### Data & Comparison Tables

Use `ComparisonTable` for feature matrices. Supports boolean checkmarks:

```jsx
<ComparisonTable 
  headers={['Feature', 'v13', 'v14']}
  rows={[
    { label: 'Content Blocks', values: [true, true] },
    { label: 'Symfony 7', values: [false, true] },
    { label: 'PHP 8.2+', values: [true, true] }
  ]} 
/>
```

### Code Blocks with Syntax Highlighting

```jsx
<CodeBlock 
  language="php" 
  filename="Classes/Controller/PageController.php"
  highlightLines={[3, 7]}
>
{`<?php
declare(strict_types=1);

namespace Vendor\\Extension\\Controller;

use Psr\\Http\\Message\\ResponseInterface;
use TYPO3\\CMS\\Extbase\\Mvc\\Controller\\ActionController;

final class PageController extends ActionController
{
    public function indexAction(): ResponseInterface
    {
        return $this->htmlResponse();
    }
}`}
</CodeBlock>
```

### Callout Boxes

```jsx
<Callout type="info" title="Best Practice">
  Always use `declare(strict_types=1);` in PHP files.
</Callout>

<Callout type="warning" title="Breaking Change">
  This API changed in TYPO3 v14.
</Callout>

<Callout type="danger" title="Security">
  Never expose sensitive configuration files.
</Callout>
```

### MDX Images

```jsx
<MDXImage 
  src="/images/architecture-diagram.png" 
  alt="TYPO3 Extension Architecture"
  caption="Figure 1: Domain-Driven Design in TYPO3 Extensions"
/>
```

## 4. Mermaid Diagrams (Theming)

All diagrams must explicitly override the theme to match the Teal/Amber palette:

```markdown
%%{init: {'theme': 'base', 'themeVariables': { 
  'primaryColor': '#14b8a6', 
  'primaryTextColor': '#ffffff',
  'primaryBorderColor': '#0d9488',
  'lineColor': '#334155',
  'secondaryColor': '#f59e0b',
  'tertiaryColor': '#fef3c7',
  'edgeLabelBackground': '#ffffff'
}}}%%
graph TD
    A[Client Request] -->|HTTP| B(Load Balancer)
    B --> C{TYPO3 Backend}
    C -->|Cache Hit| D[Response]
    C -->|Cache Miss| E[Database]
    E --> D
```

## 5. Accessibility Guidelines (WCAG 2.1 AA)

### Contrast Requirements

- Ensure **4.5:1** contrast ratio for all text
- Large text (18px+ bold, 24px+ regular): **3:1** minimum

### Interactive Elements

- All interactive elements must have visible **focus states**
- Use ring: `focus:ring-2 focus:ring-teal-500 focus:ring-offset-2`

### Images and Media

- All images MUST include `alt` text
- Use `caption` prop in MDXImage component
- Decorative images: use `alt=""`

### Keyboard Navigation

- All interactive elements must be keyboard accessible
- Logical tab order (no positive tabindex)
- Skip links for main content

## 6. Responsive Breakpoints

| Breakpoint | Width | Tailwind Prefix |
|------------|-------|-----------------|
| Mobile | < 640px | (default) |
| Tablet | ≥ 640px | `sm:` |
| Desktop | ≥ 1024px | `lg:` |
| Wide | ≥ 1280px | `xl:` |

## 7. Component Spacing Scale

Use consistent spacing based on 4px grid:

| Token | Value | Usage |
|-------|-------|-------|
| `space-1` | 4px | Icon gaps |
| `space-2` | 8px | Inline elements |
| `space-4` | 16px | Component padding |
| `space-6` | 24px | Section gaps |
| `space-8` | 32px | Major sections |
| `space-12` | 48px | Page sections |

## 8. Button Styles

### Primary Button

```html
<button class="bg-teal-500 hover:bg-teal-600 text-white font-medium px-6 py-3 rounded-lg transition-colors focus:ring-2 focus:ring-teal-500 focus:ring-offset-2">
  Primary Action
</button>
```

### Secondary Button

```html
<button class="border-2 border-teal-500 text-teal-500 hover:bg-teal-50 font-medium px-6 py-3 rounded-lg transition-colors">
  Secondary Action
</button>
```

### Ghost Button

```html
<button class="text-slate-600 hover:text-teal-500 hover:bg-slate-100 px-4 py-2 rounded transition-colors">
  Ghost Action
</button>
```

