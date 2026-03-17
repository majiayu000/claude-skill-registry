---
name: kata-help
description: Show available Kata skills, displaying the usage guide, explaining skill reference, or when the user asks for help with Kata. Triggers include "help", "show skills", "list skills", "what skills", "kata skills", and "usage guide".
metadata:
  version: "0.1.0"
allowed-tools: Read Write Bash
---

<objective>
Display the complete Kata skill reference with version info.

First, read the installed version:

```bash
if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then
  cat "$CLAUDE_PLUGIN_ROOT/VERSION" 2>/dev/null
else
  echo "unknown"
fi
```

Then output the reference content below, inserting the version at the top. Do NOT add:

- Project-specific analysis
- Git status or file context
- Next-step suggestions
- Any commentary beyond the reference
  </objective>

<reference>
# Kata Skill Reference

**Version:** {version from bash above}

**Kata** is a spec-driven development framework for Claude Code. It creates hierarchical project plans optimized for agentic development.

## Quick Start

1. `/kata-new-project` - Initialize project (includes research, requirements, roadmap)
2. `/kata-plan-phase 1` - Create detailed plan for first phase
3. `/kata-execute-phase 1` - Execute the phase

## Staying Updated

Kata evolves fast. Check for updates periodically:

```
/kata-whats-new
```

Shows what changed since your installed version and how to update.

## Core Workflow

```
/kata-new-project → /kata-plan-phase → /kata-execute-phase → repeat
```

### Project Initialization

**`/kata-new-project`**
Initialize new project through unified flow.

One skill takes you from idea to ready-for-planning:
- Deep questioning to understand what you're building
- Optional domain research (spawns 4 parallel researcher agents)
- Requirements definition with v1/v2/out-of-scope scoping
- Roadmap creation with phase breakdown and success criteria

Creates all `.planning/` artifacts:
- `PROJECT.md` — vision and requirements
- `config.json` — workflow mode (interactive/yolo)
- `research/` — domain research (if selected)
- `REQUIREMENTS.md` — scoped requirements with REQ-IDs
- `ROADMAP.md` — phases mapped to requirements
- `STATE.md` — project memory

Usage: `/kata-new-project`

**`/kata-map-codebase`**
Map an existing codebase for brownfield projects.

- Analyzes codebase with parallel Explore agents
- Creates `.planning/codebase/` with 7 focused documents
- Covers stack, architecture, structure, conventions, testing, integrations, concerns
- Use before `/kata-new-project` on existing codebases

Usage: `/kata-map-codebase`

### Phase Planning

**`/kata-discuss-phase <number>`**
Help articulate your vision for a phase before planning.

- Captures how you imagine this phase working
- Creates CONTEXT.md with your vision, essentials, and boundaries
- Use when you have ideas about how something should look/feel

Usage: `/kata-discuss-phase 2`

**`/kata-research-phase <number>`**
Comprehensive ecosystem research for niche/complex domains.

- Discovers standard stack, architecture patterns, pitfalls
- Creates RESEARCH.md with "how experts build this" knowledge
- Use for 3D, games, audio, shaders, ML, and other specialized domains
- Goes beyond "which library" to ecosystem knowledge

Usage: `/kata-research-phase 3`

**`/kata-listing-phase-assumptions <number>`**
See what Claude is planning to do before it starts.

- Shows Claude's intended approach for a phase
- Lets you course-correct if Claude misunderstood your vision
- No files created - conversational output only

Usage: `/kata-listing-phase-assumptions 3`

**`/kata-plan-phase <number>`**
Create detailed execution plan for a specific phase.

- Generates `.planning/phases/XX-phase-name/XX-YY-PLAN.md`
- Breaks phase into concrete, actionable tasks
- Includes verification criteria and success measures
- Multiple plans per phase supported (XX-01, XX-02, etc.)

Usage: `/kata-plan-phase 1`
Result: Creates `.planning/phases/01-foundation/01-01-PLAN.md`

### Execution

**`/kata-execute-phase <phase-number>`**
Execute all plans in a phase.

- Groups plans by wave (from frontmatter), executes waves sequentially
- Plans within each wave run in parallel via Task tool
- Verifies phase goal after all plans complete
- Updates REQUIREMENTS.md, ROADMAP.md, STATE.md

Usage: `/kata-execute-phase 5`

### Quick Mode

**`/kata-execute-quick-task`**
Execute small, ad-hoc tasks with Kata guarantees but skip optional agents.

Quick mode uses the same system with a shorter path:
- Spawns planner + executor (skips researcher, checker, verifier)
- Quick tasks live in `.planning/quick/` separate from planned phases
- Updates STATE.md tracking (not ROADMAP.md)

Use when you know exactly what to do and the task is small enough to not need research or verification.

Usage: `/kata-execute-quick-task`
Result: Creates `.planning/quick/NNN-slug/PLAN.md`, `.planning/quick/NNN-slug/SUMMARY.md`

