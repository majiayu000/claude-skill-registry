---
name: web-research
description: "Use when the user wants web research: gathering cited, multi-angle evidence on a specific question. Triggers on: \"research X for me\", \"do web research on\", \"look up sources for\", \"find citations for\", \"gather evidence on\", \"what does the web say about X\". Also invoked programmatically by other beagle skills (prfaq-beagle Ignition, brainstorm-beagle reference points, strategy-interview context grounding) via the companion contract. Does NOT trigger on codebase lookups (\"find this function\", \"search the repo\"), local file search, LLM-as-judge evaluation, or paywalled/auth-gated scraping. Produces a written plan, parallel-subagent findings, and a cited synthesis report on disk — never inline prose, never unsourced claims."
---

# Web Research

Turn a sharp research question into cited, gap-flagged findings by delegating to parallel web-search subagents.

The deliverable is always on disk: a written plan the caller can review, one findings file per subtopic, and a synthesized report with numbered citations. Nothing returns as inline prose, and no claim ships without a URL + title + verbatim excerpt behind it.

## When to use

- A user asks for web research on a topic — "research X", "look up sources for Y", "gather evidence on Z".
- Another beagle skill invokes this one programmatically as a research companion (see `references/companion-contract.md`).
- The caller wants auditable output: a plan the user approved, findings files per subtopic, and a citation-backed synthesis.

## When NOT to use

- Codebase lookups ("where is this function defined", "search the repo"). Use Grep/Glob.
- Local file search or document extraction. Use the file tools or `artifact-analysis`.
- Comparative evaluation of two implementations. Use `llm-judge`.
- Paywalled or authentication-gated scraping. Out of scope — ask the caller to paste extracted content instead.
- Reshaping or coaching the research question. That is the caller's job; this skill treats the incoming question as final.

## Workflow

Four steps, in order. No step is skippable.

1. **Write `plan.md`** — main question verbatim, 1-5 non-overlapping subtopics, what each subtopic should establish, and how the findings will be synthesized.
2. **Plan review gate** — show the plan to the user for confirmation. Skipped only when the caller passes `auto_proceed: true`.
3. **Dispatch subagents and synthesize** — spawn up to 3 concurrent subagents (one per subtopic), wait for all to return, then write `report.md`.
4. **Verify before returning** — run the verification checklist in `references/failure-modes.md` to confirm all expected artifacts exist and are well-formed. Any check that fails becomes an entry in `Gaps & Limitations`.

### Hard gates (objective pass conditions)

Advance only when the prior gate **passes**. A pass is always evidenced by a file on disk, a caller flag, or a structured error — not an internal “I checked.”

| Gate | Blocks | Pass condition |
| --- | --- | --- |
| **G0 — Tools** | Slug derivation, `output_dir`, any write | `WebSearch` (or equivalent) is available. On fail: emit JSON per `references/failure-modes.md` (“Fail-fast on missing web tools”); **do not** create `plan.md` or any other artifact. |
| **G1 — Re-run** | First write under `output_dir` | `output_dir` has no `plan.md` or `report.md`, **or** `refresh: true` with prior contents archived per “Re-run protection” in `references/failure-modes.md`. |
| **G2 — Plan artifact** | Subagent dispatch | `plan.md` exists and includes every required bullet under “The research plan (`plan.md`)”. |
| **G3 — Review** | Dispatch | User has confirmed the plan **or** `auto_proceed: true`. |
| **G4 — Findings set** | Synthesis | For each subtopic in `plan.md`, `findings/<slug>.md` exists and has `status:` frontmatter (stub allowed). |
| **G5 — Deliverable** | Success return to caller | `report.md` exists; end-of-run checklist in `references/failure-modes.md` (“Verification checklist”) is satisfied **or** each failed check is recorded under `Gaps & Limitations`. |

```
Receive question ──→ Write plan.md ──→ Review gate (unless auto_proceed)
                                      ↓
                                    User confirms
                                      ↓
                                    Dispatch subagents (up to 3 parallel)
                                      ↓
                                    Collect findings/<slug>.md files
                                      ↓
                                    Synthesize report.md
                                      ↓
                                    Return paths to caller
```

