---
name: anti-autoresearch
description: "End-to-end substantive-integrity forensic sweep of a research paper (especially autoresearch / AI-Scientist-style output). Orchestrates the whole pipeline: ingest (arxiv-id | pdf | dir → working dir + pdftotext for L0) → /evidence-ledger (artifact manifest + observability level L0/L1/L2 + span-anchored claims.json) → fan out the integrity auditor skills (consistency, citation, baseline, experiment, presentation, proof-derivation, eval-design — each reads the ledger, emits span-anchored findings) + the zero-verdict-weight AIS writing-style track → advisory memos (/adversarial-case-builder + /novelty-duplication-advisory, no verdict weight) → deterministic tools/adjudicate_findings.py (--ledger REQUIRED) → reviewer-ready Integrity Forensics Report. Cross-model (fresh codex per dimension) and reviewer≠adjudicator: the model proposes findings, the deterministic adjudicator decides the verdict. Observability-aware, detect-only, never an opaque AI-text classifier (a separate zero-weight AIS section lists AI writing-style impressions, never moving the verdict). Triggers: \"anti-autoresearch\", \"integrity audit this paper\", \"forensic review\", \"audit a submission\", \"审一篇投稿的诚信\"."
argument-hint: [paper-dir | pdf-path | arxiv-id]
allowed-tools: Bash(*), Read, Write, Grep, Glob, Skill, WebSearch, WebFetch, mcp__codex__codex, mcp__mcp-dblp__search, mcp__mcp-dblp__fuzzy_title_search, mcp__mcp-dblp__get_venue_info
---

# /anti-autoresearch — the orchestrator

Run a full substantive-integrity forensic pass on **$ARGUMENTS** and hand a human
reviewer / area chair an evidence-first Integrity Forensics Report.

> 🔒 **External cadence: the verdict is not a poll.** The pipeline is the
> verdict-producing path — its output changes only when the **paper / repo / ledger**
> changes, not with the clock. **Do not** wrap `/anti-autoresearch` (or any auditor
> sub-skill) in `/loop` / `/schedule` / `CronCreate` to "re-check". A heartbeat may
> only *wait on* the **external** steps that precede the verdict (an arXiv download, a
> citation web lookup) — never re-fire the adjudicated verdict, and never "decide the
> paper is fine now." Re-run the sweep when the inputs change; that is the only honest
> trigger.

> 🛡️ **The dual of ARIS.** ARIS ships an internal audit stack so its *own* autoresearch
> output stays honest; Anti-Autoresearch is that same audit DNA **pointed outward** at a
> third party's submission. This is decision **support** for a human — it surfaces
> span-anchored discrepancies to investigate. It is **not** an AI-text detector and it
> does **not** judge misconduct (`DESIGN.md` §1; `references/`).

## Why this exists

A machine-driven research pipeline (or rushed human) writes the abstract, the tables,
the method section, the bibliography, and the appendix in separate passes and never
reconciles them. The result is a paper that disagrees with itself, cites papers that do
not exist or argue the opposite, claims SOTA while omitting the obvious baseline, or
reports numbers the code never computed. Six LLMs each re-reading the PDF would
hallucinate six different structures and invite the obvious dismissal — *"an LLM
grading another LLM's paper is just slop."*

This orchestrator answers that structurally. **One deterministic pass** turns the paper
into a hashed, span-anchored evidence ledger; **six auditors** read only that ledger
and *propose* findings; a **deterministic adjudicator** *decides* the verdict by fixed
rules with no model in the loop; and **observability levels** make it impossible to
shout "fraud" from a PDF. Same artifacts → same ledger → same verdict.

## Pipeline role (what this run does, and never does)

```
[0] ingest          arxiv-id | pdf | dir  →  working dir (+ pdftotext text for L0)
        │
        ▼
[1] /evidence-ledger   tools/build_manifest.py + tools/build_claim_ledger.py
        │              → artifact_manifest.json (derives observability level L)
        │              → claims.json   (span-anchored, hashed; the ONLY structure auditors read)
        ▼
[2] fan out auditors (each reads the ledger, emits <skill>.findings.json):
        consistency-audit          (always · flagship · deterministic arithmetic + semantic)
        citation-forensics         (if ≥1 citation claim)
        baseline-comparison-audit  (if ≥1 comparison / SOTA scope claim)
        experiment-forensics       (always · L0/L1 = info "could-not-verify" · L2 = full code audit)
        presentation-signals       (always · AUXILIARY · capped at minor)
        ai-style-impressions       (always · AIS track · NOT integrity · zero verdict weight)
        proof-derivation-forensics (if ≥1 theorem/proof/derivation claim · verdict-bearing · dim=proof · L1 source, CAN reach HARD_FLAGS; L0 PDF-only → info)
        eval-design-forensics      (if ≥1 comparison/eval claim · family H · dim=evaluation · L0/L1 stated-tells: leakage / judge-validity / selective-reporting)
        │
        ▼
[3] advisory memos (each reads the ledger + merged findings · NO verdict weight):
        /adversarial-case-builder      → adversarial-case-builder.memo.md       (strongest evidence-bound objection)
        /novelty-duplication-advisory  → novelty-duplication-advisory.memo.md   (if ≥1 contribution claim · MEMO-ONLY · prior-work overlap · capped at info)
        │
        ▼
[4] tools/adjudicate_findings.py  --ledger REQUIRED  → report.json + REPORT.md
        │   gates (in order): ANCHOR → OBSERVABILITY → FP-RISK → MEMO → SURFACE
        │   overall_verdict ∈ {CLEAN_GIVEN_EVIDENCE, SOFT_FLAGS, HARD_FLAGS}  (rules, no model)
        ▼
[5] present REPORT.md to the human (verdict + level first; state what could NOT be checked)
```

- **Auditors propose; the adjudicator decides.** No auditor (and not this orchestrator)
  ever computes `overall_verdict`; only `tools/adjudicate_findings.py` does, by fixed
  rules (`references/reviewer-independence.md` Layer 2; `DESIGN.md` §3).
- **Detect-only.** No step ever edits the audited paper or repo. This is a third-party
  forensics tool, never a co-author (no `Edit` is granted; the reviewer sandbox is
  `read-only`).
- **Observability caps everything.** L0 (PDF-only) / L1 (source) **cannot** assert
  code/result-level fraud — those need L2 (repo + results). The adjudicator demotes any
  finding above the run's level (`references/observability-levels.md`; `DESIGN.md` §4).

## Constants & conventions

```
REVIEWER_MODEL     = gpt-5.5  (via mcp__codex__codex) — a DIFFERENT model family from the executor (Claude)
REVIEWER_REASONING = xhigh    — always; the effort knob never lowers reviewer quality
REVIEWER_SANDBOX   = read-only — detect-only; the reviewer never mutates the paper
THREAD_POLICY      = FRESH mcp__codex__codex per dimension / per cited key; NEVER codex-reply across them
                     (codex-reply is deliberately NOT in allowed-tools — the bias guard)
RUN_THREADS        = serial   — one codex thread at a time; concurrent codex MCP calls can hang
LEDGER_VERSION     = 0.1       (stamped by tools/build_claim_ledger.py)
TAXONOMY_VERSION   = 0.5       (references/hack-pattern-taxonomy.md; 46 integrity patterns A–H + 13 AIS impressions + 2 ADV advisory; stamped into every report)
OBSERVABILITY      = derived   L0 (pdf/text) · L1 (latex, no results) · L2 (repo + results); L3 NEVER (no reproduction)
ADJUDICATOR        = deterministic-rules-v0   (tools/adjudicate_findings.py — the ONLY verdict source)
DETECT_ONLY        = true · EMITS_VERDICT = true (computed by code, not by a model)
REAL TOOLS (resolve ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)):
   tools/build_manifest.py · tools/build_claim_ledger.py · tools/check_numeric_consistency.py
   · tools/check_presentation.py · tools/adjudicate_findings.py   (confirm flags with --help; never invent flags)
OUTPUTS (in PAPER_DIR) — artifact_manifest.json · claims.json · <skill>.findings.json (+ *.deterministic.findings.json)
   · adversarial-case-builder.memo.md · report.json · REPORT.md · .aris/traces/<skill>/<date>_run<NN>/
```

