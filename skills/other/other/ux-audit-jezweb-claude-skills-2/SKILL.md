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

## Depth Levels

Control how thorough the audit is. Pass as an argument: `/ux-audit quick`, `/ux-audit thorough`, or default to standard.

| Depth | Duration | Autonomy | What it covers |
|-------|----------|----------|---------------|
| **quick** | 5-10 min | Interactive | One user flow, happy path only. Spot check after a change. |
| **standard** | 20-40 min | Semi-autonomous | Full walkthrough + QA sweep of main pages. Default. |
| **thorough** | 1-3 hours | Fully autonomous | Multiple personas, all pages, all modes combined. Overnight mode. |

### Thorough Mode: Overnight Workflow

The thorough mode is designed to run unattended. Kick it off at end of day, review the report in the morning.

1. **Discover all routes** — read router config, crawl navigation, build complete page inventory
2. **Create a task list** — track progress so work survives context limits
3. **UX Walkthrough x3 personas**:
   - First-time user (non-technical, time-poor, first visit)
   - Power user (daily user, knows the app, looking for efficiency)
   - Mobile user (phone, touch targets, small viewport)
4. **Full QA sweep** — every page, all CRUD, all states (empty, error, loading, populated)
5. **Resilience testing** — every form: bad data, mid-navigation, back button, refresh, double-submit
6. **Cross-cutting per page** — dark mode screenshot, mobile viewport (375px) screenshot, keyboard navigation
7. **Screenshot everything** — save to `.jez/screenshots/ux-audit/` (numbered chronologically)
8. **Comprehensive report** — `docs/ux-audit-thorough-YYYY-MM-DD.md` with issue counts by severity
9. **Summary** — top 5 critical issues, overall health score, "one thing to fix first"

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

**Clarity**: Is the next step obvious without thinking?
**Trust**: Do I feel confident this will do what I expect? Am I afraid I'll break something?
**Efficiency**: How many clicks/steps is this taking? Is there a shorter path?
**Recovery**: If I make a mistake right now, can I get back?
**Delight vs frustration**: Would I sigh, smile, or swear at this moment?

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
| Evaluating each screen during walkthrough | [references/walkthrough-checklist.md](references/walkthrough-checklist.md) |
| Writing the audit report | [references/report-template.md](references/report-template.md) |
| Browser tool commands and selection | [references/browser-tools.md](references/browser-tools.md) |
