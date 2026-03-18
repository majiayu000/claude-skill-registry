---
name: qa-test
description: Browser-based QA verification after any implementation. Use when someone says "QA this", "test this in browser", "verify the feature", "qa test", "browser test", or after completing an /implement-change to verify acceptance criteria in a real browser. Opens Chrome via MCP, exercises each acceptance criterion, verifies via DOM snapshots, and reports pass/fail. The "closer" for every implementation — proof it works, not just that tests pass.
---

# QA Test

Verify implemented features in a real browser. Exercise each acceptance criterion, verify via snapshots, report results.

**Context-efficient design**: browser testing runs in a sub-agent so snapshot/interaction data stays out of the main thread. Main thread only sees compact pass/fail summaries.

## Process

1. Pre-flight (sub-agent) — gather criteria, resolve URL, check environment
2. Interactive setup — human steers browser for hard-to-automate steps (login, drag, etc.)
3. Browser testing (sub-agent) — exercises all criteria in isolated context
4. Report results — main thread receives compact summary only
5. Handle failures — retry failed criteria after manual intervention if needed

### 1. Pre-flight Sub-agent

Launch an `Explore` sub-agent **before** any browser interaction to gather all context in parallel.

**Sub-agent prompt:**

```
Gather QA pre-flight context for testing. Return a structured JSON block with:

1. **acceptance_criteria**: List of testable criteria. Check these sources in order,
   stop at the first that has criteria:
   - The user's prompt (if criteria were given explicitly)
   - Current PR description: run `gh pr view --json body` via Bash
   - Current branch diff: run `git diff main...HEAD --stat` then read changed files
     to infer what user-visible behavior changed
   - Linked issue: check PR body for issue references, fetch with `gh issue view`

2. **test_url**: Where to test. Check in order:
   - `.tap/tap-audit.md` Environments section
   - `package.json` scripts for `dev`, `start`, or similar
   - Common defaults: localhost:3000, :5173, :4321, :6886

3. **app_running**: Try to fetch the test_url via `curl -s -o /dev/null -w '%{http_code}'`.
   Return the status code. If not running, return the dev command that would start it.

4. **test_pages**: List of specific page URLs/routes to visit based on the changed files
   (e.g., if `modules/campaigns/` changed, the test page is likely `/campaigns/...`)

5. **db_available**: Check if postgres MCP tools are available (search for
   `mcp__postgres__execute_sql` or similar). Return true/false.

6. **has_async_flows**: Based on the changed files, flag whether the feature involves
   background jobs (Temporal workflows, queues, webhooks) that need async verification.

7. **needs_login**: Whether the app requires authentication. Check for login pages,
   auth middleware, or session requirements in the codebase.

Return results as a structured summary, not raw tool output.
```

**Using the pre-flight results:**

- If `app_running` is not 200, start the dev server (background) and wait for it
- Use `acceptance_criteria` as the test plan
- Use `test_pages` to know where to navigate first
- If `db_available`, include database verification steps
- If `has_async_flows`, use the async testing pattern
- If `needs_login`, prompt user for interactive setup before launching browser sub-agent

**Fallback (no sub-agent):** If sub-agents are unavailable, gather criteria and resolve URL sequentially.

<details>
<summary>Manual fallback: Gather criteria and resolve URL</summary>

**Gather acceptance criteria** from (in priority order):
- Explicit criteria provided in the prompt
- Current ticket/issue (if referenced)
- PR description
- `.tap/tap-audit.md` for environment context

If no criteria found, ask in human mode. In agent mode, infer from the diff.

**Resolve test URL** (in priority order):
1. URL provided in the prompt
2. `.tap/tap-audit.md` → Environments section
3. `package.json` scripts → `dev`, `start`, or similar
4. Common defaults: `http://localhost:3000`, `http://localhost:5173`, `http://localhost:4321`

Verify the app is running before proceeding.

</details>

### 2. Interactive Setup (Main Thread)

Before launching the browser testing sub-agent, handle anything that's hard to automate in the main thread. The browser state persists since the sub-agent connects to the same Chrome instance.

**When to prompt for interactive setup:**
- `needs_login` is true → ask user: "App requires login. Want me to navigate to login page so you can sign in, or should I attempt automated login?"
- Complex drag-and-drop or gesture-based preconditions
- Multi-factor auth, CAPTCHAs, OAuth popups

