---
name: coding-agents
description: Spawn and control external coding agents (Claude Code, Codex, OpenCode, Pi) for delegating tasks. Use when (1) user asks to run another coding agent, (2) delegating subtasks to a different AI tool, (3) running multiple agents in parallel on separate issues, (4) spawning an agent in an isolated environment or worktree, (5) user mentions "codex", "opencode", "pi agent", or running "another claude".
---

# Coding Agents

Orchestrate external coding agents programmatically. Use this when you want to delegate tasks to other AI coding tools.

## Prefer interactive mode

Interactive sessions via tmux should be the default for most tasks. Background mode is only appropriate for the simplest tasks that require very few commands or edits (e.g., "count the files in src/", "what version of node is this project using?").

Why interactive is better:
- You can observe progress and catch issues early
- You can respond if the agent asks clarifying questions
- You can interrupt if the agent goes off track
- Agents often need multiple turns to complete real work
- Debugging is much easier when you can see what happened

Use background mode only when:
- The task is trivial (one or two simple commands)
- You are confident the agent will complete without interaction
- You are running many parallel tasks and cannot watch them all

## Interactive mode requires the tmux Skill

For interactive sessions, you MUST use the tmux Skill. The tmux Skill contains:
- "Orchestrating Claude Code sub-agents" recipe - the primary pattern for this use case
- Socket conventions and session management
- Sending input, monitoring output, cleanup

Read and follow the tmux Skill for all interactive agent orchestration.

For parallel work on multiple issues, use the git worktrees Skill to create isolated branches.

## Available agents

Read the relevant reference file for the agent you need right now:

- [references/claude-code.md](references/claude-code.md) - Anthropic's Claude Code CLI
- [references/codex.md](references/codex.md) - OpenAI's Codex CLI
- [references/opencode.md](references/opencode.md) - Open-source coding agent
- [references/pi.md](references/pi.md) - Lightweight multi-provider agent

Each reference includes: invocation, key flags, and completion detection.

## Rules

1. Respect tool choice - if user asks for Codex, use Codex. Do not offer to do the task yourself.
2. Be patient - do not kill sessions because they seem slow. Agents take time.
3. Monitor without interfering - check progress but let the agent work.
4. Use appropriate flags - permission-bypassing flags for unattended/background work only.
5. Isolate work - use worktrees or temp directories to avoid conflicts with your current work.
6. Clean up - kill sessions and remove worktrees when done, unless the user asked you not to.