**Overrides** (pass after `—`): `effort: balanced` (default) | `max` (auditors fan the
checklist into more fresh threads for breadth) · `enrich: true` (default; the ledger's
additive semantic pass) | `false` · `human checkpoint: false` (default) | `true` (pause
after Step 1 to confirm L, and before Step 5). Example:
`/anti-autoresearch ~/papers/submission — effort: max, human checkpoint: true`.

> ⚠️ **Shell state does not persist between Bash calls** (cwd + env reset each call).
> Every block below re-derives `ROOT` and `PAPER_DIR` at its top and reads `L` /
> `PAPER_ID` from `claims.json` (the authoritative source after Step 1). Never rely on a
> variable set in an earlier block, and never `cd` into the paper dir. Keep `PAPER_DIR`
> **space-free** (simplest way to stay safe across the inline `*.tex` / `*.findings.json` globs).

## Execution modes & the Reviewer Calling Convention

**Pick the mode automatically — both produce the *identical* file set, and Step 4 (the
verdict) is byte-deterministic given those files + the ledger.**

- **Delegation (default — if the `Skill` tool is available):** invoke `/evidence-ledger`,
  the six auditors, and the two advisory memos (`/adversarial-case-builder` +
  `/novelty-duplication-advisory`). Each sub-skill runs its own
  deterministic tools + its exact codex reviewer prompt + its own anchor validation, and
  writes its `<skill>.findings.json`. The orchestrator validates the emitted files and
  adjudicates. This mirrors ARIS `/research-pipeline` delegating all GPT review to
  `/auto-review-loop` rather than prompting GPT itself.
- **Inline (fallback — only shell + Read/Write + codex MCP):** run the deterministic
  tools yourself with the exact commands below; for each cross-model dimension open a
  **fresh** `mcp__codex__codex` thread, send the **verbatim** reviewer-prompt block —
  the fenced `prompt:` / checklist inside that sub-skill's `## Step … — Cross-model …`
  section in `skills/<dim>/SKILL.md` (Read it — the single source of truth; fill its
  `[...]` inputs from `claims.json`), save the raw reply, then run the **shared anchor gate**
  (Step 2) to produce the validated `<dim>.findings.json`.

The orchestrator's job is to guarantee the *envelope* and the *independence invariants*
every reviewer call obeys:

- **Envelope (every auditor instantiates this exact shape):**
  ```text
  mcp__codex__codex:
    model: gpt-5.5
    config: {"model_reasoning_effort": "xhigh"}
    sandbox: read-only
    cwd: <absolute PAPER_DIR>          # so the reviewer reads claims.json + sources directly
    prompt: |
      <the auditor's per-dimension checklist + the SIX HARD RULES below>
  ```
- **The executor passes only structured inputs** — paths + the ledger (`claims.json`) +
  the per-dimension checklist + the run level `L`. It **never** summarizes the paper,
  pre-judges, leaks a hunch, or whispers "this is probably AI-generated"
  (`references/reviewer-independence.md` Layer 1; the tool is agnostic to authorship).
- **Six hard rules the orchestrator requires in every auditor's prompt** (a finding that
  breaks one is structurally worthless): **(1) ANCHOR** — every above-`info` finding
  carries ≥1 `evidence{claim_id, span}` where `claim_id` exists in `claims.json` and
  `span` is a *verbatim, whitespace-normalized substring of that claim's `text_span`*
  (`span in claim`, never `claim in span`); **(2) DISCREPANCY, NOT ACCUSATION** —
  describe what to *check/ask*, never "reject"/"fabricated"; **(3) OBSERVABILITY** — set
  `observability_level_required` to the lowest tier at which the discrepancy is decidable
  (code/result confirmation ⇒ `2`); **(4) HONEST FP RISK** — set `false_positive_risk`
  truthfully (legit "best config", labeled pilots, rounding, deterministic metrics are
  common FPs); **(5) HAND OFF EXTERNAL CLAIMS** — "first / SOTA" the text cannot settle ⇒
  `verdict_local: needs_external_check` + `requires_external_check: true`; **(6)
  pattern_id ∈ taxonomy v0.4 only**.
- **Reviewer ≠ adjudicator.** The reviewer *proposes* findings; only
  `tools/adjudicate_findings.py` *decides* the verdict (Layer 2). The model is demoted
  from judge to evidence-extractor.
- **Fresh thread per dimension, serial.** A new `mcp__codex__codex` call per auditor (and
  per cited key inside `citation-forensics`); **never** `codex-reply` carrying one
  dimension's conclusions into another (the bias guard). Keep the calls **serial** —
  concurrent codex threads can hang; fan-out buys *breadth of dimensions*, not
  parallelism. On a stall, re-invoke the *identical* prompt in a fresh thread (never
  `codex-reply`); if it still fails, write `[]` and continue — a dead reviewer must never
  become a fabricated finding.

## Re-entrancy: resuming a partial / re-run sweep

The pipeline is a **pure function of `PAPER_DIR`'s contents** — every step writes a
predictable file, so a crashed or repeated run resumes by *probing what already exists*.
There is no run-state file and no "accepted vs done" gate, because **Step 4 recomputes
the verdict deterministically** from whatever findings are present every time. Probe
completeness *and staleness* before redoing work:

```bash
PAPER_DIR="<from Step 0>"
python3 - "$PAPER_DIR" <<'PY'
import json, os, glob, sys
D = sys.argv[1]
def is_array(p):
    try: return isinstance(json.load(open(p, encoding="utf-8")), list)
    except Exception: return False
def is_ledger(p):
    try:
        d = json.load(open(p, encoding="utf-8")); return isinstance(d, dict) and "claims" in d
    except Exception: return False
def newest_source(d):
    s = []
    for ext in ("*.tex", "*.txt", "*.bib"):
        s += glob.glob(os.path.join(d, ext)) + glob.glob(os.path.join(d, "**", ext), recursive=True)
    return max((os.path.getmtime(p) for p in s), default=0.0)
led = os.path.join(D, "claims.json"); have = is_ledger(led)
stale = have and os.path.getmtime(led) < newest_source(D)
print(f"STEP1 ledger      : {'present' if have else 'MISSING'}{'  ⚠ STALE → rebuild (sources changed)' if stale else ''}")
for f in ("consistency-audit.deterministic", "consistency-audit", "citation-forensics",
          "baseline-comparison-audit", "experiment-forensics",
          "presentation-signals.deterministic", "presentation-signals",
          "proof-derivation-forensics", "eval-design-forensics",
          "ai-style-impressions.deterministic", "ai-style-impressions"):
    p = os.path.join(D, f + ".findings.json")
    print(f"STEP2 {f:<32}: {'ok' if (os.path.isfile(p) and is_array(p)) else 'todo'}")
print(f"STEP3 adversarial memo            : {'present' if os.path.isfile(os.path.join(D,'adversarial-case-builder.memo.md')) else 'todo'}")
print(f"STEP3 novelty advisory memo       : {'present' if os.path.isfile(os.path.join(D,'novelty-duplication-advisory.memo.md')) else 'todo'}")
print(f"STEP4 report.json : {'present' if os.path.isfile(os.path.join(D,'report.json')) else 'todo'}")
PY
```

Rule: a **stale ledger forces a full rebuild** (Step 1 → re-fan Step 2 → re-adjudicate)
— stale findings anchored to an old ledger are worse than none. If the ledger is fresh,
skip Step 1 and only re-run the auditors marked `todo`. Always re-run Step 4 (cheap,
deterministic, the only verdict source). Re-running from scratch is always safe — same
inputs → same outputs.

---

## Step 0 — Ingest: resolve the input to a working dir

Turn `$ARGUMENTS` (a directory, a PDF, or an arXiv id) into a single **working
directory** (`PAPER_DIR`) that contains the best source the level allows. Prefer LaTeX
(stable `file:line` spans → L1) over PDF text (best-effort → L0); leave any `code/` +
`results/` in place so the manifest can derive L2.

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
test -f "$ROOT/tools/adjudicate_findings.py" || { echo "FATAL: not inside the Anti-Autoresearch checkout (point ROOT at it)."; exit 1; }
ARG="$ARGUMENTS"

