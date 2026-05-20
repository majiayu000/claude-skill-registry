---
name: raweb-code
description: >
  Write accessible HTML, CSS, and JavaScript that conforms to RAWeb 1.1
  (Luxembourg Web Accessibility Framework, based on EN 301 549 / WCAG 2.1).
  Use when developing web interfaces, components, forms, navigation, or any
  front-end code that must meet Luxembourg accessibility law. Covers all 17
  RAWeb themes with code-level guidance, accessible patterns, and anti-patterns.
  Default conformance target: Level AA.
metadata:
  author: luxembourg-accessibility-skillset
  version: 1.2.0
  raweb-version: "1.1"
  wcag-version: "2.1"
  license: CC-BY-3.0-LU
  source: https://github.com/accessibility-luxembourg/ReferentielAccessibiliteWeb
allowed-tools: Bash Read Grep
---

# RAWeb 1.1 — Accessible Code Development Guide

You are an accessibility-aware developer. Every piece of HTML, CSS, and JavaScript
you write MUST conform to **RAWeb 1.1** (Level AA by default). RAWeb is Luxembourg's
official web accessibility framework implementing EN 301 549 and WCAG 2.1.

## How to use the reference data

The full RAWeb 1.1 criteria, test methodologies, and glossary are available as
JSON files. Use the lookup script to query specific criteria on demand:

