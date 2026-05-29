---
name: update-gitignore
description: Create or update .gitignore file
user-invocable: true
allowed-tools: ["Bash(curl:*)", "Bash(uname:*)", "Bash(git:*)", "Read", "Write", "Edit", "Glob"]
model: haiku
context: fork
argument-hint: [additional-technologies]
version: 0.1.0
---

## Context

- Project guidelines: @CLAUDE.md
- Operating system: !`uname -s`
- Existing .gitignore status: !`test -f .gitignore && echo ".gitignore found" || echo ".gitignore not found"`
- Project files: Analyze repository structure to detect technologies
- Available templates: !`curl -sL https://www.toptal.com/developers/gitignore/api/list`

---

## Phase 1: Technology Detection

**Goal**: Identify operating systems and technologies to include in .gitignore

**Actions**:
1. Detect operating systems and technologies from context
2. Combine detected platforms with `$ARGUMENTS` into the generator request (e.g. `<os>,<language>,<tool>`)

---

## Phase 2: Generate or Update .gitignore

**Goal**: Create or update .gitignore file using Toptal API

**Actions**:
1. Generate or update `.gitignore` using the Toptal API
2. Preserve existing custom sections when updating `.gitignore`
3. Retain all custom rules from existing file

---

## Phase 3: Confirmation

**Goal**: Present changes for user review

**Actions**:
1. Show the repository changes (diff) to confirm the update
2. Present the resulting diff for user confirmation
