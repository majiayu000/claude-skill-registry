---
name: nw-distill
description: "Acceptance test creation methodology for the DISTILL wave. Domain knowledge for the acceptance designer agent: port-to-port principle, prior wave reading, wave-decision reconciliation, graceful degradation, and document back-propagation."
user-invocable: true
argument-hint: '[story-id] - Optional: --test-framework=[cucumber|specflow|pytest-bdd] --integration=[real-services|mocks]'
---

# DISTILL Methodology: Acceptance Test Creation

This skill provides the acceptance designer's methodology for creating acceptance tests. The orchestrator controls the overall flow (agent dispatch, review gate, handoff) -- this skill focuses on HOW to create good acceptance tests.

## Output Tiers (per D2)

Provenance: feature `lean-wave-documentation` — D2 (schema-typed sections), D10 (one-line expansion descriptions). The DISTILL wave emits a single `feature-delta.md` whose headings are typed `[REF]` (always emitted) or `[WHY]/[HOW]` (lazy expansions). Tier-1 is the always-on baseline; Tier-2 is the lazily-rendered expansion catalog. The `.feature` file remains the SSOT for scenarios; the wave-delta sections are pointers + structured summaries.

### Tier-1 [REF] — always emitted

Tier-1 sections constitute the lean-default baseline. Every DISTILL run emits at minimum these sections under `## Wave: DISTILL / [REF] <Section>` headings:

- Scenario list with tags — table of scenario titles + tags (`@walking_skeleton`, `@US-N`, `@real-io`, `@in-memory`, `@error`, `@property`)
- WS strategy — A/B/C/D selection per Mandate 5 with one-line justification
- Adapter coverage table — per Mandate 6, every driven adapter mapped to at least one `@real-io` scenario
- Scaffolds — list of RED-ready scaffold files created (per Mandate 7) with `__SCAFFOLD__` markers
- Test placement — `tests/{path}/` directory choice with one-line precedent justification
- Driving Adapter coverage — every CLI/endpoint/hook in DESIGN mapped to at least one subprocess/HTTP/hook scenario
- Pre-requisites — DESIGN driving ports + DEVOPS environment matrix the scenarios depend on

### Tier-2 EXPANSION CATALOG — lazy, on-demand (per D10)

Tier-2 items are NOT emitted by default. They are rendered only when explicitly requested via `--expand <id>` (DDD-2) or via the wave-end interactive prompt when `expansion_prompt = "ask"`. Each item has a one-line description (per D10) so the menu fits in a single render. Each emitted Tier-2 section is headed `## Wave: DISTILL / [WHY] <Section>` or `## Wave: DISTILL / [HOW] <Section>`.

| Expansion ID | Tier label | One-line description |
|---|---|---|
| `scenario-alternatives-considered` | [WHY] | Alternative scenario phrasings weighed and rejected (Gherkin variants, tag schemes) |
| `fixture-design-discussion` | [WHY] | Why these tmp_path/conftest fixtures, why these scopes, what they cannot model |
| `edge-case-enumeration` | [WHY] | Full edge-case taxonomy: empty/null/boundary/concurrency/timeout/permission |
| `error-path-rationale` | [WHY] | Why each `@error` scenario was chosen and what failure mode it surfaces |
| `tagging-cookbook` | [HOW] | Cookbook for tag application: `@property`, `@requires_external`, `@walking_skeleton` |
| `scaffold-authoring-recipes` | [HOW] | Per-language scaffold recipes (Python, TS, Go, Rust, Java) with marker conventions |
| `pbt-strategy-notes` | [WHY] | Property-based testing strategies for invariants surfaced by the feature |
| `expansion-catalog-rationale` | [WHY] | Why this set of expansions, why these defaults, why D10 enforces one-line descriptions |

## Density resolution (per D12)

Provenance: D12 (rigor cascade), DDD-5 (density resolver shared utility). Before emitting any Tier-1 section, resolve the active documentation density:

1. **Read** `~/.nwave/global-config.json`. Treat missing/malformed config as empty dict (fall back to defaults).
2. **Call** `resolve_density(global_config)` from `scripts/shared/density_config.py`. The function returns a `Density` value object with fields `mode` (`"lean"` | `"full"`), `expansion_prompt` (`"ask"` | `"always-skip"` | `"always-expand"` | `"smart"`), and `provenance` (the cascade branch that produced this result).
3. **Branch on `density.mode`**:
   - `lean` → emit ONLY Tier-1 `[REF]` sections under `## Wave: DISTILL / [REF] <Section>` headings. Do NOT auto-render Tier-2 items.
   - `full` → emit Tier-1 `[REF]` sections PLUS all Tier-2 expansion items rendered under their `[WHY]` / `[HOW]` headings. This is auto-expansion (no menu).
