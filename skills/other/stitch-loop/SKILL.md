---
name: stitch-loop
description: Iteratively build multi-page websites using Stitch. Reads next-prompt.md (the baton), generates the next page with Stitch MCP, integrates it into the site, then updates next-prompt.md to continue the loop. Works with stitch-design-md and stitch-ui-prompt-architect for consistent multi-page output.
allowed-tools:
  - "stitch*:*"
  - "Bash"
  - "Read"
  - "Write"
---

# Stitch Build Loop

**Constraint:** Only use this skill when the user explicitly mentions "Stitch" and multi-page or iterative site building.

You are an **autonomous frontend builder** in an iterative site-building loop. Each iteration: (1) Read the baton, (2) Generate a page with Stitch MCP, (3) Integrate into the site, (4) Write the next baton so the loop continues.

## Prerequisites

- Stitch MCP Server (see `stitch-setup` skill or https://stitch.withgoogle.com/docs/mcp/guide/)
- `DESIGN.md` — generate with `stitch-design-system` from an existing screen (required for consistency)
- `SITE.md` — site vision, Stitch project ID, sitemap, roadmap (create if missing)

## The baton system

`next-prompt.md` is the relay baton between iterations. It tells the loop what page to build next.

### Baton format

```markdown
---
page: about
---

**DESIGN SYSTEM (REQUIRED):**
[Paste DESIGN.md Section 6 here verbatim]

**Page request:**
About page with company mission, team section (3 people), and timeline.
```

**Rules:**
- `page` frontmatter → output filename (`about.html`)
- The body **must** include the design system block from `DESIGN.md` Section 6
- You **must** update `next-prompt.md` at the end of every iteration — the loop stops if this is missing

---

## Execution protocol

### Step 1 — Read the baton

Parse `next-prompt.md`:
- Extract `page` from YAML frontmatter
- Extract the full prompt body (including the design system block)

### Step 2 — Consult context files

| File | What to look for |
|------|-----------------|
| `SITE.md` | Stitch project ID (Section 2), sitemap (Section 3), roadmap / next pages (Section 4), creative freedom (Section 5) |
| `DESIGN.md` | Section 6 — copy this into every prompt, not just the current one |

**Check:** Do not rebuild pages already in `SITE.md` sitemap. Do not deviate from the visual language in `DESIGN.md`.

### Step 3 — Generate with Stitch

1. Run `list_tools` → find Stitch MCP prefix
2. If `stitch.json` exists, use stored `projectId` — do not create a new project
3. If no `stitch.json`, call `create_project` → save numeric ID to `stitch.json`
4. Call `generate_screen_from_text`:
   - `projectId`: numeric ID (no `projects/` prefix)
   - `prompt`: full baton content including DESIGN SYSTEM block
   - `deviceType`: match what's in `SITE.md` or `DESIGN.md`
5. Call `get_screen` with numeric projectId + screenId
6. Download HTML: `bash scripts/fetch-stitch.sh "[htmlCode.downloadUrl]" "queue/[page].html"`
7. Download screenshot: save to `queue/[page].png`

### Step 4 — Integrate into site

1. Move `queue/[page].html` → `site/public/[page].html`
2. Fix asset paths (make relative to `site/public/`)
3. Wire navigation: replace `href="#"` placeholders with real paths to existing pages
4. Ensure the header/footer matches other pages in the site

### Step 4.5 — Visual verification (if Chrome DevTools MCP available)

If `chrome*` tools are in `list_tools`:
1. Start local server: `npx serve site/public -p 3000`
2. Navigate to `http://localhost:3000/[page].html`
3. Take screenshot, compare against `queue/[page].png`
4. Stop server

### Step 5 — Update SITE.md

- Add `[x] [page].html` to the sitemap
- Remove consumed ideas from creative freedom section
- Update roadmap if a backlog item was completed

### Step 6 — Write the next baton (CRITICAL)

**You must update `next-prompt.md` before completing — the loop stalls if you skip this.**

1. Pick next page from: sitemap → roadmap → creative freedom → or invent one that fits
2. Write `next-prompt.md` with:
   - Valid YAML frontmatter (`page: <next-page-name>`)
   - `**DESIGN SYSTEM (REQUIRED):**` block copied verbatim from `DESIGN.md` Section 6
   - Clear page description

---

## File structure

```
project/
├── next-prompt.md       ← Baton (current task; updated each iteration)
├── stitch.json          ← Stitch project ID (persist between loops!)
├── DESIGN.md            ← From stitch-design-system
├── SITE.md              ← Vision, sitemap, roadmap
├── queue/               ← Staging: [page].html, [page].png
└── site/
    └── public/          ← Production: index.html, about.html, etc.
```

---

## SITE.md template

```markdown
# Site Vision

[One paragraph describing the site's purpose, audience, and overall feeling]

## Stitch Project

- **Project ID (numeric):** [ID from stitch-mcp-create-project]

## Sitemap

- [ ] index.html — Home
- [ ] about.html — About
- [ ] contact.html — Contact

## Roadmap

1. index.html — main landing page
2. about.html — company/team info
3. contact.html — contact form

## Creative freedom

Additional pages or sections not yet planned...
```

---

## Common pitfalls

- ❌ Forgetting to update `next-prompt.md` (loop stops)
- ❌ Rebuilding a page already in SITE.md sitemap
- ❌ Omitting `DESIGN.md` Section 6 from the prompt (causes visual drift)
- ❌ Using `projects/ID` format instead of numeric in `generate_screen_from_text`
- ❌ Leaving `href="#"` instead of wiring real page links
- ❌ Not persisting `stitch.json` (creates new project every iteration)

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Inconsistent visual styles across pages | Keep DESIGN.md updated; always copy Section 6 into baton |
| Loop stalls at next iteration | Check `next-prompt.md` has valid frontmatter and non-empty body |
| Stitch generation fails | Ensure baton includes DESIGN SYSTEM block and a specific page request |
| Broken navigation | Use relative paths for internal links; check `site/public/` structure |

---

## References

- `scripts/fetch-stitch.sh` — Reliable GCS HTML downloader
- `stitch-design-system` — Generate DESIGN.md from an existing screen
- `stitch-ui-prompt-architect` — Enhance vague baton text into structured prompts
- `docs/prd-to-stitch-workflow.md` — PRD-driven multi-screen workflow
