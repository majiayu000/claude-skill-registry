---
name: tailwindcss-plugins
description: Tailwind CSS plugins including official plugins and custom plugin development
---

# Tailwind CSS Plugins

## Official Plugins

### @tailwindcss/typography

Beautiful typographic defaults for content you don't control (Markdown, CMS content).

#### Installation

```bash
npm install -D @tailwindcss/typography
```

```css
@import "tailwindcss";
@plugin "@tailwindcss/typography";
```

#### Basic Usage

```html
<article class="prose">
  <h1>Article Title</h1>
  <p>This content gets beautiful default styles...</p>
</article>
```

#### Size Modifiers

| Class | Description |
|-------|-------------|
| `prose-sm` | Smaller text (14px base) |
| `prose` | Default (16px base) |
| `prose-lg` | Larger text (18px base) |
| `prose-xl` | Extra large (20px base) |
| `prose-2xl` | Huge (24px base) |

```html
<article class="prose md:prose-lg lg:prose-xl">
  <!-- Responsive sizing -->
</article>
```

#### Color Themes

```html
<article class="prose prose-slate">Gray theme</article>
<article class="prose prose-zinc">Zinc theme</article>
<article class="prose prose-neutral">Neutral theme</article>
<article class="prose prose-stone">Stone theme</article>
```

#### Dark Mode

```html
<article class="prose dark:prose-invert">
  <!-- Automatically inverts for dark mode -->
</article>
```

#### Element Modifiers

Override specific elements:

```html
<article class="
  prose
  prose-headings:text-blue-600
  prose-a:text-blue-500
  prose-a:no-underline
  prose-code:text-pink-500
  prose-img:rounded-lg
  prose-strong:text-gray-900
  prose-blockquote:border-blue-500
">
  Content
</article>
```

#### Max Width Control

```html
<!-- Remove max-width constraint -->
<article class="prose max-w-none">
  Full width content
</article>
```

#### Escaping Prose Styles

```html
<article class="prose">
  <h1>Styled heading</h1>
  <p>Styled paragraph</p>

  <div class="not-prose">
    <!-- This div and its children escape prose styles -->
    <CustomComponent />
  </div>

  <p>Back to prose styles</p>
</article>
```

#### Custom Class Name

```css
@plugin "@tailwindcss/typography" {
  className: wysiwyg;
}
```

```html
<article class="wysiwyg">Content</article>
```

### @tailwindcss/forms

Resets form elements to a consistent, easily-styleable baseline.

#### Installation

```bash
npm install -D @tailwindcss/forms
```

```css
@import "tailwindcss";
@plugin "@tailwindcss/forms";
```

#### Styled Elements

The plugin applies styles to:
- `input[type='text']`
- `input[type='email']`
- `input[type='password']`
- `input[type='number']`
- `input[type='url']`
- `input[type='date']`
- `input[type='datetime-local']`
- `input[type='month']`
- `input[type='week']`
- `input[type='time']`
- `input[type='search']`
- `input[type='tel']`
- `input[type='checkbox']`
- `input[type='radio']`
- `select`
- `select[multiple]`
- `textarea`

#### Basic Usage

```html
<!-- Text input -->
<input type="email" class="rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500">

<!-- Select -->
<select class="rounded-lg border-gray-300">
  <option>Option 1</option>
  <option>Option 2</option>
</select>

<!-- Checkbox -->
<input type="checkbox" class="rounded text-blue-500 focus:ring-blue-500">

<!-- Radio -->
<input type="radio" class="text-blue-500 focus:ring-blue-500">

<!-- Textarea -->
<textarea class="rounded-lg border-gray-300" rows="4"></textarea>
```

#### Strategy: Class-Based

