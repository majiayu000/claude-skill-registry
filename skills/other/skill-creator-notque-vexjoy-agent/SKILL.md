---
name: skill-creator
description: "Create and iteratively improve skills through eval-driven validation."
agent: toolkit-governance-engineer
routing:
  force_route: true
  triggers:
    - create skill
    - create a skill
    - create new skill
    - new skill
    - scaffold skill
    - scaffold a skill
    - build a skill
    - skill template
    - skill design
    - test skill
    - improve skill
    - optimize description
    - skill eval
  pairs_with:
    - agent-evaluation
    - verification-before-completion
  complexity: Complex
  category: meta
allowed-tools:
  - Read
  - Edit
  - Write
  - Bash
  - Glob
  - Grep
  - Agent
---

# Skill Creator

Create skills and iteratively improve them through measurement.

## Output style directive (applies to every generated skill/agent)

Generated SKILL.md and agent bodies must be written as **dense informational
text focused on accuracy**. Minimize prose, maximize signal, no filler.

- No motivational framing, no pep talk, no "this will help you...".
- No repeated restatement of the same constraint in different words.
- Prefer tables, numbered phases, and bullet lists over paragraphs.
- Every sentence must carry information the model will act on; cut anything
  that is only atmosphere.
- Explanations of "why" stay short and attached to the rule they justify --
  one clause, not a paragraph.

New and edited skill files are written to the **Dense-Complete Writing standard**:
`skills/shared-patterns/dense-complete-writing.md`. That file is the canonical rule;
the bullets above are its application to skill scaffolding.

This is a generation constraint on the outputs of this skill, not a style note
for this skill's own prose. Enforce it during the "Write the SKILL.md" phase
and during any agent scaffolding.

The process:

- Decide what the skill should do and how it should work
- Write a draft of the skill
- Create test prompts and run claude-with-the-skill on them
- Evaluate the results -- both with agent reviewers and optionally human review
- Improve the skill based on what the evaluation reveals
- Repeat until the skill demonstrably helps

Figure out where the user is in this process and help them progress. If they say
"I want to make a skill for X", help narrow scope, write a draft, write test cases,
and run the eval loop. If they already have a draft, go straight to testing.

---

## Creating a skill

### Capture intent

Start by understanding what the user wants. The current conversation might already
contain a workflow worth capturing ("turn this into a skill"). If so, extract:

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases, what contexts)
3. What is the expected output?
4. Are the outputs objectively verifiable (code, data transforms, structured files)
   or subjective (writing quality, design aesthetics)? Objectively verifiable outputs
   benefit from test cases. Subjective outputs are better evaluated by human review.

### Duplicate Domain Check

Before creating any new skill, check whether an existing umbrella skill already
covers this domain. This is mandatory -- skipping it leads to system prompt bloat
and routing degradation.

**Step 1**: Search for existing domain coverage.
```bash
grep -i "<domain-keyword>" skills/INDEX.json
ls skills/ | grep "<domain-prefix>"
```

**Step 2**: If a domain skill exists, determine whether the new skill's scope is a
sub-concern of the existing skill. Sub-concerns MUST be added as reference files
on the existing skill, not created as separate skills.

Pattern (correct): `skills/perses/references/plugins.md`
Incorrect (creates domain overlap): `skills/perses-plugin-creator/SKILL.md`

**Step 3**: If no domain skill exists and the domain has multiple sub-concerns,
create the skill with a `references/` directory from the start.

**One domain = one skill + many reference files. Never create multiple skills for
the same domain.**

Only proceed to writing a new SKILL.md if no existing skill covers the domain, or
if the user explicitly confirms creating a new skill after reviewing the overlap.

### Research

Read `docs/PHILOSOPHY.md` before writing any component. The philosophy contains
binding architectural decisions — not suggestions — that govern how agents carry
knowledge, how skills structure workflows, how references are organized, and how
content is framed. Components that violate the philosophy will fail review.

