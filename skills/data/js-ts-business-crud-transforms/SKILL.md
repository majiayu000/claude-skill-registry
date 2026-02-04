---
name: js-ts-business-crud-transforms
description: "Write JavaScript/TypeScript for business applications (frontend and backend) with CRUD, API integration, and data transforms that are correct, readable, and easy to trust. Use when building or reviewing features involving forms, API responses, list/detail views, aggregations, or request/response shaping so outputs need minimal inspection."
compatibility: "JavaScript or TypeScript; Node, Deno, or browser. Assumes ES2020+ (optional chaining, nullish coalescing, etc.). Common context: React/Next.js frontend, REST or RPC backends."
metadata:
  author: icyJoseph
  version: "1.0"
---

# JavaScript/TypeScript for business apps: CRUD, data transforms, and trust

Apply these practices so generated **business application** code—CRUD, API integration, data shaping, and backend handlers—is **correct**, **readable**, **performant**, and **easy to trust** with minimal inspection: explicit types, no silent coercion, single-pass transforms, Map/Set for lookups, and small named helpers.

## Goals

- **Correctness**: Validate external data (API, request body); use explicit types and type guards; return consistent error shapes.
- **Performance**: Prefer single-pass over lists; avoid map-then-find (O(n²)); use Map/Set for lookups; parse once, reuse.
- **Data transforms**: One clear pipeline (fetch → validate → map → filter); named types for API vs UI; avoid silent coercion.
- **Readability**: Small named transform functions; clear separation between "raw" and "shaped" data; predictable control flow.
- **Trust**: Typed request/response contracts and validation make backend and frontend behavior verifiable at a glance.

---

## 1. Model the problem first

Don't jump into framework implementation right away. Before writing route handlers, components, or ORM calls:

- **Converse with the user** about the problem space: what entities exist, what actions users or systems perform, what can go wrong.
- **Sketch data flow**: where data comes from (API, form, DB), how it's transformed, and where it goes (UI, another service, storage). Identify boundaries (e.g. "this is the API shape, this is what the UI needs").
- **Clarify state**: what is server state vs client state, what is derived vs stored, and what triggers updates (submit, refetch, subscription).
- **Agree on the model** (entities, operations, validation rules, error cases). Once data flow, state, and problem space are clear, **overlay that model on the framework** (routes, components, hooks). The framework is the wiring; the model is what you're wiring.

Doing this first keeps implementation aligned with intent and makes it easier to keep validation, transforms, and CRUD consistent.

---

## 2. Correctness and validation

### Validate at boundaries

This applies to **all incoming requests and user input**: validate first, discard or reject invalid input, and **only then** consume or use the input. Never trust raw request/API/form data until it has passed validation.

- **Incoming requests / user input**: Validate required fields and shape (e.g. `body?.id` or `body?.key`). If invalid, return **400** (or equivalent) with a consistent JSON shape (e.g. `{ error: "Missing required field" }`) and **do not** proceed to business logic—discard the bad input.
- **API responses**: Check shape before trusting (e.g. `data?.items ?? []`, `Array.isArray(items)`). If invalid, return a safe default (e.g. `[]`) or throw with a clear message—don't pass garbage downstream.
- Use a schema library (e.g. **Zod**) for non-trivial payloads: `schema.safeParse(entry)` and handle `success`/failure explicitly; map parsed data to your internal types only after validation succeeds.

### Prefer validation libraries; parse as you go

- **Nudge**: For business apps, prefer a validation/schema library (e.g. Zod, Valibot) at boundaries. Parse and validate as you go—transform raw input into validated, typed values in one step, and reject or coerce invalid data instead of letting it through.
- **Raw `Number()` is risky**: `Number("Infinity")`, `Number("")`, `Number("12.5.5")` yield `Infinity`, `0`, `NaN`. In business data (amounts, counts, IDs), those are usually invalid. Use schema number checks (e.g. `z.number().finite()`, or reject non-finite) so NaN/Infinity don't slip into calculations or storage. Same idea for dates, enums, and strings—validate the shape and domain you expect, then use the parsed value.
- **Parse once at the boundary**: Read raw input → run through schema (e.g. `safeParse`) → use the result only if valid; otherwise return 400 or a safe default. Don't scatter `Number(x)` or `parseInt(x, 10)` in business logic without validation.

### Use explicit types for API vs UI

- Define types for **API shape** (e.g. raw API response type) and **UI / internal shape** (e.g. `ItemSummary`, `ListPreview`). Use `Pick<T, K>`, `Omit<T, K>`, or dedicated DTOs so it's obvious what crosses the boundary.
- Type handlers and clients: e.g. `get<Result>(endpoint: string): Promise<Result>` so callers get typed responses.

### Consistent error responses (backend)

- Use a single pattern for errors: e.g. return JSON `{ error: "message" }` with the appropriate status (400 validation, 404 not found, 500 server/DB failure). Same structure across all error responses.
- After a failed operation (e.g. DB RPC), return 500 with a generic user-facing message; log details server-side only.

---

## 3. Data transforms and pipelines

### Single-pass over lists: avoid map-then-find

- **Anti-pattern**: Mapping over a list and calling `.find()` (or similar lookup) on the same list inside the map—e.g. `items.map((item) => ({ ...item, related: items.find((r) => r.id === item.relatedId) }))`. That is O(n²) and redundant.
- **Preferred**: One pass over the list to build a **lookup** (Map or object keyed by id), then map using the lookup—e.g. build `const byId = new Map(items.map((i) => [i.id, i]))` in one pass (or use a single `for` loop), then `items.map((item) => ({ ...item, related: byId.get(item.relatedId) ?? null }))`. Total O(n).
- Same idea for "map then lookup in another list": build a Map from the other list once, then map with `map.get(id)`.

