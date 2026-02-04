---
name: verify-build
description: Run build and automated consistency checks across types, config, state, and webhook ordering.
user-invocable: true
---

You are a build verifier for the claude-code-reviewer project. Run the build and a series of automated consistency checks, then present results as a pass/fail checklist.

## Checks

### 1. TypeScript Build

Run `npm run build`. If it fails, stop and report the errors. All subsequent checks require a passing build.

### 2. Config Defaults Completeness

Compare every field in the `ReviewConfig` interface (`src/types.ts`) against the keys present in `DEFAULTS.review` in `src/config.ts`.

- Read `src/types.ts` and extract all fields from `ReviewConfig`
- Read `src/config.ts` and extract all keys from `DEFAULTS.review`
- **PASS** if every `ReviewConfig` field has a corresponding default
- **FAIL** if any field is missing — list the missing fields

Do the same for `PollingConfig`, `WebhookConfig`, and `GithubConfig` against their respective DEFAULTS sections.

### 3. Config.yaml Documentation

Compare documented fields in `config.yaml` against the `ReviewConfig` interface.

- Read `config.yaml` and extract all keys under the `review:` section
- Compare against `ReviewConfig` fields from `src/types.ts`
- **PASS** if every `ReviewConfig` field is documented in config.yaml
- **FAIL** if any field is undocumented — list the missing fields

Also check `polling:`, `webhook:`, `github:`, and the top-level `mode:` field.

### 4. State Backfill Completeness

Compare `PRState` fields from `src/types.ts` against:
- The `getOrCreate()` defaults in `src/state/store.ts` (the object literal in the `if (!this.state.prs[key])` block)
- The V2 backfill loop in `store.ts` (the `for (const entry of Object.values(this.state.prs))` block after V2 load)
- The V1 migration in `migrateV1()`

A field is covered if it appears in EITHER `getOrCreate` defaults OR the backfill loop OR V1 migration.

- **PASS** if every `PRState` field is covered
- **FAIL** if any field could be undefined at runtime — list missing fields

Do the same for `ReviewRecord` fields against the backfill loop (`for (const rev of entry.reviews)`).

### 5. Webhook Response Ordering

Verify that in `src/webhook/server.ts`, the HTTP response (`res.writeHead(202)` + `res.end()`) is sent BEFORE any async `processPR()` or `triggerCommentReview()` calls.

- Read `server.ts` and check the `pull_request` event handler and `handleIssueComment` method
- For each handler that calls `processPR` or `triggerCommentReview`, verify `res.writeHead(202)` and `res.end("Accepted")` appear on earlier lines
- **PASS** if response always precedes async work
- **FAIL** if any handler sends the response after starting async work

## Output Format

Present results as a checklist:

```
## Build Verification Results

- [x] TypeScript build — passed
- [x] Config defaults — all ReviewConfig fields have defaults
- [ ] Config.yaml docs — MISSING: fieldA, fieldB
- [x] State backfill — all PRState fields covered
- [x] Webhook response ordering — response before async in all handlers
```

Use `[x]` for pass, `[ ]` for fail. For failures, include specific details about what's wrong and where to fix it.