Read the repository CLAUDE.md before writing anything. Project conventions override
default patterns.

### Write the SKILL.md

Based on the user interview, create the skill directory and write the SKILL.md.

**Skill structure:**

```
skill-name/
├── SKILL.md              # Required -- the workflow
├── SPEC.md               # Optional -- contract for complex/high-impact skills
├── EVAL.md               # Optional -- repeatable eval cases for complex/high-impact skills
├── scripts/              # Deterministic CLI tools the skill invokes
├── agents/               # Subagent prompts used only by this skill
├── references/           # Deep context loaded on demand
└── assets/               # Templates, viewers, static files
```

**Maintenance artifacts** -- For Complex skills, security-sensitive skills,
router-facing skills, PR/release workflows, and skills likely to be iterated over
time, create `SPEC.md` and `EVAL.md` alongside SKILL.md:

- `SPEC.md`: purpose, scope, non-goals, invariants, dependencies, and success
  criteria. It is the contract maintainers use when changing the skill.
- `EVAL.md`: representative prompts/cases, expected routing or behavior,
  known failure modes, and pass/fail checks. It is the regression suite for
  skill behavior.

Do not create `SOURCES.md` as a standard artifact. Provenance belongs in docs,
ADRs, citations, or research files when it matters. If the LLM does not need the
file to execute, evaluate, or maintain the component, keep it out of the
component directory.

Maintenance artifacts are not runtime context. SKILL.md should not instruct the
model to load `SPEC.md` or `EVAL.md` during ordinary execution. Load them only
when creating, evaluating, redesigning, or modifying the skill.

**Frontmatter** -- name, description, routing metadata. Description caps: 60 chars max for non-invocable skills, 120 chars for user-invocable. No "Use when:", "Use for:", or "Example:" in the description. The `/do` router has its own routing tables.

**`user_invocable` default is `false`.** New skills are agent-facing by default:
the `/do` router dispatches them, and the user never types the skill name. Emit
the frontmatter field explicitly so the default is visible:

```yaml
user_invocable: false  # default -- router-dispatched, not user-typed
```

Flipping to `true` requires an explicit justification comment in the
frontmatter naming the user-facing trigger phrases and why routing through
`/do` is insufficient. Example:

```yaml
user_invocable: true  # justification: users type "/pr-workflow" directly as
                      # a slash-command entry point; /do dispatch is bypassed
                      # because the user is already scoped to the PR lifecycle.
```

No justification = leave it `false`. User-invocable expands the system-prompt
surface and the slash-command namespace; both are scarce.

**`force_route` -- when to set `true`.** Adds `force_bonus = 2.0` to the router
match score (see `force_bonus` in `scripts/pre-route.py`). Without it, single-trigger skills cap
at "low" confidence and may not route at all -- the bug PR #663 fixed for
`agent-creator`. Confidence ladder: `force_route + 2+ triggers` = high;
`force_route + 1 trigger` = medium; `3+ triggers without force` = medium;
otherwise low.

Set `force_route: true` when the skill matches one of these patterns:

| Pattern | Examples |
|---------|----------|
| Umbrella / lifecycle (one trigger phrase = one phase) | `planning`, `feature-lifecycle`, `pr-workflow` |
| Setup or installation (user states explicit intent) | `install`, `fish-shell-config` |
| Framework scaffolding (no semantic ambiguity) | `agent-creator` |
| Deterministic methodology tools (user names the tool) | `quick`, `python-quality-gate`, `go-patterns` |
| Trace/diagnostic queries (verb + noun is unambiguous) | `explanation-traces` |

Leave `force_route` off and earn confidence through trigger count when the skill matches one of these patterns:

| Pattern | Why earn confidence via trigger count |
|---------|----------------------------------------|
| Domain task skills with overlapping triggers ("review", "debug", "refactor") | Generic verbs route accurately across domains when paired with domain-specific siblings |
| Single trigger that could mean different things ("fix") | Adding companion triggers disambiguates intent |
| Skills sharing trigger phrases with siblings | Trigger-count tiebreak picks the best match cleanly |

