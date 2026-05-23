---
name: ralph-run
description: Run RALPH autonomous development loop with multi-agent pipeline
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, AskUserQuestion, TodoWrite
---

# RALPH-RUN - Multi-Agent Autonomous Development

Execute the RALPH development cycle using a multi-agent pipeline:
**Planner → Coder → QA Reviewer → QA Fixer**

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-run` | Start with default 10 iterations |
| `/ralph-run 20` | Start with 20 iterations |
| `/ralph-run --parallel` | Run independent subtasks in parallel |
| `/ralph-run --simple` | Skip planner, direct implementation |
| `/ralph-run --task "desc"` | Single-task mode (no PRD needed) |
| `/ralph-run --no-worktree` | Run in current branch (skip worktree isolation) |

## Related Commands

| Command | Description |
|---------|-------------|
| `/ralph-merge` | Merge completed worktree to main branch |
| `/ralph-review` | Review worktree changes before merging |
| `/ralph-discard` | Abandon worktree without merging |

## Triggers

- `/ralph-run`
- "run RALPH"
- "start autonomous development"
- "implement the PRD"

## Critical Rules

1. **USE AGENT PIPELINE** - Planner → Coder → QA Reviewer → QA Fixer
2. **ONE SUBTASK AT A TIME** - Complete fully before moving on
3. **QA MUST PASS** - No skipping QA validation
4. **ASK WHEN UNCERTAIN** - Use AskUserQuestion for ambiguity
5. **RESPECT BOUNDARIES** - Never modify files in boundaries list
6. **LOG TO MEMORY** - Save learnings for future iterations
7. **MAX 3 QA FIX ATTEMPTS** - Escalate to human after 3 failures

## Multi-Agent Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    RALPH Pipeline v3.0                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │ PLANNER  │───▶│  CODER   │───▶│ QA REV   │───▶│ QA FIX   │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│        │                │               │               │       │
│        ▼                ▼               ▼               ▼       │
│   impl_plan.json   subtask done    QA report      fixes done   │
│                                         │               │       │
│                                         └───────────────┘       │
│                                         (loop until pass)       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Phase 0: Prerequisites & Worktree Setup

Before starting, verify environment and set up isolated worktree:

```bash
# Check for PRD
if [ -f prd.json ]; then
  REMAINING=$(cat prd.json | jq '[.userStories[] | select(.passes == false)] | length')
  PROJECT=$(cat prd.json | jq -r '.project')
  BRANCH=$(cat prd.json | jq -r '.branchName // "ralph/feature"')
  echo "✓ PRD: $PROJECT - $REMAINING stories remaining"
else
  echo "❌ No prd.json - run /prd first"
  exit 1
fi

# Check for implementation plan
if [ -f implementation_plan.json ]; then
  echo "✓ Implementation plan exists"
else
  echo "⚠ No implementation_plan.json - will invoke Planner"
fi

# Check for config
[ -f .ralph/config.yaml ] && echo "✓ Config loaded"
[ -f PROJECT_SPEC.md ] && echo "✓ Project spec loaded"
```

### Worktree Isolation (unless --no-worktree)

RALPH runs in an isolated git worktree to protect the main branch:

```
╔════════════════════════════════════════════════════════════════╗
║                    Worktree Setup                               ║
╚════════════════════════════════════════════════════════════════╝

Checking for existing worktree...

Creating worktree for: user-authentication
  Branch: ralph/user-authentication
  Path: .worktrees/user-authentication/

✓ Worktree created
✓ .gitignore updated (ignoring .worktrees/)

All development will happen in: .worktrees/user-authentication/

When complete, use:
  /ralph-merge    - Merge changes to main
  /ralph-review   - Review changes before merging
  /ralph-discard  - Abandon changes
