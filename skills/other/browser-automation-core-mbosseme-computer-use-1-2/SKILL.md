---
name: "Core Browser Automation"
description: "General-purpose patterns for reliable browser automation (selectors, waiting, scrolling, overlays, HITL)."
tools:
  - playwright
---

## Selector Strategy (Stability First)
- **Priority 1**: `data-testid`, `data-test`, `data-cy`, `id` (if stable).
- **Priority 2**: Accessible roles with names (e.g., `getByRole('button', { name: 'Submit' })`).
- **Priority 3**: Text content (e.g., `getByText('Submit')`) - use with caution if text is dynamic.
- **Avoid**: Brittle CSS selectors (e.g., `div > div:nth-child(3)`), XPath, or selectors tied to visual layout.

## Waiting Strategy (No Flaky Sleeps)
- **Explicit Waits**: Wait for elements to be **attached**, **visible**, and **enabled** before interacting.
- **State Changes**: Wait for clear UI signals (spinners disappearing, success messages appearing).
- **Bounded Polling**: If no clear signal exists, use a loop with a short sleep (1-2s) and a max retry count.
- **Avoid**: Long blind sleeps (e.g., `sleep(5000)`).

## Evidence Capture Hygiene
- When a tool accepts a `filename`, prefer a **simple filename** (e.g., `tab2-detail-limit-200.png`) rather than passing a full/relative directory path; some environments will prepend their own output directory and can accidentally create nested paths.

### Evidence screenshot trimming (dashboard-only)
When screenshots include large empty gutters (common with embedded BI dashboards), prefer a **deterministic local crop** after capture:

- Goal: keep the dashboard content + filter state, remove browser/app chrome and big white margins.
- Pitfall: naive “non-white bbox” cropping can fail because full-width top chrome forces the crop to remain full width.
- Recommended tool:
  - `python scripts/make_clean_dashboard_screenshots.py runs/<RUN_ID>/playwright-output/*.png`
  - Produces `_clean.png` siblings next to originals.

Notes:
- Capture screenshots with the relevant filter pane/state visible (e.g., procode dropdown showing the selected value).
- Prefer cropping before embedding into emails/PDFs so evidence stays consistent across formats.

## Scroll Strategy
- **Window vs. Container**: Determine if the scrollbar belongs to the `window` or a specific container element.
- **Incremental Scan**: Scroll in small chunks (e.g., half viewport) to trigger lazy-loading or reveal elements.
- **Check after Scroll**: Re-evaluate the page state after scrolling (elements might become visible).

## Handling Overlays & Modals
- **Detection**: Watch for common overlay selectors (dialogs, cookie banners, "interstitial" layers).
- **Dismissal**: Look for "Close", "X", "Accept", "Reject", "No thanks" buttons.
- **Click Intercepted**: If a click fails due to an overlay, find the overlay, dismiss it, and retry the click.

## Frames & Iframes
- **Detection**: If an element is not found, check if it resides within an `iframe`.
- **Switching**: Switch context to the iframe before querying elements inside it.

## Deep Links & SPA Navigation
- **Treat URL parameters as opaque**: Do not attempt to "clean" or "fix" URLs by stripping parameters (e.g., tokens, session IDs) unless confirmed to be tracking-only. Many modern apps ("Magic Links", portals) rely on complex tokens in the URL to grant access.
- **Prefer Extraction over Construction**: When processing a list of links (e.g., from an email), extract the exact URL string rather than trying to construct it from a pattern.
- **Isolate Navigation**: When moving between two deep links in the same SPA (Single Page App), unexpected state contamination can occur. If a navigation fails or redirects to the wrong view:
  - Try opening a **new context** or ensuring a **clean navigation** event (`page.goto()`) rather than relying on in-app clicking.

## Embedded BI Dashboards (Tableau-like)

### Common traits
- The interactive visualization is often inside an `iframe` (e.g., `iframe[title="Data Visualization"]`).
- Many charts/tables are **canvas-rendered**: the underlying DOM won’t contain the visible text, so `locator('text=...')` may fail even when the label is on screen.
- The accessibility tree (roles like `treegrid`, `row`, `gridcell`, `textbox`, `button`) is frequently the most reliable way to target UI.

### Reliable interaction patterns
- **Target inside the iframe** using role-based selectors (preferred): `frameLocator(...).getByRole(...)`.
- **Prefer table-row evidence** over brittle filters when filters are multi-select or unclear.
  - If a category row is not present due to a “top N” limit, increase a visible limit control (e.g., `Detail Limit`) to expose the desired rows.
