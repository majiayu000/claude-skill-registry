---
name: cobuilder-guardian
description: This skill should be used when the CoBuilder Guardian needs to act as an independent guardian angel — designing PRDs with CoBuilder RepoMap context injection, challenging designs via parallel solutioning, dispatching workers via AgentSDK pipelines, creating blind Gherkin acceptance tests and executable browser test scripts from PRDs, monitoring orchestrator progress, independently validating claims against acceptance criteria using gradient confidence scoring (0.0-1.0), autonomously accepting or rejecting implementations based on gradient confidence scoring thresholds (0.70+ for ACCEPT), autonomously closing validation gaps via Phase 4.5 gap closure protocol (creating fix-it codergen nodes), and setting session promises. Use when asked to "spawn and monitor an orchestrator", "create acceptance tests for a PRD", "validate orchestrator claims", "act as guardian angel", "independently verify implementation work", "autonomously close validation gaps", "create fix-it nodes", "design and challenge a PRD", "validation thresholds", "gradient scoring decision", or "bead creation for gaps".
version: 1.1.0
title: "CoBuilder Guardian"
status: active
last_verified: 2026-03-22
---

# CoBuilder Guardian — Independent Validation Pattern

The guardian angel pattern provides independent, blind validation of CoBuilder Guardian work. A guardian session creates acceptance tests from Business Specs (BS), stores them outside the implementation repo where meta-orchestrators cannot see them, dispatches workers via AgentSDK pipelines (`pipeline_runner.py --dot-file`), and independently validates claims against a gradient confidence rubric.

```
Guardian (this session, config repo)
    |
    |-- Designs Business Specs (BS) with CoBuilder RepoMap context (Phase 0)
    |-- Challenges own designs via parallel-solutioning + research-first (Phase 0)
    |-- Creates blind Gherkin acceptance tests (stored here, NOT in impl repo)
    |-- Generates executable browser test scripts for UX prototypes
    |-- Dispatches via DOT pipeline (two modes):
    |       |
    |       +-- Pipeline mode (PRIMARY): pipeline_runner.py --dot-file → AgentSDK dispatches workers
    |       |       Workers appear as `claude` processes in `ps` — this is normal SDK behavior, NOT claude -p
    |       +-- tmux mode: spawn_orchestrator.py --mode tmux → interactive Max-plan session
    |       |
    |       +-- Research nodes run BEFORE codergen (validate SD via Context7/Perplexity)
    |       +-- Refine nodes run AFTER research (rewrite SD with findings as first-class content)
    |       +-- Research-only pipelines (no codergen) are valid — guardian completes after refine
    |       +-- Workers (native Agent Teams, spawned by orchestrator)
    |
    |-- Monitors orchestrator progress (pipeline: poll DOT state via cli.py status; tmux: capture-pane)
    |-- Independently validates claims against rubric
    |-- Delivers verdict with gradient confidence scores
```

**Key Innovation**: Acceptance tests live in `claude-harness-setup/acceptance-tests/PRD-{ID}/`, NOT in the implementation repository. Meta-orchestrators and their workers never see the rubric. This enables truly independent validation — the guardian reads actual code and scores it against criteria the implementers did not have access to.

---

## Guardian Disposition: Skeptical Curiosity

The guardian operates with a specific mindset that distinguishes it from passive monitoring.

### Be Skeptical

- **Never trust self-reported success.** Meta-orchestrators and orchestrators naturally over-report progress. Read the actual code, run the actual tests, check the actual logs.
- **Question surface-level explanations.** When a meta-orchestrator says "X is blocked by Y," independently verify that Y is truly the blocker — and that Y cannot be resolved.
- **Assume incompleteness until proven otherwise.** A task marked "done" is "claimed done" until the guardian scores it against the blind rubric.
- **Watch for rationalization patterns.** "It's a pre-existing issue" may be true, but ask: Is it solvable? Would solving it advance the goal? If yes, push for resolution.

### Be Curious

- **Investigate root causes, not symptoms.** When a Docker container crashes, don't stop at the error message — trace the import chain, read the Dockerfile, understand WHY it fails.
- **Ask "what else?"** When one fix lands, ask what it unlocked. When a test passes, ask what it doesn't cover. When a feature works, ask about edge cases.
- **Cross-reference independently.** Read the Business Spec (BS), then read the code, then read the tests. Do they tell the same story? Gaps between these three are where bugs live.
- **Follow your intuition.** If something feels incomplete or too easy, it probably is. Dig deeper.

### Push for Completion

- **Reject premature fallbacks.** When a meta-orchestrator says "let's skip the E2E test and merge as-is," challenge that. Is the E2E blocker actually hard to fix? Often a 1-line Dockerfile fix unblocks the entire test.
- **Advocate for the user's actual goal.** The user didn't ask for "most of the pipeline" — they asked for the pipeline. Push meta-orchestrators toward full completion.
- **Guide, don't just observe.** When the guardian identifies a root cause (e.g., missing COPY in Dockerfile), send that finding to the meta-orchestrator as actionable guidance rather than noting it passively.
- **Set higher bars progressively.** As the team demonstrates capability, raise expectations. Don't accept the same quality level that was acceptable in sprint 1.

