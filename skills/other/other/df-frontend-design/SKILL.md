---
name: df:frontend-design
description: |
  Build, review, or visually inspect UI using eden-ui components, Rails ERB partials, and Tailwind design tokens.
  Use when the user wants to create new views, design components, audit existing UI, review frontend code, or visually test rendered pages.
  Triggers on: "build the UI", "design this page", "create a view", "review the frontend", "audit the UI", "check UI consistency", "make it look good", "frontend review", "visual review", "check how it looks", "inspect the page"
argument-hint: "<build|review|visual> [description, file paths, or URL]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - AskUserQuestion
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_snapshot
  - mcp__plugin_playwright_playwright__browser_take_screenshot
  - mcp__plugin_playwright_playwright__browser_click
  - mcp__plugin_playwright_playwright__browser_evaluate
  - mcp__plugin_playwright_playwright__browser_console_messages
  - mcp__plugin_playwright_playwright__browser_resize
  - mcp__plugin_playwright_playwright__browser_tabs
  - mcp__plugin_playwright_playwright__browser_wait_for
---
<objective>
Build new UI, review existing code, or visually inspect rendered pages against eden-ui conventions.

**Three modes:**

**Build mode** — Generate Rails ERB views/partials using eden-ui components. Compose from the 150+ eden-ui helpers rather than writing raw Tailwind. Produces production-grade views that match the eden-ui design system (configured brand palette, dark mode, Stimulus interactivity).

**Review mode** — Audit existing views/partials for eden-ui compliance. Check for: raw HTML that should use eden-ui helpers, missing dark mode support, hardcoded colors instead of design tokens, incorrect component composition, accessibility gaps, missing Stimulus controllers for interactive patterns.

**Visual mode** — Load pages in a browser via Playwright and inspect the rendered output. Check visual consistency, responsive behavior, dark mode rendering, interactive component functionality, and design token compliance in the actual DOM/CSS. Catches issues that static code review misses: layout breaks, z-index conflicts, animation glitches, computed style mismatches.

Output: Working ERB files (build), actionable code findings with fixes (review), or visual audit report with screenshots (visual).
</objective>

<execution_context>
@~/.claude/devflow/references/eden-ui-conventions.md
</execution_context>

<context>
Mode + target: $ARGUMENTS
- `build <description>` — Generate new views (e.g., "build user settings page")
- `review [paths]` — Audit existing files (e.g., "review app/views/dashboard/")
- `visual [URL or path]` — Visual browser inspection (e.g., "visual http://localhost:3000/dashboard")
- If no mode specified, infer from context

**Live reference — read from eden-ui source when needed:**
- Component helpers: `../eden-ui/app/helpers/eden_ui/component_helper.rb`
- Component partials: `../eden-ui/app/views/eden_ui/components/`
- Design tokens: `../eden-ui/app/assets/stylesheets/eden_ui/tokens.css`
- Stimulus controllers: `../eden-ui/app/assets/javascripts/eden_ui/controllers/`

@.planning/STATE.md
</context>

<process>

## Build Mode

0. **Read project brand** — Check `config/initializers/eden_ui.rb` for `brand_color` and `font_preset` settings. This determines the primary palette (e.g., `:blue` means `primary-*` maps to blue shades, not gold). Use `primary-*` classes — never hardcode `gold-*` unless the brand is explicitly gold.

1. **Understand the request** — What page/view/partial is needed? What data does it display? What actions does it support?

2. **Check eden-ui for matching components** — Read `../eden-ui/app/helpers/eden_ui/component_helper.rb` to find the exact helper signatures for components you'll use. Read specific partials in `../eden-ui/app/views/eden_ui/components/` to understand accepted parameters and rendering behavior.

3. **Plan the composition** — List which eden-ui components will compose the view. Identify layout choice (app, auth, marketing). Map data flow from controller to view.

4. **Generate ERB** — Write the view files using eden-ui helpers exclusively:
   - Use `eden_page_header` for page titles with breadcrumbs
   - Use `eden_card` for content containers
   - Use `eden_data_table` for tabular data
   - Use `eden_form_group` + `eden_input`/`eden_select`/etc. for forms
   - Use `eden_modal` / `eden_drawer` for overlay interactions
   - Use `eden_empty_state` for zero-data scenarios
   - Use `eden_flash_message` for notifications
   - Include Stimulus controller data attributes for interactivity
   - All components must support dark mode (eden-ui handles this internally)

5. **Verify** — Confirm all helper calls use valid parameters by cross-referencing eden-ui source. Check that Stimulus controllers referenced exist in the importmap.

## Review Mode

0. **Read project brand** — Check `config/initializers/eden_ui.rb` for `brand_color` and `font_preset` settings. When brand is not `:gold`, flag any `gold-*` hardcodes as violations.

1. **Discover target files** — Glob for `*.html.erb` in the specified paths. If no path given, scan `app/views/` excluding vendored/eden_ui engine views.

2. **Read eden-ui component inventory** — Load the helper file to know what's available.

