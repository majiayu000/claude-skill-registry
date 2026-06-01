---
name: localize
description: >
  · Audit app i18n/l10n: hardcoded strings, locale catalogs, translations, fallback gaps. Triggers: 'i18n', 'internationalization', 'localization', 'locale', 'hardcoded strings', 'next-intl'.
license: MIT
compatibility: "Requires Node.js 20+. Optional: react-i18next, vue-i18n, next-intl, svelte-i18n, ngx-translate, i18next (per framework)"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-12"
  effort: high
  argument_hint: "[component-or-catalog]"
---

# Localize: App Internationalization Workflow

**Target versions (May 2026):** react-i18next 17.x, vue-i18n 11.x, next-intl 4.x, i18next 26.x

Systematic approach to internationalizing applications. Covers two scenarios: adding
multilingual support from scratch and auditing existing i18n for gaps. Built from real
production pain - the hardest part of i18n is not translation but finding every string
that needs it, and making sure translations read naturally in context rather than as
mechanical word-by-word output.

## When to use

- Adding multilingual support to an existing single-language app
- Auditing a codebase for untranslated hardcoded strings
- Checking an already-internationalized app for completeness or quality gaps
- Setting up locale catalogs, providers, and translation infrastructure
- Generating machine translations for new or changed source strings
- Validating catalog completeness across locales
- Adding new languages to an already-internationalized app
- Reviewing translation quality (voice consistency, domain accuracy, placeholder integrity)

## When NOT to use

- Translating standalone documents, README files, or prose - just ask the LLM directly
- Reviewing code quality or style issues - use **code-review** or **anti-slop**
- Building AI/LLM features that produce multilingual output at runtime - use **ai-ml**
- Setting up backend API endpoints for locale handling - use **backend-api**
- Writing tests for i18n behavior - use **testing** (though this skill includes validation)

---

## AI Self-Check

AI tools consistently produce the same i18n mistakes. **Before returning any generated i18n
code, catalogs, or translations, verify against this list:**

- [ ] **Native orthography in catalogs**: translated strings use proper Unicode characters
  for the target language (umlauts, accents, cedillas, CJK characters, etc.). ASCII-only
  rules from global or project config (CLAUDE.md, AGENTS.md, .cursorrules, etc.) apply to
  source code and prose, NOT to locale catalogs. Writing "hinzugefuegt" (ASCII ae/oe/ue
  substitution) instead of proper umlauts is a bug. Locale files are the one place where
  native script is mandatory.
- [ ] **Every string category covered**: checked all categories in the String Categories
  table below, not just visible text. Toast notifications, validation messages, aria-labels,
  placeholders, title attributes, alt text, loading states, conditional fragments, and error
  messages are the most commonly missed
- [ ] **Source catalog is the type authority**: types for message keys derive from the source
  locale (usually English), not from a union of all locales
- [ ] **Placeholders preserved**: every `{0}`, `{name}`, `{{var}}`, `%s`, `%d` in source
  strings appears identically in translated strings - same count, same order, same syntax
- [ ] **Brand names protected**: product names, service names, and proper nouns are preserved
  exactly in all locales
- [ ] **No partial extraction**: if auditing a file, every user-facing string in that file
  is extracted - not just the obvious ones. Check JSX text content, attribute values, template
  literals, and string arguments to UI functions
- [ ] **Fallback chain exists**: missing keys fall back to the source locale, then to the
  key itself - never to an empty string or a crash
- [ ] **Validation script created**: a script or test exists that compares all locale catalogs
  against the source for missing keys, extra keys, and empty values
- [ ] **Keys use dot notation**: keys follow a consistent `namespace.context.label` pattern.
  Keys describe what the text is for, not what it says
- [ ] **Voice consistency**: translations within each language use the same register (formal
  or informal) throughout. German "du" vs "Sie", French "tu" vs "vous", Spanish "tu" vs
  "usted" - pick one per language and stick with it across the entire catalog
- [ ] **Context-aware translation**: translations read naturally in the app's domain, not as
  mechanical word-by-word output. UI labels, error messages, and toast notifications should
  sound like a native speaker wrote them for that specific app
- [ ] **No library API hallucination**: if using a library (i18next, next-intl, vue-i18n),
  verify import paths, hook names, and configuration options against current docs
- [ ] **RTL/bidirectional text handled**: layout direction set in HTML lang/dir attributes,
  no LTR-only CSS assumptions
- [ ] **Catalog files parseable**: JSON/YAML validates without syntax errors, no trailing
  commas or unquoted keys
- [ ] **Locale detection complete**: browser navigator.language, Accept-Language header,
  or user preference stored and respected
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Locale data checked**: ICU message syntax, plural categories, and CLDR assumptions match the target locales
- [ ] **Fallback behavior tested**: missing keys, pseudo-locales, RTL, and long strings are exercised

