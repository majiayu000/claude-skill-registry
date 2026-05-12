---
name: review-health
description: First-pass strategic-orientation review of a repository. Produces an evidence-cited map (not a grade) calibrated to a reference class, helping the user decide where to engage, where to tread carefully, and where to leave alone. Advisory only — no changes made.
model: opus
---

# Review-Health — Strategic Orientation for a Repository

A first-pass review skill for the moment you want to step back and assess a repo strategically: you've just inherited it, you're evaluating a FOSS project for adoption, you're onboarding a teammate, or you're revisiting your own project to decide where to invest. The skill produces an evidence-cited map of the repo's state — not a grade. Its output is built to inform strategic decisions about engagement, not to itemize every imperfection.

**This skill is advisory only. It makes no changes.** To act on findings, hand off to `/refactor`, `/review-arch`, `/review-test`, `/review-security`, or other specialists as the findings indicate.

## Philosophy

**Observation before interpretation.** The skill's procedure enforces an OODA cadence — Observe, Orient, Decide, Act — with strict phase gates. The Observe phase collects signals without verdicts. Only after observation is complete does interpretation begin. This is the structural countermeasure to the most common failure mode of informal code review: fixating on the first file opened and building a distorted mental model from there.

**"Good" is relational, not absolute.** A 34% test-coverage finding is a different finding in a research prototype than in an OSS library with external consumers. The skill's calibration is anchored in **reference classes** (`references/classes/`): the repo is classified into a class first, and each dimension is evaluated against class-specific expectations. Classification is a cited, overridable output — the user sees which class was applied and can correct it in one line. Every downstream finding reflows against the correct class.

**Every claim carries evidence.** A finding without a `file:line` citation or a tool-output reference is not a finding; it is an assertion and must be dropped or demoted to the Coverage Manifest. This is enforced structurally (the phase-integrity check in §Evidence Discipline), not stylistically.

**Named unknowns beat silent unknowns.** The Coverage Manifest is first-class output. Tools that weren't available, signals that couldn't be computed, and questions that couldn't be answered are named explicitly with the reasons they couldn't be resolved. A honest "we couldn't assess X" beats a confident assessment that silently excluded X.

**Breadth first. Compose, don't reinvent.** This skill is the wide-and-shallow pass. When a finding warrants a deep-and-narrow follow-up, the skill routes to a sibling specialist (`/review-arch`, `/refactor`, `/review-test`, `/review-security`, etc.) with a scoped argument. The skill does its own work at breadth level; it defers to siblings only when a sibling is an exact fit for what needs doing.

## Cognitive Failure Modes This Skill Countermands

New-repo orientation has a small set of predictable cognitive failures. The skill's procedure is designed to counter each:

- **Inheritor's paralysis + availability bias** — fixating on the first file opened, building a distorted mental model from a non-representative sample. *Countermeasure: systematic Observe phase that enumerates signals from fixed collection points before any interpretation.*
- **Unknown-unknowns dominance** — not knowing what you don't know about the repo. *Countermeasure: Coverage Manifest elevates missing tooling and un-assessed dimensions to first-class output.*
- **Premature closure** — committing to a verdict before evidence is complete. *Countermeasure: phase-integrity gates — Orient cannot cite anything not captured in Observe; Decide cannot cite anything not captured in Orient.*
- **Expert deference** — accepting prior-author choices without questioning. *Countermeasure: differential-diagnosis classification forces candidate alternatives to be considered with evidence for and against each.*
- **Free-floating adjectives** — "health: good" with no reference point. *Countermeasure: reference-class calibration with cited per-class rubrics.*

The practitioner traditions this skill draws from — OODA (Boyd), medical differential diagnosis, home inspection (ASHI severity tiers), marine surveying (reference-class calibration), technical due diligence (M&A), intelligence situational-awareness briefings — are all codifications of these countermeasures in domains that have had to solve "rapid assessment of unfamiliar systems under uncertainty" at higher stakes than software review.