```bash
# List all topics
!`${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh topics`

# Look up a specific criterion
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh criterion 1.1

# Look up test methodology
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh methodology 1.1.1

# Search criteria by keyword
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh search "form"

# Check glossary definition
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh glossary "text alternative"
```

The raw JSON reference files are located at:
- `${CLAUDE_SKILL_DIR}/references/criteres.json` — All 136+ criteria with tests and WCAG/EN 301 549 mappings
- `${CLAUDE_SKILL_DIR}/references/methodologies.json` — Step-by-step test procedures
- `${CLAUDE_SKILL_DIR}/references/glossaire.json` — Glossary of accessibility terms
- `${CLAUDE_SKILL_DIR}/references/themes.json` — Topic names
- `${CLAUDE_SKILL_DIR}/references/niveaux.json` — WCAG conformance levels per criterion

When writing code for a specific component, ALWAYS look up the relevant RAWeb
criteria first to ensure full compliance. For example, before writing a form,
run `search "form"` and `topic 11`.

---

## Core rules (apply to ALL code you write)

### 1. Images (Topic 1)

**ALWAYS:**
- Every `<img>` conveying information MUST have a meaningful `alt` attribute (1.1)
- Every decorative `<img>` MUST have `alt=""` and no `title`, `aria-label`, or `aria-labelledby` (1.2)
- Every `<svg>` conveying information MUST have `role="img"` + text alternative via `aria-label` or `aria-labelledby` (1.1)
- Decorative `<svg>` MUST have `aria-hidden="true"` (1.2)
- Text alternatives must be short and concise — 80 characters max recommended (1.3)
- Complex images (charts, infographics) need a detailed description accessible via adjacent link or `aria-describedby` (1.6)
- Avoid images of text unless the visual effect cannot be achieved with CSS (1.8, 1.9 — Level AA)

**NEVER:**
- Leave `alt` undefined on an informative image
- Use `alt="image"`, `alt="photo"`, `alt="icon"` — describe what the image conveys
- Use `title` as the sole text alternative (poor assistive technology support)

```html
<!-- GOOD: informative image -->
<img src="chart.png" alt="Sales increased 40% in Q3 2024">

<!-- GOOD: decorative image -->
<img src="decoration.svg" alt="">

<!-- GOOD: complex image with detailed description -->
<figure>
  <img src="orgchart.png" alt="Company organisation chart. Full description below.">
  <figcaption>
    <details>
      <summary>Full description of the organisation chart</summary>
      <p>The CEO reports to the board. Three departments report to the CEO...</p>
    </details>
  </figcaption>
</figure>

<!-- GOOD: SVG informative -->
<svg role="img" aria-label="Warning: connection unstable">
  <use href="#icon-warning"/>
</svg>

<!-- GOOD: SVG decorative -->
<svg aria-hidden="true" focusable="false"><use href="#flourish"/></svg>
```

### 2. Frames (Topic 2)

- Every `<iframe>` MUST have a descriptive `title` attribute (2.1)
- The `title` must be relevant to the frame content (2.2)

```html
<iframe src="map.html" title="Interactive map of our office locations"></iframe>
```

### 3. Colours (Topic 3)

- Information must NEVER be conveyed by colour alone (3.1)
- Text contrast ratio: at least **4.5:1** (normal text) or **3:1** (large text ≥18pt / bold ≥14pt) (3.2 — Level AA)
- Non-text elements (icons, borders, UI components): at least **3:1** contrast against adjacent colours (3.3 — Level AA)

```html
<!-- BAD: colour alone conveys meaning -->
<span class="text-red">Required field</span>

<!-- GOOD: colour + text indicator -->
<span class="text-red">Required field *</span>
<span class="sr-only">(required)</span>

<!-- Or better with native HTML -->
<input type="text" required aria-required="true">
```

### 4. Multimedia (Topic 4)

- Pre-recorded video with audio MUST have captions (4.1, 4.3)
- Pre-recorded audio MUST have a text transcript (4.1)
- Pre-recorded video MUST have audio description if visual information is not in the audio track (4.5, 4.6 — Level AA)
- Auto-playing media MUST be controllable: pause, stop, or mute within 3 seconds (4.10)
- No auto-playing audio longer than 3 seconds without a control mechanism (4.11)

```html
<video controls>
  <source src="presentation.mp4" type="video/mp4">
  <track kind="captions" src="captions-en.vtt" srclang="en" label="English" default>
  <track kind="descriptions" src="descriptions-en.vtt" srclang="en" label="English audio descriptions">
</video>
```

### 5. Tables (Topic 5)

- Data tables MUST use `<th>` elements for headers with appropriate `scope` attribute (5.6, 5.7)
- Complex tables MUST use `id`/`headers` associations (5.7)
- Every data table MUST have a caption or title via `<caption>`, `aria-label`, or `aria-labelledby` (5.4)
- Layout tables MUST NOT use `<th>`, `<caption>`, `scope`, or `headers` (5.8)
- Every data table MUST have a summary to help understand its structure when the table is complex (5.5)

```html
<!-- GOOD: simple data table -->
<table>
  <caption>Q3 2024 Revenue by Region</caption>
  <thead>
    <tr>
      <th scope="col">Region</th>
      <th scope="col">Revenue</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Europe</th>
      <td>€2.4M</td>
      <td>+12%</td>
    </tr>
  </tbody>
</table>
```

### 6. Links (Topic 6)

- Every link MUST have an explicit accessible name (6.1)
- The link's accessible name must be relevant and describe the destination or function (6.1)
- Avoid ambiguous link text: never use "click here", "read more", "learn more" without context (6.1)
- If the visible text is not sufficient, add context via `aria-label` or `aria-labelledby` — but the `aria-label` MUST include the visible text (6.1, 6.2)

```html
<!-- BAD -->
<a href="/report.pdf">Click here</a>

<!-- GOOD -->
<a href="/report.pdf">Download the Q3 2024 financial report (PDF, 2.4 MB)</a>

<!-- GOOD: contextual with aria-label containing visible text -->
<article>
  <h3>RAWeb 1.1 released</h3>
  <p>The new version adds 17 additional criteria...</p>
  <a href="/news/raweb" aria-label="Read more about RAWeb 1.1 released">Read more</a>
</article>
```

### 7. Scripts (Topic 7)

- Every script MUST be operable by keyboard AND any pointing device (7.1)
- All script-driven UI must be compatible with assistive technologies (7.1)
- Status messages must be communicated without focus change using `role="status"`, `role="alert"`, `role="log"`, `aria-live`, or `aria-relevant` (7.4)
- Script-inserted content must be accessible (7.2)
- Moving, blinking, or auto-updating content must be controllable: pause, stop, hide (7.5 — Level AA)

```html
<!-- GOOD: live region for status updates -->
<div role="status" aria-live="polite" aria-atomic="true">
  <p>3 results found.</p>
</div>

<!-- GOOD: alert for important messages -->
<div role="alert">
  <p>Your session will expire in 2 minutes.</p>
</div>
```

```javascript
// GOOD: keyboard + pointer support
button.addEventListener('click', handler);  // covers mouse + Enter/Space
button.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    handler(e);
  }
});
```

### 8. Mandatory Elements (Topic 8)

- Every page MUST have a valid `<!DOCTYPE html>` (8.1)
- Every page MUST have a `lang` attribute on `<html>` matching the primary language (8.3)
- Language changes in content MUST be marked with `lang` on the relevant element (8.7 — Level AA)
- Every page MUST have a unique and relevant `<title>` (8.5, 8.6)
- The page `<title>` MUST be updated when the page state changes significantly (8.6)
- No duplicate `id` attributes in the page (8.2)
- Opening and closing tags must be used per specification; nesting must be valid (8.1)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Contact Us — Acme Corp</title>
</head>
<body>
  <p>Visit our <span lang="fr">bureau principal</span> in Luxembourg.</p>
</body>
</html>
```

### 9. Information Structure (Topic 9)

- Use headings (`<h1>`–`<h6>`) with a logical hierarchy — no skipped levels (9.1)
- Use semantic HTML5 landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>` (9.2)
- Use lists (`<ul>`, `<ol>`, `<dl>`) for list content (9.3)
- Use `<blockquote>` for quotations with proper `cite` if applicable (9.4)

```html
<body>
  <header role="banner">
    <nav aria-label="Main navigation">...</nav>
  </header>
  <main role="main">
    <h1>Page Title</h1>
    <section aria-labelledby="section-heading">
      <h2 id="section-heading">Section</h2>
      <h3>Sub-section</h3>
    </section>
  </main>
  <footer role="contentinfo">...</footer>
</body>
```

### 10. Presentation of Information (Topic 10)

- Content must remain readable and functional at 200% zoom (10.4 — Level AA)
- Content must reflow at 320px CSS width without horizontal scrolling (10.11 — Level AA)
- Use CSS for all visual presentation; do not use HTML presentation attributes (10.1)
- No loss of information when CSS is disabled (10.2, 10.3)
- Visible focus indicator must be present on all interactive elements (10.7)
- Do not hide content in a way that becomes unreachable (10.8)
- Text spacing: users must be able to override line-height (1.5×), paragraph spacing (2×), letter-spacing (0.12em), word-spacing (0.16em) without loss of content (10.12 — Level AA)

```css
/* GOOD: visible focus indicator */
:focus-visible {
  outline: 3px solid #0056b3;
  outline-offset: 2px;
}

/* GOOD: ensure reflow support */
.container {
  max-width: 100%;
  overflow-wrap: break-word;
}

/* NEVER: hide focus outline globally */
/* *:focus { outline: none; } ← FORBIDDEN */
```

### 11. Forms (Topic 11)

**This is a critical topic. Always look up criteria with `bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh topic 11` when implementing forms.**

- Every form field MUST have a visible label (11.1) AND a programmatically associated label (11.1)
- Label association: `<label for="id">`, `aria-labelledby`, `aria-label`, or `title` (11.1)
- The `<label>` element with `for` attribute is the preferred method (11.1)
- The accessible name MUST include the visible label text (11.2)
- Labels must be relevant — clearly describe the expected input (11.2)
- Related fields MUST be grouped with `<fieldset>` and `<legend>` (11.5)
- Required fields must be indicated before the form or at the field level (11.10)
- Use `required` and/or `aria-required="true"` for mandatory fields (11.10)
- Error messages must be linked to the field and describe the error and expected format (11.11 — Level AA)
- Input purpose for personal data must use `autocomplete` with appropriate values (11.13 — Level AA)

```html
<form novalidate>
  <fieldset>
    <legend>Personal information</legend>

    <div>
      <label for="fname">First name <span aria-hidden="true">*</span></label>
      <input type="text" id="fname" name="fname"
             autocomplete="given-name"
             required aria-required="true"
             aria-describedby="fname-error">
      <p id="fname-error" role="alert" class="error" hidden>
        Please enter your first name.
      </p>
    </div>

    <div>
      <label for="email">Email address <span aria-hidden="true">*</span></label>
      <input type="email" id="email" name="email"
             autocomplete="email"
             required aria-required="true"
             aria-describedby="email-hint email-error">
      <p id="email-hint" class="hint">Format: name@example.com</p>
      <p id="email-error" role="alert" class="error" hidden>
        Please enter a valid email address (e.g., name@example.com).
      </p>
    </div>
  </fieldset>

  <button type="submit">Submit</button>
</form>
```

### 12. Navigation (Topic 12)

- At least two navigation mechanisms among: main nav, sitemap, search engine (12.1 — Level AA)
- Skip links must be present to bypass repeated content blocks (12.7)
- Skip links must be visible on focus (12.7)
- Tab order must be logical and consistent with visual reading order (12.8)
- Never use positive `tabindex` values (12.8)
- Navigation landmarks must be consistent across pages (12.2 — Level AA)
- The active page must be indicated in navigation menus (12.2)

```html
<body>
  <!-- Skip link: first focusable element -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <nav aria-label="Main navigation">
    <ul>
      <li><a href="/" aria-current="page">Home</a></li>
      <li><a href="/about">About</a></li>
      <li><a href="/contact">Contact</a></li>
    </ul>
  </nav>

  <main id="main-content" tabindex="-1">
    <!-- Page content -->
  </main>
</body>
```

```css
.skip-link {
  position: absolute;
  top: -100%;
  left: 0;
  z-index: 1000;
  padding: 0.5rem 1rem;
  background: #000;
  color: #fff;
}
.skip-link:focus {
  top: 0;
}
```

### 13. Consultation (Topic 13)

- Links to downloadable files must indicate format and size (13.3)
- Refreshes and redirects must not be automatic unless controllable by user (13.1)
- Time limits must be adjustable, extendable, or removable (13.1)
- Opening a new window must be indicated to the user (13.2)
- No unexpected context change on focus or input without prior warning (13.1)
- Moving or flashing content must be controllable (13.8)
- No more than 3 flashes per second (13.8)

```html
<!-- GOOD: file download with format and size -->
<a href="/report.pdf">
  Annual report 2024 <span class="file-info">(PDF, 3.2 MB)</span>
</a>

<!-- GOOD: new window warning -->
<a href="https://external.example.com" target="_blank"
   rel="noopener noreferrer">
  External resource
  <span class="sr-only">(opens in a new window)</span>
</a>
```

---

## Component patterns (WAI-ARIA APG)

When building interactive components, look up the correct ARIA pattern from the
local reference data BEFORE writing any code. The component library contains 30
patterns extracted from the [WAI-ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/patterns/)
with keyboard interactions, required/optional ARIA attributes, and implementation notes.

### How to use

```bash
# Find the right pattern by keyword (e.g., "modal", "dropdown", "toggle")
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh find "<keyword>"

# Show full pattern details (keyboard, ARIA roles, attributes, notes)
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh show <slug>

# List all 30 available patterns
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh list

# Find patterns that use a specific ARIA role
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh roles "<role>"
```

### Workflow

1. **Identify** the component the developer is building (dialog, tabs, slider, etc.)
2. **Search** using `find` with the most natural keyword the developer used
3. **Load** the full pattern with `show <slug>` to get keyboard interactions and ARIA requirements
4. **Cross-reference** with RAWeb criteria — especially Topics 7 (Scripts), 11 (Forms), and 12 (Navigation)
5. **Apply** the pattern, preferring native HTML elements over ARIA roles when possible

### Available patterns

The individual pattern files are located at:
`${CLAUDE_SKILL_DIR}/references/components/<slug>.json`

Each file contains:
- `description` — What the component is
- `keyboard_interactions` — All required and optional keyboard behaviours
- `aria.roles` — Which ARIA roles to use and where
- `aria.required_attributes` — Attributes that MUST be present
- `aria.optional_attributes` — Attributes to add when applicable
- `notes` — Implementation tips and common pitfalls

### Quick mapping: common requests → pattern slugs

| When the developer says... | Look up slug |
|---------------------------|-------------|
| modal, dialog, popup, overlay, lightbox | `dialog-modal` |
| tabs, tab panel, tabbed interface | `tabs` |
| accordion, collapsible, FAQ | `accordion` |
| dropdown menu, context menu, submenu | `menubar` or `menu-button` |
| toast, notification, flash message | `alert` |
| confirm dialog, delete confirmation | `alertdialog` |
| carousel, slideshow, image gallery | `carousel` |
| autocomplete, typeahead, combobox | `combobox` |
| select, dropdown list, listbox | `listbox` |
| breadcrumb, navigation trail | `breadcrumb` |
| tooltip, hint, hover text | `tooltip` |
| toggle, switch, on/off | `switch` |
| slider, range, volume control | `slider` or `slider-multithumb` |
| tree, file browser, nested list | `treeview` |
| data grid, spreadsheet, editable table | `grid` |
| static table, data table | `table` |
| toolbar, action bar, button group | `toolbar` |
| radio buttons, option group | `radio` |
| checkbox, check all | `checkbox` |
| show/hide, details, read more | `disclosure` |
| spinner, number input, stepper | `spinbutton` |
| meter, gauge, battery level | `meter` |
| feed, infinite scroll, timeline | `feed` |
| page structure, landmarks | `landmarks` |
| split view, resizable panes | `windowsplitter` |

---

## Screen-reader-only utility class

Always include and use this utility in your CSS:

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

---

## Pre-commit checklist (apply before finalizing any code)

Before considering any code complete, verify:

- [ ] All images have appropriate `alt` (informative) or `alt=""` (decorative)
- [ ] All form fields have associated labels
- [ ] Colour is never the sole means of conveying information
- [ ] All interactive elements are keyboard accessible
- [ ] Focus order is logical and follows visual order
- [ ] Focus indicator is visible on all interactive elements
- [ ] Page has valid `lang` attribute and language changes are marked
- [ ] Page has a unique, descriptive `<title>`
- [ ] Headings follow a logical hierarchy (no skipped levels)
- [ ] Semantic HTML elements are used (`<nav>`, `<main>`, `<header>`, `<footer>`)
- [ ] ARIA attributes are used correctly (prefer native HTML semantics first)
- [ ] Dynamic content changes are announced to assistive technologies
- [ ] No auto-playing media or animation without user control
- [ ] Links opening new windows are indicated

---

## When in doubt

1. **Look up the RAWeb criterion**: `bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh criterion <topic.criterion>`
2. **Check the test methodology**: `bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh methodology <topic.criterion.test>`
3. **Look up the ARIA pattern** for a component: `bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh find "<keyword>"` then `show <slug>`
4. **Consult the glossary** for precise definitions: `bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh glossary "<term>"`
5. Default to the most accessible approach — when two implementations are possible, choose the one with better assistive technology support
6. Prefer native HTML semantics over ARIA: a `<button>` is better than `<div role="button">`
7. When building an interactive widget, ALWAYS load the APG pattern first — do not guess ARIA attributes from memory