For opt-in styling (doesn't apply global resets):

```css
@plugin "@tailwindcss/forms" {
  strategy: class;
}
```

```html
<!-- Explicitly opt-in to form styles -->
<input type="text" class="form-input rounded-lg">
<select class="form-select rounded-lg">
<textarea class="form-textarea rounded-lg">
<input type="checkbox" class="form-checkbox rounded">
<input type="radio" class="form-radio">
```

#### Form Classes Reference

| Class | Element |
|-------|---------|
| `form-input` | Text inputs |
| `form-textarea` | Textareas |
| `form-select` | Selects |
| `form-multiselect` | Multiple selects |
| `form-checkbox` | Checkboxes |
| `form-radio` | Radio buttons |

#### Styling Checkboxes/Radios

```html
<!-- Colored checkbox -->
<input type="checkbox" class="rounded text-pink-500">

<!-- Accent color (native) -->
<input type="checkbox" class="accent-purple-600">

<!-- Custom size -->
<input type="checkbox" class="h-6 w-6 rounded text-blue-500">
```

### @tailwindcss/container-queries

Style elements based on their container's size instead of the viewport.

#### Installation

```bash
npm install -D @tailwindcss/container-queries
```

```css
@import "tailwindcss";
@plugin "@tailwindcss/container-queries";
```

#### Basic Usage

```html
<!-- Define a container -->
<div class="@container">
  <!-- Use container query breakpoints -->
  <div class="flex flex-col @md:flex-row @lg:gap-8">
    <div class="@sm:text-lg @md:text-xl">
      Responsive to container, not viewport
    </div>
  </div>
</div>
```

#### Container Breakpoints

| Prefix | Width |
|--------|-------|
| `@xs` | 320px |
| `@sm` | 384px |
| `@md` | 448px |
| `@lg` | 512px |
| `@xl` | 576px |
| `@2xl` | 672px |
| `@3xl` | 768px |
| `@4xl` | 896px |
| `@5xl` | 1024px |
| `@6xl` | 1152px |
| `@7xl` | 1280px |

#### Named Containers

```html
<!-- Name the container -->
<div class="@container/sidebar">
  <!-- Reference by name -->
  <div class="@md/sidebar:flex">
    Only flex when sidebar container is md
  </div>
</div>

<div class="@container/main">
  <div class="@lg/main:grid-cols-3">
    Grid when main container is lg
  </div>
</div>
```

#### Arbitrary Container Values

```html
<div class="@container">
  <div class="@[400px]:flex @[600px]:grid">
    Arbitrary breakpoint values
  </div>
</div>
```

## Creating Custom Plugins (v4)

### CSS-Only Utilities

For simple utilities, use the `@utility` directive instead of a JavaScript plugin:

```css
/* In your CSS file */
@utility content-auto {
  content-visibility: auto;
}

@utility text-balance {
  text-wrap: balance;
}

@utility scrollbar-none {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

@utility scrollbar-none::-webkit-scrollbar {
  display: none;
}
```

### JavaScript Plugins

For complex plugins requiring JavaScript:

```javascript
// plugins/my-plugin.js
import plugin from 'tailwindcss/plugin'

export default plugin(function({ addUtilities, addComponents, matchUtilities, theme }) {
  // Add static utilities
  addUtilities({
    '.content-auto': {
      'content-visibility': 'auto',
    },
    '.text-balance': {
      'text-wrap': 'balance',
    },
  })

  // Add components
  addComponents({
    '.btn': {
      padding: theme('spacing.2') + ' ' + theme('spacing.4'),
      borderRadius: theme('borderRadius.lg'),
      fontWeight: theme('fontWeight.medium'),
    },
    '.btn-primary': {
      backgroundColor: theme('colors.blue.500'),
      color: theme('colors.white'),
      '&:hover': {
        backgroundColor: theme('colors.blue.600'),
      },
    },
  })

  // Add dynamic utilities
  matchUtilities(
    {
      'text-shadow': (value) => ({
        textShadow: value,
      }),
    },
    { values: theme('textShadow') }
  )
})
```

Load in CSS:

```css
@import "tailwindcss";
@plugin "./plugins/my-plugin.js";
```

### Plugin with Theme Extension

```javascript
// plugins/gradients.js
import plugin from 'tailwindcss/plugin'

export default plugin(
  function({ matchUtilities, theme }) {
    matchUtilities(
      {
        'text-gradient': (value) => ({
          backgroundImage: value,
          backgroundClip: 'text',
          color: 'transparent',
        }),
      },
      { values: theme('textGradient') }
    )
  },
  {
    theme: {
      textGradient: {
        primary: 'linear-gradient(to right, #667eea, #764ba2)',
        secondary: 'linear-gradient(to right, #f093fb, #f5576c)',
        sunset: 'linear-gradient(to right, #fa709a, #fee140)',
      },
    },
  }
)
```

### Adding Custom Variants

```javascript
// plugins/variants.js
import plugin from 'tailwindcss/plugin'

export default plugin(function({ addVariant }) {
  // Peer states
  addVariant('peer-checked', ':merge(.peer):checked ~ &')

  // Group states
  addVariant('group-focus-visible', ':merge(.group):focus-visible &')

  // Data attributes
  addVariant('data-active', '&[data-active="true"]')
  addVariant('data-loading', '&[data-loading]')

  // Custom selectors
  addVariant('hocus', ['&:hover', '&:focus'])
  addVariant('not-first', '&:not(:first-child)')
  addVariant('not-last', '&:not(:last-child)')
})
```

## Community Plugins

### Popular Plugins

| Plugin | Description |
|--------|-------------|
| `tailwindcss-animate` | Animation utilities |
| `tailwindcss-motion` | Advanced motion/animation |
| `@headlessui/tailwindcss` | Headless UI variants |
| `tailwind-scrollbar` | Scrollbar styling |
| `tailwindcss-3d` | 3D transform utilities |
| `tailwindcss-fluid-type` | Fluid typography |

### tailwindcss-animate

```bash
npm install -D tailwindcss-animate
```

```css
@plugin "tailwindcss-animate";
```

```html
<div class="animate-in fade-in slide-in-from-bottom-4 duration-500">
  Animated content
</div>

<div class="animate-out fade-out slide-out-to-top-4 duration-300">
  Exiting content
</div>
```

## Best Practices

### 1. Load Only What You Need

```css
/* Only load plugins you actually use */
@plugin "@tailwindcss/typography";
/* @plugin "@tailwindcss/forms"; -- commented out if not using */
```

### 2. Use CSS Utilities First

Before creating a JavaScript plugin, try the `@utility` directive:

```css
/* Simple custom utility - no JS needed */
@utility glass {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.1);
}
```

### 3. Document Custom Plugins

```javascript
/**
 * @name Text Gradient Plugin
 * @description Adds text gradient utilities
 * @usage class="text-gradient-primary"
 */
export default plugin(...)
```

### 4. Test Plugin Compatibility

When upgrading Tailwind, verify all plugins work with the new version:

```bash
npm outdated | grep tailwind
npm update @tailwindcss/typography @tailwindcss/forms
```
