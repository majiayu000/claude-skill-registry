---
name: perspective-swarm
description: Protocol specification for multi-perspective brainstorming via 5 parallel agents with confidence-weighted synthesis. Executed by brainstorming-pm orchestrator.
version: 1.0.0
tags: [brainstorming, multi-agent, synthesis, parallel, decision-support]
orchestrator: brainstorming-pm
---

# perspective-swarm

Enable rapid multi-perspective brainstorming through parallel agent execution, producing a confidence-weighted synthesis that surfaces convergent insights and divergent alternatives.

## Protocol Status

**Document type**: Protocol specification
**Orchestrator**: `brainstorming-pm/SKILL.md`

This document defines the perspective-swarm protocol: the stages, archetypes, state machine, quality gates, and operational parameters for multi-perspective brainstorming. It is a declarative specification, not an executable skill.

For orchestration and execution, see `brainstorming-pm/SKILL.md`, which handles session management, tool selection, agent delegation, model selection, and user interaction.

Handoff metadata (discovery, categories, payload schema) is defined in the brainstorming-pm skill, which is the discoverable entry point for this workflow.

## When to Use

- You need diverse viewpoints on a decision, problem, or creative challenge
- Time is limited (15-30 minutes) but you want rigorous multi-angle analysis
- You want to identify both consensus themes and unique insights
- The problem benefits from optimistic, critical, analytical, innovative, and pragmatic lenses

## When NOT to Use

- Deep literature review needed (use lit-pm instead)
- Single-perspective analysis is sufficient
- Implementation or execution is the goal (this produces analysis only)
- Domain-specific expertise required (this uses general archetypes)

## Workflow Overview

```
                  User
                  Prompt
                    |
           +-------v-------+
           | Stage 1:      | Frame problem, validate input
           | FRAMING       | Generate 5 agent prompts
           +-------+-------+
                   |
                   | [Optional: User confirms framing]
                   |
+------------------v-----------------------------------+
| Stage 2: DIVERGING (Parallel)                       |
| +-----+ +-----+ +-----+ +-----+ +-----+             |
| |Opt. | |Crit.| |Anal.| |Innov| |Prag.|             |
| +--+--+ +--+--+ +--+--+ +--+--+ +--+--+             |
+----+-------+-------+-------+-------+-----------------+
     +-------+-------+-------+-------+
                     |
              +------v------+
              | Stage 3:    | Identify convergent/divergent insights
              | CONVERGING  | Apply confidence weighting
              +------+------+
                     |
              +------v------+
              | Stage 4:    | Present synthesis
              | OUTPUT      | Accept / Refine / Handoff to workflow
              +-------------+
```

## Detailed Workflow

### Stage 1: Problem Framing (2-5 minutes)

**State**: FRAMING

1. **Validate user prompt**:
   - Minimum 10 characters
   - Maximum 1000 characters
   - At least one clear question or challenge
   - No prohibited content

2. **Identify problem type**: decision | creative | analytical | strategic

3. **Reframe challenge** in neutral language (no leading/biasing)

4. **Generate 5 archetype-specific prompts** (see references/persona-archetypes.md)

5. **Create session directory**: `/tmp/swarm-session-{YYYYMMDD}-{HHMMSS}-{uuid4-8char}/`
   - `{uuid4-8char}` is the first 8 characters of a uuid4 (e.g., `a1b2c3d4`)

6. **Create session lock**: Write `.session.lock` file with workflow_id and timestamp
   - Lock prevents concurrent access to same session
   - Stale locks (> 30 minutes) may be overwritten

7. **Save framing output**: `stage-1-framing.yaml`

**Quality Gate**:
- [ ] Problem clearly articulated
- [ ] All 5 agent prompts generated
- [ ] No leading/biasing language in framing

**Optional Checkpoint**: Present reframed challenge to user before proceeding to Stage 2. User can:
- Approve and continue
- Refine the framing
- Abort

### Stage 2: Parallel Perspective Generation (5-15 minutes)

**State**: DIVERGING

The orchestrator launches 5 parallel agents via Task tool. Each agent:

1. **Adopts archetype lens** (Optimist, Critic, Analyst, Innovator, Pragmatist)

2. **Conducts brief research**: 1-2 WebSearch queries
   - On WebSearch failure: proceed with reasoning-only, reduce confidence by 1

3. **Generates perspective report** (target ~2000 tokens):
   - Key insight (1-2 sentences)
   - Supporting evidence (2-3 bullet points with sources)
   - Confidence level (1-5, self-assessed)
   - Blind spots acknowledged

4. **Saves output**: `perspectives/{archetype}.md`

**Token Budget Note**: The 2000 token target is advisory. Agents are instructed to target ~2000 tokens but enforcement is prompt-based only. Slight overages are acceptable; significant overages should be flagged in validation warnings.

**Timeouts**:
- Per-agent: 10 minutes
- Stage total: 15 minutes
- On timeout: Mark incomplete, proceed with available

**Quality Gate (per agent)**:
- [ ] Key insight present (required)
- [ ] At least 1 evidence point (required)
- [ ] Confidence level 1-5 (required, clamp if out of range)
- [ ] Blind spots acknowledged (required)

