---
name: pick-next-prompt
description: "Pick the next prompt from .turbo/prompts.md and plan its implementation. Use when the user asks to \"pick next prompt\", \"next prompt\", \"continue prompt plan\", \"what's next\", \"next implementation step\", or \"continue with the plan\"."
---

# Pick Next Prompt

Pick the next prompt from `.turbo/prompts.md` and plan its implementation.

## Step 1: Run `/plan-style` Skill

Run the `/plan-style` skill to load planning conventions.

## Step 2: Read the Prompt Plan

Read `.turbo/prompts.md`. Parse all prompts extracting:
- Prompt number and title
- Status (`pending`, `in-progress`, `done`)
- Dependencies (`Depends on` field)
- The prompt text block

Also read `.turbo/spec.md` (or the spec path referenced in the prompt plan header) for full context.

## Step 3: Pick the Next Prompt

Find the first `pending` prompt whose dependencies are all `done`.

- **If found**: proceed to Step 4
- **If all prompts are `done`**: report completion to the user — the plan is finished
- **If remaining prompts are blocked**: report which prompts are blocked and by what

## Step 4: Adapt the Prompt

Re-read the spec and compare against the current project state. Adjust the prompt if implementation has diverged:

- **File paths changed** — update references to match actual structure
- **Architecture evolved** — adjust the prompt to work with what was actually built
- **Scope shifted** — add or remove items based on what prior work produced
- **New information** — incorporate discoveries from previous sessions

Update `.turbo/prompts.md` with adjustments to the selected prompt. For affected future prompts, update their Context and Depends-on fields if the adaptation changes what they can assume.

Mark the selected prompt `in-progress` in `.turbo/prompts.md`.

## Step 5: Plan

Using the selected prompt as the requirements, explore the codebase, design the implementation, and write a detailed plan (exact file paths, function signatures, data flow, test cases).

The plan's final step must instruct: "Mark prompt N as `done` in `.turbo/prompts.md`."

## Rules

- Never modify the spec file — only `.turbo/prompts.md` is writable (besides the plan file)
- If the prompt plan file does not exist, tell the user to run `/create-prompt-plan` first
- Keep adaptations minimal — adjust only what diverged, do not rewrite prompts unnecessarily
