---
name: nw-discuss
description: "Conducts Jobs-to-be-Done analysis, UX journey design, and requirements gathering through interactive discovery. Use when starting feature analysis, defining user stories, or creating acceptance criteria."
user-invocable: true
argument-hint: '[feature-name] - Optional: --phase=[jtbd|journey|requirements] --interactive=[high|moderate] --output-format=[md|yaml]'
---

# NW-DISCUSS: Jobs-to-be-Done Analysis, UX Journey Design, and Requirements Gathering

**Wave**: DISCUSS (wave 2 of 6) | **Agent**: Luna (nw-product-owner) | **Command**: `/nw-discuss`

## Overview

Execute DISCUSS wave through Luna's integrated workflow: JTBD analysis|UX journey discovery|emotional arc design|shared artifact tracking|requirements gathering|user story creation|acceptance criteria definition. Luna uncovers jobs users accomplish, maps to journeys and requirements, handles complete lifecycle from user motivations through DoR-validated stories ready for DESIGN. Establishes ATDD foundation.

For greenfield projects (no src/ code, no docs/feature/ history), Luna proposes Walking Skeleton as Feature 0.

## Interactive Decision Points

### Decision 1: Feature Type
**Question**: What type of feature is this?
**Options**:
1. User-facing -- UI/UX functionality visible to end users
2. Backend -- APIs, services, data processing
3. Infrastructure -- DevOps, CI/CD, tooling
4. Cross-cutting -- Spans multiple layers (auth, logging, etc.)
5. Other -- user provides custom input

### Decision 2: Walking Skeleton
**Question**: Should we start with a walking skeleton?
**Options**:
1. Yes -- recommended for greenfield projects
2. Depends -- brownfield; Luna evaluates existing structure first
3. No -- feature is isolated enough to skip

### Decision 3: UX Research Depth
**Question**: Priority for UX research depth?
**Options**:
1. Lightweight -- quick journey map, focus on happy path
2. Comprehensive -- full experience mapping with emotional arcs
3. Deep-dive -- extensive user research, multiple personas, edge cases

### Decision 4: JTBD Analysis
**Question**: Include Jobs-to-be-Done analysis?
**Options**:
1. Yes -- recommended when user motivations are unclear or multiple jobs compete
2. No -- skip JTBD, proceed directly to journey design (default)

## Prior Wave Consultation

Before beginning DISCUSS work, read SSOT and prior wave artifacts:

1. **SSOT** (if `docs/product/` exists):
   - `docs/product/journeys/{name}.yaml` — existing journey to extend (if applicable)
   - `docs/product/jobs.yaml` — validated jobs and opportunity scores
   - `docs/product/vision.md` — product vision
2. **Project context**: `docs/project-brief.md` | `docs/stakeholders.yaml`
3. **DISCOVER artifacts**: Read `docs/feature/{feature-id}/discover/` (if present)
4. **DIVERGE artifacts**: Read `docs/feature/{feature-id}/diverge/recommendation.md` and `job-analysis.md` (if present — job is already validated, do not re-run JTBD)

**Migration gate**: If `docs/product/` does not exist but `docs/feature/` has existing features, STOP. The project has old-model features that should be migrated to SSOT before new waves run. Guide the user to `docs/guides/migrating-to-ssot-model/README.md` and complete the migration first. If `docs/product/` does not exist and no old features exist (greenfield), DISCUSS will bootstrap it.

DISCUSS follows DISCOVER and optionally DIVERGE — reading SSOT first ensures continuity with prior features, then prior wave artifacts ground requirements in evidence.

**READING ENFORCEMENT**: You MUST read every file listed in Prior Wave Consultation above using the Read tool before proceeding. After reading, output a confirmation checklist (`✓ {file}` for each read, `⊘ {file} (not found)` for missing). Do NOT skip files that exist — skipping causes requirements disconnected from evidence.

After reading, check whether any DISCUSS decisions would contradict DISCOVER evidence. Flag contradictions and resolve with user before proceeding. Example: DISCOVER found "users don't want automation" but DISCUSS story assumes "automated workflow" — this must be resolved.

## Document Update (Back-Propagation)

When DISCUSS decisions change assumptions established in DISCOVER:

1. **Document change** — Add a `## Changed Assumptions` section at the end of the affected DISCUSS artifact. Gate: section exists in artifact.
2. **Reference original** — Quote the original DISCOVER document and the original assumption verbatim. Gate: source document and quote both present.
3. **State new assumption** — State the new assumption and rationale for the change. Gate: rationale is explicit.
4. **Preserve DISCOVER** — Do NOT modify DISCOVER documents directly. Gate: DISCOVER documents unchanged.

