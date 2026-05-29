---
name: compare-erb-js
description: Compare ERB and JavaScript template outputs for the offline scoring SPA. Use when working on ERB-to-JS conversion, debugging template parity issues, or verifying that changes to scoring views work correctly in both ERB and SPA modes.
---

# Compare ERB vs JavaScript Template Output

Use `scripts/render_erb_and_js.rb` to verify that ERB templates and their JavaScript-converted equivalents produce matching output. This is essential for the offline scoring SPA which uses auto-converted ERB templates.

## Basic Usage

```bash
# Compare heat list
bundle exec ruby scripts/render_erb_and_js.rb db/2025-barcelona-november.sqlite3 83

# Compare individual heat
bundle exec ruby scripts/render_erb_and_js.rb db/2025-barcelona-november.sqlite3 83 1

# With style parameter
bundle exec ruby scripts/render_erb_and_js.rb db/2025-barcelona-november.sqlite3 83 1 radio
```

Or using environment variable:
```bash
RAILS_APP_DB=2025-barcelona-november bundle exec ruby scripts/render_erb_and_js.rb 83 1
```

## What It Does

1. Renders the ERB template via Rails routing (extracts `<main>` content)
2. Fetches converted JavaScript templates from `/templates/scoring.js`
3. Fetches normalized data from `/scores/:judge/heats/data`
4. Hydrates the data using `heat_hydrator.js` (for individual heats)
5. Renders using the JavaScript template
6. Compares row counts and saves both outputs for diff analysis

## Output Files

All files are saved to `/tmp/` for analysis:

- `/tmp/erb_rendered.html` - ERB template output (main content only)
- `/tmp/js_rendered.html` - JavaScript template output
- `/tmp/scoring_templates.js` - Converted templates from `/templates/scoring.js`
- `/tmp/heats_data.json` - Raw normalized data from server
- `/tmp/js_template_data.json` - Hydrated data passed to JS template

## Analyzing Differences

```bash
# Quick diff
diff /tmp/erb_rendered.html /tmp/js_rendered.html

# Side-by-side comparison
diff -y /tmp/erb_rendered.html /tmp/js_rendered.html | less

# Compare specific attributes
diff <(grep -o 'href="[^"]*"' /tmp/erb_rendered.html | sort) \
     <(grep -o 'href="[^"]*"' /tmp/js_rendered.html | sort)
```

## Common Differences

Some differences are expected due to ERB-to-JS conversion limitations:

- **HTML entity encoding**: ERB uses `&quot;` while JS uses `"`
- **link_to blocks**: Block form of `link_to` may render differently
- **Whitespace**: Minor whitespace differences are normal

## Architecture

This tool supports the "Server computes, hydration joins, templates filter" principle:

- **Server**: Computes derived values and paths (respects RAILS_APP_SCOPE)
- **Hydration**: `heat_hydrator.js` joins normalized data by resolving IDs
- **Templates**: ERB and JS templates filter/format data identically

## Key Source Files

### Server-side (Rails)

- `app/controllers/scores_controller.rb`
  - `heats_data` action: Returns normalized JSON data for SPA
  - `heat` action: Sets instance variables for ERB templates
  - Computes `paths:` hash with server-computed URLs

- `app/controllers/templates_controller.rb`
  - `scoring` action: Converts ERB templates to JavaScript on-the-fly
  - Defines path helper stubs for JS templates
  - Uses `ErbPrismConverter` for conversion

- `lib/erb_prism_converter.rb`
  - Converts ERB templates to JavaScript functions using Ruby's Prism parser
  - Handles Ruby-to-JS translation (loops, conditionals, method calls)

### Client-side (JavaScript)

- `app/javascript/lib/heat_hydrator.js`
  - `buildLookupTables()`: Creates Maps for O(1) entity lookup
  - `hydrateHeat()`: Resolves IDs to full objects
  - `buildHeatTemplateData()`: Prepares complete data for templates

- `app/javascript/controllers/heat_app_controller.js`
  - Main Stimulus controller for the offline scoring SPA
  - Loads templates and data, handles navigation
  - Manages offline/online state transitions

### ERB Templates (source of truth)

- `app/views/scores/heat.html.erb` - Main heat view
- `app/views/scores/heatlist.html.erb` - Heat list view
- `app/views/scores/_heat_header.html.erb` - Heat header partial
- `app/views/scores/_info_box.html.erb` - Info box with feedback errors
- `app/views/scores/_navigation_footer.html.erb` - Prev/next navigation
- `app/views/scores/_table_heat.html.erb` - Standard heat table
- `app/views/scores/_rank_heat.html.erb` - Finals ranking view
- `app/views/scores/_solo_heat.html.erb` - Solo heat view
- `app/views/scores/_cards_heat.html.erb` - Card-based scoring view

### Scripts

- `scripts/render_erb_and_js.rb` - This comparison tool
- `scripts/hydrate_heats.mjs` - Node.js script for hydrating data (used by comparison tool)