Rule of thumb: if a future contributor reading the trigger list could reasonably
ask "did the user mean *this* or *that*?", leave `force_route` off and rely on
multiple triggers for confidence.

> See `references/skill-template.md` for the complete frontmatter template with all fields and valid values.

**Frontmatter validation (mandatory post-write gate):** After writing SKILL.md,
validate YAML frontmatter:

```bash
python3 scripts/validate-skill-frontmatter.py skills/<skill-name>/SKILL.md
```

Scaffold is not complete until this exits 0. The validator catches: broken YAML,
name/directory mismatch, missing routing section, missing triggers, missing
category, top-level `pairs_with`, and `force_routing` typo.

The description is the primary triggering mechanism. Claude tends to undertrigger skills -- be explicit about trigger contexts. Include "Use for" with concrete phrases users would say.

**Body** -- workflow first, then context:

1. Brief overview (2-3 sentences: what this does and how)
2. Instructions / workflow phases (the actual methodology)
3. Reference material (commands, guides, schemas)
4. Error handling (cause/solution pairs for common failures)
5. References to bundled files

Constraints belong inline within the workflow step where they apply. Explain the reasoning behind constraints -- "Run with `-race` because race conditions are silent until production" generalizes; "ALWAYS run with -race" does not.

**Do-pair validation** -- After writing any failure-mode blocks, run:
```bash
python3 scripts/validate-references.py --check-do-framing
```
Every failure-mode block must have a paired "Do instead" counterpart. Blocks
without one fail the check. If a prohibition genuinely has no correct alternative,
annotate it with `<!-- no-pair-required: reason -->` to pass validation without
a "Do instead" block. Ship the skill only after this check exits 0.

**Triple-validation verdicts on documented patterns** -- When the skill
documents patterns the model is supposed to apply (mental models, heuristics,
phrase fingerprints, voice traits, code conventions), every pattern block
carries an explicit verdict from the triple-validation rubric: **KEEP**,
**FOOTNOTE**, or **DROP**. KEEP and FOOTNOTE patterns ship in the SKILL.md;
DROP patterns stay in working notes (`pattern-candidates.md` or equivalent)
and never reach the published file.

The rubric (recurrence, generative power, exclusivity) lives at
`skills/content/create-voice/references/extraction-validation.md`. Load it on demand
when running the gate; do not duplicate the content here.

Three accepted verdict markers, in priority order:

1. A line in the pattern's body containing `**Verdict**: KEEP` /
   `**Verdict**: FOOTNOTE` / `**Verdict**: DROP`.
2. An inline tag at the end of the H3 heading: `### M1: Mechanism-first (KEEP)`.
3. A blanket tag on the parent H2 heading covering every child:
   `## Mental Models (KEEP-verdict)`. Per-block markers override the blanket.

For each KEEP or FOOTNOTE pattern, attach one line of evidence covering the
three checks ("appears in X and Y; predicts Z; distinguishes from peer W").
Patterns without that evidence fail the gate even if they carry a verdict
word -- the verdict is a claim, the evidence is what makes it auditable.

**Phase gate (before shipping):** every documented pattern carries a KEEP or
FOOTNOTE verdict with one-line evidence covering the three checks. Patterns
without verdicts fail the gate. The deterministic check below enforces the
verdict half; the evidence half is read by reviewers.

```bash
python3 scripts/check-skill-verdicts.py skills/<your-skill>/SKILL.md
```

The script walks H3 sections under H2 parents named Mental Models, Heuristics,
Phrase Fingerprints, or Patterns (case-insensitive substring match) and exits
non-zero on any block lacking a KEEP or FOOTNOTE verdict, or carrying DROP.
Wire it into the post-scaffold gate alongside `validate-references.py`. Skills
that document no patterns (pure workflow skills) exit 0 trivially -- the gate
only fires when there are patterns to verdict.

