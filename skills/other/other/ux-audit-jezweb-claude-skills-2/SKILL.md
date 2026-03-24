---
name: ux-audit
description: "Dogfood web apps — browse as a real user, notice friction, document findings. Adopts a user persona, tracks emotional friction (trust, anxiety, confusion), counts click efficiency, tests resilience (mid-form navigation, back button, refresh), and asks 'would I come back?'. Produces ranked audit reports. Trigger with 'ux audit', 'dogfood this', 'ux walkthrough', 'qa test', 'test the app', or 'check all pages'."
compatibility: claude-code-only
---

# UX Audit

Dogfood web apps by browsing them as a real user would — with their goals, their patience, and their context. Goes beyond "does it work?" to "is it good?" by tracking emotional friction (trust, anxiety, confusion), counting click efficiency, testing resilience, and asking the ultimate question: "would I come back?" Uses Chrome MCP (for authenticated apps with your session) or Playwright for browser automation. Produces structured audit reports with findings ranked by impact.

## Browser Tool Detection

Before starting any mode, detect available browser tools:

1. **Chrome MCP** (`mcp__claude-in-chrome__*`) — preferred for authenticated apps. Uses the user's logged-in Chrome session, so OAuth/cookies just work.
2. **Playwright MCP** (`mcp__plugin_playwright_playwright__*`) — for public apps or parallel sessions.
3. **playwright-cli** — for scripted flows and sub-agent browser tasks.

If none are available, inform the user and suggest installing Chrome MCP or Playwright.

See [references/browser-tools.md](references/browser-tools.md) for tool-specific commands.

## URL Resolution

If the user didn't provide a URL, find one automatically. **Prefer the deployed/live version** — that's what real users see.

1. **Check wrangler.jsonc** for custom domains or `routes`:
   ```bash
   grep -E '"pattern"|"custom_domain"' wrangler.jsonc 2>/dev/null
   ```
   If found, use the production URL (e.g. `https://app.example.com`).

2. **Check for deployed URL** in CLAUDE.md, README, or package.json `homepage` field.

3. **Fall back to local dev server** — check if one is already running:
   ```bash
   lsof -i :5173 -i :3000 -i :8787 -t 2>/dev/null
   ```
   If running, use `http://localhost:{port}`.

4. **Ask the user** as a last resort.

**Why live over local**: The live site has real data, real auth, real network latency, real CDN behaviour, and real CORS/CSP policies. Testing locally misses deployment-specific issues (missing env vars, broken asset paths, CORS errors, slow API responses). The UX audit should test what the user actually experiences.

**When local is better**: The user explicitly says "test localhost", or the feature isn't deployed yet.

## Depth Levels

Control how thorough the audit is. Pass as an argument: `/ux-audit quick`, `/ux-audit thorough`, or default to standard.

| Depth | Duration | Autonomy | What it covers |
|-------|----------|----------|---------------|
| **quick** | 5-10 min | Interactive | One user flow, happy path only. Spot check after a change. |
| **standard** | 20-40 min | Semi-autonomous | Full walkthrough + QA sweep of main pages. Default. |
| **thorough** | 1-3 hours | Fully autonomous | Multiple personas, all pages, all modes combined. Overnight mode. |
| **exhaustive** | 4-8+ hours | Fully autonomous | Every interactive element on every page. Every button clicked, every dialog opened, every form filled, every state triggered. Leave nothing untested. |

### Exhaustive Mode

The exhaustive mode goes beyond thorough. Thorough tests workflows and pages. Exhaustive tests **every single interactive element** in the application.

