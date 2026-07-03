---
name: diverge-codex
description: Delegate creative divergence to a fresh Codex subagent before implementation. Use when the user explicitly asks Codex to delegate brainstorming, obtain an independent Codex context, or keep implementation separate from approach generation. Generate 3–5 conceptually distinct approaches, pause for selection, then assign the selected approach for implementation.
---

# Diverge with a fresh Codex context

Use a fresh subagent to reduce anchoring from the lead agent's conversation history. Preserve the brainstorm-then-select discipline from `$diverge`; do not claim cross-model diversity because both contexts run Codex.

Read [`../diverge/reference/creative-preference-optimization.md`](../diverge/reference/creative-preference-optimization.md) only when the user asks for the rationale or when refining the creativity criteria.

## Gate delegation

Delegate only when the user explicitly invokes `$diverge-codex` or asks for a subagent, independent context, or delegated brainstorm. If the skill was loaded implicitly without such a request, run the ordinary `$diverge` workflow locally.

## Phase 1: brief the brainstormer

Extract the task, hard constraints, existing artifacts, and acceptance criteria. Do not add an implementation preference.

Spawn one fresh Codex subagent with only the task-local context it needs. Give it this contract:

```text
Generate 3–5 conceptually distinct approaches to TASK. Do not implement.

Label every approach [Novel], [Surprising], [Diverse], or [Conventional].
Include at least one [Novel] and one [Surprising] approach. For each, provide:
1. Core mechanism — one sentence.
2. How it works and why it differs — two or three sentences.
3. Main tradeoff — one sentence.

Do not restate one idea with different vocabulary. Return only the approaches.
```

Do not reveal the lead agent's preferred solution or likely implementation. Consume the subagent's final answer, not its internal trace.

## Phase 2: present and pause

Check that the response contains 3–5 mechanically distinct approaches and satisfies the required labels. If it does not, send one focused correction to the same subagent.

Present the approaches without silently ranking, filtering, or rewriting them. Ask the user to select one approach or request a compatible synthesis. Stop before implementation.

## Phase 3: implement after selection

Send the selected approach, original task, constraints, and acceptance checks back to the same subagent when possible. Require it to:

- inspect current workspace state before editing;
- preserve unrelated user changes;
- implement the selected mechanism rather than substituting another;
- run proportionate checks; and
- return changed files, verification evidence, and any residual risk.

The lead agent owns integration. Inspect the resulting diff and verification output, fix integration defects, and report the final outcome.

## Fallbacks

- If subagents are unavailable, state that the independent-context path is unavailable and run `$diverge` locally.
- If the brainstorm subagent fails or returns empty output, retry once with a shorter brief, then fall back locally.
- If the selected approaches cannot be combined without changing the requested behavior, explain the incompatibility before proposing a hybrid.

## Constraints

- Never implement during the divergence phase.
- Never describe same-model subagents as independent model families.
- Never break a user selection by replacing it with the lead agent's preferred approach.
- Never delegate without the explicit delegation gate above.
