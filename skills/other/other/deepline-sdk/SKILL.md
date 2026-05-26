---
name: deepline-sdk
description: "Use this skill for any GTM Engineering work in Deepline — prospecting, list-building, account research, contact enrichment, email/phone/LinkedIn lookup, ICP qualification, lead scoring, outreach copy, and CSV-driven row work. Triggers on phrases like 'enrich this CSV', 'find contacts at these companies', 'build a TAM list', 'waterfall emails for these leads', 'detect job changes', 'write a sequence for', and on any request that mentions Deepline, plays, or named GTM providers (Apollo, Crustdata, Hunter, Dropleads, etc.). Use this even when the user does not explicitly say 'GTM' — most CSV-with-leads tasks and most provider-driven enrichment tasks are GTM tasks. SKIP only when the request is a Clay table extraction (use clay-to-deepline), a cloud-workflow / cron / webhook setup with no enrichment dimension (use workflow-hello-world), or has no Deepline / outbound / data-enrichment dimension at all."
---

# Deepline SDK

Deepline is a TypeScript SDK and CLI for GTM execution: durable, typed workflows that call providers, fan out across rows, run waterfalls, validate, and produce CSVs. This skill teaches an agent how to **choose the right execution path for a job** and then **use the live CLI to discover the current tools and plays** for that path.

This skill is **decision-routed**: read the right job doc for what you are doing, plus the cross-cutting rules below.

> **Names of plays and tools are starting hints. The CLI is the live source of truth.**
>
> Tool IDs and play names get renamed, deprecated, and added all the time. Treat any name in this skill as a starting hint, then confirm with the four discovery commands:
>
> - `deepline plays search <category> --json` — find the current canonical play for a pattern
> - `deepline plays describe <name> --json` — confirm input contract before invoking
> - `deepline tools search <category> --json` — find the current provider tool for a need
> - `deepline tools describe <id> --json` — confirm input contract before invoking
>
> When you are unsure about command shape, run `deepline <command> --help` before guessing flags.

## Two surfaces against one backend

Deepline has two surfaces that hit the same registry, runs, and provider catalog:

- **The CLI** (`deepline`) is for *invoking, discovering, and managing*. It's how you search for tools and plays, run them, inspect runs, and promote a `*.play.ts` file to a live registered play.
- **The SDK** is the TypeScript package (`import from 'deepline'`) for *writing*. Use `definePlay` to write a `*.play.ts` file. Inside, the runtime context (`ctx.tool`, `ctx.runPlay`, `ctx.map`, `ctx.csv`, etc.) is how the play body talks to the same backend the CLI talks to. There is also a programmatic client (`Deepline.connect()`) for embedding tool and play calls in your own Node app — see `shared/plays-best-practices.md`.

The lifecycle of a custom play makes the relationship concrete:

1. Write `my-play.play.ts` with the SDK's `definePlay`.
2. Run it locally via the CLI: `deepline plays run my-play.play.ts --input '{...}' --watch`.
3. Promote it: `deepline plays set-live my-play.play.ts`. Now it's a registered play named `my-play`.
4. Invoke by name from anywhere: `deepline plays run my-play ...` from the CLI, or `ctx.runPlay('my-play', input)` from another play.

Same backend, three invocation paths.

## Mental model

Deepline has two kinds of building blocks. CLI probes answer questions; durable play steps accumulate progress.

Think of a play as a checkpointed data pipeline, not a final wrapper around manual CLI work. For multi-step work, use the CLI to probe the smallest unknowns cheaply, then move each confirmed provider call, row shape, filter, and output column into a local `*.play.ts` file with stable keys. Rerun the play after each step so Deepline can reuse durable checkpoints instead of repeating known-good work.

The loop:

1. Probe one provider/tool/play call with `describe` and a tiny sample run.
2. Add that step to the play with a stable `ctx.tools.execute`, `ctx.runPlay`, or `ctx.map(...).step(...)` key.
3. Run `deepline plays check <file.play.ts>`.
4. Run the play on a tiny input or one row.
5. Inspect the result, then add the next step.

