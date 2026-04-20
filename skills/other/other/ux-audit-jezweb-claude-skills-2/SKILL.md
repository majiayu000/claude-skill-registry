---
name: ux-audit
description: "Exhaustive UX audit of a web app. Walks every thread a real user would follow, tests every interactive element, runs scenario battery (keyboard-only, heavy data, destructive actions, second user, interrupted workflow, wrong turn, returning user, first contact), produces ranked findings with screenshots, then offers a fix-and-verify loop. Requires a persona. Trigger with 'ux audit', 'dogfood this', 'audit the app', 'qa sweep', 'exhaustive test', 'check all pages'."
compatibility: claude-code-only
---

# UX Audit

Exhaustively audit a web app from the perspective of a real user. Two lenses, combined:

- **Flow lens** — walk the 3–5 real tasks a user would do ("threads"). Count clicks, mark dead ends, screenshot every state change.
- **Element lens** — after threads, sweep every interactive element not already hit. Forms, menus, toggles, edge data volumes.

Then run an eight-scenario battery (first contact, interrupted workflow, wrong turn recovery, returning user, keyboard only, heavy data, destructive confidence, second user) and close with a fix-and-verify loop for critical findings.

This is the thorough one. There is no quick mode. If the user wants a targeted check ("audit the dashboard"), scope the audit to that area — but within that area, still go exhaustive. Runtime is unbounded: assume a long-running session, write findings to the report incrementally, don't batch.

## Setup

Four things before any browsing. Stop if any fail.

### 1. Browser tool

| Target | Tool | Why |
|--------|------|-----|
| **Authenticated app** (internal tools, client apps) | Chrome MCP | Uses your real logged-in Chrome session — OAuth, cookies, RBAC just work |
| **Public site** (marketing, competitor, unauthed) | Playwright MCP | No login needed |
| **Neither available** | **Stop** | Ask the user to connect Chrome MCP or install Playwright |

Do **not** silently fall back to a fresh Playwright session for an authenticated app — the audit is worthless if you can't log in. If Chrome MCP isn't connected, stop and say: *"Open Chrome, click Connect in the Claude extension, then rerun."*

See [references/browser-tools.md](references/browser-tools.md) for commands.

### 2. URL

Prefer the deployed/live version — that's what real users see.

1. Check `wrangler.jsonc` for `pattern` or `custom_domain`
2. Check CLAUDE.md, README, `package.json` `homepage` field
3. Fall back to `lsof -i :5173 -i :3000 -i :8787 -t` for a running dev server
4. Ask the user

Live site has real auth, real latency, real CDN and CORS behaviour. Local misses deployment-specific bugs (missing env vars, broken asset paths, CORS, slow APIs). Only use local if the user asks or the feature isn't deployed.

### 3. Viewport

Pin the window at the start:

```
width: 1440, height: 900
```

This is the standard MacBook resolution and the audit's baseline. Responsive sweep (below) also tests 1280, 1024, 768, 375. **Do not go above 2000px wide** — it breaks the harness.

### 4. Persona

The audit needs a persona. Without one, findings drift toward generic "looks fine". Source in order:

1. **Argument** — if the user provided one ("ux audit as a busy insurance broker")
2. **Project personas** — read `.jez/personas/default.md` and `.jez/personas/<app-name>.md` if they exist
3. **Ask** — if neither, ask one question: *"Who uses this app and what are they trying to get done?"*

Capture: role, tech comfort, time pressure, emotional state, device context. A good persona predicts what they'd miss ("A receptionist between phone calls won't scroll below the fold").

### 5. Screenshot post-processing

On Retina Macs, Chrome captures screenshots at 2× the logical viewport — a 1440×900 window produces a 2880×1800 PNG. That's larger than the vision pipeline needs and wastes context. Downsize screenshots after each capture phase:

```bash
img-process batch ./screenshots --action optimise --max-width 1440
```

The `optimise` action is idempotent — no-op if already ≤ 1440px, downsize otherwise. Safe to run unconditionally, on every folder, at any point. At minimum, run it after each thread traversal and after the responsive sweep.

Playwright MCP users can set `deviceScaleFactor: 1` in the browser context to sidestep this entirely — screenshots match viewport 1:1. Chrome MCP has no equivalent flag, so post-process instead.

## Discovery

### Sitemap crawl

Build the complete page inventory before auditing any page.

1. **Router config** — read the app's route definitions (React Router, TanStack Router, Next.js app dir)
2. **Nav crawl** — click through every section and sub-section of the sidebar/menu
3. **Deep links** — URLs in CLAUDE.md, docs, or a prior audit report

One line per route, with purpose: `/app/clients — list of clients, search, add new`.

### Thread inventory

Identify 3–5 real tasks that make up a user's day. These are the spines of the audit.

