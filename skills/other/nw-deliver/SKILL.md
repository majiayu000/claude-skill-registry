---
name: nw-deliver
description: "Orchestrates the full DELIVER wave end-to-end (roadmap > execute-all > finalize). Use when all prior waves are complete and the feature is ready for implementation."
user-invocable: true
argument-hint: '[feature-description] - Example: "Implement user authentication with JWT"'
---

# NW-DELIVER: Complete DELIVER Wave Orchestrator

**Wave**: DELIVER (wave 6 of 6)|**Agent**: Main Instance (orchestrator)|**Command**: `/nw-deliver "{feature-description}"`

## Overview

Orchestrates complete DELIVER wave: feature description → production-ready code with mandatory quality gates. You (main Claude instance) coordinate by delegating to specialized agents via Task tool. Final wave (DISCOVER > DISCUSS > SPIKE > DESIGN > DEVOPS > DISTILL > DELIVER).

Sub-agents cannot use Skill tool or `/nw-*` commands. You MUST:
- Read the relevant command file and embed instructions in the Task prompt
- Remind the crafter to load its skills as needed for the task (skill files are at `~/.claude/skills/nw-{skill-name}/SKILL.md`)

## Output Tiers (per D2)

Provenance: feature `lean-wave-documentation` — D2 (schema-typed sections), D10 (one-line expansion descriptions). The DELIVER wave emits a single `feature-delta.md` whose headings are typed `[REF]` (always emitted) or `[WHY]/[HOW]` (lazy expansions). Tier-1 is the always-on baseline; Tier-2 is the lazily-rendered expansion catalog. Implementation details live in code; the wave-delta sections are pointers + structured summaries.

### Tier-1 [REF] — always emitted

Tier-1 sections constitute the lean-default baseline. Every DELIVER run emits at minimum these sections under `## Wave: DELIVER / [REF] <Section>` headings:

- Implementation summary — one-paragraph description of what shipped (no design rationale)
- Files modified — categorized list (production, tests, docs) with one-line per file
- Scenarios green count — `<N> of <M>` from the `.feature` file with timestamp
- DoD check — itemized pass/fail against the DISCUSS Definition of Done items
- Demo evidence — captured stdout/exit-code per Elevator Pitch demo command (Phase 3.5 gate)
- Quality gates — per-phase outcomes (refactor, review, mutation, integrity)
- Pre-requisites — DISTILL scenarios + DESIGN component manifest the implementation depended on

### Tier-2 EXPANSION CATALOG — lazy, on-demand (per D10)

Tier-2 items are NOT emitted by default. They are rendered only when explicitly requested via `--expand <id>` (DDD-2) or via the wave-end interactive prompt when `expansion_prompt = "ask"`. Each item has a one-line description (per D10) so the menu fits in a single render. Each emitted Tier-2 section is headed `## Wave: DELIVER / [WHY] <Section>` or `## Wave: DELIVER / [HOW] <Section>`.

| Expansion ID | Tier label | One-line description |
|---|---|---|
| `refactoring-journal` | [HOW] | L1-L6 refactoring log with rationale per micro-transformation |
| `retrospective-notes` | [WHY] | 5 Whys analysis on issues encountered, lessons learned, what to repeat/avoid |
| `performance-measurements` | [WHY] | Benchmarks, profiling output, latency/memory deltas vs baseline |
| `alternative-implementations-rejected` | [WHY] | Implementation approaches tried and rejected with one-paragraph reason each |
| `mutation-testing-report` | [HOW] | Mutmut/Pitest output: kill rate, surviving mutants, mitigation actions |
| `architecture-decision-deviations` | [WHY] | Where DELIVER deviated from DESIGN and the back-propagation logged in upstream-issues.md |
| `coverage-deltas` | [HOW] | Per-module coverage delta with rationale for any drops |
| `expansion-catalog-rationale` | [WHY] | Why this set of expansions, why these defaults, why D10 enforces one-line descriptions |

## Density resolution (per D12)

Provenance: D12 (rigor cascade), DDD-5 (density resolver shared utility). Before emitting any Tier-1 section, resolve the active documentation density:

1. **Read** `~/.nwave/global-config.json`. Treat missing/malformed config as empty dict (fall back to defaults).
2. **Call** `resolve_density(global_config)` from `scripts/shared/density_config.py`. The function returns a `Density` value object with fields `mode` (`"lean"` | `"full"`), `expansion_prompt` (`"ask"` | `"always-skip"` | `"always-expand"` | `"smart"`), and `provenance` (the cascade branch that produced this result).
3. **Branch on `density.mode`**:
   - `lean` → emit ONLY Tier-1 `[REF]` sections under `## Wave: DELIVER / [REF] <Section>` headings. Do NOT auto-render Tier-2 items.
   - `full` → emit Tier-1 `[REF]` sections PLUS all Tier-2 expansion items rendered under their `[WHY]` / `[HOW]` headings. This is auto-expansion (no menu).
4. **At wave end**, branch on `density.expansion_prompt`:
   - `"ask"` → present the expansion menu (Tier-2 catalog above with one-line descriptions per D10) and append user-selected items as `## Wave: DELIVER / [WHY|HOW] <Section>` headings.
   - `"always-skip"` → no menu, no extra sections (idempotent re-runs, CI mode).
   - `"always-expand"` → equivalent to `mode = "full"` for this run; auto-render every Tier-2 item.
   - `"smart"` → out of scope for v1 (per OQ-3); treat as `"ask"` until heuristic is empirically tuned.

The resolver itself encodes the D12 cascade: explicit `documentation.density` override > `rigor.profile` mapping (`lean`→`lean`, `standard`→`lean`+`ask`, `thorough`→`full`, `exhaustive`→`full`+all-expansions, `custom`→`lean`+`ask`) > hard default `lean`+`ask`. This skill MUST NOT replicate the cascade locally — call `resolve_density(global_config)` and trust its output.

**Section heading prefix convention (per D2)**: every emitted section starts with `## Wave: DELIVER / [REF] <Section>` for Tier-1; `## Wave: DELIVER / [WHY] <Section>` or `## Wave: DELIVER / [HOW] <Section>` for Tier-2. Validator `scripts/validation/validate_feature_delta.py` enforces the regex `^## Wave: \w+ / \[(REF|WHY|HOW)\] .+$` on every wave heading.

### Ad-hoc override — user request mid-session

Even when `density.mode = "lean"` and `density.expansion_prompt = "always-skip"`, the user may ask DURING the wave session for specific expansions:

- "expand jtbd" / "expand jtbd-narrative" / "more on jtbd"
- "add alternatives considered"
- "show migration playbook"
- "tell me why" (interpretive — append the WHY rationale section relevant to the most recent decision)
- "more on <X>" (where `<X>` is one of the expansion catalog items for this wave)

When the user makes such a request:

1. Append the corresponding `[WHY]` or `[HOW]` section to `feature-delta.md` under the current wave's heading.
2. Emit a `DocumentationDensityEvent` with `choice="expand"` and `expansion_id=<the requested item>` to `JsonlAuditLogWriter`.
3. Do NOT modify `~/.nwave/global-config.json`. The override is ONE-SHOT for this wave only.

If the user's request matches NO item in this wave's Expansion Catalog, respond with the catalog list (one-line description per item per D10) and ask for clarification — do NOT improvise an expansion outside the catalog.

## Telemetry (per D4 + DDD-6)

Provenance: D4 (telemetry schema instrumented day-one), D6 (first-install pedagogical prompt creates audit signal), DDD-6 (telemetry event class lives in DES domain, writer reused). Every expansion choice — whether the user expanded an item or skipped the menu — emits a structured event to the existing `JsonlAuditLogWriter` driven adapter.

**Event type**: `DocumentationDensityEvent` (dataclass at `src/des/domain/telemetry/documentation_density_event.py`).

**Schema fields** (per D4):

```
{
  "feature_id": "<feature-id>",
  "wave": "DELIVER",
  "expansion_id": "<id-from-catalog-or-'*'-for-skip-all>",
  "choice": "skip" | "expand",
  "timestamp": "<ISO-8601 datetime>"
}
```

**Emission pattern**:

1. Construct a `DocumentationDensityEvent(feature_id=..., wave="DELIVER", expansion_id=..., choice=..., timestamp=...)`.
2. Call `event.to_audit_event()` to convert to the open `AuditEvent` shape (`event_type="DOCUMENTATION_DENSITY"` and the schema fields nested under `data`).
3. Dispatch via `JsonlAuditLogWriter().log_event(audit_event)`.

