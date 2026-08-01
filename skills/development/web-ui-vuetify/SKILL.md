---
name: web-ui-vuetify
description: Material Design component library for Vue 3
---

# Vuetify Patterns

> **Quick Guide:** Vuetify provides 80+ pre-styled Vue 3 components implementing Material Design. Configure with `createVuetify()` -- set `theme` for colors, `defaults` for global component props, and `blueprint: md3` for MD3 compliance. Use `v-defaults-provider` for scoped prop overrides. Customize at the SASS level with `@use 'vuetify/settings'` for compile-time changes. **Current: v3.8.x** -- `useRules` composable for form validation, date picker improvements, performance optimizations. Vuetify is **template-driven** -- prefer declarative props/slots over imperative JS.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST install and register Vuetify as a Vue plugin via `app.use(vuetify)` -- components will not render without the plugin)**

**(You MUST use the `defaults` system in `createVuetify()` or `v-defaults-provider` for consistent component props -- never repeat the same prop on every instance)**

**(You MUST use named slots (`v-slot:item.<key>`, `v-slot:prepend`) for component customization -- not wrapper divs with manual styling)**

**(You MUST define `v-data-table` headers and column arrays outside the component -- inline arrays cause re-renders on every parent update)**

</critical_requirements>

---

**Auto-detection:** Vuetify, vuetify, createVuetify, v-btn, v-card, v-data-table, v-text-field, v-select, v-autocomplete, v-dialog, v-navigation-drawer, v-app-bar, v-toolbar, v-chip, v-snackbar, v-form, v-defaults-provider, v-theme-provider, useTheme, useDisplay, useDate, useRules, mdi, @mdi/font, vuetify/blueprints, vuetify/settings, vuetify/styles

**When to use:**

- Building Vue 3 applications with pre-styled Material Design components
- Rapid development of admin dashboards, data tables, and CRUD interfaces
- Projects that benefit from a comprehensive defaults/theming system
- Applications requiring built-in accessibility, RTL, and i18n support

**When NOT to use:**

- Non-Vue projects (Vuetify is Vue-only)
- Projects requiring a non-Material Design aesthetic without heavy customization
- Minimal bundle size is critical and only a few components are needed (consider a headless library)
- Projects using Vue 2 (Vuetify 3 requires Vue 3)

**Key patterns covered:**

- Plugin setup with `createVuetify()`, themes, and blueprints
- Global defaults and scoped defaults with `v-defaults-provider`
- SASS variable customization at compile time
- Slot-based component customization
- Data tables with sorting, filtering, pagination, and custom column rendering
- Form validation with rules arrays and `useRules` composable
- Theme toggling and `useTheme` / `useDisplay` composables

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) -- Plugin setup, theming, defaults, SASS variables, blueprints, TypeScript, composables
- [examples/data-tables.md](examples/data-tables.md) -- v-data-table headers, slots, sorting, filtering, pagination, server-side
- [examples/forms.md](examples/forms.md) -- v-form, validation rules, useRules, input components, custom validation
- [examples/layout.md](examples/layout.md) -- v-app, v-app-bar, v-navigation-drawer, v-container/v-row/v-col grid, responsive patterns
- [reference.md](reference.md) -- Decision frameworks, component quick reference, anti-patterns

---

<philosophy>

## Philosophy

Vuetify is an **opinionated, batteries-included** component library. Unlike headless libraries, Vuetify ships styled components with a complete design system. Its power comes from three layers of customization:

1. **Theme layer** -- colors, dark mode, typography via `createVuetify({ theme })`. All components inherit automatically.
2. **Defaults layer** -- global or scoped prop values via `defaults` config or `v-defaults-provider`. Change every `v-btn` to `variant="outlined"` in one line.
3. **SASS layer** -- compile-time variable overrides via `@use 'vuetify/settings'`. Changes border-radius, heights, font families at the CSS level.

**Vuetify 3.x key features:**

- Full Vue 3 Composition API support
- Tree-shakeable components via `vuetify-loader` / `vite-plugin-vuetify`
- Material Design 3 blueprint (`md3`) for MD3 compliance
- Built-in composables: `useTheme`, `useDisplay`, `useDate`, `useRules`
- `v-defaults-provider` for scoped prop cascading (unique to Vuetify)
- Extensive slot system for deep component customization without CSS hacks
- Built-in i18n, RTL, and accessibility

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Plugin Setup

Every Vuetify app requires `createVuetify()` and `app.use()`. The plugin provides the theme, defaults, icons, and locale to all components.

