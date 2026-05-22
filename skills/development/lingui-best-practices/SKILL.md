---
name: lingui-best-practices
description: Implement internationalization with Lingui in React and JavaScript applications. Use when adding i18n, translating UI, working with Trans/useLingui/Plural, extracting messages, compiling catalogs, or when the user mentions Lingui, internationalization, i18n, translations, locales, message extraction, ICU MessageFormat, or working with .po files.
---

# Lingui Best Practices

Lingui is a powerful internationalization (i18n) framework for JavaScript. This skill covers best practices for implementing i18n in React and vanilla JavaScript applications.

## Quick Start Workflow

The standard Lingui workflow consists of these steps:

1. Wrap your app in `I18nProvider`
2. Mark messages for translation using macros (`Trans`, `t`, etc.)
3. Extract messages: `lingui extract`
4. Translate the catalogs
5. Compile catalogs: `lingui compile`
6. Load and activate locale in your app

## Core Packages

Import from these packages:

```jsx
// React macros (recommended)
import { Trans, Plural, Select, useLingui } from "@lingui/react/macro";

// Core macros for vanilla JS
import { t, msg, plural, select } from "@lingui/core/macro";

// Runtime (rarely used directly)
import { I18nProvider } from "@lingui/react";
import { i18n } from "@lingui/core";
```

## Setup I18nProvider

Wrap your application with `I18nProvider`:

```jsx
import { I18nProvider } from "@lingui/react";
import { i18n } from "@lingui/core";
import { messages } from "./locales/en/messages";

i18n.load("en", messages);
i18n.activate("en");

function App() {
  return (
    <I18nProvider i18n={i18n}>
      {/* Your app */}
    </I18nProvider>
  );
}
```

## Translating UI Text

### Use Trans for JSX Content

The `Trans` macro is the primary way to translate JSX:

```jsx
import { Trans } from "@lingui/react/macro";

// Simple text
<Trans>Hello World</Trans>

// With variables
<Trans>Hello {userName}</Trans>

// With components (rich text)
<Trans>
  Read the <a href="/docs">documentation</a> for more info.
</Trans>

// Extracted as: "Read the <0>documentation</0> for more info."
```

**When to use**: For any translatable text in JSX elements.

### Use useLingui for Non-JSX

For strings outside JSX (attributes, alerts, function calls):

```jsx
import { useLingui } from "@lingui/react/macro";

function MyComponent() {
  const { t } = useLingui();

  const handleClick = () => {
    alert(t`Action completed!`);
  };

  return (
    <div>
      <img src="..." alt={t`Image description`} />
      <button onClick={handleClick}>{t`Click me`}</button>
    </div>
  );
}
```

**When to use**: Element attributes, alerts, function parameters, any non-JSX string.

### Use msg for Lazy Translations

When you need to define messages at module level or in arrays/objects:

```jsx
import { msg } from "@lingui/core/macro";
import { useLingui } from "@lingui/react";

// Module-level constants
const STATUSES = {
  active: msg`Active`,
  inactive: msg`Inactive`,
  pending: msg`Pending`,
};

function StatusList() {
  const { _ } = useLingui();
  
  return Object.entries(STATUSES).map(([key, message]) => (
    <div key={key}>{_(message)}</div>
  ));
}
```

**When to use**: Module-level constants, arrays of messages, conditional message selection.

## Pluralization

Use the `Plural` macro for quantity-dependent messages:

```jsx
import { Plural } from "@lingui/react/macro";

<Plural 
  value={messageCount}
  one="You have # message"
  other="You have # messages"
/>
```

The `#` placeholder is replaced with the actual value.

### Exact Matches

Use `_N` syntax for exact number matches (takes precedence over plural forms):

```jsx
<Plural
  value={count}
  _0="No messages"
  one="One message"
  other="# messages"
/>
```

### With Variables and Components

Combine with `Trans` for complex messages:

```jsx
<Plural
  value={count}
  one={`You have # message, ${userName}`}
  other={
    <Trans>
      You have <strong>#</strong> messages, {userName}
    </Trans>
  }
/>
```

## Formatting Dates and Numbers

Use `i18n.date()` and `i18n.number()` for locale-aware formatting:

```jsx
import { useLingui } from "@lingui/react/macro";

