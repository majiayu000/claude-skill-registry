---
name: ai-style-impressions
description: "Transparent, itemized impressions of AI-generated WRITING STYLE — the repo's ONLY non-integrity track. Two passes: a deterministic defensive-hedge density screen (tools/check_ai_style.py, AIS-DEFENSIVE-HEDGE) plus a fresh cross-model GROSS-cases-only semantic pass over the 13 AIS-* style tells (broken narrative arc, LLM phrase tics, jargon-stuffing, invented codenames, clause/formula walls, gratuitous pseudocode, bullet overuse, bold-module spam, restatement loops, focus drift, single-style figures, appendix dumping). Every finding is named, LOCATED, span-anchored to the evidence ledger (claims.json), carries not_integrity_finding:true + false_positive_risk:high + an fp_case, and gets ZERO verdict weight: the adjudicator forces it to info, excludes it from overall_verdict, and renders it in a SEPARATE report section. NOT an AI-text classifier — no scores, no \"this is AI-written\", no authorship probability; a paper can be CLEAN_GIVEN_EVIDENCE and still list many. Emits ai-style-impressions.findings.json; computes NO verdict; if a tell is actually substantive it routes to the integrity auditor. Triggers: \"AI style\", \"vibe check\", \"writing fingerprint\", \"AI 文风\", \"vibe paper\"."
argument-hint: [paper-dir | claims.json]
allowed-tools: Bash(*), Read, Write, mcp__codex__codex
---

# AI Writing-Style Impressions — itemized, located, ZERO verdict weight (NOT integrity findings)

Surface AI writing-**style** impressions for: **$ARGUMENTS** (requires `claims.json`
from `/evidence-ledger`). Emit span-anchored `ai-style-impressions.findings.json`.
Every finding here is an **impression** with **ZERO verdict weight** — this skill
proposes **no integrity finding** and computes **no verdict**.

> ⚠️ **This is the repo's ONLY non-integrity output, and it is non-integrity by
> construction.** AIS findings are transparent, itemized impressions of AI-generated
> *writing style*. The adjudicator (`tools/adjudicate_findings.py`) gives **every** AIS
> finding **ZERO verdict weight** — it is forced to `info`, excluded from
> `overall_verdict`, and rendered in a **separate** report section,
> *"AI Writing-Style Impressions — NOT integrity findings · ZERO verdict weight"*. **A
> paper can be `CLEAN_GIVEN_EVIDENCE` and still list many AIS impressions.** These are
> **not** factual/integrity inconsistencies and imply **no authorship probability**. We
> are **not** an opaque AI-text classifier: no scores, never *"this is AI-written"* /
> *"likely AI-generated"*. Every finding is a **named, located, itemized** observation
> with an `fp_case`. For authorship detection use a dedicated tool (Pangram / GPTZero /
> Binoculars) — that is out of scope here, by design.

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> report-input — it proposes the impressions the deterministic adjudicator renders in
> the zero-weight AIS section. Re-firing it on a wall-clock timer adds no signal: its
> output changes only when the **paper / ledger** changes, not with the clock. Schedule
> the *external wait that precedes it* — ledger built → check **once**. (Mirrors ARIS's
> external-cadence doctrine.)

## Why this exists

Real reviewers say the quiet part out loud about *style*: *"这一看就是大模型写的味儿"* (this
reads like an LLM wrote it), *"满篇 'it is worth noting' / '值得注意的是'"* (every
paragraph hedges with "it is worth noting"), *"通篇 not only…but also、一堆 however/
therefore"* (chains of however/therefore/moreover), *"堆术语，论证是空的"* (term-stuffing with
no argument under it), *"实验叫 'Experiment Set Gamma'，从没定义"* (an undefined internal
codename used as if defined), *"图都是一个味儿的 AI 生成图"* (the figures share one generated
visual grammar), *"附录像把跑的 trace 一股脑倒进去"* (the appendix reads like a dumped run
trace). An autoresearch pipeline (or a rushed human leaning on an assistant) produces
exactly these *style* artifacts.

These signals are **real** in the sense that reviewers react to them — but they are
**not evidence of misconduct, and not evidence of authorship.** Honest LLM-assisted
writing produces phrase tics; non-native English produces awkward transitions; a house
style produces bold module names and consistent figures; a careful author hedges in the
Limitations. So this skill's contract is narrow and permanent:

- it emits **only** the 13 `AIS-*` style patterns, each as an **impression**;
- it tags **every** finding `not_integrity_finding: true` + `false_positive_risk: high`
  and attaches an `fp_case` (the legitimate, not-necessarily-AI explanation);
- it **never** says a paper is "AI-generated", never assigns a probability or a score,
  and **never** moves the verdict;
- **silence is the common, correct output** — most papers should produce few or zero
  AIS impressions.

It exists so a reviewer's *style* reactions become **named, located, checkable
impressions** instead of an unfalsifiable "vibe" — and so that whenever a style tell is
actually a **substantive** problem, this skill **hands it to the right integrity
auditor** rather than smuggling it in under a style label.

## Core doctrine (the non-negotiables)

**Ledger-anchored, span-verified, ZERO verdict weight, NOT an authorship classifier,
reviewer ≠ adjudicator.** Two passes feed the pipeline:

1. a **deterministic** pass (no model) — the one objectively computable style signal: a
   conservative **defensive-hedge density screen** (`AIS-DEFENSIVE-HEDGE`), which fires
   only on a genuine pattern (≥4 distinct strong-template hedge sentences across ≥2
   non-excluded sections **and** ≥25% of all scope sentences). It flags the **recurrence
   of the hedge SHAPE**, never who wrote it (`tools/check_ai_style.py`);
2. a **fresh cross-model GROSS-cases-only** semantic pass — the 13 judgment-call style
   tells, each span-anchored, `not_integrity_finding: true`, `false_positive_risk:
   high`, with an `fp_case`. (`AIS-DEFENSIVE-HEDGE` is **dual**: deterministic for the
   pervasive case above + this semantic pass for the sub-threshold/qualitative posture
   the density screen misses.)

