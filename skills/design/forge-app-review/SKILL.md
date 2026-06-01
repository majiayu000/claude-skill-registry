---
name: forge-app-review
description: >
  Reviews Forge apps for security vulnerabilities, architecture issues, cost inefficiencies, performance problems,
  and trigger/scheduling waste before deployment. Use when the user says "review my Forge app", "check my app",
  "pre-deploy check", "is my app ready to deploy", "audit my Forge app", "check for security issues", "check
  performance", "review manifest", "check my Forge app for problems", "app review", "optimize my Forge app costs",
  "reduce invocations", "why is my app expensive", "check my triggers", or any request to evaluate a Forge app's
  quality, safety, cost efficiency, or readiness. Also triggers when users ask about Forge best practices, permission
  scopes, resolver optimization, storage efficiency, cold start reduction, frontend offloading, trigger filtering,
  scheduled trigger frequency, N+1 API calls, bulk API usage, verbose logging, or Forge platform pricing.
---

# Forge App Review

Deep pre-deploy review of Forge apps across **Security**, **Architecture**, **Cost**, **Performance**, and **Triggers & Scheduling**. Produces a severity-sorted issue list with actionable fixes.

## Forge Pricing Reference

Forge uses a consumption-based pricing model. Charges only apply above free monthly allowances. Use this table to assess cost impact of findings:

| Capability | Billing Unit | Free Monthly Allowance | Overage Price (USD) |
|-----------|-------------|----------------------|-------------------|
| **Functions: Duration** | GB-seconds | 100,000 GB-seconds | $0.000025 / GB-second |
| **KVS: Reads** | GB read | 0.1 GB | $0.055 / GB |
| **KVS: Writes** | GB written | 0.1 GB | $1.090 / GB |
| **Logs: Writes** | GB written | 1 GB | $1.005 / GB |
| **SQL: Compute duration** | Hours | 1 hour | $0.143 / hour |
| **SQL: Compute requests** | Per 1M requests | 100,000 requests | $1.929 / 1M requests |
| **SQL: Data stored** | GB-hours | 730 GB-hours | $0.00076850 / GB-hour |

**Key cost insight:** KVS writes are ~20× more expensive than reads. Logging is ~$1/GB over the free tier. The cost formula for functions is: **GB-seconds = (memoryMiB ÷ 1024) × duration in seconds**.

**Free capabilities** (not billed): UI modules (UI Kit and Custom UI frontends run in the browser), Jira expressions, Forge Remote invocations (though the remote function runtime is billed), entity properties (stored by the product, not by Forge Storage).

---

## Execution Mandate

When triggered, immediately:

1. Read `manifest.yml` — this is the source of truth for permissions, modules, egress, triggers, scheduled triggers, and function memory settings
2. Read `package.json` — check dependencies, versions, scripts
3. Scan all resolver files in `src/` — check patterns, error handling, data flow, API call patterns (N+1, missing fields, sequential calls), logging verbosity
4. Scan UI code (Custom UI or UI Kit) — check component patterns, bridge usage, whether API calls and logic could be moved to the frontend, product context usage, invoke patterns (chatty, per-render)
5. Check for Forge Storage / Entity Store usage patterns — TTL strategy, write frequency, query vs iteration, entity properties vs KVS
6. Check trigger and scheduling configuration — frequency, filtering, ignoreSelf, early exit, polling vs event-driven
7. Check for Forge Remote usage or opportunities — compute offloading, trade-offs
8. Compile all findings into a severity-sorted issue list

Do NOT ask the user what to review. Review everything. Do NOT modify any code unless explicitly asked. Do NOT skip categories — even if the app looks clean, confirm it explicitly.

---

## Review Process

### Step 1: Manifest Analysis (`manifest.yml`)

Read the manifest first. Extract:
- **Permissions/scopes** — list all `scopes` and `permissions` entries
- **Modules** — list all module types and their function key references
- **Egress** — check `app.connect.remotes` or `permissions.external.fetch.backend` URLs
- **Environment variables** — check for `app.storage` or environment variable declarations

Cross-reference every `function` key in modules against actual resolver `resolver.define()` calls.

### Step 2: Dependencies (`package.json`)

