---
id: "6974bab8-e50f-43ab-9fbb-c42a9ca16326"
name: "100 / tool / 33"
description: "General SOP for common requests related to 100, tool, 33."
version: "0.1.0"
tags:
  - "100"
  - "tool"
  - "33"
triggers:
  - "Use when the user asks for a process or checklist."
  - "Use when you want to reuse a previously mentioned method/SOP."
examples:
  - input: "Break this into best-practice, executable steps."
---

# 100 / tool / 33

General SOP for common requests related to 100, tool, 33.

## Prompt

Follow this SOP (replace specifics with placeholders like <PROJECT>/<ENV>/<VERSION>):
1) Offline OpenAI-format conversation source.
2) Title: ad90ddb4-9e5f-4403-842b-48f21aea66b9.json#conv_1
3) Use the user questions below as the PRIMARY extraction evidence.
4) Use the full conversation below as SECONDARY context reference.
5) In the full conversation section, assistant/model replies are reference-only and not skill evidence.
6) Primary User Questions (main evidence):
7) |  | AIME(0.75x) |  | GPQA-Diamond(0.75x) |  | MATH(0.75x) |  |
8) | --- | --- | --- | --- | --- | --- | --- |
9) | Model | On Time | ACC | w/tool call | On Time | ACC | w/tool call | On Time | ACC | w/tool call |
10) | DeepSeek-V3.2 | 33.3 | 33.3 | 100.0 | 43.4 | 33.3 | 100.0 | 75.0 | 74.0 | 100.0 |

For each step, include: action, checks, and failure rollback/fallback plan.
Output format: for each step number, provide status/result and what to do next.

## Triggers

- Use when the user asks for a process or checklist.
- Use when you want to reuse a previously mentioned method/SOP.

## Examples

### Example 1

Input:

  Break this into best-practice, executable steps.