## Agent Invocation

@nw-product-owner

IF Decision 4 = Yes: Execute *jtbd-analysis for {feature-id}, then *journey informed by JTBD artifacts, then *story-map, then *gather-requirements with outcome KPIs.
IF Decision 4 = No (default): Execute *journey for {feature-id}, then *story-map, then *gather-requirements with outcome KPIs.

Context files: see Prior Wave Consultation above + project context files.

**Configuration:**
- format: visual | yaml | gherkin | all (default: all)
- research_depth: {Decision 3} | interactive: high | output_format: markdown
- elicitation_depth: comprehensive | feature_type: {Decision 1}
- walking_skeleton: {Decision 2}
- output_directory: docs/feature/{feature-id}/discuss/

## Workflow

At the start of execution, create these tasks using TaskCreate and follow them in order:

### Phase 1: Jobs-to-be-Done Analysis (OPTIONAL — when Decision 4 = Yes)

Grounds all subsequent artifacts in real user motivations.

1. **Job Discovery** — Ask user what users are trying to accomplish. Capture in job story format: "When [situation], I want to [motivation], so I can [outcome]." Gate: all primary jobs documented in job story format.
2. **Job Dimensions** — For each job, identify functional (practical task), emotional (desired feeling), and social (desired perception) dimensions. Gate: three dimensions documented per job.
3. **Four Forces Analysis** — For each primary job, document Push (current frustration), Pull (desired future), Anxiety (adoption concerns), Habit (current behavior must change). Extract forces from interview transcripts, support tickets, or analytics when available rather than relying solely on user description. Gate: all four forces documented per job.
4. **Opportunity Scoring** — Rank jobs by importance vs. satisfaction gap. High importance + low satisfaction = strongest opportunities. Produce scored table. Gate: scored table produced when multiple jobs exist.
5. **JTBD-to-Story Bridge** — Map each job story to the user stories and acceptance criteria it will feed in Phase 3. Gate: every user story traces to at least one job.

| Artifact | Path |
|----------|------|
| Job Stories | `docs/feature/{feature-id}/discuss/jtbd-job-stories.md` |
| Four Forces | `docs/feature/{feature-id}/discuss/jtbd-four-forces.md` |
| Opportunity Scores | `docs/feature/{feature-id}/discuss/jtbd-opportunity-scores.md` (when multiple jobs) |

### Phase 2: Journey Design

Luna runs deep discovery (mental model|emotional arc|shared artifacts|error paths) informed by JTBD, produces visual journey + YAML schema + Gherkin scenarios. Each journey maps to one or more identified jobs.

1. **Mental Model Discovery** — Uncover user mental model: what users believe about the system, their vocabulary, and assumptions. Gate: mental model documented with no vague steps.
2. **Happy Path Definition** — Define all steps start-to-goal with expected outputs at each step. Gate: complete happy path with explicit outputs per step.
3. **Emotional Arc Design** — Map emotional state at each step. Confidence must build progressively toward goal. Gate: emotional arc coherent with upward trajectory.
4. **Shared Artifact Tracking** — Identify every `${variable}` or artifact passed between steps. Document single source of truth for each. Gate: every shared artifact has one documented source.
5. **Error Path Mapping** — Identify failure modes and recovery paths for critical steps. Gate: error paths documented for each high-risk step.
6. **Gherkin Scenario Generation** — Produce Gherkin scenarios covering happy path and key error paths. Gate: scenarios cover all journey steps.

| Artifact | Path |
|----------|------|
| Visual Journey | `docs/feature/{feature-id}/discuss/journey-{name}-visual.md` |
| Journey Schema | `docs/feature/{feature-id}/discuss/journey-{name}.yaml` |
| Gherkin Scenarios | `docs/feature/{feature-id}/discuss/journey-{name}.feature` |
| Artifact Registry | `docs/feature/{feature-id}/discuss/shared-artifacts-registry.md` |

### Phase 2.5: User Story Mapping

Luna loads `user-story-mapping` skill before this phase.