## Workflow Overview

```
┌────────────────────────────────────────────────────────────────┐
│                      REVIEW-HEALTH                             │
├────────────────────────────────────────────────────────────────┤
│  Phase 0 — Preflight                                           │
│    • Elicit lens (what's the user doing?)                      │
│    • Determine scope (whole repo / directory / module)         │
│                                                                │
│  Phase 1 — OBSERVE (no interpretation allowed)                 │
│    • Repo enumeration (size, structure, entry points)          │
│    • Git-history signals (cadence, churn, bus factor)          │
│    • Tooling signals (lint, coverage, CI, deps, secrets)       │
│    • Documentation signals (README, inline, architectural)     │
│    • Coverage Manifest: what couldn't be collected and why     │
│                                                                │
│  Phase 2 — ORIENT (classification + rubric application)        │
│    • Differential diagnosis → reference class (cited)          │
│    • Apply class rubric to each dimension                      │
│    • Severity-tier individual findings                         │
│    • Cross-cutting synthesis                                   │
│                                                                │
│  Phase 3 — DECIDE (strategic options for the user's lens)      │
│    • Generate 2-4 engagement options                           │
│    • Each option cites Orient findings                         │
│                                                                │
│  Phase 4 — ACT (concrete next steps)                           │
│    • Top 3-5 recommendations                                   │
│    • Sibling-skill routing with scoped arguments               │
└────────────────────────────────────────────────────────────────┘
```

## Workflow Details

### Phase 0 — Preflight

**Elicit the lens.** Ask the user one question:

> What's the context for this review?
> 1. Inheriting a work repository — taking over maintenance or ownership
> 2. Evaluating a FOSS project — for adoption, contribution, or dependency
> 3. Revisiting my own repo — strategic overview of current state
> 4. Onboarding a teammate — generating a map for someone else
> 5. Other — briefly describe

Default: ask; do not guess from context. The lens is a load-bearing input — it shapes the Decide phase's option generation and informs classification.

**Determine scope.** Default: the whole repo. If the user specifies a directory or module, honor that scope in all phases. If the repo is unusually large (>100k LOC or >10 top-level subsystems), ask whether to scope down before running the full pass.

**Abort if:** not a git repository, or no source files in scope. Do not abort on missing tooling — that's handled by the Coverage Manifest.

### Phase 1 — OBSERVE

Collect signals. **Interpretation is not allowed in this phase.** Output language is neutral and factual — "X is present / absent / at value Y," not "X is good / concerning / inadequate." Every signal carries a citation: a `file:line` reference, a tool invocation with its output, or an explicit "could not be collected" entry.

