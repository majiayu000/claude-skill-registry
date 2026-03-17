---
name: web-i18n-vue-i18n
description: Type-safe i18n for Vue 3 Composition API
---

# vue-i18n Internationalization Patterns

> **Quick Guide:** Use vue-i18n v11+ for type-safe internationalization in Vue 3. `useI18n` composable for translations, `d()` for dates, `n()` for numbers, `i18n-t` component for rich text. Set `legacy: false` for Composition API mode (Legacy API is deprecated in v11, removed in v12).

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST set `legacy: false` in createI18n for Composition API mode)**

**(You MUST use a SINGLE `useI18n()` call per component - destructure all needed functions from one call)**

**(You MUST wrap async state updates in `runInAction` equivalent or handle locale reactivity properly)**

**(You MUST use named constants for locale codes - NO inline locale strings)**

</critical_requirements>

---

**Auto-detection:** vue-i18n, useI18n, createI18n, i18n-t, i18n-d, i18n-n, locale detection, pluralization, Vue 3 i18n, Composition API i18n

**When to use:**

- Implementing internationalization in Vue 3 applications
- Rendering localized messages with interpolation and pluralization
- Formatting dates, numbers, and currency per locale
- Setting up locale-based routing and lazy loading
- Building type-safe translation systems with TypeScript

**Key patterns covered:**

- Project setup with createI18n and Composition API
- useI18n composable for messages, dates, numbers
- Pluralization with pipe syntax and custom rules
- Component interpolation with i18n-t, i18n-d, i18n-n
- Lazy loading translations for performance
- TypeScript integration for type-safe keys

**When NOT to use:**

- Simple single-locale applications (skip i18n complexity)
- Legacy Vue 2 applications (use vue-i18n v8)
- Non-Vue applications (use framework-specific i18n solution)

**Detailed Resources:**

