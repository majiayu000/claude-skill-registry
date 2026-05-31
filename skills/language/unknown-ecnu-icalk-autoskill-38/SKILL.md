---
id: "95095330-7c14-4dee-b6b9-04b8f0b3e79f"
name: "из / по / на"
description: "General SOP for common requests related to из, по, на."
version: "0.1.0"
tags:
  - "из"
  - "по"
  - "на"
triggers:
  - "Use when the user asks for a process or checklist."
  - "Use when you want to reuse a previously mentioned method/SOP."
examples:
  - input: "Break this into best-practice, executable steps."
---

# из / по / на

General SOP for common requests related to из, по, на.

## Prompt

Follow this SOP (replace specifics with placeholders like <PROJECT>/<ENV>/<VERSION>):
1) Offline OpenAI-format conversation source.
2) Title: f99427b91a04d43a5244f1b54e024a1f.json#conv_1
3) Use the user questions below as the PRIMARY extraction evidence.
4) Use the full conversation below as SECONDARY context reference.
5) In the full conversation section, assistant/model replies are reference-only and not skill evidence.
6) Primary User Questions (main evidence):
7) Азбуковники являлись     одним      из     наиболее     распространенных
8) лексикографических жанров в Московской Руси конца XVI — начала XVII вв . Они   были    созданы   на    материале   предшествующих    лексикографических сводов —  глоссариев  и   приточников ,  в  которых   объяснялись  трудные  для
9) понимания ,  как  правило ,  иноязычные  слова
10) текстов , религиозные понятия и христианские

For each step, include: action, checks, and failure rollback/fallback plan.
Output format: for each step number, provide status/result and what to do next.

## Triggers

- Use when the user asks for a process or checklist.
- Use when you want to reuse a previously mentioned method/SOP.

## Examples

### Example 1

Input:

  Break this into best-practice, executable steps.
