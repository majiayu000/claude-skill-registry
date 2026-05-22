---
name: default-workflow
version: 1.0.0
description: Development workflow for features, bugs, refactoring. Auto-activates for multi-file implementations.
auto_activates:
  - "implement feature spanning multiple files"
  - "complex integration across components"
  - "refactor affecting 5+ files"
explicit_triggers:
  - /ultrathink
  - /amplihack:default-workflow
confirmation_required: true
skip_confirmation_if_explicit: true
token_budget: 4500
---

# Default Workflow Skill

## Purpose

This skill provides the standard development workflow for all non-trivial code changes in amplihack. It auto-activates when detecting multi-file implementations, complex integrations, or significant refactoring work.

The workflow defines the canonical execution process: from requirements clarification through design, implementation, testing, review, and merge. It ensures consistent quality by orchestrating specialized agents at each step and enforcing philosophy compliance throughout.

This is a thin wrapper that references the complete workflow definition stored in a single canonical location, ensuring no duplication or drift between the skill interface and the workflow specification.

## Canonical Source

**This skill is a thin wrapper that references the canonical workflow:**

**Source**: `.claude/workflow/DEFAULT_WORKFLOW.md` (471+ lines)

The canonical workflow contains the complete development process with all details, agent specifications, and execution guidance.

## Execution Instructions

When this skill is activated, you MUST:

1. **Read the canonical workflow** immediately:

   ```
   Read(file_path=".claude/workflow/DEFAULT_WORKFLOW.md")
   ```

   Note: Path is relative to project root. Claude Code resolves this automatically.

2. **Follow all steps** exactly as specified in the canonical workflow

3. **Use TodoWrite** to track progress through workflow steps with format:
   - `Step N: [Step Name] - [Specific Action]`
   - Example: `Step 1: Rewrite and Clarify Requirements - Use prompt-writer agent`
   - This helps users track exactly which workflow step is active

4. **Invoke specialized agents** as specified in each workflow step:
   - Step 1: prompt-writer, analyzer, ambiguity agents
   - Step 4: architect, api-designer, database, tester, security agents
   - Step 5: builder, integration agents
   - Step 6: cleanup, optimizer agents
   - Step 7: pre-commit-diagnostic agent
   - Step 9-15: Review and merge agents

## Why This Pattern

**Benefits:**

- Single source of truth for workflow definition
- No content duplication or drift
- Changes to workflow made once in canonical location
- Clear delegation contract between skill and workflow
- Reduced token usage (skill is ~60 lines vs 471+ in canonical source)

## Auto-Activation Triggers

This skill auto-activates for:

- Features spanning multiple files (5+)
- Complex integrations across components
- Refactoring affecting 5+ files
- Any non-trivial code changes requiring structured workflow

## Related Files

- **Canonical Workflow**: `.claude/workflow/DEFAULT_WORKFLOW.md`
- **Command Interface**: `.claude/commands/amplihack/ultrathink.md`
- **Orchestrator Skill**: `.claude/skills/ultrathink-orchestrator/`
- **Investigation Workflow**: `.claude/skills/investigation-workflow/`
