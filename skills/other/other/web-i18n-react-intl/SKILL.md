---
name: web-i18n-react-intl
description: ICU message format internationalization
---

# React-Intl (FormatJS) Internationalization Patterns

> **Quick Guide:** Use react-intl for internationalization with ICU Message Format. `FormattedMessage` for JSX content, `useIntl` for string attributes and programmatic use, `defineMessages` for extractable message descriptors. Wrap app with `IntlProvider` and configure `onError` for missing translations.
>
> **Version Note:** react-intl v8+ requires React 19+. For React 18 projects, use react-intl v6.x.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST wrap the application root with `IntlProvider` and configure locale, messages, and defaultLocale)**

**(You MUST include the `other` category in ALL plural and select ICU messages - omission causes runtime errors)**

**(You MUST use named constants for locale codes - NO inline locale strings)**

**(You MUST verify React version compatibility: v8+ requires React 19+, use v6.x for React 18)**

</critical_requirements>

---

**Auto-detection:** react-intl, FormatJS, FormattedMessage, useIntl, IntlProvider, defineMessages, ICU message format, formatMessage, FormattedDate, FormattedNumber

**When to use:**

- Implementing internationalization in React applications (non-Next.js)
- Rendering localized messages with ICU syntax (interpolation, pluralization, select)
- Formatting dates, numbers, currency, and relative time per locale
- Extracting and compiling translation messages for TMS workflows
- Building type-safe i18n with TypeScript augmentation

**Key patterns covered:**

- IntlProvider setup with error handling and default rich text elements
- FormattedMessage component for declarative JSX translations
- useIntl hook for imperative string formatting (attributes, props)
- defineMessages for static message extraction
- ICU Message Format syntax (plurals, select, ordinals, rich text)
- Date, time, number, and relative time formatting components
- TypeScript integration for type-safe message IDs
- Testing patterns with custom render wrapper

**When NOT to use:**

- Next.js App Router applications (use next-intl instead - better SSR integration)
- Simple single-locale applications (skip i18n complexity)
- Server Components without React context (use createIntl from @formatjs/intl)

**Detailed Resources:**

- For code examples, see [examples/](examples/) (core.md, formatting.md, pluralization.md)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

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

Wrap your application root with `IntlProvider` to establish i18n context.

#### Constants

```typescript
// src/i18n/config.ts
export const SUPPORTED_LOCALES = ["en", "de", "fr", "es"] as const;
export const DEFAULT_LOCALE = "en";

export type Locale = (typeof SUPPORTED_LOCALES)[number];

export function isValidLocale(locale: string): locale is Locale {
  return SUPPORTED_LOCALES.includes(locale as Locale);
}
```

#### Implementation

```typescript
// src/providers/intl-provider.tsx
import { IntlProvider } from "react-intl";
import type { ReactNode } from "react";
import { DEFAULT_LOCALE, type Locale } from "../i18n/config";

type Props = {
  children: ReactNode;
  locale: Locale;
  messages: Record<string, string>;
};

export function AppIntlProvider({ children, locale, messages }: Props) {
  return (
    <IntlProvider
      locale={locale}
      defaultLocale={DEFAULT_LOCALE}
      messages={messages}
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

export { AppIntlProvider };
```

**Why good:** named constants for locales enable type-safe usage throughout app, custom onError distinguishes missing translations from actual errors, defaultLocale provides fallback for missing messages

```typescript
// WRONG - No error handling, hardcoded locale
import { IntlProvider } from "react-intl";

function App({ children }) {
  return (
    <IntlProvider locale="en" messages={messages}>
      {children}
    </IntlProvider>
  );
}
```

**Why bad:** hardcoded locale string prevents type safety, missing onError causes console noise for missing translations, no defaultLocale means no fallback behavior

---

### Pattern 2: FormattedMessage Component (Declarative)

Use `FormattedMessage` for rendering translated text directly in JSX.

```typescript
// src/components/greeting.tsx
import { FormattedMessage } from "react-intl";

type Props = {
  userName: string;
  unreadCount: number;
};

export function Greeting({ userName, unreadCount }: Props) {
  return (
    <div>
      <h1>
        <FormattedMessage
          id="greeting.welcome"
          defaultMessage="Welcome back, {name}!"
          values={{ name: userName }}
        />
      </h1>
      <p>
        <FormattedMessage
          id="greeting.unread"
          defaultMessage="{count, plural, =0 {No unread messages} one {# unread message} other {# unread messages}}"
          values={{ count: unreadCount }}
        />
      </p>
    </div>
  );
}

export { Greeting };
```

**Why good:** FormattedMessage renders directly in JSX, ICU plural syntax handles all count cases including zero, values are explicitly named for refactoring safety

**When to use:** Text content rendered directly in JSX, rich text with embedded formatting, when translation is the primary content of an element.

**When not to use:** String attributes like placeholder, aria-label, title (use useIntl instead).

---

### Pattern 3: useIntl Hook (Imperative)

Use `useIntl` when you need formatted strings for attributes, props, or programmatic use.