if [ -d "$ARG" ]; then                       # ---- DIRECTORY ----
  PAPER_DIR="$(cd "$ARG" && pwd)"
  # if only a PDF is present, extract text so the ledger has an L0 source.
  # Deterministic primary-PDF pick (issue #11) — never lexicographic-first: a dir
  # holding only figure/supplement PDFs yields NO pick (exit 1, honest) instead of
  # extracting a figure as the paper. Only exit 1 is tolerated.
  if ! ls "$PAPER_DIR"/*.tex >/dev/null 2>&1 && ! ls "$PAPER_DIR"/*.txt >/dev/null 2>&1; then
    P=$(python3 "$ROOT/tools/select_primary_pdf.py" "$PAPER_DIR"); rc=$?
    [ "$rc" -le 1 ] || { echo "FATAL: select_primary_pdf.py failed (rc=$rc)"; exit 1; }
    [ -n "$P" ] && pdftotext -layout "$P" "$PAPER_DIR/paper.txt"
  fi

elif [ -f "$ARG" ] && case "$ARG" in *.pdf) true;; *) false;; esac; then   # ---- PDF FILE ----
  PAPER_DIR="$(cd "$(dirname "$ARG")" && pwd)"
  pdftotext -layout "$ARG" "$PAPER_DIR/paper.txt" \
    || echo "WARN: pdftotext failed/missing — try: mutool draw -F txt, or pip install pdfminer.six (pdf2txt.py)."

else                                          # ---- ARXIV ID (e.g. 2401.01234) ----
  ID=$(printf '%s' "$ARG" | grep -oE '[0-9]{4}\.[0-9]{4,5}(v[0-9]+)?' | head -1)
  [ -n "$ID" ] || { echo "FATAL: '$ARG' is not a dir, a .pdf, or an arXiv id."; exit 1; }
  PAPER_DIR="$(pwd)/aar-$ID"; mkdir -p "$PAPER_DIR"
  # LaTeX source first (best spans → L1). e-print may be a tarball OR a single gzipped .tex.
  if curl -fsSL "https://arxiv.org/e-print/$ID" -o "$PAPER_DIR/src.tgz"; then
    tar -xzf "$PAPER_DIR/src.tgz" -C "$PAPER_DIR" 2>/dev/null \
      || gunzip -c "$PAPER_DIR/src.tgz" > "$PAPER_DIR/main.tex" 2>/dev/null
  fi
  if ! ls "$PAPER_DIR"/*.tex >/dev/null 2>&1; then     # fallback: PDF → text (L0)
    curl -fsSL "https://arxiv.org/pdf/$ID.pdf" -o "$PAPER_DIR/paper.pdf" \
      && pdftotext -layout "$PAPER_DIR/paper.pdf" "$PAPER_DIR/paper.txt"
  fi
fi

echo "PAPER_DIR = $PAPER_DIR"
ls -1 "$PAPER_DIR"/*.tex "$PAPER_DIR"/*.bib "$PAPER_DIR"/*.txt "$PAPER_DIR"/*.pdf 2>/dev/null
ls -d  "$PAPER_DIR"/code "$PAPER_DIR"/src "$PAPER_DIR"/results "$PAPER_DIR"/outputs 2>/dev/null   # L2 candidates
```

**Validation gate.** `PAPER_DIR` must now contain **anchorable text** — at least one
`*.tex` or `*.txt`. A bare `*.pdf` is **not** enough: the ledger builders accept only
`--latex` / `--pdf-text`, so Step 0 must have extracted `paper.txt`. If extraction failed
or no source is present, **stop** and report exactly what was searched — there is nothing
to anchor spans against, so there can be no ledger (see Failure handling below).

**Failure handling.**
- *No `pdftotext`* → fall back to `mutool draw -F txt in.pdf out.txt` or
  `pip install pdfminer.six && pdf2txt.py in.pdf > out.txt`. If text extraction is
  impossible, you cannot build an L0 ledger from a PDF — ask the user for the LaTeX.
- *arXiv unreachable* (network gated / proxy needed) → say so and ask the user to drop
  the source or PDF into a local dir, then re-invoke with that **paper-dir**. Never
  fabricate a ledger from an absent paper. (A heartbeat *may* wait on this download — a
  pre-verdict external step — but only the sweep, run once the source lands, produces the
  verdict.)
- *arXiv `.tex` extracted but no obvious `main.tex`* → fine; `/evidence-ledger` globs
  `*.tex`. (`PAPER_ID` is set authoritatively by the ledger in Step 1 — do not hand-pick
  it here.)

## Step 1 — Build the evidence ledger (always first; the spine)

Delegate to `/evidence-ledger`, which runs the real deterministic tools
(`tools/build_manifest.py` → `artifact_manifest.json` + observability level **L**;
`tools/build_claim_ledger.py` → `claims.json`) and, by default, one additive
span-anchored semantic-enrichment pass. Everything downstream reads these two files.

```
/evidence-ledger "<PAPER_DIR>"            # add "— enrich: false" to ship the deterministic backbone alone
```

Then read **L** and **PAPER_ID** back from the ledger — it is the source of truth for
every later block (re-derive, never persist):

```bash
PAPER_DIR="<from Step 0>"
test -f "$PAPER_DIR/claims.json" || { echo "FATAL: /evidence-ledger did not produce claims.json — re-run Step 1."; exit 1; }
L=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["observability_level"])' "$PAPER_DIR/claims.json")
PAPER_ID=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["paper_id"])' "$PAPER_DIR/claims.json")
python3 - "$PAPER_DIR/claims.json" "$PAPER_DIR/artifact_manifest.json" <<'PY'
import json, sys, collections
L = json.load(open(sys.argv[1], encoding="utf-8")); M = json.load(open(sys.argv[2], encoding="utf-8"))
assert L["observability_level"] == M["observability_level"], "ledger level != manifest level"
t = collections.Counter(c["type"] for c in L["claims"])
print(f"PAPER_ID={L['paper_id']}  L={L['observability_level']}  claims={len(L['claims'])}  types={dict(t)}")
PY
```

**Validation gate.**
- `claims.json` exists and `claims` is non-empty. **Zero claims on a paper that visibly
  has numbers/citations** means the ingest source was wrong (e.g. a PDF with no usable
  text, or a dir with no `.tex`/`.txt`) → fix Step 0 and re-run `/evidence-ledger`.
- The ledger's `observability_level` **matches the artifacts present** (a PDF-only run
  MUST be `L=0`; never hand a higher level to anything because a repo "exists somewhere
  else"). The level is the honesty contract for the whole run — carry this `L` forward;
  it caps every finding's severity in Step 4.
- `— human checkpoint: true` → present `L`, the claim-type histogram, and the source
  list, and pause for confirmation before fanning out.

**Failure handling.** If `/evidence-ledger` is unavailable, build the ledger directly
with the real tools (exact flags — confirm via `--help`):
```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); PAPER_DIR="<from Step 0>"
SLUG=$(basename "$PAPER_DIR" | tr -cs 'A-Za-z0-9.' '-')
TXT=(); [ -f "$PAPER_DIR/paper.txt" ] && TXT=(--pdf-text "$PAPER_DIR/paper.txt")
python3 "$ROOT/tools/build_manifest.py" --paper-id "$SLUG" --dir "$PAPER_DIR" "${TXT[@]}" --out "$PAPER_DIR/artifact_manifest.json"
L=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["observability_level"])' "$PAPER_DIR/artifact_manifest.json")
if ls "$PAPER_DIR"/*.tex >/dev/null 2>&1; then
  python3 "$ROOT/tools/build_claim_ledger.py" --paper-id "$SLUG" --latex "$PAPER_DIR"/*.tex --observability-level "$L" --out "$PAPER_DIR/claims.json"
else
  python3 "$ROOT/tools/build_claim_ledger.py" --paper-id "$SLUG" --pdf-text "$PAPER_DIR/paper.txt" --observability-level "$L" --out "$PAPER_DIR/claims.json"
fi
```

## Step 2 — Fan out the six auditors (breadth; the verdict is NOT decided here)

Decide which auditors apply **from the ledger's claim types**, then run each applicable
skill. Each reads `claims.json`, opens a **fresh codex thread per dimension** (a
different model family from the executor), proposes span-anchored findings, validates its
own spans, and writes `<skill>.findings.json` (the deterministic auditors also write
`<skill>.deterministic.findings.json`). The orchestrator only *sequences* these calls and
enforces the Reviewer Calling Convention above — it authors no finding.

```bash
PAPER_DIR="<from Step 0>"
python3 - "$PAPER_DIR/claims.json" <<'PY'
import json, re, sys, os
d = json.load(open(sys.argv[1], encoding="utf-8")); cl = d.get("claims", [])
paper_dir = os.path.dirname(os.path.abspath(sys.argv[1])) or "."
CMP = re.compile(r"state[- ]of[- ]the[- ]art|\bSOTA\b|outperform\w*|\bbest\b|surpass\w*|"
                 r"beats?|superior|first to|compared? (?:to|with)|baseline|prior (?:work|art)", re.I)
has_cite = any(c.get("type") == "citation" for c in cl)
has_cmp  = any(c.get("type") in ("scope", "comparison", "baseline", "caption") and CMP.search(c.get("text_span","")) for c in cl)
# proofs: scan the SOURCE for theorem/proof/derivation markers (mirrors /proof-derivation-forensics's
# own HAS_PROOFS gate). The skill self-guards (writes [] if it finds none), so this gate is a
# budget hint, not a correctness gate — running proof-derivation-forensics unconditionally is safe.
TH  = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|claim|conjecture|"
                 r"proof|definition|assumption)\*?\}", re.I)
EQ  = re.compile(r"\\begin\{(equation|align|gather|multline|eqnarray)\*?\}|\\\[", re.I)
TXT = re.compile(r"\b(Theorem|Lemma|Proposition|Corollary|Proof|Q\.?E\.?D\.?)\b")
ph = 0
for s in d.get("source_files", []):
    sp = s.get("path", ""); kind = s.get("kind", "")
    cand = sp if os.path.isabs(sp) else os.path.join(paper_dir, sp)
    if not os.path.isfile(cand): cand = sp
    try: t = open(cand, encoding="utf-8", errors="replace").read()
    except OSError: continue
    ph += (len(TH.findall(t)) + len(EQ.findall(t))) if kind == "latex" else len(TXT.findall(t))
if ph == 0:                                            # L0 fallback: theorem/proof words inside ledger spans
    ph = sum(1 for c in cl if TXT.search(c.get("text_span", "") or ""))
has_proof = ph > 0
# contribution claims (Step 3 novelty advisory anchor universe): scope/method/comparison OR abstract/intro
CONTRIB_SECT = {"abstract", "intro", "introduction"}
has_contrib = any((c.get("type") in ("scope", "method", "comparison")
                   or ((c.get("location") or {}).get("section", "") or "").lower() in CONTRIB_SECT)
                  and c.get("claim_id") and c.get("text_span") for c in cl)
print("RUN (always): /consistency-audit  /experiment-forensics  /presentation-signals  /ai-style-impressions")
print(f"RUN /citation-forensics            : {has_cite}   (≥1 citation claim)")
print(f"RUN /baseline-comparison-audit     : {has_cmp}    (≥1 comparison/SOTA scope claim)")
print(f"RUN /proof-derivation-forensics    : {has_proof}   (≥1 theorem/proof/derivation marker; self-guards → [] if none)")
print(f"RUN /eval-design-forensics         : {has_cmp}    (≥1 comparison/eval claim · leakage / judge-validity / selective-reporting; self-guards → [] if no eval protocol)")
print(f"RUN /novelty-duplication-advisory  : {has_contrib}   (Step 3 memo · ≥1 contribution claim · MEMO-ONLY)")
PY
```

Run the applicable skills (pass `PAPER_DIR` so each locates the ledger). **Keep the
reviewer calls serial.** Each row's `Writes` column is the exact filename the Step-4 glob
expects; the `Owns` column is the taxonomy-v0.4 patterns that skill may emit:

| Skill | Run when | Writes | Owns (pattern_ids, taxonomy v0.4) |
|-------|----------|--------|-----------------------------------|
| `/consistency-audit "<PAPER_DIR>"` | **always** (flagship; L0-decidable) | `consistency-audit.deterministic.findings.json` (+ semantic `consistency-audit.findings.json`) | HP-NUM-INFLATE, HP-DELTA-ERROR, HP-AGG-DRIFT, HP-DENOM-DRIFT, HP-UNIT-DIR-MISMATCH, HP-CAPTION-MISMATCH, HP-APPENDIX-CONTRA, HP-METHOD-DRIFT, HP-ABLATION-ATTRIB, HP-SCOPE-INFLATE, HP-THEOREM-SCOPE-DRIFT, HP-SUSPICIOUS-REGULARITY(L0→info), HP-ARGUMENT-CHAIN-BREAK, HP-CAUSAL-EVIDENCE-LEAP, HP-ACRONYM-DRIFT, HP-GRANULARITY-IMPOSSIBLE, HP-VARIANCE-IMPOSSIBLE, HP-STAT-INCONSISTENCY |
| `/citation-forensics "<PAPER_DIR>"` | ≥1 `citation` claim | `citation-forensics.findings.json` | HP-CITE-HALLUC, HP-CITE-CONTEXT, HP-CITE-RETRACTED |
| `/baseline-comparison-audit "<PAPER_DIR>"` | ≥1 comparison/SOTA scope claim | `baseline-comparison-audit.findings.json` | HP-MISSING-BASELINE, HP-WEAK-BASELINE, HP-SIG-OVERLAP, HP-DELTA-ERROR(cross-claim), HP-RESOURCE-IDENTITY-MISMATCH |
| `/experiment-forensics "<PAPER_DIR>"` | **always** (depth scales with L) | `experiment-forensics.findings.json` | HP-FAKE-GT, HP-SELF-NORM, HP-PHANTOM-RESULT, HP-DEAD-METRIC, HP-SCOPE-INFLATE(verified), HP-METHOD-DRIFT(L2), HP-SUSPICIOUS-REGULARITY(L2), HP-PLACEHOLDER-DATA(L2), HP-RESULT-ARTIFACT-MISMATCH(L2), HP-MISSING-REPRO-ARTIFACT(L2) |
| `/presentation-signals "<PAPER_DIR>"` | **always** (AUXILIARY, capped at `minor`) | `presentation-signals.deterministic.findings.json` (+ semantic `presentation-signals.findings.json`) | HP-DUP-TABLE, HP-PIPELINE-ARTIFACT, HP-THIN-FLOAT, HP-LLM-FIGURE, HP-PAGE-PADDING |
| `/proof-derivation-forensics "<PAPER_DIR>"` | ≥1 theorem/proof/derivation claim (self-guards: writes `[]` if `HAS_PROOFS=no`) | `proof-derivation-forensics.findings.json` | HP-PROOF-OBLIGATION-GAP, HP-PROOF-CIRCULARITY, HP-DERIVATION-INVALID, HP-SYMBOL-SEMANTIC-DRIFT, HP-ASSUMPTION-SMUGGLE, HP-UNDEFINED-NOTATION |
| `/eval-design-forensics "<PAPER_DIR>"` | ≥1 comparison/eval claim (family H, L0/L1 stated-tells; dim=evaluation) | `eval-design-forensics.findings.json` | HP-EVAL-LEAKAGE, HP-JUDGE-VALIDITY, HP-SELECTIVE-REPORTING |
| `/ai-style-impressions "<PAPER_DIR>"` | **always** (AIS track · NOT integrity · **zero verdict weight** · separate report section) | `ai-style-impressions.deterministic.findings.json` (+ semantic `ai-style-impressions.findings.json`) | AIS-NARRATIVE-ARC-BREAK, AIS-LLM-PHRASE-TICS, AIS-DEFENSIVE-HEDGE, AIS-JARGON-STUFF, AIS-INVENTED-CODENAME, AIS-CLAUSE-FORMULA-WALL, AIS-GRATUITOUS-PSEUDOCODE, AIS-BULLET-LIST-OVERUSE, AIS-BOLD-MODULE-SPAM, AIS-RESTATE-OVERCLAIM, AIS-FOCUS-DRIFT, AIS-SINGLE-STYLE-FIGURES, AIS-APPENDIX-DUMPING-GROUND |

Notes the orchestrator must honor:
- **experiment-forensics always runs**, but at **L0/L1 it emits only info-level
  "could-not-verify" signals** (`observability_level_required: 2`) — never a fraud flag
  from a PDF. Its full line-by-line code audit only fires at **L2**; the eval `file:line`
  is description detail, the **anchor is the paper claim**.
- **presentation-signals is auxiliary**: every finding is `false_positive_risk: high` and
  the adjudicator **caps it at `minor`** (by `SURFACE_ONLY_SKILLS` AND by `SURFACE_PATTERNS`
  `pattern_id`), so the surface dimension can contribute at most `SOFT_FLAGS`, never
  `HARD_FLAGS`. It is **not** an AI-text classifier (`references/hack-pattern-taxonomy.md`
  §F). Most papers ⇒ `[]`.
- **proof-derivation-forensics is verdict-bearing** (`dimension: proof`), but unlike the L2
  code dimensions it **decides from the LaTeX proof source (L1)** — a span-anchored
  **critical** family-G flaw (a circular proof; an invalid step / smuggled assumption /
  inverted symbol the headline theorem depends on) **can reach `HARD_FLAGS` with no repo or
  results**, but needs the **L1 source**: PDF-extracted math is unreliable, so at an L0
  (PDF-only) run family-G findings surface as `info` only. There is **no deterministic companion** (proof validity is semantic), so it
  writes the single `proof-derivation-forensics.findings.json`. It **self-guards**: if the
  paper has no theorem/proof/derivation markers (`HAS_PROOFS=no`) it writes `[]` and never
  calls the reviewer — so running it unconditionally is safe; the decision block only gates
  it for budget. It emits **only the five family-G patterns**; abstract-vs-theorem scope
  drift stays with consistency-audit (`HP-THEOREM-SCOPE-DRIFT`), not here
  (`references/hack-pattern-taxonomy.md` §G).
- A skill that finds nothing — or an optional auditor that does not apply — still writes
  `[]` to its predictable path. **Silent skip is forbidden** (so the run records that the
  dimension ran and was clean, not silently absent): `echo '[]' > "$PAPER_DIR/citation-forensics.findings.json"`.
- **No double-counting.** Each auditor writes its own filename, so the `*.findings.json`
  glob enumerates each file exactly once; the deterministic and semantic passes stay in
  *separate* files. (Finding-id prefixes: `NUM###`/`HL###` numeric, `PRES###`
  presentation, `EF###` experiment, `F###` other semantic. Ids may repeat across
  semantic files; that is cosmetic — the report keys on skill + file, not id.)

**Inline mode only — the shared anchor gate.** When delegation is unavailable, run each
applicable dimension's codex call yourself (envelope + verbatim sub-skill prompt above;
save the raw reply to `$PAPER_DIR/.aris/<dim>.response.md`), then convert that raw reply
into a validated `<dim>.findings.json` with this gate. It enforces invariant #3 exactly
as `tools/adjudicate_findings.py` re-binds it (`span in claim`, never `claim in span`).
`SURFACE=1` only for presentation-signals:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); PAPER_DIR="<from Step 0>"
LEDGER="$PAPER_DIR/claims.json"; SKILL="<dimension>"; SURFACE="<0 or 1>"
mkdir -p "$PAPER_DIR/.aris"   # the fresh-thread raw reply is saved here before this gate runs
RAW="$PAPER_DIR/.aris/$SKILL.response.md"; OUT="$PAPER_DIR/$SKILL.findings.json"
python3 - "$LEDGER" "$RAW" "$OUT" "$SKILL" "$SURFACE" <<'PY'
import json, re, sys
ledger_p, raw_p, out_p, skill, surface = sys.argv[1:6]
surface = surface == "1"
nw = lambda s: " ".join((s or "").split())
SEV={"critical","major","minor","info"}; VL={"fail","warn","clean","needs_external_check"}
FPR={"low","medium","high"}; ABOVE={"critical","major","minor"}
claims = {c["claim_id"]: c for c in json.load(open(ledger_p, encoding="utf-8")).get("claims", []) if c.get("claim_id")}
raw = open(raw_p, encoding="utf-8").read(); m = re.search(r"\[.*\]", raw, re.S)
prop = json.loads(m.group(0) if m else raw)
if isinstance(prop, dict): prop = prop.get("findings", [])
kept = []; n = 0; demoted = 0; capped = 0
for f in prop:
    if not isinstance(f, dict): continue
    n += 1; f["finding_id"] = f"F{n:03d}"; f["skill"] = skill
    if f.get("severity") not in SEV: f["severity"] = "info"
    if f.get("verdict_local") not in VL: f["verdict_local"] = "warn"
    if f.get("false_positive_risk") not in FPR: f["false_positive_risk"] = "high" if surface else "medium"
    if f["verdict_local"] == "needs_external_check": f["requires_external_check"] = True
    if surface:                                   # surface signals: forced high-FP, capped at minor, L0-decidable
        f["false_positive_risk"] = "high"; f["observability_level_required"] = 0
        if f["severity"] in ("critical", "major"): f["severity"] = "minor"; capped += 1
    anchored = []
    for ev in (f.get("evidence") or []):
        cid = ev.get("claim_id"); span = nw(ev.get("span", "")); c = claims.get(cid)
        if c and span and span in nw(c.get("text_span", "")):   # span IN claim, NOT claim IN span
            ev.setdefault("location", c.get("location", {}))
            ev.setdefault("artifact_hash", c.get("evidence_anchor", ""))
            anchored.append(ev)
    f["evidence"] = anchored
    if f["severity"] in ABOVE and not anchored: f["severity"] = "info"; demoted += 1
    # observability_level_required is passed through verbatim — a missing/invalid one is
    # left as-is so the adjudicator's OBSERVABILITY gate fail-closes it to info.
    f["reviewer"] = {"model": "gpt-5.5", "reasoning": "xhigh", "deterministic": False}
    kept.append(f)
json.dump(kept, open(out_p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"{skill}: validated {len(kept)} ({demoted} ->info unanchored, {capped} surface-capped) -> {out_p}")
PY
```

For dimension-specific extras (citation must anchor to a `type:"citation"` claim;
baseline pattern-ownership + cross-row delta dedup; presentation surface allow-list),
prefer the sub-skill's own `Validate + anchor` step — it is a strict superset of this
gate. The deterministic passes have **no** LLM step — run their tools directly:
```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); PAPER_DIR="<from Step 0>"
python3 "$ROOT/tools/check_numeric_consistency.py" --ledger "$PAPER_DIR/claims.json" \
    --out "$PAPER_DIR/consistency-audit.deterministic.findings.json"
python3 "$ROOT/tools/check_presentation.py" --ledger "$PAPER_DIR/claims.json" \
    --out "$PAPER_DIR/presentation-signals.deterministic.findings.json"
```

**Validation gate — files exist + parse, and every above-info finding is anchored.** This
independently re-checks invariant #3 (it mirrors the adjudicator; it is report-only here —
the adjudicator is the *binding* gate and fail-closes anything unanchored to `info`):

```bash
PAPER_DIR="<from Step 0>"
python3 - "$PAPER_DIR" <<'PY'
import json, glob, os, sys
D = sys.argv[1]
claims = {c["claim_id"]: " ".join((c.get("text_span") or "").split())
          for c in json.load(open(f"{D}/claims.json", encoding="utf-8"))["claims"] if c.get("claim_id")}
nw = lambda s: " ".join((s or "").split()); ABOVE = {"critical", "major", "minor"}
mandatory = ["consistency-audit.deterministic", "consistency-audit", "experiment-forensics",
             "presentation-signals.deterministic", "presentation-signals",
             "ai-style-impressions.deterministic", "ai-style-impressions"]
missing = []
for f in mandatory:
    p = f"{D}/{f}.findings.json"; ok = os.path.isfile(p)
    if ok:
        try: ok = isinstance(json.load(open(p, encoding="utf-8")), list)
        except Exception: ok = False
    if not ok: missing.append(f)
total_bad = 0
for p in sorted(glob.glob(f"{D}/*.findings.json")):
    if p.endswith(".proposed.findings.json"): continue   # defensive: never adjudicate a raw/intermediate file
    try: arr = json.load(open(p, encoding="utf-8"))
    except Exception: print(f"BAD JSON  {os.path.basename(p)}"); continue
    bad = sum(1 for f in arr if f.get("severity") in ABOVE and not any(
        ev.get("claim_id") in claims and nw(ev.get("span")) and nw(ev["span"]) in claims[ev["claim_id"]]
        for ev in (f.get("evidence") or [])))
    total_bad += bad
    print(f"{os.path.basename(p):<46} findings={len(arr):<3} above-info-unanchored={bad}")
if missing: print("MISSING/BAD mandatory:", ", ".join(missing), "-> re-run those auditors")
print(f"TOTAL unanchored above-info (adjudicator will demote to info): {total_bad}")
PY
```

**Failure handling.** A *missing* mandatory file → re-invoke that skill. A codex *stall*
inside a sub-skill → it re-invokes the identical prompt in a fresh thread (never
`codex-reply`); if it still fails it writes `[]` and the run continues. Unanchored
above-info findings are not a stop condition (the adjudicator demotes them); a *large*
count signals a thin ledger/source — note it in the report's limitations. Any
`pattern_id` present MUST be in `references/hack-pattern-taxonomy.md` (v0.4); never patch
findings by hand.

## Step 3 — Advisory memos (last; memo-only, no verdict weight)

After the auditors (so the ledger + the merged findings exist), run the two **advisory**
skills. Both are **memo-only**: the adjudicator lists each in `MEMO_ONLY_SKILLS` and its
MEMO gate pins any finding either emits to `info`, so neither can move the verdict — they
hand a human area chair context to weigh, nothing more.

**3a — Adversarial case builder.** Synthesize the single strongest *evidence-bound*
objection:

```
/adversarial-case-builder "<PAPER_DIR>"          # → adversarial-case-builder.memo.md
```

Every point in the memo must cite an existing ledger `claim_id` or finding `finding_id` —
no new uncited accusations. It is passed to the adjudicator via `--memo` and shown as
informational with **no verdict weight** (the `MEMO_ONLY_SKILLS` cap pins any
`adversarial-case-builder` finding to `info`, even if it also emits a `findings.json`). If
the anchored evidence does not support a strong rejection, the honest memo says the paper
survives.

**3b — Novelty & duplication advisory** (run if `has_contrib` from the Step-2 decision
block — ≥1 contribution claim). This is the **only** skill that reaches *outside* the
paper: it retrieves candidate prior work (DBLP fuzzy-title + boolean · WebSearch ·
WebFetch) from the paper's own title + contribution spans and lays the overlap
**side-by-side** for the two *advisory* taxonomy signals — `ADV-TRIVIAL-COMBINATION`
(standard A+B+C / 缝合) and `ADV-DUPLICATE-PUBLICATION` (repackaged submission):

```
/novelty-duplication-advisory "<PAPER_DIR>"      # → novelty-duplication-advisory.memo.md (+ info-only findings mirror)
```

It **never rules** "trivial" or "duplicate" (a reviewer judgment, not decidable at *any*
observability level), and **absence of a retrieved match is NOT evidence of originality**.
Unlike 3a it does **not** flow through `--memo` (the adjudicator has a single memo slot):
its human-facing `novelty-duplication-advisory.memo.md` is surfaced in Step 5, and it also
writes an **info-only `novelty-duplication-advisory.findings.json` mirror** that the Step-4
glob picks up and the `MEMO_ONLY_SKILLS` gate caps at `info` (recorded, never
verdict-bearing). With no contribution claim, or when retrieval surfaces nothing, it writes
an honest-null memo + `[]` — "no candidate overlap found" still says nothing about novelty.
It is the literature-facing complement to `citation-forensics`: that audits works the paper
**does** cite; this surfaces prior work it may **not** have cited at all.

Both memos are **non-blocking** — if either is skipped, Step 4 still runs (an empty
`--memo` for the adversarial case; an absent novelty mirror simply contributes nothing).

## Step 4 — Adjudicate (deterministic — this is the verdict)

The single decider. Pass every auditor's `*.findings.json` (the glob now also enumerates
the verdict-bearing `proof-derivation-forensics.findings.json` and the info-only
`novelty-duplication-advisory.findings.json` mirror — the latter capped at `info` by the
MEMO gate), the **required** ledger, the run level, the taxonomy version, and the
adversarial memo. `--ledger` is what re-verifies each
finding quotes a **verbatim ledger span**; argparse makes it mandatory — and without a
ledger every above-info finding **fails closed to `info`** (a missing ledger silently
neuters the audit), which is why it is non-optional here.

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); PAPER_DIR="<from Step 0>"
L=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["observability_level"])' "$PAPER_DIR/claims.json")
PAPER_ID=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["paper_id"])' "$PAPER_DIR/claims.json")

# Build the findings list portably (no `mapfile` — macOS ships bash 3.2 without it).
# Defensive: never adjudicate a raw/intermediate *.proposed.findings.json, should a sub-skill ever stage one.
FINDINGS=()
for p in "$PAPER_DIR"/*.findings.json; do
  [ -f "$p" ] || continue
  case "$p" in *.proposed.findings.json) continue;; esac
  FINDINGS+=("$p")
done
[ ${#FINDINGS[@]} -gt 0 ] || { echo "FATAL: no findings files in $PAPER_DIR — did Step 2 run?"; exit 1; }
printf '  findings: %s\n' "${FINDINGS[@]##*/}"

