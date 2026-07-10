---
name: baseline-comparison-audit
description: "Audit whether a paper's baseline comparisons are COMPLETE, FAIR, and SIGNIFICANT: a required recent SOTA baseline is missing while 'best/SOTA' is claimed (HP-MISSING-BASELINE); a baseline is undertuned / given less compute-tuning-data, run at a mismatched config, or the equal-budget ablation-as-baseline is absent (HP-WEAK-BASELINE); 'outperforms' is asserted over overlapping error bars or with no variance/seeds (HP-SIG-OVERLAP); and a cross-row 'improves over baseline by X%' is arithmetically wrong (HP-DELTA-ERROR, cross-row form only). A versioned per-domain baseline profile + a live leaderboard/recency search are assembled by the EXECUTOR as structured facts; a fresh cross-model reviewer (gpt-5.5 xhigh, read-only, fresh thread per dimension) PROPOSES findings, each span-anchored to a ledger claim_id; tools/adjudicate_findings.py DECIDES the verdict. Works at L0 (stated comparisons) and deepens at L2 (configs/result files). A completeness question it cannot settle internally becomes needs_external_check, never a guessed missing baseline. Emits baseline-comparison-audit.findings.json; computes NO verdict. Detect-only. Triggers: \"baseline audit\", \"missing baselines\", \"is the comparison fair\", \"weak baseline\", \"baseline 误报\", \"SOTA earned?\"."
argument-hint: [paper-dir | claims.json]
allowed-tools: Bash(*), Read, Write, Grep, Glob, WebSearch, WebFetch, mcp__codex__codex
---

# Baseline Comparison Audit — is the comparison complete, fair, and significant?

Audit baseline-comparison integrity for: **$ARGUMENTS** (requires `claims.json`
from `/evidence-ledger`). Emit span-anchored `baseline-comparison-audit.findings.json`.
This skill computes **no verdict**.

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> verdict-bearing input — it proposes the findings the deterministic adjudicator
> turns into the report. Re-firing it on a wall-clock timer adds no signal: its
> output changes only when the **paper / ledger** (or the live leaderboard it
> cross-checks) changes, not with the clock. Schedule the *external wait that
> precedes it* — ledger built → audit **once**. (Mirrors ARIS's external-cadence
> doctrine.)

> Adapted from ARIS `paper-claim-audit` — its **scope-overclaim** and
> **delta-arithmetic** checks, reframed from "paper vs result files" to **"is the
> SOTA claim earned, and is the comparison a fair fight?"** — plus a per-domain
> baseline profile and a completeness / fairness / significance split. A favourite
> autoresearch shortcut is to claim SOTA while omitting the obvious recent baseline,
> to beat an undertuned one, or to write "outperforms" over error bars that overlap.
> This skill is the constraint that asks for the fair fight, pointed at a third
> party's submission, and it stays honest about what it cannot settle from a PDF.

## Why this exists

An autoresearch pipeline (or rushed human) optimises for the *headline* and treats
the comparison table as scaffolding to fill, not a fair experiment to run. The
repeatable failure modes:

- **Completeness** — "achieves state-of-the-art on GSM8K" while the obvious recent
  baseline a 2024–2026 reviewer expects is simply absent from the table, or the
  strong classical **floor** (BM25 for retrieval, GBDT for tabular, a linear/naive
  forecaster for time-series) is skipped while only weak neural baselines are beaten.
  `HP-MISSING-BASELINE`
- **Fairness** — the proposed method is tuned for 100 epochs / 5 seeds / extra data,
  the baseline is run at default settings for 10; or the compared rows use different
  backbones, splits, or eval protocols; or the single most informative baseline —
  the method's **own backbone with the new component removed, at an identical
  budget** — is missing. `HP-WEAK-BASELINE`
- **Significance** — "consistently outperforms" on a 0.3-point gap with overlapping
  error bars, with no variance / no seed count reported at all, or resting on a single
  dataset too thin for the "consistent / across-the-board" wording. `HP-SIG-OVERLAP`
- **Delta arithmetic** — "improves over the strongest baseline by 16%" when the
  baseline row is 73.1 and the proposed row is 78.0 (+6.7% relative / +4.9 points),
  the two operands sitting in *different* cells so the single-sentence deterministic
  pass cannot pair them. `HP-DELTA-ERROR` (cross-row form)

None of these is inherently misconduct — they are what an optimizing agent does when
nothing forces a fair comparison. The *stated* version is decidable at **L0** from
the manuscript; the *verified* version (real configs, real seeds) deepens at **L2**.
What this skill will **not** do is *guess*: where no domain profile exists and the
leaderboard search is inconclusive, the completeness question is handed off as
`needs_external_check`, not invented.

## Core principle

**Ledger-anchored, span-verified, reviewer≠adjudicator, honest about what it cannot
settle.** Four properties:

1. **Anchor to a PAPER claim.** Every above-`info` finding cites a ledger `claim_id`
   and quotes a **verbatim span of that claim's `text_span`**
   (`references/integrity-forensics-contract.md` rules 1–2). The "outperforms / SOTA
   / best / first" language lives in `comparison` and `scope` claims; the reported
   baseline set lives in `baseline` claims; values/table rows in `number` /
   `table_cell` claims. The anchor is whichever paper claim the finding undermines —
   the expected-baseline list, a leaderboard URL, or a config `file:line` are
   **forensic context for the description**, never the anchor.
2. **The executor assembles facts; the reviewer judges.** The profile + a live
   `WebSearch`/`WebFetch` give a *candidate expected-baseline set with sources and
   dates*; the executor passes it as **structured input** and never pre-declares
   "baseline X is missing" (`references/reviewer-independence.md`). The model
   **proposes**; `tools/adjudicate_findings.py` **decides**. This skill computes **no
   verdict**.
3. **Unsettleable completeness → hand off, don't guess.** "Is this really SOTA /
   first / the right baseline set?" cannot be closed from inside the paper. Unless an
   omission is *unambiguous, sourced, same-benchmark, and pre-dating*, emit
   `verdict_local: needs_external_check` + `requires_external_check: true`, not a flag
   (contract rule 6).
4. **Observability caps severity.** Stated-comparison checks are L0; a fairness
   finding that needs the actual config/seed files is `observability_level_required:
   2` and auto-demotes on a PDF-only run (`references/observability-levels.md`).

## How this differs from the other auditors (route correctly)

| Auditor | Question it answers | Level |
|---------|---------------------|------|
| `consistency-audit` | Does the paper contradict ITSELF / described method = evaluated method? (owns text-only `HP-SCOPE-INFLATE` + single-sentence `HP-DELTA-ERROR`) | L0 |
| `experiment-forensics` | Are the reported numbers what the code actually computes? (fake GT, self-norm, phantom) | L2 |
| **`baseline-comparison-audit`** (this) | **Are the right baselines present (completeness), fairly tuned/configured (fairness), and is "outperforms/SOTA" statistically earned (significance)?** | **L0 stated / L2 verified** |
| `citation-forensics` | Do the cited baseline papers exist and support the claim? | L0 |
| `presentation-signals` | Surface "AI-flavor" hints (auxiliary, capped at minor) | L0 |
| `adversarial-case-builder` | Strongest evidence-bound rejection memo (no verdict weight) | any |