**Progressive disclosure** -- SKILL.md is the routing target, not the reference
library. It stays lean so it loads fast when Claude considers invoking it, then
reads `references/` on demand as phases execute. See
`references/progressive-disclosure.md` for the full model, economics, and
extraction decision tree.

Key rules:
- SKILL.md: brief overview, phase structure with gates, one-line pointers to
  reference files, error handling
- `references/`: checklists, rubrics, agent dispatch prompts, report templates,
  pattern catalogs, example collections -- anything only needed at execution time
- If SKILL.md exceeds **500 lines** after writing, extract detailed content to
  `references/` before proceeding
- If SKILL.md exceeds **700 lines**, extraction is mandatory -- it is carrying
  reference content that should not be loaded on every routing decision

The most effective complex skills (`sapcc-review`, `voice-writer`) keep SKILL.md under 600 lines and put operational depth in `references/` and `agents/`. Rich `references/` content adds depth at zero routing cost; deterministic `scripts/` ensure consistency; bundled `agents/` prompts enable specialized dispatch without routing overhead.

> See `references/progressive-disclosure.md` for the real numbers and extraction decision tree.

### Bundled scripts

Extract deterministic, repeatable operations into `scripts/*.py` CLI tools with
argparse interfaces. Scripts save tokens (the model doesn't reinvent the wheel
each invocation), ensure consistency across runs, and can be tested independently.

Pattern: `scripts/` for deterministic ops, SKILL.md for LLM-orchestrated workflow.

### Bundled agents

For skills that spawn subagents with specialized roles, bundle agent prompts in
`agents/`. These are not registered in the routing system -- they are internal to
the skill's workflow.

| Scenario | Approach |
|----------|----------|
| Agent used only by this skill | Bundle in `agents/` |
| Agent shared across skills | Keep in repo `agents/` directory |
| Agent needs routing metadata | Keep in repo `agents/` directory |

### Agent creation standard

When this skill scaffolds a repo-level agent, read `docs/PHILOSOPHY.md` first.
The philosophy governs how agents carry knowledge (not thin wrappers), how review
knowledge separates from implementation knowledge, and how references are
organized for progressive disclosure. An agent built without reading the
philosophy will misplace domain knowledge or violate structural conventions.

Apply the same maintenance-artifact rule to the agent package:

```
agents/
├── {agent-name}.md
└── {agent-name}/
    ├── SPEC.md            # Optional -- contract for complex/high-impact agents
    ├── EVAL.md            # Optional -- repeatable eval cases
    └── references/
        └── ...
```

Use `SPEC.md` and `EVAL.md` for agents that are complex, high-impact,
security-sensitive, router-facing, or likely to be tuned repeatedly. Do not
create `SOURCES.md` as a default agent artifact.

### Path placeholder convention (per ADR-201)

Author-machine paths leak into reference docs as casually as paste-from-shell-history. They look like stable interfaces ("see `/tmp/foo/` for the canonical layout") but they exist on the author's box only. A user who follows the doc literally arrives at a path that does not exist — or, worse, finds an unrelated `/tmp/foo/` from someone else's tooling.

Any path appearing in a published reference doc that matches one of the following MUST be either an angle-bracket placeholder OR a path explicitly labelled as the author's local validation harness:

- `/tmp/...`
- `/home/<author>/...`
- `~/<author-specific>/...` (anything with a user-name segment)
- `/Users/<author>/...` (macOS user dir)
- `/private/var/folders/...` (macOS tmp dir)

**Form (a) — placeholder (preferred):**

```markdown
Place outputs at `<your-output-dir>/assets/<slug>/final.png`.
```

**Form (b) — labelled author-harness (only when the path has documentary value as a worked example):**

```markdown
> **Author's local validation harness, replace before use:** `/tmp/sprite-demo/...`
```

Form (b) is allowed only when the path is referenced for evidence (e.g. "in our test run we observed X at /tmp/sprite-demo/foo.png"). Form (a) is preferred everywhere else.

