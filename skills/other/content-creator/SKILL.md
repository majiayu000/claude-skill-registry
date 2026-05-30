---
name: content-creator
description: >
  Self-configuring content creation pipeline with geo-lint validation.
  On first use, scans your project to learn its framework, content schema,
  categories, and authors, then creates SEO & GEO-optimized content matched
  to your brand voice. Validates every piece with geo-lint's 92 rules until
  zero violations. Triggers on: "content-creator", "create content",
  "write blog", "new post", "content calendar", "brand voice",
  "content strategy".
argument-hint: "setup | create [blog|page|project] | voice | calendar | refresh"
allowed-tools:
  - Bash(npx geo-lint*)
  - Bash(npm *)
  - Bash(node *)
  - Bash(python *brand_voice*)
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - AskUserQuestion
  - Agent
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  contributors:
    - Jamin Mahmood-Wiebe
  category: marketing
  domain: content-creation
  updated: 2026-03-01
---

# Content Creator

Self-configuring content creation pipeline. Creates SEO & GEO-optimized content
matched to your project and brand voice, then validates with geo-lint until clean.

For project-specific rules (components, file naming, categories), the skill
generates a local `content-config` skill on first use via the `setup` workflow.

## Command Router

Parse `$ARGUMENTS` and route to the matching workflow:

| Argument | Workflow |
|----------|----------|
| `setup` | Auto-discover project, questionnaire, generate content-config |
| `create [blog\|page\|project]` | Full content creation pipeline |
| `voice` | Analyze and configure brand voice |
| `calendar` | Plan monthly content calendar |
| `refresh` | Re-scan project, update content-config |
| _(no args)_ | If no config exists → auto-trigger `setup`. Otherwise show commands. |

## Pre-Flight Check

Before any workflow except `setup`:

1. Check if `.claude/skills/content-config/SKILL.md` exists in the project root.
2. If missing → inform the user: "No project content config found. Running setup first..." Then auto-trigger the `setup` workflow.
3. If found → read it into context and proceed with the requested workflow.

---

## Workflow: setup

Three phases: auto-discover → questionnaire → generate.

### Phase 1: Auto-Discovery

Run these steps silently, collecting results into a discovery report:

**1. Framework Detection**
- Read `package.json` dependencies and devDependencies for: `next`, `astro`, `@astrojs/*`, `gatsby`, `hugo`, `nuxt`, `vite`, `remix`, `@11ty/eleventy`
- Check for config files: `next.config.*`, `astro.config.*`, `nuxt.config.*`, `gatsby-config.*`, `.eleventy.js`
- Record: framework name + version

**2. Content Directories**
- Search for common patterns: `content/`, `src/content/`, `posts/`, `blog/`, `pages/`, `articles/`, `src/pages/`
- If `geo-lint.config.ts` exists → read its `contentPaths`
- Record: all content directories and file extensions (`.md`, `.mdx`, `.astro`, `.html`)

**3. Frontmatter Schema**
- Read 5–10 representative content files across detected directories
- Parse YAML frontmatter (lines between `---` delimiters)
- Compute the union of all field names; classify each as required (present in >80% of files) or optional
- Record: field schema with types inferred from values

**4. Categories**
- Extract unique values from `category` and `categories` frontmatter fields across all content
- Cross-reference with `geo-lint.config.ts` `categories` array if present
- Record: canonical category list

**5. Authors**
- Extract unique `author` values from all content frontmatter
- Record: author names

**6. Locales & i18n**
- Detect from: frontmatter `locale` fields, file naming patterns (`.de.mdx`, `.en.mdx`), directory patterns (`/de/`, `/en/`)
- Check `geo-lint.config.ts` i18n config if present
- Record: locales and default locale

**7. Site URL**
- Check in order: `geo-lint.config.ts` siteUrl → `package.json` homepage → framework config `site`/`url` field
- Record: URL or "not found"

**8. Image Directories**
- Search for: `public/images/`, `static/images/`, `assets/images/`, `src/assets/`
- Record: directories found

**9. Components (MDX projects only)**
- If `.mdx` files exist → scan for JSX component usage patterns (`<ComponentName`)
- Exclude standard HTML tags
- Record: component names found

### Phase 2: Questionnaire

Present the discovery summary as a formatted table. Then use `AskUserQuestion` to gather:

1. **Confirm discoveries** — "Here's what I found about your project: [table]. Is this correct? Any corrections?"
2. **Brand voice archetype** — Options from `references/brand_guidelines.md`: The Expert, The Friend, The Innovator, The Guide, The Motivator. Allow primary + secondary selection.
3. **Tone attributes** — Pick 3–5 from: Authoritative, Friendly, Innovative, Trustworthy, Inspiring, Educational, Witty
4. **Target audience** — Free text (e.g., "B2B decision-makers in manufacturing, CTOs")
5. **Content goals** — Free text (e.g., "thought leadership, lead generation, brand awareness")

