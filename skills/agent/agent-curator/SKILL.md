---
skill_name: agent-curator
activation_code: AGENT_CURATOR_V1
version: 1.0.0
phase: any
prerequisites:
  - Agent definition file exists
  - Human available for adjudication conversation
outputs:
  - Updated agent definition
  - Curation session record
description: |
  Deep curation of a single agent definition through structured human conversation.
  Coordinates knowledge research, persona refinement, tooling optimization, and
  instruction quality improvement. One agent at a time, with due care.
---

# Agent Curator Skill

## Activation

Invoke for ad-hoc agent curation or project preparation:

```
[ACTIVATE:AGENT_CURATOR_V1]
Parameters:
  agent: path/to/agent.md
  mode: broad | project
  project: {project-name}  # Required if mode=project
```

## Purpose

Drive a structured conversation to deeply improve an agent definition across all dimensions:

1. **Knowledge Sources** (P0) — Find and integrate esteemed references
2. **Persona & Doctrine** (P1) — Sharpen identity and mental model
3. **Tooling & MCP** (P2) — Optimize tool and server configuration
4. **Local Corpora** (P3) — Materialize high-value knowledge locally
5. **Instruction Quality** (P4) — Refine priorities, modes, and behaviors

## Two Modes

### Broad Improvement Mode

For general agent enhancement:
- Changes should improve effectiveness across all use cases
- Improvements are candidates for upstream contribution
- Long-term maintenance burden considered

### Project-Specific Mode

For preparing an agent for a specific project:
- Changes may include project-specific knowledge/tooling
- Consider whether changes should stay local or go upstream
- Immediate utility prioritized, but long-term impact considered

## Execution Flow

### Phase 0: Scope Establishment

Present scope selection:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    AGENT CURATION SESSION                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Agent: {agent-name}                                                   ║
║  Tier: {focused | expert | phd}                                        ║
║  Current File: {path}                                                  ║
║                                                                        ║
║  What is the goal of this curation session?                           ║
║                                                                        ║
║  [B] Broad Improvement                                                 ║
║      Enhance general effectiveness across all use cases               ║
║      Changes are candidates for upstream contribution                  ║
║                                                                        ║
║  [P] Project-Specific Preparation                                      ║
║      Optimize for: {project-name if provided}                         ║
║      May include project-specific knowledge/tooling                    ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

Wait for human selection before proceeding.

### Phase 1: Initial Analysis

Load and analyze the agent definition:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    INITIAL ASSESSMENT                                  ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Agent: {agent-name}                                                   ║
║  Mode: {Broad | Project-Specific}                                      ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ DIMENSION SCORES                                                │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ Knowledge Sources   [██░░░] 2/5  HIGH gap                       │   ║
║  │ Persona & Doctrine  [████░] 4/5  LOW gap                        │   ║
║  │ Tooling & MCP       [███░░] 3/5  MEDIUM gap                     │   ║
║  │ Local Corpora       [█░░░░] 1/5  HIGH gap                       │   ║
║  │ Instruction Quality [████░] 4/5  LOW gap                        │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Key Observations:                                                     ║
║    • {observation-1}                                                   ║
║    • {observation-2}                                                   ║
║    • {observation-3}                                                   ║
║                                                                        ║
║  Recommended Focus: Knowledge Sources, Local Corpora                  ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [C] Continue with full curation                                       ║
║  [F] Focus on high-gap dimensions only                                 ║
║  [S] Skip to specific phase                                            ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Phase 2: Knowledge Sources (P0)

#### Step 2a: Current State Audit