4. **At wave end**, branch on `density.expansion_prompt`:
   - `"ask"` → present the expansion menu (Tier-2 catalog above with one-line descriptions per D10) and append user-selected items as `## Wave: DISTILL / [WHY|HOW] <Section>` headings.
   - `"always-skip"` → no menu, no extra sections (idempotent re-runs, CI mode).
   - `"always-expand"` → equivalent to `mode = "full"` for this run; auto-render every Tier-2 item.
   - `"smart"` → out of scope for v1 (per OQ-3); treat as `"ask"` until heuristic is empirically tuned.

The resolver itself encodes the D12 cascade: explicit `documentation.density` override > `rigor.profile` mapping (`lean`→`lean`, `standard`→`lean`+`ask`, `thorough`→`full`, `exhaustive`→`full`+all-expansions, `custom`→`lean`+`ask`) > hard default `lean`+`ask`. This skill MUST NOT replicate the cascade locally — call `resolve_density(global_config)` and trust its output.

**Section heading prefix convention (per D2)**: every emitted section starts with `## Wave: DISTILL / [REF] <Section>` for Tier-1; `## Wave: DISTILL / [WHY] <Section>` or `## Wave: DISTILL / [HOW] <Section>` for Tier-2. Validator `scripts/validation/validate_feature_delta.py` enforces the regex `^## Wave: \w+ / \[(REF|WHY|HOW)\] .+$` on every wave heading.

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
  "wave": "DISTILL",
  "expansion_id": "<id-from-catalog-or-'*'-for-skip-all>",
  "choice": "skip" | "expand",
  "timestamp": "<ISO-8601 datetime>"
}
```

**Emission pattern**:

1. Construct a `DocumentationDensityEvent(feature_id=..., wave="DISTILL", expansion_id=..., choice=..., timestamp=...)`.
2. Call `event.to_audit_event()` to convert to the open `AuditEvent` shape (`event_type="DOCUMENTATION_DENSITY"` and the schema fields nested under `data`).
3. Dispatch via `JsonlAuditLogWriter().log_event(audit_event)`.

The wave-skill harness invokes the helper `scripts/shared/telemetry.py:write_density_event(...)` which performs all three steps. This skill MUST NOT bypass the helper or write JSONL directly — every density telemetry event flows through the shared helper to keep the audit-log schema consistent.

**When to emit**:
- One event per user choice in the expansion menu when `expansion_prompt = "ask"` (`choice = "expand"` for selected items, `choice = "skip"` with `expansion_id = "*"` if the user skips the entire menu).
- One synthetic `choice = "skip"` event with `expansion_id = "*"` when `expansion_prompt = "always-skip"` (records the skipped menu opportunity).
- One `choice = "expand"` event per Tier-2 item rendered when `mode = "full"` or `expansion_prompt = "always-expand"`.

This telemetry feeds the propagation success metric: when DELIVER consumes a lean DISTILL feature-delta and produces no `--expand` for fixture-design or edge-case enumeration, the `[REF]` baseline plus the `.feature` file is sufficient for the crafter.

## Feature-Delta Schema (US-01, US-02)

Provenance: `unified-feature-delta` US-01 (scaffold command) and US-02 (E1+E2 validator rules).

Every `feature-delta.md` is a Markdown document with `## Wave: <NAME>` sections. The canonical table format must be used in every `### [REF] Inherited commitments` block.

### Scaffold command

```
nwave-ai init-scaffold --feature <feature-name>
```

Creates `docs/feature/<feature-name>/feature-delta.md` with three pre-populated wave sections (DISCUSS, DESIGN, DISTILL), each containing a ready-to-fill commitments table. The scaffold passes the E1+E2 validator immediately.

### Canonical table format

Every `### [REF] Inherited commitments` block MUST have exactly four columns in this order:

```markdown
## Wave: DISCUSS

### [REF] Inherited commitments

| Origin | Commitment | DDD | Impact |
|--------|------------|-----|--------|
| n/a | <commitment text> | n/a | <impact text> |
```

Column semantics:
- **Origin**: wave and row reference of the upstream commitment (e.g., `DISCUSS#row1`) or `n/a` for root commitments
- **Commitment**: the specific commitment inherited or newly introduced in this wave
- **DDD**: Design Decision Document reference that authorizes any change (e.g., `DDD-3`) or `n/a` / `(none)` when not applicable
- **Impact**: substantive description (>=10 words or a consequence verb from the verb list) of the commitment's effect on the system

