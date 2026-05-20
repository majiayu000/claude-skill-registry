---
name: repo-check-deps
description: "{{ 𝛀𝛀𝛀 }} Investigate this repo's dependencies in detail"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash(npm:*)", "Bash(bun:*)", "Bash(pnpm:*)", "Bash(deno:*)", "WebSearch", "WebFetch"]
argument-hint: ["optional: concerning dep"]
---

<overview>
  Provide an in-depth analysis of this codebase's package dependencies, particularly $ARGUMENTS.
</overview>
<steps>
  1. Probe deeply into all deps, comparing their codebase version number with their current most recent version
  2. Check for deprecation notices & security warnings available online or via package management
  3. Suggest fixes and updates
</steps>
