---
name: prompt-optimization
description: Improve and rewrite user prompts to reduce ambiguity and improve LLM output quality. Use when a user asks to optimize, refine, clarify, or rewrite a prompt for better results, or when the request is about prompt optimization or prompt rewriting.
---

# Prompt Optimization

## Goal

Improve the user's prompt so Codex (or any LLM) produces better output while preserving intent.

## Workflow

1. Read the user's original prompt carefully.
2. Identify ambiguity, missing context, or unclear intent.
3. Rewrite the prompt to remove ambiguity and provide clear instructions.
4. Retain the core intention of the user's request.
5. Add relevant constraints (format, length, style) when helpful.

## Output format

Provide:
- Improved prompt
- Short explanation of what was improved

## Constraints

- Do not assume domain knowledge not in the original prompt.
- Preserve user intent.

## Example triggers
- “Draft me an email asking for feedback.”
- “Turn this into a daily to-do list.”
- $automating-productivity