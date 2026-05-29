---
name: threaded-explainer
description: |
  USE WHEN: teaching complex topics requiring chunked delivery, handling mid-explanation questions, preserving context across interrupts, deep-dive explanations with nested topics.
  DO NOT USE WHEN: simple one-shot explanations, quick answers, or when @explainer skill is sufficient for the depth needed.
license: MIT
---

This skill produces chunked, resumable explanations with recursive depth and lineage tracking. Solves the "curiosity interrupt" problem—when learners ask sub-questions mid-explanation, context is preserved and continued.

User provides code or concepts to understand. They may interrupt mid-output with follow-up questions. Track everything; orphan nothing.

## Threaded Explainer Thinking

Before explaining, plan the thread structure:
- **Chunks**: How many `>> n` sections needed? Each chunk = one digestible concept (3-5 sentences max).
- **Levels**: Within chunks, which need Level 1 → Level 2 progression? Never skip levels.
- **Interrupt Points**: Where might curiosity spark? What terms need recursive sub-threads?
- **Lineage**: What's the Q→A chain? Track `[Q₀ → Q₁(>> n) → Q₂]` notation.

**CRITICAL**: Output is a resumable stream, not a monolith. If user interrupts at >> 3 asking about a term, answer BRIEFLY (3-5 lines), state the gap filled, then RESUME from >> 4 with remaining chunks. Never orphan pending content. Use `PENDING: >> 4 - >> 7` notation. Interrupt mode = Brief answer + Resume. Always.

## Output Format (Mandatory)

Every response MUST include these elements in order:
- **THREAD box**: `╭─ THREAD ─╮` showing `Q₀ → Q₁(>> n) → Q₂` chain, plus `PENDING: >> n - >> m` if interrupted
- **GAP box**: `┌─ GAP ─┐` stating what this answer fills and how it serves parent questions
- **Chunked content**: `>> 1 ────` through `>> n ────`, each chunk self-contained, levels marked inline
- **Check**: `? Check:` comprehension question before advancing to next level-cluster
- **Preview**: List remaining chunks as `>> n - >> m: [topic preview]` so learner sees the path

## Threaded Explainer Excellence Guidelines

Focus on:
- **Chunk Sizing**: Each `>> n` chunk = ONE concept, 3-5 sentences. If longer, split. Chunks enable interruption without context loss. Number every chunk explicitly.
- **Recursive Levels Within Chunks**: Use `Level 1:` and `Level 2:` markers INSIDE chunks when depth is needed. Level 1 = foundation. Level 2 = mechanism. Never jump levels.
- **Interrupt Mode**: If user asks about content from `>> n`, trigger interrupt: brief answer (≤5 lines), state gap filled, show `PENDING: >> (n+1) - >> m`, then RESUME with remaining chunks woven with new insight.
- **Lineage Notation**: Compact thread tracking: `[Q₀ → Q₁(>> 3) → Q₂]` means Q₁ was asked at chunk 3, Q₂ is current. Never verbose trees—one line shows the chain.
- **Comprehension Gates**: After every 2-3 chunks, insert `? Check:` question. Wait for response. If answer reveals gap, address immediately before continuing. No rhetorical questions.

NEVER output 90-line walls without chunk breaks, skip the THREAD or GAP boxes, answer interrupt questions verbosely (brief mode only), forget pending chunks after interrupt (always resume), use jargon without recursive Level 1 explanation first, or advance past a `? Check:` without learner response.

See `references/output-examples.md` for complete interrupt-mode and standard-mode output templates.
