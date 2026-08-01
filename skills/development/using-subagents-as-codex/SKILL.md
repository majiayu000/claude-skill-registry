---
name: using-subagents-as-codex
description: Use when Codex would benefit from a background subagent so the primary
  session stays lean—this skill walks through codex-subagent start/send/peek/log/watch
  usage, controller ID tagging, and disk-based
---

name: using-subagents-as-codex
description: Use when Codex would benefit from a background subagent so the primary session stays lean—this skill walks through codex-subagent start/send/peek/log/watch usage, controller ID tagging, and disk-based prompt/result handling for reliable async work.

# Using Subagents as Codex

## Overview

`codex-subagent` is the standard way to launch Codex-controlled helpers whose prompts/results live on disk (`.codex-subagent`). This skill explains when to spin up a subagent, how to run `start`/`send/peek/log/watch`, and how controller IDs keep multiple Codex terminals from colliding.

## When to Use

Use this skill any time the main Codex session might benefit from parallel or long-running work: research threads, context-heavy builds, or anything that would otherwise bloat the active chat. Install the CLI into this folder (`npm install --prefix ~/.codex/skills/using-subagents-as-codex --production .`) and call it via `~/.codex/skills/using-subagents-as-codex/codex-subagent …` so the path works regardless of your current repository. The installer creates a tiny wrapper script named `codex-subagent` that `import()`s the real CLI from `node_modules/codex-subagent-cli/dist/codex-subagent.js`; keep it executable, and rerun the install command if it ever disappears. The CLI auto-detects the controlling Codex PID, so mistagging is rare—but the instructions below ensure you never forget prompts, policies, or result capture.

### Symptoms / Triggers

| Situation                                                 | Why this skill helps                                                                                 |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Need background research while main session keeps context | `start`/`send` run subagents fully outside your chat.                                                |
| Lots of copy/paste between prompts                        | Prompt files keep history reproducible.                                                              |
| Hard to remember what a subagent already answered         | `peek`/`log` read NDJSON logs safely.                                                                |
| Multiple Codex tabs open                                  | Controller IDs keep each set of threads isolated (use `--controller-id` when intentionally sharing). |

### Best Practices

- **Always encode the workspace path in the prompt file.** Start each prompt with something like “Work inside `/Users/jesse/.../repo`; run all commands there” so the helper doesn’t guess (or touch the wrong repo).
- **Default to `peek`.** Use `peek` for “what’s new?” checks and reserve `watch --duration-ms …` for short-lived polls. It keeps the main session quiet and avoids giant NDJSON dumps.
- **Detach unless you absolutely need streaming.** `start`/`send` default to background mode so you can keep working; add `--wait` only when you need live streaming.
- **Batch launches via manifests.** `start --manifest tasks.json` (or `--manifest-stdin`) lets you describe several prompts/personas in one JSON file so you don’t litter the repo with throwaway prompt files. Pair manifest labels with `wait --labels …` to block on the entire batch completing.
- **Watch the “Launch diagnostics” section.** After every detached `start`/`send`, run `codex-subagent list`. If the diagnostics section shows `NOT RUNNING` or “still waiting for Codex,” read the referenced `.codex-subagent/state/launch-errors/<id>.log`, fix the root cause (missing profile, sandbox refusal, bad cwd), and relaunch before assuming the helper is working.

## Workflow (Do This Every Time)

1. **Prep prompt**: Write the request to a prompt file (`task.txt`, `followup.txt`) or a JSON blob consumed via `--json`. JSON keeps throwaway prompts self-contained (`{"prompt":"…","cwd":"…","label":"…"}`) while files remain better for versioned work. **Always include the repo/workdir instructions** so the helper never guesses.
2. **Launch**: `~/.codex/skills/using-subagents-as-codex/codex-subagent start --role <role> --policy workspace-write --prompt-file task.txt [--output-last last.txt] [--controller-id my-session] [--wait]`. Detached mode is the default—Codex keeps running for minutes/hours while the CLI returns immediately. Add `--wait` only when you need to sit in the session until Codex finishes. When launching a batch, pass `--manifest tasks.json` instead of `--prompt-file` so each entry can specify its own prompt/label/persona (detached by default, per-entry `wait: true` will block inline). Swap in `--json prompt.json`/`--json -` when you want inline prompts, and lean on `--print-prompt`/`--dry-run` to inspect or skip execution before Codex runs. **Immediately run `codex-subagent list`**; if the `Launch diagnostics` section shows `NOT RUNNING` or “still waiting for Codex,” open the referenced `.codex-subagent/state/launch-errors/<launch-id>.log`, fix the issue, and relaunch before moving on.
3. **Inspect**: Use `peek --thread <id> [--output-last last.txt]` to fetch the newest unseen assistant message without resuming; it updates `last_pulled_id` so repeated peeks are quiet when nothing changed. This is your default “what happened?” command—reach for `watch` only when you really need repeated polling.
4. **Resume**: When you have follow-up instructions, `send --thread <id> --prompt-file followup.txt [--cwd /repo/path] [--wait]`. Policy/role come from the registry; you only supply the new prompt (file or `--json followup.json`), and `--wait` is optional when you want to block until the resumed turn completes (otherwise it detaches like `start`). `--print-prompt`/`--dry-run` work here too when you need to inspect the composed text.
5. **Request code review**: When dispatching review subagents, explicitly say “Use the template from requesting-code-review/code-reviewer.md; the code-reviewer skill isn’t installed here.” That keeps reviewers from trying `use-skill code-reviewer` and ensures they follow the right template.
6. **Review history**: `log --thread <id> [--tail 20] [--raw]` prints NDJSON history; grep/pipe as needed. Add `--verbose` when you want the “last activity …” summary even if nothing new printed.
7. **Watch if needed**: For “any updates yet?” loops, run `watch --thread <id> [--interval-ms 5000] [--duration-ms 60000] [--controller-id ...]`. It repeatedly runs `peek`; stop with Ctrl+C or let `--duration-ms` stop it automatically during demos.
8. **Wait for batches**: When you’ve launched several detached helpers (especially via `--manifest`), run `wait --threads id1,id2` or `wait --labels "Task 1","Task 2"` so the CLI blocks until each thread reaches a terminal state. Add `--follow-last` to print the final assistant reply per thread, and `--timeout-ms` to bail out if they stall. This keeps you from spam-checking `peek` in a loop.
9. **Record outcomes**: After each peek/log/watch, paste the relevant sentence back into your main Codex convo so teammates know the status.
10. **Demo sanity check**: On new machines, run `npm run demo` once to ensure `start` + `watch` wiring works locally.

