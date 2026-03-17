---
description: Create new skill via skill-builder workflow (project)
argument-hint: [type: simple|standard|complex] [depth: base|extended|full] [context?]
---

## Parameters
Type: $1
Depth: $2
Context: ${3:-none}

## Infrastructure
@.claude/skills/skill-builder/SKILL.md
@.claude/skills/parallel-dispatch/SKILL.md
@.claude/skills/deep-research/SKILL.md
@.claude/styles/report.md

## Task
Execute skill-builder **Tasks:** with Scope=create, Type=$1, Depth=$2.

Context=${3:-none} provides purpose, triggers, and outputs for requirements capture.