---
name: i18n-patterns
description: Internationalization (i18n) patterns using inline t() calls with compile-time Babel transformation. Use when adding or modifying translated text, working with locales, creating new pages or components that need translations, using the t() function, mentioning i18n, translations, locale switching, useLocale, setLocale, or when the user asks about how translations work in this project. Also use when working with the i18n codegen pipeline, Babel plugin, or generated translation bundles.
---

# Internationalization (i18n)

## How It Works

Translations are written **inline** using the `t()` function. A Babel plugin transforms these calls at compile time into hash-based lookups against generated JSON bundles. The same `t()` API works in both server and client components — the Babel plugin selects the correct runtime automatically.

```
Source: t({ en: "Hello", zh: "你好" })
  ↓ Babel plugin
Server: __i18n_lookup("a8cfb50c")   — reads from server JSON bundle
Client: useI18nLookup("a8cfb50c")  — reads from React context (hook)
```

## Supported Locales

- `en` — English
- `zh` — Chinese

Defined as `SupportedLocale` in `src/types.ts`. Routes use `[locale]` parameter: `/en/about`, `/zh/about`.

## The `t()` Function

Import from `#src/i18n.ts`. Pass an object with `en` and `zh` string literal properties:

```tsx
import { t } from "#src/i18n.ts";

// Plain text
t({ en: "Hello", zh: "你好" });

// With HTML markup — returns ReactNode instead of string
t(
  { en: "<strong>Bold text</strong>", zh: "<strong>粗体文字</strong>" },
  { parse: true },
);
```

Both `en` and `zh` values must be **string literals** — no variables, template literals, or expressions. The codegen and Babel plugin rely on statically extracting these at build time.

Supported HTML tags in `{ parse: true }` mode: `<strong>`, `<em>`, `<b>`, `<i>`, `<p>`.

## Server Components

Use `t()` directly. No special setup needed — the Babel plugin handles everything:

```tsx
import { t } from "#src/i18n.ts";

export default function Page() {
  return <h1>{t({ en: "Welcome", zh: "欢迎" })}</h1>;
}
```

For **page files** (`page.tsx` under `[locale]`), the Babel plugin auto-injects `setLocale()` at the top of the default export function. You do not need to manually call `setLocale` or accept `params` — the plugin makes the function async, reads `params.locale`, and calls `setLocale(validateLocale(params.locale))` for you.

Layout files that need the locale for other purposes (e.g. `generateMetadata`, routing logic) should still read `params` manually since they have non-i18n reasons to do so.

## Client Components

Use `t()` identically — the Babel plugin detects `"use client"` and swaps in client-specific lookup functions that read from React context:

```tsx
"use client";

import { t } from "#src/i18n.ts";

export function SearchButton() {
  return <button>{t({ en: "Search", zh: "搜索" })}</button>;
}
```

Client translations are provided automatically. The codegen generates a **manifest** mapping page/layout files to their client translation bundles. The Babel plugin reads this manifest and auto-wraps the default export's return value with `<ClientTranslationsProvider>`, so client components receive translations without any manual wiring.

### Getting the Locale in Client Components

Use the `useLocale()` hook when you need the locale value itself (not for translations):

```tsx
"use client";

import { useLocale } from "#src/hooks/use-locale.ts";

export function LocaleAwareComponent() {
  const locale = useLocale();
  const formatter = new Intl.NumberFormat(locale);
  return <span>{formatter.format(1234)}</span>;
}
```

## Generating Localized URLs

```tsx
import { getLocalePath } from "#src/utils/pathname.ts";

getLocalePath("/about", locale); // → "/en/about" or "/zh/about"
```

## Build Pipeline

### Codegen (`pnpm codegen:i18n`)

The codegen script in `tooling/i18n-codegen/` does:

1. **Extracts** all `t()` calls from source files via AST parsing
2. **Generates** global JSON bundles: `src/_generated/i18n/translations.{en,zh}.json`
3. **Traces** client component imports from each page/layout entry point
4. **Generates** per-page client bundles: `src/_generated/i18n/client/{name}.{en,zh}.json`
5. **Generates** loader modules: `src/_generated/i18n/client-loaders/{name}.ts`
6. **Generates** manifest: `src/_generated/i18n/manifest.json`

Run codegen after adding/changing any `t()` call, or the Babel plugin won't find the translation key at runtime.

### Babel Plugin (`tooling/i18n-babel-plugin/`)

Runs at compile time (both dev and build). Transforms:

- `t({en, zh})` → `__i18n_lookup(key)` (server) or `useI18nLookup(key)` (client)
- `t({en, zh}, { parse: true })` → `__i18n_lookupParse(key)` or `useI18nLookupParse(key)`
- Auto-injects `setLocale` for page files with `t()` calls
- Auto-wraps returns with `<ClientTranslationsProvider>` for manifest entries

## Common Patterns

### Adding Translations to a New Page

```tsx
// src/app/[locale]/my-page/page.tsx
import { t } from "#src/i18n.ts";

export default function Page() {
  return (
    <div>
      <h1>{t({ en: "My Page", zh: "我的页面" })}</h1>
      <p>{t({ en: "Some content", zh: "一些内容" })}</p>
    </div>
  );
}
```

Then run `pnpm codegen:i18n` to regenerate bundles.

### Adding Translations to a Client Component

```tsx
// src/components/my-component.tsx
"use client";

import { t } from "#src/i18n.ts";

export function MyComponent() {
  return <span>{t({ en: "Click me", zh: "点击我" })}</span>;
}
```

The parent page/layout must be in the manifest for client translations to work. Run `pnpm codegen:i18n` — the codegen traces imports and auto-generates the client bundle.

### Rich Text with Markup

```tsx
{
  t(
    {
      en: "Read our <strong>terms of service</strong>",
      zh: "阅读我们的<strong>服务条款</strong>",
    },
    { parse: true },
  );
}
```

## Common Mistakes

- Using variables or template literals in `t()` — values must be string literals
- Forgetting to run `pnpm codegen:i18n` after adding new `t()` calls
- Manually adding `setLocale` to page files — the Babel plugin does this automatically
- Creating separate `translations.json` files — translations live inline in the component
- Using `getTranslations()` or `useTranslations()` — these no longer exist; use `t()` everywhere