1. **Load Skill** — Load `user-story-mapping` skill. Gate: skill loaded.
2. **Backbone** — Map user activities (big steps) horizontally across the top of the story map. Gate: all major activities identified and ordered.
3. **Walking Skeleton** — Identify minimum slice that delivers end-to-end value. Gate: walking skeleton slice defined.
4. **Elephant Carpaccio Slicing** — Decompose stories into **thin vertical slices**, each shipping end-to-end in ≤1 day (≤6 hours of crafter dispatch), each with a named learning hypothesis. This supersedes the old "group into at least two releases" gate. The discipline and its rationale are documented below. Gate: every slice has (a) end-to-end value, (b) ≤1 day ship estimate, (c) a named learning hypothesis of the form "disproves X if it fails", (d) production data (not synthetic), (e) a dogfood moment within the same day, (f) explicit IN/OUT scope lists.
5. **Slice Taste Tests** — Apply the carpaccio taste tests to each slice before committing:
   - If a slice lists "ship 4+ new components" → it is NOT thin. Split further.
   - If every slice depends on a new abstraction → ship the abstraction FIRST as its own slice (or postpone it).
   - If no slice disproves any pre-commitment → the slicing is decoration, not discipline. Rethink.
   - If a slice uses only synthetic data → it proves plumbing, not value. Require a production-data acceptance criterion.
   - If 2+ slices are identical except for scale → merge them.
   Gate: all taste tests pass OR the failures are documented with a reason.
6. **Slice Briefs** — Produce one brief per slice at `docs/feature/{feature-id}/slices/slice-NN-name.md` with: goal (one sentence), IN scope, OUT scope, learning hypothesis (what this disproves if it fails, what it confirms if it succeeds), acceptance criteria, dependencies, effort estimate, reference class, pre-slice SPIKE if uncertainty is high. Each brief is ≤100 lines. Gate: brief exists for each slice listed in the story map.
7. **Prioritization** — Suggest slice execution order based on (a) learning leverage (highest-uncertainty slices first, so failures cost less), (b) dependency chain, (c) dogfood cadence. Gate: prioritization rationale documented per slice, NOT just per release bucket.

| Artifact | Path |
|----------|------|
| Story Map | `docs/feature/{feature-id}/discuss/story-map.md` |
| Prioritization | `docs/feature/{feature-id}/discuss/prioritization.md` |
| Slice Briefs | `docs/feature/{feature-id}/slices/slice-NN-*.md` (one per slice) |

### Phase 3: Requirements and User Stories

Luna crafts LeanUX stories informed by JTBD + journey artifacts. Every story traces to at least one job story. Validates against DoR, invokes peer review, prepares handoff.

1. **Story Drafting** — Craft user stories in LeanUX format. Each story traces to at least one job story from Phase 1 (or states "JTBD skipped" if Decision 4 = No). Gate: every story has a job traceability reference.
1b. **Elevator Pitch Test (MANDATORY, per-story)** — Every user story MUST contain an `### Elevator Pitch` subsection immediately after the story narrative, with exactly these three lines:

```markdown
### Elevator Pitch
Before: {one sentence — what the user cannot do today}
After: run `{exact command / endpoint / UI action}` → sees `{exact observable output}`
Decision enabled: {one sentence — what the user decides with that output}
```

Rules:
- The "After" line MUST reference a real user-invocable entry point (CLI subcommand, HTTP endpoint path, UI action name) — not a service function or internal API
- The "sees" portion MUST describe concrete observable output (stdout text, HTTP response body, screen element) — not internal state or "tests green"
- The "Decision enabled" line is the Job-to-be-Done connection: if the user cannot make any decision with the output, the story is infrastructure, not value — merge it into the story that DOES enable a decision
- If a story legitimately has no user-visible output (pure infra migration), it MUST be labelled `@infrastructure` and BLOCK the slice — a slice containing only `@infrastructure` stories cannot be released

Gate: every non-`@infrastructure` story has a complete Elevator Pitch. Slices with only `@infrastructure` stories are flagged for re-slicing.

2. **Acceptance Criteria** — Embed testable acceptance criteria in each story. Gate: every AC is verifiable without ambiguity. AC MUST verify the Elevator Pitch's "After" command produces the "sees" output end-to-end.
3. **Requirements Completeness** — Calculate requirements completeness score. Gate: score > 0.95.
4. **Outcome KPIs** — Define measurable outcome KPIs with targets. Gate: each KPI has a numeric target and measurement method.
5. **DoR Validation** — Validate all 9 DoR items with evidence. Gate: DoR passed with evidence for all 9 items.
6. **Peer Review** — Invoke peer review. Gate: review approved.
7. **Handoff Preparation** — Confirm handoff acceptance by nw-solution-architect (DESIGN wave). Gate: handoff accepted.

| Artifact | Path |
|----------|------|
| User Stories (includes requirements + embedded AC) | `docs/feature/{feature-id}/discuss/user-stories.md` |
| DoR Validation | `docs/feature/{feature-id}/discuss/dor-validation.md` |
| Outcome KPIs | `docs/feature/{feature-id}/discuss/outcome-kpis.md` |

## Success Criteria

