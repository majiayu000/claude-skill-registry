---
name: frontier-ui
description: >
  Frontier Code UI standards based on Hero section patterns (dark theme, cyan/purple accents, gradients, glowing effects).
  Trigger: When creating/modifying UI components, sections, or visual elements.
license: Apache-2.0
metadata:
  author: frontier-code
  version: "1.0"
  scope: [root]
  auto_invoke: "Creating/modifying UI components, sections, or visual elements"
---

## When to Use

- Creating or modifying any UI component (buttons, cards, sections, etc.)
- Designing new page sections
- Adding interactive elements with hover states
- Implementing typography and color schemes
- Creating visual effects (glows, gradients, animations)
- Working with responsive layouts

## Critical Patterns

### Color Palette

**Backgrounds** (Dark Theme)
- Primary: `bg-slate-950` (darkest)
- Secondary: `bg-slate-900`, `bg-slate-800`
- Accents: `bg-slate-800/50` (semi-transparent)

**Accent Colors**
- Primary: `cyan` (cyan-500, cyan-400, cyan-300)
- Secondary: `purple` (purple-500, purple-400)
- Success: `green` (green-400, green-500)
- Info: `blue` (blue-500)
- Warning: `orange` (orange-500)
- Error: `pink` (pink-500)

**Text Colors**
- Primary: `text-slate-300`, `text-white`
- Secondary: `text-slate-400`
- Muted: `text-slate-500`

### Gradients

**Text Gradients**
```astro
<span class="bg-gradient-to-r from-cyan-400 via-cyan-300 to-purple-400 bg-clip-text text-transparent">
  Frontier Code
</span>
```

**Background Gradients**
```astro
<!-- Hero background -->
<div class="bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950"></div>

<!-- Button gradient -->
<div class="bg-gradient-to-r from-cyan-500 to-cyan-600"></div>
<div class="bg-gradient-to-r from-purple-500 to-cyan-500"></div>

<!-- Dynamic text gradient -->
<span class="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent"></span>
```

### Typography

**Hero Headings**
```astro
<h1 class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold">
  Title
</h1>
```

**Subheadings**
```astro
<h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-light text-slate-300">
  Subtitle
</h2>
```

**Body Text**
```astro
<p class="text-lg sm:text-xl text-slate-400 leading-relaxed">
  Description text
</p>
```

**Small Labels**
```astro
<span class="px-4 py-2 bg-slate-800/50 border border-cyan-500/30 rounded-full text-cyan-400 text-sm font-mono">
  &lt;Frontier /&gt;
</span>
```

**Status Badges**
```astro
<div class="flex items-center gap-2">
  <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
  <span class="text-slate-500 text-sm font-mono">Status</span>
</div>
```

### Spacing

**Vertical Spacing**
- Sections: `py-16 sm:py-20 lg:py-24`
- Margin between elements: `mb-8`, `mb-12`, `mb-16`
- Gap: `gap-2`, `gap-4`, `gap-8`

### Borders

**Subtle Borders**
```astro
<!-- Outline button/badge -->
class="border-2 border-cyan-500/50"

<!-- Badge border -->
class="border border-cyan-500/30"

<!-- Hover state border -->
class="hover:border-cyan-400"
```

### Rounded Corners

- Buttons/badges: `rounded-lg`
- Circular elements: `rounded-full`

### Shadows & Glows

**Text Shadow**
```astro
style="text-shadow: 0 0 40px rgba(0, 245, 255, 0.5);"
```

**Blur Effects**
```astro
<!-- Background glow orbs -->
<div class="w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse"></div>

<!-- Button shadow -->
class="hover:shadow-lg hover:shadow-cyan-500/50"
```

### Animations

**Pulse Animation**
```astro
class="animate-pulse"
<!-- Add delay for staggered effects -->
style="animation-delay: 0.2s;"
```

**Bounce Animation**
```astro
class="animate-bounce"
```

**Custom Blink (Cursor)**
```astro
<style>
  @keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0; }
  }
  .animate-blink {
    animation: blink 1s infinite;
  }
</style>
<span class="w-2 h-8 bg-purple-400 animate-blink"></span>
```

### Transitions

**Standard Transitions**
```astro
class="transition-all duration-300"

<!-- Hover effects -->
class="hover:scale-105"
class="hover:shadow-lg hover:shadow-cyan-500/50"
class="hover:bg-cyan-500/10"
class="hover:border-cyan-400 hover:text-cyan-300"

<!-- Opacity transitions -->
class="opacity-0 group-hover:opacity-100 transition-opacity duration-300"
```

### Buttons

**Primary Gradient Button**
```astro
<a href="#" class="group relative px-8 py-4 bg-gradient-to-r from-cyan-500 to-cyan-600 text-white font-semibold rounded-lg overflow-hidden transition-all duration-300 hover:scale-105 hover:shadow-lg hover:shadow-cyan-500/50">
  <div class="absolute inset-0 bg-gradient-to-r from-purple-500 to-cyan-500 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
  <span class="relative flex items-center gap-2">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="..." />
    </svg>
    <span>Button Text</span>
  </span>
</a>
```