Check:
- Node.js engine compatibility (Forge requires Node 18.x+)
- Unnecessary large dependencies (e.g., `lodash` when only one function is used, `moment` instead of native Date or `dayjs`)
- Missing `@forge/api`, `@forge/bridge`, or `@forge/ui` depending on app type
- Dev dependencies leaking into production
- Outdated `@forge/*` packages

### Step 3: Resolver Code

Read all files that contain `resolver.define` or `Resolver` imports. Check for:
- Error handling patterns
- API call patterns (`requestJira`, `requestConfluence`, `api.asUser()`, `api.asApp()`)
- Data validation and sanitization
- Storage operations
- External fetch calls

### Step 4: UI Code

For **UI Kit** apps — scan for `@forge/react` imports, component usage, hooks.
For **Custom UI** apps — scan for `@forge/bridge` usage, `invoke()` calls, CSP compliance.

In both cases, check for:
- **Frontend offloading opportunities**: Are there resolvers that only do read-only `requestJira()`/`requestConfluence()` calls that could instead use `@forge/bridge` directly from the browser?
- **Product context via resolver**: Is the app invoking a resolver just to get issue/project/space key? Use `useProductContext()` (UI Kit) or `view.getContext()` (Custom UI) instead.
- **Invoke on every render**: Is `invoke()` called without proper `useEffect` with empty dependency array, causing re-invocation on every render?
- **Client-side logic**: Is data formatting, sorting, filtering, or validation done in a resolver when it could run in the browser for free?

### Step 5: Storage Analysis

Search for usage of:
- `storage.get`, `storage.set`, `storage.delete` — check for unnecessary writes, short TTLs (KVS writes are ~20× more expensive than reads), and missing caching patterns
- `storage.query` (Entity Store) — check for proper use of indexes, `.where()`, and `.limit()` instead of fetching all items and filtering in code
- Entity properties (`requestJira` to `/properties/`) — note these are **free** and stored by the product (not Forge Storage quota), suitable for small per-entity metadata (max 32 KB per property). Good for flags, markers, timestamps attached to Jira issues or Confluence pages. Queryable via JQL for Jira entity properties. **Not suitable for sensitive data** — visible to other apps and users via REST API.
- Cache patterns — is app-level data that rarely changes (e.g., custom field IDs, project configs, workflow statuses) being fetched from APIs on every invocation? Should be cached in KVS with a TTL (1 hour+ preferred to minimize writes)
- Write amplification — a 1-minute TTL cache with 100 calls/hour causes ~60 writes/hour; a 1-hour TTL causes ~1 write/hour at ~60× less cost

### Step 6: Trigger & Scheduling Analysis

Check the manifest for `scheduledTrigger` and `trigger` modules:
- **Scheduled triggers**: Is the interval appropriate? (`fiveMinutes` is rarely justified — prefer `hour`, `day`, or `week`)
- **Polling vs events**: Is a scheduled trigger polling for changes that could be caught by a product event trigger?
- **Event filtering**: Do product event triggers have `filter.expression` to limit invocations to relevant events?
- **ignoreSelf**: If the app writes to entities and listens to events on those entities, is `filter.ignoreSelf: true` set? (Jira only)
- **Early exit**: Do trigger handler functions check for work to do before running expensive operations?
- **External polling**: Could scheduled triggers polling external services be replaced with web triggers?

### Step 7: Forge Remote Analysis

Check if the app uses Forge Remote (`remotes:` section in manifest):
- If present, note that Forge Remote offloads compute to an external backend — the Forge function is not executed for those calls, saving FaaS invocations. But the app loses "Runs on Atlassian" eligibility.
- If not present, check whether the app would benefit from Forge Remote:
  - Compute-intensive operations (ML inference, image processing, complex report generation)
  - Long-running operations that approach the 25-second function timeout
  - Existing backend services the app duplicates logic from
  - Large-scale storage needs exceeding Forge Storage limits
- Note: For most apps, staying on-platform is simpler. Only recommend Forge Remote when there's a genuine need.

### Step 8: Compile Findings

Produce a single issue list sorted: **Critical → Warning → Info**.

---

## Security Checks