```

**Worktree Structure:**

```
project/
├── .worktrees/                    # Worktree directory (gitignored)
│   └── {spec-name}/               # Isolated working copy
│       ├── src/                   # Full project copy
│       ├── .ralph/                # RALPH state
│       └── prd.json               # PRD file
├── src/                           # Main branch (untouched)
└── prd.json                       # Original PRD
```

**Benefits:**
- Main branch stays clean until merge
- Safe experimentation without polluting history
- Easy discard if implementation goes wrong
- Review all changes before integrating

## Phase 1: Planning (Planner Agent)

**If no `implementation_plan.json` exists, invoke the Planner:**

The Planner agent decomposes stories into subtasks:

```
╔════════════════════════════════════════════════════════════════╗
║                    Phase 1: PLANNING                            ║
║                    Agent: Planner                               ║
╚════════════════════════════════════════════════════════════════╝

Analyzing PRD...
Reading PROJECT_SPEC.md for patterns...
Querying memory for past implementations...

Decomposing US-001 into subtasks:
  ST-001-1: Create User type definitions
  ST-001-2: Create Zod validation schema
  ST-001-3: Create User service layer
  ST-001-4: Add unit tests

Writing implementation_plan.json...
```

**Planner outputs `implementation_plan.json`:**

```json
{
  "stories": [{
    "storyId": "US-001",
    "subtasks": [{
      "id": "ST-001-1",
      "title": "Create User type definitions",
      "files_to_create": ["src/types/user.ts"],
      "files_to_modify": ["src/types/index.ts"],
      "dependencies": [],
      "acceptance_criteria": ["User interface defined", "Exported from index"]
    }]
  }]
}
```

## Phase 2: Implementation (Coder Agent)

For each subtask, the Coder agent implements:

```
╔════════════════════════════════════════════════════════════════╗
║                    Phase 2: IMPLEMENTATION                      ║
║                    Agent: Coder                                 ║
║                    Subtask: ST-001-1                            ║
╚════════════════════════════════════════════════════════════════╝

Reading subtask requirements...
Checking project patterns...
Loading memory insights...

Implementing: Create User type definitions
  → Creating src/types/user.ts
  → Modifying src/types/index.ts

Running quality gates...
  ✓ Typecheck passed
  ✓ Lint passed
  ✓ Tests passed

Subtask implementation complete.
Passing to QA Reviewer...
```

**Coder can spawn subagents for parallel work:**

```javascript
// For independent subtasks, use Task tool
Task({
  subagent_type: "general-purpose",
  description: "Implement ST-001-2",
  prompt: "Implement the Zod validation schema...",
  run_in_background: true
})
```

## Phase 3: QA Review (QA Reviewer Agent)

QA Reviewer validates each subtask against acceptance criteria:

```
╔════════════════════════════════════════════════════════════════╗
║                    Phase 3: QA REVIEW                           ║
║                    Agent: QA Reviewer                           ║
║                    Subtask: ST-001-1                            ║
╚════════════════════════════════════════════════════════════════╝

Validating acceptance criteria...

Criterion: User interface defined
  ✓ PASS - Found User interface in src/types/user.ts:5-15

Criterion: Exported from index
  ✗ FAIL - Export statement missing from src/types/index.ts

Quality Gates:
  ✓ Typecheck
  ✓ Lint
  ✓ Tests

Issues Found: 1
  [HIGH] Missing export in src/types/index.ts

Status: NEEDS_FIX
Passing to QA Fixer...
```

**QA Report Schema:**

```json
{
  "subtaskId": "ST-001-1",
  "status": "needs_fix",
  "criteria": [
    {"criterion": "User interface defined", "passed": true},
    {"criterion": "Exported from index", "passed": false, "issue": "Missing export"}
  ],
  "issues": [{
    "severity": "high",
    "file": "src/types/index.ts",
    "suggestion": "Add: export * from './user';"
  }]
}
```

## Phase 4: QA Fix (QA Fixer Agent)

If QA fails, QA Fixer attempts to resolve issues:

```
╔════════════════════════════════════════════════════════════════╗
║                    Phase 4: QA FIX                              ║
║                    Agent: QA Fixer                              ║
║                    Attempt: 1/3                                 ║
╚════════════════════════════════════════════════════════════════╝

Issues to fix: 1
  [HIGH] Missing export in src/types/index.ts

Applying fix...
  → Editing src/types/index.ts
  → Adding: export * from './user';

Re-running quality gates...
  ✓ Typecheck passed
  ✓ Lint passed
  ✓ Tests passed