Both emit findings conforming to `schemas/finding.schema.json` (plus the AIS-only fields
`not_integrity_finding` / `fp_case`). **Every above-info finding cites a ledger
`claim_id` + a verbatim span** (`references/integrity-forensics-contract.md` rules 1–2).
Because the ledger holds only *checkable* claims (numbers, scope, captions, citations,
table cells) and almost no free prose, a style impression that cannot land on an
extracted claim **stays `info`** — a note, never an above-info impression. The model
**proposes**; `tools/adjudicate_findings.py` **decides** — and for AIS it always decides
the same thing: **info, zero weight, separate section** (`reviewer-independence.md`
Layer 2). This skill computes **no verdict** and proposes **no integrity finding**.

## How this differs from the other auditors (route correctly)

| Auditor | Question it answers | Verdict weight |
|---------|---------------------|----------------|
| **`ai-style-impressions`** (this) | **What AI writing-STYLE tells does a reviewer notice? Named, located, itemized impressions — NOT integrity** | **ZERO (forced to `info`, separate report section, excluded from `overall_verdict`)** |
| `presentation-signals` | Checkable *surface* tells (dup tables, thin/LLM figures, page padding, leftover pipeline strings) | capped at `minor` (`SOFT_FLAGS` at most) |
| `consistency-audit` | Does the paper contradict ITSELF / described method = evaluated method? | full |
| `experiment-forensics` | Are the reported numbers what the code computes? (fake GT, self-norm, phantom — L2) | full |
| `baseline-comparison-audit` | Right baselines present, tuned, "SOTA" earned? | full |
| `citation-forensics` | Do the cited papers exist + support the claim they are used for? | full |
| `eval-design-forensics` | Evaluation validity (leakage / judge bias / selective reporting)? | full |
| `proof-derivation-forensics` | Proof gaps / circularity / invalid steps / undefined notation? | full |
| `adversarial-case-builder` | Strongest evidence-bound rejection memo | ZERO (advisory memo) |

**Stay in lane.** This skill emits **only** the 13 `AIS-*` style patterns — nothing
else. An `AIS-*` impression is the *lowest-stakes* thing in the report by construction
(it carries no verdict weight at all); **never** use it to carry a substantive
accusation. When a style tell is actually a substantive integrity problem, **hand it
off** (do not encode it as an AIS impression):

| Pattern (`AIS-*`) | The style impression (gross cases only) | Not-necessarily-AI (high FP — the `fp_case`) | If it is actually SUBSTANTIVE → route to |
|-------------------|------------------------------------------|----------------------------------------------|------------------------------------------|
| `AIS-NARRATIVE-ARC-BREAK` | abrupt 1–2¶ intro / dump-like or vague abstract; no background→contribution→evidence arc | terse-but-clear abstract; non-native phrasing; field conventions | argument chain truly breaks → `HP-ARGUMENT-CHAIN-BREAK` (`consistency-audit`) |
| `AIS-LLM-PHRASE-TICS` | generic LLM tics overused ("it is worth noting" / "值得注意的是" / "意义在于", "not only…but also", chains of however/therefore/moreover, "therefore" mid-sentence, clichéd em-dash/semicolon, flowery empty adverbs like *elegantly* / *theoretically*) | honest LLM-assisted writing; non-native English; house style (**HUGE FP** — gross cases only) | **never routes** (pure style) |
| `AIS-DEFENSIVE-HEDGE` *(also Step 1)* | pervasive "we do not claim…" / "not X but rather Y" defensive framing instead of stating what was done | one scoping sentence; Limitations hedges are expected; **some venues penalize the ABSENCE of caveats** | a hedge reveals a real scope/eval limitation → `HP-SCOPE-INFLATE` (B) / `eval-design-forensics` (H) |
| `AIS-JARGON-STUFF` | dense term-stuffing where the surrounding argument carries no content | genuinely dense, correct technical writing (**very high FP**) | **never routes** |
| `AIS-INVENTED-CODENAME` | undefined internal-project-flavored run/experiment codename used as if defined (e.g. "Experiment Set Gamma") | legitimate named methods / benchmarks / release tags | points to a missing results file → `HP-MISSING-REPRO-ARTIFACT` / `HP-PHANTOM-RESULT` (D) |
| `AIS-CLAUSE-FORMULA-WALL` | fragmented "short clause then a wall of formulas"; formulas dumped without prose connective | dense-but-correct theory; field norms | a load-bearing symbol is actually UNDEFINED → `HP-UNDEFINED-NOTATION` (G) |
| `AIS-GRATUITOUS-PSEUDOCODE` | pseudocode/algorithm blocks that merely restate the prose / add no operational content | genuinely helpful algorithm listings | the algorithm CONTRADICTS the described method → `HP-METHOD-DRIFT` (`consistency-audit`) |
| `AIS-BULLET-LIST-OVERUSE` | prose organized as many bullets; sequential/progressive logic flattened into parallel-looking bullets | legitimate enumerations; checklists | **never routes** |
| `AIS-BOLD-MODULE-SPAM` | verbose module names with excessive bolding / acronym staging | reasonable emphasis; defined acronyms | the SAME module gets incompatible abbreviations → `HP-ACRONYM-DRIFT` (B, `consistency-audit`) |
| `AIS-RESTATE-OVERCLAIM` | rhetorical restatement loop — repeatedly re-asserting "we propose an X / we do an X" | legitimate signposting | the claim EXCEEDS the evidence → `HP-SCOPE-INFLATE` (B) / family H |
| `AIS-FOCUS-DRIFT` | high-level motivation suddenly pivots to a minor implementation detail / over-emphasizes an unnecessary requirement | modular paper with explicit cross-refs | the motivation→method→experiment chain substantively breaks → `HP-ARGUMENT-CHAIN-BREAK` (B) |
| `AIS-SINGLE-STYLE-FIGURES` | figures share a generic generated visual grammar / single-style AI illustrations | legitimate consistent house figure style; conceptual teasers | checkable figure-vs-content thinness stays `HP-LLM-FIGURE` / `HP-THIN-FLOAT` (family F, `presentation-signals`) |
| `AIS-APPENDIX-DUMPING-GROUND` | appendix reads like unintegrated trace / dumping; AI-trace heavy | legitimately long supplementary detail | CONTRADICTS the main text → `HP-APPENDIX-CONTRA` (B); exact assistant/template artifact → `HP-PIPELINE-ARTIFACT` (F); affects reported data → family D |

(The pure-style ids above migrated **out of** taxonomy §F into this zero-weight AIS
track in **v0.5**; see `DEPRECATED_STYLE_PATTERNS` in `tools/adjudicate_findings.py`,
which keeps the old §F ids as deprecated aliases forced to zero weight so a stale
`findings.json` can never push them to `SOFT_FLAGS`.)