Before step 1, verify the environment has `WebSearch` (or equivalent). `WebFetch` is desirable for subagents that need full-page content beyond search snippets, but not required — `WebSearch`-only environments can still produce useful findings. If `WebSearch` is absent, fail fast per `references/failure-modes.md` — do not create `plan.md`, do not spawn subagents.

## Inputs

The input contract is small and strict:

| Field               | Type              | Required | Default | Purpose                                                              |
| ------------------- | ----------------- | -------- | ------- | -------------------------------------------------------------------- |
| `research_question` | string            | yes      | —       | The question to answer, already distilled. The skill does not reshape it. |
| `output_dir`        | absolute path     | no       | derived | Where plan.md, findings/, and report.md land.                        |
| `auto_proceed`      | bool              | no       | `false` | When true, skip the plan review gate and dispatch immediately.       |
| `refresh`           | bool              | no       | `false` | When true, allow overwriting a prior run in the same `output_dir`.   |

The skill does not parse caller-specific structures. Callers distill their brief into one sharp question string before invoking.

**When to pass `auto_proceed: true` vs `false`.** Pass `false` (the default) when the user will still benefit from seeing the subtopic plan before searches burn — e.g. the caller wants this skill's plan-review gate to serve as that check. Pass `true` when the caller has already satisfied the "is this the right framing" question through its own interaction with the user, and another gate would just be friction — e.g. the user explicitly asked mid-conversation for background research, or the caller runs its own review loop upstream. The rule is about where the review happens, not whether it happens.

## Output location

If the caller provides `output_dir`, use it verbatim. Otherwise derive the default:

```
.beagle/research/<YYYY-MM-DD>-<topic-kebab>/
```

**Slug derivation** (stable so re-running the same question on the same day lands on the same folder):

1. Take the research question.
2. Lowercase.
3. Strip punctuation (keep letters, digits, spaces, hyphens).
4. Collapse runs of whitespace to single hyphens.
5. Truncate to 60 characters on a word boundary (cut at the last hyphen before 60). If there is no hyphen before position 60, hard-cut at 60.
6. Prepend `YYYY-MM-DD-`.

**Re-run protection.** Before writing anything, check whether `output_dir` already contains `plan.md` or `report.md`. If it does and `refresh` is not `true`, refuse with a message naming the existing folder. When `refresh: true`, archive the prior contents into `<output_dir>/.archive-<timestamp>/` first, then start fresh. See `references/failure-modes.md` and `references/companion-contract.md`.

Every run lands in its own folder so callers weeks later can re-read the plan, findings, and report without re-running the skill.

## The research plan (`plan.md`)

The plan is written before any subagents run and is the caller's chance to catch bad framing before searches burn.

`plan.md` contains:

- **Research question** — the input string, verbatim.
- **Subtopics** — 1 to 5, non-overlapping, each with a one-line name.
- **What each subtopic should establish** — concrete bullets, not "research everything about X".
- **Synthesis approach** — how the subtopics' findings will combine into `report.md`.
- **Budget** — how many subagents will spawn and how many searches each has (see Budget defaults below).

**Plan review gate.** By default, show `plan.md` to the user and wait for confirmation before dispatching. The user can revise subtopics, add or remove them, or reject the framing entirely. When the caller passes `auto_proceed: true`, skip the gate and dispatch immediately — this is the programmatic-companion path where the caller has its own review loop.

## Subagent dispatch

Up to 3 subagents run concurrently. Each gets a mechanically-derived brief built from `plan.md` — no interpretation drift between the plan the user approved and the briefs the subagents received. The brief template lives in `references/subagent-brief.md`.

Each subagent:

- Runs its budgeted web searches (3-5 by default).
- Writes `findings/<subtopic-slug>.md` under `output_dir`.
- Returns one terse status line to the orchestrator (path + status), never inline findings.

The orchestrator waits for all subagents to finish, then verifies every expected findings file exists before moving to synthesis. A missing file is a silent failure, recorded in `Gaps & Limitations` — see `references/failure-modes.md`.

See `references/subagent-brief.md` for the full brief shape and the required frontmatter on each findings file.

## Citations