Status: ALL_FIXED
Returning to QA Reviewer for verification...
```

**QA Fix Loop:**

```
QA Reviewer ─────▶ PASS ─────▶ Next Subtask
     │
     ▼
  FAIL (issues)
     │
     ▼
QA Fixer ─────▶ Fixed ─────▶ QA Reviewer (re-verify)
     │
     ▼
  Attempt 3 failed
     │
     ▼
ESCALATE TO HUMAN
```

## Phase 5: Commit & Update

After subtask passes QA:

```bash
# Commit the changes
git add -A
git commit -m "feat: ST-001-1 - Create User type definitions

- Created User interface with id, email, createdAt
- Exported from src/types/index.ts
- All quality gates pass

Reviewed-By: QA-Agent
Co-Authored-By: RALPH <noreply@anthropic.com>"

# Update implementation plan
# Mark subtask as complete
```

## Phase 6: Memory & Learning

Log insights to `.ralph/memory/insights.json`:

```json
{
  "context": "Implementing type definitions",
  "learning": "Always export new types from index.ts immediately",
  "tags": ["types", "exports", "patterns"],
  "timestamp": "2026-01-25T10:30:00Z"
}
```

## Phase 7: Context Compaction

If `compact_after_each_story: true` in config:

```
📦 Compacting context...

Preserving:
  - PRD state (5 stories remaining)
  - Memory insights (12 total)
  - Progress log (1 story complete)

Releasing:
  - File exploration details
  - Implementation specifics
  - QA fix history

Context compacted at 60% threshold.
```

## Full Iteration Output

```
╔════════════════════════════════════════════════════════════════╗
║               RALPH Iteration 1 Complete                        ║
╚════════════════════════════════════════════════════════════════╝

Worktree: .worktrees/user-authentication
Branch: ralph/user-authentication

Story: US-001 - Create User model
Subtasks: 4/4 complete

Pipeline Summary:
  ┌──────────────────────────────────────────────────────────────┐
  │ Planner   │ ✓ Created 4 subtasks                            │
  │ Coder     │ ✓ Implemented all subtasks                      │
  │ QA Review │ ✓ 3 passed first time, 1 needed fix             │
  │ QA Fixer  │ ✓ Fixed 1 issue (missing export)                │
  └──────────────────────────────────────────────────────────────┘

Quality Gates:
  ✓ Typecheck passed
  ✓ Lint passed
  ✓ Tests passed (4 new tests)

Commits (in worktree):
  abc1234 feat: ST-001-1 - Create User type definitions
  def5678 feat: ST-001-2 - Create Zod validation schema
  ghi9012 feat: ST-001-3 - Create User service layer
  jkl3456 feat: ST-001-4 - Add unit tests

Memory:
  + 3 new insights saved

Progress: 1/6 stories (17% complete)
Remaining: 5 stories

Worktree Status:
  ✓ 4 commits ahead of main
  ✓ 12 files changed

Next: US-002 - Implement password hashing

When complete, run /ralph-merge to integrate changes.
```

## Escalation Protocol

When QA Fixer fails 3 times:

```
╔════════════════════════════════════════════════════════════════╗
║                 ESCALATION REQUIRED                             ║
╚════════════════════════════════════════════════════════════════╝

Subtask: ST-001-3 - Create User service
Attempts: 3 (max reached)

Unresolved Issue:
  [HIGH] Type mismatch in UserService.create()

  Tried:
    1. Cast to correct type - still fails
    2. Add type assertion - introduces any
    3. Refactor function signature - breaks tests

Recommendation:
  This may require architectural changes.

Options:
  1. Provide guidance to continue
  2. Skip this subtask for now
  3. Abort RALPH run
```

Use AskUserQuestion for human decision.

## Parallel Mode

With `/ralph-run --parallel`:

```
╔════════════════════════════════════════════════════════════════╗
║               RALPH Parallel Mode                               ║
╚════════════════════════════════════════════════════════════════╝

Analyzing subtask dependencies...

Parallel Batch 1 (no dependencies):
  → Spawning agent: ST-001-1
  → Spawning agent: ST-001-2

Waiting for completion...

[████████░░] ST-001-1: Implementing types...
[██████████] ST-001-2: ✓ Complete

