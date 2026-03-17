---
name: maz-ui
description: Maz-UI v4 - Modern Vue & Nuxt component library with 50+ standalone components, composables, directives, theming, i18n, and SSR support. Use when building Vue/Nuxt applications with forms, dialogs, tables, animations, or need responsive design system with dark mode.
---

# Maz-UI v4 - Vue & Nuxt Component Library

Maz-UI is a comprehensive, standalone component library for Vue 3 and Nuxt 3 applications, offering 50+ production-ready components, powerful theming, internationalization, and exceptional developer experience.

**Latest Version**: 4.3.3 (as of 2025-12-29)
**Package**: `maz-ui` | `@maz-ui/nuxt` | `@maz-ui/themes` | `@maz-ui/translations` | `@maz-ui/icons`

## Quick Start

### Vue 3 Installation

```bash
# Install core packages
pnpm add maz-ui @maz-ui/themes

# Or with npm
npm install maz-ui @maz-ui/themes
```

**Setup** in `main.ts`:

```typescript
import { createApp } from 'vue'
import { MazUi } from 'maz-ui/plugins/maz-ui'
import { mazUi } from '@maz-ui/themes'
import { en } from '@maz-ui/translations'
import 'maz-ui/styles'
import App from './App.vue'

const app = createApp(App)

app.use(MazUi, {
  theme: { preset: mazUi },
  translations: { messages: { en } }
})

app.mount('#app')
```

**Use Components**:

```vue
<script setup>
import MazBtn from 'maz-ui/components/MazBtn'
import MazInput from 'maz-ui/components/MazInput'
import { ref } from 'vue'

const inputValue = ref('')
</script>

<template>
  <MazInput v-model="inputValue" label="Name" />
  <MazBtn color="primary">Submit</MazBtn>
</template>
```

###  Nuxt 3 Installation

```bash
# Install Nuxt module
pnpm add @maz-ui/nuxt
```

**Setup** in `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  modules: ['@maz-ui/nuxt']
  // That's it! Auto-imports enabled 🎉
})
```

**Use Components** (no imports needed):

```vue
<script setup>
// Auto-imported composables
const theme = useTheme()
const toast = useToast()
const inputValue = ref('')
</script>

<template>
  <!-- Auto-imported components -->
  <MazInput v-model="inputValue" label="Name" />
  <MazBtn color="primary" @click="toast.success('Submitted!')">
    Submit
  </MazBtn>
</template>
```

## Core Capabilities

### 🎨 Components (50+)

**Forms & Inputs**:
- `MazInput` - Text input with validation states
- `MazSelect` - Dropdown select
- `MazTextarea` - Multi-line text input
- `MazCheckbox` - Checkbox with label
- `MazRadio` - Radio buttons
- `MazSwitch` - Toggle switch
- `MazSlider` - Range slider
- `MazInputPhoneNumber` - International phone input with validation
- `MazInputCode` - Code/PIN input
- `MazInputPrice` - Currency input with formatting
- `MazInputTags` - Tag/chip input
- `MazDatePicker` - Date picker
- `MazChecklist` - Searchable checklist

**UI Elements**:
- `MazBtn` - Button with variants
- `MazCard` - Container card
- `MazBadge` - Label badge
- `MazAvatar` - User avatar
- `MazIcon` - Icon display
- `MazSpinner` - Loading spinner
- `MazTable` - Data table with sorting/pagination
- `MazTabs` - Tab navigation
- `MazStepper` - Step indicator
- `MazPagination` - Pagination controls

**Overlays & Modals**:
- `MazDialog` - Modal dialog
- `MazDialogConfirm` - Confirmation dialog
- `MazDrawer` - Slide-out drawer
- `MazBottomSheet` - Mobile bottom sheet
- `MazBackdrop` - Overlay backdrop
- `MazPopover` - Floating popover
- `MazDropdown` - Dropdown menu

