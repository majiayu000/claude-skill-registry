---
name: web-i18n-react-intl
description: ICU message format internationalization
---

# React-Intl (FormatJS) Internationalization Patterns

> **Quick Guide:** Use react-intl for internationalization with ICU Message Format. `FormattedMessage` for JSX content, `useIntl` for string attributes and programmatic use, `defineMessages` for extractable message descriptors. Wrap app with `IntlProvider` and configure `onError` for missing translations. Always include the `other` category in plurals and selects.
>
> **Version Note:** react-intl v7.x supports React 16.6+/17/18/19. v8+ requires React 19 only (React 18 support dropped). Current latest: v10.x.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap the application root with `IntlProvider` and configure locale, messages, and defaultLocale)**

**(You MUST include the `other` category in ALL plural and select ICU messages - omission causes runtime errors)**

**(You MUST use named constants for locale codes - NO inline locale strings)**

**(You MUST verify React version compatibility: v7.x supports React 16.6-19, v8+ requires React 19 only)**

</critical_requirements>

---

**Auto-detection:** react-intl, FormatJS, FormattedMessage, useIntl, IntlProvider, defineMessages, ICU message format, formatMessage, FormattedDate, FormattedNumber, FormattedRelativeTime

**When to use:**

- Implementing internationalization in React applications
- Rendering localized messages with ICU syntax (interpolation, pluralization, select)
- Formatting dates, numbers, currency, and relative time per locale
- Extracting and compiling translation messages for TMS workflows
- Building type-safe i18n with TypeScript augmentation

**Key patterns covered:**

- IntlProvider setup with error handling and default rich text elements
- FormattedMessage vs useIntl: declarative JSX vs imperative strings
- defineMessages for static message extraction
- ICU Message Format syntax (plurals, select, ordinals, rich text)
- Date, time, number, currency, relative time, and list formatting
- TypeScript integration for type-safe message IDs
- Lazy loading locale data with dynamic imports

**When NOT to use:**

