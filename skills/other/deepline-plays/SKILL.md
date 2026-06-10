---
name: deepline-plays
description: 'Use for Deepline Plays/CLI V2 work: get started, find/describe/run prebuilts, process CSVs, bootstrap/wrap/fork plays, author durable V2 workflows, find companies or contacts, size TAM, inspect/export runs, explain billing, and repair failures. Triggers on deepline CLI work, plays, prebuilts, CSV enrichment, prospecting, TAM, provider routing, play authoring, staleAfterSeconds, datasets, runs, exports, billing, and eval-style GTM tasks.'
---

# Getting Started With Deepline Plays

Deepline GTM work is paid uncertainty reduction. The play is the notebook, stable ids are the cache, datasets are durable row state, getters are the interface, and CSV is an input/output boundary. Start from live Deepline contracts, then run exactly or build a small durable wrapper.

Default rule: every user request is fresh unless the user names a project, play file, run id, saved play, or asks to continue prior work. Do not inspect old local `.play.ts`, README, or CSV files for route evidence.

Run one Deepline command at a time when you need its output. Avoid `jq`, shell parsing, background jobs, raw `curl`, env spelunking, or local provider probes around Deepline commands. JSON output is for reading directly.

## Core Loop

1. **Preflight:** check auth/health/balance when spend or cloud execution is likely.
2. **Describe before spend:** `plays search` -> `plays describe`; for tools, `tools search` -> `tools describe`.
3. **Choose direct vs build:** direct-run only when the described contract exactly matches input, output, export, freshness, and pricing. Otherwise bootstrap/wrap/fork.
4. **Check before run:** `plays describe` is the gate for prebuilts; `plays check <file>` is mandatory for local, bootstrapped, or forked plays.
5. **Pilot before scale:** run 1-3 rows or a small sample, then inspect/export.
6. **Report reality:** run id, export path, charged credits or why not visible, executed/reused/failed counts when available, and repair class.

Safe planning-only commands: auth/health/balance, `plays search`, `plays describe`, `tools search`, `tools describe`, `plays check`, `plays bootstrap --help`, and local scaffolding. Do not call `plays run` or provider execution in planning-only mode.

## Which Piece?

| Situation | Use | First commands | Gate |
| --- | --- | --- | --- |
| Known play/prebuilt may fit exactly | This page + run/export reference | `deepline plays describe prebuilt/<name> --json` | Input/output/export/pricing/freshness match |
| CSV needs aliases, validation, projection, or join | This page + run/export reference | `plays describe`, inspect headers, `plays bootstrap` | `plays check` and pilot pass |
| Find companies, contacts, or TAM | `references/find-companies-contacts-tam.md` + this page | `plays search "company list TAM..."`, fallback `tools search` | Criteria, evidence, count/sample basis, and cost are legible |
| Company -> contacts -> email/phone | Company/contact/TAM reference + this page | search/describe company, people, and channel contracts | Pilot proves account grain and contact identity |
| API/cron/webhook monitor | This page + generated refs + run/export reference | `plays bootstrap --help`, generated SDK/API refs | Trigger, input, side effects, and pilot are isolated |
| Billing/rerun/debug/export question | `references/run-export-inspect-repair.md` first | `runs get`, `runs export`, `runs logs` | No paid rerun until run metadata is understood |

## Find And Describe

Names are hints. Live `search` and `describe` are source of truth.

```bash
deepline plays search "<job words>" --json
deepline plays describe prebuilt/<candidate> --json
deepline tools search "<provider need>" --categories <category> --json
deepline tools describe <tool-id> --json
```

Rules:

- `plays search` defaults to trusted Deepline-managed prebuilts. Use `--all` only when the user explicitly names or asks for their own/user/org play.
- Search results are candidates. Describe before using them.
- Do not use `tools describe` for a prebuilt play.
- Job-change/email/phone/LinkedIn/contact workflows are live play searches, not job docs.
- If the task is account sourcing, contacts, provider strategy, signals, or TAM, load `references/find-companies-contacts-tam.md`.

Contract checklist from `plays describe` / `tools describe`:

- canonical reference and namespace
- owner/editability/cloneability
- scalar, CSV, or API input modes
- required fields and accepted aliases
- output object and row dataset shape
- nested paths and flattened export headers
- pricing and billing mode
- freshness/staleness behavior
- direct-run vs bootstrap/wrap/fork constraints
- run/export/clone starter commands
- declared getters such as `result.extractedValues.email?.get()`

## Direct Prebuilt Run

Direct-run only when exact:

