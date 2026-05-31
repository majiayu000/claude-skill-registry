---
name: gsd-workflow
description: Use when the user asks "what should I work on", mentions GSD phases, ROADMAP, or .planning/ artifacts. Routes to the correct GSD command for the current project state.
description-frequency: on-demand
user-invocable: true
type: skill
category: gsd
status: stable
origin: tibsfox
modified: false
first_seen: 2026-02-26
first_path: project-claude/skills/gsd-workflow/SKILL.md
superseded_by: null
---
# GSD Workflow Routing

Route user intent to GSD commands. Explicit /gsd: commands bypass routing -- read `.claude/commands/gsd/[command].md` directly.

## 5-Stage Classification Pipeline

When the user provides natural language related to project workflow, route through the GSD Orchestrator's classification pipeline:

1. **Exact match** -- direct command mapping (fastest)
2. **Lifecycle filtering** -- narrow candidates by current project phase
3. **Bayesian classification** -- probabilistic intent matching
4. **Semantic fallback** -- embedding-based similarity for ambiguous requests
5. **Confidence resolution** -- threshold check; ask user if uncertain

**When to use the orchestrator:** The user says something like "review the requirements," "what's the project status," "let's verify phase 3," or any natural language that maps to a GSD lifecycle action but doesn't use explicit slash commands.

**When to bypass it:** The user types an explicit GSD slash command. Execute directly.

**When confidence is low:** Ask the user to clarify rather than guessing. A wrong routing is worse than a clarifying question.

## Quick Command Routing

The top-10 most common routes:

| User Says | Route To |
|-----------|----------|
| "what should I work on" | `/gsd:progress` |
| "continue where I left off" | `/gsd:progress` |
| "build phase X" | `/gsd:execute-phase X` |
| "plan the next phase" | `/gsd:plan-phase N` |
| "discuss how phase X should work" | `/gsd:discuss-phase N` |
| "something's broken" | `/gsd:debug` |
| "quick fix / small task" | `/gsd:quick` |
| "verify phase X" | `/gsd:verify-work X` |
| "add a phase" | `/gsd:add-phase` |
| "start new project" | `/gsd:new-project` |

For full routing tables including skill-creator actions, see `references/command-routing.md`.

## Guidance Heuristics

### When to Suggest GSD

**Always suggest GSD when:**
- User asks to build, create, or implement something substantial
- User seems unsure where to start
- Work would benefit from planning before coding
- Context is fresh (session just started)

**Suggest with explanation:**
```
This looks like a good candidate for `/gsd:plan-phase N` -- it'll break this
down into atomic tasks with verification criteria. Want me to run that,
or would you prefer to dive in directly?
```

### When to Suggest skill-creator

**Suggest skill-creator when:**
- You notice the same sequence of steps has occurred 3+ times
- The user corrects the same kind of output repeatedly
- A workflow is complex enough to benefit from codification
- The user asks "why do I keep having to tell you this?"

**Suggest naturally:**
```
I've noticed we run the same lint -> test -> fix cycle after every code change.
Want me to capture this as a skill so it happens automatically?
```

### When to Allow Override

**Respect user override when:**
- They explicitly say "just do it" or "skip the ceremony"
- The task is genuinely trivial (< 5 minutes)
- They're exploring/experimenting, not building
- They have domain expertise and know what they want

**Acknowledge gracefully:**
```
Got it -- working on this directly. If it grows in scope, we can always
capture it in a plan retroactively with `/gsd:quick`.
```

### When to Push Back

**Gently push back when:**
- User is about to make changes without understanding current state
- Work would conflict with existing plans
- The request is ambiguous and needs questioning

**Push back helpfully:**
```
Before I make changes, let me check `/gsd:progress` -- there might be
existing plans that touch this area. One moment...
```

## Phase Behavior

### Instruction Markers

| Marker | Meaning | Claude Action |
|--------|---------|---------------|
| `## > Next Up` | Next command to run | Read the instruction and execute it |
| `/clear first ->` | Context window full, needs reset | Tell user to run `/clear`, then continue |
| `Ready to build` | Planning complete, execution ready | Proceed to `/gsd:plan-phase` or `/gsd:execute-phase` |
| `ROADMAP CREATED` | Roadmap agent finished | Review output, proceed to next phase |
| `PLAN CREATED` | Planning agent finished | Proceed to execution |

### Workflow Patterns

**Standard Cycle:**
```
/gsd:plan-phase N -> /clear -> /gsd:execute-phase N -> /gsd:verify-work N
```

**Fresh Session Recovery:**
```
/gsd:progress  (or)  /gsd:resume-work
```

**Mid-Work Context Reset:**
```
/gsd:pause-work -> /clear -> /gsd:resume-work
```

**Debugging Flow:**
```
/gsd:debug "description" -> investigate -> /clear -> /gsd:debug (resume)
```

For phase transition details and response patterns, see `references/phase-behavior.md`.

## YOLO Mode

**Detection:** Read `.planning/config.json`. If `"mode": "yolo"`, autonomous operation is active.

**6-Step Autonomous Protocol:**
1. **Read GSD command output carefully** -- it contains your next instruction
2. **Execute the suggested command** -- don't wait for user confirmation
3. **Handle `/clear` requirements** -- inform user when context reset is needed
4. **Continue the workflow** -- GSD is a pipeline, keep it moving
5. **Load relevant skills** -- even in YOLO mode, check for applicable skills before phases
6. **Record observations** -- YOLO sessions generate high-value pattern data

For example recognition and edge cases, see `references/yolo-mode.md`.

## Running GSD Commands

To run a GSD command, read the command file from `.claude/commands/gsd/[command].md` and follow its process. The command file contains:
- `<objective>` -- What the command achieves
- `<process>` -- Step-by-step instructions to follow
- `<success_criteria>` -- How to know it's complete

**Critical:** Don't just acknowledge GSD output -- act on it.

## Skill Loading Before GSD Phases

Before executing any GSD phase, load relevant generated skills:

1. Check `.claude/commands/` for project-level skills
2. Check `~/.claude/commands/` for user-level skills
3. Project-level skills take precedence over user-level on conflict
4. Load only skills relevant to the current phase and task
5. Respect the token budget: 2-5% of context window maximum

**Critical:** When forking subagent contexts for GSD phases (`execute-phase`, `verify-work`), include relevant skills in the subagent's context. Clean context means free of stale conversation history -- not free of learned knowledge.

## Anti-Patterns

- **Don't** stop after GSD output without reading "Next Up" instructions
- **Don't** wait for user input when YOLO mode is enabled and next step is clear
- **Don't** start coding without checking if a plan exists
- **Don't** make changes that span multiple phases in one session
- **Don't** skip commits -- GSD's atomic commits enable rollback
- **Don't** ignore STATE.md warnings or blockers
- **Don't** create plans manually -- use `/gsd:plan-phase`
- **Don't** be rigid -- GSD serves the user, not the other way around
