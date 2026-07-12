---
name: advisor
description: Consult an independent GPT-5.6 reviewer (Terra by default; Sol on request, for a stronger but costlier review), matched to your current reasoning-effort level. Use before committing to an interpretation or a substantial piece of writing/analysis, when stuck (recurring errors, a non-converging approach, results that do not fit), when considering a change of approach, or when you believe a task is complete and want a check before finalizing. Not a co-implementer — read-only advisory only, does not edit files.
---

# Advisor (GPT-5.6 consulted)

Consult an independent **GPT-5.6** reviewer for one specific decision point, at the same reasoning effort you are currently running at. This is the Codex-side counterpart of the Claude-side `advisor` skill (`plugin/skills/advisor/` in `open-science-skills`), built the same session for the same reason: a single-turn advisory consult, not a delegated implementation.

**Which 5.6 tier, and why it matters.** There are three distinct GPT-5.6 tiers, not one model: `gpt-5.6-sol` (flagship, "most capable"), `gpt-5.6-terra` (balanced, "everyday work"), `gpt-5.6-luna` (fast/cheap). This skill defaults to **`gpt-5.6-terra`** for routine consults — it is cheaper and confirmed reliable. `gpt-5.6-sol` is confirmed working on both hosts this repo runs on (July 2026, both authenticated via ChatGPT login) — an earlier "rejected outright under ChatGPT-account auth" finding no longer reproduces; whether that was a temporary rollout gate or a stale/outdated-CLI artifact is unclear, so re-verify with a smoke test if `sol` ever errors on your account rather than assuming it's gated. Pass `--model gpt-5.6-sol` explicitly for a stronger, costlier consult — see *Effort calibration* below.

Read [`scripts/sol-advisor.sh`](scripts/sol-advisor.sh) before the first run — the flags and the effort-handling note there are load-bearing.

## Sandbox constraint — read this before your first run

`sol-advisor.sh` shells out to a nested `codex exec` process. Confirmed by direct reproduction (July 2026, both hosts this repo runs on): a `codex exec` process running under **any** sandbox mode (`read-only` or `workspace-write`) cannot spawn a working nested `codex exec` child — it fails immediately with `Error: failed to initialize in-process app-server client: Operation not permitted` (macOS) or `Read-only file system` (Linux). This is structural — the OS sandbox applies transitively to the whole process tree — and is **not** fixed by passing `--dangerously-bypass-approvals-and-sandbox` to the nested call itself; only an unsandboxed top-level session avoids it entirely.

- If you are interactive (not `codex exec` invoked non-interactively) and this failure surfaces, request escalation for that one shell command (`sandbox_permissions: require_escalated`, with a short justification) so it runs outside the sandbox — this is exactly the case the built-in escalation path exists for.
- If you are running non-interactively (`codex exec` at the top level shows `approval: never` in its own banner — no human is available to approve an escalation), this call cannot succeed. Report the failure honestly; do not silently produce the review yourself in place of the consult (that defeats the point of an independent second opinion) and do not retry indefinitely.

## When to use

- **Before substantive work** — before writing, before committing to an interpretation, before building on an assumption. Orientation (finding files, reading a source) is not substantive; writing, editing, and declaring an answer are.
- **When you believe a task is complete.** Make the deliverable durable first (write the file, save the result, commit the change) — the consult takes real time.
- **When stuck** — errors recurring, an approach not converging, results that do not fit.
- **When considering a change of approach.**

On tasks longer than a few steps, consult at least once before committing to an approach and once before declaring done. Give the advice serious weight: if a step you followed on the consult's advice fails empirically, or you have primary-source evidence contradicting a specific claim, adapt. If your own evidence and the consult's advice point different directions, surface the conflict in one more consult rather than silently picking a side.

## Effort calibration — read this before running

The consulted model should run at the **same reasoning effort you are currently running at**, not a hardcoded default. Codex does not expose its own live reasoning-effort setting as an environment variable inheritable by subprocesses (confirmed empirically: dumping `env` inside a running `codex exec` call shows no `CODEX_REASONING_EFFORT` or equivalent — only Claude Code's own `$CLAUDE_EFFORT` leaked through from an enclosing Claude Code process, which is not your effort level when you are the one running as Codex).

What Codex *does* expose: the "reasoning effort: `<level>`" line shown in your own session banner at startup, visible in your own context. Before running the consult, **read that value from your own session context** and pass it explicitly:

```bash
scripts/sol-advisor.sh --prompt-file <briefing-path> --out <output-path> -C "$PWD" --effort <your-own-level>
```

Do not omit `--effort` and let it silently default to the script's fallback (`high`) unless `high` genuinely is your own current level — the fallback exists so the script never errors on a missing flag, not as a substitute for checking your own level.

## Steps

1. **Compose the briefing.** A self-contained document: the task, what you have done so far (key steps, findings, decisions), your current approach or the specific claim to check, and the precise question. Concrete — file paths, line numbers, the actual claim. Save to a scratch file. The consulted model has no access to your conversation beyond this file.

2. **If declaring a task complete, make the deliverable durable first.**

3. **Read your own current reasoning-effort level from your session context**, then run:

   ```bash
   scripts/sol-advisor.sh --prompt-file <briefing-path> --out <output-path> -C "$PWD" --effort <your-level>
   ```

4. **Read the output file** and weigh the advice. Integrate it; if you diverge from it, be able to say why.

## Notes

- `scripts/sol-advisor.sh --check` verifies the `codex` CLI is on PATH.
- The spawned session runs `--sandbox read-only` and `--ephemeral` — advisory only, no edits, not saved as a resumable session.
- **Default model is `gpt-5.6-terra`, not `gpt-5.6-sol`** — cost, not reliability. There are three distinct GPT-5.6 tiers (`sol` flagship / `terra` balanced / `luna` fast) — not one model with a shorthand. An earlier finding claimed `gpt-5.6-sol` was rejected outright on a Codex CLI authenticated via `codex login` with a ChatGPT account (as opposed to an API key) — `"The 'gpt-5.6' model is not supported when using Codex with a ChatGPT account."` This has since been re-tested (July 2026) and no longer reproduces: `sol` now works on hosts authenticated the identical way (`codex login status` → `Logged in using ChatGPT`). Whether the original block was a temporary rollout gate or an artifact of an outdated CLI on that host is unclear — if `sol` ever errors on your account, check `codex --version` first (an outdated CLI rejects even `terra`/`luna` with a *different*, version-specific error) before concluding it's an account gate. Pass `--model gpt-5.6-sol` explicitly for a stronger reviewer at higher cost. If the model you asked for is unreachable for any reason, report it and ask whether to stop or use a named replacement — do not silently fall back further (e.g. to `gpt-5.5`) for what is supposed to be a genuinely independent second opinion (a reviewer identical to the executor defeats the point of this specific skill; if a same-model consult is actually fine for the task at hand, the calling agent should use its own judgment directly rather than spend a consult on it).
- Effort enum: `none, minimal, low, medium, high, xhigh` (Codex's scale — no `max`; Claude Code's `max` has no Codex equivalent).
- Companion skill: `plugin/skills/advisor/` (Claude-side) — same pattern, consulting Fable 5, effort read from `$CLAUDE_EFFORT` instead of the session banner.