1. - [ ] (when JTBD selected) JTBD analysis complete: all jobs in job story format
2. - [ ] (when JTBD selected) Job dimensions identified: functional|emotional|social per job
3. - [ ] (when JTBD selected) Four Forces mapped per job (push|pull|anxiety|habit)
4. - [ ] (when JTBD selected) Opportunity scores produced (when multiple jobs)
5. - [ ] UX journey map with emotional arcs and shared artifacts
6. - [ ] (when JTBD selected) Every journey maps to at least one job
7. - [ ] Discovery complete: user mental model understood, no vague steps
8. - [ ] Happy path defined: all steps start-to-goal with expected outputs
9. - [ ] Emotional arc coherent: confidence builds progressively
10. - [ ] Shared artifacts tracked: every ${variable} has single documented source
11. - [ ] Story map created with backbone, walking skeleton, and **elephant carpaccio slices** (≤1 day each, each with a named learning hypothesis, each with its own slice brief at `docs/feature/{id}/slices/slice-NN-*.md`, all carpaccio taste tests passed)
12. - [ ] Outcome KPIs defined with measurable targets
13. - [ ] Prioritization suggestions based on outcome impact
14. - [ ] Requirements completeness score > 0.95
15. - [ ] (when JTBD selected) Every user story traces to at least one job story
16. - [ ] All acceptance criteria testable
17. - [ ] DoR passed: all 9 items validated with evidence
18. - [ ] Peer review approved
19. - [ ] Handoff accepted by nw-solution-architect (DESIGN wave)

## Next Wave

**Handoff To**: nw-solution-architect (DESIGN wave) + nw-platform-architect (DEVOPS wave, KPIs only)
**Deliverables**: User stories + story map + outcome KPIs + SSOT journey/jobs updates | JTBD artifacts (when selected)

DISCUSS hands off to BOTH DESIGN (full artifacts) and DEVOPS (outcome-kpis.md only). DEVOPS and DESIGN can proceed in parallel — DESIGN receives the complete artifact set while DEVOPS receives only the KPI file to drive observability and instrumentation design.

## Wave Decisions Summary

Before completing DISCUSS, produce `docs/feature/{feature-id}/discuss/wave-decisions.md`:

```markdown
# DISCUSS Decisions — {feature-id}

## Key Decisions
- [D1] {decision}: {rationale} (see: {source-file})

## Requirements Summary
- Primary jobs/user needs: {1-3 sentence summary}
- Walking skeleton scope: {if applicable}
- Feature type: {user-facing|backend|infrastructure|cross-cutting}

## Constraints Established
- {constraint from requirements analysis}

## Upstream Changes
- {any DISCOVER assumptions changed, with rationale}
```

This summary enables DESIGN to quickly assess DISCUSS outcomes. DESIGN reads this plus key artifacts (user-stories.md, story-map.md, outcome-kpis.md) rather than all DISCUSS files.

## Expected Outputs

```
docs/feature/{feature-id}/discuss/     (feature delta)
  user-stories.md               (requirements + embedded AC, each story traces to a job)
  story-map.md
  dor-validation.md
  outcome-kpis.md
  wave-decisions.md

docs/product/                          (SSOT updates)
  journeys/{name}.yaml          (create or extend journey schema)
  journeys/{name}-visual.md     (human-readable journey narrative)
  jobs.yaml                     (add validated job if new)
```

## Examples

### Example 1: User-facing feature with comprehensive UX research
```
/nw-discuss first-time-setup
```
Orchestrator asks Decision 1-3. User selects "User-facing", "No skeleton", "Comprehensive". Luna starts with JTBD analysis: discovers jobs like "When I first open the app, I want to feel productive immediately, so I can justify the purchase." Maps four forces for each job. Scores opportunities. Then runs journey discovery informed by JTBD, produces visual journey + YAML + Gherkin. Finally crafts stories where each traces to a job, validates DoR, and prepares handoff.

### Example 2: JTBD-only invocation
```
/nw-discuss --phase=jtbd onboarding-flow
```
Runs only Luna's JTBD analysis phase (job discovery + dimensions + four forces + opportunity scoring). Produces JTBD artifacts without proceeding to journey design or requirements. Useful for early discovery when you need to understand user motivations before committing to UX design.

### Example 3: Journey-only invocation
```
/nw-discuss --phase=journey release-nwave
```
Runs only Luna's journey design phases (discovery + visualization + coherence validation). Produces journey artifacts without proceeding to requirements crafting. Useful when JTBD is already done and journey design needs standalone iteration.

### Example 4: Requirements-only invocation
```
/nw-discuss --phase=requirements new-plugin-system
```
Runs only Luna's requirements phases (gathering + crafting + DoR validation). Assumes JTBD and journey artifacts already exist or are not needed (e.g., backend feature).
