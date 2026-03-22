---
name: wordpress-elementor
description: >
  Edit Elementor pages and manage templates on WordPress sites.
  Workflow: identify page, choose editing method (browser or WP-CLI), execute, verify.
  Use when editing Elementor pages, updating text in Elementor widgets,
  applying or managing Elementor templates, or making content changes
  to pages built with Elementor page builder.
compatibility: claude-code-only
---

# WordPress Elementor

Edit Elementor pages and manage templates on existing WordPress sites. Produces updated page content via browser automation (for visual/structural changes) or WP-CLI (for safe text replacements).

## Prerequisites

- Working WP-CLI connection or admin access (use **wordpress-setup** skill)
- Elementor installed and active: `wp @site plugin status elementor`

## Workflow

### Step 1: Identify the Page

Find the page to edit:

```bash
# List Elementor pages (pages with _elementor_data meta)
wp @site post list --post_type=page --meta_key=_elementor_edit_mode --meta_value=builder \
  --fields=ID,post_title,post_name,post_status

# Get the Elementor edit URL
# Format: https://example.com/wp-admin/post.php?post={ID}&action=elementor
```

### Step 2: Choose Editing Method

| Change Type | Method | Risk |
|-------------|--------|------|
| Text content updates | WP-CLI search-replace | Low (with backup) |
| Image URL swaps | WP-CLI meta update | Low (with backup) |
| Widget styling | Browser automation | None |
| Add/remove sections | Browser automation | None |
| Layout changes | Browser automation | None |
| Template application | Browser automation | None |

**Rule of thumb**: If you're only changing text or URLs within existing widgets, WP-CLI is faster. For anything structural, use the visual editor via browser.

### Step 3a: Text Updates via WP-CLI (Safe Method)

**Always back up first**:

```bash
# Export the Elementor data
wp @site post meta get {post_id} _elementor_data > /tmp/elementor-backup-{post_id}.json
```

**Simple text replacement**:

```bash
# Dry run — check what would change
wp @site search-replace "Old Heading Text" "New Heading Text" wp_postmeta \
  --include-columns=meta_value \
  --dry-run --precise

# Execute (after confirming dry run looks correct)
wp @site search-replace "Old Heading Text" "New Heading Text" wp_postmeta \
  --include-columns=meta_value --precise
```

**After updating**, clear Elementor's CSS cache:

```bash
wp @site elementor flush-css
```

If the `elementor` WP-CLI command isn't available:

```bash
wp @site option delete _elementor_global_css
wp @site post meta delete-all _elementor_css
```

### Step 3b: Visual Editing via Browser Automation

For structural changes, use browser automation to interact with Elementor's visual editor.

**Open the editor**:

1. Navigate to `https://example.com/wp-admin/post.php?post={ID}&action=elementor`
2. Wait for the editor to fully load (Elementor loading screen disappears)
3. The page appears in the main panel with the widget sidebar on the left

**Common editing tasks**:

1. **Edit text widget**: Click on the text element in the preview → edit inline or in the sidebar
2. **Edit heading**: Click the heading → update text in the sidebar panel
3. **Change image**: Click image widget → click the image in sidebar → select new from media library
4. **Edit button**: Click button → update text, URL, and styling in sidebar
5. **Save**: Click the green "Update" button (or Ctrl+S)

Use playwright-cli for independent sessions:

```bash
playwright-cli -s=wp-editor open "https://example.com/wp-admin/"
# Login first, then navigate to Elementor editor
playwright-cli -s=wp-editor navigate "https://example.com/wp-admin/post.php?post={ID}&action=elementor"
```

Or Chrome MCP if using the user's logged-in session.

See `references/elementor-workflows.md` for detailed browser automation steps.

### Step 4: Manage Templates

**List saved templates**:

```bash
wp @site post list --post_type=elementor_library --fields=ID,post_title,post_status
```

**Apply a template to a new page**:

1. Create the page: `wp @site post create --post_type=page --post_title="New Page" --post_status=draft`
2. Open in Elementor via browser
3. Click the folder icon (Add Template)
4. Select from "My Templates" tab
5. Click "Insert"
6. Customise and save

**Duplicate an existing page**:

```bash
# Get source page's Elementor data
SOURCE_DATA=$(wp @site post meta get {source_id} _elementor_data)
SOURCE_CSS=$(wp @site post meta get {source_id} _elementor_page_settings)

# Create new page
NEW_ID=$(wp @site post create --post_type=page --post_title="Duplicated Page" --post_status=draft --porcelain)

# Copy Elementor data
wp @site post meta update $NEW_ID _elementor_data "$SOURCE_DATA"
wp @site post meta update $NEW_ID _elementor_edit_mode "builder"
wp @site post meta update $NEW_ID _elementor_page_settings "$SOURCE_CSS"

# Regenerate CSS
wp @site elementor flush-css
```

### Step 5: Verify

```bash
# Check the page status
wp @site post get {post_id} --fields=ID,post_title,post_status,guid

# Get live URL
wp @site post get {post_id} --field=guid
```

Take a screenshot to confirm visual changes:

```bash
playwright-cli -s=verify open "https://example.com/{page-slug}/"
playwright-cli -s=verify screenshot --filename=page-verify.png
playwright-cli -s=verify close
```

---

## Critical Patterns

### Elementor Data Format

Elementor stores page content as JSON in `_elementor_data` postmeta. The structure is:

```
Section → Column → Widget
```

Each element has an `id`, `elType`, `widgetType`, and `settings` object. Direct manipulation of this JSON is possible but fragile — always back up first and prefer `search-replace` over manual JSON editing.

### CSS Cache

After any WP-CLI change to Elementor data, you must flush the CSS cache. Elementor pre-generates CSS from widget settings. Stale cache = visual changes don't appear.

```bash
wp @site elementor flush-css
# OR if elementor CLI not available:
wp @site option delete _elementor_global_css
wp @site post meta delete-all _elementor_css
```

### Elementor Pro vs Free

| Feature | Free | Pro |
|---------|------|-----|
| Basic widgets | Yes | Yes |
| Theme Builder | No | Yes |
| Custom fonts | No | Yes |
| Form widget | No | Yes |
| WooCommerce widgets | No | Yes |
| Dynamic content | No | Yes |

Theme Builder templates (header, footer, archive) are stored as `elementor_library` post type with specific meta indicating their display conditions.

### Common Elementor WP-CLI Commands

If the Elementor CLI extension is available:

```bash
wp @site elementor flush-css          # Clear CSS cache
wp @site elementor library sync       # Sync with template library
wp @site elementor update db          # Update database after version change
```

---

## Reference Files

- `references/elementor-workflows.md` — Browser automation steps, template management, safe editing patterns