**Do NOT raise here** (hand off instead): generic in-text scope inflation
("comprehensive / extensive / robust" decoupled from a SOTA/comparison claim) →
`consistency-audit` owns `HP-SCOPE-INFLATE`; a single-sentence "from A to B, X%"
delta whose operands and stated value sit in **one** sentence → already caught
deterministically by `consistency-audit` (do **not** re-emit — Step 5 dedups);
whether a baseline *number* matches the repo/code → `experiment-forensics` (L2);
whether a *cited* baseline paper exists / is used in-context → `citation-forensics`;
surface / AI-flavor → `presentation-signals`. This skill **never** emits an
F-pattern.

## Per-domain baseline profile (`PROFILE_VERSION = 0.1` — a SEED prior, always verified live)

The expected baseline set a competent 2024–2026 reviewer carries into the table. It
is **advisory** and deliberately at the level of *families / floors* (not pinned
method names that go stale); the **live `WebSearch`/`WebFetch` leaderboard check
(Step 2) is the authoritative cross-check** — the profile only seeds the question.
The **Fairness control** column names the matched-budget axis a `HP-WEAK-BASELINE`
finding turns on; the **Variance norm** column is what `HP-SIG-OVERLAP` turns on.

| Domain / benchmark | Expected baseline families (**bold = the easy-to-skip floor**) | Fairness control (matched-budget axis) | Variance norm (significance) |
|---|---|---|---|
| LLM reasoning / QA — GSM8K, MATH, MMLU, BBH, GPQA | a current frontier model (Llama-3.x, Qwen2.5, DeepSeek) + the prior method on the same benchmark; **strong CoT / self-consistency on the same base** | same base model; identical #shots, decoding (temp / SC samples), tool access, finetune data | variance over prompts/seeds for small gaps |
| Image classification — ImageNet-1k | a recent strong backbone at matched params/FLOPs (ConvNeXt-V2, DeiT-III, Swin-V2, MAE-ViT); **a well-tuned modern CNN** | params, FLOPs, input res, epochs, augmentation, pretrain data | single run common; ±std if pretraining differs |
| Detection / segmentation — COCO, ADE20K | a recent strong detector/segmenter at the same backbone & schedule (DINO, Co-DETR, ViTDet, Mask2Former); **a strong one-stage baseline** | backbone, schedule (1×/3×), input scale, extra data | single run common; ±std on mIoU if available |
| Machine translation — WMT | tuned Transformer-big + a recent NMT/LLM-MT system; **report COMET, not only BLEU** | data, model size, beam, vocab; same test split + (de)tok protocol | bootstrap CI on BLEU/COMET |
| Generation — FID on ImageNet/COCO, GenEval | a recent strong generator at matched sampling budget (DiT, EDM2, U-ViT, LDM); **report precision/recall, not only FID** | NFE/sampler, params, guidance; identical FID protocol (#samples, ref stats) | FID over a fixed sample size; seed/sample noise |
| Retrieval / RAG — BEIR, MTEB, NQ | a strong dense retriever + prior SOTA; **BM25 (the lexical floor)** | same corpus, index, eval protocol (full vs sampled negatives) | per-query bootstrap CI |
| Tabular learning | a strong recent DL-tab model + prior SOTA; **a well-tuned GBDT (XGBoost/LightGBM/CatBoost) — it MUST be tuned** | HPO-budget parity, features, splits | std over folds/seeds |
| Time-series forecasting | a strong recent forecaster + prior SOTA; **a linear / naive-seasonal baseline** | lookback, horizon, normalization, splits | std over windows/seeds |
| RL — control (MuJoCo/DMC), offline (D4RL), Atari | tuned SAC/TD3/PPO (online), CQL/IQL/Decision-Transformer (offline), Rainbow/IQN/DrQ/SPR (Atari); **a well-tuned standard algorithm** | env steps / frames / dataset, net size, #eval seeds & episodes | ≥5 seeds + std/IQM (rliable CI) |
| Code generation — HumanEval, MBPP, LiveCodeBench | a current frontier code LLM + prior SOTA + a same-size open base; **the base model w/o the proposed scaffold** | model size, #shots, decoding, contamination window | variance over samples (pass@k seeds) |
| Speech ASR — LibriSpeech | a Whisper-class / Conformer system + prior SOTA | training data, decoding / LM | WER ±CI if available |
| Graph — OGB | a strong GNN family + the prior OGB-leaderboard entry | features, splits | std over seeds |

**Cross-domain control (always applicable, even off-profile):** the single most
informative baseline is the proposed method's **own backbone / base model with the
new component removed, run at an identical budget** — the ablation-as-baseline. Its
absence, or an unequal budget for it, is the most common fairness failure and is
checkable for *any* paper, profile row or not.

**Honesty rule (load-bearing): no profile row + inconclusive search ⇒ NO guessed
"missing baseline".** Run the *fairness* + *significance* checks (which need no
profile) and emit the completeness question as `needs_external_check`. The profile
seeds a *question*, never a detector.

## Constants & Reviewer Calling Convention

```
REVIEWER_MODEL        = gpt-5.5                  # different family from executor (Claude)
REVIEWER_REASONING    = xhigh                    # always; effort never lowers reviewer quality
REVIEWER_SANDBOX      = read-only                # detect-only; never mutate the paper
REVIEWER_CWD          = <paper-dir>              # so it can read claims.json + sources directly
THREAD_POLICY         = fresh mcp__codex__codex per DIMENSION (and per entry on fan-out);
                        NEVER mcp__codex__codex-reply across dimensions/entries
TAXONOMY_VERSION      = 0.5                      # references/hack-pattern-taxonomy.md
PROFILE_VERSION       = 0.1                      # the per-domain baseline profile above (advisory)
PATTERNS_OWNED        = HP-MISSING-BASELINE, HP-WEAK-BASELINE, HP-SIG-OVERLAP,
                        HP-DELTA-ERROR (cross-row comparison form only — see Step 4),
                        HP-RESOURCE-IDENTITY-MISMATCH (named dataset/model/benchmark vs its
                        public record — HF card / Papers-with-Code; gather-facts-then-judge,
                        observability_level_required 0; FP-suppress subset/variant/version)
FINDINGS_FILE         = baseline-comparison-audit.findings.json
FINDING_ID_NAMESPACE  = BC###                    # distinct from F###/NUM###/HL### (consistency), EF### (experiment)
TRACE_POLICY          = forensic (never silently dropped)
TRACE_DIR             = .aris/traces/baseline-comparison-audit/<YYYY-MM-DD>_run<NN>/
```

- **Executor (Claude)** builds none of the judgment: it locates the ledger, extracts
  the comparison surface, assembles the candidate expected set **with sources and
  publication dates**, at L2 gathers **mechanical config/result facts** (grep/hash —
  listing what exists is a fact, not a judgment), passes **paths + the ledger + those
  facts + the checklist** to the reviewer, validates the reviewer's spans, and writes
  the findings file. It never summarizes the paper, pre-judges "X is missing", or
  leaks an opinion into the prompt (`reviewer-independence.md`). Passing what a public
  leaderboard says (with its date) is the same allowed division `experiment-forensics`
  (grep/hash facts) and `citation-forensics` (canonical metadata) use — reference
  facts, not hunches about the manuscript.
- **Reviewer (codex / gpt-5.5)** reads `claims.json` and the sources, decides which
  comparisons are incomplete / unfair / not significant, applies the known
  false-positive cases, and self-reports `false_positive_risk`. It is the
  evidence-extractor, not the judge.
- **Fresh thread per dimension.** Completeness (Step 3) and fairness + significance +
  delta (Step 4) are **separate fresh** `mcp__codex__codex` calls. On `— effort: max`
  or many comparison rows, fan each comparison **entry** out into its own fresh call —
  never `codex-reply` carrying one entry's conclusion into another (the bias guard).
  `codex-reply` is intentionally absent from `allowed-tools`.

---

## Step 0 — Preconditions: locate the ledger, read the run level

The ledger is the **only** structure this skill reasons over. Resolve it and read
the observability level **L** and `paper_id` it was built at (each Bash block is
self-contained — shell state does not persist between calls, so re-derive paths every
block):

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
# applicability signal — comparison / scope / baseline / table_cell are this skill's inputs:
rel = sum(by.get(t, 0) for t in ("comparison", "scope", "baseline", "table_cell"))
print("APPLICABLE   =", "yes" if rel else "low (no comparison/scope/baseline/table claims)")
PY
```

**Failure handling.** If `NO_LEDGER` is printed, stop and tell the user to run
`/evidence-ledger` first — this skill never re-reads the raw PDF and invents its own
structure (contract rule 1). Carry `L`, `PAPER_ID`, and the absolute `LEDGER` /
`PAPER_DIR` into every step below.

## Step 1 — Extract the comparison surface from the ledger (decide whether to run)

Pull the claims this audit reasons over and decide if there is anything to audit:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json from Step 0>"
python3 - "$LEDGER" <<'PY'
import json, re, sys, collections
d = json.load(open(sys.argv[1], encoding="utf-8"))
claims = d.get("claims", [])
COMPARE = re.compile(r"\b(state[- ]of[- ]the[- ]art|SOTA|outperform\w*|best|"
                     r"surpass\w*|beats?|superior|first to|consistently|"
                     r"compared?\s+(?:to|with)|baseline|prior\s+(?:work|art))\b", re.I)
anchors, baselines = [], []
for c in claims:
    t, span = c.get("type"), c.get("text_span", "")
    # the SOTA / outperforms assertion (the anchor for completeness + fairness):
    if t == "comparison" or (t == "scope" and COMPARE.search(span)):
        anchors.append((c["claim_id"], t, c.get("location", {}).get("section", "?"), span[:150]))
    # the baseline SET the paper reports (mechanical; the reviewer decides completeness):
    if t == "baseline":
        baselines.append((c["claim_id"], c.get("location", {}).get("section", "?"), span[:150]))
print(f"ANCHOR (comparison/SOTA) claims: {len(anchors)}   baseline-list claims: {len(baselines)}")
for cid, t, sec, sp in anchors[:40]:
    print(f"  [anchor:{t}] {cid} [{sec}] {sp!r}")
for cid, sec, sp in baselines[:20]:
    print(f"  [baseline] {cid} [{sec}] {sp!r}")
nums = collections.Counter(c.get("type") for c in claims if c.get("type") in ("number", "table_cell"))
mets = collections.Counter((c.get("value") or {}).get("metric") for c in claims
                           if (c.get("value") or {}).get("metric"))
print("VALUE CLAIMS =", dict(nums), "  METRICS (seed the profile row) =", dict(mets))
print("APPLICABLE   =", "yes" if (anchors or baselines) else "no -> write [] and stop")
PY
```

**Branch.** If **APPLICABLE = no** (zero comparison/SOTA/baseline claims), this skill
is **not applicable**: write an empty `baseline-comparison-audit.findings.json`
(`[]`), record a one-line `NOT_APPLICABLE` reason in the trace (Step 7), and stop.
**Silent skip is forbidden** — the orchestrator globs `*.findings.json` and expects
the file to exist. Otherwise record the **anchor claims** (the SOTA/comparison
assertions) and the **reported-baseline list** for the prompts. A purely mechanical
grep helps surface the table/baseline names (do **not** judge completeness here — that
is the reviewer's job):

```bash
LEDGER="<abs path to claims.json from Step 0>"
grep -rInE '\\begin\{tabular|\\caption|baseline|w\.r\.t|vs\.?|\bours?\b' \
    "$(dirname "$LEDGER")" --include='*.tex' 2>/dev/null | head -60
```

## Step 2 — Assemble the candidate expected-baseline set (profile + live search + recency guard)

Determine the benchmark/task from the anchor claims (and the method section), then
build a **candidate expected set with sources** — structured *evidence*, not a
verdict. The recency guard is what stops you from naming a hallucinated or concurrent
baseline as "missing":

1. **Profile lookup.** If the task is in the per-domain profile above, take its
   expected baseline families (incl. the **floor**) and the matched-budget axis. If
   no row matches → mark the domain `NO_PROFILE`; completeness defaults to
   `needs_external_check`.
2. **Live leaderboard cross-check** (the authoritative source; record the query + the
   top systems + their **dates/venues**):
   ```
   WebSearch: "<benchmark> state-of-the-art <paper/current year> leaderboard"
   WebSearch: "<benchmark> papers with code"
   WebFetch:  <the Papers-with-Code / leaderboard URL>   # top 5–8 systems + their dates
   ```
3. **Recency + existence guard.** For each candidate baseline, record its
   `same_benchmark?` · `published_before_paper?` · `source_url` · `date`. A system
   concurrent with or post-dating the audited paper is a **legitimate omission** (a
   false positive for "missing"), not a flag.

Create the run's trace dir **now** — its first use is the file written just below, so
it must exist before Step 7. Reuse this exact `RUNDIR` in Steps 3–7 (do **not** create
a second one):

```bash
DATE=$(date +%Y-%m-%d); N=1
while [ -d ".aris/traces/baseline-comparison-audit/${DATE}_run$(printf %02d $N)" ]; do N=$((N+1)); done
RUNDIR=".aris/traces/baseline-comparison-audit/${DATE}_run$(printf %02d $N)"; mkdir -p "$RUNDIR"
echo "RUNDIR = $RUNDIR"   # carry this exact path forward (shell state does not persist)
```

Write these facts (not opinions) into `$RUNDIR/expected_baseline_set.json`:

```json
{
  "task": "GSM8K grade-school math (LLM reasoning)",
  "profile_version": "0.1",
  "profile_hit": true,
  "leaderboard_source": "https://paperswithcode.com/sota/arithmetic-reasoning-on-gsm8k  (read <UTC date>)",
  "expected_baselines": [
    {"name": "Self-Consistency CoT", "year": 2023, "same_benchmark": true, "published_before_paper": true, "source": "<url>"},
    {"name": "<recent frontier model> few-shot CoT", "year": 2024, "same_benchmark": true, "published_before_paper": true, "source": "<url>"}
  ],
  "notes": "off-profile or inconclusive search -> completeness becomes needs_external_check, not a guess"
}
```

**Failure handling.** No network / search fails → fall back to the profile alone and
mark every completeness candidate `requires_external_check: true` (you could not
confirm recency/availability). An empty candidate set + `NO_PROFILE` ⇒ skip the
completeness flag and emit a single `needs_external_check` info finding instead.
**Never** phrase the set as "the paper is missing X" — that is the reviewer's call.

## Step 3 — Completeness pass (cross-model, fresh thread) → HP-MISSING-BASELINE

Open a **fresh** `mcp__codex__codex` thread (Reviewer Calling Convention). The
reviewer reads `claims.json` from its `cwd` for the *present* baselines and compares
against your *external* expected-set facts; every finding anchors to a ledger
`claim_id`. Send EXACTLY (fill every `[ ... ]`):

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are a baseline-COMPLETENESS forensics reviewer. You judge ONE thing: given
    what this paper claims ("state-of-the-art / best / first / outperforms prior
    work") on a benchmark, is an OBVIOUS, RECENT, RELEVANT baseline absent from the
    comparison? You do NOT judge whether numbers are real and you do NOT grade the
    paper. Describe a discrepancy to CHECK, never an accusation; hand off what you
    cannot ground.

    INPUTS (in your working directory — read them directly):
      - claims.json — the evidence ledger. The SOTA/comparison LANGUAGE lives in
        type:"comparison" and type:"scope" claims; the PRESENT baseline set in
        type:"baseline" claims; reported values + table rows in type:"number" /
        type:"table_cell"; figure/table labels in type:"caption". This is the ONLY
        structure you reason over; each claim = {claim_id, type, text_span (VERBATIM),
        location, value?}. You MAY re-open a source file to confirm a span is real,
        but you may NOT introduce a claim that is not in the ledger.
    REFERENCE (external facts gathered by the executor — cite the source in your
    finding; treat as GIVEN data, NOT a verdict, do not second-guess):
      - Profile row (PROFILE_VERSION 0.1): expected baseline FAMILIES = [...];
        matched-budget axis = [...].
      - Live leaderboard (<URL>, accessed <DATE>): top current systems + their
        dates/venues = [...].
      - Candidate expected set (name · same_benchmark? · published_before_paper? ·
        source): [paste expected_baseline_set.json from Step 2, or "NO_PROFILE /
        search unavailable"].
    ANCHOR TARGETS (the SOTA/comparison claims — claim_id + verbatim):
      [paste the anchor claims from Step 1]
    BASELINES THE PAPER REPORTS (mechanical extraction — may be incomplete):
      [paste the baseline-list claims + the grep names from Step 1]
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.

    HARD RULES (a finding that breaks any of these is worthless):
    1. ANCHOR. Every finding above "info" MUST carry >=1 evidence {claim_id, span}
       where claim_id EXISTS in claims.json and span is a VERBATIM whitespace-
       normalized SUBSTRING of THAT claim's text_span (no paraphrase). The primary
       anchor is the SOTA/outperforms claim (a comparison/scope claim); the named
       missing baseline goes in `description`, never as the anchor. ALWAYS anchor —
       even a needs_external_check finding — so it stays navigable.
    2. DISCREPANCY, NOT ACCUSATION. Never "reject", "fabricated", "the authors hid X".
    3. OBSERVABILITY. A missing-baseline-as-STATED is decidable from the manuscript
       => observability_level_required = 0.
    4. HAND OFF WHAT YOU CANNOT SETTLE (the core rule of this step). Emit
       HP-MISSING-BASELINE above info ONLY when ALL hold: (a) a SOTA/best/outperforms
       claim is anchored; (b) a SPECIFIC, NAMED baseline is absent from the present
       set; (c) per the supplied sources that baseline is an ESTABLISHED, publicly-
       available, PRE-DATING standard for THIS exact benchmark (not concurrent, not
       post-dating, not unavailable, not justified-as-omitted in the paper). If ANY of
       (b)/(c) is uncertain — concurrent/post-dating per the dates, no code, niche
       benchmark, NO_PROFILE, the paper justifies the omission — DO NOT flag: set
       verdict_local "needs_external_check", requires_external_check true, severity
       "info", false_positive_risk "high", and name what a human should verify.
    5. HONEST FP. Concurrency/post-dating, unavailability, and a stated justification
       are the common false positives here — say so. If the expected set is empty/
       inconclusive, do NOT manufacture a missing baseline.
    6. pattern_id MUST be HP-MISSING-BASELINE.

    SEVERITY DECISION (HP-MISSING-BASELINE):
      - unambiguous, sourced, same-benchmark, clearly PRE-DATING omission AND the
        paper's HEADLINE is the SOTA/best claim -> "critical", FP "low",
        requires_external_check false.
      - clearly relevant + likely prior but contestable, OR a skipped strong FLOOR
        (BM25/GBDT/linear) while only weak baselines are beaten -> "major", FP
        "medium", requires_external_check true.
      - uncertain / NO_PROFILE / cannot confirm recency or relevance -> "info",
        verdict_local "needs_external_check", requires_external_check true.

    OUTPUT: a single JSON array and NOTHING ELSE (no prose, no code fence). Each
    element conforms to schemas/finding.schema.json:
      {"finding_id":"BC001","skill":"baseline-comparison-audit",
       "pattern_id":"HP-MISSING-BASELINE","title":"short, neutral",
       "description":"which expected baseline is absent + the SOTA claim it undermines + the source",
       "severity":"critical|major|minor|info","observability_level_required":0,
       "evidence":[{"claim_id":"C0xx","span":"verbatim substring",
                    "location":{"file":"...","section":"..."}}],
       "verdict_local":"fail|warn|clean|needs_external_check",
       "requires_external_check":true|false,"false_positive_risk":"low|medium|high",
       "recommended_reviewer_action":"what to CHECK or ASK — never 'reject'"}
    An empty array [] is a valid, honest result (the expected baselines are all present).
```

Persist the raw response to the trace dir (Step 7) **before** parsing. **Failure
handling:** MCP stall → re-invoke the **identical** prompt as a fresh
`mcp__codex__codex` (never `codex-reply`). Prose instead of JSON → the Step 5
validator extracts the outermost `[...]`; if none, re-ask once "Output ONLY the JSON
array." If the web cross-check was unavailable, bias every completeness item toward
`needs_external_check` — never invent a leaderboard entry.

## Step 4 — Fairness + Significance + cross-row Delta pass (cross-model, fresh thread; L2 deepen)

A **separate, new** `mcp__codex__codex` thread for the head-to-head rows. At **L2**
first gather mechanical config/seed facts (paths + raw grep/hash only — no
interpretation, the same executor/reviewer division as `experiment-forensics`);
**skip this block at L0/L1** (there are no configs to read):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
PAPER_DIR="<abs PAPER_DIR from Step 0>"
L="<L from Step 0>"
# (L2 ONLY) per-method budget / tuning / seed asymmetry FACTS — paths + raw hits.
# Guarded: skip entirely at L0/L1 (no configs to read — the reviewer block gets "L<2: ...").
if [ "$L" = "2" ]; then
  grep -rInE 'epochs?|max_steps|learning_rate|\blr\b|batch_?size|seed|n_seeds|num_runs|backbone|warm.?up|sweep|tune|budget' \
      "$PAPER_DIR" --include='*.yaml' --include='*.yml' --include='*.json' --include='*.toml' 2>/dev/null | head -80
  find "$PAPER_DIR" -type f \( -name '*config*' -o -name '*args*' -o -name 'hparams*' \) 2>/dev/null | sort | head -40
  # space-safe and tolerant of zero matches (a bare `shasum $(...)` would hang on no args):
  find "$PAPER_DIR" -maxdepth 3 \( -name '*config*' -o -path '*results*.json' \) 2>/dev/null \
      | head -n 20 | while IFS= read -r ff; do shasum -a 256 "$ff" 2>/dev/null; done
fi
```

Then send EXACTLY (fill every `[ ... ]`):

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are a baseline-FAIRNESS-and-SIGNIFICANCE forensics reviewer. For each head-
    to-head comparison the paper draws ("we outperform / are better than / achieve X
    vs baseline Y"), check whether it is FAIR (matched budget/tuning/config),
    SIGNIFICANT (the gap exceeds reported noise), and whether the stated cross-row
    improvement matches its operands. PROPOSE findings only — do NOT grade the paper;
    describe a discrepancy to CHECK, never an accusation. You do NOT judge whether the
    numbers are real (that needs the code) — only what the paper's OWN comparison shows.

    INPUTS (read directly in your working directory):
      - claims.json — comparison LANGUAGE in type:"comparison" / type:"scope"; the
        baseline set in type:"baseline"; values + table rows in type:"number" /
        type:"table_cell"; labels in type:"caption". The ONLY structure you navigate
        by; each claim = {claim_id, type, text_span (VERBATIM), location, value?}. You
        MAY re-open a source file (and, at L2, the config/result files) to confirm a span.
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.
    HEAD-TO-HEAD comparison claims (anchor targets — claim_id + verbatim text_span):
      [paste the comparison/scope anchor claims + the relevant number/table_cell claims]
    REPORTED VARIANCE / SEEDS (if any, with claim_id):
      [paste any "+/-", "std", "over N seeds", "n=" spans, or write "NONE REPORTED"]
    L2 CONFIG FACTS (raw grep/hash hits + config paths — uninterpreted; empty if L<2):
      [paste the grep/find/shasum output above, or "L<2: no repo/configs available"]

    HARD RULES:
    1. ANCHOR every finding above "info" to a real claim_id + a VERBATIM substring of
       that claim. Anchor to the comparison claim (and the row's number/table_cell as
       extra evidence). A config file:line is forensic detail for the description —
       NOT a valid anchor. No verbatim span ⇒ keep at "info".
    2. DISCREPANCY, NOT ACCUSATION. Say what to CHECK/ASK. Never "reject"/"faked".
    3. OBSERVABILITY — set observability_level_required to the LOWEST tier at which the
       discrepancy is DECIDABLE: 0 when the asymmetry/variance/delta is VISIBLE IN THE
       PAPER TEXT/TABLES (e.g. "we train ours 300 epochs" vs a cited 90-epoch baseline
       number); 2 when CONFIRMING it needs the repo's config/result files (it auto-
       demotes on an L0/L1 run — that is correct, not a loss).
    4. HONEST FP. A documented identical budget, standard reference numbers cited from
       a baseline's own paper, a large gap, a reported significance test, and
       genuinely deterministic metrics are COMMON false positives — say so.
    5. pattern_id MUST be one of: HP-WEAK-BASELINE, HP-SIG-OVERLAP, HP-DELTA-ERROR,
       HP-RESOURCE-IDENTITY-MISMATCH.

    CHECKLIST (one finding per concrete discrepancy):
     1. FAIRNESS / WEAK BASELINE [HP-WEAK-BASELINE] — the proposed method gets more
        compute / tuning / data, or runs at more favorable settings, than the baseline;
        the compared rows use non-matching configs (backbone / data / split /
        decoding); a baseline is left at defaults while the method is tuned; a baseline
        number is copied from an old paper at a different budget. The strongest single
        check: is the method's OWN backbone-without-the-new-component (the ablation-as-
        baseline) reported at an IDENTICAL budget? severity major. observability 0 if
        the asymmetry is STATED in text; 2 if only the configs reveal it. FP: identical
        budget documented; a standard reference number quoted from the baseline's own
        paper (citing a published number is legitimate — note any config delta, do not
        allege).
     2. SIGNIFICANCE / OVERLAP [HP-SIG-OVERLAP] — "outperforms / better / consistently"
        claimed where reported error bars OVERLAP, or where NO variance / seed count is
        reported for a SMALL gap (within the field's typical noise for this metric).
        severity: major if error bars are reported AND overlap; minor if merely absent
        variance for a small gap (rise to major only if the headline rests on it).
        observability 0. FP (high → say so): a large gap; a significance test reported;
        a genuinely deterministic metric (exact match on a fixed test set). Two further
        thin-evidence signals — each a recurring real-review tell — to flag EXPLICITLY
        (SAME pattern_id HP-SIG-OVERLAP, SAME anchor = the comparison/SOTA claim):
        (a) NO VARIANCE / SEEDS REPORTED — the comparison rests on bare point estimates
            with NO ±/std/CI and NO seed/run count reported AT ALL (one number per cell,
            no "over N seeds"), so the gap cannot be told from run-to-run noise. severity
            minor for a small gap; major when the headline rests on it OR the profile's
            "Variance norm" column expects >=N seeds for this domain (e.g. RL >=5 seeds,
            retrieval per-query CI) and none are reported. observability 0. FP (high →
            say so): a large clearly-separated gap; a reported significance test; a
            genuinely deterministic / single-pass metric where seeds are moot.
        (b) SINGLE-DATASET-ONLY — a "consistently / robustly / across-the-board /
            general" comparison claim that rests on ONE dataset/benchmark (or a single
            split/domain), too thin for the breadth the wording asserts. severity minor;
            major only when that breadth IS the headline. observability 0. FP (high →
            say so): the claim is explicitly SCOPED to that one benchmark ("on GSM8K we
            …"); the dataset is the field-standard SOLE benchmark for the task; or broad
            scope genuinely exists elsewhere in the paper. LANE: this fires ONLY when
            anchored to a comparison/SOTA claim — generic scope-language inflation with
            NO comparison claim ("a comprehensive study") is consistency-audit's
            HP-SCOPE-INFLATE, not this; do NOT double-emit.
     3. CROSS-ROW DELTA ARITHMETIC [HP-DELTA-ERROR] — recompute a stated "improves over
        <baseline> by X%" as (proposed-baseline)/baseline AND absolute points; flag if
        X disagrees beyond rounding, or relative/absolute are conflated to inflate.
        severity major; critical if the corrected delta deflates a "large/significant"
        framing. observability 0. FP: abs-vs-rel stated explicitly; rounding. DELTA
        SCOPE (critical to avoid double-counting): flag ONLY when the two operands are
        a BASELINE row value and the PROPOSED row value living in DIFFERENT
        sentences/cells — the cross-row case a single-sentence regex cannot pair. Do
        NOT re-flag a delta whose operands AND stated value sit in ONE sentence — the
        deterministic consistency pass already owns those.
     4. RESOURCE IDENTITY [HP-RESOURCE-IDENTITY-MISMATCH] — a named dataset / benchmark /
        model is described with a checkable PUBLIC-RECORD property its registry contradicts
        (ImageNet-1k stated with the wrong #classes/size; a model's parameter count off from
        its card; a "SOTA 91.2 on <benchmark>" disagreeing with that benchmark's public
        leaderboard). RESOLVE each named resource against its HuggingFace dataset/model card
        or Papers-with-Code record (WebFetch/WebSearch — FACTS only; put the URL + access
        date in `description`); the reviewer judges the discrepancy. Anchor to the paper
        claim NAMING the resource (never the registry URL). severity major; critical if the
        mis-described resource IS the headline (the SOTA number that is the contribution).
        observability 0 (public-record contradiction) / 2 (the repo loads a different
        resource than named). FP (→ needs_external_check, never a guessed "wrong"): a
        declared subset/variant (ImageNet-100, a 10% split, a distilled/quantized model); a
        version difference (-21k vs -1k, v1 vs v2); an explicit redefinition; a stale /
        ambiguous registry or a leaderboard updated after submission. LANE: method
        described ≠ method evaluated is HP-METHOD-DRIFT (consistency-audit); a fabricated
        citation identity is HP-CITE-HALLUC — this is the named RESOURCE's identity vs its
        public record.

    OUTPUT: a single JSON array and NOTHING ELSE (schemas/finding.schema.json), same
    shape as the completeness prompt; set finding_id "BC0xx",
    skill "baseline-comparison-audit". An empty array [] is valid and honest. Set
    requires_external_check only when you genuinely cannot settle a point at this level.
```

**Deepen at L2.** When `L == 2`, the L2 config facts let the reviewer promote a
text-only suspicion to a confirmed `HP-WEAK-BASELINE` (keep `observability_level_required:
0` if the text already showed the asymmetry; use `2` for asymmetry only the configs
reveal). **Fan-out (optional, breadth).** On `— effort: max` or many comparison rows,
issue this checklist **per comparison entry** as a separate fresh `mcp__codex__codex`
call and concatenate the arrays — never `codex-reply`. Persist each raw reply to the
trace (Step 7). **Failure handling:** identical to Step 3 (fresh identical re-invoke
on stall; re-ask for the strict JSON array on prose; never hand-author findings).

## Step 5 — Validate + anchor + dedup (the anti-hallucination gate)

The executor enforces the **ANCHOR** gate (the one `tools/adjudicate_findings.py`
re-applies, so an anchored finding you keep is not silently rejected downstream) plus
baseline-specific **owned-pattern + delta-dedup + schema-hygiene** pre-filters,
**before** keeping anything. The span must be a verbatim, whitespace-normalized
**substring of** the cited claim (`span in base`, never `base in span` — appending
hallucinated text to a real claim must fail). Pass **every** saved raw reviewer
response (completeness + fairness + any per-entry fan-out files); they merge into one
findings file with one `BC###` namespace:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"
OUT="$(dirname "$LEDGER")/baseline-comparison-audit.findings.json"
# args: LEDGER OUT then each saved raw reviewer response file from Steps 3–4:
python3 - "$LEDGER" "$OUT" "<resp_completeness.md>" "<resp_fairness.md>" <<'PY'
import json, re, sys, os
ledger_path, out_path = sys.argv[1], sys.argv[2]
resp_paths = [p for p in sys.argv[3:] if p and os.path.isfile(p)]

def nw(s):                                   # mirror adjudicator _norm_ws (whitespace only)
    return " ".join((s or "").split())

OWNED = {"HP-MISSING-BASELINE", "HP-WEAK-BASELINE", "HP-SIG-OVERLAP", "HP-DELTA-ERROR",
         "HP-RESOURCE-IDENTITY-MISMATCH"}
ABOVE = {"critical", "major", "minor"}

ledger = json.load(open(ledger_path, encoding="utf-8"))
base = {c["claim_id"]: nw(c.get("text_span", "")) for c in ledger.get("claims", [])
        if c.get("claim_id")}

# best-effort dedup target: claim_ids the DETERMINISTIC consistency delta pass already
# flagged (consistency-audit.deterministic.findings.json, if it exists in this dir).
det_path = os.path.join(os.path.dirname(os.path.abspath(ledger_path)),
                        "consistency-audit.deterministic.findings.json")
det_delta = set()
if os.path.isfile(det_path):
    try:
        for f in json.load(open(det_path, encoding="utf-8")):
            if f.get("pattern_id") == "HP-DELTA-ERROR":
                for ev in f.get("evidence") or []:
                    if ev.get("claim_id"): det_delta.add(ev["claim_id"])
    except Exception:
        pass

proposed = []
for p in resp_paths:
    raw = open(p, encoding="utf-8").read()
    m = re.search(r"\[.*\]", raw, re.S)      # tolerate prose / code-fence wrapping
    try:
        chunk = json.loads(m.group(0) if m else raw)
        proposed += chunk.get("findings", []) if isinstance(chunk, dict) else chunk
    except Exception as e:
        print(f"WARN: could not parse {p}: {e}", file=sys.stderr)

kept, demoted, deduped, not_owned = [], 0, 0, 0
for f in proposed:
    if not isinstance(f, dict):
        continue
    f["skill"] = "baseline-comparison-audit"
    # ANCHOR: keep only evidence whose span is a verbatim ws-normalized substring of its claim
    anchored = [ev for ev in (f.get("evidence") or [])
                if ev.get("claim_id") in base and nw(ev.get("span", "")) and
                nw(ev["span"]) in base[ev["claim_id"]]]                 # span IN claim, not claim IN span
    f["evidence"] = anchored
    # owned-pattern gate: a non-owned pattern cannot rise above info here
    if f.get("pattern_id") and f["pattern_id"] not in OWNED and f.get("severity") in ABOVE:
        f["severity"] = "info"; f.setdefault("_demotions", []).append("pattern-not-owned"); not_owned += 1
    # best-effort delta dedup vs the deterministic single-sentence pass
    if f.get("pattern_id") == "HP-DELTA-ERROR" and f.get("severity") in ABOVE \
       and any(ev.get("claim_id") in det_delta for ev in anchored):
        f["severity"] = "info"; f.setdefault("_demotions", []).append("dup-of-deterministic-delta"); deduped += 1
    # ANCHOR gate: above-info needs >=1 anchored span
    if f.get("severity") in ABOVE and not anchored:
        f["severity"] = "info"; f.setdefault("_demotions", []).append("unanchored"); demoted += 1
    # OBSERVABILITY hygiene — MIRROR the adjudicator, fail-closed: an above-info finding whose
    # observability_level_required is missing/invalid demotes to info. NEVER silently default to 0
    # (that would let a forgotten level-2 config-only asymmetry survive an L0 run). type() not
    # isinstance() so JSON booleans (True==1) are rejected, exactly as adjudicate_findings.py does.
    olr = f.get("observability_level_required")
    if f.get("severity") in ABOVE and (type(olr) is not int or not (0 <= olr <= 3)):
        f["severity"] = "info"; f.setdefault("_demotions", []).append("undeclared-observability"); demoted += 1
    # FP-RISK hygiene — false_positive_risk is the REVIEWER's self-assessment (it drives the
    # adjudicator's cap); the executor never guesses it. Missing/invalid demotes to info, never a default.
    if f.get("severity") in ABOVE and f.get("false_positive_risk") not in ("low", "medium", "high"):
        f["severity"] = "info"; f.setdefault("_demotions", []).append("undeclared-fp-risk"); demoted += 1
    f.setdefault("reviewer", {"model": "gpt-5.5", "reasoning": "xhigh", "deterministic": False})
    # honest hand-off: needs_external_check carries no severity weight (adjudicate_findings.py has
    # no such gate, so the validator makes the claim true) — pin it to info, never drop it.
    if f.get("verdict_local") == "needs_external_check":
        f["requires_external_check"] = True
        if f.get("severity") in ABOVE:
            f["severity"] = "info"; f.setdefault("_demotions", []).append("needs-external-check-no-weight")
    kept.append(f)

for k, f in enumerate(kept, 1):                                        # one namespace, sequential
    f["finding_id"] = f"BC{k:03d}"

json.dump(kept, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
above = sum(1 for x in kept if x.get("severity") in ABOVE)
print(f"validated {len(kept)} baseline findings (above_info={above}; {demoted} demoted->info "
      f"(unanchored/undeclared); {not_owned} not-owned->info; {deduped} delta deduped) -> {out_path}")
PY
```

Scope of this gate: **anchoring + owned-pattern + delta-dedup + schema hygiene only**
(schema hygiene = the *presence/validity* of the reviewer's required fields — a
missing/invalid `observability_level_required` or `false_positive_risk` on an
above-info finding fails **closed to info**, never a guessed default). Do **not**
re-implement the adjudicator's verdict-bearing gates (the observability LEVEL
*downgrade* `req > run_level`, the FP-risk *cap*, the surface cap, the verdict) — those
need the run level and belong to `tools/adjudicate_findings.py`, the single decider.
`needs_external_check` findings are pinned to `info` (the honest hand-off carries no
severity weight), never dropped. The remaining judgments are the **reviewer's**, per the
prompt — concurrency/post-dating FP on a missing baseline, a large-gap/significance-
test FP on overlap, the `observability_level_required: 2` tag for config-only
asymmetry; if a kept finding plainly violates one of these, re-run that pass with the
correction noted (never hand-fabricate). **Failure handling.** A `JSONDecodeError`/
empty array for a step means that reviewer reply was malformed → re-run that step with
the strict-JSON reminder. A finding that loses all evidence is **kept as info** (never
silently dropped — the forensic record stays).

**Worked HP-MISSING-BASELINE (headline SOTA, critical):**

```json
{
  "finding_id": "BC001",
  "skill": "baseline-comparison-audit",
  "pattern_id": "HP-MISSING-BASELINE",
  "title": "Headline SOTA claim omits an expected, pre-dating same-benchmark baseline",
  "description": "Claim C007 asserts 'state-of-the-art on GSM8K'. The expected-set facts list Self-Consistency CoT (2023; same benchmark; predates this submission per paperswithcode <url>, accessed <date>) as a standard strong baseline, but it appears in no comparison/baseline claim in the ledger. Discrepancy to verify: a 'state-of-the-art' headline that omits an obvious pre-dating baseline — confirm the claim survives once it is included, or whether the omission is justified.",
  "severity": "critical",
  "observability_level_required": 0,
  "evidence": [
    {"claim_id": "C007", "span": "achieves state-of-the-art accuracy on GSM8K",
     "location": {"file": "main.tex", "section": "abstract"}}
  ],
  "verdict_local": "fail",
  "requires_external_check": false,
  "false_positive_risk": "low",
  "recommended_reviewer_action": "Ask the authors to add Self-Consistency CoT (and any other pre-dating leaderboard baseline) or to justify its omission as concurrent/unavailable; confirm the SOTA claim survives the comparison."
}
```

**Worked needs_external_check (off-profile — hand off, do NOT guess):**

```json
{
  "finding_id": "BC002",
  "skill": "baseline-comparison-audit",
  "pattern_id": "HP-MISSING-BASELINE",
  "title": "Baseline completeness not settleable internally (off-profile benchmark)",
  "description": "Claim C011 claims to 'outperform all prior methods' on a niche benchmark not covered by the baseline profile, and the leaderboard search was inconclusive. Completeness cannot be decided from the available inputs — NOT an allegation of an omission, only a hand-off for a domain expert to confirm the expected baseline set.",
  "severity": "info",
  "observability_level_required": 0,
  "evidence": [
    {"claim_id": "C011", "span": "outperform all prior methods",
     "location": {"file": "main.tex", "section": "experiments"}}
  ],
  "verdict_local": "needs_external_check",
  "requires_external_check": true,
  "false_positive_risk": "high",
  "recommended_reviewer_action": "Have a domain expert enumerate the expected baseline set for this benchmark and check it against the paper's comparison table."
}
```

**Worked HP-WEAK-BASELINE (L2, config-confirmed budget gap):**

```json
{
  "finding_id": "BC003",
  "skill": "baseline-comparison-audit",
  "pattern_id": "HP-WEAK-BASELINE",
  "title": "Compared rows use an unequal training budget",
  "description": "Claim C019 reports the proposed method (78.0) 'outperforms the baseline' (73.1) in Table 2. configs/ours.yaml sets epochs=100, n_seeds=5 (sha256 a1b2c3…) while configs/baseline.yaml sets epochs=10, n_seeds=1 — a 10x budget asymmetry in the compared rows, with no matched-budget / equal-budget ablation-as-baseline run reported. Discrepancy to verify: the 4.9-point gap may reflect compute, not method.",
  "severity": "major",
  "observability_level_required": 2,
  "evidence": [
    {"claim_id": "C019", "span": "our method (78.0) outperforms the baseline (73.1)",
     "location": {"file": "main.tex", "section": "table:2"}}
  ],
  "verdict_local": "warn",
  "reviewer": {"model": "gpt-5.5", "reasoning": "xhigh", "thread_id": "<codex thread>", "deterministic": false},
  "requires_external_check": false,
  "false_positive_risk": "low",
  "recommended_reviewer_action": "Ask the authors for the baseline under the same epochs/seeds/backbone budget as the proposed method (the config delta is at configs/{ours,baseline}.yaml), or to document why the budgets differ."
}
```

## Step 6 — Emit (one file)

Step 5 wrote the validated array to **`baseline-comparison-audit.findings.json`** (a
bare JSON array conforming to `schemas/finding.schema.json`), in the ledger's
directory. If both passes found nothing — or this skill was not applicable (Step 1) —
the file is `[]`; **write it anyway** (silent skip is forbidden; the orchestrator's
`*.findings.json` glob and the standalone adjudicate command both expect it at a
predictable path). This skill writes **exactly one** findings file: **no second
deterministic file** — unlike `consistency-audit`, baseline runs no deterministic tool
of its own, and it **never re-runs `tools/check_numeric_consistency.py`** (that tool
stamps `skill: consistency-audit`, so re-running it here would double-count under the
orchestrator glob). Its delta dimension is cross-model and deliberately
non-overlapping with consistency-audit's deterministic delta pass.

## Step 7 — Trace (forensic; never silently dropped)

Save every reviewer call under the **same `RUNDIR` created at the start of Step 2**
(`.aris/traces/baseline-comparison-audit/<YYYY-MM-DD>_run<NN>/`). This repo ships no
`save_trace.sh`, so write files directly — reuse that path; do **not** re-run the bump
loop here (it would allocate a second empty dir):

```bash
RUNDIR="<the RUNDIR printed in Step 2>"   # e.g. .aris/traces/baseline-comparison-audit/<date>_run01
mkdir -p "$RUNDIR"                          # idempotent — the dir already exists from Step 2
```

Populate it:

```
.aris/traces/baseline-comparison-audit/<date>_run<NN>/
  run.meta.json                       # {skill, paper_id, run_level_L, profile_version:"0.1", domain, ledger_sha?, generated_at, not_applicable?}
  expected_baseline_set.json          # Step 2 external facts (leaderboard URL + dates + candidate set)
  001-completeness.request.json       # the EXACT Step-3 prompt sent (paths + ledger + sourced facts + checklist)
  001-completeness.response.md        # the FULL raw reviewer response (input to Step 5)
  001-completeness.meta.json          # {model:"gpt-5.5", reasoning:"xhigh", thread_id, sandbox:"read-only"}
  002-fairness-significance.request.json
  002-fairness-significance.response.md
  002-fairness-significance.meta.json
  # 00N-comparison-<entry>.* for each per-entry fan-out call, if used
```

Each `request.json` is the independence audit trail — it must show the executor sent
only **paths + the ledger + sourced external facts + the checklist**, never a digest
or pre-judgment of the paper. `expected_baseline_set.json` makes the completeness
expectation reproducible (which leaderboard, when, what dates).

## Step 8 — Hand off, or adjudicate standalone

Within `/anti-autoresearch`, **stop here**: the orchestrator globs every
`*.findings.json`, runs the adjudicator once over the union, and emits `REPORT.md` +
`report.json`. When running this skill **alone**, you may produce the report yourself
— `--ledger` is **required** (it is what verifies each finding quotes a real ledger
span; without it every above-info finding fails closed to `info`):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"; D="$(dirname "$LEDGER")"
python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "$D/baseline-comparison-audit.findings.json" \
    --ledger "$LEDGER" \
    --paper-id "<PAPER_ID>" --observability-level <L> --taxonomy-version 0.5 \
    --out "$D/baseline.report.json" --md "$D/baseline.REPORT.md"
# prints e.g.: verdict=SOFT_FLAGS crit=0 maj=1 min=2 -> baseline.report.json, baseline.REPORT.md
```

The adjudicator applies, in order: ANCHOR → OBSERVABILITY → FP-RISK → MEMO → SURFACE
gates, then computes `overall_verdict` ∈ {CLEAN_GIVEN_EVIDENCE, SOFT_FLAGS,
HARD_FLAGS} (any span-anchored **critical** decidable at `L` → HARD_FLAGS). No model
is in the final decision; this skill rolls up under the `baseline` dimension via
`SKILL_TO_DIMENSION`. `needs_external_check` findings carry no severity weight — they
surface as open questions for a human, never as a flag. *(Use the `baseline.*` output
names when standalone so you do not clobber the orchestrator's combined `report.json`
/ `REPORT.md`.)*

## Output contract

This skill **always** writes, into the ledger's directory:

- `baseline-comparison-audit.findings.json` — a JSON array
  (`schemas/finding.schema.json`); the validated completeness + fairness +
  significance + cross-row delta findings (or `[]`). Each above-info finding carries
  `evidence[].claim_id` + a verbatim `span`, an integer `observability_level_required`,
  a `pattern_id` ∈ {`HP-MISSING-BASELINE`, `HP-WEAK-BASELINE`, `HP-SIG-OVERLAP`,
  `HP-DELTA-ERROR`}, and an honest `false_positive_risk`. Unsettleable completeness
  appears as `verdict_local: needs_external_check` + `requires_external_check: true`,
  never a guessed missing baseline.
- `.aris/traces/baseline-comparison-audit/<date>_run<NN>/` — the external-facts file +
  the raw reviewer call(s).

It writes **no verdict and no report** of its own — `report.json` / `REPORT.md` come
only from `tools/adjudicate_findings.py` (Step 8 / the orchestrator). It writes **no
second deterministic file** and never edits the audited paper.

## Key rules

- **No span → no severity.** Reject unanchored/paraphrased findings to `info` here
  (the adjudicator re-enforces). `span in claim`, whitespace-normalized — never
  `claim in span`. The anchor is a PAPER claim; the expected-set list / leaderboard
  URL / config `file:line` is forensic detail in the description, never the anchor.
- **No profile + inconclusive search ⇒ no guessed "missing baseline".** Hand off as
  `needs_external_check`, anchored to the SOTA claim. A guess is worse than a hand-off.
- **Recency / existence guard.** Confirm a candidate "missing" baseline is real,
  same-benchmark, and **pre-dates** the submission before flagging; concurrent/
  post-dating work is a legitimate omission (FP), not a flag.
- **Asymmetry is the fairness signal.** Unequal budget / tuning / data, mismatched
  backbone/split/protocol, or a missing equal-budget ablation-as-baseline. A standard
  reference number quoted from a baseline's own paper is legitimate (high FP) — note
  the config delta, don't allege. Stated in text → level 0; config-only → level 2.
- **Small gap + thin evidence (no variance/seeds, or single-dataset-only) is a flag to
  CHECK, not proof.** Keep `HP-SIG-OVERLAP` honest: overlapping reported error bars =
  major; merely-absent variance / no seed count reported at all for a small gap =
  minor, FP high; a "consistently/across-the-board" claim resting on a single dataset =
  minor (major only if breadth is the headline), FP high if the claim is scoped to that
  benchmark; a large gap or a reported significance test suppresses it.
- **Delta cross-check, not double-count.** Re-verify only *cross-row* "improves over
  baseline by X%" arithmetic whose operands span a sentence + a table row; never
  re-emit a single-sentence delta (owned by `consistency-audit`'s deterministic pass).
  Baseline never re-runs `check_numeric_consistency.py` (it stamps consistency-audit).
- **Reviewer ≠ adjudicator.** The model proposes findings; `adjudicate_findings.py`
  decides the verdict. This skill emits findings only.
- **Cross-model, fresh thread per dimension/entry.** Reviewer is a different family
  (gpt-5.5 xhigh); completeness and fairness/significance/delta are separate fresh
  `mcp__codex__codex` threads; `codex-reply` is never used (absent from `allowed-tools`).
- **Observability honesty.** Config/budget asymmetry only the repo reveals gets
  `observability_level_required: 2` so a PDF-only run auto-demotes it. You cannot prove
  an undocumented budget gap from a PDF.
- **Stay in lane.** Generic text scope-overclaim → `consistency-audit`
  (`HP-SCOPE-INFLATE`); code/result fraud → `experiment-forensics` (L2); citation
  issues → `citation-forensics`; surface/AI-flavor → `presentation-signals`. This
  skill **never** emits an F-pattern.
- **Discrepancy, not accusation.** Output asks a reviewer to *check/ask*, never to
  reject; the tool audits comparison integrity, not authorship.
- **Detect-only.** Never edit the audited paper (reviewer sandbox is read-only).
- **Reproducible.** Same ledger + same findings → same verdict; the leaderboard facts
  (with URL + date) are traced so the completeness expectation is auditable.

## When NOT to use this skill

- **No `claims.json` yet** → run `/evidence-ledger` first; this skill never invents
  structure from the raw PDF.
- **The paper makes no comparison / SOTA / baseline claim** (`APPLICABLE = no` in
  Step 1) → write `[]` and stop; there is nothing to audit.
- **Generic in-text scope inflation with no comparison** ("a *comprehensive* study")
  → `/consistency-audit` (`HP-SCOPE-INFLATE`).
- **A single-sentence "from A to B, X%" delta** → already caught deterministically by
  `/consistency-audit`; do not re-emit.
- **Whether a baseline NUMBER matches the repo / code** (fake GT, self-norm, phantom)
  → `/experiment-forensics` at **L2**.
- **Whether a *cited* baseline paper EXISTS / is used in-context** →
  `/citation-forensics`.
- **An AI-text / "looks machine-written" verdict** → out of scope; surface hints live
  in `/presentation-signals` (auxiliary, capped at minor). This repo is **not** an
  AI-text classifier.
- **On a timer** → never `/loop` / `/schedule` / `CronCreate` this skill; re-fire only
  when the paper, ledger, or live leaderboard changes (see the fence at the top).

## Review tracing

Forensic policy — never silently skipped. The exact `RUNDIR` layout and the
reviewer-independence audit-trail rule for each `request.json` (only paths + ledger +
sourced external facts + checklist were sent — no digest, no pre-judgment) are
specified once in **Step 7**; follow it for every `mcp__codex__codex` call
(completeness, fairness, and any per-entry fan-out).
