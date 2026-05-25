---
name: start
description: One command from "plugin installed" to "running brief on your idea." Combines /mycelium:setup (project-state initialization) and /mycelium:interview (10-minute discovery brief) into a single flow. Run this immediately after installing the Mycelium plugin — it's the recommended entry point for first-time users.
---

# /mycelium:start — combined first-time entry

When this skill runs, follow the flow below. The skill is designed so a first-time user goes from "plugin installed" to "holding a one-page brief on their idea" in a single invocation.

## Step 1: Welcome (~30 seconds of context, then move on)

Output a short welcome before doing anything. Do NOT skip this — the install-to-here gap is the friction point this skill exists to address. The user just installed a 45-skill framework and has no context yet.

> "Welcome to Mycelium.
>
> Mycelium is a discovery-and-discipline harness for AI agents — it forces the agent to think before it codes. 30+ product-thinking frameworks (JTBD, OST, Wardley, Cagan four risks, Cynefin, BVSSH...) connected by evidence gates, so critical steps cannot be skipped.
>
> What I'm about to do, in two steps:
>   1. Set up project-state directories in your `.claude/` (canvas, diamonds, memory). ~10 seconds.
>   2. Run a 10-minute discovery brief: 4 questions about your idea, then a one-page brief covering who it's for, the biggest assumption, the biggest risk, and your next concrete move.
>
> Your project root files (CLAUDE.md, README.md, LICENSE, etc.) are NOT touched — Mycelium ships as a Claude Code plugin and lives in plugin cache. Only your `.claude/` directory is created.
>
> Let's begin."

## Step 2: Detect existing state — HARD GATE

**This must be the very first action after the welcome. Do NOT run any other Bash commands, Edit/Write operations, or "let me prepare the directories" reasoning before this gate fires.**

Run exactly this check, and only this check:

```bash
test -f "$CLAUDE_PROJECT_DIR/.claude/diamonds/active.yml"
```

- **If exit code 0** (file EXISTS): the project already has Mycelium state. Skip directly to Step 4 routing output. **Do NOT run setup. Do NOT run mkdir. Do NOT touch `.gitkeep` stubs.** Setup-style operations on an already-initialized project waste tokens and trigger Read-before-Write tool errors when the agent then tries to write to existing files. Detected during 2026-05-09 plugin-form dogfood — the agent ran `mkdir -p .claude/...` before honoring this gate, then hit a Write error on `active.yml` and only then realized the project was initialized. The fix is structural: the gate is the first action.

- **If exit code 1** (file does NOT exist): invoke the setup workflow inline. Follow the instructions in `${CLAUDE_PLUGIN_ROOT}/skills/setup/SKILL.md` exactly — same Step 1 detection (which will fall through), Step 2 directory creation with `.gitkeep` stubs, Step 3 starter file writes, Step 4 AGENTS.md prompt (default-yes in non-interactive contexts), Step 5 confirmation message. Do not duplicate the setup logic here; reference it.

After setup completes, do NOT print setup's "Next:" line — this skill is the next step. Print:

> "Setup done. Now: 4 questions about your idea, ~10 minutes."

## Step 3: Run interview (universal-flow shape)

Invoke the interview workflow inline. Follow the instructions in `${CLAUDE_PLUGIN_ROOT}/skills/interview/SKILL.md` from Phase 0 onward.

Because setup just ran, the canvas is empty — /interview's canvas-state detection will route to the Universal Brief Flow (the 4-question brief shape, not the legacy time-budget-routed ceremony). Render the brief, write canvas state, render the depth menu. Per opp-006 narration discipline in interview/SKILL.md, do not narrate phase numbers to the user — reference the outcome (e.g., "the brief", "the project-type question") instead of the phase index.

After the brief is rendered and the user picks a depth-menu option, the start skill is done. Hand off to whatever the user chose (`/mycelium:assumption-test` for "Test the biggest assumption", continued discovery for "Go deeper", graceful exit for "Stop for now", etc.).

## Step 4: Routing for already-initialized projects

If Step 2 detected existing canvas state (the user has Mycelium installed already on this project), do NOT run setup or interview. Instead, print:

> "This project already has Mycelium state from [date of last write to .claude/diamonds/active.yml]. Last diamond touched: [scale, phase, confidence, name]. Three options:
>   1. Run `/mycelium:diamond-assess` to see current state and what to work on next.
>   2. Run `/mycelium:interview` to add a new idea as a sibling diamond on this product.
>   3. Stop and look around. Canvas files are in `.claude/canvas/`."

Then exit. The user picks the next move.

## What this skill does NOT do

- Does NOT modify CLAUDE.md, README.md, CONTRIBUTORS.md, or LICENSE.
- Does NOT block or prompt at the welcome step — it's read-and-continue, not interactive.
- Does NOT replace setup or interview. They remain invocable directly. start is the convenience composition.
- Does NOT run on every session — only on first invocation. After the first run, canvas state exists and Step 2 routes to diamond-assess.

## Why this skill exists

Without `/mycelium:start`, the first-time plugin user has to:
1. Run `/plugin install mycelium@haabe-mycelium` (Claude Code message: "installed")
2. Wonder what to do
3. Find `/mycelium:setup` (no obvious pointer at install time)
4. Run setup (gets a brief next-step message)
5. Run `/mycelium:interview`
6. Get value (the brief)

That's 5 typed commands and 2 cognitive gaps before value lands. The void between steps 1 and 5 is real friction.

`/mycelium:start` collapses 1→6 into 1→2 with a welcome message that gives the framework a 30-second introduction at exactly the moment the user has the question "what is this and what do I do." Setup+interview both still exist as separate skills for users who want them piecewise.

## Theory grounding

- Norman: visible affordances at the moment of cognitive need (the welcome message at the install gate).
- Krug "Don't Make Me Think": one command instead of two, with explanation built in.
- Hashimoto regeneration zones: the welcome is generation-cheap context that the user can re-read or skip; doesn't add discipline cost to the actual work.
- Brownfield-additive principle (Bentes 2026-05-08): the start skill respects the same "no project root modification" constraint as setup — it adds project state without touching user-owned root files.

## Source

The friction this skill addresses surfaced 2026-05-09 during the founder's smoke-test of the v0.20.x plugin form. The user reported: "the onboarding has worsened substantially since converting to plugin. The user is left in the unknown void for quite a bit."

Setup + welcome + immediate interview transition is the first response. If the welcome-as-text approach proves insufficient (subsequent dogfood reports the void persists), graduate to: SessionStart hook that detects first-run-after-install and emits the welcome unprompted.
