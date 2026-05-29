---
name: research:cancel
description: Cancel a research plan. Updates status to CANCELLED and moves to archive/. Use when research is no longer needed or has been superseded.
---

# Research Cancel Skill

Cancel a research plan that is no longer being pursued.

## Process

1. **Identify the research to cancel:**
   - If the user specifies a number/name, use that
   - Otherwise, list active research plans and ask user to choose
   - Never auto-cancel — always require explicit identification

2. **Ask for cancellation reason** (optional but recommended):
   - "Why is this research being cancelled?"
   - Common reasons: superseded by other research, no longer relevant, answered by other means
   - If superseded, ask what supersedes it

3. **Update research files:**

   **Update `research-plan.md` status header:**
   ```markdown
   ## Status: CANCELLED

   **Cancelled:** YYYY-MM-DD
   **Reason:** [User's reason, if provided]
   **Superseded by:** [Reference, if applicable]
   ```

   **Update `.research-state.json`:**
   ```json
   {
     "status": "cancelled",
     "cancelled_at": "2026-01-28T10:30:00Z",
     "updated_at": "2026-01-28T10:30:00Z",
     "cancellation_reason": "No longer needed",
     "superseded_by": null,
     ...existing fields...
   }
   ```

4. **Move to archive:**
   ```bash
   mv research/NNNN-topic-name research/archive/
   ```

5. **Confirm to user:**
   ```
   **Cancelled:** `research/archive/NNNN-topic-name/`
   **Status:** CANCELLED
   **Reason:** [reason]
   **Questions answered:** X/Y at time of cancellation
   ```

## Notes

- If research agents are still running in the background, note this to the user. The agents will complete but their findings won't be synthesized.
- Partial findings files are preserved in the archive for potential future reference.
