---
name: i18n-and-localization
description: "Use when implementing internationalization and localization. Covers i18n library selection, message extraction workflows, pluralization, RTL support, locale-aware formatting, and translation management."
---

# Internationalization & Localization

## The Principle

```
EXTERNALIZE ALL USER-FACING STRINGS FROM DAY ONE.
Retrofitting i18n is 10x harder than building it in.
```

i18n = making code locale-ready. l10n = adapting for a specific locale.

## Library Selection

| Framework | Library | Notes |
|-----------|---------|-------|
| React | `react-intl` (FormatJS) | ICU MessageFormat, mature, large community |
| React | `i18next` + `react-i18next` | Framework-agnostic core, rich plugin ecosystem |
| Next.js | `next-intl` | App Router native, RSC support, built-in routing |
| Next.js | `next-i18next` | Pages Router; for App Router prefer `next-intl` |
| Vue | `vue-i18n` | Official Vue integration, composition API support |
| Svelte | `svelte-i18n` | Reactive stores, SSR support |
| Angular | `@angular/localize` | Built-in, compile-time translation |
| Vanilla JS | `i18next` | No framework dependency, works everywhere |

### Decision Criteria

| Factor | react-intl | i18next | next-intl |
|--------|:---:|:---:|:---:|
| ICU MessageFormat | Native | Plugin | Native |
| SSR/RSC support | Manual | Plugin | Built-in |
| Namespace splitting | No | Yes | Yes |
| Backend loading | No | Yes (plugins) | Built-in |
| Non-React usage | No | Yes | No |
| Bundle size (core) | ~25KB | ~15KB + plugins | ~20KB |

**Default recommendation**: `next-intl` for Next.js App Router, `react-intl` for other React, `i18next` for multi-framework or vanilla.

## ICU Message Format

The standard for translatable messages. Learn it once, use everywhere.

### Basic

```
Hello, {name}!
You have {count} items in your cart.
```

### Pluralization

```icu
{count, plural,
    =0 {No messages}
    one {1 message}
    other {{count} messages}
}
```

Plural categories by language: `zero`, `one`, `two`, `few`, `many`, `other`. English uses `one` + `other`. Arabic uses all six. Always include `other` as fallback.

### Select (Gender / Enum)

```icu
{gender, select,
    female {{name} updated her profile}
    male {{name} updated his profile}
    other {{name} updated their profile}
}
```

### Nested (Plural + Select)

```icu
{gender, select,
    female {{count, plural,
        one {{name} added 1 photo to her album}
        other {{name} added {count} photos to her album}
    }}
    other {{count, plural,
        one {{name} added 1 photo to their album}
        other {{name} added {count} photos to their album}
    }}
}
```

### Number and Date in Messages

```icu
Price: {price, number, ::currency/USD}
Sale ends: {date, date, medium}
```

## Message Extraction Workflow

### Structure

```
src/
  components/
    Header.tsx
locales/
  en.json          # Source language (developer writes)
  fr.json          # Translated (translator writes)
  ja.json          # Translated
```

### Key Naming Conventions

| Convention | Example | Pros | Cons |
|------------|---------|------|------|
| Nested by feature | `cart.checkout.button` | Organized, namespace isolation | Verbose |
| Flat with prefix | `cart_checkout_button` | Simple, easy grep | No hierarchy |
| Content-based | `Add to Cart` | Readable as key | Breaks on text change |

**Recommended**: Nested by feature. Use the component/page path as namespace.

```json
{
  "cart": {
    "title": "Shopping Cart",
    "checkout": {
      "button": "Proceed to Checkout",
      "empty": "Your cart is empty"
    },
    "items": "{count, plural, one {1 item} other {{count} items}}"
  }
}
```

### Extraction Tools

```bash
# FormatJS: extract from source, compile for runtime
formatjs extract 'src/**/*.tsx' --out-file locales/en.json --id-interpolation-pattern '[sha512:contenthash:base64:6]'
formatjs compile locales/en.json --out-file compiled/en.json

# i18next-parser
i18next 'src/**/*.{ts,tsx}' --output 'locales/$LOCALE/$NAMESPACE.json'
```

## Locale-Aware Formatting with Intl API

The `Intl` API is built into all modern browsers and Node.js. Use it instead of libraries like `moment` or `date-fns` for formatting.

### Numbers

```typescript
// Currency
new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' })
  .format(1234.56);  // "1.234,56 €"

// Percentage
new Intl.NumberFormat('en-US', { style: 'percent', maximumFractionDigits: 1 })
  .format(0.856);  // "85.6%"

// Compact notation
new Intl.NumberFormat('en-US', { notation: 'compact' })
  .format(1500000);  // "1.5M"
```

### Dates

```typescript
// Medium date
new Intl.DateTimeFormat('ja-JP', { dateStyle: 'medium' })
  .format(new Date());  // "2025/01/15"

// Relative time
new Intl.RelativeTimeFormat('en', { numeric: 'auto' })
  .format(-1, 'day');  // "yesterday"

// Time zones
new Intl.DateTimeFormat('en-US', {
  timeZone: 'Asia/Tokyo',
  dateStyle: 'full',
  timeStyle: 'short'
}).format(new Date());  // "Wednesday, January 15, 2025 at 2:30 AM"
```

### Lists

```typescript
new Intl.ListFormat('en', { style: 'long', type: 'conjunction' })
  .format(['Alice', 'Bob', 'Charlie']);  // "Alice, Bob, and Charlie"

new Intl.ListFormat('en', { style: 'long', type: 'disjunction' })
  .format(['red', 'blue', 'green']);  // "red, blue, or green"
```

