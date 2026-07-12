---
name: advisor
description: Consult Fable 5 as an independent, stronger second reviewer, matched to your current reasoning-effort level. Use before committing to an interpretation or a substantial piece of writing/analysis, when stuck (recurring errors, a non-converging approach, results that do not fit), when considering a change of approach, or when you believe a task is complete and want a check before finalizing. Fallback for when the native advisor tool is unavailable ("The advisor tool is unavailable"). Not a co-implementer — read-only advisory only, does not edit files.
allowed-tools:
  - Read
  - Write
  - Bash
---

# advisor — Fable 5, as a second reviewer

The native `advisor()` tool sometimes reports itself unavailable ("The advisor tool is unavailable. Do not try to use it again.") mid-session. This skill is the fallback: it spawns an independent, isolated Fable 5 session as a stronger reviewer, matched to whatever reasoning-effort level the calling session is currently running at.

## What this is not

The native tool automatically forwards your entire conversation transcript — no composition required. This skill cannot do that: `fable-advisor.sh` spawns a brand-new `claude` process with no memory of this conversation. **You must compose a self-contained briefing** (see Steps) before invoking it. This is the one real difference from the native tool; the rest of the behavior (independent judgment, read-only, called before substantive work or when stuck) is designed to match it.

## When to use

Same triggers as the native advisor, restated because they are easy to skip under time pressure:

- **Before substantive work** — before writing, before committing to an interpretation, before building on an assumption. Orientation (finding files, reading a source) is not substantive; writing, editing, and declaring an answer are.
- **When you believe a task is complete.** Make the deliverable durable first (write the file, save the result, commit the change) — the consult takes real time, and a durable result survives if the session ends mid-consult; an unwritten one does not.
- **When stuck** — errors recurring, an approach not converging, results that do not fit.
- **When considering a change of approach.**

On tasks longer than a few steps, consult at least once before committing to an approach and once before declaring done. On short reactive tasks where the next action is dictated by tool output you just read, one consult (or none) is enough — the value is highest before the approach crystallizes.

Give the advice serious weight. If a step you followed on Fable's advice fails empirically, or you have primary-source evidence contradicting a specific claim, adapt — don't let a passing self-test overrule advice that was checking something the test doesn't cover. If your own evidence points one way and Fable points another, do not silently pick a side: one more consult with the conflict stated plainly ("I found X, you suggest Y, which constraint breaks the tie?") is cheap insurance against committing to the wrong branch.

## Effort calibration

Fable runs at the **same reasoning-effort level as the calling session**, not a hardcoded default. This is load-bearing: a cheap consult under a `max`-effort task wastes the point of asking, and a maximal consult under a `low`-effort quick task wastes time and money for no benefit.

Mechanism (verified empirically this session, not assumed from documentation): Claude Code exposes the current session's effort level as the environment variable `$CLAUDE_EFFORT` (confirmed present via `env`, and confirmed to propagate into spawned subprocesses). `fable-advisor.sh` defaults `--effort` to `$CLAUDE_EFFORT` automatically — you do not need to pass it explicitly unless you want to deliberately override (e.g., a cheaper `medium`-effort consult mid-task even though the session itself is at `max`).

## Steps

1. **Compose the briefing.** Write a self-contained document covering: the task (what you were asked to do and why), what you have done so far (key steps, findings, decisions already made), your current approach or the specific claim you want checked, and the precise question for Fable. Be concrete — file paths, line numbers, the actual claim, not a vague "does this look right?" Save it to a scratch file.

2. **If declaring a task complete, make the deliverable durable first** (write/save/commit) — before running step 3, per the triggers above.

3. **Run the consult** (Bash tool, `timeout: 900000` as a backstop — the script has its own internal timeout too):

   ```bash
   ~/.claude/skills/advisor/scripts/fable-advisor.sh \
     --prompt-file <briefing-path> \
     --out <output-path> \
     -C "$PWD"
   ```

   Omit `--effort` to inherit `$CLAUDE_EFFORT` automatically. Pass `--effort <level>` explicitly only to deliberately override.

4. **Read the output file** and weigh the advice per the guidance above. Do not just append it verbatim to your response — integrate it, and if you diverge from it, be able to say why.

## Arguments

- No arguments — this skill's job is triggered by the situations above, not by a payload. Compose the briefing per Steps.

## Notes

- `~/.claude/skills/advisor/scripts/fable-advisor.sh --check` verifies the `claude` CLI is on PATH and reports the live `$CLAUDE_EFFORT` value — run once after install, or when a consult behaves unexpectedly.
- The spawned Fable session runs `--permission-mode plan` (no file edits) and `--no-session-persistence` (not saved as a resumable session) — advisory only, by design, matching the native tool's own scope.
- Default model is `fable` (the latest Fable alias). Override with `--model <id>` if a specific pinned version is ever needed.
- Effort enum: `low, medium, high, xhigh, max` — matches `/effort` in Claude Code. If `$CLAUDE_EFFORT` is unset for some reason, the script falls back to `high` rather than guessing low or silently failing.
- Companion skill: `codex/advisor/` — the same pattern for a Codex-native session (GPT-5.5/5.6 executor consulting GPT-5.6 "Sol"). Effort detection works differently there since Codex does not expose an inheritable effort env var; see that skill's own notes.
- If `claude` reports the `fable` alias unavailable, report it and ask whether to stop or use a named replacement — do not silently fall back to a different model family for what is supposed to be an independent second opinion.
