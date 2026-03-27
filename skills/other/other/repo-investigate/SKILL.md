---
name: repo-investigate
description: "{{ 𝛀𝛀𝛀 }} Investigate a codebase in detail"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Write"]
argument-hint: [focus of investigation]
---

<overview>
  Provide an in-depth analysis of this codebase, focussing squarely on $ARGUMENTS.
</overview>
<steps>
  1. Probe deeply into all files & the relationships between them.
  2. If no focus is specified, consider the codebase as a whole.
  3. Create a structured .md document in @docs/investigations/ with your findings
</steps>
