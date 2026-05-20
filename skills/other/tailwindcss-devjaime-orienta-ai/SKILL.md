---
name: tailwindcss
description: Tailwind CSS utility-first styling for JARVIS UI components
model: sonnet
risk_level: LOW
version: 1.1.0
---

# Tailwind CSS Development Skill

> **File Organization**: This skill uses split structure. See `references/` for advanced patterns.

## 1. Overview

This skill provides Tailwind CSS expertise for styling the JARVIS AI Assistant interface with utility-first CSS, creating consistent and maintainable HUD designs.

**Risk Level**: LOW - Styling framework with minimal security surface

**Primary Use Cases**:
- Holographic UI panel styling
- Responsive HUD layouts
- Animation utilities for transitions
- Custom JARVIS theme configuration

## 2. Core Responsibilities

### 2.1 Fundamental Principles

1. **TDD First**: Write component tests before styling implementation
2. **Performance Aware**: Optimize CSS output size and rendering performance
3. **Utility-First**: Compose styles from utility classes, extract components when patterns repeat
4. **Design System**: Define JARVIS color palette and spacing in config
5. **Responsive Design**: Mobile-first with breakpoint utilities
6. **Dark Mode Default**: HUD is always dark-themed
7. **Accessibility**: Maintain sufficient contrast ratios

## 3. Implementation Workflow (TDD)

### 3.1 TDD Process for Styled Components

Follow this workflow for every styled component:

#### Step 1: Write Failing Test First

```typescript
// tests/components/HUDPanel.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HUDPanel from '~/components/HUDPanel.vue'

describe('HUDPanel', () => {
  it('renders with correct JARVIS theme classes', () => {
    const wrapper = mount(HUDPanel, {
      props: { title: 'System Status' }
    })

    const panel = wrapper.find('[data-testid="hud-panel"]')
    expect(panel.classes()).toContain('bg-jarvis-bg-panel/80')
    expect(panel.classes()).toContain('border-jarvis-primary/30')
    expect(panel.classes()).toContain('backdrop-blur-sm')
  })

  it('applies responsive grid layout', () => {
    const wrapper = mount(HUDPanel)
    const grid = wrapper.find('[data-testid="panel-grid"]')

    expect(grid.classes()).toContain('grid-cols-1')
    expect(grid.classes()).toContain('md:grid-cols-2')
    expect(grid.classes()).toContain('lg:grid-cols-3')
  })

  it('shows correct status indicator colors', async () => {
    const wrapper = mount(HUDPanel, {
      props: { status: 'active' }
    })

    const indicator = wrapper.find('[data-testid="status-indicator"]')
    expect(indicator.classes()).toContain('bg-jarvis-primary')
    expect(indicator.classes()).toContain('animate-pulse')

    await wrapper.setProps({ status: 'error' })
    expect(indicator.classes()).toContain('bg-jarvis-danger')
  })

  it('maintains accessibility focus styles', () => {
    const wrapper = mount(HUDPanel)
    const button = wrapper.find('button')

    expect(button.classes()).toContain('focus:ring-2')
    expect(button.classes()).toContain('focus:outline-none')
  })
})
```

#### Step 2: Implement Minimum to Pass

```vue
<!-- components/HUDPanel.vue -->
<template>
  <div
    data-testid="hud-panel"
    class="bg-jarvis-bg-panel/80 border border-jarvis-primary/30 backdrop-blur-sm rounded-lg p-4"
  >
    <div
      data-testid="panel-grid"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
    >
      <slot />
    </div>
    <span
      data-testid="status-indicator"
      :class="statusClasses"
    />
    <button class="focus:ring-2 focus:outline-none focus:ring-jarvis-primary">
      Action
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title?: string
  status?: 'active' | 'warning' | 'error' | 'inactive'
}>()

const statusClasses = computed(() => ({
  'bg-jarvis-primary animate-pulse': props.status === 'active',
  'bg-jarvis-warning': props.status === 'warning',
  'bg-jarvis-danger': props.status === 'error',
  'bg-gray-500': props.status === 'inactive'
}))
</script>
```

#### Step 3: Refactor if Needed

Extract repeated patterns to @apply directives:

```css
/* assets/css/components.css */
@layer components {
  .hud-panel {
    @apply bg-jarvis-bg-panel/80 border border-jarvis-primary/30 backdrop-blur-sm rounded-lg p-4;
  }

  .hud-grid {
    @apply grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4;
  }
}
```

#### Step 4: Run Full Verification

