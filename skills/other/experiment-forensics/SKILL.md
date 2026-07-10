---
name: experiment-forensics
description: "Audit experiment integrity against the evidence ledger. At L2 (repo + result files present) a fresh cross-model reviewer reads the eval code line-by-line for fake/derived ground truth, score self-normalization, phantom results (a paper number with no backing file/key), dead/uncalled metric code, verified-scope inflation, method-described ≠ method-evaluated drift, synthesized-looking results, placeholder/fake data still wired into a released result, code-output ≠ reported-number mismatch, and missing reproducibility artifacts (an empirical/agent/LLM paper shipping neither code nor the prompts/configs its results need) — every finding span-anchored to a ledger claim_id. At L0/L1 (PDF / source only) the same patterns are surfaced as info-level 'could-not-verify' signals where the ledger gives an anchor (observability_level_required:2) — NEVER a fraud verdict from a PDF. The reviewer PROPOSES findings; tools/adjudicate_findings.py computes the verdict. Detect-only. Triggers: \"experiment forensics\", \"audit the results\", \"check the eval code\", \"实验诚实度\"."
argument-hint: [paper-dir | repo-dir]
allowed-tools: Bash(*), Read, Write, Grep, Glob, mcp__codex__codex
---

# Experiment Forensics — are the reported results what the code computes?

Audit experiment integrity for: **$ARGUMENTS** (a paper-dir or repo-dir; use an
ABSOLUTE path — it is referred to as `TARGET` below). Emit span-anchored
`experiment-forensics.findings.json`.

> 🔒 **Do not wrap this skill in `/loop`, `/schedule`, or `CronCreate`.** It is
> verdict-bearing input — it proposes the findings the deterministic adjudicator
> turns into the report. Re-firing it on a wall-clock timer adds no signal: what
> unlocks new conclusions is a higher **observability level** (a repo / result
> files arriving → L2), not elapsed time. Schedule the *external wait that precedes
> it* — artifacts released → run **once** at the new level. (Mirrors ARIS's
> external-cadence doctrine.)

> Adapted from ARIS `experiment-audit` (#57/#131), reframed for the reviewer side.
> The original audits *your own* experiment before you claim results; this audits a
> *third party's* submission. The crucial reframe: at **L0/L1 (no code)** these
> patterns are **not decidable** — they appear only as info-level "could-not-verify"
> signals. **Code-level fraud requires L2.** A PDF can never produce a fraud verdict.

## Why this exists

LLM-driven research pipelines (and rushed human work) produce results that *look*
computed but are not what the paper claims. The repeatable failure modes — ported
from ARIS's experiment-integrity audit — are:

1. **Fake ground truth** — the eval "reference/target" is *derived from model
   outputs* and reported as performance, not as a labeled proxy. `HP-FAKE-GT`
2. **Score self-normalization** — a metric divided by the model's **own** max/min/
   mean to approach 1.0; no raw score shown. `HP-SELF-NORM`
3. **Phantom results** — a paper number maps to a result file or metric key that
   does not exist (or a function never called). `HP-PHANTOM-RESULT`
4. **Dead metric code** — a metric defined in eval code, discussed in the paper,
   but never called / never present in any result file. `HP-DEAD-METRIC`
5. **Scope inflation (verified)** — "comprehensive/robust/SOTA" while the repo
   actually ran 1–2 datasets/seeds/configs. `HP-SCOPE-INFLATE`
6. **Method drift (confirmed)** — the method *described* differs from the method
   *evaluated* (A-lite, A+oracle, extra data, different backbone, test-time labels
   the method claims not to use). `HP-METHOD-DRIFT`
7. **Synthesized-looking results** — numbers across configs related by a too-clean
   arithmetic pattern ("不像跑出来的"). `HP-SUSPICIOUS-REGULARITY`
8. **Placeholder / fake data in released code** — the released code still ships
   placeholder/dummy/fake data (e.g. a `# fake data for plotting` annotation, a
   `TODO: replace with real data`, a hard-coded `np.random.*` array) and a *reported*
   figure/number is drawn from it rather than from a real run. `HP-PLACEHOLDER-DATA`
   (flag the checkable code marker; do not infer who wrote it)
9. **Result ≠ artifact** — the code / result artifacts, read or run as released, produce
   numbers *different* from the paper's reported values for the same experiment.
   `HP-RESULT-ARTIFACT-MISMATCH` (an implementation that computes a different
   loss/normalization/architecture than the equations state is `HP-METHOD-DRIFT`, not this)
10. **Missing reproducibility artifacts** — an empirical / agent / LLM paper ships
    neither code nor the prompts/configs/hyperparameters its results depend on, so the
    claim cannot be reproduced even in principle (the *absence* is L0-stated; *what its
    results specifically need* is L2-verified). `HP-MISSING-REPRO-ARTIFACT`

These are NOT inherently misconduct — they are failure modes of optimizing agents
that lack an integrity constraint. This skill is that constraint, pointed outward,
and it stays honest about what it can and cannot see.

## Core principle (two independence axes)

**The executor (Claude) collects paths + the ledger and passes them through; a
fresh, different-family reviewer (codex) reads the code and proposes findings; a
deterministic tool decides the verdict.** Both axes from
`references/reviewer-independence.md` hold:

- **Layer 1 — cross-model (executor ≠ reviewer).** The executor never summarizes,
  pre-judges, or leaks a hunch into the prompt — it ships only paths + `claims.json`
  + the checklist + the observability level. The reviewer is a different model family.
- **Layer 2 — reviewer ≠ adjudicator.** The reviewer is demoted from *judge* to
  *evidence-extractor*: it emits span-anchored findings; `tools/adjudicate_findings.py`
  computes `overall_verdict` by fixed rules. Same ledger + same findings → same
  verdict, with no model in the final decision.

## How this differs from the other auditors (route correctly)

| Auditor | Question it answers | Level |
|---------|---------------------|------|
| **`experiment-forensics`** (this) | **Are the reported numbers what the eval code actually computes?** (fake/derived GT, self-norm, phantom result, dead metric, verified scope, method drift, placeholder/fake data, code↔paper mismatch, missing repro artifacts) | **L2** (L0/L1 → info-only; missing-repro absence is L0-stated, surfaced info here) |
| `consistency-audit` | Does the paper contradict ITSELF / does described method = evaluated method? | L0 |
| `baseline-comparison-audit` | Are the right baselines present, tuned, and is "SOTA" earned? | L0 stated / L2 verified |
| `citation-forensics` | Do the cited papers exist and support the claim made? | L0 |
| `presentation-signals` | Surface "AI-flavor" hints (auxiliary, capped at minor) | L0 |
| `adversarial-case-builder` | Strongest evidence-bound rejection memo (no verdict weight) | any |

**Do NOT raise here** (hand off instead): pure text-vs-text contradiction or
scope-vs-evidence-in-text → `consistency-audit`; "first / SOTA / beats prior work"
external truth → `baseline-comparison-audit` + `citation-forensics` (emit
`needs_external_check`); citation existence/context → `citation-forensics`;
surface/AI-flavor → `presentation-signals`; **evaluation-design validity** (train/test
leakage, a conflicted/unvalidated LLM judge, declared-but-unreported conditions) →
`eval-design-forensics` (family H, L0/L1 stated-tells — distinct from this skill's L2
code/result-integrity); the rejection memo → `adversarial-case-builder`. (Note:
an LLM that produces the GROUND-TRUTH labels stays here as `HP-FAKE-GT`, L2 — only the
LLM-as-*judge* validity question hands off to `eval-design-forensics`.)

## Pipeline role + the anchoring model (read before running)

This is an **auditor** skill in the integrity-forensics pipeline
(`references/integrity-forensics-contract.md`):

```
/evidence-ledger  →  claims.json (+ artifact_manifest.json, observability level L)
                          │
       experiment-forensics  ── reads the ledger, PROPOSES findings ──►  experiment-forensics.findings.json
                          │
   tools/adjudicate_findings.py  (deterministic; the ONLY thing that computes a verdict)
```

- It **reads the ledger**, it **never re-reads the raw paper to invent structure**,
  and it **never computes the overall verdict** — the orchestrator runs
  `tools/adjudicate_findings.py` for that. This skill stops at emitting findings.
- **The anchor is always a PAPER claim.** Every above-info finding cites a ledger
  `claim_id` and quotes a **verbatim span of that claim's `text_span`** (the paper
  number/scope/method sentence it undermines). The eval-code smoking gun
  (`src/eval.py:88`) is **not** a ledger claim, so it lives in the finding's
  `description` / `recommended_reviewer_action`, never as the anchor. No paper claim
  to anchor to ⇒ the finding cannot rise above `info`. (See worked examples.)
