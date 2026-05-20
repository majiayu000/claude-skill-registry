---
name: pr-wordy-main-omega
description: "{{ 𝛀𝛀𝛀 }} Create a pull request to main"
model: opus
disable-model-invocation: true
allowed-tools: ["Bash(git:*)", "Bash(gh:*)", "Read", "Glob", "Grep"]
---

## Steps
1. Look at the commits on this branch
2. Analyse the overall effect of these changes if merged into `main`
3. Use `<template>` to write the pull request content
4. Check for my approval, then:
    - If approved, create the PR to `main`
    - If not, incorporate changes and repeat step 3

<rules>
  <title-rules>
    1. Brief & descriptive
    2. Use title case
    3. Be understandable to non-devs
  </title-rules>
  <summary-rules>
    Describe the PR with a non-technical, absurd metaphor.
  </summary-rules>
  <tldr-rules>
    1. List any steps devs must take after pulling this down
  </tldr-rules>
  <changes-rules>
    Break changes into files or categories depending on PR scope. Use collapsible details.
  </changes-rules>
</rules>

## Template
```md
# {{ title }}
## Overview
{{ overview }}
## Summary
{{ absurd metaphor }}
> [!TIP]
> {{ tldr }}
---
## Changes
{{ changes with collapsible details }}
---
```
