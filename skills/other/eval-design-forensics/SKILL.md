---
name: eval-design-forensics
description: "Audit whether a paper's EVALUATION DESIGN actually measures what it claims and whether its reporting is complete — the validity layer family D (experiment-forensics) cannot reach. Three patterns: train/test leakage means the reported score may not measure generalization (HP-EVAL-LEAKAGE — adopts the Kapoor & Narayanan 8-type / 3-category leakage taxonomy; the illegitimate-proxy / sampling-bias / pretraining-contamination subtypes hand off as needs_external_check, naming but NEVER running Oren-2023 exchangeability / Shi-2023 Min-K% / Golchin-2023 Time-Travel / BIG-bench canary); a load-bearing LLM judge is conflicted (same model/family as a compared system) or unvalidated (no human-agreement, no bias control) (HP-JUDGE-VALIDITY); a declared condition/metric is dropped or switched to favor the method, or 'best' is chosen with no held-out set (HP-SELECTIVE-REPORTING). Verdict-bearing at L0/L1 from the DESCRIBED protocol — NOT repo-gated like experiment-forensics; L2 only CONFIRMS against split/preprocessing/result files. A fresh cross-model reviewer (gpt-5.5 xhigh, read-only, fresh thread per pass) PROPOSES findings, each span-anchored to a ledger claim_id; tools/adjudicate_findings.py DECIDES the verdict. Leakage and under-reporting are usually HONEST methodological errors — every finding describes a discrepancy to CHECK, never an accusation. An LLM generating GROUND-TRUTH labels is HP-FAKE-GT (experiment-forensics) — routed there, not here. Emits eval-design-forensics.findings.json; computes NO verdict. Detect-only. Triggers: \"eval design audit\", \"evaluation validity\", \"train/test leakage\", \"data leakage\", \"is the score measuring generalization\", \"LLM judge bias\", \"is the judge validated\", \"selective reporting\", \"cherry-picked results\", \"评估设计审计\", \"评测有效性\", \"数据泄漏\", \"训练测试集泄漏\", \"裁判模型有没有验证\", \"选择性报告\"."
argument-hint: [paper-dir | claims.json]
allowed-tools: Bash(*), Read, Write, Grep, Glob, WebSearch, WebFetch, mcp__codex__codex
---

# Eval-Design Forensics — does the evaluation measure what the paper claims?