- **Observability caps severity.** Findings declare `observability_level_required`.
  Every code/result-level pattern is decidable only at **L2**; at L0/L1 it is emitted
  as `info` (Step 2). `tools/adjudicate_findings.py` is the structural backstop — any
  `observability_level_required` above the run's level is demoted to `info`.

## Constants & Reviewer Calling Convention

- **REVIEWER = `mcp__codex__codex`** — model `gpt-5.5`, `config:
  {"model_reasoning_effort": "xhigh"}`, `sandbox: read-only`, `cwd` = `TARGET` (the
  repo/paper dir, where the code + results live). A **different model family** from
  the executor (Claude). One **fresh thread per audit pass**; **never
  `mcp__codex__codex-reply`** across passes (the bias guard — reply is deliberately
  absent from `allowed-tools`). See `references/reviewer-independence.md`.
- **PATTERNS_OWNED** (must match `references/hack-pattern-taxonomy.md`,
  `taxonomy_version 0.5`): `HP-FAKE-GT`, `HP-SELF-NORM`, `HP-PHANTOM-RESULT`,
  `HP-DEAD-METRIC`, `HP-SCOPE-INFLATE` (verified form), `HP-METHOD-DRIFT` (L2
  confirm), `HP-SUSPICIOUS-REGULARITY` (L2 confirm), `HP-PLACEHOLDER-DATA` (L2),
  `HP-RESULT-ARTIFACT-MISMATCH` (L2), `HP-MISSING-REPRO-ARTIFACT` (verdict-bearing
  at L2 — absence noticeable at L0/L1 but surfaced as info there, confirmed at L2).
- **ROOT** = `$(git rev-parse --show-toplevel 2>/dev/null || pwd)`; **L** =
  `observability_level` from `artifact_manifest.json`; **OUTPUT** =
  `experiment-forensics.findings.json` (a bare JSON array).
- **FILES** (all under `TARGET`, next to `claims.json`): the only output is
  `experiment-forensics.findings.json`; the reviewer handoff is
  `.aris/last_reviewer_response.txt`; traces live in
  `.aris/traces/experiment-forensics/<date>_run<NN>/`.
- ⚠️ **Shell state does not persist between Bash calls** (cwd + env reset each call).
  Every block below re-resolves `ROOT` and `TARGET` at its top and reads `L` /
  `paper_id` from the manifest/ledger. **Never** rely on a variable from an earlier
  block, and **never `cd` into `TARGET`** (it would break `ROOT` resolution).

Division of labor (`references/reviewer-independence.md`):

- **Executor (Claude)** locates the ledger, lists artifact paths, gathers *mechanical
  facts* (file listings, literal-string greps, hashes), passes **paths + the ledger +
  the checklist** to the reviewer, validates the reviewer's spans, and writes the
  findings file. It never summarizes file contents, pre-judges, or leaks an opinion.
- **Reviewer (codex / gpt-5.5)** reads `./claims.json` and the code/result files
  directly from its `cwd`, proposes findings, and self-reports `false_positive_risk`.
  **Told:** the artifact paths, the ledger, the per-pass checklist, the level.
  **Not told:** any other auditor's findings, the executor's hunches, or "this looks
  AI-generated" — the tool audits integrity, not authorship.
- **One fresh thread per pass.** The A–F checklist is a single call; the optional
  G/H passes are each a NEW thread. If codex stalls (long sessions can hang),
  re-invoke the **same** prompt in a fresh thread — never `codex-reply`.