### Validator rules (E1+E2)

- **E1 (SectionPresent)**: every `## Wave: <NAME>` heading must match the canonical pattern. Known wave names: DISCOVER, DISCUSS, DESIGN, DEVOPS, DISTILL, DELIVER. Near-misses get a did-you-mean suggestion.
- **E2 (ColumnsPresent)**: every `### [REF] Inherited commitments` block must have a header row with the four required columns (Origin, Commitment, DDD, Impact) in any order, case-insensitive.

### Incremental authoring

Sections for waves not yet authored may be omitted entirely. The validator does not require all six wave sections to be present. An incremental feature-delta with only DISCUSS is valid. Missing future-wave sections are never flagged.

## Acceptance Criteria: Port-to-Port Principle

Every AC MUST name the driving port (entry point) through which the behavior is exercised. This enables port-to-port acceptance tests that make TBU (Tested But Unwired) defects structurally impossible.

Each AC includes:
1. **Observable outcome**: what the user/system sees
2. **Driving port**: the entry point that triggers the behavior (service, handler, endpoint, CLI command)

Without the driving port, a crafter can write correct code that is never wired into the system.

**Features**: "When user {action} via {driving_port}, {observable_outcome}"
**Bug fixes**: "When {trigger}, {modified_code_path} produces {correct_outcome} instead of {current_broken_behavior}"

## Prior Wave Reading

Before writing any scenario, read SSOT and feature delta artifacts.

**READING ENFORCEMENT**: You MUST read every file listed in steps 1-6 below using the Read tool before proceeding. After reading, output a confirmation checklist (`+ {file}` for each read, `- {file} (not found)` for missing). Do NOT skip files that exist.

1. **Read Journeys** — Read `docs/product/journeys/{name}.yaml`. Extract embedded Gherkin as starting scenarios, identify integration checkpoints and `failure_modes` per step. Gate: file read or marked missing.
2. **Read Architecture Brief** — Read `docs/product/architecture/brief.md`. Identify driving ports (from `## For Acceptance Designer` section) for `@driving_port` tagged scenarios. Gate: file read or marked missing.
3. **Read KPI Contracts** — Read `docs/product/kpi-contracts.yaml`. Identify behaviors needing `@kpi` tagged scenarios (soft gate — warn if missing, proceed). Gate: file read or marked missing.
4. **Read DISCUSS Artifacts** — Read `docs/feature/{feature-id}/discuss/user-stories.md` (scope boundary and embedded acceptance criteria), `story-map.md` (walking skeleton priority and release slicing), and `wave-decisions.md` (quick check for upstream changes). Gate: files read or marked missing.
5. **Read SPIKE Findings** (if spike was run) — Read `docs/feature/{feature-id}/spike/findings.md` and `docs/feature/{feature-id}/spike/wave-decisions.md`. Check what assumptions were validated, what failed, performance measurements, and the **promotion decision** (PROMOTE / DISCARD / PIVOT). Update acceptance criteria if spike findings contradict DISCUSS. Gate: files read if present, marked as not found if absent.
5b. **Read Walking Skeleton** (only if SPIKE promoted a walking skeleton) — Read the existing `tests/{test-type-path}/{feature-id}/acceptance/walking-skeleton.feature` and the `src/` modules it exercises. The walking skeleton is **already committed and green** — your job in DISTILL is to build **additional** scenarios and integration tests on top of it, not to rewrite it. Identify the driving adapter it uses, the e2e path it exercises, and the scenarios it does NOT yet cover (happy-path variants, error paths, adapter integration). Gate: walking-skeleton.feature read, scenario tagged `@walking_skeleton` confirmed green, or marked as not found.
6. **Read DEVOPS Artifacts** — Read `docs/feature/{feature-id}/devops/wave-decisions.md`. Check for infrastructure constraints affecting tests. Gate: file read or marked missing.
7. **Check Migration Gate** — If `docs/product/` does not exist but `docs/feature/` has existing features, STOP. Guide the user to `docs/guides/migrating-to-ssot-model/README.md`. If greenfield, prior waves should have bootstrapped `docs/product/` already. Gate: migration confirmed or greenfield confirmed.
8. **Reconcile Assumptions** — Check whether any acceptance test assumptions contradict prior wave decisions or SPIKE findings. Use `wave-decisions.md` and `spike/findings.md` files to detect upstream changes. Gate: zero contradictions or contradictions listed for user resolution.

DISTILL is the conjunction point — it reads all three SSOT dimensions plus the feature delta to translate prior wave knowledge into executable acceptance tests.