- SSR frameworks with built-in i18n (use the framework's i18n solution for better SSR integration)
- Simple single-locale applications (skip i18n complexity)
- Server-side rendering without React context (use `createIntl` from `@formatjs/intl`)

**Detailed Resources:**

- [examples/core.md](examples/core.md) - IntlProvider setup, FormattedMessage, useIntl, defineMessages, TypeScript integration, lazy loading
- [examples/formatting.md](examples/formatting.md) - Date, time, number, currency, relative time, and list formatting
- [examples/pluralization.md](examples/pluralization.md) - Plural, ordinal, select, nested ICU patterns
- [reference.md](reference.md) - Decision frameworks, ICU syntax quick reference, API tables, anti-patterns

---

<philosophy>

## Philosophy

React-intl follows the principle of **ICU Message Format standardization** with both declarative and imperative APIs. Translations use industry-standard ICU syntax enabling compatibility with professional translation management systems. The library is built on browser-native `Intl` APIs for optimal performance and accurate locale-aware formatting.

**Core principles:**

1. **ICU Standard**: Use industry-standard ICU Message Format for professional translation workflows
2. **Dual API**: FormattedMessage for JSX content, useIntl for string contexts (attributes, programmatic use)
3. **Native Intl**: Built on browser Intl APIs for accurate locale-specific formatting
4. **Extractable**: defineMessages enables CLI extraction for translation management

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: IntlProvider Setup

Wrap your application root with `IntlProvider`. Configure `onError` to distinguish missing translations from actual errors, set `defaultLocale` for fallback, and define `defaultRichTextElements` for consistent markup.

```typescript
export function AppIntlProvider({ children, locale, messages }: Props) {
  return (
    <IntlProvider
      locale={locale}
      defaultLocale={DEFAULT_LOCALE}
      messages={messages}
      defaultRichTextElements={DEFAULT_RICH_TEXT_ELEMENTS}
      onError={(err) => {
        if (err.code === "MISSING_TRANSLATION") {
          console.warn(`Missing translation: ${err.message}`);
          return;
        }
        throw err;
      }}
    >
      {children}
    </IntlProvider>
  );
}
```

**Why good:** custom onError distinguishes missing translations from actual errors, defaultLocale provides fallback, defaultRichTextElements ensure consistent markup

See [examples/core.md](examples/core.md) for full setup with locale config, lazy loading, and app integration.

---

### Pattern 2: FormattedMessage (Declarative JSX)

Use `FormattedMessage` for rendering translated text directly in JSX elements. Supports ICU syntax for interpolation, pluralization, and rich text.

```typescript
<FormattedMessage
  id="greeting.unread"
  defaultMessage="{count, plural, =0 {No messages} one {# message} other {# messages}}"
  values={{ count: unreadCount }}
/>
```

**When to use:** Text content rendered directly in JSX, rich text with embedded formatting.

**When not to use:** String attributes like placeholder, aria-label, title (use useIntl instead).

---

### Pattern 3: useIntl Hook (Imperative Strings)

Use `useIntl` when you need formatted strings for attributes, props, or programmatic use.

```typescript
const intl = useIntl();
const placeholder = intl.formatMessage({
  id: "search.placeholder",
  defaultMessage: "Search products...",
});

<input placeholder={placeholder} aria-label={ariaLabel} />
```

**When to use:** Input placeholders, ARIA labels, document titles, third-party component props, conditional logic based on formatted values.

---

### Pattern 4: defineMessages for Static Extraction

Group related messages with `defineMessages` for CLI extraction and IDE autocomplete.

```typescript
export const productMessages = defineMessages({
  title: {
    id: "product.title",
    defaultMessage: "Product Details",
    description: "Page title for product detail page",
  },
  reviewCount: {
    id: "product.reviewCount",
    defaultMessage:
      "{count, plural, =0 {No reviews} one {# review} other {# reviews}}",
    description: "Number of product reviews with pluralization",
  },
});
```

**Why good:** centralizes related messages, descriptions provide translator context, CLI extracts these automatically, IDE autocomplete for references

See [examples/core.md](examples/core.md) for usage patterns with FormattedMessage and useIntl.

---

### Pattern 5: Rich Text Formatting

Use XML-like tags in messages for embedded markup. Translators can reorder tags per language grammar while the complete sentence stays in one translation unit.

```typescript
<FormattedMessage
  id="terms.notice"
  defaultMessage="By signing up, you agree to our <terms>Terms</terms> and <privacy>Privacy Policy</privacy>."
  values={{
    terms: (chunks) => <a href="/terms">{chunks}</a>,
    privacy: (chunks) => <a href="/privacy">{chunks}</a>,
  }}
/>
```

Configure global tag handlers via `defaultRichTextElements` on `IntlProvider` for `<b>`, `<i>`, `<br>` tags.

---

### Pattern 6: Formatting Components

Locale-aware formatting for dates, numbers, currency, relative time, and lists.

```typescript
<FormattedDate value={date} year="numeric" month="long" day="numeric" />
// en-US: "January 15, 2024" | de-DE: "15. Januar 2024"

<FormattedNumber value={amount} style="currency" currency={currency} />
// en-US: "$1,234.56" | de-DE: "1.234,56 EUR"

<FormattedList type="conjunction" value={names} />
// en: "Alice, Bob, and Charlie" | es: "Alice, Bob y Charlie"
```

Use imperative equivalents (`intl.formatDate()`, `intl.formatNumber()`) when you need strings for attributes or programmatic use.

See [examples/formatting.md](examples/formatting.md) for comprehensive date/time, number, currency, relative time, and list examples.

---

### Pattern 7: TypeScript Integration

Enable type-safe message IDs with TypeScript module augmentation.

```typescript
// src/types/intl.d.ts
import type messages from "../lang/en.json";

type MessageIds = keyof typeof messages;

declare global {
  namespace FormatjsIntl {
    interface Message {
      ids: MessageIds;
    }
  }
}
```

Typos in message IDs become compile-time errors. Add `"esnext.intl"` to `compilerOptions.lib` in tsconfig.json.

---

### Pattern 8: Message Extraction Workflow

Use FormatJS CLI for extracting and compiling messages.

1. **Extract** messages from source code: `formatjs extract 'src/**/*.{ts,tsx}' --out-file lang/en.json`
2. **Send** to translation management system (TMS)
3. **Compile** translations to AST format: `formatjs compile lang/en.json --out-file compiled/en.json --ast`

**Why compile to AST:** 30-50% faster initial render for large message catalogs - skips runtime parsing.

---

### Pattern 9: ICU Pluralization

ICU plural syntax handles language-specific rules. Always include `other` as fallback.

```
{count, plural, =0 {No items} one {# item} other {# items}}
{position, selectordinal, one {#st} two {#nd} few {#rd} other {#th}}
{gender, select, male {He} female {She} other {They}} liked your post.
```

Different languages have different plural categories (English: one/other, Russian: one/few/many/other, Arabic: zero/one/two/few/many/other).

See [examples/pluralization.md](examples/pluralization.md) for nested patterns, ordinals, select, and language-specific examples.

</patterns>

---

<performance>

## Performance

### Message Compilation (AST Pre-parsing)

Compile messages to AST at build time to skip runtime parsing. Impact: 30-50% faster initial render for large catalogs.

### Lazy Loading Locale Data

Use dynamic imports to load only the current locale's messages. Cache loaded messages to prevent duplicate fetches. See [examples/core.md](examples/core.md) for implementation.

### RawIntlProvider with createIntl

Use `createIntl` + `createIntlCache` + `RawIntlProvider` for manual control over intl object creation. Useful when you want to memoize the intl instance explicitly.

### Avoid Inline Message Objects

Define messages outside components with `defineMessages` rather than passing inline objects to `FormattedMessage`. Inline objects create new references each render, preventing memoization optimizations.

</performance>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- **Missing `IntlProvider` wrapper** - All useIntl and FormattedMessage calls fail without context
- **Missing `other` category in plural/select** - Runtime error: "other" is REQUIRED in ICU syntax
- **Hardcoded locale strings** - Use named constants from config for type safety
- **Using FormattedMessage for attributes** - Returns ReactNode, not string; breaks placeholder, aria-label, title

**Medium Priority Issues:**

- **Missing `defaultLocale` on IntlProvider** - No fallback for missing translations
- **No `onError` handler** - Console noise for every missing translation
- **Missing description in defineMessages** - Translators lack context for accurate translation

**Common Mistakes:**

- Concatenating translated strings instead of single message with placeholders (word order varies by language)
- Applying English grammar rules programmatically (possessives, plurals) instead of using ICU syntax
- Using `{count}` instead of `{count, plural, ...}` for countable items
- Missing `#` in plural branches (shows nothing instead of the count value)

**Gotchas & Edge Cases:**

- `FormattedMessage` returns `ReactNode`, not `string` - cannot use for HTML attributes
- `formatMessage` returns `string` for plain values, but `string | ReactNode[]` when rich text tag functions are in values
- Rich text tag functions receive `chunks` array, not single element
- `formatNumber` with `style: "percent"` expects decimal (0.25 for 25%), not percentage
- `formatRelativeTime` value is relative to NOW - negative for past, positive for future
- ICU escaping: single quote `'` escapes special characters, double single quote `''` produces literal apostrophe
- Browser Intl support varies - consider polyfills for older browsers
- `injectIntl` HOC was removed in v10 - use `useIntl` hook instead
- Use `onWarn` prop on IntlProvider to suppress or handle `defaultRichTextElements` warnings when messages are not pre-compiled

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap the application root with `IntlProvider` and configure locale, messages, and defaultLocale)**

**(You MUST include the `other` category in ALL plural and select ICU messages - omission causes runtime errors)**

**(You MUST use named constants for locale codes - NO inline locale strings)**

**(You MUST verify React version compatibility: v7.x supports React 16.6-19, v8+ requires React 19 only)**

**Failure to follow these rules will cause runtime errors and broken internationalization.**

</critical_reminders>