**Minimum agents required**: 4 of 5

**On < 4 agents**: The orchestrator presents user options:
```
PERSPECTIVE GENERATION INCOMPLETE: Only {N} of 5 agents completed

Completed: {list}
Failed: {list with reasons}

Options:
(A) Retry failed agents (estimated +5 min)
(B) Proceed with {N} perspectives (reduced diversity)
(C) Abort workflow
```

### Stage 3: Convergence Analysis & Synthesis (5-10 minutes)

**State**: CONVERGING

During Stage 3, the orchestrator executes two parallel tracks: (A) convergence analysis (primary), and (B) workflow discovery (secondary, non-blocking). See `references/workflow-discovery.md` for parallel execution details.

1. **The orchestrator collects all perspective outputs**

2. **The convergence analysis identifies convergent insights**:
   - Themes appearing in 2+ perspectives
   - Apply confidence weighting (see references/convergence-algorithm.md)

3. **Identify divergent insights**:
   - Unique insights from single perspectives
   - Attribute to originating archetype

4. **Handle missing archetypes** (if 4 agents):
   | Missing | Compensation |
   |---------|--------------|
   | Optimist | Add: "Consider opportunities we may be missing" |
   | Critic | Add explicit risk caveat section |
   | Analyst | Note reduced quantitative rigor |
   | Innovator | Note potentially conservative recommendations |
   | Pragmatist | Flag implementation feasibility as uncertain |

5. **Conflicts are presented neutrally**:
   - All sides shown with evidence strength noted
   - No forced artificial consensus

6. **The orchestrator generates the synthesis document**: `stage-3-synthesis.md`

**Quality Gate**:
- [ ] All available perspectives incorporated
- [ ] At least 2 convergent insights OR explicit "portfolio of options" framing
- [ ] At least 3 divergent insights captured
- [ ] Conflicts presented neutrally
- [ ] Blind spots aggregated

### Stage 4: User Review & Optional Handoff

**State**: AWAITING_USER

**Pre-requisite**: Discovery results available from Stage 3 (cached in `available-workflows.yaml`). If Stage 3 discovery did not complete, the orchestrator runs discovery synchronously (5-second timeout) before presenting options.

The orchestrator presents synthesis to user with options:

```
## Synthesis Complete

[Executive summary]

**Core Options:**
(A) Accept - Workflow complete
(B) Refine - Provide feedback, return to Stage 3

**Continue with another workflow:**
{If handoff-eligible workflows found, display top 3-5 by relevance}

Example output when workflows available:
(C) [research] lit-pm - Comprehensive literature review (4-24 hours)
(D) [implementation] programming-pm - Software implementation (2-8 hours)
(E) [creative] pov-expansion - Cross-domain perspective analysis (2-3 hours)

Example output when NO workflows found:
---
No handoff-eligible workflows detected.
To enable handoffs, add `handoff:` metadata to skill SKILL.md files.
See: references/workflow-discovery.md
---

Select an option:
```

**On Accept**: State -> COMPLETED
**On Refine**: State -> CONVERGING (with user feedback)
**On Handoff (C/D/E...)**:
1. Validate selected workflow still available
2. Generate handoff-payload.yaml (see references/handoff-schema.md)
3. Invoke target skill with payload path
4. State -> COMPLETED (on successful handoff)

**Relevance Scoring**: Workflows are ranked by relevance to synthesis content:
- Category match to problem_type: +3 points
- High uncertainty signals + research category: +2 points
- Implementation keywords + implementation category: +2 points
- Low convergence + research category: +2 points
- Project-scope workflows: +1 point priority bonus

## Session Directory Structure

```
/tmp/swarm-session-{YYYYMMDD}-{HHMMSS}-{uuid4-8char}/
├── .session.lock                   # Prevents concurrent access
├── workflow-state.yaml             # Resumable state
├── stage-1-framing.yaml            # Problem framing output
├── perspectives/                   # Parallel outputs
│   ├── optimist.md
│   ├── critic.md
│   ├── analyst.md
│   ├── innovator.md
│   └── pragmatist.md
├── stage-3-synthesis.md            # Final synthesis
├── available-workflows.yaml        # Discovered handoff targets (cached)
└── handoff-payload.yaml            # (if handoff requested)
```

## State Machine

```
States: INITIALIZED | FRAMING | DIVERGING | CONVERGING | AWAITING_USER | COMPLETED | FAILED | ABORTED

Transitions:
  INITIALIZED -> FRAMING     : on session start
  FRAMING -> DIVERGING       : on framing complete (+ optional user confirmation)
  DIVERGING -> CONVERGING    : on min 4 agents complete
  DIVERGING -> FAILED        : on < 4 agents AND user chooses abort
  CONVERGING -> AWAITING_USER: on synthesis complete
  AWAITING_USER -> CONVERGING: on user refinement request
  AWAITING_USER -> COMPLETED : on user accept
  AWAITING_USER -> COMPLETED : on successful lit-pm handoff
  ANY -> ABORTED             : on user abort
  ANY -> FAILED              : on unrecoverable error
```

