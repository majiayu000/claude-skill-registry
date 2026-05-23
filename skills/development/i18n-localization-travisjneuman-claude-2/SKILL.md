---
name: i18n-localization
description: Internationalization and localization for global applications. Use when adding multi-language support, handling regional formats, or preparing apps for global markets.
---

# Internationalization & Localization

Comprehensive guide for building globally-ready applications.

## Key Concepts

### Terminology

```
i18n (Internationalization):
- Engineering for multiple languages/regions
- Building the infrastructure
- Happens once, during development

L10n (Localization):
- Adapting for specific locale
- Translation, formatting, content
- Happens per locale, ongoing

Locale:
- Language + Region combination
- Format: language-REGION (e.g., en-US, pt-BR)
- Determines formatting rules
```

### What Needs Localization?

| Category      | Examples                     |
| ------------- | ---------------------------- |
| **Text**      | UI labels, messages, errors  |
| **Numbers**   | 1,234.56 vs 1.234,56         |
| **Dates**     | MM/DD/YYYY vs DD/MM/YYYY     |
| **Times**     | 12-hour vs 24-hour           |
| **Currency**  | $1,234.56 vs €1.234,56       |
| **Plurals**   | 1 item vs 2 items vs 5 items |
| **Direction** | LTR vs RTL                   |
| **Images**    | Cultural appropriateness     |
| **Colors**    | Cultural significance        |
| **Names**     | Order, formality             |

---

## Text & Messages

### Externalize All Strings

```typescript
// DON'T: Hardcoded strings
const message = "Welcome back, " + username;

// DO: Externalized, translatable
const message = t('welcome_back', { name: username });

// Translation file (en.json)
{
  "welcome_back": "Welcome back, {{name}}"
}

// Translation file (es.json)
{
  "welcome_back": "Bienvenido de nuevo, {{name}}"
}
```

### Message Format

```typescript
// ICU Message Format (recommended)
// Handles plurals, select, dates, numbers

// Simple
"greeting": "Hello, {name}!"

// Plural
"items_count": "{count, plural, =0 {No items} one {# item} other {# items}}"

// Select (gender, etc.)
"notification": "{gender, select, male {He} female {She} other {They}} liked your post"

// Nested
"cart": "{itemCount, plural,
  =0 {Your cart is empty}
  one {You have # item in your cart}
  other {You have # items in your cart}
}"
```

### Pluralization

```
Languages have different plural rules:

English: 1 (one), 2+ (other)
French:  0-1 (one), 2+ (other)
Russian: Complex rules for 1, 2-4, 5-20, 21, etc.
Arabic:  6 plural forms!
Chinese: No plural forms

Always use library pluralization, never DIY:
- react-intl / formatjs
- i18next
- Intl.PluralRules API
```

---

## Date & Time

### JavaScript Intl API

```typescript
// Date formatting
const date = new Date("2024-03-15");

new Intl.DateTimeFormat("en-US").format(date);
// "3/15/2024"

new Intl.DateTimeFormat("de-DE").format(date);
// "15.3.2024"

new Intl.DateTimeFormat("ja-JP").format(date);
// "2024/3/15"

// With options
new Intl.DateTimeFormat("en-US", {
  weekday: "long",
  year: "numeric",
  month: "long",
  day: "numeric",
}).format(date);
// "Friday, March 15, 2024"
```

### Time Zones

```typescript
// Always store in UTC
const utcDate = new Date().toISOString();
// "2024-03-15T14:30:00.000Z"

// Display in user's timezone
new Intl.DateTimeFormat("en-US", {
  timeZone: "America/New_York",
  dateStyle: "full",
  timeStyle: "long",
}).format(new Date(utcDate));
// "Friday, March 15, 2024 at 10:30:00 AM EDT"

// Get user's timezone
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
```

### Relative Time

```typescript
const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });

rtf.format(-1, "day"); // "yesterday"
rtf.format(1, "day"); // "tomorrow"
rtf.format(-3, "hour"); // "3 hours ago"
rtf.format(2, "week"); // "in 2 weeks"

// For automatic unit selection, use a library like date-fns
import { formatDistanceToNow } from "date-fns";
formatDistanceToNow(date, { addSuffix: true });
// "3 days ago"
```

---

## Numbers & Currency

### Number Formatting

```typescript
const number = 1234567.89;

new Intl.NumberFormat("en-US").format(number);
// "1,234,567.89"

new Intl.NumberFormat("de-DE").format(number);
// "1.234.567,89"

new Intl.NumberFormat("fr-FR").format(number);
// "1 234 567,89"

// Percentages
new Intl.NumberFormat("en-US", {
  style: "percent",
  minimumFractionDigits: 1,
}).format(0.256);
// "25.6%"
```

### Currency Formatting

