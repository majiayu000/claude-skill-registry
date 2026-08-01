---
name: ralph
description: This skill guides users through setting up and running Ralph - an autonomous
  coding loop that repeatedly feeds prompts to Claude until a project is complete.
---

# Ralph Playbook Skill

This skill guides users through setting up and running Ralph - an autonomous coding loop that repeatedly feeds prompts to Claude until a project is complete.

Based on Geoffrey Huntley's [Ralph Playbook](https://github.com/ghuntley/how-to-ralph-wiggum).

---

## Quick Reference

| Item | Description |
|------|-------------|
| **What is Ralph** | A bash loop that feeds prompts to Claude until your project is complete |
| **Workflow** | 3 phases: Requirements (human+LLM) → Planning (loop) → Building (loop) |
| **Files** | `loop.sh`, `PROMPT_plan.md`, `PROMPT_build.md`, `AGENTS.md`, `IMPLEMENTATION_PLAN.md`, `specs/*` |
| **Setup** | Copy templates, fill in `AGENTS.md`, create `specs/*.md`, run `chmod +x loop.sh` |
| **Run Planning** | `./loop.sh plan 3` — generates `IMPLEMENTATION_PLAN.md` |
| **Run Building** | `./loop.sh 20` — implements tasks, commits, pushes |
| **Key Principle** | Trust the loop; steer via specs (upstream) and tests (downstream) |
| **Context Budget** | ~176K usable tokens; keep AGENTS.md small (~60 lines) |
| **Plan is Disposable** | If wrong, regenerate; don't patch |
| **Work Branches** | `./loop.sh plan-work "description"` for scoped planning |

---

## Quick Start Checklist

Guide the user through these steps interactively:

### 1. Setup Files
- [ ] Copy `loop.sh` to project root
- [ ] Copy `PROMPT_plan.md` to project root
- [ ] Copy `PROMPT_build.md` to project root
- [ ] Copy `AGENTS.md` to project root (fill in your commands)
- [ ] Create empty `IMPLEMENTATION_PLAN.md`
- [ ] Create `specs/` directory
- [ ] Run `chmod +x loop.sh`

### 2. Define Requirements (Phase 1)
- [ ] Identify Jobs to Be Done (JTBD)
- [ ] Break each JTBD into Topics of Concern
- [ ] Write one `specs/[topic].md` per topic
- [ ] Include acceptance criteria in each spec

### 3. Fill in AGENTS.md
- [ ] Add build commands
- [ ] Add test commands
- [ ] Add typecheck/lint commands
- [ ] Keep it brief (~60 lines max)

### 4. Update PROMPT_plan.md
- [ ] Replace `[project-specific goal]` with your goal

### 5. Run Planning (Phase 2)
- [ ] Run `./loop.sh plan 3`
- [ ] Review generated `IMPLEMENTATION_PLAN.md`
- [ ] Adjust specs if needed, re-run planning

### 6. Run Building (Phase 3)
- [ ] Run `./loop.sh 20` (or unlimited with `./loop.sh`)
- [ ] Monitor commits with `git log --oneline`
- [ ] Ctrl+C to stop when done

---

## Table of Contents

