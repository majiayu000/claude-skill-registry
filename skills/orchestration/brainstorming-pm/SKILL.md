---
name: brainstorming-pm
description: >
  Use when orchestrating multi-perspective brainstorming sessions requiring
  parallel agent execution, confidence-weighted synthesis, and optional
  workflow handoff. Coordinates 5 parallel perspective agents through a
  4-stage pipeline (framing, diverging, converging, output).
version: 1.0.0
tags: [orchestrator, brainstorming, multi-agent, synthesis, parallel]

handoff:
  accepts_handoff: true
  handoff_categories: [analysis, creative]
  handoff_description: "Multi-perspective brainstorming with 5 parallel agents (15-30 minutes)"
  handoff_trigger: "--handoff {payload_path}"
  protocol_version: "2.0"
  requires:
    - context.original_prompt
    - context.problem_type
  optional_consumes:
    - context.synthesis_summary
    - research_seeds.suggested_terms
    - insights.uncertainties

prerequisites:
  - A clear question, decision, problem, or creative challenge from the user
  - Understanding of the perspective-swarm protocol (references included)
success_criteria:
  - 5 parallel perspective agents launched and at least 4 complete
  - Confidence-weighted synthesis produced with convergent and divergent insights
  - User presented with actionable options (accept, refine, handoff)
  - Total workflow completes within 45-minute safety ceiling
estimated_duration: 15-30 minutes
---

# brainstorming-pm

Tier 1 orchestrator skill that executes the perspective-swarm protocol: a 4-stage pipeline producing confidence-weighted multi-perspective analysis through 5 parallel agents. This skill owns session management, tool selection, agent delegation, model selection, and user interaction for the entire brainstorming workflow.

**Protocol specification**: See `../perspective-swarm/SKILL.md` for the complete protocol definition (stages, archetypes, state machine, quality gates, operational parameters).

**Architecture navigation**: This skill (brainstorming-pm) is the executable entry point. The protocol spec (perspective-swarm) defines *what* happens. This skill defines *how* it happens. Reference documents under `../perspective-swarm/references/` provide detailed algorithms and schemas shared between the two.

## When to Use

- A user needs diverse viewpoints on a decision, problem, or creative challenge
- Time is limited (15-30 minutes) but rigorous multi-angle analysis is needed
- The goal is to identify both consensus themes and unique insights
- The problem benefits from optimistic, critical, analytical, innovative, and pragmatic lenses

## When NOT to Use

- Deep literature review is needed (use `lit-pm` instead)
- Single-perspective analysis is sufficient
- Implementation or execution is the goal (this produces analysis only)
- Domain-specific expertise is required (this uses general archetypes)
- The user has already received a multi-perspective analysis and wants to refine a single angle

## Delegation Mandate

You are an orchestrator. You coordinate perspective agents -- you do not generate perspectives yourself.

**What the orchestrator DOES:**
- Session setup (directory creation, lock files, state initialization)
- Problem framing (Stage 1, performed inline)
- Tool invocation (launching Task agents for Stage 2)
- Quality gate evaluation (checking outputs against required criteria)
- Convergence synthesis (Stage 3, performed inline -- this is the exception)
- User communication (presenting options, collecting feedback)
- State management (reading/writing workflow-state.yaml)
- Workflow discovery and handoff coordination (Stage 3-4)

**What the orchestrator DOES NOT DO:**
- Generate perspective content (delegate to Task agents)
- Conduct web research for perspectives (agents do their own research)
- Adopt persona lenses (Optimist, Critic, etc.)
- Make decisions on behalf of the user

**Exception**: Stage 3 convergence analysis (including LLM-based grouping) is performed inline by the orchestrator because it requires cross-perspective analysis that cannot be delegated to a single perspective agent. This is analysis *of* perspectives, not a perspective itself.

**Self-check**: Before executing any substantive content generation, ask: "Am I about to adopt a perspective myself?" If yes, delegate via Task tool instead.

## Tool Selection

| Situation | Tool | Rationale |
|-----------|------|-----------|
| Stage 2: Launch perspective agents | Task tool (5 concurrent) | Parallel execution required; each agent is independent |
| Stage 3: Convergence analysis | Inline (no tool) | Cross-perspective synthesis cannot be delegated to one agent |
| Stage 3: LLM grouping | Inline (no tool) | Simple structured output call; no delegation needed |
| Stage 3: Workflow discovery | Inline (file-system scan) | No LLM involved; fast directory scan |
| Stage 4: Handoff invocation | Skill tool | Target skill invocation with payload |

