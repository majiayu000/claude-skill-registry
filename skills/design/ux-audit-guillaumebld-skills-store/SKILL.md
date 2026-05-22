---
name: ux-audit
description: "Run UX walkthroughs and QA sweeps on live web apps using browser automation. Walks through apps as a real user, flags friction points and usability issues, tests CRUD operations, and produces ranked audit reports. Trigger with 'ux audit', 'ux walkthrough', 'qa test', 'test the app', or 'check all pages'."
compatibility: claude-code-only
---

# UX Audit

Walk through live web apps as a real user to find usability issues and verify functionality. Uses Chrome MCP (for authenticated apps with your session) or Playwright for browser automation. Produces structured audit reports with findings ranked by impact.

## Browser Tool Detection

Before starting any mode, detect available browser tools:

1. **Chrome MCP** (`mcp__claude-in-chrome__*`) — preferred for authenticated apps. Uses the user's logged-in Chrome session, so OAuth/cookies just work.
2. **Playwright MCP** (`mcp__plugin_playwright_playwright__*`) — for public apps or parallel sessions.
3. **playwright-cli** — for scripted flows and sub-agent browser tasks.

If none are available, inform the user and suggest installing Chrome MCP or Playwright.

See [references/browser-tools.md](references/browser-tools.md) for tool-specific commands.

## Operating Modes

### Mode 1: UX Walkthrough

**When**: "ux walkthrough", "walk through the app", "is the app intuitive?", "ux audit"

This is the highest-value mode. Instead of mechanically clicking buttons, walk through the app as a first-time user performing a realistic task.

1. Ask the user for a **task scenario** (e.g., "I need to create a new patient and book them for surgery")
2. Navigate to the app's entry point
3. Attempt the task as a first-time user would — no prior knowledge of the UI
4. At each screen, evaluate against the walkthrough checklist (see [references/walkthrough-checklist.md](references/walkthrough-checklist.md)):
   - Is the next step obvious without thinking?
   - Do labels and icons make sense?
   - Is navigation discoverable?
   - Are dangerous actions (delete, override) guarded?
   - Is the most important information prominent?
   - Does the result match my expectation?
5. Take screenshots at friction points
6. After completing (or failing) the task, compile findings into a UX audit report
7. Write report to `docs/ux-audit-YYYY-MM-DD.md` using the template from [references/report-template.md](references/report-template.md)

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

| Scenario | Mode |
|----------|------|
| After building a feature, before showing users | UX Walkthrough |
| Before a release, verify nothing is broken | QA Sweep |
| Quick check on a specific page after changes | Targeted Check |
| Periodic UX health check | UX Walkthrough |
| Client demo prep | QA Sweep + UX Walkthrough |

**Skip this skill for**: API-only services, CLI tools, unit/integration tests (use test frameworks), performance testing.

## Autonomy Rules

- **Just do it**: Navigate pages, take screenshots, read page content, evaluate usability
- **Brief confirmation**: Before starting a full QA sweep (can be lengthy), before writing report files
- **Ask first**: Before submitting forms with real data, before clicking delete/destructive actions

## Tips

- Chrome MCP is ideal for authenticated apps — it uses your real session
- For long QA sweeps, use the task list to track progress across pages
- Take screenshots at key friction points — they make the report actionable
- Run UX walkthrough before QA sweep — finding "buttons work but users are confused" is more valuable than "all buttons work"

## Reference Files

| When | Read |
|------|------|
| Evaluating each screen during walkthrough | [references/walkthrough-checklist.md](references/walkthrough-checklist.md) |
| Writing the audit report | [references/report-template.md](references/report-template.md) |
| Browser tool commands and selection | [references/browser-tools.md](references/browser-tools.md) |