The wave-skill harness invokes the helper `scripts/shared/telemetry.py:write_density_event(...)` which performs all three steps. This skill MUST NOT bypass the helper or write JSONL directly — every density telemetry event flows through the shared helper to keep the audit-log schema consistent.

**When to emit**:
- One event per user choice in the expansion menu when `expansion_prompt = "ask"` (`choice = "expand"` for selected items, `choice = "skip"` with `expansion_id = "*"` if the user skips the entire menu).
- One synthetic `choice = "skip"` event with `expansion_id = "*"` when `expansion_prompt = "always-skip"` (records the skipped menu opportunity).
- One `choice = "expand"` event per Tier-2 item rendered when `mode = "full"` or `expansion_prompt = "always-expand"`.

This telemetry feeds the post-deploy retrospective: a DELIVER wave that records `choice = "expand"` for `retrospective-notes` is a signal the team needed deeper learning capture; over time the data drives whether retrospective notes should be promoted to Tier-1.

## CRITICAL BOUNDARY RULES

1. **NEVER implement steps directly.** ALL implementation MUST be delegated to the selected crafter (@nw-software-crafter or @nw-functional-software-crafter per step 1.5) via Task tool with DES markers. You are ORCHESTRATOR — coordinate, not implement.
2. **NEVER write phase entries to execution-log.json.** Only the crafter subagent that performed TDD work may append entries.
3. **Extract step context from roadmap.json ONLY for Task prompt.** Grep roadmap for step_id ~50 lines context, extract (description|acceptance_criteria|files_to_modify), pass in DES template.

**DES monitoring is non-negotiable.** Circumventing DES — faking step IDs, omitting markers, or writing log entries manually — is a **violation that invalidates the delivery**. DES detects unmonitored steps and flags them; finalize **blocks** until every flagged step is re-executed through a properly instrumented Task. There is no workaround: unverified steps cannot pass integrity verification, and the delivery cannot be finalized. Without DES monitoring, nWave cannot **verify** TDD phase compliance. For non-deliver tasks (docs, research, one-off edits): `<!-- DES-ENFORCEMENT : exempt -->`.

## Rigor Profile Integration

Before dispatching any agent, read the rigor profile from `.nwave/des-config.json` (key: `rigor`). If absent, use standard defaults.

**How rigor affects deliver phases:**

| Setting | Effect |
|---------|--------|
| `agent_model` | Pass as `model` parameter to all Task tool invocations for crafter agents. If `"inherit"`, omit `model` parameter (Task tool inherits from session). |
| `reviewer_model` | Pass as `model` parameter to reviewer Task invocations. If `"skip"`, skip Phase 4 entirely. |
| `review_enabled` | If `false`, skip Phase 4 (Adversarial Review). |
| `double_review` | If `true`, run Phase 4 twice with separate review scopes. |
| `tdd_phases` | Pass to crafter in DES template. Replace `# TDD_PHASES` section with the configured phases. If only `[RED_UNIT, GREEN]`, omit PREPARE/RED_ACCEPTANCE/COMMIT instructions. |
| `refactor_pass` | If `false`, skip Phase 3 (Complete Refactoring). |
| `mutation_enabled` | If `false`, skip Phase 5 regardless of mutation strategy in CLAUDE.md. |

**Task invocation with rigor model:**
```python
Task(
    subagent_type="{agent}",
    model=rigor_agent_model,  # omit this line entirely if "inherit"
    max_turns=45,
    prompt=...,
)
```

## Prior Wave Consultation

Before beginning DELIVER work, read prior wave content. With lean v3.14, all wave decisions live in a single `feature-delta.md` (sections tagged `## Wave: <NAME> / [REF|WHY|HOW] <Section>`); legacy multi-file directories are no longer produced.

1. **DISCOVER** (skip): Synthesized into DISCUSS sections of `feature-delta.md`.
2. **DISCUSS** (read on demand): in `docs/feature/{feature-id}/feature-delta.md` under `## Wave: DISCUSS / [REF] ...` sections. Already encoded as acceptance scenarios — read for elevator pitch extraction (Phase 3.5) and clarification only.
3. **DESIGN** (structural context, MANDATORY): Read `docs/product/architecture/brief.md` (cross-feature SSOT — component boundaries, driving ports, C4 diagrams). PLUS read `docs/feature/{feature-id}/feature-delta.md` filtered to `## Wave: DESIGN / [REF] ...` sections — DDD list, component decomposition, driving/driven ports, technology choices, decisions table, reuse analysis.
4. **DEVOPS** (read on demand): in `feature-delta.md` under `## Wave: DEVOPS / [REF] ...` sections. Read only if test environment issues arise.
5. **DISTILL** (primary input, MANDATORY): TWO sources:
   - `feature-delta.md` `## Wave: DISTILL / [REF] ...` sections — scenario list with tags, walking skeleton strategy, adapter coverage, scaffold inventory, test placement, driving adapter coverage, pre-requisites
   - Executable `.feature` files at the test placement path declared in DISTILL (e.g. `tests/{feature-id-or-bounded-context}/acceptance/*.feature`) — these are the authoritative specification