- described scalar/CSV/API input matches the user input
- no CSV mapping or semantic repair is needed
- output schema includes the requested result
- export dataset path is known
- freshness/caching behavior is acceptable
- pricing mode and likely scale are acceptable

Typical flow:

```bash
deepline plays describe prebuilt/<name> --json
deepline plays run prebuilt/<name> --input '{"field":"value"}' --watch
deepline runs get <run-id> --full --json
deepline runs export <run-id> --dataset result.rows --out rows.csv
```

For CSV prebuilts, compare required headers to actual headers. If aliases are unsupported or output projection is custom, bootstrap a wrapper instead of editing the prebuilt.

## Bootstrap, Wrap, Fork

Bootstrap is the composition tool. It is not anti-prebuilt.

Bootstrap/wrap when:

- CSV headers need mapping, validation, or projection
- a prebuilt is a useful stage but not the whole answer
- company rows need people/contact/channel fanout
- provider source rows need durable row state
- final output needs flat user-facing columns
- row gates, fallback legs, miss reasons, or stale policy matter

Fork when internals need to change:

- provider/tool order
- internal stale policy
- getter metadata
- billing stage
- native prebuilt logic

Do not fork for simple CSV aliases or final formatting. Wrap instead.

```bash
deepline plays bootstrap <family> --from <source> --using play:prebuilt/<candidate> --limit 5 --out workflow.play.ts
deepline plays get prebuilt/<name> --source --out fork.play.ts
deepline plays check workflow.play.ts
```

Route families: `people-list`, `company-list`, `people-email`, `people-phone`, `company-people`, `company-people-email`, `company-people-phone`.

If bootstrap syntax fails, run `deepline plays bootstrap --help` or route help and retry with explicit stage flags such as `--people`, `--email`, or `--phone`.

## Authoring Basics

Use the current V2 shape from generated references when exact syntax matters:

```ts
import { definePlay } from 'deepline';

type Input = { limit?: number };

export default definePlay(
  'gtm-play',
  async (ctx, input: Input = {}) => {
    return { ok: true, limit: input.limit ?? 5 };
  },
  { billing: { maxCreditsPerRun: 50 } },
);
```

Authoring rules:

- Prefer typed inline input. Import validators only if generated refs or bootstrap output prove they exist.
- Use `ctx.csv`, `ctx.dataset`, `ctx.tools.execute`, `ctx.runPlay`, `ctx.step`, `ctx.fetch`, and `ctx.secrets`.
- Do not use local `fs`, raw `fetch`, shell commands, env reads, `Date.now`, or `Math.random` inside play bodies.
- Use stable ids for paid work. Rename ids only to refresh wrong/stale provider data or changed semantics.
- Return datasets for CSV/exportable outputs.
- Use declared getters. Do not parse raw payload paths when `extractedValues.*.get()` exists.
- Project to flat user-facing columns with `status`, `miss_reason`, evidence/source, and requested output fields.

Dynamic staleness pattern:

```text
.withColumn("job_change", {
  run: async ({ row, ctx, previousCell }) => {
    if (previousCell?.value.status === "stale_contact") {
      return previousCell.value;
    }

    return await checkJobChange(row, ctx);
  },
  staleAfterSeconds: (value) =>
    value.status === "stale_contact" ? null : 30 * 24 * 60 * 60,
})
```

Semantics:

- `value` is the new value returned by `run`.
- `null` stale time means no next expiry.
- Existing cells with missing stale metadata may schedule once to backfill.
- The `previousCell` guard avoids paying again during metadata backfill.

## Load References

Load only when the task needs it:

- `references/find-companies-contacts-tam.md` (**Find Companies, Contacts, And TAM**): account sourcing, contacts, TAM, portfolio/investor lists, hiring-qualified companies, signals, personas, provider playbooks, account-first strategy, evidence, or fanout economics.
- `references/run-export-inspect-repair.md` (**Run, Export, Inspect, Repair**): before scale; after every meaningful run; for billing, rerun, export, cached rows, failed rows, logs, suspicious output, partial repair, or UI/run mismatch.
- `references/sdk-reference.md`: exact current SDK signatures.
- `references/api-reference.md`: exact API/manual invocation, polling, streaming, stop, list, inspect/export, and artifact routes.

Do not load a separate reference for ordinary prebuilt search/describe/run, CSV contracts, bootstrap, wrapping, or forking. Those basics are here.

## Finish Shape

When work ran, summarize:

- route and play reference
- run id
- rows requested and returned
- executed/reused/failed counts when visible
- charged credits or why credits are missing/zero
- export path and dataset path
- miss/failure classes
- next action: scale, rerun, repair, or stop

When no paid run happened, say so explicitly and list the safe commands used.
