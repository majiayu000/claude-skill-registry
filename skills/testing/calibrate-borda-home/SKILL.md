---
name: calibrate
description: Calibration testing for agents and skills. Generates synthetic problems with known outcomes (quasi-ground-truth), runs targets against them, and measures recall, precision, and confidence calibration — revealing whether self-reported confidence scores track actual quality.
argument-hint: '{all|agents|skills|routing|<name>} [fast|full] [ab] [apply]'
allowed-tools: Read, Write, Edit, Bash, Agent, TaskCreate, TaskUpdate
---

<objective>

Validate agents and skills by measuring their outputs against synthetic problems with defined ground truth. The primary signal is **calibration bias** — the gap between self-reported confidence and actual recall. A well-calibrated agent reports 0.9 confidence when it genuinely finds ~90% of issues. A miscalibrated one may report 0.9 while only finding 60%.

Calibration data drives the improvement loop: systematic gaps become instruction updates; persistent overconfidence adjusts effective re-run thresholds stored in MEMORY.md.

</objective>

<inputs>

- **$ARGUMENTS**: `{all|agents|skills|<name>} [fast|full] [ab] [apply]`

  - **Target** (first token — defaults to `all`):
    - `all` — all agents + all calibratable skills (`/audit`, `/review`)
    - `agents` — all agents only
    - `skills` — calibratable skills only (`/audit`, `/review`)
    - `routing` — routing accuracy test: measures how accurately a `general-purpose` orchestrator selects the correct `subagent_type` for synthetic task prompts (not a per-agent quality benchmark; not included in `all`, `agents`, or `skills` — invoke explicitly)
    - `<agent-name>` — single agent (e.g., `sw-engineer`)
    - `/audit` or `/review` — single skill
  - **Pace** (optional, default `fast`):
    - `fast` — 3 problems per target
    - `full` — 10 problems per target
  - **`ab`** (optional): also run a `general-purpose` baseline and report delta metrics
  - **`apply`** (optional):
    - With `fast` or `full`: run the calibration benchmark then immediately apply the new proposals at the end
    - Without `fast`/`full`: skip benchmark; apply proposals from the most recent past run

  Every invocation surfaces a report: benchmark runs print the new results; bare `apply` prints the saved report from the last run before applying any changes.

</inputs>

<constants>