**Integration-target paths stay as-is.** When a skill explicitly knows about a target project — `~/road-to-aew`, `~/deeproute` — those references stay literal. The skill's frontmatter and body explain that the skill targets that project; the path is part of the integration contract, not a leak.

**Authoring-time enforcement.** Before declaring a skill shippable, run the toolkit-wide audit grep. Any non-empty result is a violation requiring placeholder replacement:

```bash
grep -rnE '(/tmp/[a-z][a-z0-9_-]+|/home/[a-z][a-z0-9_-]+|/Users/[a-z][a-z0-9_-]+)' \
  skills/<your-skill>/SKILL.md skills/<your-skill>/references/*.md 2>/dev/null \
  | grep -v '<your-' \
  | grep -v "Author's local validation harness"
```

The validation pass invoked at the post-scaffold gate (next section) includes this grep. New skills do not ship with leaked author paths.

### Post-scaffold: regenerate skills INDEX.json (mandatory)

After the skill directory + SKILL.md are on disk, regenerate the skills index.
Without this step the router cannot discover the new skill and requests that
should match it fall through to the fallback handler.

```bash
python3 scripts/generate-skill-index.py
```

Run it from the repo root. Treat it as a commit-gating step: the scaffold is
not complete until INDEX.json reflects the new skill. Diff the file before
staging to confirm exactly one new entry was added.

### Post-scaffold: content-cleanliness audit

Audit the SKILL.md for non-runtime content (meta-commentary, changelog prose,
narration the runtime never reads). The audit globs `<root>/*/SKILL.md`, so
point `--root` at the new skill's category directory to scan it:

```bash
python3 scripts/audit-skill-content.py --root skills/<category> --severity high
```

Exit 0 with zero high-severity violations is the gate. Drop to `--severity low`
to see every flagged line. This catches content that bloats the skill without
serving the runtime — distinct from condense (prose density) and joy-check (framing).

### Post-scaffold: joy-check + do-pair validation

Before declaring the skill shippable, run both checks. They catch different
failure modes: joy-check catches grievance-mode framing that drags the model
toward pessimism; do-pair validation catches failure modes with no paired
"Do instead" counterpart.

**Joy-check** (framing). Invoke the `joy-check` skill on the SKILL.md and each
`references/*.md` file. The accepted deterministic substitute is:

```bash
python3 scripts/validate-references.py --check-do-framing
```

This script enforces the positive-pairing rule that joy-check encodes
structurally: every failure mode gets a constructive counterpart. Use it when
dispatching the full `joy-check` skill is disproportionate (small edits,
CI contexts, or when only structural pairing matters). For any new skill that
ships prose-heavy references, prefer the full `joy-check` skill -- tone drift
is not caught by the pairing script.

**Do-pair validation** (structural). Same command, different failure class.
Ship the skill only after this exits 0:

```bash
python3 scripts/validate-references.py --check-do-framing
```

### Post-scaffold: condense

After creation and validation, run the `condense` skill on the new SKILL.md to
maximize information density. The condense skill strips prose filler while
preserving every instruction, rule, gate, and code block — because new skills
tend to ship verbose and the condense pass catches what the author's eye skips.

---

## Testing the skill

This is the core of the eval loop. Do not stop after writing -- test the skill
against real prompts and measure whether it actually helps.

### Create test prompts

Write 2-3 realistic test prompts -- the kind of thing a real user would say. Rich,
detailed, specific. Not abstract one-liners.

Bad: `"Format this data"`
Good: `"I have a CSV in ~/downloads/q4-sales.csv with revenue in column C and costs
in column D. Add a profit margin percentage column and highlight rows where margin
is below 10%."`

Share prompts with the user for review before running them.

> See `references/bundled-components.md` for the evals.json format and workspace directory layout.

### Run test prompts

For each test case, spawn two subagents in the same turn -- one with the skill
loaded, one without (baseline). Launch everything at once so it finishes together.

**With-skill run:** Tell the subagent to read the skill's SKILL.md first, then
execute the task. Save outputs to the workspace.