```typescript
// src/components/search-input.tsx
import { useIntl } from "react-intl";

export function SearchInput() {
  const intl = useIntl();

  const placeholder = intl.formatMessage({
    id: "search.placeholder",
    defaultMessage: "Search products...",
  });

  const ariaLabel = intl.formatMessage({
    id: "search.ariaLabel",
    defaultMessage: "Search for products in the catalog",
  });

  return (
    <input
      type="search"
      placeholder={placeholder}
      aria-label={ariaLabel}
    />
  );
}

export { SearchInput };
```

**Why good:** useIntl returns strings suitable for HTML attributes, placeholder and aria-label require string values not ReactNode, message descriptors are type-safe

**When to use:** Input placeholders and ARIA labels, passing translated strings to third-party components, conditional rendering based on formatted values, programmatic string manipulation.

---

### Pattern 4: defineMessages for Static Extraction

Use `defineMessages` to declare messages that the CLI can extract.

```typescript
// src/messages/product.messages.ts
import { defineMessages } from "react-intl";

export const productMessages = defineMessages({
  title: {
    id: "product.title",
    defaultMessage: "Product Details",
    description: "Page title for product detail page",
  },
  addToCart: {
    id: "product.addToCart",
    defaultMessage: "Add to Cart",
    description: "Button text for adding product to shopping cart",
  },
  outOfStock: {
    id: "product.outOfStock",
    defaultMessage: "Out of Stock",
    description: "Badge text when product is unavailable",
  },
  priceLabel: {
    id: "product.priceLabel",
    defaultMessage: "Price: {price}",
    description: "Price display with formatted currency",
  },
  reviewCount: {
    id: "product.reviewCount",
    defaultMessage:
      "{count, plural, =0 {No reviews} one {# review} other {# reviews}}",
    description: "Number of product reviews with pluralization",
  },
});
```

**Why good:** centralizes related messages in one file, descriptions provide context for translators, CLI extracts these automatically, IDE autocomplete for message references

#### Usage

```typescript
// src/components/product-card.tsx
import { useIntl } from "react-intl";
import { productMessages } from "../messages/product.messages";

export function ProductCard({ product }: { product: Product }) {
  const intl = useIntl();

  return (
    <article>
      <h2>{intl.formatMessage(productMessages.title)}</h2>
      <p>{intl.formatMessage(productMessages.reviewCount, { count: product.reviewCount })}</p>
      <button>{intl.formatMessage(productMessages.addToCart)}</button>
    </article>
  );
}
```

---

### Pattern 5: Rich Text Formatting

Use XML-like tags in messages for embedded markup.

```typescript
// src/components/terms-notice.tsx
import { FormattedMessage } from "react-intl";

export function TermsNotice() {
  return (
    <p>
      <FormattedMessage
        id="terms.notice"
        defaultMessage="By signing up, you agree to our <terms>Terms of Service</terms> and <privacy>Privacy Policy</privacy>."
        values={{
          terms: (chunks) => <a href="/terms">{chunks}</a>,
          privacy: (chunks) => <a href="/privacy">{chunks}</a>,
        }}
      />
    </p>
  );
}

export { TermsNotice };
```

**Why good:** translation string stays complete and translatable, markup tags are developer-defined, translators can reorder tags per language grammar

#### Default Rich Text Elements

Configure global tag handlers in `IntlProvider` for consistent styling:

```typescript
// src/providers/intl-provider.tsx
import { IntlProvider } from "react-intl";
import type { ReactNode } from "react";

const DEFAULT_RICH_TEXT_ELEMENTS = {
  b: (chunks: ReactNode) => <strong>{chunks}</strong>,
  i: (chunks: ReactNode) => <em>{chunks}</em>,
  br: () => <br />,
};

export function AppIntlProvider({ children, locale, messages }: Props) {
  return (
    <IntlProvider
      locale={locale}
      messages={messages}
      defaultRichTextElements={DEFAULT_RICH_TEXT_ELEMENTS}
    >
      {children}
    </IntlProvider>
  );
}
```

---

### Pattern 6: Formatting Components

Use dedicated components for locale-aware date, time, number, and list formatting.

#### Date and Time

```typescript
// src/components/event-date.tsx
import { FormattedDate, FormattedTime } from "react-intl";

export function EventDate({ date }: { date: Date }) {
  return (
    <time dateTime={date.toISOString()}>
      <FormattedDate
        value={date}
        year="numeric"
        month="long"
        day="numeric"
        weekday="long"
      />
      {" at "}
      <FormattedTime
        value={date}
        hour="numeric"
        minute="numeric"
        timeZoneName="short"
      />
    </time>
  );
}

// Output (en-US): "Monday, January 15, 2024 at 3:30 PM EST"
// Output (de-DE): "Montag, 15. Januar 2024 um 15:30 MEZ"
```

#### Numbers and Currency

