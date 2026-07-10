---
name: consistency-audit
description: "Flagship intra-paper self-consistency forensics: does the paper contradict ITSELF across abstract/intro/tables/body/appendix, and does the method DESCRIBED match the method EVALUATED? Needs no external ground truth — works PDF-only (L0). Runs a deterministic arithmetic pass + a fresh cross-model semantic pass, every finding span-anchored to the evidence ledger (claims.json), reviewer≠adjudicator. Emits consistency-audit.findings.json; NEVER computes the verdict. Triggers: \"consistency audit\", \"check the paper against itself\", \"self-consistency\", \"内部自洽\"."
argument-hint: [paper-dir | claims.json]
allowed-tools: Bash(*), Read, Write, mcp__codex__codex
---

# Consistency Audit — the paper vs itself

Audit intra-paper self-consistency for: **$ARGUMENTS** (requires `claims.json`
from `/evidence-ledger`). Emit span-anchored `consistency-audit.findings.json`;
the deterministic adjudicator — not this skill — computes the verdict.

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> verdict-bearing input — it proposes the findings the deterministic adjudicator
> turns into the report. Re-firing it on a wall-clock timer adds no signal: its
> output changes only when the **paper / ledger** changes, not with the clock.
> Schedule the *external wait that precedes it* — ledger built → audit **once**.
> (Mirrors ARIS's external-cadence doctrine.)

> The flagship instrument. Internal contradiction is the single most defensible
> thing you can check on an unknown submission: it needs no external GT, runs at L0
> (PDF-only), and is exactly where machine-generated papers crack — they hallucinate
> *local* coherence. Recall scales with the ledger: a PDF-text (L0) ledger extracts
> only number/scope spans, so the table/caption/method-drift checks gain teeth at L1
> (LaTeX), where tables and captions are actually extracted. Adapted from ARIS
> `paper-claim-audit`, reframed from "paper vs result files" to **"paper vs
> itself."** There is no external ground truth in this skill.

## Why this exists

An autoresearch pipeline (or rushed human) writes the abstract, the tables, the
method section, and the appendix in separate passes and never reconciles them. The
result is a paper that disagrees with **itself**:

- abstract quotes 85.3% accuracy; the best row of its own Table 2 is 84.7%;
- "improves by 16%" when 73.1 → 78.0 is +6.7% relative / +4.9 points;
- "mean over 5 seeds" where the number is the single best seed, and N=3 in the table;
- method section says "no test-time labels"; the experimental-setup paragraph loads
  gold labels for calibration;
- "comprehensive evaluation across diverse benchmarks" on two datasets, one domain.

None of this needs the code, the data, or a single external fact to detect — only
the paper, read against itself. That is why this skill is the flagship and the only
auditor that always runs: it **runs at L0** (no external GT), the level at which we
have the least to work with — though L0/PDF-text recall is bounded by what the
extractor recovers (number/scope spans only); the richer table/caption checks need
the L1 LaTeX ledger.

## Core principle

**Ledger-anchored, span-verified, paper-vs-itself, reviewer≠adjudicator.** Two
passes feed the pipeline:

1. a **deterministic** arithmetic pass (no model) — reproducible, the eval backbone;
2. a **fresh cross-model** semantic pass — meaning drift the arithmetic can't see.

Both emit findings conforming to `schemas/finding.schema.json`. **Every above-info
finding cites a ledger `claim_id` + a verbatim span** (`references/integrity-forensics-contract.md`
rules 1–2). The model **proposes**; `tools/adjudicate_findings.py` **decides**
(`references/reviewer-independence.md` Layer 2). This skill computes **no verdict**.

## How this differs from the other auditors (route correctly)

| Auditor | Question it answers | Level |
|---------|---------------------|------|
| **`consistency-audit`** (this) | **Does the paper contradict ITSELF / does described method = evaluated method?** | **L0 — intra-paper, no external lookup** |
| `experiment-forensics` | Are the reported numbers what the code actually computes? (fake GT, self-norm, phantom) | L2 |
| `baseline-comparison-audit` | Are the right baselines present, tuned, and is "SOTA" earned? | L0 stated / L2 verified |
| `citation-forensics` | Do the cited papers exist and support the claim made? | L0 |
| `proof-derivation-forensics` | Does the WRITTEN proof/derivation actually establish its theorem? (gap / circularity / invalid step / symbol drift / smuggled assumption) | L1 |
| `presentation-signals` | Surface "AI-flavor" hints (auxiliary, capped at minor) | L0 |
| `adversarial-case-builder` | Strongest evidence-bound rejection memo (no verdict weight) | any |

**Do NOT raise here** (hand off instead): code/result-level fraud → `experiment-forensics`
(needs L2); "first / SOTA / beats prior work" external truth → `baseline-comparison-audit`
+ `citation-forensics` (emit `needs_external_check`); citation existence/context →
`citation-forensics`; proof / derivation validity (a theoretical relation that must be
*derived*, not measured — gap / circularity / invalid step / symbol drift / smuggled
assumption) → `proof-derivation-forensics` (family G); surface/AI-flavor →
`presentation-signals`; the rejection memo → `adversarial-case-builder`. This skill
never reaches outside the paper.

## Constants & Reviewer Calling Convention

```
REVIEWER_MODEL          = gpt-5.5                  # different family from executor (Claude)
REVIEWER_REASONING      = xhigh                    # always; effort never lowers reviewer quality
REVIEWER_SANDBOX        = read-only                # detect-only; never mutate the paper
REVIEWER_CWD            = <paper-dir>              # so it can read claims.json + sources directly
THREAD_POLICY           = fresh mcp__codex__codex per run; NEVER mcp__codex__codex-reply
TAXONOMY_VERSION        = 0.5                      # references/hack-pattern-taxonomy.md
DETERMINISTIC_FINDINGS  = consistency-audit.deterministic.findings.json   # Step 1 (tool)
SEMANTIC_FINDINGS       = consistency-audit.findings.json                 # Step 4 (validated)
TRACE_POLICY            = forensic (never silently dropped)
TRACE_DIR               = .aris/traces/consistency-audit/<YYYY-MM-DD>_run<NN>/
```

- **Executor (Claude)** builds nothing of the judgment: it locates the ledger,
  passes **paths + the ledger + the checklist** to the reviewer, validates the
  reviewer's spans, and writes the findings file. It never summarizes the paper,
  pre-judges, or leaks an opinion into the prompt (`reviewer-independence.md`).
- **Reviewer (codex / gpt-5.5)** reads `claims.json` and the sources, proposes
  findings, and self-reports `false_positive_risk`. It is the evidence-extractor,
  not the judge.
- **Fresh thread per run.** If you fan out the checklist into groups for breadth,
  each group is a **new** `mcp__codex__codex` call — never `codex-reply` carrying one
  group's conclusions into another (the bias guard). `codex-reply` is intentionally
  absent from `allowed-tools`.

---

## Step 0 — Preconditions: locate the ledger, read the run level

The ledger is the **only** structure this skill reasons over. Resolve it and read
the observability level **L**, `paper_id`, and the claim count it was built at (each
Bash block is self-contained — shell state does not persist between calls, so
re-derive paths every step):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
# $ARGUMENTS is a paper-dir OR a claims.json path:
LEDGER="$ARGUMENTS"; [ -d "$LEDGER" ] && LEDGER="$LEDGER/claims.json"
# Only the NO-ARGUMENT case defaults to the CWD ledger. An EXPLICIT argument that
# resolves to a missing claims.json must NOT silently fall back to $(pwd) — that
# could audit the wrong paper; let the NO_LEDGER check below fire instead.
[ -z "$ARGUMENTS" ] && LEDGER="$(pwd)/claims.json"
python3 - "$LEDGER" <<'PY'
import json, sys, os
p = sys.argv[1]
if not os.path.isfile(p):
    sys.exit("NO_LEDGER: claims.json not found. Run /evidence-ledger FIRST "
             "(it writes artifact_manifest.json + claims.json).")
d = json.load(open(p, encoding="utf-8"))
print("LEDGER      =", os.path.abspath(p))
print("PAPER_DIR   =", os.path.dirname(os.path.abspath(p)) or ".")
print("PAPER_ID    =", d.get("paper_id", "?"))
print("RUN_LEVEL_L =", d.get("observability_level", 0))
print("CLAIMS      =", len(d.get("claims", [])))
PY
```

**Carry forward** the absolute `LEDGER` / `PAPER_DIR`, plus `L` and `PAPER_ID`, into
every step below.

**Failure / edge handling.**
- **`NO_LEDGER`** → stop and tell the user to run `/evidence-ledger` first. This skill
  never re-reads the raw PDF and invents its own structure (contract rule 1).
- **`CLAIMS == 0`** → the ledger has nothing to audit. Run Step 1 anyway (it emits
  `[]`), then **skip Steps 2–3** and write the empty semantic file directly —
  `printf '[]\n' > "$(dirname "$LEDGER")/consistency-audit.findings.json"` — record a
  trace note (Step 5), and stop. An empty findings array is a valid, non-silent
  output — the adjudicator reads it as "this dimension found nothing". **Do not**
  call the reviewer on an empty ledger.
- **Ledger `observability_level` is 2** → consistency checks run identically (they
  are intra-paper); the extra L2 power (paper-number↔result-file match, fake GT)
  belongs to `/experiment-forensics`, not here.

## Step 1 — Deterministic arithmetic pass (no LLM)

Pure arithmetic over the ledger; reproducible; runs before any model:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json from Step 0>"
python3 "$ROOT/tools/check_numeric_consistency.py" \
    --ledger "$LEDGER" \
    --out "$(dirname "$LEDGER")/consistency-audit.deterministic.findings.json"
# statistical self-consistency (GRIM / GRIMMER / statcheck) — also pure arithmetic,
# disjoint GRIM###/VAR###/STAT### ids; the orchestrator globs *.findings.json so this
# file is picked up automatically. z-tests are stdlib; t/F/chi2/r use optional scipy.
python3 "$ROOT/tools/check_stat_consistency.py" \
    --ledger "$LEDGER" \
    --out "$(dirname "$LEDGER")/consistency-audit.stat.findings.json"
```

This emits five pattern types, each already schema-valid, span-anchored,
`reviewer.deterministic: true`, and `observability_level_required: 0`:

| Pattern | id namespace | Severity / FP | What it catches |
|---------|-------------|---------------|-----------------|
| `HP-DELTA-ERROR` | `NUM###` | major / **low** | stated "improves by X%" contradicts its own two operands `(new−old)/old`, incl. relative-vs-absolute and reduction-direction confusion (±0.6 pt rounding tolerance). |
| `HP-NUM-INFLATE` | `HL###` | minor / **high** | a metric-bearing headline %-number in abstract/intro/conclusion appears in **no** extracted table cell. Only fires when ≥1 `table_cell` claim exists; a "look here" signal, not a verdict. |
| `HP-GRANULARITY-IMPOSSIBLE` | `GRIM###` | minor (major if headline) / **low** | a proportion reported over integer N that is not round(k/N) at the stated precision (GRIM); excludes macro/weighted/relative and non-count metrics. |
| `HP-VARIANCE-IMPOSSIBLE` | `VAR###` | major / **low–med** | a reported SD larger than a bounded metric can have at that mean (Bhatia–Davis); requires an explicit SD label, skips SEM/CI. |
| `HP-STAT-INCONSISTENCY` | `STAT###` | major (critical if headline) / **med** | a reported p that overstates the .05 significance its own test statistic supports (statcheck); z = stdlib, t/F/χ²/r = optional scipy. |

**Worked example — real output on the `delta_inflate` fixture.** Ledger claim `C003`
text is *"FooNet reaches 78.0\% accuracy, improving from a 73.1\% baseline to 78.0\%
accuracy, a 16.7\% relative improvement."* The tool emits (span shown exactly as it
appears in the JSON — LaTeX escapes preserved verbatim, which is what the anchor
gate matches against):