## What this skill REFUSES to emit (even as an impression)

These are **never** emitted, not even as an `info` note. They are unfalsifiable, or
they are authorship claims, or they are aesthetics — none is a *located, repeated,
named* observation:

- **any standalone single-punctuation tell** — one em-dash, one semicolon, one adverb.
  A style impression is about **recurrence at a location**, never a single character;
- **generic non-native English / awkward prose** — that is a writing-quality opinion,
  not an AI-style tell, and is a massive FP for international authors;
- **"this is AI-written" / any authorship probability / any classifier score** — out of
  scope by design; we audit style *impressions*, never provenance;
- **pure aesthetic judgments** — "ugly", "too polished", "looks generated" with nothing
  located;
- **presence-only flags** — "has bullets" / "has an appendix" / "short intro" with no
  located, repeated, named observation. Presence ≠ pattern.

## Constants & Reviewer Calling Convention

```
REVIEWER_MODEL          = gpt-5.5                  # different family from executor (Claude)
REVIEWER_REASONING      = xhigh                    # always; effort never lowers reviewer quality
REVIEWER_SANDBOX        = read-only                # detect-only; never mutate the paper
REVIEWER_CWD            = <paper-dir>              # so it can read claims.json + pdf-text + the PDF directly
THREAD_POLICY           = fresh mcp__codex__codex per run; NEVER mcp__codex__codex-reply
TAXONOMY_VERSION        = 0.5                      # AIS track migrated out of §F in v0.5
VERDICT_WEIGHT          = 0        # adjudicator forces every AIS finding to info + excludes it from overall_verdict
NOT_INTEGRITY_FINDING   = true     # on EVERY finding (deterministic + semantic) — not optional
DETERMINISTIC_PATTERNS  = AIS-DEFENSIVE-HEDGE   # Step 1 (tools/check_ai_style.py), pervasive case only
SEMANTIC_PATTERNS       = the 13 AIS-* style tells, GROSS cases only   # Step 2 (reviewer)
                          # AIS-DEFENSIVE-HEDGE is DUAL: density screen (Step 1) + sub-threshold (Step 2)
DEFAULT_FP_RISK         = high     # every AIS impression; this is not optional
OBS_REQUIRED            = 0        # every AIS pattern is decidable at L0 (PDF-only)
SEVERITY                = impression, never a flag (the adjudicator forces it to info; no cap needed here)
DETERMINISTIC_FINDINGS  = ai-style-impressions.deterministic.findings.json   # Step 1, ids AIS###
SEMANTIC_FINDINGS       = ai-style-impressions.findings.json                 # Step 3, ids F### (validated)
TRACE_POLICY            = forensic (never silently dropped)
TRACE_DIR               = .aris/traces/ai-style-impressions/<YYYY-MM-DD>_run<NN>/
```

- **Executor (Claude)** builds none of the judgment: it locates the ledger + the PDF,
  passes **paths + the ledger + the checklist** to the reviewer, validates the
  reviewer's spans, forces the AIS fields, and writes the findings file. It never
  summarizes the paper, pre-judges "this looks AI-written", or leaks an opinion into the
  prompt (`reviewer-independence.md` Layer 1).
- **Reviewer (codex / gpt-5.5)** reads `claims.json` + the PDF-text + the PDF itself
  (visually only if it can render it; otherwise caption text only — see
  `AIS-SINGLE-STYLE-FIGURES`), proposes **gross-only** style impressions, and
  self-reports `fp_case`. It is the evidence-extractor, not the judge — and it never
  issues an authorship verdict.
- **Fresh thread per run.** `codex-reply` is intentionally absent from `allowed-tools`;
  never carry one run's conclusions into another (the bias guard).
- **Detect-only.** No `Edit` in `allowed-tools`; the reviewer sandbox is `read-only`.
  `Write` is used **only** for this skill's own findings / trace artifacts, never the
  audited paper. This is a third-party forensics tool, never a co-author.

---

## Step 0 — Preconditions: locate the ledger, read the level, find the PDF

The ledger is the **only** structure this skill reasons over for anchoring. Resolve it,
read the run's observability level **L** and `paper_id`, count the claim types AIS
anchors to, and locate the PDF + text source the reviewer will read (each Bash block is
self-contained — shell state does not persist between calls, so re-derive paths):

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
cl = d.get("claims", [])
caps = [c for c in cl if c.get("type") == "caption"]
tabs = sorted({(c.get("location") or {}).get("section","") for c in cl
               if c.get("type") == "table_cell"
               and str((c.get("location") or {}).get("section","")).startswith("table:")})
scope = [c for c in cl if c.get("type") == "scope"]
print("LEDGER       =", os.path.abspath(p))
print("PAPER_DIR    =", os.path.dirname(os.path.abspath(p)) or ".")
print("PAPER_ID     =", d.get("paper_id", "?"))
print("RUN_LEVEL_L  =", d.get("observability_level", 0))
print("CLAIMS       =", len(cl))
print("SCOPE_CL     =", len(scope), "  (anchors for AIS-DEFENSIVE-HEDGE / -RESTATE-OVERCLAIM / -NARRATIVE-ARC-BREAK / -FOCUS-DRIFT)")
print("CAPTION_CL   =", len(caps), "  (anchors for AIS-SINGLE-STYLE-FIGURES / -INVENTED-CODENAME in captions)")
print("TABLE_SECS   =", len(tabs), tabs, "  (anchors for AIS-INVENTED-CODENAME used in result tables)")
paper_dir = os.path.dirname(os.path.abspath(p)) or "."
srcs = d.get("source_files", [])
for sf in srcs:
    print("SOURCE       =", sf.get("kind"), sf.get("path"))
# Deterministically pick the prose source + the PDF the reviewer will read, FROM the
# ledger's source_files (authoritative); fall back to a sorted glob. source_files paths
# may be relative to PAPER_DIR or absolute. This is the ONLY selection (no shell `ls`
# later), so the PDF-only/L0 path with no pdf source resolves to NONE.
import glob
def _resolve(rel):
    cand = rel if os.path.isabs(rel or "") else os.path.join(paper_dir, rel or "")
    return os.path.abspath(cand) if os.path.isfile(cand) else ""
