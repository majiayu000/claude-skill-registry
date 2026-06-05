---
name: kai-product-maker
description: Build a Gumroad-ready digital product from scratch — ebook, card deck, playbook, Notion template, or flipbook. Walks from concept → content outline → design brief → per-item markdown → images → multi-format build (PDF, HTML flipbook, Notion, card deck) → Gumroad sales page + email blast + launch assets. Use when "make a digital product", "build an ebook", "create a playbook", "card deck", "notion template product", "gumroad product", "make a pdf to sell", or any request to ship a sellable information product.
---

Ship a Gumroad-ready digital product following the same process used for **The Algorithm Engine** (TikTok ebook), **The Approval Engine** (Notion card deck), and **The Comment Connor Playbook** (HTML flipbook + PDF). Three examples, one process.

## When to use

- User has a topic + an audience and wants a polished, sellable product ($7-$97 range)
- User has research or content drafts but no structure, images, or sales page
- User wants to turn a TikTok hit / blog post / consulting framework into a paid deliverable

## When NOT to use

- User wants a free lead magnet only → `/kai-write` or `/kai-landing-page`
- User already has a finished PDF and just needs a sales page → `/kai-write` (press/sales copy)
- User wants a SaaS-level product (not information) — this skill is for static digital goods

## Examples to read

Before planning, skim these three completed products — they're the ground truth for what "done" looks like:

