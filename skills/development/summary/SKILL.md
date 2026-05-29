---
name: summary
description: Generate branch summaries for PR descriptions.
---

# Summary

Generate concise summaries of changes made on the current branch for PR descriptions.

## Requirements

- Must be in a git repository
- Must be on a branch (not main/master)

## Execution

Create a short summary of changes made on this branch suitable for a PR description.

**Scope:** Current branch vs main

### Steps

1. **Verify branch context:**
   - Check current branch: `git branch --show-current`
   - Ensure not on main/master (error if so)

2. **Get changes:**
   - Run `git diff main...HEAD` to see all changes since divergence
   - Run `git log main..HEAD --oneline` to see commit history

3. **Analyze changes:**
   - Review the diff to understand what was changed
   - Look at commit messages for context
   - Identify the main purpose/theme of the changes
   - Note key files/components modified
   - Identify the type of change (feature/fix/refactor/docs/etc.)

4. **Generate summary:**
   - Create a concise 2-4 sentence summary capturing:
     - What was changed (high-level)
     - Why it was changed (if evident from commits/diff)
     - Any notable technical decisions or approaches
   - Focus on "why" over "what" where possible
   - Use clear, direct language
   - Avoid technical jargon unless necessary

5. **Format for PR:**
   - Present the summary ready to paste into PR description
   - Include list of key files changed (if helpful)
   - Suggest test plan items if relevant

### Output Format

```markdown
## Summary
[2-4 sentence summary]

## Key Changes
- [Main change 1]
- [Main change 2]
- [Main change 3]

## Test Plan
- [ ] [Test item 1 if relevant]
- [ ] [Test item 2 if relevant]
```

### Notes

- Keep it SHORT - PR descriptions should be scannable
- Focus on the "why" and "so what" over implementation details
- If the branch has many unrelated changes, call that out
- Suggest splitting the summary if changes are too diverse