python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "${FINDINGS[@]}" \
    --ledger "$PAPER_DIR/claims.json" \
    --paper-id "$PAPER_ID" --observability-level "$L" --taxonomy-version 0.5 \
    --memo "$(cat "$PAPER_DIR/adversarial-case-builder.memo.md" 2>/dev/null)" \
    --limitation "Run observability level L$L — see references/observability-levels.md for what this tier can and cannot decide." \
    --out "$PAPER_DIR/report.json" --md "$PAPER_DIR/REPORT.md"
# prints e.g.: verdict=SOFT_FLAGS crit=0 maj=0 min=1 -> .../report.json, .../REPORT.md
```

- **`--observability-level "$L"`** is the run level: it auto-demotes any finding whose
  `observability_level_required` exceeds `L` (e.g. an L2 code-fraud pattern on an L0 run
  → `info`, counted under `downgraded_for_observability`).
- The adjudicator **auto-writes level-derived limitations** at L0/L1 (and an anchoring
  note if `--ledger` anchoring ever fails); Step 4 **also always passes an explicit
  `--limitation`** (above), so the report's `limitations` is never empty on this path —
  honesty is part of the contract. Each extra `--limitation` (repeatable) is added
  alongside the auto-written ones. For a byte-reproducible eval run add
  `--generated-at "<fixed ISO8601>"`; omit it normally (a harmless `utcnow`
  DeprecationWarning may print to stderr; exit 0).

It applies, in order (each gate fail-closed and logged per finding): **ANCHOR**
(above-info without a verbatim ledger span → `info`; counted under `unanchored_demoted`) →
**OBSERVABILITY** (`observability_level_required` missing/invalid or > run `L` → `info`;
counted under `downgraded_for_observability`) → **FP-RISK** (`high` caps at `minor`,
`medium` caps at `major`) → **MEMO** (`adversarial-case-builder` + `novelty-duplication-advisory` → `info`) → **SURFACE**
(`presentation-signals` skill OR a `SURFACE_PATTERNS` `pattern_id` → `minor`). Then, over
the **surviving** severities:

```
any surviving critical          → HARD_FLAGS
else any surviving major/minor  → SOFT_FLAGS
else                            → CLEAN_GIVEN_EVIDENCE   (= "nothing checkable at L is broken", NOT "honest")
```

**Validation gate.** Confirm the report is well-formed:

```bash
PAPER_DIR="<from Step 0>"
python3 - "$PAPER_DIR/report.json" <<'PY'
import json, sys
r = json.load(open(sys.argv[1], encoding="utf-8"))
assert r["overall_verdict"] in {"CLEAN_GIVEN_EVIDENCE", "SOFT_FLAGS", "HARD_FLAGS"}, r["overall_verdict"]
assert r["adjudicator"] == "deterministic-rules-v0" and r["human_review_required"] is True
assert r["anchoring_verified"] is True, "ledger anchoring did not run — --ledger missing?"
assert r["limitations"], "limitations must always be populated (the honesty contract)"
c = r["counts"]
print(f"verdict={r['overall_verdict']}  L={r['observability_level']}  taxonomy=v{r['taxonomy_version']}")
print(f"counts: crit={c['critical']} maj={c['major']} min={c['minor']} info={c['info']} "
      f"obs-demoted={c['downgraded_for_observability']} unanchored-demoted={c.get('unanchored_demoted',0)}")
