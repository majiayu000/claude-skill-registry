---
name: shopify-app-i18n
description: Guide for adding Multi-language support to Shopify Apps using i18next. Covers setup, localization files, and Admin context.
---

# Internationalization (i18n) for Shopify Apps

Shopify merchants exist globally. Your app MUST support multiple languages to be featured or widely adopted.

## 1. Stack
- **Library**: `i18next` (Standard)
- **React**: `react-i18next`
- **Remix**: `remix-i18next`

## 2. Setup

### Installation
```bash
npm install i18next react-i18next remix-i18next i18next-fs-backend i18next-http-backend
```

### Configuration (`app/i18n.server.ts`)
Create a server-side instance to detect language.

```typescript
import { RemixI18Next } from "remix-i18next/server";
import { createInstance } from "i18next";
import i18n from "~/i18n"; // client config
import { resolve } from "node:path";

export const i18nServer = new RemixI18Next({
  detection: {
    supportedLanguages: i18n.supportedLngs,
    fallbackLanguage: i18n.fallbackLng,
  },
  // This is the configuration for i18next
  i18next: {
    ...i18n,
    backend: {
      loadPath: resolve("./public/locales/{{lng}}/{{ns}}.json"),
    },
  },
});
```

### Root Loader (`app/root.tsx`)
Inject the locale into the document.

```typescript
export async function loader({ request }: LoaderFunctionArgs) {
  const locale = await i18nServer.getLocale(request);
  return json({ locale });
}

export const handle = {
  // In the handle export, we can add a reference to a translation namespace
  // This will load the translations for this namespace for this route
  i18n: "common",
};

export default function App() {
  const { locale } = useLoaderData<typeof loader>();
  useChangeLanguage(locale); // Syncs remix locale with i18next
  
  return (
    <html lang={locale} dir={i18n.dir(locale)}>
      {/* ... */}
    </html>
  );
}
```

## 3. Translation Files
Store JSON files in `public/locales`.

```
public/
  locales/
    en/
      common.json
    fr/
      common.json
    vi/
      common.json
```

**Example `common.json`**:
```json
{
  "welcome": "Welcome to my app",
  "dashboard": {
    "title": "Dashboard",
    "stats": "Statistics"
  }
}
```

## 4. Usage in Components

```typescript
import { useTranslation } from "react-i18next";

export function DashboardHeader() {
  const { t } = useTranslation("common");

  return (
    <Page title={t("dashboard.title")}>
      <p>{t("welcome")}</p>
    </Page>
  );
}
```

## 5. Detecting Shopify Admin Language
Shopify passes the locale in the URL query params (`?locale=fr-FR`) or you can fetch it from the GraphQL Admin API (`Shop.billingAddress.country` or similar, though strictly speaking the Admin UI language is preferred).

Typically, `remix-i18next` detection handles the request headers/query params automatically if configured correctly.

## 6. Translating App Extensions
For Theme App Extensions or Checkout UI Extensions, they have their *own* `locales` folder in their directory. They do NOT share the Remix app's locales.
- **Theme Extension**: `extensions/my-ext/locales/en.default.json`
- **Checkout UI**: `extensions/checkout-ui/locales/en.json`