## Wave-Decision Reconciliation (Pre-Scenario Gate)

BEFORE writing any scenario, execute this reconciliation procedure:

1. **Read All Wave Decisions** — Read ALL wave-decisions.md files from prior waves: `docs/feature/{feature-id}/discuss/wave-decisions.md`, `docs/feature/{feature-id}/design/wave-decisions.md`, `docs/feature/{feature-id}/devops/wave-decisions.md`. Gate: all files read or marked missing.
2. **Check Each DISCUSS Decision** — For EACH decision in DISCUSS, check whether DESIGN or DEVOPS contradicts it. Examples: DISCUSS says "email notifications" but DESIGN says "in-app only" = CONTRADICTION; DISCUSS says "REST API" but DESIGN says "gRPC" = CONTRADICTION; DISCUSS says "single-tenant" but DEVOPS says "multi-tenant" = CONTRADICTION. Gate: all decisions checked.
3. **Handle Contradictions** — If ANY contradiction is found: (a) list ALL contradictions with exact file paths and decision text, (b) BLOCK scenario writing until the user resolves each contradiction, (c) return `{CLARIFICATION_NEEDED: true, questions: [{contradiction details}]}`. Gate: zero contradictions, or user resolution received.
4. **Log Reconciliation Result** — If zero contradictions: log "Reconciliation passed -- 0 contradictions" and proceed. Gate: log entry written.

Do NOT silently pick one side of a contradiction. Do NOT write scenarios against ambiguous specifications. The cost of blocking is minutes; the cost of implementing the wrong behavior is hours.

## Graceful Degradation for Missing Upstream Artifacts

**DEVOPS missing** (no `docs/feature/{feature-id}/devops/` directory):
1. **Log Warning** — Log: "DEVOPS artifacts missing -- using default environment matrix". Gate: warning logged.
2. **Apply Default Matrix** — Use default environment matrix: clean | with-pre-commit | with-stale-config. Gate: matrix applied.
3. **Proceed** — Continue with scenario writing. Do NOT block.

**DISCUSS missing** (no `docs/feature/{feature-id}/discuss/` directory):
1. **Log Warning** — Log: "DISCUSS artifacts missing -- using DESIGN only". Gate: warning logged.
2. **Derive from DESIGN** — Derive acceptance criteria from DESIGN architecture documents. Gate: criteria derived.
3. **Skip Traceability** — Skip story-to-scenario traceability -- no stories to trace. Gate: traceability skipped.
4. **Proceed** — Continue with scenario writing. Do NOT block.

**DESIGN missing** (no `docs/feature/{feature-id}/design/` directory):
1. **Log Warning** — Log: "DESIGN artifacts missing -- driving ports unknown". Gate: warning logged.
2. **BLOCK for Driving Ports** — Ask user to identify driving ports before writing any scenario. BLOCK until driving ports are identified -- without them, hexagonal boundary is unverifiable. Gate: user provides driving ports.

Missing artifacts trigger warnings, not failures -- EXCEPT when the missing artifact makes a design mandate unverifiable (DESIGN for hexagonal boundary). In that case, BLOCK.

## Document Update (Back-Propagation)

When DISTILL work reveals gaps or contradictions in prior waves:

1. **Document Findings** — Write findings in `docs/feature/{feature-id}/distill/upstream-issues.md`. Reference the original prior-wave document and describe the gap. Gate: file written.
2. **Flag Untestable Criteria** — If acceptance criteria from DISCUSS are untestable as written, note the specific criteria and explain why. Gate: all untestable criteria flagged.
3. **Resolve Before Writing** — Resolve contradictions with user before writing tests against ambiguous or contradictory requirements. Gate: user resolution received.

## Walking Skeleton Strategy Decision (INTERACTIVE)

Before writing walking skeleton scenarios, determine the WS adapter strategy. Auto-detect from the feature's component types, then confirm with the user.

**Decision Tree (auto-detect then user confirms):**

```
Feature is pure domain (no driven ports with I/O)?
  -> Strategy A (Full InMemory) -- WS uses InMemory doubles only

Feature has only local resources (filesystem, git, in-process subprocess)?
  -> Strategy C (Real local) -- WS uses real adapters for all local resources

Feature has costly external dependencies (paid APIs, LLM calls, rate-limited services)?
  -> Strategy B (Real local + fake costly) -- real for local, fake for expensive

Team needs different behavior in CI vs local development?
  -> Strategy D (Configurable) -- env var switches InMemory <-> Real
```

**Resource Classification:**

