---
name: spec
description: "Core specification workflow engine. Triggers stage agents (CREATE, RESEARCH, PLAN, IMPLEMENT, REVIEW, TEST, etc.) for structured development. Triggers on keywords: spec, specification, plan spec, implement spec, review spec"
project-agnostic: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Skill
---

/spec STAGE SPEC: STRICTLY FOLLOW ${CLAUDE_PLUGIN_ROOT}/agents/spec/{STAGE}.md using STAGE AND SPEC as the variables

## Variables

STAGE=$ARGUMENTS
SPEC=$ARGUMENTS / LAST USED SPEC

## Spec Rules

- Default path: specs/<YYYY>/<MM>/<branch>/<NNN>-<title>.md
- Modify AI Section only; never touch Human Section
- Commit after each stage: `spec(<NNN>): <STAGE> - <title>`
- One stage = one commit (do NOT bundle multiple stages)

## Conditional Documentation

When working with external specs storage, read:
- `${CLAUDE_PLUGIN_ROOT}/scripts/spec-resolver.sh`
- `${CLAUDE_PLUGIN_ROOT}/scripts/external-specs.sh`
- `${CLAUDE_PLUGIN_ROOT}/scripts/lib/config-loader.sh`