**Baseline run:** Same prompt, no skill loaded. Save to a separate directory.

### Evaluate results

Evaluation has three tiers, applied in order:

**Tier 1: Deterministic checks** -- run automatically where applicable:
- Does the code compile? (`go build`, `tsc --noEmit`, `python -m py_compile`)
- Do tests pass? (`go test -race`, `pytest`, `vitest`)
- Does the linter pass? (`go vet`, `ruff`, `biome`)

**Tier 2: Agent blind review** -- dispatch using `agents/comparator.md`:
- Comparator receives both outputs labeled "Output 1" / "Output 2"
- It does NOT know which is the skill version
- Scores on relevant dimensions, picks a winner with reasoning
- Save results to `blind_comparison.json`

**Tier 3: Human review (optional)** -- generate the comparison viewer:
```bash
python3 scripts/eval_compare.py path/to/workspace
open path/to/workspace/compare_report.html
```

The viewer shows outputs side by side with blind labels, agent review panels,
deterministic check results, winner picker, feedback textarea, and a
skip-to-results option. Human reviews are optional -- agent reviews are sufficient
for iteration.

### Draft assertions

While test runs are in progress, draft quantitative assertions for objective
criteria. Good assertions are discriminating -- they fail when the skill doesn't
help and pass when it does. Non-discriminating assertions ("file exists") provide
false confidence.

Run the grader (`agents/grader.md`) to evaluate assertions against outputs:
- PASS requires genuine substance, not surface compliance
- The grader also critiques the assertions themselves -- flagging ones that would
  pass regardless of skill quality

Aggregate results with `scripts/aggregate_benchmark.py` to get pass rates,
timing, and token usage with mean/stddev across runs.

---

## Improving the skill

This is the iterative heart of the process.

**Generalize from feedback.** If a fix only helps the test case but wouldn't generalize, it's overfitting. Try different approaches rather than fiddly adjustments.

**Keep instructions lean.** Read execution transcripts, not just final outputs. Remove instructions that cause the model to waste time -- they consume attention budget without producing value.

**Explain the reasoning.** Motivation-based instructions generalize better than bare imperatives. "Prefer X because Y" lets the model apply the principle to situations the skill author didn't anticipate.

**Extract repeated work.** If all subagents independently wrote similar helper scripts, bundle that script in `scripts/`. One shared implementation beats N independent reinventions.

### The iteration loop

1. Apply improvements to the skill
2. Rerun all test cases into `iteration-<N+1>/`, including baselines
3. Generate the comparison viewer with `--previous-workspace` pointing at the
   prior iteration
4. Review -- agent or human
5. Repeat until results plateau or the user is satisfied

Stop iterating when:
- Feedback is empty (outputs look good)
- Pass rates aren't improving between iterations
- The user says they're satisfied

---

## Description optimization

After the skill works well, optimize the description for triggering accuracy.

> See `references/bundled-components.md` for the full optimization loop: eval query format, train/test split, `optimize_description.py` usage, and overfitting guards.

---

## Enriching existing skills

Use this mode when a skill already exists but produces shallow, generic output -- it
has thin `references/`, no `scripts/`, and passes an eval by luck rather than
by containing domain knowledge that changes behavior.

Indicators this mode is appropriate:
- `references/` has fewer than 2 files, or none at all
- No `scripts/` directory
- Eval outputs look plausible but lack domain idioms, concrete examples, or
  checklists specific to the skill's domain
- The skill passes a test because the model already knows the domain, not because
  the skill contributes anything

### The enrichment loop

Six phases: AUDIT (measure current depth), RESEARCH (find gaps), ENRICH (add reference content), TEST (A/B vs baseline), EVALUATE (blind comparator), PUBLISH (branch + PR). Max 3 iterations before escalating to the user. Each retry uses a different research angle: iteration 1 = official docs, iteration 2 = common mistakes, iteration 3 = advanced patterns.

