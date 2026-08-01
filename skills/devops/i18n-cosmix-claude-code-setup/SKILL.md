---
name: i18n
description: 'Internationalization and localization implementation. Use when implementing
  multi-language support, translation systems, locale-specific formatting, or RTL
  layouts. Keywords: i18n, l10n, international'
---

---
name: i18n
description: Internationalization and localization implementation. Use when implementing multi-language support, translation systems, locale-specific formatting, or RTL layouts. Keywords: i18n, l10n, internationalization, localization, translation, locale, RTL, pluralization, i18next, react-intl, gettext, ICU, formatting.
---

# Internationalization (i18n)

## Overview

Internationalization (i18n) is the process of designing software so it can be adapted to various languages and regions without engineering changes. Localization (l10n) is the actual adaptation for a specific locale. This skill covers architecture patterns, translation formats, locale-specific formatting, and popular libraries.

## Key Concepts

### Internationalization Architecture

**Core Principles:**

- Separate translatable content from code
- Use locale identifiers (e.g., `en-US`, `fr-FR`, `zh-Hans`)
- Support dynamic locale switching
- Handle fallback chains (e.g., `de-AT` -> `de` -> `en`)

**Architecture Pattern:**

```
src/
  locales/
    en/
      common.json
      products.json
      errors.json
    fr/
      common.json
      products.json
      errors.json
  i18n/
    config.ts
    index.ts
```

**Locale Configuration:**

```typescript
interface LocaleConfig {
  code: string; // e.g., 'en-US'
  language: string; // e.g., 'en'
  region?: string; // e.g., 'US'
  direction: "ltr" | "rtl";
  dateFormat: string;
  numberFormat: Intl.NumberFormatOptions;
  currency: string;
}

const locales: Record<string, LocaleConfig> = {
  "en-US": {
    code: "en-US",
    language: "en",
    region: "US",
    direction: "ltr",
    dateFormat: "MM/dd/yyyy",
    numberFormat: { style: "decimal", minimumFractionDigits: 2 },
    currency: "USD",
  },
  "de-DE": {
    code: "de-DE",
    language: "de",
    region: "DE",
    direction: "ltr",
    dateFormat: "dd.MM.yyyy",
    numberFormat: { style: "decimal", minimumFractionDigits: 2 },
    currency: "EUR",
  },
  "ar-SA": {
    code: "ar-SA",
    language: "ar",
    region: "SA",
    direction: "rtl",
    dateFormat: "dd/MM/yyyy",
    numberFormat: { style: "decimal", minimumFractionDigits: 2 },
    currency: "SAR",
  },
};
```

### Translation File Formats

**JSON Format (i18next, react-intl):**

```json
{
  "common": {
    "welcome": "Welcome, {{name}}!",
    "items_count": "{{count}} item",
    "items_count_plural": "{{count}} items"
  },
  "products": {
    "title": "Products",
    "addToCart": "Add to Cart",
    "price": "Price: {{price, currency}}"
  },
  "errors": {
    "required": "This field is required",
    "minLength": "Must be at least {{min}} characters"
  }
}
```

**Nested JSON with Namespaces:**

```json
{
  "nav": {
    "home": "Home",
    "products": "Products",
    "about": "About Us"
  },
  "footer": {
    "copyright": "Copyright 2024",
    "links": {
      "privacy": "Privacy Policy",
      "terms": "Terms of Service"
    }
  }
}
```

**YAML Format:**

```yaml
common:
  welcome: "Welcome, {name}!"
  items_count:
    one: "{count} item"
    other: "{count} items"

products:
  title: Products
  addToCart: Add to Cart
  outOfStock: Out of Stock

errors:
  required: This field is required
  email: Please enter a valid email
```

**PO/POT Format (gettext):**

```po
# English translations
msgid ""
msgstr ""
"Content-Type: text/plain; charset=UTF-8\n"
"Language: en\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\n"

#: src/components/Header.js:15
msgid "Welcome"
msgstr "Welcome"

#: src/components/Cart.js:42
msgid "item"
msgid_plural "items"
msgstr[0] "item"
msgstr[1] "items"

#: src/components/Product.js:28
#, python-format
msgid "Price: %(price)s"
msgstr "Price: %(price)s"
```

### Pluralization Rules

**ICU MessageFormat:**