PY
```

**The verdict is reproducible: same findings + same `L` → same verdict, with no model in
the final decision.**

## Step 5 — Present

Show the human `REPORT.md`. **Lead with the verdict + the observability level**, then the
evidence-first table, then detail, then the advisory memos (adversarial + novelty/
duplication), then — always — the limitations (what could *not* be checked at this level):

```bash
PAPER_DIR="<from Step 0>"; sed -n '1,60p' "$PAPER_DIR/REPORT.md"
```

Present in this shape (fill from `report.json` / `REPORT.md`):

```
🔬 Integrity Forensics — <PAPER_ID>
   Verdict: <CLEAN_GIVEN_EVIDENCE | SOFT_FLAGS | HARD_FLAGS>   Observability: L<L>   Taxonomy: v0.4
   Findings above info: critical <n> · major <n> · minor <n>   (demoted: obs <n>, unanchored <n>)
   Top flags: <ID> <severity> <pattern_id> — <one-line, where>
   Could NOT check at L<L>: <one line from limitations — e.g. "code/result-level patterns need L2">
   Advisory (no verdict weight): adversarial objection + novelty/duplication overlap — <PAPER_DIR>/novelty-duplication-advisory.memo.md
   Report: <PAPER_DIR>/REPORT.md   ·   Machine-readable: <PAPER_DIR>/report.json
   This is decision support for a human reviewer/AC — it flags discrepancies to investigate, not misconduct.
