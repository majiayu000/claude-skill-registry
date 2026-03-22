---
name: shipflow-enrich
description: Research the web and upgrade a blog article, product page, or entire content folder — fresh data, actionable advice, user-centric, conversion-driven
disable-model-invocation: true
argument-hint: <file-path or folder>
---

## Context

- Current directory: !`pwd`
- Project CLAUDE.md: !`head -120 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`
- Content language: !`grep -ri "lang=" src/layouts/*.astro src/app/layout.tsx 2>/dev/null | head -3 || echo "detect from content"`
- Content structure: !`ls $ARGUMENTS 2>/dev/null | head -30 || echo "single file mode"`

## Your task

Upgrade content to be genuinely useful, technically accurate, and action-driving. The reader should leave knowing more AND knowing exactly what to do next.

---

### MODE DETECTION

- If `$ARGUMENTS` is a **file**: single article/page mode.
- If `$ARGUMENTS` is a **folder**: batch mode — use **AskUserQuestion** to let the user pick which files:
  - Question: "Which files should I enrich?"
  - `multiSelect: true`
  - List all content files in the folder (`.md`, `.mdx`, `.astro`) with their title from frontmatter as description
  - Pre-select all files
- If no argument: use **AskUserQuestion** to help the user pick:
  - Question: "What content should I enrich?"
  - `multiSelect: false`
  - Scan for content directories (`src/content/`, `src/pages/`, `content/`) and list them as options
  - Include a "Specific file" option — if selected, ask for the path

---

### PHASE 1: UNDERSTAND THE CONTENT

1. Read the target file(s).
2. Identify for each piece:
   - **Topic**: What specific subject does this cover?
   - **Audience**: Who is reading this? What's their skill level? What problem are they solving?
   - **Intent**: Is the reader researching, comparing, learning, or ready to act?
   - **Current quality**: Is it thin/outdated/generic, or already solid but could be sharper?
   - **Language**: French or English? Match it exactly.
   - **Content type**: Blog post, tutorial, product page, landing page, documentation?

---

### PHASE 2: RESEARCH

For each piece of content, search the web for:

1. **Current data & stats** — Find the latest numbers, benchmarks, studies (2024-2026). Replace any outdated stats. Cite sources naturally with inline links.
2. **Technical accuracy** — Verify claims, API references, tool versions, framework features. If something has changed (new API, deprecated method, better alternative), update it.
3. **What the competition covers** — Search the same topic. Identify what the top 3 results include that this content doesn't. Fill those gaps.
4. **Real examples & case studies** — Find concrete examples, real company stories, actual results. Generic advice is forgettable; specific examples stick.
5. **Expert quotes or frameworks** — Find a relevant expert perspective, mental model, or methodology to reference (not just random quotes for decoration).

Use `WebSearch` and `mcp__exa__web_search_exa` for research. Search in the **same language** as the content (French topics → French queries + English queries for technical depth).

---

### PHASE 3: REWRITE

Apply these principles to every piece of content:

#### Be the reader's smartest friend
- Write like you're explaining to a colleague over coffee — knowledgeable but never condescending.
- Anticipate their questions. Answer them before they ask.
- Use "you" constantly. This is about them, not about us.
- Acknowledge their pain points honestly before offering solutions.

#### Make it technically credible
- Every claim backed by data, a source, or a concrete example.
- Include specific numbers: "reduces load time by 40%" not "improves performance."
- Name the tools, versions, and methods. Vague = useless.
- If something is nuanced or "it depends," say so and explain when each option applies.
- Link to official docs, studies, or authoritative sources inline (not in a footnote nobody reads).

#### Make it scannable and structured
- **Hook in the first 2 sentences**: State the problem or outcome. No throat-clearing intros.
- **Subheadings that tell a story**: A reader skimming headings should get 80% of the value.
- **Short paragraphs** (2-3 sentences max). One idea per paragraph.
- **Bullet points and numbered lists** for steps, comparisons, checklists.
- **Bold key phrases** so the scanner catches the important bits.
- **TL;DR or key takeaway** at the top for long articles (> 1500 words).

#### Push to action — every single time
- End every major section with a micro-CTA or next step.
- The conclusion is NOT a summary. It's a launchpad: "Here's what to do right now."
- Be specific: "Open your terminal and run `npx create-astro`" not "consider trying Astro."
- For business content: tie every insight to revenue, time saved, or growth.
- For technical content: tie every concept to a concrete implementation step.
- Include a **"Start here" box** or **"Quick win"** callout for readers who want immediate results.