**Feedback & Animation**:
- `MazFullscreenLoader` - Loading overlay
- `MazLoadingBar` - Progress bar
- `MazCircularProgressBar` - Circular progress
- `MazReadingProgressBar` - Reading progress indicator
- `MazAnimatedText` - Text animations
- `MazAnimatedElement` - Element animations
- `MazAnimatedCounter` - Number counter animation
- `MazCardSpotlight` - Card with spotlight effect

**Layout & Display**:
- `MazCarousel` - Image carousel
- `MazGallery` - Image gallery
- `MazAccordion` - Collapsible panels
- `MazExpandAnimation` - Expand/collapse animation
- `MazLazyImg` - Lazy-loaded image
- `MazPullToRefresh` - Pull-to-refresh gesture
- `MazChart` - Chart.js integration

### 🔧 Composables (14+)

**Theming**:
- `useTheme()` - Theme and dark mode management

**Translations**:
- `useTranslations()` - i18n management

**UI Interactions**:
- `useToast()` - Toast notifications
- `useDialog()` - Programmatic dialogs
- `useWait()` - Loading states

**Utilities**:
- `useBreakpoints()` - Responsive breakpoints
- `useWindowSize()` - Window dimensions
- `useTimer()` - Timer/countdown
- `useFormValidator()` - Form validation (Valibot)
- `useIdleTimeout()` - Idle detection
- `useUserVisibility()` - Page visibility
- `useSwipe()` - Swipe gestures
- `useReadingTime()` - Reading time calculation
- `useStringMatching()` - String utilities
- `useDisplayNames()` - Localized display names

### 📌 Directives (5)

- `v-tooltip` - Tooltips
- `v-click-outside` - Outside click detection
- `v-lazy-img` - Lazy loading
- `v-zoom-img` - Image zoom
- `v-fullscreen-img` - Fullscreen image viewer

### 🔌 Plugins (4)

- **AOS** - Animations on scroll
- **Dialog** - Template-free dialogs
- **Toast** - Notifications
- **Wait** - Global loading states

## Key Features

✅ **Standalone Components** - Import only what you need, zero bloat
✅ **SSR/SSG Ready** - Full Nuxt 3 support with auto-imports
✅ **TypeScript-First** - Complete type safety out of the box
✅ **Dark Mode** - Built-in dark/light theme switching
✅ **Tree-Shakable** - Optimized bundle sizes
✅ **Responsive** - Mobile-first design
✅ **Accessible** - ARIA-compliant components
✅ **Themeable** - 4 built-in presets + custom themes
✅ **i18n** - Multi-language support with @maz-ui/translations
✅ **840+ Icons** - Optimized SVG icon library (@maz-ui/icons)

## Template Structure

Maz-UI provides **two sets of production-ready templates** organized by framework:

### Vue 3 + Vite Templates (`templates/vue/`)
- ✅ Pure Vue 3 with Vite
- ✅ Uses standard `fetch()` API
- ✅ Explicit imports for all dependencies
- ✅ No framework-specific dependencies
- ✅ Optimized for SPA development

**Use when**: Building Vue 3 applications with Vite

**Available templates**:
- `setup/vite.config.ts` - Vite configuration with auto-imports
- `components/form-basic.vue` - Basic form validation
- `components/form-multi-step.vue` - Multi-step form with stepper
- `components/dialog-confirm.vue` - Dialog confirmation patterns
- `components/data-table.vue` - Data table with pagination, search, sort

