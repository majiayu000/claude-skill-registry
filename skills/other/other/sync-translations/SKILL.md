---
name: sync-translations
description: Keeps all translation files in messages/ in sync. Use this skill whenever new UI text is added to the codebase, a translation key is missing in one language, or the wording of an existing translation changes. Detects missing keys, stale translations, and structural drift between language files.
---

Synchronize all translation files in `messages/` so every language contains the same keys with correct, natural translations.

## Project i18n Setup

- **Library:** `next-intl`
- **Source of truth for structure:** `messages/de.json` (German, default locale)
- **All locales:** defined in `src/i18n/config.ts` → currently `['de', 'en']`
- **Message files:** `messages/<locale>.json` — one per locale, flat namespace objects
- **Usage in code:** `useTranslations('<namespace>')` / `getTranslations('<namespace>')`, then `t('key')`

## Your Task

When invoked, work through the following steps in order.

---

### Step 1 — Read everything relevant

1. Read `src/i18n/config.ts` to get the current list of locales.
2. Read every file in `messages/` (one per locale).
3. Scan the entire `src/` directory for translation key usage:
   - Find all `useTranslations('namespace')` and `getTranslations('namespace')` calls
   - Find all `t('key')`, `t('namespace.key')`, and `t('key', {...})` call patterns
   - Focus on `.tsx`, `.ts` files under `src/`

---

### Step 2 — Identify what needs to change

Check for **four types of issues**:

#### A) Missing keys
A key exists in one language file but not in another.
- **Reference language:** `de.json` (German is the source of truth for structure)
- List every key path (e.g. `dashboard.noTransactions`) that is present in `de.json` but absent from another locale.
- Also check the reverse: keys in non-German files that don't exist in `de.json` are orphaned and should be noted but NOT automatically deleted — report them for manual review.

#### B) Keys used in code but missing from ALL message files
A `t('key')` call references a key that doesn't exist in any `messages/` file.
- These are newly added UI strings that haven't been translated yet.
- They need to be added to every locale.

#### C) Structural drift
The JSON structure (nesting, namespace names) differs between files.
- Example: `de.json` has `{ "expenses": { "title": "..." } }` but `en.json` has `"expensesTitle": "..."` at the top level.
- Flag these — do not silently restructure without reporting.

#### D) Explicitly changed wording (only when invoked after a specific change)
If the user describes a text change (e.g. "I updated the label for X"), identify the affected key and update all other locales to match the new meaning.

---

### Step 3 — Plan before editing

Write out a concise change plan before touching any file. Group by locale and type:

```
de.json  — no changes needed (reference)
en.json  — ADD 3 keys:
             expenses.filterByCategory  (missing)
             analytics.forecastTitle    (missing)
             settings.resetConfirm      (missing)
         — NOTE: orphaned key 'dashboard.chartPlaceholder' exists only in en.json
```

If no changes are needed, state that clearly and stop.

---

### Step 4 — Edit the message files

Apply every planned addition or correction.

**Translation quality rules:**
- Translations must be natural, idiomatic, and context-aware — not word-for-word.
- **German (de):** formal enough for a finance app, but approachable. Use "du" forms unless the existing file uses "Sie". Check the existing tone before adding new strings.
- **English (en):** concise, professional. Match the register of existing English strings.
- For financial/accounting terms use the standard terminology of the target language (e.g. "Girokonto" not "Gehaltskonto", "Savings Account" not "Saving Account").
- Preserve all interpolation placeholders exactly: `{count}`, `{name}`, `{amount}` must appear unchanged in every locale.
- Preserve ICU message syntax for plurals and selects if used.
- Keep key order inside each namespace consistent with `de.json` — new keys go at the bottom of their namespace.

**File format rules:**
- Valid JSON only — no trailing commas, no comments.
- Same indentation as the existing file (2 spaces).
- Do not reformat or reorder existing keys — only add or correct.

---

### Step 5 — Check for new locales

After syncing, re-read `src/i18n/config.ts`. If a new locale was added that has no file in `messages/` yet, create the full `messages/<locale>.json` by translating every key from `de.json`. Apply the same translation quality rules.

---

### Step 6 — Verify

After all edits, confirm:

- [ ] Every key present in `de.json` exists in all other locale files
- [ ] No interpolation placeholder (`{...}`) is missing or renamed in any translation
- [ ] All files are valid JSON (balanced braces, no trailing commas)
- [ ] No key used in `src/` code is missing from any `messages/` file
- [ ] No existing key was accidentally deleted or reordered

Report the checklist result. List any orphaned keys (present in non-German files but not in `de.json`) separately as items for manual review — do not delete them automatically.