```bash
# Run all style-related tests
npm run test -- --grep "HUDPanel"

# Check for unused CSS
npx tailwindcss --content './components/**/*.vue' --output /dev/null

# Verify build size
npm run build && ls -lh .output/public/_nuxt/*.css
```

## 4. Performance Patterns

### 4.1 Purge Optimization

```javascript
// tailwind.config.js
// Good: Specific content paths
export default {
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './composables/**/*.ts'
  ]
}

// Bad: Too broad, includes unused files
export default {
  content: ['./src/**/*']  // Includes tests, stories, etc.
}
```

### 4.2 JIT Mode Efficiency

```javascript
// Good: Let JIT generate only used utilities
export default {
  mode: 'jit',  // Default in v3+
  theme: {
    extend: {
      // Only extend what you need
      colors: {
        jarvis: {
          primary: '#00ff41',
          secondary: '#0891b2'
        }
      }
    }
  }
}

// Bad: Defining unused variants
export default {
  variants: {
    extend: {
      backgroundColor: ['active', 'group-hover', 'disabled']  // May not use all
    }
  }
}
```

### 4.3 @apply Extraction Strategy

```vue
<!-- Good: Extract when pattern repeats 3+ times -->
<style>
@layer components {
  .btn-jarvis {
    @apply px-4 py-2 rounded font-medium transition-all duration-200
           focus:outline-none focus:ring-2 focus:ring-offset-2;
  }
}
</style>

<!-- Bad: @apply for single-use styles -->
<style>
.my-unique-element {
  @apply p-4 m-2 text-white;  /* Just use utilities in template */
}
</style>
```

### 4.4 Responsive Breakpoints Efficiency

```vue
<!-- Good: Mobile-first, minimal breakpoints -->
<div class="p-2 md:p-4 lg:p-6">
  <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4">
</div>

<!-- Bad: Redundant breakpoint definitions -->
<div class="p-2 sm:p-2 md:p-4 lg:p-4 xl:p-6">
  <div class="grid grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-2">
</div>
```

### 4.5 Dark Mode Efficiency

```javascript
// Good: Single dark mode strategy (JARVIS is always dark)
export default {
  darkMode: 'class',  // Use 'class' for explicit control
  theme: {
    extend: {
      colors: {
        jarvis: {
          bg: {
            dark: '#0a0a0f',  // Define dark colors directly
            panel: '#111827'
          }
        }
      }
    }
  }
}

// Bad: Light/dark variants when app is always dark
<div class="bg-white dark:bg-gray-900">  // Unnecessary light styles
```

### 4.6 Animation Performance

```javascript
// Good: GPU-accelerated properties
export default {
  theme: {
    extend: {
      keyframes: {
        glow: {
          '0%, 100%': { opacity: '0.5' },  // opacity is GPU-accelerated
          '50%': { opacity: '1' }
        }
      }
    }
  }
}

// Bad: Layout-triggering properties
keyframes: {
  resize: {
    '0%': { width: '100px' },  // Triggers layout recalc
    '100%': { width: '200px' }
  }
}
```

## 5. Technology Stack & Versions

### 5.1 Recommended Versions

| Package | Version | Notes |
|---------|---------|-------|
| tailwindcss | ^3.4.0 | Latest with JIT mode |
| @nuxtjs/tailwindcss | ^6.0.0 | Nuxt integration |
| tailwindcss-animate | ^1.0.0 | Animation utilities |

### 5.2 Configuration

```javascript
// tailwind.config.js
export default {
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './composables/**/*.ts',
    './plugins/**/*.ts'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        jarvis: {
          primary: '#00ff41',
          secondary: '#0891b2',
          warning: '#f59e0b',
          danger: '#ef4444',
          bg: {
            dark: '#0a0a0f',
            panel: '#111827'
          }
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'monospace'],
        display: ['Orbitron', 'sans-serif']
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'scan': 'scan 2s linear infinite',
        'glow': 'glow 2s ease-in-out infinite alternate'
      },
      keyframes: {
        scan: {
          '0%': { transform: 'translateY(-100%)' },
          '100%': { transform: 'translateY(100%)' }
        },
        glow: {
          '0%': { boxShadow: '0 0 5px #00ff41' },
          '100%': { boxShadow: '0 0 20px #00ff41' }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('tailwindcss-animate')
  ]
}
```

## 6. Implementation Patterns

### 6.1 HUD Panel Component