When the user gives you an existing or starter `*.play.ts`, run it before
editing output getter paths. `tools describe` shows declared contracts and
semantic getters; it does not prove what that play serialized at runtime. If
the run output is empty, null, or shaped wrong, use the `top-level outputs:` or
`inspect rows:` `deepline db query` command printed by the run, then edit from
that stored row. Top-level `ctx.tools.execute` / `ctx.step` results are in
`top-level outputs`; `ctx.map` stage results are in `inspect rows`.

Use direct CLI calls for probes, schema inspection, and known prebuilt one-offs. Use a play as soon as the work has multiple provider calls, row fanout, a waterfall, intermediate filtering, or a final output schema the user may want to rerun.

A play should accumulate known-good steps. It should not be a last-minute escape hatch after broad CLI probing, JSON parsing failures, or output truncation. If a `plays check` failure takes more than two edits to resolve, stop and re-anchor on current play-authoring patterns in `shared/plays-best-practices.md`.

| Building block | What it is                                                                                                                                                                                                                                      | How to find one                           | How to invoke                                                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **Tool**       | A single provider call. One tool ID per integration capability (e.g. an email-finder, a company-search, a job-search).                                                                                                                          | `deepline tools search <category> --json` | `deepline tools execute <id> --payload '{...}' --json` from the CLI, or `ctx.tools.execute({ id, tool, input, description })` from a play |
| **Play**       | A typed workflow that composes tools and other plays. Some plays are shipped by Deepline ("prebuilt") for canonical patterns like email waterfalls; others are written by you in a `*.play.ts` file ("custom"). Both kinds invoke the same way. | `deepline plays search <category> --json` | `deepline plays run <name-or-file> --input '{...}' --watch` from the CLI, or `ctx.runPlay(name, input)` from another play |


**Probe** vs **pipeline** is a judgment call:

- **Direct CLI probes** are the right answer for: a single provider lookup, a quick search to inspect what is available, an interactive exploration of a CSV, or kicking off a known prebuilt play once.
- **Custom `*.play.ts` pipelines** are the right answer when: the workflow has multiple row-aware stages (enrich, then validate; lookup, then qualify), the workflow needs to be durable across long runs, the workflow will be re-run on different inputs, or the typed composition makes the logic clearer than a chain of CLI commands.

If a prebuilt play already covers the goal, use it directly — do not wrap it in a custom play just to invoke it.

## Choose your job

Start by reading the matching job doc, then use the CLI loop below to discover live tool and play names. The rules and mental model above apply to every Deepline task, but the provider-specific path, the filters that silently fail, and the order to validate things in are in the job docs — they encode what previous runs learned the expensive way (broad people searches before company qualification, guessed payloads, missing evidence columns, runs that collected data but never wrote the CSV).

For multi-phase tasks (e.g. "find 5 VP Marketing contacts at US fintech companies and get work emails"), discovery and row-level enrichment are different phases — read both docs in order before executing. The first picks the source; the second handles the waterfall.

| If the user wants to… | Start in | Then read |
| --- | --- | --- |
| Find companies (TAM, ICP-matching list, portfolio extraction) | `jobs/finding-companies-and-contacts.md` | `jobs/enriching-and-researching.md` if hydration / research columns are needed |
| Find contacts across a market, segment, ICP, or industry | `jobs/finding-companies-and-contacts.md` | `jobs/enriching-and-researching.md` if emails / phones / LinkedIn URLs are needed |
| Find contacts at known companies (persona lookup, role-based discovery) | `jobs/finding-companies-and-contacts.md` | `jobs/enriching-and-researching.md` if enrichment is needed |
| Detect signals on a list (active hiring, job changes, recent funding) | `jobs/finding-companies-and-contacts.md` | `jobs/enriching-and-researching.md` for AI verification of the signal |
| Fill emails / phones / LinkedIn URLs / company hydration on existing rows | `jobs/enriching-and-researching.md` | |
| Custom AI research per row (pain points, summaries, context for outreach) | `jobs/enriching-and-researching.md` | `jobs/writing-outreach.md` if copy follows |
| Score, classify, or qualify rows against an ICP | `jobs/enriching-and-researching.md` | |
| Write per-row outreach copy, sequences, or scoring language | `jobs/writing-outreach.md` | `jobs/enriching-and-researching.md` if research columns are missing |
| Build, copy, or debug a custom `*.play.ts` file | `shared/plays-best-practices.md` | `references/debugging.md` when a run or check fails |
| Look up a CLI command's flags or output behavior | `deepline <command> --help` | |
| **Exit conditions** | | |
| Extract / convert a Clay table | route to `clay-to-deepline` | Different surface entirely. |
| Set up a cloud cron / webhook workflow with no enrichment | route to `workflow-hello-world` | |
| Pure copywriting with no row-level data work | stay in `jobs/writing-outreach.md` and skip discovery / enrichment | |