For each page discovered:
1. **Inventory all interactive elements** — buttons, links, inputs, selects, checkboxes, toggles, tabs, accordions, modals triggers, dropdowns, context menus, drag handles, sliders
2. **Click/interact with every one** — open every dialog, expand every accordion, select every tab, toggle every switch, trigger every dropdown
3. **Screenshot each state** — default, hover, active, open, closed, expanded, collapsed, selected, error
4. **Test every form** — fill with valid data, submit. Fill with invalid data, submit. Leave empty, submit. Test every field individually.
5. **Test every combination** — if there are filters, test each filter value. If there are tabs, test each tab. If there are sort options, test each sort.
6. **Dark mode + light mode** — every page, every dialog, every state in both modes
7. **Three viewport widths** — 1280px, 768px, 375px for every page and dialog
8. **Keyboard navigation** — tab through every page, verify focus order, test Enter/Space/Escape on every interactive element
9. **Right-click/context menus** — if the app has custom context menus, test every option in every context
10. **Edge states** — what happens with 0 items, 1 item, 100 items, 1000 items? What happens with very long text in every field?
11. **Concurrent tabs** — open the same page in two tabs, interact in both, check for conflicts
12. **Every error path** — trigger every validation error, every 404, every permission denied, every timeout

**Progress tracking**: This mode generates a LOT of findings. Write findings to the report incrementally — don't hold everything in memory. Update `docs/ux-audit-exhaustive-YYYY-MM-DD.md` after each page is complete.

**Element inventory format** (per page):
```
/clients — 47 interactive elements
  [x] "Add Client" button — opens modal ✓, form submits ✓, validation ✓
  [x] Search input — filters correctly ✓, clear button works ✓, empty search ✓
  [x] Sort dropdown — all 4 options work ✓, persists on navigation ✗ (BUG)
  [x] Client row click — navigates to detail ✓
  [x] Star button — toggles ✓, persists on refresh ✓
  [ ] Pagination — next ✓, prev ✓, page numbers ✓, items per page ✗ (not tested - no data)
  ...
```

### Thorough Mode: Overnight Workflow

The thorough mode is designed to run unattended. Kick it off at end of day, review the report in the morning. The user should NOT need to find issues themselves — this mode catches everything.

**Mindset**: Don't run through a checklist. Think about the real person who will use this app every day. What are the threads of their workday? How will they move through the system? Will they understand what they're looking at? Will the app teach them how to use it through its design, or will they be guessing? Read [references/workflow-comprehension.md](references/workflow-comprehension.md) before starting.

1. **Discover all routes** — read router config, crawl navigation, build complete page inventory
2. **Identify workflow threads** — what are the 3-5 real tasks a user does in a day? Map them before testing individual pages. See [references/workflow-comprehension.md](references/workflow-comprehension.md).
3. **Create a task list** — track progress across the audit
4. **Visual & layout sweep** (every page):
   - Screenshot at 1280px, 1024px, 768px, 375px widths
   - Screenshot in light mode and dark mode
   - Run JS overflow detection on each page (see below)
   - Check for clipped text, overlapping elements, broken grids
   - Compare sidebar + content alignment across all pages
4. **Workflow thread testing** — follow each identified thread end to end:
   - Does the next step suggest itself at every point?
   - Can the user leave and come back without losing their place?
   - Do transitions between pages preserve context (filters, selections)?
   - Do nav labels match how a user would describe their work?
   - After creating/saving/deleting, does the app take them somewhere logical?
5. **UX Walkthrough x3 personas**:
   - First-time user (non-technical, time-poor, first visit)
   - Power user (daily user, knows the app, looking for efficiency)
   - Mobile user (phone, touch targets, small viewport)
6. **Full QA sweep** — every page, all CRUD, all states (empty, error, loading, populated)
7. **Resilience testing** — every form: bad data, mid-navigation, back button, refresh, double-submit
8. **Accessibility basics** — heading hierarchy, alt text, focus order, colour contrast
9. **Console error sweep** — check browser console on every page for JS errors, failed network requests, deprecation warnings
10. **Wayfinding & comprehension check** — on each page: do I know where I am? Can I get back? Does the heading tell me what I can do here? Are visual cues guiding me to the right action?
11. **Scenario tests** — run all six from [references/scenario-tests.md](references/scenario-tests.md):
    - New hire onboarding (can you figure out the app with zero guidance?)
    - Interrupted workflow (start a task, close the tab, come back — what survived?)
    - Wrong turn recovery (go to the wrong page, how many clicks to get back on track?)
    - Day two (repeat the same tasks — is it faster? are there shortcuts?)
    - Explain it to a colleague (write a 2-min guide for each workflow — gaps = UX failures)
    - What changed? (log in after creating data — can you tell what needs attention?)