```typescript
const amount = 1234.56;

new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
}).format(amount);
// "$1,234.56"

new Intl.NumberFormat("de-DE", {
  style: "currency",
  currency: "EUR",
}).format(amount);
// "1.234,56 €"

new Intl.NumberFormat("ja-JP", {
  style: "currency",
  currency: "JPY",
}).format(amount);
// "¥1,235" (no decimal for JPY)
```

### Currency Best Practices

```typescript
// Store amount + currency code
interface Money {
  amount: number; // In smallest unit (cents)
  currency: string; // ISO 4217 code (USD, EUR, etc.)
}

// Format for display
function formatMoney(money: Money, locale: string): string {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency: money.currency,
  }).format(money.amount / 100); // Convert cents to units
}

// Handle exchange rates on backend
// Never convert currencies client-side
```

---

## RTL (Right-to-Left) Support

### RTL Languages

```
RTL Languages:
- Arabic (ar)
- Hebrew (he)
- Persian/Farsi (fa)
- Urdu (ur)

Layout considerations:
┌─────────────────────────────┐  ┌─────────────────────────────┐
│ Logo      Menu    Settings  │  │ Settings    Menu      Logo  │
│ ← Back                      │  │                      Back → │
│ [Icon] Label                │  │                Label [Icon] │
│                      Next → │  │ ← Next                      │
└─────────────────────────────┘  └─────────────────────────────┘
        LTR Layout                        RTL Layout
```

### CSS for RTL

```css
/* Use logical properties */
/* DON'T: Physical properties */
.element {
  margin-left: 10px;
  padding-right: 20px;
  text-align: left;
  float: left;
}

/* DO: Logical properties */
.element {
  margin-inline-start: 10px;
  padding-inline-end: 20px;
  text-align: start;
  float: inline-start;
}

/* Set direction based on locale */
html[dir="rtl"] {
  direction: rtl;
}

/* Or use :dir() pseudo-class */
.icon:dir(rtl) {
  transform: scaleX(-1); /* Mirror icons */
}

/* Flexbox auto-reverses in RTL */
.container {
  display: flex;
  /* No need to change for RTL */
}
```

### HTML Direction

```html
<!-- Set at document level -->
<html lang="ar" dir="rtl">
  <!-- Or dynamically -->
  <div dir="auto">
    <!-- Auto-detects text direction -->
    مرحبا بالعالم
  </div>

  <!-- Isolate bidirectional text -->
  <p>The word <bdi>مرحبا</bdi> means "hello".</p>
</html>
```

---

## Implementation (React)

### react-intl Setup

```typescript
// src/i18n/index.ts
import { createIntl, createIntlCache } from '@formatjs/intl';

const cache = createIntlCache();

const messages = {
  en: () => import('./locales/en.json'),
  es: () => import('./locales/es.json'),
  fr: () => import('./locales/fr.json'),
};

export async function loadMessages(locale: string) {
  const loader = messages[locale] || messages.en;
  return (await loader()).default;
}

// App.tsx
import { IntlProvider } from 'react-intl';

function App() {
  const [locale, setLocale] = useState('en');
  const [messages, setMessages] = useState({});

  useEffect(() => {
    loadMessages(locale).then(setMessages);
  }, [locale]);

  return (
    <IntlProvider locale={locale} messages={messages}>
      <MainApp />
    </IntlProvider>
  );
}
```

### Using Translations

```tsx
import { FormattedMessage, useIntl } from "react-intl";

function ProductCard({ product }) {
  const intl = useIntl();

  return (
    <div>
      {/* Component-based */}
      <h2>
        <FormattedMessage id="product.title" values={{ name: product.name }} />
      </h2>

      {/* Hook-based (for attributes, etc.) */}
      <img
        src={product.image}
        alt={intl.formatMessage({ id: "product.image_alt" })}
      />

      {/* Numbers */}
      <p>
        <FormattedNumber
          value={product.price}
          style="currency"
          currency="USD"
        />
      </p>

      {/* Dates */}
      <p>
        <FormattedDate value={product.createdAt} dateStyle="medium" />
      </p>

      {/* Plurals */}
      <p>
        <FormattedMessage
          id="product.reviews"
          values={{ count: product.reviewCount }}
        />
      </p>
    </div>
  );
}
```

### Translation Files

```json
// locales/en.json
{
  "product.title": "{name}",
  "product.image_alt": "Photo of {name}",
  "product.reviews": "{count, plural, =0 {No reviews} one {# review} other {# reviews}}",
  "cart.empty": "Your cart is empty",
  "cart.checkout": "Proceed to checkout"
}

// locales/es.json
{
  "product.title": "{name}",
  "product.image_alt": "Foto de {name}",
  "product.reviews": "{count, plural, =0 {Sin reseñas} one {# reseña} other {# reseñas}}",
  "cart.empty": "Tu carrito está vacío",
  "cart.checkout": "Proceder al pago"
}
```

