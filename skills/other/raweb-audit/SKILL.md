---
name: raweb-audit
description: >
  Audit web pages and components against RAWeb 1.1 (Luxembourg Web Accessibility
  Framework). Use when reviewing existing code for accessibility compliance,
  generating audit reports, checking conformance levels, or preparing for
  Luxembourg accessibility certification. Covers all 17 themes with systematic
  test procedures. Default target: Level AA.
metadata:
  author: luxembourg-accessibility-skillset
  version: 1.2.0
  raweb-version: "1.1"
  wcag-version: "2.1"
  license: CC-BY-3.0-LU
  source: https://github.com/accessibility-luxembourg/ReferentielAccessibiliteWeb
allowed-tools: Bash Read Grep
---

# RAWeb 1.1 — Accessibility Audit Skill

You are an accessibility auditor. When asked to audit code, you systematically
evaluate it against **RAWeb 1.1** criteria (Level AA by default). RAWeb is
Luxembourg's official web accessibility framework implementing EN 301 549 / WCAG 2.1.

## Reference data

Use the lookup script to query the full RAWeb 1.1 criteria database:

```bash
# List all topics
!`${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh topics`

# Look up a specific criterion
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh criterion <topic.criterion>

# Full test methodology for a specific test
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh methodology <topic.criterion.test>

# All criteria at a given level
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh level AA

# Search criteria by keyword
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh search "<keyword>"

# Glossary definitions
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh glossary "<term>"
```

Raw JSON files: `${CLAUDE_SKILL_DIR}/references/`

### Component pattern references (WAI-ARIA APG)

When auditing interactive components (dialogs, tabs, menus, carousels, etc.),
verify their implementation against the correct WAI-ARIA pattern:

```bash
# Find the expected pattern for a component
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh find "<keyword>"

# Show full expected keyboard + ARIA spec for a component
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh show <slug>

# Check which patterns use a specific ARIA role
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh roles "<role>"

# List all 30 available patterns
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh list
```

Individual pattern files: `${CLAUDE_SKILL_DIR}/references/components/<slug>.json`

Each pattern file contains the expected `keyboard_interactions`, `aria.roles`,
`aria.required_attributes`, and `aria.optional_attributes` as defined by the APG.
Use these as the **source of truth** when checking whether a component's ARIA
implementation is correct and complete (RAWeb criteria 7.1, 7.3, 12.8).

---

## Audit methodology

### Step 1: Determine scope

Before auditing, clarify:
- **Target level**: A or AA (default: AA)
- **Scope**: full page, specific component, or page sample
- **Themes to focus on**: all 17, or specific themes relevant to the content

### Step 2: Systematic evaluation by theme

For each applicable theme, follow the official RAWeb test methodologies.
ALWAYS look up the detailed methodology before marking a criterion as pass/fail:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh methodology <topic.criterion.test>
```

### Step 3: Report findings

Use the structured report format below.

---

## Audit execution: Theme-by-theme checklist

When performing a full audit, evaluate the following themes in order.
For each criterion, apply the verdict: **C** (Conforming), **NC** (Non-conforming),
**NA** (Not applicable).

### Theme 1 — Images
Scan for: `<img>`, `<svg>`, `<canvas>`, `<object>`, `<embed>`, `<area>`, `[role="img"]`, `<input type="image">`

| Check | Criteria |
|-------|----------|
| Informative images have text alternatives | 1.1 |
| Decorative images are properly hidden | 1.2 |
| Text alternatives are relevant and concise | 1.3 |
| CAPTCHA/test images have correct alternatives | 1.4 |
| CAPTCHA has a non-visual alternative | 1.5 |
| Complex images have detailed descriptions | 1.6 |
| Detailed descriptions are relevant | 1.7 |
| Images of text have CSS alternatives (AA) | 1.8 |
| Images of text with captions have relevant alternatives | 1.9 |

### Theme 2 — Frames
Scan for: `<iframe>`, `<frame>`

| Check | Criteria |
|-------|----------|
| Frames have `title` attributes | 2.1 |
| Frame titles are relevant | 2.2 |

### Theme 3 — Colours
Requires visual inspection and contrast analysis tools.

| Check | Criteria |
|-------|----------|
| Information not conveyed by colour alone | 3.1 |
| Text contrast ≥ 4.5:1 (normal) / 3:1 (large) — AA | 3.2 |
| Non-text contrast ≥ 3:1 — AA | 3.3 |

### Theme 4 — Multimedia
Scan for: `<video>`, `<audio>`, `<object>`, `<embed>`, `<canvas>`, `<svg>`, `<bgsound>`

| Check | Criteria |
|-------|----------|
| Pre-recorded media has text transcript | 4.1 |
| Captions present and relevant | 4.1, 4.3 |
| Audio description available (AA) | 4.5, 4.6 |
| Media controls are keyboard accessible | 4.10 |
| No auto-playing audio > 3 seconds | 4.11 |

### Theme 5 — Tables
Scan for: `<table>`, `<th>`, `<td>`, `<caption>`, `[role="table"]`

| Check | Criteria |
|-------|----------|
| Data tables identified with appropriate markup | 5.1, 5.3 |
| Tables have captions/titles | 5.4 |
| Tables have summaries when complex | 5.5 |
| Header cells use `<th>` with `scope` | 5.6, 5.7 |
| Layout tables do not use table semantics | 5.8 |

### Theme 6 — Links
Scan for: `<a>`, `[role="link"]`

| Check | Criteria |
|-------|----------|
| Links have accessible names | 6.1 |
| Link text is relevant to destination | 6.1 |
| Link accessible names include visible text | 6.2 |

### Theme 7 — Scripts
Scan for: `onclick`, `onkeydown`, `addEventListener`, `[role]`, `[aria-*]`, `[tabindex]`

| Check | Criteria |
|-------|----------|
| Script elements keyboard operable | 7.1 |
| Script content accessible to AT | 7.2 |
| Script elements can be navigated in order | 7.3 |
| Status messages use appropriate ARIA roles | 7.4 |
| Animated/moving content has controls (AA) | 7.5 |

### Theme 8 — Mandatory Elements
Full-page checks.

| Check | Criteria |
|-------|----------|
| Valid DOCTYPE and no parsing errors | 8.1, 8.2 |
| `lang` attribute on `<html>` is valid | 8.3, 8.4 |
| Page `<title>` is present and relevant | 8.5, 8.6 |
| Language changes marked with `lang` (AA) | 8.7, 8.8 |
| No duplicate `id` attributes | 8.2 |
| Opening/closing tags properly nested | 8.1 |

### Theme 9 — Information Structure
Scan for: `<h1>`–`<h6>`, `<ul>`, `<ol>`, `<dl>`, `<blockquote>`, `<header>`, `<nav>`, `<main>`, `<footer>`, `<aside>`, `<section>`, `<article>`

| Check | Criteria |
|-------|----------|
| Headings logically ordered (no skipped levels) | 9.1 |
| Document structure uses landmarks | 9.2 |
| Lists use proper markup | 9.3 |
| Quotations properly marked | 9.4 |

### Theme 10 — Presentation of Information
CSS and layout checks.

| Check | Criteria |
|-------|----------|
| CSS used for presentation, not HTML attributes | 10.1 |
| Content readable without CSS | 10.2, 10.3 |
| Content usable at 200% zoom (AA) | 10.4 |
| Content reflows at 320px CSS width (AA) | 10.11 |
| Visible focus on all interactive elements | 10.7 |
| Hidden content not keyboard-trapping | 10.8 |
| Custom text spacing does not break content (AA) | 10.12 |
| Custom user properties can override (AA) | 10.13 |

### Theme 11 — Forms
Scan for: `<form>`, `<input>`, `<select>`, `<textarea>`, `<button>`, `<fieldset>`, `<legend>`, `<label>`, `[role="form"]`

| Check | Criteria |
|-------|----------|
| All fields have associated labels | 11.1 |
| Labels are relevant | 11.2 |
| Labels include visible text in accessible name | 11.2 |
| Grouped fields use `<fieldset>/<legend>` | 11.5 |
| Required fields indicated before or at field | 11.10 |
| Error messages linked to fields and descriptive (AA) | 11.11 |
| `autocomplete` used for personal data (AA) | 11.13 |

### Theme 12 — Navigation
Full-page/site checks.

| Check | Criteria |
|-------|----------|
| ≥2 navigation mechanisms (nav, sitemap, search) — AA | 12.1 |
| Navigation consistent across pages (AA) | 12.2 |
| Skip links present and functional | 12.7 |
| Tab order logical | 12.8 |
| No positive `tabindex` values | 12.8 |
| Active page indicated in navigation | 12.2 |
| Navigation landmarks labelled when multiple | 12.3 |

### Theme 13 — Consultation
Behavioural and interaction checks.

| Check | Criteria |
|-------|----------|
| No uncontrollable refreshes or redirects | 13.1 |
| New windows indicated to user | 13.2 |
| Downloads indicate format and size | 13.3 |
| Time limits adjustable | 13.1 |
| No unexpected context changes | 13.1 |
| No content flashing > 3 times/second | 13.8 |
| Moving content has pause/stop controls | 13.8 |

### Themes 14–17 (EN 301 549 Extended)
These themes go beyond standard WCAG web testing and cover documentation,
editing tools, support services, and real-time communication. Query them
individually when relevant:

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh topic 14  # Documentation & accessibility features
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh topic 15  # Editing tools
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh topic 16  # Support services
bash ${CLAUDE_SKILL_DIR}/scripts/raweb-lookup.sh topic 17  # Real-time communication
```

---

## Report format

When presenting audit results, use this structured format:

```markdown
# RAWeb 1.1 Accessibility Audit Report

**Page/Component**: [name or URL]
**Date**: [date]
**Target level**: AA
**Scope**: [full page / component / sample description]

## Summary

| Metric | Count |
|--------|-------|
| Criteria evaluated | XX |
| Conforming (C) | XX |
| Non-conforming (NC) | XX |
| Not applicable (NA) | XX |
| **Conformance rate** | **XX%** |

## Critical issues (must fix)

### Issue 1: [Short title]
- **Criterion**: RAWeb X.X (Level A/AA) — [criterion title]
- **WCAG**: X.X.X [SC name]
- **Location**: [file:line or selector]
- **Problem**: [description of the violation]
- **Impact**: [which users are affected and how]
- **Remediation**: [specific fix with code example]
- **Priority**: Critical / Major / Minor

## Detailed results by theme

### Theme X: [Name]

| Criterion | Level | Verdict | Notes |
|-----------|-------|---------|-------|
| X.1 | A | C / NC / NA | [detail] |
| X.2 | AA | C / NC / NA | [detail] |

## Recommendations

[Prioritised list of improvements beyond strict compliance]
```

---

## Code scanning patterns

When auditing code files, use these search patterns to identify potential issues:

```bash
# Images without alt
grep -rn '<img ' --include="*.html" --include="*.jsx" --include="*.tsx" --include="*.vue" | grep -v 'alt='

# Empty links
grep -rn '<a[^>]*>[[:space:]]*</a>' --include="*.html" --include="*.jsx" --include="*.tsx"

# Positive tabindex
grep -rn 'tabindex="[1-9]' --include="*.html" --include="*.jsx" --include="*.tsx"

# onclick without keyboard equivalent
grep -rn 'onclick' --include="*.html" | grep -v '<button\|<a '

# Missing form labels
grep -rn '<input\|<select\|<textarea' --include="*.html" --include="*.jsx" --include="*.tsx" | grep -v 'aria-label\|aria-labelledby\|id='

# Autoplaying media
grep -rn 'autoplay' --include="*.html" --include="*.jsx" --include="*.tsx"

# Iframes without title
grep -rn '<iframe' --include="*.html" --include="*.jsx" --include="*.tsx" | grep -v 'title='

# Missing lang attribute
grep -rn '<html' --include="*.html" | grep -v 'lang='

# Colour-only indicators (potential — needs manual review)
grep -rn 'color:.*red\|color:.*green\|text-red\|text-green\|text-danger\|text-success' --include="*.css" --include="*.scss"
```

---

## Severity classification

| Level | Description | Example |
|-------|-------------|---------|
| **Critical** | Blocks access entirely for some users | Missing form labels, keyboard traps, no alt on critical images |
| **Major** | Significant barrier but workaround exists | Poor contrast, missing skip links, ambiguous link text |
| **Minor** | Inconvenience but does not block access | Missing `lang` on inline foreign text, redundant ARIA |

---

## When auditing, ALWAYS:

1. **Look up the exact criterion** before rendering a verdict — do not rely on memory
2. **Apply the official test methodology** from `methodologies.json`
3. **Check the expected ARIA pattern** for interactive components: `bash ${CLAUDE_SKILL_DIR}/scripts/raweb-component-lookup.sh show <slug>` — verify keyboard interactions, required roles, and required attributes match the APG specification
4. **Use precise RAWeb criterion numbers** (e.g., "RAWeb 11.1", not just "WCAG 1.3.1")
5. **Include the WCAG mapping** for cross-reference (found in the criterion's `references`)
6. **Provide actionable remediation** with code examples — when the fix involves an ARIA widget, include the correct pattern from the component reference
7. **Distinguish between Level A and AA** violations — both are required for conformance, but Level A failures are more critical
8. **Note when automated testing is insufficient** — many criteria require manual verification (contrast on images, relevance of alternatives, etc.)
