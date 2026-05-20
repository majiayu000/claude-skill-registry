---
name: translate
description: Translates untranslated strings in a locale JSON file for the Oinkoin app. Use when the user wants to localise or update translations for a specific language, or says "translate <locale>".
argument-hint: "[locale-file]"
---

# Skill: translate

Translate untranslated strings in a locale JSON file for the Oinkoin app.

## Usage
```
/translate <locale-file>
```
Example: `/translate assets/locales/it.json`

If no file is specified, address all the locale files

---

## How translations work in this project

- All locale files live in `assets/locales/` (e.g. `it.json`, `de.json`, `pt-BR.json`).
- `assets/locales/en-US.json` is the **source of truth**: every key AND its English value are listed there.
- Every other locale file has the **same keys**. A string is **untranslated** when its value is identical to its key (i.e. it was never localised and still reads in English).
- A string is **already translated** when its value differs from its key. **Never touch those.**

## Step-by-step instructions

### 0. Sync keys with the codebase (always run first)
Run the sync script from the project root to ensure `en-US.json` is up-to-date and stale keys are removed from all locale files:
```
python3 scripts/update_en_strings.py
```
This regenerates `en-US.json` from all `.i18n` strings found in `lib/`, and removes obsolete keys from every other locale file. Run it before translating so you are working against the current set of keys.

### 1. Read the target locale file
Read the full file specified by the user.

### 2. Identify untranslated strings
A string is untranslated when `value == key`. Collect every such entry.

If there are no untranslated strings, tell the user and stop.

### 3. For each untranslated string — look up context before translating
Do **not** guess from the key text alone. For each untranslated key:

- Search the Dart source code (Grep in `lib/`) for the exact key string to find where it is used.
- Look at the surrounding widget/function/page to understand the context (e.g. is it a button label, a dialog title, an error message, a settings toggle description?).
- Only then choose the most natural, contextually appropriate translation for the target language.

### 4. Write the translated strings
Edit the locale file, replacing only the untranslated values. Keep every other entry byte-for-byte identical.

### 5. Report what changed
After editing, print a compact table of the strings you translated:

| Key | Translation |
|-----|-------------|
| … | … |

---

## Important rules

- **Never modify already-translated strings** (value ≠ key).
- **Never change keys** — only values.
- Preserve placeholders exactly as written: `%s`, `%d`, `%1$s`, etc.
- Match the tone and terminology of the strings that ARE already translated in the same file — consistency matters more than literal accuracy.
- For technical or brand terms (e.g. "Oinkoin Pro", "PIN", "CSV", "JSON") keep them untranslated.
- If a string has no natural translation (e.g. it is already the correct word in the target language), it is fine to leave the value equal to the key — but note this in your report.
- Process the **whole file** in one pass; do not ask for confirmation before each string.

## Exceptions

For British english use en-GB.json - in this case, key and value will most of case matches. Consider all the strings as already translated and skip it.
