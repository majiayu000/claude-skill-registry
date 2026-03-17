---
description: Refine existing skill via skill-builder workflow (project)
argument-hint: [skill-path] [type: simple|standard|complex] [depth: base|extended|full]
---

## Parameters
Skill: $1
Type: $2
Depth: $3

## Infrastructure
@.claude/skills/skill-builder/SKILL.md
@.claude/skills/skill-builder/references/workflows/refine.md
@.claude/skills/parallel-dispatch/SKILL.md
@.claude/skills/deep-research/SKILL.md
@.claude/styles/report.md

## Target
@$1/SKILL.md

## Task
Execute skill-builder **Tasks:** with Scope=refine.

Compare input (Type=$2, Depth=$3) vs target frontmatter to derive mode:
- Input = existing → optimize
- Input > existing → upgrade
- Input < existing → downsize