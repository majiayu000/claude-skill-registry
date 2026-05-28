---
name: drive-workflow
description: Implementation workflow for processing tickets.
user-invocable: false
---

# Drive Workflow

Step-by-step workflow for implementing a single ticket during `/drive`.

## Steps

### 1. Read and Understand the Ticket

- Read the ticket file to understand requirements
- Identify key files mentioned in the ticket
- Understand the implementation steps outlined

### 2. Implement the Ticket

- Follow the implementation steps in the ticket
- Use existing patterns and conventions in the codebase
- Run type checks (per CLAUDE.md) to verify changes
- Fix any type errors or test failures before proceeding

### 3. Ask User to Review Implementation

**STOP and ask the user to review the implementation before proceeding.**

Show ticket context to help user understand what they're reviewing:

- Display the ticket title (H1 heading from ticket file)
- Include a brief summary (first 1-2 sentences from Overview section)
- Show a summary of changes made

Use AskUserQuestion tool to confirm:

- "Approve" - implementation is correct, proceed to commit and continue to next ticket
- "Approve and stop" - implementation is correct, commit this ticket but stop driving
- "Abandon" - write failure analysis, discard changes, and continue to next ticket

**Do NOT proceed to commit until user explicitly approves.**

#### Approval Prompt Format

```
**Ticket: <Title from H1>**
<Summary from Overview section - first 1-2 sentences>

Implementation complete. Changes made:
- <Change 1>
- <Change 2>

Do you approve this implementation?
[Approve / Approve and stop / Abandon]
```

### 4. Update Effort and Write Final Report

After user approves:

1. **Update the `effort` field** in the ticket's YAML frontmatter with actual time spent in numeric hours. Valid values: `0.1h`, `0.25h`, `0.5h`, `1h`, `2h`, `4h`. Do NOT use t-shirt sizes (XS, S, M) or minutes (10m). Estimate based on implementation complexity.

2. **Append a "## Final Report" section** to the ticket file.

**If no insights discovered:**

```markdown
## Final Report

Development completed as planned.
```

**If meaningful insights were discovered during implementation:**

Add a "### Discovered Insights" subsection capturing learnings that help future developers understand the codebase:

```markdown
## Final Report

Development completed as planned.

### Discovered Insights

- **Insight**: <what was discovered>
  **Context**: <why this matters for understanding the codebase>
```

#### What Makes a Good Insight

Include insights that fall into these categories:

- **Architectural patterns**: Hidden design decisions or conventions not documented elsewhere
- **Code relationships**: Non-obvious dependencies or coupling between components
- **Historical context**: Why something exists in its current form (discovered via git blame or comments)
- **Edge cases**: Gotchas or surprising behaviors that future developers should know

#### Insight Guidelines

- Keep insights actionable and specific, not vague observations
- Insights should benefit someone reading the ticket months later
- Don't duplicate information already in the ticket's Overview or Implementation Steps
- If no meaningful insights were discovered, omit the subsection entirely

This creates a historical record of decisions and discoveries made during implementation.

### 5. Commit and Archive Using Skill

After writing the final report, run the archive-ticket skill which handles everything:

```bash
bash .claude/skills/archive-ticket/sh/archive.sh \
  <ticket-path> \
  "<commit-message>" \
  <repo-url> \
  "<description>" \
  [modified-files...]
```

**CRITICAL**: The archive script is the ONLY way to archive tickets. It handles everything automatically.

#### Prohibited Actions

NEVER do any of the following:

- NEVER use `mv` or `git mv` to move ticket files
- NEVER create directories like `done/`, `completed/`, `finished/`, or any custom archive location
- NEVER manually update CHANGELOG files
- NEVER manually set `commit_hash` or `category` frontmatter fields

The ONLY valid archive location is `.workaholic/tickets/archive/<branch>/`. The script determines the branch name and creates the directory. Any manual file operations will result in incorrect archive structure.

**Note**: The archive script uses `git add -A`, which includes:

- All implementation changes
- The archived ticket file
- Any uncommitted ticket files in `.workaholic/tickets/todo/`
- CHANGELOG updates

This means newly created tickets are automatically included in drive commits.

### After Committing

- If user selected "Approve": automatically proceed to the next ticket without asking for confirmation
- If user selected "Approve and stop": stop driving and report how many tickets remain (e.g., "Stopped. 2 tickets remaining in queue.")

### If User Selects "Abandon"

When the user selects "Abandon", do NOT commit implementation changes. Instead:

1. **Discard implementation changes**: Run `git restore .` to revert all uncommitted changes
2. **Append Failure Analysis section** to the ticket file:

   ```markdown
   ## Failure Analysis

   ### What Was Attempted
   - <Brief description of the implementation approach>

   ### Why It Failed
   - <Reason the implementation didn't work or was abandoned>

   ### Insights for Future Attempts
   - <Learnings that could help if this is reattempted>
   ```

3. **Move ticket to fail directory**:
   ```bash
   mkdir -p .workaholic/tickets/fail
   mv <ticket-path> .workaholic/tickets/fail/
   ```
4. **Commit the ticket move** to preserve the failure analysis in git history:
   ```bash
   git add .workaholic/tickets/
   git commit -m "Abandon: <ticket-title>"
   ```
5. **Continue to next ticket** without asking for confirmation

This allows users to abandon a failed implementation attempt while preserving insights from the attempt for future reference.

## Commit Message Rules

- NO prefixes (no `[feat]`, `fix:`, etc.)
- Start with present-tense verb (Add, Update, Fix, Remove, Refactor)
- Focus on **WHAT** changed in the title
- Keep title concise (50 chars or less)

## Description Rules

- 1-2 sentences explaining the motivation behind the change
- Capture the "why" from the ticket's Overview section
- This appears in CHANGELOG and helps generate meaningful PR descriptions
