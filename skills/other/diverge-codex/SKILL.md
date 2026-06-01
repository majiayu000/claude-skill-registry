---
name: diverge-codex
description: Delegate creative divergence to Codex (GPT-5.4). Codex generates 3-5 conceptually distinct approaches before any implementation; Claude presents them for selection, then has Codex implement the chosen one. Cross-model brainstorm-then-select.
argument-hint: "[describe the task to delegate to Codex for divergent brainstorming]"
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
---

# Diverge → Codex

Delegate a task to Codex (GPT-5.4) with explicit creative divergence instructions. Claude structures the prompt; Codex brainstorms; Claude presents the options for selection; Codex implements the chosen approach. Running the brainstorm on a second model family widens the space of approaches beyond what one model proposes.

## Heritage and scope

Cross-model sibling of [`diverge`](../diverge/SKILL.md), grounded in **Creative Preference Optimization** (Ismayilzada et al., 2025; background in [`../diverge/reference/creative-preference-optimization.md`](../diverge/reference/creative-preference-optimization.md)). Same brainstorm-then-select discipline, run on a different model whose blind spots differ from Claude's.

## Codex invocation mechanism

Plain Claude Code has no native `codex:codex-rescue` subagent. Every "ask Codex" step below means: use the `Bash` tool to call `codex exec` directly (the same mechanism `paper-review-lite-codex` uses). Requirements:

- **`< /dev/null`** — closes stdin. Without it, `codex exec` hangs on "Reading additional input from stdin…" even when the prompt is passed as a CLI argument. This is the single most common failure mode.
- **`--skip-git-repo-check`** so it runs regardless of git state, and **`--sandbox`** set per phase: `read-only` for brainstorming (no file writes), `workspace-write` for implementation.
- **`timeout: 600000`** (10 min) on the Bash call as a backstop.

The result returns on stdout — read it directly from the Bash output. Treat a non-zero exit, or empty output, as a Codex failure: report it and offer to fall back to `/diverge` (Claude-only).

## Steps

1. **Take the task.** Use `$ARGUMENTS`. If empty, ask the user what they want to solve.

2. **Clarify if needed.** If the task is ambiguous about the goal (not the implementation), ask one focused question before delegating. Skip if clear.

3. **Brainstorm via Codex.** Run the brainstorm prompt through `codex exec` (read-only sandbox), substituting `TASK` with the user's request verbatim:

   ```bash
   codex exec --sandbox read-only --skip-git-repo-check "$(cat <<'CODEXEOF'
   <brainstorm prompt template below, with TASK substituted>
   CODEXEOF
   )" < /dev/null
   ```

4. **Present approaches** to the user verbatim — do not paraphrase or filter them. Ask which to pursue, or whether to synthesize.

5. **Implement via Codex.** Run the implementation prompt through `codex exec` (workspace-write sandbox, `-C` set to the project directory), substituting `TASK` and `SELECTED_APPROACH`:

   ```bash
   codex exec --sandbox workspace-write --skip-git-repo-check -C "<project dir>" "$(cat <<'CODEXEOF'
   <implementation prompt template below, with TASK and SELECTED_APPROACH substituted>
   CODEXEOF
   )" < /dev/null
   ```

## Brainstorm prompt template

```xml
<task>
Before implementing, generate 3–5 conceptually distinct approaches to:

TASK

Label each approach:
  [Novel]       — different conceptual basis from the conventional solution
  [Surprising]  — violates the obvious assumption; not the first answer
  [Diverse]     — maximally different from the other options in this list
  [Conventional]— the expected path, for contrast

For each approach provide:
- Core mechanism (1 sentence)
- How it works and what makes it distinct (2–3 sentences)
- Main tradeoff (1 sentence)

Do not implement. Present all approaches and stop.
</task>

<constraints>
At least one approach must be [Surprising].
At least one must be [Novel].
Approaches must differ in underlying mechanism, not just vocabulary.
Prioritize novelty and surprise over immediate quality.
Do not write any implementation code.
</constraints>

<structured_output_contract>
Numbered list only. No preamble. No implementation code.
Format each: number, label, mechanism line, explanation, tradeoff line.
</structured_output_contract>
```

## Implementation prompt template

```xml
<task>
Implement the following approach to: TASK

Selected approach: SELECTED_APPROACH

Implement it fully. Edit files in place where applicable.
</task>
```

## Notes

- Always brainstorm first — never ask Codex to implement on the first delegation.
- Do not inject your own implementation preferences — let Codex generate the approaches.
- Present Codex's approaches verbatim; do not paraphrase or filter them.
- If Codex is unavailable or errors, fall back to `/diverge` (Claude-only).