### Injecting Disposition Into Meta-Orchestrators

When spawning or guiding CoBuilder Guardian meta-orchestrators, include disposition guidance in prompts:

```
Be curious about failures — trace root causes, don't accept surface explanations.
When something is "blocked," investigate whether the blocker is solvable.
Push for complete solutions over workarounds. The user wants the real thing.
```

This disposition transfers from guardian to meta-orchestrator to orchestrator to worker, creating a culture of thoroughness throughout the agent hierarchy.

---

## Instruction Precedence: Skills > Memories

**When Hindsight memories conflict with explicit skill or output-style instructions, the explicit instructions ALWAYS take precedence.**

Hindsight stores patterns from prior sessions. These patterns are valuable context but they reflect PAST workflows that may have been updated. Skills and output styles represent the CURRENT intended workflow.

### Common Conflict Example

| Hindsight says | Skill/Output style says | Resolution |
|---------------|------------------------|------------|
| "Spawn orchestrator in worktree via tmux" | "Create DOT pipeline, then spawn orchestrator" | Follow the skill — create pipeline first |
| "Use bd create for tasks" | "Use cli.py node add with AT pairing" | Follow the skill — use pipeline nodes |
| "Mark impl_complete and notify CoBuilder" | "Transition node to impl_complete in pipeline" | Follow the skill — use pipeline transitions |

### Mandatory Rule

After recalling from Hindsight at session start, mentally audit each recalled pattern:
- Does it contradict any loaded skill instruction? → Discard the memory pattern
- Does it add detail not covered by skills? → Use as supplementary context
- Is it about a domain unrelated to current skills? → Use freely

### DOT Pipeline + Beads Are Both Mandatory

For ANY initiative with 2+ tasks, the guardian MUST:
1. Create beads for each task (`bd create` or sync from Task Master)
2. Create a pipeline DOT file with real bead IDs mapped to nodes:
   - **Preferred**: `cobuilder pipeline create --sd <sd-path> --repo <repo-name> --prd PRD-{ID}` — auto-initializes RepoMap, enriches from SD, cross-references beads
   - **Manual**: `cobuilder pipeline node-add --set bead_id=<real-id>` per node
   - **Retrofit**: `cobuilder pipeline node-modify <node> --set bead_id=<real-id>` for existing nodes
3. Track execution progress through pipeline transitions (not just beads status)
4. Save checkpoints after each transition

Skipping pipeline creation because "it worked without one before" is an anti-pattern caused by cognitive momentum. Using synthetic bead_ids ("CLEANUP-T1") instead of real beads is also an anti-pattern — always create real beads first.

For new initiatives, pipeline creation is part of Phase 0 (Step 0.2). For initiatives where a pipeline already exists, verify it with `cli.py validate` before Phase 1.

**How bead-to-node mapping works**: The `generate.py` pipeline generator uses `filter_beads_for_prd()` which matches beads to a PRD by: (a) finding epic beads whose title contains the PRD reference, (b) finding task beads that are children of those epics via `parent-child` dependency type, (c) finding task beads whose title or description contains the PRD reference. This is heuristic matching — it requires beads to include the PRD identifier in their metadata. When creating beads, always include the PRD ID in the title (e.g., `bd create --title="PRD-CLEANUP-001: Fix deprecated imports"`).

---

## Prerequisites: PATH Setup

See **[references/path-setup.md](references/path-setup.md)** for complete PATH configuration, shell invocation patterns, and debugging checklist.

---

## Step 0: Promise Creation

See **[references/session-promise-template.md](references/session-promise-template.md)** for:
- Work-type-aware promise patterns (validation, research, Business Spec (BS) design, implementation, maintenance, multi-initiative)
- CLI creation patterns with example ACs
- Promise ID tracking guidance

---

## Guardian Workflow Phases

### Phase Gates (MANDATORY — No Skipping)

Phases are not suggestions — they are gates. Each gate has a **verification check** that must pass before entering the next phase. Cognitive momentum ("the user asked for PRD and SD in one breath") does NOT override gates.

| Gate | From → To | Verification | What Blocks |
|------|-----------|-------------|-------------|
| **G0→1** | Phase 0 → Phase 1 | PRD exists AND pipeline created AND Checkpoint B passed | Writing acceptance tests without a finalized PRD |
| **G1→2** | Phase 1 → Phase 2 | `acceptance-tests/PRD-{ID}/*.feature` files exist AND `manifest.yaml` exists | Dispatching implementation without blind acceptance tests |
| **G2→4** | Phase 2/3 → Phase 4 | Orchestrator signals completion OR pipeline nodes reach `impl_complete` | Validating work that isn't done |