12. **Screenshot everything** — save to `.jez/screenshots/ux-audit/` (numbered chronologically)
13. **Comprehensive report** — `docs/ux-audit-thorough-YYYY-MM-DD.md` with issue counts by severity
14. **Summary** — top 5 critical issues, workflow gaps, scenario test results, "one thing to fix first"

#### Automated Layout Detection (JS Injection)

On each page, inject JavaScript via the browser tool to programmatically detect layout issues:

```javascript
// Detect elements overflowing their parent
document.querySelectorAll('*').forEach(el => {
  const r = el.getBoundingClientRect();
  const p = el.parentElement?.getBoundingClientRect();
  if (p && (r.left < p.left - 1 || r.right > p.right + 1)) {
    console.warn('OVERFLOW:', el.tagName, el.className, 'extends beyond parent');
  }
});

// Detect text clipped by containers
document.querySelectorAll('h1,h2,h3,h4,p,span,a,button,label').forEach(el => {
  if (el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2) {
    console.warn('CLIPPED:', el.tagName, el.textContent?.slice(0,50));
  }
});

// Detect elements with zero or negative visibility
document.querySelectorAll('*').forEach(el => {
  const s = getComputedStyle(el);
  const r = el.getBoundingClientRect();
  if (r.width > 0 && r.height > 0 && r.left + r.width < 0) {
    console.warn('OFF-SCREEN LEFT:', el.tagName, el.className);
  }
});

// Detect low contrast text (rough check)
document.querySelectorAll('h1,h2,h3,p,span,a,li,td,th,label,button').forEach(el => {
  const s = getComputedStyle(el);
  if (s.color === s.backgroundColor || s.opacity === '0') {
    console.warn('INVISIBLE TEXT:', el.tagName, el.textContent?.slice(0,30));
  }
});
```

Read console output after injection. Each warning is a potential finding to screenshot and investigate.

#### Responsive Breakpoint Sweep

For each page, resize the viewport through standard breakpoints and screenshot:

| Width | What it represents | Check for |
|-------|-------------------|-----------|
| 1280px | Desktop (standard) | Baseline layout, sidebar + content |
| 1024px | Small desktop / tablet landscape | Nav collapse point, grid reflow |
| 768px | Tablet portrait | Sidebar behaviour, stacked layout |
| 375px | Mobile | Everything stacked, touch targets, no horizontal scroll |

If the layout changes between breakpoints (sidebar collapses, grid reduces columns), screenshot the transition point too.

#### Console Error Sweep

On each page, read the browser console for:
- **JS errors** (TypeError, ReferenceError, etc.) — severity: High
- **Failed network requests** (404, 500, CORS) — severity: High
- **React/framework warnings** (key props, deprecated APIs) — severity: Medium
- **CSP violations** — severity: Medium
- **Deprecation warnings** — severity: Low

#### Network Error Detection (thorough + exhaustive)

**Critical**: Visual browsing misses API failures that the UI hides. Data-fetching libraries (TanStack Query, SWR) swallow HTTP errors and show empty/loading states instead of error messages. A component showing "No results found" might actually be getting a 403 — but the UI looks normal.

Monitor network responses throughout the entire audit session. If using Playwright, attach a response listener before browsing starts:

```javascript
// Inject into page or use Playwright's page.on('response')
// Collect all non-2xx API responses
const networkErrors = [];
// After each page navigation, check for failed fetch/XHR requests
// by reading the browser's network log or console output
```

If using Chrome MCP, use `read_network_requests` to check for failed API calls after each page visit.

**What to collect**: URL, HTTP status, method, the page you were on when it happened.

**Severity mapping**:
| Status | Severity | What it usually means |
|--------|----------|----------------------|
| 500+ | Critical | Server error — something is broken |
| 403 | High | Permission error OR route collision (static route shadowed by `/:param`) |
| 404 | Medium | Missing endpoint — may be a renamed/removed API route |
| 401 | Low | Expected for unauthenticated probes, but flag if it happens on authenticated pages |
| CORS error | High | API endpoint missing CORS headers — feature broken in production |

