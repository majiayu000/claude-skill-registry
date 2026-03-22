---
name: i18n-translate
description: >
  Translate Camunda Modeler i18n plugin keys into a target language, using the German translation as the
  authoritative base. Use this skill whenever the user wants to add a new language, translate keys,
  fill in missing translations for an existing language, or update/complete a partial translation in the
  camunda-modeler-i18n-plugin repository. Also trigger when the user mentions locale codes, language names,
  or talks about translating the modeler UI.
---

# i18n Translation Skill

Translate Camunda Modeler i18n plugin UI strings into a target language. The German (de) translation is
the most complete and serves as the authoritative source for all keys and their meaning.

## When to use

- Adding a brand-new language to the plugin
- Filling gaps in an existing language (keys present in German but missing in the target)
- Regenerating or replacing an entire language's translations

## Inputs

The user provides:
- **Target language** — a language name (e.g. "Spanish", "Italian") or locale code (e.g. "es", "ja")

## Workflow

### Step 1: Determine locale code and label

Map the user's input to:
- A **locale code** for file/folder naming (e.g. `es`, `ja`, `ko`). Use the same conventions as existing
  locales in the project — lowercase, hyphens for regional variants (e.g. `pt-br`, `zh-Hans`).
- A **variable-safe key** for use in JS imports (replace `-` with `_`, e.g. `pt_br`, `zh_Hans`).
- A **display label** in the target language's native script (e.g. "Español", "日本語").

Confirm the locale code, JS key, and display label with the user before proceeding.

### Step 2: Read the German base files

Read all four German translation source files to get the complete set of keys:

```
client/bpmnjs-i18n-extension/languages/de/bpmn-js.js
client/bpmnjs-i18n-extension/languages/de/dmn-js.js
client/bpmnjs-i18n-extension/languages/de/properties-panel.js
client/bpmnjs-i18n-extension/languages/de/other.js
```

Each file exports a default object of `{ 'English key': 'German translation' }` pairs.

### Step 3: Determine which keys need translation

- **New language**: All keys from all four German files need translation.
- **Existing language**: Read the target language's files, diff against the German files, and identify
  missing keys. Only translate the missing ones — do not overwrite existing translations.

### Step 4: Translate

For each key that needs translation, translate the **German value** into the target language.

Translation rules:
- The **object keys** (left side) are English strings used as lookup identifiers by the modeler runtime.
  **Never modify the keys.** Only translate the values (right side).
- Preserve `{parameter}` placeholders exactly as they appear (e.g. `{element}`, `{count}`, `{semantic}`).
- Keep technical terms that are industry-standard and not typically translated:
  BPMN, DMN, FEEL, CMMN, PMML, Gateway, Pool, Lane, Token, ID, XML, JSON, ISO 8601, EL, JUEL, Groovy,
  JRuby, Python, Java, JavaScript, Zeebe, Camunda, UTC, QName.
- For BPMN/DMN domain terms (e.g. "Boundary Event", "Intermediate Catch Event", "Decision Table",
  "Hit Policy"), use the established translations for that language if they exist in the BPMN/DMN
  community. If unsure, keep the English term and add the translation in parentheses.
- Preserve trailing/leading spaces if the German value has them — they are intentional for UI concatenation.
- Match the casing style of the German translations (e.g. if German capitalizes the first word only,
  do the same in the target language, respecting that language's conventions).
- Strings like `'-'`, `'BPMN'`, `'DMN'`, `'ID'`, `'FEEL'`, `'Foo'` that are identical in German and
  English should remain identical in the target language too.

Translate in batches per file. After each file, briefly summarize the count of translated keys.

### Step 5: Write the translation files

Each of the four files must follow this exact format. See [references/file-template.md](references/file-template.md) for the full template.

Key points:
- Include the Apache 2.0 license header (Copyright 2025 Miragon GmbH)
- Use `export default { ... };` syntax
- Keep keys in the same order as the German source file
- One key-value pair per line, single-quoted strings, trailing comma on each entry

For **existing languages** where you are filling gaps: insert the new keys at the position matching
their order in the German file, so the file stays consistently ordered.

### Step 6: Write the barrel file

Create or verify the barrel file at `client/bpmnjs-i18n-extension/languages/<locale>.js`:

```javascript
import bpmnJs from './<locale>/bpmn-js';
import dmnJs from './<locale>/dmn-js';
import propertiesPanel from './<locale>/properties-panel';
import other from './<locale>/other';

export default {
    ...bpmnJs,
    ...dmnJs,
    ...propertiesPanel,
    ...other
};
```

Include the license header. Match the exact style of `de.js`.

### Step 7: Register the language (new languages only)

Skip this step if the language already exists in the plugin.

1. **`client/bpmnjs-i18n-extension/translate.js`** — Add an import for the new locale and include it
   in the `languages` object. Place the import alphabetically among existing imports.

2. **`client/config/I18nPlugin.js`** — Add a new entry to the `options` array with the locale's JS key
   as `value` and the native display label as `label`. Place it alphabetically by label.

### Step 8: Summary

After all files are written, output a summary:
- Language added/updated: name and locale code
- Files created or modified (with paths)
- Total keys translated
- Reminder to run `npm run build` and test in the modeler
