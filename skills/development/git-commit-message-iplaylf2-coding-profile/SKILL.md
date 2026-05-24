---
name: git-commit-message
description: Generate semantic commit messages in English. Use when the user asks for a commit message or semantic commit guidance. Prefer the user’s stated change intent and context, and keep the message consistent with the actual change.
metadata:
  short-description: Semantic commit messages
---

# Git Commit Message

Generate one semantic commit message that captures the change at the right level: intent and effect first, details second.

## Output

Provide:

* One semantic commit message in English.
* Alternatives only if the user asks for options.

## Format

Default to `<type>(<scope>): <summary>`.
If `scope` is unclear, omit it or ask one quick clarification.

Examples:

* `docs(cli): simplify installation section`
* `fix(parser): handle empty input`

## Workflow

1. Build a change summary from context.

   * Prefer the user’s stated purpose, constraints, and affected area.
   * Treat code edits as evidence of the change, not the full story.
2. Validate against the actual change.

   * Use staged changes when available; otherwise use the user’s described edits.
   * If the stated intent conflicts with the change, ask a brief clarification.
3. Choose `type` and `scope`.

   * Pick the smallest accurate `type`.
   * Choose a narrow, stable `scope` that names the primary area changed.
4. Write the summary.

   * Present tense, factual, information-dense.
   * Prefer explicit intent and effect when available.
   * If no intent is provided, describe the change at a semantic level without inventing reasons.

## Heuristics

* Optimize for information density. Avoid embellishment.
* Keep `type`, `scope`, and `summary` complementary. Avoid overlap.
* Choose a scope that adds signal. Do not repeat obvious repo or product names.
* Prefer semantic outcomes over mechanical descriptions of edits.
* Do not infer intent when it is not stated. Ask one brief question only when required for correct `type`, `scope`, or intent.