```typescript
import { createApp } from "vue";
import { createVuetify } from "vuetify";

const vuetify = createVuetify({
  theme: {
    defaultTheme: "light",
    themes: {
      light: {
        colors: {
          primary: "#1867C0",
          secondary: "#5CBBF6",
        },
      },
    },
  },
  defaults: {
    VBtn: { variant: "flat", rounded: "lg" },
    VTextField: { variant: "outlined", density: "comfortable" },
    VCard: { elevation: 2, rounded: "lg" },
  },
});

const app = createApp(App);
app.use(vuetify);
app.mount("#app");
```

**Why good:** single configuration point, all components inherit theme and default props, tree-shakeable

For blueprints, SASS variables, TypeScript augmentation, and SSR setup, see [examples/core.md](examples/core.md).

---

### Pattern 2: Theming and Dark Mode

Define multiple themes in `createVuetify` and toggle with `useTheme`. Vuetify generates CSS variables for each theme.

```vue
<script setup>
import { useTheme } from "vuetify";

const theme = useTheme();

function toggleTheme() {
  theme.global.name.value = theme.global.current.value.dark ? "light" : "dark";
}
</script>

<template>
  <v-btn @click="toggleTheme" icon="mdi-brightness-6" />
</template>
```

**Why good:** reactive theme switching, CSS variables prevent flash of wrong theme, custom themes can extend built-in ones

For custom theme creation and color variations, see [examples/core.md](examples/core.md).

---

### Pattern 3: Global Defaults and Scoped Defaults

The `defaults` system is Vuetify's most powerful consistency tool. Set props globally in `createVuetify()` or scope them with `v-defaults-provider`.

```vue
<template>
  <!-- All buttons inside this provider get these defaults -->
  <v-defaults-provider
    :defaults="{
      VBtn: { color: 'secondary', variant: 'tonal' },
      VCard: { elevation: 0, border: true },
    }"
  >
    <v-card>
      <v-card-text>
        <!-- This button is tonal + secondary without explicit props -->
        <v-btn>Scoped Default</v-btn>
      </v-card-text>
    </v-card>
  </v-defaults-provider>
</template>
```

**Why good:** eliminates prop repetition, section-specific styling without CSS, nests and cascades like CSS scoping

---

### Pattern 4: Slot-Based Component Customization

Vuetify components expose named slots for every internal element. Use `v-slot` to replace or augment internal rendering.

```vue
<template>
  <v-text-field label="Amount" type="number">
    <template v-slot:prepend-inner>
      <v-icon>mdi-currency-usd</v-icon>
    </template>
    <template v-slot:append-inner>
      <v-chip size="x-small" color="success">.00</v-chip>
    </template>
  </v-text-field>
</template>
```

**Why good:** customizes internal elements without CSS overrides, type-safe slot props, preserves component behavior

For data table column slots, see [examples/data-tables.md](examples/data-tables.md).

---

### Pattern 5: Data Table Overview

`v-data-table` handles sorting, pagination, filtering, and selection. Define headers outside the template, use `v-slot:item.<key>` for custom column rendering.

```vue
<script setup>
const headers = [
  { title: "Name", key: "name" },
  { title: "Status", key: "status" },
  { title: "Actions", key: "actions", sortable: false },
];
</script>

<template>
  <v-data-table :items="items" :headers="headers">
    <template v-slot:item.status="{ item }">
      <v-chip
        :color="item.status === 'active' ? 'success' : 'error'"
        size="small"
      >
        {{ item.status }}
      </v-chip>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon size="small" @click="edit(item)">mdi-pencil</v-icon>
    </template>
  </v-data-table>
</template>
```

**Why good:** headers array is stable (no re-render), slot customization per column, built-in sort/filter/paginate

For server-side data tables, expandable rows, and search, see [examples/data-tables.md](examples/data-tables.md).

---

### Pattern 6: Form Validation

Vuetify forms use `:rules` arrays on inputs. Each rule is a function returning `true` or an error string. The `useRules` composable (v3.8+) provides common validators.

```vue
<script setup>
import { ref } from "vue";
import { useRules } from "vuetify/labs/rules";

const form = ref(null);
const email = ref("");
const rules = useRules();

async function submit(event: SubmitEvent) {
  const { valid } = await form.value.validate();
  if (!valid) return;
  // proceed with submission
}
</script>

<template>
  <v-form ref="form" validate-on="submit" @submit.prevent="submit">
    <v-text-field
      v-model="email"
      label="Email"
      :rules="[rules.required(), rules.email()]"
    />
    <v-btn type="submit" color="primary">Submit</v-btn>
  </v-form>
</template>
```

**Why good:** declarative validation, `useRules` eliminates boilerplate rule functions, `validate-on` controls timing

