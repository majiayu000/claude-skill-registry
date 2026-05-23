---
name: delaying-tasks
description: >
  Schedule a delayed or interval-based action with minimal heartbeats.
  Use to wait before running a check (e.g., GH Actions, PR status, CI pipeline)
  or to poll on a bounded interval. Trigger on: "wait", "delay", "poll", "check later",
  "retry after", "schedule check".
version: 0.8.0
---

# Delaying Tasks Skill

Use this skill to run a delayed one-shot or bounded polling loop. Use the `/delay` command to invoke this skill.

## Agent Delegation

This skill delegates to specialized agents via the **Task tool**:

| Operation | Agent | Returns |
|-----------|-------|---------|
| One-shot delay | `delay-once` | JSON: success, duration, action |
| Bounded polling | `delay-poll` | JSON: success, attempts, stopped_early, action |

To invoke an agent, use the Task tool with:
- Prompt file: `.claude/agents/<agent-name>.md`
- Parameters as documented in each agent's Inputs section

## Modes
- One-shot delay: `/delay --minutes N [--action "text"]` or `/delay --until HH:MM|ISO [--action "text"]`
- Interval/polling (bounded): `/delay --every 1m --for 10m [--action "text"]` or `/delay --every 1m --attempts 10 [--action "text"]`
- Stop-on-success polling: add `--stop-on-success` with either `--prompt <name>` (uses `.prompts/<name>.md`) or `--prompt-text "..."` (auto-creates `.prompts/delay-success-<ts>.md` wrapping the text). The prompt must return JSON: `{ "Success": true|false|"true"|"false", "Cancelled": true|false|"true"|"false", "Message": "<details>" }`. `Cancelled=true` stops immediately.
- Cancel: not supported; reject requests instead of pretending to cancel.

## Behaviors
- Heartbeat: print a simple “Waiting Xm...” once per minute (or interval) to show liveness; no additional chatter.
- Completion: print the action text on completion so the caller/skill can perform the follow-up check; heartbeats + final Action line only.
- Bounds: require max duration or attempts for polling to avoid runaway loops; enforce a minimum interval (e.g., 1m) to avoid busy waiting.
- Stop-on-success: between checks, sleep via `.claude/scripts/delay-run.sh --every <interval> --attempts 1 --suppress-action`; after each sleep, run the success-check prompt from `.prompts/` and parse JSON Success/Cancelled/Message. Stop early when Success=true or Cancelled=true; otherwise continue until attempts/duration used.
- No network-dependent work is performed by this skill; the action text is just a cue for the caller.

## Agents
- `delay-once`: handles one-shot delays, emits heartbeats, prints action text at end.
- `delay-poll`: handles bounded polling (interval + max duration/attempts), emits heartbeats each interval, stops on success/timeout, prints action text at end.

## Safety
- Reject unbounded polls.
- For short delays (<1m), reduce heartbeat spam (e.g., single “Waiting N seconds…” then completion).
- Return concise outputs only; no tool traces.
