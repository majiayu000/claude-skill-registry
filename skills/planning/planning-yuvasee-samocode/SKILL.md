---
name: planning
description: Create implementation plans with phase management.
---

# Planning

Creates detailed implementation plans with phases, stored within the session folder.

## Requirements

- Active session must exist (session path in working memory)
- If no active session: **STOP and ask user** for session path

## Execution

**Session path:** [SESSION_PATH from working memory]
**Context:** $ARGUMENTS

### Steps

1. **Gather context:**
   - Read recent dive/task documents from session
   - Review project documentation if available
   - Understand current codebase state

2. **Create plan file:**
   - Location: `[SESSION_PATH]/[TIMESTAMP_FILE]-plan-[plan-slug].md`

   **Phase design principles:**
   - Each phase is executed as a **single samocode iteration** — keep phases bite-sized and independently completable
   - 1–3 focused steps per phase (not counting lint/typecheck)
   - Split by logical boundary: one file/module/concern per phase when possible
   - Prefer more small phases over fewer large ones

   Structure:
   ```markdown
   # Plan: [Title]
   Created: [TIMESTAMP_LOG]

   ## Task Definition
   [Concise summary]

   ## Requirements
   - [ ] [Requirement 1]
   - [ ] [Requirement 2]

   ## Context
   [Key files, current state, constraints]

   ## Implementation Phases

   ### Phase 1: [Name]
   - [ ] [Step]
   - [ ] [Step]
   - [ ] Run pyright/ruff or tsc - fix errors

   ### Phase 2: [Name]
   - [ ] [Step]
   - [ ] [Step]
   - [ ] Run pyright/ruff or tsc - fix errors

   ### Phase 3: Testing
   - [ ] [Test case]
   - [ ] Final checks

   ## Notes
   [Important context from task definition]
   ```

3. **Update session:**
   - Edit `[SESSION_PATH]/_overview.md`:
     - Add to Flow Log: `- [TIMESTAMP_ITERATION] Plan created -> [filename].md`
     - Add to Plans: `- [filename].md - [brief description]`
     - Add to Files: `- [filename].md - Plan: [brief description]`
   - Commit (if git repo): `cd [SESSION_DIR] && git add . && git commit -m "Plan: [title]"`

4. **Report back:** Plan summary and file location