- **Confirm state from the UI**: after applying a filter or changing a limit, re-snapshot and verify a clear change (row appears, numbers change, undo/revert enables, etc.).

### Quick filter pitfalls + recovery
- Typing into a quick-filter search box may only filter the list of options and may **not** apply the filter until a checkbox/value is explicitly selected.
- Some quick-filter widgets expose a textbox in the accessibility tree but don’t expose a stable DOM `input` selector.
- When a filter isn’t collapsing the view as expected, use a deterministic fallback:
  - Increase the visible row limit (e.g., `Detail Limit`) and read the exact row’s values directly.

### Platform note (macOS)
- Keyboard modifiers differ:
  - Select all: `Meta` (Command) + `A` on macOS (not `Control` + `A`).

## Human-in-the-Loop (HITL) Policy
- **Auth**: Stop for Login/SSO/MFA/CAPTCHA. Ask user to complete and type "Done".
- **Irreversible Actions**: **ALWAYS** ask for explicit confirmation before clicking:
  - Submit / Complete / Finish
  - Attest / Certify
  - Approve / Confirm / Yes
  - Send / Pay
- **Ambiguity**: If unsure if an action is irreversible, ASK first.

## Recovery Rules
- **Element not found**:
  - Check for iframes.
  - Check for shadow DOM.
  - Check if the element is behind an overlay.
  - Scroll to bring it into view.
