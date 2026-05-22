---
name: dev
description: Orchestrate TDD-based development workflow – plan with test-first approach, save to Obsidian vault, split into trackable steps, and execute sequentially with status tracking. Acts as project manager, delegating tasks to specialized agents.
allowed-tools: Bash(tmux:*)
---

# Dev orchestrator

要件と簡単な仕様を元にTDDベースの計画を作成し、各stepに分割する。stepごとに実行し、完全な実装を目指す。

## Requirements

- Follow user's instructions ($ARGUMENTS)
- Your main role is the project manager so assign tasks to other agents as far as possible

## Procedure

0. **Setup**: Initialize workflow state
   - Derive `{branch_name}` from current git branch (same rule as plan-on-md: `feature/#468` → `468`)
   - Create `docs/{branch_name}/dev-workflow.yaml`:
     ```yaml
     save:
       status: Ready
     split:
       status: Pending
     execute:
       status: Pending
     ```
   - This MUST be done BEFORE entering plan mode

1. **Plan (execute yourself)**: Create TDD implementation plan using EnterPlanMode
   - Follow the TDD structure defined in [tdd-plan.md](steps/tdd-plan.md) — Red → Green → Refactor order
   - Get user approval via ExitPlanMode

2. **Save**: Store the approved plan in Obsidian vault
   - Update YAML: `save: In progress`
   - Use `tmux list-panes` to find an available shell pane
   - Send: `tmux send-keys -t <pane> 'claude "/plan-on-md"' Enter`
   - Tell the user: "plan-on-md を別ペインに委譲しました。完了したら教えてください"
   - User confirms completion → Update YAML: `save: Done`, `split: In progress`

3. **Split**: Break the plan into individual step files
   - Send: `tmux send-keys -t <pane> 'claude "/plan-steps-split"' Enter`
   - Tell the user: "plan-steps-split を別ペインに委譲しました。完了したら教えてください"
   - User confirms completion → Update YAML: `split: Done`, `execute: In progress`

4. **Execute**: Run steps sequentially
   - Send: `tmux send-keys -t <pane> 'claude "/proceed-by-step"' Enter`
   - Tell the user: "proceed-by-step を別ペインに委譲しました。完了したら教えてください"
   - User confirms completion → Update YAML: `execute: Done`

## IMPORTANT: Workflow State

A PreToolUse hook reads `docs/{branch_name}/dev-workflow.yaml` and injects the current workflow phase.
The hook finds the first phase with `status: Ready` and directs you to execute that phase.
After plan approval, your NEXT action is determined by the YAML status, not by implementing code directly.
Status values follow [status.md](rules/status.md): Ready / In progress / In review / Pending / Done