**What this catches that visual browsing misses**:
- Route collisions (e.g. `GET /api/boards/users` shadowed by `GET /api/boards/:boardId`)
- Endpoints that fail silently (TanStack Query shows empty data instead of error)
- CORS issues only visible in production
- Auth middleware rejecting valid sessions
- Missing endpoints after refactoring

**Report format**: Group by status code in a "Network Errors" section:
```markdown
## Network Errors (detected during browsing)

### 403 Forbidden (2 endpoints)
- `GET /api/boards/users` on /app/boards/123 — likely route collision with /:boardId
- `POST /api/settings/theme` on /app/settings — permission check failing

### 500 Internal Server Error (1 endpoint)
- `GET /api/reports/summary` on /app/dashboard — server error
```

### Autonomy by Depth

| Action | quick | standard | thorough |
|--------|-------|----------|----------|
| Navigate pages | Just do it | Just do it | Just do it |
| Take screenshots | Key moments | Friction points | Every page + every issue |
| Fill forms with test data | Ask first | Ask first | Just do it (obviously fake data) |
| Click delete/destructive | Ask first | Ask first | Ask first (only exception) |
| Submit forms | Ask first | Brief confirmation | Just do it (test data only) |
| Write report file | Just do it | Brief confirmation | Just do it |

## Operating Modes

### Mode 1: UX Walkthrough (Dogfooding)

**When**: "ux walkthrough", "walk through the app", "is the app intuitive?", "ux audit", "dogfood this"

This is the highest-value mode. You are **dogfooding** the app — using it as a real user would, with their goals, their constraints, and their patience level. Not a mechanical checklist pass, but genuinely trying to get a job done.

#### Step 1: Adopt a User Persona

Ask the user two questions:
- **Task scenario**: What does the user need to accomplish? (e.g., "Create a new patient and book them for surgery")
- **Who is the user?**: What's their context? (e.g., "A busy receptionist between phone calls, on a desktop, moderate tech comfort")

If the user doesn't specify a persona, adopt a reasonable default: a non-technical person who is time-poor, mildly distracted, and using this app for the first time today.

#### Step 2: Approach with Fresh Eyes

Navigate to the app's entry point. From here, attempt the task with **no prior knowledge of the UI**. Adopt the persona's mindset:
- Don't use browser dev tools or read source code to figure out where things are
- Don't assume labels mean what a developer intended — read them literally
- If something is confusing, don't power through — note it as friction
- If you feel uncertain about what a button will do, that's a finding

#### Step 3: Evaluate Each Screen

At each screen, evaluate against the walkthrough checklist (see [references/walkthrough-checklist.md](references/walkthrough-checklist.md)). Key questions to hold in mind:

**Layout**: Is all text fully visible? Nothing clipped or overlapping? Spacing consistent?
**Comprehension**: Do I understand what this page is for and what I can do here? Do the labels make sense to a non-developer?
**Wayfinding**: Do I know where I am in the app? Can I get back to where I came from? Does the nav show my location?
**Flow**: Does this page connect naturally to the last one? Is the next step obvious without thinking?
**Trust**: Do I feel confident this will do what I expect? Am I afraid I'll break something?
**Efficiency**: How many clicks/steps is this taking? Is there a shorter path?
**Recovery**: If I make a mistake right now, can I get back?

#### Step 4: Count the Cost

Track the effort required to complete the task:
- **Click count**: How many clicks from start to finish?
- **Decision points**: How many times did I have to stop and think?
- **Dead ends**: Did I go down a wrong path and have to backtrack?
- **Time impression**: Does this feel fast or tedious?

#### Step 5: Test Resilience

After completing the main task, test what happens when things go wrong:
- Navigate away mid-form — is data preserved?
- Submit with missing/bad data — are error messages helpful and specific?
- Use the back button — does the app handle it gracefully?
- Refresh the page — does state survive?

#### Step 6: Ask the Big Questions

After completing (or failing) the task, reflect as the persona:
- **Would I come back?** Or would I look for an alternative?
- **Could I teach a colleague to use this?** In under 2 minutes?
- **What's the one thing that would make this twice as easy?**

