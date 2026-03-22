---
name: shipflow-audit-seo
description: Professional SEO audit — single page (with argument) or full technical + on-page site audit (no argument)
disable-model-invocation: true
argument-hint: [file-path | "global"] (omit for full project)
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -100 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- All pages: !`find src/pages src/app -name "*.astro" -o -name "*.tsx" -o -name "*.vue" 2>/dev/null | grep -v node_modules | sort`
- Sitemap: !`cat public/sitemap*.xml 2>/dev/null | head -50 || echo "no sitemap found"`
- Robots.txt: !`cat public/robots.txt 2>/dev/null || echo "no robots.txt"`
- SEO/head component: !`find src -name "*seo*" -o -name "*head*" -o -name "*meta*" 2>/dev/null | grep -v node_modules | head -10 || echo "none found"`
- Astro config: !`cat astro.config.* 2>/dev/null | head -50 || echo "no astro config"`
- Content files count: !`find src/content -type f 2>/dev/null | wc -l || echo "0"`

## Mode detection

- **`$ARGUMENTS` is "global"** → GLOBAL MODE: audit ALL projects in the workspace.
- **`$ARGUMENTS` is a file path** → PAGE MODE: SEO review of that single page.
- **`$ARGUMENTS` is empty** → PROJECT MODE: full technical + on-page SEO audit.

---

## GLOBAL MODE

Audit ALL web projects in the workspace for SEO issues.

1. Read `/home/claude/shipflow_data/PROJECTS.md` — check the **Domain Applicability** table. Identify projects with ✓ in the SEO column.

2. Use **AskUserQuestion** to let the user choose:
   - Question: "Which projects should I audit for SEO?"
   - `multiSelect: true`
   - One option per applicable project: label = project name, description = stack from PROJECTS.md
   - All applicable projects pre-listed as options

3. Use the **Task tool** to launch one agent per **selected** project — ALL IN A SINGLE MESSAGE (parallel). Each agent: `subagent_type: "general-purpose"`.

   Agent prompt must include:
   - `cd [path]` then read `CLAUDE.md` for project context
   - The complete **PROJECT MODE** section from this skill (all 7 phases: Technical SEO → On-Page Scan → Content SEO → Structured Data → Internal Linking → Fix → Report)
   - The **Tracking** section from this skill
   - Rule: **read-only analysis** — no code fixes, only update AUDIT_LOG.md and TASKS.md

4. After all agents return, compile a **cross-project SEO report**:

   ```
   GLOBAL SEO AUDIT — [date]
   ═══════════════════════════════════════
   PROJECT SCORES
     [project]    [A/B/C/D]  —  summary
     ...
   CROSS-PROJECT PATTERNS
     [Systemic SEO issues in 2+ projects]
   ALL ISSUES BY SEVERITY
     🔴 [project] file:line — description
     🟠 [project] file:line — description
     🟡 [project] file:line — description
   Total: X critical, Y high, Z medium across N projects
   ═══════════════════════════════════════
   ```