**READING ENFORCEMENT**: You MUST read `feature-delta.md` (full file) AND `docs/product/architecture/brief.md` AND every `.feature` file referenced in the DISTILL Test Placement section before proceeding. After reading, output a confirmation checklist (`✓ {file}` for each read, `⊘ {file} (not found)` for missing). Do NOT skip files that exist — skipping causes implementation disconnected from architecture and acceptance tests.

**Migration fallback for legacy features**: If `docs/feature/{feature-id}/feature-delta.md` does NOT exist BUT legacy multi-file directories (`discuss/`, `design/`, `devops/`, `distill/`) DO exist, treat the legacy layout as authoritative for THIS feature only. Read all files in those directories. Future waves should consolidate to `feature-delta.md` per lean v3.14.

**Upstream issues check**: look for `## Wave: <NAME> / [WHY] Upstream Issues` sections in `feature-delta.md` (or legacy `upstream-changes.md` / `upstream-issues.md` files in legacy multi-file features). If unresolved issues exist, flag them to the user before starting implementation.

**On-demand escalation**: If during implementation a crafter encounters ambiguity not resolved by DISTILL tests or DESIGN architecture, the orchestrator re-reads specific sections of `feature-delta.md` — never re-reads the full file unnecessarily.

## Document Update (Back-Propagation)

When DELIVER implementation reveals gaps or contradictions in prior waves:
1. Document findings as a `## Wave: DELIVER / [WHY] Upstream Issues` section appended to `docs/feature/{feature-id}/feature-delta.md` (lean v3.14 — Tier-2 expansion) OR `docs/feature/{feature-id}/deliver/upstream-issues.md` (legacy multi-file)
2. Reference the original prior-wave document and describe the issue
3. If implementation requires deviating from architecture or requirements, document the deviation and rationale
4. Resolve with user before continuing past the affected step

## Orchestration Flow

At the start of execution, create these tasks using TaskCreate and follow them in order:

0. **Read Rigor Profile** — Read `.nwave/des-config.json` key `rigor`. Store: `agent_model`, `reviewer_model`, `tdd_phases`, `review_enabled`, `double_review`, `mutation_enabled`, `refactor_pass`. Use standard defaults if absent. Gate: rigor profile loaded or defaults set.

0.5. **Prior Wave Consultation** — Read `docs/feature/{feature-id}/feature-delta.md` (lean v3.14: full file with DISCUSS/DESIGN/DEVOPS/DISTILL sections) + `docs/product/architecture/brief.md` + every `.feature` file declared in the DISTILL Test Placement section. Legacy fallback: if `feature-delta.md` is missing but multi-file dirs exist, read those instead. Flag contradictions, resolve before proceeding. Summarize key design decisions into a reusable DESIGN_CONTEXT block for crafter dispatch (component structure, boundaries, tech choices, data models). Gate: all required files read, confirmation checklist output, no unresolved contradictions.

1. **Setup** — Parse input, derive `feature-id` (kebab-case), create `docs/feature/{feature-id}/deliver/`.
   - a. Create `execution-log.json` via CLI: `des-init-log --project-dir docs/feature/{feature-id}/deliver --feature-id {feature-id}`. Do NOT use Write tool directly.
   - b. Create deliver session marker: `.nwave/des/deliver-session.json`.
   - Gate: directory exists, `execution-log.json` created via CLI, session marker written.

1.5. **Detect Development Paradigm** — Read project `CLAUDE.md` (project root, NOT `~/.claude/CLAUDE.md`). Search "## Development Paradigm".
   - Found → extract paradigm: `"functional"` → `@nw-functional-software-crafter` or `"object-oriented"` → `@nw-software-crafter` (default).
   - Not found → ask user "OOP or Functional?", offer to write to `CLAUDE.md`.
   - Store selected crafter for all Phase 2 dispatches.
   - Functional → property-based testing default; `@property` tags signal PBT; example-based = fallback.
   - Gate: crafter selected and stored.

