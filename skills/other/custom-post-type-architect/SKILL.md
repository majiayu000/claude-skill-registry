---
name: custom-post-type-architect
description: "Design and create WordPress custom post types end to end — CPT + supporting taxonomies + ACF field group + sample entries + builder-specific single template suggestion. Uses new v7.1 MCP tools: respira_create_post_type, respira_create_taxonomy, respira_create_acf_field_group."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: content-creation
---

# Custom Post Type Architect

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** content-creation
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + MCP server

---

## Description

Given a brief — "I need a portfolio with case studies" or "we run a podcast and want each episode to be its own page" — design and create the WordPress custom post type, supporting taxonomies, and ACF field group end to end. Uses the new v7.1 MCP tools: `respira_create_post_type`, `respira_create_taxonomy`, `respira_create_acf_field_group`.

The output is a fully wired content architecture, ready to use:

1. The CPT itself (labels, supports, public-vs-private, has_archive, REST exposure)
2. Supporting taxonomies (e.g. industries for case studies, seasons for podcast episodes)
3. ACF field group bound to the CPT (custom fields the editor sees)
4. 1–2 sample entries so the agent can verify the rendering
5. Builder-aware single-template suggestion for the active builder

---

## When to Use

- Setting up a portfolio, case studies, team members, events, podcast episodes, recipes, properties, locations, products-but-not-WooCommerce, FAQs, testimonials, courses, lessons, or any structured content type
- Migrating away from custom-fields-in-posts to a proper content type
- Auditing an existing site that's overloaded the default "post" type with non-blog content

---

## Trigger Phrases

- "create a custom post type"
- "build a portfolio"
- "set up a case study type"
- "add a team members section"
- "scaffold a CPT"
- "create a podcast post type"
- "build an events section"
- "we need a new content type"

---

## Execution Workflow

### Step 1 — Confirm site + builder

Call `respira_get_active_site` and `respira_get_builder_info`. The builder choice affects Step 6 (template suggestion).

### Step 2 — Understand the brief

Ask the user three short questions if not already clear from their request:

1. **What is the content?** (case studies, podcast episodes, team, events, ...)
2. **How is it organized?** (categories, tags, custom taxonomies — e.g. case studies organized by industry + service-type)
3. **What fields does each entry need?** (e.g. case study: client name, hero image, deliverables, outcomes, before/after metrics, related case studies)

If the user can't articulate the fields, propose a default set based on the content type. Default sets:

- **Case studies:** client name, industry (taxonomy), service-type (taxonomy), hero image, brief, deliverables, outcomes, key metrics (3-5), client logo, related case studies (relationship)
- **Team members:** name, role, bio, headshot, social links (LinkedIn / X / personal site), department (taxonomy)
- **Events:** title, date/time, location, address, virtual/in-person, registration URL, capacity, hero image
- **Podcast episodes:** title, episode number, season (taxonomy), audio file URL, duration, show notes, guest name, guest links
- **Properties (real estate):** address, price, bedrooms, bathrooms, sqm, status (taxonomy: for-sale / sold / under-offer), gallery, neighborhood (taxonomy)
- **Recipes:** title, prep time, cook time, servings, ingredients (repeater), steps (repeater), category (taxonomy), cuisine (taxonomy), difficulty, dietary tags

### Step 3 — Design the CPT shape

Output the proposed shape for user review:

```markdown
## Proposed CPT: `case_study`

- **Singular label:** Case Study
- **Plural label:** Case Studies
- **Menu icon:** dashicons-portfolio
- **Public:** yes
- **Has archive:** yes (URL: /case-studies/)
- **Supports:** title, editor, thumbnail, excerpt, revisions
- **REST API:** exposed (so the builder + Respira can read/write)
- **Hierarchical:** no
- **Show in admin menu:** yes, position 25 (under Pages)

## Supporting taxonomies

1. `case_study_industry` — Industries (e.g. SaaS, e-commerce, healthcare)
2. `case_study_service` — Service types (e.g. branding, website, copywriting)

## ACF field group: `Case Study Fields`

- Hero image (image, required)
- Client name (text, required)
- Brief (textarea)
- Deliverables (repeater — title + description)
- Outcomes (repeater — metric name + before + after)
- Client logo (image)
- Related case studies (relationship → case_study)
```

Wait for confirmation. The user might want to add or remove fields.

### Step 4 — Create the CPT + taxonomies

After confirmation, run the create calls:

1. `respira_create_post_type` — creates the CPT with the proposed shape
2. `respira_create_taxonomy` — once per supporting taxonomy, bound to the CPT
3. `respira_create_acf_field_group` — the ACF field group, bound to the CPT via location rules

Each call should report back: "✓ Created CPT `case_study`" / "✓ Created taxonomy `case_study_industry`" / "✓ Created ACF field group with 8 fields bound to `case_study`."

### Step 5 — Generate sample entries

Create 1–2 sample entries so the user can immediately see the CPT working in the admin and the editor renders correctly. Use `respira_create_custom_post` with realistic but generic content (no real customer names — generic personas like "BrandQ" or "agency-A").

The sample entries should populate every ACF field so the user can see the full shape.

### Step 6 — Suggest a builder-specific single template

Based on the active builder, suggest where to create the single template:

- **Bricks:** "Create a single template at Templates → Add New → Type: Single → Conditions: Post Type = case_study. Suggested elements: ..."
- **Elementor:** "Create a single template at Templates → Theme Builder → Single → Add Conditions → Posts: case_study. Suggested widgets: ..."
- **Divi:** "Create a Theme Builder template at Divi → Theme Builder → Add Template → Posts: case_study. Suggested modules: ..."
- **Gutenberg / FSE theme:** "Create a single-case_study.html template in the theme or via Appearance → Editor → Templates → Add → Single Item: Case Study."
- **Oxygen / Breakdance:** "Create a Single template targeting case_study."

If the user wants to scaffold the template now, offer to build it: that's a separate skill flow (use `respira_build_page` against the single template surface for the chosen builder).

### Step 7 — Verify

Output a summary with:

- The CPT slug + admin URL (`/wp-admin/edit.php?post_type=case_study`)
- The archive URL on the front-end (`/case-studies/`)
- The 2 sample entry URLs
- A note about whether the single template was scaffolded or left for the user

---

## Hard rules

- Always ask before creating. The CPT shape preview in Step 3 is mandatory. Customers will be writing into this CPT for years — get it right the first time.
- Use snake_case slugs (`case_study`, `case_study_industry`) — never spaces or hyphens. WordPress CPT slugs have a 20-character hard limit.
- Always expose `show_in_rest` so the builder + Respira can read/write the CPT. If `show_in_rest` is false, the post type is invisible to the REST API and most modern builders break on it.
- Never name a CPT `post`, `page`, `attachment`, `revision`, `nav_menu_item`, `custom_css`, `customize_changeset`, `oembed_cache`, `user_request`, `wp_block`, `wp_template`, `wp_template_part`, `wp_global_styles`, `wp_navigation` — these are reserved.
- ACF field group location rules must bind to the CPT (`post_type == case_study`), not to a category or template. Wrong location rule = fields invisible in the admin.
- Sample entries use generic personas. Never use real customer names from memory or any other source.

---

## Telemetry

Records: site URL hash, CPT slug created, taxonomy count, ACF field count, builder active, sample entries created, success/failure. No CPT names, no field values, no content sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`