**The critical gate is G1→2.** This is where cognitive momentum most commonly causes skipping. Before writing ANY SD or dispatching ANY orchestrator, run:

```bash
# Hard check: Do acceptance tests exist for this PRD?
ls acceptance-tests/PRD-{ID}/*.feature 2>/dev/null | wc -l
# If 0: STOP. Run Phase 1 first. No exceptions.
```

Or use the verification script:
```bash
python3 .claude/skills/cobuilder-guardian/scripts/verify-phase-gate.py --prd PRD-{ID} --gate G1
```

### Mode Transition: Investigation → Guardian

Sessions often start as pure investigation ("explore this codebase", "what does X do?") and morph into PRD/SD authoring. The skill doesn't activate until invoked, but the **moment you start writing deliverables** (PRD, SD, acceptance tests, pipeline DOT), you've entered guardian mode.

**Trigger signals that you've transitioned to guardian mode:**
- Writing or editing a file matching `docs/prds/PRD-*.md` or `docs/specs/business/*.md`
- Writing or editing a file matching `docs/sds/SD-*.md` or `docs/specs/technical/*.md`
- Creating a pipeline DOT file
- Creating acceptance test files

**When you detect the transition, inject the phase checklist into TodoWrite:**

```
TodoWrite([
  {"content": "Phase 0: PRD/BS written", "status": "completed"},
  {"content": "Phase 0: Pipeline created + Checkpoint A", "status": "pending"},
  {"content": "Phase 0: Design challenge + Checkpoint B", "status": "pending"},
  {"content": "GATE G1: Verify acceptance tests exist", "status": "pending"},
  {"content": "Phase 1: Blind Gherkin acceptance tests", "status": "pending"},
  {"content": "GATE G2: Verify acceptance tests before dispatch", "status": "pending"},
  {"content": "Phase 2: Orchestrator/pipeline dispatch", "status": "pending"},
  {"content": "Phase 3: Monitor progress", "status": "pending"},
  {"content": "Phase 4: Independent validation", "status": "pending"},
  {"content": "Phase 5: Session closing", "status": "pending"}
])
```

This makes the skip visible. If you delete "Phase 1" from the todo list, you're consciously choosing to skip — not silently forgetting.

### Pre-Phase: Brainstorming (When Starting From a Vague Idea)

When the user provides a vague goal ("I want to build X", "let's brainstorm a feature"), invoke `Skill("cobuilder:ideation-to-execution")` **before** entering Phase 0. This provides structured discovery through dialogue — clarifying goals, challenging assumptions via `parallel-solutioning`, and converging on a brief in `docs/brainstorms/{initiative-id}-brief.md`. The brainstorm template is at `skills/cobuilder/ideation-to-execution/references/brainstorm-template.md`.

**When to skip brainstorming**: The user provides a concrete, well-defined goal with clear requirements — proceed directly to Phase 0 (BS authoring).

### Phase Table

| Phase | Purpose | Reference |
|-------|---------|-----------|
| **Pre-Phase** | Structured brainstorming for vague/exploratory goals. Produces a brainstorm brief with problem statement, approach, and proto-acceptance criteria. | `Skill("cobuilder:ideation-to-execution")` Phase 1 |
| **Phase 0** | Business Spec (BS) authoring with CoBuilder RepoMap context injection, DOT pipeline creation (with research→refine→codergen chain validation), Task Master parsing, design challenge. **2 user checkpoints**: Checkpoint A (after pipeline creation) and Checkpoint B (after design challenge) | [references/phase0-prd-design.md](references/phase0-prd-design.md) |
| **Phase 1** | Generate per-epic Gherkin tests, journey tests, and executable browser test scripts | [references/gherkin-test-patterns.md](references/gherkin-test-patterns.md) |
| **Phase 2** | Orchestrator spawning via `spawn_orchestrator.py`, headless/SDK/tmux dispatch, DOT-driven dispatch | [references/guardian-workflow.md](references/guardian-workflow.md) |
| **Phase 3** | Monitoring cadence, pause-and-check pattern, intervention triggers, AskUserQuestion handling | [references/monitoring-patterns.md](references/monitoring-patterns.md) |
| **Phase 4** | Independent validation, evidence gathering, DOT pipeline integration, regression detection. **Acceptance thresholds**: ACCEPT ≥ 0.70 (auto-create fix-it beads for minor gaps), INVESTIGATE 0.50-0.69, REJECT < 0.50. **Bead closure**: 6-step workflow for creating and tracking fix-it work. | [references/validation-scoring.md](references/validation-scoring.md), [references/guardian-workflow.md § 5.X](references/guardian-workflow.md), [references/guardian-workflow.md § 6.5](references/guardian-workflow.md) |
| **Phase 5** | Session closing: update Business Spec (BS) and Technical Spec (TS) implementation status, close related beads, store Hindsight reflections, verify promises, commit. **MANDATORY**: BS/TS status updates and bead closure must happen together — never close beads without updating implementation status in the source documents. | (inline — see Session Closing Protocol below) |