---

## Implementation (Node.js)

### i18next Setup

```typescript
import i18next from "i18next";
import Backend from "i18next-fs-backend";

await i18next.use(Backend).init({
  lng: "en",
  fallbackLng: "en",
  supportedLngs: ["en", "es", "fr", "de"],
  backend: {
    loadPath: "./locales/{{lng}}/{{ns}}.json",
  },
  interpolation: {
    escapeValue: false,
  },
});

// Usage
const t = i18next.t;

t("welcome", { name: "John" });
// "Welcome, John!"

// Change language
await i18next.changeLanguage("es");
```

### Express Middleware

```typescript
import { Request, Response, NextFunction } from "express";

function detectLocale(req: Request, res: Response, next: NextFunction) {
  // Priority: Query param > Cookie > Accept-Language header > Default
  const locale =
    req.query.locale ||
    req.cookies.locale ||
    req.acceptsLanguages(["en", "es", "fr"]) ||
    "en";

  req.locale = locale;
  req.t = i18next.getFixedT(locale);

  next();
}

app.use(detectLocale);

app.get("/api/greeting", (req, res) => {
  res.json({
    message: req.t("greeting", { name: req.user.name }),
  });
});
```

---

## Translation Workflow

### File Structure

```
locales/
├── en/
│   ├── common.json       # Shared strings
│   ├── auth.json         # Auth-related
│   ├── products.json     # Product-related
│   └── errors.json       # Error messages
├── es/
│   └── ...
├── fr/
│   └── ...
└── _source/
    └── en.json           # Source of truth
```

### Key Naming Convention

```json
{
  // Feature.element.description
  "auth.login.button": "Sign In",
  "auth.login.error.invalid_credentials": "Invalid email or password",

  // Or flat with prefixes
  "btn_login": "Sign In",
  "err_invalid_credentials": "Invalid email or password"

  // Consistent, descriptive, unique
}
```

### Translation Management

```
TOOLS:
- Lokalise, Crowdin, Phrase (SaaS platforms)
- Weblate (open source)
- POEditor, Transifex

WORKFLOW:
1. Extract strings from code
2. Upload to translation platform
3. Translators work in context
4. Review translations
5. Download and integrate
6. Test in app
7. Repeat for changes

AUTOMATION:
- CI/CD integration
- Automatic string extraction
- Translation memory
- Machine translation + human review
```

---

## Testing

### Pseudo-Localization

```typescript
// Transforms: "Hello" → "[Ħëľľö!!!]"
// Helps identify:
// - Hardcoded strings
// - Text truncation issues
// - Character encoding problems
// - Layout issues with longer text

function pseudoLocalize(text: string): string {
  const charMap: Record<string, string> = {
    a: "ä",
    b: "β",
    c: "ç",
    d: "δ",
    e: "ë",
    // ... etc
  };

  const transformed = text
    .split("")
    .map((c) => charMap[c.toLowerCase()] || c)
    .join("");

  // Add padding (most translations are 30% longer)
  const padding = "!".repeat(Math.ceil(text.length * 0.3));

  return `[${transformed}${padding}]`;
}
```

### Locale Testing Checklist

```
FOR EACH LOCALE:
□ All strings translated
□ No hardcoded text visible
□ Dates format correctly
□ Numbers format correctly
□ Currency displays properly
□ Plurals work for all cases
□ UI accommodates text length
□ RTL layout correct (if applicable)
□ Images are appropriate
□ No encoding issues
□ Forms validate appropriately
```

---

## Best Practices

### DO:

- Externalize ALL user-facing strings
- Use ICU message format for complex strings
- Support locale switching without reload
- Test with pseudo-localization
- Store dates in UTC, display in local time
- Use native Intl APIs when possible
- Plan for text expansion (30-50% longer)
- Support RTL from the start

### DON'T:

- Hardcode any user-facing text
- Concatenate strings for messages
- Assume date/number formats
- Handle plurals manually
- Forget about cultural context
- Translate in code (use translation files)
- Ignore bidirectional text issues
- Skip testing with real languages

---

## Checklist

### Initial Setup

- [ ] Choose i18n library
- [ ] Set up translation file structure
- [ ] Configure locale detection
- [ ] Add locale switcher UI
- [ ] Set up RTL support

### Per Feature

- [ ] Extract all strings to translation files
- [ ] Use message format for variables
- [ ] Handle plurals correctly
- [ ] Format dates/numbers/currency
- [ ] Test with pseudo-localization
- [ ] Review text in context

### Launch

- [ ] Professional translations complete
- [ ] All locales tested
- [ ] RTL layouts verified
- [ ] SEO for multi-language (hreflang)
- [ ] Locale-specific content reviewed
