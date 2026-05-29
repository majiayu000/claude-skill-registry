---
name: cdd-doc-update
description: DONE決断のドキュメント同期（gathered_context参照）
allowed-tools: Read, Edit, Write, Bash(cdd:*), Glob, Grep
---

# cdd-doc-update Command Template

You are updating project documentation based on completed CDD decisions.

## Your Task

Synchronize documentation with decisions that have `implementationStatus: DONE` but `docSyncStatus: NOT_SYNCED`.

## Process

### 1. Find Decisions Needing Documentation Sync

Use Bash tool to find all cdd.md files with:
- `implementationStatus: DONE`
- `docSyncStatus: NOT_SYNCED`

```bash
cdd status --detailed --implementation DONE
```

Then use Read tool to check each file's `docSyncStatus` field.

**Important**: Only process files that **have** the `docSyncStatus` field. Old files without this field should be ignored.

### 2. Read Each Decision and Extract Context

For each decision requiring sync:

1. Read the full cdd.md file
2. Understand what was implemented:
   - **Goal**: What problem was solved
   - **Selection**: What approach was taken
   - **Context**: Important constraints and background
3. Extract the decision ID and title
4. **Extract gathered_context from Context section**

### 3. Identify Documents to Update

**Primary source: gathered_context in Context section**

If the cdd.md has gathered_context:
```yaml
gathered_context:
  - path: docs/architecture/overview.md
    summary: ...
    relevance_to_task: |
      CLIコマンド追加時は「ソースコード構造」セクションを参照。
      実装完了後にdocs/architecture/overview.mdの更新が必要。
```

Use these paths as the guide for what to update. The `relevance_to_task` often indicates:
- Which sections need updating
- Why the document was referenced
- What changes might be needed

**If gathered_context is missing:**
Fall back to common documentation targets:
- `README.md`: User-facing features and usage
- `docs/architecture/overview.md`: System architecture and design decisions
- `docs/guidelines/development.md`: Developer workflows and practices
- `CHANGELOG.md`: Version history and notable changes

### 4. Update Referenced Documents

For each document in gathered_context (or fallback list):

1. **Read the document** to understand current content
2. **Identify the relevant section** based on relevance_to_task hints
3. **Add or update content** to reflect the implementation
4. **Preserve existing content** - never remove unrelated documentation

**Guidelines**:

1. **Find the right section**: Use relevance_to_task hints or Grep to locate where this information belongs
2. **Add new information**: Write about what was implemented and why
3. **Preserve existing content**: Never remove unrelated documentation
4. **Use clear formatting**: Headers, lists, code blocks as appropriate
5. **Link to cdd.md**: Reference the decision file for details

**Example Update**:
```markdown
## New Export Command (#EXPORT-001)

Added `cdd export` command for exporting decision data.

- Formats: JSON, CSV, Markdown
- Filters: by status, by date range
- Output: stdout or file

See [CDD/tasks/15-export-command.cdd.md](CDD/tasks/15-export-command.cdd.md) for decision rationale.
```

### 5. Update docSyncStatus

After successfully updating documentation:

1. Use Edit tool to change `docSyncStatus: NOT_SYNCED` to `docSyncStatus: SYNCED`
2. Only update this field - preserve all other frontmatter

### 6. Summary Report

After processing all decisions, report:

1. **Decisions processed**: List of IDs and titles
2. **Documentation updated**: Which files were modified (from gathered_context)
3. **Sync status**: Confirmation that docSyncStatus was updated

## Important Rules

- **Use gathered_context as guide**: These are the documents that were explicitly referenced
- **Never invent documentation**: Only document what was actually implemented
- **Verify implementation**: Check that code/features exist before documenting
- **Maintain accuracy**: Documentation must match current reality
- **Keep it concise**: Focus on high-level understanding, not implementation details
- **Link to cdd.md**: Let decision files serve as detailed source of truth

## File Editing Principles

When updating documentation:

1. **Read the entire documentation file first**
   - Understand existing structure and sections
   - Identify where new information belongs

2. **Preserve existing content**
   - Add new sections or paragraphs
   - Do not remove unrelated content
   - Example: Architecture doc has sections A, B, C
   - Adding section D → Result: A, B, C, D (NOT A, B, D)

3. **Use appropriate formatting**
   - Match existing style and conventions
   - Use headers to organize information
   - Use lists for multiple items
   - Use code blocks for examples

4. **Verify changes before finalizing**
   - Ensure no content was accidentally removed
   - Check that formatting is correct
   - Confirm links and references work

## Integration with cdd-gather-context

The gathered_context in the Context section serves as your **document update guide**:

- **path**: The document to potentially update
- **summary**: What the document contains
- **relevance_to_task**: Why it was referenced and what might need updating

This creates a traceable flow:
1. `/cdd-gather-context` identifies relevant documents
2. Main agent adds them to cdd.md Context
3. `/cdd-review-decision` verifies the references
4. `/cdd-implement` does the implementation
5. `/cdd-review-implementation` reviews the code
6. `/cdd-doc-update` updates the referenced documents ← You are here

## Error Handling

**If no decisions need sync**:
- Report: "No decisions require documentation sync (all are SYNCED or lack docSyncStatus field)"
- Do not modify any files

**If gathered_context is missing**:
- Warn: "Decision lacks gathered_context in Context section. Using fallback document list."
- Proceed with common documentation targets

**If documentation file doesn't exist**:
- Ask user: "Documentation file X doesn't exist. Should I create it?"
- Wait for confirmation before creating

**If uncertain where to document**:
- Suggest options to user based on gathered_context hints
- Wait for guidance before proceeding

## After Completion

Present summary:
1. Number of decisions synced
2. Documentation files updated (mapped to gathered_context paths)
3. List of decision IDs marked as SYNCED