### Phase 3: Generation

1. **Generate `.claude/skills/content-config/SKILL.md`** in the project root using the Content-Config Template below. Fill all `[placeholders]` with discovered and questionnaire data.

2. **geo-lint.config.ts** — if it does not exist:
   - Generate it with discovered `siteUrl`, `contentPaths`, `categories`, and `geo.brandName` if known
   - Install `@ijonis/geo-lint` as a devDependency if not present

3. **geo-lint.config.ts** — if it exists but is missing discovered data:
   - Propose additions (new categories, new contentPaths) for user confirmation

4. **Validation test** — run `npx geo-lint --format=json` to confirm config loads correctly

5. Report: "Setup complete. Your content pipeline is ready. Run `/content-creator create` to start."

---

## Workflow: create

Full content creation pipeline with built-in validation.

### Step 1: Load Project Config

Read `.claude/skills/content-config/SKILL.md` for project-specific rules: content schema, brand voice, categories, components, file naming conventions, languages.

### Step 2: Topic & Type

Ask the user for:
- **Topic or title** for the new content piece
- **Content type** — blog, page, or project (default: blog)

### Step 3: Duplicate & Overlap Gate (MANDATORY)

Scan ALL existing content (titles, slugs, descriptions) before proceeding:

| Finding | Action |
|---------|--------|
| Exact duplicate (same topic + angle) | **Stop.** Suggest updating the existing post instead. |
| Substantial overlap (same topic, different angle) | **Stop.** Propose a clearly differentiated angle. Get user approval before proceeding. |
| Tangential overlap (related topic, distinct focus) | **Proceed.** Note the related post for cross-linking. |
| No overlap | **Proceed.** |

Report which existing posts were checked and the gate result.

### Step 4: Keyword & Search Research (MANDATORY)

Use `WebSearch` to research the topic. Follow the **purchase-intent-first** strategy:

1. Search for trending angles, competitor coverage, and keyword variations
2. Identify: 1 primary keyword, 3–5 secondary keywords, 10–15 LSI keywords
3. Explicitly mine for purchase-intent keywords (e.g., +pricing/cost, +provider/agency, +comparison/vs/alternative; for German markets also +Kosten, +Anbieter, +Vergleich)
4. Run the SERP Viability Filter for the primary keyword:
   - **Authority Check** — are top results Wikipedia/Forbes (red flag) or mid-size blogs (green flag)?
   - **Intent Check** — are ranking results blog posts (match) or product pages (mismatch)?
   - **Coverage Check** — does the site already rank for this? (`site:domain "[keyword]"`)
   - **Long-Tail Check** — does a long-tail variant have community demand?
5. Document: confirmed primary keyword with 2–3 sentence rationale, intent classification, differentiation angle

### Step 5: Select Template

Load `references/content_frameworks.md`. Choose the best template for the topic:
- **How-To Guide** — prerequisites → steps → troubleshooting → results
- **Listicle** — introduction → items → action plan
- **Case Study** — challenge → solution → results → takeaways
- **Thought Leadership** — current state → trend → implications → recommendations

### Step 6: Write Content

Follow the project schema from content-config:
- Use correct frontmatter fields (all required fields populated)
- Follow file naming conventions (locale suffixes if bilingual)
- Apply brand voice (archetypes, tone attributes, target audience)
- Use available MDX components where they enhance the content (if applicable)
- SEO targets: keyword density 1–3%, proper heading hierarchy (one H1, no skipped levels), 1,500–2,500 words for blog posts
- Add 2–3 internal links to related existing posts
- Add 1–2 external links to authoritative sources

### Step 7: Validate (MANDATORY)

Run the geo-lint validation loop:

```bash
npx geo-lint --format=json --root=.
```

1. Filter violations to the newly created file
2. Fix ALL violations — **errors first, then warnings**
3. Re-run the linter after fixes
4. Repeat until zero violations for the new post
5. Maximum **5 fix passes** — if violations remain after 5 passes, report which rules still fail and why

**Rules that require human input** (do NOT fix, report to user):
- `geo-low-citation-density` — requires real statistics; never fabricate
- `image-not-found` — image file must exist on disk
- `broken-internal-link` — target page may not exist
- `category-invalid` — must use configured categories

### Step 8: Cross-Link

- Update 1–2 existing related posts with links to the new content
- Verify internal links resolve correctly

### Step 9: Report

Summary: files created, content type, primary keyword, violations fixed, internal links added, any items requiring human attention.