5. Update `/home/claude/shipflow_data/AUDIT_LOG.md` (one row per project, SEO column) and `/home/claude/shipflow_data/TASKS.md` (each project's `### Audit: SEO` subsection).

6. Ask: **"Which projects should I fix?"** — list projects with scores. Fix only approved projects, one at a time.

---

## PAGE MODE

### Step 1: Gather the page

1. Read the target file (`$ARGUMENTS`).
2. Read the layout/head component that injects meta tags.
3. Read the SEO config/defaults (BaseHead.astro, metadata.ts, or equivalent).
4. Read the sitemap config if it exists.

### Step 2: Audit against this checklist

Score each category **A/B/C/D**. Be strict — production SEO standard.

#### 1. Meta Tags & Head
- [ ] `<title>` present, 50-60 characters, includes primary keyword
- [ ] `<meta description>` present, 150-160 characters, includes CTA
- [ ] `<meta robots>` allows indexing (or intentionally noindex)
- [ ] `<link rel="canonical">` present and correct (absolute URL)
- [ ] `<html lang="xx">` matches content language
- [ ] No duplicate meta tags

#### 2. Open Graph & Social
- [ ] `og:title`, `og:description`, `og:image` present
- [ ] `og:image` is 1200x630px with absolute URL
- [ ] `og:type` is set (article, website, product, etc.)
- [ ] `og:url` matches canonical
- [ ] Twitter card meta present
- [ ] Social preview would look good when shared

#### 3. Heading Structure
- [ ] Exactly one `<h1>` per page
- [ ] H1 contains primary keyword naturally
- [ ] Heading hierarchy is sequential (no skips)
- [ ] Headings are descriptive, not generic
- [ ] No headings used purely for styling

#### 4. Content & Keywords
- [ ] Primary keyword appears in: title, H1, first paragraph, URL
- [ ] Keyword density is natural (1-2%, not stuffed)
- [ ] Related/LSI keywords are present
- [ ] Content length is competitive for keyword intent
- [ ] No duplicate content with other pages

#### 5. Images & Media
- [ ] All `<img>` have descriptive `alt` text
- [ ] Images use modern formats (WebP/AVIF)
- [ ] Images have explicit `width` and `height` (prevents CLS)
- [ ] Below-fold images are lazy-loaded
- [ ] Hero/LCP image is NOT lazy-loaded (`fetchpriority="high"`)

#### 6. Technical SEO
- [ ] URLs are clean (lowercase, hyphens)
- [ ] Page is in sitemap.xml
- [ ] Internal links use descriptive anchor text
- [ ] At least 2-3 internal links to/from this page
- [ ] No broken links
- [ ] Structured data / JSON-LD present
- [ ] Breadcrumbs present for nested pages

#### 7. Performance (SEO-impacting)
- [ ] No render-blocking resources in `<head>`
- [ ] Critical CSS inlined or loaded early
- [ ] Fonts use `font-display: swap`
- [ ] No massive JS bundles for static content
- [ ] Third-party scripts are deferred

### Step 3: Fix

For each issue rated B or worse:
1. Identify the exact file and line.
2. Fix it directly in the code.
3. For content decisions (keyword choice, meta description wording), propose 2 options.

### Step 4: Report

```
SEO REVIEW: [page name] — target keyword: "[inferred keyword]"
─────────────────────────────────────
Meta Tags & Head   [A/B/C/D] — one-line summary
Social / OG        [A/B/C/D] — one-line summary
Heading Structure  [A/B/C/D] — one-line summary
Content & Keywords [A/B/C/D] — one-line summary
Images & Media     [A/B/C/D] — one-line summary
Technical SEO      [A/B/C/D] — one-line summary
Performance        [A/B/C/D] — one-line summary
─────────────────────────────────────
OVERALL            [A/B/C/D]

Fixed: X issues | Needs decision: Y issues
```

---

## PROJECT MODE

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `src/` dir, no `astro.config.*`) BUT contains multiple project subdirectories — you are at the **workspace root**, not inside a project.

Use **AskUserQuestion**:
- Question: "You're at the workspace root. Which project(s) should I audit for SEO?"
- `multiSelect: true`
- Options:
  - **All projects** — "Run SEO audit across every applicable project" (Recommended)
  - One option per SEO-applicable project from `/home/claude/shipflow_data/PROJECTS.md`: label = project name, description = stack

Then proceed to **GLOBAL MODE** with the selected projects.

### Phase 1: Technical SEO Infrastructure

#### Crawlability & Indexation
- [ ] `robots.txt` exists and is correct
- [ ] `sitemap.xml` exists and lists all public pages
- [ ] Sitemap referenced in `robots.txt`
- [ ] Canonical URLs on all pages (absolute URLs)
- [ ] No orphan pages
- [ ] No accidental `noindex`
- [ ] 404 page exists with proper status code
- [ ] Redirects are 301 (not 302)

#### Site Architecture
- [ ] URL structure is clean, hierarchical, consistent
- [ ] Max 3 clicks from homepage to any page
- [ ] Breadcrumbs on nested pages
- [ ] Pagination uses `rel="next"` / `rel="prev"` if applicable