```

State plainly, in the user's words, what the level did and did not permit: e.g. *"L0 run
— I checked internal self-consistency, arithmetic, citation existence/context, and stated
scope/baselines; I could NOT verify code/result-level integrity (fake GT,
self-normalization, phantom results) — that needs the repo + result files (L2)."*
`CLEAN_GIVEN_EVIDENCE` means **"nothing checkable at L<L> is broken,"** NOT "the paper is
honest." `human_review_required` is always `true`.

`— human checkpoint: true` → pause here for the user before treating the run as closed.

## Deterministic-only fallback (no model in the loop)

When no cross-model reviewer is available (offline / no codex), you can still produce a
real, reproducible report from the deterministic core alone — the load-bearing,
eval-gated part of the repo (**100% recall on the three deterministic patterns
`HP-DELTA-ERROR` / `HP-NUM-INFLATE` / `HP-DUP-TABLE`, zero clean false-positives**;
`README.md` Status). All real tools, exact flags:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); PAPER_DIR="<from Step 0>"
TXT=(); [ -f "$PAPER_DIR/paper.txt" ] && TXT=(--pdf-text "$PAPER_DIR/paper.txt")
python3 "$ROOT/tools/build_manifest.py"      --paper-id mypaper --dir "$PAPER_DIR" "${TXT[@]}" --out "$PAPER_DIR/artifact_manifest.json"
L=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["observability_level"])' "$PAPER_DIR/artifact_manifest.json")
if ls "$PAPER_DIR"/*.tex >/dev/null 2>&1; then            # L1/L2 source path
  python3 "$ROOT/tools/build_claim_ledger.py"  --paper-id mypaper --latex "$PAPER_DIR"/*.tex \
      --observability-level "$L" --out "$PAPER_DIR/claims.json"
else                                                       # L0 text path (no *.tex)
  python3 "$ROOT/tools/build_claim_ledger.py"  --paper-id mypaper --pdf-text "$PAPER_DIR/paper.txt" \
      --observability-level "$L" --out "$PAPER_DIR/claims.json"
fi
python3 "$ROOT/tools/check_numeric_consistency.py" --ledger "$PAPER_DIR/claims.json" \
    --out "$PAPER_DIR/consistency-audit.deterministic.findings.json"
python3 "$ROOT/tools/check_presentation.py"        --ledger "$PAPER_DIR/claims.json" \
    --out "$PAPER_DIR/presentation-signals.deterministic.findings.json"
python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "$PAPER_DIR"/*.deterministic.findings.json \
    --ledger "$PAPER_DIR/claims.json" --paper-id mypaper --observability-level "$L" \
    --taxonomy-version 0.5 \
    --limitation "Deterministic-only run (no cross-model reviewer): semantic + code-level dimensions were NOT run." \
    --out "$PAPER_DIR/report.json" --md "$PAPER_DIR/REPORT.md"
```

