---
name: ralph
description: Execute iterative development loop through user stories. Implements one story at a time with quality gates, commits, and learning persistence. Ships features autonomously.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task, AskUserQuestion, Skill
user_invocable: true
argument-hint: <requirements> [--branch NAME] [--max-stories N] [--max-iterations N]
---

# Ralph: Autonomous AI Development Loop

Execute the complete Ralph workflow: generate a PRD with user stories, then autonomously implement them one at a time with quality gates, commits, and learning persistence.

## Invocation

```bash
/ralph <requirements> [options]
```

**Arguments:**
- `<requirements>` - Feature description (inline text, file path, or URL)
- `--branch NAME` - Branch name (default: auto-generated with `ralph/` prefix)
- `--max-stories N` - Maximum stories to generate (default: 10)
- `--max-iterations N` - Maximum iterations to run (default: from prd.json or 10)

**Examples:**
```bash
/ralph "Build a user authentication system with login and registration"
/ralph ./requirements.md --branch ralph/auth-system
/ralph "Add dark mode toggle" --max-stories 5 --max-iterations 10
```

## Execution Flow

This skill orchestrates two phases sequentially:

### Phase 1: Planning (via /ralph-plan)

1. **Gather Requirements** - Parse input (file, URL, or inline text)
2. **Analyze Codebase** - Understand existing patterns and structure
3. **Ask Clarifying Questions** - 3-5 questions to refine scope
4. **Generate PRD** - Create atomic, testable user stories
5. **Initialize Tracking** - Create `.ralph/prd.json` and `.ralph/progress.txt`
6. **Create Branch** - Set up feature branch

### Phase 2: Execution (via /ralph-execute)

1. **Load Context** - Read PRD, progress, and AGENTS.md
2. **Select Story** - Pick highest-priority pending story
3. **Implement** - Code the story following existing patterns
4. **Quality Gates** - Run typecheck, lint, test, build
5. **Commit** - Git commit on success
6. **Learn** - Update progress.txt with learnings
7. **Loop** - Continue until all stories complete or blocked

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                        /ralph                                │
│                                                              │
│  ┌──────────────┐          ┌──────────────────────────────┐ │
│  │  /ralph-plan │ ───────▶ │       /ralph-execute         │ │
│  │              │          │                              │ │
│  │ • Questions  │          │ ┌──────────────────────────┐ │ │
│  │ • PRD gen    │          │ │ Story 1 → Gates → Commit │ │ │
│  │ • Branch     │          │ │ Story 2 → Gates → Commit │ │ │
│  └──────────────┘          │ │ Story 3 → Gates → Commit │ │ │
│                            │ │ ...                      │ │ │
│                            │ └──────────────────────────┘ │ │
│                            └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Steps

### Step 1: Invoke /ralph-plan

First, use the Skill tool to invoke `/ralph-plan` with the user's requirements:

```
Skill: ralph-plan
Args: <requirements> [--branch NAME] [--max-stories N]
```

This will:
- Ask clarifying questions
- Generate `.ralph/prd.json` with user stories
- Initialize `.ralph/progress.txt`
- Create/switch to feature branch

**Wait for planning to complete before proceeding.**

### Step 2: Confirm with User

After planning completes, present the summary:

```
RALPH PLANNING COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━

Project: [Name]
Branch: [branch-name]
Stories: [N] user stories

Ready to begin autonomous implementation.

Proceed with /ralph-execute?
```

Use AskUserQuestion with options:
- **Yes, start execution** - Continue to Phase 2
- **Review PRD first** - Show story details
- **Stop here** - Exit without executing

### Step 3: Invoke /ralph-execute

If user confirms, use the Skill tool to invoke `/ralph-execute`:

```
Skill: ralph-execute
Args: [--max-iterations N]
```

This will autonomously:
- Implement stories one at a time
- Run quality gates
- Commit on success
- Log learnings
- Continue until done

### Step 4: Report Completion

After execution completes, summarize:

```
RALPH COMPLETE
━━━━━━━━━━━━━━

All [N] stories processed!

Summary:
- Stories Passed: [N]
- Stories Blocked: [N]
- Total Commits: [N]

Branch: [branch-name]
Ready for review and merge.

Next Steps:
1. Review: git log --oneline -n [N]
2. Push: git push -u origin [branch-name]
3. PR: gh pr create
```

## Error Handling

| Phase | Error | Action |
|-------|-------|--------|
| Planning | Invalid requirements | Ask user to clarify |
| Planning | Branch exists | Offer to reuse or rename |
| Execution | No PRD found | Error - planning didn't complete |
| Execution | Story blocked | Log and continue to next |
| Execution | Max iterations | Report and exit gracefully |

## When to Use /ralph vs Individual Skills

| Use Case | Skill |
|----------|-------|
| Full feature from scratch | `/ralph` |
| Re-run planning with changes | `/ralph-plan` |
| Resume existing PRD | `/ralph-execute` |
| Quick preview | `/ralph-execute --dry-run` |

## Output Files

After successful execution:
1. `.ralph/prd.json` - PRD with story status
2. `.ralph/progress.txt` - Learnings and history
3. `AGENTS.md` - Updated with reusable patterns
4. Git commits for each completed story

## Credits

Original Ralph by @GeoffreyHuntley
