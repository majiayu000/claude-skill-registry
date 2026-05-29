---
name: task-definition
description: Interactive task definition with Q&A and documentation.
---

# Task Definition

Defines tasks through interactive Q&A, documenting requirements and decisions.

## Requirements

- Active session must exist (session path in working memory)
- If no active session: **STOP and ask user** for session path

## Execution

**Session path:** [SESSION_PATH from working memory]
**Task:** $ARGUMENTS

### Steps

1. **Analyze the task:**
   - Review recent dive/task documents in the session for context
   - Check project docs for related documentation
   - Understand scope and implications

2. **Interactive clarification:**
   - Identify ambiguities, edge cases, implementation options
   - Check if `[SESSION_PATH]/_qa.md` exists with answers from previous run
   - If `_qa.md` exists and has answers: read them and continue to step 4
   - If questions needed, write to `[SESSION_PATH]/_qa.md`:
     ```markdown
     # Q&A: [task description]
     Status: waiting

     ## Questions

     ### Q1: [Clear question]
     A) [option]
     B) [option]
     C) [option]
     **Suggestion:** [recommended option] - [justification]
     **Answer:** _waiting_

     ### Q2: [Clear question]
     A) [option]
     B) [option]
     **Suggestion:** [recommended option] - [justification]
     **Answer:** _waiting_
     ```
   - **IMPORTANT:** Do NOT use checkbox format `- [ ]`. Use lettered options (A, B, C) one per line.
   - Each question MUST have a suggestion with clear justification
   - Present questions to user formatted as:
     ```
     Q1: [Clear question]
     A) [option]
     B) [option]
     C) [option]
     Suggestion: [recommended] - [why]
     ```
   - If waiting for answers: "Questions written to _qa.md. Please answer and re-run /task to continue."
   - Continue asking until all ambiguities resolved
   - When no more questions: "No more questions, we can move on!"
   - DO NOT start any code edits - wait for explicit instruction

3. **Document the task (after Q&A complete):**
   - Create file: `[SESSION_PATH]/[TIMESTAMP_FILE]-task-[task-slug].md`

   ```markdown
   # Task: [title]
   Date: [TIMESTAMP_LOG]

   ## Description
   [What needs to be accomplished]

   ## Requirements
   [Bullet list]

   ## Clarifications

   ### [Topic]
   **Q:** [question]
   **A:** [answer/decision]
   **Rationale:** [why]

   ## Edge Cases
   [Things to watch for]

   ## Success Criteria
   [How we know it's done]
   ```

4. **Update session:**
   - Edit `[SESSION_PATH]/_overview.md`:
     - Add to Flow Log: `- [TIMESTAMP_ITERATION] Task defined: [title] -> [filename].md`
     - Add to Files: `- [filename].md - Task: [title]`
   - Delete `_qa.md` if it exists
   - Commit (if git repo): `cd [SESSION_DIR] && git add . && git commit -m "Task: [title]"`

5. **Suggest next steps:** /create-plan, /do, /dop2
