---
name: migrate-divi-to-breakdance
description: Converts Divi-built WordPress pages to Breakdance Builder. Parses Divi's shortcode tree from post_content, maps each module to its Breakdance element equivalent, generates a migration plan for approval, and writes Breakdance content to the target pages. Use when user says "migrate Divi to Breakdance", "switch from Divi to Breakdance", or "rebuild Divi pages in Breakdance".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Divi to Breakdance

Converts Divi-built WordPress pages to Breakdance Builder. Parses Divi's shortcode-based content from post_content, maps each module to its Breakdance element equivalent, generates a migration plan for approval, and writes Breakdance content to the target pages. Use this skill whenever someone wants to move from Divi to Breakdance, switch builders from Divi to Breakdance, or rebuild Divi pages in Breakdance.

## What This Skill Does

Divi and Breakdance take very different approaches to content storage — Divi uses nested shortcodes in `post_content`, while Breakdance uses a structured format in post meta. This skill bridges that gap by parsing the full Divi shortcode tree, understanding each module's intent, and recreating it as the appropriate Breakdance element. Breakdance was built by the Oxygen team with a focus on clean output and intuitive editing, making it a popular Divi replacement for users who want better performance without a steep learning curve.

**Handles:**
- et_pb_section → Breakdance Section element
- et_pb_row/et_pb_column → Breakdance Div elements with flex layout
- et_pb_text → Breakdance Text element
- et_pb_blurb → Breakdance Icon Box or container with children
- et_pb_image → Breakdance Image element
- et_pb_button → Breakdance Button element
- et_pb_video → Breakdance Video element
- et_pb_divider → Breakdance Separator element
- et_pb_accordion/et_pb_toggle → Breakdance Accordion element
- et_pb_tabs → Breakdance Tabs element
- et_pb_gallery → Breakdance Gallery element
- et_pb_slider → Breakdance Slider element
- et_pb_pricing_tables → Breakdance Pricing Table element
- et_pb_code → Breakdance Code element
- et_pb_counters → Breakdance Progress Bar element
- et_pb_map → Breakdance Map element
- Custom CSS → Breakdance custom CSS fields
- Column widths → Breakdance flex percentages

**Preserves:**
- All text content and inline formatting
- Image URLs, alt text, dimensions
- Typography settings (font, size, weight, line-height)
- Color values and gradients
- Spacing (margin, padding)
- Background images, overlays
- Border and shadow settings
- Button labels, URLs, targets
- CSS classes

## What This Skill Does NOT Do

- **Specialty sections** — Divi's specialty layouts need manual setup in Breakdance.
- **Global modules** — Divi's `et_pb_layout` global modules are inlined during migration. Breakdance global blocks are separate.
- **Third-party Divi modules** — Plugins extending Divi are flagged for manual recreation.
- **Divi theme customizer** — Global design settings from the Divi customizer must be configured in Breakdance's design settings.
- **Dynamic content** — Divi's dynamic features need Breakdance's dynamic data system.
- **Contact forms** — et_pb_contact_form must be rebuilt with Breakdance's form element or a forms plugin.
- **Divi Library** — Layouts in et_pb_layout post type are not migrated automatically.
- **Motion effects and animations** — Scroll effects differ between builders.
- **Theme dependency** — If using Divi theme, switching to Breakdance means using a different base theme.

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Divi theme or Divi Builder plugin active (to read source content)
- Breakdance plugin installed and active (to write target content)
- Read access to scan Divi content
- Write access to create duplicates with Breakdance content

## Trigger Phrase

- "migrate divi to breakdance"

## Alternative Triggers

- "convert divi to breakdance"
- "switch from divi to breakdance"
- "rebuild divi pages in breakdance"
- "move from divi to breakdance"
- "divi to breakdance migration"
- "replace divi with breakdance"

## Source Builder: Divi

Divi stores content as shortcodes in `post_content`:

```
[et_pb_section fb_built="1" _builder_version="4.x"]
  [et_pb_row]
    [et_pb_column type="4_4"]
      [et_pb_text]<p>Content</p>[/et_pb_text]
      [et_pb_image src="photo.jpg" alt="Photo"][/et_pb_image]
    [/et_pb_column]
  [/et_pb_row]
[/et_pb_section]
```

Key Divi specifics:
- **Hierarchy**: section → row → column → module (strict nesting)
- **Column types**: `4_4` (100%), `1_2` (50%), `1_3` (33%), `2_3` (66%), `1_4` (25%), `3_4` (75%)
- **Settings as attributes**: `background_color`, `custom_margin`, `custom_padding`
- **Content encoding**: HTML entities, percent-encoding in attribute values
- **Global modules**: `global_module` attribute referencing `et_pb_layout` post
- **Section types**: regular, fullwidth, specialty

Read Divi content via `wordpress_extract_builder_content` with `builder=divi`.

## Target Builder: Breakdance

Breakdance stores content in post meta with a structured element format.

Key Breakdance specifics:
- Elements use types like `EssentialElements\\Heading`, `EssentialElements\\Text`, `EssentialElements\\Image`
- Section and Div elements for layout structure
- Clean CSS output with minimal wrapper markup
- Built-in form builder, WooCommerce support, popup system
- Responsive design through breakpoint-specific settings
- Created by the Oxygen team — combines Oxygen's clean output with friendlier UX

Write Breakdance content via `wordpress_inject_builder_content` with `builder=breakdance`.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Confirm Divi is active via `wordpress_list_plugins` and `wordpress_get_site_context`.
3. Confirm Breakdance is installed and active via `wordpress_list_plugins`.
4. **Important**: If using Divi theme, note the user needs a compatible base theme for Breakdance.
5. Scan all content for Divi usage:
   - `wordpress_list_pages` and `wordpress_list_posts`
   - Check builder via `wordpress_get_builder_info`
6. Extract Divi content via `wordpress_extract_builder_content` with `builder=divi`
7. Build inventory:
   - Total Divi pages/posts
   - Module types (frequency count)
   - Specialty sections detected
   - Global modules referenced
   - Third-party modules
   - Content encoding issues
   - Complexity per page

### Phase 2: Migration Plan

```
## Divi → Breakdance Migration Plan

### Theme Note
[If Divi theme]: Switching from Divi theme. Breakdance works with most
themes — you'll need a lightweight base theme (Astra, GeneratePress, etc.)
or Breakdance can handle full site rendering.

### Why Breakdance
Breakdance produces significantly cleaner CSS and HTML output compared to
Divi. Built by the Oxygen team, it offers similar power with a more
intuitive interface. Most Divi modules have direct Breakdance equivalents.

### Site Inventory
- Total Divi pages: X
- Total modules to convert: X
- Auto-convertible: X (Y%)
- Manual attention: X (Y%)

### Module → Element Mapping
| Divi Module        | Breakdance Element | Status |
|-------------------|-------------------|--------|
| et_pb_text        | Text              | Auto   |
| et_pb_image       | Image             | Auto   |
| et_pb_blurb       | Icon Box          | Auto   |
| et_pb_button      | Button            | Auto   |
| et_pb_slider      | Slider            | Auto   |
| et_pb_accordion   | Accordion         | Auto   |
| et_pb_pricing     | Pricing Table     | Auto   |
| et_pb_contact     | Form              | Partial|
| [divi addon]      | —                 | Manual |

### Page-by-Page Plan
1. **[Page Title]** — X modules, [complexity]
2. ...
```

Ask for confirmation:
> Ready to migrate? Your original Divi pages remain completely untouched.
> 1. Migrate all pages
> 2. Migrate specific pages
> 3. Start with a test page (recommended)
> 4. Just keep this plan

### Phase 3: Page-by-Page Migration

For each approved page:

