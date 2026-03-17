---
name: bmad:sprint
description: Autonomous story execution with Codex validation. Runs create/implement/review cycles per story in a bash loop until done or halted.
argument-hint: "[--epic N] [--story KEY] [--yolo] [--skip-codex] [--resume]"
---

# BMAD Sprint

Run stories autonomously with Codex validation at key boundaries. The loop is bash, state lives in files, Claude gets fresh context per session.

## Usage

```bash
# Run all stories for an epic, AFK mode
/bmad:sprint --epic 1 --yolo

# Run a single story interactively
/bmad:sprint --story 1-1-init-project

# Skip Codex validation (faster, less safe)
/bmad:sprint --epic 1 --skip-codex

# Resume interrupted sprint
/bmad:sprint --resume

# Full run, all epics, overnight
/bmad:sprint --yolo
```

## What It Does

For each story in the queue:

1. **Session 1: Create + Validate** - Creates story from epic, validates quality (max 3 fix cycles)
2. **Codex Boundary 1** - Reviews story spec for completeness
3. **Session 2: Test-Plan + Implement** - ATDD RED phase (failing tests), then GREEN phase (make pass)
4. **Codex Boundary 2** - Reviews code for bugs/security
5. **Session 3: Test-Review + Code-Review** - Quality scoring + senior review
6. **Commit** - Git commit per story

When all stories in an epic complete:
- **Epic Completion**: debt-fixer, test-trace, retrospective, docs-updater

## Halt Conditions

**Always halts (even in yolo):**
- Codex `[HALT]` after max fix rounds
- Unrecoverable errors
- Blocked stories (needs human)
- No signal from Claude

**Mode-dependent:**
- Interactive: pauses between stories for review
- Yolo: auto-continues through everything

## State Tracking

Sprint progress tracked in `_bmad-output/implementation-artifacts/tracking/SPRINT.md`:
- Current story and session
- Story completion status
- Codex validation results
- Checkpoints for resume

Story statuses in `_bmad-output/implementation-artifacts/tracking/sprint-status.yaml`.

## Prerequisite

Before first run, generate sprint-status.yaml:
```
/bmad-bmm-sprint-planning
```

## Execution

This runs in a tmux session so you can detach and reattach.

```bash
ARGS="$ARGUMENTS"
SESSION_NAME="bmad-sprint"

# Find the script (project-local or global)
if [[ -f ".claude/skills/bmad-sprint/scripts/sprint.sh" ]]; then
  SCRIPT=".claude/skills/bmad-sprint/scripts/sprint.sh"
else
  SCRIPT="$HOME/.claude/skills/bmad-sprint/scripts/sprint.sh"
fi

# Kill existing session if running, create new one
tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true
tmux new-session -d -s "$SESSION_NAME" -c "$(pwd)"

# Run the sprint script in the tmux session
tmux send-keys -t "$SESSION_NAME" "bash $SCRIPT $ARGS" Enter

# Tell user how to attach
echo ""
echo "================================================================"
echo "BMAD Sprint started in tmux session: $SESSION_NAME"
echo "================================================================"
echo ""
echo "To attach and watch progress:"
echo "  tmux attach -t $SESSION_NAME"
echo ""
echo "To detach (while attached):"
echo "  Ctrl+b then d"
echo ""
echo "To check if still running:"
echo "  tmux has-session -t $SESSION_NAME 2>/dev/null && echo 'Running' || echo 'Finished'"
echo ""
```
