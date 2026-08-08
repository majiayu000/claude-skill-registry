---
name: suede-codex-fleet
description: "Claude-directed parallel OpenAI Codex CLI worker fleet for bulk generation. Use when a job is high-volume, well-specified, and splits into independent worker-sized tasks (content batches, test generation, bulk refactors) and Codex CLI is installed and logged in. Claude decomposes, briefs, spawns codex exec runs in parallel, and review-gates every output. Workers are always codex exec processes billed to the user's OpenAI subscription — never substitute Claude subagent fan-out on any model, and halt rather than fall back if Codex CLI is unavailable. NOT FOR: multi-lane Claude agents coordinating one complex change (use suede-agent-teams); low-volume, judgment-dense copy Claude should write itself (use suede-copy or johnny-suede-write)."
---

# Suede Fable Fleet

The Suede Fable Fleet: a high-end Claude model is the admiral — it decomposes, briefs, and reviews — and parallel OpenAI Codex CLI workers are the fleet. The skill id and command stay `suede-codex-fleet` on purpose: GitHub search, skill marketplaces, and MCP catalogs match the terms people actually type — Codex CLI orchestration, codex exec, multi-agent worker fleet — not the brand name. Do not rename the folder or frontmatter `name` to match the brand.

> **"Fable" in the brand name is not the model `claude-fable-5`.** The workers in this fleet are always OpenAI Codex CLI processes. Never read "Fable Fleet" as license to spawn Claude models.

## The workers are Codex processes — never Claude models

**This is the economic point of the skill.** Codex workers bill to the user's OpenAI/ChatGPT subscription. Claude subagents bill to their Anthropic limit. Someone asking for a codex fleet is deliberately routing volume *off* the Anthropic meter — satisfying that request with Claude models inverts the cost model and spends the exact budget they were protecting.

`codex exec` is therefore the only way a worker runs here. Never substitute `Agent`, `Task`, `Workflow`, subagent fan-out, or any other in-house orchestration for a worker — not with `fable`, not with `opus`, not with any model, not "just for this one batch". Claude's role is admiral only: decompose, brief, review, assemble. If you are about to spawn something that is not a `codex exec` process, you have left this skill — stop and re-read the routing table below.

**Preflight failure is a halt, not a fallback.** If Codex CLI is missing, not logged in, or not on `PATH`, say which check failed and ask whether to proceed on Claude models, with a rough estimate of what that fan-out will consume. Never fall back silently.

**What getting this wrong costs** (measured, 2026-07-27): a Claude-model fleet ran in place of an explicitly requested codex fleet — 3,258 turns, ~1.29 billion tokens, 97% of them cache reads from workers each hauling ~500k tokens of context per turn. About $1,843 of API-equivalent spend, 23% of one weekly allocation, for work that should have cost nothing on that account.

## When to use this skill instead of related skills

- **suede-codex-fleet** (this skill): offload high-volume, well-specified generation to Codex CLI workers; Claude plans, briefs, and reviews
- **suede-agent-teams**: multi-lane Claude agents coordinating one complex code change with gates and handoffs
- **suede-copy / johnny-suede-write**: Claude writes the copy itself; right choice when volume is low and judgment density is high

**Core principle:** Claude tokens buy judgment, Codex tokens buy volume. Clear spec + high volume goes to Codex. Fuzzy spec or expensive-if-wrong stays with Claude. Nothing ships unreviewed.

## Preflight (run before first spawn)

1. `which codex && codex --version` — CLI present (validated against codex-cli 0.138.0).
2. `codex login status` — must show logged in (your ChatGPT subscription pays for the run).

   Checks 1 and 2 are the cost boundary. If either fails, **stop and report which one** — do not substitute Claude workers to keep the job moving.
3. Workspace has an `AGENTS.md` at its root. Codex auto-loads it; it carries voice, context, hard bans, and output conventions so briefs stay short. If missing, write it first — that is the highest-leverage file in the system.
4. Workspace has `briefs/` and `out/` directories (create as needed).

## The loop

1. **Decompose.** Split the job into independent worker-sized tasks. Independent means: no worker needs another worker's output.
2. **Brief.** One markdown file per task in `briefs/`. Codex never sees the Claude conversation, so each brief is self-contained: job, inputs (file paths), exact deliverable, acceptance criteria it must self-check, and the exact output path in `out/`.
3. **Spawn.** One `codex exec` per brief, in parallel, in the background:

```bash
caffeinate -i codex exec -C <workspace> --sandbox workspace-write --skip-git-repo-check \
  -o <workspace>/out/<run-name>-final-message.txt \
  "Read AGENTS.md at the workspace root, then execute the brief at briefs/<brief>.md exactly. Write the deliverable to the output file the brief names, run the brief's acceptance-criteria self-check, and state pass/fail per criterion in your final message."
```

   - `-C` sets the worker's root; `--skip-git-repo-check` is required outside git repos.
   - `caffeinate -i` (macOS) is standard on every spawn: it blocks idle sleep for exactly the worker's lifetime and releases on exit, so the machine stays awake while any worker is alive and sleeps normally once the fleet drains. A slept Mac kills every in-flight worker silently. Lid stays open — closed-lid sleep overrides caffeinate unless the Mac is in clamshell mode (external display + power). On non-macOS hosts, drop the prefix.
   - `--sandbox workspace-write` only. Never `danger-full-access`. Workers write files; they do not push, deploy, or touch secrets.
   - Leave the model default unless explicitly asked to override with `-m`.
4. **Review gate (Claude, mandatory).** Read every `out/` file. Check against the brief's acceptance criteria and the AGENTS.md hard bans. Worker self-checks are evidence, not verdicts. If the output fails 0 acceptance criteria but has surface defects (typos, formatting, a wrong label), Claude edits the file directly; do not respawn for a comma.
5. **Delta, don't regenerate.** If the output fails 1-2 acceptance criteria, send a one-line correction: `codex exec resume <session-id> "<delta>"` (session id is printed at run start; `resume --last` is ambiguous with parallel runs). If it fails 3+ criteria or violates an AGENTS.md hard ban, respawn with the delta appended to the brief. Regenerating from scratch wastes the subscription and loses what was right. Correction budget per output: up to three genuinely different fixes — each attempt must change the diagnosis or the strategy, never rerun the last one. Stop early when the same root cause repeats across attempts; report the repeating cause and let the user pick the next move.
6. **Ship.** Claude assembles the reviewed survivors into the final deliverable. Report what was spawned, what passed, what got fixed.

## Brief template

```markdown
# Brief <id> — <task name>

Read `AGENTS.md` in the workspace root first. This brief only adds the task.

## Job
<one paragraph: what and why>

## Inputs
<file paths the worker must read>

## Deliverable
<exact structure, counts, variants, labels>

## Acceptance criteria (self-check before finishing)
<numbered, mechanically checkable: limits, bans, required elements>

## Output
Write to `out/<file>.md`. <structure spec>
```

## Fleet workspaces

Keep a persistent workspace per recurring fleet job (a social-content fleet, a test-generation fleet, a refactor fleet) instead of rebuilding context every run. The workspace root holds the `AGENTS.md` contract, `briefs/`, and `out/`. When a brief produces output that passes review cleanly, keep it — proven briefs are the templates for the next run of the same shape.

## Hard boundaries

- Workers are `codex exec` processes, always. Never substitute Claude-model fan-out (`Agent`, `Task`, `Workflow`, subagents) for a worker, on any model — the brand name "Fable Fleet" is not a reference to `claude-fable-5`.
- Never ship worker output without the Claude review gate.
- Workers never run git push, deploys, or credentialed commands; content and code-edit tasks only, inside the sandbox.
- Secrets never go into briefs or AGENTS.md; workers get file paths, not tokens.
- If a worker's output violates evidence boundaries or hard bans, the fix is Claude's edit or a delta run, never "close enough".

## Troubleshooting

- `codex exec` refuses to start outside a repo: add `--skip-git-repo-check`.
- Every worker died mid-run with truncated or missing output and no error: the machine slept. Spawn with the `caffeinate -i` prefix and keep the lid open (or use clamshell mode).
- Not logged in / usage errors: `codex login status`, then run `codex login` interactively.
- Worker wrote nothing to `out/`: read the `-o` final-message file and the task output log; usually a sandbox denial or a brief pointing at a wrong path.
- Parallel runs are independent processes; spawn each with its own background shell call and collect on completion.

## Routing Reference

- Multi-lane Claude agent coordination with gates and handoffs -> suede-agent-teams
- Low-volume, judgment-dense copy -> suede-copy / johnny-suede-write
- Proving the assembled deliverable meets spec -> private Suede Labs companion,
  not in this pack: `suede-verify`
- Skill authoring or estate-lint questions about this file -> private Suede
  Labs companion, not in this pack: `suede-skill-forge`