#### Make it feel alive
- Use current examples (2024-2026, not 2020 case studies).
- Reference real tools, real companies, real numbers.
- Include before/after comparisons where applicable.
- Add context: "This matters because..." — connect the dots for the reader.
- No filler. Every sentence must earn its place. If a paragraph says "X is important," delete it and show WHY it's important.

---

### PHASE 4: ENRICH WITH EXTRAS

Where appropriate, add:

- [ ] **Comparison tables** — for tool/framework/approach comparisons
- [ ] **Step-by-step instructions** — numbered, with expected outcomes at each step
- [ ] **Code snippets** — working, copy-paste ready, with comments explaining the "why"
- [ ] **Callout boxes** — for warnings, pro tips, or "common mistakes"
- [ ] **Internal links** — connect this content to other relevant pages on the same site
- [ ] **Updated stats with sources** — inline links to authoritative sources
- [ ] **FAQ section** — address the long-tail questions people actually search for
- [ ] **Estimated reading time** — in frontmatter if the framework supports it

---

### PHASE 5: CONVERSION LAYER

Every piece of content should serve the business. Add naturally (not forced):

- [ ] **Contextual CTA** — related to what the reader just learned (not a random product plug)
- [ ] **Lead magnet hook** — "Want the full checklist? Get it free..." (if the site has email capture)
- [ ] **Social proof** — mention user count, client results, or testimonials where relevant
- [ ] **Next content** — link to the logical next article/page in the reader's journey
- [ ] **Author credibility** — brief mention of why this author/company knows this topic

Do NOT make content feel like a sales page. The value comes first. The CTA is a natural extension of the value.

---

### PHASE 6: QUALITY CHECK

Before finishing, verify:

- [ ] All added stats have a source link (no unattributed claims)
- [ ] All code snippets are syntactically correct and up to date
- [ ] No broken links or placeholder URLs
- [ ] Frontmatter is complete (title, description, date updated, tags)
- [ ] Meta description is rewritten to match the upgraded content
- [ ] Reading flow is smooth when read top-to-bottom
- [ ] The piece passes the "so what?" test — every section answers why the reader should care

---

### PHASE 7: REPORT

For single files:
```
ENRICHED: [article title]
─────────────────────────────────────
Topic:           [subject]
Audience:        [who + intent]
Language:        [FR/EN]
Sources added:   X (from Y web searches)
Stats updated:   X
Sections added:  [list]
CTAs added:      X
Word count:      before → after
─────────────────────────────────────
Key changes:
• [change 1]
• [change 2]
• ...
```

For folders:
```
ENRICHED: [folder] — X/Y files upgraded
═══════════════════════════════════════
  article-1.md     ✓  +X sources, +Y words
  article-2.md     ✓  +X sources, +Y words
  article-3.md     ⏭  skipped (already strong)
  ...
═══════════════════════════════════════
Total sources added:  X
Total stats updated:  X
Total CTAs added:     X
```

---

### IMPORTANT

- **Language matching is sacred.** French content stays French. English stays English. Research in both languages for depth, but write in the content's language.
- **For French sites** (webinde, siteweb---transformemavie): respect the existing editorial conventions in CLAUDE.md (tutoiement, heading format "TECHNIQUE : MÉTAPHORE", scientific sources with natural links, never delete existing content).
- **Never invent stats.** If you can't find a source, say "according to industry benchmarks" or skip it. A wrong number destroys trust.
- **Never delete the author's voice.** Enhance structure, add data, sharpen the message — but keep THEIR personality. You're a co-writer, not a replacement.
- **Batch mode prioritization:** In a folder, process high-traffic pages first (homepage, pillar content) before long-tail articles. Skip files that are already strong — say so in the report.
- **Update the frontmatter `date`** or `lastUpdated` field to today when content is significantly changed.
- **Accents français obligatoires.** Lors de toute création ou modification de contenu en français, vérifier systématiquement que TOUS les accents sont présents et corrects (é, è, ê, à, â, ù, û, ô, î, ï, ç, œ, æ). Les accents manquants sont une faute d'orthographe. Relire chaque texte produit pour s'assurer qu'aucun accent n'a été oublié — c'est une erreur très fréquente à corriger impérativement.