| ID | Check | Severity | What to Look For |
|----|-------|----------|-----------------|
| SEC-01 | Overly broad scopes | Critical | `read:jira-work` when only `read:jira-work:jira` (granular) is needed. Any `write:` scope that isn't actually used in code. Any `manage:` or `admin:` scope. |
| SEC-02 | Missing egress restrictions | Critical | External `fetch()` calls in resolvers without matching `permissions.external.fetch.backend` entries in manifest. Wildcard egress domains (`*`). |
| SEC-03 | Hardcoded secrets | Critical | API keys, tokens, passwords, or credentials in source code instead of using Forge environment variables (`process.env.FORGE_*` or `getAppEnvironmentVariable()`). |
| SEC-04 | Missing input sanitization | Critical | User-provided data passed directly to API calls, storage keys, or rendered in Custom UI without sanitization. SQL/NoSQL injection patterns in storage queries. |
| SEC-05 | Unsafe Custom UI CSP | Warning | `unsafe-inline`, `unsafe-eval`, or overly broad `connect-src` in Custom UI resource configuration. |
| SEC-06 | Missing auth checks | Warning | Resolvers that don't verify user context before performing write operations. Missing `context.accountId` validation. |
| SEC-07 | Sensitive data in storage | Warning | PII, tokens, or credentials stored in Forge Storage without encryption or with overly broad access. |
| SEC-08 | Excessive permissions | Warning | `permissions.scopes` includes scopes not referenced by any API call in the codebase. Every scope should have a matching API usage. |
| SEC-09 | Classic scopes used | Info | Using classic (coarse-grained) scopes like `read:jira-work` instead of granular scopes like `read:jira-work:jira`. Granular scopes are preferred. |
| SEC-10 | Unnecessary asApp() usage | Warning | Using `api.asApp()` or `asApp()` for API calls in UI-triggered resolvers when `asUser()` would suffice. `asApp()` bypasses user permission checks — users can access data beyond their entitlements. Only use `asApp()` when there is no user context (scheduled triggers, web triggers) or when the API requires app-level auth (e.g., App Storage API). |

---

## Architecture Checks

| ID | Check | Severity | What to Look For |
|----|-------|----------|-----------------|
| ARC-01 | Function key mismatch | Critical | `resolver.define('functionName')` doesn't match the `function` key in `manifest.yml` modules. |
| ARC-02 | Monolithic resolver | Warning | Single resolver file with 5+ `resolver.define()` calls handling unrelated functionality. Split into separate files by domain. |
| ARC-03 | Missing error handling | Warning | `resolver.define()` callbacks without try-catch. API calls (`requestJira`, `requestConfluence`) without `.catch()` or error status checks. |
| ARC-04 | Incorrect API usage | Warning | Using `api.asApp()` when `api.asUser()` is appropriate (or vice versa). Missing `response.json()` parsing. Not checking `response.ok` or `response.status`. |
| ARC-05 | Module type mismatch | Warning | Using a `jira:issuePanel` module for content that should be a `jira:issueGlance` or `jira:issueContext`. Module type should match UX intent. |
| ARC-06 | Missing resolver validation | Warning | Resolver accepts payload from UI but doesn't validate shape/types before processing. |
| ARC-07 | Poor code organization | Info | All code in a single file. No separation between API logic, business logic, and data access. |
| ARC-08 | Unused modules | Info | Modules defined in `manifest.yml` that have no corresponding UI or resolver implementation. |
| ARC-09 | Missing TypeScript | Info | JavaScript used instead of TypeScript. TypeScript catches many issues at build time. |
| ARC-10 | Forge Remote trade-offs not considered | Info | App uses Forge Remote (`remotes:` in manifest) but may not need it — Forge Remote makes the app ineligible for "Runs on Atlassian" status and requires operating your own infrastructure (patching, uptime, incident response). Only use when on-platform capabilities are genuinely insufficient (compute-intensive tasks, >25s timeout needs, existing backend integration, storage limits exceeded). |

---

## Cost Checks