```vue
<template>
  <div class="
    relative
    bg-jarvis-bg-panel/80
    border border-jarvis-primary/30
    rounded-lg
    p-4
    backdrop-blur-sm
    shadow-lg shadow-jarvis-primary/10
  ">
    <!-- Scanline overlay -->
    <div class="
      absolute inset-0
      bg-gradient-to-b from-transparent via-jarvis-primary/5 to-transparent
      animate-scan
      pointer-events-none
    " />

    <!-- Content -->
    <div class="relative z-10">
      <h3 class="
        font-display
        text-jarvis-primary
        text-lg
        uppercase
        tracking-wider
        mb-2
      ">
        {{ title }}
      </h3>
      <slot />
    </div>
  </div>
</template>
```

### 6.2 Status Indicator

```vue
<template>
  <div class="flex items-center gap-2">
    <span :class="[
      'w-2 h-2 rounded-full',
      {
        'bg-jarvis-primary animate-pulse': status === 'active',
        'bg-jarvis-warning': status === 'warning',
        'bg-jarvis-danger animate-ping': status === 'error',
        'bg-gray-500': status === 'inactive'
      }
    ]" />
    <span class="text-sm text-gray-300">{{ label }}</span>
  </div>
</template>
```

### 6.3 Button Variants

```vue
<template>
  <button :class="[
    'px-4 py-2 rounded font-medium transition-all duration-200',
    'focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-jarvis-bg-dark',
    {
      'bg-jarvis-primary text-black hover:bg-jarvis-primary/90 focus:ring-jarvis-primary':
        variant === 'primary',
      'bg-transparent border border-jarvis-secondary text-jarvis-secondary hover:bg-jarvis-secondary/10 focus:ring-jarvis-secondary':
        variant === 'secondary',
      'bg-jarvis-danger text-white hover:bg-jarvis-danger/90 focus:ring-jarvis-danger':
        variant === 'danger'
    }
  ]">
    <slot />
  </button>
</template>
```

## 7. Quality Standards

### 7.1 Accessibility

```vue
<!-- Good - Sufficient contrast -->
<span class="text-jarvis-primary"><!-- #00ff41 on dark bg --></span>

<!-- Good - Focus visible -->
<button class="focus:ring-2 focus:ring-jarvis-primary focus:outline-none">

<!-- Good - Screen reader text -->
<span class="sr-only">Status: Active</span>
```

## 8. Common Mistakes & Anti-Patterns

### 8.1 Anti-Patterns

#### Avoid: Excessive Custom CSS

```vue
<!-- Bad - Custom CSS when utilities exist -->
<style>
.custom-panel {
  padding: 1rem;
  border-radius: 0.5rem;
}
</style>

<!-- Good - Use utilities -->
<div class="p-4 rounded-lg">
```

#### Avoid: Inconsistent Spacing

```vue
<!-- Bad - Mixed spacing values -->
<div class="p-3 mt-5 mb-2">

<!-- Good - Consistent scale -->
<div class="p-4 my-4">
```

#### Avoid: Hardcoded Colors

```vue
<!-- Bad - Hardcoded hex -->
<div class="text-[#00ff41]">

<!-- Good - Theme color -->
<div class="text-jarvis-primary">
```

## 9. Pre-Implementation Checklist

### Phase 1: Before Writing Code

- [ ] Write component tests for expected class applications
- [ ] Verify JARVIS theme colors are defined in config
- [ ] Check content paths include all source files
- [ ] Review existing components for reusable patterns

### Phase 2: During Implementation

- [ ] Use utilities before custom CSS
- [ ] Apply consistent spacing scale (4, 8, 12, 16...)
- [ ] Include focus states for all interactive elements
- [ ] Test responsive breakpoints at each size
- [ ] Use theme colors, never hardcoded hex values

### Phase 3: Before Committing

- [ ] All component tests pass: `npm test`
- [ ] Build completes without CSS errors: `npm run build`
- [ ] Check CSS bundle size hasn't grown unexpectedly
- [ ] Verify no unused @apply extractions
- [ ] Test accessibility with keyboard navigation

## 10. Summary

Tailwind CSS provides utility-first styling for JARVIS:

1. **TDD**: Write tests for class applications before implementation
2. **Performance**: Optimize content paths and use JIT mode
3. **Theme**: Define JARVIS colors and fonts in config
4. **Utilities**: Compose styles from utilities, extract patterns with @apply
5. **Accessibility**: Maintain focus states and sufficient contrast

**Remember**: The JARVIS HUD has a distinct visual identity - maintain consistency with the theme configuration and test all styling with vitest.

---

**References**:
- `references/advanced-patterns.md` - Complex layout patterns