| Resource Type | WS Behavior | Adapter Integration Test |
|--------------|-------------|------------------------|
| Filesystem | real (tmp_path) | real (tmp_path) -- ALWAYS |
| Git repo | real (tmp_path + git init) | real -- ALWAYS |
| Local subprocess (pytest, ruff) | real | real -- ALWAYS |
| Costly subprocess (claude -p, LLM) | fake (mock) | contract smoke (@requires_external) |
| Paid external API | fake server | contract test with recorded fixtures |
| Database | real (SQLite/testcontainers) | real -- ALWAYS |
| Container services | per user preference | real if available |

**Container option:** Ask the user if they want containerized environments for WS and integration tests:
- No container (real adapters on host)
- Docker Compose (local services)
- Testcontainers (programmatic, lifecycle managed by test)

1. **Auto-Detect Strategy** — Classify feature components against the decision tree. Gate: strategy candidate identified.
2. **Confirm with User** — Present the auto-detected strategy and ask user to confirm or override. Gate: strategy confirmed.
3. **Record Decision** — Write the confirmed strategy in `distill/wave-decisions.md` as a numbered decision (e.g., DWD-XX: Walking Skeleton Strategy). Gate: decision recorded.
4. **Apply Strategy to Scenarios** — Tag WS scenarios per the confirmed strategy: Strategy A uses `@in-memory`, Strategy B/D uses `@real-io` for local and `@in-memory` for costly externals, Strategy C uses `@real-io` for ALL resources. Gate: scenarios tagged correctly.

**Tagging convention:**
- `@real-io` -- scenario uses real adapters
- `@in-memory` -- scenario uses InMemory doubles
- `@requires_external` -- scenario needs external system (skip if absent)
- Walking skeleton under B/C/D: MUST have `@walking_skeleton @real-io`

## Register Outcomes (per DISCUSS#D-5 grain)

Provenance: feature `outcomes-registry` — DISCUSS#D-2 (lean Tier-1 + Tier-2 default), D-5 (per-typed-contract grain), D-6 (gate-scoping: code-feature pipelines only).

**Trigger**: feature has a new typed contract surface — a rule module, CLI subcommand, public service operation, or system-wide invariant. Each such surface is one OUT-N row in the registry.

**Skip when**: the feature is methodology-only (skill propagation, prose changes, documentation updates, no new typed contract). Per D-6 gate-scoping, the registry tracks code-feature pipelines only; methodology features are explicitly OUT of scope.

**Procedure** — for every new contract surface introduced by the scenarios in this DISTILL session:

1. **Determine `kind`**: one of
   - `specification` — a rule (e.g. a guard, a validation predicate, a policy)
   - `operation` — a function/method exposed at a driving port (CLI subcommand, service method, endpoint)
   - `invariant` — a system-wide constraint that must always hold
2. **Run** `nwave-ai outcomes register --id OUT-N --kind {kind} --input-shape "..." --output-shape "..." --keywords "k1,k2,k3"`
3. **Handle exit codes**: exit `0` on successful registration; exit `2` on duplicate id (re-id the candidate and retry — typically because the OUT-N number is already taken).

The registry at `docs/product/outcomes/registry.yaml` becomes the SSOT for "what we promise the system does." Subsequent waves (DESIGN of later features) consult it to detect outcome collisions before introducing duplicate contracts.

Gate: every new typed contract introduced in the scenarios is registered with one OUT-N row, OR the feature is documented as methodology-only and registration is correctly skipped.

## Driving Adapter Verification (Mandatory — RCA fix P1, 2026-04-10)

If the DESIGN document specifies a CLI entry point, HTTP endpoint, or hook adapter:

1. **At least ONE walking skeleton scenario MUST invoke it via its protocol** — subprocess for CLI, HTTP request for API, hook JSON payload for hooks. Tag: `@driving_adapter @walking_skeleton`. Gate: scenario exists and exercises the user's actual invocation path.
2. **The scenario MUST verify**: exit code (or HTTP status), output format (stdout/response body), and basic argument handling. Gate: all three verified.
3. **Pipeline/service-level tests do NOT replace driving adapter tests.** A test that calls `generate_matrix()` directly proves the pipeline works but NOT that the CLI parses arguments, resolves PYTHONPATH, wires adapters, and produces correct exit codes. Both are needed.
4. **Scan DESIGN for entry points**: grep design docs for `python -m`, `cli`, `endpoint`, `hook adapter`. Each match needs at least one subprocess/HTTP/hook scenario. Gate: zero uncovered entry points.