**Outline Button**
```astro
<a href="#" class="px-8 py-4 border-2 border-cyan-500/50 text-cyan-400 font-semibold rounded-lg hover:bg-cyan-500/10 hover:border-cyan-400 hover:text-cyan-300 transition-all duration-300 hover:scale-105">
  Button Text
</a>
```

### Sections

**Hero Section Structure**
```astro
<section id="hero" class="relative min-h-screen flex items-center justify-center overflow-hidden bg-slate-950">
  <!-- Background layers -->
  <div id="particles" class="absolute inset-0 opacity-20"></div>
  <div class="absolute inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950"></div>

  <!-- Glow orbs -->
  <div class="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl animate-pulse"></div>
  <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style="animation-delay: 1s;"></div>

  <!-- Grid pattern -->
  <div class="absolute inset-0 bg-[linear-gradient(rgba(0,245,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(0,245,255,0.03)_1px,transparent_1px)] bg-[size:50px_50px]"></div>

  <!-- Content -->
  <Container>
    <div class="relative z-10 max-w-5xl mx-auto text-center">
      <!-- Content goes here -->
    </div>
  </Container>
</section>
```

**Standard Section**
```astro
<section id="{id}" class="relative py-16 sm:py-20 lg:py-24 bg-slate-950">
  <Container>
    <div class="max-w-6xl mx-auto">
      <!-- Section content -->
    </div>
  </Container>
</section>
```

### Container Pattern

```astro
<div class="relative z-10 max-w-5xl mx-auto text-center">
  <!-- Centered content -->
</div>

<div class="max-w-6xl mx-auto">
  <!-- Full-width container -->
</div>

<div class="max-w-3xl mx-auto leading-relaxed">
  <!-- Text content -->
</div>
```

### Responsive Design

**Always use mobile-first responsive utilities:**
```astro
<!-- Spacing -->
class="py-16 sm:py-20 lg:py-24"

<!-- Typography -->
class="text-5xl sm:text-6xl md:text-7xl lg:text-8xl"

<!-- Layout -->
class="flex flex-col sm:flex-row gap-4 justify-center"
```

### Icons

```astro
<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="..." />
</svg>
```

## Code Examples

### Complete Badge Component
```astro
---
const { label = '', color = 'cyan' } = Astro.props;
const colors = {
  cyan: 'text-cyan-400 border-cyan-500/30 bg-slate-800/50',
  purple: 'text-purple-400 border-purple-500/30 bg-slate-800/50',
  green: 'text-green-400 border-green-500/30 bg-slate-800/50'
};
---
<span class={`px-4 py-2 rounded-full text-sm font-mono border ${colors[color]}`}>
  {label}
</span>
```

### Status Indicator with Delay
```astro
---
const { status = '', color = 'green', delay = 0 } = Astro.props;
const colors = {
  green: 'bg-green-500',
  cyan: 'bg-cyan-500',
  purple: 'bg-purple-500'
};
---
<div class="flex items-center gap-2">
  <div class={`w-2 h-2 ${colors[color]} rounded-full animate-pulse`} style={`animation-delay: ${delay}s;`}></div>
  <span class="text-slate-500 text-sm font-mono">{status}</span>
</div>
```

## Decision Tree: Which Style to Apply?

| Situation | Use |
|-----------|-----|
| Primary action | Gradient button `from-cyan-500 to-cyan-600` |
| Secondary action | Outline button `border-cyan-500/50` |
| Headings | Large with text gradient `from-cyan-400 via-cyan-300 to-purple-400` |
| Subheadings | Light weight `font-light text-slate-300` |
| Labels/badges | Rounded pill `rounded-full` with subtle border |
| Background | Dark `bg-slate-950` with gradient overlay |
| Glow effects | `bg-{color}/20 rounded-full blur-3xl` |
| Hover effects | `hover:scale-105 hover:shadow-lg hover:shadow-{color}/50` |
| Grid patterns | `bg-[linear-gradient(...)] bg-[size:50px_50px]` |

## Anti-Patterns

❌ Don't use:
- White backgrounds for main sections (use slate-950/slate-900)
- Solid colors without gradients for accents
- Sharp corners on buttons/badges (use rounded-lg/rounded-full)
- Heavy shadows without color tint (use `shadow-{color}/50`)
- Text without spacing (add `leading-relaxed`)
- Missing responsive utilities (always add `sm:` `md:` `lg:`)

## Commands

No specific commands - UI is purely declarative through Tailwind classes.

## Resources

- **Examples**: Hero section at `src/components/sections/Hero.astro`
- **Color Reference**: Use cyan/purple as primary accents, slate for neutrals
- **Animation Library**: Tailwind built-in + custom `@keyframes` for blinking