#### Performance (SEO-critical)
- [ ] SSG/SSR used (not client-side rendering for content)
- [ ] HTML served with proper content
- [ ] Images optimized
- [ ] LCP image eagerly loaded
- [ ] No render-blocking resources
- [ ] Fonts use `font-display: swap`

### Phase 2: On-Page SEO — Systematic Scan

For EVERY page, check and record in a table:

| Page | Title (len) | H1 | Meta Desc (len) | OG Image | Schema | Internal Links |
|------|------------|-----|-----------------|----------|--------|---------------|

### Phase 3: Content SEO

- [ ] No duplicate titles across pages
- [ ] No duplicate meta descriptions
- [ ] No thin pages (< 300 words)
- [ ] Blog/article pages have: author, date, category
- [ ] Content collections have proper frontmatter

### Phase 4: Structured Data

- [ ] JSON-LD on relevant pages:
  - Homepage: `Organization` or `WebSite`
  - Blog posts: `Article`
  - Product/pricing: `Product` or `Offer`
  - FAQ sections: `FAQPage`
  - Breadcrumbs: `BreadcrumbList`
- [ ] JSON-LD is valid schema.org

### Phase 5: Internal Linking

Map the internal link graph:
1. Which pages have the most inbound internal links?
2. Which important pages are under-linked?
3. Are anchor texts descriptive?
4. Does navigation reinforce page hierarchy?

### Phase 6: Fix

Fix all issues in code. Priority:
1. **Missing/broken meta tags** — highest SEO impact
2. **Missing structured data** — add JSON-LD
3. **Heading hierarchy** — semantic corrections
4. **Image alt text** — descriptive alts everywhere
5. **Internal linking gaps** — add contextual links
6. **Sitemap/robots.txt** — ensure completeness
7. **Performance** — lazy loading, fonts, images

### Phase 7: Report

```
SEO AUDIT: [project name]
═══════════════════════════════════════

TECHNICAL SEO
  Crawlability:      [A/B/C/D]
  Site Architecture:  [A/B/C/D]
  Performance:        [A/B/C/D]

ON-PAGE SEO (X pages scanned)
  Titles:            X/Y correct
  Meta Descriptions: X/Y correct
  H1 Tags:           X/Y correct
  OG Tags:           X/Y complete
  Alt Text:          X/Y images covered

STRUCTURED DATA
  Pages with schema: X/Y
  Types used:        [list]

INTERNAL LINKING
  Avg links/page:    X
  Orphan pages:      [list]
  Under-linked:      [list]

PAGE-BY-PAGE
  /                  [A/B/C/D]
  /about             [A/B/C/D]
  ...
═══════════════════════════════════════
OVERALL              [A/B/C/D]

Fixed: X issues across Y files
Critical remaining: Z items
```

---

## Tracking (all modes)

After generating the report and applying fixes:

### Log the audit

Append a row to two files:

1. **Global `/home/claude/shipflow_data/AUDIT_LOG.md`**: append a row filling only the SEO column, `—` for others.
2. **Project-local `./AUDIT_LOG.md`**: same without the Project column.

Create either file if missing.

### Update TASKS.md

1. **Local TASKS.md** (project root): add/replace an `### Audit: SEO` subsection with critical (🔴), high (🟠), and medium (🟡) issues as task rows.
2. **Master `/home/claude/shipflow_data/TASKS.md`**: find the project's section, add/replace an `### Audit: SEO` subsection with the same tasks. Update the Dashboard "Top Priority" if critical issues found.

---

## Important (all modes)

- Infer the target keyword from content and URL. If unclear, ask.
- For French content: meta descriptions and titles in French, accented URL slugs OK if project is consistent.
- Never stuff keywords. Natural language always wins.
- Structured data must be valid JSON-LD with schema.org types.
- For Astro sites: leverage `@astrojs/sitemap` and `<Image>` component.
- For 100+ content page sites, focus detailed audit on templates/layouts since all pages of a type share the same SEO structure.
- **Accents français obligatoires.** Lors de toute création ou modification de contenu en français (meta descriptions, titres, alt text, données structurées), vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe. Relire chaque texte produit pour s'assurer qu'aucun accent n'a été oublié — c'est une erreur très fréquente à corriger impérativement.