Parallel Batch 2 (depends on batch 1):
  → Spawning agent: ST-001-3
  → Spawning agent: ST-001-4
```

## Simple Mode

With `/ralph-run --simple`:

Skip the Planner agent, implement stories directly:

```
╔════════════════════════════════════════════════════════════════╗
║               RALPH Simple Mode                                 ║
╚════════════════════════════════════════════════════════════════╝

Skipping Planner (simple mode)
Implementing US-001 directly...

Pipeline: Coder → QA Reviewer → QA Fixer
```

## Complexity-Based Pipeline Adaptation

RALPH automatically adapts the pipeline based on PRD complexity:

### Auto-Detection

```
╔════════════════════════════════════════════════════════════════╗
║               Complexity Classification                         ║
╚════════════════════════════════════════════════════════════════╝

Analyzing PRD complexity...

Level: STANDARD
Score: 28

Metrics:
  Stories: 6
  Files affected: 12
  Dependencies: 3
  Acceptance criteria: 24

Pipeline configured for STANDARD complexity.
```

### SIMPLE Pipeline (1-2 stories, minimal dependencies)

```
╔════════════════════════════════════════════════════════════════╗
║               SIMPLE Pipeline                                   ║
╚════════════════════════════════════════════════════════════════╝

Complexity: SIMPLE (score < 15)

Pipeline: CODER → LIGHT QA

  - No Planner agent (direct implementation)
  - Light QA validation (essential checks only)
  - No parallel execution
  - No research phase
  - Single iteration per story
```

### STANDARD Pipeline (3-6 stories, moderate complexity)

```
╔════════════════════════════════════════════════════════════════╗
║               STANDARD Pipeline                                 ║
╚════════════════════════════════════════════════════════════════╝

Complexity: STANDARD (score 15-40)

Pipeline: PLANNER → CODER → QA REVIEWER → QA FIXER

  - Full planning phase
  - Standard QA validation
  - Parallel execution enabled
  - Max 3 QA fix attempts
  - Memory logging
```

### COMPLEX Pipeline (7+ stories, architectural changes)

```
╔════════════════════════════════════════════════════════════════╗
║               COMPLEX Pipeline                                  ║
╚════════════════════════════════════════════════════════════════╝

Complexity: COMPLEX (score > 40)

Pipeline: RESEARCH → PLANNER → SELF-CRITIQUE → CODER → EXTENSIVE QA

  - Research phase before planning
  - Extended planning with risk analysis
  - Self-critique validates plan quality
  - Extensive QA with more iterations
  - Max 5 QA fix attempts
  - Mandatory human checkpoints
```

### Override Complexity

Force a specific complexity level:

```bash
/ralph-run --complexity=COMPLEX
/ralph-run --complexity=SIMPLE
```

### Complexity Settings in Config

```yaml
# .ralph/config.yaml
complexity:
  auto_detect: true
  default_level: STANDARD

  simple:
    max_qa_attempts: 2
    use_planner: false
    parallel_enabled: false

  standard:
    max_qa_attempts: 3
    use_planner: true
    parallel_enabled: true

  complex:
    max_qa_attempts: 5
    use_planner: true
    parallel_enabled: true
    research_phase: true
    self_critique: true
    human_checkpoints: true
```

## Error Recovery

| Error | Action |
|-------|--------|
| No PRD found | Direct to `/prd [feature]` |
| No implementation plan | Invoke Planner agent |
| QA fails 3 times | Escalate to human |
| Quality gate fails | QA Fixer attempts fix |
| Agent timeout | Retry or skip subtask |
| Unclear requirements | Use AskUserQuestion |

## Configuration

In `.ralph/config.yaml`:

```yaml
pipeline:
  use_planner: true
  max_qa_attempts: 3
  parallel_enabled: false
  max_parallel_agents: 4

settings:
  compact_after_each_story: true
  compact_threshold: 60
  commit_after_each_subtask: true
```

## Tips

- **Trust the pipeline** - Let each agent do its job
- **QA is mandatory** - Never skip validation
- **Escalate early** - 3 failed attempts = human help needed
- **Log everything** - Memory helps future iterations
- **Parallel when safe** - Only for truly independent work
