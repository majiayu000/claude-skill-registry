---
name: ralph-plan
description: Interactive vision planning using Socratic method. Use when user asks to "ralph plan vision", "plan a vision", "ralph plan roadmap", "ralph plan stories", "ralph plan tasks", or needs to define product vision/roadmap/stories/tasks through guided dialogue.
argument-hint: <vision|roadmap|stories|tasks|subtasks> [options]
---

# Ralph Plan

Interactive planning tools for defining product vision, roadmap, user stories, and tasks.

## Execution Instructions

When this skill is invoked, check the ARGUMENTS provided:

### If argument is `vision`:

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/ralph/planning/vision-interactive.md` (relative to project root). DO NOT proceed without reading this file first - it contains the full Socratic workflow you MUST follow.

After reading the workflow file, begin the session with:

---

"Let's work on clarifying your product vision. I'll ask questions to help you articulate what you're building and why.

**To start:** What problem are you trying to solve, and for whom?

(You can say 'done' at any point when you feel we've covered enough. I'll offer to save our progress incrementally as we go.)"

---

Then follow ALL phases in the workflow file you just read.

### If argument is `roadmap`:

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/ralph/planning/roadmap-interactive.md` (relative to project root). DO NOT proceed without reading this file first - it contains the full Socratic workflow with ALL phases you MUST follow.

1. First, read `docs/planning/VISION.md` to understand the product vision
2. If no VISION.md exists, inform the user and suggest they run `/ralph-plan vision` first
3. Begin the session with:

---

"Let's work on your product roadmap. I've read your vision document and I'll ask questions to help translate it into actionable milestones.

**To start:** What's the most important thing users should be able to do in your first release?

(You can say 'done' at any point when you feel we've covered enough. I'll offer to save our progress incrementally as we define milestones.)"

---

Then follow ALL phases in the workflow file you just read. Do NOT skip phases or give shallow output.

### If argument is `stories` (with optional milestone name):

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/ralph/planning/stories-interactive.md` (relative to project root). DO NOT proceed without reading this file first - it contains the full Socratic workflow you MUST follow.

1. First, read `docs/planning/VISION.md` and `docs/planning/ROADMAP.md` to understand the product context
2. If no VISION.md or ROADMAP.md exists, inform the user and suggest they run `/ralph-plan vision` and `/ralph-plan roadmap` first
3. If a milestone name was provided as a second argument (e.g., `/ralph-plan stories my-milestone`), use that milestone
4. If no milestone was provided, ask the user which milestone they want to create stories for
5. Begin the session with:

---

"Let's create user stories for the **[milestone]** milestone.

I've reviewed the roadmap - this milestone focuses on: [list key deliverables from ROADMAP.md]

**To start:** Who are the primary users that will benefit from these capabilities? What are they trying to accomplish?

(You can say 'done' at any point when you feel we've covered enough, or ask me to save a story when we've defined it well.)"

---

Then follow ALL phases in the workflow file you just read.

**IMPORTANT - Incremental Saving:** Save each story as it's well-defined:
- After each story is discussed and refined, offer to write it to a file
- Don't batch all stories at the end
- This protects against crashes/disconnects

### If argument is `tasks` (with required story ID):

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/ralph/planning/tasks-interactive.md` (relative to project root). DO NOT proceed without reading this file first - it contains the full Socratic workflow you MUST follow.

1. A story ID must be provided as the second argument (e.g., `/ralph-plan tasks STORY-001-auth`)
2. If no story ID is provided, ask the user which story to create tasks for and list available stories
3. Find the story file in `docs/planning/milestones/*/stories/<story-id>.md`
4. If the story is not found, list available stories and ask for clarification
5. Read the story file to understand the user outcomes
6. Explore the codebase to understand existing patterns relevant to the story
7. Begin the session with:

---

"Let's create technical tasks for story **[story-id]**.

I've read the story - it focuses on: [brief summary of narrative and key acceptance criteria].

Let me also explore the codebase to understand existing patterns..."

[Read relevant files/directories based on the story context]

"Based on the story and the codebase, here's what I see:
- [relevant existing code/patterns]
- [dependencies/integrations involved]

**To start:** Looking at the acceptance criteria, which capability should we tackle first? What's your thinking on the technical approach?

(You can say 'done' at any point when you feel we've covered enough, or ask me to save a task when we've defined it well.)"

---

Then follow ALL phases in the workflow file you just read.

**IMPORTANT - Incremental Saving:** Save each task as it's well-defined:
- After each task is discussed and refined, offer to write it to a file
- Don't batch all tasks at the end
- This protects against crashes/disconnects

