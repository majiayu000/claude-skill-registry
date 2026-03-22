---
name: shipflow-audit-translate
description: Translation audit — single page (with argument) or full project i18n consistency check (no argument). Verifies completeness, quality, and consistency of all translations.
disable-model-invocation: true
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -100 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Default locale: !`grep -ri "defaultLocale\|default_locale\|i18n" astro.config.* next.config.* src/i18n/* 2>/dev/null | head -10 || echo "unknown"`
- i18n files: !`find src -path "*/i18n/*" -o -path "*/locales/*" -o -path "*/messages/*" -o -path "*/translations/*" -o -path "*/lang/*" 2>/dev/null | sort`
- Locale directories: !`find src/pages -mindepth 1 -maxdepth 1 -type d 2>/dev/null | sort || echo "no locale dirs"`
- Content collections: !`find src/content -type d -mindepth 1 -maxdepth 2 2>/dev/null | sort || echo "none"`
- All pages: !`find src/pages src/app -name "*.astro" -o -name "*.tsx" -o -name "*.vue" 2>/dev/null | grep -v node_modules | sort`
- Hardcoded strings: !`grep -rn --include="*.{astro,tsx,jsx,vue}" -E '>(["'"'"'])[A-ZÀ-Ÿ][^<]{5,}\1|>\s*[A-ZÀ-Ÿ][a-zà-ÿ]{3,}[^<]*<' src/components/ src/layouts/ 2>/dev/null | head -20 || echo "none found"`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: audit ALL multilingual projects in the workspace.
- **`$ARGUMENTS` is a file path** → PAGE MODE: check translations for that specific page.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full i18n audit of the entire project.

---

## GLOBAL MODE

Audit ALL multilingual projects in the workspace for translation completeness and i18n quality.

1. Read `/home/claude/shipflow_data/PROJECTS.md` — check the **Domain Applicability** table. Identify projects with ✓ in the Translate column.

2. Use **AskUserQuestion** to let the user choose:
   - Question: "Which projects should I audit for translations?"
   - `multiSelect: true`
   - One option per applicable project: label = project name, description = stack from PROJECTS.md
   - All applicable projects pre-listed as options

3. Use the **Task tool** to launch one agent per **selected** project — ALL IN A SINGLE MESSAGE (parallel). Each agent: `subagent_type: "general-purpose"`.

   Agent prompt must include:
   - `cd [path]` then read `CLAUDE.md` for project context
   - The complete **PROJECT MODE** section from this skill (all 7 phases: i18n Architecture Review → Translation Completeness Matrix → Consistency Audit → Hardcoded String Detection → Technical SEO for i18n → Fix → Report)
   - The **Tracking** section from this skill
   - Rule: **read-only analysis** — no code fixes, only update AUDIT_LOG.md and TASKS.md

4. After all agents return, compile a **cross-project translation report**:

   ```
   GLOBAL TRANSLATION AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]    [A/B/C/D]  —  summary
     ...
   CROSS-PROJECT PATTERNS
     [Shared terminology inconsistencies, common i18n gaps]
   ALL ISSUES BY SEVERITY
     🔴 [project] file:line — description
     🟠 [project] file:line — description
     🟡 [project] file:line — description
   Total: X critical, Y high, Z medium across N projects
   ═══════════════════════════════════════
   ```