**Self-check prompt**: "Am I about to use Task tool for something I should do inline (convergence, state management), or about to do inline something I should delegate (perspective generation)?"

## Model Selection

Model selection is currently advisory. All components inherit the orchestrator's model because the Task tool does not yet support explicit model selection.

| Component | Current | Target |
|-----------|---------|--------|
| Orchestrator | Inherited | Claude Opus 4.5 |
| Perspective Agents | Inherited | Claude Sonnet 4.5 |
| LLM Grouping | Inherited (inline) | Claude Haiku 4.5 |

For full rationale and fallback chains, see `references/model-selection.md`.

**Note**: When the Task tool gains a `model` parameter, update Stage 2 Task invocations to specify `claude-sonnet-4-5` and Stage 3 grouping calls to specify `claude-haiku-4-5`.

## State Anchoring

Start every response with: `[Stage N/4 - {stage_name}] {brief status}`

Before starting any stage:
1. Read `workflow-state.yaml` from the session directory
2. Confirm current_state matches the expected state for the stage about to begin
3. If mismatch: diagnose (stale state? crashed mid-stage?) and offer user resume/restart options

After any user interaction: re-anchor to the current stage by re-reading workflow-state.yaml and re-stating the stage header.

## Archival Compliance

On invocation, check for handoff context:
1. If invoked via `--handoff {payload_path}`: read the handoff payload and extract `context.original_prompt`, `context.problem_type`, and any optional fields into Stage 1 inputs
2. Check for `.archive-metadata.yaml` in the working directory for archival context
3. Follow the same archival patterns as `technical-pm` (fallback to `.archive-metadata.yaml` if no handoff payload)

## Invocation

```
# Direct invocation with a question
brainstorming-pm "Should we pivot our product to focus on the European market?"

# Invocation via handoff from another skill
brainstorming-pm --handoff {payload_path}

# Resume a previous session
brainstorming-pm --resume {workflow_id}
```

---

## Stage-by-Stage Orchestration

### Stage 1: Framing (2-5 minutes)

**Preconditions**: User has provided a prompt (or handoff payload received).

**Actions** (performed inline by orchestrator):
1. Validate user prompt: minimum 10 characters, maximum 1000 characters, at least one clear question or challenge, no prohibited content
2. Identify problem type: `decision | creative | analytical | strategic`
3. Reframe challenge in neutral language (no leading or biasing)
4. Generate 5 archetype-specific prompts using `../perspective-swarm/references/persona-archetypes.md` templates
5. Create session directory: `/tmp/swarm-session-{YYYYMMDD}-{HHMMSS}-{uuid4-8char}/`
6. Create session lock: write `.session.lock` with `workflow_id` and ISO8601 timestamp
7. Initialize `workflow-state.yaml` with `current_state: FRAMING`
8. Save framing output: `stage-1-framing.yaml`

**Quality Gate**:
- [ ] Problem clearly articulated
- [ ] All 5 agent prompts generated
- [ ] No leading/biasing language in reframed challenge

**Optional Checkpoint**: Present reframed challenge to user before proceeding.
- On approve: continue to Stage 2
- On refine: re-enter framing with user feedback
- On abort: update state to ABORTED, release session lock, inform user

**State Update**: `current_state: FRAMING -> DIVERGING` (on gate pass)

### Stage 2: Parallel Perspective Generation (5-15 minutes)

**Preconditions**: Stage 1 complete. 5 archetype prompts generated. Session directory exists.

**Actions**:
1. Launch 5 Task tool invocations concurrently. Each Task receives:
   - Archetype persona instructions (from `../perspective-swarm/references/persona-archetypes.md`)
   - Reframed challenge text
   - Session directory path and output location (`perspectives/{archetype}.md`)
   - Research guidance: "Conduct 1-2 WebSearch queries to support your analysis"
   - Output format requirements: key insight (1-2 sentences), supporting evidence (2-3 bullets with sources), confidence level (1-5, self-assessed), blind spots acknowledged
   - Token target: ~2000 tokens (advisory)

2. Maintain status board and display to user:
   ```
   [Stage 2/4 - DIVERGING] Parallel perspectives in progress

   | Agent      | Status      | Elapsed |
   |------------|-------------|---------|
   | Optimist   | complete    | 6:30    |
   | Critic     | in_progress | 8:15    |
   | Analyst    | complete    | 7:45    |
   | Innovator  | timeout     | 10:00   |
   | Pragmatist | complete    | 8:00    |
   ```