- For code examples, see [examples/](examples/) (core.md, formatting.md, lazy-loading.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

---

<philosophy>

## Philosophy

vue-i18n follows the principle of **locale-aware, reactive rendering** with support for complex message formatting. Translations are organized as JSON objects, loaded globally or per-component. The Composition API mode (`legacy: false`) provides a modern, type-safe approach using the `useI18n` composable.

**Core principles:**

1. **Composition API first**: Use `useI18n()` composable with `legacy: false` for modern Vue 3 patterns
2. **Single composable call**: Destructure all functions (`t`, `d`, `n`, `locale`) from ONE `useI18n()` call
3. **Locale reactivity**: Locale changes automatically trigger re-renders via Vue's reactivity system
4. **Message format standard**: Use pipe-separated plurals and named interpolation for translator-friendly messages

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Project Setup

Set up vue-i18n with Composition API mode using the standard file structure.

#### File Structure

```
src/
  i18n/
    index.ts         # Main i18n configuration
    types.ts         # TypeScript type declarations
  locales/
    en.json          # English translations
    ja.json          # Japanese translations
    fr.json          # French translations
main.ts              # App entry with i18n plugin
```

#### Configuration

```typescript
// src/i18n/index.ts
import { createI18n } from "vue-i18n";
import en from "../locales/en.json";

export const SUPPORTED_LOCALES = ["en", "ja", "fr"] as const;
export const DEFAULT_LOCALE = "en";

export type SupportedLocale = (typeof SUPPORTED_LOCALES)[number];

export const i18n = createI18n({
  legacy: false, // REQUIRED for Composition API
  locale: DEFAULT_LOCALE,
  fallbackLocale: DEFAULT_LOCALE,
  globalInjection: true, // Default since v9.2, injects $t, $d, $n into templates
  messages: {
    en,
  },
});

export { i18n };
```

**Why good:** `legacy: false` enables Composition API mode, named constants for locales enable type-safe usage, fallbackLocale prevents missing translation errors, globalInjection enables template shorthand (default true since v9.2)

```typescript
// main.ts
import { createApp } from "vue";
import { i18n } from "./i18n";
import App from "./App.vue";

const app = createApp(App);
app.use(i18n);
app.mount("#app");
```

**Why good:** i18n plugin registered once at app root, all components inherit translation capability

---

### Pattern 2: useI18n Composable

Use the useI18n composable in components for translations, formatting, and locale management.

#### Basic Usage

```vue
<script setup lang="ts">
import { useI18n } from "vue-i18n";

// CRITICAL: Single call, destructure all needed functions
const { t, d, n, locale, availableLocales } = useI18n();

const switchLocale = (newLocale: string) => {
  locale.value = newLocale;
};
</script>

<template>
  <h1>{{ t("greeting") }}</h1>
  <p>{{ t("messages.welcome", { name: "Vue" }) }}</p>
  <p>{{ d(new Date(), "long") }}</p>
  <p>{{ n(1000, "currency") }}</p>

  <select :value="locale" @change="switchLocale($event.target.value)">
    <option v-for="loc in availableLocales" :key="loc" :value="loc">
      {{ loc }}
    </option>
  </select>
</template>
```

**Why good:** single useI18n call prevents sync issues, locale.value is reactive and triggers re-renders, destructuring provides all needed functions

```vue
<!-- BAD - Multiple useI18n calls cause sync issues -->
<script setup lang="ts">
const { t } = useI18n();
const { locale } = useI18n(); // WRONG: Second call!
const { d } = useI18n(); // WRONG: Third call!
</script>
```

**Why bad:** multiple useI18n calls create separate instances that may not stay synchronized, leads to subtle bugs

---

### Pattern 3: Message Interpolation

Use named placeholders and linked messages for flexible translations.

#### Named Interpolation

```json
// locales/en.json
{
  "greeting": "Hello, {name}!",
  "items": "You have {count} items in your cart.",
  "email": "{account}{'@'}{domain}"
}
```

```typescript
const { t } = useI18n();

t("greeting", { name: "John" }); // "Hello, John!"
t("items", { count: 5 }); // "You have 5 items in your cart."
t("email", { account: "user", domain: "example.com" }); // "user@example.com"
```

**Why good:** named placeholders are explicit and refactorable, literal interpolation (`{'@'}`) escapes special characters

#### Linked Messages

```json
{
  "app": {
    "name": "My App"
  },
  "welcome": "Welcome to @:app.name!",
  "brand": "vue i18n",
  "message": {
    "upper": "@.upper:brand",
    "lower": "@.lower:brand",
    "capitalize": "@.capitalize:brand"
  }
}
```

```typescript
t("welcome"); // "Welcome to My App!"
t("message.upper"); // "VUE I18N"
t("message.capitalize"); // "Vue i18n"
```

**Why good:** linked messages (`@:key`) avoid duplication, built-in modifiers (upper, lower, capitalize) transform referenced values

---

### Pattern 4: Pluralization

Use pipe-separated syntax for plural forms with automatic `{n}` and `{count}` injection.

#### Basic Plural Syntax

```json
{
  "car": "car | cars",
  "apple": "no apples | one apple | {count} apples",
  "items": "no items | {n} item | {n} items"
}
```

```typescript
const { t } = useI18n();

t("car", 1); // "car"
t("car", 2); // "cars"

t("apple", 0); // "no apples"
t("apple", 1); // "one apple"
t("apple", 10); // "10 apples"

t("items", 5); // "5 items"
```

**Why good:** pipe syntax is translator-friendly, `{n}` and `{count}` are auto-injected with the plural value, three forms handle zero/one/many

#### Custom Plural Rules

```typescript
// For languages with complex rules (Russian, Arabic, Polish)
const i18n = createI18n({
  legacy: false,
  locale: "ru",
  pluralRules: {
    ru: (choice: number, choicesLength: number) => {
      if (choice === 0) return 0;

      const teen = choice > 10 && choice < 20;
      const endsWithOne = choice % 10 === 1;

      if (!teen && endsWithOne) return 1;
      if (!teen && choice % 10 >= 2 && choice % 10 <= 4) return 2;
      return choicesLength < 4 ? 2 : 3;
    },
  },
  messages: {
    ru: {
      apple: "нет яблок | {n} яблоко | {n} яблока | {n} яблок",
    },
  },
});
```

**Why good:** custom pluralRules handle languages with more than two forms, function receives choice count and returns index into plural array

---

### Pattern 5: Component Interpolation

Use `i18n-t`, `i18n-d`, and `i18n-n` components for rich text with Vue components inside translations.

#### i18n-t for Rich Text

```json
{
  "tos": "I agree to the {terms}.",
  "termsLink": "Terms of Service"
}
```

```vue
<template>
  <i18n-t keypath="tos" tag="p">
    <template #terms>
      <a href="/terms">{{ t("termsLink") }}</a>
    </template>
  </i18n-t>
</template>
```

**Why good:** translation string stays translatable, Vue components can be inserted via named slots, `tag` prop controls wrapper element

#### i18n-t with Pluralization

```json
{
  "items": "no items | {n} item | {n} items"
}
```

```vue
<template>
  <i18n-t keypath="items" :plural="count" tag="p">
    <template #n>
      <strong>{{ count }}</strong>
    </template>
  </i18n-t>
</template>

<script setup lang="ts">
import { ref } from "vue";
const count = ref(5);
</script>
```

**Why good:** plural value passed via `:plural` prop, `#n` slot allows styling the number, result: "**5** items"

#### i18n-d and i18n-n for Styled Parts

```vue
<template>
  <!-- DateTime with styled parts -->
  <i18n-d :value="date" format="long" tag="time">
    <template #month="{ month }">
      <span class="month">{{ month }}</span>
    </template>
    <template #day="{ day }">
      <span class="day">{{ day }}</span>
    </template>
  </i18n-d>

  <!-- Number with styled parts -->
  <i18n-n :value="price" format="currency" tag="span">
    <template #currency="{ currency }">
      <span class="currency-symbol">{{ currency }}</span>
    </template>
    <template #integer="{ integer }">
      <span class="integer">{{ integer }}</span>
    </template>
  </i18n-n>
</template>
```

**Why good:** scoped slots expose formatted parts (month, day, currency, integer), enables fine-grained styling of formatted values

---

### Pattern 6: DateTime and Number Formatting

Configure and use locale-aware formatting for dates, times, and numbers.

#### DateTime Format Configuration

```typescript
const datetimeFormats = {
  "en-US": {
    short: {
      year: "numeric",
      month: "short",
      day: "numeric",
    },
    long: {
      year: "numeric",
      month: "long",
      day: "numeric",
      weekday: "long",
      hour: "numeric",
      minute: "numeric",
    },
  },
  "ja-JP": {
    short: {
      year: "numeric",
      month: "short",
      day: "numeric",
    },
    long: {
      year: "numeric",
      month: "long",
      day: "numeric",
      weekday: "long",
      hour: "numeric",
      minute: "numeric",
      hour12: false,
    },
  },
};

const i18n = createI18n({
  legacy: false,
  locale: "en-US",
  datetimeFormats, // Note: camelCase, not dateTimeFormats
});
```

```typescript
const { d } = useI18n();

d(new Date(), "short"); // "Apr 19, 2024"
d(new Date(), "long"); // "Friday, April 19, 2024 at 2:30 PM"
```

**Why good:** named formats ensure consistency across app, locale-specific formats handle cultural differences (12h vs 24h time)

#### Number Format Configuration

```typescript
const numberFormats = {
  "en-US": {
    currency: {
      style: "currency",
      currency: "USD",
      notation: "standard",
    },
    decimal: {
      style: "decimal",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    },
    percent: {
      style: "percent",
      useGrouping: false,
    },
  },
  "ja-JP": {
    currency: {
      style: "currency",
      currency: "JPY",
      useGrouping: true,
      currencyDisplay: "symbol",
    },
  },
};

const i18n = createI18n({
  legacy: false,
  locale: "en-US",
  numberFormats,
});
```

```typescript
const { n } = useI18n();

n(10000, "currency"); // "$10,000.00"
n(0.15, "percent"); // "15%"
```

**Why good:** Intl.NumberFormat under the hood, handles locale-specific separators and symbols automatically

</patterns>

---

<integration>

## Integration Guide

**vue-i18n is Vue 3's standard i18n solution.** It integrates with Vue's reactivity system for automatic re-renders on locale change.

**Works with:**

- **Vue 3 Composition API**: Designed for `<script setup>` with useI18n composable
- **Vue Router**: Locale-based routing with navigation guards
- **SSR Frameworks**: Compatible with Nuxt 3 via @nuxtjs/i18n module

**Component State Guidance:**

- Locale state is managed by vue-i18n - use `locale.value` from useI18n to read/write
- Locale changes are reactive - all components using `t()`, `d()`, `n()` update automatically
- Use `globalInjection: true` for template shorthand (`$t`, `$d`, `$n`)

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST set `legacy: false` in createI18n for Composition API mode)**

**(You MUST use a SINGLE `useI18n()` call per component - destructure all needed functions from one call)**

**(You MUST wrap async state updates in `runInAction` equivalent or handle locale reactivity properly)**

**(You MUST use named constants for locale codes - NO inline locale strings)**

**Failure to follow these rules will break i18n reactivity and cause translation inconsistencies.**

</critical_reminders>