---

## Workflow: voice

Analyze and configure brand voice settings.

1. If Python is available → run the brand voice analyzer from the skill's install directory (`~/.claude/skills/content-creator/scripts/brand_voice_analyzer.py`) on 3–5 recent content files
2. Display current voice profile: formality spectrum, tone attributes, perspective, readability score
3. Compare against the configured voice in `.claude/skills/content-config/SKILL.md`
4. If adjustments needed → ask user via `AskUserQuestion` with archetype and tone options
5. Update `.claude/skills/content-config/SKILL.md` with new voice preferences

If Python is not available, analyze voice manually by reading content and assessing tone, formality, and perspective.

---

## Workflow: calendar

Plan a monthly content calendar.

1. Load `assets/content_calendar_template.md` as the base template
2. Read existing content to identify: publishing cadence, topic gaps, category distribution, seasonal patterns
3. Use `WebSearch` to research trending topics in the project's domain and industry
4. Generate a monthly calendar with: topics, target keywords, content types, suggested templates, publishing dates
5. Follow the 40/25/25/10 content pillar ratio: Educational / Inspirational / Conversational / Promotional
6. Save to a location the user chooses (default: `docs/content-calendar.md`)

---

## Workflow: refresh

Re-scan the project and update content-config.

1. Re-run all auto-discovery steps from the `setup` Phase 1
2. Read existing `.claude/skills/content-config/SKILL.md`
3. Compute diff: new categories, new authors, new components, new locales, new content types, changed directories
4. Present changes as a before/after comparison table
5. If user approves → update content-config, **preserving user-customized sections** (brand voice, audience, goals)
6. If `geo-lint.config.ts` also needs updates (new categories, new contentPaths) → propose those changes separately
7. Report what changed

---

## Content-Config Template

The `setup` workflow generates `.claude/skills/content-config/SKILL.md` in the user's project. The agent fills `[placeholders]` with discovered and questionnaire data:

```markdown
---
name: content-config
description: [ProjectName]-specific content creation rules. Defines content schemas,
  categories, brand voice, and geo-lint validation workflow. Generated by
  /content-creator setup — edit freely to refine.
---

# [ProjectName] Content Config

Generated by `/content-creator setup`. Extends the global `content-creator` skill
with project-specific rules. Edit this file to refine your content pipeline.

## Brand Identity

### Brand Voice
- **Archetypes:** [Primary] (primary) + [Secondary] (secondary)
- **Tone:** [3-5 chosen attributes, comma-separated]
- **Target Audience:** [from questionnaire]
- **Content Goals:** [from questionnaire]

### Authors
| Author | Focus Areas |
|--------|------------|
| [Name] | [inferred from existing content topics, or "General"] |

## Content Schema

### Framework
[Framework name] [version]

### Content Types
| Type | Directory | URL Prefix | Extensions |
|------|-----------|------------|------------|
| [type] | [dir] | [prefix] | [.mdx, .md] |

### Required Frontmatter
[List fields present in >80% of files, with inferred types]

### Optional Frontmatter
[List fields present in <80% of files]

### Canonical Categories
[Comma-separated list, or "None configured — add to geo-lint.config.ts"]

## File Naming
[Convention discovered — e.g., "kebab-case.mdx" or "slug.de.mdx / slug.en.mdx"]

## Languages
[Locales discovered + default locale, or "Single language"]

## Components
[MDX component names found, or "N/A — no MDX components detected"]

## Content Creation Workflow

1. **Duplicate check** — scan existing content for topic overlap before writing
2. **Keyword research** — use WebSearch, purchase-intent first
3. **Write** — follow schema above, apply brand voice, use components where appropriate
4. **Validate** — run `npx geo-lint --format=json`, filter to new file
5. **Fix all violations** — errors AND warnings, max 5 passes
6. **Cross-link** — add 2-3 internal links, update 1-2 existing posts

New content MUST ship with zero geo-lint violations.

## Validation Commands

npx geo-lint --format=json        # Full project lint (JSON output)
npx geo-lint --root=.             # Full project lint (human-readable)
npx geo-lint --rules              # Show all 92 rules with fix strategies
```

---

## Reference Guides

Load these on demand — do not read them all into context at once:

| Reference | When to load |
|-----------|-------------|
| `references/brand_guidelines.md` | During `setup` (voice selection) and `voice` workflow |
| `references/content_frameworks.md` | During `create` (template selection) |
| `references/social_media_optimization.md` | When creating social media content |
| `assets/content_calendar_template.md` | During `calendar` workflow |
| `scripts/brand_voice_analyzer.py` | During `voice` workflow (optional — requires Python) |