- [Workflow](#workflow)
- [Key Principles](#key-principles)
- [Loop Mechanics](#loop-mechanics)
- [Files](#files)
- [Enhancements](#enhancements)

---

## Workflow

### Three Phases, Two Prompts, One Loop

Ralph isn't just "a loop that codes." It's a funnel with 3 Phases, 2 Prompts, and 1 Loop.

#### Phase 1: Define Requirements (LLM conversation)

- Discuss project ideas → identify Jobs to Be Done (JTBD)
- Break individual JTBD into topic(s) of concern
- Use subagents to load info from URLs into context
- LLM understands JTBD topic of concern: subagent writes `specs/FILENAME.md` for each topic

#### Phase 2 / 3: Run Ralph Loop (two modes, swap `PROMPT.md` as needed)

Same loop mechanism, different prompts for different objectives:

| Mode | When to use | Prompt focus |
|------|-------------|--------------|
| PLANNING | No plan exists, or plan is stale/wrong | Generate/update `IMPLEMENTATION_PLAN.md` only |
| BUILDING | Plan exists | Implement from plan, commit, update plan as side effect |

**Prompt differences per mode:**

- PLANNING prompt does gap analysis (specs vs code) and outputs a prioritized TODO list—no implementation, no commits.
- BUILDING prompt assumes plan exists, picks tasks from it, implements, runs tests (backpressure), commits.

**Why use the loop for both modes?**

- BUILDING requires it: inherently iterative (many tasks × fresh context = isolation)
- PLANNING uses it for consistency: same execution model, though often completes in 1-2 iterations
- Flexibility: if plan needs refinement, loop allows multiple passes reading its own output
- Simplicity: one mechanism for everything; clean file I/O; easy stop/restart

**Context loaded each iteration:** `PROMPT.md` + `AGENTS.md`

**PLANNING mode loop lifecycle:**

1. Subagents study `specs/*` and existing `/src`
2. Compare specs against code (gap analysis)
3. Create/update `IMPLEMENTATION_PLAN.md` with prioritized tasks
4. No implementation

**BUILDING mode loop lifecycle:**

1. Orient – subagents study `specs/*` (requirements)
2. Read plan – study `IMPLEMENTATION_PLAN.md`
3. Select – pick the most important task
4. Investigate – subagents study relevant `/src` ("don't assume not implemented")
5. Implement – N subagents for file operations
6. Validate – 1 subagent for build/tests (backpressure)
7. Update `IMPLEMENTATION_PLAN.md` – mark task done, note discoveries/bugs
8. Update `AGENTS.md` – if operational learnings
9. Commit
10. Loop ends → context cleared → next iteration starts fresh

#### Concepts

| Term | Definition |
|------|------------|
| Job to be Done (JTBD) | High-level user need or outcome |
| Topic of Concern | A distinct aspect/component within a JTBD |
| Spec | Requirements doc for one topic of concern (`specs/FILENAME.md`) |
| Task | Unit of work derived from comparing specs to code |

**Relationships:**

- 1 JTBD → multiple topics of concern
- 1 topic of concern → 1 spec
- 1 spec → multiple tasks (specs are larger than tasks)

**Example:**

- JTBD: "Help designers create mood boards"
- Topics: image collection, color extraction, layout, sharing
- Each topic → one spec file
- Each spec → many tasks in implementation plan

**Topic Scope Test: "One Sentence Without 'And'"**

- Can you describe the topic of concern in one sentence without conjoining unrelated capabilities?
  - ✓ "The color extraction system analyzes images to identify dominant colors"
  - ✗ "The user system handles authentication, profiles, and billing" → 3 topics
- If you need "and" to describe what it does, it's probably multiple topics

---

## Key Principles

### Context Is Everything

- When 200K+ tokens advertised = ~176K truly usable
- And 40-60% context utilization for "smart zone"
- Tight tasks + 1 task per loop = 100% smart zone context utilization

This informs and drives everything else:

- **Use the main agent/context as a scheduler** - Don't allocate expensive work to main context; spawn subagents whenever possible instead
- **Use subagents as memory extension** - Each subagent gets ~156kb that's garbage collected; fan out to avoid polluting main context
- **Simplicity and brevity win** - Applies to number of parts in system, loop config, and content; verbose inputs degrade determinism
- **Prefer Markdown over JSON** - To define and track work, for better token efficiency

### Steering Ralph: Patterns + Backpressure

Creating the right signals & gates to steer Ralph's successful output is critical. You can steer from two directions:

**Steer upstream:**
- Ensure deterministic setup: Allocate first ~5,000 tokens for specs
- Every loop's context is allocated with the same files so model starts from known state (`PROMPT.md` + `AGENTS.md`)
- Your existing code shapes what gets used and generated
- If Ralph is generating wrong patterns, add/update utilities and existing code patterns to steer it toward correct ones

**Steer downstream:**
- Create backpressure via tests, typechecks, lints, builds, etc. that will reject invalid/unacceptable work
- Prompt says "run tests" generically. `AGENTS.md` specifies actual commands to make backpressure project-specific
- Backpressure can extend beyond code validation: LLM-as-judge tests can provide backpressure for subjective criteria

**Remind Ralph to create/use backpressure:**
- "Important: When authoring documentation, capture the why — tests and implementation importance."

### Let Ralph Ralph

Ralph's effectiveness comes from how much you trust it to do the right thing (eventually) and engender its ability to do so.

- **Let Ralph Ralph** - Lean into LLM's ability to self-identify, self-correct and self-improve; applies to implementation plan, task definition and prioritization; eventual consistency achieved through iteration
- **Use protection** - To operate autonomously, Ralph requires `--dangerously-skip-permissions`; run in isolated environments with minimum viable access

**Escape hatches:**
- Ctrl+C stops the loop
- `git reset --hard` reverts uncommitted changes
- Regenerate plan if trajectory goes wrong

### Move Outside the Loop

To get the most out of Ralph, you need to get out of his way. Ralph should be doing all of the work, including deciding which planned work to implement next and how to implement it. Your job is now to sit on the loop, not in it.

**Observe and course correct** – especially early on, sit and watch. What patterns emerge? Where does Ralph go wrong? The prompts you start with won't be the prompts you end with.

**Tune it like a guitar** – instead of prescribing everything upfront, observe and adjust reactively. When Ralph fails a specific way, add a sign to help him next time.

Signs aren't just prompt text. They're anything Ralph can discover:
- Prompt guardrails - explicit instructions like "don't assume not implemented"
- `AGENTS.md` - operational learnings about how to build/test
- Utilities in your codebase - when you add a pattern, Ralph discovers it and follows it

**The plan is disposable:**
- If it's wrong, throw it out, and start over
- Regeneration cost is one Planning loop; cheap compared to Ralph going in circles
- Regenerate when:
  - Ralph is going off track
  - Plan feels stale or doesn't match current state
  - Too much clutter from completed items
  - You've made significant spec changes

---

## Loop Mechanics

### Outer Loop Control

The minimal form of `loop.sh` script:

```bash
while :; do cat PROMPT.md | claude ; done
```

**What controls task continuation?**

1. Bash loop runs → feeds `PROMPT.md` to claude
2. PROMPT.md instructs → "Study IMPLEMENTATION_PLAN.md and choose the most important thing"
3. Agent completes one task → updates IMPLEMENTATION_PLAN.md on disk, commits, exits
4. Bash loop restarts immediately → fresh context window
5. Agent reads updated plan → picks next most important thing

**Key insight:** The IMPLEMENTATION_PLAN.md file persists on disk between iterations and acts as shared state between otherwise isolated loop executions.

No sophisticated orchestration needed - just a dumb bash loop that keeps restarting the agent, and the agent figures out what to do next by reading the plan file each time.

### Inner Loop Control (Task Execution)

A single task execution has no hard technical limit. Control relies on:

- **Scope discipline** - PROMPT.md instructs "one task" and "commit when tests pass"
- **Backpressure** - tests/build failures force the agent to fix issues before committing
- **Natural completion** - agent exits after successful commit

Ralph can go in circles, ignore instructions, or take wrong directions - this is expected and part of the tuning process.

### Enhanced Loop Script

The full `loop.sh` wraps core loop with mode selection (plan/build), max-iterations support, and git push after each iteration.

**Usage:**
```bash
./loop.sh              # Build mode, unlimited iterations
./loop.sh 20           # Build mode, max 20 iterations
./loop.sh plan         # Plan mode, unlimited iterations
./loop.sh plan 5       # Plan mode, max 5 iterations
```

**Claude CLI flags:**
- `-p` (headless mode): Enables non-interactive operation, reads prompt from stdin
- `--dangerously-skip-permissions`: Bypasses all permission prompts for fully automated runs
- `--output-format=stream-json`: Outputs structured JSON for logging/monitoring
- `--model opus`: Primary agent uses Opus for task selection and coordination
- `--verbose`: Provides detailed execution logging

---

## Files

### Project Structure

```
project-root/
├── loop.sh                         # Ralph loop script
├── PROMPT_build.md                 # Build mode instructions
├── PROMPT_plan.md                  # Plan mode instructions
├── AGENTS.md                       # Operational guide loaded each iteration
├── IMPLEMENTATION_PLAN.md          # Prioritized task list (generated/updated by Ralph)
├── specs/                          # Requirement specs (one per JTBD topic)
│   ├── [jtbd-topic-a].md
│   └── [jtbd-topic-b].md
├── src/                            # Application source code
└── src/lib/                        # Shared utilities & components
```

### loop.sh

The outer loop script that orchestrates Ralph iterations.

```bash
#!/bin/bash
# Usage: ./loop.sh [plan] [max_iterations]

if [ "$1" = "plan" ]; then
    MODE="plan"
    PROMPT_FILE="PROMPT_plan.md"
    MAX_ITERATIONS=${2:-0}
elif [[ "$1" =~ ^[0-9]+$ ]]; then
    MODE="build"
    PROMPT_FILE="PROMPT_build.md"
    MAX_ITERATIONS=$1
else
    MODE="build"
    PROMPT_FILE="PROMPT_build.md"
    MAX_ITERATIONS=0
fi

ITERATION=0
CURRENT_BRANCH=$(git branch --show-current)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode:   $MODE"
echo "Prompt: $PROMPT_FILE"
echo "Branch: $CURRENT_BRANCH"
[ $MAX_ITERATIONS -gt 0 ] && echo "Max:    $MAX_ITERATIONS iterations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: $PROMPT_FILE not found"
    exit 1
fi

while true; do
    if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
        echo "Reached max iterations: $MAX_ITERATIONS"
        break
    fi

    cat "$PROMPT_FILE" | claude -p \
        --dangerously-skip-permissions \
        --output-format=stream-json \
        --model opus \
        --verbose

    git push origin "$CURRENT_BRANCH" 2>/dev/null || \
        git push -u origin "$CURRENT_BRANCH"

    ITERATION=$((ITERATION + 1))
    echo -e "\n\n================ LOOP $ITERATION ================\n"
done
```

### PROMPTS

The instruction set for each loop iteration. Swap between PLANNING and BUILDING versions as needed.

**Prompt Structure:**

| Section | Purpose |
|---------|---------|
| Phase 0 (0a, 0b, 0c) | Orient: study specs, source location, current plan |
| Phase 1-4 | Main instructions: task, validation, commit |
| 999... numbering | Guardrails/invariants (higher number = more critical) |

**Key Language Patterns** (Geoff's specific phrasing):
- "study" (not "read" or "look at")
- "don't assume not implemented" (critical - the Achilles' heel)
- "using parallel subagents" / "up to N subagents"
- "only 1 subagent for build/tests" (backpressure control)
- "Ultrathink"
- "capture the why"
- "keep it up to date"

#### PROMPT_plan.md Template

```
0a. Study `specs/*` with up to 250 parallel Sonnet subagents to learn the application specifications.
0b. Study @IMPLEMENTATION_PLAN.md (if present) to understand the plan so far.
0c. Study `src/lib/*` with up to 250 parallel Sonnet subagents to understand shared utilities & components.
0d. For reference, the application source code is in `src/*`.

1. Study @IMPLEMENTATION_PLAN.md (if present; it may be incorrect) and use up to 500 Sonnet subagents to study existing source code in `src/*` and compare it against `specs/*`. Use an Opus subagent to analyze findings, prioritize tasks, and create/update @IMPLEMENTATION_PLAN.md as a bullet point list sorted in priority of items yet to be implemented. Ultrathink. Consider searching for TODO, minimal implementations, placeholders, skipped/flaky tests, and inconsistent patterns. Study @IMPLEMENTATION_PLAN.md to determine starting point for research and keep it up to date with items considered complete/incomplete using subagents.

IMPORTANT: Plan only. Do NOT implement anything. Do NOT assume functionality is missing; confirm with code search first. Treat `src/lib` as the project's standard library for shared utilities and components. Prefer consolidated, idiomatic implementations there over ad-hoc copies.

ULTIMATE GOAL: We want to achieve [project-specific goal]. Consider missing elements and plan accordingly. If an element is missing, search first to confirm it doesn't exist, then if needed author the specification at specs/FILENAME.md. If you create a new element then document the plan to implement it in @IMPLEMENTATION_PLAN.md using a subagent.
```

#### PROMPT_build.md Template

```
0a. Study `specs/*` with up to 500 parallel Sonnet subagents to learn the application specifications.
0b. Study @IMPLEMENTATION_PLAN.md.
0c. For reference, the application source code is in `src/*`.

1. Your task is to implement functionality per the specifications using parallel subagents. Follow @IMPLEMENTATION_PLAN.md and choose the most important item to address. Before making changes, search the codebase (don't assume not implemented) using Sonnet subagents. You may use up to 500 parallel Sonnet subagents for searches/reads and only 1 Sonnet subagent for build/tests. Use Opus subagents when complex reasoning is needed (debugging, architectural decisions).
2. After implementing functionality or resolving problems, run the tests for that unit of code that was improved. If functionality is missing then it's your job to add it as per the application specifications. Ultrathink.
3. When you discover issues, immediately update @IMPLEMENTATION_PLAN.md with your findings using a subagent. When resolved, update and remove the item.
4. When the tests pass, update @IMPLEMENTATION_PLAN.md, then `git add -A` then `git commit` with a message describing the changes. After the commit, `git push`.

99999. Important: When authoring documentation, capture the why — tests and implementation importance.
999999. Important: Single sources of truth, no migrations/adapters. If tests unrelated to your work fail, resolve them as part of the increment.
9999999. As soon as there are no build or test errors create a git tag. If there are no git tags start at 0.0.0 and increment patch by 1 for example 0.0.1 if 0.0.0 does not exist.
99999999. You may add extra logging if required to debug issues.
999999999. Keep @IMPLEMENTATION_PLAN.md current with learnings using a subagent — future work depends on this to avoid duplicating efforts. Update especially after finishing your turn.
9999999999. When you learn something new about how to run the application, update @AGENTS.md using a subagent but keep it brief. For example if you run commands multiple times before learning the correct command then that file should be updated.
99999999999. For any bugs you notice, resolve them or document them in @IMPLEMENTATION_PLAN.md using a subagent even if it is unrelated to the current piece of work.
999999999999. Implement functionality completely. Placeholders and stubs waste efforts and time redoing the same work.
9999999999999. When @IMPLEMENTATION_PLAN.md becomes large periodically clean out the items that are completed from the file using a subagent.
99999999999999. If you find inconsistencies in the specs/* then use an Opus 4.5 subagent with 'ultrathink' requested to update the specs.
999999999999999. IMPORTANT: Keep @AGENTS.md operational only — status updates and progress notes belong in `IMPLEMENTATION_PLAN.md`. A bloated AGENTS.md pollutes every future loop's context.
```

### AGENTS.md

Single, canonical "heart of the loop" - a concise, operational "how to run/build" guide.

- NOT a changelog or progress diary
- Describes how to build/run the project
- Captures operational learnings that improve the loop
- Keep brief (~60 lines)

Status, progress, and planning belong in `IMPLEMENTATION_PLAN.md`, not here.

**Template:**

```markdown
## Build & Run

Succinct rules for how to BUILD the project:

## Validation

Run these after implementing to get immediate feedback:

- Tests: `[test command]`
- Typecheck: `[typecheck command]`
- Lint: `[lint command]`

## Operational Notes

Succinct learnings about how to RUN the project:

...

### Codebase Patterns

...
```

### IMPLEMENTATION_PLAN.md

Prioritized bullet-point list of tasks derived from gap analysis (specs vs code) - generated by Ralph.

- Created via PLANNING mode
- Updated during BUILDING mode (mark complete, add discoveries, note bugs)
- Can be regenerated – "I have deleted the TODO list multiple times" → switch to PLANNING mode
- Self-correcting – BUILDING mode can even create new specs if missing

No pre-specified template - let Ralph/LLM dictate and manage format that works best for it.

### specs/*

One markdown file per topic of concern. These are the source of truth for what should be built.

- Created during Requirements phase (human + LLM conversation)
- Consumed by both PLANNING and BUILDING modes
- Can be updated if inconsistencies discovered (rare, use subagent)

No pre-specified template - let Ralph/LLM dictate and manage format that works best for it.

---

## Enhancements

### Use Claude's AskUserQuestionTool for Planning

During Phase 1 (Define Requirements), use Claude's built-in `AskUserQuestionTool` to systematically explore JTBD, topics of concern, edge cases, and acceptance criteria through structured interview before writing specs.

**When to use:** Minimal/vague initial requirements, need to clarify constraints, or multiple valid approaches exist.

**Invoke:** "Interview me using AskUserQuestion to understand [JTBD/topic/acceptance criteria/...]"

### Acceptance-Driven Backpressure

Derive test requirements during planning from acceptance criteria. This creates explicit connections between specifications and verification.

Add to `PROMPT_plan.md` instruction 1:
```
For each task in the plan, derive required tests from acceptance criteria in specs - what specific outcomes need verification (behavior, performance, edge cases). Tests verify WHAT works, not HOW it's implemented.
```

Add to `PROMPT_build.md`:
```
999. Required tests derived from acceptance criteria must exist and pass before committing. Tests are part of implementation scope, not optional.
```

### Non-Deterministic Backpressure

For acceptance criteria that resist programmatic validation (creative quality, aesthetics, UX feel), use LLM-as-judge tests with binary pass/fail.

Create `src/lib/llm-review.ts`:
```typescript
interface ReviewResult {
  pass: boolean;
  feedback?: string;
}

function createReview(config: {
  criteria: string;
  artifact: string;
  intelligence?: "fast" | "smart";
}): Promise<ReviewResult>;
```

### Ralph-Friendly Work Branches

To use branches with Ralph while maintaining the pattern, scope at plan creation, not at task selection.

**Workflow:**
1. Full planning on main: `./loop.sh plan`
2. Create work branch: `git checkout -b ralph/feature-name`
3. Scoped planning: `./loop.sh plan-work "feature description"`
4. Build: `./loop.sh 20`
5. PR: `gh pr create`

This requires adding `plan-work` mode to `loop.sh` and creating `PROMPT_plan_work.md`.

### JTBD → Story Map → SLC Release

For product-focused releases, extend the framework:

1. Define audience and their JTBDs → `AUDIENCE_JTBD.md`
2. Define activities for each JTBD → `specs/*.md`
3. Plan slices through User Story Map
4. Build Simple, Lovable, Complete releases

---

## Setup Commands

To set up Ralph in the current project, copy the template files:

```bash
# From the skill templates directory
cp .claude/skills/ralph/templates/loop.sh ./
cp .claude/skills/ralph/templates/PROMPT_plan.md ./
cp .claude/skills/ralph/templates/PROMPT_build.md ./
cp .claude/skills/ralph/templates/AGENTS.md ./
touch IMPLEMENTATION_PLAN.md
mkdir -p specs

# Make loop executable
chmod +x loop.sh
```

Then fill in:
1. `AGENTS.md` with your build/test/lint commands
2. `PROMPT_plan.md` with your `[project-specific goal]`
3. `specs/*.md` with your requirements

---

## Attribution

Based on Geoffrey Huntley's Ralph technique and Clayton Farr's Ralph Playbook.

- Original: https://ghuntley.com/ralph/
- Playbook: https://github.com/ghuntley/how-to-ralph-wiggum