```
╔═══════════════════════════════════════════════════════════════════════╗
║              KNOWLEDGE SOURCES — CURRENT STATE                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ EXISTING SOURCES                                                │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ ✓ {url-1}                                                       │   ║
║  │   Authority: Official  |  Status: 200 OK  |  Unique Value: Yes │   ║
║  │                                                                 │   ║
║  │ ⚠ {url-2}                                                       │   ║
║  │   Authority: Community |  Status: 200 OK  |  Unique Value: ?   │   ║
║  │                                                                 │   ║
║  │ ✗ {url-3}                                                       │   ║
║  │   Authority: Vendor    |  Status: 404     |  Action: Remove    │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Issues Found:                                                         ║
║    • 1 broken URL                                                      ║
║    • 2 sources with unclear unique value                              ║
║    • Missing: authoritative specification references                   ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [R] Research new sources                                              ║
║  [A] Address issues (remove broken, evaluate unclear)                  ║
║  [N] Next phase (no changes)                                           ║
╚═══════════════════════════════════════════════════════════════════════╝
```

#### Step 2b: Knowledge Research

Delegate to `agent-knowledge-researcher` and `web-researcher`:

```
Researching authoritative sources for: {agent-domain}

Using Opus to identify esteemed references...
Using Firecrawl for parallel discovery...

Evaluating:
  • Official documentation sites
  • Specification repositories
  • Academic papers (if applicable)
  • Vendor documentation
```

#### Step 2c: Source-by-Source Adjudication

Present EACH source individually for human decision:

```
╔═══════════════════════════════════════════════════════════════════════╗
║              SOURCE ADJUDICATION (1 of N)                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Source: {source-title}                                                ║
║  URL: {url}                                                            ║
║  Authority: {tier} ({tier-name})                                       ║
║                                                                        ║
║  Unique Value:                                                         ║
║    {explanation of what this provides that nothing else does}          ║
║                                                                        ║
║  Materialization Recommendation: {URL | Local Excerpt | Embed}        ║
║    Rationale: {why this materialization}                               ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [A] Add with recommended materialization                              ║
║  [M] Add with different materialization                                ║
║  [S] Skip this source                                                  ║
║  [D] Show more details                                                 ║
╚═══════════════════════════════════════════════════════════════════════╝
```

Repeat for each source. Never bulk-add.

### Phase 3: Persona & Doctrine (P1)

```
╔═══════════════════════════════════════════════════════════════════════╗
║              PERSONA & DOCTRINE                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ CURRENT INTERPRETIVE LENS                                       │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ {current lens text}                                             │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Assessment: {Good | Needs sharpening | Missing}                      ║
║                                                                        ║
║  ┌────────────────────────────────────────────────────────────────┐   ║
║  │ PROPOSED IMPROVEMENT                                            │   ║
║  ├────────────────────────────────────────────────────────────────┤   ║
║  │ {proposed improved lens}                                        │   ║
║  └────────────────────────────────────────────────────────────────┘   ║
║                                                                        ║
║  Rationale: {why this is better}                                      ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [A] Accept improvement                                                ║
║  [K] Keep current                                                      ║
║  [E] Edit proposal                                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

Similarly for vocabulary calibration and core principles.

### Phase 4: Tooling & MCP (P2)

```
╔═══════════════════════════════════════════════════════════════════════╗
║              TOOLING & MCP                                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Current Tool Modes:                                                   ║
║    audit: {tools}                                                      ║
║    solution: {tools}                                                   ║
║    research: {tools}                                                   ║
║                                                                        ║
║  Current MCP Servers:                                                  ║
║    • {server-1}: {purpose}                                             ║
║    • {server-2}: {purpose}                                             ║
║                                                                        ║
║  Recommendations:                                                      ║
║    [+] Add MCP server: {server}                                        ║
║        Rationale: {why this would help}                                ║
║                                                                        ║
║    [~] Modify tool mode: {mode}                                        ║
║        Proposal: {change}                                              ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  Review each recommendation? [Y/n]                                     ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Phase 5: Local Corpora (P3)

