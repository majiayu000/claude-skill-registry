---
name: i18n
description: Internationalization management tool for syncing and translating language files
---

# I18n Management Skill

Manage multilingual content in the `translations/` directory. This skill provides tools to synchronize language files with the English reference and assist with translations.

## Overview

This project uses `next-intl` for internationalization with JSON message files organized in `translations/`:

```
translations/
├── en/                    # English (source of truth)
│   ├── index.ts           # Main export file
│   ├── shared.json
│   ├── components.json
│   └── pages/
│       ├── home.json
│       ├── manifesto.json
│       ├── docs.json
│       ├── articles.json
│       ├── curated-collections.json
│       ├── stacks.json
│       ├── comparison.json
│       ├── landscape.json
│       ├── open-source-rank.json
│       └── search.json
├── de/                    # German
├── es/                    # Spanish
├── fr/                    # French
├── id/                    # Indonesian
├── ja/                    # Japanese
├── ko/                    # Korean
├── pt/                    # Portuguese
├── ru/                    # Russian
├── tr/                    # Turkish
├── zh-Hans/               # Simplified Chinese
└── zh-Hant/               # Traditional Chinese
```

**Important:** Each locale must maintain the exact same file structure and JSON key order as `en/`.

## I18n Architecture

The project has **two separate internationalization systems** that share the same 12 locale configuration:

### 1. UI Translation System (next-intl)
- **Purpose:** Translates static UI strings (buttons, labels, page content, etc.)
- **Location:** `translations/{locale}/*.json`
- **Usage:** Via `useTranslations()` hook or `getTranslations()` server function
- **Managed by:** This skill's sync and translate commands

