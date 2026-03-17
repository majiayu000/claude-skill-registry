---
name: ultrathink-orchestrator
version: 1.0.0
description: Auto-invokes ultrathink workflow for any work request (default orchestrator)
DEPRECATED: true
deprecation_notice: |
  This skill is DEPRECATED as of 2025-11-26.
  Workflow selection is now handled directly in CLAUDE.md via the
  "MANDATORY: Workflow Selection" section. The indirection through
  skills has been eliminated to ensure consistent workflow enforcement.
auto_activate: false
priority: 5
triggers:
  - "implement"
  - "create"
  - "build"
  - "add"
  - "fix"
  - "update"
  - "refactor"
  - "design"
---

# Ultrathink Orchestrator Skill

## Purpose

This skill provides automatic orchestration for development and investigation tasks. It detects the task type from keywords and delegates to the appropriate workflow skill (investigation-workflow or default-workflow).

Auto-activation priority is LOW (5) to allow more specific skills to match first. When activated, this orchestrator selects between investigation-workflow and default-workflow based on the user's request keywords.

This skill acts as a thin wrapper around the canonical ultrathink command, following the amplihack pattern of single-source-of-truth for command logic.

## Canonical Sources

**This skill is a thin wrapper that references canonical sources:**

- **Primary Command**: `.claude/commands/amplihack/ultrathink.md` (278 lines)
- **Workflow Sources**:
  - Development: `.claude/workflow/DEFAULT_WORKFLOW.md`
  - Investigation: `.claude/workflow/INVESTIGATION_WORKFLOW.md`

The canonical command contains complete task detection logic, complexity estimation, and orchestration patterns for both investigation and development workflows.

## Execution Instructions

When this skill is activated, you MUST:

1. **Read the canonical command** for task detection logic:

   ```
   Read(file_path=".claude/commands/amplihack/ultrathink.md")
   ```

   Note: Path is relative to project root. Claude Code resolves this automatically.

2. **Detect task type** using keywords from the canonical command:
   - **Investigation keywords**: investigate, explain, understand, analyze, research, explore
   - **Development keywords**: implement, build, create, add feature, fix, refactor, deploy
   - **Hybrid tasks**: Both investigation and development keywords present

3. **Invoke appropriate workflow skill**:
   - Investigation: `Skill(skill="investigation-workflow")`
   - Development: `Skill(skill="default-workflow")`
   - Hybrid: Both sequentially (investigation first, then development)

4. **Fallback** if skill not found:
   - Read workflow markdown files directly
   - Investigation: `.claude/workflow/INVESTIGATION_WORKFLOW.md`
   - Development: `.claude/workflow/DEFAULT_WORKFLOW.md`
   - Follow workflow steps as specified

## Why This Pattern

**Benefits:**

- Single source of truth for orchestration logic in canonical command
- No content duplication between command and skill
- Task detection rules defined once, maintained once
- Changes to ultrathink command automatically inherited by skill

**Trade-offs:**

- Requires Read tool call to fetch canonical logic
- Slight indirection vs. inline implementation

This pattern aligns with amplihack philosophy: ruthless simplicity through elimination of duplication.

## Related Files

- **Canonical Command**: `.claude/commands/amplihack/ultrathink.md`
- **Development Workflow Skill**: `.claude/skills/default-workflow/`
- **Investigation Workflow Skill**: `.claude/skills/investigation-workflow/`
- **Canonical Workflows**:
  - `.claude/workflow/DEFAULT_WORKFLOW.md`
  - `.claude/workflow/INVESTIGATION_WORKFLOW.md`