| ID | Check | Severity | What to Look For |
|----|-------|----------|-----------------|
| CST-01 | Chatty resolvers | Warning | UI making multiple `invoke()` calls on load when data could be batched into a single resolver call. Each invocation counts toward Forge function invocation limits and GB-seconds. |
| CST-02 | No pagination / missing maxResults | Warning | Product API calls (e.g., search issues, get pages) without `maxResults`/`limit` parameters or pagination handling. Fetching default page sizes (often 50–100) when only a few results are needed wastes bandwidth and function duration. Always pass explicit `maxResults` matched to actual need. Conversely, when you DO need all results, use the maximum allowed page size (e.g., `maxResults=100` for Jira search) to minimize the number of paginated round-trips — fewer requests means shorter function duration. |
| CST-03 | Unnecessary storage ops | Warning | Reading the same storage key multiple times in a single invocation. Writing to storage on every invocation when data hasn't changed. KVS writes are ~20× more expensive than reads — minimize write frequency. Short TTL caches (e.g., 1-minute TTL) cause excessive writes; prefer longer TTLs (1 hour+) where data allows. |
| CST-04 | Bloated bundle | Warning | Dependencies that significantly increase bundle size: `lodash` (use `lodash-es` or individual imports), `moment` (use `dayjs` or `date-fns`), `axios` (use native `fetch`). |
| CST-05 | Redundant API calls | Warning | Fetching the same data from product APIs multiple times in one resolver execution. Cache results in variables. |
| CST-06 | Logic in resolver that could run client-side | Warning | Data formatting, sorting, filtering, validation, or transformation done in a resolver when it could run in the browser for free. UI Kit and Custom UI frontends run entirely in the browser and are not subject to function invocation costs. Look for resolvers that only reshape data — move that logic to the frontend. |
| CST-07 | Resolver used for product context | Warning | Invoking a resolver just to get the current issue key, project key, or space key. UI Kit apps should use `useProductContext()` from `@forge/react`; Custom UI apps should use `view.getContext()` from `@forge/bridge`. These provide context directly in the browser with no function invocation. |
| CST-08 | API calls via resolver instead of bridge | Warning | Using a Forge resolver/function to make read-only `requestJira()` or `requestConfluence()` calls when the same call could be made directly from the frontend using `@forge/bridge`. Both UI Kit and Custom UI can call `requestJira()` / `requestConfluence()` directly from the browser — no function invocation needed. Only keep API calls in resolvers when they require `asApp()` context, access secrets, or perform sensitive operations. |
| CST-09 | Resolver called on every render | Warning | Calling `invoke()` inside a component render body or in a `useEffect` without an empty dependency array, causing repeated function invocations on every re-render. Fetch once on mount and store the result in component state. |
| CST-10 | N+1 API calls | Warning | Fetching a list of items then making a separate API call for each item to get details. Use bulk endpoints instead: `POST /rest/api/3/issue/bulkfetch` for issues, `GET /rest/api/3/user/bulk` for users, `POST /rest/api/3/search` with `fields` parameter for search+details in one call. |
| CST-11 | Missing field selection on API calls | Warning | API calls (especially search/list endpoints) that don't specify a `fields` parameter, fetching all fields when only a few are needed. Always specify `fields=summary,status,assignee` (etc.) to reduce response payload size, bandwidth, and function duration. |
| CST-12 | Verbose logging in hot paths | Warning | `console.log()` with large payloads (e.g., `JSON.stringify(event)`) in high-frequency functions like product event triggers or popular resolvers. Log writes are billable at $1.005/GB over the 1 GB free tier. Log only errors and meaningful state changes in production. Use conditional logging gated behind an environment variable for debug output. |
| CST-13 | Large resolver payloads | Info | Resolver returning more data than the UI needs. Trim response objects to only include fields the UI consumes. |
| CST-14 | Unused dependencies | Info | Packages in `dependencies` that are not imported anywhere in the source code. |
| CST-15 | Memory over-provisioning | Info | Function `memoryMiB` in manifest set higher than needed. Default is 256 MB. Simple resolvers doing a single API call often work fine with 128 MB. Cost formula: GB-seconds = (memoryMiB ÷ 1024) × duration. Halving memory halves cost per second. Check for `memoryMiB: 512` or `1024` on lightweight functions. Note: more memory can also improve CPU allocation, which may reduce duration enough to offset the higher per-second cost — profile before reducing. |
| CST-16 | Entity properties not used for free storage | Info | App stores small per-entity metadata (flags, timestamps, status markers) in Forge KVS when Jira entity properties or Confluence content properties could be used instead. Entity properties are **free** (stored by the product, no Forge Storage quota), travel with the entity during export/import, and Jira entity properties are queryable via JQL. Max 32 KB per property. Not suitable for sensitive data (visible via REST API). |
| CST-17 | Pre-filtering not pushed to API layer | Warning | Resolver fetches all items from an API and filters in code (e.g., fetching all issues then checking status in a loop). Push filtering to the API layer: use JQL conditions (`status = Done AND assignee is EMPTY`), CQL, or API query parameters so only relevant items are returned. For scheduled jobs, use date-based filters (`updated >= "${lastRunDate}"`) to process only items changed since the last run. The real saving comes from doing less work, not from batching. |
| CST-18 | Polling external service instead of web trigger | Info | Scheduled trigger polls an external third-party service for updates. Consider replacing with a Forge web trigger — register the web trigger URL as a webhook with the external service so it calls your app only when something changes. Web trigger invocations have no flagfall or network cost, though function runtime is still billed. Eliminates all empty polling invocations. |

