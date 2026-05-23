---
name: perspective-swarm
description: Multi-perspective brainstorming via 5 parallel agents with confidence-weighted synthesis
version: 1.0.0
tags: [brainstorming, multi-agent, synthesis, parallel, decision-support]
---

# perspective-swarm

Enable rapid multi-perspective brainstorming through parallel agent execution, producing a confidence-weighted synthesis that surfaces convergent insights and divergent alternatives.

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
              | OUTPUT      | Accept / Refine / Handoff to lit-pm
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

Launch 5 parallel agents. Each agent:

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

**On < 4 agents**: Present user options:
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

1. **Collect all perspective outputs**

2. **Identify convergent insights**:
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

5. **Resolve conflicts**:
   - Present all sides neutrally
   - Note evidence strength for each
   - Do NOT force artificial consensus

6. **Generate synthesis document**: `stage-3-synthesis.md`

**Quality Gate**:
- [ ] All available perspectives incorporated
- [ ] At least 2 convergent insights OR explicit "portfolio of options" framing
- [ ] At least 3 divergent insights captured
- [ ] Conflicts presented neutrally
- [ ] Blind spots aggregated

### Stage 4: User Review & Optional Handoff

**State**: AWAITING_USER

Present synthesis to user with options:

```
## Synthesis Complete

[Executive summary]

**Options:**
(A) Accept - Workflow complete
(B) Refine - Provide feedback, return to Stage 3
(C) Deep dive - Hand off to lit-pm for comprehensive literature review
```

**On Accept**: State -> COMPLETED
**On Refine**: State -> CONVERGING (with user feedback)
**On Deep dive**: Generate handoff-payload.yaml, invoke lit-pm

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
└── handoff-payload.yaml            # (if lit-pm requested)
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

On skill invocation, check for existing sessions:
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

- `lit-pm` - Optional handoff target for deep literature review
- Adapts patterns from: `parallel-coordinator`, `synthesizer`

## Notes

- **Parallel Independence**: Perspective agents MUST NOT see each other's outputs during Stage 2. This preserves diversity and prevents premature convergence (research-validated).

- **No Forced Consensus**: The synthesis should present conflicts neutrally. Disagreement between perspectives is valuable signal, not noise.

- **Divergent Value**: Unique insights from a single perspective may be the most valuable output. Do not penalize or bury non-convergent views.

- **Research Limitation**: This skill provides rapid analysis (15-30 min), not comprehensive research. For deep dives, hand off to lit-pm.

## References

- [persona-archetypes.md](references/persona-archetypes.md) - Archetype definitions
- [convergence-algorithm.md](references/convergence-algorithm.md) - Weighting logic
- [workflow-state-schema.md](references/workflow-state-schema.md) - Session state format
- [handoff-schema.md](references/handoff-schema.md) - Lit-pm handoff format

## Examples

- [product-decision-example.md](examples/product-decision-example.md) - Complete walkthrough