1.6. **Detect Mutation Testing Strategy** — Read same `CLAUDE.md`, search "## Mutation Testing Strategy".
   - Found → extract: `per-feature` | `nightly-delta` | `pre-release` | `disabled`.
   - Not found → default `"per-feature"`.
   - Log strategy for traceability. Note: strategy locks at deliver start; `CLAUDE.md` edits during delivery take effect next run.
   - Gate: strategy recorded.

2. **Phase 1 — Roadmap Creation + Review** — Gate: roadmap created, integrity verified, reviewer approved.
   - a. Skip if `docs/feature/{feature-id}/deliver/roadmap.json` exists with `validation.status == "approved"`. If found in `design/` instead, move to `deliver/` and log warning.
   - b. Dispatch `@nw-solution-architect` to create `roadmap.json` (load `~/.claude/skills/nw-roadmap/SKILL.md`). Step IDs MUST match `NN-NN` format (01-01, 01-02). If `distill/` exists, architect MUST populate `test_file` and `scenario_name` per step.
   - c. Run automated quality gate (see Roadmap Quality Gate section below).
   - c2. Run roadmap integrity verification (HARD GATE): `des-verify-integrity docs/feature/{feature-id}/deliver/ --roadmap-only`. BLOCK on any format error; fix before dispatching any crafter.
   - d. Dispatch `@nw-acceptance-designer-reviewer` to review roadmap (load `~/.claude/skills/nw-review/SKILL.md`): verify every DISTILL scenario has a step, flag orphan scenarios as BLOCKER; flag steps covering 8+ scenarios as `@sizing-review-needed`; verify walking skeleton scenarios map to Phase 1 steps.
   - e. Retry once on rejection → stop for manual intervention.

3. **Phase 2 — Execute All Steps** — Gate: all steps reach COMMIT/PASS in `execution-log.json`.
   - a. Extract steps from `roadmap.json` in dependency order.
   - b. Check `execution-log.json` for prior completion (resume mode).
   - c. Dispatch selected crafter (from step 1.5) with full DES Prompt Template from `execute.md` (load `~/.claude/skills/nw-execute/SKILL.md`). Include DES markers (`DES-VALIDATION`, `DES-PROJECT-ID`, `DES-STEP-ID`) + all mandatory sections. Functional crafter → PBT default; `@property` tags signal PBT.
   - d. Verify COMMIT/PASS in `execution-log.json` per step.
   - e. Missing phase → RE-DISPATCH agent. NEVER write entries directly.
   - f. Stop on first failure.
   - g. Timeout recovery: GREEN completed → resume (~5 turns); GREEN partial → resume; otherwise → restart with higher `max_turns`.
   - h. Wiring smoke check: verify every new function defined in production files has at least one call site in production code (not just tests). Flag "function X defined but only called from tests" → re-dispatch crafter.
   - i. Acceptance test gate: after each step's COMMIT/PASS, run `tests/acceptance/{feature-id}/`. Fix failures before proceeding to next step. No deferral.