#### Step 7: Document and Report

Take screenshots at friction points. Compile findings into a UX audit report.
Write report to `docs/ux-audit-YYYY-MM-DD.md` using the template from [references/report-template.md](references/report-template.md)

**Severity levels**:
- **Critical** — blocks the user from completing their task
- **High** — causes confusion or significant friction
- **Medium** — suboptimal but the user can work around it
- **Low** — polish and minor improvements

### Mode 2: QA Sweep

**When**: "qa test", "test all pages", "check everything works", "qa sweep"

Systematic mechanical testing of all pages and features.

1. **Discover pages**: Read the app's router config, sitemap, or manually navigate the sidebar/menu to find all routes
2. **Create a task list** of areas to test (group by feature area)
3. **For each page/feature**:
   - Page renders without errors
   - Data displays correctly (tables, lists, details)
   - Forms submit successfully (create)
   - Records can be edited (update)
   - Delete operations work with confirmation
   - Validation fires on bad input
   - Empty states display correctly
   - Error states are handled
4. **Cross-cutting concerns**:
   - Dark mode: all elements visible, no contrast issues
   - Mobile viewport (375px): layout doesn't break, touch targets adequate
   - Search and filters: return correct results
   - Notifications: display and can be dismissed
5. Produce a **QA sweep summary table**:

   | Page | Status | Issues |
   |------|--------|--------|
   | /patients | Pass | — |
   | /patients/new | Fail | Form validation missing on email |

6. Write report to `docs/qa-sweep-YYYY-MM-DD.md`

### Mode 3: Targeted Check

**When**: "check [feature]", "test [page]", "verify [component] works"

Focused testing of a specific area.

1. Navigate to the specific page or feature
2. Test thoroughly — all states, edge cases, error paths
3. Report findings inline (no separate file unless user requests)

## When to Use

| Scenario | Mode | Depth |
|----------|------|-------|
| Just changed a page, quick sanity check | Targeted Check | quick |
| After building a feature, before showing users | UX Walkthrough | standard |
| Before a release, verify nothing is broken | QA Sweep | standard |
| Quick check on a specific page after changes | Targeted Check | quick |
| Periodic UX health check | UX Walkthrough | standard |
| Client demo prep | QA Sweep + UX Walkthrough | standard |
| End-of-day comprehensive test, review in morning | All modes combined | thorough |
| Pre-launch full audit with evidence | All modes combined | thorough |
| Test literally everything before a client demo | Every element on every page | exhaustive |
| Weekend-long complete app certification | Every element, state, viewport, mode | exhaustive |

**Skip this skill for**: API-only services, CLI tools, unit/integration tests (use test frameworks), performance testing.

## Autonomy Rules

Default rules (standard depth). See "Autonomy by Depth" table above for quick/thorough overrides.

- **Just do it**: Navigate pages, take screenshots, read page content, evaluate usability
- **Brief confirmation**: Before starting a full QA sweep (can be lengthy), before writing report files
- **Ask first**: Before submitting forms with real data, before clicking delete/destructive actions

## Tips

- Chrome MCP is ideal for authenticated apps — it uses your real session
- For long QA sweeps, use the task list to track progress across pages
- Take screenshots at key friction points — they make the report actionable
- Run UX walkthrough before QA sweep — finding "buttons work but users are confused" is more valuable than "all buttons work"
- Stay in persona throughout — if you catch yourself thinking "a developer would know to..." stop. The user isn't a developer.
- Every hesitation is a finding. If you paused to figure out what to click, that's friction worth reporting.
- The "one thing to make it twice as easy" is often the most actionable insight in the whole report

## Reference Files

| When | Read |
|------|------|
| Before starting thorough mode — understand the user's world | [references/workflow-comprehension.md](references/workflow-comprehension.md) |
| Evaluating each screen during walkthrough | [references/walkthrough-checklist.md](references/walkthrough-checklist.md) |
| Running the six scenario tests | [references/scenario-tests.md](references/scenario-tests.md) |
| Writing the audit report | [references/report-template.md](references/report-template.md) |
| Browser tool commands and selection | [references/browser-tools.md](references/browser-tools.md) |
