---
name: app-comprehensive-test-generator
description: Generate exhaustive user-flow and edge-case test scenarios from an app's codebase, produce scenario .md files, execute tests using connected or newly created MCPs, and produce an app.qa.report.md summarizing failures and suggested fixes. 
---

Skill purpose

This Skill analyzes an application's codebase to enumerate all practical user-flow and edge-case scenarios (starting from a prioritized sample set), writes human-readable scenario .md files, automatically or manually executes those scenarios using available MCP(s) or by provisioning recommended MCP stubs, validates results, and compiles a consolidated QA report (app.qa.report.md) describing failures, reproducible steps, severity, and suggested fixes.















Step-by-step instructions Claude must follow

1. Gather context
  - Ask the user for repository location, runtime environment, available MCP connections, authentication details, and which sample scope to start with (default: core user flows: sign-up, login, search/browse, add-to-cart, checkout/payment).
  - If code is provided, fetch and index relevant files (routes/controllers, API endpoints, UI flows, business logic, tests). If not provided, request access or a zip.

2. Static analysis and feature extraction
  - Parse source code to extract endpoints, routes, UI screens, form fields, auth flows, third-party integrations, database operations, and configuration flags.
  - Build a feature map listing actions (e.g., create-account, login, forgot-password, search, filter, sort, add-to-cart, apply-coupon, checkout), inputs, preconditions, and side effects.

3. Scenario enumeration
  - For chosen sample scope, generate scenarios covering:
    - Happy path(s)
    - Input boundary conditions (empty, long, invalid formats)
    - Authorization/permission variations (unauthenticated, low-privilege user)
    - Error and retry flows (network failure, service timeout, DB error)
    - Integration edge cases (payment declines, third-party API rate-limit)
    - Concurrency and state races where applicable
  - Use reasonable combinatorial pruning to avoid explosion: prioritize by user impact and probability. Default: enumerate full set for core flows and provide counts.

4. Produce scenario .md files
  - For each scenario, create a .md file in a scenarios/ directory with a consistent template:
    - Title
    - Scope and priority
    - Preconditions (state, test data)
    - Steps (precise reproducible steps, API requests or UI actions)
    - Expected result / acceptance criteria
    - Cleanup steps
  - Number or tag scenarios for traceability (e.g., S001-signup-happy, S002-signup-invalid-email).

5. Select or provision MCP(s)
  - Detect connected MCP(s) and their capabilities (API-driven, headless browser, device farm). If none or insufficient, recommend and optionally generate a minimal MCP stub/config (e.g., Playwright/Playwright config, Cypress project, Postman collection, or a Python test harness) tailored to the app.
  - Ask user permission before creating new MCP artifacts in the repo.

6. Test execution (manual trigger)
  - Provide a command or CI job to run a selected scenario or the full suite (examples: npm run test:scenario S001, python tests/run.py --scenario S001, playwright test --project=...).
  - When user triggers execution, run scenarios via selected MCP(s) and capture outputs: logs, screenshots, HTTP traces, DB diffs, exit codes, timing.

7. Result validation and triage
  - Compare actual results to expected acceptance criteria.
  - For each failing scenario, collect: failure summary, raw evidence (logs, request/response bodies, screenshots), reproducible steps, severity (blocker/major/minor), likely root cause hints, and suggested fix or mitigation.

8. Produce app.qa.report.md
  - Summarize run: date/time, environment, MCPs used, scenarios executed, pass/fail counts.
  - For each failing scenario include:
    - Scenario id & title
    - Short description
    - Steps to reproduce (concise)
    - Evidence links or inline snippets
    - Severity and suggested fix
  - Attach or link generated scenario .md files and any test artifacts (screenshots, log files).

9. Iteration and expansion
  - Offer to expand coverage gradually: from sample scope to entire app, using feedback to refine pruning and priority.
  - Maintain scenario files and test harness in repo so they can be run by developers.

Usage examples

- Example 1: User provides repo and asks to start with core flows
  - Claude: analyzes repo, extracts features, creates scenarios/S001-signup-happy.md ... S010-checkout-payment-decline.md, provisions a Playwright config, describes commands to run tests, and waits for manual run. After run, Claude produces app.qa.report.md summarizing results.

- Example 2: User has an MCP connected (API-driven test runner)
  - Claude: inspects MCP capabilities, maps scenarios to MCP tasks, executes selected scenarios, collects logs and screenshots, produces app.qa.report.md with failures.

- Example 3: User wants only scenario generation
  - Claude: runs steps 1–4, outputs scenarios/*.md files and a summary, but does not provision or execute tests until prompted.

Scenario .md template (example)

Title: S001 - Signup: happy path
Priority: P0
Preconditions:
- Clean DB or test account seed
- Email delivery stubbed
Steps:
1. Go to POST /api/signup with payload {email: user@example.com, password: P@ssw0rd}
2. Confirm email via GET /api/confirm?token=... (use token from intercepted emails)
Expected:
- 201 Created with user id
- User can login at POST /api/login
Cleanup:
- Delete created user from test DB

Best practices

- Start small: run core flows first and confirm stability before expanding to full-surface tests.
- Keep scenario .md files human-readable and small; reference test data factories.
- Use environment isolation (test DB, feature flags off) to avoid flakiness and destructive side effects.
- Collect rich evidence (HTTP traces, DB snapshots, screenshots) to speed triage.
- Tag scenarios by area and priority to allow selective execution (smoke/regression/extended).
- Limit combinatorial explosion with heuristics: focus on high-impact permutations first.

Commands and integrations suggestions

- Playwright (E2E browser): playwright.config.js, tests/scenarios/*.spec.ts
- Cypress: cypress/e2e/scenarios/*.cy.js
- API harness: tests/api/scenarios/*.py using requests and pytest paramization
- Postman: collection.json with scenario folders and example environments

Permissions and safety

- Request explicit permission before creating or modifying files in the repo or provisioning new MCP artifacts.
- By default, operate in a non-destructive test mode (use test databases, mocked payment gateways).

When to ask clarifying questions

- If repo access or environment details are missing, ask for them before analysis.
- If the user wants a different starting scope or automatic scheduling (CI), confirm preferred behavior.

Related files or templates (optional to generate on user approval)

- A minimal Playwright starter (playwright.config.js) and example test harness can be generated upon request.

