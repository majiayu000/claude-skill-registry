---
name: citation-forensics
description: "Citation-integrity forensics: is every reference real, correctly attributed, and used in a context the cited work actually supports? Catches hallucinated references (no paper at the claimed arXiv id/DOI/venue, fabricated authors/year), metadata drift (wrong year/venue/version), and wrong-context citations (a real paper cited for a claim it never makes — or argues against). A hot zone for machine-generated papers. Decidable at L0 (text + canonical sources). Span-anchored to the evidence ledger (claims.json); the executor gathers canonical facts (DBLP / arXiv / DOI), then one FRESH cross-model thread per cited key proposes findings; reviewer != adjudicator. Emits citation-forensics.findings.json; NEVER computes the verdict. Triggers: \"citation forensics\", \"check the references\", \"hallucinated citations\", \"wrong-context citation\", \"verify references\", \"引用核对\"."
argument-hint: [paper-dir | claims.json]
allowed-tools: Bash(*), Read, Write, Grep, Glob, WebSearch, WebFetch, mcp__codex__codex, mcp__mcp-dblp__search, mcp__mcp-dblp__fuzzy_title_search, mcp__mcp-dblp__get_venue_info
---

# Citation Forensics — are the references real and honestly used?

Audit citation integrity for: **$ARGUMENTS** (requires `claims.json` from
`/evidence-ledger`; reasons over its `type:"citation"` claims). Emit span-anchored
`citation-forensics.findings.json`. This skill computes **no verdict**.

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> verdict-bearing input — it proposes the citation findings the deterministic
> adjudicator turns into the report. Re-firing it on a wall-clock timer adds no
> signal: its output changes only when the **paper / ledger / bibliography**
> changes, not with the clock, and each run spends real cross-model + lookup budget
> per cited key. Schedule the *external wait that precedes it* — bibliography
> finalized → ledger rebuilt → audit **once**. (Mirrors ARIS's external-cadence
> doctrine.)

> Adapted from ARIS `citation-audit`, re-wired onto this repo's evidence ledger and
> the reviewer≠adjudicator contract, and reframed from "audit + **rewrite** the bib"
> to **"emit ledger-anchored findings, never touch the paper."** Three layers, ported
> verbatim: **existence → metadata → context.** Following the repo's
> `baseline-comparison-audit` pattern, the **executor** gathers the canonical facts
> (DBLP / arXiv / DOI) as neutral evidence; a **fresh cross-model reviewer** judges
> existence + metadata + context over those facts. The reviewer never grades — the
> deterministic adjudicator does.

## Why this exists

An autoresearch pipeline (or a rushed human) generates a bibliography in a separate
pass from the prose and never reconciles the two. The failure modes are **not**
wildly fake entries — those are easy to spot. The dangerous ones are:

- **Hallucinated reference** — no paper exists at the claimed arXiv id / DOI / venue;
  authors, title, or year are fabricated. (`HP-CITE-HALLUC`, critical)
- **Metadata drift** — a real paper cited with the wrong year, wrong venue (the arXiv
  preprint number used after the work appeared at CVPR/ICML/NeurIPS, or vice versa),
  or a v1 title silently merged with a v3 retitle. (`HP-CITE-HALLUC`, major)
- **Wrong-context citation** — a real paper used to support a claim it does **not**
  make, or argues *against* (e.g. citing a self-refinement paper to support
  "self-feedback yields correlated errors" when the cited paper argues the
  opposite). (`HP-CITE-CONTEXT`, major)

None of this needs the code, the data, or a re-run — only the citing sentence (from
the ledger) checked against the cited work's public record (DBLP / arXiv /
publisher). That is why this layer is **L0-decidable** (observability-wise — no repo
or result files needed) and independently defensible. (The citing-sentence *claims* it
anchors to still enter the ledger only via the LaTeX path; a pure PDF-text ledger
yields none — see Step 0.)

## Core principle

**Ledger-anchored, span-verified, canonical-fact-checked-or-handed-off,
reviewer≠adjudicator, detect-only.**

1. The cite keys and the **citing sentences** come from the deterministic ledger
   (`claims.json`, `type:"citation"`), never from re-reading the PDF.
2. The executor assembles a neutral per-key **dossier** (citing spans + the claimed
   `.bib` metadata) and gathers a reproducible **resolution snapshot** of the
   canonical record (DBLP / arXiv / DOI). It gathers **facts, never a judgment** —
   whether a mismatch is fabrication, a typo, or a preprint→venue migration is the
   reviewer's call.
3. A **fresh cross-model reviewer** (gpt-5.5 xhigh, one thread per cited key)
   *proposes* findings, judging existence + metadata + context over those facts.
4. **Every above-info finding cites a ledger `claim_id` + a verbatim span** of the
   **citing sentence** (`references/integrity-forensics-contract.md` rules 1–2). The
   bib entry, the canonical record, and any URL live in the finding's `description`,
   never as the anchor span.
5. The model **proposes**; `tools/adjudicate_findings.py` **decides**
   (`references/reviewer-independence.md` Layer 2). This skill emits findings only.
6. **Fact-or-hand-off honesty.** Existence/metadata MUST be settled against a real
   source (snapshot record + URL in `description`). Cannot settle → `verdict_local:
   needs_external_check` — **never** a guessed "fabricated". A false hallucination
   flag is a serious error.

> **The anchor is the citing sentence, not the bib line.** `tools/build_claim_ledger.py`
> puts `type:"citation"` claims in the ledger whose `text_span` is the *sentence that
> contains `\cite{key}`* and whose `refs` are the cite keys — it does **not** parse
> the `.bib`. So a citation finding always anchors to that citing sentence (quote a
> verbatim substring of it, e.g. `\cite{smith2024bar}` or the surrounding phrase).
> What the `.bib` claims and what DBLP/arXiv actually return go in `description` —
> there is no ledger claim for the `.bib` line to anchor to. A bib key that is in the
> `.bib` but never `\cite`d has no citation claim, cannot be anchored, and is
> therefore **out of scope** (detect-only; not flagged).

## How this differs from the other auditors (route correctly)