### 2. Manifest Translation System
- **Purpose:** Translates manifest data (IDEs, CLIs, models, providers, etc.)
- **Location:** `manifests/**/*.json` (in each manifest file's `translations` field)
- **Usage:** Via `localizeManifestItem()` and `localizeManifestItems()` functions
- **Managed by:** Manual editing of manifest files or manifest automation tools

**This skill manages only the UI Translation System.** For manifest translations, edit the manifest JSON files directly or use the manifest-automation skill.

## Enabled Locales

Currently enabled locales in `src/i18n/config.ts`:
- `en` - English (source of truth)
- `de` - Deutsch (German)
- `es` - Español (Spanish)
- `fr` - Français (French)
- `id` - Bahasa Indonesia (Indonesian)
- `ja` - 日本語 (Japanese)
- `ko` - 한국어 (Korean)
- `pt` - Português (Portuguese)
- `ru` - Русский (Russian)
- `tr` - Türkçe (Turkish)
- `zh-Hans` - 简体中文 (Simplified Chinese)
- `zh-Hant` - 繁體中文 (Traditional Chinese)

All 12 locales are fully enabled and must be maintained in sync.

## Subcommands

### `sync`

Synchronize all enabled locale directories with `en/` as the source of truth.

**What it does:**

- Scans all locale directories in `translations/` that are enabled in config
- Compares each JSON file's keys with the corresponding English file
- **Adds missing keys** with English text as placeholder (needs translation)
- **Removes extra keys** not present in English files
- **Preserves JSON structure, key order, and formatting** (2-space indentation)
- **Keeps the `index.ts` file structure** for each locale

**Usage:**

When you need to sync language files, use this command in Claude Code:

```
Please run the i18n sync command
```

Claude Code will execute:

```bash
node .claude/skills/i18n/scripts/sync.mjs
```

**Output Example:**

```
🔄 Syncing translation files with en/...

✓ Synced de/
  + Added 3 keys in components.json
  + Added 5 keys in pages/home.json
  - Removed 1 key in shared.json

✓ Synced zh-Hans/
  + Added 8 keys in pages/stacks.json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Sync complete!
  Modified: 2 locales
  Added: 16 keys
  Removed: 1 key
```

**When to use:**

- After adding new keys to any English JSON file
- After removing obsolete keys from any English JSON file
- After adding new JSON files to the English structure
- Before starting translation work (ensures all keys exist)
- When adding a new locale

---

### `translate <locale>`

Generate translation tasks for Claude Code to translate missing content.

**What it does:**

- Reads all JSON files from `en/` and `<locale>/`
- Identifies keys that need translation (currently in English or missing)
- Outputs a structured translation task with guidelines
- Provides context and instructions for accurate translation

**Usage:**

When you need to translate content, use this command in Claude Code:

```
Please run the i18n translate command for ja
```

Claude Code will execute:

```bash
node .claude/skills/i18n/scripts/translate.mjs ja
```

**Workflow:**

1. The script outputs content that needs translation in JSON format
2. Claude Code reads the guidelines and translates the content
3. You provide the translated JSON back
4. Claude Code updates the locale JSON files

**Translation Guidelines (automatically enforced):**

✓ **Preserve brand names:** `AI Coding Stack`, `Claude Code`, etc.
✓ **Keep placeholders intact:** `{count}`, `{name}`, `${variable}`
✓ **Don't translate URLs:** `https://example.com`
✓ **Don't translate file paths:** `/path/to/file`
✓ **Maintain terminology consistency** throughout the translation
✓ **Preserve reference syntax:** `@:path.to.key` for internal references

**Output Example:**

```
🌐 Translation Assistant for ja

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Translation Task
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target Language: 日本語 (Japanese)
Entries to translate: 15

Files affected:
  - components.json: 5 entries
  - pages/home.json: 8 entries
  - shared.json: 2 entries

⚠ Translation Guidelines:
  1. Preserve brand names: "AI Coding Stack", "Claude Code"
  2. Keep placeholders intact: {count}, {name}, ${variable}
  3. Don't translate URLs and file paths
  4. Maintain consistent terminology
  5. Preserve reference syntax: @:path.to.key

Content to translate:

```json
{
  "components.languageSwitcher.english": "English",
  "pages.home.hero.title": "Welcome to AI Coding Stack",
  "shared.navigation.docs": "Documentation",
  ...
}
```
```

---

## File Structure

```
.claude/skills/i18n/
├── SKILL.md              # This documentation
└── scripts/
    ├── sync.mjs          # Synchronization script
    └── translate.mjs     # Translation assistant script
```

## Technical Details

**Language:** Node.js (ES Modules)
**Dependencies:** Built-in Node.js modules only (`fs`, `path`)
**JSON Format:** 2-space indentation, trailing newline
**Encoding:** UTF-8

### Translation File Structure

Each locale has:
1. **JSON files**: Contain the actual message data
2. **index.ts**: Imports and assembles messages

```typescript
// translations/en/index.ts
import components from './components.json'
import articles from './pages/articles.json'
import comparison from './pages/comparison.json'
import curatedCollections from './pages/curated-collections.json'
import docs from './pages/docs.json'
import home from './pages/home.json'
import landscape from './pages/landscape.json'
import manifesto from './pages/manifesto.json'
import openSourceRank from './pages/open-source-rank.json'
import search from './pages/search.json'
import stacks from './pages/stacks.json'
import shared from './shared.json'

const messages = {
  shared,
  components,
  pages: {
    home,
    manifesto,
    docs,
    articles,
    curatedCollections,
    stacks,
    comparison,
    landscape,
    openSourceRank,
    search,
  },
}

export default messages
```

### How Keys Are Compared

The scripts use recursive traversal to handle nested JSON structures. Keys are compared using dot notation:

```json
{
  "pages": {
    "home": {
      "hero": {
        "title": "Welcome"
      }
    }
  }
}
```

Becomes: `pages.home.hero.title = "Welcome"`

### Adding a New Language

**Note:** The project currently supports 12 locales. To add a new locale (e.g., Italian 'it'):

1. Add the locale to `src/i18n/config.ts`:

```typescript
export const locales = [
  'en', 'de', 'es', 'fr', 'id', 'ja', 'ko', 'pt', 'ru', 'tr', 'zh-Hans', 'zh-Hant',
  'it'  // Add new locale
] as const;
```

2. Update locale names:

```typescript
export const localeNames: Record<Locale, string> = {
  // ... existing locales
  it: 'Italiano',
}

export const localeToOgLocale: Record<Locale, string> = {
  // ... existing locales
  it: 'it_IT',
}
```

3. Add to translate.mjs LOCALE_NAMES (`.claude/skills/i18n/scripts/translate.mjs`):

```javascript
const LOCALE_NAMES = {
  // ... existing locales
  it: 'Italiano (Italian)',
}
```

4. Create the locale directory structure:

```bash
mkdir -p translations/it/pages
cp translations/en/index.ts translations/it/index.ts
cp translations/en/*.json translations/it/
cp translations/en/pages/*.json translations/it/pages/
```

5. Run sync to ensure structure matches:

```
Please run the i18n sync command
```

6. Run translate to generate translation tasks:

```
Please run the i18n translate command for it
```

## Best Practices

1. **Always run `sync` before `translate`** to ensure all keys exist
2. **Make changes to English files first**, then sync other locales
3. **Review translations** for context accuracy, especially technical terms
4. **Use Git** to track changes and review diffs before committing
5. **Keep brand names consistent** across all languages
6. **Test translations** in the actual UI to verify formatting and length
7. **Preserve key order** to make diffs easier to review
8. **Use reference syntax** (`@:path.to.key`) for reused content

## Troubleshooting

**Problem:** Script says "directory not found"

- **Solution:** Ensure you're running from project root
- Check that `translations/` directory exists

**Problem:** Keys are out of sync after adding new content

- **Solution:** Run `sync` command to update all locale files

**Problem:** Translation contains placeholders like `{0}` instead of `{count}`

- **Solution:** Verify the English source uses named placeholders, re-translate

**Problem:** Some text appears in English in the translated app

- **Solution:** Run `translate` to find missing translations, check for English fallbacks

**Problem:** index.ts imports are wrong after sync

- **Solution:** The sync script preserves index.ts structure; manually check imports match actual JSON files

## Integration with next-intl

This skill is designed to work with the project's `next-intl` setup:

```typescript
// src/i18n/request.ts
const rawMessages = (await import(`../../translations/${locale}/index.ts`)).default
const messages = resolveReferences(rawMessages)
```

The JSON files are loaded through the index.ts for each locale, and the `resolveReferences` function handles reference syntax.

### Reference Resolution

The project supports **reference syntax** for reusing translations:

**Basic Reference:** `@:path.to.key`
```json
{
  "shared": {
    "appName": "AI Coding Stack",
    "welcome": "Welcome to @:shared.appName"
  }
}
// Result: "Welcome to AI Coding Stack"
```

**Reference with Modifiers:** `@.modifier:path.to.key`

Supported modifiers:
- `@.upper:path` - Convert to UPPERCASE
- `@.lower:path` - Convert to lowercase
- `@.capitalize:path` - Capitalize first letter

```json
{
  "terms": {
    "documentation": "documentation",
    "title": "@.capitalize:terms.documentation Guide"
  }
}
// Result: "Documentation Guide"
```

**Important:**
- References are resolved at runtime by `src/i18n/lib-core.ts`
- Circular references are detected and will throw an error
- References can be nested (references within references)
- Keep reference syntax intact during translation

## License

This skill is part of the AI Coding Stack project and follows the project's Apache 2.0 license.