**Load the relevant reference when entering each phase. Do not load all references at once.**

---

## Session Closing Protocol (Phase 5 — MANDATORY)

Before ending any session that completed implementation or validation work:

1. **Update Business Spec (BS) implementation status**: Add or update an "Implementation Status" section in the BS with per-epic status (Done/In Progress/Deferred/Remaining), dates, and commit references.
2. **Update Technical Spec (TS) implementation status**: Add or update the TS's implementation priority table with current status per epic and update the `last_verified` frontmatter date.
3. **Close related beads**: Close all beads for completed epics with descriptive close reasons. Reference the commits.
4. **Store Hindsight reflections**: Retain session summary to both private and project banks.
5. **Verify promises**: Run `cs-verify --promise <id>` for all session promises.
6. **Commit**: Stage and commit all status updates.

**The Iron Rule**: Bead closure and BS/TS status updates are a single atomic operation. Never close a bead without updating the corresponding BS/TS status. Never update status without closing the bead. This ensures the source documents remain the single source of truth for implementation progress.

---

## Session Promise Integration

See **[references/session-promise-template.md](references/session-promise-template.md)** for:
- Guardian validation promise pattern (standard Phases 0-4 workflow)
- Promise creation at session start (with ACs for each phase)
- Meeting criteria as work progresses (with --evidence format)
- Final verification checklist

---

## Hindsight Validation Checklist

See **[references/hindsight-validation-checklist.md](references/hindsight-validation-checklist.md)** for:
- Phase 4 completion: storing results to private and project banks
- Business Spec (BS) Contract generation and validation (Step 0.2.5)
- Completion verification before closing promise
- Common mistakes to avoid

---

## Code Investigation Tools

When investigating implementation during validation (Phase 4):