| Auditor | Question it answers | Level |
|---------|---------------------|------|
| **`citation-forensics`** (this) | **Do the cited papers exist, with correct metadata, and support the claim they are used for?** | **L0** |
| `consistency-audit` | Does the paper contradict ITSELF / described method = evaluated method? | L0 |
| `baseline-comparison-audit` | Are the right baselines present, tuned, and is "SOTA" earned? | L0 stated / L2 verified |
| `experiment-forensics` | Are the reported numbers what the code actually computes? (fake GT, self-norm, phantom) | L2 |
| `presentation-signals` | Surface "AI-flavor" hints (auxiliary, capped at minor) | L0 |
| `adversarial-case-builder` | Strongest evidence-bound rejection memo (no verdict weight) | any |

**Do NOT raise here** (hand off instead): numeric self-contradiction / method drift →
`consistency-audit`; "first / SOTA / beats prior work" as an *empirical* claim →
`baseline-comparison-audit` (emit `needs_external_check`); code/result-level fraud →
`experiment-forensics` (needs L2); surface / AI-flavor of the prose →
`presentation-signals`; the rejection memo → `adversarial-case-builder`. **Stay in
lane:** this skill judges only whether *the cited work* exists, is described
correctly, and supports the citing sentence — not whether the citing paper's own
claim is true.

## Constants & Reviewer Calling Convention

```
REVIEWER_MODEL       = gpt-5.5                  # different family from executor (Claude)
REVIEWER_REASONING   = xhigh                    # always; effort never lowers reviewer quality
REVIEWER_SANDBOX     = read-only                # detect-only; never mutate the paper or .bib
REVIEWER_CWD         = <PAPER_DIR>              # so it can re-open claims.json + the .bib to confirm a span
THREAD_POLICY        = ONE fresh mcp__codex__codex per CITED KEY; NEVER mcp__codex__codex-reply across keys
TAXONOMY_VERSION     = 0.5                      # references/hack-pattern-taxonomy.md §E
PATTERNS             = HP-CITE-HALLUC (existence/metadata) | HP-CITE-CONTEXT (wrong context) | HP-CITE-RETRACTED (retracted/withdrawn)
OBS_REQUIRED         = 0 for all three patterns # decidable at L0 (text + canonical / retraction sources)
FACT_GATHERING       = executor, Step 2: DBLP MCP + WebSearch/WebFetch -> resolution.json (FACTS, never a verdict)
DOSSIER              = <PAPER_DIR>/.aris/citation-forensics/dossier.json      # Step 1 (rehashable; NOT /tmp)
RESOLUTION           = <PAPER_DIR>/.aris/citation-forensics/resolution.json   # Step 2 (rehashable; NOT /tmp)
FINDINGS             = <PAPER_DIR>/citation-forensics.findings.json           # Step 4 output
TRACE_POLICY         = forensic (never silently dropped)
TRACE_DIR            = <PAPER_DIR>/.aris/traces/citation-forensics/<YYYY-MM-DD>_run<NN>/
```

- **Executor (Claude)** builds none of the judgment: it pulls the citation claims
  from the ledger, assembles the per-key dossier, gathers the canonical resolution
  facts, validates the reviewer's spans, and writes the findings file. It never
  summarizes the paper, pre-judges "this reference is fake", or leaks an opinion into
  the prompt — only structured inputs (the dossier + the neutral resolution snapshot
  + the checklist). (`reviewer-independence.md` Layer 1.)
- **Reviewer (codex / gpt-5.5)** judges existence + metadata + context per key over
  the executor's facts and self-reports `false_positive_risk`. It is the
  evidence-weigher, not the judge. Like the other auditors it runs
  `config: {"model_reasoning_effort": "xhigh"}`, `sandbox: read-only`; the lookups
  are the executor's job (Step 2), not the reviewer's.
- **Fresh thread per cited key.** `codex-reply` is intentionally absent from
  `allowed-tools`; never carry one key's conclusion into another (the bias guard).
- **Detect-only.** No `Edit` in `allowed-tools` — this skill never rewrites the
  `.bib` or any `.tex` (that is ARIS `citation-audit`'s job, not a forensics tool's).

---

## Step 0 — Preconditions: locate the ledger, read the level, find the bib, set the run dir

The ledger is the **only** structure this skill reasons over. Resolve it and read the
run's observability level **L**, `paper_id`, the set of cited keys, and the
bibliography path(s) (each Bash block is self-contained — shell state does not
persist, so re-derive paths every time):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
# $ARGUMENTS is a paper-dir OR a claims.json path:
LEDGER="$ARGUMENTS"; [ -d "$LEDGER" ] && LEDGER="$LEDGER/claims.json"
# Only the NO-ARGUMENT case defaults to the CWD ledger. An EXPLICIT argument that
# resolves to a missing claims.json must NOT silently fall back to $(pwd) — that
# could audit the wrong paper; let the NO_LEDGER check below fire instead.
[ -z "$ARGUMENTS" ] && LEDGER="$(pwd)/claims.json"
python3 - "$LEDGER" <<'PY'
import json, sys, os, glob
p = sys.argv[1]
if not os.path.isfile(p):
    sys.exit("NO_LEDGER: claims.json not found. Run /evidence-ledger FIRST "
             "(it writes artifact_manifest.json + claims.json).")