Audit evaluation-design and reporting validity for: **$ARGUMENTS** (requires
`claims.json` from `/evidence-ledger`). Emit span-anchored
`eval-design-forensics.findings.json`. This skill computes **no verdict**.

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> verdict-bearing input — it proposes the findings the deterministic adjudicator
> turns into the report. Re-firing it on a wall-clock timer adds no signal: its
> output changes only when the **paper / ledger** changes (or a repo arrives,
> raising the observability level), not with the clock. Schedule the *external wait
> that precedes it* — ledger built (or artifacts released → L2) → audit **once**.
> (Mirrors ARIS's external-cadence doctrine.)

> Adapted from the ML-evaluation-methodology literature — the leakage taxonomy of
> Kapoor & Narayanan (2023), the LLM-as-judge validity work (MT-Bench
> self-enhancement, self-preference, position bias), and the "Show Your Work" /
> reproducibility-checklist reporting norms — reframed to audit a **third party's**
> evaluation. A favourite autoresearch shortcut is to report a number that is
> arithmetically self-consistent (family A), runs real code against a real ground
> truth (family D), and **still does not measure what it claims**: the protocol
> leaks, the load-bearing metric is a conflicted/unvalidated LLM judge, or the
> reporting quietly drops a declared condition. This skill is the constraint that
> asks "is this a *valid measurement of the claim*?", pointed at a submission, and
> it stays honest — leakage and under-reporting are usually **honest methodological
> errors**, so every finding is a discrepancy to *clarify*, never an accusation.

## Why this exists

An optimizing pipeline (or rushed human) treats the evaluation as a number to make
go up, not a measurement to keep valid. The repeatable failure modes — distinct
from "is the number real?" (family D) — are:

- **Leakage** — the train/test boundary is broken (preprocessing fit before the
  split, no held-out set, duplicates across splits, a random split over time-ordered
  data, the same subject in both splits, an evaluated LLM that saw the benchmark in
  pretraining), so the reported score may not measure **generalization** at all.
  `HP-EVAL-LEAKAGE`
- **Judge validity** — the headline rests on an automatic **LLM judge** that is
  *conflicted* (the same model/family as a compared system, so its preference for
  that system is the "evidence") or *unvalidated* (no human-agreement correlation,
  no position/length bias control). `HP-JUDGE-VALIDITY`
- **Selective reporting** — a dataset / baseline / metric / seed-count the setup
  **explicitly declares** is dropped from the results, the metric is **switched**
  across tables to keep the method ahead, or "we report the best run/prompt/
  checkpoint" with **no held-out selection set** (selecting on the test set).
  `HP-SELECTIVE-REPORTING`

None of these is inherently misconduct — they are what an agent does when nothing
forces a *valid* evaluation. The **stated** version is decidable at **L0/L1** from
the described protocol; the **verified** version (real split/preprocessing/result
files) deepens at **L2**. What this skill will **not** do is *guess*: three leakage
subtypes are undecidable even with the repo and are handed off as
`needs_external_check`, not invented (see below).

## Core principle

**Ledger-anchored, span-verified, reviewer≠adjudicator, honest about what it cannot
settle.** Four properties:

1. **Anchor to a PAPER claim.** Every above-`info` finding cites a ledger `claim_id`
   and quotes a **verbatim span of that claim's `text_span`**
   (`references/integrity-forensics-contract.md` rules 1–2). The leak/judge/reporting
   tell lives in the *protocol / setup-description* — usually `method` and `scope`
   claims, with `comparison` / `number` for the judge metric and
   `caption` / `table_cell` / `baseline` for reporting. The anchor is whichever paper
   claim the finding undermines; a split-file `file:line`, a config, or a leaderboard
   date is **forensic context for the description**, never the anchor.
2. **The executor assembles facts; the reviewer judges.** At L2 the executor gathers
   **mechanical** split/preprocessing/judge/result facts (grep/hash — listing what
   exists is a fact, not a judgment) and may record one **public-record date fact**
   (a benchmark's release vs a model's cutoff, for the contamination FP guard). It
   passes **paths + the ledger + those facts + the checklist** to the reviewer and
   never pre-declares "this leaks" (`references/reviewer-independence.md`). The model
   **proposes**; `tools/adjudicate_findings.py` **decides**. This skill computes **no
   verdict**.
3. **Undecidable leakage subtypes → hand off, don't guess.** An *illegitimate-proxy
   feature*, *sampling bias in the test set*, and *pretraining/benchmark
   contamination* are domain / black-box judgments not settleable from the PDF **or
   the repo**. Emit `verdict_local: needs_external_check` + `requires_external_check:
   true` (contract rule 6); **name** the external methods a domain check would use —
   exchangeability (Oren 2023), Min-K% Prob (Shi 2023), Time-Travel (Golchin 2023),
   BIG-bench canary strings — and **never run them**.
4. **Verdict-bearing at L0/L1; observability still caps the L2-confirm.** Unlike
   `experiment-forensics` (no eval code at L0/L1 ⇒ info-only), a **stated-tell** here
   is decided from the described protocol and emits
   `observability_level_required: 0`. The **L2 confirmation** of the same leak/
   omission is a **separate** finding with `observability_level_required: 2` that
   auto-demotes on a PDF-only run (`references/observability-levels.md`). So a
   PDF-only run keeps the stated-tell as a flag and the verification as an info
   "confirm-at-L2" pointer — never the reverse.

## How this differs from the other auditors (route correctly)

This skill is the **L0/L1-stated / L2-verified** sibling of
`baseline-comparison-audit` and `proof-derivation-forensics` (both verdict-bearing
**without a repo**) — *not* the L2-only `experiment-forensics`.

| Auditor | Question it answers | Level |
|---------|---------------------|------|
| **`eval-design-forensics`** (this) | **Is the evaluation a VALID measurement of the claim, and is the reporting complete?** (train/test leakage, conflicted/unvalidated LLM judge, declared-but-unreported / metric-switch / best-without-held-out) | **L0/L1 stated · L2 verified** |
| `experiment-forensics` | Are the reported numbers what the **code** computes? (fake/derived GT, self-norm, phantom, dead metric) | L2 |
| `consistency-audit` | Does the paper contradict ITSELF / described method = evaluated method? (owns `HP-AGG-DRIFT`, `HP-APPENDIX-CONTRA`, text-only `HP-SCOPE-INFLATE`) | L0 |
| `baseline-comparison-audit` | Are the right baselines present, fairly tuned, and is "SOTA" earned? (owns `HP-MISSING-BASELINE`, `HP-SIG-OVERLAP`) | L0 stated / L2 verified |
| `citation-forensics` | Do the cited papers exist and support the claim? | L0 |
| `presentation-signals` | Surface "AI-flavor" hints (auxiliary, capped at minor) | L0 |
| `adversarial-case-builder` | Strongest evidence-bound rejection memo (no verdict weight) | any |

**Do NOT raise here** (hand off instead):

- **An LLM generating the GROUND-TRUTH labels/targets** (not judging outputs) →
  `experiment-forensics` `HP-FAKE-GT` (L2). The clean split: a judge whose
  **preference IS the reported metric** is `HP-JUDGE-VALIDITY` (here, L0/L1 stated);
  a model that **fabricates the reference** the metric is computed against is
  `HP-FAKE-GT` (there, needs the code, L2). When unsure which, prefer the L2 route
  and set `needs_external_check`.
- **best-reported-as-mean** (the aggregation lies) → `consistency-audit`
  `HP-AGG-DRIFT`; **thin overall scope** with no comparison → `consistency-audit`
  `HP-SCOPE-INFLATE`; **appendix-vs-main disagreement on the same quantity** →
  `consistency-audit` `HP-APPENDIX-CONTRA`.
- **A never-mentioned expected SOTA baseline** (completeness) →
  `baseline-comparison-audit` `HP-MISSING-BASELINE`; a "consistently/across-the-board"
  comparison resting on **one dataset** → `baseline-comparison-audit`'s single-dataset
  `HP-SIG-OVERLAP`.
- **Whether a reported number matches the code** (fake GT, self-norm, phantom) →
  `experiment-forensics` (L2); **whether a cited paper exists / is used in context**
  → `citation-forensics`; **surface / AI-flavor** → `presentation-signals`.

`HP-SELECTIVE-REPORTING` is **scoped to declared-but-unreported / cherry-picked-
among-shown** — the gap between what the setup *promised* and what the tables
*deliver*. It never re-emits the four patterns above.

## The Kapoor & Narayanan leakage taxonomy (adopted — paraphrased)

`HP-EVAL-LEAKAGE` adopts the **eight leakage types in three categories** of Kapoor &
Narayanan (2023), paraphrased. The reviewer maps each finding to one type and records
it in the `description`.

| K&N category (the leakage **TYPE**) | The tell (subtypes) | This repo's **observability** | Common false positive |
|---|---|---|---|
| **L1 — no clean train/test separation** | (a) no held-out test set at all; (b) preprocessing (scaling / imputation / resampling) **fit on all data before the split**; (c) feature selection fit before the split; (d) duplicate / near-duplicate records across splits | **L0** stated / **L2** verified | a transductive / semi-supervised design where overlap is **intended and declared**; preprocessing fit on **train only**, then applied to test (the *correct* pattern) |
| **L2 — illegitimate (proxy) feature** | a feature that stands in for the target, or would be unavailable at prediction time | **needs_external_check** (domain judgment) | a "proxy-looking" feature that is **genuinely available** at prediction time |
| **L3 — test set not from the distribution of interest** | (a) **temporal** leakage (random split over time-ordered data / training on the future); (b) **non-independence** (same subject / patient / group in both splits); (c) **sampling bias** in the test set | (a),(b) **L0** stated / **L2** verified; (c) **needs_external_check** | a correctly time-respecting split; a standard fixed benchmark split the field uses |
| **(LLM-specific) pretraining / benchmark contamination** | the evaluated model may have seen the public benchmark during pretraining | **needs_external_check** (black-box) — name Oren 2023 (exchangeability), Shi 2023 (Min-K%), Golchin 2023 (Time-Travel), BIG-bench canary; **never run them** | a benchmark released **after** the model's training cutoff, or a corpus **documented to exclude** it |

> ⚠️ **Two scales — do not conflate them.** K&N's **L1 / L2 / L3** are leakage-*type*
> labels (severity-ordered *categories of leak*). This repo's **L0 / L1 / L2** are
> *observability* levels (what you can *see*: PDF / +source / +repo). They are
> orthogonal. A K&N-**L1** preprocessing leak that is *stated* in the protocol is
> decidable at observability-**L0**. Every finding carries **both**: the K&N type in
> `description`, the observability in `observability_level_required`.

## Constants & Reviewer Calling Convention

```
REVIEWER_MODEL        = gpt-5.5                  # different family from executor (Claude)
REVIEWER_REASONING    = xhigh                    # always; effort never lowers reviewer quality
REVIEWER_SANDBOX      = read-only                # detect-only; never mutate the paper
REVIEWER_CWD          = <paper-dir>              # so it can read claims.json + the protocol/source directly
THREAD_POLICY         = fresh mcp__codex__codex per PASS (and per entry on fan-out);
                        NEVER mcp__codex__codex-reply across passes/entries (the bias guard)
TAXONOMY_VERSION      = 0.5                      # references/hack-pattern-taxonomy.md (family H)
LEAKAGE_TAXONOMY      = Kapoor & Narayanan 2023  # 8 types / 3 categories — adopted, paraphrased
PATTERNS_OWNED / ALLOWED = HP-EVAL-LEAKAGE, HP-JUDGE-VALIDITY, HP-SELECTIVE-REPORTING   # emit ONLY these
DIMENSION             = evaluation              # SKILL_TO_DIMENSION["eval-design-forensics"]
FINDINGS_FILE         = eval-design-forensics.findings.json
FINDING_ID_NAMESPACE  = ED###                    # distinct from F###/NUM###/HL### (consistency), EF### (experiment), BC### (baseline), PD### (proof)
VERDICT_BEARING_AT    = L0/L1 (stated-tells)     # NOT repo-gated; L2 only CONFIRMS
TRACE_POLICY          = forensic (never silently dropped)
TRACE_DIR             = .aris/traces/eval-design-forensics/<YYYY-MM-DD>_run<NN>/
```

- **Executor (Claude)** builds none of the judgment: it locates the ledger, extracts
  the evaluation surface (protocol / judge / declared-condition claims), at L2 gathers
  **mechanical** split/preprocessing/judge/result facts (grep/hash) and at most one
  **public-record date fact** for the contamination guard, passes **paths + the ledger
  + those facts + the checklist** to the reviewer, validates the reviewer's spans, and
  writes the findings file. It never summarizes the paper, pre-judges "this leaks", or
  leaks an opinion into the prompt (`reviewer-independence.md`). Passing a public
  release date (with its source) is the same allowed division `citation-forensics`
  (canonical metadata) and `baseline-comparison-audit` (leaderboard dates) use —
  reference facts, not hunches.
- **Reviewer (codex / gpt-5.5)** reads `claims.json` and the source (and, at L2, the
  split/preprocessing/judge/result files) directly from its `cwd`, decides which
  evaluations leak / rest on a conflicted-or-unvalidated judge / under-report, applies
  the known false-positive cases, and self-reports `false_positive_risk`. It is the
  evidence-extractor, not the judge.
- **Fresh thread per pass.** Leakage (Step 3) and judge-validity + selective-reporting
  (Step 4) are **separate fresh** `mcp__codex__codex` calls. On `— effort: max` or many
  evaluation tracks, fan each track **entry** out into its own fresh call — never
  `codex-reply` carrying one entry's conclusion into another (the bias guard).
  `codex-reply` is intentionally absent from `allowed-tools`.

---

## Step 0 — Preconditions: locate the ledger, read the run level

The ledger is the **only** structure this skill reasons over. Resolve it and read the
observability level **L** and `paper_id` it was built at (each Bash block is
self-contained — shell state does not persist, so re-derive paths every block):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
# $ARGUMENTS is a paper-dir OR a claims.json path:
LEDGER="$ARGUMENTS"; [ -d "$LEDGER" ] && LEDGER="$LEDGER/claims.json"
# Only the NO-ARGUMENT case defaults to the CWD ledger. An EXPLICIT argument that
# resolves to a missing claims.json must NOT silently fall back to $(pwd) — that
# could audit the wrong paper; let the NO_LEDGER check below fire instead.
[ -z "$ARGUMENTS" ] && LEDGER="$(pwd)/claims.json"
python3 - "$LEDGER" <<'PY'
import json, sys, os, collections
p = sys.argv[1]
if not os.path.isfile(p):
    sys.exit("NO_LEDGER: claims.json not found. Run /evidence-ledger FIRST "
             "(it writes artifact_manifest.json + claims.json).")
d = json.load(open(p, encoding="utf-8"))
claims = d.get("claims", [])
by = collections.Counter(c.get("type") for c in claims)
print("LEDGER       =", os.path.abspath(p))
print("PAPER_DIR    =", os.path.dirname(os.path.abspath(p)) or ".")
print("PAPER_ID     =", d.get("paper_id", "?"))
print("RUN_LEVEL_L  =", d.get("observability_level", 0))
print("CLAIMS       =", len(claims), dict(by))
# applicability signal — method/scope carry the protocol; comparison/number the judge
# metric; caption/table_cell/baseline the reported conditions:
rel = sum(by.get(t, 0) for t in ("method", "scope", "comparison", "number", "table_cell", "caption", "baseline"))
print("APPLICABLE   =", "yes" if rel else "low (no protocol/scope/comparison/table claims)")
PY
```

**Failure handling.** If `NO_LEDGER` is printed, stop and tell the user to run
`/evidence-ledger` first — this skill never re-reads the raw PDF and invents its own
structure (contract rule 1). Carry `L`, `PAPER_ID`, and the absolute `LEDGER` /
`PAPER_DIR` into every step below.

## Step 1 — Extract the evaluation surface from the ledger (decide whether to run)

Pull the claims this audit reasons over — the **protocol** (leakage anchors), the
**judge** (validity anchors), and the **declared conditions** (reporting anchors) —
and decide if there is anything to audit. This is a mechanical surface scan; the
reviewer decides validity:

```bash
LEDGER="<abs path to claims.json from Step 0>"
python3 - "$LEDGER" <<'PY'
import json, re, sys, collections
d = json.load(open(sys.argv[1], encoding="utf-8"))
claims = d.get("claims", [])
LEAK = re.compile(r"\b(train(?:ing)?[\s/_-]*(?:and[\s/_-]*)?test|train[\s/_-]*test|split|held?[\s-]*out|"
                  r"cross[\s-]*validat|k-?fold|preprocess|standardi[sz]|normali[sz]|imput|"
                  r"resampl|oversampl|smote|feature[\s-]*select|leak|duplicat|de-?dup|"
                  r"temporal|time[\s-]*(?:series|order)|contaminat|pre-?train|data\s+split)\b", re.I)
JUDGE = re.compile(r"\b(LLM[-\s]*as[-\s]*a?[-\s]*judge|as\s+(?:a\s+)?judge|automatic(?:ally)?\s+(?:judg|evaluat|scor|rat)|"
                   r"GPT-?4o?|GPT-?3\.5|Claude|Gemini|win[\s-]*rate|pairwise|preference|"
                   r"rated\s+by|scored\s+by|judged\s+by|LLM\s+(?:judge|evaluator|grader))\b", re.I)
DECLARE = re.compile(r"\b(we\s+(?:evaluate|report|test|measure|use)|datasets?|benchmarks?|metrics?|"
                     r"seeds?|over\s+\d+\s+(?:seed|run)|best\s+(?:checkpoint|prompt|run|model|epoch)|"
                     r"five|four|three|\{[^}]*\})\b", re.I)
leak_a, judge_a, report_a = [], [], []
for c in claims:
    t, span = c.get("type"), c.get("text_span", "")
    sec = c.get("location", {}).get("section", "?")
    if t in ("method", "scope") and LEAK.search(span):
        leak_a.append((c["claim_id"], t, sec, span[:160]))
    if t in ("comparison", "scope", "method", "number") and JUDGE.search(span):
        judge_a.append((c["claim_id"], t, sec, span[:160]))
    if t in ("scope", "method", "caption", "table_cell", "baseline") and DECLARE.search(span):
        report_a.append((c["claim_id"], t, sec, span[:160]))
print(f"LEAKAGE anchors: {len(leak_a)}  JUDGE anchors: {len(judge_a)}  REPORTING anchors: {len(report_a)}")
for tag, rows in (("leak", leak_a), ("judge", judge_a), ("report", report_a)):
    for cid, t, sec, sp in rows[:30]:
        print(f"  [{tag}:{t}] {cid} [{sec}] {sp!r}")
print("APPLICABLE   =", "yes" if (leak_a or judge_a or report_a) else "no -> write [] and stop")
PY
```

**Branch.** If **APPLICABLE = no** (no protocol / judge / declared-condition claims),
this skill is **not applicable**: write an empty `eval-design-forensics.findings.json`
(`[]`), record a one-line `NOT_APPLICABLE` reason in the trace (Step 7), and stop.
**Silent skip is forbidden** — the orchestrator globs `*.findings.json` and expects
the file to exist. Otherwise record the three anchor lists for the prompts. A purely
mechanical grep of the source helps surface the protocol/table language (do **not**
judge validity here — that is the reviewer's job):

```bash
LEDGER="<abs path to claims.json from Step 0>"
grep -rInE 'train[ /_-]*test|split|held[ -]*out|cross[ -]*valid|preprocess|standardi|normali|impute|leak|duplicat|as a judge|win rate|pairwise|we (evaluate|report) on|best (checkpoint|prompt|run)' \
    "$(dirname "$LEDGER")" --include='*.tex' --include='*.txt' 2>/dev/null | head -60
```

## Step 2 — Gather mechanical facts (L2 split/preprocessing/judge/result; optional date fact)

Create the run's trace dir **now** — its first use is the facts file written just below,
so it must exist before Step 7. Reuse this exact `RUNDIR` in Steps 3–7 (do **not**
create a second one):

```bash
DATE=$(date +%Y-%m-%d); N=1
while [ -d ".aris/traces/eval-design-forensics/${DATE}_run$(printf %02d $N)" ]; do N=$((N+1)); done
RUNDIR=".aris/traces/eval-design-forensics/${DATE}_run$(printf %02d $N)"; mkdir -p "$RUNDIR"
echo "RUNDIR = $RUNDIR"   # carry this exact path forward (shell state does not persist)
```

**At L2 only** (repo + result files present), gather raw, uninterpreted facts — paths
+ grep/hash only, the same executor/reviewer division as `experiment-forensics`. Skip
this block at L0/L1 (there is no code to read — the reviewer block gets "L<2: ..."):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PAPER_DIR="<abs PAPER_DIR from Step 0>"; L="<L from Step 0>"; RUNDIR="<the RUNDIR above>"
if [ "$L" = "2" ]; then
  # (a) split / preprocessing / dedup ordering FACTS (the K&N-L1 / L3 tells) -> leakage_grep.txt
  grep -rInE 'train_test_split|StratifiedKFold|KFold|GroupKFold|TimeSeriesSplit|\.split\(|train/val|holdout|hold-out|'\
'StandardScaler|MinMaxScaler|fit_transform|\.fit\(|SimpleImputer|impute|SMOTE|resample|oversampl|'\
'SelectKBest|feature_select|drop_duplicates|duplicated\(|dedup|shuffle=True|random_state' \
      "$PAPER_DIR" --include='*.py' --include='*.ipynb' 2>/dev/null | head -80 > "$RUNDIR/leakage_grep.txt"
  # (b) LLM-judge calling code FACTS -> judge_grep.txt
  grep -rInE 'as_judge|llm_judge|judge_model|gpt-?4|gpt-?3\.5|claude|gemini|openai|anthropic|'\
'pairwise|win_rate|preference|rate_response|score_response|annotate' \
      "$PAPER_DIR" --include='*.py' --include='*.ipynb' --include='*.yaml' --include='*.json' 2>/dev/null | head -60 > "$RUNDIR/judge_grep.txt"
  # (c) which DECLARED conditions actually produced result files (the selective-reporting L2 confirm) -> reporting_grep.txt
  { find "$PAPER_DIR/results" "$PAPER_DIR/outputs" "$PAPER_DIR/logs" -type f \( -name '*.json' -o -name '*.csv' \) 2>/dev/null | sort | head -60
    echo "## metric/dataset keys present in result files:"
    grep -rIhoE '"(dataset|benchmark|metric|seed|split|task)"[^,}]{0,40}' \
      "$PAPER_DIR/results" "$PAPER_DIR/outputs" "$PAPER_DIR/logs" 2>/dev/null | sort -u | head -60; } > "$RUNDIR/reporting_grep.txt"
  # (d) reproducibility anchors: hash each discovered file (space-safe; tolerant of zero matches)
  { grep -rIlE 'split|scaler|judge|metric' "$PAPER_DIR" --include='*.py' 2>/dev/null | head -n 20
    find "$PAPER_DIR" -maxdepth 3 -path '*results*' -name '*.json' 2>/dev/null | head -n 20; } \
    | while IFS= read -r ff; do shasum -a 256 "$ff" 2>/dev/null; done > "$RUNDIR/hashes.txt"
  echo "L2 facts -> $RUNDIR/{leakage_grep,judge_grep,reporting_grep,hashes}.txt"
else
  echo "L<2: stated-tell pass only (no split/judge/result files to read)."
fi
```

**Optional contamination date fact (the FP guard, not a detector).** If a benchmark is
named and an evaluated model's training cutoff is knowable, you MAY record **one**
public-record date fact — `WebSearch`/`WebFetch` for "<benchmark> release date" and
"<model> training cutoff" — and write it (URL + access date) to
`$RUNDIR/contamination_dates.json`. This is a **fact** that *suppresses* a false
contamination flag (benchmark released after the cutoff → legitimate); it is **never**
a contamination *detector*. The skill never runs Min-K% / exchangeability / Time-Travel.

**Failure handling.** No network → skip the date fact; the reviewer treats
contamination as `needs_external_check` regardless. Empty L2 greps (a thin repo) → pass
"L2 but no split/judge/result files found" to the reviewer so it does not invent a leak.

## Step 3 — Leakage pass (cross-model, fresh thread) → HP-EVAL-LEAKAGE

Open a **fresh** `mcp__codex__codex` thread (Reviewer Calling Convention). The reviewer
reads `claims.json` from its `cwd` for the described protocol and, at L2, the split/
preprocessing files; every finding anchors to a ledger `claim_id`. Send EXACTLY (fill
every `[ ... ]`):

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are a train/test-LEAKAGE forensics reviewer. You judge ONE thing: given the
    EVALUATION PROTOCOL this paper describes (and, at L2, the split/preprocessing code
    it ships), is there a leak that means the reported score may NOT measure
    generalization? You do NOT judge whether numbers are real (that needs the code and
    is another auditor) and you do NOT grade the paper. Describe a discrepancy to
    CHECK/CLARIFY, never an accusation — leakage is most often an HONEST methodological
    error. Hand off what you cannot ground.

    INPUTS (in your working directory — read them directly):
      - claims.json — the evidence ledger. The PROTOCOL/SPLIT/PREPROCESSING language
        lives in type:"method" and type:"scope" claims; the ONLY structure you reason
        over. Each claim = {claim_id, type, text_span (VERBATIM), location, value?}. You
        MAY re-open a source file (and, at L2, the split/preprocessing code) to confirm a
        span is real, but you may NOT introduce a claim not in the ledger.
    LEAKAGE ANCHOR TARGETS (protocol/scope claims — claim_id + verbatim text_span):
      [paste the LEAKAGE anchors from Step 1]
    L2 SPLIT/PREPROCESSING FACTS (raw grep/hash — uninterpreted; empty if L<2):
      [inline RUNDIR/leakage_grep.txt + RUNDIR/hashes.txt, or "L<2: no repo/code available"]
    CONTAMINATION DATE FACT (public record, if gathered — GIVEN data, not a verdict):
      [inline RUNDIR/contamination_dates.json, or "none gathered"]
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.

    THE LEAKAGE TAXONOMY you map onto (Kapoor & Narayanan 2023 — 8 types / 3 categories;
    paraphrase the type in your description). ⚠️ K&N's L1/L2/L3 below are leakage-TYPE
    labels — they are NOT this repo's observability L0/L1/L2 (what you can SEE). Set
    observability_level_required from what you can SEE, and name the K&N type in text:
      - K&N L1 (no clean separation): (a) no held-out test; (b) preprocessing fit on ALL
        data BEFORE the split; (c) feature selection before the split; (d) duplicate /
        near-duplicate rows across splits.  -> observability 0 (stated) / 2 (verified).
      - K&N L2 (illegitimate/proxy feature): a feature that proxies the target or is
        unavailable at prediction time.  -> needs_external_check (domain judgment).
      - K&N L3 (test not from the distribution of interest): (a) temporal leakage (random
        split over time-ordered data / training on the future); (b) non-independence
        (same subject/patient/group in both splits) -> observability 0 / 2; (c) sampling
        bias in the test set -> needs_external_check.
      - Pretraining/benchmark CONTAMINATION of an evaluated LLM (the model may have seen
        the public benchmark in pretraining) -> needs_external_check. You may NAME the
        external methods a human would use (exchangeability, Oren 2023; Min-K% Prob, Shi
        2023; Time-Travel, Golchin 2023; BIG-bench canary) but you do NOT run them.

    HARD RULES (a finding that breaks any of these is worthless):
    1. ANCHOR. Every finding above "info" MUST carry >=1 evidence {claim_id, span} where
       claim_id EXISTS in claims.json and span is a VERBATIM whitespace-normalized
       SUBSTRING of THAT claim's text_span (no paraphrase). The anchor is the protocol/
       split/preprocessing claim the leak undermines; a code file:line goes in
       `description`, never as the anchor. ALWAYS anchor — even a needs_external_check
       finding — so it stays navigable.
    2. DISCREPANCY, NOT ACCUSATION. Never "reject", "fabricated", "the authors cheated".
    3. OBSERVABILITY. A leak visible in the DESCRIBED protocol => observability_level_
       required = 0 (this is verdict-bearing from a PDF). A leak only CONFIRMABLE from the
       split/preprocessing files => a SEPARATE finding with observability_level_required = 2
       (it auto-demotes on an L0/L1 run — that is correct). NEVER put the stated tell at 2.
    4. HAND OFF THE 3 UNDECIDABLE SUBTYPES. illegitimate-proxy feature, sampling bias, and
       pretraining/benchmark contamination are NOT decidable from the PDF or the repo:
       set verdict_local "needs_external_check", requires_external_check true, severity
       "info", false_positive_risk "high", and name what a human should check.
    5. HONEST FP. A declared transductive/semi-supervised overlap, a standard fixed
       benchmark split, preprocessing fit on TRAIN ONLY then applied to test, a correctly
       time-respecting split, a benchmark released AFTER the model's cutoff — these LOOK
       like leaks but are legitimate. Say so; if the protocol is under-described, prefer
       needs_external_check over a flag.
    6. pattern_id MUST be HP-EVAL-LEAKAGE.

    SEVERITY DECISION (HP-EVAL-LEAKAGE):
      - unambiguous stated leak (e.g. "standardize all features, then split") that
        plausibly invalidates the HEADLINE generalization claim -> "critical", FP "low",
        observability 0, requires_external_check false.
      - a leak affecting a NON-headline result, or a stated tell that needs the code to
        confirm -> "major" (FP "medium"); the L2 confirmation is a separate observability-2
        finding.
      - proxy / sampling-bias / contamination -> "info", needs_external_check, FP "high".

    OUTPUT: a single JSON array and NOTHING ELSE (no prose, no code fence). Each element
    conforms to schemas/finding.schema.json:
      {"finding_id":"ED001","skill":"eval-design-forensics","pattern_id":"HP-EVAL-LEAKAGE",
       "title":"short, neutral","description":"which K&N type + the protocol span it
       undermines + (L2) the split/preprocessing file:line","severity":"critical|major|
       minor|info","observability_level_required":0,
       "evidence":[{"claim_id":"C0xx","span":"verbatim substring",
                    "location":{"file":"...","section":"..."}}],
       "verdict_local":"fail|warn|clean|needs_external_check",
       "requires_external_check":true|false,"false_positive_risk":"low|medium|high",
       "recommended_reviewer_action":"what to CHECK or ASK — never 'reject'"}
    An empty array [] is a valid, honest result (the protocol shows no leak).
```

Persist the raw response to the trace dir (Step 7) **before** parsing. **Failure
handling:** MCP stall → re-invoke the **identical** prompt as a fresh
`mcp__codex__codex` (never `codex-reply`). Prose instead of JSON → the Step 5 validator
extracts the outermost `[...]`; if none, re-ask once "Output ONLY the JSON array." If
the L2 facts were empty, bias every code-confirm item toward `needs_external_check` —
never invent a split file.

## Step 4 — Judge-validity + Selective-reporting pass (cross-model, fresh thread)

A **separate, new** `mcp__codex__codex` thread. Send EXACTLY (fill every `[ ... ]`):

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are an EVALUATION-VALIDITY and REPORTING-COMPLETENESS forensics reviewer. You
    judge two things: (1) does a headline metric rest on an LLM JUDGE that is conflicted
    or unvalidated? (2) does the reporting DROP a condition the setup declared, SWITCH a
    metric to favor the method, or select "best" with no held-out set? PROPOSE findings
    only — do NOT grade the paper; describe a discrepancy to CHECK/CLARIFY, never an
    accusation. You do NOT judge whether the numbers are real (another auditor).

    INPUTS (read directly in your working directory):
      - claims.json — the JUDGE protocol lives in type:"method"/"comparison"/"scope"/
        "number"; the DECLARED conditions in type:"scope"/"method"; the reported tables in
        type:"table_cell"/"caption"/"number"/"baseline". The ONLY structure you navigate
        by; each claim = {claim_id, type, text_span (VERBATIM), location, value?}. You MAY
        re-open a source file (and, at L2, the judge/result files) to confirm a span.
    JUDGE ANCHOR TARGETS (claim_id + verbatim text_span):
      [paste the JUDGE anchors from Step 1]
    REPORTING ANCHOR TARGETS (declared-condition / table claims — claim_id + verbatim):
      [paste the REPORTING anchors from Step 1]
    L2 JUDGE + RESULT-FILE FACTS (raw grep — uninterpreted; empty if L<2):
      [inline RUNDIR/judge_grep.txt + RUNDIR/reporting_grep.txt, or "L<2: no repo available"]
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.

    HARD RULES:
    1. ANCHOR every finding above "info" to a real claim_id + a VERBATIM substring of that
       claim. For JUDGE-VALIDITY anchor to the judge-protocol claim naming the judge model
       (and the compared-systems claim showing the family overlap, as extra evidence). For
       SELECTIVE-REPORTING anchor to the setup-DECLARATION claim (what was promised). A
       config/result file:line is forensic detail for the description — NOT a valid anchor.
    2. DISCREPANCY, NOT ACCUSATION. Say what to CHECK/ASK. Never "reject"/"faked".
    3. OBSERVABILITY. Judge identity + the absence of reported validation are read off the
       described protocol => observability_level_required 0 (1 if only the source shows it).
       A declared-but-unreported condition is stated => 0; CONFIRMING the condition actually
       ran but went unreported needs the result files => a SEPARATE observability-2 finding.
    4. HONEST FP. (judge) a judge validated against human agreement with bias controls
       reported; a judge from a clearly DIFFERENT family than every compared system AND not
       load-bearing (corroborated by human eval / standard metrics); a calibrated standard
       protocol. UNVALIDATED-ONLY is HIGH-FP — missing validation *reporting* is not proof
       none was done (may be in an appendix / a cited standard). (reporting) a declared
       condition omitted but explicitly justified ("full grid in the repo"); different
       tasks legitimately using different standard metrics; best-selection on a DECLARED
       held-out validation set; an honestly-labeled pilot.
    5. pattern_id MUST be one of: HP-JUDGE-VALIDITY, HP-SELECTIVE-REPORTING.

    CHECKLIST (one finding per concrete discrepancy):
     1. JUDGE VALIDITY [HP-JUDGE-VALIDITY] — a headline comparison rests on an automatic
        LLM judge, and either:
        (a) CONFLICTED — the judge is the same MODEL or model FAMILY as a compared system
            (especially the proposed one), so its preference for that system IS the
            evidence (self-enhancement / self-preference). This is the lower-FP STRUCTURAL
            case (family overlap is checkable) -> severity major, false_positive_risk
            "medium". observability 0.
        (b) UNVALIDATED — the LLM judge is load-bearing yet the paper reports NO
            human-agreement validation (no correlation / kappa vs humans) AND NO bias
            control (no position-swap, no length/verbosity control) -> severity major if
            the headline rests on it, minor otherwise; false_positive_risk "high" (caps at
            minor). observability 0.
        ROUTING: an LLM that generates the GROUND-TRUTH labels/targets (not judging
        outputs) is HP-FAKE-GT (experiment-forensics, L2) — do NOT raise it here; if
        unsure which, set verdict_local "needs_external_check".
     2. SELECTIVE REPORTING [HP-SELECTIVE-REPORTING] — one of:
        (a) a dataset / baseline / metric / seed-count the SETUP EXPLICITLY DECLARES is
            then omitted from the results and is not in the appendix;
        (b) METRIC-SWITCHING across tables (Table 2 reports M where the method leads;
            Table 3 quietly switches to M' where it also leads) in a way that consistently
            favors the proposed method;
        (c) "we report the best checkpoint / prompt / run" with NO held-out selection set
            (selecting on the test set).
        severity major; critical if the omission/switch/selection is what PRODUCES the
        headline (false_positive_risk "low" when the declared-vs-reported gap is
        unambiguous); minor if peripheral. observability 0 (stated) / 2 (the result file
        shows the condition ran but went unreported — a SEPARATE finding).
        DE-DUP (do NOT emit these — route them): best-reported-as-mean -> HP-AGG-DRIFT
        (consistency-audit); thin overall scope with no comparison -> HP-SCOPE-INFLATE
        (consistency-audit); a never-mentioned expected baseline -> HP-MISSING-BASELINE
        (baseline-comparison-audit); appendix-vs-main on the SAME quantity ->
        HP-APPENDIX-CONTRA (consistency-audit). This pattern is ONLY declared-but-unreported
        / cherry-picked-among-shown.

    OUTPUT: a single JSON array and NOTHING ELSE (schemas/finding.schema.json), same shape
    as the leakage prompt; set finding_id "ED0xx", skill "eval-design-forensics". An empty
    array [] is valid and honest. Set requires_external_check only when you genuinely
    cannot settle a point at this level.
```

**Deepen at L2.** When `L == 2`, the judge/result facts let the reviewer promote a
text-only suspicion to a confirmed finding (keep `observability_level_required: 0` if
the text already showed the tell; use `2` only for what the files reveal). **Fan-out
(optional, breadth).** On `— effort: max` or many evaluation tracks, issue the relevant
checklist item **per track** as a separate fresh `mcp__codex__codex` call and
concatenate the arrays — never `codex-reply`. Persist each raw reply to the trace
(Step 7). **Failure handling:** identical to Step 3.

## Step 5 — Validate + anchor (the anti-hallucination gate)

The executor enforces the **ANCHOR** gate (the one `tools/adjudicate_findings.py`
re-applies, so an anchored finding you keep is not silently rejected downstream) plus
eval-design-specific **owned-pattern + schema-hygiene + external-check** pre-filters,
**before** keeping anything. The span must be a verbatim, whitespace-normalized
**substring of** the cited claim (`span in base`, never `base in span` — appending
hallucinated text to a real claim must fail). Pass **every** saved raw reviewer response
(leakage + judge/reporting + any per-track fan-out files); they merge into one findings
file with one `ED###` namespace:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"
OUT="$(dirname "$LEDGER")/eval-design-forensics.findings.json"
# args: LEDGER OUT then each saved raw reviewer response file from Steps 3–4:
python3 - "$LEDGER" "$OUT" "<resp_leakage.md>" "<resp_judge_reporting.md>" <<'PY'
import json, re, sys, os
ledger_path, out_path = sys.argv[1], sys.argv[2]
resp_paths = [p for p in sys.argv[3:] if p and os.path.isfile(p)]

def nw(s):                                   # mirror adjudicator _norm_ws (whitespace only)
    return " ".join((s or "").split())

OWNED = {"HP-EVAL-LEAKAGE", "HP-JUDGE-VALIDITY", "HP-SELECTIVE-REPORTING"}   # ALLOWED set
ABOVE = {"critical", "major", "minor"}
# OBS map — the canonical observability each owned pattern is decidable at (documentation;
# the REVIEWER sets observability_level_required per finding, and the adjudicator does the
# real req>run_level downgrade). stated-tell = 0; repo confirm = 2; the 3 leakage external
# subtypes carry no level (needs_external_check -> info).
OBS = {"HP-EVAL-LEAKAGE": "0 stated / 2 verified (proxy|sampling|contamination -> needs_external_check)",
       "HP-JUDGE-VALIDITY": "0/1 stated (2 may corroborate)",
       "HP-SELECTIVE-REPORTING": "0 stated / 2 verified"}

ledger = json.load(open(ledger_path, encoding="utf-8"))
base = {c["claim_id"]: nw(c.get("text_span", "")) for c in ledger.get("claims", [])
        if c.get("claim_id")}

proposed = []
for p in resp_paths:
    raw = open(p, encoding="utf-8").read()
    m = re.search(r"\[.*\]", raw, re.S)      # tolerate prose / code-fence wrapping
    try:
        chunk = json.loads(m.group(0) if m else raw)
        proposed += chunk.get("findings", []) if isinstance(chunk, dict) else chunk
    except Exception as e:
        print(f"WARN: could not parse {p}: {e}", file=sys.stderr)

kept, demoted, not_owned, ext = [], 0, 0, 0
for f in proposed:
    if not isinstance(f, dict):
        continue
    # OWNED gate: this skill emits ONLY family-H patterns — a missing/non-owned pattern_id is
    # DROPPED (not demoted), so nothing foreign can ride the `evaluation` dimension or survive
    # above-info on a malformed/absent id.
    if f.get("pattern_id") not in OWNED:
        not_owned += 1
        continue
    f["skill"] = "eval-design-forensics"
    # ANCHOR: keep only evidence whose span is a verbatim ws-normalized substring of its claim.
    # Guard malformed evidence (non-list / non-dict items can't anchor).
    anchored = [ev for ev in (f.get("evidence") if isinstance(f.get("evidence"), list) else [])
                if isinstance(ev, dict) and ev.get("claim_id") in base and nw(ev.get("span", "")) and
                nw(ev["span"]) in base[ev["claim_id"]]]               # span IN claim, never claim IN span
    f["evidence"] = anchored
    # ANCHOR gate: above-info needs >=1 anchored span
    if f.get("severity") in ABOVE and not anchored:
        f["severity"] = "info"; f.setdefault("_demotions", []).append("unanchored"); demoted += 1
    # OBS hygiene — MIRROR the adjudicator, fail-closed: an above-info finding whose
    # observability_level_required is missing/invalid demotes to info. NEVER default to 0
    # (that would let a forgotten level-2 code-confirm survive an L0 run). type() not
    # isinstance() so JSON booleans (True==1) are rejected, exactly as adjudicate_findings.py.
    olr = f.get("observability_level_required")
    if f.get("severity") in ABOVE and (type(olr) is not int or not (0 <= olr <= 3)):
        f["severity"] = "info"; f.setdefault("_demotions", []).append("undeclared-observability"); demoted += 1
    # FP-RISK hygiene — false_positive_risk is the REVIEWER's self-assessment (it drives the
    # adjudicator's cap); the executor never guesses it. Missing/invalid demotes to info.
    if f.get("severity") in ABOVE and f.get("false_positive_risk") not in ("low", "medium", "high"):
        f["severity"] = "info"; f.setdefault("_demotions", []).append("undeclared-fp-risk"); demoted += 1
    f.setdefault("reviewer", {"model": "gpt-5.5", "reasoning": "xhigh", "deterministic": False})
    # honest hand-off: needs_external_check carries no severity weight (the 3 leakage external
    # subtypes land here) — pin it to info, never drop it. Mirrors the adjudicator's gate 6.
    if f.get("verdict_local") == "needs_external_check" or f.get("requires_external_check") is True:
        f["requires_external_check"] = True
        if f.get("severity") in ABOVE:
            f["severity"] = "info"; f.setdefault("_demotions", []).append("needs-external-check-no-weight"); ext += 1
    kept.append(f)

for k, f in enumerate(kept, 1):                                       # one namespace, sequential
    f["finding_id"] = f"ED{k:03d}"

json.dump(kept, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
above = sum(1 for x in kept if x.get("severity") in ABOVE)
seen = sorted({f.get("pattern_id") for f in kept if f.get("pattern_id") in OWNED})
print(f"validated {len(kept)} eval-design findings (above_info={above}; {demoted} demoted->info "
      f"(unanchored/undeclared); {not_owned} not-owned dropped; {ext} needs-external-check->info) -> {out_path}")
print("OBS map for patterns seen:", {p: OBS[p] for p in seen})
PY
```

Scope of this gate: **anchoring + owned-pattern + schema hygiene + external-check
pinning only** (schema hygiene = the *presence/validity* of the reviewer's required
fields — a missing/invalid `observability_level_required` or `false_positive_risk` on an
above-info finding fails **closed to info**, never a guessed default). Do **not**
re-implement the adjudicator's verdict-bearing gates (the observability LEVEL *downgrade*
`req > run_level`, the FP-risk *cap* `{high:minor, medium:major, low:critical}`, the
verdict) — those need the run level and belong to `tools/adjudicate_findings.py`, the
single decider. `needs_external_check` findings (the 3 leakage external subtypes, and any
unsure judge/GT call) are pinned to `info`, never dropped. The remaining judgments are the
**reviewer's**, per the prompt — the K&N type, the conflicted-vs-unvalidated split, the
`observability_level_required: 2` tag for a code-only confirm; if a kept finding plainly
violates one, re-run that pass with the correction noted (never hand-fabricate). A finding
that loses all evidence is **kept as info** (the forensic record stays).

**Worked HP-EVAL-LEAKAGE (stated preprocessing-before-split, headline, critical, L0):**

```json
{
  "finding_id": "ED001",
  "skill": "eval-design-forensics",
  "pattern_id": "HP-EVAL-LEAKAGE",
  "title": "Preprocessing fit before the split may leak the test set into the reported accuracy",
  "description": "Claim C006 describes the protocol as 'we standardize all features, then split 80/20'. Standardizing before the split fits the scaler on the test rows (Kapoor & Narayanan leakage type L1 — no clean train/test separation), so the headline accuracy may not measure generalization. Discrepancy to verify: confirm whether the scaler was in fact fit on the training partition only and applied to test.",
  "severity": "critical",
  "observability_level_required": 0,
  "evidence": [
    {"claim_id": "C006", "span": "we standardize all features, then split 80/20",
     "location": {"file": "main.tex", "section": "method"}}
  ],
  "verdict_local": "fail",
  "requires_external_check": false,
  "false_positive_risk": "low",
  "recommended_reviewer_action": "Ask the authors whether the scaler/imputer was fit on TRAIN ONLY and then applied to test; if it was fit on all data before the split, the reported accuracy should be re-measured with a leak-free pipeline."
}
```

**Worked needs_external_check (pretraining contamination — hand off, do NOT guess):**

```json
{
  "finding_id": "ED002",
  "skill": "eval-design-forensics",
  "pattern_id": "HP-EVAL-LEAKAGE",
  "title": "Benchmark may be contaminated in the evaluated model's pretraining (not decidable here)",
  "description": "Claim C012 reports a headline score on a widely-published benchmark using a frontier LLM. Whether the model saw this benchmark during pretraining is a black-box question undecidable from the PDF or the repo — NOT an allegation. A domain check would use an exchangeability test (Oren 2023), Min-K% Prob (Shi 2023), Time-Travel (Golchin 2023), or BIG-bench canary strings; this tool does not run them.",
  "severity": "info",
  "observability_level_required": 0,
  "evidence": [
    {"claim_id": "C012", "span": "achieves 91.2 on the public benchmark",
     "location": {"file": "main.tex", "section": "experiments"}}
  ],
  "verdict_local": "needs_external_check",
  "requires_external_check": true,
  "false_positive_risk": "high",
  "recommended_reviewer_action": "Have a domain expert run a contamination probe (Min-K% / exchangeability / Time-Travel) or confirm the benchmark post-dates the model's training cutoff."
}
```

**Worked HP-JUDGE-VALIDITY (conflicted judge, major, L0):**

```json
{
  "finding_id": "ED003",
  "skill": "eval-design-forensics",
  "pattern_id": "HP-JUDGE-VALIDITY",
  "title": "Headline win-rate rests on a judge that shares a family with the proposed system",
  "description": "Claim C021 reports 'our GPT-4-based agent wins 78% of pairwise comparisons, judged by GPT-4'. The judge shares a model family with the proposed system (self-enhancement / self-preference: an evaluator favors its own family's generations), and no human-agreement number is reported. Discrepancy to verify: the 78% is the load-bearing evidence yet the judge is conflicted and unvalidated.",
  "severity": "major",
  "observability_level_required": 0,
  "evidence": [
    {"claim_id": "C021", "span": "wins 78% of pairwise comparisons, judged by GPT-4",
     "location": {"file": "main.tex", "section": "experiments"}}
  ],
  "verdict_local": "warn",
  "requires_external_check": false,
  "false_positive_risk": "medium",
  "recommended_reviewer_action": "Ask for a human-agreement validation of the judge (correlation/kappa) and a family-disjoint or position-swapped judge; report the win-rate under a judge that does not share a family with the proposed system."
}
```

**Worked HP-SELECTIVE-REPORTING (declared-but-unreported datasets, L0):**

```json
{
  "finding_id": "ED004",
  "skill": "eval-design-forensics",
  "pattern_id": "HP-SELECTIVE-REPORTING",
  "title": "Two declared evaluation datasets are not reported and not in the appendix",
  "description": "Claim C008 declares 'we evaluate on five datasets {A,B,C,D,E}', but every results table reports only {A,B,C} and no appendix reports D or E. Discrepancy to verify: ask for the D/E results, or an explicit reason for the omission. (De-dup: this is declared-but-unreported, not best-as-mean (HP-AGG-DRIFT) or a missing expected baseline (HP-MISSING-BASELINE).)",
  "severity": "major",
  "observability_level_required": 0,
  "evidence": [
    {"claim_id": "C008", "span": "we evaluate on five datasets",
     "location": {"file": "main.tex", "section": "experiments"}}
  ],
  "verdict_local": "warn",
  "requires_external_check": false,
  "false_positive_risk": "low",
  "recommended_reviewer_action": "Ask the authors for the results on datasets D and E (or an explicit justification for omitting them); confirm the headline survives once the declared conditions are all reported."
}
```

## Step 6 — Emit (one file)

Step 5 wrote the validated array to **`eval-design-forensics.findings.json`** (a bare
JSON array conforming to `schemas/finding.schema.json`), in the ledger's directory. If
both passes found nothing — or this skill was not applicable (Step 1) — the file is
`[]`; **write it anyway** (silent skip is forbidden; the orchestrator's `*.findings.json`
glob and the standalone adjudicate command both expect it at a predictable path). This
skill writes **exactly one** findings file and runs **no deterministic tool of its own**
(unlike `consistency-audit`): every finding is a cross-model proposal, span-anchored,
gated, and handed to the adjudicator.

## Step 7 — Trace (forensic; never silently dropped)

Save every reviewer call under the **same `RUNDIR` created at the start of Step 2**
(`.aris/traces/eval-design-forensics/<YYYY-MM-DD>_run<NN>/`). This repo ships no
`save_trace.sh`, so write files directly — reuse that path; do **not** re-run the bump
loop here (it would allocate a second empty dir):

```bash
RUNDIR="<the RUNDIR printed in Step 2>"   # e.g. .aris/traces/eval-design-forensics/<date>_run01
mkdir -p "$RUNDIR"                          # idempotent — the dir already exists from Step 2
```

Populate it:

```
.aris/traces/eval-design-forensics/<date>_run<NN>/
  run.meta.json                       # {skill, paper_id, run_level_L, taxonomy_version:"0.5", leakage_taxonomy:"K&N 2023", generated_at, not_applicable?}
  leakage_grep.txt / judge_grep.txt / reporting_grep.txt / hashes.txt   # Step 2 L2 facts (if L2)
  contamination_dates.json            # optional public-record date fact (if gathered)
  001-leakage.request.json            # the EXACT Step-3 prompt sent (paths + ledger + facts + taxonomy + checklist)
  001-leakage.response.md             # the FULL raw reviewer response (input to Step 5)
  001-leakage.meta.json               # {model:"gpt-5.5", reasoning:"xhigh", thread_id, sandbox:"read-only"}
  002-judge-reporting.request.json
  002-judge-reporting.response.md
  002-judge-reporting.meta.json
  # 00N-track-<entry>.* for each per-track fan-out call, if used
```

Each `request.json` is the independence audit trail — it must show the executor sent
only **paths + the ledger + the K&N taxonomy + the mechanical facts + the checklist**,
never a digest or pre-judgment of the paper (`references/reviewer-independence.md`).

## Step 8 — Hand off, or adjudicate standalone

Within `/anti-autoresearch`, **stop here**: the orchestrator globs every
`*.findings.json`, runs the adjudicator once over the union, and emits `REPORT.md` +
`report.json`. When running this skill **alone**, you may produce the report yourself —
`--ledger` is **required** (it verifies each finding quotes a real ledger span; without
it every above-info finding fails closed to `info`):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"; D="$(dirname "$LEDGER")"
python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "$D/eval-design-forensics.findings.json" \
    --ledger "$LEDGER" \
    --paper-id "<PAPER_ID>" --observability-level <L> --taxonomy-version 0.5 \
    --out "$D/eval-design.report.json" --md "$D/eval-design.REPORT.md"
# prints e.g.: verdict=SOFT_FLAGS crit=0 maj=1 min=1 -> eval-design.report.json, eval-design.REPORT.md
```

The adjudicator applies, in order: ANCHOR → OBSERVABILITY → FP-RISK → MEMO → SURFACE →
EXTERNAL-CHECK gates, then computes `overall_verdict` ∈ {CLEAN_GIVEN_EVIDENCE,
SOFT_FLAGS, HARD_FLAGS} (any span-anchored **critical** decidable at `L` → HARD_FLAGS).
No model is in the final decision; this skill rolls up under the **`evaluation`**
dimension via `SKILL_TO_DIMENSION`. `needs_external_check` findings carry no severity
weight — they surface as open questions for a human, never as a flag. *(Use the
`eval-design.*` output names when standalone so you do not clobber the orchestrator's
combined `report.json` / `REPORT.md`.)*

## Output contract

This skill **always** writes, into the ledger's directory:

- `eval-design-forensics.findings.json` — a JSON array (`schemas/finding.schema.json`);
  the validated leakage + judge-validity + selective-reporting findings (or `[]`). Each
  above-info finding carries `evidence[].claim_id` + a verbatim `span`, an integer
  `observability_level_required`, a `pattern_id` ∈ {`HP-EVAL-LEAKAGE`,
  `HP-JUDGE-VALIDITY`, `HP-SELECTIVE-REPORTING`}, and an honest `false_positive_risk`.
  The three undecidable leakage subtypes (illegitimate-proxy / sampling-bias /
  contamination) and any unsure judge-vs-GT call appear as
  `verdict_local: needs_external_check` + `requires_external_check: true`, never a
  guessed leak.
- `.aris/traces/eval-design-forensics/<date>_run<NN>/` — the mechanical-facts files +
  the raw reviewer call(s).

It writes **no verdict and no report** of its own — `report.json` / `REPORT.md` come
only from `tools/adjudicate_findings.py` (Step 8 / the orchestrator). It writes **no
second deterministic file** and never edits the audited paper.

## Key rules

- **Verdict-bearing at L0/L1; the L2-confirm is separate.** A stated leak / conflicted
  judge / declared-but-unreported condition is decidable from the described protocol →
  `observability_level_required: 0` (this is the opposite of `experiment-forensics`,
  which is info-only below L2). The L2 *confirmation* of the same tell is a separate
  `observability_level_required: 2` finding that auto-demotes on a PDF-only run.
- **No span → no severity.** Reject unanchored/paraphrased findings to `info` here (the
  adjudicator re-enforces). `span in claim`, whitespace-normalized — never `claim in
  span`. The anchor is a PAPER claim (the protocol / judge / declared-condition
  sentence); the split-file `file:line`, config, or leaderboard date is forensic detail
  in the description, never the anchor.
- **Two scales — never conflate.** K&N leakage **types** L1/L2/L3 are not this repo's
  **observability** levels L0/L1/L2. Carry both: the K&N type in `description`, the
  observability in `observability_level_required`.
- **Hand off the 3 undecidable leakage subtypes.** Illegitimate-proxy feature, sampling
  bias, and pretraining/benchmark contamination → `needs_external_check`; name the
  external methods (Oren 2023 / Min-K% / Time-Travel / canary) but **never run them**.
- **Judge ≠ ground-truth generator.** A judge whose preference IS the metric is
  `HP-JUDGE-VALIDITY` (here); a model that fabricates the reference the metric is
  computed against is `HP-FAKE-GT` (`experiment-forensics`, L2). Conflicted (family
  overlap) caps at major (FP medium); unvalidated-only caps at minor (FP high).
- **Selective-reporting stays in lane.** Only declared-but-unreported / metric-switch /
  best-without-held-out. best-as-mean → `HP-AGG-DRIFT`; thin scope → `HP-SCOPE-INFLATE`;
  never-mentioned baseline → `HP-MISSING-BASELINE`; appendix-vs-main on the same quantity
  → `HP-APPENDIX-CONTRA`. Do not double-emit.
- **Discrepancy, not accusation.** Leakage and under-reporting are usually honest
  methodological errors; output asks a reviewer to *check/clarify*, never to reject. The
  absence of a *reported* validation is not proof none was done (high-FP care).
- **Reviewer ≠ adjudicator.** The model proposes findings; `adjudicate_findings.py`
  decides the verdict. This skill emits findings only.
- **Cross-model, fresh thread per pass/track.** Reviewer is a different family (gpt-5.5
  xhigh); leakage and judge/reporting are separate fresh `mcp__codex__codex` threads;
  `codex-reply` is never used (absent from `allowed-tools`).
- **Detect-only.** Never edit the audited paper (reviewer sandbox is read-only).
- **Reproducible.** Same ledger + same findings → same verdict; the mechanical facts and
  any date fact (with URL + date) are traced so the expectation is auditable.

## When NOT to use this skill

- **No `claims.json` yet** → run `/evidence-ledger` first; this skill never invents
  structure from the raw PDF.
- **The paper describes no evaluation protocol / judge / declared conditions**
  (`APPLICABLE = no` in Step 1) → write `[]` and stop.
- **An LLM generating the ground-truth labels/targets** (not judging outputs) →
  `/experiment-forensics` `HP-FAKE-GT` at **L2**.
- **best-reported-as-mean / appendix-vs-main / thin in-text scope with no comparison**
  → `/consistency-audit` (`HP-AGG-DRIFT` / `HP-APPENDIX-CONTRA` / `HP-SCOPE-INFLATE`).
- **A never-mentioned expected baseline, or "SOTA / first / beats prior work"** →
  `/baseline-comparison-audit` (+ `/citation-forensics`), handed off via
  `needs_external_check`.
- **Whether a reported number matches the repo / code** (fake GT, self-norm, phantom)
  → `/experiment-forensics` at **L2**.
- **An AI-text / "looks machine-written" verdict** → out of scope; surface hints live in
  `/presentation-signals` (auxiliary, capped at minor). This repo is **not** an AI-text
  classifier.
- **On a timer** → never `/loop` / `/schedule` / `CronCreate` this skill; re-fire only
  when the paper, ledger, or observability level changes (see the fence at the top).

## Review tracing

Forensic policy — never silently skipped. The exact `RUNDIR` layout and the
reviewer-independence audit-trail rule for each `request.json` (only paths + ledger +
the K&N taxonomy + mechanical facts + checklist were sent — no digest, no pre-judgment)
are specified once in **Step 7**; follow it for every `mcp__codex__codex` call (leakage,
judge/reporting, and any per-track fan-out).

## Acknowledgements

The taxonomy this skill operationalizes is reframed from the ML-evaluation-methodology
literature for **third-party** forensics — ledger-anchored findings, observability
tiers, and reviewer ≠ adjudicator:

- **Kapoor, S. & Narayanan, A. (2023),** "Leakage and the reproducibility crisis in
  machine-learning-based science," *Patterns* — the eight leakage types / three
  categories that `HP-EVAL-LEAKAGE` adopts and paraphrases (**priority ack**).
  Contamination methods are **named only**, never run: Oren et al. (2023) exchangeability
  test; Shi et al. (2023) Min-K% Prob; Golchin & Surdeanu (2023) Time-Travel; the
  BIG-bench (Srivastava et al. 2022) canary-string convention.
- **Zheng et al. (2023),** "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" —
  self-enhancement bias and the human-agreement bar behind `HP-JUDGE-VALIDITY`;
  **Panickssery et al. (2024),** self-preference (evaluators favor their own
  generations); **Wang et al. (2024),** position bias in LLM evaluators.
- **Dodge et al. (2019),** "Show Your Work: Improved Reporting of Experimental Results,"
  and **Pineau et al. (2021),** the ML Reproducibility Checklist (NeurIPS 2019
  Reproducibility Program report) — the under-reporting norms behind
  `HP-SELECTIVE-REPORTING`.