Note: The state machine has 8 states total (INITIALIZED, FRAMING, DIVERGING, CONVERGING, AWAITING_USER, COMPLETED, FAILED, ABORTED).

## Session Lock Protocol

On session initialization:
1. Create `.session.lock` file in session directory
2. Write content: `{workflow_id}\n{ISO8601_timestamp}`
3. Before any operation, verify lock file matches current workflow_id

On resume detection:
1. Check if `.session.lock` exists
2. If lock timestamp > 30 minutes old, consider stale and overwritable
3. If lock is fresh (< 30 minutes), warn user that session may be in use

```yaml
# .session.lock format
workflow_id: swarm-20260204-183000-a1b2c3d4
locked_at: 2026-02-04T18:30:00Z
```

## Error Handling

### WebSearch Failure

```yaml
classification:
  transient: retry after 30 seconds
  rate_limited: exponential backoff (30s, 60s, 120s)
  no_results: proceed without search, note "limited research"
  service_down: proceed with reasoning-only, reduce confidence by 1

fallback_behavior:
  - Agent proceeds with pure reasoning
  - Marks output as "unverified by external sources"
  - Auto-reduces confidence by 1 level
```

### Session Recovery

On invocation, the orchestrator checks for existing sessions:
```
Found incomplete session from {timestamp}: {original_prompt}
Session state: {stage} - {status}

Options:
(A) Resume from {checkpoint}
(B) Start fresh (archives previous)
(C) Abort
```

## Resource Limits

```yaml
resource_limits:
  max_concurrent_agents: 5
  max_websearch_per_agent: 2
  max_webfetch_per_agent: 1
  target_tokens_per_perspective: 2000  # Advisory, not enforced
  session_expiry: 24 hours
```

## Timeout Configuration

| Stage | Timeout | Exceeded Action |
|-------|---------|-----------------|
| 1 (Framing) | 5 min | Escalate to user |
| 2 (Perspectives) | 15 min total | Proceed with available (min 4) |
| 2 (per agent) | 10 min | Mark incomplete, proceed |
| 3 (Synthesis) | 10 min | Deliver partial synthesis |
| 4 (User Review) | No timeout | User-controlled |
| Global | 45 min | Safety ceiling, escalate |

## Quality Gates Summary

| Gate | Stage | Pass Threshold |
|------|-------|----------------|
| Input Validation | 1 | Prompt meets criteria |
| Framing | 1 | All checks pass |
| Per-Agent | 2 | 4/4 required elements |
| Minimum Coverage | 2 | >= 4 of 5 agents |
| Synthesis | 3 | All checks pass |
| User Approval | 4 | Accept, Refine, or Handoff |

## Dependencies

- Any skill with `handoff:` metadata is a valid handoff target
- Discovery algorithm documented in: `references/workflow-discovery.md`
- Handoff schema documented in: `references/handoff-schema.md`
- Adapts patterns from: `parallel-coordinator`, `synthesizer`

**Known handoff-eligible skills** (as of implementation):
- `lit-pm` - Comprehensive literature review [research]
- `programming-pm` - Software implementation [implementation]
- `pov-expansion` - Cross-domain perspectives [creative, analysis]

## Orchestration

This protocol is designed to be executed by the `brainstorming-pm` orchestrator skill. See `brainstorming-pm/SKILL.md` for:
- Execution instructions and stage-by-stage orchestration
- Tool selection (Task tool for Stage 2, inline for Stage 3)
- Model selection guidance
- Delegation patterns and quality gate evaluation

## Model Selection

Model selection guidance for each workflow component is documented in `brainstorming-pm/references/model-selection.md`. Summary:

| Component | Current | Target |
|-----------|---------|--------|
| Orchestrator | Inherited | Claude Opus 4.5 |
| Perspective Agents | Inherited | Claude Sonnet 4.5 |
| LLM Grouping | Inherited (inline) | Claude Haiku 4.5 |

## Notes

- **Parallel Independence**: Perspective agents MUST NOT see each other's outputs during Stage 2. This preserves diversity and prevents premature convergence (research-validated).

- **No Forced Consensus**: The synthesis should present conflicts neutrally. Disagreement between perspectives is valuable signal, not noise.

- **Divergent Value**: Unique insights from a single perspective may be the most valuable output. Do not penalize or bury non-convergent views.

- **Research Limitation**: This skill provides rapid analysis (15-30 min), not comprehensive research. For deep dives, hand off to lit-pm.

## References

- [persona-archetypes.md](references/persona-archetypes.md) - Archetype definitions
- [convergence-algorithm.md](references/convergence-algorithm.md) - Weighting logic
- [workflow-state-schema.md](references/workflow-state-schema.md) - Session state format
- [handoff-schema.md](references/handoff-schema.md) - Generic handoff payload format (v2.0)
- [workflow-discovery.md](references/workflow-discovery.md) - Handoff target discovery algorithm
- [brainstorming-pm/SKILL.md](../brainstorming-pm/SKILL.md) - Orchestrator skill
- [model-selection.md](../brainstorming-pm/references/model-selection.md) - Model selection guidance

## Examples

- [product-decision-example.md](examples/product-decision-example.md) - Complete walkthrough
