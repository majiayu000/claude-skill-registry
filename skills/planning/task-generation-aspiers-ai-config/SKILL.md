---
name: task-generation
description: Generate a detailed task list from a PRP. Use after a PRP is created and ready for implementation planning.
---

# Task Generation

Generate a detailed, step-by-step task list in Markdown format based on an existing Product Requirements Prompt (PRP).

## When to Use This Skill

Use this skill when:
- A PRP exists at `.ai/[feature-name]/prp.md`
- You need to break down the feature into implementable tasks
- Planning how a junior developer will implement the feature

## Input

- `feature_name` - Locates the PRP at `.ai/[feature-name]/prp.md`

## Process

1. **Receive PRP Reference**: The user points to a specific PRP file
2. **Analyze PRP**: Read and analyze the functional requirements, user stories, and other sections
3. **Clarify Open Questions**: If there are still any open questions, ask the user for clarification and amend the PRP accordingly before proceeding
4. **Phase 1: Generate Parent Tasks**: Based on the PRP analysis, create the main high-level tasks (3-8 parent tasks). Present these to the user in the specified format (without sub-tasks yet). Inform: "I have generated the high-level tasks. Ready to generate sub-tasks? Respond with 'go' to proceed."
5. **Wait for Confirmation**: Pause and wait for the user to respond with "go"
6. **Phase 2: Generate Sub-Tasks**: Once confirmed, break down each parent task into smaller, actionable sub-tasks
7. **Identify Relevant Files**: Based on tasks and PRP, identify potential files that need creation or modification
8. **Generate Final Output**: Combine parent tasks, sub-tasks, relevant files, and notes
9. **Save Task List**: Save to `.ai/[feature-name]/tasks.md`
10. **Commit Task List**: Stage and commit the new task list

## Commit Message Template

```
feat: add .ai/[feature-name]/tasks.md

Generate tasks according to .ai/[feature-name]/prp.md
```

## Output Format

The `tasks.md` file _must_ follow this structure:

```markdown
# Context

See [prp.md][./prp.md] for the corresponding Product Requirements Prompt.

# Relevant Files

- `path/to/file1.ts` - Brief description of why this file is relevant
- `path/to/file1.test.ts` - Unit tests for `file1.ts`
- `path/to/another/file.tsx` - Brief description
- `path/to/another/file.test.tsx` - Unit tests for `another/file.tsx`
- `lib/utils/helpers.ts` - Utility functions needed for calculations
- `lib/utils/helpers.test.ts` - Unit tests for helpers.ts

# Tasks

- [ ] 1. Parent Task Title
  - [ ] 1.1. Sub-task description 1.1
  - [ ] 1.2. Sub-task description 1.2

- [ ] 2. Parent Task Title
  - [ ] 2.1. Sub-task description 2.1

- [ ] 3. Parent Task Title (may not require sub-tasks)
```

## Target Audience

Assume the primary reader is a **junior developer** who will implement the feature.
Tasks should be clear, actionable, and provide enough context for someone less
familiar with the codebase to complete them.

## Interaction Model

The process explicitly requires a pause after generating parent tasks to get
user confirmation ("Go") before proceeding to generate detailed sub-tasks.
This ensures the high-level plan aligns with user expectations.