```javascript
const messages = {
  // English
  en: {
    items: "{count, plural, =0 {No items} one {# item} other {# items}}",
    cartItems: `{count, plural,
      =0 {Your cart is empty}
      one {You have # item in your cart}
      other {You have # items in your cart}
    }`,
  },
  // Russian (3 plural forms)
  ru: {
    items: `{count, plural,
      one {# товар}
      few {# товара}
      many {# товаров}
      other {# товаров}
    }`,
  },
  // Arabic (6 plural forms)
  ar: {
    items: `{count, plural,
      zero {لا عناصر}
      one {عنصر واحد}
      two {عنصران}
      few {# عناصر}
      many {# عنصرًا}
      other {# عنصر}
    }`,
  },
};
```

**Select and SelectOrdinal:**

```javascript
const messages = {
  gender: `{gender, select,
    male {He}
    female {She}
    other {They}
  } liked your post.`,

  ordinal: `{position, selectordinal,
    one {#st}
    two {#nd}
    few {#rd}
    other {#th}
  } place`,
};
```

### Date/Time/Number Formatting

**Using Intl API:**

```typescript
class LocaleFormatter {
  private locale: string;

  constructor(locale: string) {
    this.locale = locale;
  }

  formatNumber(value: number, options?: Intl.NumberFormatOptions): string {
    return new Intl.NumberFormat(this.locale, options).format(value);
  }

  formatCurrency(value: number, currency: string): string {
    return new Intl.NumberFormat(this.locale, {
      style: "currency",
      currency,
    }).format(value);
  }

  formatDate(date: Date, options?: Intl.DateTimeFormatOptions): string {
    return new Intl.DateTimeFormat(this.locale, options).format(date);
  }

  formatRelativeTime(value: number, unit: Intl.RelativeTimeFormatUnit): string {
    return new Intl.RelativeTimeFormat(this.locale, {
      numeric: "auto",
    }).format(value, unit);
  }

  formatList(
    items: string[],
    type: "conjunction" | "disjunction" = "conjunction",
  ): string {
    return new Intl.ListFormat(this.locale, { type }).format(items);
  }
}

// Usage
const formatter = new LocaleFormatter("de-DE");
formatter.formatNumber(1234567.89); // "1.234.567,89"
formatter.formatCurrency(99.99, "EUR"); // "99,99 €"
formatter.formatDate(new Date()); // "19.12.2024"
formatter.formatRelativeTime(-1, "day"); // "gestern"
formatter.formatList(["A", "B", "C"]); // "A, B und C"
```

**Date Format Patterns by Locale:**

```typescript
const datePatterns: Record<string, Intl.DateTimeFormatOptions> = {
  short: { dateStyle: "short" },
  medium: { dateStyle: "medium" },
  long: { dateStyle: "long" },
  full: { dateStyle: "full" },
  custom: {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long",
  },
};

// Results vary by locale:
// en-US: "Thursday, December 19, 2024"
// de-DE: "Donnerstag, 19. Dezember 2024"
// ja-JP: "2024年12月19日木曜日"
```

### RTL (Right-to-Left) Support

**CSS Logical Properties:**

```css
/* Instead of physical properties */
.card {
  /* Use logical properties for automatic RTL support */
  margin-inline-start: 1rem; /* margin-left in LTR, margin-right in RTL */
  margin-inline-end: 2rem;
  padding-inline: 1rem;
  padding-block: 0.5rem;
  border-inline-start: 3px solid blue;
  text-align: start; /* left in LTR, right in RTL */
}

/* Flexbox and Grid automatically adapt */
.container {
  display: flex;
  flex-direction: row; /* Adapts to document direction */
  gap: 1rem;
}
```

**Direction-Aware Styling:**

```css
/* Set direction at root */
html[dir="rtl"] {
  direction: rtl;
}

/* Use :dir() pseudo-class */
.icon:dir(rtl) {
  transform: scaleX(-1); /* Flip icons */
}

/* Bidirectional text handling */
.mixed-content {
  unicode-bidi: isolate;
}
```

**React RTL Implementation:**

```tsx
import { createContext, useContext, ReactNode } from "react";

interface DirectionContextType {
  direction: "ltr" | "rtl";
  isRTL: boolean;
}

const DirectionContext = createContext<DirectionContextType>({
  direction: "ltr",
  isRTL: false,
});

export function DirectionProvider({
  locale,
  children,
}: {
  locale: string;
  children: ReactNode;
}) {
  const rtlLocales = ["ar", "he", "fa", "ur"];
  const language = locale.split("-")[0];
  const isRTL = rtlLocales.includes(language);
  const direction = isRTL ? "rtl" : "ltr";

  return (
    <DirectionContext.Provider value={{ direction, isRTL }}>
      <div dir={direction}>{children}</div>
    </DirectionContext.Provider>
  );
}

export const useDirection = () => useContext(DirectionContext);
```

### Content Localization Strategies

**Dynamic Content Loading:**

```typescript
async function loadTranslations(locale: string, namespace: string) {
  try {
    const translations = await import(`../locales/${locale}/${namespace}.json`);
    return translations.default;
  } catch {
    // Fallback to default locale
    const fallback = await import(`../locales/en/${namespace}.json`);
    return fallback.default;
  }
}
```

**Server-Side Locale Detection:**

```typescript
function detectLocale(request: Request): string {
  // 1. Check URL parameter
  const url = new URL(request.url);
  const urlLocale = url.searchParams.get("locale");
  if (urlLocale && isValidLocale(urlLocale)) return urlLocale;

  // 2. Check cookie
  const cookieLocale = getCookie(request, "locale");
  if (cookieLocale && isValidLocale(cookieLocale)) return cookieLocale;

  // 3. Check Accept-Language header
  const acceptLanguage = request.headers.get("Accept-Language");
  if (acceptLanguage) {
    const preferred = parseAcceptLanguage(acceptLanguage);
    const matched = preferred.find((l) => isValidLocale(l));
    if (matched) return matched;
  }

  // 4. Default locale
  return "en-US";
}

function parseAcceptLanguage(header: string): string[] {
  return header
    .split(",")
    .map((lang) => {
      const [code, q] = lang.trim().split(";q=");
      return { code: code.trim(), q: parseFloat(q) || 1 };
    })
    .sort((a, b) => b.q - a.q)
    .map(({ code }) => code);
}
```

### Libraries: i18next, react-intl, gettext

**i18next Setup:**

```typescript
import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import Backend from "i18next-http-backend";
import LanguageDetector from "i18next-browser-languagedetector";

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    supportedLngs: ["en", "de", "fr", "es", "ar"],
    ns: ["common", "products", "errors"],
    defaultNS: "common",
    backend: {
      loadPath: "/locales/{{lng}}/{{ns}}.json",
    },
    interpolation: {
      escapeValue: false,
      format: (value, format, lng) => {
        if (format === "currency") {
          return new Intl.NumberFormat(lng, {
            style: "currency",
            currency: "USD",
          }).format(value);
        }
        if (value instanceof Date) {
          return new Intl.DateTimeFormat(lng).format(value);
        }
        return value;
      },
    },
    react: {
      useSuspense: true,
    },
  });

export default i18n;
```

**i18next Usage in React:**

```tsx
import { useTranslation, Trans } from "react-i18next";

function ProductCard({ product }) {
  const { t, i18n } = useTranslation(["products", "common"]);

  return (
    <div>
      <h2>{product.name}</h2>
      <p>{t("products:price", { price: product.price })}</p>
      <p>{t("common:items_count", { count: product.stock })}</p>

      <Trans i18nKey="products:description" values={{ name: product.name }}>
        Check out <strong>{{ name: product.name }}</strong> today!
      </Trans>

      <button onClick={() => i18n.changeLanguage("de")}>
        {t("common:switchLanguage")}
      </button>
    </div>
  );
}
```

**react-intl Setup:**

```tsx
import { IntlProvider, FormattedMessage, useIntl } from "react-intl";

const messages = {
  en: {
    "app.greeting": "Hello, {name}!",
    "app.items": "{count, plural, =0 {No items} one {# item} other {# items}}",
  },
  de: {
    "app.greeting": "Hallo, {name}!",
    "app.items":
      "{count, plural, =0 {Keine Artikel} one {# Artikel} other {# Artikel}}",
  },
};

function App() {
  const [locale, setLocale] = useState("en");

  return (
    <IntlProvider locale={locale} messages={messages[locale]}>
      <Content />
    </IntlProvider>
  );
}

function Content() {
  const intl = useIntl();

  return (
    <div>
      <FormattedMessage id="app.greeting" values={{ name: "World" }} />

      <p>{intl.formatMessage({ id: "app.items" }, { count: 5 })}</p>

      <p>
        {intl.formatNumber(1234.56, { style: "currency", currency: "EUR" })}
      </p>
      <p>{intl.formatDate(new Date(), { dateStyle: "long" })}</p>
    </div>
  );
}
```

**Python gettext:**

```python
import gettext
from pathlib import Path

# Setup
localedir = Path(__file__).parent / 'locales'
translation = gettext.translation(
    'messages',
    localedir=localedir,
    languages=['de'],
    fallback=True
)
_ = translation.gettext
ngettext = translation.ngettext

# Usage
print(_("Hello, World!"))
print(_("Welcome, %(name)s!") % {'name': 'User'})

count = 5
print(ngettext(
    "%(count)d item",
    "%(count)d items",
    count
) % {'count': count})
```

## Best Practices

### Architecture

- Extract all user-facing strings into translation files
- Use namespaces to organize translations by feature/page
- Implement locale fallback chains
- Load translations lazily for better performance

### Translation Keys

- Use descriptive, hierarchical keys (e.g., `products.card.addToCart`)
- Include context in keys when meaning is ambiguous
- Never use raw text as keys (brittle, hard to track)
- Document placeholders and their expected values

### Formatting

- Always use locale-aware formatting for dates, numbers, currencies
- Use ICU MessageFormat for complex pluralization
- Handle timezone conversion server-side when possible
- Consider cultural differences (e.g., name order, address format)

### RTL Support

- Use CSS logical properties exclusively
- Test with actual RTL content, not just mirrored LTR
- Handle bidirectional text properly
- Ensure icons and images are direction-appropriate

### Testing

- Test with pseudo-localization to catch hardcoded strings
- Test with long translations (German) for UI overflow
- Test with RTL languages for layout issues
- Automate extraction of untranslated strings

## Examples

### Complete React i18n Setup

```tsx
// i18n/config.ts
import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import Backend from "i18next-http-backend";
import LanguageDetector from "i18next-browser-languagedetector";

export const supportedLocales = [
  { code: "en-US", name: "English", dir: "ltr" },
  { code: "de-DE", name: "Deutsch", dir: "ltr" },
  { code: "ar-SA", name: "العربية", dir: "rtl" },
] as const;

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: "en-US",
    supportedLngs: supportedLocales.map((l) => l.code),
    load: "currentOnly",
    ns: ["common", "products"],
    defaultNS: "common",
    backend: {
      loadPath: "/locales/{{lng}}/{{ns}}.json",
    },
    detection: {
      order: ["querystring", "cookie", "navigator"],
      caches: ["cookie"],
    },
  });

export default i18n;

// hooks/useLocale.ts
import { useTranslation } from "react-i18next";
import { supportedLocales } from "../i18n/config";

export function useLocale() {
  const { i18n } = useTranslation();

  const currentLocale =
    supportedLocales.find((l) => l.code === i18n.language) ||
    supportedLocales[0];

  const changeLocale = async (code: string) => {
    await i18n.changeLanguage(code);
    document.documentElement.dir =
      supportedLocales.find((l) => l.code === code)?.dir || "ltr";
    document.documentElement.lang = code;
  };

  return {
    locale: currentLocale,
    locales: supportedLocales,
    changeLocale,
    isRTL: currentLocale.dir === "rtl",
  };
}

// components/LocaleSwitcher.tsx
import { useLocale } from "../hooks/useLocale";

export function LocaleSwitcher() {
  const { locale, locales, changeLocale } = useLocale();

  return (
    <select
      value={locale.code}
      onChange={(e) => changeLocale(e.target.value)}
      aria-label="Select language"
    >
      {locales.map((l) => (
        <option key={l.code} value={l.code}>
          {l.name}
        </option>
      ))}
    </select>
  );
}
```

### Translation Extraction Script

```javascript
// scripts/extract-translations.js
const fs = require("fs");
const path = require("path");
const parser = require("@babel/parser");
const traverse = require("@babel/traverse").default;

const sourceDir = "./src";
const outputFile = "./locales/extracted.json";

function extractTranslationKeys(code) {
  const keys = new Set();

  const ast = parser.parse(code, {
    sourceType: "module",
    plugins: ["jsx", "typescript"],
  });

  traverse(ast, {
    CallExpression(path) {
      if (
        path.node.callee.name === "t" ||
        path.node.callee.property?.name === "t"
      ) {
        const arg = path.node.arguments[0];
        if (arg?.type === "StringLiteral") {
          keys.add(arg.value);
        }
      }
    },
  });

  return keys;
}

function walkDir(dir) {
  const allKeys = new Set();

  const files = fs.readdirSync(dir);
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      walkDir(filePath).forEach((k) => allKeys.add(k));
    } else if (/\.(tsx?|jsx?)$/.test(file)) {
      const code = fs.readFileSync(filePath, "utf8");
      extractTranslationKeys(code).forEach((k) => allKeys.add(k));
    }
  }

  return allKeys;
}

const keys = walkDir(sourceDir);
const result = {};
keys.forEach((key) => {
  result[key] = "";
});

fs.writeFileSync(outputFile, JSON.stringify(result, null, 2));
console.log(`Extracted ${keys.size} translation keys`);
```