Examples:
- **Insurance broker app**: renew a policy, create a new client, work through today's queue
- **Project management**: morning triage, update a task, send a client summary
- **SEO tool**: check latest crawl, diagnose a regression, export a report

How to find them:
- Ask the user if they know the app's use cases
- Read CLAUDE.md / README for "what this app does"
- Infer from top-level nav — each major section usually maps to a thread

Write them down. They structure the traversal phase.

### Element inventory

For each route as you reach it, list every interactive element:

```
/app/clients — 31 elements
  Buttons: Add Client, Import, Export, Filter, Sort (5)
  Inputs: Search
  Table: row-click ×N, star toggle ×N, action menu ×N
  Pagination: Next, Prev, page numbers, items-per-page
```

This inventory powers the coverage metric. After the audit you can say *"tested 29 of 31 elements on /app/clients; 2 pagination controls not reached due to data volume"*. Coverage becomes arithmetic, not a vibe.

Build inventories lazily — per-page as you traverse, not all up-front.

## Thread Traversal (primary phase)

For each thread:

1. **Start from the app entry point** — not mid-thread. Real users land at `/` or `/dashboard`.
2. **Walk as the persona** — if they'd skim, skim. If they'd misread a label, misread it. Note the hesitations.
3. **Screenshot every state change** — default → hover/focus → active → after click → after load → confirmation. Meaningful transitions, not every pixel movement. With modern context windows and sub-agent review, don't scrimp — the filmstrip is the evidence.
4. **Track the cost**:
   - Click count from entry to completion
   - Decision points (moments you stopped to think)
   - Dead ends (wrong paths and backtracks)
   - Interrupt recovery (close the tab at step 3, return at step 4 — did state survive?)
5. **Hand screenshots to a sub-agent for review** — at the end of each thread, dispatch: *"Here are 42 screenshots from Thread 2 (Create Client). Flag every moment of: unclear next action, broken visual hierarchy, lost context, confusing copy, missing feedback, anxiety, or 'did that work?'. Return structured findings."* The sub-agent returns a list; you stay focused on driving the browser.

At the end of each thread, answer three questions (as the persona):
- **Did it end clearly?** Did I know the task was done?
- **Would I come back?** Confidence, trust, momentum.
- **One thing to make this twice as easy?** Often the most actionable insight in the report.

See [references/walkthrough-checklist.md](references/walkthrough-checklist.md) for per-screen evaluation prompts and [references/workflow-comprehension.md](references/workflow-comprehension.md) for wayfinding, mental model, and page-to-page continuity.

## Element Exhaustion (completeness phase)

For each route, work the inventory. Skip elements already exercised by thread traversal.

| Element type | Test |
|--------------|------|
| Button | Click, screenshot result. If it opens a modal → test the modal. If it triggers an action → verify feedback. |
| Link | Follow it. Destination matches the label? |
| Input | Valid, invalid, empty, very long, special characters (`O'Brien`, `café`, emoji, `<script>`). |
| Select / dropdown | Every option. Verify behaviour per option. |
| Toggle / checkbox | On, off. Persistence on refresh? |
| Tab | Every tab. URL updates? Back button works? |
| Accordion | Expand, collapse. State saves? |
| Menu / context menu | Every item. Right-click for context menus. |
| Drag handle | Drag to new position. Drag to invalid target. |
| Pagination | Next, prev, jump, items-per-page. |

For **every form**:
- Valid data → verify creation/update/confirmation
- Invalid data → field-level error, form state preserved
- Empty submit → required-field marking
- Tab through fields → focus order logical

For **every list/table**, test at these volumes if data permits:
- 0 items (empty state)
- 1 item (pluralisation edge case)
- 100 items (pagination)
- 1000+ items (virtualisation, search, filter performance)

Write findings to the report as you go. Don't hold them in memory.

## Responsive Sweep

For each route:

| Width | Mode | Why |
|-------|------|-----|
| 1440px | light | Baseline (matches audit viewport) |
| 1280px | light | Standard desktop |
| 1024px | light | Tablet landscape / nav collapse point |
| 768px | light | Tablet portrait / stacked layout |
| 375px | light | Mobile / touch targets |
| 1440px | dark | Dark mode baseline |
| 375px | dark | Dark mode mobile |

On any page that breaks at an intermediate width, screenshot the transition point.

Run the automated layout-detection JS (overflow, clipping, invisible text) at each width — snippets in [references/walkthrough-checklist.md](references/walkthrough-checklist.md). Read console output after injection; every warning is a potential finding.

## Scenario Battery

Eight scenarios. All eight, always. They catch what screen-by-screen testing misses. Full protocols in [references/scenario-tests.md](references/scenario-tests.md).