The verdict reflects only the deterministic patterns; the report's limitations must say
the semantic / code-level dimensions were not run. Run `python3 "$ROOT/eval/run_eval.py"`
(and `python3 "$ROOT/tests/test_adjudicator.py"`) any time to prove this core still
catches the bundled injected defects and stays clean on the clean fixture (the CI gate).

## Output contract

A completed run leaves, in `PAPER_DIR` (we never edit the paper itself):

- `artifact_manifest.json` (`schemas/artifact_manifest.schema.json`) — observable inputs
  (hashed) + the derived observability level.
- `claims.json` (`schemas/claims.schema.json`) — the span-anchored, hashed evidence
  ledger every auditor read.
- `<skill>.findings.json` for each auditor that ran, plus `*.deterministic.findings.json`
  for the consistency and presentation deterministic passes. Each conforms to
  `schemas/finding.schema.json`; `[]` is a valid, honest result, and every optional
  auditor's file is present even when empty.
- `adversarial-case-builder.memo.md` — the evidence-bound objection memo (informational).
- `novelty-duplication-advisory.memo.md` — the prior-work overlap advisory (informational,
  memo-only), present when the novelty advisory ran; alongside it the retrieval records
  `novelty-duplication-advisory.profile.json` / `.candidates.json` and the info-only
  `novelty-duplication-advisory.findings.json` mirror (capped at `info` by the MEMO gate).
- `report.json` (`schemas/report.schema.json`) + `REPORT.md` — the **only** files
  carrying `overall_verdict`, produced solely by `tools/adjudicate_findings.py`
  (`adjudicator: deterministic-rules-v0`, `human_review_required: true`).
- `.aris/traces/<skill>/<date>_run<NN>/` — each sub-skill's raw reviewer calls
  (forensic), plus this orchestrator's own run trace (see Review tracing).

The orchestrator itself **never** computes a verdict, **never** edits the audited paper,
and **never** hand-authors a finding — it ingests, sequences the skills, runs the
deterministic adjudicator, and presents.

## Key rules

- **Ledger first, always; auditors propose, only `adjudicate_findings.py` decides.** No
  auditor runs without `claims.json`, and no model is in the final decision; the verdict
  is reproducible (`references/reviewer-independence.md` Layer 2; `DESIGN.md` §3).
- **No span → no severity.** Every above-info finding must cite a ledger `claim_id` and
  quote a verbatim, whitespace-normalized substring of that claim (`span in claim`, never
  `claim in span`). The orchestrator's anchor sweep checks this; the adjudicator binds it
  (fail-closed to `info`). `--ledger` is therefore **mandatory** in Step 4.