### Collation (Sorting)

```typescript
const collator = new Intl.Collator('de-DE');
['ä', 'a', 'z'].sort(collator.compare);  // ['a', 'ä', 'z']
```

## RTL Support

### CSS Logical Properties

Replace physical properties with logical ones for automatic RTL support.

| Physical (don't use) | Logical (use this) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `margin-right` | `margin-inline-end` |
| `padding-left` | `padding-inline-start` |
| `text-align: left` | `text-align: start` |
| `float: left` | `float: inline-start` |
| `left: 10px` | `inset-inline-start: 10px` |
| `border-left` | `border-inline-start` |
| `width` | `inline-size` (when direction-dependent) |

### HTML Setup

```html
<html lang="ar" dir="rtl">
```

```typescript
// Dynamic direction
const direction = ['ar', 'he', 'fa', 'ur'].includes(locale) ? 'rtl' : 'ltr';
document.documentElement.setAttribute('dir', direction);
document.documentElement.setAttribute('lang', locale);
```

### Bidirectional Text

```html
<!-- Isolate embedded LTR text in RTL context -->
<p>الاسم: <bdi>John Smith</bdi></p>

<!-- Or use Unicode marks -->
<p>الاسم: &#x200F;John Smith&#x200F;</p>
```

### RTL Checklist

- [ ] All layout uses CSS logical properties (no `left`/`right`)
- [ ] Icons that imply direction (arrows, back) are mirrored
- [ ] Icons that don't imply direction (search, close) are NOT mirrored
- [ ] Form fields align correctly
- [ ] Scrollbars appear on correct side
- [ ] No hardcoded `text-align: left` in component styles

## Lazy Loading Locale Bundles

Don't ship all translations to every user.

```typescript
// next-intl: automatic per-route loading
// app/[locale]/layout.tsx
import { getMessages } from 'next-intl/server';

export default async function Layout({ children, params: { locale } }) {
  const messages = await getMessages();
  return <NextIntlClientProvider messages={messages}>{children}</NextIntlClientProvider>;
}

// i18next: dynamic import
i18next.init({
  partialBundledLanguages: true,
  backend: {
    loadPath: '/locales/{{lng}}/{{ns}}.json',
  },
});

// Manual dynamic import
const messages = await import(`../locales/${locale}.json`);
```

**Bundle size impact**: A typical app with 500 translation keys = ~15-30KB per locale. Lazy loading saves (N-1) * 15-30KB from initial bundle.

## Testing i18n

### Pseudo-Localization

Replaces characters with accented variants to catch hardcoded strings and layout issues without actual translations.

```
"Submit" → "[Šüƀɱîţ]"
"Hello, {name}!" → "[Ĥëļļö, {name}!]"
```

Tools: `pseudo-localization` npm package, FormatJS `--pseudo-locale` flag.

### String Expansion Testing

Translated text is often 30-50% longer than English. Test with expanded strings.

| Source Language | Target | Typical Expansion |
|----------------|--------|-------------------|
| English | German | +30% |
| English | French | +20% |
| English | Finnish | +30-40% |
| English | Japanese | -30% (fewer chars, but may need wider layout for CJK) |
| English | Arabic | +25% |

### What to Test

```typescript
// Test that all keys exist in all locale files
const en = require('./locales/en.json');
const fr = require('./locales/fr.json');
const missingKeys = Object.keys(flatten(en)).filter(k => !flatten(fr)[k]);
expect(missingKeys).toEqual([]);

// Test ICU syntax validity
import { parse } from '@formatjs/icu-messageformat-parser';
Object.entries(messages).forEach(([key, msg]) => {
  expect(() => parse(msg)).not.toThrow();
});
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| String concatenation | `"Hello, " + name` -- can't reorder for other languages | Use ICU: `"Hello, {name}"` |
| Hardcoded date format | `MM/DD/YYYY` is US-only | Use `Intl.DateTimeFormat` |
| Splitting sentences | `"Click " + <a>here</a> + " to continue"` | Use rich text: `"Click <link>here</link> to continue"` |
| Assuming text direction | CSS `margin-left` | Use `margin-inline-start` |
| Plural with ternary | `count === 1 ? "item" : "items"` | Use ICU plural rules (languages have 2-6 plural forms) |
| Numbers without formatting | `"$" + price` | Use `Intl.NumberFormat` with currency |
| Hardcoded currency symbol | `"$" + amount` | Currency symbol position varies by locale (€10 vs 10€) |
| Missing context for translators | Key: `"save"` (verb or noun?) | Add description: `"save_button": "Save"` with context comment |

## Gotchas

- English has 2 plural forms; Arabic has 6, Polish has 4. Never hardcode plural logic -- use ICU plural rules
- `Intl.DateTimeFormat` output varies by browser/OS version; snapshot tests on dates will be brittle
- RTL languages aren't just mirrored; phone numbers, URLs, and code remain LTR even in RTL context
- ICU MessageFormat `#` in plural rules refers to the plural value, not a literal `#` -- escape with `'#'`
- Some languages (Chinese, Japanese) don't use spaces between words; CSS `word-break: break-all` may be needed
- Translation memory tools (Crowdin, Lokalise) require stable keys; changing keys invalidates existing translations
- Next.js App Router and `next-intl` require server components for async message loading; client components need the provider wrapper
- Currency formatting must use the user's locale for number format but the transaction's currency code -- these are independent

## Cross-References

- **frontend:nextjs-app-router-patterns** -- routing patterns for locale-based paths, middleware setup
- **frontend:react-state-management** -- managing locale state, context providers for i18n