## Quick Reference

| Command   | Required                                                                  | Optional                                                                                                                                       | Notes                                                                                                                                                                                |
| --------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `start`   | `--role`, `--policy`, `--prompt-file` **or** `--json` **or** `--manifest` | `--output-last`, `--controller-id`, `--root`, `--cwd`, `--label`, `--persona`, per-manifest `wait`/`outputLast`, `--print-prompt`, `--dry-run` | Launches new thread(s); refuses “allow everything”. `--manifest` lets you describe many prompts at once, each with its own label/persona/`wait`.                                     |
| `send`    | `--thread`, `--prompt-file` **or** `--json`                               | `--output-last`, `--controller-id`, `--wait`, `--cwd`, `--persona`, `--print-prompt`, `--dry-run`                                              | Resumes existing thread; detached by default, add `--wait` to block. Missing `--persona` means “reuse whatever the thread already had.”                                              |
| `peek`    | `--thread`                                                                | `--output-last`, `--controller-id`, `--verbose`                                                                                                | Reads newest unseen assistant message only.                                                                                                                                          |
| `log`     | `--thread`                                                                | `--tail <n>`, `--raw`, `--controller-id`, `--verbose`                                                                                          | Reads stored NDJSON history, optionally appending “last activity …”.                                                                                                                 |
| `status`  | `--thread`                                                                | `--tail`, `--raw`, `--stale-minutes`                                                                                                           | One-shot summary (latest turn, idle duration, follow-up suggestion).                                                                                                                 |
| `watch`   | `--thread`                                                                | `--interval-ms`, `--output-last`, `--duration-ms`, `--controller-id`                                                                           | Loops `peek` until stopped (or until `--duration-ms` elapses).                                                                                                                       |
| `wait`    | selection (`--threads`, `--labels`, or `--all-controller`)                | `--interval-ms`, `--timeout-ms`, `--follow-last`, `--controller-id`                                                                            | Polls the registry/logs until every selected thread stops. Perfect for `--manifest` batches; `--follow-last` prints their final assistant replies.                                   |
| `label`   | `--thread`, `--label`                                                     | `--controller-id`                                                                                                                              | Attaches/updates a friendly label (empty string clears it).                                                                                                                          |
| `archive` | _(none)_                                                                  | `--thread`, `--completed`, `--yes`, `--dry-run`, `--controller-id`                                                                             | Moves completed threads + logs under `.codex-subagent/archive/…`.                                                                                                                    |
| `list`    | _(none)_                                                                  | `--controller-id`, `--root`                                                                                                                    | Shows threads owned by current controller (running threads first) **and** a `Launch diagnostics` section for pending/failed detached launches (includes error messages + log paths). |

## Common Mistakes + Fixes

| Mistake                                         | Fix                                                                                               |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Forgetting to write prompt to disk              | Create `task.txt` _first_, then run CLI; version control it if helpful.                           |
| Expecting `peek` to resume Codex                | `peek`/`log` are read-only; run `send` for actual execution.                                      |
| Multiple Codex terminals stepping on each other | Use distinct `--controller-id` values when you intentionally want to separate/merge thread pools. |
| Leaving `watch` running                         | Use `Ctrl+C`, `--duration-ms`, or wrap `timeout 30 node ... watch ...` during tests.              |
| Committing `.codex-subagent`                    | Leave it ignored unless sharing sample logs on purpose.                                           |

## Verification Snapshot

Baseline testing showed agents launching subagents inline (prompt strings) and forgetting which session owned the thread, causing `thread belongs to a different controller` errors. Following the workflow above (prompt file + controller tagging + peek/log usage) kept state consistent and prevented accidental cross-session access.

## Checklist

- [ ] Prompt written to disk before CLI call.
- [ ] `start` executed with correct role/policy and (if needed) `--controller-id` / `--persona`.
- [ ] `send` only after `peek/log/status` confirms prior output.
- [ ] `peek`/`log` (or `status`) run before summarizing results back to main chat.
- [ ] `watch` stopped with Ctrl+C, `--duration-ms`, or timeout.
- [ ] Completed threads archived (or intentionally retained) so the registry stays lean.
- [ ] `.codex-subagent` left untracked unless intentionally shared.
