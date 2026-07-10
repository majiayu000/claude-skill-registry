---
name: proof-derivation-forensics
description: "Family-G proof & derivation integrity forensics: does a THIRD PARTY's written proof/derivation actually establish its theorem, or does it skip an obligation, assume its own conclusion, take an invalid step, drift a symbol's meaning, or smuggle an unstated assumption? Decides from the WRITTEN proof/derivation — verdict-bearing at L1 (the LaTeX source; PDF-extracted math is unreliable, so an L0 PDF-only run surfaces info only) — never asserts 'fabricated', only that the step shown does not hold. A fresh cross-model reviewer reads the theorem/proof + an extraction-only obligation scaffold and proposes per-obligation findings, each span-anchored to the evidence ledger (claims.json); reviewer≠adjudicator. Emits proof-derivation-forensics.findings.json; NEVER computes the verdict. dimension=proof, can be critical. Triggers: \"proof forensics\", \"check this proof\", \"derivation integrity\", \"audit the math\", \"证明审计\", \"推导有没有漏洞\"."
argument-hint: [paper-dir | claims.json]
allowed-tools: Bash(*), Read, Write, mcp__codex__codex
---

# Proof & Derivation Forensics — does the written proof hold?

Audit family **G (proof & derivation integrity)** for: **$ARGUMENTS** (requires
`claims.json` from `/evidence-ledger`). A fresh cross-model reviewer reads each
theorem/proof and proposes span-anchored findings; this skill writes
`proof-derivation-forensics.findings.json`. The deterministic adjudicator — not this
skill — computes the verdict.

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> verdict-bearing input — it proposes the findings the deterministic adjudicator
> turns into the report. Re-firing it on a wall-clock timer adds no signal: its
> output changes only when the **paper / ledger** changes, not with the clock.
> Schedule the *external wait that precedes it* — ledger built → audit **once**.
> (Mirrors ARIS's external-cadence doctrine.)

> Broken math is the single most-cited "obviously machine-written" tell in real
> reviews ("过不去的步骤用文字糊弄", "车轱辘话复述当证明", "关键公式符号用反"). Unlike the
> surface signals of family F, family-G flaws are **substantive** and **can be
> critical**: a theorem whose proof is circular, skips a load-bearing obligation, or
> takes an invalid step **does not support its claim**. And — crucially — proof
> validity is decidable from the *written* proof: we never need the code or results,
> so family G is **verdict-bearing at L1** (the LaTeX source) and can still reach
> HARD_FLAGS with no repo — but needs that source, because PDF-extracted math is
> unreliable; at an L0 (PDF-only) run a family-G flaw surfaces as `info` only. Adapted from ARIS
> `proof-checker` (per-obligation ledger + 20-category taxonomy + counterexample red
> team) and `formula-derivation` (identity/proposition/approximation/interpretation
> step typing), **reframed from "fix my own proof" to "audit a third party's proof,
> detect-only."** There is no fixing here and no authorship verdict — only "the step
> shown does not hold," with the exact line quoted.

## Why this exists

An autoresearch pipeline (or a rushed human) writes a theorem statement, then a
proof, then an abstract that advertises the theorem — in separate passes, never
reconciled at the level of the *argument*. The result is a proof that does not
establish its own claim:

- "By compactness a maximizer exists" — but compactness of the domain is never shown
  (a missing existence obligation invoked as fact);
- "Lemma 3 follows from Theorem 1," whose proof in turn invokes Lemma 3 (circular);
- "By Jensen, $\mathbb{E}[f(X)] \ge f(\mathbb{E}[X])$" for a **concave** $f$ — the
  inequality runs the wrong way (an invalid step);
- the definition fixes $\le$, but equation (7) and the proof use $\ge$; or `argmin`
  in Def 2 becomes `argmax` in the proof of Thm 4 (a symbol's meaning drifts);
- a concentration bound uses **independence** of the $X_i$, but the theorem only
  assumes they are identically distributed (a stronger assumption smuggled in).

None of this needs the code, the data, or any external fact to detect — only the
proof, read against the obligations its own theorem creates. That is why family G is
**substantive and decided from the written proof (verdict-bearing at L1)**: a senior
area chair reads a proof and decides validity from the page; this tool needs the LaTeX
source (L1) to do it reliably, since PDF-extracted math is unreliable — at an L0 PDF-only
run it surfaces info only. So does this skill — via a cross-model reviewer, with every finding
anchored to a verbatim ledger span and the verdict computed by deterministic code.

**Honest recall bound (read this).** The evidence ledger (`build_claim_ledger.py`)
has **no dedicated theorem/proof/equation extractor**: proof text enters
`claims.json` only as the `number`, `scope`, `citation`, `caption`, and `table_cell`
spans that happen to *overlap* it (a bound with a constant, a "for all / general"
sentence, a `\cite{}` to an imported result, an equation paragraph carrying a
decimal). The reviewer **judges from the full proof source**, but every finding must
**anchor to a ledger claim** whose `text_span` verbatim-contains the failing
fragment. A pure-symbol step covered by no such claim cannot rise above `info` — that
is the honest outcome, not a defect. Recall is materially higher at **L1** (LaTeX:
equation paragraphs and theorem-statement sentences are captured with stable line
numbers) than at **L0** (PDF text). Step 1 pre-computes, per theorem, the exact
**anchor-candidate** `claim_id`s so the reviewer knows where it can and cannot ground
a finding.

## Core principle

**Ledger-anchored, span-verified, decide-from-the-written-proof, reviewer≠adjudicator.**
There is **no deterministic tool** for family G (no arithmetic backbone like
consistency-audit's `check_numeric_consistency.py`) — proof validity is a semantic
judgment. So this skill runs exactly one substantive pass:

- a **fresh cross-model** reviewer pass that reads each theorem + its proof + an
  **extraction-only obligation scaffold** (Step 1) and proposes one finding per
  *undischarged obligation / invalid step / drift / smuggle / circularity*.

Every above-`info` finding conforms to `schemas/finding.schema.json` and **cites a
ledger `claim_id` + a verbatim span** (`references/integrity-forensics-contract.md`
rules 1–2). The model **proposes**; `tools/adjudicate_findings.py` **decides**
(`references/reviewer-independence.md` Layer 2). This skill computes **no verdict**,
and **never edits** the audited paper. We never write "fabricated" or "faked" — we
write, with the line quoted, *the step shown does not hold / the obligation is not
discharged / the symbol's meaning drifted*.

## How this differs from the other auditors (route correctly)

| Auditor | Question it answers | Level |
|---------|---------------------|------|
| **`proof-derivation-forensics`** (this) | **Does the WRITTEN proof/derivation actually establish its theorem? (gap / circularity / invalid step / symbol drift / smuggled assumption)** | **L1 — from the written math (LaTeX source), no external lookup** |
| `consistency-audit` | Does the paper contradict ITSELF (numbers, scope, method)? incl. abstract-general-vs-theorem-narrow (`HP-THEOREM-SCOPE-DRIFT`) | L0 |
| `citation-forensics` | Does a cited theorem EXIST and is it cited in a context it supports? | L0 |
| `experiment-forensics` | Are reported numbers what the code actually computes? (fake GT, self-norm, phantom) | L2 |
| `baseline-comparison-audit` | Are the right baselines present, tuned, and is "SOTA" earned? | L0 stated / L2 verified |
| `adversarial-case-builder` | Strongest evidence-bound rejection memo (no verdict weight) | any |

**Do NOT raise here** (hand off instead):
- abstract/title advertises generality the *theorem statement* doesn't have →
  `consistency-audit` owns `HP-THEOREM-SCOPE-DRIFT`; the headline framing goes to
  `adversarial-case-builder`. *This skill owns the proof-internal twin:* the proof
  uses an assumption the **theorem statement** never lists (`HP-ASSUMPTION-SMUGGLE`).
- whether a cited result **exists** or is **cited in the right context** →
  `citation-forensics`. *This skill owns the proof-internal twin:* a cited theorem is
  **applied without verifying its hypotheses** at the point of use
  (`HP-PROOF-OBLIGATION-GAP`).
- results-table arithmetic / delta / aggregation / number coherence →
  `consistency-audit`. This skill audits the **derivation**, not results tables.
- code/result-level fraud (fake GT, self-normalization, phantom numbers) →
  `experiment-forensics` at **L2**. Family G never reaches for code; if you think a
  flaw needs the code to decide, it is not a proof-validity finding.
- "first / SOTA / novel" external truth → emit `needs_external_check` and hand to
  `baseline-comparison-audit` + `citation-forensics`, never a guess.

## Constants & Reviewer Calling Convention

```
REVIEWER_MODEL          = gpt-5.5                  # different family from executor (Claude)
REVIEWER_REASONING      = xhigh                    # always; effort never lowers reviewer quality
REVIEWER_SANDBOX        = read-only                # detect-only; never mutate the paper
REVIEWER_CWD            = <paper-dir>              # so it can read claims.json + the proof sources directly
THREAD_POLICY           = fresh mcp__codex__codex per run (and per fan-out theorem group);
                          NEVER mcp__codex__codex-reply
TAXONOMY_VERSION        = 0.5                      # references/hack-pattern-taxonomy.md
OWNED_PATTERNS          = HP-PROOF-OBLIGATION-GAP · HP-PROOF-CIRCULARITY ·
                          HP-DERIVATION-INVALID · HP-SYMBOL-SEMANTIC-DRIFT ·
                          HP-ASSUMPTION-SMUGGLE · HP-UNDEFINED-NOTATION   # family G; emit ONLY these
OBLIGATION_SCAFFOLD     = <TRACE_DIR>/obligation-ledger.md   # Step 1 — EXTRACTION ONLY,
                          not a verdict, NOT claims.json, NOT the anchor substrate
FINDINGS                = proof-derivation-forensics.findings.json   # Step 3 — the ONLY
                          findings file (no deterministic tool exists for family G)
TRACE_POLICY            = forensic (never silently dropped)
TRACE_DIR               = .aris/traces/proof-derivation-forensics/<YYYY-MM-DD>_run<NN>/
```

- **Executor (Claude)** builds nothing of the judgment: it locates the ledger,
  extracts the obligation scaffold (structure only, **never validity**), pre-computes
  the per-theorem anchor candidates, passes **paths + the ledger + the scaffold + the
  checklist** to the reviewer, validates the reviewer's spans, and writes the findings
  file. It never summarizes the proof, pre-judges soundness, or leaks an opinion into
  the prompt (`reviewer-independence.md`).
- **Reviewer (codex / gpt-5.5)** reads `claims.json`, the obligation scaffold, and the
  proof sources; proposes findings; self-reports `false_positive_risk`. It is the
  evidence-extractor / candidate-explainer, **not the judge**.
- **Fresh thread per run.** If you fan out by theorem for breadth, each theorem is a
  **new** `mcp__codex__codex` call — never `codex-reply` carrying one theorem's
  conclusions into another (the bias guard). `codex-reply` is intentionally absent
  from `allowed-tools`.

---

## Step 0 — Preconditions: locate the ledger, read the level, confirm proofs exist

The ledger is the **only** structure this skill anchors to. Resolve it, read the
observability level **L**, `paper_id`, the claim count, the source files, and whether
the paper contains any proof/theorem/derivation to audit (each Bash block is
self-contained — shell state does not persist between calls, so re-derive paths every
step):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
# $ARGUMENTS is a paper-dir OR a claims.json path:
LEDGER="$ARGUMENTS"; [ -d "$LEDGER" ] && LEDGER="$LEDGER/claims.json"
# Only the NO-ARGUMENT case defaults to the CWD ledger. An EXPLICIT argument that
# resolves to a missing claims.json must NOT silently fall back to $(pwd) — that
# could audit the wrong paper; let the NO_LEDGER check below fire instead.
[ -z "$ARGUMENTS" ] && LEDGER="$(pwd)/claims.json"
python3 - "$LEDGER" <<'PY'
import json, sys, os, re
p = sys.argv[1]
if not os.path.isfile(p):
    sys.exit("NO_LEDGER: claims.json not found. Run /evidence-ledger FIRST "
             "(it writes artifact_manifest.json + claims.json).")
d = json.load(open(p, encoding="utf-8"))
paper_dir = os.path.dirname(os.path.abspath(p)) or "."
print("LEDGER       =", os.path.abspath(p))
print("PAPER_DIR    =", paper_dir)
print("PAPER_ID     =", d.get("paper_id", "?"))
print("RUN_LEVEL_L  =", d.get("observability_level", 0))
print("CLAIMS       =", len(d.get("claims", [])))
# Does the paper contain proofs/theorems/derivations to audit?
TH  = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|claim|conjecture|"
                 r"proof|definition|assumption)\*?\}", re.I)
EQ  = re.compile(r"\\begin\{(equation|align|gather|multline|eqnarray)\*?\}|\\\[", re.I)
TXT = re.compile(r"\b(Theorem|Lemma|Proposition|Corollary|Proof|Q\.?E\.?D\.?)\b")
srcs, hits = [], 0
for s in d.get("source_files", []):
    sp = s.get("path", ""); kind = s.get("kind", "")
    cand = sp if os.path.isabs(sp) else os.path.join(paper_dir, sp)
    if not os.path.isfile(cand): cand = sp
    srcs.append((cand, kind))
    try: t = open(cand, encoding="utf-8", errors="replace").read()
    except OSError: continue
    hits += (len(TH.findall(t)) + len(EQ.findall(t))) if kind == "latex" else len(TXT.findall(t))
print("SOURCE_FILES =", " ; ".join(c for c, _ in srcs) or "(none)")
print("HAS_PROOFS   =", ("yes" if hits > 0 else "no"), f"(markers={hits})")
PY
```

**Carry forward** the absolute `LEDGER` / `PAPER_DIR`, the `SOURCE_FILES`, plus `L`
and `PAPER_ID`, into every step below.

**Failure / edge handling.**
- **`NO_LEDGER`** → stop and tell the user to run `/evidence-ledger` first. This skill
  never re-reads the raw PDF and invents its own structure (contract rule 1).
- **`HAS_PROOFS = no`** (no theorem/lemma/proof/derivation markers) → there is nothing
  for family G to audit (the proof analog of `NOT_APPLICABLE`). Write the empty
  findings file directly — `printf '[]\n' > "$(dirname "$LEDGER")/proof-derivation-forensics.findings.json"` —
  record a trace note (Step 5), and stop. **Silent skip is forbidden**; an empty array
  is a valid, non-silent output the adjudicator reads as "this dimension found
  nothing." Do **not** call the reviewer.
- **`CLAIMS == 0`** → the ledger has no spans to anchor to even if proofs exist; write
  the empty findings file as above, note it in the trace, and stop.
- **`RUN_LEVEL_L == 0`** (PDF-text only) → proceed, but **recall is reduced**: equation
  and theorem-statement spans are poorly captured, so obligation/assumption findings
  that need the LaTeX source to confirm an obligation is undischarged anywhere will
  carry `observability_level_required: 1` and auto-demote to `info` (honest — you can
  suspect from PDF text, you cannot confirm). Family G is at full strength at **L1**.
- **`RUN_LEVEL_L == 2`** → proof checks run identically (they are textual/semantic);
  the extra L2 power (paper-number↔result-file) belongs to `/experiment-forensics`.

## Step 1 — Build the proof-obligation scaffold (EXTRACTION ONLY — never a verdict)

Create this run's trace dir, then extract — for each theorem/lemma/proposition and
its proof — the obligations the theorem creates, **without judging whether any is
discharged**. This adapts `proof-checker`'s Phase 0.5 ledger and `formula-derivation`'s
step typing, under one hard rule:

> **The scaffold EXTRACTS, it does not ADJUDICATE.** Inventorying obligations, typing
> symbols, restating quantifiers, and tagging a step `identity / proposition /
> approximation / interpretation` is *structural extraction*. Whether a step is
> *valid* — whether an obligation is actually discharged — is a correctness verdict
> reserved for the cross-model reviewer (Step 2) and the adjudicator (Step 6). The
> executor records the obligation and a **location pointer** to where the paper claims
> to discharge it (`file:line`) — never its own judgment that the discharge is sound.
> "UNCITED" means *the paper cites no discharge location*, NOT *the executor checked
> the math and it fails*. (See `acceptance-gate.md`: the loop may self-verify that the
> scaffold is **complete**, never that the proofs are **correct**.) The scaffold is
> **not** `claims.json` and **not** the anchor substrate — findings still anchor to
> ledger claims in Step 3.

```bash
LEDGER="<abs path to claims.json from Step 0>"; D="$(dirname "$LEDGER")"
TBASE="$D/.aris/traces/proof-derivation-forensics/$(date +%F)"
NN=1; while [ -e "${TBASE}_run$(printf '%02d' "$NN")" ]; do NN=$((NN+1)); done
TRACE_DIR="${TBASE}_run$(printf '%02d' "$NN")"; mkdir -p "$TRACE_DIR"
echo "TRACE_DIR = $TRACE_DIR"   # carry this absolute path into Steps 2 and 5
```

Use **Read** to open each file in `SOURCE_FILES` and locate every
`\begin{theorem|lemma|proposition|corollary|claim|conjecture}` … `\end{...}` block and
its matching `\begin{proof}` … `\end{proof}` (or the derivation paragraphs that play
that role). For each, extract the entries below.

**Anchor candidates (the bridge to Step 3's gate).** For each theorem, list the
ledger `claim_id`s whose `text_span` overlaps the theorem+proof line window — these are
the *only* places a finding on that theorem can ground. Run (per theorem block):

```bash
LEDGER="<abs path to claims.json>"; FILE="<source file of this theorem>"
START="<thm block start line>"; END="<proof block end line>"
python3 - "$LEDGER" "$FILE" "$START" "$END" <<'PY'
import json, os, sys
ledger, f, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
d = json.load(open(ledger, encoding="utf-8"))
base = os.path.basename(f)
for c in d.get("claims", []):
    loc = c.get("location", {}) or {}
    ln = loc.get("line")
    same = base == os.path.basename(loc.get("file", "") or "")
    if same and isinstance(ln, int) and a - 2 <= ln <= b + 2:
        prev = " ".join((c.get("text_span", "") or "").split())[:90]
        print(f'{c["claim_id"]:>6}  {c.get("type",""):<10}  L{ln}  "{prev}"')
PY
```

Then **Write** the scaffold to `$TRACE_DIR/obligation-ledger.md` using this template
(one block per theorem; record pointers, never verdicts):

```md
# Proof-Obligation Scaffold — <PAPER_ID>   (EXTRACTION ONLY — NO validity verdict)
> Structures the reviewer's per-obligation pass. NOT claims.json, NOT the anchor
> substrate, contains NO "proved / sound / valid" judgments. Soundness is the Step-2
> reviewer's call; the verdict is the Step-6 adjudicator's.

## T1 — <theorem name / \label{...}>   [<file>:<line-range>]
- Statement (verbatim): "<exact theorem statement>"
- Canonical quantified form: ∀… ∃… s.t. …      (or: UNCLEAR — needs disambiguation)
- Stated hypotheses: H1 …; H2 …
- Typed symbols: κ: scalar ∈(0,1), dep (d,Σ); u*: vector ∈ℝ^d; B: matrix, sym PSD …
- Headline-dependent?: yes/no   (does the abstract / main claim rest on T1?)
- Proof location: <file>:<line-range>
- Obligations (every nontrivial step; tag identity|proposition|approximation|interpretation;
  record claimed discharge location — a pointer, NOT a validity judgment):
    - O1 [proposition]   "<step text>"   — claimed discharge: <file>:<line> | UNCITED
    - O2 [identity]      "<step text>"   — …
    - O3 [approximation] "<step text>"   — enters at <line>; later used as exact? pointer
    - O4 [interpretation]"<prose step>"  — presented as derivation? pointer
- Imported results applied: <\cite{} / named thm> @ <line>
  — hypotheses to verify at point of use: …
- Anchor-candidate claim_ids (from the helper above): C0xx, C0yy, …   (statement: C0xx)
```

**Breadth for a large multi-theorem paper (no `Agent` grant).** Scaffold
*construction* is pure structural extraction — walk the theorems **sequentially**.
This skill **spawns nothing**: `allowed-tools` grants no `Agent` (matching the other
Anti-Autoresearch auditors, which thread codex calls rather than fork subagents), so
there is no executor-side fan-out here. Breadth, when you want it, happens on the
**reviewer** side — issue one fresh `mcp__codex__codex` call per theorem in Step 2
(never `codex-reply`). Either way the extraction **never adjudicates**, and you must
**merge all theorem blocks into one scaffold before** looking for a cross-theorem
dependency **cycle** (semantic circularity for `HP-PROOF-CIRCULARITY`): a per-theorem
view misses exactly the cross-theorem cycles this skill exists to catch.

## Step 2 — Cross-model per-obligation review (reviewer ≠ adjudicator)

Open a **fresh** `mcp__codex__codex` thread (the Reviewer Calling Convention above)
and send it the checklist. The reviewer reads `claims.json`, the scaffold, and the
proof sources from its `cwd`; it judges from the **full proof**, but **every finding
must anchor to a ledger `claim_id`** — an anchor candidate from the scaffold whose
`text_span` verbatim-contains the failing fragment. Send EXACTLY (substitute the
absolute `PAPER_DIR`, the `L` value, and the scaffold path from Steps 0–1):

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are an integrity-forensics reviewer auditing a THIRD PARTY's PROOFS and
    DERIVATIONS for VALIDITY OF THE WRITTEN ARGUMENT only. You have NO external ground
    truth, you do NOT re-run anything, and you do NOT judge authorship. You decide
    from the WRITTEN proof: does it actually ESTABLISH its theorem? You NEVER assert a
    proof is "fabricated" or "faked" — you assert, with the exact line quoted, that
    THE STEP SHOWN DOES NOT HOLD / THE OBLIGATION IS NOT DISCHARGED / A SYMBOL'S
    MEANING DRIFTED / AN UNSTATED ASSUMPTION IS USED.

    INPUTS (in your working directory, read them directly):
      - claims.json — the evidence ledger: the authoritative, span-anchored list of
        checkable spans. This is the ONLY structure you ANCHOR to. Each claim has
        {claim_id, type, text_span (VERBATIM source text), location}. NOTE: the ledger
        has NO dedicated theorem/proof extractor — proof text appears only inside
        number/scope/citation/caption/table_cell spans that OVERLAP it.
      - obligation-ledger.md (path below) — an EXTRACTION-ONLY scaffold: per theorem,
        its statement, hypotheses, typed symbols, the obligations its proof creates
        (each tagged identity/proposition/approximation/interpretation), and the
        ANCHOR-CANDIDATE claim_ids. It carries NO validity verdicts — judging validity
        is YOUR job. Use it to structure your pass (one finding per failing obligation)
        and to find where you CAN anchor.
      - the proof source files (listed in claims.json source_files) — read them to see
        the FULL proof (ledger spans are fragmentary). You MAY read them freely, but
        you may NOT introduce a finding you cannot anchor to a ledger claim.
    OBLIGATION SCAFFOLD: <abs path to $TRACE_DIR/obligation-ledger.md>
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.

    HARD RULES (a finding that breaks any of these is worthless):
    1. ANCHOR. Every finding above severity "info" MUST carry >=1 evidence entry
       {claim_id, span}, where claim_id EXISTS in claims.json (prefer an anchor
       candidate the scaffold lists for that theorem) and span is a VERBATIM substring
       of THAT claim's text_span — copied character-for-character INCLUDING LaTeX
       escapes like \% \, \le \alpha (do NOT unescape, normalize, or paraphrase). The
       check is a whitespace-normalized substring match (`span in claim`); a reworded
       or unescaped span FAILS and is demoted to info. Anchor to the claim that
       verbatim-contains the FAILING fragment (the wrong step, the circular
       restatement, the inverted symbol) OR the THEOREM STATEMENT the obligation
       undermines. If NO ledger claim contains the step you object to (common for a
       pure-symbol step the extractor never captured), keep the finding at "info" and
       say so in recommended_reviewer_action — that is the honest outcome, not a loss.
    2. DECIDE FROM THE WRITTEN PROOF; DISCREPANCY, NOT ACCUSATION. description and
       recommended_reviewer_action describe what a human should CHECK or ASK and WHY
       the shown step does not follow. NEVER write "reject", "fabricated", "faked", or
       "the authors lied". You are agnostic to how the proof was produced.
    3. OBSERVABILITY. Family-G validity is decided from the LaTeX proof SOURCE, because
       PDF-extracted math is unreliable (mangled symbols, subscripts, equation structure).
       Set observability_level_required = 1 for ANY above-info family-G finding. NEVER set
       0: a proof verdict from a PDF-only read is not trustworthy — the validator floors G
       findings to L1 anyway, and at an L0 run they demote to info. NEVER set 2 — family-G
       flaws need no code or results; if you think you need code or result files to decide,
       it is NOT a proof-validity finding (route to experiment-forensics) — do not emit it here.
    4. HONEST FP RISK / COUNTEREXAMPLE-FIRST. Set false_positive_risk truthfully. A
       TERSE-BUT-VALID step the reader can fill in is NOT a gap (drop it, or info /
       high). A typo that does not affect the result is MINOR. A genuinely standard,
       cited step is a common false positive — say so. Before grading a step INVALID
       or a proof CIRCULAR, TRY TO BREAK / CONFIRM IT: attempt a minimal counterexample
       (set d=1 or K=2; a degenerate/singular case; a two-point or heavy-tailed
       distribution; adversarial parameter scaling making a neglected term dominate).
       Grade "critical"/"major" only if it truly fails or you can name the exact
       illegal manipulation; otherwise it is a CANDIDATE → severity minor,
       false_positive_risk high.
    5. CRITICAL DISCIPLINE. Reserve severity "critical" + false_positive_risk "low"
       for: a genuinely CIRCULAR proof; or an invalid step / smuggled assumption /
       inverted symbol that the HEADLINE theorem provably depends on AND you are
       mathematically certain of (ideally with a counterexample or an explicit
       algebraic contradiction). Everything else is at most "major". (The adjudicator
       caps high-FP findings at minor and medium-FP at major, so an honest FP label is
       what lets a real critical flaw stand.)
    6. PATTERN SCOPE. pattern_id MUST be one of the SIX family-G ids in the checklist.
       Do NOT emit any other HP-* here: abstract-vs-theorem scope drift
       (HP-THEOREM-SCOPE-DRIFT) and results arithmetic belong to consistency-audit;
       citation existence/context to citation-forensics; code/result fraud to
       experiment-forensics. If you spot one, NOTE it in recommended_reviewer_action
       and route it — do not raise it as a finding.

    CHECKLIST — run every item against every theorem/proof; one finding per concrete
    failing obligation. (Step-typing aid from formula-derivation: classify each
    nontrivial step as identity / proposition / approximation / interpretation. A
    step presented as a proved identity that is really an unproven proposition →
    OBLIGATION-GAP; an approximation used as if exact → DERIVATION-INVALID; an
    interpretation dressed as a derivation → OBLIGATION-GAP.)

     1. OBLIGATION GAP — a required lemma / case / transition the theorem needs is
        missing: an un-proved lemma invoked as fact; a "clearly / it follows / by
        standard arguments / by symmetry" across a REAL gap ("过不去的步骤用文字糊弄");
        an existence / compactness / concentration / generic-position / measurability
        claim never shown; an incomplete case split (boundary / degenerate / singular
        case omitted); a cited/imported theorem APPLIED without verifying EACH of its
        hypotheses at the point of use (DCT needs a dominating function; Fubini needs
        product-integrability; Jensen needs convexity + integrability; IFT needs a
        non-singular Jacobian).                            [HP-PROOF-OBLIGATION-GAP]
        severity: major; critical if the HEADLINE theorem depends on the gap.
        FP: the step is genuinely standard AND cited; the obligation is discharged in
        an appendix you can see. level: 1 (decided from the LaTeX source; an L0 PDF-only
        run surfaces info only — PDF-extracted math is unreliable).
        example: "By compactness a maximizer exists" — compactness of the domain is
        never established.

     2. CIRCULARITY — the proof assumes what it sets out to prove: the conclusion (or
        an equivalent restatement) is used as a premise; the "proof" restates the
        claim in different words and calls it done ("车轱辘话复述当证明"); Lemma A is
        proved using a corollary that quietly depends on A (a dependency cycle —
        check the MERGED scaffold).                        [HP-PROOF-CIRCULARITY]
        severity: critical (a circular proof proves nothing).
        FP: a legitimate WLOG / by-symmetry reduction; proof by contradiction that
        ASSUMES THE NEGATION (that is not circular). level: 1 (LaTeX source; an L0 PDF-only run surfaces info only).
        example: "Lemma 3 follows from Thm 1," and Thm 1's proof invokes Lemma 3.

     3. DERIVATION INVALID — an adjacent algebra / probability / calculus step does
        not follow: an illegal manipulation; a sign or factor error that propagates; a
        misapplied inequality (wrong direction; Cauchy-Schwarz / Hölder / Young /
        Jensen misused); a wrong limit; an illegal interchange of
        limit/sum/expectation/derivative/integral with no DCT/MCT/Fubini/Leibniz
        justification; a probability-mode confusion (a.s. vs in-prob vs in-L²) treated
        as free.                                            [HP-DERIVATION-INVALID]
        severity: major; critical if a HEADLINE equation/result depends on it.
        FP: a typo that does not affect the result (minor); a valid step the reader
        can fill in. level: 1 (decided from the LaTeX source; L0 PDF-only run → info only).
        example: "By Jensen, E[f(X)] >= f(E[X])" for a concave f — direction reversed.

     4. SYMBOL / SEMANTIC DRIFT — a symbol, index, quantifier, operator, or inequality
        DIRECTION changes meaning across definition → formula → proof: <= vs >=,
        argmin vs argmax, a quantifier order flipped (∀∃ vs ∃∀), one variable name
        carrying two meanings, a normalization/scaling convention silently switched
        ("关键公式符号用反").                            [HP-SYMBOL-SEMANTIC-DRIFT]
        severity: major; critical if the drift INVERTS a result.
        FP: a symbol explicitly redefined WITH notice; declared overloading. level: 1 (LaTeX source; an L0 PDF-only run surfaces info only).
        example: Def 2 fixes the objective as an argmin; the proof of Thm 4 maximizes it.

     5. ASSUMPTION SMUGGLE — the proof relies on an UNSTATED stronger assumption: it
        silently uses independence / convexity / smoothness / boundedness / i.i.d. /
        sub-Gaussianity / a regularity or moment condition the THEOREM STATEMENT never
        assumes, and the result holds only under that hidden assumption; or a constant
        "C" / "O(1)" secretly depends on (d, n, K, …) while treated as universal.
                                                            [HP-ASSUMPTION-SMUGGLE]
        severity: major (the theorem as stated is broader than what is proved).
        FP: the assumption is standard for the setting AND stated in the setup; it is
        implied by a cited result. level: 1 (LaTeX source; an L0 PDF-only run surfaces info only). Pairs with HP-THEOREM-SCOPE-DRIFT — if
        the abstract ALSO advertises the broader scope, NOTE it for consistency-audit /
        adversarial-case-builder; emit only the proof-internal smuggle here.
        example: a concentration bound uses independence of the X_i, but the theorem
        assumes only that they are identically distributed.
     6. UNDEFINED NOTATION — a load-bearing symbol / operator / index / set carries meaning in
        a key equation, lemma, or proof but is NEVER defined anywhere and is not inferable from
        standard convention, so the result cannot be checked as written ("没有 denote 的符号").
                                                            [HP-UNDEFINED-NOTATION]
        severity: major if a checkable result/proof depends on the undefined symbol; minor if
        peripheral. FP: notation genuinely standard in the subfield; a symbol defined in a
        figure / caption / appendix; reused notation from a cited setup. Distinct from
        HP-SYMBOL-SEMANTIC-DRIFT (a DEFINED symbol that CHANGES meaning); here it is simply
        never pinned down. The "short clause then a wall of formulas" style alone is
        presentation (HP-NARRATIVE-ARC-BREAK), NOT this. level: 1 (LaTeX source; an L0
        PDF-only run surfaces info only).
        example: Thm 3 bounds ‖A‖_σ but σ is never defined and is not a standard norm here.

    OUTPUT: a single JSON array, and NOTHING ELSE (no prose, no code fence). Each
    element conforms to schemas/finding.schema.json:
      {
        "finding_id": "F001",
        "skill": "proof-derivation-forensics",
        "pattern_id": "HP-PROOF-OBLIGATION-GAP",
        "title": "short, neutral",
        "description": "why the SHOWN step does not hold / the obligation is not discharged",
        "severity": "critical|major|minor|info",
        "observability_level_required": 1,
        "evidence": [{"claim_id": "C0xx", "span": "verbatim substring of that claim",
                      "location": {"file": "...", "section": "..."}}],
        "verdict_local": "fail|warn|clean|needs_external_check",
        "requires_external_check": false,
        "false_positive_risk": "low|medium|high",
        "recommended_reviewer_action": "what to CHECK or ASK — never 'reject'"
      }
    If a theorem's proof has no flaw, emit nothing for it. An empty array [] is a
    valid, honest result.
```

Immediately persist the reviewer's raw response with the **Write** tool to
`$TRACE_DIR/001-proof-review.response.md` (the dir from Step 1) before parsing. It is
the forensic record and the input Step 3 reads. (Write the other trace files now or in
Step 5 — see Step 5 for the exact set.)

**Failure handling.**
- *MCP stall / hang* (common in long sessions): re-invoke the **identical** prompt as a
  **fresh** `mcp__codex__codex` call (gpt-5.5, xhigh) — never `codex-reply`.
- *Reviewer returns prose, not a JSON array*: the Step 3 validator already extracts the
  outermost `[...]`; if there is none, re-ask once with "Output ONLY the JSON array,
  nothing else." Do not hand-author findings on the reviewer's behalf.
- *Many theorems / `— effort: max`*: fan out — issue one **separate fresh**
  `mcp__codex__codex` call per theorem (each gets only that theorem's scaffold block +
  its anchor candidates), and concatenate the arrays before Step 3. Fresh threads are
  fine; carrying context across them via `codex-reply` is not (the bias guard).

## Step 3 — Validate + anchor (the anti-hallucination gate)

The executor enforces the ANCHOR gate **before** keeping anything — exactly the rule
`tools/adjudicate_findings.py` re-applies, so nothing you keep gets silently rejected
downstream. The span must be a verbatim, whitespace-normalized **substring of** the
cited claim (`span in base`, never `base in span` — appending hallucinated text to a
real claim must fail). This validator also keeps the output **strictly family-G**:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"
PROPOSED="<abs path to the saved raw reviewer response from Step 2>"
OUT="$(dirname "$LEDGER")/proof-derivation-forensics.findings.json"
python3 - "$LEDGER" "$PROPOSED" "$OUT" <<'PY'
import json, re, sys
ledger_path, proposed_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

def nw(s):                                    # mirror adjudicator _norm_ws (whitespace only)
    return " ".join((s or "").split())

GFAMILY = {"HP-PROOF-OBLIGATION-GAP", "HP-PROOF-CIRCULARITY", "HP-DERIVATION-INVALID",
           "HP-SYMBOL-SEMANTIC-DRIFT", "HP-ASSUMPTION-SMUGGLE", "HP-UNDEFINED-NOTATION"}
# fallback observability tier per pattern (taxonomy 0.5 lowest-decidable level) — used
# ONLY when the reviewer omitted/garbled the field. ALL family-G patterns default to L1:
# a verdict-bearing proof/derivation flaw is decided from the LaTeX SOURCE, because
# PDF-extracted math is unreliable (mangled symbols, subscripts, equation structure) — an
# L0 (PDF-only) "this step is invalid" risks flagging an extraction artifact. An unknown/
# missing pattern fails closed to L2 (auto-demotes at L0/L1).
OBS = {"HP-PROOF-OBLIGATION-GAP": 1, "HP-PROOF-CIRCULARITY": 1, "HP-DERIVATION-INVALID": 1,
       "HP-SYMBOL-SEMANTIC-DRIFT": 1, "HP-ASSUMPTION-SMUGGLE": 1, "HP-UNDEFINED-NOTATION": 1}
SEV = {"critical", "major", "minor", "info"}
VL  = {"fail", "warn", "clean", "needs_external_check"}
FPR = {"low", "medium", "high"}
ABOVE_INFO = {"critical", "major", "minor"}

ledger = json.load(open(ledger_path, encoding="utf-8"))
claims = {c["claim_id"]: c for c in ledger.get("claims", []) if c.get("claim_id")}

raw = open(proposed_path, encoding="utf-8").read()
m = re.search(r"\[.*\]", raw, re.S)           # tolerate prose / code-fence wrapping
proposed = json.loads(m.group(0) if m else raw)
if isinstance(proposed, dict):                # tolerate {"findings": [...]}
    proposed = proposed.get("findings", [])

kept, dropped_nonG, demoted = [], 0, 0
n = 0
for f in proposed:
    if not isinstance(f, dict):
        dropped_nonG += 1; continue
    pid = f.get("pattern_id")
    # SCOPE: this skill emits ONLY family-G. A set pattern_id outside G is routed
    # elsewhere (consistency/citation/experiment/presentation) -> drop, logged. A
    # missing pattern_id is kept (forensic record) but fail-closes its observability.
    if pid is not None and pid not in GFAMILY:
        dropped_nonG += 1; continue
    n += 1
    f["finding_id"] = f"F{n:03d}"
    f["skill"] = "proof-derivation-forensics"
    # enum hygiene: any illegal value -> safe default
    if f.get("severity") not in SEV: f["severity"] = "info"
    if f.get("verdict_local") not in VL: f["verdict_local"] = "warn"
    if f.get("false_positive_risk") not in FPR: f["false_positive_risk"] = "high"
    if f["verdict_local"] == "needs_external_check":
        f["requires_external_check"] = True
    # ANCHOR gate: span must be a verbatim, ws-normalized SUBSTRING of its cited claim
    anchored = []
    for ev in (f.get("evidence") or []):
        if not isinstance(ev, dict):              # tolerate a stray string/None evidence item
            continue
        cid, span = ev.get("claim_id"), nw(ev.get("span", ""))
        c = claims.get(cid)
        if c and span and span in nw(c.get("text_span", "")):   # span IN claim, not claim IN span
            ev.setdefault("location", c.get("location", {}))     # enrich for human navigation
            ev.setdefault("artifact_hash", c.get("evidence_anchor", ""))
            anchored.append(ev)
    f["evidence"] = anchored
    if f["severity"] in ABOVE_INFO and not anchored:
        f["severity"] = "info"; demoted += 1                     # unanchored -> info (adjudicator would too)
    # a family-G finding above info MUST name one of the 6 G patterns; non-G ids were
    # already dropped, so a MISSING pattern_id here cannot carry weight -> info.
    if pid not in GFAMILY and f["severity"] in ABOVE_INFO:
        f["severity"] = "info"; demoted += 1
    # observability:
    olr = f.get("observability_level_required")
    olr_explicit = (not isinstance(olr, bool)) and isinstance(olr, int) and (0 <= olr <= 3)
    if not olr_explicit:
        # missing/garbled -> a written-proof flaw is decided from the LaTeX source (L1);
        # unknown pattern fail-closes to L2.
        olr = 1 if pid in GFAMILY else 2
    elif pid in GFAMILY and olr > 1 and f["severity"] in ABOVE_INFO:
        # reviewer EXPLICITLY marked an owned G finding as needing code/results (>=L2).
        # family-G validity is decided from the WRITTEN proof, so >=L2 means this finding is
        # mis-routed / over-claimed -> demote to info (do NOT silently clamp it down to L1).
        f["severity"] = "info"; demoted += 1
    # family-G floor: a verdict-bearing proof/derivation finding needs the LaTeX source (L1) —
    # PDF-extracted math is unreliable, so an L0 G finding must not raise the verdict. Clamp UP
    # to L1 (conservative: RAISES the observability bar -> auto-demotes at an L0 run; unlike the
    # >L2 case above, clamping up never launders an over-claim into a pass).
    if pid in GFAMILY and isinstance(olr, int) and olr < 1:
        olr = 1
    f["observability_level_required"] = olr
    # cross-model provenance (reviewer-independence: this is a proposal, not a verdict)
    f["reviewer"] = {"model": "gpt-5.5", "reasoning": "xhigh", "deterministic": False}
    kept.append(f)

json.dump(kept, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"validated {len(kept)} family-G findings "
      f"({demoted} demoted to info for unanchored span, "
      f"{dropped_nonG} dropped: non-G pattern routed elsewhere / malformed) -> {out_path}")
PY
```

**Scope of this gate: anchoring + schema hygiene + family-G enforcement** — verbatim-span
anchoring, enum coercion, non-G pattern rejection, observability fallback, and
cross-model provenance — so every kept finding is well-formed, honestly anchored, and
in this skill's lane. It does **not** compute the verdict, the FP-risk cap, or the
observability *downgrade* against the run level; those belong to
`tools/adjudicate_findings.py`, the single decider. Note this skill applies **no
critical-floor** (unlike consistency-audit's `HP-SUSPICIOUS-REGULARITY`): family-G
flaws legitimately reach `critical`, so the reviewer's honest `severity` + `false_positive_risk`
are preserved verbatim and the adjudicator's FP cap does the rest.

**Failure handling.** A `JSONDecodeError` means the reviewer output was malformed →
re-run Step 2 with the strict-JSON reminder. If a finding loses all evidence, it is
*kept as info* (never silently dropped — the forensic record stays).

## Step 4 — Emit (one file)

Step 3 wrote `proof-derivation-forensics.findings.json` (validated family-G findings).
This is the **only** findings file for this skill — there is no deterministic
companion (no arithmetic tool exists for family G; proof validity is semantic). If the
reviewer found nothing (or `HAS_PROOFS = no` / `CLAIMS == 0`), the file is `[]` — write
it anyway. **Silent skip is forbidden**: the orchestrator and the standalone
adjudicate command both expect the file to exist at a predictable path. The id
namespace is `F###`, disjoint from every other skill's, so the orchestrator's glob
concatenates it exactly once.

## Step 5 — Trace (forensic; never silently dropped)

You created `$TRACE_DIR` in Step 1
(`.aris/traces/proof-derivation-forensics/<date>_run<NN>/`, `NN` from `01`). This repo
ships no `save_trace.sh`, so use the **Write** tool to write these files into it (the
`response.md` and `obligation-ledger.md` were already saved in Steps 1–2):

```
$TRACE_DIR/
  run.meta.json                  # {skill, paper_id, run_level_L, taxonomy_version:"0.5", has_proofs, generated_at}
  obligation-ledger.md           # Step 1 — the EXTRACTION-ONLY scaffold (no verdicts)
  001-proof-review.request.json  # the exact prompt sent (paths + scaffold + checklist, no proof summaries)
  001-proof-review.response.md   # the FULL raw reviewer response (input to Step 3)
  001-proof-review.meta.json     # {model:"gpt-5.5", reasoning:"xhigh", thread_id, sandbox:"read-only"}
```

For a per-theorem fan-out, write `00N-proof-review.{request.json,response.md,meta.json}`
per theorem call (one triple per fresh thread). The `request.json` is the independence
audit trail — it must show the executor sent only **paths + the scaffold + the
checklist**, never a digest or pre-judgment of the proof. Paste the actual codex
`thread_id` into each per-call `.meta.json`.

## Step 6 — Hand off, or adjudicate standalone

Within `/anti-autoresearch`, stop here: the orchestrator globs every `*.findings.json`,
runs the adjudicator over the union of all skills' findings, and emits `REPORT.md` +
`report.json`. When running this skill **alone**, you may produce the report yourself —
`--ledger` is **required** (it re-verifies each finding quotes a real ledger span; the
adjudicator will not run without it, and its anchor gate is itself fail-closed — an
above-info finding it cannot anchor is demoted to `info`):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"; D="$(dirname "$LEDGER")"
python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "$D/proof-derivation-forensics.findings.json" \
    --ledger "$LEDGER" \
    --paper-id "<PAPER_ID>" --observability-level <L> --taxonomy-version 0.5 \
    --out "$D/report.json" --md "$D/REPORT.md"
```

The adjudicator applies, in order: ANCHOR → OBSERVABILITY → FP-RISK → MEMO → SURFACE
gates, then computes `overall_verdict` ∈ {CLEAN_GIVEN_EVIDENCE, SOFT_FLAGS,
HARD_FLAGS}. This skill is **verdict-bearing** (`dimension: proof`) and is neither
memo-only nor surface-only, so a span-anchored **critical** family-G finding that is
decidable at `L` (e.g. a circular proof, or an invalid step the headline depends on)
**reaches HARD_FLAGS** — with `false_positive_risk: low`, since the FP-RISK gate caps
high→minor and medium→major. No model is in the final decision. Treat a single-skill
report as a PREVIEW — the paper's verdict comes from the orchestrator over all
dimensions.

## Output contract

This skill **always** writes, into the ledger's directory:

- `proof-derivation-forensics.findings.json` — Step 3/4, a JSON array
  (`schemas/finding.schema.json`); validated family-G findings (or `[]`). Each
  above-info finding carries `evidence[].claim_id` + a verbatim `span`,
  `observability_level_required: 1` (family-G is verdict-bearing at L1), a `pattern_id`
  ∈ the five owned patterns, and `reviewer.deterministic: false`.
- `.aris/traces/proof-derivation-forensics/<date>_run<NN>/` — Steps 1/2/5: the
  extraction-only `obligation-ledger.md` and the raw reviewer call(s).

It writes **no verdict and no report** of its own — `report.json` / `REPORT.md` come
only from `tools/adjudicate_findings.py` (Step 6 / the orchestrator). The
human-readable rendering is the orchestrator's job, not this skill's.

## Key rules

- **Decide from the written proof.** Validity of written mathematics is decidable from
  the LaTeX source (L1) — verdict-bearing at L1, never needing code or results; an L0
  PDF-only read surfaces `info` only, because PDF-extracted math is unreliable. We assert
  *the step shown does not hold / the obligation is not discharged*, never *fabricated* /
  *faked* / *reject*. The tool is agnostic to authorship — it audits the argument, not provenance.
- **No span → no severity.** Every `critical`/`major`/`minor` finding must quote a
  verbatim substring of a real ledger claim. Enforced by the executor (Step 3) and
  again by the adjudicator; unanchored findings are demoted to `info`, never deleted.
- **Span direction + escapes.** Anchoring is `span in claim.text_span`
  (whitespace-normalized **only**), never the reverse. Quote LaTeX escapes (`\le`,
  `\%`, `\alpha`) exactly; un-escaping breaks the match.
- **Recall is bounded by the ledger; that is honest, not a bug.** The extractor has no
  theorem/proof spans — a pure-symbol step covered by no `number`/`scope`/`citation`
  claim cannot rise above `info`. Step 1's anchor-candidate list tells the reviewer
  where it can ground; uncovered steps stay `info`. Recall is materially higher at L1.
- **Family G only.** Emit only the five owned patterns. Abstract-vs-theorem scope →
  consistency-audit + adversarial-case-builder; citation existence/context →
  citation-forensics; results arithmetic → consistency-audit; code/result fraud →
  experiment-forensics. The Step-3 validator drops any non-G `pattern_id`.
- **Critical is earned, not floored.** Family-G findings legitimately reach `critical`
  (circular proof; invalid step / smuggle / inverted symbol the headline depends on) —
  but only with `false_positive_risk: low` and `observability_level_required ≤ L`.
  Counterexample-first: try to break the step before grading it.
- **Reviewer ≠ adjudicator.** The model proposes findings; `adjudicate_findings.py`
  decides the verdict. This skill emits findings only.
- **Cross-model, fresh thread.** Reviewer is a different family (gpt-5.5 xhigh); every
  run — and every fan-out theorem — is a new `mcp__codex__codex` thread; `codex-reply`
  is never used (the bias guard).
- **Scaffold extracts, never adjudicates.** The obligation ledger records obligations +
  location pointers only; soundness is the reviewer's call, the verdict the
  adjudicator's. The scaffold is not `claims.json` and not the anchor substrate.
- **Detect-only.** Never edit the audited paper (reviewer sandbox is read-only; `Edit`
  is absent from `allowed-tools`). There is no fix loop — that is `proof-checker`'s
  job, on your own paper, not this third-party forensic tool's.
- **Reproducible.** Same ledger + same findings → same verdict, no model in the loop.

## When NOT to use this skill

- **No `claims.json` yet** → run `/evidence-ledger` first; this skill never invents
  structure from the raw PDF.
- **The paper has no proofs/theorems/derivations** (`HAS_PROOFS = no`) → nothing for
  family G to audit; write `[]` and stop (the proof analog of `NOT_APPLICABLE`).
- **You want to FIX a proof, or it's your OWN paper** → use ARIS `/proof-checker`
  (verify-and-fix, re-review rounds, audit report). This skill is detect-only third-party
  forensics: it proposes findings and never edits.
- **The mismatch is abstract/title generality vs a narrow theorem** →
  `/consistency-audit` owns `HP-THEOREM-SCOPE-DRIFT`; the headline framing →
  `/adversarial-case-builder`. Emit only the proof-internal smuggle here.
- **You need citation existence / wrong-context** → `/citation-forensics` (this skill
  only checks whether a cited theorem's *hypotheses* were discharged at the point of
  use).
- **You need results-table arithmetic / aggregation / number coherence** →
  `/consistency-audit`.
- **You need code/result-level fraud** (fake GT, self-normalization, phantom numbers)
  → `/experiment-forensics` at **L2**; family G is decided at L1 and never reaches for code.
- **You want an "is this AI-written math" verdict** → out of scope. We assert a step
  does not hold, not who or what wrote it; surface hints live in
  `/presentation-signals` (auxiliary, capped at minor).
- **On a timer** → never `/loop` / `/schedule` / `CronCreate` this skill; re-fire only
  when the paper or ledger changes (see the fence at the top).

## Review tracing (`.aris/traces/proof-derivation-forensics/<date>_run<NN>/`)

Every run leaves a forensic trail under
`.aris/traces/proof-derivation-forensics/<YYYY-MM-DD>_run<NN>/` (`NN` from `01`,
incremented per run/day — created in Step 1):

| File | Written | Content |
|------|---------|---------|
| `run.meta.json` | Step 5 | `{skill, paper_id, run_level_L, taxonomy_version:"0.5", has_proofs, generated_at}` |
| `obligation-ledger.md` | Step 1 | the extraction-only obligation scaffold (statements, typed symbols, obligations, anchor candidates) — **no validity verdicts** |
| `00N-proof-review.request.json` | Step 5 | the exact prompt sent to the reviewer (paths + scaffold + checklist, no proof summary / no pre-judgment) — the **independence audit trail** |
| `00N-proof-review.response.md` | Step 2 | the FULL raw reviewer response (the input Step 3 parsed) |
| `00N-proof-review.meta.json` | Step 5 | `{model:"gpt-5.5", reasoning:"xhigh", thread_id, sandbox:"read-only"}` |

`N` is `001` for a single review, or one triple per theorem under fan-out. Traces are
**never silently dropped**: they let a human re-audit that the reviewer saw only
paths + the scaffold + the checklist (not a digest of the proof), that each finding's
span is a verbatim ledger substring, and that the verdict is reproducible from the
saved findings + the adjudicator alone.