### Roadmap Management

**`/kata-add-phase <description>`**
Add new phase to end of current milestone.

- Appends to ROADMAP.md
- Uses next sequential number
- Updates phase directory structure

Usage: `/kata-add-phase "Add admin dashboard"`

**`/kata-insert-phase <after> <description>`**
Insert urgent work as decimal phase between existing phases.

- Creates intermediate phase (e.g., 7.1 between 7 and 8)
- Useful for discovered work that must happen mid-milestone
- Maintains phase ordering

Usage: `/kata-insert-phase 7 "Fix critical auth bug"`
Result: Creates Phase 7.1

**`/kata-remove-phase <number>`**
Remove a future phase and renumber subsequent phases.

- Deletes phase directory and all references
- Renumbers all subsequent phases to close the gap
- Only works on future (unstarted) phases
- Git commit preserves historical record

Usage: `/kata-remove-phase 17`
Result: Phase 17 deleted, phases 18-20 become 17-19

**`/kata-move-phase <phase> <operation>`**
Move a phase between milestones or reorder within a milestone.

- Cross-milestone: moves phase to target milestone, renumbers both
- Reorder: changes phase position within milestone, renumbers all
- Only pending phases can be moved

Usage: `/kata-move-phase 3 to v1.6.0` (cross-milestone)
Usage: `/kata-move-phase 3 before 1` (reorder within milestone)

### Milestone Management

**`/kata-add-milestone <name>`**
Start a new milestone through unified flow.

- Deep questioning to understand what you're building next
- Optional domain research (spawns 4 parallel researcher agents)
- Requirements definition with scoping
- Roadmap creation with phase breakdown

Mirrors `/kata-new-project` flow for brownfield projects (existing PROJECT.md).

Usage: `/kata-add-milestone "v2.0 Features"`

**`/kata-complete-milestone <version>`**
Archive completed milestone and prepare for next version.

- Creates MILESTONES.md entry with stats
- Archives full details to milestones/ directory
- Creates git tag for the release
- Prepares workspace for next version

Usage: `/kata-complete-milestone 1.0.0`

### Progress Tracking

**`/kata-track-progress`**
Check project status and intelligently route to next action.

- Shows visual progress bar and completion percentage
- Summarizes recent work from SUMMARY files
- Displays current position and what's next
- Lists key decisions and open issues
- Offers to execute next plan or create it if missing
- Detects 100% milestone completion

Usage: `/kata-track-progress`

### Session Management

**`/kata-resume-work`**
Resume work from previous session with full context restoration.

- Reads STATE.md for project context
- Shows current position and recent progress
- Offers next actions based on project state

Usage: `/kata-resume-work`

**`/kata-pause-work`**
Create context handoff when pausing work mid-phase.

- Creates .continue-here file with current state
- Updates STATE.md session continuity section
- Captures in-progress work context

Usage: `/kata-pause-work`

### Debugging

**`/kata-debug [issue description]`**
Systematic debugging with persistent state across context resets.

- Gathers symptoms through adaptive questioning
- Creates `.planning/debug/[slug].md` to track investigation
- Investigates using scientific method (evidence → hypothesis → test)
- Survives `/clear` — run `/kata-debug` with no args to resume
- Archives resolved issues to `.planning/debug/resolved/`

Usage: `/kata-debug "login button doesn't work"`
Usage: `/kata-debug` (resume active session)

### Issue Management

**`/kata-add-issue [description]`**
Capture idea or task as issue from current conversation.

- Extracts context from conversation (or uses provided description)
- Creates structured issue file in `.planning/issues/open/`
- Infers area from file paths for grouping
- Checks for duplicates before creating
- Updates STATE.md issue count

Usage: `/kata-add-issue` (infers from conversation)
Usage: `/kata-add-issue Add auth token refresh`

**`/kata-check-issues [area]`**
List pending issues and select one to work on.

- Lists all pending issues with title, area, age
- Optional area filter (e.g., `/kata-check-issues api`)
- Loads full context for selected issue
- Routes to appropriate action (work now, add to phase, brainstorm)
- Moves issue to done/ when work begins

Usage: `/kata-check-issues`
Usage: `/kata-check-issues api`

### User Acceptance Testing

**`/kata-verify-work [phase]`**
Validate built features through conversational UAT.

- Extracts testable deliverables from SUMMARY.md files
- Presents tests one at a time (yes/no responses)
- Automatically diagnoses failures and creates fix plans
- Ready for re-execution if issues found

Usage: `/kata-verify-work 3`

### Milestone Auditing

**`/kata-audit-milestone [version]`**
Audit milestone completion against original intent.

- Reads all phase VERIFICATION.md files
- Checks requirements coverage
- Spawns integration checker for cross-phase wiring
- Creates MILESTONE-AUDIT.md with gaps and tech debt

Usage: `/kata-audit-milestone`

