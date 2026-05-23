---
name: descriptive-action
description: Use when the user asks to describe, summarize, analyze, compare, explain, or report on something (text, data, events, systems) without asking for recommendations or next steps.
version: 1.0
---

# Descriptive Action Skill

## Purpose
Produce accurate, neutral descriptions and analyses. Do not prescribe actions unless explicitly requested.

## When to use
Use this skill when the user request is primarily:
- Describe / explain / summarize / define
- Analyze / interpret / compare
- Extract facts from provided material
- Report status, metrics, or observations

Do NOT use if the user asks “what should I do”, “recommend”, “best way”, “steps”, “plan”, or “strategy”.

## Operating rules
1. Stay observational: focus on what is true in the input and what can be inferred safely.
2. Separate facts from interpretation:
   - Facts: directly supported by the provided input.
   - Inferences: clearly labeled.
3. If key information is missing, state what’s missing and proceed with bounded analysis.
4. Avoid normative language.
5. Prefer structure over prose.

## Inputs
- Text, data, artifacts, or systems to describe
- Any stated constraints (scope, timeframe, audience)

## Outputs
Structured descriptive analysis using the format below.

### Summary
- 3–6 bullets capturing the main points.

### Details
- Organized sections (background, findings, trends, constraints).

### Evidence
- Brief references to supporting input.

### Open questions
- Unknowns limiting confidence.
