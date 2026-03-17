---
name: browser
description: Browser automation CLI for AI agents. Use when testing web UIs, filling forms, taking screenshots, visual verification, or extracting page data. Triggers on "open browser", "click button", "screenshot", "visual diff", "test the page", "scrape", "fill form".
---

# Browser Automation

VERIFY AND INTERACT. Use agent-browser to prove UI changes work, test forms, extract data. Everything is ref-based: snapshot first, act by ref, verify by diff.

## Rules

- Always snapshot before acting — refs only exist after a snapshot
- Always re-snapshot after any DOM change — refs are snapshot-scoped
- Always wait for network idle on pages with async data before snapshotting
- Always close sessions when done — daemon leaks resources
- Never use CSS selectors — use @refs from snapshot or semantic locators
- SPA navigation: wait for route change to complete, not just the triggering click

## When to Use

| Need | Approach |
|------|----------|
| Prove UI change works | Visual verification flow |
| Test form behavior | Form testing flow |
| Site requires login | Auth flow first, then test |
| Extract structured data from page | Data extraction flow |
| Compare before/after visually | Diff-based evidence |
| Explore interactive elements | `snapshot -i` for interactive-only tree |

## Flow: Visual Verification

The core Claude Code use case — machine-verifiable proof that a UI change worked.

```
open URL → wait --load networkidle → screenshot before.png
→ [make code changes, reload app]
→ reload → wait --load networkidle → screenshot after.png
→ diff screenshot -b before.png → report mismatch %
```

Mismatch percentage is the evidence. Zero means identical. Non-zero means visible change — expected or not.

Use after: any UI change, hope:loop wave verification, hope:verify visual checks.

## Flow: Form Testing

Validate all form paths — happy, empty, invalid.

```
open URL → wait --load networkidle → snapshot -i
→ read refs from interactive elements
→ fill @ref "value" for each field → click @submit-ref
→ wait --load networkidle → snapshot → verify outcome
```

Test all three paths:
1. **Happy path** — fill valid data, submit, verify success state
2. **Empty submit** — submit without filling, verify validation messages appear
3. **Invalid input** — fill bad data (wrong email format, too-short password), submit, verify error states

Re-snapshot after each submission — refs invalidate on DOM change.

## Flow: Auth-Required Testing

Sessions persist browser state across commands — login once, test many.

```
agent-browser --session-name myapp open login-url
→ wait --load networkidle → snapshot -i
→ fill @username "user" → fill @password "pass" → click @login
→ wait --url "/dashboard" → snapshot → verify logged in
```

All subsequent commands reuse the session:
```
agent-browser --session myapp open /settings → snapshot -i
```

For CI: `state save ./auth.json` after login, `state load ./auth.json` before test runs.

## Flow: Data Extraction

Pull structured data from rendered pages.

```
open URL → wait --load networkidle → snapshot
→ eval --stdin to extract structured data
```

Simple values: `get text @ref` returns the text content of a single element.

Multi-line extraction for complex structures:
```bash
agent-browser eval --stdin <<'EOF'
JSON.stringify(
  [...document.querySelectorAll('.product')].map(el => ({
    name: el.querySelector('h2').textContent,
    price: el.querySelector('.price').textContent
  }))
)
EOF
```

## Flow: Semantic Locators

Alternative to refs when you know what you're looking for by label or role:

```bash
agent-browser find text "Submit" click
agent-browser find label "Email" fill "user@example.com"
agent-browser find role "button" click
agent-browser find placeholder "Search..." fill "query"
agent-browser find testid "login-btn" click
```

Locator type first, then value, then action. Defaults to `click` if no action specified.

## Composition

- **With portless:** use `myapp.localhost:1355` URLs — stable across restarts, no port guessing
- **With watch:** d3k monitors server + browser while agent-browser interacts — full context alongside automation via `d3k agent-browser --cdp $(d3k cdp-port)`
- **With hope:loop:** browser diff output as verification evidence in wave reports
- **With hope:verify:** screenshot diffs for visual regression assertions in pre-PR checks

## Anti-Patterns

- **Acting without snapshotting** — blind interaction with no refs, guaranteed failure
- **Assuming refs persist across navigations** — every DOM change invalidates all refs
- **Hardcoding port numbers** — use portless URLs; ports change between restarts
- **Screenshotting without waiting** — captures loading spinners, not the actual page
- **Forgetting to close sessions** — daemon accumulates across test runs, leaking resources
- **Snapshotting full page when only forms matter** — `snapshot -i` filters to interactive elements only
