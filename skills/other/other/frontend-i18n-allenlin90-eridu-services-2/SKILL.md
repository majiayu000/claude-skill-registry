---
name: frontend-i18n
description: Provides guidelines for implementing internationalization (i18n) in frontend applications using Paraglide JS and the shared @eridu/i18n package.
---

# Frontend i18n Pattern

This skill outlines the standard pattern for implementing internationalization in Eridu frontend applications. We use [Paraglide JS](https://inlang.com/m/gerre34r/library-inlang-paraglideJs) for type-safe, lightweight i18n.

## Architecture

- **Tooling**: `@inlang/paraglide-js` (v2+)
- **Configuration**: Defined in `project.inlang` at the app root.
- **Message Storage**: JSON files in `src/i18n/messages/{lang}.json`.
- **Output**: Generated code in `src/paraglide` (typically gitignored).
- **Shared Library**: `@eridu/i18n` (workspace package) for common translations and locale definitions.

## Workflow: Adding Translations

1.  **Locate the Message File**: Open `src/i18n/messages/en.json` (English is the source language).
2.  **Add Your Key**: Add a new key-value pair. You can nest keys for better organization.
    ```json
    {
      "dashboard": {
        "title": "My Dashboard",
        "welcomeUser": "Welcome back, {name}!"
      }
    }
    ```
3.  **Automatic Compilation**: If the dev server (`pnpm dev`) is running, Paraglide will automatically detect changes and regenerate `src/paraglide`.
4.  **Use in Component**: Import the messages and use them.

## Usage in Components

### 1. App-Specific Messages

Import from the generated local alias (usually configured as `@/paraglide/messages`).

```tsx
import * as m from '@/paraglide/messages';

export function Dashboard({ userName }) {
  // Simple message
  const title = m['dashboard.title'](); 

  // Message with parameters
  const welcome = m['dashboard.welcomeUser']({ name: userName });

  return (
    <div>
      <h1>{title}</h1>
      <p>{welcome}</p>
    </div>
  );
}
```

> **Note**: Because we use nested keys in JSON (e.g. `dashboard.title`), Paraglide exports them with the exact path as the name. Since these contain dots, you must use bracket notation: `m['dashboard.title']()`.

### 2. Shared Messages

For common terms (Save, Cancel, Table headers, etc.), use the shared `@eridu/i18n` package to ensure consistency.

```tsx
import * as sharedM from '@eridu/i18n';

// Usage
<Button>{sharedM['common.save']()}</Button>
<Button>{sharedM['common.cancel']()}</Button>
```

### 3. Locale Management

Use the `LocaleEnum` and helper functions from `@eridu/i18n` when dealing with locale logic (e.g., language switchers).

```tsx
import { LocaleEnum, LOCALE_LABELS } from '@eridu/i18n';

// Access available locales and their labels
{Object.entries(LOCALE_LABELS).map(([code, label]) => (
  <option key={code} value={code}>{label}</option>
))}
```

## Best Practices

1.  **Grouping**: Group messages by feature or page (e.g., `admin`, `auth`, `settings`).
2.  **Naming**: Use `camelCase` for keys (e.g., `welcomeUser` not `welcome-user`).
3.  **Parameters**: Use named parameters `{param}` instead of positional arguments.
4.  **No Hardcoding**: Never hardcode user-facing strings in components. Always extract them to `en.json`.
5.  **Review Shared**: Before adding a generic term like "Submit" or "Error", check `packages/i18n/messages/en.json` to see if it already exists in the shared library.

## Troubleshooting

-   **"Property '...' does not exist on type..."**: Run `pnpm dev` or `pnpm build` to force regeneration of the Paraglide files.
-   **Missing Translations**: Ensure you've added the key to `en.json`. Other languages (e.g., `zh-TW`) can be filled in later or via translation tools.