5. Update `/home/claude/shipflow_data/AUDIT_LOG.md` (one row per project, Translate column) and `/home/claude/shipflow_data/TASKS.md` (each project's `### Audit: Translate` subsection).

6. Ask: **"Which projects should I fix?"** — list projects with scores. Fix only approved projects, one at a time.

---

## PAGE MODE

### Step 1: Identify the translation setup

1. Read the target file (`$ARGUMENTS`).
2. Determine the i18n approach:
   - **File-based routing**: `/pages/en/about.astro` + `/pages/fr/about.astro` (Astro)
   - **JSON/YAML translation files**: `locales/en.json` + `locales/fr.json`
   - **Content collections**: `content/blog/en/` + `content/blog/fr/`
   - **Inline i18n**: `t('key')` function calls
   - **Hybrid**: Combination of the above
3. Read all locale versions of this page/content.
4. Read the translation files used by this page.

### Step 2: Audit

#### 1. Completeness
- [ ] All translatable strings exist in every locale
- [ ] No missing keys in any language file
- [ ] No untranslated content (strings left in the source language)
- [ ] Dynamic content (dates, numbers, currencies) uses locale-aware formatting
- [ ] Pluralization rules are handled correctly per locale
- [ ] Alt text on images is translated

#### 2. Quality
- [ ] Translations are natural, not machine-translated gibberish
- [ ] Technical terms are translated consistently (same term → same translation everywhere)
- [ ] Brand names and product names are NOT translated (kept as-is)
- [ ] Cultural adaptation: idioms, date formats, number formats match the locale
- [ ] Tone and formality match the locale convention (tu/vous in FR, Sie/du in DE, etc.)
- [ ] French typographic rules: espaces insécables before : ; ! ? « »
- [ ] No truncation issues (translated text fits the UI — FR is ~15% longer than EN, DE ~30% longer)

#### 3. Technical Correctness
- [ ] No hardcoded strings in components (everything goes through i18n)
- [ ] `<html lang="xx">` matches the current locale
- [ ] `hreflang` tags present for all locale variants
- [ ] Canonical URL and `og:url` are locale-specific
- [ ] URL slugs are translated (or intentionally kept in source language)
- [ ] Meta title and description are translated
- [ ] `<link rel="alternate">` points to other locale versions

### Step 3: Fix

For each issue found:
1. Add missing translations directly (translate them naturally).
2. Fix technical i18n issues (hreflang, lang attribute, canonical).
3. Extract hardcoded strings to the i18n system.
4. For ambiguous translations or cultural choices, propose 2 options and ask.

### Step 4: Report

```
TRANSLATION REVIEW: [page name]
─────────────────────────────────────
Locales checked:   [fr, en, ...]
Completeness       [A/B/C/D] — X/Y keys translated
Quality            [A/B/C/D] — one-line summary
Technical i18n     [A/B/C/D] — hreflang, lang, canonical
─────────────────────────────────────
OVERALL            [A/B/C/D]

Missing translations added: X
Hardcoded strings extracted: Y
Technical fixes: Z
```

---

## PROJECT MODE

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `src/` dir) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit for translations?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run translation audit across every multilingual project" (Recommended)
  - One option per multilingual project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects.

### Phase 1: i18n Architecture Review

1. Identify the i18n framework/approach used.
2. List all supported locales.
3. Identify the default locale and fallback behavior.
4. Check the routing strategy (prefix-based, domain-based, etc.).

#### Architecture checks
- [ ] i18n setup is documented or clear from config
- [ ] Default locale has a consistent URL strategy (with or without prefix, but consistent)
- [ ] Language switcher exists and works
- [ ] Language preference is persisted (cookie, URL, browser preference)
- [ ] SEO: each locale has unique URLs (not just client-side switching)

### Phase 2: Translation Completeness Matrix

Build a matrix of all translation keys across all locales:

```
KEY                          FR    EN    [other]
─────────────────────────────────────────────────
nav.home                     ✓     ✓
nav.about                    ✓     ✗     ← MISSING
hero.title                   ✓     ✓
hero.subtitle                ✓     ✗     ← MISSING
...
─────────────────────────────────────────────────
TOTAL                       X/Y   X/Y
```

For content collections (blog posts, docs), check:
- [ ] Every piece of content exists in all locales
- [ ] Slugs are consistent across locales (same content linked by slug or ID)
- [ ] Frontmatter fields (title, description, date, tags) are translated

### Phase 3: Consistency Audit

#### Terminology Consistency
Build a glossary of key terms and verify they're translated the same way everywhere:

| Source (EN)    | FR Translation | Consistent? | Files |
|---------------|----------------|-------------|-------|
| Dashboard     | Tableau de bord | ✓ / ✗      | [list] |
| Settings      | Paramètres     | ✓ / ✗      | [list] |
| ...           | ...            | ...         | ...   |

Flag: same source term translated differently across files.

#### UI String Audit
- [ ] Button labels are consistent across pages (same action = same label)
- [ ] Error messages are consistent in style and tone
- [ ] Date/time/number formatting uses `Intl` APIs (not hardcoded formats)
- [ ] Currency formatting matches locale

