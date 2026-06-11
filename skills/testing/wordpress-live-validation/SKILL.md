---
name: wordpress-live-validation
description: "Validate published WordPress posts in browser via Playwright."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_wait_for
  - mcp__plugin_playwright_playwright__browser_snapshot
  - mcp__plugin_playwright_playwright__browser_evaluate
  - mcp__plugin_playwright_playwright__browser_network_requests
  - mcp__plugin_playwright_playwright__browser_console_messages
  - mcp__plugin_playwright_playwright__browser_resize
  - mcp__plugin_playwright_playwright__browser_take_screenshot
  - mcp__chrome-devtools__navigate_page
  - mcp__chrome-devtools__take_screenshot
  - mcp__chrome-devtools__take_snapshot
  - mcp__chrome-devtools__list_console_messages
  - mcp__chrome-devtools__list_network_requests
  - mcp__chrome-devtools__lighthouse_audit
  - mcp__chrome-devtools__resize_page
routing:
  triggers:
    - validate wordpress post
    - check live post
    - verify published post
    - wordpress post looks right
    - check og tags live
    - responsive check wordpress
    - post rendering check
    - live site validation
  pairs_with:
    - publish
    - e2e-testing
  complexity: Medium
  category: content-publishing
---

# WordPress Live Validation Skill

## Overview

This skill loads a real WordPress post in a Playwright headless browser and verifies that what readers see matches what was uploaded. **The browser is the source of truth** -- REST API success does not guarantee correct rendering.

**Browser backend selection**: Playwright MCP (default) is used for automated validation and CI/CD. Use Chrome DevTools MCP when the user explicitly asks to "check in my browser" or "debug live", or when the task involves Lighthouse audits or performance profiling.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| check specifications: severities, edge cases, JS extraction | `validation-checks.md` | Loads detailed guidance from `validation-checks.md`. |
| Playwright MCP tool signatures, pitfalls, availability detection | `playwright-tools.md` | Loads detailed guidance from `playwright-tools.md`. |
| step-by-step NAVIGATE, VALIDATE, RESPONSIVE procedures | `phase-checks.md` | Loads detailed guidance from `phase-checks.md`. |
| Phase 4 REPORT output format | `output-format.md` | Loads detailed guidance from `output-format.md`. |
| post-upload validation walkthrough; wordpress-uploader integration | `examples.md` | Loads detailed guidance from `examples.md`. |
| errors, error handling | `error-handling.md` | Loads detailed guidance from `error-handling.md`. |

## Instructions

### Constraints (Always Applied)

1. **Read-Only Observation Only**: Never click, type, fill forms, or modify anything on the WordPress site. This is observation-only validation—any write action risks mutating published content.

2. **Evidence-Based Reporting**: Every check result must reference a concrete artifact (DOM value, network response, screenshot path). "Looks fine" is not acceptable. Report what the browser shows, not assumptions.

3. **Non-Blocking Reports**: Failed validation produces a report but does not revert the upload or block the pipeline. The user decides how to act on findings.

4. **Severity Classification** (enforce strictly):
   - **BLOCKER**: Readers see broken content (missing title, broken images, placeholder text, wrong H1)
   - **WARNING**: Degraded quality but functional (missing OG tags, JS errors, responsive overflow)
   - **INFO**: Informational only (rendered values without comparison baseline)
   - Never inflate or deflate—alert fatigue and hidden problems are equal harms.

5. **Browser Availability**: Requires either Playwright MCP or Chrome DevTools MCP. If neither is available, exit in Phase 1 with a skip report. Do not retry.

6. **Default Behaviors** (ON):
   - Run all check categories (content integrity, SEO/social, responsive)
   - Test three breakpoints: mobile (375px), tablet (768px), desktop (1440px)
   - Save screenshots at each breakpoint as evidence
   - Exclude known benign console patterns: ad networks (doubleclick, googlesyndication), analytics (gtag, fbevents), consent managers (cookiebot, onetrust)
   - Try content selectors in order: `article` → `.entry-content` → `.post-content` → `main`

7. **Optional Behaviors** (OFF unless enabled):
   - Draft preview mode (requires authenticated WordPress session)
   - Custom content selector override
   - Strict mode (treat all WARNINGs as BLOCKERs)
   - OG image fetch verification (navigates to og:image URL to check 200 response)

8. **Input Requirements**:
   - WordPress post URL (from wordpress-uploader, direct user input, or `{WORDPRESS_SITE}/?p={post_id}&preview=true`)
   - Optional: expected title (for title match comparison)
   - Optional: expected H2 count (for structure comparison)
   - Optional: custom content selector

---

### Phase 1: NAVIGATE

**Goal**: Load the WordPress post and confirm the content area is present.