- **Click intercepted**:
  - Identify the obscuring element.
  - Dismiss it (if it's a modal/banner).
  - Wait for it to disappear (if it's a toast/spinner).
- **Stale element**:
  - Re-query the element from the DOM before interacting.

- **Visible text not found (canvas / viz rendering)**:
  - Assume the text may not exist in the DOM.
  - Re-target via accessibility roles (e.g., `treegrid`/`gridcell`) or use a “show more rows”/limit control to surface the needed row.
---

## Visual Evidence Mode

This section teaches when and how to capture visual evidence (screenshots) for tasks that require interpreting what something **looks like**, not just what text it contains.

### Implicit Visual Recon (key trigger)
When the user asks to "investigate", "review", "analyze", or "assess" something where visual evidence is *likely* relevant (listings, products, designs, diagrams, dashboards, UI behavior, before/after, quality/condition):
1. Run a **quick visual recon** even if they didn't explicitly say "look at photos".
2. Locate gallery/images/figures/charts on the page (see Container Detection below).
3. Open 1–3 representative visuals (click thumbnails, expand carousel).
4. Take targeted screenshots only if interpretation is needed.
5. **Skip this step** if the task is purely factual (price, address, counts).

### When to Activate Visual Evidence Mode (explicit triggers)
Activate when the task requires understanding:
- **Quality / Condition / Aesthetics**: "Is this renovated?", "What's the finish level?"
- **Charts / Graphs / Dashboards**: Trends, distributions, visual KPIs not in DOM text
- **Maps / Diagrams / Floor Plans**: Spatial relationships, layouts
- **Color-coded UI state**: Status indicators, progress bars, warning highlights
- **Canvas / WebGL / Embedded Widgets**: Content not exposed in accessibility tree

**Trigger keywords** (user intent signals):
- "assess", "evaluate", "inspect", "compare", "investigate", "what does it look like"
- "condition", "quality", "finish", "style", "appearance"
- "trends", "patterns", "chart", "graph", "dashboard"

### Visual Container Detection
Before capturing, locate the relevant visual containers:
- **Image galleries**: `img`, `picture`, carousel containers, lightbox triggers
- **Charts/Graphs**: `canvas`, `svg`, chart library containers (e.g., `.highcharts-container`, `[data-viz]`)
- **Embedded dashboards**: `iframe[title*="Tableau"]`, `iframe[src*="looker"]`, BI widget containers
- **Maps**: `[class*="map"]`, `iframe[src*="maps"]`, Leaflet/Mapbox containers

### Evidence Capture Procedure
1. **Wait for load**: Ensure images/charts are fully rendered (no spinners, no "Loading..." text).
2. **Target the element**: Screenshot the specific container, not the full page.
   - Use `ref` parameter to target an element from the snapshot.
   - If no stable ref, screenshot the viewport with the element centered.
3. **Limit quantity**: 1–3 screenshots per page unless more are explicitly needed.
4. **Name descriptively**: Use filenames like `kitchen-condition.png`, `price-trend-chart.png`.
5. **Interpret with citations**: Reference observable cues (e.g., "granite countertops visible", "upward trend in Q3").

### Prefer Labels/Legends over OCR
- **First**: Check for tooltip text (hover interactions may expose values).
- **Second**: Look for legend/axis labels in the DOM or accessibility tree.
- **Third**: Only resort to visual interpretation when text is truly unavailable.

### Anti-Flailing Stop Conditions
- **Max attempts**: 3 retries per visual element before asking user for help.
- **Timeout**: If a chart/image doesn't load within 15s, note the failure and move on.
- **Ambiguity threshold**: If you cannot interpret with medium+ confidence, explicitly say so rather than guessing.

---

## Two-Speed Execution Policy

Not all browser tasks require the same level of care. Use the right speed for the task.

### Lane Definitions

| Lane | Description | When to Use |
|------|-------------|-------------|
| **FAST** | Minimal verification, trust snapshot, move quickly | Simple lookups, known-structure pages, text extraction, form fills |
| **DELIBERATE** | Recon first, wait for loading, verify after transitions | Visual interpretation, slow SPAs, dashboards, unknown layouts, qualitative judgment |

### Adaptive Lane Selection (start FAST, escalate when needed)

**Default**: Start in **FAST** lane for all tasks.

**Auto-escalate to DELIBERATE** when you hit:
- Missing/incomplete info in snapshot (expected data not found)
- SPA/dashboard still loading (spinners, placeholders, "Loading...")
- Visual-only content (canvas charts, image galleries, embedded maps)
- Conflicting cues or ambiguous state
- Qualitative judgment needed (quality, condition, aesthetics)

**Start in DELIBERATE immediately** when the task clearly demands:
- Visual interpretation of charts/dashboards/diagrams
- Quality/condition/aesthetics assessment
- Before/after or comparison tasks
- "Investigate" or "analyze" with visual components

### FAST Lane Behavior
- Navigate → snapshot → extract → done.
- Skip extra verification unless something fails.
- Trust stable selectors and accessible names.
- **Example**: "Find the HOA fee on this listing page" → extract from snapshot text.

### DELIBERATE Lane Behavior
1. **Recon pass (30–90s)**: Understand page structure before acting.
   - Identify: Where does the answer live? (text vs visual vs interactive)
   - Identify: Any iframes, overlays, lazy-loading?
2. **Wait for load signals**: Spinners gone, charts rendered, images loaded.
3. **Verify after key transitions**:
   - After navigation: URL or title confirms destination.
   - After filter/tab change: re-snapshot shows expected state change.
   - After iframe switch: context is correct.
4. **Capture evidence**: Screenshots for visual interpretation.
5. **Cite sources**: "Found in tooltip", "Visible in chart legend", "Extracted from table row".

### CAPTCHA / Bot Detection Response
If CAPTCHA or bot-detection blocks access:
1. **Stop for HITL**: User completes challenge, then says "Done".
2. **If still blocked after HITL**, consider fallback:
   - Try an alternative public source for the same data.
   - Ask user to provide screenshots or copy-paste if automation isn't viable.
3. Do not maintain site-specific blocklists; treat each block case-by-case.

---

## Examples (for reference)

### Example 1: Assess Condition/Quality from a Listing Page
**Task**: "Investigate this property listing and assess the interior condition."

**Lane**: DELIBERATE (visual interpretation required)

**Procedure**:
1. Navigate to listing URL.
2. Recon: Locate photo gallery container (carousel, thumbnail grid).
3. Wait for images to load (no placeholder spinners).
4. Screenshot 2–3 key images: kitchen, bathroom, main living area.
5. Interpret with citations:
   - "Kitchen: granite countertops, stainless appliances, modern cabinetry → Premium finish"
   - "Bathroom: updated vanity, tile flooring → Renovated"
   - "Living area: wood-look flooring, crown molding → Above average"
6. Provide confidence level: "Condition assessment: Premium/Renovated, confidence: High"

### Example 2: Summarize Trends from a Dashboard Page
**Task**: "Summarize the key trends on this analytics dashboard."

**Lane**: DELIBERATE (chart interpretation required)

**Procedure**:
1. Navigate to dashboard URL.
2. Recon: Identify chart containers (canvas, SVG, iframe).
3. Wait for charts to render (loading indicators disappear).
4. **Try text first**: Check for tooltips, legends, axis labels in DOM.
5. If text insufficient, screenshot 1–2 key charts.
6. Interpret with citations:
   - "Revenue chart shows upward trend Q1→Q3, flattening in Q4"
   - "Pie chart: Category A = 45%, Category B = 30% (from legend)"
7. Mark uncertainty if values aren't precise: "Approximate trend direction; exact values not available in DOM."