```typescript
// src/components/product-price.tsx
import { FormattedNumber } from "react-intl";

const MIN_FRACTION_DIGITS = 2;
const MAX_FRACTION_DIGITS = 2;

export function ProductPrice({ amount, currency }: { amount: number; currency: string }) {
  return (
    <FormattedNumber
      value={amount}
      style="currency"
      currency={currency}
      minimumFractionDigits={MIN_FRACTION_DIGITS}
      maximumFractionDigits={MAX_FRACTION_DIGITS}
    />
  );
}

// Output (en-US, USD): "$1,234.56"
// Output (de-DE, EUR): "1.234,56 EUR"
```

#### Lists

```typescript
// src/components/contributors.tsx
import { FormattedList } from "react-intl";

export function Contributors({ names }: { names: string[] }) {
  return (
    <FormattedList
      type="conjunction"
      value={names}
    />
  );
}

// Output (en): "Alice, Bob, and Charlie"
// Output (es): "Alice, Bob y Charlie"
```

---

### Pattern 7: TypeScript Integration

Enable type-safe message IDs with TypeScript augmentation.

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

**Why good:** typos in message IDs become compile-time errors, IDE autocomplete for message IDs, refactoring keys updates all usages

#### tsconfig.json Requirements

```json
{
  "compilerOptions": {
    "lib": ["esnext.intl", "es2017.intl", "es2018.intl"]
  }
}
```

---

### Pattern 8: Message Extraction Workflow

Use FormatJS CLI for extracting and compiling messages.

#### Package.json Scripts

```json
{
  "scripts": {
    "intl:extract": "formatjs extract 'src/**/*.{ts,tsx}' --ignore='**/*.d.ts' --out-file lang/en.json --id-interpolation-pattern '[sha512:contenthash:base64:6]'",
    "intl:compile": "formatjs compile lang/en.json --out-file src/compiled-lang/en.json --ast",
    "intl:compile:all": "formatjs compile-folder --ast lang src/compiled-lang"
  }
}
```

#### Workflow

1. **Extract** messages from source code
2. **Send** to translation management system (TMS)
3. **Compile** translations to AST format for faster runtime

**Why compile to AST:** 30-50% faster initial render for large message catalogs - skips runtime parsing.

</patterns>

---

<performance>

## Performance Optimization

### Message Compilation (AST Pre-parsing)

Compile messages to AST format at build time to skip runtime parsing:

```bash
formatjs compile lang/en.json --out-file compiled/en.json --ast
```

```typescript
// Load compiled messages instead of raw JSON
import compiledMessages from "./compiled/en.json";

<IntlProvider locale="en" messages={compiledMessages}>
```

**Impact:** 30-50% faster initial render for large message catalogs.

### Lazy Loading Locale Data

```typescript
// src/utils/load-messages.ts
const messageLoaders: Record<string, () => Promise<Record<string, string>>> = {
  en: () => import("../lang/compiled/en.json").then((m) => m.default),
  de: () => import("../lang/compiled/de.json").then((m) => m.default),
  fr: () => import("../lang/compiled/fr.json").then((m) => m.default),
};

const messageCache = new Map<string, Record<string, string>>();

export async function loadMessages(
  locale: string,
): Promise<Record<string, string>> {
  if (messageCache.has(locale)) {
    return messageCache.get(locale)!;
  }

  const loader = messageLoaders[locale] ?? messageLoaders.en;
  const messages = await loader();

  messageCache.set(locale, messages);
  return messages;
}

export { loadMessages };
```

### Avoid Inline Message Objects

```typescript
// WRONG - Creates new object on every render
function Bad() {
  return (
    <FormattedMessage
      id="greeting"
      defaultMessage="Hello!"
      description="Greeting message"
    />
  );
}

// CORRECT - Define messages outside component
const messages = defineMessages({
  greeting: {
    id: "greeting",
    defaultMessage: "Hello!",
    description: "Greeting message",
  },
});

function Good() {
  return <FormattedMessage {...messages.greeting} />;
}
```

</performance>

---

<integration>

## Integration Guide

**react-intl is context-based and React-specific.** It integrates with React's component tree via IntlProvider.

**Works with:**

- **React**: Designed specifically for React applications
- **Testing Library**: Custom render wrapper with IntlProvider
- **TypeScript**: Module augmentation for type-safe message IDs

**Component State Guidance:**

- Use IntlProvider at app root for global i18n context
- For non-React contexts (Node.js, SSR without context), use `createIntl` from `@formatjs/intl`
- Locale state is managed by your application - pass it to IntlProvider

**Replaces / Conflicts with:**

- **next-intl**: For Next.js App Router, prefer next-intl (better SSR integration)
- **i18next**: Different API and message format - choose one, not both

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST wrap the application root with `IntlProvider` and configure locale, messages, and defaultLocale)**

**(You MUST include the `other` category in ALL plural and select ICU messages - omission causes runtime errors)**

**(You MUST use named constants for locale codes - NO inline locale strings)**

**(You MUST verify React version compatibility: v8+ requires React 19+, use v6.x for React 18)**

**Failure to follow these rules will cause runtime errors and broken internationalization.**

</critical_reminders>