```json
{
  "finding_id": "NUM001",
  "skill": "consistency-audit",
  "pattern_id": "HP-DELTA-ERROR",
  "title": "Stated improvement contradicts its operands",
  "description": "Text states a 16.7% relative change, but 73.1->78 is 6.7% relative (+4.9 absolute points).",
  "severity": "major",
  "observability_level_required": 0,
  "evidence": [{
    "claim_id": "C003",
    "span": "FooNet reaches 78.0\\% accuracy, improving from a 73.1\\% baseline to 78.0\\% accuracy, a 16.7\\% relative improvement.",
    "location": {"file": ".../delta_inflate.tex", "line": 9, "section": "abstract"},
    "artifact_hash": "a0a6b6…e45804"
  }],
  "verdict_local": "fail",
  "reviewer": {"deterministic": true},
  "false_positive_risk": "low",
  "recommended_reviewer_action": "Ask the authors to reconcile the stated delta with the reported operands; verify relative-vs-absolute convention."
}
```

These deterministic findings are anchored and `observability_level_required: 0` by
construction, so they survive every adjudicator gate — do **not** re-validate,
re-ID, or mutate them.

**Failure handling.** If the tool errors, fix the invocation (run
`python3 "$ROOT/tools/check_numeric_consistency.py" --help`) — do not hand-fabricate
deterministic findings. An empty output (`[]`) is a valid result (no arithmetic
contradiction, or no tables were extracted to compare against); keep the file.