**`/kata-plan-milestone-gaps`**
Create phases to close gaps identified by audit.

- Reads MILESTONE-AUDIT.md and groups gaps into phases
- Prioritizes by requirement priority (must/should/nice)
- Adds gap closure phases to ROADMAP.md
- Ready for `/kata-plan-phase` on new phases

Usage: `/kata-plan-milestone-gaps`

### Configuration

**`/kata-configure-settings`**
Configure workflow toggles and model profile interactively.

- Toggle researcher, plan checker, verifier agents
- Select model profile (quality/balanced/budget)
- Updates `.planning/config.json`

Usage: `/kata-configure-settings`

**`/kata-set-profile <profile>`**
Quick switch model profile for Kata agents.

- `quality` — Opus everywhere except verification
- `balanced` — Opus for planning, Sonnet for execution (default)
- `budget` — Sonnet for writing, Haiku for research/verification

Usage: `/kata-set-profile budget`

### Utility Skills

**`/kata-help`**
Show this skill reference.

**`/kata-whats-new`**
See what's changed since your installed version.

- Shows installed vs latest version comparison
- Displays changelog entries for versions you've missed
- Highlights breaking changes
- Provides update instructions when behind

Usage: `/kata-whats-new`

## Files & Structure

```
.planning/
├── PROJECT.md            # Project vision
├── ROADMAP.md            # Current phase breakdown
├── STATE.md              # Project memory & context
├── config.json           # Workflow mode & gates
├── issues/               # Captured ideas and tasks
│   ├── pending/          # Issues waiting to be worked on
│   └── done/             # Completed issues
├── debug/                # Active debug sessions
│   └── resolved/         # Archived resolved issues
├── codebase/             # Codebase map (brownfield projects)
│   ├── STACK.md          # Languages, frameworks, dependencies
│   ├── ARCHITECTURE.md   # Patterns, layers, data flow
│   ├── STRUCTURE.md      # Directory layout, key files
│   ├── CONVENTIONS.md    # Coding standards, naming
│   ├── TESTING.md        # Test setup, patterns
│   ├── INTEGRATIONS.md   # External services, APIs
│   └── CONCERNS.md       # Tech debt, known issues
└── phases/
    ├── 01-foundation/
    │   ├── 01-01-PLAN.md
    │   └── 01-01-SUMMARY.md
    └── 02-core-features/
        ├── 02-01-PLAN.md
        └── 02-01-SUMMARY.md
```

## Workflow Modes

Set during `/kata-new-project`:

**Interactive Mode**

- Confirms each major decision
- Pauses at checkpoints for approval
- More guidance throughout

**YOLO Mode**

- Auto-approves most decisions
- Executes plans without confirmation
- Only stops for critical checkpoints

Change anytime by editing `.planning/config.json`

## Planning Configuration

Configure how planning artifacts are managed in `.planning/config.json`:

**`planning.commit_docs`** (default: `true`)
- `true`: Planning artifacts committed to git (standard workflow)
- `false`: Planning artifacts kept local-only, not committed

When `commit_docs: false`:
- Add `.planning/` to your `.gitignore`
- Useful for OSS contributions, client projects, or keeping planning private
- All planning files still work normally, just not tracked in git

**`planning.search_gitignored`** (default: `false`)
- `true`: Add `--no-ignore` to broad ripgrep searches
- Only needed when `.planning/` is gitignored and you want project-wide searches to include it

Example config:
```json
{
  "planning": {
    "commit_docs": false,
    "search_gitignored": true
  }
}
```

## Common Workflows

**Starting a new project:**

```
/kata-new-project        # Unified flow: questioning → research → requirements → roadmap
/clear
/kata-plan-phase 1       # Create plans for first phase
/clear
/kata-execute-phase 1    # Execute all plans in phase
```

**Resuming work after a break:**

```
/kata-track-progress  # See where you left off and continue
```

**Adding urgent mid-milestone work:**

```
/kata-insert-phase 5 "Critical security fix"
/kata-plan-phase 5.1
/kata-execute-phase 5.1
```

**Completing a milestone:**

```
/kata-complete-milestone 1.0.0
/clear
/kata-add-milestone  # Start next milestone (questioning → research → requirements → roadmap)
```

**Capturing ideas during work:**

```
/kata-add-issue                    # Capture from conversation context
/kata-add-issue Fix modal z-index  # Capture with explicit description
/kata-check-issues                 # Review and work on issues
/kata-check-issues api             # Filter by area
```

**Debugging an issue:**

```
/kata-debug "form submission fails silently"  # Start debug session
# ... investigation happens, context fills up ...
/clear
/kata-debug                                    # Resume from where you left off
```

## Getting Help

- Read `.planning/PROJECT.md` for project vision
- Read `.planning/STATE.md` for current context
- Check `.planning/ROADMAP.md` for phase status
- Run `/kata-track-progress` to check where you're up to
  </reference>
