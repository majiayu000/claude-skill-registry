# Crystallization Heuristics

Phase 3 of the compiler is where the highest leverage lives: finding
every place the source skill's prose is hiding a deterministic procedure
that *should be code*. This file is the pattern library.

The guiding rule is simple: **if the skill's author already wrote down
the exact procedure, don't make the LLM re-derive it at runtime.** Every
token spent re-deriving a known-fixed procedure is waste, and every
MANDATORY check enforced only by prose is a bug waiting to happen.

## Why crystallization is the biggest win

Skills that compile well typically see:
- **50–70% token reduction per run** from moving formatting, batching,
  and rule enforcement into code
- **Reliability wins** from making MANDATORY checks impossible to skip
- **Testability wins** from having the deterministic parts in regression
  suites instead of trusting the agent to follow instructions

Crystallization is mostly a pattern-matching exercise. This file lists
the patterns you should actively hunt for.

## The patterns

### Pattern 1 — Literal Python or pseudocode in the prompt

**What it looks like:** the skill's markdown includes fenced code blocks
(```python` or ``` `text` ) that describe exactly how to do something.
The LLM is being asked to *read* this code and *re-execute it in its
head*.

**BDR example:**
`references/conference-enrichment.md` includes a full Python function
definition for `is_pharma(company_name)` — a keyword classifier with
hardcoded include/exclude lists. The LLM reads this file, mentally
"runs" the function on each contact, and returns a list. Absurd.

**What to do:**
- Extract the code verbatim into an `extracted/*.py` module.
- Create a `pure_function` node that calls it.
- Note the extraction in the compilation report so the human reviewer
  can verify the extraction matches the original.

**How to detect:** grep for ` ```python`, ` ```py`, and `def `. Also
look for `for contact in`-style pseudocode in plain prose — it's the
same pattern without the code fence.

---

### Pattern 2 — Fixed constants embedded in prose

**What it looks like:** the skill says "batch of 10", "wait 30 days",
"accuracy below 85", "up to 250 per call". These numbers never change
run-over-run; they're API limits or policy thresholds.

**BDR examples:**
- `enrich_contact_batch`: `batch_size: 10` (ZoomInfo API limit)
- `hubspot_upsert`: `batch_size: 100` (HubSpot API limit)
- `hubspot_create_list` → `add_contacts_to_list`: `batch_size: 250`
- `exclusion_check_recent`: `days_back: 30`
- `vet_contact`: `min_accuracy_score: 85`

**What to do:**
- Lift the constant into the node's `constants:` field in the IR.
- In the extracted Python module, define it as a module-level constant
  (so it shows up once and is trivially overridable if policy changes).
- Enforce it in code — the extracted function should *reject* inputs
  that violate the constraint, not just document it.

**Why this matters:** constants that live only in prose drift when
prompts get edited. Once a limit lives in code, it stops drifting. The
BDR skill's exclusion checks say "30 days" in the prose — in the
compiled pipeline, `RECENT_EMAIL_DAYS = 30` cannot be silently
changed to 7 without a commit that shows up in review.

**How to detect:** grep for numeric literals in the prose. Most of them
are constants begging to be lifted. Questions to ask: "does this number
ever change across runs?" — if no, it's a constant.

---

### Pattern 3 — MANDATORY checks enforced only by prose

**What it looks like:** the skill uses the word "MANDATORY", "required",
"always", "must", or "do not skip" to describe a check that happens
before some irreversible action.

**BDR example:** Phase 5 exclusion checks. The skill's
`hubspot-operations.md` literally says "MANDATORY" in ALL CAPS for the
three exclusion checks (do-not-contact, recently emailed, active
sequence). In the agent loop, nothing actually prevents the LLM from
skipping these if prompt drift is bad.

**What to do:**
- Classify the check as a `pure_function` or `external_call` node.
- Set `mandatory: true` on the node in the IR. The IR schema enforces
  that mandatory nodes cannot be made conditional.
- The adapter will emit the mandatory node as an unconditional activity
  the workflow always calls in order. The prose enforcement disappears
  because the code-level enforcement replaces it.

**Why this matters:** this is the single highest-leverage pattern in
compilation. A MANDATORY prose check is a *reliability bug waiting to
happen* — every prompt edit, every model upgrade, every long agent
trajectory is a chance for the check to get forgotten. Moving it to
code makes skipping impossible.

**How to detect:** grep (case-insensitive) for "mandatory", "required",
"always", "must", "never skip", "do not skip", "be sure to". Audit
every hit.

**Calibration — err toward marking.** On real production skills MOST
deterministic nodes end up `mandatory: true`, not a handful: every
fixed threshold, every filter/exclusion rule, every data pull the
output cannot be correct without, every fixed template render. (The
first agent run on the ops-report example marked 1 of 13 nodes when
9 of 10 was right — a daily report is *made of* rules that must all
fire.) Ask per node: "if the agent version silently skipped this
step, would the output be wrong or dangerous?" If yes, mark it.
Reserve unmarked for genuinely optional enrichment — a nice-to-have
field, a best-effort lookup with a fallback.

---

### Pattern 4 — Fixed string templates for reports and outputs

**What it looks like:** the skill shows an exact expected output
format — usually in a fenced code block or a bulleted template —
and the agent's job is to fill in the blanks.

**BDR example:** `hubspot-operations.md` shows the exact
pre-enrollment report format, counts-by-reason and all. The LLM was
generating this markdown by hand every run. Wasteful.

**What to do:**
- Create a `pure_function` node that takes typed inputs (the counts,
  the contact lists) and produces the markdown string.
- The function is pure string formatting — no LLM.

**How to detect:** look for ````text` or ````markdown` blocks with
placeholder syntax (`[name]`, `{field}`, `...`). Also look for any
output spec with a fixed structure.

---

### Pattern 5 — Batching and rate-limiting loops with fixed semantics

**What it looks like:** the skill says "process in batches of N",
"chunk by Y per call", "wait between requests". The loop structure and
batch size are fixed.

**BDR examples:**
- Enrich contacts in batches of 10
- Upsert contacts in batches of 100
- Add to list in batches of 250

**What to do:**
- Extract the batch size as a constant (see Pattern 2).
- The batching loop lives inside the extracted function, not the
  workflow — the workflow calls the function once with a list of any
  size, and the function handles chunking internally.
- The adapter can set appropriate activity timeouts based on the
  expected batch count.

**How to detect:** grep for "batch of", "chunk", "max ... per".

---

### Pattern 6 — Taxonomy / enum lookups that never change

**What it looks like:** the skill does setup lookups (ID resolution,
category mapping, static reference data) at the start of every run.
The underlying data is stable — these IDs don't change month-over-month.

**BDR example:** `taxonomy_lookup` — the ZoomInfo management level IDs
(VP, Director), industry IDs (pharma, biotech), department ID (Medical
& Health). These IDs have been stable for years.

**What to do:**
- Extract as a `pure_function` node with a `cache:` config for
  aggressive caching (e.g., `persistent`, `30d`).
- On first run, the function hits the API; subsequent runs read from
  cache until TTL expires.

**How to detect:** look for "look up", "resolve", "get the ID for",
"find the category", especially as setup steps at the start of a
phase.

---

### Pattern 7 — Numeric or enum thresholds disguised as LLM rules

**What it looks like:** the skill's rubric includes a rule like
"discard contacts with accuracy below 85" or "contacts older than 90
days are stale". These look like they belong in the `llm_judge` rubric,
but they're actually hard thresholds.

**BDR example:** `vet_contact` — the rubric says "flag contacts below
85 accuracy". This is a numeric comparison, not a judgment call.

**What to do:**
- Keep the step as `llm_judge` (the rest of the rubric is fuzzy).
- But add a **pre-filter** in the signature that short-circuits on the
  hard threshold before calling the LLM. The BDR
  `signatures/vet_contact.py` does this — low-accuracy contacts never
  reach the model.
- This saves tokens on the obvious cases and guarantees consistency on
  the hard rules.

**How to detect:** look for numeric comparisons in rubrics ("below X",
"above Y", "at least Z"). Every one is a potential pre-filter.

### Pattern 8 — Independent data pulls hiding in sequential prose

**What it looks like:** the skill lists data-gathering steps in
sequence ("First pull the Slack channel. Then run the Gmail
searches.") but no step consumes another's output — the ordering
exists only because an agent executes one tool call at a time.

**What to do:** give the independent pulls no connecting edges so
they land in the same execution wave, and list every independent
entry point in `entry_nodes` (plural!). Adapters run same-wave nodes
concurrently — the compiled pipeline should be *faster* than the
agent, and parallel data pulls are usually the single biggest
wall-clock win available.

**How to detect:** for each pair of adjacent data-pull steps, ask
"does step B's input mention anything step A produced?" If not, they
are parallel regardless of the prose order. The deal-monitor example
is the canonical case: the Slack intake pull and the fixed Gmail
searches share nothing and must be two entry nodes — the first agent
run serialized them into one entry and left the speedup on the table.

---

## When NOT to crystallize

The hunt for crystallization should be aggressive, but not blind. Leave
things agentic when:

1. **The procedure genuinely varies run-over-run.** Target company
   research (BDR Phase 1.5) calls different tools for different
   indications, draws on different sources, produces different briefs.
   That's `agent_loop`, not `pure_function`.

2. **The inputs are unbounded prose.** Summarizing someone's employment
   history to check franchise alignment isn't code-able — the input
   shape is unbounded and the judgment is fuzzy. That's `llm_judge`.

3. **The skill explicitly says "this is a judgment call".** Trust the
   source. If the skill author marked something as needing human or
   LLM judgment, there's usually a reason.

4. **Crystallizing would require reimplementing an existing fuzzy
   service.** Don't try to replace a vendor's search ranking with
   your own code. Use the service; codify the *calling convention*,
   not the service's internal logic.

## The estimation heuristic

When producing the Phase 7 compilation report, estimate the
"% codifiable" as:

```
codifiable_nodes = count(pure_function) + count(external_call)
total_nodes = len(all nodes except hitl_gate)
pct = codifiable_nodes / total_nodes * 100
```

A well-compiled BDR-scale skill lands around **60–70% codifiable**.
If you're below 40%, you're probably leaving crystallization on the
table. If you're above 80%, either you have a very structured skill
or you're over-crystallizing — double-check that the remaining
`llm_judge` / `agent_loop` nodes genuinely need the LLM.

## Scanning order

When doing Phase 3, walk through the source skill in this order:

1. **Every `references/*.md` file first.** The reference files usually
   contain the highest density of crystallizable patterns (literal code,
   constants, rubrics with thresholds).
2. **Then the main `SKILL.md`.** It's orchestration-level and usually
   has fewer literal patterns, but contains the MANDATORY flags and
   phase ordering.
3. **For each file, grep for the detection terms listed in each pattern
   above.** Note every hit. You'll usually find more patterns than
   nodes — several patterns often apply to the same node.

Record every extraction candidate in the compilation report with
`file:line`, the current prose, and the proposed codified form. This
is the primary audit trail for the compilation and the thing the human
reviewer will check first.
