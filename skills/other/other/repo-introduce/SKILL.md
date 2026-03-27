---
name: repo-introduce
description: "{{ 𝛀𝛀𝛀 }} Provide a detailed high-level overview of this codebase"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep"]
argument-hint: [focus of analysis]
---

<overview>
  Provide an overview of this codebase aimed at a newly-joined developer.
</overview>
<steps>
  1. Analyse the codebase as a developer would when reading unfamiliar code.
  2. If $ARGUMENTS contains content, consider how it relates to this codebase.
  3. Provide a practical, detailed overview.
</steps>
<inputs>
  $ARGUMENTS
</inputs>
