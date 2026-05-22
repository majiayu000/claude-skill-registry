---
name: nimbus-frontend
description: Guidelines for frontend development in the NimbusImage application including Vue 2, Vuetify, Vuex patterns, theming, and component structure.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Edit
  - Write
  - Task
  - TodoWrite
user-invocable: true
---

# Nimbus Frontend Development

Guidelines for frontend development in the NimbusImage application.

## Technology Stack

- **Vue 2.7** with TypeScript
- **Vuetify 2** for UI components
- **Vuex** with `vuex-module-decorators` for state management
- **vue-property-decorator** for class-style components
- **Vite** for build tooling

## Component Patterns

### Class-Style Components

Components use `vue-property-decorator`:

```typescript
import { Vue, Component, Prop, Watch } from "vue-property-decorator";

@Component
export default class MyComponent extends Vue {
  @Prop({ required: true }) readonly value!: string;

  localState = "";

  get computedValue() {
    return this.value.toUpperCase();
  }

  @Watch("value")
  onValueChange(newVal: string) {
    this.localState = newVal;
  }

  mounted() {
    // lifecycle hook
  }
}
```

### Store Access

Access Vuex stores directly:

```typescript
import store from "@/store";
import annotationStore from "@/store/annotation";

// In component
readonly store = store;
readonly annotationStore = annotationStore;

// Use in methods
this.store.someAction();
```

## Light/Dark Mode Theming

### Checking Theme State

```typescript
// In component
get isDarkMode() {
  return this.$vuetify.theme.dark;
}
```

### Theme-Aware Styling

**Option 1: Vuetify Components** (preferred)
Use Vuetify components like `v-card`, `v-dialog`, `v-btn` - they automatically inherit the theme.

**Option 2: Theme Classes in SCSS**

```scss
// For styles on elements that have the theme class directly
.my-component.theme--dark {
  background: rgba(255, 255, 255, 0.05);
}

.my-component.theme--light {
  background: rgba(0, 0, 0, 0.05);
}
```

**Option 3: Dynamic Class Binding**

```vue
<div :class="{ 'theme--light': !$vuetify.theme.dark, 'theme--dark': $vuetify.theme.dark }">
```

**Option 4: CSS Variables**

```scss
.my-element {
  color: var(--v-primary-base);
  background: var(--v-background-base);
}
```

### Theme Persistence

Theme preference is stored in localStorage via `Persister`:

```typescript
import { Persister } from "@/store/Persister";

// Get theme
const isDark = Persister.get("theme", "dark") === "dark";

// Set theme (usually done through $vuetify.theme.dark)
this.$vuetify.theme.dark = true;
```

## Dialogs

Use Vuetify's `v-dialog` with `max-width` for consistent sizing:

```vue
<v-dialog v-model="dialogOpen" max-width="600px">
  <v-card>
    <v-card-title>Title</v-card-title>
    <v-card-text>Content</v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn @click="dialogOpen = false">Close</v-btn>
    </v-card-actions>
  </v-card>
</v-dialog>
```

## File Organization

- `src/components/` - Reusable UI components
- `src/views/` - Route-level page components
- `src/tools/` - Tool creation and configuration UI
- `src/layout/` - App layout components
- `src/utils/` - Utility functions
- `src/store/` - Vuex store modules

## Common Patterns

### API Calls

Use the API classes from store:

```typescript
import { api } from "@/store/GirderAPI";

// In component or store action
const result = await api.someMethod();
```

### Emitting Events

```typescript
this.$emit("eventName", payload);
```

### Refs

```typescript
@Ref() readonly myElement!: HTMLElement;
```

## Logging

**Never use `console.log`, `console.warn`, or `console.error` directly** - eslint will reject them.

Use the logging utilities from `@/utils/log`:

```typescript
import { logWarning, logError } from "@/utils/log";

// Instead of console.warn()
logWarning("Something unexpected happened");

// Instead of console.error()
logError("An error occurred", error);
```

## Vuetify Patterns

### Button Loading States

When using `:loading` on `v-btn`, the default slot content is replaced with just a spinner. To show custom loading content (e.g., text + spinner), use the `loader` slot:

```vue
<v-btn
  :loading="isLoading"
  :disabled="isLoading"
  :min-width="isLoading ? 260 : undefined"
  @click="doAction"
>
  <template v-slot:loader>
    <v-progress-circular
      indeterminate
      size="18"
      width="2"
      class="mr-2"
    ></v-progress-circular>
    Loading...
  </template>
  <v-icon>mdi-check</v-icon>
  Submit
</v-btn>
```

Note: Use `:min-width` to ensure the button expands to fit longer loading text.

## Style Guidelines

- Use scoped SCSS: `<style lang="scss" scoped>`
- Prefer Vuetify components over custom HTML
- Use `!important` sparingly - only when overriding Vuetify internals
- Keep custom colors as SCSS variables at the top of style blocks