When the table does not fit, default to `jobs/enriching-and-researching.md` — it covers most row-level work.

## Execution Loop

Once the job doc has named the pattern category (e.g. "name + domain → email waterfall," "structured firmographic company search"), the CLI loop is how you find the current canonical tool or play for that category and confirm its input contract. Skipping the loop makes the agent guess at provider names, input shapes, or auth state that the CLI would have answered for free.

```
1. Confirm runtime is healthy:        deepline health
2. Confirm auth is registered:        deepline auth status --json
3. For CSV tasks, inspect row shape:  deepline csv show --csv rows.csv --summary
4. Discover the right tool or play:   deepline tools search <category> --json
                                      deepline plays search <category> --json
5. Confirm the input contract:        deepline tools describe <id> --json
                                      deepline plays describe <reference> --json
6. Either:
   a) call directly for one-shot:     deepline tools execute <id> --payload '{...}' --json
                                      deepline plays run <name> --input '{...}' --watch
                                      deepline plays run <name> --csv rows.csv --columns.domain Website --watch
   b) write a *.play.ts file and run: deepline plays run <file.play.ts> --input '{...}' --watch
                                      deepline plays run <file.play.ts> --csv rows.csv --watch
7. Inspect runs as needed:            deepline runs list --play <name> --json
                                      deepline runs get <id> --json
                                      deepline runs tail <id> --json
```

Use `--json` whenever a downstream step parses output. Use `--watch` for evals and short verification runs so the command returns when the run is finished. The CLI auto-emits JSON when stdout is piped, but `--json` is explicit and safe in interactive terminals. When `run` is invoked without `--watch`, it returns the run ID and the play executes asynchronously — follow it with `deepline runs get <id> --json` or `deepline runs tail <id> --json`.

`deepline plays run <name>` runs the live registered version of the play; `deepline plays run <file.play.ts>` runs the local file directly without going through the registry. If the local file diverges from the live version, run by file path explicitly during iteration, or `set-live` the file before calling by name. For any flag's exact behavior, `deepline <command> --help` is authoritative.

## Cross-cutting rules

These apply across every job. The "why" matters more than the rule — knowing the failure mode lets you handle edge cases without re-asking.

### Pilot before scale

Run `--rows 0:1` (or a 1-2 row `--input` subset) before the full input. A misshaped payload at scale burns credits across hundreds of rows before the issue is visible; a pilot exposes the same defect on row 1 for cents.

### When tools come up empty, return null

Do not pattern-complete companies or contacts from training data when a provider returns nothing. The output then looks like success but contains rows the user cannot verify, and the campaign fails at outreach time. Returning null (or fewer rows) keeps the line between *found by tools* and *inferred from memory* visible.

### Preserve provider evidence columns

Provider responses often include proof fields the user did not explicitly ask for: job title, source URL, funding metadata, growth metrics, validation status, confidence scores, hiring counts, role context, provider provenance. Trimming output to the requested display columns makes correct rows unverifiable and leaves downstream review with nothing to work with. If the user asked for `name, title, company, email` and the provider returned `seniority`, `last_changed_at`, and `source`, keep all seven.

### All I/O through `ctx.`* (replay-safety)

Inside a custom `*.play.ts`, every non-deterministic operation goes through the runtime: `ctx.tool`, `ctx.runPlay`, `ctx.csv`, `ctx.map`, `ctx.waterfall`, `ctx.log`, `ctx.sleep`. The play body re-executes during durability replay; reading `process.env`, calling `Date.now()`, opening a file with `fs`, or hitting the network with `fetch` makes the second execution see different values, which corrupts the workflow or fails replay-safety validation. See `shared/plays-best-practices.md` before writing a custom play.