1. Read Divi content via `wordpress_extract_builder_content` with `builder=divi`
2. Parse the shortcode tree:
   - Build section → row → column → module hierarchy
   - Decode encoded content
   - Resolve global module references
   - Calculate column widths from type attributes
3. Generate Breakdance element structure:
   - `et_pb_section` → Breakdance Section
   - `et_pb_row` + `et_pb_column` → Breakdance Div elements with flex layout and percentage widths
   - Map each module to Breakdance element:
     - `et_pb_text` → Text element (preserve HTML content)
     - `et_pb_blurb` → Icon Box element (map icon, title, body)
     - `et_pb_image` → Image element (map src, alt)
     - `et_pb_button` → Button element (map text, URL, style)
     - `et_pb_accordion` → Accordion element (map items)
     - `et_pb_tabs` → Tabs element (map tab titles and content)
   - Map colors, spacing, typography to Breakdance settings
   - Flag unmappable modules
4. Create duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
5. Write Breakdance content via `wordpress_inject_builder_content` with `builder=breakdance`
6. Report status

### Phase 4: Post-Migration Verification

1. Summarize migrations:
   - Pages migrated, elements created, items flagged
2. For each migrated page:
   - Link to Breakdance editor
   - Flagged items list
   - Layout and encoding notes
3. Post-migration checklist:
   - [ ] Open each duplicate in Breakdance editor
   - [ ] Verify section and layout structure
   - [ ] Check responsive views
   - [ ] Verify images and media
   - [ ] Test links and buttons
   - [ ] Recreate flagged modules
   - [ ] Rebuild forms with Breakdance form element
   - [ ] Set up global templates (header/footer) in Breakdance
   - [ ] Review Breakdance's clean CSS output
   - [ ] Compare with Divi original
   - [ ] Check for Divi shortcode remnants

## Safety Model

- Read-only analysis first — full content scan before any changes
- Explicit user confirmation required before creating duplicates
- Original Divi pages are never modified or deleted
- All migrated content goes to draft duplicates only
- Never auto-publishes migrated pages
- Creates a snapshot before migration begins (when available)
- Provides clear rollback path (delete duplicates)
- Warns about theme implications if using Divi theme

## Honest Disclaimer

This skill converts Divi page content to Breakdance format and creates draft duplicates for review.

It cannot:
- Migrate specialty section layouts perfectly
- Convert global modules to Breakdance global blocks automatically
- Handle third-party Divi plugin modules
- Transfer Divi theme customizer settings
- Migrate popups, dynamic content, or animations
- Guarantee pixel-perfect visual fidelity from shortcodes

It can:
- Parse Divi's complex shortcode hierarchies including encoded content
- Convert 80-90% of standard Divi modules to Breakdance elements
- Produce cleaner CSS and HTML output than Divi
- Preserve all text, images, links, and core styling
- Save significant manual rebuilding time
- Clearly flag everything needing manual work
- Keep original pages completely safe

## Tooling

**Core WordPress tools**
- `wordpress_get_site_context`
- `wordpress_list_plugins`
- `wordpress_list_pages`
- `wordpress_list_posts`
- `wordpress_read_page`
- `wordpress_read_post`
- `wordpress_get_builder_info`
- `wordpress_extract_builder_content`
- `wordpress_inject_builder_content`
- `wordpress_find_builder_targets`
- `wordpress_create_page_duplicate`
- `wordpress_create_post_duplicate`

## Telemetry

After run completion, send fire-and-forget usage tracking to:

- `POST https://www.respira.press/api/skills/track-usage`

Include:
- `skill_slug = migrate-divi-to-breakdance`
- site/version context
- duration and success
- pages migrated, elements created, modules flagged counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (understand site structure and theme before migrating)
- Internal Link Builder (verify internal links post-migration)
- SEO & AEO Amplifier (verify SEO preservation post-migration)
- Technical Debt Audit (find Divi shortcode remnants post-migration)

---

Built by Respira Team
https://respira.press/skills/migrate-divi-to-breakdance
