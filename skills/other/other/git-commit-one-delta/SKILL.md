---
name: git-commit-one-delta
description: "{{ 𝚫𝚫𝚫 }} Generate a commit message. If nothing staged, stage all changes."
model: haiku
disable-model-invocation: true
allowed-tools: ["Bash(git:*)"]
---

## Steps
1. If no changes staged, stage all. If files are already staged, *do not* stage more files.
2. Generate commit message per conventional commits format.
3. Show message and await approval:
    - If approved, push to upstream
    - If changes requested, revise and repeat

<template format-reference="https://www.conventionalcommits.org/en/v1.0.0/">
  `type(scope?): description\n\nbody (optional)\n\nBREAKING CHANGE: footer (if applicable)`
</template>

<conventions>
  - Subject line: imperative mood, lowercase, no period, max 50 chars (`add feature` not `added feature` or `adds feature`)
  - Body: explain *what* and *why*, not *how*; wrap at 72 chars
</conventions>