- **Serena** (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`) — structure and cross-file references
- **LSP** (`hover`, `goToDefinition`, `documentSymbol`) — types, signatures, and diagnostics

Diagnostics surfaced by LSP (e.g., import errors, type mismatches) count as validation evidence — document them in the scorecard.

---

## Recursive Guardian Pattern

The guardian pattern is recursive. A guardian can watch:
- An S3 meta-orchestrator who spawns orchestrators who spawn workers (standard)
- Another guardian who is watching an S3 meta-orchestrator (meta-guardian)
- Multiple S3 meta-orchestrators in parallel (multi-initiative guardian)

Each level adds independent verification. The key constraint: each guardian stores its acceptance tests where the entity being watched cannot access them.

---

## Quick Reference

| Phase | Key Action | Reference |
|-------|------------|-----------|
| 0. BS Design | Write Business Spec (BS), ZeroRepo analysis, pipeline, design challenge | [references/phase0-prd-design.md](references/phase0-prd-design.md) |
| 1. Acceptance Tests | Gherkin rubrics + executable browser tests (Step 3) | [gherkin-test-patterns.md](references/gherkin-test-patterns.md) |
| 2. Orchestrator Spawn | DOT dispatch, SDK / tmux patterns, wisdom inject | [guardian-workflow.md](references/guardian-workflow.md) |
| 3. Monitoring | DOT polling (SDK), signal-file monitoring, progress monitoring | [monitoring-patterns.md](references/monitoring-patterns.md) |
| 3.5 Pipeline Progress | Haiku sub-agent monitoring with stall/failure detection | [monitoring-patterns.md](references/monitoring-patterns.md) |
| 3.6 Gate Monitoring | Detect wait.cobuilder/wait.human gates via .gate-wait markers, Guardian response handlers | [monitoring-patterns.md](references/monitoring-patterns.md) § Section 8 |
| 4. Validation | Score scenarios, run executable tests, weighted total. **ACCEPT ≥ 0.70** (solid quality; auto-create fix-it beads for minor gaps); **INVESTIGATE 0.50-0.69**; **REJECT < 0.50** | [validation-scoring.md](references/validation-scoring.md) |
| 4.5 Regression | ZeroRepo diff before journey tests | [references/validation-scoring.md](references/validation-scoring.md) |
| 4.6 Bead Closure | 6-step workflow: create fix-it bead → link to gap → assign → dispatch codergen node → validate → close | [guardian-workflow.md § 6.5](references/guardian-workflow.md) |

### Pipeline Progress Monitor Pattern

The Guardian spawns a lightweight Haiku 4.5 sub-agent to monitor pipeline progress after launching a pipeline. This **blocking** monitor sub-agent completes (waking the Guardian) only when attention is needed or after 10 minutes maximum. The monitor runs with `run_in_background=False` to ensure the Guardian waits for the results before continuing.

**Spawning Template**:
```python
Task(
    subagent_type="monitor",
    model="haiku",
    run_in_background=False,  # Blocking monitor (NOT background) - System 3 waits for result
    prompt=f"""Monitor pipeline progress for {pipeline_id} for a maximum of 10 minutes.

    Signal directory: {signal_dir}
    DOT file: {dot_file}
    Poll interval: 30 seconds
    Stall threshold: 5 minutes
    MAX_DURATION: 10 minutes - return status report regardless of state after 10 minutes

    Check signal files for new completions or failures.
    Check DOT file mtime for state transitions.
    COMPLETE immediately with a status report when:
    - A node fails (report which node and error)
    - No state change for >5 minutes (report last known state)
    - All nodes reach terminal state (report completion)
    - Any anomaly detected (unexpected state, missing signal files)
    - 10 minutes have elapsed (report current state and continue cycling)

    Do NOT attempt to fix issues. Just report what you observe.
    """
)
```

**Cyclic Monitoring Pattern**:
After each monitor completes, the Guardian analyzes the result and relaunches a new **blocking** monitor in a continuous cycle:
1. Guardian launches **blocking** monitor (`run_in_background=False`) - Guardian waits for results
2. Monitor runs for up to 10 minutes max or until event occurs (whichever comes first)
3. Monitor returns status report to the Guardian and **completes**
4. Guardian evaluates the report and decides next action
5. Guardian relaunches a new **blocking** monitor to continue watching

This creates a continuous monitoring cycle with predictable wake-up intervals and prevents monitors from running indefinitely. Each cycle has a maximum duration of 10 minutes, ensuring the Guardian remains responsive.

**Monitor Output Statuses**:
- `MONITOR_COMPLETE`: All nodes validated → Run final E2E, close initiative
- `MONITOR_ERROR`: Node failed → Investigate root cause, requeue or escalate
- `MONITOR_STALL`: No progress for >threshold → Check if worker hung, restart if needed
- `MONITOR_ANOMALY`: Unexpected state → Investigate, may need manual DOT edit
- `MONITOR_GATE_WAITING`: A `wait.cobuilder` or `wait.human` gate is active (`.gate-wait` marker detected) → Guardian handles gate response

**Monitoring Mechanism**:
- **Signal directory polling**: Monitor `.pipelines/signals/` for new/modified `.json` files with status changes
- **DOT file monitoring**: Track `.pipelines/pipelines/*.dot` mtime for state transitions
- **Stall detection**: If no state change for >stall_threshold (default 5 minutes), report stall

### Creating a New Pipeline

**MANDATORY PRE-FLIGHT: Before writing or editing ANY `.dot` pipeline file, you MUST load the reference first:**

```python
Read(".claude/skills/cobuilder-guardian/references/dot-pipeline-creation.md")
```

**This is a hard gate, not a suggestion.** The DOT format has strict schema requirements (hexagon shapes for gates, mandatory `gate_type` attributes, required 2-outbound edges on gates, required `sd_path` on codergen, required downstream `wait.human` nodes). Writing from memory WILL produce validation errors. The reference contains the exact schema, required attributes per handler, and a minimal working example.

**Do NOT skip this even if you have seen DOT files earlier in the session.** The "I remember this" rationalization is the #1 cause of DOT validation failures.

The reference covers:
- Minimal DOT example with full node types and attributes
- Handler type mapping (start, codergen, research, refine, wait.cobuilder, wait.human, exit)
- Required vs optional node attributes per handler
- Validation via `cli.py validate`

### TDD Pipeline Template (Alternative)

For initiatives with a test-driven workflow (RED → GREEN → REFACTOR per worker), use `Skill("cobuilder:tdd-pipeline")` instead of the standard `cobuilder-lifecycle` template. The TDD template generates three codergen nodes per worker task (write failing tests → minimal implementation → refactor) with automatic retry on validation failure. Instantiate via:

```bash
python3 cobuilder/templates/instantiator.py tdd-validated \
  --param prd_ref=PRD-{ID} --param sd_path=docs/sds/SD-{ID}.md \
  --param-file workers.yaml --output .pipelines/pipelines/{id}-tdd.dot
```

Workers in TDD pipelines receive `worker_powers` attributes that enable `Skill("worker-superpowers")` sub-skills (TDD, systematic debugging, verification). See the `cobuilder:tdd-pipeline` skill for workers YAML format and parameter reference.

### SDK Mode Entry Points

Two dispatch modes: **Pipeline (PRIMARY)** and **tmux (interactive)**.

| Mode | Command | When to Use |
|------|---------|------------|
| **Pipeline** | `python3 .claude/scripts/attractor/pipeline_runner.py --dot-file <path>` | Default for all DOT pipelines; uses AgentSDK to dispatch workers |
| **tmux** | `python3 .claude/scripts/attractor/spawn_orchestrator.py --mode tmux ...` | Interactive sessions requiring human observation (Max plan, no API cost) |

See **[references/guardian-workflow.md](references/guardian-workflow.md)** § "SDK Mode Entry Points" for:
- Full CLI command examples with wisdom file template
- 4-layer script hierarchy (guardian.py, runner.py, dispatch_worker.py, spawn_orchestrator.py)
- Detailed dispatch mode decision matrix

### Key Files

| File | Purpose |
|------|---------|
| `acceptance-tests/PRD-{ID}/manifest.yaml` | Feature weights, thresholds, metadata |
| `acceptance-tests/PRD-{ID}/*.feature` | Gherkin scenarios with scoring guides |
| `acceptance-tests/PRD-{ID}/executable-tests/` | Browser automation test scripts (UX PRDs) |
| `acceptance-tests/PRD-{ID}/design-challenge.md` | Phase 0 design challenge results |
| `scripts/generate-manifest.sh` | Template generator for new initiatives |

### Anti-Patterns

See **[references/guardian-workflow.md](references/guardian-workflow.md)** § "Anti-Patterns" for full list. Key categories: testing/validation, spawning, promise tracking, DOT pipeline design, and dispatch modes.

**The #1 Anti-Pattern: Urgency Bypass (Phase 1 Skip)**

```
❌ User: "Please immediately write a PRD and SD"
   Guardian: writes PRD → writes SD → dispatches orchestrator
   Result: No acceptance tests. Validation in Phase 4 has no rubric.

✅ User: "Please immediately write a PRD and SD"
   Guardian: writes PRD → GATE G1 fires → writes acceptance tests → writes SD → dispatches
   Result: Blind tests exist before implementation begins.
```

The user values correctness over speed. "Immediately" means "don't overthink it," not "skip the process." If the user truly wants to skip Phase 1, they must explicitly say so — and the guardian logs the skip to Hindsight as a deliberate override.

---

## Additional Resources

Load these reference files when entering each phase or when you need detailed guidance.

| Reference File | When to Load |
|---|---|
| [references/path-setup.md](references/path-setup.md) | Setting up cs-promise CLI PATH and shell invocation patterns |
| [references/session-promise-template.md](references/session-promise-template.md) | Creating and tracking completion promises (guardian validation, research, Business Spec (BS) design, etc.) |
| [references/hindsight-validation-checklist.md](references/hindsight-validation-checklist.md) | Storing validation results to Hindsight after Phase 4 |
| [references/phase0-prd-design.md](references/phase0-prd-design.md) | Phase 0: Business Spec (BS) authoring, pipeline creation, design challenge |
| [references/gherkin-test-patterns.md](references/gherkin-test-patterns.md) | Phase 1: Writing Gherkin acceptance tests and executable browser tests |
| [references/guardian-workflow.md](references/guardian-workflow.md) | Phase 2-3: Orchestrator spawning, monitoring patterns, intervention triggers |
| [references/validation-scoring.md](references/validation-scoring.md) | Phase 4: Independent validation, evidence gathering, gap closure protocol |
| [references/dot-pipeline-creation.md](references/dot-pipeline-creation.md) | Writing or editing DOT pipeline files manually, fixing validation errors from `cobuilder pipeline validate`, or understanding node shapes and required attributes |
| [references/gap-closure-protocol.md](references/gap-closure-protocol.md) | Phase 4.5: Autonomous closure of validation gaps via fix-it codergen nodes |
| [references/guardian-workflow.md](references/guardian-workflow.md) | Phase 2-3: Orchestrator spawning, monitoring patterns, intervention triggers, anti-patterns |

**DO NOT load all references at once.** Load on-demand as you progress through phases.

### Related CoBuilder Sub-Skills

The `cobuilder` parent skill provides orchestration-level sub-skills that complement the guardian workflow:

| Sub-Skill | Invoke As | When to Use |
|-----------|-----------|-------------|
| **ideation-to-execution** | `Skill("cobuilder:ideation-to-execution")` | Starting from a vague idea — structured brainstorming (Phase 1) → PRD (Phase 2) → SD (Phase 3) → worktree + pipeline (Phase 4) → autonomous pilot (Phase 5). Use Pre-Phase brainstorming before entering guardian Phase 0. |
| **tdd-pipeline** | `Skill("cobuilder:tdd-pipeline")` | Generating TDD-specific DOT pipelines with RED → GREEN → REFACTOR nodes per worker. Alternative to `cobuilder-lifecycle` template when test-driven workflow is preferred. |

**Worker-level powers** (TDD, debugging, verification) are in the separate `Skill("worker-superpowers")` — not loaded by the guardian directly, but referenced by pipeline node `worker_powers` attributes.

---

**Version**: 1.2.0
**Dependencies**: cs-promise CLI (requires PATH setup — see Prerequisites section), pipeline_runner.py + claude_code_sdk (primary dispatch), tmux (tmux mode — interactive, lower API cost), Hindsight MCP, ccsystem3 shell function, Task Master MCP, ZeroRepo
**Integration**: cobuilder-guardian skill, completion-promise skill, acceptance-test-writer skill, parallel-solutioning skill, research-first skill
**Theory**: Independent verification eliminates self-reporting bias in agentic systems

**Changelog**:
- v1.2.0: Cross-referenced `cobuilder` parent skill sub-skills. Added Pre-Phase (brainstorming via `Skill("cobuilder:ideation-to-execution")`) for sessions starting from vague ideas — structured discovery before Phase 0 BS authoring. Added TDD Pipeline Template section referencing `Skill("cobuilder:tdd-pipeline")` as alternative to cobuilder-lifecycle for test-driven workflows. Added "Related CoBuilder Sub-Skills" table to Additional Resources with `ideation-to-execution`, `tdd-pipeline`, and `worker-superpowers` cross-references. Root cause: guardian skill had no awareness of sibling cobuilder sub-skills, causing sessions to skip structured brainstorming and miss the TDD pipeline template option.
- v1.1.0: Added Phase Gates (G0→1, G1→2, G2→4) as mandatory structural checkpoints between phases. G1→2 (acceptance tests must exist before dispatch) is the most commonly skipped gate due to cognitive momentum. Added Mode Transition protocol (investigation → guardian) with TodoWrite checklist injection at transition point. Added `scripts/verify-phase-gate.py` for programmatic gate verification. Added "Urgency Bypass" anti-pattern documentation. Added Phase 0 → Phase 1 transition section to `phase0-prd-design.md`. Root cause: System 3 skipped Phase 1 (blind acceptance tests) when user asked for "PRD and SD" in one breath — cognitive momentum overrode the process.
- v1.0.0: Terminology migration — prose-level renaming only. "PRD" → "Business Spec (BS)" and "Solution Design/SD" → "Technical Spec (TS)" throughout descriptive prose in SKILL.md and all reference files. Code identifiers (`prd_ref`, `sd_path`), file-identifier strings like `PRD-XXX-001`, historical changelog entries, and content inside code blocks are unchanged. New spec file paths: `docs/specs/business/` (BS) and `docs/specs/technical/` (TS) for future specs; historical specs remain in `docs/prds/` and `docs/sds/`.
- v0.9.0: Added Phase 5 (Session Closing Protocol) as mandatory final phase. PRD/SD implementation status updates and bead closure are now an atomic operation — never one without the other. This ensures source documents remain the single source of truth for progress tracking.
- v0.8.0: Added validation acceptance thresholds (ACCEPT ≥ 0.70, INVESTIGATE 0.50-0.69, REJECT < 0.50) and bead closure process references throughout. Updated `description` field with autonomous threshold-based accept/reject capability and new trigger keywords ("validation thresholds", "gradient scoring decision", "bead creation for gaps"). Expanded Phase 4 row in Guardian Workflow Phases table with threshold summary and references to guardian-workflow.md §§ 5.X and 6.5. Added Phase 4.6 Bead Closure row to Quick Reference table. Bumped `last_verified` to 2026-03-09.
- v0.7.0: Removed headless mode (`--mode headless`, `spawn_orchestrator.py --mode headless`, `_build_headless_worker_cmd`, `run_headless_worker`). Headless mode is dead code — all dispatch now uses AgentSDK via `pipeline_runner.py`. Updated architecture diagram, mode table, SDK Mode Entry Points section, dependencies line. Deleted test_headless_dispatch.py and test_headless_worker.py. Two dispatch modes remain: Pipeline (PRIMARY) and tmux (interactive). Root cause: no API credits, headless = `claude -p` = API-billed, made it dead code.
- v0.5.2: Corrected dispatch model throughout. `pipeline_runner.py --dot-file` is the PRIMARY dispatch path and uses **AgentSDK** (`claude_code_sdk`) — NOT `claude -p`. Seeing `claude` in `ps` when pipeline_runner runs is normal SDK behavior (SDK internally shells to the claude binary). `claude -p` is ONLY used by `spawn_orchestrator.py --mode headless` (legacy). Updated architecture diagram, mode table, anti-patterns, and dependencies line. Root cause: System 3 misread `ps` output and incorrectly concluded pipeline_runner uses `claude -p` — the process signature looks identical but the dispatch layer is entirely different.
- v0.5.1: Rebalanced mode descriptions — tmux is equal peer to headless, not deprecated/legacy. Removed "Default for workers" label from headless. Added explicit tmux spawn command example in Quick Reference with wisdom file template. Updated system3-meta-orchestrator.md to remove "legacy tmux" and "for debugging only" language. Root cause: recent tmux-as-legacy language in docs caused orchestrator prompts to drop mandatory `Skill("orchestrator-multiagent")` invocation, resulting in direct implementation instead of delegation to workers.
- v0.6.0: 3-layer attractor consolidation. Created `guardian.py` (composes launch_guardian + guardian_agent), `runner.py` (composes spawn_runner + runner_agent with `--spawn` mode), `dispatch_worker.py` (extracted headless functions from spawn_orchestrator.py). Guardian system prompt now references `runner.py --spawn` instead of `spawn_runner.py`. Old files untouched — backward-compatible re-exports from spawn_orchestrator.py. Zero test breakage (987 tests pass).
- v0.5.0: Added headless CLI worker mode (Epic 6). Workers run via `claude -p` with Three-Layer Context: ROLE (--system-prompt from .claude/agents/), TASK (-p prompt), IDENTITY (env vars). New functions: `_build_headless_worker_cmd()` and `run_headless_worker()` in dispatch_worker.py (re-exported from spawn_orchestrator.py). `--mode headless` added to runner.py, spawn_orchestrator.py, and guardian_agent.py system prompt. tmux mode deprecated in favor of headless. JSON output parsing replaces tmux capture-pane monitoring.
- v0.4.4: Broadened Step 0 promise creation with work-type-aware decision table (research, PRD design, implementation, maintenance, multi-initiative — not just guardian validation). Added SDK Mode Entry Points section to Quick Reference with 4-layer CLI table and SDK-vs-tmux guidance. Qualified Session Promise Integration heading to clarify it's the guardian validation template. Root cause: non-standard sessions (research, PRD writing) had no promise template guidance, and SDK CLI parameters were undiscoverable without running `--help`.
- v0.4.3: Documented research-only pipeline dispatch. Added "Research-Only Pipeline Dispatch" section to guardian-workflow.md with dispatch hierarchy diagram, example DOT file, exact CLI command, and internal behavior walkthrough. Added anti-pattern for calling `run_research.py` per-node instead of using `launch_guardian.py`. Updated SKILL.md architecture diagram to acknowledge research-only as a valid pipeline topology. Root cause: colleague tried to run 4 research nodes via parallel `run_research.py` calls (exit code 2) instead of launching the guardian runner.
- v0.4.2: Added mandatory research→refine→codergen chain validation to Step 0.2 (bare codergen nodes now fail validation). Added two AskUserQuestion checkpoints to Phase 0 — Checkpoint A (after pipeline creation + chain validation) presents PRD/SD/pipeline summary; Checkpoint B (after design challenge) presents architect verdict. Both offer contextual next-step options. Prevents silent misalignment during long autonomous Phase 0 runs.
- v0.4.1: Added refine node pattern (`handler="refine"`, `shape=note`) — runs AFTER research to rewrite SD with findings as first-class content, removing inline annotations. Uses Sonnet with mandatory Hindsight reflection before editing. Pipeline flow: `research (Haiku) → refine (Sonnet) → codergen`. Added `run_refine.py` with restricted tools (Read/Edit/Write/Hindsight only). Added anti-pattern for research-without-refine. Updated guardian-workflow.md with Refine Nodes section, pre-flight checklist, and updated DOT examples.
- v0.4.0: Added research node pattern (`handler="research"`, `shape=tab`) — mandatory pre-implementation gates that validate framework patterns via Context7/Perplexity and update Solution Design documents. Added SDK-mode dispatch (4-layer: launch_guardian → guardian → runner → orchestrator, all headless via claude_code_sdk). Added 2 new anti-patterns (missing research node, docs-vs-local version mismatch). Updated architecture diagram and guardian-workflow reference. Validated E2E: PydanticAI web search agent pipeline completed all 5 nodes via SDK mode.
- v0.3.0: Progressive disclosure refactor — moved Phase 0-4 content to `references/` directory. SKILL.md now acts as a routing table (~400 lines) that points to detailed reference docs loaded on demand. Reduces cold-start context by ~8,000 words.
- v0.2.1: Replaced inline Bash spawn sequence with mandatory `spawn_orchestrator.py` usage. Added "Mandatory 3-Step Boot Sequence" section. Added "Anti-Pattern: Ad-Hoc Bash Spawn" with real-world example showing 5 violations. Added 3 new anti-patterns to table. Root cause: inline Bash in Phase 2 invited copy-paste adaptation that dropped ccorch, /output-style, and Skill("orchestrator-multiagent").
- v0.2.0: Added Phase 0 (PRD Design & Challenge) with ZeroRepo analysis, Task Master parsing, beads sync, and mandatory design challenge via parallel-solutioning + research-first. Added executable browser test scripts (Phase 1, Step 3) for UX PRDs with claude-in-chrome MCP tool mapping. Updated promise template with AC-0. Added 4 new anti-patterns. Lesson learned: PRD-P1.1-UNIFIED-FORM-001 had 17 Gherkin scoring rubrics but zero executable tests — the guardian could not automatically verify browser behavior.
- v0.1.0: Initial release — blind Gherkin acceptance tests, tmux monitoring, gradient confidence scoring, DOT pipeline integration, SDK mode.
