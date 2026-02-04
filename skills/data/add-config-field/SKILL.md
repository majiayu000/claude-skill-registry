---
name: add-config-field
description: Guide adding a new config field across types, defaults, config.yaml, and optional state/env wiring.
user-invocable: true
---

You are a guided assistant for adding new configuration fields to the claude-code-reviewer project. You will gather requirements, show current state, and produce an implementation checklist with exact file locations.

## Step 1: Gather Requirements

Ask the user for:

1. **Field name** — camelCase (e.g., `maxConcurrentReviews`)
2. **Config section** — which interface it belongs to: `ReviewConfig`, `PollingConfig`, `WebhookConfig`, `GithubConfig`, or top-level `AppConfig`
3. **Type** — TypeScript type (e.g., `number`, `boolean`, `string`, `string[]`)
4. **Default value** — what the default should be
5. **Description** — one-line description for config.yaml comment
6. **Is it also a PRState field?** — does it need to be tracked per-PR in the state file?
7. **Is it a ReviewRecord field?** — does it need to be stored per-review in the reviews array?
8. **Needs env override?** — should there be an environment variable override (like `GITHUB_TOKEN`)?

## Step 2: Show Current State

Read and display the relevant sections:

- The target interface from `src/types.ts` (e.g., `ReviewConfig`)
- The corresponding DEFAULTS section from `src/config.ts`
- The corresponding section from `config.yaml`
- If PRState field: show `PRState` interface, `getOrCreate` defaults, and V2 backfill loop from `src/state/store.ts`
- If ReviewRecord field: show `ReviewRecord` interface and the nested backfill loop (`for (const rev of entry.reviews)`) in `src/state/store.ts`

## Step 3: Generate Implementation Checklist

Produce a numbered checklist with exact file paths and locations:

### A. Add to interface — `src/types.ts`

Show the exact line to add the field to the interface, matching existing style (field name, type, with a comment if other fields have comments).

### B. Add to DEFAULTS — `src/config.ts`

Show the exact line to add in the `DEFAULTS` constant, matching existing indentation and value format.

### C. Document in config.yaml — `config.yaml`

Show the exact line to add under the relevant section, with a trailing comment matching the style of existing entries.

### D. (Optional) Add env override — `src/config.ts`

If an env override is needed, show the `if (process.env.X)` block to add in the env override section of `loadConfig()`, matching the pattern of existing overrides:
- `GITHUB_TOKEN` → string, no validation
- `WEBHOOK_SECRET` → string, no validation
- `WEBHOOK_PORT` → numeric, range validation (1-65535)
- `POLLING_INTERVAL` → numeric, `>= 1` validation
- `MODE` → enum, allowed-values validation

Use the appropriate validation pattern for the field's type. Also add a `# or ENV_VAR_NAME env var` comment to the field's entry in `config.yaml`, matching the pattern used for `secret` and `token`.

### E. (Optional) Add to PRState — `src/types.ts` + `src/state/store.ts`

If it's also a PRState field:
- Add to `PRState` interface in `src/types.ts`
- Add default in `getOrCreate()` in `src/state/store.ts`
- Add backfill in the V2 backfill loop in `store.ts` (using `entry.field ??= defaultValue`)
- Add field in the V1 migration `migrateV1()` in `store.ts`

### F. (Optional) Add to ReviewRecord — `src/types.ts` + `src/state/store.ts`

If it's a ReviewRecord field:
- Add to `ReviewRecord` interface in `src/types.ts`
- Add backfill in the nested loop in `store.ts` (`for (const rev of entry.reviews) { rev.field ??= defaultValue; }`)
- Add field in the V1 migration `migrateV1()` ReviewRecord object in `store.ts`

## Step 4: Recommend Verification

After implementation, recommend running `/verify-build` to confirm:
- Build passes
- Config defaults are complete
- Config.yaml docs are complete
- State backfill covers the new field (if applicable)

## Notes

- Do NOT make the changes yourself — present the checklist for the user to review, then implement only after confirmation
- Match existing code style exactly (indentation, trailing commas, comment format)
- If the field affects review behavior, mention that `decisions.ts` or `reviewer.ts` may need updates to actually use the field
