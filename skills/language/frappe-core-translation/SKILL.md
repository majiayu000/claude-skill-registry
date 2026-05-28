---
name: frappe-core-translation
description: >
  Use when implementing translations/i18n in Frappe v14-v16 apps.
  Covers _() in Python, __() in JavaScript, CSV translation files,
  bench commands, string extraction rules, lazy translation _lt(),
  PO/MO files [v15+], RTL support, and custom app translations.
  Prevents common mistakes with f-strings, concatenation, and template
  literals that break string extraction.
  Keywords: translation, i18n, _(), __(), _lt(), CSV, PO, gettext,
  bench get-untranslated, RTL, localization.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "3.0"
---

# Frappe Translation / i18n

> Deterministic patterns for translating Frappe apps across v14, v15, and v16.

---

## Quick Reference

| Task | Python | JavaScript |
|------|--------|------------|
| Translate string | `_("Hello")` | `__("Hello")` |
| With substitution | `_("Hello {0}").format(name)` | `__("Hello {0}", [name])` |
| With context | `_("Change", context="Coins")` | `__("Change", null, "Coins")` |
| Lazy (module-level) | `_lt("Pending")` [v15+] | N/A |
| Check RTL | `frappe.utils.is_rtl()` | `frappe.utils.is_rtl()` |

---

## Decision Tree

```
Need to translate a string?
├── In Python (.py)?
│   ├── Inside a function/method → _("text {0}").format(val)
│   ├── Module-level constant [v15+] → _lt("text")
│   └── Module-level constant [v14] → define inside function or use lazy
├── In JavaScript (.js)?
│   └── ALWAYS → __("text {0}", [val])
├── In Jinja template (.html)?
│   └── {{ _("text") }}
├── In Vue (.vue)?
│   └── __("text") in <script>, {{ __("text") }} in <template>
└── DocType label/description/option?
    └── Auto-extracted — no _() needed

Where do translations live?
├── v14 → apps/{app}/{app}/translations/{lang}.csv
├── v15+ → apps/{app}/{app}/locale/{lang}/LC_MESSAGES/{app}.po
└── User overrides → Translation DocType (highest priority)

Need to extract untranslated strings?
├── v14 → bench --site {site} get-untranslated {lang} {output}
└── v15+ → bench generate-pot-file --app {app}
```

---

## Translation Priority (Highest First)

| Priority | Source | Scope |
|----------|--------|-------|
| 1 | **Translation DocType** (user overrides) | Per-site |
| 2 | **MO files** (`locale/{lang}/.../{app}.mo`) | Per-app [v15+] |
| 3 | **CSV files** (`translations/{lang}.csv`) | Per-app |
| 4 | **Parent language** (e.g., `pt` for `pt-BR`) | Fallback |

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| `_()` / `__()` | Yes | Yes | Yes |
| `_lt()` lazy translation | No | Yes | Yes |
| CSV translations | Yes | Yes (legacy) | Yes (legacy) |
| PO/MO (gettext) | No | Yes | Yes |
| `bench generate-pot-file` | No | Yes | Yes |
| Babel JS extractor | No | Yes | Yes |
| Type hints on `_()` | No | No | Yes |

---

## Auto-Extracted Strings (No _() Needed)

These are extracted automatically by the framework:

- DocType **labels** and **descriptions**
- Select field **options** (each option line)
- Workflow **states** and **actions**
- Print Format **labels**
- Report **column labels**
- Notification **subjects** (not body)
- Dashboard chart **labels**

---

## String Extraction Rules

| File Type | Extractor | What It Finds |
|-----------|-----------|---------------|
| `.py` | Babel (AST) | `_("...")`, `_lt("...")` calls |
| `.js` | Babel tokenizer [v15+] / regex [v14] | `__("...")` calls |
| `.html` | Regex | `{{ _("...") }}` in Jinja |
| `.vue` | Same as JS | `__("...")` in script/template |
| `.json` | DocType parser | Labels, descriptions, options |

**CRITICAL**: Extractors work on the AST/tokens. They CANNOT extract dynamically constructed strings. See [Anti-Patterns](references/anti-patterns.md).

---

## Anti-Patterns (NEVER Do These)