## Step 1 — Preflight: resolve root, level, paper_id (self-contained)

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
TARGET="$ARGUMENTS"          # paper-dir or repo-dir — ABSOLUTE path
case "$TARGET" in /*) ;; *) echo "FATAL: TARGET must be a non-empty ABSOLUTE path (got: '$TARGET'). Pass the paper/repo dir as an absolute path."; exit 1 ;; esac

# Toolchain must be reachable (invariant: ROOT = the Anti-Autoresearch checkout).
test -f "$ROOT/tools/build_manifest.py" || { echo "FATAL: Anti-Autoresearch tools not under $ROOT. Run this skill from inside the Anti-Autoresearch checkout (or point ROOT at it)."; exit 1; }

# The ledger is mandatory and is produced by /evidence-ledger. Do NOT invent it.
test -f "$TARGET/claims.json" || { echo "FATAL: $TARGET/claims.json missing. Run /evidence-ledger on $TARGET first (experiment-forensics reads the ledger)."; exit 1; }

# artifact_manifest.json derives the level. Build it with the real tool if absent
# (exact flags — confirm via: python3 "$ROOT/tools/build_manifest.py" --help).
if [ ! -f "$TARGET/artifact_manifest.json" ]; then
  PID=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["paper_id"])' "$TARGET/claims.json")
  python3 "$ROOT/tools/build_manifest.py" --paper-id "$PID" --dir "$TARGET" --out "$TARGET/artifact_manifest.json"
fi

# Read the level (L) + paper_id. The manifest decides L; never override it.
python3 - "$TARGET" <<'PY'
import json, sys
t = sys.argv[1]
m = json.load(open(f"{t}/artifact_manifest.json")); c = json.load(open(f"{t}/claims.json"))
print(f"paper_id={c['paper_id']}  observability=L{int(m['observability_level'])}  "
      f"(rule: repo+results->L2, latex/no-results->L1, pdf/text-only->L0)")
PY
mkdir -p "$TARGET/.aris/traces/experiment-forensics"
```

**Branch on L** (read from the echo above; `references/observability-levels.md`):
`L < 2` → **Step 2** (info-only) → **Step 6**. `L == 2` (or 3 — treat as 2, never
re-run code) → **Steps 3–6**.

**Failure handling.** No `claims.json` ⇒ stop (the FATAL above); the ledger has not
been built and this skill never invents one — tell the user to run `/evidence-ledger`
first. Never claim a higher level than the artifacts support: L is derived
deterministically (`repo + results → L2`; `latex, no results → L1`; `pdf/text only →
L0`), and the manifest decides it — you do not override it.

## Step 2 — L0 / L1: info-only "could-not-verify" signals (the honesty backbone)

At L0/L1 there is **no eval code and no result files**, so you **cannot decide any
experiment-integrity pattern**. Do **not** assert fraud, and do **not** duplicate the
L0 text-scope check — `consistency-audit` owns scope from the manuscript. This skill's
only job here is to mark, for the human, which numbers become checkable **if a repo is
released**. Generate the signals deterministically from the ledger:

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); TARGET="$ARGUMENTS"
python3 - "$TARGET" <<'PY'
import json, re, sys
t = sys.argv[1]
claims = json.load(open(f"{t}/claims.json"))["claims"]
out, n = [], 1
def add(pat, title, desc, ev, act):
    global n
    out.append({"finding_id": f"EF{n:03d}", "skill": "experiment-forensics",
                "pattern_id": pat, "title": title, "description": desc,
                "severity": "info", "observability_level_required": 2,
                "evidence": ev, "verdict_local": "needs_external_check",
                "requires_external_check": True, "false_positive_risk": "high",
                "recommended_reviewer_action": act}); n += 1
def anc(c): return [{"claim_id": c["claim_id"], "span": c["text_span"], "location": c.get("location", {})}]

GT   = re.compile(r"reference|ground.?truth|\bgt\b|gold|agreement|target", re.I)
SCOPE= re.compile(r"comprehensive|extensive|robust|general|thorough|state[- ]of[- ]the[- ]art|\bSOTA\b", re.I)
nums = [c for c in claims if c.get("type") in ("number", "comparison")]

for c in nums:                                   # GT-provenance pointer
    if GT.search(c.get("text_span", "")):
        add("HP-FAKE-GT", "Ground-truth provenance not verifiable without the repo (L0 could-not-check)",
            "This number is reported against a 'reference/target/GT'. At this level it cannot be determined whether that reference is dataset-provided or derived from model outputs. NOT an allegation — verifiable only at L2 (eval code + result files).",
            anc(c), "Request the eval code + result files; verify GT provenance at L2 (HP-FAKE-GT).")
for c in nums:                                   # near-ceiling -> normalization pointer
    v = (c.get("value") or {}).get("normalized")
    if isinstance(v, (int, float)) and ((0.99 <= v <= 1.0) or (99.0 <= v <= 100.0)):
        add("HP-SELF-NORM", "Near-perfect score — normalization not verifiable from text",
            "A near-ceiling score with no raw value shown cannot be checked for self-normalization from a PDF.",
            anc(c), "At L2, check whether the metric is divided by the model's own output statistics (HP-SELF-NORM).")
for c in claims:                                 # verified-run-count pointer (defer text scope to consistency-audit)
    if SCOPE.search(c.get("text_span", "")):
        add("HP-SCOPE-INFLATE", "Scope language — actual run count not verifiable without the repo",
            "consistency-audit owns the L0 scope-vs-evidence-in-text check; experiment-forensics can only verify how many datasets/seeds/configs ACTUALLY ran at L2.",
            anc(c), "At L2, count the configs/seeds actually executed in the result files vs this wording.")
        break
add("HP-PHANTOM-RESULT", "Result existence not verifiable without backing files",
    "Whether each reported number maps to a real key in a real result file cannot be decided from a PDF.",
    (anc(nums[0]) if nums else []), "At L2, map each headline number to a result-file key (HP-PHANTOM-RESULT).")
add("HP-DEAD-METRIC", "Metric-code liveness not verifiable without the repo",
    "Whether any discussed metric is actually computed/called cannot be decided from a PDF.",
    [], "At L2, confirm each discussed metric is called and appears in a result file (HP-DEAD-METRIC).")
add("HP-PLACEHOLDER-DATA", "Placeholder / fake data in released code not verifiable without the repo",
    "Whether the released code still contains placeholder/dummy/fake data (e.g. a '# fake data for plotting' annotation or a hard-coded random array) feeding a reported figure/number cannot be decided from a PDF — flag the code marker, not who wrote it.",
    (anc(nums[0]) if nums else []), "At L2, grep the code for placeholder/dummy/fake markers and trace whether any reported figure/number is drawn from them (HP-PLACEHOLDER-DATA).")
add("HP-RESULT-ARTIFACT-MISMATCH", "Code-output vs paper-number agreement not verifiable without the repo",
    "Whether the released code / result artifacts actually produce the paper's reported numbers cannot be decided from a PDF. (A code-vs-equation implementation divergence is HP-METHOD-DRIFT, not this.)",
    (anc(nums[0]) if nums else []), "At L2, read the code's computation + result files and check each reported number against the code-produced value (HP-RESULT-ARTIFACT-MISMATCH).")
if nums:                                          # repro-artifact inventory pointer (absence is L0-observable)
    add("HP-MISSING-REPRO-ARTIFACT", "Reproducibility artifacts absent — empirical claims not checkable even in principle (absence noticeable at L0; verdict-bearing only at L2)",
        "This paper reports empirical/number results but the submission ships no eval code and no prompts/configs the results depend on. The ABSENCE is observable now (L0 'stated'); whether the SPECIFIC prompts/configs/hyperparameters its results need are present is verifiable only if a repo is released (L2). NOT a misconduct claim — a reproducibility gap. FP: a genuinely theoretical paper; double-blind submission norms (treat as a camera-ready expectation, lower severity).",
        anc(nums[0]), "Ask for the code + the exact prompts/configs/hyperparameters the reported numbers depend on; at L2 verify they are present and complete (HP-MISSING-REPRO-ARTIFACT).")

json.dump(out, open(f"{t}/experiment-forensics.findings.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"L<2: wrote {len(out)} info 'could-not-verify' signals (severity=info, req:2 — the adjudicator keeps them at info).")
PY
```

Each emitted finding has the shape below (info-only, `observability_level_required:2`,
empty `evidence` permitted **only** for info). Then go to **Step 6** (no reviewer call
needed at L<2 — these are deterministic pointers, not judgments):

```json
{
  "finding_id": "EF001",
  "skill": "experiment-forensics",
  "pattern_id": "HP-FAKE-GT",
  "title": "Ground-truth provenance not verifiable without the repo (L0 could-not-check)",
  "description": "Claim C014 reports agreement against a 'reference'. At L0 (PDF only) it cannot be determined whether that reference is dataset-provided or derived from model outputs. This is NOT an allegation — verifiable only once the eval code + result files are available (L2).",
  "severity": "info",
  "observability_level_required": 2,
  "evidence": [
    {"claim_id": "C014", "span": "98% agreement with the reference",
     "location": {"file": "paper.txt", "section": "experiments"}}
  ],
  "verdict_local": "needs_external_check",
  "requires_external_check": true,
  "false_positive_risk": "high",
  "recommended_reviewer_action": "Request the evaluation code and result files; verify GT provenance at L2. Do not treat as a flag at this observability level."
}
```

## Step 3 — L2: collect artifacts (executor — paths + mechanical FACTS only)

You (Claude) gather inputs and **mechanical facts**; you do **not** interpret,
summarize, or pre-judge them (`references/reviewer-independence.md`). Listing what
exists and grepping for a literal string are reproducible facts, not judgments — the
same division `citation-forensics` uses for existence vs. context. Do not `cd`; use
absolute `$TARGET/...` paths.

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); TARGET="$ARGUMENTS"
mkdir -p "$TARGET/.aris"

# (a) Eval / metric / test / score / benchmark / runner code + configs -> eval_paths.txt
find "$TARGET" -type f \( -name '*eval*.py' -o -name '*metric*.py' -o -name '*test*.py' \
   -o -name '*score*.py' -o -name '*benchmark*.py' -o -name 'run*.py' -o -name 'main.py' \
   -o -name '*.yaml' -o -name '*.toml' \) 2>/dev/null | sort > "$TARGET/.aris/eval_paths.txt"

# (b) Result files the paper's numbers should live in -> result_paths.txt
find "$TARGET/results" "$TARGET/outputs" "$TARGET/logs" -type f \( -name '*.json' -o -name '*.csv' \) 2>/dev/null | sort > "$TARGET/.aris/result_paths.txt"

# (c) Likely GT / reference loaders (FACT for the reviewer; do NOT judge) -> gt_grep.txt
grep -rInE 'ground.?truth|reference|target|label|gold|gt_|normaliz' --include='*.py' "$TARGET" 2>/dev/null | head -60 > "$TARGET/.aris/gt_grep.txt"

# (d) Phantom-result FACTS: grep EACH headline number from the ledger (no hardcoded token) -> number_grep.txt
python3 - "$TARGET" > "$TARGET/.aris/number_grep.txt" <<'PY'
import json, subprocess, sys
t = sys.argv[1]
claims = json.load(open(f"{t}/claims.json"))["claims"]
toks, seen = [], set()
for c in claims:
    if c.get("type") not in ("number", "comparison"): continue
    v = c.get("value") or {}
    for tok in (str(v.get("raw") or ""), ("" if v.get("normalized") is None else repr(v["normalized"]))):
        tok = tok.strip().rstrip("%").strip()
        if tok and tok not in seen:
            seen.add(tok); toks.append((c["claim_id"], tok))
for cid, tok in toks:
    hits = subprocess.run(["grep", "-rIn", "--", tok, f"{t}/results", f"{t}/outputs", f"{t}/logs"],
                          capture_output=True, text=True).stdout.strip()
    print(f"### {cid} token={tok!r}: {'FOUND' if hits else 'NOT FOUND under results/outputs/logs'}")
    if hits: print(hits)
PY

# (e) Reproducibility anchors: hash EVERY discovered eval script + result file -> hashes.txt
{ while IFS= read -r f; do [ -n "$f" ] && shasum -a 256 "$f"; done < "$TARGET/.aris/eval_paths.txt"
  while IFS= read -r f; do [ -n "$f" ] && shasum -a 256 "$f"; done < "$TARGET/.aris/result_paths.txt"; } 2>/dev/null > "$TARGET/.aris/hashes.txt"

# (f) Ledger claim subset the reviewer must anchor to -> claim_subset.json
python3 - "$TARGET" > "$TARGET/.aris/claim_subset.json" <<'PY'
import json, sys
t = sys.argv[1]
KEEP = {"number", "comparison", "scope", "method", "artifact_ref"}
claims = json.load(open(f"{t}/claims.json"))["claims"]
print(json.dumps([{"claim_id": c["claim_id"], "type": c["type"],
                   "text_span": c.get("text_span", ""), "location": c.get("location", {})}
                  for c in claims if c.get("type") in KEEP], indent=2, ensure_ascii=False))
PY

# (g) Placeholder / dummy / fake-data markers (FACT for the reviewer; do NOT judge) -> placeholder_grep.txt
grep -rInE 'placeholder|dummy|\bfake\b|fake data for plotting|mock(ed|_|\b)|TODO.*(replace|real|actual).*data|FIXME.*data|hard.?cod(e|ed)|np\.random\.|numpy\.random\.|random\.(rand|randn|randint|uniform|normal)|synthetic.*(demo|example|plot)' \
   --include='*.py' --include='*.ipynb' --include='*.r' --include='*.R' "$TARGET" 2>/dev/null | head -80 > "$TARGET/.aris/placeholder_grep.txt"

# (h) Repro-artifact inventory: do the runnable artifacts the results would need exist? (FACT; presence listing only) -> repro_inventory.txt
{ echo "## code (*.py):";        find "$TARGET" -type f -name '*.py' 2>/dev/null | head -20
  echo "## notebooks (*.ipynb):"; find "$TARGET" -type f -name '*.ipynb' 2>/dev/null | head -20
  echo "## prompts/templates:";   find "$TARGET" -type f \( -iname '*prompt*' -o -iname '*template*' -o -name '*.jinja' -o -name '*.j2' \) 2>/dev/null | head -40
  echo "## configs:";             find "$TARGET" -type f \( -name '*.yaml' -o -name '*.yml' -o -name '*.toml' -o -name '*.cfg' -o -name '*config*.json' -o -name '*.ini' \) 2>/dev/null | head -40
  echo "## env/deps:";            find "$TARGET" -type f \( -name 'requirements*.txt' -o -name 'environment*.yml' -o -name 'pyproject.toml' -o -name 'Pipfile' -o -name 'setup.py' -o -name '*.lock' \) 2>/dev/null | head -20
  echo "## run instructions:";    find "$TARGET" -type f \( -iname 'README*' -o -iname 'RUN*' -o -name 'Makefile' -o -name '*.sh' \) 2>/dev/null | head -20; } > "$TARGET/.aris/repro_inventory.txt"

# Machine validation gate: NO eval scripts AND NO result files => the manifest's L2 is
# unsupported -> re-derive the level (then run Step 2 if it drops below 2).
EV=$(grep -c . "$TARGET/.aris/eval_paths.txt"); RS=$(grep -c . "$TARGET/.aris/result_paths.txt")
echo "eval_scripts=$EV result_files=$RS  (paths + facts + claim_subset written under $TARGET/.aris/)"
if [ "$EV" -eq 0 ] && [ "$RS" -eq 0 ]; then
  echo "L2 UNSUPPORTED (no eval scripts, no result files) — re-deriving level:"
  python3 "$ROOT/tools/build_manifest.py" --paper-id "$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["paper_id"])' "$TARGET/claims.json")" --dir "$TARGET" --out "$TARGET/artifact_manifest.json"
fi
```

Re-read L (Step 1's reader); if it is now `< 2`, run **Step 2** instead. The files
written above (`eval_paths.txt`, `result_paths.txt`, `gt_grep.txt`, `number_grep.txt`,
`placeholder_grep.txt`, `repro_inventory.txt`, `hashes.txt`, `claim_subset.json`, all
under `$TARGET/.aris/`) are the reviewer's
inputs — inline their literal contents into the Step 4 prompt. **Do not summarize file
CONTENTS** — the reviewer reads the code/results directly via its `cwd`; you only pass
paths, raw greps/hashes, and the claim subset.

## Step 4 — L2: cross-model code audit (reviewer ≠ adjudicator)

Send paths + the ledger subset + the checklist to a **fresh** `mcp__codex__codex`.
The reviewer reads the eval code line-by-line and **proposes** findings; it does not
grade the paper. Call with: `model: "gpt-5.5"`, `config:
{"model_reasoning_effort": "xhigh"}`, `sandbox: "read-only"`, `cwd: "<TARGET>"` (so
it can read `./claims.json`, `./src/...`, `./results/...` directly), `prompt:` the
block below. Assemble that `prompt:` by inlining the Step 3 `.aris/` files at the
`[inline …]` markers (read each, paste its literal contents — paths + raw facts + the
claim subset, never a summary). **One fresh thread; never `codex-reply`.**

```
You are an experiment-integrity forensics reviewer. Your working directory is the
audited repo. Read the evidence ledger yourself at ./claims.json, then read EVERY
eval script line by line, plus the result files. Observability level = L2 (repo +
results present). For each check, PROPOSE findings — do NOT grade the paper, and
describe a DISCREPANCY to verify, never an accusation of misconduct.

Inputs (paths relative to your cwd; the executor inlines the Step 3 files verbatim):
- Ledger: ./claims.json   (anchor targets — use real claim_id + verbatim text_span)
- Ledger claim subset: [inline .aris/claim_subset.json]
- Eval / metric / test / runner scripts + configs: [inline .aris/eval_paths.txt]
- Result files: [inline .aris/result_paths.txt]
- Mechanical facts already gathered (raw, uninterpreted — GT greps, per-number result
  greps, placeholder/dummy/fake-marker greps, the repro-artifact inventory, file hashes):
  [inline .aris/gt_grep.txt + .aris/number_grep.txt + .aris/placeholder_grep.txt +
  .aris/repro_inventory.txt + .aris/hashes.txt]

## Checklist (map each finding to a pattern_id)
A. Ground-truth provenance  [HP-FAKE-GT, critical] — Where does "reference/target/
   GT/gold" come from in each eval? Loaded from the DATASET, or derived/generated
   from MODEL OUTPUTS and reported as performance? FP: explicitly labeled proxy;
   self-supervised by design.
B. Score normalization      [HP-SELF-NORM, critical] — Is any metric divided by
   max/min/mean of the model's OWN outputs to approach 1.0? Are raw scores shown?
   FP: standard min–max across ALL methods incl. baselines; raw+normalized both shown.
C. Result existence         [HP-PHANTOM-RESULT, critical] — Does each paper number
   map to a real key in a real result file, with a matching value? Any function
   referenced but never called? FP: file renamed/moved but present; number from a
   cited external reference.
D. Dead metric code         [HP-DEAD-METRIC, major] — A metric defined in eval code
   and DISCUSSED in the paper but never called / never in any result file. FP:
   utility kept for future use and not discussed as a result.
E. Scope (verified)         [HP-SCOPE-INFLATE, major] — How many datasets/seeds/
   configs ACTUALLY ran (count from result files/logs) vs the paper's scope
   language? FP: scope genuinely broad; qualifiers present.
F. Eval-type classification — For each eval, classify: real_gt | synthetic_proxy |
   self_supervised_proxy | simulation_only | human_eval. (A LABELED synthetic_proxy
   or self_supervised_proxy is legitimate — NOT HP-FAKE-GT.)

## Output (one JSON array, schemas/finding.schema.json) — output ONLY the array
For each finding:
{ "finding_id", "skill":"experiment-forensics", "pattern_id",
  "title", "description"  // name the exact file:line of the eval/result smoking gun,
  "severity", "observability_level_required": 2,
  "evidence": [ { "claim_id": <a ledger claim this undermines>,
                  "span": <VERBATIM substring of that claim's text_span>,
                  "location": {...} } ],
  "verdict_local": "fail|warn|clean|needs_external_check",
  "false_positive_risk": "low|medium|high",
  "recommended_reviewer_action": <what a human should ASK/CHECK> }

ANCHOR RULE: every finding above "info" MUST cite a ledger claim_id and quote a
verbatim span of THAT claim. The code path:line is forensic detail for the
description — it is NOT a valid anchor on its own. If no paper claim is undermined,
emit at most "info". Set false_positive_risk honestly. For "first/SOTA" claims you
cannot settle from the code, set verdict_local "needs_external_check". Do NOT output
an overall PASS/WARN/FAIL verdict — only the findings array. If nothing is wrong,
output [].
```

**Additional focused passes** (each a NEW fresh thread — never `codex-reply`), run
only when the relevant ledger claims exist:

- **G. Method identity** `[HP-METHOD-DRIFT, critical]` — when a `method` claim exists
  (or `consistency-audit` raised an L0 suspicion): does the evaluated pipeline match
  the described method, or quietly run A-lite / A+oracle / extra data / a different
  backbone / test-time labels the method claims not to use — **and** does the code, as
  written, implement the described equations (same loss / normalization / architecture)
  rather than compute a different formula than the paper states? Both are method-identity
  drift (a code-vs-equation divergence belongs here, not in pass J). FP: a deliberately
  labeled ablation. Anchor to the method-description claim.
- **H. Suspicious regularity** `[HP-SUSPICIOUS-REGULARITY, major]` — when result
  tables show a too-clean arithmetic pattern (constant offset across rows, implausibly
  smooth monotonicity, identical decimals across unrelated settings): confirm against
  the actual result files/code. FP is **high** (deterministic metrics, integer
  scores, rounding, a real linear trend) — keep severity honest; never a "fabricated"
  grade.
- **I. Placeholder / fake data** `[HP-PLACEHOLDER-DATA, critical]` — when figure/number
  claims exist and the placeholder-marker grep (`.aris/placeholder_grep.txt`) is non-empty:
  does the released code still contain placeholder / dummy / fake data — stub annotations
  (`# fake data for plotting`, `dummy`, `TODO: replace with real data`), hard-coded arrays,
  or `np.random.*` feeding a plot (flag the marker, don't infer who wrote it) — and does a REPORTED
  figure/number derive from it rather than from a real run? Trace each flagged line to the
  figure/table it produces. FP: a clearly-labeled toy example or unit-test fixture that
  feeds NO reported result. Anchor to the figure/number claim the placeholder data produces.
- **J. Result/artifact fidelity** `[HP-RESULT-ARTIFACT-MISMATCH, critical]` — when number
  claims exist: does the code / result artifacts, run as written, actually produce the
  paper's reported numbers? Read the metric computation + the result files and compare each
  headline number to the code-produced value (`.aris/number_grep.txt` is the starting map).
  **Strictly artifact-number vs paper-number.** FP: seed / version / hardware variance within
  a *stated* tolerance; a documented post-hoc correction. Anchor to the number claim that
  diverges. **An implementation that computes a different formula than the paper's equations
  is HP-METHOD-DRIFT (pass G), not this** — route a code-vs-equation divergence there; THIS
  pass only asks whether the reported numbers reproduce.
- **K. Reproducibility artifacts** `[HP-MISSING-REPRO-ARTIFACT, major]` — when the paper is
  empirical / agent / LLM-driven (number or agent/LLM-pipeline claims exist): consult the
  repro-artifact inventory (`.aris/repro_inventory.txt`) and judge whether the prompts /
  configs / hyperparameters / seeds the REPORTED results depend on are actually present and
  complete enough to reproduce them — e.g. an agent/LLM paper that ships code but omits the
  prompt templates or the model/config settings its numbers depend on. FP: a genuinely
  theoretical paper (no empirical claim to reproduce); double-blind submission norms (treat
  as a camera-ready expectation → lower severity / `needs_external_check`). Anchor to the
  empirical claim whose artifacts are missing. (At L0/L1 the bare *absence* is already
  surfaced as an info pointer in Step 2; this pass is the L2 verification of *what the
  results specifically need*.)

**Save the handoff + failure handling.** Write the reviewer's full raw reply to
`"$TARGET/.aris/last_reviewer_response.txt"` (use `Write`) before validating, and
**also** preserve each call's prompt + reply as a per-call pair that never clobbers
across batches: `Write` them to
`"$TARGET/.aris/traces/experiment-forensics/pending/prompt_<NN>.txt"` and
`".../response_<NN>.txt"` (NN = 01, 02, … one per fresh thread; Step 6 moves `pending/`
into the dated run dir). If the codex call stalls or errors (long sessions can hang),
re-invoke the **same** prompt in a **fresh** thread (never `codex-reply`); if it still
fails, write `[]` to `experiment-forensics.findings.json` and proceed — never fabricate
findings. If the repo is too large for one thread, split the result files into batches,
run one **fresh** thread per batch (same prompt, different file lists), overwrite
`last_reviewer_response.txt` with that batch's reply, and run Step 5 once per batch (the
validator merges + dedupes into the output) — the per-call `pending/` files keep every
batch's raw trace.

## Step 5 — Validate every reviewer finding (the executor gate)

The reviewer proposes; **you verify before keeping**. This mirrors the adjudicator's
`_anchored` check exactly (`span` is a whitespace-normalized *substring of* the ledger
claim, never the reverse), reads `L` from the manifest (not a persisted variable),
extracts the JSON array robustly from the raw reply, re-gates any previously-saved
findings together with the new ones, and merges + re-ids (so no stale above-info
survives a multi-batch merge):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); TARGET="$ARGUMENTS"
python3 - "$TARGET" "$TARGET/.aris/last_reviewer_response.txt" <<'PY'
import json, re, sys
t, resp = sys.argv[1], sys.argv[2]
OUT = f"{t}/experiment-forensics.findings.json"
L = int(json.load(open(f"{t}/artifact_manifest.json"))["observability_level"])
claims = {c["claim_id"]: c.get("text_span", "")
          for c in json.load(open(f"{t}/claims.json"))["claims"] if c.get("claim_id")}
OWNED = {"HP-FAKE-GT","HP-SELF-NORM","HP-PHANTOM-RESULT","HP-DEAD-METRIC",
         "HP-SCOPE-INFLATE","HP-METHOD-DRIFT","HP-SUSPICIOUS-REGULARITY",
         "HP-PLACEHOLDER-DATA","HP-RESULT-ARTIFACT-MISMATCH","HP-MISSING-REPRO-ARTIFACT"}
SEV = {"info":0,"minor":1,"major":2,"critical":3}
norm = lambda s: " ".join((s or "").split())

def extract(x):                       # robust: fenced block -> whole -> first [...]
    m = re.search(r"```(?:json)?\s*(\[.*\])\s*```", x, re.S)
    for s in ([m.group(1)] if m else []) + [x]:
        try: return json.loads(s)
        except Exception: pass
    i, j = x.find("["), x.rfind("]")
    if 0 <= i < j:
        try: return json.loads(x[i:j+1])
        except Exception: pass
    return None

try: raw = open(resp, encoding="utf-8").read()
except Exception: raw = ""
proposed = extract(raw)
if proposed is None:
    print("PARSE-FAIL: no JSON array in reviewer response; merging nothing new."); proposed = []
if isinstance(proposed, dict): proposed = proposed.get("findings", [])

try: base = json.load(open(OUT))
except Exception: base = []

gated = []                                                        # re-gate BASE + new together
for f in base + proposed:
    f["skill"] = "experiment-forensics"
    f.setdefault("title", f.get("pattern_id", "experiment-forensics finding"))
    f.setdefault("verdict_local", "needs_external_check")
    f.setdefault("observability_level_required", 2)
    f["evidence"] = [ev for ev in (f.get("evidence") or [])
                     if ev.get("claim_id") and (ev.get("span") or "").strip()]
    sev, notes = (f.get("severity", "info") if f.get("severity") in SEV else "info"), []
    if L < 2 and sev != "info":                                  # (1) L<2 => info-only
        sev = "info"; f["observability_level_required"] = 2; notes.append("L<2-info-only")
    if f.get("pattern_id") and f["pattern_id"] not in OWNED and sev != "info":  # (2) owned pattern
        sev = "info"; notes.append("pattern-not-owned")
    req = f.get("observability_level_required")                  # (3) observability gate
    if sev != "info" and not (type(req) is int and 0 <= req <= 3):
        sev = "info"; notes.append("undeclared-observability")
    elif sev != "info" and req > L:
        sev = "info"; notes.append(f"obs(req{req}>run{L})")
    if sev != "info":                                            # (4) ANCHOR gate
        ok = any(ev.get("claim_id") in claims and norm(ev.get("span"))
                 and norm(ev["span"]) in norm(claims[ev["claim_id"]])
                 for ev in f["evidence"])
        if not ok: sev = "info"; notes.append("unanchored")
    if sev in ("critical","major") and not any((ev.get("span") or "").strip() for ev in f["evidence"]):
        sev = "info"; notes.append("no-span")                    # (5) high sev needs a span
    f["severity"] = sev; f.setdefault("false_positive_risk", "medium")
    if notes: f["_executor_demotions"] = notes
    gated.append(f)

seen, merged = set(), []                                          # dedupe (base already re-gated)
for f in gated:
    e0 = (f.get("evidence") or [{}])[0]
    key = (f.get("pattern_id"), e0.get("claim_id"), e0.get("span"), f.get("title"))
    if key in seen: continue
    seen.add(key); merged.append(f)
for k, f in enumerate(merged, 1): f["finding_id"] = f"EF{k:03d}"  # re-id sequentially
json.dump(merged, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"kept={len(merged)} above_info={sum(1 for x in merged if x['severity']!='info')} -> {OUT}")
PY
```

**The executor never re-grades a finding's severity by hand** (reviewer ≠ adjudicator:
semantic FP calls belong to the reviewer, the verdict to `tools/adjudicate_findings.py`
— the deterministic gates above are the only severity changes the executor makes). The
FP cases below are already in the Step 4 checklist as the "FP:" clauses; the reviewer
suppresses them at proposal time via `false_positive_risk` / `verdict_local` / `info`.
If a proposed finding clearly matches one of them but the reviewer did **not** down-rank
it, do **not** hand-edit the verdict — re-run Step 4 in a fresh thread so the *reviewer*
re-judges:

- **Eval-type ⇒ FP:** a **labeled** `synthetic_proxy` / `self_supervised_proxy` is
  **not** `HP-FAKE-GT`.
- **HP-SELF-NORM FP:** standard min–max across **all** methods (incl. baselines), or
  raw+normalized both shown.
- **HP-PHANTOM-RESULT FP:** the file was renamed/moved but is present, or the number is
  a cited external reference.
- **HP-SUSPICIOUS-REGULARITY:** `false_positive_risk: high` by default; never a
  "fabricated" grade — a *prompt to check*.
- **HP-PLACEHOLDER-DATA FP:** a clearly-labeled toy example / unit-test fixture that feeds
  NO reported result is not a flag.
- **HP-RESULT-ARTIFACT-MISMATCH FP:** seed / version / hardware variance within a *stated*
  tolerance, or a documented post-hoc correction.
- **HP-MISSING-REPRO-ARTIFACT FP:** a genuinely theoretical paper (no empirical claim to
  reproduce), or double-blind submission norms (treat as a camera-ready expectation →
  lower severity / `needs_external_check`).

The only executor-side edits to `experiment-forensics.findings.json` are **mechanical,
non-semantic** provenance stamps: set `reviewer: {"model":"gpt-5.5","reasoning":"xhigh",
"thread_id":<id>,"deterministic":false}` and, where useful, `evidence[].artifact_hash`
= the ledger claim's `evidence_anchor` (the code-file sha goes in the description).
Severity is never hand-edited up or down.

**An empty array is a valid, honest output** — if every proposed finding was demoted
or none was proposed, `experiment-forensics.findings.json` may be `[]`.

**Worked L2 finding** (the full, copyable shape):

```json
{
  "finding_id": "EF002",
  "skill": "experiment-forensics",
  "pattern_id": "HP-SELF-NORM",
  "title": "Headline score is normalized by the model's own output maximum",
  "description": "The abstract headline metric (claim C014) is reported as 0.98. In the pipeline, results/main.json stores score_norm=0.98 computed at src/eval.py:88 (sha256 a1b2c3…) as raw_score / max(model_outputs) — the divisor is the model's OWN output max, not a fixed scale or a cross-method min–max. The raw score at the same key is 0.41, and no raw column appears in the paper. Discrepancy to verify: a metric approaching 1.0 via self-referential normalization is not comparable to baselines.",
  "severity": "critical",
  "observability_level_required": 2,
  "evidence": [
    {"claim_id": "C014", "span": "achieves a score of 0.98",
     "location": {"file": "main.tex", "section": "abstract"},
     "artifact_hash": "<sha256 of main.tex from the ledger's evidence_anchor>"}
  ],
  "verdict_local": "fail",
  "reviewer": {"model": "gpt-5.5", "reasoning": "xhigh", "thread_id": "<codex thread>", "deterministic": false},
  "false_positive_risk": "low",
  "requires_external_check": false,
  "recommended_reviewer_action": "Ask the authors for the raw (un-normalized) score and the exact normalization denominator; confirm the same normalization is applied identically to all baselines. If the divisor is the model's own output statistics, the 0.98 headline is not a valid cross-method comparison."
}
```

## Step 6 — Emit, cross-reference, trace

The validated array is already written to **`$TARGET/experiment-forensics.findings.json`**
(a bare JSON array conforming to `schemas/finding.schema.json`, re-id'd `EF001…`).
**No verdict here** — the orchestrator runs the adjudicator next. Each code-level
finding already names, via its `claim_id`, the paper claim it undermines, so the
report can show "this number ↔ this code problem" — keep that linkage intact.

**Trace** every reviewer call (forensic — never silently dropped):

```bash
ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd); TARGET="$ARGUMENTS"
DATE=$(date +%Y-%m-%d); N=1
BASE="$TARGET/.aris/traces/experiment-forensics"
while [ -d "$BASE/${DATE}_run$(printf %02d $N)" ]; do N=$((N+1)); done
RUNDIR="$BASE/${DATE}_run$(printf %02d $N)"; mkdir -p "$RUNDIR"
# Move every per-call prompt_<NN>.txt / response_<NN>.txt pair (written in Step 4) into
# the dated run dir, so prompts + ALL batch replies are preserved (no clobber):
if [ -d "$BASE/pending" ]; then mv "$BASE/pending/"* "$RUNDIR/" 2>/dev/null; rmdir "$BASE/pending" 2>/dev/null; fi
# Fallback: also keep the last raw reply (covers a single-call run that skipped pending/):
cp "$TARGET/.aris/last_reviewer_response.txt" "$RUNDIR/reviewer_response.txt" 2>/dev/null
python3 -c 'import json,sys;print("observability_level", json.load(open(sys.argv[1]))["observability_level"])' "$TARGET/artifact_manifest.json" > "$RUNDIR/level.txt"
ls -1 "$RUNDIR"
```

Then print a one-screen summary (no verdict):

```
🔬 Experiment Forensics — L<L>  (paper_id=<id>)
  findings: <N> total, <M> above info
  <EF0xx> <severity> <pattern_id> — <one-line title>
  Output: $TARGET/experiment-forensics.findings.json  (proposals only)
  Verdict: NOT computed here — handed to tools/adjudicate_findings.py via the orchestrator.
```

For reference only — **the orchestrator (not this skill)** later runs (note
`--ledger` is REQUIRED: it is what re-verifies each finding quotes a verbatim ledger
span; without it every above-info finding fails closed to `info`):

```bash
# DO NOT run here — this is the orchestrator's job.
python3 "$ROOT/tools/adjudicate_findings.py" --findings "$TARGET"/*.findings.json \
    --ledger "$TARGET/claims.json" --paper-id <id> --observability-level <L> \
    --taxonomy-version 0.5 --out "$TARGET/report.json" --md "$TARGET/REPORT.md"
```

## Output contract

- `$TARGET/experiment-forensics.findings.json` — array of `finding` objects
  (`schemas/finding.schema.json`). At L0/L1: `info`-only,
  `observability_level_required:2`, `requires_external_check:true`. At L2:
  span-anchored `critical`/`major`/`minor`/`info` with honest `false_positive_risk`.
  `[]` is a valid clean result. This skill writes **no** `report.json` / `REPORT.md`.
- `$TARGET/.aris/traces/experiment-forensics/<date>_run<NN>/` — raw reviewer
  prompt(s) + response(s) + the level used.

## Key rules

- **L0/L1 ⇒ no fraud verdicts.** Below L2 this skill emits **only** info-level "needs
  code" signals (`observability_level_required:2`); the validator and the adjudicator
  both pin them to `info`. This is the honesty backbone.
- **The anchor is a PAPER claim.** Every above-info finding quotes a verbatim span of
  a real ledger claim; the eval-code `file:line` is forensic detail in the
  description, never the anchor. Unanchored ⇒ `info`.
- **Labeled proxies are legitimate.** A labeled `synthetic_proxy` / self-supervised-
  by-design eval is **not** `HP-FAKE-GT`. Honor the eval-type classification.
- **Executor collects paths + mechanical facts; the reviewer judges the code.** No
  summaries, hunches, or "this is AI-generated" leak into the prompt
  (`reviewer-independence.md`).
- **Reviewer ≠ adjudicator.** This skill proposes findings; only
  `tools/adjudicate_findings.py` computes the verdict. Never emit a verdict here.
- **Fresh thread per pass; never `codex-reply`** (omitted from `allowed-tools` on
  purpose — the bias guard).
- **Discrepancy, not accusation.** `description` and `recommended_reviewer_action`
  ask a reviewer to *check/ask*, never "reject" or "the authors faked X".
- **Not an AI-text classifier.** "Results look too clean" is `HP-SUSPICIOUS-REGULARITY`
  — high-FP, only `major` when the *result files* contradict the table (L2); a bare
  "looks fake" from a table is deferred to `consistency-audit`. Never infer authorship
  or misconduct from surface impressions (those live, capped at minor, in
  `presentation-signals`).
- **`pattern_id` ∈ taxonomy v0.4 only** (`PATTERNS_OWNED`); the taxonomy is a
  post-hoc mapping layer, not the detector.
- **Detect-only.** Never edit the audited paper or repo; the only files this skill
  writes are its own `findings.json` and trace artifacts.

## When NOT to use this skill

- **As the verdict.** It proposes findings; `tools/adjudicate_findings.py` renders
  `CLEAN_GIVEN_EVIDENCE` / `SOFT_FLAGS` / `HARD_FLAGS`. Do not read this skill's
  output as a ruling.
- **At L0/L1 to assert fraud.** With no repo you get info-level "could-not-verify"
  signals, full stop — never a fraud claim from a PDF.
- **Without `claims.json`.** No ledger ⇒ nothing can be anchored ⇒ everything fails
  closed to `info`. Run `/evidence-ledger` first; this skill never invents structure
  from the raw PDF.
- **For text-only contradictions / scope-in-text** → `/consistency-audit`; for
  baseline integrity or "SOTA / first" → `/baseline-comparison-audit` (+
  `/citation-forensics`), handed off via `needs_external_check`.
- **For authorship / "is this AI-written".** Out of scope — surface "AI-flavor" lives
  in `/presentation-signals` (auxiliary, capped at minor); this repo is **not** an
  AI-text classifier.
- **On a timer.** Re-firing adds no signal — only a higher observability level does;
  schedule the *wait for artifacts*, then run once at the new level (see the cadence
  fence at the top).

## Review tracing

After each `mcp__codex__codex` call, save the trace following ARIS Policy C (forensic;
never silently skip): write the exact prompt, the raw response, and the observability
level into `$TARGET/.aris/traces/experiment-forensics/<date>_run<NN>/`, as set up in
Step 6. Traces are the audit trail for a reproducible, defensible report and the
evidence that reviewer-independence held (the executor passed only paths + the ledger,
not summaries).

## Acknowledgements

Ports the A–F integrity checks from ARIS `experiment-audit`, motivated by
community-reported issues (#57, #131) where executor agents fabricated ground truth
and self-normalized scores. Reframed for third-party forensics: ledger-anchored
findings, observability tiers, and reviewer ≠ adjudicator.