## Step 2 — Cross-model semantic pass (reviewer ≠ adjudicator)

The arithmetic layer cannot see *meaning* drift. First create this run's trace dir
(Step 5's layout) so the reviewer call can be persisted as it happens. Shell state
does **not** persist between Bash calls, so read the printed `TRACE_DIR` and reuse
that absolute path verbatim in Steps 2 and 5:

```bash
LEDGER="<abs path to claims.json from Step 0>"; D="$(dirname "$LEDGER")"
TBASE="$D/.aris/traces/consistency-audit/$(date +%F)"
NN=1; while [ -e "${TBASE}_run$(printf '%02d' "$NN")" ]; do NN=$((NN+1)); done
TRACE_DIR="${TBASE}_run$(printf '%02d' "$NN")"; mkdir -p "$TRACE_DIR"
echo "TRACE_DIR = $TRACE_DIR"   # carry this absolute path into Steps 2 and 5
```

Then open a **fresh** `mcp__codex__codex` thread (the Reviewer Calling Convention
above) and send it the checklist. The reviewer reads `claims.json` from its `cwd`; it
may re-open a source file to confirm a span, but **every finding must anchor to a
ledger `claim_id`**. Send EXACTLY (substitute the absolute `PAPER_DIR` and the `L`
value from Step 0):

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are an integrity-forensics reviewer auditing a research paper for INTERNAL
    self-consistency only — the paper against ITSELF. You have NO external ground
    truth and you do NOT judge whether results are "real": you find places where the
    paper contradicts itself, or where the method DESCRIBED differs from the method
    EVALUATED.

    INPUTS (in your working directory, read them directly):
      - claims.json  — the evidence ledger: the authoritative, span-anchored list of
        every checkable claim. This is the ONLY structure you reason over for
        navigation. Each claim has {claim_id, type, text_span (VERBATIM source text),
        location, value?}.
      - the source files the ledger references — you MAY re-open them to confirm a
        span is real, but you may NOT introduce a claim that is not in the ledger.
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.

    HARD RULES (a finding that breaks any of these is worthless):
    1. ANCHOR. Every finding above severity "info" MUST carry >=1 evidence entry
       {claim_id, span}, where claim_id EXISTS in claims.json and span is a VERBATIM
       substring of THAT claim's text_span — copied character-for-character INCLUDING
       LaTeX escapes like \% and \, (do NOT unescape, normalize, or paraphrase). The
       anchor check is a whitespace-normalized substring match (`span in claim`); an
       unescaped or reworded span will fail and be demoted to info. If you cannot
       quote such a span, keep the finding at "info" or drop it.
    2. DISCREPANCY, NOT ACCUSATION. description and recommended_reviewer_action
       describe what a human should CHECK or ASK. Never write "reject", "fabricated",
       or "the authors faked X".
    3. OBSERVABILITY. Set observability_level_required = the LOWEST tier at which the
       discrepancy is DECIDABLE. A purely textual contradiction (text vs text/table
       inside the paper) = 0. Anything that needs the CODE or RESULT FILES to confirm
       = 2 (it will auto-demote on a PDF-only run — that is correct, not a loss).
    4. HONEST FP RISK. Set false_positive_risk truthfully. Legit "best config"
       labels, deliberately-labeled ablations, standard rounding, deterministic
       metrics, and honestly-labeled pilots are COMMON false positives — say so.
    5. HAND OFF EXTERNAL CLAIMS. For "first / SOTA / state-of-the-art / beats all
       prior work" that internal text cannot settle: do NOT rule. Set
       verdict_local = "needs_external_check" and requires_external_check = true.
    6. pattern_id MUST be one of the HP-* ids listed in the checklist.

    CHECKLIST (run every item; one finding per concrete discrepancy):
     1. NUMBER COHERENCE — the same metric+setting reported with DIFFERENT values
        across abstract / intro / body / table / appendix, or a headline value more
        favorable than its own table row.            [HP-NUM-INFLATE, HP-APPENDIX-CONTRA]
        severity: critical if the contradicted value is the headline claim; else
        major. FP: a genuinely different, NAMED config; standard rounding. level 0.
     2. DELTA ARITHMETIC — "improves by X%": recompute (new-old)/old AND absolute
        points; flag if X disagrees beyond rounding, or relative/absolute are
        conflated to inflate.                                       [HP-DELTA-ERROR]
        severity: major; critical if the corrected delta deflates a "large/
        significant" framing. FP: abs-vs-rel stated explicitly; rounding. level 0.
        (A deterministic pass already caught the single-sentence cases; you catch
        deltas spread ACROSS sentences/tables a regex cannot pair.)
     3. AGGREGATION DRIFT — text says "mean over N seeds" but the number matches the
        BEST seed, or N in text != N in the table; variance hidden.   [HP-AGG-DRIFT]
        severity: major; critical if variance is hidden and the gap is within
        plausible seed spread. FP: best AND mean both reported; labeled pilot. level 0.
     4. DENOMINATOR / POPULATION DRIFT — two tables average over DIFFERENT subsets
        ("all tasks" vs "tasks where the method applies") but the body treats them as
        one number.                                                  [HP-DENOM-DRIFT]
        severity: major. FP: subsets clearly delimited and not conflated. level 0.
     5. METRIC DIRECTION / UNIT — % vs absolute points mixed; a lower-is-better metric
        described as higher-is-better; an improvement stated in the wrong direction.
                                                              [HP-UNIT-DIR-MISMATCH]
        severity: minor, or major if it FLIPS a comparison. FP: an unconventional but
        internally consistent, clearly-defined unit. level 0.
     6. METHOD IDENTITY DRIFT — the body describes method A, but the experimental-
        setup text describes A-lite / A+oracle / extra training data / a different
        backbone than claimed.                                      [HP-METHOD-DRIFT]
        severity: critical (this breaks the central claim). FP: a deliberately-labeled
        ablation varying the method. level 0 for a text-vs-text contradiction; set
        level 2 if confirming what was ACTUALLY run needs the code/results.
     7. ABLATION ATTRIBUTION — a gain credited to component X, but no ablation
        ISOLATES X (X is always bundled with Y).                 [HP-ABLATION-ATTRIB]
        severity: major. FP: an isolating ablation exists elsewhere; the component is
        theoretically inseparable and the paper says so. level 0.
     8. CAPTION vs CONTENT — a figure/table caption describes a method, axis, or N
        that the content does not show.                          [HP-CAPTION-MISMATCH]
        severity: minor, unless the caption is the ONLY place a key result is stated.
        FP: a loose multi-panel summary. level 0 (text) / 1 (source).
     9. SCOPE vs EVIDENCE — "comprehensive / extensive / robust / general / across the
        board" on a thin actual scope (few datasets, N=1-2, one domain).
                                                                  [HP-SCOPE-INFLATE]
        severity: minor->major. FP: scope genuinely broad; qualifiers present.
        level 0. (If the language is specifically "SOTA/first", ALSO set
        needs_external_check and hand to baseline/citation forensics.)
    10. THEOREM SCOPE DRIFT — abstract/title advertise generality; the formal result
        holds only under strong/unstated assumptions.       [HP-THEOREM-SCOPE-DRIFT]
        severity: major. FP: assumptions stated up front AND acknowledged in the
        abstract. level 0. (Flag the internal scope mismatch only; route the headline
        framing to adversarial-case-builder.)
    11. ARGUMENT-CHAIN COHERENCE — the chain the paper claims to walk — motivation
        (intro) -> mechanism (method) -> what the experiments MEASURE — has a
        SUBSTANTIVE missing link: the problem motivated is not the one the method
        addresses, or the method's claimed mechanism does not predict what the
        experiments test. This is about the CONTENT of the chain, not its prose —
        mere stylistic disjointedness / "前言不搭后语" reading / filler wording is the
        surface tell HP-NARRATIVE-ARC-BREAK (presentation-signals, capped minor), NOT this.
                                                            [HP-ARGUMENT-CHAIN-BREAK]
        severity: major; critical if the headline contribution rests on the broken
        link. FP: a dense-but-valid argument the reader must work through; a modular
        paper with explicit cross-references; non-native phrasing. level 0. If the
        missing link is a THEORETICAL relation that must be DERIVED (not narrated), do
        NOT adjudicate the math here — route it to proof-derivation-forensics (family G).
    12. CAUSAL / EVIDENCE LEAP — a relation is CONCLUDED that no experiment in the
        paper actually tests: "A and B correlate, therefore equivalent / causal"; the
        paper studies C but concludes "D affects C" with no experiment that VARIES D;
        equivalence or causation asserted from a correlation or a single setting.
                                                            [HP-CAUSAL-EVIDENCE-LEAP]
        severity: major; critical if it is the central claim. FP: the supporting
        experiment exists elsewhere in the paper (cite it); a deliberately
        observational study that does not claim causation. level 0 (the unsupported
        leap is visible in the text); set level 2 only if confirming NO run varies D
        needs the code/results. If the relation is instead established THEORETICALLY
        (a proof/derivation is given), it is NOT an evidence leap — it is a proof
        obligation: route to proof-derivation-forensics (family G).
    13. NAME / ACRONYM DRIFT — the SAME load-bearing component, method, or module is named
        or expanded INCOMPATIBLY across the paper: one acronym defined with two different
        expansions, or one component referred to by two incompatible names/acronyms
        (abstract ↔ method ↔ experiments), so a reader cannot tell they are the same thing.
                                                            [HP-ACRONYM-DRIFT]
        severity: minor; major if the drift makes a central method/result ambiguous. FP: a
        standard acronym reused for different things; author-declared overloading; a local
        scoped abbreviation; verbose names / bold-spam ALONE (that is the surface tell
        HP-JARGON-STUFF, presentation-signals, NOT this). Require the two spans to name the
        SAME object and be genuinely incompatible. level 0.
    BONUS. SUSPICIOUS REGULARITY — numbers across rows related by a too-clean
        arithmetic pattern (a constant additive/multiplicative offset, implausibly
        smooth monotonicity, identical decimals across unrelated settings).
                                                          [HP-SUSPICIOUS-REGULARITY]
        At L0/L1 this is ALWAYS severity "minor", false_positive_risk "high",
        observability_level_required 2 (so a PDF-only run auto-demotes it). It is a
        PROMPT TO CHECK, never a "fabricated" grade; it rises to major only at L2
        against the real files. FP: deterministic metrics, small integer scores,
        rounding coincidence, a real linear trend.

    OUTPUT: a single JSON array, and NOTHING ELSE (no prose, no code fence). Each
    element conforms to schemas/finding.schema.json:
      {
        "finding_id": "F001",
        "skill": "consistency-audit",
        "pattern_id": "HP-...",
        "title": "short, neutral",
        "description": "the discrepancy, in reviewer-facing language",
        "severity": "critical|major|minor|info",
        "observability_level_required": 0,
        "evidence": [{"claim_id": "C0xx", "span": "verbatim substring of that claim",
                      "location": {"file": "...", "section": "..."}}],
        "verdict_local": "fail|warn|clean|needs_external_check",
        "requires_external_check": false,
        "false_positive_risk": "low|medium|high",
        "recommended_reviewer_action": "what to CHECK or ASK — never 'reject'"
      }
    If you find no discrepancy for an item, simply emit nothing for it. An empty
    array [] is a valid, honest result.
```

Immediately persist the reviewer's raw response with the **Write** tool to
`$TRACE_DIR/001-semantic-consistency.response.md` (the dir you just created) before
parsing. It is the forensic record and the input Step 3 reads. (Write the other three
trace files now or in Step 5 — see Step 5 for the exact set.)

**Failure handling.**
- *MCP stall / hang* (common in long sessions): re-invoke the **identical** prompt
  as a **fresh** `mcp__codex__codex` call (gpt-5.5, xhigh) — never `codex-reply`.
- *Reviewer returns prose, not a JSON array*: the Step 3 validator already extracts
  the outermost `[...]`; if there is none, re-ask once with "Output ONLY the JSON
  array, nothing else." Do not hand-author findings on the reviewer's behalf.
- *(Optional fan-out for breadth)*: for a long paper or `— effort: max`, split the
  checklist into groups and issue each as a **separate fresh** `mcp__codex__codex`
  call; concatenate the arrays. Splitting into fresh threads is fine; carrying
  context across them via `codex-reply` is not.

## Step 3 — Validate + anchor (the anti-hallucination gate)

The executor enforces the ANCHOR gate **before** keeping anything — exactly the rule
`tools/adjudicate_findings.py` re-applies, so nothing you keep gets silently
rejected downstream. The span must be a verbatim, whitespace-normalized **substring
of** the cited claim (`span in base`, never `base in span` — appending hallucinated
text to a real claim must fail):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"
PROPOSED="<abs path to the saved raw reviewer response from Step 2>"
OUT="$(dirname "$LEDGER")/consistency-audit.findings.json"
python3 - "$LEDGER" "$PROPOSED" "$OUT" <<'PY'
import json, re, sys
ledger_path, proposed_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

def nw(s):                                   # mirror adjudicator _norm_ws (whitespace only)
    return " ".join((s or "").split())

# fallback observability level if the reviewer omitted it (taxonomy 0.5 decidable tier)
OBS = {"HP-NUM-INFLATE":0,"HP-APPENDIX-CONTRA":0,"HP-UNIT-DIR-MISMATCH":0,
       "HP-AGG-DRIFT":0,"HP-DENOM-DRIFT":0,"HP-METHOD-DRIFT":0,"HP-ABLATION-ATTRIB":0,
       "HP-CAPTION-MISMATCH":0,"HP-SCOPE-INFLATE":0,"HP-THEOREM-SCOPE-DRIFT":0,
       "HP-ARGUMENT-CHAIN-BREAK":0,"HP-CAUSAL-EVIDENCE-LEAP":0,"HP-ACRONYM-DRIFT":0,
       "HP-DELTA-ERROR":0,"HP-SUSPICIOUS-REGULARITY":2}
SURFACE = {"HP-DUP-TABLE","HP-THIN-FLOAT","HP-LLM-FIGURE","HP-PAGE-PADDING",
           "HP-JARGON-STUFF","HP-AI-FLAVOR"}   # owned by presentation-signals; drop here
SEV = {"critical","major","minor","info"}
VL  = {"fail","warn","clean","needs_external_check"}
FPR = {"low","medium","high"}
ABOVE_INFO = {"critical","major","minor"}

ledger = json.load(open(ledger_path, encoding="utf-8"))
claims = {c["claim_id"]: c for c in ledger.get("claims", []) if c.get("claim_id")}

raw = open(proposed_path, encoding="utf-8").read()
m = re.search(r"\[.*\]", raw, re.S)          # tolerate prose / code-fence wrapping
proposed = json.loads(m.group(0) if m else raw)
if isinstance(proposed, dict):               # tolerate {"findings": [...]}
    proposed = proposed.get("findings", [])

kept, dropped, demoted = [], 0, 0
n = 0
for f in proposed:
    if not isinstance(f, dict):
        dropped += 1; continue
    pid = f.get("pattern_id")
    if pid in SURFACE:                       # surface signals belong to presentation-signals only
        dropped += 1; continue
    n += 1
    f["finding_id"] = f"F{n:03d}"
    f["skill"] = "consistency-audit"
    # enum hygiene: any illegal value -> safe default
    if f.get("severity") not in SEV: f["severity"] = "info"
    if f.get("verdict_local") not in VL: f["verdict_local"] = "warn"
    if f.get("false_positive_risk") not in FPR: f["false_positive_risk"] = "high"
    if f["verdict_local"] == "needs_external_check":
        f["requires_external_check"] = True
    # MANDATORY floor: HP-SUSPICIOUS-REGULARITY can never shout "fraud" from a table
    # alone — pin it to minor / fp:high / req:L2 (auto-demotes on a PDF-only run),
    # overriding whatever the reviewer filled in (see "Observability honesty").
    if pid == "HP-SUSPICIOUS-REGULARITY":
        if f["severity"] in ("critical", "major"): f["severity"] = "minor"
        f["false_positive_risk"] = "high"
        f["observability_level_required"] = 2
    # ANCHOR gate: span must be a verbatim, ws-normalized SUBSTRING of its cited claim
    anchored = []
    for ev in (f.get("evidence") or []):
        if not isinstance(ev, dict):             # tolerate a stray string/None evidence item
            continue
        cid, span = ev.get("claim_id"), nw(ev.get("span",""))
        c = claims.get(cid)
        if c and span and span in nw(c.get("text_span","")):   # span IN claim, not claim IN span
            ev.setdefault("location", c.get("location", {}))    # enrich for human navigation
            ev.setdefault("artifact_hash", c.get("evidence_anchor",""))
            anchored.append(ev)
    f["evidence"] = anchored
    if f["severity"] in ABOVE_INFO and not anchored:
        f["severity"] = "info"; demoted += 1                    # unanchored -> info (adjudicator would too)
    # observability: must be a real int 0-3 (reject JSON bool, which is an int subclass)
    olr = f.get("observability_level_required")
    if isinstance(olr, bool) or not isinstance(olr, int) or not (0 <= olr <= 3):
        f["observability_level_required"] = OBS.get(pid, 2)  # unknown pattern -> fail-closed L2 (auto-demotes at L0/L1)
    # cross-model provenance (reviewer-independence: this is a proposal, not a verdict)
    f["reviewer"] = {"model": "gpt-5.5", "reasoning": "xhigh", "deterministic": False}
    kept.append(f)

json.dump(kept, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"validated {len(kept)} semantic findings "
      f"({demoted} demoted to info for unanchored span, "
      f"{dropped} dropped: surface-pattern/malformed) -> {out_path}")
PY
```

**Scope of this gate: anchoring + schema hygiene** — verbatim-span anchoring, enum
coercion, surface-pattern rejection, observability fallback, and cross-model
provenance — so every kept finding is well-formed and honestly anchored. It does
**not** compute the verdict, the FP-risk cap, or the observability *downgrade*
against the run level; those belong to `tools/adjudicate_findings.py`, the single
decider. Surface patterns (`HP-DUP-TABLE`, `HP-AI-FLAVOR`, …) are **dropped** (not
capped) here because they are owned by `presentation-signals` and are never this
skill's to emit.

**Failure handling.** A `JSONDecodeError` means the reviewer output was malformed →
re-run Step 2 with the strict-JSON reminder. If a finding loses all evidence, it is
*kept as info* (never silently dropped — the forensic record stays).

## Step 4 — Emit (two files, no merge)

Step 1 wrote `consistency-audit.deterministic.findings.json`; Step 3 wrote
`consistency-audit.findings.json` (validated semantic findings only). **Keep them
separate. Do NOT copy the deterministic findings into the semantic file** — the
orchestrator concatenates every `*.findings.json`, and both files match the glob, so
merging would double-count them and could wrongly flip the verdict. The two files
hold disjoint findings with disjoint id namespaces — deterministic `NUM###` / `HL###`
vs semantic `F###` — so concatenation is exactly the full set, once.

If the semantic pass found nothing (or `CLAIMS == 0`), `consistency-audit.findings.json`
is `[]` — write it anyway. **Silent skip is forbidden**: the orchestrator and the
standalone adjudicate command both expect the file to exist at a predictable path.

## Step 5 — Trace (forensic; never silently dropped)

You already created `$TRACE_DIR` in Step 2
(`.aris/traces/consistency-audit/<date>_run<NN>/`, `NN` from `01`). This repo ships no
`save_trace.sh`, so use the **Write** tool to write these four files into it (the
`response.md` was already saved in Step 2):

```
$TRACE_DIR/
  run.meta.json                          # {skill, paper_id, run_level_L, taxonomy_version, generated_at}
  001-semantic-consistency.request.json  # the exact prompt sent (paths + checklist, no summaries)
  001-semantic-consistency.response.md   # the FULL raw reviewer response (input to Step 3)
  001-semantic-consistency.meta.json     # {model:"gpt-5.5", reasoning:"xhigh", thread_id, sandbox:"read-only"}
```

The `request.json` is the independence audit trail — it must show the executor sent
only **paths + the ledger + the checklist**, never a digest of the paper. Paste the
actual codex `thread_id` into the per-call `.meta.json`.

## Step 6 — Hand off, or adjudicate standalone

Within `/anti-autoresearch`, stop here: the orchestrator globs every
`*.findings.json`, runs the adjudicator over the union of all skills' findings, and
emits `REPORT.md` + `report.json`. When running this skill **alone**, you may produce
the report yourself — `--ledger` is **required** (it re-verifies each finding quotes a
real ledger span; the adjudicator will not run without it, and its anchor gate is
itself fail-closed — an above-info finding it cannot anchor is demoted to `info`):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"; D="$(dirname "$LEDGER")"
python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "$D/consistency-audit.deterministic.findings.json" \
               "$D/consistency-audit.findings.json" \
    --ledger "$LEDGER" \
    --paper-id "<PAPER_ID>" --observability-level <L> --taxonomy-version 0.5 \
    --out "$D/report.json" --md "$D/REPORT.md"
```

The adjudicator applies, in order: ANCHOR → OBSERVABILITY → FP-RISK → MEMO → SURFACE
gates, then computes `overall_verdict` ∈ {CLEAN_GIVEN_EVIDENCE, SOFT_FLAGS,
HARD_FLAGS} (any span-anchored **critical** decidable at `L` → HARD_FLAGS). No model
is in the final decision. Treat a single-skill report as a PREVIEW — the paper's
verdict comes from the orchestrator over all dimensions.

## Output contract

This skill **always** writes, into the ledger's directory:

- `consistency-audit.deterministic.findings.json` — Step 1, a JSON array
  (`schemas/finding.schema.json`); arithmetic findings, `reviewer.deterministic:true`.
- `consistency-audit.findings.json` — Step 4, a JSON array; validated semantic
  findings (or `[]`). Each above-info finding carries `evidence[].claim_id` +
  verbatim `span` and an `observability_level_required`.
- `.aris/traces/consistency-audit/<date>_run<NN>/` — Step 5, the raw reviewer call.

It writes **no verdict and no report** of its own — `report.json` / `REPORT.md` come
only from `tools/adjudicate_findings.py` (Step 6 / the orchestrator). The
human-readable rendering is the orchestrator's job, not this skill's.

## Key rules

- **No span → no severity.** Every `critical`/`major`/`minor` finding must quote a
  verbatim substring of a real ledger claim. Enforced by the executor (Step 3) and
  again by the adjudicator; unanchored findings are demoted to `info`, never deleted.
- **Span direction + escapes.** Anchoring is `span in claim.text_span`
  (whitespace-normalized **only**), never the reverse. Quote LaTeX escapes (`\%`,
  `\,`) exactly; un-escaping breaks the match.
- **Reviewer ≠ adjudicator.** The model proposes findings; `adjudicate_findings.py`
  decides the verdict. This skill emits findings only.
- **Cross-model, fresh thread.** Reviewer is a different family (gpt-5.5 xhigh);
  every run is a new `mcp__codex__codex` thread; `codex-reply` is never used.
- **Observability honesty.** A discrepancy that needs code/results to confirm gets
  `observability_level_required: 2` so a PDF-only run auto-demotes it.
  `HP-SUSPICIOUS-REGULARITY` is **mandatorily** `minor` / `fp:high` / `req:2` — you
  cannot shout "fraud", or grade results as synthesized, from a table alone.
- **Discrepancy, not accusation.** Output asks a reviewer to *check/ask*, never to
  reject; the tool is agnostic to authorship — it audits integrity, not provenance.
- **Hand off external claims.** "SOTA / first" → `needs_external_check` +
  `requires_external_check: true`; to baseline / citation forensics, not a guess.
- **Taxonomy is a mapping layer, not a detector.** Detect from the ledger +
  checklist, then map to a `pattern_id` (v0.4); never start from "go find HP-X."
- **Two files, no merge.** Deterministic and semantic findings stay in separate
  files (disjoint ids) to avoid double-counting under the orchestrator's glob.
- **Detect-only.** Never edit the audited paper (reviewer sandbox is read-only).
- **Reproducible.** Same ledger + same findings → same verdict, no model in the loop.

## When NOT to use this skill

- **No `claims.json` yet** → run `/evidence-ledger` first; this skill never invents
  structure from the raw PDF.
- **You need code/result-level fraud** (fake GT, self-normalization, phantom
  numbers) → `/experiment-forensics` at **L2**; consistency-audit can only raise
  those as info-level "needs code" signals.
- **You need to verify "SOTA / first" or baseline integrity** →
  `/baseline-comparison-audit` (+ `/citation-forensics`); hand off via
  `needs_external_check`.
- **You need citation existence / wrong-context** → `/citation-forensics`.
- **You need to audit whether a PROOF/derivation actually holds** (a theorem with a
  missing obligation, a circular argument, an invalid step, a drifted symbol, or a
  smuggled assumption) → `/proof-derivation-forensics` (**family G**, L1); a
  theoretical relation that should be *derived* is its dimension, not this skill's.
- **You want an AI-text / "looks machine-written" verdict** → out of scope. Surface
  hints live in `/presentation-signals` (auxiliary, capped at minor); this repo is
  **not** an AI-text classifier.
- **On a timer** → never `/loop` / `/schedule` / `CronCreate` this skill; re-fire
  only when the paper or ledger changes (see the fence at the top).