3.5. **Post-Merge Integration Gate (Hard Gate)** — AFTER all steps reach COMMIT/PASS, BEFORE Phase 3. Gate: full acceptance suite passes in all environments AND every story's Elevator Pitch demo command produces non-empty output.
   - a. Run `pipenv run pytest tests/acceptance/{feature-id}/ -v --tb=short`.
   - b. Run acceptance tests against EVERY environment listed in the `## Wave: DEVOPS / [REF] Environment Matrix` section of `feature-delta.md` (lean v3.14) OR `docs/feature/{feature-id}/devops/environments.yaml` (legacy multi-file). If neither, use defaults: `clean`, `with-pre-commit`, `with-stale-config`.
   - c. BLOCK if ANY test fails in ANY environment.
   - d. **Elevator Pitch demo execution (HARD GATE)** — For every user story in the `## Wave: DISCUSS / [REF] User Stories with Elevator Pitches` section of `feature-delta.md` (lean v3.14) OR `docs/feature/{feature-id}/discuss/user-stories.md` (legacy) that is NOT tagged `@infrastructure`:
      - Extract the `After: run ... → sees ...` line
      - Execute the exact command (subprocess, not function call)
      - Capture stdout + exit code
      - Verify: exit code is 0, stdout is non-empty, stdout contains the substring described by the "sees" clause
      - On any failure: BLOCK with message "Story {N}: demo command {cmd} did not produce visible output — either the CLI is broken or the story Elevator Pitch is fictional. Fix one or the other."
      - Append demo output to `docs/feature/{feature-id}/feature-delta.md` as `## Wave: DELIVER / [REF] Demo Evidence` (lean v3.14 — single narrative file) OR `docs/feature/{feature-id}/deliver/wave-decisions.md` under a `## Demo Evidence — {date}` section (legacy multi-file). Do NOT create a separate demo-output file.
   - e. On failure at step a/b: identify failing environment + test, re-dispatch crafter for new TDD cycle, re-run full gate after fix. If same test fails in 2+ environments after one fix attempt, STOP and report to user.
   - f. On success: record gate passage in `execution-log.json`: `{"gate": "post-merge-integration", "status": "PASS", "environments_tested": [...], "stories_demoed": [...], "timestamp": "ISO-8601"}`.

4. **Phase 3 — Complete Refactoring (L1-L6)** — [SKIP if `rigor.refactor_pass = false`]. Gate: all tests green after each module refactored.
   - a. Collect modified files: `git diff --name-only {base-commit}..HEAD -- '*.py' | sort -u`. Split into PRODUCTION_FILES (`src/`) and TEST_FILES (`tests/`).
   - b. Run `/nw-refactor {files} --levels L1-L6` via selected crafter with DES orchestrator markers: `<!-- DES-VALIDATION : required -->`, `<!-- DES-PROJECT-ID : {feature-id} -->`, `<!-- DES-MODE : orchestrator -->`.

5. **Phase 4 — Adversarial Review** — [SKIP if `rigor.review_enabled = false` or `rigor.reviewer_model = "skip"`]. Gate: review passed or one revision complete.
   - a. Dispatch `/nw-review @nw-software-crafter-reviewer implementation "{execution-log-path}"` with `model=rigor.reviewer_model` and DES orchestrator markers.
   - b. If `rigor.double_review = true` → run review a second time with different scope focus.
   - c. Scope: ALL files modified during feature; includes Testing Theater 7-pattern detection.
   - d. One revision pass on rejection → proceed.

6. **Phase 5 — Mutation Testing** — [SKIP if `rigor.mutation_enabled = false`]. Gate: ≥80% kill rate or strategy skip logged.
   - `per-feature` → gate ≥80% kill rate (load `~/.claude/skills/nw-mutation-test/SKILL.md`).
   - `nightly-delta` → SKIP; log "handled by CI nightly pipeline".
   - `pre-release` → SKIP; log "handled at release boundary".
   - `disabled` → SKIP; log "disabled per project configuration".

7. **Phase 6 — Deliver Integrity Verification** — Gate: `verify_deliver_integrity` exits 0.
   - a. Run: `des-verify-integrity docs/feature/{feature-id}/deliver/`.
   - b. Exit 0 → proceed. Exit 1 → STOP, read output.
   - c. No entries = not executed through DES. Partial = incomplete TDD.
   - d. Violations → re-execute via Task with DES markers. Proceed only after pass.

8. **Phase 7 — Finalize** — Gate: evolution archived, session markers removed, commit pushed.
   - a. Dispatch `@nw-platform-architect` to archive to `docs/evolution/` (load `~/.claude/skills/nw-finalize/SKILL.md`).
   - b. Commit + push. Run: `rm -f .nwave/des/deliver-session.json .nwave/des/des-task-active`.

9. **Phase 8 — Retrospective (conditional)** — Skip if clean execution. Gate: 5 Whys documented or clean-run noted.
   - On issues found → dispatch `@nw-troubleshooter` for 5 Whys analysis.

10. **Phase 9 — Report Completion** — Display summary: phases, steps, reviews, artifacts. Gate: report output, return to DISCOVER for next iteration.

## Orchestrator Responsibilities

Follow this flow directly. Do not delegate orchestration.

Per phase:
1. **Read command file** — Read the relevant command file (paths listed in each phase above).
2. **Embed instructions** — Extract instructions and embed them in the Task prompt.
3. **Add task boundary** — Include task boundary instructions to prevent workflow continuation.
4. **Verify artifacts** — Verify output artifacts exist after each Task completes.
5. **Update progress** — Update `.develop-progress.json` for resume capability.

