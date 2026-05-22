---
name: tailwind-configuration
description: Use when setting up or customizing Tailwind CSS configuration, theme customization, plugins, and build setup. Covers tailwind.config.js setup and content paths.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Tailwind CSS - Configuration

Tailwind CSS is highly customizable through its configuration file, allowing you to define your design system, extend the default theme, and configure plugins.

## Key Concepts

### Configuration File Structure

The `tailwind.config.js` (or `.ts`, `.cjs`, `.mjs`) file is the heart of Tailwind customization:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      // Custom theme extensions
    },
  },
  plugins: [],
  darkMode: 'class', // or 'media'
  prefix: '',
  important: false,
  separator: ':',
}
```

### Content Configuration

The `content` array tells Tailwind where to look for class names:

```javascript
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
    './public/index.html',
  ],
  // ...
}
```

#### Content with Transform

For dynamic class names, use safelist or content transform:

```javascript
module.exports = {
  content: {
    files: ['./src/**/*.{html,js}'],
    transform: {
      md: (content) => {
        // Extract classes from markdown
        return content
      }
    }
  },
  safelist: [
    'bg-red-500',
    'bg-green-500',
    {
      pattern: /bg-(red|green|blue)-(100|200|300)/,
    },
  ],
}
```

## Theme Customization

### Extending the Default Theme

Use `theme.extend` to add to existing values without replacing them:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          200: '#bae6fd',
          300: '#7dd3fc',
          400: '#38bdf8',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c4a6e',
          950: '#082f49',
        },
        primary: '#0ea5e9',
        secondary: '#8b5cf6',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Merriweather', 'serif'],
        mono: ['Fira Code', 'monospace'],
      },
      spacing: {
        '72': '18rem',
        '84': '21rem',
        '96': '24rem',
        '128': '32rem',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      fontSize: {
        'xxs': '0.625rem',
      },
      boxShadow: {
        'inner-lg': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
        'bounce-slow': 'bounce 2s infinite',
      },
      keyframes: {
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' },
        }
      },
    },
  },
}
```

### Overriding Default Theme

Use `theme` (without `extend`) to replace default values:

```javascript
module.exports = {
  theme: {
    // This replaces the default color palette entirely
    colors: {
      white: '#ffffff',
      black: '#000000',
      gray: {
        100: '#f7fafc',
        // ... custom gray scale
        900: '#1a202c',
      },
      blue: {
        500: '#0ea5e9',
      },
    },
  },
}
```

## Best Practices

### 1. Use CSS Variables for Dynamic Colors

Combine Tailwind with CSS variables for runtime theme switching:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'rgb(var(--color-primary) / <alpha-value>)',
        secondary: 'rgb(var(--color-secondary) / <alpha-value>)',
      },
    },
  },
}
```

```css
/* globals.css */
:root {
  --color-primary: 14 165 233; /* RGB values */
  --color-secondary: 139 92 246;
}

[data-theme='dark'] {
  --color-primary: 56 189 248;
  --color-secondary: 167 139 250;
}
```

### 2. Organize Theme Extensions

Group related customizations for maintainability:

```javascript
const colors = require('./theme/colors')
const typography = require('./theme/typography')
const spacing = require('./theme/spacing')

module.exports = {
  theme: {
    extend: {
      ...colors,
      ...typography,
      ...spacing,
    },
  },
}
```

### 3. Use Plugins for Reusable Patterns

Create custom utilities with plugins:

```javascript
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addUtilities, addComponents, theme }) {
      // Add custom utilities
      addUtilities({
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            display: 'none'
          }
        },
        '.text-balance': {
          'text-wrap': 'balance',
        }
      })

      // Add custom components
      addComponents({
        '.btn': {
          padding: theme('spacing.2') + ' ' + theme('spacing.4'),
          borderRadius: theme('borderRadius.md'),
          fontWeight: theme('fontWeight.semibold'),
          '&:hover': {
            opacity: 0.8,
          }
        }
      })
    })
  ],
}
```

### 4. Configure Dark Mode

Choose the appropriate dark mode strategy:

```javascript
module.exports = {
  // Class-based (manual control)
  darkMode: 'class',

  // Or media query-based (system preference)
  // darkMode: 'media',

  // Or custom selector
  // darkMode: ['class', '[data-theme="dark"]'],
}
```

### 5. Optimize for Production

Configure for smaller bundle sizes:

```javascript
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}',
  ],
  // Remove unused styles in production
  purge: {
    enabled: process.env.NODE_ENV === 'production',
  },
}
```

## Examples

### Complete TypeScript Configuration

```typescript
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#0ea5e9',
          light: '#38bdf8',
          dark: '#0284c7',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
  darkMode: 'class',
}