> See `references/enrichment-workflow.md` for the full phase-by-phase checklist, scoring details, retry logic, and exact commit/PR flow.

---

## Bundled agents and scripts

> See `references/bundled-components.md` for the full list of bundled agents (`grader.md`, `comparator.md`, `analyzer.md`), bundled scripts, workspace layout, and evals.json format.

---

## Reference files

- `references/progressive-disclosure.md` -- The disclosure model: economics, size
  gates, what to extract, real examples from the toolkit, script and agent patterns
- `references/skill-template.md` -- Complete SKILL.md template with all sections
- `references/artifact-schemas.md` -- JSON schemas for eval artifacts (evals.json,
  grading.json, benchmark.json, comparison.json, timing.json, metrics.json)
- `references/complexity-tiers.md` -- Skill examples by complexity tier
- `references/workflow-patterns.md` -- Reusable phase structures and gate patterns
- `references/error-catalog.md` -- Common skill creation errors with solutions
- `references/enrichment-workflow.md` -- Deep reference for the enrichment loop:
  AUDIT checklist, RESEARCH strategy, ENRICH structuring, TEST/EVALUATE/PUBLISH phases,
  and retry logic in detail
- `references/domain-research-targets.md` -- Lookup table: given a skill's domain,
  which primary sources, secondary sources, and extraction targets to use during RESEARCH
- `references/bundled-components.md` -- Bundled agents, scripts, workspace layout,
  evals.json format, and description optimization procedure

---

## Error handling

### Skill doesn't trigger when it should
Cause: Description is too vague or missing trigger phrases
Solution: Add explicit "Use for" phrases matching what users actually say.
Test with `scripts/optimize_description.py`.

### Test run produces empty output
Cause: The `claude -p` subprocess didn't load the skill, or the skill path is wrong
Solution: Verify the skill directory contains SKILL.md (exact case). Check
the `--skill-path` argument points to the directory, not the file.

### Grading results show all-pass regardless of skill
Cause: Assertions are non-discriminating (e.g., "file exists")
Solution: Write assertions that test behavior, not structure. The grader's
eval critique section flags these -- read it.

### Iteration loop doesn't converge
Cause: Changes are overfitting to test cases rather than improving the skill
Solution: Expand the test set with more diverse prompts. Focus improvements
on understanding WHY outputs differ, not on patching specific failures.

### Description optimization overfits to train set
Cause: Test set is too small or train/test queries are too similar
Solution: Ensure should-trigger and should-not-trigger queries are realistic
near-misses, not obviously different. The 60/40 split guards against this,
but only if the queries are well-designed.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| fixing skill design issues: descriptions, gates, file size, retries | `preferred-patterns.md` | Loads detailed guidance from `preferred-patterns.md`. |
| reading or writing eval pipeline JSON artifacts | `artifact-schemas.md` | Loads detailed guidance from `artifact-schemas.md`. |
| bundling agents or scripts inside the skill package | `bundled-components.md` | Loads detailed guidance from `bundled-components.md`. |
| choosing the skill's complexity tier and line budget | `complexity-tiers.md` | Loads detailed guidance from `complexity-tiers.md`. |
| RESEARCH phase: documentation sources to mine per skill domain | `domain-research-targets.md` | Loads detailed guidance from `domain-research-targets.md`. |
| enriching an existing skill: AUDIT through PUBLISH loop | `enrichment-workflow.md` | Loads detailed guidance from `enrichment-workflow.md`. |
| errors | `error-catalog.md` | Loads detailed guidance from `error-catalog.md`. |
| splitting content between SKILL.md and references/ | `progressive-disclosure.md` | Loads detailed guidance from `progressive-disclosure.md`. |
| drafting the SKILL.md skeleton with required sections | `skill-template.md` | Loads detailed guidance from `skill-template.md`. |
| choosing a phase structure: sequential, multi-service, iterative, eval-driven | `workflow-patterns.md` | Loads detailed guidance from `workflow-patterns.md`. |