For custom rules, multi-field validation, and input types, see [examples/forms.md](examples/forms.md).

---

### Pattern 7: Responsive Design with useDisplay

The `useDisplay` composable provides reactive breakpoint state. Use it for logic-driven responsive behavior (template responsiveness uses Vuetify's grid props).

```vue
<script setup>
import { useDisplay } from "vuetify";

const { mobile, mdAndUp, name } = useDisplay();
</script>

<template>
  <v-navigation-drawer v-if="mdAndUp" permanent />
  <v-navigation-drawer v-else v-model="drawer" temporary />
  <v-app-bar :density="mobile ? 'compact' : 'default'" />
</template>
```

**Why good:** reactive breakpoint booleans, avoids CSS media query duplication in script, matches Vuetify's breakpoint system

</patterns>

---

<performance>

## Performance

### Tree-Shaking

Use `vite-plugin-vuetify` (Vite) or `webpack-plugin-vuetify` (Webpack) for automatic tree-shaking. Only imported components are bundled.

```typescript
// vite.config.ts
import vuetify from "vite-plugin-vuetify";

export default {
  plugins: [vuetify({ autoImport: true })],
};
```

Without the plugin, import `vuetify/components` and `vuetify/directives` to include everything (larger bundle).

### Stable References

```typescript
// GOOD: headers defined outside component
const headers: DataTableHeader[] = [{ title: "Name", key: "name" }];

// BAD: inline array recreated every render
// <v-data-table :headers="[{ title: 'Name', key: 'name' }]" />
```

### SASS Variable Customization vs Runtime Theming

```
Need to change at runtime? --> Use theme colors in createVuetify()
Need compile-time CSS changes? --> Use SASS variables (@use 'vuetify/settings')
Need per-section prop defaults? --> Use v-defaults-provider (zero CSS cost)
```

</performance>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Missing `app.use(vuetify)` -- components render as empty custom elements without the plugin
- Inline header/column arrays on `v-data-table` -- causes full table re-render on every parent update
- Using `this.$vuetify` in Composition API -- use `useTheme()`, `useDisplay()`, `useDate()` composables instead
- Importing `vuetify/components` and `vuetify/directives` when `vite-plugin-vuetify` is available -- negates tree-shaking

**Medium Priority Issues:**

- Setting `variant`, `density`, `rounded` on every component instance -- use `defaults` in `createVuetify()` instead
- Wrapping Vuetify components in extra divs for styling -- use the component's own props/slots/classes
- Hardcoding colors (`#1867C0`) in templates instead of using theme colors (`color="primary"`)
- Using `v-if` to toggle dialogs/drawers instead of `v-model` -- loses transition animations and internal state

**Common Mistakes:**

- Forgetting `import 'vuetify/styles'` when not using the build plugin -- no styles load at all
- Using CSS `!important` to override Vuetify styles -- use SASS variables or `class` prop with higher specificity
- Not setting `validate-on` on `v-form` -- defaults to `input` which validates on every keystroke (use `"submit"` or `"blur lazy"` for better UX)
- Placing `v-col` without a parent `v-row` inside `v-container` -- grid system requires the full nesting

**Gotchas & Edge Cases:**

- `density` accepts `"default"`, `"comfortable"`, `"compact"` -- it is NOT a numeric value
- `v-data-table-server` is a separate component for server-side pagination -- do not use `v-data-table` with manual pagination
- `v-defaults-provider` cascades -- nested providers merge with parent, later values win
- `useDisplay` breakpoints differ from CSS breakpoints in default config (xs: 0, sm: 600, md: 960, lg: 1280, xl: 1920, xxl: 2560)
- Theme `variations` generate `-lighten-N` and `-darken-N` color variants automatically -- do not manually define them
- `v-model` on `v-dialog` controls visibility -- do not use `value` prop (Vue 3 `v-model` replaces `.sync`)
- SASS variables require the Vite/Webpack plugin with `styles.configFile` pointing to your settings file

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST install and register Vuetify as a Vue plugin via `app.use(vuetify)` -- components will not render without the plugin)**

**(You MUST use the `defaults` system in `createVuetify()` or `v-defaults-provider` for consistent component props -- never repeat the same prop on every instance)**

**(You MUST use named slots (`v-slot:item.<key>`, `v-slot:prepend`) for component customization -- not wrapper divs with manual styling)**

**(You MUST define `v-data-table` headers and column arrays outside the component -- inline arrays cause re-renders on every parent update)**

**Failure to follow these rules will produce unstyled components, unnecessary re-renders, and inconsistent UI.**

</critical_reminders>
