---
name: novelty-duplication-advisory
description: "MEMO-ONLY prior-work overlap advisory: surfaces the two ADVISORY taxonomy signals neither a tool nor a model can decide from the paper alone — ADV-TRIVIAL-COMBINATION (standard A+B+C / 缝合 stapling) and ADV-DUPLICATE-PUBLICATION (repackaged / duplicate submission). The executor RETRIEVES candidate prior work (DBLP fuzzy-title + boolean · WebSearch · WebFetch) from the paper's own title + contribution spans in the evidence ledger; TWO fresh cross-model codex reviewers (one per axis) LAY OUT the overlap side-by-side against each anchored contribution claim. It NEVER rules 'trivial' or 'duplicate' (that is a human judgment) and absence of a match is NOT evidence of originality. Emits novelty-duplication-advisory.memo.md + an info-only findings mirror; carries NO verdict weight — tools/adjudicate_findings.py lists it in MEMO_ONLY_SKILLS and caps it at info. Detect-only. Adapted from ARIS novelty-check, reframed from 'is MY idea novel' to 'here is the overlap a reviewer should weigh'. Triggers: \"novelty advisory\", \"duplication check\", \"prior-work overlap\", \"is this stapling\", \"缝合\", \"查重\", \"重复发表\", \"duplicate submission\"."
argument-hint: [paper-dir | claims.json]
allowed-tools: Bash(*), Read, Write, WebSearch, WebFetch, mcp__codex__codex, mcp__mcp-dblp__fuzzy_title_search, mcp__mcp-dblp__search
---

# Novelty & Duplication Advisory — the overlap a reviewer should weigh