3. Apply timeouts: 10 minutes per agent, 15 minutes stage total (wall-clock ceiling shared by all concurrent agents)

**Quality Gate (per agent)**:
- [ ] Key insight present (required)
- [ ] At least 1 evidence point (required)
- [ ] Confidence level 1-5 (required; clamp if out of range)
- [ ] Blind spots acknowledged (required)

**Minimum agents required**: 4 of 5

**On < 4 agents completing**: Present user options:
```
PERSPECTIVE GENERATION INCOMPLETE: Only {N} of 5 agents completed

Completed: {list}
Failed: {list with reasons}

Options:
(A) Retry failed agents (estimated +5 min)
(B) Abort workflow
```
Note: "Proceed with N perspectives" is only offered when N >= 2. When N = 0 or N = 1, only retry or abort are available because meaningful convergence analysis requires at least 2 perspectives.

**On >= 4 agents completing**: Proceed automatically to Stage 3.

**On 4 agents completing (1 failed/timed out)**: Present user options:
```
4 of 5 perspectives complete. 1 failed: {archetype} ({reason})

Options:
(A) Retry {archetype} (estimated +5 min)
(B) Proceed with 4 perspectives (reduced diversity)
(C) Abort workflow
```

**State Update**: Record each agent's completion status, confidence, search success in `workflow-state.yaml`. Then `current_state: DIVERGING -> CONVERGING`.

### Stage 3: Convergence + Parallel Discovery (5-10 minutes)

**Preconditions**: Stage 2 complete. At least 4 perspective outputs available.

The orchestrator executes two parallel tracks during Stage 3:
- **Track A** (primary, blocking): Convergence analysis
- **Track B** (secondary, non-blocking): Workflow discovery

Track B is non-blocking with respect to Track A: convergence analysis proceeds regardless of discovery status. At the Stage 3/4 transition, if discovery has not completed, the orchestrator waits up to 30 seconds before proceeding without cached results.

#### Track A: Convergence Analysis (inline)

1. Collect all perspective outputs from `perspectives/*.md`
2. Extract key insights, confidence levels, evidence, and research-backed status from each
3. Perform LLM-based semantic grouping (see `../perspective-swarm/references/convergence-algorithm.md`, Step 2a for implementation details including JSON schema and fallback triggers)
4. Apply convergence scoring algorithm (see `../perspective-swarm/references/convergence-algorithm.md`, Steps 3-5)
5. The convergence analysis identifies convergent insights (themes appearing in 2+ perspectives) with confidence weighting
6. Divergent insights (unique to single perspectives) are attributed to their originating archetype
7. Handle missing archetypes using the compensation table in the protocol spec
8. Conflicts are presented neutrally -- do not force artificial consensus
9. Generate `stage-3-synthesis.md`

#### Track B: Workflow Discovery (parallel)

1. Run workflow discovery algorithm per `../perspective-swarm/references/workflow-discovery.md`
2. Cache results to `available-workflows.yaml`
3. Self-exclusion: filter out `brainstorming-pm` and `perspective-swarm` from discovery results (prevent self-handoff)
4. Relevance scoring is deferred to Stage 4 (requires synthesis content)

**Quality Gate**:
- [ ] All available perspectives incorporated
- [ ] At least 2 convergent insights OR explicit "portfolio of options" framing
- [ ] At least 3 divergent insights captured
- [ ] Conflicts presented neutrally
- [ ] Discovery results cached (or explicitly noted as unavailable)

**State Update**: Record `convergent_count`, `divergent_count`, `grouping_method`, `grouping_latency_ms`, and `discovery` status in `workflow-state.yaml`. Then `current_state: CONVERGING -> AWAITING_USER`.

### Stage 4: User Review + Handoff

**Preconditions**: Stage 3 complete. Synthesis document generated. Discovery results available from Stage 3 (cached in `available-workflows.yaml`). If Stage 3 discovery did not complete, the orchestrator runs discovery synchronously (5-second timeout) before presenting options.

**Actions**:
1. Score discovered workflows for relevance against synthesis content (see `../perspective-swarm/references/workflow-discovery.md`, Relevance Scoring Algorithm)
2. The orchestrator presents synthesis to user with options:

```
[Stage 4/4 - OUTPUT] Synthesis Complete

[Executive summary of convergent and divergent insights]

Options:
(A) Accept - Workflow complete
(B) Refine - Provide feedback, return to Stage 3

Continue with another workflow:
(C) [research] lit-pm - Comprehensive literature review (4-24 hours)
(D) [implementation] programming-pm - Software implementation (2-8 hours)
```

