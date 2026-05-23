---
name: planning
description: Generate comprehensive plans for new features by exploring the codebase, synthesizing approaches, validating with spikes, and decomposing into beads. Use when asked to plan a feature, create a roadmap, or design an implementation approach.
---

# Feature Planning Pipeline

Generate quality plans through systematic discovery, synthesis, verification, and decomposition.

## Pipeline Overview

```
USER REQUEST → Worktree Setup → Discovery → Synthesis → Verification → Decomposition → Validation → Track Planning → Ready Plan
```

| Phase             | Tool                                     | Output                              |
| ----------------- | ---------------------------------------- | ----------------------------------- |
| 0. Worktree Setup | bd worktree                              | Isolated feature branch             |
| 1. Discovery      | Parallel sub-agents, gkg, Librarian, exa | Discovery Report                    |
| 2. Synthesis      | Oracle                                   | Approach + Risk Map                 |
| 3. Verification   | Spikes via MULTI_AGENT_WORKFLOW          | Validated Approach + Learnings      |
| 4. Decomposition  | file-beads skill                         | .beads/\*.md files                  |
| 5. Validation     | bv + Oracle                              | Validated dependency graph          |
| 6. Track Planning | bv --robot-plan                          | Execution plan with parallel tracks |

## Phase 0: Worktree Setup (Mandatory)

**Why**: Beads are tracked in git. Without worktrees, branch switching causes conflicts when PRs merge.

**Always create a worktree before creating beads for a feature:**

```bash
# From main repo root
bd worktree create .worktrees/<feature-name> --branch feature/<feature-name>
cd .worktrees/<feature-name>
```

This creates a redirect file so all beads operations share the main repo's `.beads/` database. No merge conflicts when PR lands.

**After PR merges:**

```bash
cd <main-repo>
git pull
bd worktree remove .worktrees/<feature-name>
```

**Skip worktree only if**: Quick fix on main that won't create new beads.

## Phase 1: Discovery (Parallel Exploration)

Launch parallel sub-agents to gather codebase intelligence:

```
Task() → Agent A: Architecture snapshot (gkg repo_map)
Task() → Agent B: Pattern search (find similar existing code)
Task() → Agent C: Constraints (package.json, tsconfig, deps)
Librarian → External patterns ("how do similar projects do this?")
exa → Library docs (if external integration needed)
```

### Discovery Report Template

Save to `history/<feature>/discovery.md`:

```markdown
# Discovery Report: <Feature Name>

## Architecture Snapshot

- Relevant packages: ...
- Key modules: ...
- Entry points: ...

## Existing Patterns

- Similar implementation: <file> does X using Y pattern
- Reusable utilities: ...
- Naming conventions: ...

## Technical Constraints

- Node version: ...
- Key dependencies: ...
- Build requirements: ...

## External References

- Library docs: ...
- Similar projects: ...
```

## Phase 2: Synthesis (Oracle)

Feed Discovery Report to Oracle for gap analysis:

```
oracle(
  task: "Analyze gap between current codebase and feature requirements",
  context: "Discovery report attached. User wants: <feature>",
  files: ["history/<feature>/discovery.md"]
)
```

Oracle produces:

1. **Gap Analysis** - What exists vs what's needed
2. **Approach Options** - 1-3 strategies with tradeoffs
3. **Risk Assessment** - LOW / MEDIUM / HIGH per component

### Risk Classification

| Level  | Criteria                      | Verification                 |
| ------ | ----------------------------- | ---------------------------- |
| LOW    | Pattern exists in codebase    | Proceed                      |
| MEDIUM | Variation of existing pattern | Interface sketch, type-check |
| HIGH   | Novel or external integration | Spike required               |

### Risk Indicators

```
Pattern exists in codebase? ─── YES → LOW base
                            └── NO  → MEDIUM+ base

External dependency? ─── YES → HIGH
                     └── NO  → Check blast radius

Blast radius >5 files? ─── YES → HIGH
                       └── NO  → MEDIUM
```

Save to `history/<feature>/approach.md`:

```markdown
# Approach: <Feature Name>

## Gap Analysis

| Component | Have | Need | Gap |
| --------- | ---- | ---- | --- |
| ...       | ...  | ...  | ... |

## Recommended Approach

<Description>

### Alternative Approaches

1. <Option A> - Tradeoff: ...
2. <Option B> - Tradeoff: ...

## Risk Map

| Component   | Risk | Reason           | Verification |
| ----------- | ---- | ---------------- | ------------ |
| Stripe SDK  | HIGH | New external dep | Spike        |
| User entity | LOW  | Follows existing | Proceed      |
```

## Phase 3: Verification (Risk-Based)

### For HIGH Risk Items → Create Spike Beads

Spikes are mini-plans executed via MULTI_AGENT_WORKFLOW:

```bash
bd create "Spike: <question to answer>" -t epic -p 0
bd create "Spike: Test X" -t task --blocks <spike-epic>
bd create "Spike: Verify Y" -t task --blocks <spike-epic>
```

### Spike Bead Template

```markdown
# Spike: <specific question>

**Time-box**: 30 minutes
**Output location**: .spikes/<spike-id>/

## Question

Can we <specific technical question>?

## Success Criteria

- [ ] Working throwaway code exists
- [ ] Answer documented (yes/no + details)
- [ ] Learnings captured for main plan

## On Completion

Close with: `bd close <id> --reason "YES: <approach>" or "NO: <blocker>"`
```

### Execute Spikes

Use the MULTI_AGENT_WORKFLOW:

1. `bv --robot-plan` to parallelize spikes
2. `Task()` per spike with time-box
3. Workers write to `.spikes/<feature>/<spike-id>/`
4. Close with learnings: `bd close <id> --reason "<result>"`

### Aggregate Spike Results

```
oracle(
  task: "Synthesize spike results and update approach",
  context: "Spikes completed. Results: ...",
  files: ["history/<feature>/approach.md"]
)
```

Update approach.md with validated learnings.

## Phase 4: Decomposition (file-beads skill)

Load the file-beads skill and create beads with embedded learnings:

```bash
skill("file-beads")
```

### Bead Requirements

Each bead MUST include:

- **Spike learnings** embedded in description (if applicable)
- **Reference to .spikes/ code** for HIGH risk items
- **Clear acceptance criteria**
- **File scope** for track assignment

### Example Bead with Learnings

```markdown
# Implement Stripe webhook handler

## Context

Spike bd-12 validated: Stripe SDK works with our Node version.
See `.spikes/billing-spike/webhook-test/` for working example.

## Learnings from Spike

- Must use `stripe.webhooks.constructEvent()` for signature verification
- Webhook secret stored in `STRIPE_WEBHOOK_SECRET` env var
- Raw body required (not parsed JSON)

## Acceptance Criteria

- [ ] Webhook endpoint at `/api/webhooks/stripe`
- [ ] Signature verification implemented
- [ ] Events: `checkout.session.completed`, `invoice.paid`
```

## Phase 5: Validation

### Run bv Analysis

```bash
bv --robot-suggest   # Find missing dependencies
bv --robot-insights  # Detect cycles, bottlenecks
bv --robot-priority  # Validate priorities
```

### Fix Issues

```bash
bd dep add <from> <to>      # Add missing deps
bd dep remove <from> <to>   # Break cycles
bd update <id> --priority X # Adjust priorities
```

### Oracle Final Review

```
oracle(
  task: "Review plan completeness and clarity",
  context: "Plan ready. Check for gaps, unclear beads, missing deps.",
  files: [".beads/"]
)
```

## Phase 6: Track Planning

This phase creates an **execution-ready plan** so the orchestrator can spawn workers immediately without re-analyzing beads.

### Step 1: Get Parallel Tracks

```bash
bv --robot-plan 2>/dev/null | jq '.plan.tracks'
```

### Step 2: Assign File Scopes

For each track, determine the file scope based on beads in that track:

```bash
# For each bead, check which files it touches
bd show <bead-id>  # Look at description for file hints
```

**Rules:**