def _pick(kinds, globs):
    for sf in srcs:
        if sf.get("kind") in kinds:
            r = _resolve(sf.get("path"))
            if r:
                return r
    for g in globs:
        hits = sorted(glob.glob(os.path.join(paper_dir, g)))
        if hits:
            return os.path.abspath(hits[0])
    return ""
print("PDF_TEXT_FILE=", _pick({"text", "latex"}, ["*.txt", "*.tex"])
      or "NONE (prose impressions limited to ledger spans)")
print("PDF_FILE     =", _pick({"pdf"}, ["*.pdf"])
      or "NONE (AIS-SINGLE-STYLE-FIGURES limited to caption text)")
PY
```

**Failure / edge handling.**
- `NO_LEDGER` → stop; tell the user to run `/evidence-ledger` first. This skill never
  re-reads the raw PDF and invents its own structure (contract rule 1).
- `SCOPE_CL = 0` → the hedge / restatement / arc / drift anchors are absent; those
  impressions will correctly hold at `info` (common on a pure PDF-text run that parsed
  no scope sentences). Continue.
- `CAPTION_CL = 0` and/or `PDF_FILE = NONE` → `AIS-SINGLE-STYLE-FIGURES` has no caption
  anchor and no image to inspect; the reviewer will almost certainly hold it at `info`.
  That is honest, not a failure.
- `CLAIMS = 0` (degenerate ledger) → every semantic impression will be unanchored →
  `info`. Run anyway; the file must exist.

Step 0 **prints** `RUN_LEVEL_L`, `PAPER_ID`, the absolute `LEDGER` / `PAPER_DIR`,
`PDF_FILE`, and `PDF_TEXT_FILE`. Shell variables do **not** persist across Bash calls,
so paste these **literal absolute values** into the `<...>` placeholders of each later
step — do not assume an exported `$LEDGER` survives between blocks.

## Step 1 — Deterministic impression check (no LLM): `AIS-DEFENSIVE-HEDGE`

The one objective, eval-testable style signal: a conservative **defensive-hedge density
screen**, computed purely from the ledger's `scope` claims. It fires **only** on a
genuine pattern — never on one scoping sentence — and flags the recurrence of the hedge
SHAPE, never who wrote it. Runs before any model:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json from Step 0>"
python3 "$ROOT/tools/check_ai_style.py" \
    --ledger "$LEDGER" \
    --out "$(dirname "$LEDGER")/ai-style-impressions.deterministic.findings.json"
```

