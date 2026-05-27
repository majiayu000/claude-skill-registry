---
name: artifact-analysis
description: "Use when the user wants a cited, structured read of local documents and project knowledge. Triggers on: \"analyze these docs\", \"scan my project for context\", \"read the docs folder\", \"summarize what's in .beagle/concepts/\", \"extract context from docs/\", \"what's in this folder\", \"go read everything in X and tell me what's there\". Also invoked programmatically by other beagle skills (prfaq-beagle Ignition, brainstorm-beagle reference points, strategy-interview context grounding) via the companion contract. Does NOT trigger on codebase lookups (\"find this function\", \"search the repo\"), web research (use web-research), LLM-as-judge evaluation (use llm-judge), or document editing (use humanize-beagle). Produces a written scan plan, parallel-subagent findings, and a cited synthesis report on disk — never inline prose, never unsourced claims."
---

# Artifact Analysis

Turn a set of local paths (or a beagle project's conventional knowledge locations) into a cited, structured extraction of insights, context, decisions, and raw detail.

The deliverable is always on disk: a written scan plan the caller can audit, one findings file per slice, and a synthesized report with path-anchored citations. Nothing returns as inline prose, and no claim ships without a source path + verbatim excerpt behind it.

## When to use

- A user asks for a local-document read — "analyze the docs folder", "scan the project for context", "extract what's in .beagle/concepts/".
- Another beagle skill invokes this one programmatically as a grounding companion (see `references/companion-contract.md`).
- The caller wants auditable output: a plan written before extraction, findings files per slice, and a citation-backed synthesis report.

## When NOT to use

- Codebase lookups ("where is this function defined", "grep for this symbol"). Use Grep/Glob.
- Web research. Use `web-research`.
- Comparative evaluation of two implementations or source credibility adjudication. Use `llm-judge`.
- Rewriting or editing the scanned documents. Use `humanize-beagle` or the file tools.
- PDF / image OCR / format conversion. First version reads plain text and markdown only. `beagle-core:docling` is the future path.
- Paywalled or authentication-gated remote sources. This is a local-filesystem primitive.
- Coaching, challenge, or reshaping of the caller's question. That belongs to the caller.

## Workflow

Four steps, in order. No step is skippable.

### Hard gates

Advance to the next step only when the **pass condition** is true—confirm using files under `output_dir` (and tool output), not memory.

| After | Pass condition |
| --- | --- |
| `plan.md` written | `plan.md` exists and includes intent, resolved paths, slices, per-slice briefs, skip patterns, budgets applied, and synthesis approach (same fields as **The scan plan (`plan.md`)**). |
| Subagent dispatch | Either the **empty corpus** path was taken (no subagents; `plan.md` documents zero readable documents) **or** every slice listed in `plan.md` has `findings/<slice-slug>.md` on disk. |
| `report.md` written | `report.md` exists; headings match `references/report-template.md` (seven sections plus `## Sources`). |
| Before return to caller | Every row of `references/failure-modes.md` → **Verification checklist (orchestrator runs at end)** is checked off, *or* any failed check is recorded under `## Gaps & Limitations` in `report.md` as that failure-modes file prescribes. |

1. **Write `plan.md`** — resolved paths (with any auto-discovery applied), intent summary (when provided), per-slice briefs, skip patterns, and how findings will be synthesized.
2. **Dispatch subagents** — spawn 1-3 parallel subagents over non-overlapping slices of the resolved paths. Each writes `findings/<slice-slug>.md` under `output_dir`.
3. **Synthesize `report.md`** — fold findings into the seven fixed sections with path-anchored citations.
4. **Verify before returning** — satisfy the last **Hard gates** row; execute the numbered checklist in `references/failure-modes.md` (**Verification checklist (orchestrator runs at end)**). Any check that fails becomes an entry in `Gaps & Limitations` per that file—do not return a deliverable with silent checklist failures.

```
Receive paths + optional intent ──→ Auto-discover if paths empty
                                   ↓
                                 Write plan.md (no user-confirmation pause)
                                   ↓
                                 Dispatch subagents (up to 3 parallel)
                                   ↓
                                 Collect findings/<slice>.md files
                                   ↓
                                 Synthesize report.md
                                   ↓
                                 Return paths to caller
```

Unlike `web-research`, artifact-analysis does **not** pause for a plan review gate. Local scanning is cheap; `plan.md` is written for auditability so a reader weeks later can tell what each subagent was told. Unlike web-research, there is no fail-fast on missing tools — filesystem tooling (Read, Glob, Grep) is assumed present in the Claude Code environment.

## Inputs

| Field        | Type               | Required | Default       | Purpose                                                                             |
| ------------ | ------------------ | -------- | ------------- | ----------------------------------------------------------------------------------- |
| `intent`     | string             | no       | —             | What the caller is looking for / why. When absent, the skill extracts anything structurally important. |
| `paths`      | list of strings    | no       | auto-discover | Directories and/or explicit files. When absent, auto-discover (see below).          |
| `output_dir` | absolute path      | no       | derived       | Where `plan.md`, `findings/`, and `report.md` land.                                 |
| `refresh`    | bool               | no       | `false`       | When true, allow overwriting a prior run in the same `output_dir`.                  |

The skill does not parse caller-specific structures. Callers pass an intent string and/or a path list.

### Auto-discovery

When `paths` is absent or empty, scan beagle's conventional knowledge locations:

- `.beagle/concepts/` — concept specs and analysis folders.
- `.planning/` — roadmap, state, and phase artifacts.
- `docs/` — project documentation.
- Top-level files matching `README*`, `BRIEF*`, `OVERVIEW*`, `CONTEXT*`, `CLAUDE.md`, `AGENTS.md`.

Resolved paths (including any auto-discovery) are listed verbatim in `plan.md` so the caller can see exactly which files were included.

### Intent modes

- **`intent` present** — extraction is targeted to what is relevant to the intent. Off-topic material goes into `Raw Detail Worth Preserving` only when it is a specific quote or metric worth keeping.
- **`intent` absent** — generic-salient-extraction mode. Subagents extract anything structurally important (insights, decisions, technical constraints, user/market context) without an interpretive filter.

## Output location

If the caller passes `output_dir`, use it verbatim. Otherwise derive the default:

```
.beagle/analysis/<slug>/
```

**Slug derivation** (stable so re-running the same input on the same day lands on the same folder):

1. If `intent` is present, slug from the intent string: lowercase, strip punctuation, collapse whitespace to single hyphens, truncate to 60 characters on a word boundary (cut at the last hyphen before 60; if no hyphen exists before position 60, hard-cut at 60).
2. If `intent` is absent, slug from the first scanned path's basename using the same rules.
3. Prepend `YYYY-MM-DD-`.

**Re-run protection.** Before writing anything, check whether `output_dir` already contains `plan.md` or `report.md`. If it does and `refresh` is not `true`, refuse with a message naming the existing folder. When `refresh: true`, archive the prior contents into `<output_dir>/.archive-<timestamp>/` before starting fresh. See `references/failure-modes.md`.

Callers embedding artifact-analysis in a concept-folder convention (e.g. `prfaq-beagle`) pass `output_dir` explicitly so the analysis sits next to its consumer: `.beagle/concepts/<concept-slug>/analysis/`.

## The scan plan (`plan.md`)

The plan is written before any subagent runs. It is the audit trail, not a review gate — the skill does not pause for user confirmation.

`plan.md` contains:

- **Intent** — the input string, verbatim, or `"generic salient extraction"` when intent is absent.
- **Resolved paths** — every path that will actually be scanned, with a note next to any entry that came from auto-discovery vs. caller-specified.
- **Slices** — how the resolved paths are partitioned across 1-3 subagents. Slices are non-overlapping.
- **Per-slice briefs** — one paragraph per slice summarizing what that subagent is told to extract. Derived mechanically from the spec so a reader of `plan.md` can predict what each subagent was told.
- **Skip patterns** — the denylist applied to this run (see `references/skip-patterns.md`).
- **Budgets applied** — subagent count for this run (1-3) and the skim threshold in effect (see Budget defaults below).
- **Synthesis approach** — how the per-slice findings will combine into `report.md`.

Report: `Wrote plan.md` and proceed to dispatch. No pause, no gate.

## Subagent dispatch

Up to 3 subagents run concurrently over non-overlapping slices. Each gets a mechanically-derived brief built from `plan.md` — no interpretation drift between the plan and the briefs. The brief template lives in `references/subagent-brief.md`.

Each subagent:

- Scans its assigned slice of paths, honoring skim strategies (sharded-doc: read index first; large-doc: TOC/headings first) and skip patterns.
- Writes `findings/<slice-slug>.md` under `output_dir`.
- Returns one terse status line to the orchestrator (path + status), never inline findings.

The orchestrator waits for all subagents to finish, then verifies every expected findings file exists before synthesis. A missing file is a silent failure, recorded in `Gaps & Limitations` — see `references/failure-modes.md`.

### Skim strategies

Subagents do not read everything end-to-end. They apply:

- **Sharded documents** (folder with `index.md` plus multiple sub-files) — read `index.md` first, then only the sub-files the index points to as relevant.
- **Large documents** (single file > ~50 pages or > ~2000 lines) — read the TOC, executive summary, and section headings first; pull full content only from sections relevant to the intent (or structurally important when intent is absent). The findings file records which sections were skimmed vs. read fully.
- **Short documents** (single file, moderate size) — read end-to-end.

### Skip patterns

Sensitive, binary, and vendor/build paths are skipped silently without the caller re-specifying them. The default denylist lives in `references/skip-patterns.md`. Each subagent records the paths it skipped under the `paths_skipped` frontmatter field so the audit trail shows exactly what was excluded.

## Citations

Every claim in a findings file and in `report.md` carries a citation. The shape lives in `references/citation-schema.md`. At a glance:

- **Required fields:** `path` (relative to the scanned root when possible), `excerpt` (a verbatim quoted string from the document).
- **Optional fields:** `lines` (line range or single line, only when the subagent naturally has them — never synthesized), `heading` (the nearest enclosing heading), `document_type`.

Inline references use `[^n]` footnotes; the full citation sits in the numbered `Sources` section at the bottom of the report.

## Synthesis (`report.md`)

The report has a fixed seven-section layout, in this order. Every section is required, every time — even when a section is thin, the report includes a bullet saying so.

1. `## Documents Found` — each included path with a one-line note on its relevance.
2. `## Key Insights` — the highest-signal observations from the corpus, grouped by theme.
3. `## User / Market Context` — users, customers, competition, market data surfaced from the documents.
4. `## Technical Context` — platforms, constraints, integrations, dependencies.
5. `## Ideas & Decisions` — each tagged `accepted`, `rejected`, or `open` with rationale. Rejected ideas are preserved deliberately so future work does not re-propose them.
6. `## Raw Detail Worth Preserving` — specific quotes, data points, metrics, and other detail that would be lost to summarization.
7. `## Gaps & Limitations` — what the corpus could not establish; which paths were empty, skipped, or unreadable; which subagents failed.

`Gaps & Limitations` is required even when the scan looks complete. Honest accounting of what was and was not in the corpus is part of the product. The full literal skeleton the skill copies from lives in `references/report-template.md`.

## Failure modes

- **Partial success** — one or more subagents fail. The skill continues with what succeeded and enumerates each failed slice under `Gaps & Limitations`, including the last-known brief and the stub-file reason.
- **Empty corpus** — path resolution (auto-discovery + explicit paths) yields zero readable documents. The skill writes `plan.md` and a minimal `report.md` with a single "no documents found" bullet under `Gaps & Limitations`, does not spawn subagents, and returns cleanly to the caller. Callers decide how to proceed.
- **Silent-failure detection** — every subagent writes at least a stub `findings/<slice-slug>.md` with `status:` frontmatter (`ok`, `empty`, `failed`) before returning. Missing file after dispatch = silent failure, recorded in `Gaps & Limitations`.
- **Re-run protection** — covered under "Output location" above; details in `references/failure-modes.md`.

Unlike `web-research`, artifact-analysis does **not** fail-fast on missing tools. Filesystem tooling (Read, Glob, Grep) is assumed present in the Claude Code environment. If it is somehow absent, the skill will surface that as a subagent failure under partial-success rather than aborting the whole run.

Full rules and the structured error shape live in `references/failure-modes.md`.

## Budget defaults

Tunable knobs, not hard-coded invariants:

| Knob                    | Default        |
| ----------------------- | -------------- |
| Parallel subagents      | 1-3            |
| Slice overlap           | none (enforced) |
| Skim threshold (large)  | > ~2000 lines or > ~50 pages |

A caller that needs narrower or broader scope overrides by passing a more specific `paths` list — one path per subagent forces narrower slicing; a single folder lets the skill partition internally.

## Companion invocation contract

Other beagle skills invoke this one via a small, documented contract. The minimal call passes only `intent`; the full call adds `paths`, `output_dir`, and `refresh`.

Worked examples for the three known callers (`prfaq-beagle`, `brainstorm-beagle`, `strategy-interview`) plus the success and refusal return shapes live in `references/companion-contract.md`. Callers are expected to honor the contract verbatim rather than invent parallel invocation styles.

## Tone

This skill is a tone-neutral primitive. It does not:

- Coach the caller on which documents matter.
- Adjudicate document quality or claim credibility (that is `llm-judge`'s job).
- Reshape the caller's intent into a different question.
- Adopt a posture (hardcore, Socratic, warm) — that is the caller's job.
- Editorialize in findings or the report.

If the caller is a coaching skill (`prfaq-beagle`, `brainstorm-beagle`), the coaching happens before and after this skill runs. Inside this skill, the intent is treated as final.

## Out of scope

- Scanning paywalled or authentication-gated remote sources. Use the file tools to extract content first, then pass paths in.
- LLM-as-judge evaluation of document quality or claim credibility. Use `llm-judge`.
- Coaching, challenge, or opinionated reshaping of the intent.
- Rewriting or editing the scanned documents. Read-only by design.
- Binary / image OCR, PDF text extraction, or format conversion. First version reads plain text and markdown only; `beagle-core:docling` is the future path.
- Multi-language analysis. English-only today.
- Caching or re-use of prior findings across invocations.
- Long-running or scheduled scans.

## Reference files

- `references/subagent-brief.md` — template the orchestrator mechanically fills from `plan.md` when dispatching each subagent.
- `references/citation-schema.md` — required and optional citation fields, footnote convention, and a well-formed example.
- `references/report-template.md` — literal `report.md` skeleton with all seven fixed sections.
- `references/failure-modes.md` — partial-success, empty-corpus, silent-failure detection, and re-run protection rules.
- `references/companion-contract.md` — programmatic invocation shape with worked examples for `prfaq-beagle`, `brainstorm-beagle`, and `strategy-interview`.
- `references/skip-patterns.md` — default denylist (sensitive, binary/media, vendor/build) applied to every run.