---

## Performance

- Load locale bundles per route or language instead of shipping every catalog to every user.
- Cache compiled ICU messages where the framework supports it.
- Detect hardcoded strings with static scans before manual review.


---

## Best Practices

- Keep source strings stable and meaningful; do not use English copy as an implicit key if text changes often.
- Use translators' notes for placeholders, gender, tone, and domain-specific terms.
- Never concatenate translated fragments where grammar can change by language.


## Workflow

**Entry points** (always read the AI Self-Check above first, regardless of entry point):
- Adding i18n from scratch? Start at Step 1.
- Already have i18n, checking completeness? Start at Step 1 (assess), then Step 3 (audit).
- Just need translations for new keys? Jump to Step 4.
- Just validating catalogs? Jump to Step 5.

### Step 1: Assess current state

Before touching code, understand what exists:

1. **Check for existing i18n setup** - look for i18n libraries in `package.json` (or
   equivalent), locale/translation directories, i18n config files, and translation function
   usage (`t()`, `$t()`, `useTranslations`, `FormattedMessage`, etc.)
2. **Identify the framework** - React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Angular, or
   vanilla JS/TS. This determines the provider pattern and available libraries.
3. **Locate catalog files** - find where locale/translation files live. Common locations:
   `src/locales/`, `src/i18n/messages/`, `public/locales/`, or inline `<i18n>` blocks.
   Note the format (JSON, YAML, TS objects) and identify the source locale.
4. **Count the scope** - estimate how many files contain user-facing strings. Adapt
   the file extension to your framework. The JSX-text regex alone undercounts by a
   lot (misses attributes, toasts, errors) - combine with attribute and toast patterns:
   ```bash
   # React/JSX: text content + attribute values (placeholder, title, alt, aria-label)
   grep -rlE '>[A-Z][a-z]|(placeholder|title|alt|aria-label)="[A-Z]' \
     --include='*.tsx' --include='*.jsx' src/ | wc -l
   # Toast/validation strings hide in logic (not JSX). Check separately.
   grep -rlE 'toast\.(success|error|info|warn)|setError\(' \
     --include='*.ts' --include='*.tsx' src/ | wc -l
   # Vue: *.vue | Svelte: *.svelte | Angular: *.html + *.ts (see references/audit-patterns.md)
   ```
5. **Check for partial i18n** - the worst state is partially translated: some strings use
   `t()`, others are hardcoded. Map which areas are done and which are not.
6. **If i18n exists, check quality** - run the validation patterns from Step 5 to find
   missing keys, inconsistent voice, or stale translations.

### Step 2: Set up i18n infrastructure

If no i18n system exists, set one up. If one exists, skip to Step 3.

**Architecture decisions** (decide these first, not mid-implementation):

| Decision | Options | Guidance |
|----------|---------|----------|
| Catalog format | JSON, YAML, TS objects | TS objects give type safety without tooling. JSON works with most libraries |
| Key structure | flat, nested, dot-notation | Dot-notation (`auth.signIn`) balances readability and grep-ability |
| Interpolation | positional `{0}`, named `{name}`, ICU | Named for readability. Positional is simpler for machine translation |
| Pluralization | separate keys, ICU MessageFormat | Separate keys work for 2-form languages (English, German). Use ICU for Slavic and Arabic: Russian and Polish each have 4 CLDR plural categories (one/few/many/other), Arabic has 6. Picking "singular/plural" keys up front will force a rewrite later |
| Locale detection | browser, URL path, cookie, header | Browser detection for first visit, persisted preference after |
| Fallback | source locale, then key | Always. Never return empty or crash on missing key |
| Voice register | formal, informal | Decide per target language upfront. Document the choice |

**Components to create:**

1. **Locale registry** - supported locales, aliases, normalization, native display names
2. **Source catalog** - English (or source language) with all keys
3. **Provider/context** - framework-appropriate state for active locale
4. **Translation function** - `t(key)` lookup with fallback chain
5. **Locale persistence** - local storage for pre-auth, database for authenticated users
6. **Validation script** - compares all catalogs against source (see Step 5)
7. **Language switcher** - a visible UI element for changing locale. Place it where users
   can find it without digging through settings (e.g., below login form when unauthenticated,
   in the app bar when authenticated). Show native language names (Deutsch, not German).

**RTL awareness:** if any target locale uses right-to-left script (Arabic, Hebrew, Persian,
Urdu), the UI needs `dir="rtl"` support, CSS logical properties (`margin-inline-start`
instead of `margin-left`), and bidirectional text handling. RTL is a layout concern beyond
catalog setup - plan for it in the infrastructure, not as an afterthought.

