---
name: deliverable-lint
description: Reviews a whole deliverable, such as a talk, course module, paper, chapter, or referee report, against its manifest without rewriting. Runs a deterministic gate for build, citations, numbers, facts, and leaks, then stops on failure. It assigns a cheap finder to each section, runs a strong-model whole-work pass, and adjudicates into checks/<date>/findings.json and report.md with anchors, severities, and honest NOT-CHECKED coverage within a dollar budget. Use when the user says "lint the deliverable", "review the whole talk/module/paper", "night shift", "pre-ship review", or before release. Revision remains serial and author-led.
argument-hint: '[--budget USD (default 3) --headless --sections a,b --skip-fast --continue]'
---

# Deliverable lint

Detection is parallel; revision is serial. This skill finds; it never edits a source file, never edits the wiki, and never runs a rewrite. The author (or `sci-edit`, one section at a time under its guard) does the revising afterwards.

## Stage 0 and 1: prepare the run (shared script)

- The nearest `deliverable.yml` upward from cwd. Refuse to run without one; point at `deliverable-open`.
- `python3 $HYG/lint_prepare.py --root <dir> --budget <usd> --mode manual|headless [--sections a,b] [--skip-fast]` where `$HYG` is `~/Documents/GitHub/resources/project_hygiene/scripts`. It reserves `checks/YYYY-MM-DD[-N]/` (never reuses a directory), runs the fast gate into `<run>/fast.json` (`--build` unless headless; `--skip-fast` records a skipped gate, which can never become "passed"), freezes the input hash and start time in `<run>/inputs/run.json`, writes `<run>/inputs/index.json` with every manifest section and an absolute output path per section, and one `<run>/inputs/section-<id>.md` per selected section containing everything a finder needs: the manifest's audience, claim, and done-test; the planning index and brief; the gate's citation status for its lines; the voice rules (resolved from the installed `sci-edit` skill or the writing-toolkit clone, NOT CHECKED if absent); the neighbours; the line-numbered section text; speaker notes for a deck; the knowledge-base source paths when the manifest names one; the kind profile's lint questions (`project_hygiene/kinds/<kind>.md`); and the exact JSON output contract.
- Read `<run>/fast.json`. Every FAIL becomes a P0 verbatim. If anything failed, run the adjudicator now and stop: an LLM review of a deliverable that does not build or cites a source nobody can find is spend without a return. `--continue` overrides.

## Stage 2: section finders, in parallel

One worker per selected section, all launched together and all awaited before stage 3 (Claude: `Agent` calls in one message, `model: "sonnet"`; Codex: bounded child workers, queued to the slot limit). Each worker gets one instruction: read its `inputs/section-<id>.md` and write the single JSON object the file specifies to the path the file names. The file carries the three questions (clarity and voice; claim-to-source; consistency) and, when the manifest names a `knowledge_base`, a fourth (support: does the cited source's Markdown say it; contradicted = P0 with the passage as verification). A worker sets a coverage value to `false` for any question it could not answer; the adjudicator counts a section as checked only when every required dimension is `true`. A worker that returns prose instead of the object is rerun once, then its section is NOT CHECKED.

## Stage 3: the global pass

One worker at the strongest model the session can spawn (Claude: `model: "opus"`, asked to think at high effort; Codex: the exposed spawn configuration with a fresh or limited-history fork), over the assembled deliverable in section order with the same argument map. Four questions: order and flow (does the sequence carry the claim; where does a section assume what a later one establishes; for a talk, do the timings fit the slot); spec conformance (is the manifest's claim made, is the done-test met, is the register right for the audience); repetition and contradiction across sections; release rules. It writes one JSON object `{"coverage": {"order":..,"spec":..,"repetition":..,"release":..}, "findings": [...]}` to `<run>/finders/global.json` with the same finding fields; a section-local defect it notices goes in as `dimension: global-local`.

## Stage 4: adjudicate

`python3 $HYG/lint_adjudicate.py --root <dir> --run <run> --models finders=<model>,global=<model>,adjudicator=<this session's actual model>` does the mechanical part identically for both vendors: verifies every anchor (file, line, verbatim quote; unanchored findings are dropped and counted), dedupes across dimensions, downgrades a claim-source P0 with no gate failure at that file and line and a support or consistency P0 with no verification passage, keeps the frozen start hash and marks the run stale if the inputs changed, records coverage honestly, and derives the verdict from all four conditions: fast gate passed, every section and the global pass checked, not stale, zero open P0. Then you read `report.md` as the domain expert: a disputed P0 needs an independent evidence check (a second lookup, a source passage; on Claude the `orchestrate` skill's `codex-peer.sh --mode cross-check` is one such check when installed); without one it stays disputed and blocking. Two models agreeing is not evidence, and a failed lookup means unresolved, never fabricated.

## Budget

`--budget` is in US dollars, default 3; the per-section figures are planning allowances (0.10 per section, 1.00 for the global pass, 0.50 for adjudication), not prices, and a subscription session cannot enforce a hard cap. Before stage 2, if the allowance exceeds the budget, drop finders from the end of the section list and mark those sections NOT CHECKED; if the global pass alone exceeds it, stop after the gate and record every section and the global pass as NOT CHECKED. `meta.cost.reported_usd` is the harness's metered figure when one exists and `null` otherwise, never a guess.

## Outputs

`<run>/findings.json` (`meta` with the frozen and current hashes, `stale`, models, cost, and a `verdict` block; `coverage` with the fast-gate state, whether the build was checked, every section's status and reason, the global pass, and the unanchored count; `findings` ranked P0/P1/P2 with `id`, `severity`, `dimension`, `rule`, `file`, `section`, `line`, `end_line`, `quote`, `finding`, `action`, `verification`, `disposition`, `source`) and `<run>/report.md` (verdict in the first line, the summary block, findings grouped by severity with `file:line`, the NOT CHECKED list, one paragraph for the author). Shipping needs the verdict's four conditions; `check_deliverable.py ship` refuses otherwise unless `--no-lint` waives the review and the receipt records the waiver.

## Headless

`--headless` (what `night-shift.py` passes): no questions, no edits outside `checks/`; `lint_prepare.py --mode headless` runs the gate without `--build` and records the build as NOT CHECKED (shipping still builds); write both files, print the report's first ten lines, exit. If the fast gate fails, that is still a complete run.

## Notes

- Never put the whole deliverable into one rewrite prompt; this skill does not rewrite at all. `sci-edit manuscript` is the serial, guarded path for the fix.
- `paper-review-lite` fans out over review dimensions and `presubmit` runs the adversarial pipeline; both are for a manuscript at a submission milestone. This skill is the cheaper, section-anchored pass for any deliverable at any milestone, and it feeds them: run it first.
- The author reacts by dictating into `inbox/` and running `deliverable-intake`; accepted findings become tasks, rejected ones go under `Rejected findings` in the declared wiki's `08-open-questions.md` so they are not raised again.

## Codex notes

Run the section workers as bounded children queued to the slot limit, await all, then the global worker, then the shared adjudicator; without delegation, run the same workers sequentially and say so in coverage. Record observed model identities in `--models`; never relabel a Codex model as Sonnet or Opus. The voice rules resolve from `~/.agents/skills/sci-edit/voice.md` or the writing-toolkit clone; `lint_prepare.py` marks them NOT CHECKED if absent. A disputed P0 needs an independent evidence check available in this runtime (a second lookup, a source passage); `codex-peer.sh` is a Claude-side helper and is not assumed here.