- File scopes must NOT overlap between tracks
- Use glob patterns: `packages/sdk/**`, `apps/server/**`
- If overlap unavoidable, merge into single track

### Step 3: Generate Agent Names

Assign unique adjective+noun names to each track:

- BlueLake, GreenCastle, RedStone, PurpleBear, etc.
- Names are memorable identifiers, NOT role descriptions

### Step 4: Create Execution Plan

Save to `history/<feature>/execution-plan.md`:

```markdown
# Execution Plan: <Feature Name>

Epic: <epic-id>
Generated: <date>

## Tracks

| Track | Agent       | Beads (in order)      | File Scope        |
| ----- | ----------- | --------------------- | ----------------- |
| 1     | BlueLake    | bd-10 → bd-11 → bd-12 | `packages/sdk/**` |
| 2     | GreenCastle | bd-20 → bd-21         | `packages/cli/**` |
| 3     | RedStone    | bd-30 → bd-31 → bd-32 | `apps/server/**`  |

## Track Details

### Track 1: BlueLake - <track-description>

**File scope**: `packages/sdk/**`
**Beads**:

1. `bd-10`: <title> - <brief description>
2. `bd-11`: <title> - <brief description>
3. `bd-12`: <title> - <brief description>

### Track 2: GreenCastle - <track-description>

**File scope**: `packages/cli/**`
**Beads**:

1. `bd-20`: <title> - <brief description>
2. `bd-21`: <title> - <brief description>

### Track 3: RedStone - <track-description>

**File scope**: `apps/server/**`
**Beads**:

1. `bd-30`: <title> - <brief description>
2. `bd-31`: <title> - <brief description>
3. `bd-32`: <title> - <brief description>

## Cross-Track Dependencies

- Track 2 can start after bd-11 (Track 1) completes
- Track 3 has no cross-track dependencies

## Key Learnings (from Spikes)

Embedded in beads, but summarized here for orchestrator reference:

- <learning 1>
- <learning 2>
```

### Validation

Before finalizing, verify:

```bash
# No cycles in the graph
bv --robot-insights 2>/dev/null | jq '.Cycles'

# All beads assigned to tracks
bv --robot-plan 2>/dev/null | jq '.plan.unassigned'
```

## Output Artifacts

| Artifact          | Location                              | Purpose                            |
| ----------------- | ------------------------------------- | ---------------------------------- |
| Discovery Report  | `history/<feature>/discovery.md`      | Codebase snapshot                  |
| Approach Document | `history/<feature>/approach.md`       | Strategy + risks                   |
| Spike Code        | `.spikes/<feature>/`                  | Reference implementations          |
| Spike Learnings   | Embedded in beads                     | Context for workers                |
| Beads             | `.beads/*.md`                         | Executable work items              |
| Execution Plan    | `history/<feature>/execution-plan.md` | Track assignments for orchestrator |

## Quick Reference

### Tool Selection

| Need               | Tool                                                                        |
| ------------------ | --------------------------------------------------------------------------- |
| Codebase structure | `mcp__gkg__repo_map`                                                        |
| Find definitions   | `mcp__gkg__search_codebase_definitions`                                     |
| Find usages        | `mcp__gkg__get_references`                                                  |
| Semantic search    | `mcp__morph_mcp__warpgrep_codebase_search`                                  |
| External patterns  | `librarian`                                                                 |
| Library docs       | `mcp__MCP_DOCKER__resolve-library-id` → `mcp__MCP_DOCKER__get-library-docs` |
| Web research       | `mcp__MCP_DOCKER__web_search_exa`                                           |
| Gap analysis       | `oracle`                                                                    |
| Create beads       | `skill("file-beads")` + `bd create`                                         |
| Validate graph     | `bv --robot-*`                                                              |

### Common Mistakes

- **Skipping discovery** → Plan misses existing patterns
- **No risk assessment** → Surprises during execution
- **No spikes for HIGH risk** → Blocked workers
- **Missing learnings in beads** → Workers re-discover same issues
- **No bv validation** → Broken dependency graph