---

## Trigger & Scheduling Checks

| ID | Check | Severity | What to Look For |
|----|-------|----------|-----------------|
| TRG-01 | Excessive scheduled trigger frequency | Warning | Scheduled triggers using `interval: fiveMinutes` or `interval: hour` when the data they process changes less frequently. Ask: how often does the underlying data actually change? Prefer `day` or `week` intervals unless sub-hourly freshness is genuinely required. |
| TRG-02 | Polling instead of event triggers | Warning | Scheduled triggers that poll for changes (e.g., checking if issues were updated) instead of using product event triggers (`avi:jira:updated:issue`, etc.) that fire only when the event actually occurs. Replace polling with event-driven triggers to eliminate empty invocations. |
| TRG-03 | Missing trigger event filters | Warning | Product event triggers without a `filter` expression in the manifest. Without filtering, the function is invoked for every matching event across the entire site. Use manifest-level `filter.expression` to restrict invocations to specific projects, issue types, or conditions. |
| TRG-04 | Missing ignoreSelf on triggers | Warning | App that writes to Jira entities AND listens to events on those same entities, without `filter.ignoreSelf: true` in the manifest. This causes feedback loops where the app's own updates trigger its own handler. (Jira events only — not yet supported for Confluence.) |
| TRG-05 | No early exit in trigger handler | Info | Trigger handler functions that don't check whether there is real work to do before performing expensive operations. Add a lightweight guard at the top of the function (e.g., check a timestamp, check event fields) and return early if no action is needed. |
| TRG-06 | Polling external service instead of web trigger | Info | Scheduled trigger polling an external service for updates. Consider replacing with a Forge web trigger — register the web trigger URL as a webhook with the external service so it calls you only when something changes. |

---

## Performance Checks

