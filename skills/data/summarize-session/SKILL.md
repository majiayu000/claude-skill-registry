---
name: summarize-session
description: Summarize the current session and generate reusable Claude rules, skills, or commands.
---

# Summarize Session

## Purpose

At the end of a productive coding session, analyze the conversation to extract reusable patterns and generate Claude Code artifacts (rules, skills, commands) that can accelerate future work.

## Instructions

1. **Review Session Activity**
   - What problems were solved?
   - What code was written or modified?
   - What workflows were performed?
   - What decisions were made and why?

2. **Identify Patterns**

   **Rules Candidates** (coding standards, project conventions):
   - Repeated code style corrections
   - Error patterns that were fixed
   - Best practices established
   - Project-specific conventions

   **Skills Candidates** (multi-step workflows):
   - Complex operations performed multiple times
   - Sequences of commands that go together
   - Integration or deployment workflows
   - Testing or validation procedures

   **Commands Candidates** (single-action shortcuts):
   - Frequently used command combinations
   - Build/test/deploy shortcuts
   - Common git operations
   - Project-specific utilities

3. **Generate Artifacts**

   For each identified pattern, create the appropriate artifact:

   **Rules** → `.claude/rules/<name>/RULE.md`
   ```markdown
   ---
   name: rule-name
   description: Brief description
   ---

   # Rule Name

   ## When to Apply
   ...

   ## Guidelines
   ...
   ```

   **Skills** → `.claude/skills/<name>/SKILL.md`
   ```markdown
   ---
   name: skill-name
   description: Brief description
   ---

   # Skill Name

   ## Instructions
   1. Step 1
   2. Step 2
   ...
   ```

   **Commands** → `.claude/commands/<name>.md`
   ```markdown
   # Command Name

   Description of what this command does.

   ## Steps
   1. ...
   2. ...
   ```

4. **Validate Artifacts**
   - Ensure artifacts are general enough to be reusable
   - Remove session-specific details
   - Test that instructions are complete and actionable

5. **Document Session Summary**
   - What was accomplished
   - What artifacts were generated
   - Recommendations for next session

## Output Format

```markdown
## Session Summary

### Accomplished
- [List of completed tasks]

### Generated Artifacts

#### Rules
- `<rule-name>`: <description>

#### Skills
- `<skill-name>`: <description>

#### Commands
- `<command-name>`: <description>

### Next Steps
- [Recommendations for future work]
```

## Examples

### Example: After Adding a New Adapter

**Identified Pattern**: Multi-step process for adding adapters
**Generated**: Skill `ai-rules-adapter-builder`

### Example: After Fixing Multiple Type Errors

**Identified Pattern**: TypeScript strict mode conventions
**Generated**: Rule `typescript-conventions`

### Example: After Repeated Test Commands

**Identified Pattern**: Test-then-commit workflow
**Generated**: Command `test-and-commit`