export default config
```

### Multi-Brand Configuration

```javascript
const brandColors = {
  brandA: {
    primary: '#0ea5e9',
    secondary: '#8b5cf6',
  },
  brandB: {
    primary: '#10b981',
    secondary: '#f59e0b',
  },
}

const currentBrand = process.env.BRAND || 'brandA'

module.exports = {
  theme: {
    extend: {
      colors: {
        primary: brandColors[currentBrand].primary,
        secondary: brandColors[currentBrand].secondary,
      },
    },
  },
}
```

### Framework-Specific Configurations

#### Next.js

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

#### Vite + React

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

#### Vue 3

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## Common Patterns

### Design Tokens Integration

```javascript
const designTokens = {
  colors: {
    primary: {
      50: '#eff6ff',
      500: '#3b82f6',
      900: '#1e3a8a',
    },
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
  },
}

module.exports = {
  theme: {
    extend: {
      colors: designTokens.colors,
      spacing: designTokens.spacing,
    },
  },
}
```

### Responsive Breakpoint Customization

```javascript
module.exports = {
  theme: {
    screens: {
      'xs': '475px',
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px',
      '3xl': '1920px',
    },
  },
}
```

### Plugin Configuration

```javascript
module.exports = {
  plugins: [
    // Official plugins
    require('@tailwindcss/forms')({
      strategy: 'class', // or 'base'
    }),
    require('@tailwindcss/typography')({
      className: 'prose',
    }),
    require('@tailwindcss/container-queries'),

    // Custom plugin
    require('./plugins/utilities'),
  ],
}
```

## Anti-Patterns

### ❌ Don't Hardcode Values in Multiple Places

```javascript
// Bad: Repeating values
module.exports = {
  theme: {
    extend: {
      spacing: {
        'custom': '17px',
      },
      width: {
        'custom': '17px',
      },
      height: {
        'custom': '17px',
      },
    },
  },
}

// Good: Use spacing scale consistently
module.exports = {
  theme: {
    extend: {
      spacing: {
        'custom': '17px',
      },
    },
  },
}
// Then use w-custom, h-custom, p-custom, etc.
```

### ❌ Don't Extend When You Mean to Replace

```javascript
// Bad: Accidentally keeping default colors
module.exports = {
  theme: {
    extend: {
      colors: {
        // This adds to the default palette, doesn't replace it
        blue: { 500: '#custom-blue' }
      },
    },
  },
}

// Good: Be explicit about replacing
module.exports = {
  theme: {
    colors: {
      // This replaces the entire color palette
    },
  },
}
```

### ❌ Don't Use Overly Specific Content Paths

```javascript
// Bad: Too specific, might miss files
module.exports = {
  content: [
    './src/components/Button.tsx',
    './src/components/Card.tsx',
    // ...hundreds of files
  ],
}

// Good: Use glob patterns
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
}
```

### ❌ Don't Forget to Configure safelist for Dynamic Classes

```javascript
// Bad: Dynamic classes won't be included
<div className={`bg-${color}-500`}>

// Good: Add to safelist
module.exports = {
  safelist: [
    {
      pattern: /bg-(red|green|blue|yellow)-(500|600|700)/,
    },
  ],
}

// Better: Use complete class names
<div className={color === 'red' ? 'bg-red-500' : 'bg-blue-500'}>
```

## Related Skills

- **tailwind-utility-classes**: Using Tailwind's utility classes effectively
- **tailwind-components**: Building reusable component patterns
- **tailwind-plugins**: Creating custom Tailwind plugins
- **tailwind-performance**: Optimizing Tailwind for production
