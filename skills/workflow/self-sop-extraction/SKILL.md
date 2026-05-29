---
id: "39121a6d-d3f8-4ca7-b304-5fec9545ed8b"
name: "self / sop_extraction"
description: "General SOP for extracting and structuring processes or checklists from conversation evidence."
version: "0.1.1"
tags:
  - "self"
  - "sop"
  - "extraction"
  - "process"
  - "checklist"
triggers:
  - "Use when the user asks for a process or checklist."
  - "Use when you want to reuse a previously mentioned method/SOP."
examples:
  - input: "Break this into best-practice, executable steps."
---

# self / sop_extraction

General SOP for extracting and structuring processes or checklists from conversation evidence.

## Prompt

Follow this SOP to extract and structure processes from conversation evidence (replace specifics with placeholders like <PROJECT>/<ENV>/<VERSION>):
1) Identify the Offline OpenAI-format conversation source.
2) Note the Title/ID of the conversation.
3) Use the user questions provided as the PRIMARY extraction evidence.
4) Use the full conversation context as SECONDARY reference.
5) In the full conversation section, assistant/model replies are reference-only and not skill evidence.
6) Primary User Questions (main evidence): [Extract from context]
7) Configuration/Context Details: [Extract from context]

For each step, include: action, checks, and failure rollback/fallback plan.
Output format: for each step number, provide status/result and what to do next.

## Triggers

- Use when the user asks for a process or checklist.
- Use when you want to reuse a previously mentioned method/SOP.

## Examples

### Example 1

Input:

  Break this into best-practice, executable steps.