Every claim in a findings file and in `report.md` carries a citation. The shape is documented in `references/citation-schema.md`. At a glance:

- **Required fields:** `url`, `title`, `excerpt` (verbatim quote from the page).
- **Optional fields:** `retrieved_at` (ISO date), `source_type` (official-docs / vendor / blog / forum / news / other).
- **Never synthesize missing metadata.** If the subagent does not have a retrieval date, omit the field — do not fabricate one.

Inline references use `[^n]` footnotes; the full citation sits in the numbered `Sources` section at the bottom of the report.

## Synthesis (`report.md`)

The report has a fixed four-section layout, in this order. Every section is required, every time.

1. `## TL;DR` — 3-5 bullets capturing the highest-signal findings.
2. `## Findings` — organized by subtopic or theme; every claim carries a `[^n]` footnote.
3. `## Gaps & Limitations` — what the research could not establish, including any failed subagents.
4. `## Sources` — numbered bibliography matching footnote numbers.

`Gaps & Limitations` is required even when findings look complete. Honest accounting of what was and was not verifiable is part of the product. The full literal skeleton the skill copies from lives in `references/report-template.md`.

## Failure modes

- **Partial success** — one or more subagents fail. The skill continues with what succeeded and enumerates each failed subtopic under `Gaps & Limitations`, including the last-known brief and the stub-file reason. The run does not abort.
- **Fail-fast** — `WebSearch` (or equivalent) unavailable. Abort before any disk write (including `plan.md`); return structured JSON per `references/failure-modes.md`. `WebFetch` is optional for subagents and is **not** part of this gate.
- **Silent-failure detection** — every subagent writes at least a stub `findings/<slug>.md` with `status:` frontmatter (`ok`, `empty`, `failed`) before returning. Missing file after dispatch = silent failure, recorded in `Gaps & Limitations`.
- **Re-run protection** — covered under "Output location" above; details in `references/failure-modes.md`.

Full rules and the structured error shape live in `references/failure-modes.md`.

## Budget defaults

Tunable knobs, not hard-coded invariants:

| Knob                              | Default |
| --------------------------------- | ------- |
| Subtopics per run                 | 1-5     |
| Parallel subagents                | up to 3 |
| Web searches per subagent         | 3-5     |

A caller that needs broader or narrower scope can override via the brief. The plan-review gate is the right place to adjust before searches burn.

## Companion invocation contract

Other beagle skills invoke this one via a small, documented contract. The minimal call passes only `research_question`; the full call adds `output_dir`, `auto_proceed`, and `refresh`.

Worked examples for the three known callers (`prfaq-beagle`, `brainstorm-beagle`, `strategy-interview`) plus the success and fail-fast return shapes live in `references/companion-contract.md`. Callers are expected to honor the contract verbatim rather than invent parallel invocation styles.

## Tone

This skill is a tone-neutral primitive. It does not:

- Coach the caller on whether the question is the right one.
- Reshape, sharpen, or challenge the research question.
- Adopt a posture (hardcore, Socratic, warm) — that is the caller's job.
- Editorialize in findings or the report.

If the caller is a coaching skill (`prfaq-beagle`, `brainstorm-beagle`), the coaching happens before and after this skill runs. Inside this skill, the question is treated as final.

## Out of scope

- Long-running or scheduled research jobs.
- LLM-as-judge evaluation of source credibility — `llm-judge` already covers comparative evaluation.
- Scraping paywalled or authentication-gated sources.
- Coaching, challenge, or opinionated reshaping of the research question.
- Multi-language research.
- Caching or de-duplication of findings across invocations.
- Non-web research modes (local files, project docs, databases) — use `artifact-analysis`.

## Reference files

- `references/subagent-brief.md` — template the orchestrator mechanically fills from `plan.md` when dispatching each subagent.
- `references/citation-schema.md` — required and optional citation fields, footnote convention, and a well-formed example.
- `references/report-template.md` — literal `report.md` skeleton with all four fixed sections.
- `references/failure-modes.md` — partial-success, fail-fast, silent-failure detection, and re-run protection rules.
- `references/companion-contract.md` — programmatic invocation shape with worked examples for `prfaq-beagle`, `brainstorm-beagle`, and `strategy-interview`.
