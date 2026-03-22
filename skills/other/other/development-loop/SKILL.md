---
name: development-loop
description: "Complete development lifecycle: brainstorm → TDD planning → ralph implementation → review → feedback loop until approved"
---

# Development Loop - The Outer Loop for Ralph

## Overview

A complete development workflow that wraps Ralph with planning, review, and feedback cycles. Think of it as an "outer loop" that ensures quality through iterative refinement.

```
┌─────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT LOOP                          │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────┐  │
│  │BRAINSTORM│───▶│  PLAN    │───▶│   RALPH IMPLEMENT    │  │
│  │          │    │(superthink)   │   (inner loop)       │  │
│  └──────────┘    └──────────┘    └──────────┬───────────┘  │
│                                              │              │
│                                              ▼              │
│  ┌──────────┐    ┌──────────┐    ┌──────────────────────┐  │
│  │ APPROVED │◀───│  REVIEW  │◀───│   5-AGENT REVIEW     │  │
│  │  (exit)  │    │(decision)│    │                      │  │
│  └──────────┘    └────┬─────┘    └──────────────────────┘  │
│                       │ needs work                          │
│                       ▼                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              FEEDBACK LOOP                            │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐       │  │
│  │  │ FEEDBACK │───▶│  RALPH   │───▶│  REVIEW  │──┐    │  │
│  │  │  PLAN    │    │   FIX    │    │          │  │    │  │
│  │  └──────────┘    └──────────┘    └──────────┘  │    │  │
│  │       ▲                                        │    │  │
│  │       └────────── needs more work ─────────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## The Phases

### Phase 1: BRAINSTORM
**Goal:** Understand what to build through collaborative dialogue.

- Invoke `workers-do:brainstorming` skill
- Ask questions one at a time
- Explore approaches and trade-offs
- Output: Design document in `docs/plans/`

**Exit criteria:** User approves the design

### Phase 2: PLAN (Superthink)
**Goal:** Create TDD beads issues with extended thinking.

Use extended thinking to:
1. Break design into implementable modules
2. For each module, create beads issue chain:
   - `RED: [Module] tests` (tdd-red label)
   - `GREEN: Implement [Module]` (tdd-green label, blocked by RED)
   - `REFACTOR: Clean up [Module]` (tdd-refactor label, blocked by GREEN)
3. Set up cross-module dependencies
4. Prioritize order of work

**Output:** Beads issues with full dependency graph

**Exit criteria:** Issue plan reviewed and approved

### Phase 3: IMPLEMENT (Ralph Loop)
**Goal:** Autonomous implementation following TDD.

Start Ralph loop with prompt:
```
Work through beads issues in dependency order.
For each issue:
1. Claim it (bd update --status=in_progress)
2. Follow TDD: write test (RED), implement (GREEN), refactor
3. Close it (bd close)
4. Move to next ready issue (bd ready)

Continue until all issues are closed.
Output <promise>IMPLEMENTATION COMPLETE</promise> when done.
```

**Exit criteria:** All beads issues closed, tests passing

### Phase 4: REVIEW (5-Agent)
**Goal:** Comprehensive quality check.

Launch 5 parallel review agents:
1. General code review
2. Architectural review
3. TypeScript review
4. Product/vision review
5. TDD/beads compliance review

**Output:** Synthesized review with findings

**Decision point:**
- **APPROVED** → Exit loop, work is done
- **NEEDS WORK** → Continue to Phase 5

### Phase 5: FEEDBACK PLAN (Superthink)
**Goal:** Convert review feedback into actionable issues.

Use extended thinking to:
1. Analyze each review finding
2. Create beads issues for fixes:
   - `FIX: [Finding description]` with appropriate labels
3. Set priorities based on severity
4. Add dependencies if fixes depend on each other

**Output:** New beads issues for fixes

### Phase 6: FIX (Ralph Loop)
**Goal:** Address review findings.

Start Ralph loop with prompt:
```
Work through fix issues from code review.
For each issue:
1. Claim it
2. Implement the fix following TDD
3. Verify tests pass
4. Close it

Output <promise>FIXES COMPLETE</promise> when all fix issues closed.
```

### Phase 7: FINAL REVIEW
**Goal:** Verify fixes and decide if done.

Run 5-agent review again, focused on:
- Were the findings addressed?
- Any new issues introduced?
- Overall quality assessment

**Decision:**
- **APPROVED** → Exit, publish/merge
- **NEEDS MORE WORK** → Loop back to Phase 5

## State Management

The loop tracks state in `.claude/dev-loop.local.md`:

```yaml
---
phase: IMPLEMENT  # Current phase
iteration: 1      # Which review cycle
started_at: "2024-01-01T00:00:00Z"
design_doc: "docs/plans/2024-01-01-feature-design.md"
initial_issues: ["workers-xxx", "workers-yyy"]
fix_issues: []
review_findings: []
---

Original task description here...
```

## Commands

### /dev-loop "task description"
Start a new development loop.

### /dev-loop-status
Show current phase and progress.

### /dev-loop-advance
Manually advance to next phase (for human checkpoints).

### /dev-loop-cancel
Cancel the loop and clean up.

## Human Checkpoints

The loop pauses for human approval at:
1. **After BRAINSTORM** - Approve design before planning
2. **After PLAN** - Review issues before implementation
3. **After REVIEW** - Decide: approved or needs work
4. **After FINAL REVIEW** - Final approval or more iteration

## Extended Thinking Integration

Phases 2 and 5 use "superthink" - extended thinking mode for:
- Deep analysis of requirements
- Comprehensive issue breakdown
- Thorough dependency mapping
- Quality feedback analysis

Enable with: `thinking: extended` in prompts or model configuration.

## Example Usage

```bash
# Start the loop
/dev-loop "Add user authentication with JWT tokens, SSO support, and session management"

# Loop will:
# 1. Brainstorm with you about auth requirements
# 2. Create TDD issues for auth module
# 3. Ralph-loop implement the auth system
# 4. 5-agent review the implementation
# 5. Create fix issues from feedback
# 6. Ralph-loop the fixes
# 7. Final review → approve or iterate
```

## Key Principles

1. **Quality over speed** - Multiple review cycles ensure quality
2. **TDD throughout** - Every implementation follows RED-GREEN-REFACTOR
3. **Tracked work** - All work captured in beads issues
4. **Human oversight** - Key decisions require human approval
5. **Autonomous execution** - Ralph handles implementation phases
6. **Comprehensive review** - 5 specialized perspectives catch issues

## When to Use

**Good for:**
- Significant features (multi-day work)
- Complex implementations
- High-quality requirements
- Work that needs documentation

**Not good for:**
- Quick fixes (use simple TDD)
- Exploratory work (use just brainstorming)
- Urgent hotfixes (skip the loop)