### Nuxt 3 Templates (`templates/nuxt/`)
- ✅ Nuxt 3 optimized
- ✅ Uses `$fetch` (Nuxt's ofetch wrapper)
- ✅ Leverages auto-imports for components and composables
- ✅ Showcases SSR patterns and server routes
- ✅ Optimized for full-stack Nuxt development

**Use when**: Building Nuxt 3 applications

**Available templates**:
- `setup/nuxt.config.ts` - Nuxt configuration with Maz-UI module
- `components/form-basic.vue` - Basic form validation (auto-imports)
- `components/form-multi-step.vue` - Multi-step form (auto-imports)
- `components/dialog-confirm.vue` - Dialog patterns (auto-imports)
- `components/data-table.vue` - Data table with reactive data loading

Both template sets:
- ✅ Fix all validation, type inference, and pagination issues
- ✅ Follow framework best practices
- ✅ Are production-ready and fully tested
- ✅ Include setup configs and component examples

## When to Load References

Load reference files based on what you're implementing. All 21 reference files are grouped by purpose for quick discovery:

### Components (4 files)
- **`components-forms.md`** - Building forms, inputs, validation, phone numbers, dates, file uploads, MazInput, MazSelect, MazCheckbox, MazDatePicker
- **`components-feedback.md`** - Adding loaders, progress bars, animations, toasts, MazFullscreenLoader, MazCircularProgressBar, MazAnimatedText, MazCardSpotlight
- **`components-navigation.md`** - Implementing tabs, steppers, pagination, MazTabs, MazStepper, MazPagination
- **`components-layout.md`** - Working with cards, drawers, carousels, galleries, MazCard, MazAccordion, MazDrawer, MazCarousel, MazGallery

### Setup & Configuration (2 files)
- **`setup-vue.md`** - Setting up Maz-UI in Vue 3 project, auto-imports with resolvers, Vite/Webpack configuration, performance optimization
- **`setup-nuxt.md`** - Integrating with Nuxt 3, module configuration, theme strategies (hybrid/buildtime/runtime), SSR/SSG considerations

### Core Features (5 files)
- **`composables.md`** - Using all 14 composables: useToast, useTheme, useBreakpoints, useFormValidator, useTimer, useDialog, useTranslations, etc.
- **`directives.md`** - Adding directives: v-tooltip, v-click-outside, v-lazy-img, v-zoom-img, v-fullscreen-img
- **`plugins.md`** - Enabling plugins: AOS (animations on scroll), Dialog, Toast, Wait (loading states)
- **`resolvers.md`** - **CRITICAL**: Auto-import configuration with MazComponentsResolver, MazDirectivesResolver, MazModulesResolver for optimal tree-shaking
- **`translations.md`** - Implementing multi-language support (8 built-in languages), custom locales, lazy loading, SSR hydration

### Tools & Integrations (3 files)
- **`icons.md`** - Using @maz-ui/icons package (840+ icons), MazIcon component, icon sizing, colors, animations
- **`cli.md`** - Using @maz-ui/cli (legacy v3), theme configuration, migration to v4 themes system
- **`mcp.md`** - Setting up Model Context Protocol server for AI assistant integration (Claude Code, Claude Desktop, Cursor, Windsurf)

### Advanced Topics (5 files)
- **`theming.md`** - Customizing themes, dark mode, color schemes, CSS variables, 4 built-in presets (mazUi, ocean, pristine, obsidian)
- **`performance.md`** - Bundle optimization, tree-shaking, lazy loading, code splitting, reducing bundle size from ~300KB to ~15KB
- **`ssr-ssg.md`** - **Comprehensive SSR/SSG guide**: theme strategies, critical CSS, hydration prevention, dark mode without flash, static site generation
- **`accessibility.md`** - WCAG 2.1 AA compliance, keyboard navigation, screen reader support, ARIA attributes, color contrast
- **`form-validation.md`** - useFormValidator deep dive, Valibot integration, 5 validation modes (lazy, aggressive, eager, blur, progressive), TypeScript type inference

### Troubleshooting (2 files)
- **`migration-v4.md`** - Upgrading from Maz-UI v3 to v4, breaking changes, API changes, component renames, TypeScript updates
- **`troubleshooting.md`** - Debugging errors, common issues, configuration problems, SSR hydration, bundle size issues

## Top 6 Common Errors

### 1. Missing Theme Plugin Error
**Error**: `"useTheme must be used within MazUi plugin installation"`
**Cause**: MazUi plugin not installed or theme composable disabled
**Fix**:
```typescript
// Vue
app.use(MazUi, { theme: { preset: mazUi } })

// Nuxt
export default defineNuxtConfig({
  mazUi: {
    composables: { useTheme: true },
    theme: { preset: 'maz-ui' }
  }
})
```

### 2. Auto-Import Not Working (Nuxt)
**Error**: Components/composables not found despite Nuxt module installed
**Cause**: Module not properly configured or cache issue
**Fix**:
```bash
# Clear Nuxt cache
rm -rf .nuxt node_modules/.cache
pnpm install
```
**Verify** `nuxt.config.ts`:
```typescript
export default defineNuxtConfig({
  modules: ['@maz-ui/nuxt']
})
```

### 3. Styles Not Applied
**Error**: Components render but have no styling
**Cause**: CSS not imported
**Fix Vue**:
```typescript
import 'maz-ui/styles' // Add this line
```
**Fix Nuxt**:
```typescript
export default defineNuxtConfig({
  mazUi: {
    css: { injectMainCss: true } // Ensure this is true
  }
})
```

### 4. TypeScript Errors with Components
**Error**: `Cannot find module 'maz-ui/components/MazBtn'`
**Cause**: Missing type definitions or incorrect import path
**Fix**:
```typescript
// Correct import
import MazBtn from 'maz-ui/components/MazBtn'

// Or with auto-import (Nuxt)
// No import needed, just use <MazBtn>
```
**Ensure** `tsconfig.json` includes:
```json
{
  "compilerOptions": {
    "types": ["maz-ui/types"]
  }
}
```

### 5. Phone Input Country Detection Fails
**Error**: `MazInputPhoneNumber` doesn't detect country or shows wrong flag
**Cause**: Missing libphonenumber-js dependency or country data not loaded
**Fix**:
```bash
# Install peer dependency
pnpm add libphonenumber-js
```
```vue
<MazInputPhoneNumber
  v-model="phone"
  default-country-code="US"
  preferred-countries="['US', 'CA', 'GB']"
/>
```

### 6. Translations Not Loading or Showing Raw Keys
**Error**: Translation keys showing as raw strings like `inputPhoneNumber.phoneInput.example` instead of translated text
**Causes**:
- Missing locale import
- Lazy loading not awaited properly
- Language file failed to load asynchronously
- Missing `preloadFallback` configuration
- SSR hydration mismatch (Nuxt)

**Fix Vue** (Immediate Loading):
```typescript
import { fr } from '@maz-ui/translations'

app.use(MazUi, {
  translations: {
    locale: 'fr',
    fallbackLocale: 'en',
    preloadFallback: true,
    messages: { fr } // Import immediately
  }
})
```

**Fix Vue** (Lazy Loading):
```typescript
app.use(MazUi, {
  translations: {
    locale: 'fr',
    preloadFallback: true, // Ensure fallback is preloaded
    messages: {
      fr: () => import('@maz-ui/translations/locales/fr')
    }
  }
})

// In component: ALWAYS use await
const { setLocale } = useTranslations()
await setLocale('fr') // Don't forget await!
```

**Fix Nuxt** (Avoid Hydration):
```typescript
import { fr } from '@maz-ui/translations'

export default defineNuxtConfig({
  mazUi: {
    translations: {
      locale: 'fr',
      preloadFallback: true,
      messages: {
        // CRITICAL: Provide initial locale immediately (not as function)
        fr, // SSR requires immediate load

        // Other languages can be lazy
        es: () => import('@maz-ui/translations/locales/es')
      }
    }
  }
})
```

**Error Handling**:
```vue
<script setup>
const { setLocale } = useTranslations()
const toast = useToast()

async function switchLanguage(locale) {
  try {
    await setLocale(locale)
    toast.success(`Language changed to ${locale}`)
  } catch (error) {
    console.error('Translation loading error:', error)
    toast.error('Failed to load translations')
  }
}
</script>
```

**Learn More**: Load `references/translations.md` for comprehensive i18n setup, lazy loading strategies, and production patterns.

## Tree-Shaking Best Practices

**Direct Imports** (Most Optimized):
```typescript
// ✅✅✅ Best - smallest bundle
import MazBtn from 'maz-ui/components/MazBtn'
import { useToast } from 'maz-ui/composables/useToast'
import { vClickOutside } from 'maz-ui/directives/vClickOutside'
```

**Index Imports** (Good):
```typescript
// ✅ Good - tree-shakable
import { MazBtn, MazInput } from 'maz-ui/components'
import { useToast, useTheme } from 'maz-ui/composables'
```

**Avoid** (Not Tree-Shakable):
```typescript
// ❌ Imports everything
import * as MazUI from 'maz-ui'
```

## Advanced Topics

### Performance Optimization

Maz-UI can be optimized from ~300KB to ~15KB through strategic imports and tree-shaking. Use auto-import resolvers (`MazComponentsResolver`, `MazDirectivesResolver`, `MazModulesResolver`) for optimal bundle size, lazy load components with dynamic imports, and split code by feature. Load **`performance.md`** for comprehensive bundle optimization strategies.

### SSR & SSG

Full server-side rendering and static site generation support with three theme strategies: **hybrid** (critical CSS injection, no FOUC), **buildtime** (smallest bundle, static themes), and **runtime** (full theme switching, larger bundle). Prevent hydration mismatches by wrapping client-only components in `<ClientOnly>`. Load **`ssr-ssg.md`** for critical CSS patterns, dark mode without flash, and SSR/SSG checklist.

### Accessibility

All Maz-UI components are WCAG 2.1 AA compliant with proper ARIA attributes, keyboard navigation, focus management, and screen reader support. Components include semantic HTML, color contrast ratios >4.5:1, and accessible form validation. Load **`accessibility.md`** for keyboard shortcuts, focus trap patterns, and accessibility testing checklist.

### Form Validation

The `useFormValidator()` composable integrates with Valibot for type-safe schema validation with full TypeScript inference. Supports 5 validation modes (lazy, aggressive, eager, blur, progressive), async validation, custom validators, and real-time error messages. Load **`form-validation.md`** for comprehensive validation patterns and real-world examples.

### Auto-Import Resolvers

**Critical for tree-shaking**: Use `unplugin-vue-components` and `unplugin-auto-import` with Maz-UI resolvers to import only what you use. Reduces bundle size by 60-90% compared to global imports. Configure prefix handling to avoid naming conflicts with other libraries. Load **`resolvers.md`** for complete resolver configuration and troubleshooting.

## Progressive Disclosure Summary

This SKILL.md provides:
1. **Quick Start** - Get running in <5 minutes
2. **Core Capabilities** - Overview of all features
3. **Error Prevention** - Top 5 common issues solved

For detailed implementation:
- Load **reference files** based on your current task (see "When to Load References" above)
- Each reference contains comprehensive guides, code examples, and advanced configurations
- References are organized by domain (components, setup, theming, etc.) for easy navigation

## Package Ecosystem

- **maz-ui** - Core component library
- **@maz-ui/nuxt** - Nuxt 3 module with auto-imports
- **@maz-ui/themes** - Theming system and presets
- **@maz-ui/translations** - i18n support (8 built-in languages: en, fr, es, de, it, pt, ja, zh-CN)
- **@maz-ui/icons** - 840+ optimized SVG icons
- **@maz-ui/mcp** - AI agent documentation server

## Official Resources

- **Documentation**: https://maz-ui.com
- **GitHub**: https://github.com/LouisMazel/maz-ui
- **NPM**: https://www.npmjs.com/package/maz-ui
- **Discord**: https://discord.gg/maz-ui
- **Changelog**: https://github.com/LouisMazel/maz-ui/blob/master/CHANGELOG.md
