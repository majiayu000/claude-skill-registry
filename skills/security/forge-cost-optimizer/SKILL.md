---
name: forge-cost-optimizer
description: >
  Optimizes Atlassian Forge apps to reduce platform consumption and avoid unnecessary costs using Atlassian's
  "Optimise Forge platform costs" guidance. Use when the user asks to optimize Forge app costs, reduce Forge
  invocations, lower GB-seconds, reduce storage or log usage, tune memory, replace polling, improve scheduled triggers,
  reduce KVS writes, move work to the frontend, use bridge APIs, batch API calls, add caching, or evaluate Forge Remote
  trade-offs. By default, perform an audit first and offer to make the recommended changes after presenting the audit.
  Only modify files immediately when the user explicitly asks the agent to implement or apply optimizations.
---

# Forge Cost Optimizer

Optimize Forge apps for lower platform consumption while preserving correctness, security, and maintainability. This skill turns Atlassian's Forge cost optimization guidance into an actionable agent workflow.

## Source Guidance

Base recommendations on Atlassian's official guide: <https://developer.atlassian.com/platform/forge/optimise-forge-costs/>

If live Forge documentation tools are available, search the Forge docs for the exact module or API before changing code that depends on current manifest syntax, bridge APIs, storage APIs, trigger filters, or Forge Remote behavior.

## Core Principle

Prioritize changes that reduce unnecessary work:

1. **Avoid invocations entirely** — move safe work to UI Kit / Custom UI frontend, use context from the bridge, replace polling with events, add trigger filters.
2. **Do less work per invocation** — bulk API calls, field selection, source-side filtering, pagination, early exits, bounded concurrency.
3. **Reduce billed data volume** — trim resolver payloads, reduce KVS reads/writes, avoid large log payloads, use entity properties where appropriate.
4. **Tune compute cost** — right-size `memoryMiB`, reduce duration, offload only when the operational trade-off is justified.

Never reduce costs by weakening authorization, exposing secrets to the frontend, skipping required validation, dropping necessary error handling, or making data stale beyond the user's business requirements.

## When Triggered

When the user asks to optimize an existing Forge app, immediately inspect the app before asking questions unless the target app directory is ambiguous.

**Default behavior is audit-first:** complete the cost optimization audit, present prioritized recommendations, and ask the user whether they want the agent to make the recommended changes. Do not modify files during the initial audit unless the user explicitly requested implementation in the same prompt, such as "make the changes", "apply the optimizations", "fix these issues", or "update the code".

Read, in order:

1. `manifest.yml` / `manifest.yaml` — functions, modules, triggers, scheduled triggers, remotes, resources, permissions, endpoint mappings, `memoryMiB`.
2. `package.json` — dependencies, scripts, Forge package versions.
3. Backend/resolver code — `src/**`, handlers referenced by the manifest, storage usage, API calls, logging, async control flow.
4. Frontend code — UI Kit or Custom UI resources, bridge usage, `invoke()` patterns, render lifecycle, caching, payload needs.
5. Any tests or fixtures that describe behavior to preserve.

After the audit, offer clear next-step options such as implementing all quick wins, implementing selected high-impact changes, or collecting usage measurements first. If the user explicitly requested implementation upfront, make safe, localized improvements after the audit findings are understood and explain trade-offs.

## Optimization Workflow

### Step 1: Establish the Cost Profile

Identify which cost drivers the app likely uses:

| Driver | Inspect | Common signals |
|---|---|---|
| Function GB-seconds | `manifest.yml`, handlers | many resolver calls, slow sequential APIs, high `memoryMiB`, heavy transforms |
| Invocations | frontend `invoke()`, triggers | calls on render, chatty UI, scheduled polling, broad event subscriptions |
| KVS / Custom Entities | `storage.*` usage | writes on every request, loops over keys, low TTL cache churn, large values |
| Logs | `console.*` | full event/API payload logging, debug logs in hot paths |
| Forge SQL | SQL client usage | frequent compute requests, long queries, oversized stored data |
| Remote / egress | `remotes`, fetch calls | external polling, compute offload candidates, Runs on Atlassian implications |

When usage metrics are unavailable, mark estimates as qualitative: `High`, `Medium`, `Low`, or `Unknown`.

### Step 2: Find No-Invocation Opportunities

Prefer removing function invocations over making them cheaper.

Check for:

- Resolver calls that only fetch product context. Replace with:
  - UI Kit: `useProductContext()` from `@forge/react`
  - UI Kit or Custom UI: `view.getContext()` from `@forge/bridge`
- Read-only Jira/Confluence API calls routed through a resolver even though user-context access is acceptable. Consider `requestJira()` / `requestConfluence()` from `@forge/bridge`.
- Formatting, sorting, grouping, client-safe validation, or UI-only transformation in resolvers. Move to frontend when data is already authorized for the context user.
- `invoke()` calls inside render bodies, unbounded effects, repeated event handlers, or multiple calls on page load that can be cached or batched.

Keep logic in the backend when it requires `asApp()`, Forge storage, secrets, external credentials, cross-user authorization checks, or sensitive business rules.

### Step 3: Optimize Triggers and Scheduling

Check `scheduledTrigger`, `trigger`, and `webtrigger` modules.

Recommended changes:

- Increase scheduled trigger intervals when business requirements allow (`fiveMinutes` → `hour` → `day` → `week`).
- Replace scheduled polling of Atlassian product changes with product events.
- Replace scheduled polling of external services with inbound webhooks via Forge web triggers when the external service supports webhooks.
- Add manifest `filter.expression` to suppress irrelevant product events before invocation.
- Add `filter.ignoreSelf: true` for Jira triggers that would otherwise process events caused by the app itself.
- Add cheap early exits at the top of handlers before API calls, storage reads, or expensive transforms.
- Use Forge Realtime instead of frontend polling loops that repeatedly invoke resolvers waiting for backend state changes.

