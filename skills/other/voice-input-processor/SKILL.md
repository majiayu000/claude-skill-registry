---
name: voice-input-processor
description: "A pre-processor skill for input that arrives via voice-to-text or as unstructured, free-flowing thought. Use when receiving long, complex, or voice-to-text input that may contain jumbled word order, misheard or substituted words, or unclear structure. Automatically applies to substantial input (roughly 3+ sentences) showing signs of voice-to-text errors or non-linear thinking. Also triggers manually when the user says things like process this, clean this up, interpret this, or make sense of this. Interprets input charitably, corrects errors, extracts clear meaning, and produces two outputs: a short human-facing summary for confirmation, and a full structured version ready for Claude to act on or hand off to another skill."
---

# Voice Input Processor

A pre-processing skill that turns messy, voice-to-text or free-flowing input into clean, structured understanding — before any action is taken.

This skill is a **pre-processor only**. It does not write blog posts, reports, or final documents. Its sole job is comprehension and clarity. It feeds cleanly into whatever comes next — whether that is Claude acting directly, or a downstream skill taking over.

---

## Understanding This Kind of Input

People communicating via voice-to-text, or thinking out loud, are not confused or unclear in their thinking. The ideas are often rich, well-reasoned, and intelligent. The *expression* is where friction occurs.

Common patterns to expect and work with:

- **Word substitutions** — voice-to-text mishearing produces wrong but phonetically similar words (e.g. "lords" instead of "Claude", "work" instead of "word", "hand off" instead of "handoff")
- **Non-linear structure** — the core point may arrive before or after the context that explains it; ideas loop back on themselves
- **Imprecise vocabulary** — the right word may not come easily; a near-enough word is used instead; read for intent
- **Incomplete sentences** — thought moves faster than speech; words get dropped
- **Thinking out loud** — the input may include the user working something out as they speak, not just stating a conclusion

Trust the intelligence behind the input even when the surface expression is imperfect. Your job is to bridge the gap, not to judge the quality of what was said.

---

## When to Apply

**Apply automatically when input:**
- Is 3 or more sentences long and shows signs of voice-to-text errors or non-linear structure
- Contains words that appear to be misheard substitutions
- Is a memo, set of instructions, or block of ideas being handed over for processing

**Apply on manual trigger when the user says:**
- "Process this"
- "Clean this up"
- "Interpret this"
- "Make sense of this"
- Or any similar phrase indicating they want their input clarified before action

**Apply lightly when input is moderate** — a brief restatement and confirmation is enough for shorter, mostly clear input. Reserve the full pipeline for genuinely complex or lengthy input.

**Do not apply when:**
- Input is short, clear, and well-formed (1–2 sentences with obvious intent)
- The user is asking a simple factual question
- No processing is needed to understand the intent

---

## Core Principles

**Interpret charitably, not literally**
Read the whole input before judging any part of it. Assume intelligence and clear intent behind imperfect expression.

**Correct, don't question**
Do not ask the user to repeat themselves or rephrase. Make a reasonable interpretation, note assumptions briefly, and proceed. Only ask a clarifying question if the intent is genuinely ambiguous and proceeding without clarity would waste significant effort.

**Never patronise**
The user knows exactly what they mean. Your job is to bridge the gap between their intent and what was captured — not to highlight their errors.

**Retain the original input**
Do not discard the raw original input after processing. Hold it in context. If a downstream skill hits an ambiguity, or the user wants to revisit something, the original is always there to refer back to.

**Keep outputs cognitive-load aware**
Dense walls of text are harder to process. Use short sentences, clear structure, and consistent vocabulary. Avoid using multiple different words to mean the same thing — pick one and stick with it.

---

## Processing Layers

Work through these in order. For shorter input, layers 1 and 2 may be sufficient.

### Layer 1 — Interpret

Read the full input before drawing any conclusions.

- Identify likely voice-to-text substitution errors and correct them in context
- Reorder ideas into logical sequence where the original is non-linear
- Fill small gaps in meaning using context from the rest of the input
- Note any assumptions you are making — briefly, not exhaustively

### Layer 2 — Extract

From your interpreted version, identify:

- **Core intent** — what does the user actually want to happen as a result of this input?
- **Key points** — the main pieces of information or instruction, in logical order
- **Implied next step** — is this feeding into a task, a document, a decision, or a downstream skill?

### Layer 3 — Produce Two Outputs

Always produce both outputs. They serve different purposes and different audiences.

---

#### Output A — Human-Facing Summary
*Short. Scannable. Low cognitive load. For the user to read and confirm.*

Keep this to 3–5 lines maximum. Its only job is to let the user quickly verify that Claude has understood correctly. It should not try to be comprehensive.

```
## I've understood this as:
[1–2 sentence plain English summary of the core intent]

## Key points:
- [Point 1]
- [Point 2]
- [Point 3]

## Assumptions:
- [Any word corrections or interpretations — one line each, only where meaningful]
```

---

#### Output B — Full Structured Handoff
*Complete. Detailed. Preserves all nuance and intent. For Claude to act on or pass to a downstream skill.*

This version should not be slimmed down. It carries everything needed for accurate action or handoff. The user does not need to read this in full — it exists for processing, not for human review.

```
## Processed Input — Full Handoff

### Original Intent
[Clear statement of what the user wants to achieve]

### Full Content — Reordered and Corrected
[Complete cleaned version of everything the user said, in logical order,
with voice-to-text errors corrected and structure clarified]

### Key Instructions or Points
1. [Instruction or point 1]
2. [Instruction or point 2]
3. [Instruction or point 3]

### Context and Background
[Any supporting context the user provided that informs the intent]

### Assumptions Made
- [Correction or interpretation 1]
- [Correction or interpretation 2]

### Implied Next Step
[What this input is leading toward — action, document, decision, or named downstream skill]
```

---

### Layer 4 — Confirm

After presenting Output A to the user, end with a single low-effort confirmation line:

> "Does that sound right, or shall I adjust anything before we proceed?"

If the interpretation is confident and the input was clear enough, you may skip this and proceed — noting briefly what you understood.

Do not ask multiple questions. One line only.

---

## Handoff Behaviour

Output B does not get passed anywhere automatically. It sits in the conversation history, which is exactly where it needs to be.

When the user invokes another skill in the same conversation — either by asking Claude to do something, or by triggering a skill directly — that skill has access to everything in the conversation context, including Output B. It does not need to be explicitly passed. Claude will draw on it naturally.

What this means in practice:

- After producing both outputs, Claude should briefly signal what Output B is there for, so the user understands they can continue without copying anything
- If a specific downstream skill is the obvious next step, name it — but do not imply a programmatic handoff is happening
- The user just needs to say what they want next

Example closing line:
> "Output B above has the full structured version ready. Just tell me what you'd like to do with it, or invoke another skill and I'll carry this forward."

---

## What This Skill Does Not Do

This is a pre-processor. It exists to support Claude's thinking and to bridge the gap between a user's intent and Claude's understanding.

It does not write final outputs. It does not make decisions. It does not add information that was not present in the original input. It does not over-correct — if something reads oddly but the meaning is clear, note it briefly and move on.