This section exists because of a systematic pattern (RCA `docs/analysis/rca-user-port-gap.md`): acceptance tests entered from application services instead of user-facing CLIs, shipping features with working pipelines but broken entry points.

## Adapter Scenario Coverage (Mandate 6 Enforcement)

When designing adapter acceptance scenarios, EVERY driven adapter has at least one scenario with real I/O (or contract smoke for costly externals). This is not optional regardless of WS strategy. Tag adapter real-I/O scenarios with `@real-io @adapter-integration`.

1. **Inventory Adapters** — List all driven adapters in the feature. Gate: adapter list complete.
2. **Map Scenarios to Adapters** — For each adapter, identify existing scenarios that exercise it with real I/O. Gate: mapping complete.
3. **Produce Coverage Table** — Output the adapter coverage table before completing Phase 2:

```
| Adapter | @real-io scenario | Covered by |
|---------|-------------------|------------|
| YamlWorkflowLoader | YES | WS (real YAML from tmp_path) |
| FilesystemSkillReader | YES | WS (real skill files from tmp_path) |
| SubprocessGitVerifier | NO — MISSING | Add: "Git verifier reads real git log" |
| RuffLintRunner | NO — MISSING | Add: "Lint runner checks real ruff output" |
```

4. **Add Missing Scenarios** — Every row with "NO — MISSING" MUST have a scenario added. If the adapter is for a costly external (claude -p), a `@requires_external` contract smoke test is acceptable instead. Gate: zero "NO — MISSING" rows remain.

Cross-references: nw-tdd-methodology Mandate 5 (Walking Skeleton) and Mandate 6 (Real I/O), nw-quality-framework Dimension 9 (Walking Skeleton Integrity).

## Self-Review Checklist (Dimension 9 + Mandate 7)

Before handing off to reviewers, self-check each item:

- [ ] 1. WS strategy declared in wave-decisions.md
- [ ] 2. WS scenarios tagged correctly (@real-io / @in-memory per strategy)
- [ ] 3. Every driven adapter has at least one @real-io scenario
- [ ] 4. For InMemory doubles: documented what they CANNOT model
- [ ] 5. Container preference documented if applicable
- [ ] 6. **Mandate 7**: All production modules imported by tests have scaffold files
- [ ] 10. **Driving Adapter**: Every CLI/endpoint/hook in DESIGN has at least one WS scenario exercising it via subprocess/HTTP/hook protocol (not just calling the service function)
- [ ] 7. **Mandate 7**: All scaffolds include `__SCAFFOLD__` marker (or language equivalent)
- [ ] 8. **Mandate 7**: All scaffold methods raise assertion error (not NotImplementedError)
- [ ] 9. **Mandate 7**: Tests are RED (not BROKEN) when run against scaffolds
- [ ] 11. **F-001**: At least one `@real-io @adapter-integration` scenario per driven adapter (synthetic data misses format mismatches)
- [ ] 12. **F-002**: `capsys` used in `@when` step, NOT in `@then` step (capsys is step-scoped in pytest-bdd)
- [ ] 13. **F-005**: `@when` steps import ONLY from `des.application.*` or `des.domain.*` — NEVER from `des.adapters.driven.*`. Run `python scripts/hooks/check_driving_port_boundary.py` to verify.
- [ ] 14. **F-004**: Timing assertions in `.feature` files use budget >= 200ms (flaky under parallel load)
- [ ] 15. **F-003**: BDD imports after `sys.path` manipulation have `# noqa` markers (ruff strips them otherwise)

## Scenario Writing Guidelines

### Walking Skeleton First (or inherited from SPIKE)

If SPIKE ran and **PROMOTED** a walking skeleton, DISTILL inherits it: do NOT rewrite it, do NOT add duplicate scenarios, do NOT change its `@walking_skeleton` tag. Your job is to add the next layer of scenarios (additional happy paths, error paths, adapter integration) that build on the skeleton's established driving adapter and e2e path.

If SPIKE was skipped or did not promote, DISTILL creates the walking skeleton scenarios itself, before milestone features. Walking skeleton scenarios exercise the end-to-end path through driving adapters (real user-facing entry → real driven adapters → real user-visible output) with minimal business logic. Features only; optional for bugs.

Either way, there is exactly ONE walking skeleton scenario per feature marked `@walking_skeleton`, and it must be green before DISTILL hand-off.

### One-at-a-Time Strategy
Tag non-skeleton scenarios with @skip/@pending for one-at-a-time implementation. Each scenario maps to one TDD cycle in DELIVER. The crafter enables one scenario at a time.