3. **Audit each file** for these categories:

   **Component usage:**
   - Raw HTML that duplicates an eden-ui component (e.g., hand-rolled modal instead of `eden_modal`)
   - Missing helper usage (e.g., raw `<button>` instead of `eden_button`)
   - Incorrect parameter usage (wrong variant names, missing required params)

   **Design token compliance:**
   - Hardcoded colors (`bg-yellow-500`) instead of token colors (`bg-primary-500`)
   - Non-token fonts, shadows, or spacing
   - Missing `dark:` variants on custom elements (elements not rendered by eden-ui helpers)

   **Accessibility:**
   - Missing ARIA labels on interactive elements
   - Missing focus states
   - Images without alt text
   - Forms without associated labels

   **Stimulus controllers:**
   - Interactive patterns without Stimulus (onclick handlers, inline JS)
   - Missing data-controller attributes on components that need them
   - Incorrect data-action syntax

   **Composition:**
   - Forms not using `eden_form_group` wrapper
   - Tables not using `eden_data_table` or `eden_table`
   - Empty states not using `eden_empty_state`
   - Alerts/flashes not using eden-ui alert components

4. **Report findings** — Group by severity:
   - **Must fix** — Broken patterns, accessibility violations, missing dark mode
   - **Should fix** — Raw HTML replaceable by eden-ui components, hardcoded colors
   - **Consider** — Style improvements, better component composition

5. **Generate fixes** — For each must-fix and should-fix finding, provide the corrected ERB code. Apply fixes directly if the user approves.

## Visual Mode

Uses Playwright to load pages in a real browser and inspect the rendered output.

### Setup

0. **Read project brand** — Check `config/initializers/eden_ui.rb` for `brand_color` and `font_preset` settings. This context informs what colors to expect when inspecting computed styles.

1. **Confirm the app is running** — Ask the user for the base URL (default: `http://localhost:3000`). Verify the server responds before proceeding.

2. **Determine scope** — What pages/flows to inspect:
   - Single URL: inspect one page
   - Flow: a sequence of URLs or actions (e.g., "the settings flow")
   - Full audit: crawl all pages linked from a starting point

### Page Inspection Sequence

For each page, run this sequence:

3. **Navigate and snapshot** — Load the URL. Take an accessibility snapshot (`browser_snapshot`) to get the semantic structure. This is the primary inspection tool — it reveals the actual DOM tree, ARIA roles, element hierarchy.

4. **Screenshot for visual context** — Take a screenshot to see the rendered visual output. Use this to evaluate layout, spacing, color usage, and overall design quality.

5. **Design token audit** — Evaluate computed styles in the browser:
   ```js
   // Check if eden design tokens are being used
   // Look for hardcoded values that should use tokens
   () => {
     const body = getComputedStyle(document.body);
     return {
       fontFamily: body.fontFamily,
       colorScheme: document.documentElement.classList.contains('dark') ? 'dark' : 'light',
       // Sample element styles
     };
   }
   ```

6. **Component structure check** — Use the snapshot to verify:
   - Stimulus controllers are connected (`data-controller` attributes present)
   - ARIA roles and labels are correct
   - Interactive elements are keyboard-accessible (check tabindex, roles)
   - Form inputs have associated labels
   - Images have alt text
   - Heading hierarchy is logical (h1 → h2 → h3, no skips)

7. **Responsive check** — Resize the viewport and re-inspect:
   - **Desktop** (1280x800) — Full layout, sidebar visible
   - **Tablet** (768x1024) — Sidebar collapsed, responsive grid
   - **Mobile** (375x812) — Mobile nav, stacked layout

   At each breakpoint: take a screenshot, check the snapshot for layout shifts, verify navigation adapts correctly.

8. **Dark mode check** — Toggle dark mode and re-inspect:
   ```js
   () => { document.documentElement.classList.toggle('dark'); }
   ```
   Take a screenshot in dark mode. Verify:
   - No white/light backgrounds bleeding through
   - Text remains readable (sufficient contrast)
   - Brand (`primary-*`) colors render correctly on dark backgrounds
   - Borders and dividers use appropriate dark variants
   - No missing `dark:` overrides (elements that look correct in light but break in dark)

9. **Interactive component testing** — For pages with interactive elements:
   - **Modals:** Click trigger → verify modal opens → check backdrop → close with Escape
   - **Dropdowns:** Click trigger → verify menu appears → check keyboard navigation
   - **Tabs:** Click each tab → verify content switches
   - **Accordions:** Click items → verify expand/collapse
   - **Forms:** Check validation states (submit empty → check error styling)
   - **Tooltips/Popovers:** Hover triggers → verify positioning

10. **Console check** — After interactions, check browser console for:
    - JavaScript errors (broken Stimulus controllers, missing dependencies)
    - Stimulus controller connection warnings
    - Missing asset warnings (fonts, icons, images)

### Reporting

11. **Compile visual audit report** — Organize findings:

    **Layout & Spacing:**
    - Alignment issues, inconsistent padding/margins, overflow problems
    - Screenshots with annotations

    **Color & Tokens:**
    - Computed colors that don't match eden tokens
    - Contrast violations (especially in dark mode)

    **Responsive:**
    - Breakpoint-specific layout issues
    - Side-by-side screenshots (desktop/tablet/mobile)

    **Dark Mode:**
    - Elements that break in dark mode
    - Before/after screenshots

    **Interactivity:**
    - Components that don't respond to interaction
    - Console errors from Stimulus controllers
    - Focus trapping / keyboard navigation gaps

    **Accessibility:**
    - Missing ARIA attributes found in live DOM
    - Focus order issues discovered through tab navigation
    - Screen reader concerns from the accessibility snapshot

12. **Cross-reference with code** — For each visual finding, trace back to the responsible ERB file using the snapshot's element structure. Provide the file path and specific code that needs to change. Offer to apply fixes.

</process>
