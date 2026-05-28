---
name: localize
description: "Run the localization workflow: extract strings, validate localization readiness, check for hardcoded text, and generate translation-ready string tables."
argument-hint: "[scan|extract|validate|status]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
---
When this skill is invoked:

1. **Parse the subcommand** from the argument:
   - `scan` — Scan for localization issues (hardcoded strings, missing keys)
   - `extract` — Extract new strings and generate/update string tables
   - `validate` — Validate existing translations for completeness and format
   - `status` — Report overall localization status

2. **For `scan`**:
   - Search `src/` for hardcoded user-facing strings:
     - String literals in UI code that are not wrapped in a localization function
     - Concatenated strings that should be parameterized
     - Strings with positional placeholders (`%s`, `%d`) instead of named ones (`{playerName}`)
   - Search for localization anti-patterns:
     - Date/time formatting not using locale-aware functions
     - Number formatting without locale awareness
     - Text embedded in images or textures (flag asset files)
     - Strings that assume left-to-right text direction
   - Report all findings with file paths and line numbers

3. **For `extract`**:
   - Scan all source files for localized string references
   - Compare against the existing string table (if any) in `assets/data/`
   - Generate new entries for strings that don't have keys yet
   - Suggest key names following the convention: `[category].[subcategory].[description]`
   - Output a diff of new strings to add to the string table

4. **For `validate`**:
   - Read all string table files in `assets/data/`
   - Check each entry for:
     - Missing translations (key exists but no translation for a locale)
     - Placeholder mismatches (source has `{name}` but translation is missing it)
     - String length violations (exceeds character limits for UI elements)
     - Orphaned keys (translation exists but nothing references the key in code)
   - Report validation results grouped by locale and severity

5. **For `status`**:
   - Count total localizable strings
   - Per locale: count translated, untranslated, and stale (source changed since translation)
   - Generate a coverage matrix:

   ```markdown
   ## Localization Status
   Generated: [Date]

   | Locale | Total | Translated | Missing | Stale | Coverage |
   |--------|-------|-----------|---------|-------|----------|
   | en (source) | [N] | [N] | 0 | 0 | 100% |
   | [locale] | [N] | [N] | [N] | [N] | [X]% |

   ### Issues
   - [N] hardcoded strings found in source code
   - [N] strings exceeding character limits
   - [N] placeholder mismatches
   - [N] orphaned keys (can be cleaned up)
   ```

### Rules
- English (en) is always the source locale
- Every string table entry must include a translator comment explaining context
- Never modify translation files directly — generate diffs for review
- Character limits must be defined per-UI-element and enforced automatically
- Right-to-left (RTL) language support should be considered from the start, not bolted on later