1. **First Contact** — figure out the app with zero prior knowledge, then write a 2-minute plain-English guide to each thread. Gaps in the guide are UX gaps.
2. **Interrupted Workflow** — start a task, close the tab, refresh, navigate away mid-form. Does state survive?
3. **Wrong Turn Recovery** — deliberately click the wrong thing. How many clicks to get back on track? What context is lost?
4. **Returning User** — repeat a thread already done. Faster the second time? Shortcuts available? On the dashboard, can you tell what changed since last visit?
5. **Keyboard Only** — unplug the mouse. Can every thread complete keyboard-only? Focus visible? Tab order logical? Escape closes?
6. **Heavy Data** — seed with 500+ records. Lists virtualise? Search returns the right thing? Filters narrow meaningfully?
7. **Destructive Confidence** — for every delete, send, publish, pay, share: is consent clear? Does confirm copy tell you what's about to happen? Undo available?
8. **Second User** — log in as a restricted role (viewer not editor, client not staff). Read-only views coherent? Permissions errors make sense?

## Passive Error Sweeps

Run these throughout, not as a dedicated phase.

### Console errors

On every page load, check the browser console:
- JS errors (TypeError, ReferenceError) — **High**
- Framework warnings (key props, deprecated APIs) — **Medium**
- CSP violations — **Medium**
- Deprecation warnings — **Low**

### Network errors

Monitor network responses across the entire session. Visual browsing misses API failures — TanStack Query and SWR swallow errors and show empty/loading states instead. A "No results found" might actually be a 403.

| Status | Severity | Usual cause |
|--------|----------|-------------|
| 500+ | **Critical** | Server error |
| 403 | **High** | Permissions or route collision (static shadowed by `/:param`) |
| 404 | **Medium** | Missing endpoint |
| 401 | **Low** | Expected unauthenticated; flag on authenticated pages |
| CORS | **High** | Missing headers — production-only failure |

Chrome MCP: use `read_network_requests` after each page. Playwright: attach `page.on('response')` before browsing starts.

## Report

Write to `docs/ux-audit-YYYY-MM-DD.md` as you go. If `.jez/artifacts/` exists, use `.jez/artifacts/ux-audit-YYYY-MM-DD.md` instead.

Structure in [references/report-template.md](references/report-template.md):
- Summary
- Coverage metrics (threads walked, elements tested, inventoried coverage %)
- Findings by severity (Critical → Low) with screenshot refs
- Per-thread results
- Scenario battery results
- Network + console error inventory
- What works well
- Priority recommendations

**Severity:**
- **Critical** — user cannot complete the task
- **High** — confusion, friction, trust damage
- **Medium** — suboptimal, workable
- **Low** — polish

## Fix-and-Verify Loop

After writing the report, offer the loop:

*"Found N critical and M high issues. Fix them now and re-verify?"*

If yes:
1. Group findings by file/area
2. Patch each one
3. Re-walk just the affected slice (not the whole app)
4. Update the report: mark finding `✓ fixed`, `✗ still present`, or `⚠ new issue found`
5. Close with a "fixed in this session" summary

Closes the loop inside one session instead of waiting for a second audit pass tomorrow.

## Cross-reference with ux-extract

If a pattern library exists at `.jez/artifacts/ux-extracts/<ref>.md` or `docs/ux-extracts/<ref>.md`, read it before starting and use it as the bar. Findings can then say:

> *"Empty state on /app/clients shows no CTA. Reference (claude.ai) shows 3 keyboard shortcuts + 'New chat' button in the same position."*

Graceful if absent — the audit still works without a reference.

## Autonomy

- **Just do it**: Navigate, screenshot, read pages, inject layout-detection JS, submit forms with obviously-fake test data, write the report file, dispatch screenshot-review sub-agents
- **Ask first**: Destructive actions (delete, send, publish, pay). For Destructive Confidence testing, ask once before running that scenario
- **Stop and confirm**: Anything that emails/notifies external people

## Reference files

| When | Read |
|------|------|
| Per-screen evaluation questions | [references/walkthrough-checklist.md](references/walkthrough-checklist.md) |
| Workflow threads, wayfinding, mental model alignment, page-to-page continuity | [references/workflow-comprehension.md](references/workflow-comprehension.md) |
| Full protocol for each of the 8 scenarios | [references/scenario-tests.md](references/scenario-tests.md) |
| Report format and severity rubrics | [references/report-template.md](references/report-template.md) |
| Browser tool commands and viewport notes | [references/browser-tools.md](references/browser-tools.md) |

## Tips

- **Thread first, elements second.** If time is short, threads tell you more.
- **Sub-agents for screenshot review.** Don't drive the browser and analyse 200 screenshots in one loop.
- **Write findings incrementally.** The report file is cheaper memory than your context.
- **Stay in persona.** If you catch yourself thinking "a developer would know…" stop. Your persona doesn't.
- **Every hesitation is a finding.** If you paused to figure out what to click, that's friction worth reporting.
- **Coverage is arithmetic.** Inventoried ÷ tested. Publish the ratio in the report.