## Task Invocation Pattern

DES markers required for step execution. Without markers → unmonitored. Full DES Prompt Template in `~/.claude/skills/nw-execute/SKILL.md`.

When dispatching steps via Agent tool, use the COMPLETE DES template from execute.md verbatim. Fill all `{placeholders}` from roadmap step context. The DES hook validates the prompt BEFORE the sub-agent starts — abbreviated prompts that delegate template reading to the sub-agent will be BLOCKED.

Copy the template from the code block in `~/.claude/skills/nw-execute/SKILL.md` (between ``` markers), fill placeholders, and pass as the Agent prompt. The template sections are defined in execute.md — do not hardcode the list here.

```python
Task(
    subagent_type="{agent}",
    model=rigor_agent_model,  # omit if "inherit"
    prompt=f'''
<!-- DES-VALIDATION : required -->
<!-- DES-PROJECT-ID : {project_id} -->
<!-- DES-STEP-ID : {step_id} -->

# DES_METADATA
Step: {step_id}
Feature: {project_id}
Command: /nw-execute

# AGENT_IDENTITY
Agent: {agent}

# SKILL_LOADING
Before starting TDD phases, read your skill files for methodology guidance.
Skills path: ~/.claude/skills/nw-{skill-name}/SKILL.md
Always load at PREPARE: tdd-methodology.md, quality-framework.md
Load on-demand per phase as specified in your Skill Loading Strategy table.

# TASK_CONTEXT
{step context extracted from roadmap - name|description|acceptance_criteria|test_file|scenario_name|quality_gates|implementation_notes|dependencies|estimated_hours|deliverables|files_to_modify}

# DESIGN_CONTEXT
{Summarize key architectural decisions from design wave artifacts read at step 0.5.
Include: component structure, dependency-inversion boundaries, technology choices,
data models, and any design constraints relevant to this step.
Source files: docs/product/architecture/brief.md, wave-decisions.md.
If no design artifacts exist, write "No design artifacts available — use project conventions."}

# TDD_PHASES
... (copy remaining sections from execute.md template verbatim)

# TIMEOUT_INSTRUCTION
Target: 30 turns max. If approaching limit, COMMIT current progress.
''',
    description="{phase description}"
)
```

## Roadmap Quality Gate (Automated, Zero Token Cost)

After roadmap creation, before reviewer, run these checks:

1. **AC coupling** — Flag AC referencing private methods (`_method()`). HIGH → return to architect.
2. **Decomposition ratio** — Flag steps/files > 2.5. HIGH → return to architect.
3. **Identical patterns** — Flag 3+ steps with same AC structure (batch them). HIGH → return to architect.
4. **Validation-only** — Flag steps with no `files_to_modify`. HIGH → return to architect.
5. **Step ID format** — Flag non-matching `^\d{2}-\d{2}$`. HIGH → return to architect.
6. **DISTILL linkage** — If `feature-delta.md` contains `## Wave: DISTILL / [REF] ...` sections OR `docs/feature/{feature-id}/distill/` exists (legacy), flag steps missing `test_file`/`scenario_name`. HIGH → return to architect.

## Skip and Resume

1. **Check progress** — Read `.develop-progress.json` on start for resume state.
2. **Skip approved roadmap** — Skip Phase 1 if `roadmap.json` exists with `validation.status == "approved"`.
3. **Skip completed steps** — Skip steps already showing COMMIT/PASS in `execution-log.json`.
4. **Cap retries** — Max 2 retries per review rejection → stop for manual intervention.

## Input

- `feature-description` (string, required, min 10 chars)
- `feature-id`: strip prefixes (implement|add|create), remove stop words, kebab-case, max 5 words

## Outputs

**Single narrative file**: `docs/feature/{feature-id}/feature-delta.md` — implementation summary, files modified, scenarios green count, DoD check, demo evidence, quality gates, pre-requisites all become `## Wave: DELIVER / [REF|WHY|HOW] <Section>` headings. Implementation details live in code; the wave-delta sections are pointers + structured summaries.

**Machine artifacts** (declared, parseable by DES + downstream tooling):
- `docs/feature/{feature-id}/roadmap.json` — step-by-step execution plan (created by nw-solution-architect, consumed by DES dispatcher)
- `docs/feature/{feature-id}/execution-log.json` — DES audit log of phase events per step (created by `des-init-log`, written by crafter sub-agents only)
- `docs/feature/{feature-id}/.develop-progress.json` — resume marker for skip-and-resume

**Long-term archive** (outside the feature dir): `docs/evolution/{feature-id}-evolution.md` — written by the platform architect at finalize time; cross-feature retrospective context.

**SSOT updates** (per Recommendation 3 / back-propagation contract):
- `docs/product/architecture/brief.md` — append shipped components to the Component Inventory subsection; mark previously-planned components that did NOT ship as deferred.
- `docs/product/kpi-contracts.yaml` — record measured baselines for each outcome KPI (the value at GA / first dogfood) so future deltas have a reference point.

Legacy multi-file outputs (`implementation-notes.md`, `commits.md`, `retrospective.md` as separate files in `docs/feature/{id}/deliver/`) are NOT produced — that content lives in `feature-delta.md` and `docs/evolution/`. Validator: `scripts/validation/validate_feature_layout.py`.

## Quality Gates

Roadmap review (1 review, max 2 attempts)|Per-step 5-phase TDD (PREPARE→RED_ACCEPTANCE→RED_UNIT→GREEN→COMMIT)|Paradigm-appropriate crafter|L1-L6 refactoring (Phase 3)|Adversarial review + Testing Theater detection (Phase 4)|Mutation ≥80% if per-feature (Phase 5)|Integrity verification (Phase 6)|All tests passing per phase

## Design Compliance Check (MANDATORY — RCA F-2 fix)

After each crafter step's COMMIT, verify the files modified match the DESIGN specification:

1. Read the `## Wave: DESIGN / [REF] Component Decomposition` table in `feature-delta.md` (lean v3.14) OR `docs/feature/{feature-id}/design/architecture-design.md` "Changes Per File" table (legacy multi-file)
2. Compare against `git diff --name-only` for the crafter's commit
3. If the crafter created a NEW file not listed in the design table: **STOP and flag**
   - A new file means a new component — this may be duplication of an existing component
   - Check the DESIGN's Reuse Analysis table (F-1) — if the new file's class overlaps an existing component, the crafter must extend the existing component instead
   - Do NOT proceed to the next step until resolved
4. If the crafter modified files not in the design table: acceptable (tests, config) but flag for review

This gate prevents the pattern where crafters create parallel implementations instead of extending existing components (see RCA `docs/analysis/rca-systematic-duplication-despite-design.md`).

## Wave Completion Enforcement (MANDATORY — RCA F-3 fix)

A feature CANNOT be marked COMPLETE unless ALL waves in its scope have been executed:

- DISTILL must have produced acceptance test files (`.feature` + `test_*.py`)
- All acceptance tests must be GREEN (no "DESIGNED, DISTILL needed" allowed at close)
- Old code paths superseded by new components must be DELETED (no fallback coexistence)
- The scaffold marker `__SCAFFOLD__ = True` must not exist in any production file

Violating this rule creates dead code, dual paths, and accumulated technical debt.

## Success Criteria

- [ ] Roadmap created and approved
- [ ] All steps COMMIT/PASS (5-phase TDD)
- [ ] **Design compliance verified** per step (F-2 — no unauthorized new files)
- [ ] **Wave sequence complete** (F-3 — no "DISTILL needed" at close)
- [ ] L1-L6 refactoring complete (Phase 3)
- [ ] Adversarial review passed (Phase 4)
- [ ] Mutation gate ≥80% or skipped per strategy (Phase 5)
- [ ] Integrity verification passed (Phase 6)
- [ ] Evolution archived (Phase 7)
- [ ] Retrospective or clean execution noted (Phase 8)
- [ ] Completion report (Phase 9)

## Examples

### 1: Fresh Feature
`/nw-deliver "Implement user authentication with JWT"` → roadmap → review → TDD all steps → mutation → finalize → report

### 2: Resume After Failure
Same command → loads `.develop-progress.json` → skips completed → resumes from failure

### 3: Single Step Alternative
For manual granular control, use individual commands:
```
/nw-roadmap @nw-solution-architect "goal"
/nw-execute {selected-crafter} "feature-id" "01-01"
/nw-finalize @nw-platform-architect "feature-id"
```

## Completion

DELIVER is final wave. After completion → DISCOVER for next feature or mark project complete.
