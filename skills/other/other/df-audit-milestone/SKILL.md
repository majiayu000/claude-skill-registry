---
name: df:audit-milestone
description: |
  Audit milestone completion against original intent before archiving.
  Expensive operation that checks requirements coverage and cross-objective integration.
argument-hint: "[version]"
disable-model-invocation: true
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Task
  - Write
---
<objective>
Verify milestone achieved its definition of done. Check requirements coverage, cross-objective integration, and end-to-end flows.

**This command IS the orchestrator.** Reads existing VERIFICATION.md files (objectives already verified during execute-objective), aggregates tech debt and deferred gaps, then spawns integration checker for cross-objective wiring.
</objective>

<execution_context>
@~/.claude/devflow/workflows/audit-milestone.md
</execution_context>

<context>
Version: $ARGUMENTS (optional — defaults to current milestone)

**Original Intent:**
@.planning/PROJECT.md
@.planning/REQUIREMENTS.md

**Planned Work:**
@.planning/ROADMAP.md
@.planning/config.json (if exists)

**Completed Work:**
Glob: .planning/objectives/*/*-SUMMARY.md
Glob: .planning/objectives/*/*-VERIFICATION.md
</context>

<process>
Execute the audit-milestone workflow from @~/.claude/devflow/workflows/audit-milestone.md end-to-end.
Preserve all workflow gates (scope determination, verification reading, integration check, requirements coverage, routing).
</process>