### Phase 4: Hardcoded String Detection

Search all components, layouts, and pages for hardcoded user-facing strings:
- Text between HTML tags that isn't using `t()` or translation function
- `aria-label`, `placeholder`, `title`, `alt` attributes with hardcoded text
- Strings in JavaScript/TypeScript that appear in the UI

For each: extract to the i18n system and translate.

### Phase 5: Technical SEO for i18n

- [ ] `<html lang="xx">` dynamically set per locale
- [ ] `<link rel="alternate" hreflang="xx">` on all pages for all locales
- [ ] `<link rel="alternate" hreflang="x-default">` points to default locale
- [ ] Sitemap includes all locale URLs
- [ ] `og:locale` set correctly per page
- [ ] Canonical URLs are locale-specific (not all pointing to default)
- [ ] Meta title and description translated in every locale

### Phase 6: Fix

Fix all issues in code. Priority:
1. **Missing translations** — translate and add them
2. **Hardcoded strings** — extract to i18n system
3. **Inconsistent terminology** — standardize across all files
4. **Technical SEO** — hreflang, lang, canonical, sitemap
5. **Formatting** — dates, numbers, currencies using `Intl`
6. **French typography** — espaces insécables

### Phase 7: Report

```
TRANSLATION AUDIT: [project name]
═══════════════════════════════════════

I18N ARCHITECTURE
  Framework:         [approach used]
  Locales:           [fr, en, ...]
  Default locale:    [xx]
  Routing:           [prefix / domain / hybrid]
  Language switcher: [present / missing]

COMPLETENESS (by locale)
  FR:  X/Y keys (Z missing)
  EN:  X/Y keys (Z missing)
  ...

CONTENT COLLECTIONS
  Blog:    X/Y articles in all locales
  Docs:    X/Y pages in all locales
  ...

CONSISTENCY
  Terminology:    X inconsistencies across Y terms
  UI strings:     [consistent / mixed]
  Formatting:     [Intl APIs / hardcoded / mixed]

HARDCODED STRINGS
  Components:     X strings to extract
  Layouts:        X strings to extract
  Pages:          X strings to extract

TECHNICAL SEO
  hreflang:       [complete / partial / missing]
  Sitemap:        [all locales / default only]
  Meta tags:      X/Y pages fully translated

PAGE-BY-PAGE
  /                  FR [A/B/C/D]  EN [A/B/C/D]
  /about             FR [A/B/C/D]  EN [A/B/C/D]
  ...
═══════════════════════════════════════
OVERALL              [A/B/C/D]

Missing translations added: X
Hardcoded strings extracted: Y
Terminology standardized: Z terms
Technical fixes: W
```

---

## Tracking (all modes)

After generating the report and applying fixes:

### Log the audit

Append a row to two files:

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`**: append a row filling only the Translate column, `—` for others.
2. **Project-local `./AUDIT_LOG.md`**: same without the Project column.

Create either file if missing.

### Update TASKS.md

1. **Local TASKS.md** (project root): add/replace an `### Audit: Translate` subsection with critical (🔴), high (🟠), and medium (🟡) issues as task rows.
2. **Master `/home/claude/shipflow_data/TASKS.md`**: find the project's section, add/replace an `### Audit: Translate` subsection with the same tasks.

---

## Important (all modes)

- **Translate naturally.** No Google Translate quality. Write like a native speaker of each locale.
- For French: tutoiement/vouvoiement per project CLAUDE.md, espaces insécables before : ; ! ? and around « », no unnecessary anglicisms.
- Brand names, product names, and technical terms that are universally known (API, URL, JavaScript, etc.) stay in English.
- When a project uses bilingual message templates (e.g., `titleFr`/`titleEn`), check BOTH fields for every entry.
- For Astro content collections: check that the slug/ID linking between locales is correct — a French article must map to its English counterpart.
- Don't just flag missing translations — actually write the translation and add it.
- If you're unsure about a translation, propose 2 options and ask.
- **Accents français obligatoires.** Lors de toute création ou modification de contenu en français, vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe. Relire chaque texte produit pour s'assurer qu'aucun accent n'a été oublié — c'est une erreur très fréquente à corriger impérativement.