```
╔═══════════════════════════════════════════════════════════════════════╗
║              LOCAL CORPORA                                             ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Materialization Candidates:                                           ║
║                                                                        ║
║  1. {knowledge-topic}                                                  ║
║     From: {source}                                                     ║
║     Size: ~{token-estimate} tokens                                     ║
║     Stability: {stable | slow-decay | fast-decay}                     ║
║     Recommendation: {Materialize | Keep as URL}                        ║
║                                                                        ║
║  2. {knowledge-topic-2}                                                ║
║     ...                                                                ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [R] Review each candidate                                             ║
║  [A] Accept all recommended                                            ║
║  [N] No local materialization                                          ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Phase 6: Instruction Quality (P4)

```
╔═══════════════════════════════════════════════════════════════════════╗
║              INSTRUCTION QUALITY                                       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Findings:                                                             ║
║                                                                        ║
║  [HIGH] Instruction Interference                                       ║
║    P1.5 conflicts with P2.3 on {topic}                                ║
║    Proposed resolution: {resolution}                                   ║
║                                                                        ║
║  [MEDIUM] Missing Cognitive Mode                                       ║
║    Convergent mode not defined                                         ║
║    Proposed: {mode definition}                                         ║
║                                                                        ║
║  [LOW] Escalation Calibration                                          ║
║    Threshold may be too high for this domain                          ║
║    Proposed: Lower from 0.7 to 0.6                                     ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [R] Review each finding                                               ║
║  [H] Address HIGH severity only                                        ║
║  [N] No instruction changes                                            ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Phase 7: Synthesis

```
╔═══════════════════════════════════════════════════════════════════════╗
║              CURATION COMPLETE                                         ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Agent: {agent-name}                                                   ║
║  Mode: {Broad | Project-Specific}                                      ║
║                                                                        ║
║  Changes Summary:                                                      ║
║    Knowledge:    +3 sources, -1 broken, 2 URLs validated              ║
║    Persona:      Interpretive lens sharpened                          ║
║    Tooling:      +1 MCP server (firecrawl)                            ║
║    Corpora:      1 local excerpt added                                ║
║    Instructions: 1 conflict resolved, 1 mode added                    ║
║                                                                        ║
║  Score Improvement:                                                    ║
║    Knowledge:    2/5 → 4/5                                             ║
║    Persona:      4/5 → 5/5                                             ║
║    Tooling:      3/5 → 4/5                                             ║
║    Corpora:      1/5 → 3/5                                             ║
║    Instructions: 4/5 → 5/5                                             ║
║                                                                        ║
╠═══════════════════════════════════════════════════════════════════════╣
║  [S] Save updated definition                                           ║
║  [R] Review changes before saving                                      ║
║  [C] Cancel (discard all changes)                                      ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Final: Contribution Offer (Broad Mode Only)

```
╔═══════════════════════════════════════════════════════════════════════╗
║              CONTRIBUTE UPSTREAM?                                      ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  These improvements may benefit other users of this agent.            ║
║                                                                        ║
║  Would you like to contribute to the upstream agents repo?            ║
║                                                                        ║
║  [Y] Yes - Prepare PR to turbobeest/agents                            ║
║  [N] No - Keep improvements local only                                 ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Agent Coordination

This skill uses the `agent-curation-orchestrator` to:
- Drive the structured conversation
- Coordinate with `agent-knowledge-researcher` for source discovery
- Coordinate with `web-researcher` for Firecrawl-based research
- Apply changes using appropriate tier editor

## Signals

| Signal | Meaning |
|--------|---------|
| `CURATION_STARTED` | Session begun for agent |
| `CURATION_PHASE_COMPLETE` | Individual phase finished |
| `CURATION_COMPLETE` | All phases done, agent updated |
| `CURATION_CANCELLED` | Session cancelled, no changes |

## Integration with Dev-System Phases

During project phases, this skill can be invoked to prepare agents:

```
Phase 6 Pre-Gate: Preparing for specification work

The typescript-pro agent will be used.
Would you like to curate it for this project? [Y/n]

[ACTIVATE:AGENT_CURATOR_V1]
  agent: agents/-03-agents/.../typescript-pro.md
  mode: project
  project: {current-project-name}
```

## Completion

Outputs:
- Updated agent definition file
- Curation session record in `.claude/curation-logs/`
- Optional: PR to upstream agents repo

Next: Resume normal operations or continue with phase work.