Lay out, for **$ARGUMENTS** (a paper-dir or a `claims.json` from `/evidence-ledger`), the
candidate prior-work overlap a human reviewer should weigh for two reviewer-judgment signals
— **trivial combination** ("standard A+B+C") and **duplicate publication** ("repackaged prior
work"). Retrieve candidates, map them side-by-side against the paper's ledger-anchored
contribution, and emit `novelty-duplication-advisory.memo.md`. Run AFTER `/evidence-ledger`
(so `claims.json` exists). This skill **decides nothing** — it never rules "trivial" or
"duplicate", and the deterministic adjudicator caps it at `info`.

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It retrieves
> external prior work once and synthesizes it into one advisory memo. Even though it is
> **memo-only** (the adjudicator caps it at `info`, so it adds no verdict weight), the
> no-new-signal cadence rule still applies: its output changes only when the **ledger / the
> paper / the literature** change, never with the wall clock. It is tempting to re-fire on a
> timer "to catch newly-posted prior work," but a wall-clock loop burns real DBLP + web +
> cross-model budget on every tick for a paper that has not changed. Schedule the *work that
> precedes it* — ledger built → run this **once**. (Mirrors ARIS's external-cadence doctrine:
> `/loop`·`/schedule` are fire-control, not a judge.)

> Adapted from ARIS `novelty-check`, with **one deliberate reframing and one deliberate
> downgrade.** The reframing: ARIS `novelty-check` asks *"is MY idea novel — should I PROCEED
> / ABANDON?"* and hands the author a `Score: X/10` + a recommendation; this skill asks *"here
> is the overlap a third-party reviewer should weigh"* and hands the human candidates, not a
> verdict. The downgrade: it is **memo-only.** Novelty is the textbook example of a judgment
> that is **not decidable from the paper alone, and not decidable at any observability level**
> — it depends on a corpus you can never prove you searched exhaustively. So this skill
> **retrieves and lays out** overlap; it refuses to grade it. `tools/adjudicate_findings.py`
> lists `novelty-duplication-advisory` in `MEMO_ONLY_SKILLS` and caps anything it emits at
> `info`. The memo *informs*; the human *judges*; the deterministic adjudicator owns the
> report verdict — and this skill never moves it.

## Why this exists

Two complaints recur in real reviews of autoresearch (and rushed human) output, and neither
is an *internal*-consistency failure the other auditors catch — they are *relational* to the
wider literature:

- **"标准的 A + B + C，全是已知模块" / "缝合" (stapling)** — the paper bolts together three
  well-known techniques and presents the bundle as the contribution. Whether that bundle is a
  genuine advance or a trivial staple is a **reviewer judgment** — a surprising combination is
  publishable, an obvious one is not, and no tool can draw that line.
- **"这不就是 X 换了个壳" (repackaged / duplicate submission)** — the submission looks like a
  prior paper (often the authors' own) with a new title. An *exact* title/abstract/DOI match
  is reportable; the **absence** of a match proves nothing, because your search corpus is
  never complete.

Both are listed in `references/hack-pattern-taxonomy.md` (v0.4) under **Advisory signals (NOT
in the 39 · zero verdict weight · reviewer-judgment only)** — `ADV-TRIVIAL-COMBINATION` and
`ADV-DUPLICATE-PUBLICATION`. The taxonomy is explicit: *"Novelty is a reviewer judgment; the
tool can lay out the prior-work overlap, it cannot rule 'trivial'"* and *"the absence of a
match is **not** evidence of originality."*

So this skill does the one honest, high-leverage thing the other auditors do not: it **reaches
outside the paper** to *retrieve* candidate prior work, and **lays it out side-by-side**
against the paper's own contribution so a human can weigh novelty with the overlap in front of
them. It is the only auditor that consults an external corpus — which is exactly why it can
carry **no verdict weight**: the moment a tool grades novelty from an incomplete search, it
manufactures the "AI slop grading AI slop" failure this repo exists to refuse. It is the
literature-facing complement to `citation-forensics`: that skill audits the papers the
submission **does** cite; this one surfaces prior work it may **not** have cited at all.

## Core principle

**MEMO-ONLY · retrieve-don't-rule · ledger-anchored on the paper side · real-record-bound on
the prior-work side · cross-model, fresh thread per axis · reviewer ≠ adjudicator · never
rules novelty · absence ≠ originality.** Three honesty spines hold this skill up:

1. **Paper side is ledger-anchored.** The contribution being compared is pulled from
   `claims.json` (`claim_id` + verbatim span) — never re-invented from the raw PDF
   (`references/integrity-forensics-contract.md` rule 1). The paper's **title** may be read
   from the source *as a search seed only* — it is never used as an anchor.
2. **Prior-work side is real-record-bound.** Every candidate comes from a **real retrieval
   call** (DBLP / WebSearch / WebFetch) and carries a **verifiable identifier** (arXiv id /
   DOI / DBLP url). Nothing is recalled "from memory" — fabricating a prior paper here is the
   same sin as a hallucinated citation (mirrors ARIS `novelty-check`'s anti-hallucination rule
   and `citation-discipline`).
3. **No verdict — by design.** The cross-model reviewers **propose** an overlap map + the open
   questions; they are forbidden to conclude "trivial" or "duplicate." The executor
   **validates** anchors; `tools/adjudicate_findings.py` **owns the verdict** and caps this
   skill at `info` (`references/reviewer-independence.md` Layer 2). A retrieval that finds
   nothing is a valid output that says **nothing** about novelty — "no candidate overlap
   found" is not "the paper is original."

> **Deliberate exception to "the reviewer reads only the ledger."** The other auditors reason
> strictly inside the paper. This one must consult an external corpus, so the executor
> performs the retrieval and hands each reviewer a *structured candidates file* (real records,
> with identifiers) alongside the ledger. That file is retrieval output, **not** a Claude
> opinion or digest of the paper — so the spirit of reviewer-independence (no executor
> judgment leaks into the reviewer prompt) still holds.

> **The anchor is the contribution sentence, not the prior work.** Every surfaced item anchors
> to one of the submission's own **contribution claims** — a `scope` / `method` / `comparison`
> claim, OR (because the deterministic extractor types most abstract/intro contribution
> sentences as `number` / `citation` / `scope`, so the three contribution *types* alone are
> too thin to anchor to on a real ledger) any claim located in the `abstract` / `intro`
> section. The candidate prior work — its title, arXiv id / DOI / DBLP url, overlap kind —
> lives in the memo table and the finding's `description`, **never** as the anchor span: there
> is no ledger claim for an external paper (same shape as `citation-forensics`, where the DBLP
> facts go in `description` and the anchor is the citing sentence).

## How this differs from the other auditors (route correctly)

| Auditor | Question it answers | External lookup? | Verdict weight |
|---------|---------------------|:---:|:---:|
| `consistency-audit` | Does the paper contradict ITSELF / described method = evaluated method? | no | yes (via adjudicator) |
| `experiment-forensics` | Are reported numbers what the code computes? (fake GT, self-norm, phantom) | no | yes (L2) |
| `baseline-comparison-audit` | Right baselines present, tuned, "SOTA" earned? | profile only | yes |
| `citation-forensics` | Do the *cited* papers EXIST and support the claim they are used for? | yes (existence/context of *cited* works) | yes |
| `proof-derivation-forensics` | Does the written proof / derivation hold? | no | yes |
| `presentation-signals` | Surface "AI-flavor" hints (auxiliary) | no | capped at minor |
| `adversarial-case-builder` | Strongest *anchored* rejection memo + defense | no | none (memo-only) |
| **`novelty-duplication-advisory`** (this) | **What prior-work OVERLAP should a reviewer weigh for trivial-combination / duplicate?** | **YES — retrieves *uncited* prior work** | **none (memo-only, capped at info)** |

**Route, do not overreach.** `citation-forensics` checks the works the paper *already cites*;
this skill goes looking for prior work the paper *omits or overlaps*. A **wrong-context or
fabricated citation** belongs to `citation-forensics`. A **"SOTA / first / beats prior work"**
claim that needs a baseline comparison belongs to `baseline-comparison-audit` (this skill can
emit `needs_external_check` and hand it off). An **internal** scope-overclaim ("comprehensive"
on thin scope) belongs to `consistency-audit` (`HP-SCOPE-INFLATE`). This skill owns *only* the
two advisory overlap signals — and even those it only *surfaces*.

## How this differs from ARIS `novelty-check` (the parent)

| | ARIS `novelty-check` | `novelty-duplication-advisory` (forensics) |
|---|---|---|
| Frame | "is MY idea novel — PROCEED / ABANDON?" | "here is the overlap a REVIEWER should weigh" |
| Subject | the author's own prospective idea | a third party's submitted paper |
| Paper side | a free-text method description | **ledger claims** (`claim_id` + verbatim span) |
| Output | a `Score: X/10` + recommendation + "suggested positioning" | a side-by-side overlap memo — **no score, no recommendation** |
| Verdict | "Novelty: HIGH/MEDIUM/LOW" | **none** — never rules trivial/duplicate; capped at `info` |
| Empty retrieval | "looks novel, proceed" | "no candidate overlap found — this says **nothing** about novelty" |
| Prior-work anchoring | `verify_papers.py` (anti-hallucination) | every candidate a resolved record in `candidates.json`; unresolved → dropped |

The multi-source retrieval and the cross-model verification are kept *exactly* (they are the
load-bearing parts). What changes is the refusal to grade: a forensics tool that scored
novelty from an incomplete corpus would be precisely the over-claim this repo refuses.

## Constants & Reviewer Calling Convention

```
REVIEWER_MODEL       = gpt-5.5                # different family from the executor (Claude)
REVIEWER_REASONING   = xhigh                  # always; effort never lowers reviewer quality
REVIEWER_SANDBOX     = read-only              # detect-only; never mutate the paper
REVIEWER_CWD         = <paper-dir>            # so it reads claims.json + candidates.json from cwd
THREAD_POLICY        = TWO fresh mcp__codex__codex calls — ONE per axis (duplicate / combination);
                       NEVER mcp__codex__codex-reply across them (the per-dimension bias guard)
CONCURRENCY          = serial                 # Codex MCP hangs on concurrent calls — Thread 2 waits for Thread 1
AXES                 = duplicate (ADV-DUPLICATE-PUBLICATION) | combination (ADV-TRIVIAL-COMBINATION)
OBS_REQUIRED         = 0 for both             # decidable-as-advisory from text + the public corpus (no repo/results)
RETRIEVAL_SOURCES    = DBLP (fuzzy_title_search + boolean search) · WebSearch · WebFetch (abstracts)
ANTI_HALLUCINATION   = every candidate comes from a REAL retrieval call + carries a verifiable id +
                       is a record in candidates.json; the reviewer cites candidate_id ONLY (never "from memory")
ANCHOR_UNIVERSE      = contribution claims = type∈{scope,method,comparison} OR section∈{abstract,intro,introduction};
                       prior work goes in the memo/description, NOT the anchor span
DISPOSITION          = candidate_overlap_surfaced | no_candidate_overlap_found | retrieval_incomplete
                       (INFORMATIONAL, NOT a verdict; "no overlap found" ≠ "the paper is original")
ADVISORY_PATTERNS    = ADV-TRIVIAL-COMBINATION · ADV-DUPLICATE-PUBLICATION   (zero verdict weight)
TAXONOMY_VERSION     = 0.5                     # references/hack-pattern-taxonomy.md
MEMO_FILE            = novelty-duplication-advisory.memo.md            # canonical human-facing output
FINDINGS_FILE        = novelty-duplication-advisory.findings.json      # info-only mirror (or []); globbed, capped at info
PROFILE_FILE         = novelty-duplication-advisory.profile.json       # executor-built retrieval profile (from the ledger)
CANDIDATES_FILE      = novelty-duplication-advisory.candidates.json    # retrieved prior work (REAL records only)
TRACE_POLICY         = forensic (never silently dropped)
TRACE_DIR            = .aris/traces/novelty-duplication-advisory/<YYYY-MM-DD>_run<NN>/
```

- **Executor (Claude)** owns the **retrieval** and **none of the judgment**: it pulls the
  contribution spans from the ledger, reads the title from the source as a search seed, runs
  the external searches, assembles a structured `candidates.json` of **real returned records**,
  passes **the ledger + the candidates file + the per-axis checklist** to each reviewer,
  validates every anchor the reviewers return, and renders the memo. It never summarizes the
  paper, pre-judges overlap, or leaks an opinion into a prompt
  (`references/reviewer-independence.md`).
- **Reviewer (codex / gpt-5.5, xhigh, read-only)** reads `claims.json` + `candidates.json`
  from its `cwd`, lays each candidate beside the contribution span it overlaps with, and lists
  the open questions. It is the overlap-mapper, **not** the judge — and it is **forbidden** to
  output a "trivial" / "duplicate" / "not novel" verdict. It cites only `candidate_id`s that
  exist in `candidates.json`.
- **Two fresh threads, serial, no `codex-reply`.** The duplicate axis and the combination axis
  are independent `mcp__codex__codex` calls; never carry one axis's conclusion into the other
  (the per-dimension bias guard). `codex-reply` is intentionally absent from `allowed-tools`.
- **Detect-only.** No `Edit` in `allowed-tools`; the reviewer sandbox is `read-only`. This
  skill never touches the audited paper.

---

## Step 0 — Preconditions: locate the ledger, read the run level, open the trace

This skill reasons over the **ledger** (paper side) + **retrieved candidates** (prior-work
side) — never the raw PDF for structure. Resolve the ledger and read the observability level
**L**, `paper_id`, and the count of contribution claims (each Bash block is self-contained —
shell state does not persist between calls, so re-derive paths every step):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
# $ARGUMENTS is a paper-dir OR a claims.json path:
LEDGER="$ARGUMENTS"; [ -d "$LEDGER" ] && LEDGER="$LEDGER/claims.json"
# Only the NO-ARGUMENT case defaults to the CWD ledger. An EXPLICIT argument that
# resolves to a missing claims.json must NOT silently fall back to $(pwd) — that could
# advise on the wrong paper; let the NO_LEDGER check below fire instead.
[ -z "$ARGUMENTS" ] && LEDGER="$(pwd)/claims.json"
python3 - "$LEDGER" <<'PY'
import json, sys, os
p = sys.argv[1]
if not os.path.isfile(p):
    sys.exit("NO_LEDGER: claims.json not found. Run /evidence-ledger FIRST "
             "(it writes artifact_manifest.json + claims.json).")
d = json.load(open(p, encoding="utf-8"))
CONTRIB_TYPES = {"scope", "method", "comparison"}
CONTRIB_SECT  = {"abstract", "intro", "introduction"}
def sect(c): return ((c.get("location") or {}).get("section") or "").lower()
contrib = [c for c in d.get("claims", [])
           if c.get("claim_id") and c.get("text_span")
           and (c.get("type") in CONTRIB_TYPES or sect(c) in CONTRIB_SECT)]
print("LEDGER         =", os.path.abspath(p))
print("PAPER_DIR      =", os.path.dirname(os.path.abspath(p)) or ".")
print("PAPER_ID       =", d.get("paper_id", "?"))
print("RUN_LEVEL_L    =", d.get("observability_level", 0))
print("CONTRIB_CLAIMS =", len(contrib), "(scope/method/comparison + abstract/intro — the anchor universe)")
PY
```

**Carry forward** the absolute `LEDGER` / `PAPER_DIR`, plus `L` and `PAPER_ID`, into every step
below.

**Failure / edge handling.**
- **`NO_LEDGER`** → stop and tell the user to run `/evidence-ledger` first. This skill never
  re-reads the raw PDF and invents its own structure (contract rule 1).
- **`CONTRIB_CLAIMS == 0`** → there is no contribution claim to anchor to. Recall scales with
  the ledger: an **L0 PDF-text** ledger extracts mostly number/scope spans, so contribution
  anchoring is thin; the richer abstract/intro spans enter via the **L1 LaTeX** path. Prefer
  re-running `/evidence-ledger` on the LaTeX source. If you cannot, skip the reviewer call,
  write the honest-null memo + an empty findings file directly (Step 4's honest-null snippet),
  and stop. Never invent a contribution claim.
- **Observability level does not gate *whether* this skill runs.** Retrieval needs only the
  title/contribution text, available at L0+. There is no graded verdict to gate — the judgment
  is not decidable at *any* level (it is a human call). The info-only mirror carries
  `observability_level_required: 0`, and the MEMO gate caps it at `info` regardless.

Create the trace directory now (forensic; written before any reviewer/retrieval call):

```bash
PAPER_DIR="<abs PAPER_DIR from Step 0>"
DATE=$(date +%F); N=1
while [ -d "$PAPER_DIR/.aris/traces/novelty-duplication-advisory/${DATE}_run$(printf %02d $N)" ]; do N=$((N+1)); done
TRACE="$PAPER_DIR/.aris/traces/novelty-duplication-advisory/${DATE}_run$(printf %02d $N)"
mkdir -p "$TRACE"; echo "TRACE = $TRACE"   # carry this absolute path into every later step
```

Write `"$TRACE/run.meta.json"` (via **Write**) =
`{"skill":"novelty-duplication-advisory","paper_id":"<PAPER_ID>","run_level_L":<L>,"taxonomy_version":"0.5","retrieval":{"duplicate":"pending","combination":"pending"},"generated_at":"<UTC ISO-8601>"}`.

## Step 1 — Build the retrieval profile from the ledger (executor, deterministic)

Pull the paper's **contribution** (the thing whose novelty a reviewer weighs) straight from the
ledger — `scope` / `method` / `comparison` claims plus anything in the `abstract` / `intro`
sections — and read the **title** from the source as a *search seed*. These spans are the
**paper-side anchors**; the executor never paraphrases them and never invents a contribution
the ledger does not contain.

```bash
LEDGER="<abs claims.json from Step 0>"
PAPER_DIR="$(dirname "$LEDGER")"
python3 - "$LEDGER" "$PAPER_DIR" <<'PY'
import json, sys, os, re
ledger_path, paper_dir = sys.argv[1], sys.argv[2]
d = json.load(open(ledger_path, encoding="utf-8"))
claims = d.get("claims", []); PID = d.get("paper_id", "?")
src = d.get("source_files", []) or []
def sect(c): return ((c.get("location") or {}).get("section") or "").lower()

CONTRIB_TYPES = {"scope", "method", "comparison"}
CONTRIB_SECT  = {"abstract", "intro", "introduction"}
PRI = {"abstract", "intro", "introduction"}
CUE = re.compile(r"\b(we\s+(propose|present|introduce|develop|design|show|demonstrate)|"
                 r"our\s+(approach|method|framework|model|contribution|key\s+idea)|"
                 r"in\s+this\s+(paper|work)|the\s+first\s+to|novel|contributions?\s+(are|of))\b", re.I)

ranked = []
for c in claims:
    if not c.get("claim_id") or not c.get("text_span"):
        continue
    s = sect(c)
    if not (c.get("type") in CONTRIB_TYPES or s in CONTRIB_SECT):
        continue
    span = c["text_span"]
    score = (2 if s in PRI else 0) + (2 if CUE.search(span) else 0) + (1 if c.get("type") in CONTRIB_TYPES else 0)
    ranked.append((score, {"claim_id": c["claim_id"], "type": c.get("type", "?"),
                           "section": s or "?", "text_span": span}))
ranked.sort(key=lambda x: -x[0])
contrib = [c for _, c in ranked][:10]

# title SEARCH SEED (never an anchor): prefer a title-section ledger claim, else \title{...}
# from a latex source (brace-matched), else the first substantive line of the pdf text.
def strip_tex(s):
    s = re.sub(r"\\thanks\{[^}]*\}", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    return " ".join(s.replace("{", " ").replace("}", " ").replace("\\", " ").split())
def title_from_latex(txt):
    m = re.search(r"\\title\s*(\[[^\]]*\])?\s*\{", txt)
    if not m: return None
    i, depth = m.end(), 1
    while i < len(txt) and depth:
        depth += (txt[i] == "{") - (txt[i] == "}"); i += 1
    t = strip_tex(txt[m.end():i-1]); return t if len(t) >= 6 else None

title, title_src = None, None
for c in claims:
    if sect(c) == "title" and c.get("text_span"):
        title, title_src = c["text_span"], "ledger:title-claim"; break
if not title:
    for s in src:
        if s.get("kind") == "latex" and os.path.isfile(s.get("path", "")):
            t = title_from_latex(open(s["path"], encoding="utf-8", errors="replace").read())
            if t: title, title_src = t[:240], "source:" + os.path.basename(s["path"]); break
if not title:
    for s in src:
        if s.get("kind") in ("text", "pdf") and os.path.isfile(s.get("path", "")):
            for ln in open(s["path"], encoding="utf-8", errors="replace"):
                ln = ln.strip()
                if len(ln) >= 12 and not ln.lower().startswith(("arxiv", "http", "doi")):
                    title, title_src = ln[:240], "source:" + os.path.basename(s["path"]); break
        if title: break
if not title and contrib:
    title, title_src = contrib[0]["text_span"][:240], "fallback:abstract-claim"

prof = {"paper_id": PID, "title_seed": title, "title_seed_source": title_src,
        "title_seed_is_anchor": False, "contribution_claims": contrib,
        "n_contribution_claims": len(contrib)}
out = os.path.join(paper_dir, "novelty-duplication-advisory.profile.json")
json.dump(prof, open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("PROFILE  =", out)
print("TITLE    =", (title or "(none — combination axis only)")[:120], "| source:", title_src)
print("CONTRIB  =", len(contrib))
for c in contrib[:10]:
    print(f"  [{c['claim_id']}] ({c['section']}/{c['type']}) {c['text_span'][:100]}")
if not contrib:
    print("NO_CONTRIB: ledger has no scope/method/comparison/abstract/intro claim — "
          "cannot build a retrieval query. Treat like CONTRIB_CLAIMS==0 (Step 4 honest-null).")
PY
```

**Sanity gate (before searching).** `title_seed` should look like a paper title and `CONTRIB`
should be > 0 for any normal paper. If a span looks truncated or mis-sectioned, **Read**
`claims.json` and spot-check that contribution `claim_id`'s `text_span` before you build a
query from it — a malformed seed wastes the external-search budget. Never fabricate a title or
a contribution to fill a gap.

**Building the queries (literal terms only).** From `profile.json`:
- **Title (for the duplicate axis).** Use `title_seed` verbatim. It is a **query seed, not an
  anchor** (`title_seed_is_anchor: false`); re-opening a source to quote it is permitted
  because it is a query input, not a finding. If it is `None`, run only the combination axis.
- **Constituent techniques (for the combination axis).** Decompose the contribution into ≤4
  named techniques using **literal terms copied from the contribution spans** (the method
  names, the architecture, the training objective). Do **not** introduce vocabulary the spans
  do not contain — that would manufacture overlap. If the contribution is one atomic method (no
  decomposition into ≥2 known components), the combination axis is **N/A**; say so and run only
  the duplicate axis.

**Failure handling.** `NO_CONTRIB` → write the honest-null memo + empty findings (Step 4
snippet) and stop. A thin ledger may yield a weak query — note that limitation in the memo; do
not pad the query with guessed terms.

## Step 2 — Retrieve candidate prior work (executor; real records only)

The executor runs the searches and assembles `candidates.json`. **This step records FACTS,
never a ruling** — whether a candidate is "the same paper", a benign extended version, or
unrelated is the reviewer's lay-out (Step 3) and ultimately the human's call. **Every record
must come from a real call below and carry a verifiable identifier.** Never add a paper you
"remember."

**2a — Duplicate axis (DBLP fuzzy title + exact-phrase web).** A near-identical title / DOI to
a *different* paper is the strongest reportable duplicate-candidate (taxonomy: *"an exact
title/abstract/DOI match is reportable"*). Call DBLP with the profile title:

```
mcp__mcp-dblp__fuzzy_title_search:
  title: "<title_seed from profile.json>"
  similarity_threshold: 0.7
  max_results: 10
  include_bibtex: false
```

Then a web pass for an exact-phrase / preprint match (DBLP indexes venues, not all preprints):

```
WebSearch:
  query: "\"<the exact paper title>\""          # quoted: catch a repackaged/duplicate posting
WebSearch:
  query: "<paper title, unquoted> arxiv"        # catch a near-duplicate preprint
```

For the top title-similar hits (and any exact web hit), `WebFetch` the abstract to record a
snippet for the side-by-side (the abstract is what lets the reviewer judge *degree* of
overlap):

```
WebFetch:
  url: "<arxiv abs / DOI / DBLP ee url of the candidate>"
  prompt: "Return ONLY: the paper title, the author list, the venue+year, and the verbatim
           first 2-3 sentences of the abstract. No commentary."
```

**2b — Combination axis (per-technique prior work).** For each constituent technique from Step
1, find the canonical prior work that *establishes* it — the work a reviewer would cite to call
it "well-known." Use DBLP boolean search (terms joined by `and`; **parentheses are
unsupported**) and/or WebSearch:

```
mcp__mcp-dblp__search:
  query: "<technique-A literal terms> and <technique-A qualifier>"
  max_results: 8
  year_from: 2015
mcp__mcp-dblp__search:
  query: "<technique-B literal terms> and <technique-B qualifier>"
  max_results: 8
WebSearch:
  query: "<technique-C literal terms> method  (survey OR original)"
```

Record the 1–2 most representative prior works per technique. The goal is to lay out *"the
contribution = A [prior work] + B [prior work] + C [prior work]"* for the human — **not** to
conclude the staple is trivial.

**2c — Assemble + validate `candidates.json`.** Use **Write** to create
`<PAPER_DIR>/novelty-duplication-advisory.candidates.json` from the **actual returned records**
— one object per candidate, exactly these keys:

```json
[
  {
    "candidate_id": "K01",
    "source": "dblp_fuzzy_title | dblp_boolean | websearch | webfetch",
    "title": "<verbatim returned title>",
    "authors": ["<as returned, if available>"],
    "venue": "<as returned>",
    "year": 2024,
    "identifier": {"arxiv": "", "doi": "", "dblp_url": "", "url": "<at least ONE non-empty>"},
    "title_similarity": 0.83,
    "abstract_snippet": "<verbatim from WebFetch, if fetched>",
    "retrieved_for": "duplicate | combination:A | combination:B | combination:C",
    "query": "<the exact query string used>"
  }
]
```

Then run the validation + self-record gate (de-dups by identifier, flags the paper's own record
so it is never mis-reported as a duplicate, and refuses memory-sourced entries):

```bash
PAPER_DIR="<abs PAPER_DIR from Step 0>"
CAND="$PAPER_DIR/novelty-duplication-advisory.candidates.json"
PROF="$PAPER_DIR/novelty-duplication-advisory.profile.json"
python3 - "$CAND" "$PROF" <<'PY'
import json, sys, re
cand_path, prof_path = sys.argv[1], sys.argv[2]
prof = json.load(open(prof_path, encoding="utf-8"))
def norm(s): return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
ptitle = norm(prof.get("title_seed"))
pauthors = {norm(a) for a in (prof.get("authors") or []) if a}   # audited paper's authors (for self-record check)
try:
    arr = json.load(open(cand_path, encoding="utf-8"))
except Exception as e:
    sys.exit(f"CANDIDATES_PARSE_FAILED: {e} — fix candidates.json (assemble from REAL calls only).")
SRC = {"dblp_fuzzy_title", "dblp_boolean", "websearch", "webfetch"}
seen, clean, dropped = set(), [], 0
for c in arr:
    if not isinstance(c, dict): dropped += 1; continue
    ident = c.get("identifier") or {}
    idval = next((v for v in (ident.get("arxiv"), ident.get("doi"),
                              ident.get("dblp_url"), ident.get("url")) if v), None)
    if c.get("source") not in SRC or not c.get("title") or not idval:
        dropped += 1; continue                      # no real source / no identifier -> not a real record
    key = idval.strip().lower()
    if key in seen: continue                        # de-dup by identifier
    seen.add(key)
    c["candidate_id"] = "K%02d" % (len(clean) + 1)  # re-id deterministically
    # self-record guard: a near-identical title MAY be the AUDITED paper's own record (its
    # preprint/venue copy). But title-similarity ALONE is not enough — a real duplicate-
    # publication by DIFFERENT authors can share a near-identical title. Treat as the paper's
    # OWN record (and exclude) ONLY when title is near-identical AND authorship overlaps; if the
    # title matches but authorship can't be confirmed, SURFACE it flagged for human author-check
    # rather than silently dropping a possible real duplicate.
    sim = c.get("title_similarity")
    title_match = bool(ptitle) and (norm(c.get("title")) == ptitle
                                    or (isinstance(sim, (int, float)) and sim >= 0.95))
    cand_auth = {norm(a) for a in (c.get("authors") or []) if a}
    authors_overlap = bool(pauthors and cand_auth and (pauthors & cand_auth))
    c["self_record_suspected"]   = bool(title_match and authors_overlap)        # confirmed own record -> exclude
    c["self_record_unconfirmed"] = bool(title_match and not authors_overlap)    # near title, authorship unverified -> surface + flag
    clean.append(c)
json.dump(clean, open(cand_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
dup = sum(1 for c in clean if c["retrieved_for"] == "duplicate" and not c["self_record_suspected"])
comb = sum(1 for c in clean if str(c["retrieved_for"]).startswith("combination"))
self_n = sum(1 for c in clean if c["self_record_suspected"])
print(f"candidates kept={len(clean)} (duplicate-axis usable={dup}, combination-axis={comb}, "
      f"self-record-suspected={self_n}) dropped(no-source/no-id/malformed)={dropped} -> {cand_path}")
if not clean:
    print("NO_CANDIDATES: retrieval surfaced nothing usable. This is a VALID result and says "
          "NOTHING about novelty (absence of a match is not evidence of originality). "
          "Step 4 -> disposition=no_candidate_overlap_found.")
PY
```

`candidates.json` lives in `PAPER_DIR` so each reviewer reads it from its `cwd`. When done,
update `"$TRACE/run.meta.json"` `retrieval` to record per-axis status (`"done"` /
`"unavailable"`). **Failure handling.** `CANDIDATES_PARSE_FAILED` → the assembled JSON is
malformed; rebuild it from the real returned records (never hand-fabricate). `NO_CANDIDATES` →
skip Step 3, go to Step 4's honest-null path. If a DBLP/web tool errors or web access is
unavailable for a whole axis, set that axis to `"unavailable"` in `run.meta.json` → the run
becomes `retrieval_incomplete` (Step 4), and the memo will say the search could not be
completed and therefore concludes **nothing** about originality. Do **not** backfill from
memory.

## Step 3 — Cross-model overlap mapping (TWO fresh per-axis threads; never rules)

Issue **two fresh** `mcp__codex__codex` calls — **one per axis, serial** (Codex MCP hangs on
concurrent calls; never `codex-reply`, never carry one axis into the other). Each reviewer reads
`claims.json` + `candidates.json` from its `cwd` and lays out overlap. Each is told —
repeatedly — that it must **not** conclude "trivial" or "duplicate."

### Thread 1 — duplicate axis (tag `001`)

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are an integrity-forensics reviewer preparing a NEUTRAL, ADVISORY prior-work
    overlap brief for a human area chair on ONE question: where does this submission's
    contribution OVERLAP with a candidate that may be a repackaged / duplicate publication?
    You lay the overlap out side-by-side. You are FORBIDDEN to render a judgment: never
    output "duplicate", "plagiarized", "not novel", "derivative", or "reject". Duplication
    is the human's call; you only surface the overlap so they can weigh it.

    INPUTS — read these directly from your working directory:
      - claims.json — the evidence ledger. The contribution lives in its scope / method /
        comparison claims AND in any abstract/intro claim {claim_id, type, text_span
        (VERBATIM), location}. These contribution claims are the ONLY anchor universe; do
        NOT invent a claim that is not in it.
      - novelty-duplication-advisory.candidates.json — REAL retrieved prior work, one record
        per candidate {candidate_id (e.g. K01), title, authors, venue, year, identifier,
        title_similarity?, abstract_snippet?, retrieved_for, self_record_suspected}. These
        are FACTS, not a verdict. Consider candidates with retrieved_for=="duplicate". You
        may cite ONLY candidate_ids present here — never recall a paper from memory, never
        invent ids/titles. A candidate not in this file is DELETED downstream as a hallucination.
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.

    WHAT TO DO — for each non-self candidate that genuinely overlaps the submission's
    title / contribution, emit ONE overlap item that:
      * anchors to the most specific contribution claim it overlaps with (a VERBATIM
        substring of that claim's text_span);
      * names the candidate by its EXACT candidate_id and states the overlap_kind
        (near_exact_title | abstract_overlap | same_core_contribution) using the file's
        title/abstract — never memory;
      * if self_record_suspected==true, the candidate is very likely THIS paper's own
        preprint/venue copy — EXCLUDE it from the duplicate axis (you may note it was excluded);
      * describes the RESIDUAL DELTA: what the submission still claims BEYOND the candidate
        (descriptive only — NOT a "the delta is too small" ruling).

    HARD RULES (an item that breaks any of these is worthless):
    1. ANCHOR. Every item carries >=1 anchor {claim_id, span} where claim_id is a
       contribution claim in claims.json and span is a VERBATIM, whitespace-normalized
       SUBSTRING of THAT claim's text_span (copy LaTeX escapes like \% exactly; do NOT
       unescape/paraphrase). The candidate goes in candidate_ids/the description, NEVER in
       span. No anchor -> drop the item.
    2. CANDIDATES FROM THE FILE ONLY. Every candidate_id must appear in candidates.json.
       Never fabricate a paper. A false "duplicate" is a serious error.
    3. NEVER RULE. Do NOT classify the paper duplicate/novel. reviewer_action is what a human
       should WEIGH or CHECK ("compare the method against K01 and judge whether the
       contribution is subsumed"), never "reject"/"duplicate".
    4. ABSENCE IS NOT ORIGINALITY. If no non-self candidate genuinely overlaps, emit an EMPTY
       array []. Do NOT conclude the paper is original — the memo states absence of a match
       is not evidence of originality.
    5. OBSERVABILITY = 0 for every item.
    6. pattern_id is exactly "ADV-DUPLICATE-PUBLICATION".

    OUTPUT: a single JSON array, and NOTHING ELSE (no prose, no code fence). Each element:
      {
        "id": "O1",
        "axis": "duplicate",
        "pattern_id": "ADV-DUPLICATE-PUBLICATION",
        "label": "short neutral label",
        "overlap_statement": "~30 words: what part of the contribution overlaps which candidate",
        "anchors": [{"claim_id": "C0xx", "span": "verbatim substring of that contribution claim"}],
        "candidate_ids": ["K01"],
        "overlap_kind": "near_exact_title | abstract_overlap | same_core_contribution",
        "residual_delta_note": "~40 words: what the submission still claims beyond the candidate (descriptive, NOT a ruling)",
        "reviewer_action": "what the human should WEIGH/CHECK — never 'duplicate'/'reject'"
      }
    An empty array [] is a valid, honest result.
```

### Thread 2 — combination axis (tag `002`, a SECOND fresh thread)

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are an integrity-forensics reviewer preparing a NEUTRAL, ADVISORY prior-work brief
    for a human area chair on ONE question: the submission combines known techniques — which
    components are individually ESTABLISHED in prior work, and does the COMBINATION itself
    already appear somewhere? You lay this out side-by-side. You are FORBIDDEN to render a
    judgment: never output "trivial", "incremental", "mere stapling", "缝合", "not novel",
    or "reject". Whether a combination is a real contribution is the human's call.

    INPUTS — read directly from your working directory:
      - claims.json — the contribution lives in scope/method/comparison claims AND in any
        abstract/intro claim {claim_id, type, text_span (VERBATIM), location}. ONLY anchor
        universe; do not invent claims.
      - novelty-duplication-advisory.candidates.json — REAL retrieved prior work. Consider
        candidates with retrieved_for starting "combination". Cite ONLY candidate_ids
        present here; never recall a paper from memory.
    RUN OBSERVABILITY LEVEL L = <L from Step 0>.

    WHAT TO DO:
      1. From the contribution claims, identify the component techniques the paper combines
         (A, B, C ...). If it does not decompose into >=2 known components, emit [] (the
         combination axis is N/A — say nothing, do not force a decomposition).
      2. For EACH component the candidates show is established in prior work, emit one item
         anchored to the contribution claim that introduces it, citing the component's
         established prior work by candidate_id.
      3. Optionally emit one item for THE COMBINATION if the candidates show the same
         combination already exists. If no such candidate was retrieved, do NOT infer
         "novel" — simply omit it.
      4. In residual_delta_note, describe what the paper claims is NEW about the combination
         (mechanism / setting / result) — descriptive only.

    HARD RULES (same discipline as the duplicate axis):
    1. ANCHOR every item to a VERBATIM substring of a contribution claim. Prior work goes in
       candidate_ids/description, NEVER in span. No anchor -> drop the item.
    2. CANDIDATES FROM THE FILE ONLY — never fabricate prior work.
    3. NEVER RULE — no "trivial"/"incremental"/"novel"; reviewer_action is what the human
       should WEIGH ("assess whether combining K05 and K06 for this task is a contribution
       beyond the components"), never a verdict.
    4. ABSENCE IS NOT ORIGINALITY — if no component overlap is in the file, emit []. Do not
       conclude the paper is novel.
    5. OBSERVABILITY = 0 for every item.
    6. pattern_id is exactly "ADV-TRIVIAL-COMBINATION".

    OUTPUT: a single JSON array, NOTHING ELSE. Each element:
      {
        "id": "O1",
        "axis": "combination",
        "pattern_id": "ADV-TRIVIAL-COMBINATION",
        "label": "component or combination label",
        "overlap_statement": "~30 words: which component/combination overlaps which prior work",
        "anchors": [{"claim_id": "C0xx", "span": "verbatim substring of the contribution claim"}],
        "candidate_ids": ["K05"],
        "overlap_kind": "component_established | combination_appears",
        "residual_delta_note": "~40 words: what the paper claims is new about the combination (descriptive, NOT a ruling)",
        "reviewer_action": "what the human should WEIGH — never 'trivial'/'reject'"
      }
    An empty array [] is a valid, honest result.
```

**Persist immediately, then run the next thread.** After EACH call returns, save the FULL raw
reply with **Write** to `"$TRACE/<NNN>-<axis>.response.md"` (`001-duplicate.response.md`,
`002-combination.response.md`), the exact prompt to `"$TRACE/<NNN>-<axis>.request.json"`, and
`"$TRACE/<NNN>-<axis>.meta.json"`
(`{"model":"gpt-5.5","reasoning":"xhigh","sandbox":"read-only","thread_id":"<id>"}`). The
`.response.md` files are the immutable input to Step 4. Keep each `thread_id`.

**Failure handling.**
- *MCP stall / hang* (common in long sessions): re-invoke the **identical** prompt as a
  **fresh** `mcp__codex__codex` call (gpt-5.5, xhigh) — never `codex-reply`.
- *Returns prose, not a JSON array*: Step 4 extracts the outermost `[...]`; if there is none,
  re-ask that one axis with "Output ONLY the JSON array, nothing else." Never hand-author
  overlap items on the reviewer's behalf.
- *Reviewer slips in a verdict* ("this is trivial / a duplicate"): that text is advisory memo
  content only; Step 4 strips leaked ruling words and the adjudicator caps the skill at `info`.
  Do not propagate it as a conclusion.
- *(Optional fan-out, `— effort: max`)*: run each combination component as a separate fresh
  `mcp__codex__codex` probe for breadth, then concatenate the arrays. Separate fresh threads
  are fine; carrying context via `codex-reply` is not. These are **NOT Claude subagents** and
  there is deliberately **no `Agent` grant** — the reviewer must be cross-model (non-Claude),
  and Codex MCP is **serial** (concurrent calls hang), so probes run **sequentially** (Tier-3
  in the fan-out ladder).

## Step 4 — Validate + anchor, render the memo + the info-only findings mirror

Everything the reviewers proposed is now **validated deterministically** by the executor: every
**anchor** must be a verbatim span of a real ledger contribution claim, and every
**candidate_id** must exist in `candidates.json` (the anti-hallucination gate — a candidate the
file does not contain is *deleted*, so the memo can never name a prior-work paper that was not
actually retrieved; a self-record cannot appear on the duplicate axis). Leaked ruling words are
neutralized. The adjudicator independently re-applies the span-anchor gate and the MEMO cap as
the authoritative verdict, so this memo can never out-rank it. This single command writes both
deliverables:

```bash
PAPER_DIR="<abs PAPER_DIR from Step 0>"
LEDGER="$PAPER_DIR/claims.json"
CAND="$PAPER_DIR/novelty-duplication-advisory.candidates.json"
TRACE="<abs TRACE dir from Step 0>"
RUNMETA="$TRACE/run.meta.json"
python3 - "$LEDGER" "$CAND" "$TRACE" "$PAPER_DIR" "$RUNMETA" <<'PY'
import json, re, sys, os, glob
ledger_path, cand_path, trace_dir, paper_dir, runmeta = sys.argv[1:6]
def nw(s): return " ".join((s or "").split())

led = json.load(open(ledger_path, encoding="utf-8"))
L = int(led.get("observability_level", 0)); PID = led.get("paper_id", "?")
CONTRIB_TYPES = {"scope", "method", "comparison"}
CONTRIB_SECT  = {"abstract", "intro", "introduction"}
# a contribution CUE — so an abstract/intro claim only anchors if it actually states a
# contribution, not background/citation/problem-statement text (avoids over-anchoring).
CONTRIB_CUE = re.compile(r"\b(we\s+(propose|present|introduce|develop|design|show|"
                         r"contribute)|our\s+(method|approach|model|framework|contribution)|"
                         r"novel|first\s+to|state[- ]of[- ]the[- ]art|key\s+(idea|contribution))\b", re.I)
def sect(c): return ((c.get("location") or {}).get("section") or "").lower()
def is_contrib(c):
    if c.get("type") in CONTRIB_TYPES: return True            # deterministic contribution types
    return sect(c) in CONTRIB_SECT and bool(CONTRIB_CUE.search(c.get("text_span", "")))
claims = {c["claim_id"]: c for c in led.get("claims", [])
          if c.get("claim_id") and is_contrib(c)}

cands = {}
if os.path.isfile(cand_path):
    for c in json.load(open(cand_path, encoding="utf-8")):
        if isinstance(c, dict) and c.get("candidate_id"):
            cands[c["candidate_id"]] = c

# retrieval_incomplete is honestly recorded by Step 2 in run.meta.json
retrieval_incomplete = False
try:
    rm = json.load(open(runmeta, encoding="utf-8"))
    rv = rm.get("retrieval", {})
    retrieval_incomplete = isinstance(rv, dict) and any(v == "unavailable" for v in rv.values())
except Exception:
    pass

AXES = {"duplicate": "ADV-DUPLICATE-PUBLICATION", "combination": "ADV-TRIVIAL-COMBINATION"}
# neutralize leaked VERDICT phrasings. The bare descriptive word "duplicate" stays intact
# (it is this skill's axis term — e.g. "duplicate axis", "duplicate candidate"), but RULING
# phrasings that assert a verdict ("is a duplicate", "duplicate of", "duplicated publication")
# ARE scrubbed — surfacing candidate overlap must never read as a ruling that it IS a duplicate.
RULE_WORDS = re.compile(
    r"\b(not\s+novel|lacks?\s+novelty|trivial\w*|incremental|mere\s+stapl\w*|"
    r"reject\w*|plagiar\w*|derivative|duplicate[sd]?\s+publication|repackag\w*)\b"
    r"|\b(?:is|are|appears?|seems?|clearly|essentially|simply)\s+(?:a\s+|an\s+)?duplicate\b"
    r"|\bduplicate\s+of\b|缝合", re.I)
n_scrubbed = 0
def scrub(s):
    global n_scrubbed
    out, n = RULE_WORDS.subn("[reviewer-judgment]", s or "")
    n_scrubbed += n; return out

def claim_anchor(a):
    if not isinstance(a, dict): return None
    cid, span = a.get("claim_id"), nw(a.get("span", ""))
    c = claims.get(cid)
    if c and span and span in nw(c.get("text_span", "")):   # span IN claim, never claim IN span
        return {"claim_id": cid, "span": span,
                "location": c.get("location", {}), "artifact_hash": c.get("evidence_anchor", "")}
    return None

items, dropped, n_halluc = [], [], 0
for fp in sorted(glob.glob(os.path.join(trace_dir, "*.response.md"))):
    raw = open(fp, encoding="utf-8", errors="replace").read()
    m = re.search(r"\[.*\]", raw, re.S)            # tolerate prose / code-fence wrapping
    if not m:
        print(f"  note: no JSON array in {os.path.basename(fp)} (treated as [])"); continue
    try:
        arr = json.loads(m.group(0))
    except Exception as e:
        print(f"  WARN: unparseable JSON in {os.path.basename(fp)}: {e} (treated as [])"); continue
    if isinstance(arr, dict): arr = arr.get("findings", arr.get("items", []))
    for it in (arr or []):
        if not isinstance(it, dict): dropped.append({"why": "malformed"}); continue
        axis = it.get("axis")
        if axis not in AXES:                       # infer from pattern_id if missing
            axis = next((a for a, p in AXES.items() if p == it.get("pattern_id")), None)
        if axis not in AXES:
            dropped.append({"label": it.get("label", ""), "why": "unknown-axis"}); continue
        anch = [v for v in (claim_anchor(a) for a in (it.get("anchors") or [])) if v]
        good_ids, bad_ids, self_ids = [], [], []
        for cid in (it.get("candidate_ids") or []):
            c = cands.get(cid)
            if not c:
                bad_ids.append(cid)                                  # not in candidates.json -> hallucinated ref
            elif axis == "duplicate" and c.get("self_record_suspected"):
                self_ids.append(cid)                                 # confirmed own record -> excluded (NOT hallucinated)
            else:
                good_ids.append(cid)                                 # real candidate (incl. self_record_unconfirmed -> surfaced w/ flag)
        n_halluc += len(bad_ids)
        rec = {"axis": axis, "pattern_id": AXES[axis], "label": scrub(nw(it.get("label", ""))),
               "overlap_statement": scrub(nw(it.get("overlap_statement", ""))), "anchors": anch,
               "candidate_ids": good_ids, "overlap_kind": nw(it.get("overlap_kind", "")),
               "residual_delta_note": scrub(nw(it.get("residual_delta_note", ""))),
               "reviewer_action": scrub(nw(it.get("reviewer_action", "")))}
        # LOAD-BEARING only if it anchors to a real contribution span AND cites a real candidate
        if anch and good_ids:
            items.append(rec)
        else:
            dropped.append({**rec, "why": ("no-anchor" if not anch else "no-resolved-candidate")})
for i, p in enumerate(items, 1): p["id"] = "O%d" % i

n_dup  = sum(1 for p in items if p["axis"] == "duplicate")
n_comb = sum(1 for p in items if p["axis"] == "combination")
if retrieval_incomplete: disp = "retrieval_incomplete"
elif items:              disp = "candidate_overlap_surfaced"
else:                    disp = "no_candidate_overlap_found"

# ---------- render memo ----------
def cstr(cid):
    c = cands.get(cid, {}); idv = c.get("identifier", {}) or {}
    ref = idv.get("arxiv") or idv.get("doi") or idv.get("dblp_url") or idv.get("url") or ""
    flag = (" ⚠️ near-identical title, authorship unverified — confirm self-record vs real duplicate"
            if c.get("self_record_unconfirmed") else "")
    return f"**{c.get('title','?')}** ({c.get('venue','?')} {c.get('year','?')}) — `{ref}` [{cid}]{flag}"
def astr(a):
    sec = (a.get("location") or {}).get("section", "")
    return f"claim `{a['claim_id']}`{f' ({sec})' if sec else ''}: “{a['span']}”"

out = []
out.append(f"**Novelty / Duplication Advisory — {PID}** (retrieval-grounded, MEMO-ONLY — no verdict weight).")
out.append(f"Reviewer: gpt-5.5 xhigh, two fresh per-axis threads (no codex-reply)  ·  Run level: L{L}  "
           f"·  Disposition (informational, NOT a verdict): **{disp}**")
out.append(f"Overlap items surfaced: {n_dup} duplicate · {n_comb} combination  ·  Candidates retrieved: {len(cands)}  "
           f"·  Hallucinated candidate refs dropped: {n_halluc}  ·  Ruling words neutralized: {n_scrubbed}")
out += ["", "> ⚠️ **This is not a novelty verdict.** It lays out prior work the contribution OVERLAPS with so a "
        "human reviewer can weigh `ADV-TRIVIAL-COMBINATION` and `ADV-DUPLICATE-PUBLICATION` themselves. **It never "
        "rules \"trivial\" or \"duplicate\", and the absence of a candidate match below is NOT evidence of "
        "originality** — the search corpus is incomplete by construction (recent / non-indexed / paywalled / "
        "differently-titled work is missed). A same-authors match is legitimate self-overlap (arXiv→venue, "
        "workshop→conference, extended journal), not misconduct. `tools/adjudicate_findings.py` lists this skill in "
        "`MEMO_ONLY_SKILLS` and caps it at `info`; it carries no verdict weight.", ""]

for axis, head in [("duplicate", "ADV-DUPLICATE-PUBLICATION — candidate near-duplicates (verify; never a verdict)"),
                   ("combination", "ADV-TRIVIAL-COMBINATION — is the contribution a standard A+B+C? (reviewer judgment)")]:
    rows = [p for p in items if p["axis"] == axis]
    out += [f"### {head}", ""]
    if not rows:
        out += ["_No resolved candidate overlap surfaced on this axis. **Not** an originality finding — see the caveat above._", ""]
        continue
    for p in rows:
        out.append(f"#### {p['id']} — {p['label'] or '(unlabeled)'}  ·  _{p['overlap_kind'] or 'overlap'}_")
        if p["overlap_statement"]:   out.append(f"- **Overlap:** {p['overlap_statement']}")
        if p["anchors"]:             out.append("- **Submission contribution (anchor):** " + " ; ".join(astr(a) for a in p["anchors"]))
        if p["candidate_ids"]:       out.append("- **Candidate prior work:** " + " ; ".join(cstr(c) for c in p["candidate_ids"]))
        if p["residual_delta_note"]: out.append(f"- **Residual delta the paper still claims (descriptive):** {p['residual_delta_note']}")
        if p["reviewer_action"]:     out.append(f"- **For the human reviewer to weigh:** {p['reviewer_action']}")
        out.append("")

if disp == "no_candidate_overlap_found":
    out += ["### No candidate overlap found (NOT an originality verdict)", "",
            "The retrieval ran but surfaced no resolved prior-work overlap with the submission's title / "
            "contribution at this search depth. This is **not** evidence the work is original: the corpus search is "
            "necessarily incomplete, and the queries are bounded by the ledger's contribution spans. A human reviewer "
            "should still judge novelty against their own knowledge of the field. No verdict is rendered.", ""]
elif disp == "retrieval_incomplete":
    out += ["### Retrieval incomplete (inconclusive)", "",
            "One or more lookups were unavailable, so the prior-work search could not be completed. This memo "
            "concludes **nothing** about novelty or duplication; re-run with corpus access for a fuller picture.", ""]
if dropped:
    out += ["### Dropped (no anchor / no resolved candidate — excluded from the brief)", ""]
    out += [f"- {p.get('label') or '(no label)'}: {p.get('why','')}" for p in dropped]
    out.append("")
out += ["### Retrieval & anchoring audit", "",
        f"- overlap items surfaced: {len(items)}  ·  dropped: {len(dropped)}  ·  hallucinated/self candidate refs dropped: {n_halluc}  ·  ruling words neutralized: {n_scrubbed}",
        "- every surfaced candidate is a resolved record in candidates.json (real call + verifiable id); every anchor "
        "is a verbatim span of a contribution ledger claim.", ""]
out += ["---",
        "_Informational only. `tools/adjudicate_findings.py` lists `novelty-duplication-advisory` in "
        "`MEMO_ONLY_SKILLS` and caps every finding it emits at `info`, so this memo contributes **no verdict "
        "weight**. Novelty is a reviewer judgment; the deterministic adjudicator owns the report verdict, and neither "
        "it nor this skill rules \"trivial\" or \"duplicate\"._"]
memo_path = os.path.join(paper_dir, "novelty-duplication-advisory.memo.md")
open(memo_path, "w", encoding="utf-8").write("\n".join(out) + "\n")

# ---------- info-only findings mirror: one per surfaced item; MEMO gate caps at info ----------
mir = []
for k, p in enumerate(items, 1):
    cdesc = "; ".join(cstr(c) for c in p["candidate_ids"])
    ev = [{"claim_id": a["claim_id"], "span": a["span"], "location": a.get("location", {}),
           "artifact_hash": a.get("artifact_hash", "")} for a in p["anchors"]]
    mir.append({
        "finding_id": "NDA%03d" % k, "skill": "novelty-duplication-advisory",
        "pattern_id": p["pattern_id"],
        "title": (p["label"] or "prior-work overlap")[:120],
        "description": (p["overlap_statement"] + (" — candidates: " + cdesc if cdesc else "")
                        + ((" Residual: " + p["residual_delta_note"]) if p["residual_delta_note"] else "")
                        + "  [ADVISORY: prior-work overlap for the reviewer to weigh — NOT a trivial/duplicate ruling.]").strip(),
        "severity": "info",                        # memo-only: never verdict-bearing
        "observability_level_required": 0,
        "evidence": ev,                            # may be [] (schema permits empty evidence for info)
        "verdict_local": "needs_external_check", "requires_external_check": True,
        "false_positive_risk": "high",
        "recommended_reviewer_action": p["reviewer_action"] or ("Weigh the contribution against: " + cdesc),
        "reviewer": {"model": "gpt-5.5", "reasoning": "xhigh", "deterministic": False},
    })
find_path = os.path.join(paper_dir, "novelty-duplication-advisory.findings.json")
json.dump(mir, open(find_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"disposition={disp} (informational, NOT a verdict) | surfaced={len(items)} (dup={n_dup}, comb={n_comb}) "
      f"| dropped={len(dropped)} | hallucinated/self_dropped={n_halluc} | ruling_scrubbed={n_scrubbed}")
print("memo     ->", memo_path)
print("findings ->", find_path, f"({len(mir)} info-only)")
PY
```

**Scope of this gate:** anchor validation (verbatim span of a contribution claim), candidate
validation (the **anti-hallucination** check — every `candidate_id` must exist in
`candidates.json`; self-records excluded from the duplicate axis), ruling-word neutralization,
the informational disposition, and rendering. It computes **no verdict** and prints **no
novelty grade** — the memo is advisory and the adjudicator decides (and caps this skill at
`info`).

**CONTRIB_CLAIMS == 0 / NO_CONTRIB / NO_CANDIDATES — honest-null path.** When Step 0/1/2 sent
you here, write the two files directly (no reviewer call) so the orchestrator's globs still find
them:

```bash
PAPER_DIR="<abs PAPER_DIR from Step 0>"
printf '[]\n' > "$PAPER_DIR/novelty-duplication-advisory.findings.json"
# then Write novelty-duplication-advisory.memo.md stating: retrieval found no candidate
# overlap (or the ledger had no contribution to query); disposition=no_candidate_overlap_found;
# and — explicitly — that this is NOT evidence of originality.
```

**Always emit.** Write `novelty-duplication-advisory.findings.json` even when it is `[]` —
**silent skip is forbidden**; the orchestrator and the standalone adjudicate command both expect
the file at a predictable path. **Failure handling.** *All candidates dropped as hallucinated
AND the reviewer made strong overlap claims* → the reviewer cited prior work not in the file;
re-run that axis's Step 3 once (it must cite only `candidates.json` ids). Do **not** ship a memo
naming a paper that was never retrieved. *Empty items + complete retrieval* →
`no_candidate_overlap_found` (a correct output; do not re-run to manufacture overlap). *Lookups
unavailable* → `retrieval_incomplete` (concludes nothing).

## Step 5 — Trace (forensic; never silently dropped)

The trace dir from Step 0 must, after the run, contain both reviewer calls and the retrieval
inputs (this repo ships no `save_trace.sh`, so write the files directly with **Write**):

```
.aris/traces/novelty-duplication-advisory/<date>_run<NN>/
  run.meta.json                       # {skill, paper_id, run_level_L, taxonomy_version, retrieval{duplicate,combination}, disposition, generated_at}
  001-duplicate.request.json          # the EXACT prompt + paths sent (ledger + candidates + checklist — the independence audit trail)
  001-duplicate.response.md           # the FULL raw reviewer array (input to Step 4)
  001-duplicate.meta.json             # {model:"gpt-5.5", reasoning:"xhigh", thread_id, sandbox:"read-only"}
  002-combination.request.json        # the EXACT prompt sent
  002-combination.response.md         # the FULL raw reviewer array
  002-combination.meta.json
```

The retrieval artifacts `novelty-duplication-advisory.profile.json` and
`novelty-duplication-advisory.candidates.json` live in `PAPER_DIR` (so each reviewer reads
`candidates.json` from its `cwd`); `run.meta.json` references both and records the per-axis
retrieval status. Each `request.json` must show the executor sent only **paths + the ledger +
the candidates + the per-axis checklist** — never a Claude-authored digest or hunch like "this
looks derivative" (reviewer-independence). The `response.md` files are the immutable inputs Step
4 consumes.

## Step 6 — Hand off, or adjudicate standalone

Within `/anti-autoresearch`, **stop here.** The orchestrator globs every `*.findings.json` —
your info-only `novelty-duplication-advisory.findings.json` included, which the MEMO gate caps
at `info` — so the skill's presence reliably reaches the report without raising the verdict. The
canonical human-facing artifact is `novelty-duplication-advisory.memo.md` in `PAPER_DIR`,
surfaced to the human **alongside** `REPORT.md` as a standalone advisory. (The adjudicator's
single `--memo` slot carries the `adversarial-case-builder` memo; this advisory is presented
directly, not through `--memo`.)

Running this skill **alone** is fine — `--ledger` is **required** (it anchors every above-info
finding; without it everything fails closed to `info`). Adjudicating confirms the
no-verdict-weight property:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs path to claims.json>"; D="$(dirname "$LEDGER")"
PAPER_ID=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["paper_id"])' "$LEDGER")
L=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["observability_level"])' "$LEDGER")
python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "$D"/*.findings.json \
    --ledger "$LEDGER" \
    --paper-id "$PAPER_ID" --observability-level "$L" --taxonomy-version 0.5 \
    --out "$D/report.json" --md "$D/REPORT.md"
```

The adjudicator applies its gates in order (ANCHOR → OBSERVABILITY → FP-RISK → **MEMO** →
SURFACE) and computes `overall_verdict` ∈ {CLEAN_GIVEN_EVIDENCE, SOFT_FLAGS, HARD_FLAGS} from
the **other** auditors' findings. The MEMO gate caps every `novelty-duplication-advisory`
finding at `info`, and this skill is absent from `SKILL_TO_DIMENSION`, so it contributes **no
dimension verdict and cannot move the overall verdict** — by design. A standalone run with no
other findings therefore yields `CLEAN_GIVEN_EVIDENCE`; that is **correct**, not a miss — the
value of this skill is the **memo**; read it. Treat a single-skill report as a PREVIEW.

## Output contract

This skill **always** writes, into the ledger's directory (`PAPER_DIR`):

- `novelty-duplication-advisory.memo.md` — **canonical.** Core overlap brief per axis
  (`ADV-DUPLICATE-PUBLICATION` candidate table + `ADV-TRIVIAL-COMBINATION` decomposition), the
  mandatory *absence-≠-originality* caveat, the self-overlap caveat, the informational
  disposition, and the retrieval/anchoring audit. Carries no verdict weight; surfaced to the
  human alongside `REPORT.md`. Prints **no** novelty score and **no** trivial/duplicate verdict.
- `novelty-duplication-advisory.findings.json` — **info-only** mirror (one entry per surfaced
  overlap item; possibly `[]`), conforming to `schemas/finding.schema.json`,
  `"skill":"novelty-duplication-advisory"`, `pattern_id` ∈ {ADV-DUPLICATE-PUBLICATION,
  ADV-TRIVIAL-COMBINATION}, every entry `severity:"info"`,
  `verdict_local:"needs_external_check"`, `observability_level_required:0`. Written even when
  empty for predictable `*.findings.json` globbing; the MEMO gate makes it a no-op.
- `novelty-duplication-advisory.candidates.json` — the retrieved prior work (real records, with
  identifiers; self-records flagged). Each reviewer's prior-work universe; forensic.
- `novelty-duplication-advisory.profile.json` — the ledger-derived retrieval profile.
- `.aris/traces/novelty-duplication-advisory/<date>_run<NN>/` — the two raw reviewer calls.

It writes **no verdict and no report** of its own — `report.json` / `REPORT.md` come only from
`tools/adjudicate_findings.py` (Step 6 / the orchestrator).

## Key rules

- **Never rules novelty — by design.** The skill never outputs "trivial", "not novel",
  "duplicate", a novelty score, or a recommendation. It surfaces overlap and questions; the
  human judges; the adjudicator's `MEMO_ONLY_SKILLS` cap pins it to `info` and it is absent from
  `SKILL_TO_DIMENSION`. Leaked ruling words are neutralized in Step 4.
- **Absence ≠ originality.** "No candidate overlap found" / "retrieval incomplete" is a valid
  result that says **nothing** about novelty — the corpus is incomplete by construction. The
  memo states this explicitly; never let an empty retrieval read as "the paper is novel."
- **Prior-work side real-record-bound (anti-hallucination).** Every candidate comes from a real
  DBLP/WebSearch/WebFetch call and carries a verifiable identifier; the reviewer cites only
  `candidate_id`s in `candidates.json`. A fabricated prior paper is the same sin as a
  hallucinated citation — forbidden, and dropped in Step 4.
- **Paper side ledger-anchored.** Every contribution reference cites a contribution `claim_id`
  (type∈{scope,method,comparison} or section∈{abstract,intro}) + a verbatim span (`span in
  text_span`, whitespace-normalized, never the reverse; LaTeX escapes quoted exactly). The
  candidate goes in the table / `description`, never in the span. No anchor → dropped.
- **The title is a seed, not an anchor.** `\title{…}` (or the PDF's first line) seeds the
  duplicate search; it anchors nothing (`title_seed_is_anchor: false`). A duplicate overlap
  anchors to a contribution `claim_id`.
- **Exclude the paper's own record.** A near-identical title flagged `self_record_suspected` is
  the audited paper's own preprint/venue copy, not a duplicate; it is excluded from the
  duplicate axis (flagged, never silently dropped). Self-overlap (arXiv→venue,
  workshop→conference, extended journal) is legitimate, never misconduct.
- **Executor retrieves; reviewers map.** WebSearch / DBLP / WebFetch lookups are the executor's
  Step 2; each reviewer lays out overlap over those facts. The executor never pre-judges overlap
  into the prompt — it hands raw retrieved records (structured, not a digest), preserving
  reviewer-independence even though the corpus is external.
- **Cross-model, two fresh serial per-axis threads.** Reviewer is a different family (gpt-5.5
  xhigh, read-only); each axis is a new `mcp__codex__codex` thread, run sequentially;
  `codex-reply` is never used. Reviewer ≠ executor ≠ adjudicator.
- **Hand off external truth it does not own.** A "SOTA/first/beats prior work" claim →
  `baseline-comparison-audit`; a wrong-context/fabricated *cited* work → `citation-forensics`.
  This skill owns only the two advisory overlap signals.
- **L0 advisory framing.** `observability_level_required: 0` for both signals (decidable-as-
  advisory from text + the public corpus). Output asks a reviewer to CHECK/WEIGH, never
  "reject" / "plagiarism" / "the authors faked X." The tool audits overlap, not provenance.
- **Detect-only.** Never edit the audited paper (no `Edit`; reviewer sandbox read-only).
- **Taxonomy is a mapping layer (v0.4).** The two `ADV-*` ids are advisory signals with zero
  verdict weight — set them on the info-only findings, never to claim a decision.
- **Reproducible.** Same ledger + same candidates snapshot + same reviewer outputs → same
  validated memo + same disposition.

## When NOT to use this skill

- **No `claims.json` yet** → run `/evidence-ledger` first; this skill never invents structure
  from the raw PDF, and it needs the contribution spans to build its query (the title is read
  from the source only as a search seed).
- **You want a novelty SCORE / a PROCEED-vs-ABANDON recommendation** → that is the
  *author-facing* ARIS `/novelty-check`, not this forensics advisory. This skill never scores or
  recommends; it only surfaces overlap for a human to weigh.
- **You want a "this paper is trivial / a duplicate" verdict** → impossible by design; novelty
  is a reviewer judgment and this skill is capped at `info`. Read the memo and decide yourself.
- **You need to verify a *cited* reference exists / is used in the right context** →
  `/citation-forensics` (this skill is about overlap with work the paper need not cite).
- **You need to verify an empirical "first / SOTA / beats prior work" claim** →
  `/baseline-comparison-audit` (a baseline-integrity verdict, not an overlap memo).
- **You need intra-paper contradiction or method drift** → `/consistency-audit`
  (`HP-SCOPE-INFLATE` for an internal scope-overclaim).
- **You need code/result-level fraud** (fake GT, self-normalization, phantom numbers) →
  `/experiment-forensics` at **L2**.
- **You want an AI-text / "looks machine-written" verdict** → out of scope. Surface hints live
  in `/presentation-signals` (auxiliary, capped at minor); this repo is **not** an AI-text
  classifier and **not** a plagiarism detector — it surfaces candidates to weigh.
- **No corpus access** → the retrieval cannot run; the honest output is `retrieval_incomplete`
  (concludes nothing), not a guessed "no duplication".
- **On a timer** → never `/loop` / `/schedule` / `CronCreate` this skill; re-fire only when the
  paper / ledger / literature change (see the fence at the top). Re-running burns external-search
  budget for an identical memo.

## Review tracing

Trace policy is **forensic** (never silently skipped) — see **Step 5** for the exact layout:
`run.meta.json` + per-axis `001-duplicate.{request.json,response.md,meta.json}` and
`002-combination.{...}` (and, under `— effort: max`, each combination-component probe). Write
each `.response.md` during Step 3, immediately after its reviewer call. Every `request.json`
must contain only the paths + the ledger + the candidates file + the per-axis checklist that
were sent — the reviewer-independence audit trail. The retrieved `candidates.json` and
`profile.json` are persisted in `PAPER_DIR` and referenced from `run.meta.json` so the
prior-work universe the memo rests on is reproducible.