This emits at most one finding with `pattern_id: AIS-DEFENSIVE-HEDGE`,
`reviewer.deterministic: true`, `not_integrity_finding: true`,
`false_positive_risk: high`, `observability_level_required: 0`, `finding_id: AIS###`,
and ≤3 representative hedge spans, each anchored to a `scope` ledger claim. It fires only
when **≥4 distinct strong-template hedge sentences** ("we do not claim …", "not X but
rather Y", "本文并不声称 …") appear **across ≥2 non-excluded sections** AND constitute
**≥25% of all scope sentences** — hedges in Limitations / Related-Work / Ethics /
Broader-Impact / Acknowledgements are **excluded** (expected and legitimate). Because
PDF-text ledgers label every section `unknown`, the ≥2-section gate makes this
effectively LaTeX-decided — conservative by design.

**Failure handling.** If the tool errors, fix the invocation
(`python3 "$ROOT/tools/check_ai_style.py" --help`) — do **not** hand-fabricate
deterministic findings. An empty output (`[]`) is a valid, expected result (no pervasive
hedging, or no `scope` claims were extracted); keep the file.

## Step 2 — Cross-model GROSS-cases-only semantic pass (the 13 impressions; reviewer ≠ adjudicator)

The style tells are judgment calls. Open a **fresh** `mcp__codex__codex` thread (the
Reviewer Calling Convention above), `cwd = PAPER_DIR` so it can read `claims.json`, the
PDF-text, and the PDF directly. First create the forensic trace dir and fix the exact
response path — shell state does not persist, so this prints the literal paths to reuse:

```bash
LEDGER="<abs path to claims.json from Step 0>"; PAPER_DIR="$(dirname "$LEDGER")"
TS="$(date +%F)"; BASE="$PAPER_DIR/.aris/traces/ai-style-impressions"
NN=1; while [ -d "$(printf '%s/%s_run%02d' "$BASE" "$TS" "$NN")" ]; do NN=$((NN+1)); done
TRACE_DIR="$(printf '%s/%s_run%02d' "$BASE" "$TS" "$NN")"; mkdir -p "$TRACE_DIR"
echo "TRACE_DIR = $TRACE_DIR"
echo "PROPOSED  = $TRACE_DIR/001-style-semantic.response.md   # save the raw reply here; reuse as PROPOSED in Step 3"
```

Replace the bracketed placeholders below with the real values from Step 0, send EXACTLY
this, and save the **verbatim** reviewer reply to the `PROPOSED` path above (the Step 3
input) **before** parsing:

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are recording AI writing-STYLE impressions only — the kind of style tell a
    reviewer notices at a glance. You are explicitly NOT deciding whether the paper is
    AI-written, NOT assigning any probability or score, and NOT deciding whether it is
    fraudulent. You are NOT an AI-text classifier. Your output is a list of transparent,
    LOCATED style IMPRESSIONS that a deterministic adjudicator will give ZERO verdict
    weight (forced to info, excluded from the verdict, shown in a separate
    non-integrity section). It can NEVER raise a verdict. Default to SILENCE: an empty
    array [] is the expected, correct output for most papers.

    INPUTS (in your working directory, read them directly):
      - claims.json        — the evidence ledger: the authoritative, span-anchored list
        of every checkable claim {claim_id, type, text_span (VERBATIM source text),
        location, value?}. This is the ONLY thing you may anchor a finding to.
      - <PDF_TEXT_FILE from Step 0>   — extracted PDF text (for prose / phrasing / structure).
      - <PDF_FILE from Step 0, if any> — the rendered PDF (for figure-style inspection).
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.

    HARD RULES (a finding that breaks any of these is worthless):
    1. GROSS ONLY. Flag only BLATANT, RECURRING cases. If you are unsure, do NOT flag.
       This is especially binding for AIS-LLM-PHRASE-TICS and AIS-JARGON-STUFF (the most
       FP-prone). A single instance is NEVER the pattern.
    2. ANCHOR. Every finding above severity "info" MUST carry >=1 evidence entry
       {claim_id, span}, where claim_id EXISTS in claims.json and span is a VERBATIM
       substring of THAT claim's text_span (no paraphrase, no added words). If you
       cannot quote a verbatim ledger span, emit it at severity "info" (a note) or drop
       it. The ledger holds numbers, scope, captions, citations, and table cells;
       generic prose is usually NOT in it, so most style impressions will correctly
       remain "info".
    3. IMPRESSION FIELDS. Set severity = "minor" for an ANCHORED impression and "info"
       for an unanchored one. Set false_positive_risk = "high",
       observability_level_required = 0, and "not_integrity_finding": true for EVERY
       finding. Provide an "fp_case": the concrete legitimate (not-necessarily-AI)
       explanation for THIS tell. NEVER use "major"/"critical" (these are impressions,
       not flags).
    4. NO ACCUSATION, NO AUTHORSHIP VERDICT, NO SCORE. description and
       recommended_reviewer_action say what a human should GLANCE AT as a readability
       impression. NEVER write "AI-generated", "AI-written", "likely AI", a probability,
       a score, "fabricated", or "reject". A style tell is a prompt to look, nothing more.
    5. STAY IN LANE. pattern_id MUST be exactly one of the 13 AIS-* below. If you notice
       a SUBSTANTIVE problem (numbers contradict, a citation looks fake, a symbol is
       undefined, the method drifts, a codename points to a missing result), do NOT
       encode it here — it belongs to the integrity auditor named in the checklist.
       Ignore it; this track is style-only and carries zero weight.
    6. NEVER EMIT (not even as info): any standalone single-punctuation tell (one
       em-dash / one semicolon / one adverb); generic non-native English / awkward prose;
       "this is AI-written" or any authorship probability/score; pure aesthetics
       ("ugly" / "too polished"); presence-only flags ("has bullets" / "has an appendix"
       / "short intro") with nothing located, repeated, and named.

    CHECKLIST (the 13 AIS-* style tells; one finding per concrete, blatant, RECURRING case.
    "ROUTE" = where it goes IF it is actually substantive — then it is NOT an AIS finding):
      AIS-NARRATIVE-ARC-BREAK  — abrupt 1-2 paragraph intro, or a dump-like / vague
                        abstract with no background -> contribution -> evidence arc.
                        fp_case: terse-but-clear abstract; non-native phrasing; field
                        conventions. ROUTE: argument chain truly breaks ->
                        HP-ARGUMENT-CHAIN-BREAK (consistency-audit).
      AIS-LLM-PHRASE-TICS — generic LLM phrasing tics OVERUSED: "it is worth noting" /
                        "值得注意的是" / "意义在于", "not only ... but also", chains of
                        however/therefore/moreover, "therefore" mid-sentence, clichéd
                        em-dash/semicolon habits, flowery empty adverbs (elegantly,
                        theoretically). fp_case: honest LLM-assisted writing; non-native
                        English; house style (HUGE FP — gross cases only). ROUTE: never
                        (pure style).
      AIS-DEFENSIVE-HEDGE — pervasive "we do not claim ..." / "not X but rather Y"
                        defensive framing instead of stating what was done. NOTE: Step 1
                        already emits this DETERMINISTICALLY for the clearly pervasive
                        case; here flag only a sub-threshold/qualitative posture it misses
                        (e.g. a self-incriminating limitation volunteered in the
                        contribution paragraph). Anchor >=2 representative hedge spans.
                        fp_case: one scoping sentence is legitimate; Limitations hedges are
                        expected; some venues penalize the ABSENCE of caveats. ROUTE: a
                        hedge reveals a real scope/eval limitation -> HP-SCOPE-INFLATE (B)
                        / eval-design-forensics (H).
      AIS-JARGON-STUFF — dense term-stuffing where the surrounding argument carries no
                        content. fp_case: genuinely dense, correct technical writing (very
                        high FP). ROUTE: never.
      AIS-INVENTED-CODENAME — an undefined internal-project-flavored run/experiment
                        codename used AS IF defined (e.g. "Experiment Set Gamma"),
                        appearing in a table/caption/heading/results sentence and never
                        defined — and not the paper's formal method name, a standard
                        dataset/split, an ablation label, or a config id. fp_case:
                        legitimate named methods / benchmarks / defined release tags.
                        ROUTE: it points to a MISSING results file / unreproducible run ->
                        HP-MISSING-REPRO-ARTIFACT / HP-PHANTOM-RESULT (family D).
      AIS-CLAUSE-FORMULA-WALL — fragmented "short clause then a wall of formulas"; formulas
                        dumped without prose connective tissue. fp_case: dense-but-correct
                        theory; field norms. ROUTE: a load-bearing symbol is actually
                        UNDEFINED -> HP-UNDEFINED-NOTATION (G).
      AIS-GRATUITOUS-PSEUDOCODE — pseudocode/algorithm blocks that merely restate the prose
                        or add no operational content. fp_case: genuinely helpful algorithm
                        listings. ROUTE: the algorithm CONTRADICTS the described method ->
                        HP-METHOD-DRIFT (consistency-audit).
      AIS-BULLET-LIST-OVERUSE — prose organized as many bullets, incl. sequential /
                        progressive logic flattened into parallel-looking bullets. fp_case:
                        legitimate enumerations; checklists. ROUTE: never.
      AIS-BOLD-MODULE-SPAM — verbose module names with excessive bolding / acronym staging.
                        fp_case: reasonable emphasis; defined acronyms. ROUTE: the SAME
                        module gets incompatible abbreviations -> HP-ACRONYM-DRIFT (B,
                        consistency-audit).
      AIS-RESTATE-OVERCLAIM — a rhetorical restatement loop: repeatedly re-asserting "we
                        propose an X / we do an X". fp_case: legitimate signposting. ROUTE:
                        the claim EXCEEDS the evidence -> HP-SCOPE-INFLATE (B) / family H.
      AIS-FOCUS-DRIFT — high-level motivation suddenly pivots to a minor implementation
                        detail, or over-emphasizes an unnecessary requirement. fp_case: a
                        modular paper with explicit cross-refs. ROUTE: the
                        motivation->method->experiment chain substantively breaks ->
                        HP-ARGUMENT-CHAIN-BREAK (B).
      AIS-SINGLE-STYLE-FIGURES — figures share a generic generated visual grammar /
                        single-style AI illustrations. If you cannot VISUALLY inspect the
                        PDF, judge only from the caption text and otherwise leave it at
                        "info". fp_case: legitimate consistent house figure style;
                        conceptual teasers. ROUTE: checkable figure-vs-content thinness
                        stays HP-LLM-FIGURE / HP-THIN-FLOAT (family F, presentation-signals).
      AIS-APPENDIX-DUMPING-GROUND — the appendix reads like unintegrated trace / dumping;
                        AI-trace heavy. fp_case: legitimately long supplementary detail.
                        ROUTE: it CONTRADICTS the main text -> HP-APPENDIX-CONTRA (B); it
                        contains an exact assistant/template artifact -> HP-PIPELINE-ARTIFACT
                        (F); it affects reported data -> family D.

    OUTPUT: a single JSON array, and NOTHING ELSE (no prose, no code fence). Each
    element conforms to schemas/finding.schema.json plus the AIS fields:
      {
        "finding_id": "F001",
        "skill": "ai-style-impressions",
        "pattern_id": "<one of the 13 AIS-* ids>",
        "title": "short, neutral",
        "description": "the located style impression, plus the explicit note that it is an impression with ZERO verdict weight — not a factual/integrity inconsistency, not evidence of AI authorship, no probability implied",
        "severity": "minor",
        "observability_level_required": 0,
        "evidence": [{"claim_id": "C0xx", "span": "verbatim substring of that claim",
                      "location": {"file": "...", "section": "..."}}],
        "verdict_local": "warn",
        "false_positive_risk": "high",
        "not_integrity_finding": true,
        "fp_case": "the concrete legitimate (not-necessarily-AI) explanation for THIS tell",
        "recommended_reviewer_action": "what to GLANCE AT as a readability impression — never 'reject', never 'AI-generated', never a score"
      }
    If nothing is blatant, return []. That is the expected output for most papers.
```

**Failure handling.**
- *MCP stall / hang* (common in long sessions): re-invoke the **identical** prompt as a
  **fresh** `mcp__codex__codex` call (gpt-5.5, xhigh) — never `codex-reply`.
- *Reviewer returns prose, not a JSON array*: the Step 3 validator extracts the
  outermost `[...]`; if there is none, re-ask once with "Output ONLY the JSON array,
  nothing else." Do not hand-author findings on the reviewer's behalf.
- *Reviewer slips toward authorship/probability language, or emits a non-AIS pattern*:
  that is what the Step 3 fields + the AIS allow-list are for — the validator strips any
  authorship verdict shape by forcing `not_integrity_finding` and drops any non-`AIS-`
  pattern. Do not pre-suppress; let the gate work.

## Step 3 — Validate + anchor + tag (keep only `AIS-*`; never cap; never let integrity through)

The executor enforces the ANCHOR gate, the AIS allow-list, and the AIS field-forcing
**before** keeping anything. Unlike `presentation-signals`, this validator does **not**
cap severity — the adjudicator zero-weights every AIS finding regardless — but it
**MUST** drop any non-`AIS-` pattern (an integrity problem must be raised by its own
auditor, never smuggled into the zero-weight track). The span must be a verbatim,
whitespace-normalized **substring of** the cited claim (`span in base`, never `base in
span` — appending hallucinated text to a real claim must fail):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"
PROPOSED="<the PROPOSED path printed in Step 2>"   # the verbatim reviewer reply you saved
OUT="$(dirname "$LEDGER")/ai-style-impressions.findings.json"
python3 - "$LEDGER" "$PROPOSED" "$OUT" <<'PY'
import json, re, sys
ledger_path, proposed_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

def nw(s):                                   # mirror adjudicator _norm_ws (whitespace only)
    return " ".join((s or "").split())

# The 13 AIS-* style impressions. The deterministic Step 1 (tools/check_ai_style.py) owns the
# PERVASIVE AIS-DEFENSIVE-HEDGE case; it is KEPT here too because that pattern is DUAL (Step 2
# catches the sub-threshold/qualitative posture the density screen misses; ids never collide —
# Step 1 is AIS###, this file is F###). EVERYTHING ELSE is DROPPED: any HP-* / integrity pattern,
# any non-AIS id, anything malformed. An integrity problem belongs to its own auditor and must
# NEVER be smuggled into the zero-weight AIS track.
AIS_PATTERNS = {
    "AIS-NARRATIVE-ARC-BREAK", "AIS-LLM-PHRASE-TICS", "AIS-DEFENSIVE-HEDGE",
    "AIS-JARGON-STUFF", "AIS-INVENTED-CODENAME", "AIS-CLAUSE-FORMULA-WALL",
    "AIS-GRATUITOUS-PSEUDOCODE", "AIS-BULLET-LIST-OVERUSE", "AIS-BOLD-MODULE-SPAM",
    "AIS-RESTATE-OVERCLAIM", "AIS-FOCUS-DRIFT", "AIS-SINGLE-STYLE-FIGURES",
    "AIS-APPENDIX-DUMPING-GROUND",
}
SEV = {"critical", "major", "minor", "info"}
VL  = {"fail", "warn", "clean", "needs_external_check"}
ABOVE_INFO = {"critical", "major", "minor"}

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
    if pid not in AIS_PATTERNS:              # keep ONLY AIS-*; never let an integrity/non-AIS pattern through
        dropped += 1; continue
    n += 1
    f["finding_id"] = f"F{n:03d}"
    f["skill"] = "ai-style-impressions"      # force-correct the skill tag
    f["pattern_id"] = pid
    f["not_integrity_finding"] = True        # the doctrine, on EVERY finding (not optional)
    f["false_positive_risk"] = "high"        # AIS impressions are high-FP by design (not optional)
    f["observability_level_required"] = 0    # every AIS pattern is L0-decidable
    if f.get("verdict_local") not in VL: f["verdict_local"] = "warn"
    f.setdefault("fp_case", "Style impression only; common in honest LLM-assisted / "
                 "non-native writing and house style — not evidence of AI authorship.")
    f.setdefault("recommended_reviewer_action", "Glance at the cited span as a readability "
                 "impression; not misconduct, not an authorship judgment, no score.")
    sev = f.get("severity")
    if sev not in SEV: sev = "minor"         # neutral default. NO severity cap: the adjudicator
                                             # forces every AIS finding to info + zero weight regardless.
    # ANCHOR gate: span must be a verbatim ws-normalized SUBSTRING of its cited claim
    anchored = []
    for ev in (f.get("evidence") or []):
        cid, span = ev.get("claim_id"), nw(ev.get("span", ""))
        c = claims.get(cid)
        if c and span and span in nw(c.get("text_span", "")):   # span IN claim, not claim IN span
            ev.setdefault("location", c.get("location", {}))     # enrich for human navigation
            ev.setdefault("artifact_hash", c.get("evidence_anchor", ""))
            anchored.append(ev)
    f["evidence"] = anchored
    if sev in ABOVE_INFO and not anchored:
        sev = "info"; demoted += 1           # unanchored impression -> info note, NEVER silently dropped
    f["severity"] = sev
    # cross-model provenance (reviewer-independence: this is a proposal, not a verdict)
    f["reviewer"] = {"model": "gpt-5.5", "reasoning": "xhigh", "deterministic": False}
    kept.append(f)

json.dump(kept, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"validated {len(kept)} AI-style impressions "
      f"({demoted} unanchored -> info note, "
      f"{dropped} dropped: non-AIS/integrity/malformed) -> {out_path}")
PY
```

Scope of this gate: **AIS allow-list + anchoring + AIS field-forcing** (it does **not**
run `schemas/finding.schema.json`, just like `presentation-signals`) — drop everything
that is not an `AIS-*` pattern, verbatim-span anchoring (unanchored above-info →
`info`), `skill` forced to `ai-style-impressions`, `not_integrity_finding` forced
`true`, FP-risk forced `high`, observability fixed to `0`, `fp_case` /
`recommended_reviewer_action` defaulted if missing, enum coercion, and cross-model
provenance. **No severity cap** — capping is unnecessary because
`tools/adjudicate_findings.py` independently forces every AIS finding to `info` (by
`skill`, by the `AIS-` prefix, AND by the deprecated-style-id set) and assigns it
`_verdict_weight = 0`, so it is excluded from `overall_verdict` no matter what severity
it carries here.

**Worked impression — `AIS-LLM-PHRASE-TICS` (anchored → kept, but ZERO verdict weight):**

```json
{
  "finding_id": "F001",
  "skill": "ai-style-impressions",
  "pattern_id": "AIS-LLM-PHRASE-TICS",
  "title": "Recurrent 'it is worth noting' / however-therefore phrasing",
  "description": "The cited scope sentence opens with 'It is worth noting that' and the surrounding text repeatedly chains 'however … therefore … moreover' — a common LLM phrasing tic that lowers information density. This is a STYLE IMPRESSION with ZERO verdict weight: not a factual/integrity inconsistency, not evidence of AI authorship, and no probability is implied.",
  "severity": "minor",
  "observability_level_required": 0,
  "evidence": [{"claim_id": "C012",
                "span": "It is worth noting that our method generalizes across settings",
                "location": {"file": "paper.txt", "section": "introduction"}}],
  "verdict_local": "warn",
  "false_positive_risk": "high",
  "not_integrity_finding": true,
  "fp_case": "Honest LLM-assisted drafting, non-native English, and many house styles use exactly these transitions; this is not a tell of AI authorship.",
  "recommended_reviewer_action": "Glance at whether the phrasing tics make the section read padded; an impression only — not misconduct, not an authorship judgment."
}
```

**Worked non-finding — single em-dash (REFUSED, not emitted):** the reviewer is tempted
to flag one em-dash in a sentence. This is on the **refuse-list** (a standalone
single-punctuation tell is never a pattern) — it is **not** emitted, not even as `info`.
A style impression is about a *located, repeated, named* observation; one character is
not one. **We are not an AI-text classifier.**

**Worked routing — `AIS-INVENTED-CODENAME` vs `HP-PHANTOM-RESULT`:** the reviewer sees
"Experiment Set Gamma" in a results table with no definition. If it is merely an
undefined, generation-flavored label, it is an `AIS-INVENTED-CODENAME` impression (zero
weight). But if that codename's row reports a number with **no backing results file**,
that is a substantive integrity problem — **drop the AIS impression and route it** to
`experiment-forensics` (`HP-PHANTOM-RESULT` / `HP-MISSING-REPRO-ARTIFACT`, family D, at
L2). The style track never carries the substantive accusation.

**Failure handling.** A `KeyError` / `JSONDecodeError` means the reviewer output was
malformed → re-run Step 2 once with the strict-JSON reminder. If it is **still**
unparseable, fail closed: write an empty array to `ai-style-impressions.findings.json`
(`printf '[]' > "$OUT"`) so the output contract's file exists — never hand-author
findings on the reviewer's behalf. If a finding loses all evidence, it is *kept as
`info`* (never silently dropped — the forensic record stays).

## Step 4 — Emit (two files, no merge)

Step 1 wrote `ai-style-impressions.deterministic.findings.json` (ids `AIS###`); Step 3
wrote `ai-style-impressions.findings.json` (validated semantic impressions, ids `F###`).
**Keep them separate. Do NOT copy the deterministic finding into the semantic file** —
the orchestrator concatenates `*.findings.json`, so merging would double-count
`AIS-DEFENSIVE-HEDGE`. The id namespaces (`AIS###` vs `F###`) do not collide.

If the semantic pass found nothing blatant, `ai-style-impressions.findings.json` is `[]`
— write it anyway. **Silent skip is forbidden**: the orchestrator and the standalone
adjudicate command both expect the file to exist at a predictable path. For this
style-impression skill, `[]` (or all-`info`) is the **common, correct** result.

## Step 5 — Trace (forensic; never silently dropped)

Save the raw reviewer call under the `TRACE_DIR` created in Step 2
(`.aris/traces/ai-style-impressions/<YYYY-MM-DD>_run<NN>/`). This repo ships no
`save_trace.sh`, so write the files directly:

```
.aris/traces/ai-style-impressions/<date>_run<NN>/
  run.meta.json                    # {skill, paper_id, run_level_L, ledger_sha?, generated_at}
  001-style-semantic.request.json  # the EXACT prompt sent (paths + checklist; no paper digest)
  001-style-semantic.response.md   # the FULL raw reviewer response (input to Step 3)
  001-style-semantic.meta.json     # {model:"gpt-5.5", reasoning:"xhigh", thread_id, sandbox:"read-only"}
```

The `request.json` is the independence audit trail — it must show the executor sent only
**paths + the ledger + the checklist**, never a hunch like "this looks AI-generated".
(Step 1 is deterministic and needs no trace beyond its output file.)

## Step 6 — Hand off, or adjudicate standalone

Within `/anti-autoresearch`, **stop here**: the orchestrator globs every
`*.findings.json`, runs the adjudicator, and emits `REPORT.md` + `report.json` — with
the AIS findings rendered in their **separate, zero-weight** section. When running this
skill **alone**, you may produce the report yourself — `--ledger` is **required** (it is
what re-verifies each finding quotes a real ledger span):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"; D="$(dirname "$LEDGER")"
# derive paper-id + level from the ledger so this block is self-contained (no carried vars):
PAPER_ID="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["paper_id"])' "$LEDGER")"
L="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("observability_level",0))' "$LEDGER")"
python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "$D/ai-style-impressions.deterministic.findings.json" \
               "$D/ai-style-impressions.findings.json" \
    --ledger "$LEDGER" \
    --paper-id "$PAPER_ID" --observability-level "$L" --taxonomy-version 0.5 \
    --out "$D/report.json" --md "$D/REPORT.md"
```

The adjudicator forces every AIS finding to `info` and `_verdict_weight = 0`, then
renders them under *"## AI Writing-Style Impressions — NOT integrity findings · ZERO
verdict weight"* with their `fp_case` and reviewer note. Because **every** finding here
is zero-weight, an **AIS-only run's `overall_verdict` is ALWAYS
`CLEAN_GIVEN_EVIDENCE`** — no AIS impression can reach even `SOFT_FLAGS`, let alone
`HARD_FLAGS`. The impressions populate the separate section only; they **never** move
the integrity verdict. No model is in the final decision.

## Output contract

This skill **always** writes, into the ledger's directory:

- `ai-style-impressions.deterministic.findings.json` — Step 1, a JSON array
  (`schemas/finding.schema.json` + AIS fields); the `AIS-DEFENSIVE-HEDGE` density finding
  with `reviewer.deterministic:true`, `not_integrity_finding:true`, ids `AIS###` (or `[]`).
- `ai-style-impressions.findings.json` — Step 3, a JSON array; validated semantic style
  impressions, ids `F###` (or `[]`). Each above-info finding carries
  `evidence[].claim_id` + a verbatim `span`, `severity` ≤ `minor`,
  `false_positive_risk: high`, `not_integrity_finding: true`,
  `observability_level_required: 0`, an `fp_case`, and a `pattern_id` ∈ the 13 `AIS-*`
  set.
- `.aris/traces/ai-style-impressions/<date>_run<NN>/` — Step 5, the raw reviewer call.

It writes **no verdict and no report** of its own — `report.json` / `REPORT.md` come
only from `tools/adjudicate_findings.py` (Step 6 / the orchestrator), which renders the
AIS findings in the separate zero-weight section. They **never** move `overall_verdict`.

## Key rules

- **ZERO verdict weight, always.** Every AIS finding is forced to `info` and excluded
  from `overall_verdict` by the adjudicator (by `skill`, by the `AIS-` prefix, and by
  the deprecated-style-id set). A paper can be `CLEAN_GIVEN_EVIDENCE` and list many.
- **Not authorship detection; not a classifier.** Never label a paper "AI-generated" /
  "likely AI", never assign a probability or a score. We surface located *impressions*,
  not provenance.
- **Every finding is named + located + has an `fp_case`.** No vibe, no "looks
  generated" with nothing anchored; `not_integrity_finding: true` on all of them.
- **Default to silence.** Most papers should produce few or zero AIS impressions; an
  empty (or all-`info`) result is the common, correct output.
- **No span → no above-info impression.** Reject unanchored / paraphrased findings to
  `info` here (the adjudicator re-enforces). `span in claim`, whitespace-normalized —
  never `claim in span`.
- **Stay in lane; route the substantive.** Emit only the 13 `AIS-*` patterns. When a
  tell is actually substantive (contradiction, fake citation, undefined notation, method
  drift, phantom result), hand it to the named integrity auditor — never encode it as a
  zero-weight style impression.
- **No severity cap needed, but no non-AIS pattern through.** The validator does not cap
  (the adjudicator zero-weights AIS regardless), but it **must** drop every non-`AIS-`
  pattern.
- **Two files, no merge.** Deterministic (`AIS###`) and semantic (`F###`) findings stay
  in separate files to avoid double-counting the dual `AIS-DEFENSIVE-HEDGE`.
- **Cross-model, fresh thread.** Reviewer is a different family (gpt-5.5 xhigh); every
  run is a new `mcp__codex__codex` thread; `codex-reply` is never used.
- **Detect-only.** Never edit the audited paper (no `Edit` in `allowed-tools`; reviewer
  sandbox is `read-only`).
- **Reproducible.** Same ledger + same findings → same (always-`CLEAN_GIVEN_EVIDENCE`,
  AIS-only) verdict + same impression list.

## When NOT to use this skill

- **No `claims.json` yet** → run `/evidence-ledger` first; this skill never invents
  structure from the raw PDF.
- **You want an AI-text / "looks machine-written" / authorship verdict or score** → out
  of scope **by design**. AIS records style impressions, never provenance; for
  authorship detection use a dedicated tool (Pangram / GPTZero / Binoculars).
- **You found a real integrity problem** → route it to the owning auditor, not here:
  numeric/method self-contradiction → `/consistency-audit`; citation existence /
  wrong-context → `/citation-forensics`; "SOTA" / baseline integrity →
  `/baseline-comparison-audit`; code/result fraud (fake GT, self-norm, phantom) →
  `/experiment-forensics` at L2; proof gaps / undefined notation →
  `/proof-derivation-forensics`; evaluation validity → `/eval-design-forensics`;
  checkable surface tells (dup tables, thin/LLM figures, padding, pipeline strings) →
  `/presentation-signals`.
- **As the basis for a reject / accusation** → never. An AIS impression carries zero
  verdict weight; the strongest thing it can do is say "here is a located style tell a
  reviewer might react to — look closer, and route it if it is actually substantive."
- **On a timer** → never `/loop` / `/schedule` / `CronCreate` this skill; re-fire only
  when the paper or ledger changes (see the fence at the top).

## Review tracing

Forensic trace policy and file layout are defined once in **Step 5** (Policy:
**forensic** — never silently skipped). The `request.json` records only the paths +
ledger + checklist that were sent (the reviewer-independence audit trail); the
`response.md` is the immutable input that Step 3 validates.