**What to do:**
1. Navigate to the relevant page via Chrome MCP
2. Tell the user what action is needed
3. Wait for user confirmation that setup is complete
4. Then launch the browser testing sub-agent

If no interactive setup is needed, skip directly to step 3.

### 3. Browser Testing (Sub-agent)

**Launch a `general-purpose` sub-agent** for all browser interaction. This keeps snapshot/interaction data out of the main thread context.

**Sub-agent prompt template:**

```
You are running browser-based QA tests. The browser is already open and may already
be logged in / set up.

Test URL: {test_url}
Acceptance criteria to verify:
{numbered list of criteria}

Additional context:
- DB tools available: {db_available}
- Has async flows: {has_async_flows}
- Test pages: {test_pages}

## How to test

Use Chrome MCP tools (`mcp__chrome-devtools__*`).

**Snapshot-first workflow** — use `take_snapshot` for BOTH finding elements AND
verifying results. Do NOT use `take_screenshot` unless a criterion fails and you
need visual debugging evidence.

**For each criterion:**
1. Navigate to the relevant page
2. `take_snapshot` → get element UIDs and current state
3. Interact via UIDs (`click`, `fill`, `hover`)
4. `take_snapshot` → verify state changed as expected
5. Check `list_console_messages` for errors
6. Check `list_network_requests` for failed requests (4xx, 5xx)

**Important**: UIDs are ephemeral — always take a fresh snapshot before interacting.

**On failure only**: `take_screenshot` and save to `./qa-evidence/` for debugging.

**React/SPA hover interactions:**
Chrome DevTools `hover` only triggers CSS `:hover`, NOT JS `mouseenter`/`mouseover`.
If a UI element only appears via React's `onMouseEnter`:
1. Try `click` directly in the area
2. If that fails, `evaluate_script` to dispatch mouseenter event
3. `take_snapshot` to confirm

**Testing patterns:**
- Form submission: fill → submit → snapshot to verify success + check no errors
- Navigation: click → snapshot to verify new state + check URL
- State changes: trigger action → snapshot to verify → reload → snapshot to verify persistence
- Async: trigger → snapshot for intermediate state → poll snapshots → verify final state
- Error states: trigger invalid input → snapshot to verify error messaging

**Always check:**
- Console errors (JS exceptions)
- Failed network requests (4xx, 5xx)

## Report format

Return ONLY a compact summary in this exact format:

RESULT: [PASS / FAIL / PARTIAL]

CRITERIA:
1. [criterion] — PASS/FAIL — [one-line observation]
2. [criterion] — PASS/FAIL — [one-line observation]
...

ERRORS: [any console errors or failed network requests, or "none"]

FAILURES: [for any failed criterion: what happened, what was expected,
screenshot path if captured]

NEEDS_MANUAL: [any criteria that couldn't be tested due to automation
limitations — e.g., drag-and-drop, complex gestures]
```

### 4. Report Results

The sub-agent returns a compact summary. Present it to the user.

**Human mode**: Show the summary. If any failures, ask: "Want me to fix this and re-test, or is this expected?"

**Agent mode**: If all pass, proceed (e.g., open PR). If any fail, attempt fix-and-retest.

### 5. Failure Handling

**Automation failures (NEEDS_MANUAL):**
1. The user performs the manual action in the browser (main thread)
2. Launch a new sub-agent to verify only the remaining criteria
3. The new sub-agent picks up the browser state left by the user

**Code failures (FAIL):**

*Agent mode:*
1. Fix the code
2. Launch new sub-agent to re-test only failed criteria
3. Max 2 fix-and-retest cycles

*Human mode:*
- Present failures
- Ask: "Want me to fix this and re-test, or is this expected behavior?"

### Optional: Database Verification

Include in the sub-agent prompt when `db_available` is true. For features that create or modify data:

- **Record creation**: Verify expected rows exist with correct values
- **Relational data**: Confirm junction table rows were created
- **Status transitions**: Confirm async workflows completed

## Boundaries

- Does NOT write unit tests (that's implement-acceptance-tests)
- Does NOT review code quality (that's CLAUDE.md / code review)
- Does NOT assess blast radius (that's /blast-radius)
- Tests user-visible behavior in the browser, with optional database verification
- Does NOT modify acceptance criteria — tests what was specified