### Prebuilts are templates

Search for a prebuilt before writing a custom play. If the prebuilt's behavior fits, run it directly. If only CSV headers differ, pass column aliases such as `--columns.first_name "First Name"` instead of copying the play.

When the user asks to customize, compose, extend, or use a prebuilt as a starting point, prefer the copy/edit loop over rewriting from scratch:

```bash
deepline plays search <task> --json
deepline plays describe <play-name-from-search> --json
deepline plays get <play-name-from-search> --source --out ./my-play.play.ts
deepline plays check ./my-play.play.ts
deepline plays run ./my-play.play.ts --csv pilot.csv --watch
```

Copy a prebuilt only for semantic changes: provider order, validation policy, extra stages, filtering, or output shape. `plays get --source --out` preserves the provider order, input contract, CSV handling, logs, and output conventions the prebuilt already got right. Do not parse `play.sourceCode` out of JSON when copying templates. Run the copied play by file path while iterating, then `set-live` when stable. See `shared/plays-best-practices.md` for the copy/edit loop.

### Outputs go in a project-local working directory

Set up a task-descriptive slug at step zero (e.g. `deepline/data/acme-email-waterfall`). `/tmp/` is wiped on reboot and users have lost paid enrichment outputs to it; outputs that cost credits belong in a directory the user controls.

```bash
WORKDIR="deepline/data/<descriptive-slug>" && mkdir -p "$WORKDIR" && echo "$WORKDIR"
```

When authoring a custom `*.play.ts`, keep the play file in the current working directory when `node_modules/deepline` is available there; otherwise use a project directory with the Deepline SDK dependencies installed. Eval and scratch workspaces may provide those dependencies locally, and in that case the play source should stay inside the current workspace. Do not search parent repos or unrelated worktrees for old `*.play.ts` scratch files. After a run completes, export the final CSV to the user-requested output path with `deepline runs export <run-id> --out <path>`.

### `ctx.csv` returns a dataset, not an array

When a play processes a CSV, the play owns the input field name. If the play declares `input: { csv: string }`, run it with `deepline plays run enrich.play.ts --csv leads.csv --watch` and call `ctx.csv(input.csv, { columns, required })`. A play can instead declare `leads_csv` or another unreserved name; the matching CLI flag is just the field name. If the play declares a field that collides with a reserved run flag, such as `file`, pass it through JSON input: `--input '{"file":"leads.csv"}'`. `ctx.csv()` with no argument is invalid. The return value is a `PlayDataset` — pass it directly to `ctx.map`, do not cast it, do not read `.length`, do not iterate it manually. Row progress, retries, idempotency, and table output all depend on the runtime owning the iteration; manual `for...of` loops break those guarantees. See `jobs/enriching-and-researching.md` for the row-work patterns built on this contract.

## Examples

Two minimal shapes anchoring the one-shot-vs-custom-play choice. Realistic patterns (provider routing, two-stage maps, validation) live in the job docs.

### One-shot CLI

```bash
deepline plays search email --json
deepline plays describe <play-name-from-search> --json
deepline plays run <play-name-from-search> --input '{...}' --watch
```

### Custom `*.play.ts`

```typescript
import { definePlay } from 'deepline';

type Lead = {
  first_name: string;
  last_name: string;
  linkedin_url?: string | null;
};

export default definePlay('lead-review-list', async (ctx, input: { leads: Lead[] }) => {
  const rows = await ctx
    .map('lead_review', input.leads)
    .step('full_name', (lead) => `${lead.first_name} ${lead.last_name}`.trim())
    .step('linkedin_url', (lead) => lead.linkedin_url ?? null)
    .run({ description: 'Prepare leads for review.' });

  return { rows };
});
```

For two-stage maps (enrich → validate), provider routing, the Sales Nav URL trap, and the personal-vs-work email split, read `jobs/enriching-and-researching.md`. For the full `ctx.*` contract, replay-safety rules, idempotent iteration, and copying-prebuilt pattern, read `shared/plays-best-practices.md`.
