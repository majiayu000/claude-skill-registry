---
name: translations
description: Work with internationalization using next-intl and PO files. Use when handling translations, i18n, PO files, getExtracted, useExtracted, translating content, or when the user needs to add or modify translations.
---

# Internationalization (i18n) Workflow

## Overview

This project uses `next-intl` with PO file extraction. Translations are extracted from the codebase using `pnpm build`.

## Key Functions

- **Server Components**: Use `getExtracted` (no locale needed)
- **Client Components**: Use `useExtracted`
- **Metadata/Server Actions**: Use `getExtracted` with locale parameter

## Critical Rules

### 1. No Dynamic Values in Translation Keys

**IMPORTANT**: The `t` function from `getExtracted`/`useExtracted` does NOT support dynamic values.

```tsx
// BAD: Dynamic key - will NOT work
const category = getCategory();
t(category); // Error!
t(MYLABELS[category]);

// GOOD: String literals only
t("Arts courses");
t("Business courses");
t("Technology courses");
```

### 2. String Interpolation IS Supported

You CAN use string interpolation for dynamic values within translations:

```tsx
// GOOD: Interpolation with static key
t("Explore all {category} courses", { category: "arts" });
t("Welcome, {name}!", { name: user.name });
t("{count} items remaining", { count: 5 });
```

### 3. Don't Pass `t` Function Around

You can't pass the `t` function to other functions or components:

```tsx
// BAD: Passing t function
function myFunction(t, label) {
  return t(label);
}
myFunction(t, "Some label");

// GOOD: Call t directly
function myFunction(translatedLabel: string) {
  return translatedLabel;
}
myFunction(t("Some label"));
```

### 4. Locale Parameter Rules

```tsx
// Server Component - no locale needed
const t = await getExtracted();
t("Hello");

// generateMetadata - needs locale
export async function generateMetadata({ params }) {
  const { locale } = await params;
  const t = await getExtracted(locale);
  return { title: t("Page Title") };
}
```

## Workflow for Adding Translations

1. **Add translation call in code**:

   ```tsx
   const t = await getExtracted();
   return <h1>{t("New page title")}</h1>;
   ```

2. **Run build to extract translations**:

   ```bash
   pnpm build
   ```

   This updates PO files with new strings.

3. **Translate empty strings in PO files**:

   - Find PO files in `apps/{app}/src/i18n/locales/`
   - Fill in empty `msgstr` values

4. **Check for missing translations**:
   ```bash
   pnpm i18n:check
   ```

## Handling MISSING_TRANSLATION Errors

When you see a `MISSING_TRANSLATION` error:

1. Go to the relevant PO file
2. Find the empty `msgstr` for the string
3. Add the translation

```po
# Before
msgid "Welcome to Zoonk"
msgstr ""

# After
msgid "Welcome to Zoonk"
msgstr "Bem-vindo ao Zoonk"
```

**Never create new translations in PO files manually** - only extract them using `pnpm build`. If you're on an environment where you can't run `pnpm build`, just ignore this i18n step.

## Updating app-error.ts Files

When updating `app-error.ts` files:

1. Add the new error code
2. Update `error-messages.ts` to include the new error code
3. Run `pnpm build` to update PO files

## Common Patterns

### Conditional Text

```tsx
// Use separate translation keys
const status = isActive ? t("Active") : t("Inactive");
```

### Pluralization

```tsx
// Use interpolation with count
t("{count} item", { count: 1 }); // "1 item"
t("{count} items", { count: 5 }); // "5 items"
```

### Rich Text (with components)

```tsx
t.rich("Read our {link}", {
  link: (chunks) => <Link href="/terms">{chunks}</Link>,
});
```
