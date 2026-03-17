---
name: react-native-i18n-workflow
description: Manages internationalization strings and translation workflows using i18next and react-i18next. Use when adding new text, supporting additional languages, or implementing pluralization and interpolation in Fitness Tracker App.
---

# React Native i18n Workflow

This skill handles the internationalization (i18n) workflow for the Fitness Tracker App, ensuring type-safe translations and consistent language support.

## When to Use This Skill

Use this skill when you need to:
- Add new translatable strings to the app
- Support a new language
- Implement interpolation (e.g., "Hello {{name}}!")
- Use pluralization in translations
- Handle RTL (Right-to-Left) language detection and layout
- Ensure type safety for translation keys

## Translation Files

Translations are stored in `app/i18n/` with one file per language (e.g., `en.ts`, `ja.ts`).

### English (Source) Pattern
```typescript
// app/i18n/en.ts
const en = {
  common: {
    ok: "OK!",
    cancel: "Cancel",
  },
  homeScreen: {
    title: "My Collection",
    deleteAlertMessage: "Delete this {{category}} workout?",
  }
}
export default en
export type Translations = typeof en
```

## Using Translations

### 1. The `translate` Helper
Use the standalone `translate` function for non-component logic:
```typescript
import { translate } from "@/i18n"

const title = translate("homeScreen:title")
const message = translate("homeScreen:deleteAlertMessage", { category: "cat" })
```

### 2. The `tx` Prop
Many components support a `tx` prop for automatic translation:
```tsx
<Text tx="homeScreen:title" preset="heading" />
<Button tx="common:ok" onPress={handlePress} />
```

### 3. The `useTranslation` Hook
For complex cases or dynamic content:
```tsx
import { useTranslation } from "react-i18next"

const { t } = useTranslation()
return <Text>{t("homeScreen:title")}</Text>
```

## Advanced Patterns

### Interpolation
Keys: `greeting: "Hello, {{name}}!"`
Usage: `translate("greeting", { name: "Mirza" })`

### Pluralization
Keys: 
`pet_one: "{{count}} pet"`
`pet_other: "{{count}} pets"`
Usage: `translate("pet", { count: 5 })`

### Key Path Types
We use `TxKeyPath` to ensure keys exist at compile time.
Format: `section:key` for top level, `section:nested.key` for deeper levels.

## References

See [TRANSLATION_STRUCTURE.md](references/TRANSLATION_STRUCTURE.md) for detailed file patterns.

See [I18N_BEST_PRACTICES.md](references/I18N_BEST_PRACTICES.md) for naming conventions and workflow steps.
