---
name: answer-reviewer-questions
description: "For each reviewer question on a PR, recall implementation reasoning and compose a raw answer. Use when the user asks to \"answer reviewer questions\", \"draft answers to PR questions\", or \"explain reviewer questions\"."
---

# Answer Reviewer Questions

For each reviewer question thread, recall the implementer's reasoning and compose a raw answer. The answers are plain text and feed into a downstream reply-drafting skill that applies voice rules and reply formatting.

## Step 1: Collect Question Threads

Use the question threads from conversation context. Each thread has: thread id, file path, line (use `originalLine` when `line` is null), the reviewer's original comment, and the reconciled intent from `/interpret-feedback`.

If no question threads were provided, report that there are no questions to answer and stop.

## Step 2: Answer Each Thread

For each thread:

1. Run the `/recall-reasoning` skill with `<path>:<line>`. It returns either recalled reasoning from a past transcript, or a fallback derived from reading the commit diff and surrounding code.
2. Compose a one-or-two-sentence answer from the returned reasoning. Quote or paraphrase the implementer's own words when the recalled reasoning explains the decision well.
3. Do not mention Claude, transcripts, or that the reasoning was recalled. The answer reads as the implementer's own explanation.

## Step 3: Output Answers

Output one block per thread:

```
**Thread <id>** (<path>:<line>)
<answer text>
_Grounding: derived from current code_
```

Include the `_Grounding:_` line only when `/recall-reasoning` returned no transcript. Omit it when the answer is grounded in recalled reasoning.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Do not load `/github-voice` or apply reply formatting. Downstream drafting applies voice rules when composing the actual reply.
- When `/recall-reasoning` returned no transcript, still compose an answer from the current code and include the `_Grounding:_` line so the downstream drafter knows the answer has weaker grounding.