**Signal battery (run what applies; record what doesn't):**

**Repo shape:**
- Languages present and LOC by language (use `tokei`, `scc`, `cloc`, or equivalent; fall back to file-extension counting)
- Top-level directory layout (use `tree -L 2 -d` or `ls -la`)
- Entry points (framework conventions: `main.go`, `cli.py`, `src/index.ts`, `bin/`, `cmd/`; also: manifest declarations for binaries/scripts)
- Build system and package manifests detected (`package.json`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `Gemfile`, `composer.json`, etc.)

**Git-history signals:**
- Age: first-commit and latest-commit timestamps (`git log --reverse | head -1`, `git log -1`)
- Cadence: commits per month trend (`git log --pretty=format:"%ad" --date=format:"%Y-%m"` + sort/count)
- Contributors: distinct authors in last 12 months (`git shortlog -sne --since="12 months ago"`)
- Churn concentration: files with highest commit count (`git log --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20`)
- Bus factor proxy: files with single-author commit history in core modules

**Tooling signals (best-effort; record absences):**
- Test framework: detect via manifests and directory presence (`tests/`, `*_test.go`, `spec/`)
- Test-to-code LOC ratio
- Coverage: if a coverage report is present (`.coverage`, `coverage.xml`, `lcov.info`), parse it; if not, note absence
- Lint/static-analysis config: `.eslintrc`, `.golangci.yml`, `pyproject.toml [tool.ruff]`, etc.
- CI configuration: `.github/workflows/`, `.gitea/workflows/`, `.gitlab-ci.yml`, `.circleci/`, `Jenkinsfile`, etc.
- Dependency audit: run `npm audit`, `pip-audit`, `bundle audit`, `cargo audit`, `govulncheck`, or equivalent if available; record output summary
- Dependency staleness: `npm outdated`, `pip list --outdated`, `go list -u -m all`, or equivalent
- Secrets scan: look for committed credentials (`.env` tracked in git, `API_KEY=` in source, private-key headers in files)

**Documentation signals:**
- Top-level README presence and length
- Inline documentation density (comment-to-code ratio in core modules, sampled)
- Architectural documentation (`docs/`, `ARCHITECTURE.md`, ADR directories)
- CHANGELOG presence and recency
- Contributing guide, code of conduct, issue/PR templates

**Coverage Manifest entries.** For every tool that couldn't run, signal that couldn't be computed, or area that couldn't be assessed, record:
- What was attempted
- Why it didn't yield data (tool not available, no network access, no test infrastructure, signal undefined for this repo type, etc.)
- Whether the user might want to provide input (e.g., "run with a test database available and re-invoke")

**Output of Phase 1:** a structured Observation Record with numbered entries (`O1`, `O2`, ...) or equivalent referenceable IDs. Every Orient finding will cite these IDs.

### Phase 2 — ORIENT

Interpret signals. This is where findings are produced.

**Step 2a: Classify the repo (differential diagnosis).**

Load the class definitions from `references/classes/`. For each candidate class, gather confirming and disconfirming evidence from the Observation Record and the user's stated lens:

> **Candidate: `production-service`**
> For: `O12` (Dockerfile present with runtime target), `O17` (CI workflow gates merges), `O8` (>5 contributors in last 12 months)
> Against: `O4` (no deployment artifacts, no on-call docs)
> Confidence: Low

Rank candidates by weight of evidence. Pick the best-fit class. Hedge explicitly:

> **Classified as: `solo-utility`** (medium confidence)
> Reason: small contributor count, no deployment infrastructure, no external-consumer signals. Override if you consider this repo to be a different class.

For hybrid repos, apply multiple class rubrics to the dimensions where they differ and flag the hybrid explicitly. (Example: a CLI tool that's also a published library gets `solo-utility` for its command surface and `oss-library` for its public API.)

**Step 2b: Load the class rubric.**

Read the matched class file under `references/classes/<class-name>.md`. The rubric defines five dimensions (test health, dependency health, CI/automation health, documentation, architecture hygiene) with three levels each (Foundational / Adequate / Strong) and per-level criteria.

**Step 2c: Apply the rubric to each dimension.**

For each dimension, place the repo at Foundational / Adequate / Strong with cited evidence from the Observation Record:

> **Test Health: Adequate**
> Criteria met: `O22` shows test-to-code ratio of 0.34 (above 0.15 threshold for Adequate); `O23` confirms tests cover all three primary CLI commands. Strong would require `O24`'s coverage report to show ≥60% for core modules (observed: 45%), plus a matrix against supported runtime versions.
> Gap to Strong: coverage below threshold in `src/parser/` and `src/validators/`; no runtime-version matrix in CI.

**Step 2d: Severity-tier individual findings.**

Within each dimension's assessment, individual notable findings get ASHI severity tiers (see `references/severity-tiers.md`): Safety Hazard / Major / Minor / Cosmetic. Severity is intrinsic to the finding, independent of class. Lead with Safety, then Major. Minor is reported concisely; Cosmetic is aggregated or omitted unless requested.

**Step 2e: Cross-cutting synthesis.**

Look across dimensions and modules for patterns no single dimension would reveal:
- Divergent conventions at module boundaries (different error-handling or logging between `src/api/` and `src/workers/`)
- Type duplication (models defined in multiple places)
- Dependency inconsistency across sub-packages
- Auth or configuration model divergence between client and server code
- Documentation drift (README claims X; code implements Y)

Cross-cutting findings are often the highest-leverage observations in the whole review. They're the ones per-dimension or per-language reviewers miss structurally.

**Step 2f: Coverage Manifest.**

Carry forward the Phase 1 Coverage Manifest entries, and add any new ones surfaced during interpretation. Name what the skill couldn't assess. This section is not a caveat; it is first-class output.

**Phase 2 integrity check:** every Orient claim must cite one or more Observation Record IDs. Any claim that cannot be cited is dropped, demoted to Coverage Manifest, or explicitly flagged as "interpretation — no direct evidence."

### Phase 3 — DECIDE

Generate strategic options for the user's lens. For each option, state what it entails and what findings from Orient support or complicate it.

**Lens-specific option patterns:**

*Inheriting a work repository:*
- "Adopt as-is with compensating controls" — what controls would mitigate the standing risks
- "Invest in remediation before extending" — which Major findings to address first, estimated scope
- "Carve out a subset" — is there a safe module to work in while the rest is addressed

*Evaluating a FOSS project:*
- "Adopt" — proceed; state the accepted risks
- "Adopt with wrappers or pinning" — what buffering would be needed
- "Don't adopt" — what disqualifying findings made the call
- "Fork and stabilize" — when the project is valuable but under-maintained

*Revisiting my own repo:*
- "Continue current trajectory" — findings align with intent
- "Rebalance investment" — which dimensions warrant more attention given the class
- "Promote class" — findings suggest the repo has outgrown its current class; move to a higher-standards class

*Onboarding a teammate:*
- "Start in module X" — safest region for initial contribution
- "Read docs in this order" — prioritized reading list
- "Known hazards to brief on" — things the newcomer should hear before encountering

Each option cites Orient finding IDs. The user picks; the skill does not pick for them.

**Phase 3 integrity check:** every option's supporting rationale must cite Orient findings by ID.

### Phase 4 — ACT

Produce a concrete next-step queue: top 3-5 recommendations, prioritized by severity × lens-relevance. Each recommendation is either:

- A specific action the user takes (with file:line pointers)
- A sibling-skill invocation with scoped arguments

**Sibling-skill routing pattern:**

> Architecture concerns concentrated in `services/billing/`:
> Run `/review-arch services/billing/` for a deep structural read.

> Test gaps in `src/parser/` and `src/validators/`:
> Run `/review-test src/parser/ src/validators/` for coverage-gap analysis.

> Dependency audit surfaced high-severity CVEs:
> Run `/review-security` with focus on direct and transitive dependencies.

Route to a sibling skill *only* when the sibling does exactly what needs to be done at the depth warranted. If the finding needs shallow follow-up, recommend the action directly rather than routing.

## Evidence Discipline

The skill's credibility is load-bearing. These rules are structural, not stylistic:

**Every claim cites evidence.** Findings in Orient, Decide, and Act cite either an Observation Record ID (preferred) or a direct `file:line` / tool-output reference. A claim without evidence is dropped or moved to Coverage Manifest.

**Phase integrity.** Orient claims cite Observe. Decide options cite Orient. Act recommendations cite Orient or Decide. A claim in a later phase that cannot cite an earlier phase's finding is a violation and must be re-examined.

**Self-check before delivery.** Before presenting results, scan for: uncited adjectives, claims phrased as "the author should..." without a cited basis, any verdict word in the Observe section. Remove or re-cite.

**Coverage Manifest is not a weakness.** Named unknowns are strictly better than silent unknowns. "We couldn't assess X because Y" is informative; confident-sounding output that silently omitted X is not.

## Agent Coordination

The skill is primarily executed by the main Claude instance — OODA cadence is inherently sequential and benefits from synthesis within a single context. Subagents are used narrowly:

- **Observe-phase scouts (optional, parallelizable):** for large repos, parallel subagents can be dispatched to run discrete signal-collection tasks (git-history analysis, dep-audit, lint-run, complexity-scan). Each returns structured signals, not prose. Use only when Observe-phase signal gathering is heavy enough to benefit from parallelism.
- **SME consultation (optional, narrow):** if a single dimension requires specialized knowledge the main instance lacks (e.g., idiom-correctness in Zig, or GraphQL schema coherence), a language/domain SME may be consulted for that dimension only. The SME returns a rubric-placement with evidence; it does not write prose summary.

Do not routinely spawn per-language SMEs. That is the prior failure mode this redesign corrects.

## Sibling-Skill Composition

`/review-health` is allowed and encouraged to recommend sibling skills. It does not normally invoke them itself — recommendations are for the user.

 | Finding type                               | Sibling skill      | When to route                                                          |
 | ------------------------------------------ | ------------------ | ---------------------------------------------------------------------- |
 | Architectural coupling / module boundaries | `/review-arch`     | Architecture hygiene at Foundational + cross-cutting coupling findings |
 | Tactical cleanup (DRY, naming, dead code)  | `/refactor`        | Multiple Minor findings in a single module                             |
 | Test coverage or test quality gaps         | `/review-test`     | Test health at Foundational, or specific coverage gaps                 |
 | Security findings (CVEs, secrets, auth)    | `/review-security` | Safety-tier findings involving security                                |
 | Performance hotspots                       | `/review-perf`     | Observations of perf-sensitive code without benchmarks                 |
 | Accessibility (for web projects)           | `/review-a11y`     | Documentation findings for web UI code                                 |
 | Documentation gaps                         | `/tidy-docs`      | Documentation at Foundational                                          |
 | Pre-release readiness                      | `/review-release`  | When the user is preparing to publish/deploy                           |

Route with a scoped argument when possible: `/review-arch services/billing/` is more useful than `/review-arch`.

## Output Format

**Inline by default.** Present the report as structured markdown in the conversation. The user can save it manually if desired.

**Output structure (present in this order):**

1. **Context** — lens, scope, classification (with evidence and override instruction)
2. **Observation Record** — the factual Phase 1 signals, grouped by category, ID-referenced
3. **Findings (Orient)** — per-dimension rubric placement with cited evidence; severity-tiered findings within; cross-cutting synthesis
4. **Coverage Manifest** — what couldn't be assessed, with reasons
5. **Strategic Options (Decide)** — lens-specific options with supporting findings
6. **Next Steps (Act)** — top 3-5 recommendations; sibling-skill routing with scoped arguments

Keep the Observation Record compact and scannable (tables where appropriate; not prose paragraphs). The Findings section is the primary narrative. Recommendations are bulleted and concrete.

## Abort Conditions

**Abort:**
- Not a git repository
- No source files detected in scope

**Do NOT abort:**
- Specific tools unavailable (record in Coverage Manifest, continue best-effort)
- A classification candidate is unclear (apply multi-class, flag hybrid)
- A dimension can't be rated at all (record as "Un-assessed" in Coverage Manifest)

## What This Skill Is Not

- **Not a code-quality linter.** Line-by-line defects are out of scope. Hand off to `/refactor` or `/review-arch`.
- **Not a security audit.** Safety findings are surfaced, but thorough security review is `/review-security`.
- **Not a performance analysis.** Perf hotspots are noted as signals; actual profiling is `/review-perf`.
- **Not a grade.** There is no overall "health score." The skill produces a map, not a scalar.
- **Not a substitute for reading the code.** The user will still need to engage with the repo. The skill helps them engage *well*.