| Example | Format | Price | Location |
|---------|--------|-------|----------|
| **Algorithm Engine** | 9-chapter PDF ebook + system prompt | $47-67 | `E:\Dev2\DigitalProduct\AlgoProduct\` |
| **Approval Engine** | Mobile-first Notion card deck (30 cards) | $37 | `E:\Dev2\DigitalProduct\ApprovalEngine\` |
| **Comment Connor Playbook** | HTML flipbook + PDF (20 workflows) | $37 | `E:\Dev2\DigitalProduct\CommentConnorPlaybook\` |

Each has the same scaffolding: numbered `content/*.md`, `images/`, `PRODUCT_BRIEF.md`, `BUILD_PROMPT.md`, build script, sales copy, production checklist.

---

## Phase 0: Load Product Context

Check `MARKETING.md` in project root for voice, audience, positioning. If absent, run `/kai-start` or get from user: what you sell, ICP, brand voice, distribution channels.

---

## Phase 1: Product Concept (one short discovery pass)

Ask only what isn't already answerable from MARKETING.md / prior context:

1. **Working title + subtitle** (can change at the end)
2. **One-sentence promise** — what changes for the reader after they finish?
3. **Format** — pick one primary:
   - **PDF ebook** — linear read, 30-80 pages (ref: Algorithm Engine)
   - **HTML flipbook + PDF** — illustrated, page-by-page, designed (ref: Comment Connor)
   - **Notion card deck** — mobile-first, scannable snippets, 20-50 cards (ref: Approval Engine)
   - **Template pack** — fill-in worksheets / prompts (usually a bolt-on, not standalone)
4. **Price point** — $7 / $17 / $27 / $37 / $47 / $67 / $97 — higher price means more production polish, not more pages
5. **Unit count** — chapters / workflows / cards / templates (affects scope everywhere downstream)
6. **Source material** — TikTok script / blog series / consulting framework / research doc — where does the content come from?

Output: one-paragraph concept in user's voice. Get approval before moving on.

---

## Phase 2: Folder Scaffold

Create at `E:\Dev2\DigitalProduct\<ProductName>\` with this shape:

```
<ProductName>/
├── PRODUCT_BRIEF.md              # design + spec (Phase 3)
├── BUILD_PROMPT.md               # how to assemble deliverables (Phase 6)
├── content/                      # numbered source files (Phase 4)
│   ├── 00_cover_intro.md
│   ├── 01_<topic>.md
│   └── ...
├── images/                       # cover, dividers, per-item art (Phase 5)
│   ├── character_reference.png   # if illustrated
│   ├── cover.png
│   └── ...
├── Research/                     # source notes (optional)
├── GUMROAD_SALES_COPY.md         # Phase 7
├── EMAIL_BLAST.md                # Phase 7
├── PRODUCTION_CHECKLIST.md       # Phase 8
└── VIDEO_SCRIPTS.md              # launch content (optional)
```

Naming convention: `00_` prefix for front matter, `01_`-`NN_` for items in reading order. Zero-pad so files sort correctly.

---

## Phase 3: PRODUCT_BRIEF.md (design spec — do this BEFORE content)

Lock design choices up front so every asset is consistent. Copy the structure from `E:\Dev2\DigitalProduct\CommentConnorPlaybook\PRODUCT_BRIEF.md`. Minimum sections:

1. **What you're building** — one paragraph, tone matches the product (tactical manual / corporate tool / field guide)
2. **Aesthetic direction** — one named mood ("Tactical Field Manual", "Corporate Cool", "Academic Textbook", "Zine") + 3-5 mood references
3. **Color palette** — bg / surface / border / primary text / dim text / accent / danger / success. 6-8 hex codes
4. **Typography** — headline font, body font, code/prompt font (use Google Fonts for HTML; pair with system-font fallbacks). Italics, stamps, letter-spacing rules
5. **Page/card layout** — what goes where on a typical page/card. Include per-page element list
6. **Page sequence** — full doc outline front-to-back (cover → inside cover → TOC → sections → back cover)
7. **Image specs** — character reference, cover dimensions, per-item style, consistency rules
8. **Distribution formats** — which files get shipped (PDF, HTML, Notion, CSV, zip bundle)

Get user approval on the brief before producing content. Design inconsistency is the #1 reason products feel cheap.

---

## Phase 4: Content Production (the actual product)

One markdown file per unit (chapter / workflow / card). **Structure every file the same way** — consistency is the signal of quality.

For an **ebook-style chapter**, use:
- `## Chapter Title` (H2)
- One-paragraph setup
- Numbered or bulleted body
- "Watch out for" / "What NOT to do" callout
- "Why this works" callout
- Links forward to next chapter

For a **card/workflow** (Approval Engine / Comment Connor pattern):
- `## Situation` — when to reach for this
- `## Goal` — what success looks like
- `## What NOT to say` — anti-pattern
- `## Use this instead` — the actual script/prompt (in code block)
- `## Why this works` — one-sentence rationale
- Tags / category at the end

Content rules:
- **Every piece of content must live in `content/*.md`.** The build is downstream of content — never edit assembled HTML/PDF directly
- Keep each file self-contained (reader can land on it cold)
- Ship examples, not theory — real screenshots, real numbers, real scripts
- If facts matter (statistics, patent numbers, quotes), put a `Research/` folder beside `content/` and cite sources

Quality gate: after every 5 items produced, run `/kai-gate` for a Four U's score (target 12+/16). Pause to fix before producing more.

---

## Phase 5: Images (do these LAST among production assets)

Images are expensive in tokens and iteration time — lock content and brief first.

**Minimum set** (varies by format):

| Asset | Purpose | Notes |
|-------|---------|-------|
| `character_reference.png` | Consistency sheet | If using a character/mascot. Not shipped, just for prompt consistency |
| `cover.png` | Gumroad thumbnail + product cover | 1600×900 for Gumroad; 2:3 portrait for PDF cover |
| `cat_<name>.png` × N | Category dividers | One per section cluster |
| `01_<slug>.png` × N | Per-item illustration | Same character/style across all |
| `Product_Thumbnail.png` | Gumroad square | 400×400 |

Generation: prompt the image model with the character reference and the aesthetic from PRODUCT_BRIEF.md. Batch-generate, then review for consistency — kill any drift before moving on. Reference Comment Connor's `generate_images.py` for a batch script pattern.

---

## Phase 6: BUILD_PROMPT.md + Build

Write `BUILD_PROMPT.md` — a self-contained prompt a fresh Claude Code session can follow to produce the final deliverables from `content/` + `images/` + `PRODUCT_BRIEF.md`. Structure (copy from `CommentConnorPlaybook/BUILD_PROMPT.md`):

1. **What exists** — list content/images/brief files the build must read
2. **What to build** — one section per deliverable
3. **Do not regenerate** — warn off redoing completed work

Then run the build. Format-specific scripts:

| Format | Tool | Reference |
|--------|------|-----------|
| **PDF ebook** | pandoc + xelatex, or merge-pdfs from per-section PDFs | `AlgoProduct/merge_pdfs.py` + `AlgoProduct/HOW_TO_COMBINE_PDFS.md` |
| **HTML flipbook** | Self-contained HTML file, images as base64, keyboard + touch nav | `CommentConnorPlaybook/build_html.py` |
| **HTML print version** | Same HTML but `@page` + print CSS, browser-to-PDF export | `CommentConnorPlaybook/build.py` |
| **Notion card deck** | `setup_notion.py` + CSV import | `ApprovalEngine/setup_notion.py` + `NOTION_IMPORT.csv` |

Verify the build by opening the deliverable yourself (or via `/browse`) before moving on.

---

## Phase 7: Sales + Launch Assets

Four files to write, in this order:

1. **`GUMROAD_SALES_COPY.md`** — full sales page. Structure from `AlgoProduct/GUMROAD_SALES_COPY.md`:
   - Headline + subheadline
   - Section 1: The hook (problem framed painfully)
   - Section 2: The reveal (what you found / built)
   - Section 3: Proof (screenshots, numbers, case study)
   - Section 4: What's inside (bullet list)
   - Section 5: Who this is for / NOT for
   - Section 6: Price anchor + CTA
   - Guarantee + PS

2. **`EMAIL_BLAST.md`** — 3-email launch sequence (tease → launch → last-call). Mirror the sales page hook.

3. **`COVER_IMAGE_PROMPT.md`** — the exact image-model prompt you used. Saves regenerating later.

4. **`VIDEO_SCRIPTS.md`** — 1-2 short video scripts for TikTok/Reels launch (hook-first, 30-60s). Compose with `/kai-video` for this step.

Final sales-copy gate: run `/kai-gate` against the sales copy with the "sales" profile. Pass Four U's, no banned words, clear CTA.

---

## Phase 8: Package + Launch Checklist

Create the **customer-facing zip** at `<ProductName>/<ProductName>_Package/` with exactly what the buyer downloads. Pattern from `AlgoProduct/CUSTOMER_PACKAGE_STRUCTURE.md`:

```
<ProductName>_Package/
├── START_HERE.txt              # First thing the customer reads
├── <ProductName>_MAIN.pdf      # The core deliverable
├── <bonus files>               # System prompts, templates, checklists
└── README.md                   # What's inside + how to use
```

Then ship `PRODUCTION_CHECKLIST.md` with CRITICAL / IMPORTANT / NICE-TO-HAVE tasks. Copy structure from `AlgoProduct/PRODUCTION_CHECKLIST.md` — it already has the right shape (🔴🟡🟢 priority, time estimates, tool names, "why this matters" per item).

Final launch gate:
- [ ] Brief matches finished product (no design drift)
- [ ] All content files referenced in build are in `content/`
- [ ] Images consistent with character reference
- [ ] PDF renders cleanly end-to-end (TOC links work, no widow/orphan disasters)
- [ ] Sales copy scored 12+/16 on Four U's
- [ ] Zip package contains only customer-facing files (no source research, no old drafts)
- [ ] Gumroad product draft created with thumbnail + sales copy + file upload
- [ ] 3 launch emails queued
- [ ] 1 launch video scripted

---

## Composition with other kai skills

| Step | Composes with |
|------|---------------|
| Define voice before writing | `/kai-brand` |
| Write any single content file | `/kai-write` |
| Score content quality | `/kai-gate` |
| Launch video scripts | `/kai-video` / `/kai-video-production` |
| Launch email sequence | `/kai-email-system` |
| Turn one product into 15+ social assets | `/kai-repurpose` |
| Find who else has bought similar products | `/kai-competitors` |

## Red flags

- **Content inconsistency between items** — each file should have the same structure. If they drift, the product feels amateur
- **Image drift** — character/style slips across illustrations. Fix by pinning character reference in every image prompt
- **Scope creep mid-production** — resist adding a 10th chapter when 9 was the plan. Ship, then release 1.1
- **Writing the sales copy before content is done** — you don't know what you're selling yet. Sales copy comes last
- **Shipping without a launch video** — no video = no traffic = dead Gumroad listing