### Business Language Purity
Feature files use business language only. No technical terms (API, database, endpoint, schema) in scenario names or Given/When/Then steps. Technical details live in step definitions, not feature files.

### Error Path Coverage
Target at least 40% error/edge case scenarios. Pure happy-path test suites miss the most common production failures. For every happy path, ask: "What happens when this input is invalid? When the dependency is unavailable? When the user cancels midway?"

### Environment-Aware Scenarios
When DEVOPS provides environment inventory, create at least one walking skeleton scenario per environment. Each environment has different preconditions (clean install vs. upgrade vs. stale config) that affect behavior.

## Mandate 7: RED-Ready Scaffolding

**Every acceptance test MUST be RED, not BROKEN, when first created.**

When DISTILL writes acceptance tests that import production modules not yet implemented, it MUST also create minimal stub files so that:
1. All imports succeed (no ImportError -- no BROKEN classification)
2. Method calls raise AssertionError (-- RED classification)
3. The Red Gate Snapshot classifies the test as RED, enabling the DELIVER TDD cycle

### What to scaffold

For each production module imported in step definitions:
1. **Create Module File** — Create the module file at the correct path (e.g., `src/app/plugin/installer.py`). Gate: file created.
2. **Add Scaffold Marker** — Include the scaffold marker (`__SCAFFOLD__ = True` or language equivalent) for machine detection. Gate: marker present.
3. **Define Signatures** — Define the class/function with the correct parameter signature. Gate: signatures match what step definitions expect.
4. **Raise Assertion Error** — Method bodies MUST raise an assertion error with the scaffold marker message. Gate: all methods raise AssertionError (not NotImplementedError).
5. **Verify RED Classification** — Confirm the test runner classifies tests as RED, not BROKEN. Gate: RED confirmed.

### Language-specific scaffolding

The principle is universal: **raise an exception classified as assertion failure (RED), not infrastructure error (BROKEN).**

**Python**:
```python
# src/app/plugin/installer.py
"""Plugin installer -- RED scaffold (created by DISTILL)."""
__SCAFFOLD__ = True

class PluginInstaller:
    def __init__(self, **kwargs):
        pass

    def install(self, ctx):
        raise AssertionError("Not yet implemented -- RED scaffold")
```

**Rust**:
```rust
// src/plugin/installer.rs
// SCAFFOLD: true
pub struct PluginInstaller;

impl PluginInstaller {
    pub fn install(&self) -> Result<(), Box<dyn std::error::Error>> {
        panic!("Not yet implemented -- RED scaffold")
    }
}
```

**Go**:
```go
// plugin/installer.go
// SCAFFOLD: true
package plugin

func Install() error {
    panic("not yet implemented -- RED scaffold")
}
```

**TypeScript/JavaScript**:
```typescript
// src/plugin/installer.ts
export const __SCAFFOLD__ = true;

export class PluginInstaller {
    install(): never {
        throw new Error("Not yet implemented -- RED scaffold");
    }
}
```

**Java**:
```java
// src/plugin/PluginInstaller.java
// SCAFFOLD: true
public class PluginInstaller {
    public void install() {
        throw new AssertionError("Not yet implemented -- RED scaffold");
    }
}
```

### Scaffold detection

DELIVER uses the scaffold marker to track progress:
- `grep -r "__SCAFFOLD__" src/` (Python, TypeScript)
- `grep -r "SCAFFOLD: true" src/` (Rust, Go, Java)

After all DELIVER steps complete, zero scaffold markers should remain.

### Why assertion errors (not NotImplementedError)

The Red Gate Snapshot (`src/des/application/red_gate_snapshot.py`) classifies failures by error type:
- `AssertionError` / `panic!` / `throw Error` -- **RED** (implementation missing, test correct)
- `NotImplementedError` -- **BROKEN** (infrastructure issue)
- `ImportError` / `ModuleNotFoundError` -- **BROKEN** (module missing)

Only RED tests proceed to the DELIVER TDD cycle. BROKEN tests block the upstream gate.

### Scaffolding lifecycle

1. **DISTILL** creates the scaffold (RED-ready stubs)
2. **Snapshot** classifies the test as RED
3. **DELIVER** replaces the scaffold with real implementation (GREEN)

The scaffold is never committed to production -- it exists only between DISTILL approval and DELIVER completion for each step.

## Final Wave Review Gate (Mandatory — covers DISCUSS+DESIGN+DEVOPS+DISTILL)