3. Handle user choice:
   - **Accept**: `current_state -> COMPLETED`. Archive session.
   - **Refine**: `current_state -> CONVERGING`. Capture user feedback. Loop back to Stage 3 with feedback incorporated into synthesis.
   - **Handoff (C/D/...)**: Validate target skill still available. Generate `handoff-payload.yaml` per `../perspective-swarm/references/handoff-schema.md`. Invoke target skill with payload path. `current_state -> COMPLETED` on successful handoff.

**State Update**: Record `user_decision`, any `refinement_feedback`, and `handoff_target` in `workflow-state.yaml`.

---

## Session Management

Session directory structure and lock protocol are defined in the perspective-swarm protocol spec (`../perspective-swarm/SKILL.md`, "Session Directory Structure" and "Session Lock Protocol" sections). The orchestrator follows those specifications exactly.

**Atomic writes**: All writes to `workflow-state.yaml` must use the atomic write pattern:
1. Write complete state to a `.tmp` file
2. Validate YAML syntax of the `.tmp` file
3. Rename `.tmp` to target path (`workflow-state.yaml`)
4. Retain `.bak` of previous version

The orchestrator reads the complete state file, updates relevant fields in memory, and writes the complete file atomically. File-level replace semantics, not field-level merge.

**Session recovery**: On invocation, the orchestrator checks for existing sessions in `/tmp/swarm-session-*/`. See the protocol spec for the recovery prompt format and options (Resume / Start fresh / Cancel).

## Error Handling

### WebSearch Failure

Classification and handling follow the protocol spec (see `../perspective-swarm/SKILL.md`, "Error Handling" section):
- **Transient**: retry after 30 seconds
- **Rate limited**: exponential backoff (30s, 60s, 120s)
- **No results**: proceed without search, note "limited research"
- **Service down**: proceed with reasoning-only, reduce confidence by 1

### Agent Timeout

- Per-agent timeout: 10 minutes. Mark as timed out, proceed with available agents.
- Stage 2 total timeout: 15 minutes. Hard ceiling for all agent completion.
- If < 4 agents complete after timeout: present user options (retry/abort).

### Catastrophic Failure

- < 4 agents complete AND user chooses abort: `current_state -> FAILED`
- Unrecoverable error at any stage: `current_state -> FAILED`, preserve session for debugging
- Global 45-minute safety ceiling: escalate to user regardless of stage

## Timeout Summary

| Stage | Timeout | Action on Timeout |
|-------|---------|-------------------|
| 1 (Framing) | 5 min | Escalate to user |
| 2 (Perspectives) | 15 min total | Proceed with available (min 4) |
| 2 (per agent) | 10 min | Mark incomplete, proceed |
| 3 (Synthesis) | 10 min | Deliver partial synthesis |
| 3 (Discovery) | 30 sec wait + 5 sec sync | Proceed without cached results |
| 4 (User Review) | No timeout | User-controlled |
| Global | 45 min | Safety ceiling, escalate |

## Handoffs

| Condition | Hand Off To |
|-----------|-------------|
| User accepts synthesis (Stage 4, option A) | User (workflow complete) |
| User requests deeper research (Stage 4, option C+) | Discovered workflow target (via handoff payload) |
| User aborts at any stage | User (session preserved for potential resume) |

**Incoming handoff**: When invoked via `--handoff {payload_path}`, extract `context.original_prompt` and `context.problem_type` from the payload. Map optional fields (`synthesis_summary`, `suggested_terms`, `uncertainties`) to Stage 1 framing inputs. Proceed directly to Stage 1 with pre-populated context.

## References

- [perspective-swarm/SKILL.md](../perspective-swarm/SKILL.md) - Protocol specification (stages, archetypes, state machine, quality gates)
- [persona-archetypes.md](../perspective-swarm/references/persona-archetypes.md) - Archetype definitions and prompt templates
- [convergence-algorithm.md](../perspective-swarm/references/convergence-algorithm.md) - Convergence scoring and LLM grouping implementation
- [workflow-state-schema.md](../perspective-swarm/references/workflow-state-schema.md) - Session state format and schema
- [handoff-schema.md](../perspective-swarm/references/handoff-schema.md) - Generic handoff payload format (v2.0)
- [workflow-discovery.md](../perspective-swarm/references/workflow-discovery.md) - Handoff target discovery algorithm
- [model-selection.md](references/model-selection.md) - Model selection guidance and fallback chains
- [strategic-decision-example.md](examples/strategic-decision-example.md) - Complete orchestration walkthrough
