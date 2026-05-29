---
name: loom-manager-workflow
description: Manage Loom team tickets as a team manager with limited permissions (no git merge/push, no loom team commands). Handle ticket lifecycle: create, update, add notes, track dependencies, identify blockages.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-29T10:20:56.340Z"
  updated_at: "2026-01-29T10:20:56.340Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Manage Loom team tickets as a team manager when you cannot use `loom team` commands or git merge/push operations.

# When To Use
- You are a team manager for a Loom team
- You need to create tickets, update status, add notes
- You cannot execute merges or push code directly
- Workers are doing implementation in worktrees

# Constraints
- Do NOT use `loom team *` commands
- Do NOT use `git merge*` or `git push*` commands
- Only use `loom ticket` commands for ticket management
- Use git read commands: `git status`, `git log`, `git diff`, `git show`, `git branch`

# Core Workflow

## 1. Create Tickets
- Use `loom ticket create --priority <1|2> --type <feature|task|example> --tag <phase,tags>`
- Tickets created without title/description need notes added immediately
- Add note with: tasks, dependencies, acceptance criteria, examples

## 2. Update Ticket Status
- `loom ticket start <id>` - move to in_progress
- `loom ticket close <id>` - move to closed
- Note: no "ready" or "blocked" commands exist via CLI, use notes instead

## 3. Add Notes
- `loom ticket add-note <id> "Your note here"`
- Use notes for: detailed requirements, dependency tracking, urgent requests, review feedback

## 4. Track Dependencies
- Add notes starting with "DEPENDENCIES:" or "BLOCKED:"
- List ticket IDs and explain relationship
- Example: "DEPENDENCIES: Depends on vp-045b (API Clients) being merged first"

## 5. Identify Blockages
- Check implementation complete (git log shows feature commits)
- If complete but in_progress: add URGENT note requesting merge
- Include: commit hash, branch name, merge target

## 6. List and Review
- `loom ticket list` - see all tickets
- `loom ticket show <id>` - see full details including notes
- Use `--status` filter if available

# Best Practices
- Add dependency notes to both parent and child tickets
- Use phase tags (phase1, phase2, phase3) for organization
- When creating multiple related tickets, create them all then add notes
- Inspect branches before declaring ready (git log, git diff)
- Clear priority guidance: P1 features must complete before P2

# Worker Communication
- Workers update tickets via `loom ticket add-note`
- Workers should set status to in_progress when starting
- Workers should request review before considering complete
- Workers can escalate via notes when blocked

# Verification
- Run `loom ticket list` to check overall state
- Use `git branch -a` to see all feature branches
- Check `loom ticket show <id>` for full context
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