- **Observability honesty.** Carry the ledger's `L` everywhere; it caps severity. L0/L1
  **cannot** assert code/result-level fraud — those auto-demote to `info` on a sub-L2
  run. Never present an L0 run as if it could see code; the report's limitations say what
  was unverifiable (`references/observability-levels.md`; `DESIGN.md` §4).
- **Cross-model, fresh thread per dimension.** Reviewer = gpt-5.5 xhigh (a different
  family from Claude); each auditor uses a new `mcp__codex__codex` thread and never
  `codex-reply` (deliberately absent from `allowed-tools` — the bias guard). The executor
  passes only paths + the ledger + the checklist, never a summary or a hunch.
- **Detect-only.** No step edits the audited paper or repo (no `Edit` granted; reviewer
  sandbox is `read-only`). Output describes a *discrepancy to check/ask*, never "reject"
  or "the authors faked X".
- **Surface signals stay weak.** `presentation-signals` is auxiliary, capped at `minor`
  (by skill and by `pattern_id`), default `false_positive_risk: high`. This repo is
  **not** an AI-text classifier — for authorship use a dedicated detector.
- **Proof decides from the source; novelty never decides.** `proof-derivation-forensics`
  is verdict-bearing (`dimension: proof`) and decides from the LaTeX proof source (L1) — a
  span-anchored **critical** family-G flaw reaches `HARD_FLAGS` with no repo/results, but
  needs the L1 source (PDF-extracted math is unreliable; an L0 PDF-only run → `info`); it
  emits only the five family-G patterns and self-guards to `[]` when no proof is present.
  `novelty-duplication-advisory` is **memo-only** (`MEMO_ONLY_SKILLS`, capped at `info`):
  it retrieves and *lays out* prior-work overlap but **never** rules trivial/duplicate, and
  absence of a retrieved match is **not** evidence of originality (the only auditor that
  consults an external corpus, which is exactly why it carries no verdict weight).
- **`pattern_id` ∈ taxonomy v0.4 only**; the taxonomy is a post-hoc mapping layer, not
  the detector (`references/hack-pattern-taxonomy.md`).
- **The adjudicator ingests validated findings only.** The `*.findings.json` glob feeds
  the adjudicator; defensively exclude any raw/intermediate `*.proposed.findings.json` a
  sub-skill might stage, so an unvalidated array can never reach the verdict.
- **Silent skip is forbidden.** A non-applicable / clean auditor still writes `[]`.
- **Large file handling.** If `Write` fails on size, retry with a Bash heredoc
  (`cat << 'EOF' > file`) — do not ask permission, just do it. This is only ever for
  **our own output files** in `PAPER_DIR`; detect-only still holds (never write/edit the
  audited sources).
- **Reproducible.** Same artifacts → same ledger → same findings → same verdict; re-run
  only when the inputs change (the cadence fence at the top).

## When NOT to use (and routing to standalone skills)

- **You only want one dimension** → call the auditor directly (`/consistency-audit`,
  `/citation-forensics`, `/baseline-comparison-audit`, `/experiment-forensics`,
  `/presentation-signals`, `/proof-derivation-forensics`); each can adjudicate itself with
  `--ledger` when run alone.
- **You only want the prior-work overlap** (trivial-combination / duplicate-publication
  signals) → `/novelty-duplication-advisory` (memo-only; it surfaces overlap but never rules
  novelty, and the absence of a match is not evidence of originality).
- **You only need the ledger** (extract claims, no verdict) → `/evidence-ledger`.
- **You want an AI-text / "looks machine-written" verdict** → out of scope by design;
  this tool audits *integrity under limited evidence*, not authorship (`DESIGN.md` §1).
- **You want the paper auto-fixed** → out of scope; this is a third-party forensics tool,
  not a co-author. (ARIS `citation-audit` etc. are the co-author-mode tools.)
- **You want reproduction (re-run the code, L3)** → out of scope in v0; we never claim
  reproduction. L2 verifies paper-number ↔ result-file match, not a re-run.
- **On a timer** → never `/loop` / `/schedule` / `CronCreate` the verdict; re-run only
  when the paper / repo / ledger changes (see the cadence fence at the top).

## Typical run profile

Forensics is fast — the budget is reviewer calls, not GPU. Use this to set expectations
and to choose `— effort: max` (more fresh threads per dimension) vs the
deterministic-only fallback (zero reviewer calls).

| Stage | Reviewer calls | Reads | Writes | Notes |
|-------|----------------|-------|--------|-------|
| 0 ingest | 0 | `$ARGUMENTS` (dir/pdf/arxiv) | `paper.txt` / extracted `*.tex` | network only for arXiv |
| 1 ledger | 0–1 (enrich) | sources | `artifact_manifest.json`, `claims.json` | deterministic backbone + 1 optional additive pass |
| 2 auditors | 1+ per applicable dimension (serial; `— effort: max` → more) | `claims.json` (+ sources, +L2 code) | `<skill>.findings.json` (+ deterministic) | the bulk of the wall-clock; never parallel; `/proof-derivation-forensics` runs iff theorems/proofs are present |
| 3 memos | 1 (adversarial) + 2 per-axis fresh threads (novelty, optional) + DBLP/web retrieval | ledger + findings (+ external corpus) | `adversarial-case-builder.memo.md`, `novelty-duplication-advisory.memo.md` | non-blocking; no verdict weight; novelty is the only step that hits the network |
| 4 adjudicate | 0 | findings + ledger | `report.json`, `REPORT.md` | deterministic; the only verdict source |
| 5 present | 0 | `REPORT.md` | — | verdict + level first |

A heartbeat may **wait** on the only external steps (Stage 0 download, Stage 2 citation
web lookups, Stage 3 novelty prior-work retrieval) — it may **never** re-fire Stage 4 or
"decide the paper is fine."

## Review tracing

Each auditor saves its own raw reviewer calls under `.aris/traces/<skill>/<date>_run<NN>/`
(forensic policy — never silently dropped: `run.meta.json` + per-call `request.json` /
`response.md` / `meta.json`, where `request.json` shows the executor sent only paths + the
ledger + the checklist — the reviewer-independence audit trail). The orchestrator
additionally writes a top-level run trace so the whole sweep is reproducible:

```bash
PAPER_DIR="<from Step 0>"; ARG="<original input arg, from Step 0>"; DATE=$(date +%Y-%m-%d); N=1
while [ -d "$PAPER_DIR/.aris/traces/anti-autoresearch/${DATE}_run$(printf %02d $N)" ]; do N=$((N+1)); done
RUNDIR="$PAPER_DIR/.aris/traces/anti-autoresearch/${DATE}_run$(printf %02d $N)"; mkdir -p "$RUNDIR"
python3 - "$PAPER_DIR" "$RUNDIR" "$ARG" <<'PY'
import json, glob, os, sys, hashlib, datetime
D, RUN, ARG = sys.argv[1], sys.argv[2], sys.argv[3]
def sha(p):
    try: return hashlib.sha256(open(p, "rb").read()).hexdigest()
    except Exception: return None
rep = json.load(open(f"{D}/report.json", encoding="utf-8")) if os.path.exists(f"{D}/report.json") else {}
meta = {
    "skill": "anti-autoresearch", "input_arg": ARG, "paper_dir": D,
    "paper_id": rep.get("paper_id"), "observability_level": rep.get("observability_level"),
    "ledger_sha256": sha(f"{D}/claims.json"),
    "findings_files": [os.path.basename(p) for p in sorted(glob.glob(f"{D}/*.findings.json"))
                       if not p.endswith(".proposed.findings.json")],
    "overall_verdict": rep.get("overall_verdict"), "counts": rep.get("counts"),
    "adjudicator": rep.get("adjudicator"), "taxonomy_version": rep.get("taxonomy_version"),
    "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
}
json.dump(meta, open(f"{RUN}/run.meta.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote", f"{RUN}/run.meta.json", "->", meta["overall_verdict"])
PY
```

Traces are the reproducibility + independence audit trail: they prove the executor sent
the reviewer only structured inputs and that the verdict came from the deterministic
adjudicator, not a model.
