---
name: web-utilities-vueuse
description: VueUse composable utility collection for Vue 3 - browser, sensor, network, state, animation, and component utilities
---

# VueUse Composable Patterns

> **Quick Guide:** VueUse provides 250+ composable functions for Vue 3 that wrap browser APIs, sensors, network, state, and component logic into reactive composables. Import individual functions from `@vueuse/core` for tree-shaking. All composables return reactive refs and follow Vue Composition API conventions. Use `useLocalStorage` for persistent state, `useFetch` for reactive HTTP, `useIntersectionObserver` for visibility detection, `createGlobalState` for shared state, and `useVModel` for two-way binding helpers. Always call composables in `<script setup>` or `setup()` synchronously. Clean up is automatic via Vue's lifecycle.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST call VueUse composables synchronously inside `<script setup>` or `setup()` -- NEVER inside async callbacks, setTimeout, or conditional blocks)**

**(You MUST use `shallowRef` instead of `ref` for large objects/arrays in VueUse composables to avoid deep reactivity overhead)**

**(You MUST handle SSR by checking `typeof window !== "undefined"` or using VueUse's built-in SSR-safe composables -- browser APIs crash during server rendering)**

**(You MUST import individual composables from `@vueuse/core` -- NEVER use `import * as vueuse` which defeats tree-shaking)**

</critical_requirements>

---

**Auto-detection:** VueUse, vueuse, @vueuse/core, @vueuse/integrations, useLocalStorage, useSessionStorage, useClipboard, useFetch, useMouse, useScroll, useIntersectionObserver, useResizeObserver, useElementVisibility, useMediaQuery, usePreferredDark, useDark, useToggle, useCounter, useCycleList, useWebSocket, useEventSource, useEventListener, useTransition, useRafFn, createGlobalState, useRefHistory, syncRef, useVModel, useVirtualList, onClickOutside, onKeyStroke, createFetch

**When to use:**

- Browser API access with reactive wrappers (localStorage, clipboard, media queries)
- Sensor data as reactive refs (mouse position, scroll, resize, intersection)
- Reactive HTTP requests with abort, refetch, and interceptors
- Global state shared across components without a state management library
- Component utilities (v-model helpers, virtual lists, keyboard shortcuts)
- SSR-safe browser API access

**When NOT to use:**

- Complex state management with actions/mutations (use a dedicated state solution)
- Server-side data fetching with caching/invalidation (use your data-fetching solution)
- Simple one-off operations that don't need reactivity
- Non-Vue projects (VueUse depends on Vue 3's reactivity system)

**Key patterns covered:**

- Core utilities (`useToggle`, `useCounter`, `useCycleList`)
- Browser composables (`useLocalStorage`, `useClipboard`, `useMediaQuery`, `useEventListener`)
- Sensor composables (`useMouse`, `useScroll`, `useIntersectionObserver`, `useResizeObserver`)
- Network composables (`useFetch`, `useWebSocket`, `useEventSource`)
- State composables (`createGlobalState`, `useRefHistory`, `syncRef`)
- Component composables (`useVModel`, `useVirtualList`, `onClickOutside`, `onKeyStroke`)
- Animation composables (`useTransition`, `useRafFn`)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Core utilities, browser APIs, event listeners
- [examples/sensors.md](examples/sensors.md) - Mouse, scroll, intersection, resize, visibility
- [examples/network.md](examples/network.md) - useFetch, useWebSocket, useEventSource
- [examples/state.md](examples/state.md) - createGlobalState, useRefHistory, syncRef, persistence
- [examples/component.md](examples/component.md) - useVModel, useVirtualList, onClickOutside, onKeyStroke
- [reference.md](reference.md) - Composable decision framework, SSR guide, gotchas

---

<philosophy>

## Philosophy

VueUse follows the **Composition API composable pattern**: encapsulate reactive logic in reusable functions that return refs and methods. Each composable wraps a single concern (a browser API, sensor, or utility) and handles setup/teardown automatically via Vue's lifecycle.

**Key principle:** VueUse composables are designed for tree-shaking. Import only what you use -- each function is independently importable with minimal overhead.

```typescript
import { useLocalStorage, useDark, useMediaQuery } from "@vueuse/core";

// Reactive localStorage -- syncs across tabs
const userName = useLocalStorage("user-name", "Guest");

// Dark mode with auto-detection
const isDark = useDark();

// Responsive breakpoint
const MOBILE_BREAKPOINT = "(max-width: 768px)";
const isMobile = useMediaQuery(MOBILE_BREAKPOINT);
```

### When to Use VueUse

- Wrapping browser APIs with reactivity (localStorage, clipboard, geolocation)
- Tracking DOM state reactively (scroll position, element visibility, mouse)
- Lightweight global state without full store setup
- Component utilities (keyboard shortcuts, click outside, virtual lists)
- Reactive data fetching for simple cases

### When NOT to Use VueUse

- Complex server state with caching, invalidation, optimistic updates (use your data-fetching solution)
- Complex client state with computed derivations and devtools (use a dedicated state solution)
- Non-Vue projects (the reactivity system is Vue-specific)
- When native browser API is sufficient without reactivity

### Current Version

VueUse **v14.x** is the current stable release, supporting Vue 3.5+. All composables are written in TypeScript with full type inference.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Reactive Storage (useLocalStorage, useSessionStorage)

Persistent reactive state that syncs with browser storage and across tabs.

```vue
<script setup lang="ts">
import { useLocalStorage, useSessionStorage } from "@vueuse/core";

interface UserPreferences {
  theme: "light" | "dark";
  fontSize: number;
  sidebarCollapsed: boolean;
}

const DEFAULT_PREFERENCES: UserPreferences = {
  theme: "light",
  fontSize: 14,
  sidebarCollapsed: false,
};

// ✅ Good Example - Typed reactive localStorage
const preferences = useLocalStorage<UserPreferences>(
  "user-prefs",
  DEFAULT_PREFERENCES,
);

// Read and write like a normal ref
preferences.value.theme = "dark"; // auto-persists to localStorage

// Session-only storage (cleared on tab close)
const sessionToken = useSessionStorage("session-token", "");

// Remove from storage
preferences.value = null; // removes the key from localStorage
</script>
```

**Why good:** automatic serialization/deserialization, cross-tab sync via storage events, typed with generics, cleanup is automatic

```typescript
// ❌ Bad Example - Manual localStorage
const prefs = ref(JSON.parse(localStorage.getItem("user-prefs") ?? "null"));

watch(
  prefs,
  (val) => {
    localStorage.setItem("user-prefs", JSON.stringify(val)); // manual sync
  },
  { deep: true },
);
// No cross-tab sync, no automatic cleanup, error-prone serialization
```

**Why bad:** manual serialization is error-prone, no cross-tab sync, no SSR safety, deep watcher on every change is expensive

---

### Pattern 2: Event Listeners (useEventListener)

Auto-cleaned event listeners with type safety.

```vue
<script setup lang="ts">
import { useEventListener } from "@vueuse/core";
import { useTemplateRef } from "vue";

const buttonRef = useTemplateRef("button");

// ✅ Good Example - Auto-cleanup event listeners
// Automatically removed when component unmounts
useEventListener(window, "resize", () => {
  console.log("Window resized:", window.innerWidth);
});

// Works with template refs -- waits for mount
useEventListener(buttonRef, "click", (event) => {
  console.log("Button clicked:", event);
});

// Multiple events on same target
useEventListener(document, "visibilitychange", () => {
  console.log("Visibility:", document.visibilityState);
});
</script>
```

**Why good:** automatic cleanup on unmount prevents memory leaks, handles ref lifecycle (waits for mount), type-safe event names

```typescript
// ❌ Bad Example - Manual event listener
onMounted(() => {
  window.addEventListener("resize", handleResize);
});
onUnmounted(() => {
  window.removeEventListener("resize", handleResize); // easy to forget!
});
```

**Why bad:** manual add/remove is error-prone -- missing `onUnmounted` cleanup causes memory leaks

---

### Pattern 3: Media Queries and Dark Mode

Reactive responsive design and theme management.

```vue
<script setup lang="ts">
import {
  useMediaQuery,
  usePreferredDark,
  useDark,
  useToggle,
} from "@vueuse/core";

// ✅ Good Example - Reactive breakpoints
const MOBILE_BREAKPOINT = "(max-width: 768px)";
const TABLET_BREAKPOINT = "(min-width: 769px) and (max-width: 1024px)";

const isMobile = useMediaQuery(MOBILE_BREAKPOINT);
const isTablet = useMediaQuery(TABLET_BREAKPOINT);

// System preference detection
const prefersDark = usePreferredDark();

// Full dark mode with toggle (adds class to html element)
const isDark = useDark();
const toggleDark = useToggle(isDark);
</script>

<template>
  <nav :class="{ 'nav--compact': isMobile }">
    <button @click="toggleDark()">
      {{ isDark ? "Light Mode" : "Dark Mode" }}
    </button>
  </nav>
</template>
```

**Why good:** reactive media queries update the ref automatically on resize, `useDark` handles class toggling and persistence, `useToggle` provides a clean toggle function

---

### Pattern 4: Clipboard Access

Reactive clipboard API with permission handling.

```vue
<script setup lang="ts">
import { useClipboard } from "@vueuse/core";

// ✅ Good Example - Clipboard with feedback
const source = ref("Text to copy");
const { text, copy, copied, isSupported } = useClipboard({ source });

async function handleCopy(): Promise<void> {
  await copy(); // copies source.value to clipboard
  // `copied` ref is true for 1.5s (default) after copy
}
</script>

<template>
  <div v-if="isSupported">
    <button @click="handleCopy">
      {{ copied ? "Copied!" : "Copy" }}
    </button>
  </div>
  <div v-else>Clipboard API not supported</div>
</template>
```

**Why good:** `isSupported` check for graceful degradation, `copied` provides automatic feedback timing, `source` reactive binding

---

### Pattern 5: Core Utilities (useToggle, useCounter, useCycleList)

Simple reactive utilities for common state patterns.

```vue
<script setup lang="ts">
import { useToggle, useCounter, useCycleList } from "@vueuse/core";

// ✅ Good Example - Toggle state
const [isOpen, toggleOpen] = useToggle(false);

// Counter with bounds
const MIN_COUNT = 0;
const MAX_COUNT = 100;
const { count, inc, dec, reset } = useCounter(0, {
  min: MIN_COUNT,
  max: MAX_COUNT,
});

// Cycle through options
const themes = ["light", "dark", "auto"] as const;
const {
  state: currentTheme,
  next: nextTheme,
  prev: prevTheme,
} = useCycleList([...themes]);
</script>

<template>
  <div>
    <button @click="toggleOpen()">{{ isOpen ? "Close" : "Open" }}</button>
    <div>
      <button @click="dec()">-</button>
      <span>{{ count }}</span>
      <button @click="inc()">+</button>
    </div>
    <button @click="nextTheme()">Theme: {{ currentTheme }}</button>
  </div>
</template>
```

**Why good:** eliminates boilerplate for common patterns, `useCounter` enforces min/max bounds, `useCycleList` handles wrapping automatically

---

### Pattern 6: useFetch for Reactive HTTP

Reactive data fetching with abort, refetch, and interceptors.

```vue
<script setup lang="ts">
import { useFetch } from "@vueuse/core";
import { computed } from "vue";

const userId = ref(1);
const apiUrl = computed(() => `/api/users/${userId.value}`);

// ✅ Good Example - Reactive fetch with auto-refetch
const { data, isFetching, error, abort } = useFetch(apiUrl, {
  refetch: true, // re-fetches when apiUrl changes
}).json<User>();

// Manual fetch with immediate: false
const { data: submitResult, execute } = useFetch("/api/submit", {
  immediate: false,
})
  .post(formData)
  .json();

async function handleSubmit(): Promise<void> {
  await execute(); // manually trigger the fetch
}
</script>
```

**Why good:** URL reactivity triggers automatic refetch, `.json<T>()` provides type-safe parsing, `abort` for cancellation, `immediate: false` for manual control

See [examples/network.md](examples/network.md) for `createFetch`, interceptors, and advanced patterns.

---

### Pattern 7: createGlobalState for Shared State

Lightweight global state without a state management library.

```typescript
// stores/counter.ts
import { createGlobalState } from "@vueuse/core";
import { computed, shallowRef } from "vue";

// ✅ Good Example - Global state with computed
export const useGlobalCounter = createGlobalState(() => {
  const count = shallowRef(0);
  const doubleCount = computed(() => count.value * 2);
  const isPositive = computed(() => count.value > 0);

  function increment(): void {
    count.value++;
  }

  function decrement(): void {
    count.value--;
  }

  function reset(): void {
    count.value = 0;
  }

  return { count, doubleCount, isPositive, increment, decrement, reset };
});
```

```vue
<!-- Any component can use the shared state -->
<script setup lang="ts">
import { useGlobalCounter } from "@/stores/counter";

const { count, doubleCount, increment, decrement } = useGlobalCounter();
</script>
```

**Why good:** shared state across components, no provider/inject boilerplate, composable pattern with computed derivations, `shallowRef` for performance

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Calling composables inside `async` functions, `setTimeout`, or event handlers -- composables must be called synchronously in `setup()` to bind to the component lifecycle
- Using `ref` instead of `shallowRef` for large objects in storage composables -- causes unnecessary deep reactivity tracking on every nested property
- Accessing browser APIs without SSR guards -- `useLocalStorage`, `useClipboard`, `useMouse` crash during server-side rendering

**Medium Priority:**

- Using `import * from "@vueuse/core"` -- defeats tree-shaking, imports the entire 250+ function library
- Not using `isSupported` check from composables that wrap browser APIs -- causes runtime errors in unsupported environments
- Creating custom composables for functionality VueUse already provides -- check the docs first
- Using `watch` + `ref` to track DOM state that VueUse composables handle reactively (`useMouse`, `useScroll`, etc.)

**Gotchas & Edge Cases:**

- `useLocalStorage` returns a `RemovableRef` -- setting `.value = null` removes the key from storage entirely, not storing `null`
- `useFetch` with `refetch: true` fires immediately AND on URL change -- use `immediate: false` if you only want manual control
- `createGlobalState` creates a singleton per import -- state persists until page reload, even after all components unmount
- `useIntersectionObserver` callback fires immediately with current state on creation -- don't assume first callback means element just became visible
- `useDark` modifies the `html` element's class -- ensure your CSS expects the class name it adds (default: `dark`)
- `useWebSocket` auto-reconnects by default -- pass `autoReconnect: false` if you want manual control
- `useEventListener` with a template ref waits for `onMounted` internally -- the listener is NOT active during `setup()`
- `useRefHistory` tracks every change by default -- use `{ deep: false }` for shallow tracking or `useManualRefHistory` for explicit snapshots

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST call VueUse composables synchronously inside `<script setup>` or `setup()` -- NEVER inside async callbacks, setTimeout, or conditional blocks)**

**(You MUST use `shallowRef` instead of `ref` for large objects/arrays in VueUse composables to avoid deep reactivity overhead)**

**(You MUST handle SSR by checking `typeof window !== "undefined"` or using VueUse's built-in SSR-safe composables -- browser APIs crash during server rendering)**

**(You MUST import individual composables from `@vueuse/core` -- NEVER use `import * as vueuse` which defeats tree-shaking)**

**Failure to follow these rules will cause SSR crashes, performance degradation, and lifecycle errors.**

</critical_reminders>
