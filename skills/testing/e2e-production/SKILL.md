---
name: e2e-production
description: Production E2E testing for The Simpsons API using Chrome DevTools MCP for browser automation and Neon MCP for real-time database verification. Covers smoke journeys, mutation validation, and deployment sanity checks. Use when the user asks to run, design, or validate E2E tests against the production site, verify live deployments, or perform post-deploy checks.
---

# Production E2E Skill (Browser + DB Correlation)

## Safety rules

- Prefer read-only checks; do not mutate production data unless the user explicitly approves.
- **Database Safety:** When verifying mutations in Neon, use targeted `SELECT` statements. Never run `UPDATE` or `DELETE` in production via MCP unless part of a user-sanctioned cleanup.
- Use a dedicated test account and tag any created data for cleanup.
- Avoid load testing or high concurrency in production.
- Record timestamp, base URL, and build/commit metadata when available.

## Tooling Integration

### 1. Browser Automation (Chrome DevTools MCP)

- Use `navigate`, `click`, `type`, and `fill_form` to simulate user journeys.
- Capture `console_messages` to detect runtime errors (React hydration, 404s, 500s).
- Use `take_snapshot` for fast, text-based verification of the DOM and accessibility tree.

### 2. Database State Contrast (Neon MCP)

- **MANDATORY CORRELATION:** For every UI mutation, perform a corresponding query in Neon to verify the persistence layer.
- **Schema Awareness:** Always prefix tables with `the_simpson.` (e.g., `the_simpson.characters`) to bypass `search_path` limitations.
- **Verification Pattern:**
  1. `browser.click` (Submit Form)
  2. `browser.wait_for_selector` (Success Message)
  3. `neon.run_sql` (SELECT \* FROM table WHERE id = ...)
  4. Compare UI state vs DB result.

## Preconditions

- Resolve the production base URL from `NEXT_PUBLIC_APP_URL` or explicit user input.
- Ensure credentials exist in env (`E2E_TEST_EMAIL`, `E2E_TEST_PASSWORD`, and any OTP secret if required).
- Confirm third-party rate limits when tests rely on external APIs.

## Default discovery scope (read-only)

1. Start at the base URL and validate initial render.
2. Discover navigation entry points (header, footer, menus, CTAs) and explore them.
3. Identify public vs. protected sections based on redirects or access prompts.
4. If login is required, authenticate with the dedicated test user.
5. Traverse list-to-detail patterns and capture representative pages.
6. Prefer read-only flows; avoid any action that implies a write.
7. Track visited routes and stop when navigation loops or no new routes appear.

## Optional mutation scope (explicit approval required)

- Any create/update/delete flows discovered by the agent.
- **Form Integrity:** Ensure ALL fields in a form are filled according to their types (selects, multiline text, etc.) to test database schema constraints and UI validation.
- **Diary Entries:** Create a new memory, filling all fields (Who, Where, What), verify it appears in the timeline with accurate data, verify the record in `the_simpson.diary_entries` using Neon MCP, and finally delete it (verifying deletion in both UI and DB).
- **Collections:** Create a new collection (Name, Description), verify success, check the `the_simpson.collections` table, and delete it if UI allows (otherwise mark for DB cleanup).
- **Social Actions:** Test Following/Unfollowing characters or users; verify row existence/removal in `the_simpson.follows`.
- **Sync Triggers:** Trigger data synchronization and verify UI feedback + check `the_simpson.jobs_metadata` or equivalent for execution logs.

## Workflow

1. **Initialization:** Resolve production URL and activate `chrome-devtools` tools.
2. **Discovery (Read-Only):** Run a discovery-based traversal using `navigate_page` and `take_snapshot`. Capture browser console errors and network 4xx/5xx responses.
3. **Database Baseline:** Identify the tables involved in the planned mutations and run a baseline query in Neon to check current counts or specific records.
4. **Mutation & Contrast (Approved ONLY):**
   - Execute the mutation flow in the browser (e.g., `fill_form` + `click`).
   - Immediately after the UI confirms success, execute a SQL query in Neon to "contrast" the UI state with the persisted data.
   - Fail the test if the UI says "Success" but the DB doesn't reflect the change (or vice versa).
5. **Cleanup:** Ensure any created data is deleted via the UI, and verify the DB is back to its baseline state.
6. **Summarize:** Provide a report including pass/fail status, console errors, and the results of the UI vs. DB state contrast.

## References

- For specific table schemas, see [app/\_lib/db-schema.ts](app/_lib/db-schema.ts).
- For historical lessons on production issues, see [docs/DEPLOYMENT_LESSONS.md](docs/DEPLOYMENT_LESSONS.md).