| ID | Check | Severity | What to Look For |
|----|-------|----------|-----------------|
| PRF-01 | Sequential API calls | Warning | Multiple independent API calls made with `await` one after another instead of `Promise.all()` or `Promise.allSettled()`. Parallel duration ≈ slowest single call vs sequential duration = sum of all calls. Limit parallelism to 5–10 concurrent requests to avoid HTTP 429 rate limits — batch the rest. |
| PRF-02 | Cold start imports | Warning | Heavy libraries imported at the top level of resolver files. Use dynamic `import()` inside resolver handlers for rarely-used heavy dependencies. |
| PRF-03 | Missing loading states | Warning | UI Kit: No `<Spinner>` or loading indicator while resolver data is being fetched. Custom UI: No loading state while `invoke()` is pending. |
| PRF-04 | Large storage entities | Warning | Storing large objects (>100KB) in a single Forge Storage key. Split into smaller chunks or use Entity Store with indexed queries. |
| PRF-05 | Blocking resolver logic | Warning | CPU-intensive operations (JSON parsing of large payloads, complex string manipulation, sorting large arrays) in resolvers without consideration of the 25-second timeout. |
| PRF-06 | Storage iteration instead of query | Warning | Fetching all items from Forge Storage via `storage.query().getMany()` and filtering in code. Use `storage.query()` with indexes, `.where()`, and `.limit()` to push filtering to the storage layer. This reduces KVS read volume and function compute time. |
| PRF-07 | No caching of stable data | Warning | Repeated product API calls for data that rarely changes (e.g., custom field IDs, project metadata, workflow statuses) without any caching strategy. Cache in Forge Storage with a TTL (1 hour+ recommended). Use entity properties (free, stored by the product) for small per-entity data that doesn't need Forge Storage quota. |
| PRF-08 | Unnecessary re-renders | Info | UI Kit: State updates in loops or effects that trigger excessive re-renders. Custom UI: Missing `useMemo`/`useCallback` for expensive computations. |
| PRF-09 | Unoptimized images | Info | Custom UI apps serving large unoptimized images or assets. Use compressed formats and lazy loading. |
| PRF-10 | Code-side filtering instead of API filtering | Warning | Fetching all items from an API and filtering in resolver code. Push filtering to the API layer using JQL, CQL, or API query parameters so only relevant items are returned. For scheduled jobs, use date-based filters (`updated >= "lastRunDate"`) to process only recent changes. The real saving comes from fetching less data, not from batching — a single invocation iterating over thousands of unfiltered items rapidly consumes compute quota. |

---

## Output Format

ALWAYS present findings as a single flat list sorted by severity (Critical first, then Warning, then Info). Do NOT group issues by category — interleave categories within the severity-sorted list. Use this template:

```
## Forge App Review Results

### Summary
- 🔴 Critical: X issues
- 🟡 Warning: Y issues
- 🔵 Info: Z issues

### Issues

🔴 **SEC-01: Overly broad scopes**
  Location: `manifest.yml` line ~X
  Detail: Scope `write:jira-work` is declared but only `read:issue:jira` is used in resolvers.
  Fix: Replace with granular scope `read:issue:jira`. Remove unused write scope.

🟡 **PRF-01: Sequential API calls**
  Location: `src/resolvers/index.js` line ~Y
  Detail: Three `requestJira` calls awaited sequentially. These are independent and can run in parallel.
  Fix: Wrap in `Promise.all([call1, call2, call3])`.

🔵 **ARC-09: Missing TypeScript**
  Location: Project root
  Detail: Project uses JavaScript. TypeScript would catch type errors at build time.
  Fix: Consider migrating to TypeScript. Run `forge create` with TypeScript template for reference.
```

When no issues are found in a category, explicitly state it:
```
✅ **Security**: No issues found
✅ **Triggers & Scheduling**: No issues found (or: No triggers defined)
```

---

## Anti-Patterns — Do NOT Do These

- Do NOT modify code unless the user explicitly asks for fixes
- Do NOT skip reading `manifest.yml` — it is the foundation of the review
- Do NOT guess about permissions — cross-reference every scope against actual API calls in code
- Do NOT report issues without a specific file/line location when possible
- Do NOT combine multiple issues into one finding — each gets its own entry
- Do NOT only check one category — always review all five (Security, Architecture, Cost, Performance, Triggers & Scheduling)
- Do NOT suggest adding dependencies to fix issues — prefer built-in solutions
- Do NOT report issues about test files or dev tooling unless they affect production

---

## Edge Cases

### Minimal App (Hello World)
If the app is very simple (1 module, 1 resolver, minimal UI), still run all checks but expect mostly clean results. Report Info-level suggestions for future growth (e.g., "Consider TypeScript as the app grows").

### Custom UI vs UI Kit
Detect which type by checking:
- UI Kit: imports from `@forge/react`, uses `ForgeReconciler`, JSX with Forge components
- Custom UI: has a `static/` directory or `resources` in manifest, imports from `@forge/bridge`
- Both: some apps use both — check each separately

### Monorepo / Multi-Module
If the manifest declares multiple modules, trace each module's function key to its resolver independently. Don't assume all modules share the same issues.

### No Manifest Found
If `manifest.yml` doesn't exist in the workspace, stop and tell the user: "No `manifest.yml` found. Are you in the correct Forge app directory?" Do NOT proceed without the manifest.