function MyComponent() {
  const { i18n } = useLingui();
  const lastLogin = new Date();
  
  return (
    <Trans>
      Last login: {i18n.date(lastLogin)}
    </Trans>
  );
}
```

These use the browser's `Intl` API for proper locale formatting.

## Message IDs and Context

### Explicit IDs

Provide a custom ID for stable message keys:

```jsx
<Trans id="header.welcome">Welcome to our app</Trans>
```

### Context for Disambiguation

When the same text has different meanings, use `context`:

```jsx
<Trans context="direction">right</Trans>
<Trans context="correctness">right</Trans>
```

These create separate catalog entries.

### Comments for Translators

Add context for translators:

```jsx
<Trans comment="Greeting shown on homepage">Hello World</Trans>
```

## Configuration

Basic `lingui.config.js`:

```js
import { defineConfig } from "@lingui/cli";

export default defineConfig({
  sourceLocale: "en",
  locales: ["en", "es", "fr", "de"],
  catalogs: [
    {
      path: "<rootDir>/src/locales/{locale}/messages",
      include: ["src"],
      exclude: ["**/node_modules/**"],
    },
  ],
});
```

For detailed configuration patterns, see [configuration.md](references/configuration.md).

## Best Practices

### Always Use Macros

Prefer macros over runtime components. Macros are compiled at build time, reducing bundle size:

```jsx
// ✅ Good - uses macro
import { Trans } from "@lingui/react/macro";

// ❌ Avoid - runtime only
import { Trans } from "@lingui/react";
```

### Keep Messages Simple

Avoid complex expressions in messages - they'll be replaced with placeholders:

```jsx
// ❌ Bad - loses context
<Trans>Hello {user.name.toUpperCase()}</Trans>
// Extracted as: "Hello {0}"

// ✅ Good - clear variable name
const userName = user.name.toUpperCase();
<Trans>Hello {userName}</Trans>
// Extracted as: "Hello {userName}"
```

### Use Trans for JSX, t for Strings

Choose the right tool:

```jsx
// ✅ For JSX content
<h1><Trans>Welcome</Trans></h1>

// ✅ For string values
const { t } = useLingui();
<img alt={t`Profile picture`} />
```

### Don't Use Macros at Module Level

Macros need component context - use `msg` instead:

```jsx
// ❌ Bad - won't work
import { t } from "@lingui/core/macro";
const LABELS = [t`Red`, t`Green`, t`Blue`];

// ✅ Good - use msg for lazy translation
import { msg } from "@lingui/core/macro";
const LABELS = [msg`Red`, msg`Green`, msg`Blue`];
```

### Use the ESLint Plugin

Install and configure `eslint-plugin-lingui` to catch common mistakes automatically:

```bash
npm install --save-dev eslint-plugin-lingui
```

```js
// eslint.config.js
import pluginLingui from "eslint-plugin-lingui";

export default [
  pluginLingui.configs["flat/recommended"],
];
```

## Common Patterns

### Dynamic Locale Switching

```jsx
import { i18n } from "@lingui/core";

async function changeLocale(locale) {
  const { messages } = await import(`./locales/${locale}/messages`);
  i18n.load(locale, messages);
  i18n.activate(locale);
}
```

### Loading Catalogs Dynamically

```jsx
import { useEffect } from "react";
import { i18n } from "@lingui/core";

function loadCatalog(locale) {
  return import(`./locales/${locale}/messages`);
}

function App() {
  useEffect(() => {
    loadCatalog("en").then(catalog => {
      i18n.load("en", catalog.messages);
      i18n.activate("en");
    });
  }, []);
  
  return <I18nProvider i18n={i18n}>{/* ... */}</I18nProvider>;
}
```

### Memoization with useLingui

When using memoization, use the `t` function from the macro version:

```jsx
import { useLingui } from "@lingui/react/macro";
import { msg } from "@lingui/core/macro";
import { useMemo } from "react";

const welcomeMessage = msg`Welcome!`;

function MyComponent() {
  const { t } = useLingui(); // Macro version - reference changes with locale
  
  // ✅ Safe - t reference updates with locale
  const message = useMemo(() => t(welcomeMessage), [t]);
  
  return <div>{message}</div>;
}
```

## Troubleshooting

If you encounter issues:

1. **Messages not extracted**: Check `include` patterns in `lingui.config.js`
2. **Translations not applied**: Ensure catalogs are compiled with `lingui compile`
3. **Runtime errors**: Verify `I18nProvider` wraps your app
4. **Type errors**: Run `lingui compile --typescript` for TypeScript projects

For detailed common mistakes and pitfalls, see [common-mistakes.md](references/common-mistakes.md).
