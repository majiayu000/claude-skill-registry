---
name: gh-issue
description: Create a GitHub issue from a dendron note, stripping frontmatter and formatting for team review. Supports preview before submission.
---

# Create GitHub Issue from Dendron Note

When the user wants to submit a GitHub issue based on an existing dendron note (or asks you to draft one), follow this workflow.

## Workflow

1. **Identify the source note**: The user provides a path or dendron note name. Read the file.

2. **Identify the target repo**: Default is `Mjvolk3/Swanki`. Ask the user which repo to file against if not obvious from context.

3. **Draft the issue title**: Short, actionable title (under 80 chars). Imperative form, e.g. "Add validation for cloze card fields".

4. **Draft the issue body**: Strip the dendron frontmatter (everything between the opening and closing `---` lines). Keep the markdown content as-is. The note should already follow the formatting conventions below -- if it doesn't, reshape it lightly.

5. **Write to temp file for preview**: Write the body to `/tmp/gh-issue-body.md` so the user can review it in their editor before submission.

6. **Infer a label** from the issue content. Use one of the standard GitHub labels:
   - `enhancement` -- new feature, proposal, or improvement (most common for our workflow)
   - `bug` -- something is broken or producing wrong results
   - `documentation` -- docs additions or improvements
   - `question` -- needs discussion or clarification
   - `help wanted` -- we need input or assistance

   Pick the best fit based on the note content (e.g., a "Proposal" section usually means `enhancement`, a "Problem" describing broken behavior means `bug`).

7. **Show the user the planned submission**:
   ```
   Title: <title>
   Repo: <owner/repo>
   Label: <label>
   Body: /tmp/gh-issue-body.md
   ```
   Ask the user to confirm or request changes.

8. **Submit**: Once approved, run:
   ```bash
   gh issue create --repo <owner/repo> --title "<title>" --label "<label>" --body-file /tmp/gh-issue-body.md
   ```

9. **Report**: Show the issue URL returned by `gh`. Note that issue types (Task, Bug, etc.) cannot be set via CLI -- remind the user to set it in the GitHub UI if needed.

## Issue Formatting Conventions

Notes submitted as issues should use this structure (all sections optional except Problem):

```markdown
## Problem / Context

What is the issue? Why does it matter? Link to source code when relevant using full GitHub URLs (e.g. `[function_name](https://github.com/Mjvolk3/Swanki/blob/main/path/file.py#L10-L20)`).

## Proposal

What should change? Keep it concrete.

## Flow

Optional. Mermaid sequence or flow diagrams showing how the change fits the system. These render natively on GitHub.

## Code Changes

Optional. Reference specific files with their repo-relative paths in bold headers. Show minimal code snippets -- just the changed/new lines, not full functions.

## Priority

One-liner: High/Medium/Low + brief justification.
```

## Important Notes

- Always strip dendron frontmatter (the `---` YAML block at the top)
- Always strip dendron wiki-links (`[[note.path]]`) -- these don't render on GitHub. Replace with plain text or remove.
- GitHub renders mermaid diagrams natively -- keep them as-is
- GitHub renders markdown tables natively -- keep them as-is
- Full GitHub permalink URLs (to source code) render as clickable links -- prefer these over repo-relative paths in prose
- Always preview before submitting -- write to `/tmp/gh-issue-body.md` first
- The user's dendron notes are their working notes; the issue body may need light editing to remove internal references or add context

## Example Invocations

- "/gh-issue notes/scratch.2026.02.10.124842-cloze-validation.md"
- "/gh-issue scratch.2026.02.10.124842-cloze-validation.md to Mjvolk3/Swanki"
- "create a github issue from this note"