See `references/phase-checks.md` "Phase 1: NAVIGATE — Detailed Steps" for the 4-step procedure (verify browser MCP availability, navigate, wait for content area with selector chain, remove cookie/consent banners with the JS snippet).

**GATE**: Page loaded with HTTP 200 (or 30x redirect to 200), content selector found. If 4xx/5xx or no selector found: capture screenshot, report FAIL with HTTP status, STOP. Do not proceed to Phase 2.

---

### Phase 2: VALIDATE

**Verification means execution, not reasoning.** Run the command. Do not reason about whether the command would pass. Do not summarize the expected output. Execute the check, paste the exit code, paste the relevant output. A verification phase that produces a verdict without an observed tool result is not a verification — it is a guess with a rigor aesthetic.

**Goal**: Inspect rendered DOM and network activity for content integrity and SEO completeness. Run all checks without stopping on individual failures.

The 7 checks (with severity, JS extraction snippets, and pass/fail criteria) are documented in `references/phase-checks.md` "Phase 2: VALIDATE — All 7 Checks":

1. **Title Match** (BLOCKER)
2. **H2 Structure** (WARNING)
3. **Image Loading** (BLOCKER)
4. **JavaScript Console Errors** (WARNING)
5. **OG Tags** (WARNING)
6. **Meta Description** (WARNING)
7. **Placeholder/Draft Text** (BLOCKER)

**GATE**: All 7 checks executed, each with severity and evidence. Proceed to Phase 3.

---

### Phase 3: RESPONSIVE CHECK

**Goal**: Verify rendering at three standard breakpoints. Capture visual evidence.

Test each viewport in sequence:

| Viewport | Width | Height | Represents |
|----------|-------|--------|------------|
| Mobile | 375 | 812 | iPhone-class |
| Tablet | 768 | 1024 | iPad-class |
| Desktop | 1440 | 900 | Standard laptop |

See `references/phase-checks.md` "Phase 3: RESPONSIVE CHECK — Detailed Steps" for the per-viewport 4-step procedure (resize, screenshot, overflow check, container visibility check) with the JS snippets.

**GATE**: Screenshots captured at all three viewports. Overflow and visibility recorded. Proceed to Phase 4.

---

### Phase 4: REPORT

**Goal**: Produce structured pass/fail report with severity counts and evidence artifacts.

See `references/output-format.md` for the full report template, status markers (`[PASS]`, `[FAIL]`, `[WARN]`, `[INFO]`, `[SKIP]`), and result classification rules.

**GATE**: Report generated with accurate severity counts. Screenshots saved. Result matches blocker tally.

---

## Integration with wordpress-uploader

When invoked after `wordpress-uploader`, this skill acts as an optional **Phase 5: POST-PUBLISH VALIDATION**. See `references/examples.md` for the integration flow and the `post_url` / `post_id` / `--title` inputs the uploader provides.

The validation is **non-blocking by default**: a FAIL result produces a report for the user but does not revert the upload. The user decides whether to act on findings.

---

## Examples

See `references/examples.md` for worked examples (post-upload validation, standalone live check, OG tag verification) and the wordpress-uploader integration flow.

---

## Error Handling

See `references/error-handling.md` for the full error matrix (Playwright MCP not available, page returns 4xx/5xx, content selector not found, network timeout on image checks, cookie banner blocks content).

---

## References

For detailed check specifications and Playwright tool usage:
- **Validation Checks**: [references/validation-checks.md](references/validation-checks.md) – severity rationale, edge cases, and extended check specifications
- **Playwright Tools**: [references/playwright-tools.md](references/playwright-tools.md) – MCP tool signatures, usage patterns, and common pitfalls
- **Phase Check Details**: [references/phase-checks.md](references/phase-checks.md) – Phase 1/2/3 step-by-step procedures with JS snippets
- **Output Format**: [references/output-format.md](references/output-format.md) – Phase 4 report template, status markers, result classification
- **Examples**: [references/examples.md](references/examples.md) – worked examples and wordpress-uploader integration flow
- **Error Handling**: [references/error-handling.md](references/error-handling.md) – full error matrix for browser availability, HTTP failures, selector misses, network timeouts, cookie banners

### Complementary Skills
- [pre-publish-checker](../pre-publish-checker/SKILL.md) – validates source markdown before upload (complementary, not overlapping)
- [wordpress-uploader](../wordpress-uploader/SKILL.md) – uploads content to WordPress (upstream integration)
- [seo-optimizer](../seo-optimizer/SKILL.md) – validates SEO properties against source (data consumer of this skill's output)
- [endpoint-validator](../endpoint-validator/SKILL.md) – similar validation pattern for API endpoints