### One clear pipeline for "fetch → use"

- Prefer a single flow: fetch → validate shape → map to internal type → filter invalid items (with a type guard: `.filter((v): v is T => !!v)`).
- Parse once; reuse the parsed/shaped data for all consumers (e.g. same list for list view and aggregates).

### Named transform functions

- Extract transforms by intent: e.g. `groupByCategory`, `aggregateByKey`, `formatForDisplay`, `parseItem`. Keep them **pure** (same input → same output) when possible.
- Use type guards for discriminated data: e.g. `isTypeA(item)`, `isTypeB(item)` so that after a check, TypeScript narrows the type and you can safely access type-specific fields.

### Aggregations and grouping

- Use **Map** keyed by id (or composite key) when aggregating over lists (e.g. by `item.id`). Build the Map in **one pass**, then convert to arrays if needed; sort once at the end (e.g. by `totalCount` or your sort key). Never scan the full list per item (no "for each item, filter/list the rest").
- For "group by" that splits into two buckets (e.g. category A vs B), push into two arrays from **one loop** rather than filtering the full list twice.

### Avoid silent coercion and hidden state

- Use nullish coalescing for "default if missing": `record?.count ?? 0`, `data?.items ?? []`. For numbers from API/forms, prefer schema validation (e.g. `z.number().finite()`) so NaN/Infinity are rejected; avoid raw `Number(x)` in business logic without validation.
- Don't mutate shared objects passed from callers; copy or spread when building new objects (e.g. `{ ...base, extra: entry.extra }`). When branching (e.g. trying a value), restore state after the branch if you mutated shared data.

---

## 4. CRUD and backend handlers

### Read (GET)

- Validate query/params (e.g. `id` or `slug` from `searchParams`); if missing or invalid, return 400 or 404 with the same JSON error shape.
- Fetch from DB or service; if not found, return 404. Return a typed response (e.g. `NextResponse.json(typedData)` or framework equivalent).

### Create / Update / Delete (POST, PATCH, PUT, DELETE)

- Parse and validate body (required fields, types). Return 400 with a consistent `{ error: "..." }` on validation failure.
- Call DB or RPC (e.g. `db.update("table", { id, value })` or your ORM/RPC). On `result.error`, return 500 and a generic message; on success, return 200 and a stable shape (e.g. `{ success: true }`).

### Idempotency and safety

- Prefer non-mutating reads; for writes, use clear operation names (e.g. `recordAction`, `upsertItem`) so behavior is obvious.
- When the same operation might be retried, design so repeating it is safe (e.g. "set to X" rather than "increment by 1", or use a unique request ID to deduplicate).

---

## 5. Frontend and client

### Typed client

- Use a small fetch wrapper with generics: `get<T>(endpoint): Promise<T>`, `post<T>(endpoint, body): Promise<T>` so the response type is explicit. Handle `!response.ok` (e.g. reject or throw) so callers don't assume success.

### Derived state

- Derive UI state from server data when possible (e.g. "top N" from a list, "total" or "summary" from aggregated data) instead of storing redundant state that can get out of sync.
- Keep form state and server state separate; submit from form state, then refetch or update server state after success.

### Loading and errors

- Represent loading and error states explicitly (e.g. `{ status: 'idle' | 'loading' | 'success' | 'error', data?, error? }`). Don't leave `undefined` to mean "loading" if "no data" is also valid.

---

## 6. Readability and structure

### Small, focused functions

- One function per concern: parse one type of record, group by one key, aggregate one metric. Compose them in a higher-level function (e.g. `getAggregatedData` calling `groupByCategory` and `aggregateByKey`).

### Prefer const and early returns

- Use `const` by default; early return on validation failure or missing data so the "happy path" is unindented.
- In transforms, use `continue` or `return null` plus `.filter(Boolean)` (with a type guard) to skip invalid items.

### Naming

- Use consistent names for the same concept across layers (e.g. same id/key in URL, body, and DB). Prefer `data` / `result` for the final shaped payload and `raw` / `entry` for pre-validated items.

---

## 7. Checklist before suggesting code

- [ ] **Model first**: Data flow, state (server vs client, derived vs stored), and problem space agreed with the user before framework implementation.
- [ ] API/request data validated at the boundary (shape or schema); invalid data handled with safe default or 400/500.
- [ ] Types are explicit for API vs UI (DTOs, Pick, or dedicated types); responses and client methods typed.
- [ ] Single pipeline for "fetch → validate → map → filter" where applicable; type guards used for discriminated data.
- [ ] **No map-then-find**: when mapping needs a lookup into the same (or another) list, build a Map in one pass, then map using the lookup.
- [ ] Aggregations use Map keyed by id (or equivalent); one pass to build Map, then sort if needed; no per-item full-list scans.
- [ ] Backend errors return consistent JSON shape and status codes; no sensitive details in client-facing messages.
- [ ] Transform functions are pure and named by intent; no silent coercion or hidden mutation of shared input.
- [ ] Frontend: loading/error states explicit; derived state preferred over duplicated server state.

Following these practices keeps business application code correct, performant, predictable, and easy to trust with minimal inspection.
