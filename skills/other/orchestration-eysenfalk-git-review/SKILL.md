---
name: orchestration
description: "Teams vs subagents decision framework, resource constraints, enforcement hooks awareness, and orchestrator rules for git-review. Use when coordinating multi-agent work, spawning teams, or managing agent resources."
---

# Orchestration

## Resource Constraints

- **12GB RAM available.** Each teammate (new Claude Code session in tmux) costs ~4GB. Subagents (same session) cost minimal RAM.
- Teammate limit: **3 concurrent teammates** + orchestrator (12GB / 4GB)
- Subagent limit: **5 concurrent subagents** (shared session, much lighter)
- **Prefer subagents** for parallelism — 5 subagents > 3 teammates for the same RAM
- When resuming after a crash, always check for stale teams/worktrees before spawning new agents.
- If a session feels sluggish or memory-constrained, reduce agent count before it becomes an OOM.

## Decision Framework: When to use teams vs subagents

Agent teams are enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`). Use the right tool for the job.

**Default: subagent.** Only escalate to team when peer communication adds value.

### Use a SUBAGENT (Task tool, no team_name) when:

- Single agent, single task, no peer review needed
- Agent reports results back to orchestrator and is done
- Multiple independent tasks in parallel (multiple Task calls)
- Quick fixes, verifications, research, exploration

### Use a TEAM (TeamCreate + team_name) when:

- Agents need to **communicate with each other** (review, feedback, challenges)
- **Tech-lead review cycle**: coder implements → tech-lead reviews → coder fixes → tech-lead re-approves
- **3+ tasks with dependencies** where agents self-claim from shared task list
- **Long-lived agents** that do multiple sequential tasks
- **Competing hypotheses** where agents debate and challenge each other
- User explicitly wants visible tmux panes to observe/interact

## Team Peer Communication (THE WHOLE POINT)

Teams exist so agents can message each other directly. If agents only report to the lead, use subagents instead.

**Required communication patterns when using teams:**
- **Tech-lead + coder**: tech-lead reviews coder's changes via `SendMessage`, sends APPROVED or feedback. Coder fixes issues and notifies tech-lead.
- **Parallel coders on related files**: coordinate interfaces and shared types via `SendMessage`
- **Researcher + implementer**: researcher shares findings directly with coder, not just the lead

**Anti-pattern**: spawning a team where every agent only talks to the lead. That's subagents with extra overhead.

## Team Spawning Workflow

1. `TeamCreate` — create a named team (creates shared task list)
2. `Task` with `team_name` and `name` — spawn teammates into the team
3. Teammates communicate via `SendMessage` (peer-to-peer, not just to lead)
4. `SendMessage` with `type: "shutdown_request"` — gracefully stop teammates
5. `TeamDelete` — clean up team resources (only after all teammates shut down)

## Subagent Spawning Workflow

1. `Task` with `subagent_type` — no team_name, no TeamCreate
2. Agent does its work and returns results
3. No shutdown ceremony needed

## Rules (both modes)

- Use `haiku` model for lightweight/test agents to save tokens
- Each agent gets its own context window; they do NOT inherit conversation history
- Provide full task context in the spawn prompt
- Avoid assigning multiple agents to the same file to prevent conflicts
- **RAM constraints (12GB available):**
  - Teammates: each spawns a NEW Claude Code session (~4GB RAM each) → max **3 teammates** + orchestrator
  - Subagents: share orchestrator's session (minimal RAM) → max **5 subagents** concurrently
  - This is why subagents are the default — you get more parallelism for the same RAM
  - Previous sessions crashed with OOM from excessive teammate spawning

## Enforcement Hooks Awareness

- Enforcement hooks (`enforce-ticket`, `protect-hooks`, `enforce-orchestrator-delegation-v2`) can block Claude's own edits and bash commands. When working on hook-protected paths:
  1. Check which hooks are active in `.claude/settings.json` before editing
  2. If blocked, report back to team lead rather than repeatedly retrying
  3. Never attempt to disable or bypass enforcement hooks

## Intermediate Results (Filesystem Offloading)

- Agent results go to `.claude/results/<agent-name>-<timestamp>.json`
- Clean up after successful commit
- Never pass large diffs through SendMessage — write to file, share path
- Write structured intermediate results to `.claude/scratch/` (gitignored)
- Agents read files selectively rather than passing large payloads in conversation
- When cleaning worktrees (`.trees/<ticket-id>/`), also clean `.claude/results/` and `.claude/scratch/` for that agent
