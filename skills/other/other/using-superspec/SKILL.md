---
name: using-superspec
description: |
  Use at the start of any conversation - establishes how to find and use SuperSpec skills.
  Combines development discipline with spec-driven documentation.
---

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply, you MUST invoke it.
IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.
This is not negotiable. This is not optional.
</EXTREMELY-IMPORTANT>

# Using SuperSpec

SuperSpec combines **development discipline** with **spec-driven documentation**.

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Spec First** | All development has Spec as source of truth |
| **TDD Enforced** | Write test first, watch it fail, then implement |
| **Two-Stage Review** | Spec compliance → Code quality |
| **Evidence First** | Verification over claims |
| **Delta Tracking** | Structured change history |
| **Archive Everything** | Complete development documentation |

## The Unified Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FULL WORKFLOW (large features, team review needed)                      │
├─────────────────────────────────────────────────────────────────────────┤
│  /superspec:brainstorm   →  Progressive design (Explore → Propose → Spec)│
│          ↓                                                               │
│  superspec validate      →  Validate specs (CLI) + team review           │
│          ↓                                                               │
│  /superspec:plan         →  Create TDD implementation plan               │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│  FAST TRACK (small-medium features, solo development)                    │
├─────────────────────────────────────────────────────────────────────────┤
│  /superspec:kickoff      →  All-in-one: brainstorm + validate + plan     │
└─────────────────────────────────────────────────────────────────────────┘

          ↓ (both paths continue with)

/superspec:execute         →  Subagent-driven TDD implementation
        ↓
/superspec:verify          →  Verify implementation matches specs
        ↓
/superspec:finish-branch   →  Complete branch (merge/PR)
        ↓
/superspec:archive         →  Archive change, apply deltas
```

### Brainstorm Phases

```
/superspec:brainstorm
        │
        ├─→ Phase 1: EXPLORE
        │   • Free exploration
        │   • Clarifying questions
        │   • Visualize ideas
        │
        ├─→ Phase 2: PROPOSE
        │   • Define Why + What Changes
        │   • Define Capabilities + Impact
        │   • Output: proposal.md
        │
        ├─→ Phase 3: DESIGN
        │   • 2-3 approaches comparison
        │   • Technical decisions
        │   • Output: design.md
        │
        └─→ Phase 4: SPEC
            • Define Requirements
            • Define Scenarios (→ tests)
            • Output: specs/*.md
```

## How to Access Skills

**In Claude Code:** Use the `Skill` tool. When you invoke a skill, its content is loaded - follow it directly.

## The Rule

**Invoke relevant skills BEFORE any response or action.**

Even a 1% chance a skill might apply means invoke it to check.

## Skill Categories

### Design Phase
| Skill | When to Use |
|-------|-------------|
| `kickoff` | **Fast track** - idea to plan in one session (small-medium features) |
| `brainstorm` | **Full workflow** - progressive design with review points (large features) |

### Planning Phase
| Skill | When to Use |
|-------|-------------|
| `plan-writing` | Creating TDD implementation plan |
| `git-worktree` | Setting up isolated development environment |

### Implementation Phase
| Skill | When to Use |
|-------|-------------|
| `tdd` | Writing any implementation code |
| `subagent-development` | Executing plan with subagents (default) |
| `executing-plans` | Batch execution with checkpoints (alternative) |
| `dispatching-parallel-agents` | For 2+ independent tasks in parallel |
| `systematic-debugging` | Debugging issues |

### Quality & Discipline Phase
| Skill | When to Use |
|-------|-------------|
| `verification-before-completion` | Before marking any task complete - evidence first |
| `receiving-code-review` | Responding to code review feedback professionally |

### Review Phase
| Skill | When to Use |
|-------|-------------|
| `spec-validation` | Validating specifications |
| `code-review` | Reviewing implementation |

### Completion Phase
| Skill | When to Use |
|-------|-------------|
| `superspec:verify` | Verifying implementation matches specs |
| `superspec:finish-branch` | Completing branch (merge/PR/keep/discard) |
| `superspec:archive` | Archiving completed changes (after finish-branch) |

## Red Flags - STOP and Check Skills

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I'll just write this code quickly" | TDD skill is REQUIRED. No exceptions. |
| "Tests after achieve the same goals" | NO. Tests-first = "what should this do?" |
| "I know what that means" | Knowing concept ≠ using skill. Invoke it. |
| "This doesn't need a spec" | If behavior changes, it needs a spec. |
| "I'll document later" | Documentation is part of the workflow. Do it now. |

## Skill Priority

When multiple skills could apply:

1. **Process skills first** (brainstorm) - determine approach through 4 phases
2. **Implementation skills second** (tdd, subagent-development) - guide execution
3. **Completion skills last** (verify, archive) - finalize work

## Document Outputs

| Phase | Skill | Output |
|-------|-------|--------|
| Brainstorm | `brainstorm` | `proposal.md` + `design.md` + `specs/**/*.md` |
| Plan | `plan-writing` | `superspec/changes/[id]/plan.md` + `tasks.md` |
| Execute | `subagent-development` | Actual code + tests |
| Finish | `finish-branch` | Merged branch or PR created |
| Archive | `archive` | `superspec/changes/archive/YYYY-MM-DD-[id]/` |

## Validation Checkpoints

### After Spec Phase
```bash
superspec validate [change-id] --strict
```
- Every Requirement has at least one Scenario
- Scenario format is correct (#### Scenario:)
- MODIFIED includes full content
- REMOVED includes Reason and Migration

### After Execute Phase
```bash
superspec verify [change-id]
```
- Every Scenario has corresponding test
- All tests pass
- No features outside of Specs

### Before Archive
- All validation passes
- Final code review approved
- Tests green

## The Iron Laws

### TDD Law
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```
Write code before test? Delete it. Start over.

### Spec Law
```
SPECS ARE TRUTH. CHANGES ARE PROPOSALS.
```
No implementation without a Spec. No Spec without a Proposal.

### SuperSpec Law
```
EVERY SCENARIO BECOMES A TEST. EVERY TEST TRACES TO A SCENARIO.
```
Spec → Test → Implementation → Verification. Full traceability.

### Verification Law
```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```
"It should work" is not evidence. Run the test. Show the output. Then claim completion.

## Quick Reference

```bash
# CLI Commands
superspec init                    # Initialize project
superspec list                    # List changes
superspec list --specs            # List specs
superspec show [item]             # Show details
superspec validate [id] --strict  # Validate specs
superspec verify [id]             # Verify implementation
superspec archive [id] --yes      # Archive change

# Slash Commands (AI Assistant)
/superspec:kickoff                # Fast track: brainstorm + validate + plan
/superspec:brainstorm             # Full workflow: progressive design only
/superspec:plan                   # Create TDD plan (after brainstorm)
/superspec:execute                # Execute with subagents
/superspec:verify                 # Verify implementation
/superspec:finish-branch          # Complete branch (merge/PR)
/superspec:archive                # Archive change
```