### If argument is `tasks <story-id> --auto`:

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/ralph/planning/tasks-auto.md` (relative to project root). DO NOT proceed without reading this file first - it contains the full auto-generation workflow.

1. A story ID must be provided (e.g., `/ralph-plan tasks STORY-001-auth --auto`)
2. Find the story file in `docs/planning/milestones/*/stories/<story-id>.md`
3. If the story is not found, report error and list available stories
4. Analyze the codebase for patterns relevant to the story
5. Generate task files automatically following the workflow

**Auto mode outputs:**
- Task files are created without interaction
- Summary reports what was generated
- No incremental saving prompts (all tasks saved at once)

### If argument is `tasks --milestone <name> --auto`:

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/ralph/planning/tasks-milestone.md` (relative to project root). DO NOT proceed without reading this file first - it contains the parallel agent orchestration workflow.

1. A milestone name must be provided (e.g., `/ralph-plan tasks --milestone ralph --auto`)
2. Discover all stories in `docs/planning/milestones/<name>/stories/`
3. If no stories found, report error with available milestones
4. Calculate starting task ID by scanning ALL existing task directories
5. Spawn parallel `task-generator` subagents (one per story)
6. Each agent generates tasks for its story independently
7. Report summary of all generated tasks

**Parallelization benefits:**
- Faster: Multiple stories processed concurrently
- Better quality: Smaller context per agent
- Consistent: Same patterns applied across all stories

### If argument is `subtasks` (with required source):

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/ralph/planning/subtasks-from-source.md` (relative to project root). DO NOT proceed without reading this file first - it contains the full workflow you MUST follow.

1. A source must be provided - either:
   - A file path (e.g., `/ralph-plan subtasks ./review-findings.md`)
   - A text description (e.g., `/ralph-plan subtasks "Fix array bounds check"`)
   - The `--review` flag to parse `logs/reviews.jsonl`
2. If no source and no `--review` flag, ask the user what source to use
3. Optionally accept `--milestone <name>` to set target milestone
4. Optionally accept `--story <ref>` to link subtasks to a story
5. Optionally accept `--1-to-1` flag to bypass decomposition/sizing logic (one input item → one subtask)
6. Read the source and extract actionable items
7. Generate subtasks following the schema and sizing constraints from the workflow (unless `--1-to-1` is set)
8. Write to `docs/planning/milestones/<milestone>/subtasks.json` (append or create)

Begin the session with:

---

"I'll generate subtasks from the provided source.

**Source:** [file path / text / review diary]
**Target:** [milestone / story if provided]

Let me read and analyze the source to extract actionable items..."

---

Then follow ALL steps in the workflow file you just read.

### If no argument or unknown argument:

Show the usage documentation below.

---

## Usage

```
/ralph-plan <subcommand>
```

## Subcommands

| Subcommand | Description |
|------------|-------------|
| `vision` | Start interactive vision planning session |
| `roadmap` | Start interactive roadmap planning session |
| `stories` | Start interactive stories planning session for a milestone |
| `tasks` | Start interactive tasks planning session for a story |
| `subtasks` | Generate subtasks from any source (file, text, or review diary) |

## Vision Planning

Start an interactive Socratic dialogue to help define and clarify product vision.

### Invocation

```
/ralph-plan vision
```

### What Happens

1. Begins a multi-turn conversation using the Socratic method
2. Guides you through exploring:
   - Product purpose and problem being solved
   - Target users using Jobs To Be Done framework
   - Key capabilities and differentiators
   - Current state vs future vision
3. Creates or updates `docs/planning/VISION.md` when ready

### Important Notes

- This is **interactive only** - no auto mode exists for vision planning
- Vision planning requires human insight and decision-making
- You control the pace and can exit anytime by saying "done"
- The session can span multiple turns as needed

## Roadmap Planning

Start an interactive Socratic dialogue to help define product milestones and roadmap.

### Invocation

```
/ralph-plan roadmap
```

### What Happens

1. Reads your existing VISION.md document (if it exists)
2. Begins a multi-turn conversation using the Socratic method
3. Guides you through exploring:
   - Scope and priority for first release
   - Tradeoffs and hard decisions
   - Dependency mapping between features
   - Milestone definition with outcomes
4. Creates or updates `docs/planning/ROADMAP.md` when ready

### Important Notes

- Requires VISION.md to exist (run `/ralph-plan vision` first)
- Interactive mode available, auto mode available via `roadmap-auto.md`
- Milestones use outcome-based names, not version numbers
- No time estimates - focus on sequence and dependencies
- You control the pace and can exit anytime by saying "done"

## Stories Planning

Start an interactive Socratic dialogue to help create user stories for a specific milestone.

### Invocation

```
/ralph-plan stories [milestone-name]
```

### What Happens

1. Reads your existing VISION.md and ROADMAP.md documents
2. If a milestone name is provided, uses that milestone
3. If no milestone is provided, asks which milestone to create stories for
4. Begins a multi-turn conversation using Socratic method with JTBD framework
5. Guides you through exploring:
   - Primary users and their context
   - Jobs to be done (functional, emotional, social)
   - Story scope and boundaries
   - Priority and sequencing
   - Tradeoffs and decisions
   - Acceptance criteria
6. Creates story files in `docs/planning/milestones/<milestone>/stories/`

### Important Notes

- Requires VISION.md and ROADMAP.md to exist (run vision and roadmap planning first)
- Uses Jobs To Be Done (JTBD) framework for user-centered stories
- Stories focus on user outcomes, not technical implementation
- You control the pace and can exit anytime by saying "done"
- Can save stories incrementally during the session

## Tasks Planning

Create technical tasks from stories. Two modes available:

### Single Story Mode (Interactive or Auto)

```
/ralph-plan tasks <story-id>
```

**What Happens:**
1. Reads the specified story file to understand user outcomes
2. Explores the codebase to understand existing patterns relevant to the story
3. Begins a multi-turn conversation using Socratic method (or auto-generates in auto mode)
4. Creates task files in `docs/planning/tasks/`

### Milestone Mode (Auto Only)

```
aaa ralph plan tasks --milestone <name> --auto
```

**What Happens:**
1. Discovers all stories in `docs/planning/milestones/<name>/stories/`
2. Spawns parallel `task-generator` subagents (one per story)
3. Each agent analyzes its story and the codebase
4. Task files are generated concurrently for all stories
5. Reports summary of all generated tasks

**Benefits:**
- Faster: Parallel generation vs sequential
- Better quality: Smaller context per agent
- Consistent: Same patterns applied across stories

### Important Notes

- **Single story mode**: Requires `--story <id>`
- **Milestone mode**: Requires `--milestone <name>` AND `--auto`
- Cannot combine `--story` and `--milestone`
- Tasks are linked to their parent story for traceability
- Focus is on technical implementation, not user outcomes
- References specific files and patterns from the codebase

## Subtasks Planning

Generate subtasks from any source: file, text description, or review diary.

### Invocation

```
/ralph-plan subtasks <source>
/ralph-plan subtasks --review
/ralph-plan subtasks <source> --1-to-1
```

### Input Sources

| Source Type | Example |
|-------------|---------|
| File path | `/ralph-plan subtasks ./review-findings.md` |
| Text description | `/ralph-plan subtasks "Fix array bounds check"` |
| Review diary | `/ralph-plan subtasks --review` |

### Optional Flags

- `--milestone <name>` - Target milestone for subtasks.json location
- `--story <ref>` - Link subtasks to a parent story
- `--1-to-1` - Direct mapping mode: bypass decomposition/sizing logic and map each input item directly to one subtask

### What Happens

1. Reads the source (file content, text, or logs/reviews.jsonl)
2. Extracts actionable items from the source
3. Generates subtasks following schema and sizing constraints
4. Validates each subtask fits single context window
5. Writes to `docs/planning/milestones/<milestone>/subtasks.json`

### Important Notes

- Each subtask should touch 1-3 files (not counting tests)
- Subtasks must be completable in 15-30 tool calls
- IDs are globally unique (SUB-NNN format)
- Uses supervised mode by default (user watches generation)

### When to Use `--1-to-1`

Use the `--1-to-1` flag when:
- **Tasks are already well-scoped** - Each input item is already the right size for a subtask
- **You want predictable output** - One input item → one subtask, no splitting or merging
- **Importing from external sources** - Converting issue tracker items or PR descriptions directly

Do NOT use when:
- Input items vary wildly in scope (some huge, some tiny)
- You want intelligent sizing and decomposition
- Items need to be grouped or split for optimal context window usage

## CLI Equivalent

This skill provides the same functionality as:

```bash
aaa ralph plan vision
aaa ralph plan roadmap
aaa ralph plan stories --milestone <name>
aaa ralph plan tasks --story <story-id>           # Single story
aaa ralph plan tasks --milestone <name> --auto    # All stories in milestone
aaa ralph plan subtasks <source> --milestone <name>   # From file/text
aaa ralph plan subtasks --review --milestone <name>   # From review diary
```

## References

- **Vision prompt:** `context/workflows/ralph/planning/vision-interactive.md`
- **Roadmap prompt:** `context/workflows/ralph/planning/roadmap-interactive.md`
- **Stories prompt:** `context/workflows/ralph/planning/stories-interactive.md`
- **Tasks prompt:** `context/workflows/ralph/planning/tasks-interactive.md`
- **Tasks milestone prompt:** `context/workflows/ralph/planning/tasks-milestone.md`
- **Subtasks from source:** `context/workflows/ralph/planning/subtasks-from-source.md`
- **Subtasks from task:** `context/workflows/ralph/planning/subtasks-auto.md`
- **Task generator agent:** `.claude/agents/task-generator.md`
