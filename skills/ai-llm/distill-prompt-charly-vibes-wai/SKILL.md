---
name: distill-prompt
description: Create lean, token-efficient versions of prompts
disable-model-invocation: true
---

Analyze the provided DEVELOPER-FACING PROMPT. Your task is to distill it into a concise, token-efficient, LLM-FACING PROMPT.

The distilled prompt must retain only the essential instructions, rules, and structured commands required for the LLM to perform its task.

You MUST REMOVE:
1.  All front-matter and metadata (e.g., title, tags, status, version, related, source).
2.  All explanatory sections intended for humans (e.g., "When to Use," "Notes," "Example," "References," "Philosophy").
3.  Descriptive introductions, justifications, and conversational text.
4.  Verbose examples. Summarize them only if they are essential for defining a format.

The final output should be a clean, direct set of instructions for the LLM, with no additional commentary from you.

DEVELOPER-FACING PROMPT:
---
[Paste the verbose prompt content here]
---
