---
name: geo-pipeline
description: Entry point + orchestrator for the recomby-geo GEO (Generative Engine Optimization) workflow on OpenAI Codex CLI. Use when the user wants to run any stage of the GEO pipeline on a client folder — intake, visibility audit, content-gap analysis, content brief, draft production, distribution, or monthly re-audit — or asks to "run GEO", "audit AI search visibility", or "GEO this client". Codex has no bare slash commands, so this skill is how the 7 stages (that Claude Code runs as /01-intake … /07-reaudit) are driven on Codex. It routes to the per-stage specs in this plugin's commands/ and enforces the orchestration rules. Does not auto-fill expert content — the human-in-loop brief checkpoint is the moat.
license: Recomby.ai — same terms as the recomby-geo plugin root LICENSE
---

# geo-pipeline — Codex orchestrator for recomby-geo

On Claude Code each stage is a bare slash command (`/01-intake` …
`/07-reaudit`). Codex CLI has no bare custom commands, so this skill is the
Codex entry point: it carries the orchestration rules and routes to the
per-stage specification files, which are the **single source of truth**
shared with the Claude Code side. Do not duplicate stage logic here — read
the stage file and follow it.

**Per-stage specs (read the one you're running):**
`commands/01-intake.md`, `commands/02-audit.md`, `commands/03-gap.md`,
`commands/04-content-brief.md`, `commands/05-production.md`,
`commands/06-distribution.md`, `commands/07-reaudit.md` (relative to this
plugin's root). Full directory convention + dependency graph:
`orchestrator/run.md`.

## How to run a stage on Codex

1. Identify the client folder `clients/<slug>/` and the stage the user wants.
2. Read the matching `commands/0X-*.md` and execute its Procedure verbatim.
3. Validate every JSON artifact the stage writes against its schema before
   moving on (Codex has no built-in schema validation — run it explicitly):

   ```bash
   python3 - <<'PY'
   import json, jsonschema
   pairs = {
     "brand_context.json": "brand_context.schema.json",
     "visibility_baseline.json": "visibility_baseline.schema.json",
     "content_priorities.json": "content_priorities.schema.json",
   }  # see schemas/ for the full set incl. attribution_diff + review_feedback
   # jsonschema.Draft202012Validator(json.load(open("plugins/recomby-geo/schemas/<file>"))).validate(json.load(open("clients/<slug>/<artifact>")))
   print("validate each artifact against plugins/recomby-geo/schemas/*.schema.json")
   PY
   ```

4. Stop at the human-in-loop points (see rules below).

## Stage order (never run out of order)

```
inputs/ → 01-intake → brand_context.json
        → 02-audit  → visibility_baseline.json
        → 03-gap    → content_priorities.json
        → 04-content-brief → briefs/<id>.md (+ .html, REQUIRED-FILL slots)
            [EXPERT FILLS THE SLOTS — not the AI]
          04 Step 9 verifies fills → status: ready-for-production
        → 05-production → drafts/<id>.md (+ review .html)
        → 06-distribution → distribution/<id>.json + publish-bundle.md
            [PUBLISH + WAIT 7+ days]
        → 07-reaudit (monthly) → reaudit/round-N.json → feeds next 03-gap
```

02 needs 01; 03 needs 01+02; 04 needs 01+03; 05 needs 04 (filled); 06 needs
05; 07 needs a prior 02.

## Hard rules (orchestration level)

1. **The expert fills briefs — not the AI.** `05-production` refuses to run
   unless `briefs/<id>.meta.json` status is `ready-for-production`. Never
   auto-fill REQUIRED-FILL slots; pause the pipeline if the expert is
   unavailable. This human-in-loop checkpoint is the entire moat.
2. **Schema validation is enforced.** If an artifact fails its schema, fix
   before moving on. Schemas: `schemas/*.schema.json`.
3. **One client per folder.** Don't share JSON across `clients/<slug>/`
   folders or factor out "common" context.
4. **Never run a stage out of order** (see graph above).

## Client review HTML

Stages 04 and 05 produce interactive HTML for the client via the
`geo-review-html` skill (also in this plugin). On Codex this works the same
as on Claude Code — the stage spec already calls `render_html.py`.

## Requirements

The capability skills' scripts (e.g. `seo-geo-optimizer`, `geo-review-html`)
need `python3` on PATH; the schema validation step needs `jsonschema`
(`pip install jsonschema`). These are the same dependencies as the Claude
Code side.