**Quick setup for React (react-i18next)** - the most common case:

```tsx
// 1. Install: npm install react-i18next i18next
// 2. src/i18n.ts - init once, import before rendering
import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en.json'
i18n.use(initReactI18next).init({ lng: 'en', fallbackLng: 'en',
  resources: { en: { translation: en } } })
export default i18n

// 3. src/main.tsx - import side-effect before <App />
import './i18n'

// 4. In any component
import { useTranslation } from 'react-i18next'
const { t } = useTranslation()
return <button>{t('auth.signIn')}</button>
```

**Quick setup for Vue (vue-i18n):**

```ts
// 1. Install: npm install vue-i18n
// 2. src/i18n.ts
import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
export const i18n = createI18n({ locale: 'en', fallbackLocale: 'en', messages: { en } })

// 3. In any component
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
// <button>{{ t('auth.signIn') }}</button>
```

For Next.js use `next-intl`; for others see `references/audit-patterns.md`.

Read `references/audit-patterns.md` for framework-specific patterns on where strings hide.

### Step 3: Audit and extract strings

This is where i18n projects fail. Strings hide in places that are easy to overlook.

**The rule: work file by file, not category by category.** Open a file, extract ALL strings
from ALL categories before moving on. The "one more pass" loop (toast this time, then
aria-labels, then placeholders...) is the #1 i18n time sink.

**Audit process per file:**

1. Read the file completely.
2. Walk through the String Categories table below. For each category, check whether that
   file has any instances.