- FAST_N: 3 problems per target
- FULL_N: 10 problems per target
- RECALL_THRESHOLD: 0.70 (below → agent needs instruction improvement)
- CALIBRATION_BORDERLINE: ±0.10 (|bias| within this → calibrated; between 0.10 and 0.15 → borderline)
- CALIBRATION_WARN: ±0.15 (bias beyond this → confidence decoupled from quality)
- CALIBRATE_LOG: `.claude/logs/calibrations.jsonl`
- AB_ADVANTAGE_THRESHOLD: 0.10 (delta recall or F1 above this → meaningful advantage; below → marginal or none)
- PHASE_TIMEOUT_MIN: 5 (per-phase budget — if spawned subagents haven't all returned, collect partial results and continue)
- PIPELINE_TIMEOUT_MIN: 10 (hard cutoff — pipeline not notified within 10 min of launch is timed out; extendable if the agent explains the delay)
- HEALTH_CHECK_INTERVAL_MIN: 5 (orchestrator polls each running pipeline every 5 min for liveness)
- EXTENSION_MIN: 5
- ROUTING_ACCURACY_THRESHOLD: 0.90 (below → agent descriptions need improvement)
- ROUTING_HARD_THRESHOLD: 0.80 (below → high-overlap pair descriptions need disambiguation)

Problem domain by agent:

- `sw-engineer` → Python bugs: type errors, logic errors, anti-patterns, bare `except:`, mutable defaults
- `qa-specialist` → coverage gaps: uncovered edge cases, missing exception tests, Machine Learning (ML) non-determinism
- `linting-expert` → violations: ruff rules, mypy errors, annotation gaps
- `self-mentor` → config issues: broken cross-refs, missing workflow blocks, wrong model, step gaps
- `doc-scribe` → docs gaps: missing docstrings, missing Google style sections, broken examples
- `perf-optimizer` → perf issues: unnecessary loops, repeated computation, wrong dtype, missing vectorisation
- `ci-guardian` → Continuous Integration (CI) issues: non-pinned action Secure Hash Algorithms (SHAs), missing cache, inefficient matrix
- `data-steward` → data issues: label leakage, split contamination, augmentation order bugs
- `ai-researcher` → paper analysis: missed contributions, wrong method attribution
- `solution-architect` → design issues: leaky abstractions, circular dependencies, missing Architecture Decision Record (ADR), backward-compat violations without deprecation path
- `web-explorer` → content quality: broken or unverified Uniform Resource Locators (URLs), outdated docs, incomplete extraction from fetched pages
- `oss-maintainer` → Open Source Software (OSS) governance: incorrect Semantic Versioning (SemVer) decision, missing CHANGELOG entry, bad deprecation path, wrong release checklist item

Skill domains:

- `/audit` → synthetic `.claude/` config with N injected structural issues
- `/review` → synthetic Python module with N cross-domain issues (arch + tests + docs + lint)

</constants>

<workflow>

**Task tracking**: create tasks at the start of execution (Step 1) for each phase that will run:

- "Calibrate agents" — Step 2 (benchmark mode, when target includes agents)
- "Calibrate skills" — Step 2 Skills sub-section (benchmark mode, when target includes skills)
- "Calibrate routing" — Step 2 Routing sub-section (benchmark mode, when target is `routing`)
- "Analyse and report" — Steps 3–5 (benchmark mode)
- "Apply findings" — Step 6 (apply mode only)
  Mark each in_progress when starting, completed when done. On loop retry or scope change, create a new task.

## Step 1: Parse targets and create run directory

From `$ARGUMENTS`, determine:

- **Target list** — parse the first token:
  - `all` or omitted → all agents + `/audit` + `/review`
  - `agents` → all agents only (the full agent list in the constants block)
  - `skills` → `/audit` and `/review` only
  - `routing` → routing accuracy test (NOT included in `all`, `agents`, or `skills` — invoke explicitly)
  - Any other token → single agent or skill name
- **Mode**: look for `fast` or `full` in remaining tokens — default `fast`
- **A/B flag**: `ab` present → also spawn a `general-purpose` baseline per problem
- **Apply flag**:
  - `apply` without `fast`/`full` → pure apply mode: skip Steps 2–5; go directly to Step 6
  - `apply` with `fast`/`full` → benchmark + auto-apply: run Steps 2–5 then continue to Step 6

If benchmark will run (i.e., `fast` or `full` is present, with or without `apply`): generate timestamp `YYYYMMDDTHHMMSSZ` (Coordinated Universal Time (UTC), e.g. `20260303T134448Z`). All run dirs use this timestamp.

Create tasks before proceeding:

- Benchmark only (no `apply`): TaskCreate "Calibrate agents" (if target includes agents), TaskCreate "Calibrate skills" (if target includes skills), TaskCreate "Calibrate routing" (if target is `routing`), TaskCreate "Analyse and report"
- Benchmark + auto-apply (`fast`/`full` + `apply`): TaskCreate "Calibrate agents" (if target includes agents), TaskCreate "Calibrate skills" (if target includes skills), TaskCreate "Calibrate routing" (if target is `routing`), TaskCreate "Analyse and report", TaskCreate "Apply findings"
- Pure apply mode (only `apply`, no `fast`/`full`): TaskCreate "Apply findings" only

## Step 2: Spawn pipeline subagents

Mark "Calibrate agents" in_progress. Issue all agent pipeline subagent spawns.

### Skills

Mark "Calibrate skills" in_progress. Issue all skill pipeline subagent spawns.

### Routing

When target is `routing` (skip agent/skill spawns above and the section below for this target): Mark "Calibrate routing" in_progress. Read `.claude/skills/calibrate/templates/routing-pipeline-prompt.md`. Substitute `<N>` (5 for fast, 10 for full), `<TIMESTAMP>`, `<MODE>`. Spawn a **single** `general-purpose` pipeline subagent with the substituted template as its prompt — it handles all phases internally. Proceed to Step 3 after spawning.

Issue all subagents from both agents and skills in a **single response** — agents and skills are independent and run concurrently. One `general-purpose` subagent per target; do not wait for one to finish before spawning the next.

Each subagent receives this self-contained prompt (substitute `<TARGET>`, `<DOMAIN>`, `<N>`, `<TIMESTAMP>`, `<MODE>`, `<AB_MODE>` before spawning — set `<AB_MODE>` to `true` or `false`):

______________________________________________________________________

Read the pipeline prompt template from .claude/skills/calibrate/templates/pipeline-prompt.md and use it as the self-contained prompt for each subagent. Before spawning, substitute these variables in the template: <TARGET>, <DOMAIN>, <N>, <TIMESTAMP>, <MODE>, \<AB_MODE>.

______________________________________________________________________

## Step 3: Collect results and print combined report

**Health monitoring** — apply the protocol from CLAUDE.md §8 (Background Agent Health Monitoring). Run dir for liveness checks: `.claude/calibrate/runs/<TIMESTAMP>/<TARGET>/`. Constants below tighten the global defaults for this skill:

```bash
# Initialise checkpoints after all pipeline spawns
LAUNCH_AT=$(date +%s)
for TARGET in <target-list>; do touch /tmp/calibrate-check-$TARGET; done

# Every HEALTH_CHECK_INTERVAL_MIN (5 min): check each still-running pipeline
NEW=$(find .claude/calibrate/runs/<TIMESTAMP>/$TARGET/ -newer /tmp/calibrate-check-$TARGET -type f 2>/dev/null | wc -l | tr -d ' ')
touch /tmp/calibrate-check-$TARGET
ELAPSED=$(( ($(date +%s) - LAUNCH_AT) / 60 ))
if [ "$NEW" -gt 0 ]; then
  echo "✓ $TARGET active"
elif [ "$ELAPSED" -ge 10 ]; then
  echo "⏱ $TARGET TIMED OUT (hard limit)"
elif [ "$ELAPSED" -ge 5 ]; then
  # One-time extension per CLAUDE.md §8: check output file for delay explanation
  OUTPUT_FILE=".claude/calibrate/runs/<TIMESTAMP>/$TARGET/pipeline.jsonl"
  if tail -20 "$OUTPUT_FILE" 2>/dev/null | grep -qi 'delay\|wait\|slow'; then
    echo "⏸ $TARGET: extension granted (+5 min)"
  else
    echo "⏱ $TARGET TIMED OUT"
  fi
fi
```

**On timeout**: read `tail -100 <output_file>` for partial JSON; if none use: `{"target":"<TARGET>","verdict":"timed_out","mean_recall":null,"gaps":["pipeline timed out at 10 min — re-run individually with /calibrate <target> fast"]}`. Timed-out targets appear in the report with ⏱ prefix and null metrics.

After all pipeline subagents have completed or timed out: mark "Calibrate agents" and "Calibrate skills" completed. Mark "Analyse and report" in_progress. Parse the compact JSON summary from each.

Print the combined benchmark report:

```
## Calibrate — <date> — <MODE>

| Target           | Recall | SevAcc | Fmt  | Confidence | Bias    | F1   | Scope | Verdict    | Top Gap              |
|------------------|--------|--------|------|------------|---------|------|-------|------------|----------------------|
| sw-engineer      | 0.83   | 0.91   | 0.87 | 0.85       | +0.02 ✓ | 0.81 | 0 ✓   | calibrated | async error paths    |
| ...              |        |        |      |            |         |      |       |            |                      |

*Recall: in-scope issues found / total. SevAcc: severity match rate for found issues (±1 tier) — high recall + low SevAcc = issues found but misprioritized. Fmt: fraction of found issues with location + severity + fix (actionability). Bias: confidence − recall (+ = overconfident). Scope: FP on out-of-scope input (0 ✓).*
```

**If AB mode**, add `ΔRecall`, `ΔSevAcc`, `ΔFmt`, `ΔTokens`, and `AB Verdict` columns after F1. ΔTokens = token_ratio − 1.0 (negative = specialist more concise).

```
| Target      | Recall | SevAcc | Fmt  | Bias    | F1   | ΔRecall | ΔSevAcc | ΔFmt  | ΔTokens | Scope | AB Verdict |
|-------------|--------|--------|------|---------|------|---------|---------|-------|---------|-------|------------|
| sw-engineer | 0.83   | 0.91   | 0.87 | +0.02 ✓ | 0.81 | +0.05 ~ | +0.12 ✓ | +0.15 ✓ | −0.18 ✓ | 0 ✓ | marginal ~ |

*ΔRecall/ΔSevAcc/ΔFmt: specialist − general (positive = specialist better). ΔTokens: token_ratio − 1.0 (negative = more focused). AB Verdict covers ΔRecall and ΔF1 only; use ΔSevAcc and ΔFmt as supplementary evidence for agents where ΔRecall ≈ 0.*
```

**If target is `routing`**, replace the table above with the routing-specific format:

```
## Routing Calibration — <date> — <MODE>

| Metric           | Value      | Status |
|------------------|------------|--------|
| Routing accuracy | N/M (XX%)  | ≥90% ✓ / 80–90% ~ / <80% ⚠ |
| Hard accuracy    | N/M (XX%)  | ≥80% ✓ / <80% ⚠ |
| Confusion errors | N          | 0 ✓ / >0 list pairs |
```

Flag routing accuracy < ROUTING_ACCURACY_THRESHOLD (0.90) or hard accuracy < ROUTING_HARD_THRESHOLD (0.80) with ⚠. Print confused pair details from the routing report's Confused Pairs section. Mark "Calibrate routing" completed.

Flag any target where recall < 0.70 or |bias| > 0.15 with ⚠.

After the table, print the full content of each `proposal.md` for targets where `proposed_changes > 0`.

If `apply` was **not** set, print:

```
→ Review proposals above, then run `/calibrate <targets> [fast|full] apply` to apply them.
→ Proposals saved to: .claude/calibrate/runs/<TIMESTAMP>/<TARGET>/proposal.md
```

If `apply` **was** set (benchmark + auto-apply mode), print `→ Auto-applying proposals now…` and proceed to Step 6.

Targets with verdict `calibrated` and no proposed changes get a single line: `✓ <target> — no instruction changes needed`.

## Step 4: Concatenate JSONL logs

Append each target's result line to `.claude/logs/calibrations.jsonl` (create dir if needed):

```bash
mkdir -p .claude/logs
cat .claude/calibrate/runs/<TIMESTAMP>/*/result.jsonl >> .claude/logs/calibrations.jsonl
```

## Step 5: Surface improvement signals

For each flagged target (recall < 0.70 or |bias| > 0.15):

- **Recall < 0.70**: `→ Update <target> <antipatterns_to_flag> for: <gaps from result>`
- **Bias > 0.15**: `→ Raise effective re-run threshold for <target> in MEMORY.md (default 0.70 → ~<mean_confidence>)`
- **Bias < −0.15**: `→ <target> is conservative; threshold can stay at default`

Proposals shown in Step 3 already surface the actionable signals. If `apply` was **not** set, end with:

`→ Run /calibrate <target> [fast|full] apply to run a fresh benchmark and apply proposals.`

Mark "Analyse and report" completed. If `apply` was set: proceed to Step 6.

## Step 6: Apply proposals (apply mode)

Mark "Apply findings" in_progress.

**Determine run directory**:

- Benchmark + auto-apply mode (`fast`/`full` + `apply`): use the TIMESTAMP already generated in Step 1 — proposals were just written by Steps 2–5.
- Pure apply mode (only `apply`, no `fast`/`full`): find the most recent run:

```bash
LATEST=$(ls -td .claude/calibrate/runs/*/ 2>/dev/null | head -1)
TIMESTAMP=$(basename "$LATEST")
```

For each target in the target list, check whether `.claude/calibrate/runs/<TIMESTAMP>/<target>/proposal.md` exists. Collect the set of targets that have a proposal (`found`) and those that don't (`missing`).

Print `⚠ No proposal found for <target> — run /calibrate <target> [fast|full] first` for each missing target.

**Print the run's report before applying**: for each found target, read and print `.claude/calibrate/runs/<TIMESTAMP>/<target>/report.md` verbatim so the user sees the benchmark basis before any file is changed.

**Spawn one `general-purpose` subagent per found target. Issue ALL spawns in a single response — no waiting between spawns.**

Each subagent receives this self-contained prompt (substitute `<TARGET>`, `<PROPOSAL_PATH>`, `<AGENT_FILE>`):

______________________________________________________________________

Read the proposal file at `<PROPOSAL_PATH>` and apply each "Change N" block to `<AGENT_FILE>` (or the skill file if the target is a skill).

For each change:

1. Print: `Applying Change N to <file> [<section>]`
2. Use the Edit tool — `old_string` = **Current** text verbatim, `new_string` = **Proposed** text
3. If **Current** is `"none"` (new insertion): find the section header and insert the **Proposed** text after the last item in that block
4. Skip if **Current** text is not found verbatim → print `⚠ Skipped — current text not found`
5. Skip if **Proposed** text is already present → print `✓ Already applied — skipped`

After processing all changes return **only** this compact JSON:

`{"target":"<TARGET>","applied":N,"skipped":N}`

______________________________________________________________________

After all subagents complete, collect their JSON results and print the final summary:

```
## Fix Apply — <date>

| Target      | File                          | Applied | Skipped |
|-------------|-------------------------------|---------|---------|
| sw-engineer | .claude/agents/sw-engineer.md | 2       | 0       |

→ Run /calibrate <targets> to verify improvement.
```

Mark "Apply findings" completed.

End your response with a `## Confidence` block per CLAUDE.md output standards.

</workflow>

<notes>

- **Timeout handling**: phase and pipeline budgets (see the constants block) prevent nested subagent hangs from cascading. Extension is granted once if the pipeline explains the delay in its output file — a second unexplained stall still triggers the cutoff. Timed-out pipelines appear with ⏱ prefix and `verdict:"timed_out"`; re-run individually with `/calibrate <target> fast` after the session.
- **Context safety**: each target runs in its own pipeline subagent — only a compact JSON (~200 bytes) returns to the main context. `all full ab` with 14 targets returns ~2.8KB total, well within limits.
- **Scorer delegation**: Phase 3 delegates scoring to per-problem `general-purpose` subagents. Each scorer reads response files from disk, returns ~200 bytes. The pipeline subagent holds only compact JSONs regardless of N or A/B mode — no context budget concern.
- **Nesting depth**: main → pipeline subagent → target/scorer agents (2 levels). Pipeline spawns both target agents (Phase 2) and scorer agents (Phase 3) at the same depth — no additional nesting.
- `general-purpose` is a Claude Code built-in agent type (no `.claude/agents/general-purpose.md` file needed) — it provides a baseline Claude instance with access to all tools but no custom system prompt.
- **Quasi-ground-truth limitation**: problems are generated by Claude — the same model family as the agents under test. A truly adversarial benchmark requires expert-authored problems. This benchmark reliably catches systematic blind spots and calibration drift even with this limitation.
- **Calibration bias is the key signal**: positive bias (overconfident) → raise the agent's effective re-run threshold in MEMORY.md. Negative bias (underconfident) → confidence is conservative, no action needed. Near-zero → confidence is trustworthy.
- **Do NOT use real project files**: benchmark only against synthetic inputs — no sensitive data and real files have no ground truth.
- **Skill benchmarks** run the skill as a subagent against synthetic config or code; scored identically to agent benchmarks.
- **Improvement loop**: systematic gaps → `<antipatterns_to_flag>` | consistent low recall → consider model tier upgrade (sonnet → opus) | large calibration bias → document adjusted threshold in MEMORY.md | re-calibrate after instruction changes to quantify improvement.
- **Report always**: every invocation surfaces a report — benchmark runs print the new results table; bare `apply` (no `fast`/`full`) prints the saved report from the last run before applying, so the user always sees the basis for any changes before files are touched.
- **`apply` semantics**: `fast apply` / `full apply` = run fresh benchmark then auto-apply the new proposals in one go. `apply` alone (no `fast`/`full`) = apply proposals from the most recent past run without re-running the benchmark.
- **Stale proposals**: `apply` uses verbatim text matching (`old_string` = **Current** from proposal). If the agent file was edited between the benchmark run and `apply`, any change whose **Current** text no longer matches is skipped with a warning — no silent clobbering of intermediate edits.
- **`routing` target vs `/audit` Check 12**: `/audit` Check 12 performs static analysis of description overlap (finds potential confusion zones); `/calibrate routing` tests behavioral impact — it generates real routing decisions and measures whether descriptions actually disambiguate. Run in sequence: `/audit` first (fast, structural), then `/calibrate routing` (behavioral, slower). They are complementary, not redundant.
- **`routing` not in `all`**: routing tests orchestrator dispatch logic, not agent quality — excluded from batch calibration. Run `/calibrate routing` explicitly after any agent description change.
- **Routing proposals**: the routing pipeline's Phase 5 writes description improvement proposals to `.claude/calibrate/runs/<TIMESTAMP>/routing/report.md` — look in the Proposals section for targeted wording suggestions per confused pair.
- Follow-up chains:
  - Recall < 0.70 or borderline → `/calibrate <agent> fast apply` → `/calibrate <agent>` to verify improvement — stop and escalate to user if recall is still < 0.70 after this cycle (max 1 apply cycle per run)
  - Calibration bias > 0.15 → add adjusted threshold to MEMORY.md → note in next audit
  - Routing accuracy < 0.90 or hard accuracy < 0.80 → update descriptions for confused pairs → `/calibrate routing` to verify improvement
  - Recommended cadence: run before and after any significant agent instruction change; run `/calibrate routing` after any agent description change
- **Internal Quality Loop suppressed during benchmarking**: the Phase 2 prompt explicitly tells target agents not to self-review before answering. This ensures calibration measures raw instruction quality — not the `(agent + loop)` composite. If the loop were enabled, it would inflate both recall and confidence by an unknown ratio, masking real instruction gaps and making it impossible to attribute improvement to instruction changes vs. the loop self-correcting at inference time.
- **Skill-creator complement**: `/calibrate` benchmarks agents and skills via synthetic ground-truth problems; the official `skill-creator` from the anthropics/skills repository <!-- verify at use time --> handles skill-level eval — trigger accuracy, A/B description testing, and description optimization. The two are complementary: run `/calibrate` for quality and recall, `skill-creator` for trigger reliability.
- **A/B mode rationale**: every specialized agent adds system-prompt tokens — if a `general-purpose` subagent matches its recall and F1, the specialization adds no value. `ab` mode quantifies this gap per-target so you can decide whether to keep, retrain, or retire an agent. `significant` (Δ>0.10) confirms the agent's domain depth earns its cost; `marginal` (0.05–0.10) suggests instruction improvements may help; `none` (\<0.05) signals the agent's current instructions add no measurable lift over a vanilla agent — consider strengthening domain-specific antipatterns and re-running. Token cost is informational (logged in scores.json) but not part of the verdict — prioritize recall/F1 delta as the primary signal.
- **A/B blind spot — role-specificity beyond recall**: for any agent whose domain is well-covered by general training data (structured rule application, documented conventions, standard code patterns), `none` AB verdict does NOT mean "retire the agent". Their specialization shows up in severity accuracy, output actionability, token efficiency, and scope discipline — not recall alone. The benchmark measures all four: `delta_severity_accuracy` (correct prioritization), `delta_format_score` (structured, actionable output), `token_ratio` (conciseness), and `scope_fp` (domain refusal). A `none` ΔRecall result paired with positive ΔSevAcc, ΔFmt, and negative ΔTokens still confirms the specialist earns its cost — use ΔSevAcc and ΔFmt as the primary evidence in this case.
- **AB mode nesting**: Phase 2b spawns `general-purpose` baseline agents inside the pipeline subagent. Phase 3 spawns `general-purpose` scorer agents inside the same pipeline subagent. All at 2 levels (main → pipeline → agents) — no additional depth.

</notes>