### Step 4: Optimize API and Data Fetching

Every API request inside a function contributes to duration. Look for:

- N+1 calls. Replace per-item fetches with bulk endpoints or search APIs that return requested fields.
- Missing `fields`, `expand`, `limit`, or `maxResults` constraints. Request only what the app uses.
- Filtering after fetching all data. Push filters to JQL, CQL, REST query parameters, or storage indexes.
- Sequential independent calls. Use `Promise.all` or bounded concurrency.
- Unbounded concurrency. Batch large workloads to avoid rate limits; use about 5–10 concurrent requests unless docs or tests justify otherwise.
- Large resolver responses. Return only fields consumed by the UI.

### Step 5: Optimize Storage

KVS and Custom Entity reads/writes are billed by data volume above free allowances; writes are much more expensive than reads.

Check for:

- Writes on every invocation even when values have not changed. Compare before writing or debounce writes.
- Very short cache TTLs for data that changes rarely. Prefer longer TTLs where staleness is acceptable.
- Storage reads/writes inside loops. Batch, restructure keys, or use Custom Entities queries.
- `storage.query().getMany()` followed by in-memory filtering. Use `.index(...)`, `.where(...)`, `.limit(...)`, and cursor pagination.
- Large values where only a small subset is needed. Store normalized or trimmed values.
- Small, non-sensitive per-issue/page metadata stored in KVS. Consider Jira entity properties or Confluence content properties instead, noting visibility and 32 KB size constraints.

Do not move sensitive or confidential data to entity/content properties because they may be visible through product REST APIs.

### Step 6: Optimize Logging

Find `console.log`, `console.info`, `console.warn`, `console.error`, and structured logger calls.

Recommended changes:

- Remove or gate debug logs in production hot paths.
- Never log full event payloads, API responses, storage values, secrets, tokens, personal data, or large JSON strings.
- Keep concise error logs and meaningful state changes.
- Add environment-variable gated debug logging only when useful, for example `process.env.DEBUG_LOGGING === 'true'`.

### Step 7: Tune Function Memory

Inspect function entries in `manifest.yml`.

- The cost model is GB-seconds: `(memoryMiB / 1024) × durationSeconds`.
- Lower memory for lightweight resolvers only after considering performance and test coverage.
- Keep or increase memory for large payload processing if lower memory increases duration or causes failures.
- Prefer evidence: logs, profiling, benchmark results, or realistic local tests.
- If evidence is missing, recommend measurement rather than guessing aggressive memory reductions.

### Step 8: Evaluate Forge Remote Carefully

Forge Remote can remove Forge function execution for suitable workloads, but it shifts responsibility to externally operated infrastructure.

Only recommend Forge Remote when one or more are true:

- Long-running work exceeds standard Forge function limits.
- Compute-intensive processing dominates cost or runtime.
- The team already operates a secure backend that should own the logic.
- Storage/query needs genuinely exceed Forge platform capabilities.

Always mention trade-offs:

- The team must secure, scale, monitor, patch, and operate the remote backend.
- Remote architecture may affect Runs on Atlassian eligibility.
- The external infrastructure has its own costs and compliance obligations.

## Safe Implementation Patterns

When modifying code:

1. Preserve behavior and authorization boundaries.
2. Prefer small, reviewable commits worth of changes.
3. Add or update tests when logic changes.
4. Use existing project style and dependencies; do not add dependencies for simple utilities.
5. Avoid sweeping rewrites unless the user explicitly asks.
6. Validate with the narrowest relevant test/build command.

## Finding Patterns Quickly

Search for these patterns:

```text
invoke(
useAction(
useEffect(
requestJira(
requestConfluence(
asApp().requestJira
asUser().requestJira
storage.get
storage.set
storage.query
console.log
console.info
scheduledTrigger
ignoreSelf
memoryMiB
Promise.all
for await
for (
```

Interpret results carefully; a pattern is not automatically a problem.

## Output Format

For default audit-first requests, return the audit and end by offering to implement recommended changes:

```markdown
# Forge Cost Optimization Audit

## Summary
- Overall opportunity: High | Medium | Low
- Highest-impact lever: <invocations | duration | storage | logs | memory | remote>
- Files inspected: <list>

## Prioritized Opportunities
1. [High] <title>
   - Evidence: `<file:line>` and observed pattern
   - Why it costs money: <cost driver>
   - Recommended change: <specific fix>
   - Safety notes: <authorization/data freshness/trade-offs>

## Quick Wins
- <low-risk change>

## Needs Measurement
- <changes that require usage metrics or profiling>

## Recommended Next Step
Would you like me to implement the quick wins, implement selected high-impact changes, or collect usage measurements first?
```

For requests where the user explicitly asked for implementation, return:

```markdown
# Forge Cost Optimization Complete

## Changes Made
- <file>: <change and cost driver reduced>

## Validation
- <commands run and results>

## Expected Impact
- <qualitative or measured impact>

## Follow-ups
- <optional deeper optimizations or metrics to collect>
```

## Anti-Patterns to Avoid

- Do not move privileged `asApp()` operations to the frontend.
- Do not expose secrets, app credentials, or admin-only data in browser code.
- Do not use entity properties for sensitive data.
- Do not remove logs needed for production incident diagnosis; reduce verbosity instead.
- Do not increase cache TTL beyond acceptable product freshness requirements.
- Do not recommend Forge Remote as a default; it is an architectural trade-off, not a simple cost switch.
- Do not claim exact savings without actual usage metrics.
