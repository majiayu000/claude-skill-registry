---
name: page-template-library
description: "Capture canonical page patterns (case study, service page, landing page hero + 3-up + CTA) as re-usable playbooks. Uses new v7.1 MCP tools respira_create_playbook + respira_list_playbooks + respira_update_playbook. Future page-generation skills spawn new pages from playbooks in seconds."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: workflow
---

# Page Template Library Bootstrapper

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** workflow
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + MCP server

---

## Description

Most WordPress sites have a few "canonical" page patterns the team builds over and over: the case study layout, the service page layout, the landing page hero + 3 sections + CTA layout, the team-member single layout. This skill captures those patterns as re-usable **playbooks** using the new v7.1 MCP tools (`respira_create_playbook`, `respira_list_playbooks`, `respira_update_playbook`).

Once captured, future page-generation skills (or the user directly) can spawn a new page from a playbook in seconds, on-brand, with the right structure — no more "build it from scratch every time."

---

## What it produces

A library of named playbooks on the site, each describing:

1. **Structure** — the section pattern (hero → 3-up grid → quote → CTA, etc.)
2. **Components per section** — which builder modules/widgets to use
3. **Tokens used** — references to the site's design system (primary color, heading typography, etc.)
4. **Variable slots** — the fields the user fills in when spawning a new page from this playbook (title, hero image, key stat, body copy, etc.)
5. **Builder lock** — which page builder this playbook targets (a Bricks playbook isn't portable to Elementor)

---

## When to Use

- Setting up a new site that will repeat similar page types (agency portfolio sites: case studies repeated; SaaS sites: feature pages repeated)
- After building 3+ pages with the same pattern manually — capture the pattern so the next one is instant
- Migrating from "every page hand-built" to a templated workflow
- Auditing an existing site — if you find 8 pages following the same loose pattern, capture it as a playbook so future pages snap

---

## Trigger Phrases

- "save this as a template"
- "create a playbook from this page"
- "capture this layout"
- "make a reusable template from this"
- "build a page template library"
- "save this page pattern"
- "extract the playbook"

---

## Execution Workflow

### Step 1 — Confirm site + builder

Call `respira_get_active_site` and `respira_get_builder_info`. Playbooks are builder-specific. Note the active builder — the playbook will be locked to it.

### Step 2 — Identify the source page

Two modes:

**Mode A — Capture from an existing page.** User says "save this page as a template." Get the page ID from the conversation context or ask the user which page (`respira_list_pages` for selection).

**Mode B — Capture from a pattern across multiple pages.** User says "all our case studies follow the same pattern — capture it." Call `respira_list_custom_posts(post_type=case_study)` (or `respira_list_pages` filtered by parent or template). Sample 3–5 of them and identify the common structure.

### Step 3 — Extract the structure

For Mode A (single page):

1. `respira_extract_builder_content(page_id)` — get the builder-native structure
2. Walk the tree, identify the section pattern (hero / stats / 3-up / quote / CTA / etc.)
3. Note which modules each section uses
4. Identify variable content (what should be a slot) vs static content (what's structural)

For Mode B (pattern across pages):

1. Extract each sample page's structure
2. Diff them. Sections present in all samples → structural. Sections present in some → optional. Sections unique to one → user-specific content (slot candidates).
3. The common spine becomes the playbook structure. The variable parts become slots.

### Step 4 — Identify slots

Slots are the fields the user fills in when spawning a new page from the playbook. Typical slots:

- **Title slot** (almost always)
- **Hero image slot**
- **Hero subtitle slot**
- **Headline slot** (the H1)
- **Body content slot** (long-form text region)
- **Key stat slots** (numbered stats with labels)
- **CTA text slot + CTA URL slot**
- **Related items slot** (a list — for related case studies, etc.)

Each slot has a type (text / image / number / URL / repeater) and an optional default value.

### Step 5 — Pull design system tokens

If `respira_get_option('respira_design_system')` returns a saved design system, reference its tokens in the playbook. E.g. instead of hard-coding `#2563EB`, reference `{design_system.colors.primary}`. The playbook becomes drift-resistant — if the design system updates, every page spawned from the playbook reflects the new tokens.

### Step 6 — Propose the playbook to the user

Output the proposed playbook shape:

```markdown
## Proposed playbook: `case_study_v1`

**Targets:** Bricks 1.12 (locked)
**Sections:** 5 — Hero / Stats / Body / Quote / CTA
**Design system bound:** yes (uses primary, secondary, accent + heading typography)

### Slots (the user fills these when spawning a new page)

1. **client_name** (text, required) — e.g. "Acme Studio"
2. **hero_image** (image, required) — full-width hero
3. **subtitle** (text, optional) — short kicker above the H1
4. **headline** (text, required) — the H1
5. **stats** (repeater × 3, required) — number + label per stat
6. **body** (long_text, required) — the main case study narrative
7. **client_quote** (text, optional) — pulled quote from the client
8. **client_quote_author** (text, optional)
9. **cta_text** (text, default: "Start a project") — final CTA button
10. **cta_url** (url, default: "/contact/")

### Structure (the section spine)

1. **Hero** — full-width, centered. Uses `subtitle` + `headline` + `hero_image`.
2. **Stats** — 3-up grid. Uses `stats` repeater. Colors from design system.
3. **Body** — single-column, max-width 720px. Uses `body`.
4. **Quote** — large pull quote. Uses `client_quote` + `client_quote_author`. Optional — skipped if `client_quote` empty.
5. **CTA** — centered, on accent background. Uses `cta_text` + `cta_url`.
```

Ask: *"Save this playbook? Anything to change?"*

### Step 7 — Persist the playbook

After confirmation, call `respira_create_playbook` with the structure + slots + design-system bindings.

Then: *"Playbook `case_study_v1` saved. To spawn a new case study from it, say: `build a new case study from playbook` or call `respira_get_playbook('case_study_v1')` and then `respira_build_page` with the slot values."*

### Step 8 — Optional: spawn one sample

Offer to spawn one new page from the playbook immediately as a sanity check. Use realistic but generic slot values (no real customer names). User confirms it renders correctly → playbook is verified.

---

## How other skills use playbooks

A future skill ("spawn a page from playbook X") can:

1. Call `respira_get_playbook(slug)` to get the structure + slots
2. Collect slot values from the user
3. Call `respira_build_page` with the playbook structure populated with the slot values
4. Resulting page is on-brand (design system bound), correctly structured, and ready for content

The playbook + design system + brand voice trio is the foundation for the whole content-generation suite. Build this once per site, harvest forever.

---

## Hard rules

- Playbooks are builder-specific. A Bricks playbook cannot be applied to an Elementor site. The skill must record the builder lock and refuse to spawn against a different builder.
- Playbooks reference the design system by token name, not by hex value. This makes them drift-resistant.
- Slot names use snake_case. Slot types are constrained to: `text`, `long_text`, `image`, `url`, `number`, `boolean`, `repeater`.
- A playbook with zero slots is useless. Refuse to save a playbook with no slots — that's not a template, that's a copy of an existing page.
- Never overwrite an existing playbook silently. Use `respira_list_playbooks` to check for a same-slug existing playbook; if found, show the diff and ask before updating.
- Sample entries spawned from a playbook use generic personas (BrandQ, agency-A). Never real customer names.

---

## Telemetry

Records: site URL hash, builder, playbook slug, slot count, structure section count, whether design system was bound, whether sample spawn succeeded, success/failure. No slot names, no slot values, no playbook content sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`