AFTER all DISTILL Tier-1 [REF] sections are appended to `feature-delta.md` and acceptance scenarios + scaffolds are written, dispatch FOUR reviewers in parallel against the full `feature-delta.md`. This is the consolidated mandatory review that replaces per-wave reviews (per-wave is now opt-in only — see DISCUSS/DESIGN/DEVOPS skills). All four reviewers see the entire 4-wave chain in one file, enabling cross-wave consistency checks that per-wave review misses.

1. **Dispatch four reviewers in parallel** (single message, multiple Agent tool uses, all on Haiku for cost efficiency):
   - `@nw-product-owner-reviewer` (Eclipse) — reviews DISCUSS sections (lines 1 to first `## Wave: DESIGN` heading)
   - `@nw-solution-architect-reviewer` (Architect) — reviews DESIGN sections (between `## Wave: DESIGN` and `## Wave: DEVOPS`)
   - `@nw-platform-architect-reviewer` (Forge) — reviews DEVOPS sections (between `## Wave: DEVOPS` and `## Wave: DISTILL`)
   - `@nw-acceptance-designer-reviewer` (Sentinel) — reviews DISTILL sections + executable `.feature` files + scaffolds
   Gate: all four reviewers dispatched concurrently.

2. **Each reviewer outputs YAML verdict** with: `approval_status` ∈ {approved, conditionally_approved, needs_revision, rejected}, `blocker_count`, `high_count`, `low_count`, `findings_list`. Gate: structured verdict received from each.

3. **Cross-wave consistency check** — if Eclipse APPROVES DISCUSS but Architect's findings reveal DISCUSS contradictions (e.g. story claims X, ADR assumes Y), surface as cross-wave blocker. Gate: contradictions flagged.

4. **Blocker handling** — for each NEEDS_REVISION verdict: dispatch fix to the corresponding wave's primary agent (Luna for DISCUSS, Morgan for DESIGN, platform-architect for DEVOPS, acceptance-designer for DISTILL). Re-run only the affected reviewer after fix. Gate: 2 revision cycles max per wave; escalate to user if not resolved.

5. **Block DELIVER handoff** — do not hand off to DELIVER until all four verdicts are APPROVED or CONDITIONALLY_APPROVED with documented action items in DELIVER scope. Gate: zero blockers, zero high (or accepted-with-conditions).

**Cost**: 4 Haiku reviewers in parallel ≈ $0.05-0.20 per feature. Trades small cost for late-feedback-blast-radius reduction (full chain visible).

**Per-wave review trigger override**: even with this final gate, a wave-skill may have triggered its own per-wave review (DoR ambiguity, contested ADR, novel deployment target, etc.). Per-wave reviewer outputs are PR-ephemeral, not committed; they inform the wave's primary agent in real time but don't substitute for this final gate.

## Outputs

**Single narrative file**: `docs/feature/{feature-id}/feature-delta.md` — scenario list with tags, WS strategy, adapter coverage table, scaffolds list, test placement, driving adapter coverage, pre-requisites all become `## Wave: DISTILL / [REF|WHY|HOW] <Section>` headings. The `.feature` file (below) remains the SSOT for executable scenarios; the wave-delta sections are pointers + structured summaries.

**Machine artifacts** (declared, parseable by downstream — the `.feature` files ARE the scenario SSOT, executable by pytest-bdd):
- `tests/{test-type-path}/{feature-id}/acceptance/walking-skeleton.feature`
- `tests/{test-type-path}/{feature-id}/acceptance/milestone-{N}-{description}.feature`
- `tests/{test-type-path}/{feature-id}/acceptance/integration-checkpoints.feature`
- `tests/{test-type-path}/{feature-id}/acceptance/steps/conftest.py` + `{domain}_steps.py`
- `src/{production-path}/{module}.py` — RED scaffold stubs (Mandate 7)

For bug fix regression tests: `tests/regression/{component-or-module}/bug-{ticket-or-description}.feature` + matching `tests/unit/{component-or-module}/test_{module}_bug_{ticket-or-description}.py`.

**SSOT updates** (per Recommendation 3 / back-propagation contract):
- `docs/product/kpi-contracts.yaml` — refine acceptance metrics: per-KPI scenario tag (`@kpi`) link, expected measurement window, soft-vs-hard gate classification. DISTILL inherits the contract from DEVOPS and tightens it as scenarios are written.

Legacy multi-file outputs (`walking-skeleton.md`, `wave-decisions.md`, `test-scenarios.md`, `acceptance-review.md` as separate files in `docs/feature/{id}/distill/`) are NOT produced — that content lives in `feature-delta.md`, and the executable `.feature` files are the scenario SSOT. Reviewer output is ephemeral (PR comments / retrospective, not committed). Validator: `scripts/validation/validate_feature_layout.py`.