d = json.load(open(p, encoding="utf-8"))
paper_dir = os.path.dirname(os.path.abspath(p)) or "."
cites = [c for c in d.get("claims", []) if c.get("type") == "citation"]
keys  = sorted({k for c in cites for k in (c.get("refs") or [])})
bibs  = glob.glob(os.path.join(paper_dir, "**", "*.bib"), recursive=True)
print("LEDGER      =", os.path.abspath(p))
print("PAPER_DIR   =", paper_dir)
print("PAPER_ID    =", d.get("paper_id", "?"))
print("RUN_LEVEL_L =", d.get("observability_level", 0))
print("CITE_CLAIMS =", len(cites))
print("CITE_KEYS   =", len(keys), keys)
print("BIB_FILES   =", bibs or "NONE (metadata layer will be partial)")
PY
```

Then create the run directories (start `NN` at `01`, bump if it exists):

```bash
PAPER_DIR="<PAPER_DIR printed above>"
DATE=$(date -u +%Y-%m-%d)
TBASE="$PAPER_DIR/.aris/traces/citation-forensics"
NN=01; while [ -d "$TBASE/${DATE}_run$NN" ]; do NN=$(printf '%02d' $((10#$NN + 1))); done
RUN="${DATE}_run$NN"
mkdir -p "$TBASE/$RUN" "$PAPER_DIR/.aris/citation-forensics"
echo "RUN        = $RUN"
echo "TRACE_DIR  = $TBASE/$RUN"
echo "DOSSIER    = $PAPER_DIR/.aris/citation-forensics/dossier.json"
echo "RESOLUTION = $PAPER_DIR/.aris/citation-forensics/resolution.json"
echo "FINDINGS   = $PAPER_DIR/citation-forensics.findings.json"
```

**Failure / edge handling.**
- `NO_LEDGER` → **stop**; tell the user to run `/evidence-ledger` first. This skill
  never re-reads the raw PDF and invents structure (contract rule 1).
- `CITE_CLAIMS = 0` → the ledger has no `type:"citation"` claims. This is expected on
  an **L0 PDF-text-only** run: `extract_from_text` in `tools/build_claim_ledger.py`
  extracts numbers + scope language but **not** citations (only the LaTeX path
  `extract_from_latex` emits `citation` claims). Skip to Step 4, write
  `citation-forensics.findings.json` = `[]`, and note: *"no citation claims in ledger
  — re-run /evidence-ledger with the LaTeX source, or the paper has no `\cite`."*
  **Silent skip is forbidden** — the file must exist.
- `BIB_FILES = NONE` (or only a `.bbl`) → continue. The citing sentences still anchor
  the audit, and existence + context are checkable from the cite key + the sentence +
  canonical sources. The **metadata** layer is then partial (no claimed
  authors/year/venue to compare) — say so in the dossier and tell the reviewer the
  bib entry is unavailable for that key. That is honest, not a failure.

Carry the absolute `LEDGER`, `PAPER_DIR`, `PAPER_ID`, `L`, `RUN`, `TRACE_DIR`,
`DOSSIER`, and `RESOLUTION` paths into the steps below.

## Step 1 — Build the per-key citation dossier (deterministic; no judgment)

Group every `type:"citation"` claim by cite key (a `\cite{a,b}` claim contributes to
both `a` and `b`) and, best-effort, attach the **claimed** `.bib` metadata for each
key by balanced-brace extraction from any `*.bib` under the paper dir. Pure assembly —
no web, no opinion. Stage it under `.aris/` so the verifier can rehash it (never
`/tmp`):

```bash
LEDGER="<abs LEDGER>"; PAPER_DIR="<abs PAPER_DIR>"
OUT="$PAPER_DIR/.aris/citation-forensics/dossier.json"
python3 - "$LEDGER" "$PAPER_DIR" "$OUT" <<'PY'
import json, os, re, sys, glob
ledger_path, paper_dir, out = sys.argv[1], sys.argv[2], sys.argv[3]
L = json.load(open(ledger_path, encoding="utf-8"))
cites = [c for c in L.get("claims", []) if c.get("type") == "citation"]

# 1) group citing spans by cite key
keys = {}
for c in cites:
    for k in (c.get("refs") or []):
        keys.setdefault(k, []).append({
            "claim_id": c["claim_id"],
            "span":     c.get("text_span", ""),
            "location": c.get("location", {}),
        })

# 2) best-effort: parse claimed metadata per key from any .bib (balanced-brace)
bibtext, bibfiles = "", []
for p in glob.glob(os.path.join(paper_dir, "**", "*.bib"), recursive=True):
    try:                                         # best-effort: skip an unreadable .bib
        txt = open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        continue
    bibfiles.append(p)
    bibtext += txt + "\n"

def bib_entry(key):                          # @type{key, ... } with brace matching
    m = re.search(r"@\w+\s*\{\s*" + re.escape(key) + r"\s*,", bibtext)
    if not m:
        return None
    i, depth = m.end(), 1
    while i < len(bibtext) and depth:
        depth += (bibtext[i] == "{") - (bibtext[i] == "}")
        i += 1
    return bibtext[m.start():i][:1200]

entries = [{"key": k, "n_cites": len(keys[k]),
            "bib_entry": bib_entry(k), "citing": keys[k]} for k in sorted(keys)]
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump({"n_keys": len(entries), "bib_files": bibfiles, "entries": entries},
          open(out, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
missing = [e["key"] for e in entries if not e["bib_entry"]]
print(f"dossier: {len(entries)} cited keys from {len(cites)} citation claims; "
      f"bib_files={bibfiles or 'NONE'}; no-bib-entry keys={missing} -> {out}")
PY
```

**Gate — sanity.** The printed `cited keys` count should match what you expect for
the paper. `0` keys with `CITE_CLAIMS > 0` (rare) means the `refs` were empty —
spot-read a citation claim in `claims.json`. Keys flagged `no-bib-entry` (no `.bib`,
or the key missing from it) are audited **existence + context only** — the metadata
layer is partial because there is no claimed authors/year/venue to compare. That is
honest; the reviewer infers the intended work from the cite key + the citing
sentences.

## Step 2 — Canonical-source resolution (executor gathers FACTS; non-blocking)

For each cited key, gather a **reproducible snapshot** of what the canonical record
actually is — so a finding is reproducible against staged facts even if DBLP changes
later, and so the reviewer has the evidence it needs to judge. **This step records
facts, never a verdict**: whether a mismatch is fabrication, a typo, or a
preprint→venue migration is the reviewer's call in Step 3. (Same executor-gathers /
reviewer-weighs division as `baseline-comparison-audit` Step 2.)

For each key, seed the queries from the dossier's bib title / authors / venue. If
`bib_entry` is null (no `.bib`, or only a `.bbl`), seed instead from the cite-key
tokens (author / year / keyword) plus distinctive words from that key's citing
sentence(s) in the dossier — existence + context stay checkable; the metadata layer is
then partial (nothing claimed to compare against), which is honest, not a failure:

- **DBLP fuzzy title** — `mcp__mcp-dblp__fuzzy_title_search` with `title=<bib title>`,
  `similarity_threshold=0.7` (lower to ~0.5 only if no hit). Returns canonical
  `{title, authors, venue, year, doi, ee, url}` for the top matches.
- **DBLP boolean cross-check** — `mcp__mcp-dblp__search` with
  `query="<first-author surname> and <distinctive title word>"` (the query supports
  only `and`/`or`, **no parentheses**). Confirms author↔title↔year coherence;
  `venue_filter` / `year_from` / `year_to` narrow it.
- **Venue exists** — `mcp__mcp-dblp__get_venue_info` with `venue_name=<bib venue>` to
  confirm the venue is real and of the claimed `type` (Conference or Workshop /
  Journal / Repository).
- **arXiv / DOI resolve + content** — `WebFetch` the arXiv abstract page built from
  the bib `eprint`/`arxiv` id (`https://arxiv.org/abs/<id>`) and capture the returned
  title + authors **and the abstract text** (the abstract is what lets the reviewer
  judge *context*); `WebFetch https://doi.org/<doi>` to confirm the DOI resolves to
  this work. Use `WebSearch` as a fallback for very recent papers (< ~2 weeks) not yet
  in DBLP.

Write one neutral record per key to the staged snapshot (use `Write`), and copy it
into the trace dir (Step 5):

```json
// .aris/citation-forensics/resolution.json
{
  "smith2024bar": {
    "dblp_fuzzy_top": [{"title": "...", "authors": ["..."], "venue": "...",
                        "year": 2024, "doi": "...", "url": "https://dblp.org/..."}],
    "venue_info": {"venue": "...", "type": "Conference or Workshop"},
    "arxiv": {"id": "2401.01234", "resolves": true, "title_returned": "...",
              "abstract": "... fetched abstract text, for the context layer ..."},
    "doi": {"doi": "10.1145/...", "resolves": true},
    "notes": "facts only — not a verdict"
  }
}
```

**Failure handling (non-blocking).** If a DBLP MCP call errors, or web access is
unavailable, write `{"<key>": {"status": "unavailable", "reason": "..."}}` for that
key and continue — the Step 3 reviewer then falls back to
`verdict_local: needs_external_check` for that key rather than guessing. Note the skip
in the trace. **Never** hand-author a "fabricated" conclusion from a failed lookup.

## Step 3 — Per-entry cross-model audit (existence → metadata → context)

Existence and metadata are mechanical fact-checks against the snapshot; *context*
needs judgment. **Read `dossier.json` + `resolution.json`.** For **each** entry, issue
**one fresh** `mcp__codex__codex` call (key order; tag `001`, `002`, …), `cwd =
PAPER_DIR` so the reviewer can re-open `claims.json` / the `.bib` to confirm a span.
**Inject that one key's dossier record and resolution record** in place of the two
bracketed blocks. Send EXACTLY this — it is the reviewer's complete instruction set;
add no commentary of your own about the paper:

```
mcp__codex__codex:
  model: gpt-5.5
  config: {"model_reasoning_effort": "xhigh"}
  sandbox: read-only
  cwd: <absolute PAPER_DIR from Step 0>
  prompt: |
    You are an integrity-forensics reviewer auditing ONE bibliographic citation key
    of a research paper. You judge three things and NOTHING ELSE: does the cited
    paper EXIST, is its METADATA correct, and does it actually SUPPORT the claim each
    citing sentence uses it for. You do NOT judge whether the citing paper's own
    result is true, and you NEVER accuse anyone of misconduct. You audit integrity,
    not authorship.

    Judge existence + metadata from the RESOLUTION SNAPSHOT below — canonical FACTS
    (DBLP / arXiv / DOI) gathered by the executor. It is evidence, NOT a verdict:
    cross-check the .bib's self-report against it. If the snapshot is "unavailable",
    or does not settle a key either way, say so and set verdict_local
    "needs_external_check"; do NOT guess existence, and NEVER fabricate the cited
    paper's contents. Judge CONTEXT only from the snapshot's abstract/title (the
    fetched record — never from memory of the cited paper); if the snapshot lacks
    enough of the cited paper's content to decide, set "needs_external_check" and tell
    the human which section of the cited paper to read.

    ## THE ENTRY UNDER AUDIT (from the evidence ledger; claims.json is in your cwd —
    ## you MAY re-open it to confirm a span is real, but you may NOT introduce a
    ## claim_id that is not listed here):
    [DOSSIER RECORD FOR THIS KEY — dossier.json["entries"][i]:
     {key, n_cites, bib_entry (claimed metadata; null if no .bib), citing:[{claim_id, span, location}]}]

    ## CANONICAL RESOLUTION gathered by the executor (FACTS; may be empty/unavailable):
    [RESOLUTION RECORD FOR THIS KEY — resolution.json["<key>"]]

    ## WHAT TO CHECK (run all three layers for THIS key; one finding per concrete discrepancy)
    (A) EXISTENCE — does a paper exist at the claimed arXiv id / DOI / venue with the
       claimed title (or, if bib_entry is null, the work implied by the key + the
       citing sentences)?                                            [HP-CITE-HALLUC]
       * No record resolves anywhere; authors/title/year fabricated -> severity critical.
       * The id is a TYPO but the paper plainly exists at the corrected id -> severity
         minor (a FIX, not a fabrication), false_positive_risk medium.
       * Very recent work (<~2 weeks) not yet indexed / snapshot unavailable -> set
         needs_external_check, severity info; do NOT call it fabricated.
       * IDENTIFIER-HIJACKING: the arXiv id / DOI RESOLVES, but the resolved record's
         title and/or authors in the snapshot do NOT match the citation -> the existence
         check alone is NOT enough; the load-bearing test is the title/author MATCH against
         the resolved record. Mismatch -> severity critical (resolves to an unrelated work).
         Keep wording neutral (state the metadata mismatch; do NOT use "deception"). FP: the
         id resolves to a newer VERSION of the same work.
       * PLACEHOLDER CITATION: the bib/citing span is a leftover stub ("[ref?]", "[CITATION]",
         "\cite{XXX}", "TODO: cite", "?") never replaced -> severity major if load-bearing,
         else minor; false_positive_risk medium (a clearly-marked draft).
    (B) METADATA — real paper, but wrong year / wrong venue (arXiv number used though it
       appeared at NeurIPS) / wrong-or-missing authors / v1<->v3 retitle. [HP-CITE-HALLUC]
       * severity major. A preprint->published migration (arXiv 2023 -> CVPR 2024) is
         a COMMON legitimate case: severity minor, false_positive_risk high.
    (C) CONTEXT — for EACH citing sentence: does the cited paper actually establish what
       the sentence uses it for? Flag a real paper cited to support a claim it does
       NOT make, or argues AGAINST.                                  [HP-CITE-CONTEXT]
       * severity major. In `description`, state what the cited paper actually
         establishes vs how the sentence uses it. false_positive_risk high if a
         "see also / contrast with / unlike" reading is plausible, or the load-bearing
         claim is the citing paper's OWN contribution.
       * Also flag SEMANTIC-HALLUCINATION: a real reference attached to a finding the
         cited paper does not contain, or an attribution of a specific claim/number the
         cited work never makes (paper real; attributed content not). Judge ONLY from the
         snapshot's abstract/title; if insufficient, set needs_external_check.
       * AUXILIARY INTENT LABEL: optionally add `intent` ∈ {support|contrast|mention} with
         a confidence in `description`. It only SHARPENS candidates (a contrast/mention
         reading is the common FP; only a `support` cite whose work doesn't support the
         claim is dangerous) — NEVER a verdict on its own; do not raise severity on it.

    (D) RETRACTION — does the RESOLUTION SNAPSHOT report the cited work as RETRACTED or
       withdrawn (Crossref / Retraction-Watch open metadata)? If so, and a citing sentence
       RELIES on it to support a claim with no note of the retraction, flag it. [HP-CITE-RETRACTED]
       * severity major when the retracted reference is load-bearing.
       * If the sentence cites it EXPRESSLY to discuss the retraction, or the retraction
         POST-DATES submission -> severity info/minor, false_positive_risk high (honest use).
       * An "expression of concern" / erratum / correction is NOT a full retraction -> do
         not flag as retracted. If the snapshot has no retraction record -> do NOT infer one.
       * Retraction is a FACT about the cited work (source + date in `description`), never an
         accusation against the citing authors.

    ## HARD RULES (a finding that breaks any of these is worthless)
    1. ANCHOR. Every finding above severity "info" MUST carry >=1 evidence entry
       {claim_id, span}, where claim_id is ONE OF the citing claim_ids above and span
       is a VERBATIM substring of THAT citing sentence (no paraphrase — e.g. quote
       "\cite{<key>}" or a phrase of the sentence). Put the .bib metadata, the
       canonical record, and the URL in `description`, NOT in `span` — there is no
       ledger claim for the .bib line or a DBLP URL to anchor to. If you cannot quote
       a verbatim substring of a listed sentence, keep the finding at "info".
    2. FACT OR HAND OFF — never guess from memory. Settle existence/metadata against
       the snapshot (cite the record/URL in `description`). If the snapshot cannot
       settle it, emit verdict_local "needs_external_check", requires_external_check
       true, severity "info", and say what to look up. A false "this citation is
       fabricated" is a serious error.
    3. OBSERVABILITY. Set observability_level_required = 0 on every finding: citation
       existence, metadata, and wrong-context are decidable from text + the public
       record (you do not need the repo or result files).
    4. DISCREPANCY, NOT ACCUSATION. `description` and `recommended_reviewer_action`
       say what a human should CHECK or ASK. Never "reject", "fabricated by the
       authors", "the authors faked X".
    5. HONEST FP RISK — set it truthfully. COMMON false positives: typo'd-but-
       resolvable id (a FIX); preprint->published migration; "see also / contrast"
       framing; 6+-author "and others" truncation; the claim being the citing paper's
       own contribution.
    6. pattern_id is exactly one of: "HP-CITE-HALLUC", "HP-CITE-CONTEXT", "HP-CITE-RETRACTED".

    ## OUTPUT — a single JSON array, and NOTHING ELSE (no prose, no code fence). Each
    element conforms to schemas/finding.schema.json:
      {
        "finding_id": "F001",
        "skill": "citation-forensics",
        "pattern_id": "HP-CITE-HALLUC | HP-CITE-CONTEXT | HP-CITE-RETRACTED",
        "title": "short, neutral",
        "description": "the discrepancy: what the .bib claims, what the canonical "
                       "source returns (+URL), and/or what the cited paper actually "
                       "establishes vs how it is used",
        "severity": "critical|major|minor|info",
        "observability_level_required": 0,
        "evidence": [{"claim_id": "C0xx", "span": "verbatim substring of the citing sentence",
                      "location": {"file": "...", "section": "..."}}],
        "verdict_local": "fail|warn|clean|needs_external_check",
        "requires_external_check": false,
        "false_positive_risk": "low|medium|high",
        "recommended_reviewer_action": "what to CHECK or ASK — never 'reject'"
      }
    If this key is clean on all three layers, emit []. An empty array is a valid,
    honest result.
```

**Immediately after each call returns**, persist the trace (Step 5) **before** the
next key's call: write the FULL raw reply with `Write` to
`<TRACE_DIR>/<NNN>-<key>.response.md`, the exact prompt sent to
`<NNN>-<key>.request.json`, and `<NNN>-<key>.meta.json`
(`{model, reasoning, sandbox, thread_id}`). The `.response.md` files are the immutable
input to Step 4.

**Reference output — what good findings look like** (the shape the validator keeps):

```json
// HP-CITE-CONTEXT (major) — the dangerous case: real paper, wrong claim
{
  "finding_id": "F001", "skill": "citation-forensics", "pattern_id": "HP-CITE-CONTEXT",
  "title": "Self-refinement work cited for the opposite of what it shows",
  "description": "The sentence cites \\cite{madaan2023selfrefine} to support that self-feedback yields correlated errors. The cited paper (Self-Refine, NeurIPS 2023; DBLP https://dblp.org/... confirms title/venue/authors; abstract in resolution.json) demonstrates that iterative self-feedback IMPROVES outputs — it does not establish correlated self-feedback errors. The citation supports a claim the cited work does not make.",
  "severity": "major", "observability_level_required": 0,
  "evidence": [{"claim_id": "C042", "span": "\\cite{madaan2023selfrefine}",
                "location": {"file": "sections/2.overview.tex", "section": "method"}}],
  "verdict_local": "fail", "false_positive_risk": "medium",
  "recommended_reviewer_action": "Re-read Self-Refine §1; ask which result supports 'correlated errors', or re-attribute the claim to a paper that establishes it."
}
// HP-CITE-HALLUC (critical) — no canonical record resolves
{
  "finding_id": "F002", "skill": "citation-forensics", "pattern_id": "HP-CITE-HALLUC",
  "title": "No paper resolves at the claimed arXiv id / title",
  "description": "\\cite{kim2024neuralcompress} claims arXiv:2407.99999 with authors {Kim, Park}. resolution.json: arXiv:2407.99999 does not resolve; DBLP fuzzy+boolean return no paper with this title and author set. The reference appears to have no canonical record.",
  "severity": "critical", "observability_level_required": 0,
  "evidence": [{"claim_id": "C051", "span": "\\cite{kim2024neuralcompress}",
                "location": {"file": "sections/6.related.tex", "section": "related"}}],
  "verdict_local": "fail", "false_positive_risk": "low",
  "recommended_reviewer_action": "Ask the authors for a resolvable arXiv id / DOI; verify it exists before relying on the surrounding claim."
}
```
> Contrast (NOT critical): a typo'd-but-resolvable id (`2407.9999` → real `2407.09999`)
> is a **FIX** → `severity: minor`/`info`, `false_positive_risk: low`,
> `recommended_reviewer_action: "correct the arXiv id"`. A preprint→venue migration
> (arXiv 2023 → CVPR 2024) is metadata drift at most (`major` only if the wrong record
> is load-bearing), never `critical`.

**Budget / fan-out.** Default: **one fresh thread per cited key** (the bias guard).
For a long bibliography you MAY group a handful of keys into one fresh
`mcp__codex__codex` call **only if** the prompt keeps each key in its own clearly
labeled block (with its own dossier + resolution records) and emits a flat array of
findings each anchored to its key's citing claim — but **never** use `codex-reply` to
carry one key's conclusion into another.

**Failure handling.**
- *MCP stall / hang* (common in long sessions): re-invoke the **identical** prompt as
  a **fresh** `mcp__codex__codex` call (gpt-5.5, xhigh) — never `codex-reply`.
- *Reviewer returns prose, not a JSON array*: the Step 4 validator extracts the
  outermost `[...]`; if there is none, re-ask that one key with "Output ONLY the JSON
  array, nothing else." Never hand-author findings on the reviewer's behalf.
- *Resolution unavailable for a key*: that is the honest path — expect `info` /
  `needs_external_check` for existence/metadata. Do **not** upgrade them.

## Step 4 — Validate + anchor + emit (the anti-hallucination gate)

**Coverage gate (fail closed).** First confirm Step 3 actually ran: count
`ls "$TRACE_DIR"/*.response.md | wc -l` and require one `.response.md` per cited key
(fewer only if you deliberately batched keys into a shared response — then each
batched key must still appear in some `.response.md`). **Zero response files while
`CITE_CLAIMS > 0` means Step 3 never ran — STOP and run it; do NOT emit a clean `[]`.**
The *only* legitimate empty-findings path is the `CITE_CLAIMS = 0` short-circuit from
Step 0.

Enforce the ANCHOR gate **before** keeping anything — it mirrors the verbatim-span
rule `tools/adjudicate_findings.py` re-applies (so nothing you keep is silently
rejected downstream), **plus** one citation-specific check: a citation finding must
rest on a `type:"citation"` (citing-sentence) claim, not a stray number/scope claim.
This reads every `*.response.md` in the trace dir, applies schema hygiene, merges, and
renumbers. The span must be a verbatim, whitespace-normalized **substring of** the
cited claim (`span in claim`, never `claim in span` — appending hallucinated text to a
real sentence must fail):

```bash
LEDGER="<abs LEDGER>"; TRACE_DIR="<abs TRACE_DIR>"
OUT="<abs PAPER_DIR>/citation-forensics.findings.json"
python3 - "$LEDGER" "$TRACE_DIR" "$OUT" <<'PY'
import json, re, sys, glob, os
ledger_path, trace_dir, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

def nw(s):                                    # mirror adjudicator _norm_ws (whitespace only)
    return " ".join((s or "").split())

ALLOWED    = {"HP-CITE-HALLUC", "HP-CITE-CONTEXT", "HP-CITE-RETRACTED"}   # the ONLY patterns this skill emits
OBS        = {"HP-CITE-HALLUC": 0, "HP-CITE-CONTEXT": 0, "HP-CITE-RETRACTED": 0}   # all decidable at L0 (taxonomy 0.5 §E)
SEV        = {"critical", "major", "minor", "info"}
VL         = {"fail", "warn", "clean", "needs_external_check"}
FPR        = {"low", "medium", "high"}
ABOVE_INFO = {"critical", "major", "minor"}

L = json.load(open(ledger_path, encoding="utf-8"))
claims = {c["claim_id"]: c for c in L.get("claims", []) if c.get("claim_id")}

kept, dropped, demoted, n = [], 0, 0, 0
files = sorted(glob.glob(os.path.join(trace_dir, "*.response.md")))
for fp in files:
    raw = open(fp, encoding="utf-8", errors="replace").read()
    m = re.search(r"\[.*\]", raw, re.S)       # tolerate prose / code-fence wrapping
    if not m:
        print(f"  note: no JSON array in {os.path.basename(fp)} (treated as [])"); continue
    try:
        arr = json.loads(m.group(0))
    except Exception as e:
        print(f"  WARN: unparseable JSON in {os.path.basename(fp)}: {e} (treated as [])"); continue
    if isinstance(arr, dict):                  # tolerate {"findings": [...]}
        arr = arr.get("findings", [])
    for f in arr:
        if not isinstance(f, dict):
            dropped += 1; continue
        pid = f.get("pattern_id")
        if pid not in ALLOWED:                 # stray HP-* / surface signal -> not this skill's to emit
            dropped += 1; continue
        n += 1
        f["finding_id"] = f"F{n:03d}"          # FORCE renumber — per-key arrays each start at F001
        f["skill"] = "citation-forensics"      # force-correct the skill tag
        # enum hygiene: any illegal value -> safe default
        if f.get("severity") not in SEV: f["severity"] = "info"
        if f.get("verdict_local") not in VL: f["verdict_local"] = "warn"
        if f.get("false_positive_risk") not in FPR: f["false_positive_risk"] = "high"
        if f["verdict_local"] == "needs_external_check":
            f["requires_external_check"] = True
        # ANCHOR gate: span is a verbatim ws-normalized SUBSTRING of its cited claim,
        # AND that claim must be a type:"citation" (citing-sentence) claim.
        anchored, has_cite_anchor = [], False
        for ev in (f.get("evidence") or []):
            cid, span = ev.get("claim_id"), nw(ev.get("span", ""))
            c = claims.get(cid)
            if c and span and span in nw(c.get("text_span", "")):   # span IN claim, not claim IN span
                ev.setdefault("location", c.get("location", {}))     # enrich for human navigation
                ev.setdefault("artifact_hash", c.get("evidence_anchor", ""))
                anchored.append(ev)
                if c.get("type") == "citation":
                    has_cite_anchor = True
        f["evidence"] = anchored
        if f["severity"] in ABOVE_INFO and not (anchored and has_cite_anchor):
            f["severity"] = "info"; demoted += 1   # unanchored / non-citation anchor -> info
        # observability fallback: a real int 0-3 (JSON bool is an int subclass -> reject)
        olr = f.get("observability_level_required")
        if isinstance(olr, bool) or not isinstance(olr, int) or not (0 <= olr <= 3):
            f["observability_level_required"] = OBS.get(pid, 0)
        # cross-model provenance (reviewer-independence: a proposal, not a verdict)
        f["reviewer"] = {"model": "gpt-5.5", "reasoning": "xhigh", "deterministic": False}
        kept.append(f)

json.dump(kept, open(out_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"validated {len(kept)} citation findings from {len(files)} entry response(s) "
      f"({demoted} demoted to info for unanchored/non-citation span, "
      f"{dropped} dropped: non-citation-pattern/malformed) -> {out_path}")
PY
```

Scope of this gate: **anchoring + schema hygiene** — verbatim-span anchoring (the span
must be a substring of a `type:"citation"` claim), enum coercion, non-citation-pattern
rejection, observability fallback, and cross-model provenance — so every kept finding
is well-formed and honestly anchored. It does **not** compute the verdict, the FP-risk
cap, or the observability *downgrade* against the run level; those belong to
`tools/adjudicate_findings.py`, the single decider.

**Always emit.** Write `citation-forensics.findings.json` even when it is `[]` (no
citation claims, or every key clean) — **silent skip is forbidden**; the orchestrator
and the standalone adjudicate command both expect the file at a predictable path. If
the `CITE_CLAIMS = 0` short-circuit from Step 0 fired, simply
`echo '[]' > "<PAPER_DIR>/citation-forensics.findings.json"` here. This skill has no
deterministic-tool pass — there is no `check_citations.py`; existence/metadata require
the live public record, which the executor fetches in Step 2.

**Failure handling.** A bad response file is reported and skipped (treated as `[]`) so
one malformed entry never aborts the merge — re-run that key's Step 3 with the
strict-JSON reminder if you want its findings back. A finding that loses all evidence
is **kept as info**, never silently dropped (the forensic record stays).

## Step 5 — Trace (forensic; never silently dropped)

Save every reviewer call under
`<PAPER_DIR>/.aris/traces/citation-forensics/<YYYY-MM-DD>_run<NN>/`. This repo ships
no `save_trace.sh`, so write the files directly, one set per cited key (mirror ARIS
review-tracing — fresh thread per key, full reply preserved; the `.response.md` is also
the forensic record of what the reviewer concluded over the gathered facts):

```
.aris/traces/citation-forensics/<date>_run<NN>/
  run.meta.json                       # {skill, paper_id, run_level_L, n_keys, generated_at}
  resolution.json                     # the executor's Step 2 canonical-facts snapshot (copy)
  001-<key>.request.json              # the EXACT prompt sent for this key (dossier+resolution+checklist; no paper digest)
  001-<key>.response.md               # the FULL raw reviewer reply (input to Step 4)
  001-<key>.meta.json                 # {model:"gpt-5.5", reasoning:"xhigh", sandbox:"read-only", thread_id}
  002-<key>.request.json ...
```

```bash
TRACE_DIR="<abs TRACE_DIR>"
python3 - "$TRACE_DIR" "<PAPER_ID>" "<L>" "<N_KEYS>" <<'PY'
import json, sys, datetime
d, pid, L, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
json.dump({"skill": "citation-forensics", "paper_id": pid, "run_level_L": L,
           "n_keys": n,
           "generated_at": datetime.datetime.now(datetime.timezone.utc)
                               .isoformat().replace("+00:00", "Z")},
          open(d + "/run.meta.json", "w", encoding="utf-8"), indent=2)
print("wrote", d + "/run.meta.json")
PY
```

Each `request.json` is the independence audit trail — it must show the executor sent
only the **dossier record + the neutral resolution facts + the checklist**, never a
hunch like "this looks AI-generated".

## Step 6 — Hand off, or adjudicate standalone

Within `/anti-autoresearch`, **stop here**: the orchestrator globs every
`*.findings.json`, runs the adjudicator, and emits `REPORT.md` + `report.json`. When
running this skill **alone**, you may produce the report yourself — `--ledger` is
**required** (it re-verifies each finding quotes a real ledger span; without it every
above-info finding fails closed to `info`):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
LEDGER="<abs LEDGER>"; D="$(dirname "$LEDGER")"
python3 "$ROOT/tools/adjudicate_findings.py" \
    --findings "$D/citation-forensics.findings.json" \
    --ledger "$LEDGER" \
    --paper-id "<PAPER_ID>" --observability-level <L> --taxonomy-version 0.5 \
    --out "$D/report.json" --md "$D/REPORT.md"
```

The adjudicator applies, in order: ANCHOR → OBSERVABILITY → FP-RISK → MEMO → SURFACE
gates, then computes `overall_verdict` ∈ {CLEAN_GIVEN_EVIDENCE, SOFT_FLAGS,
HARD_FLAGS}. A span-anchored, low-FP **HP-CITE-HALLUC critical** (a reference with no
canonical record) decidable at L0 → **HARD_FLAGS**; a high-FP context flag survives at
most as `minor` → **SOFT_FLAGS**. No model is in the final decision.

## Output contract

This skill **always** writes, into the ledger's directory:

- `citation-forensics.findings.json` — Step 4, a JSON array conforming to
  `schemas/finding.schema.json` (or `[]` when there are no citation claims or all are
  clean — written regardless; **silent skip is forbidden**). Each above-info finding
  carries `evidence[].claim_id` + a verbatim `span` of the citing sentence,
  `pattern_id` ∈ {HP-CITE-HALLUC, HP-CITE-CONTEXT, HP-CITE-RETRACTED}, and
  `observability_level_required: 0`.
- `.aris/citation-forensics/dossier.json` + `resolution.json` — Steps 1–2, the
  rehashable staged inputs (per-key citing spans + claimed bib metadata + canonical
  facts).
- `.aris/traces/citation-forensics/<date>_run<NN>/` — Step 5, the raw per-key reviewer
  calls (`run.meta.json` + `resolution.json` + per-key
  `request.json` / `response.md` / `meta.json`).

It writes **no verdict and no report** of its own — `report.json` / `REPORT.md` come
only from `tools/adjudicate_findings.py` (Step 6 / the orchestrator).

## Key rules

- **The anchor is the citing sentence.** Every above-info finding quotes a verbatim
  substring of a `type:"citation"` claim's `text_span`; the `.bib` line, the
  canonical record, and any URL go in `description` (the ledger has no bib claim to
  anchor to). `span in claim`, whitespace-normalized — never `claim in span`.
- **Executor gathers facts; reviewer weighs them.** DBLP / arXiv / DOI lookups are
  the executor's Step 2 (`resolution.json`); the reviewer judges existence + metadata
  + context over those facts. Same division as `baseline-comparison-audit`.
- **Fact-verify or hand off.** Existence/metadata must be settled against the
  canonical record (cited in `description`). Cannot settle → `needs_external_check`,
  never a guessed "fabricated". A false hallucination flag is a serious error.
- **Don't trust the bib.** A `.bib` entry's metadata is the *claim under audit*, not
  ground truth — verify it against DBLP / arXiv / the publisher.
- **Wrong-context > metadata.** A real paper used to support a claim it never makes is
  more dangerous than a typo'd author — and is the headline value of this skill.
- **L0 only — stay in lane.** `observability_level_required: 0` for all three patterns;
  they are decidable from text + canonical sources, no repo or results. This skill
  never asserts code/result-level fraud (that needs L2 → `experiment-forensics`).
- **Cross-model, one fresh thread per cited key.** Reviewer is a different family
  (gpt-5.5 xhigh); each key is a new `mcp__codex__codex` thread; `codex-reply` is
  never used across keys.
- **Reviewer ≠ adjudicator.** The model proposes findings; `adjudicate_findings.py`
  decides the verdict. This skill emits findings only.
- **Discrepancy, not accusation.** Output asks a reviewer to *check / ask*, never to
  reject; the tool audits citation integrity, not authorship — preprint migrations,
  "see also" framing, and `and others` truncation are honest FPs, not fraud.
- **Uncited bib entries are out of scope** by default — no citation claim to anchor
  to; detect-only, not flagged unless explicitly requested (no budget spent on them).
- **Detect-only.** Never edit the `.bib` or any `.tex` (no `Edit` in `allowed-tools`;
  reviewer sandbox `read-only`). Rewriting citations is ARIS `citation-audit`'s job.
- **Reproducible.** Same ledger + same resolution snapshot + same findings → same
  verdict.

## When NOT to use this skill

- **No `claims.json` yet** → run `/evidence-ledger` first; this skill never invents
  structure from the raw PDF.
- **No citation claims in the ledger** (e.g. an L0 PDF-text-only run, where the
  extractor does not pull citations) → there is nothing to anchor to. Re-run
  `/evidence-ledger` with the LaTeX source so `citation` claims enter the ledger;
  otherwise emit `[]` and say why.
- **You need numeric self-contradiction or method drift** → `/consistency-audit`.
- **You need to verify an empirical "SOTA / first / beats prior work" claim** →
  `/baseline-comparison-audit` (+ hand off via `needs_external_check`); this skill
  judges only whether *the cited work* supports the sentence, not whether the citing
  paper's own result is true.
- **You need code/result-level fraud** (fake GT, self-normalization, phantom numbers)
  → `/experiment-forensics` at **L2**.
- **You want an AI-text / "looks machine-written" verdict** → out of scope. Surface
  hints live in `/presentation-signals` (auxiliary, capped at minor); this repo is
  **not** an AI-text classifier.
- **You want the `.bib`/`.tex` auto-fixed** → that is ARIS `citation-audit`
  (co-author mode). This skill is detect-only.
- **On a timer** → never `/loop` / `/schedule` / `CronCreate` this skill; re-fire only
  when the paper / ledger / bibliography changes (see the fence at the top).

## Review tracing

Policy: **forensic** — never silently skip. The full per-key trace layout
(`run.meta.json` + the `resolution.json` snapshot + per-key
`NNN-<key>.request.json` / `.response.md` / `.meta.json`) is defined in **Step 5**;
write each `.response.md` during Step 3, immediately after its reviewer call. Each
`request.json` must hold only the dossier record + neutral resolution facts + the
checklist (the reviewer-independence audit trail) — never a hunch.