| Pattern | Why It Breaks | Correct Form |
|---------|---------------|--------------|
| `_(f"Hello {name}")` | f-string not extractable | `_("Hello {0}").format(name)` |
| `_("Hello " + name)` | Concatenation fragments | `_("Hello {0}").format(name)` |
| `_("Welcome %s") % name` | Old-style not extractable | `_("Welcome {0}").format(name)` |
| `` __(`Hello ${name}`) `` | Template literal not extractable | `__("Hello {0}", [name])` |
| `_(" Hello ")` | Leading/trailing spaces trimmed | `_("Hello")` |
| `_("item" if x else "items")` | Ternary inside _() | `_("item") if x else _("items")` |
| `_(variable)` | Variable not extractable | `_("Known String")` |

> Full anti-pattern catalog with code examples: [references/anti-patterns.md](references/anti-patterns.md)

---

## CSV Translation File Format

**Location**: `apps/{app}/{app}/translations/{lang}.csv`

```csv
"source","translation","context"
"Hello","Hallo",""
"Change","Wisselgeld","Coins"
"Change","Wijziging","Amendment"
```

- ALWAYS use UTF-8 encoding (no BOM)
- ALWAYS quote all fields with double quotes
- Context column is optional but MUST be present (empty string if unused)
- No hooks registration needed — auto-discovered from `translations/` directory

---

## PO/MO Files [v15+]

**Location**: `apps/{app}/{app}/locale/{lang}/LC_MESSAGES/{app}.po`

```bash
# Generate POT template
bench generate-pot-file --app {app}

# Migrate existing CSV to PO
bench migrate-csv-to-po --app {app}

# Compile PO to MO (required for runtime)
bench compile-po-to-mo --app {app}
```

PO files follow standard GNU gettext format. Use any PO editor (Poedit, Weblate, Transifex).

---

## Bench Commands

| Command | Version | Purpose |
|---------|---------|---------|
| `bench --site {site} get-untranslated {lang} {output.csv}` | All | Export untranslated strings |
| `bench update-translations {lang} {untranslated.csv} {translated.csv}` | All | Import translations |
| `bench generate-pot-file --app {app}` | v15+ | Generate .pot template |
| `bench migrate-csv-to-po --app {app}` | v15+ | Convert CSV to PO format |
| `bench compile-po-to-mo --app {app}` | v15+ | Compile PO to binary MO |

---

## RTL Support

**Hardcoded RTL languages**: `ar` (Arabic), `he` (Hebrew), `fa` (Persian/Farsi), `ps` (Pashto)

```python
# Python
if frappe.utils.is_rtl():
    # Apply RTL-specific logic
```

```javascript
// JavaScript
if (frappe.utils.is_rtl()) {
    // Apply RTL-specific logic
}
```

- Frappe auto-applies `dir="rtl"` to the `<html>` element
- ALWAYS use logical CSS properties (`margin-inline-start` not `margin-left`) for RTL compatibility
- Bootstrap RTL stylesheet is auto-loaded when RTL language is active

---

## Custom App Translation Workflow

### Adding translations to your custom app:

1. **Write translatable strings** using `_()` / `__()` with positional placeholders
2. **Extract untranslated strings**:
   - v14: `bench --site {site} get-untranslated {lang} untranslated.csv`
   - v15+: `bench generate-pot-file --app {app}`
3. **Translate** the extracted strings (manually or via PO editor)
4. **Place translations**:
   - CSV: `apps/{app}/{app}/translations/{lang}.csv`
   - PO: `apps/{app}/{app}/locale/{lang}/LC_MESSAGES/{app}.po`
5. **Compile** (v15+ PO only): `bench compile-po-to-mo --app {app}`
6. **Clear cache**: `bench --site {site} clear-cache`

---

## Reference Files

| File | Contents |
|------|----------|
| [references/api-reference.md](references/api-reference.md) | Full Python _() and JS __() API with all signatures and edge cases |
| [references/csv-and-bench.md](references/csv-and-bench.md) | CSV format spec, bench commands, PO/MO workflow, custom app setup |
| [references/anti-patterns.md](references/anti-patterns.md) | Complete anti-pattern catalog with failing and corrected examples |