3. Add keys to the source catalog. Use dot-notation: `namespace.context.label`.
4. Replace hardcoded strings with `t()` calls (or the project's equivalent).
5. Convert template literals: `` `${name} connected` `` becomes
   `t('service.connected').replace('{0}', name)` or the library's interpolation syntax.

**String categories quick reference:**

| Category | Example | Why it gets missed |
|----------|---------|-------------------|
| Toast/notification | `toast.success('Saved')` | In event handlers, not JSX |
| Validation error | `setError('Name is required')` | Buried in form logic |
| Placeholder | `placeholder="Search..."` | Attribute, not text content |
| defaultValue | `defaultValue="Search..."` | Functionally same as placeholder, different attr |
| aria-label | `aria-label="Close menu"` | Not visible on screen |
| title attribute | `title="Click to expand"` | Tooltip, invisible by default |
| alt text | `alt="User avatar"` | Image fallback, often ignored |
| Button label | `<button>Submit</button>` | Obvious but still missed in edge components |
| Loading state | `'Loading...'` | Short, feels like a constant |
| Conditional fragment | `'(not configured)'` | Not a full sentence |
| Confirm dialog | `confirm('Delete this?')` | Browser API, not component |
| Error boundary | `'Something went wrong'` | Rare path |
| Empty state | `'No results found'` | Only visible when data is absent |
| Select/option label | `<option>Choose one</option>` | Inside form elements |
| Table header | `<th>Status</th>` | Structural, feels permanent |
| Document title | `document.title = 'Settings'` | Not in the component tree |
| Server response text | `{ error: 'Invalid email' }` | Lives in API layer, not frontend |

See `references/audit-patterns.md` for false positives to skip (console.log, CSS classes,
data attributes, route patterns, etc.).

Read `references/audit-patterns.md` for grep commands that catch each category.

### Step 4: Generate translations

After the source catalog is complete and all strings use `t()` calls:

**Translation quality matters more than speed.** Machine translations that read like
mechanical word-by-word output are worse than no translation - they make the app feel
broken in every language. Read `references/translation-quality.md` for the full approach.

**Key principles:**

1. **Provide app context** in the translation prompt. Include the app's domain, what it does,
   and who uses it. "A music discovery app" produces different translations than "an enterprise
   billing system."
2. **Specify voice register** per language. Decide formal vs informal for each target language
   before translating. Document this decision.
3. **Protect brand names** - maintain a list of terms that must not be translated (product
   names, service names, technical identifiers).
4. **Translate in batches, validate between batches.** One locale at a time. Don't translate
   all 15 locales then discover a systematic error.
5. **Validate every batch** before committing (see Step 5).

Use the full prompt template from `references/translation-quality.md` - it includes
app context, voice register, protected terms, preservation rules, and explicit "do not"
constraints. Do not improvise a shorter prompt.

### Step 5: Validate catalogs

Validation is the safety net. Set it up early, run it often.

**Completeness checks:**

| Check | What it catches |
|-------|----------------|
| Missing keys | Keys in source but not in target |
| Extra keys | Stale translations for removed source keys |
| Empty values | Key exists but value is blank |
| Placeholder mismatch | Source has `{0}` but translation doesn't |
| Protected term mutation | Brand name was translated when it shouldn't be |
| Line break mismatch | Formatting differs from source |

**Validation script pattern:**

```typescript
const sourceKeys = Object.keys(sourceCatalog)
for (const locale of supportedLocales) {
  const catalog = getCatalog(locale)
  const missing = sourceKeys.filter(k => !(k in catalog))
  const extra = Object.keys(catalog).filter(k => !sourceKeys.includes(k))
  const empty = sourceKeys.filter(k => catalog[k]?.trim() === '')
  // Fail if any issues
}
```

For placeholder and protected term validation, see `references/translation-quality.md`.

**When to run:**
- After every translation generation
- In CI (pre-merge) - prevents drift from day one
- Before releases

**Quality audit for existing i18n:**

When checking an already-internationalized app, go beyond completeness:

1. Run the validation script for missing/extra/empty keys
2. Spot-check 10-20 keys across each locale for voice consistency (formal vs informal mixing)
3. Check interpolated strings render correctly with real data
4. Verify `Intl` formatting uses the locale variable, not hardcoded `'en-US'`:
   ```bash
   grep -rn "Intl\.\(DateTimeFormat\|NumberFormat\)" src/ | grep "'en"
   ```
5. Re-run the audit grep patterns from Step 3 to catch newly hardcoded strings

### Step 6: Ongoing maintenance

Once i18n is set up, the workflow for new features is:

1. Add source-language strings to the source catalog
2. Use `t()` in new code - never hardcoded strings
3. Run the validation script to see which locales need updates
4. Generate translations for the new keys
5. Validate and commit

**Preventing drift:**
- Add validation to CI so PRs with missing translations fail
- Periodically re-audit with grep patterns to catch regressions
- When reviewing PRs, check new UI text uses `t()`, not literals

---

## Reference Files

- `references/audit-patterns.md` - grep commands for finding hardcoded strings in React, Vue,
  Svelte, Angular, and vanilla JS/TS. Organized by string category. Use during Step 3.
- `references/translation-quality.md` - context-aware translation prompting, voice consistency
  rules, protected term handling, and validation script implementations. Use during Steps 4-5.

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** LOCALIZE
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **audit, review, or improve** existing i18n (hardcoded-string audit, catalog completeness check, translation quality review), emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/localize/<YYYY-MM-DD>-<slug>.md`. When invoked to **set up i18n from scratch, generate translations for new keys, or answer a question**, respond freely without the contract.
- **Deliverable path:** `docs/local/audits/localize/<YYYY-MM-DD>-<slug>.md`
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **testing** - write tests for i18n behavior (locale switching, fallbacks, formatting).
  This skill guides what to build; testing guides how to verify it.
- **code-review** - catches hardcoded strings during review. This skill catches them
  systematically via audit.
- **backend-api** - if the API serves user-facing text, locale resolution and content
  negotiation belong in the API layer. This skill handles the broader i18n setup.
- **ai-ml** - when AI-generated text needs to respond in the user's language at runtime,
  the AI locale context is an i18n concern. The response quality is an ai-ml concern.

## Rules

1. **Audit file by file, not category by category.** Extract ALL strings from a file before
   moving to the next. The "one more pass" loop is the #1 i18n time sink.
2. **Source locale is the type authority.** All message key types derive from the source
   catalog. Other locales conform to it, not the other way around.
3. **Validate before committing translations.** Never commit machine-translated catalogs
   without running placeholder and completeness checks.
4. **Never return empty strings for missing keys.** The fallback chain must end at the
   source locale value or the key itself - never empty, null, or a crash.
5. **Preserve brand names exactly.** Product names, service names, and proper nouns must
   match the source. Maintain a protected terms list per project.
6. **Maintain voice consistency per language.** Pick formal or informal register for each
   target language and enforce it across the entire catalog. Mixing registers makes the
   app feel incoherent.
7. **Translate for the app's context, not word-by-word.** UI strings should read like a
   native speaker wrote them for this specific application.
8. **Add validation to CI early.** A script that fails on missing keys prevents drift from
   day one. Don't defer this.
9. **Don't translate what shouldn't be translated.** Code identifiers, CSS classes, data
   attributes, technical log messages, and developer-facing strings stay in the source
   language.
10. **Use native orthography in locale catalogs.** Translated strings must use proper
    Unicode characters for the target language - umlauts, accents, cedillas, CJK characters,
    full-width punctuation, etc. ASCII-only rules from global or project config apply to
    source code and prose, not to translation output. Writing "hinzugefuegt" instead of
    proper German umlauts, or "nino" instead of Spanish n-with-tilde, is a translation
    bug, not a style choice.
