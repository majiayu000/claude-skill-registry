---
name: plan:cancel
description: Cancel an implementation plan. Moves the plan to archive/ with CANCELLED status. Use when a plan is superseded, abandoned, or no longer needed.
---

# Cancel Skill

Cancel an implementation plan that is no longer being pursued.

## Process

1. **Identify the plan to cancel:**
   - If the user specifies a plan number/name, use that
   - Otherwise, list in-progress plans and ask user to choose
   - Never auto-cancel - always require explicit identification

2. **Ask for cancellation reason** (optional but recommended):
   - "Why is this plan being cancelled?"
   - Common reasons: superseded by another plan, requirements changed, no longer needed
   - If superseded, ask which plan supersedes it

3. **Update plan files:**

   **Update `implementation-plan.md` status header:**
   ```markdown
   ## Status: ❌ CANCELLED

   **Cancelled:** YYYY-MM-DD
   **Reason:** [User's reason, if provided]
   **Superseded by:** NNNN-other-plan (if applicable)
   ```

   **Update `task-list.md` status:**
   ```markdown
   ## Status: ❌ CANCELLED
   ```

   **Update `.plan-state.json`:**
   ```json
   {
     "status": "cancelled",
     "cancelled_at": "2026-01-25T10:30:00Z",
     "updated_at": "2026-01-25T10:30:00Z",
     "cancellation_reason": "Superseded by 0005-dagre-module",
     "superseded_by": "0005-dagre-module",
     ...existing fields...
   }
   ```

4. **Move to archive:**
   ```bash
   mv plans/NNNN-feature-name plans/archive/
   ```

5. **Confirm to user:**
   ```
   **Cancelled:** `plans/archive/NNNN-feature-name/`
   **Status:** ❌ CANCELLED
   **Reason:** [reason]
   **Progress at cancellation:** X/Y tasks (Z%)
   ```

## Example Usage

### Cancel with reason
```
User: /plan:cancel 0004

Claude: Why is plan 0004-declaration-order-layout being cancelled?

User: Superseded by the dagre module plan

Claude: Is this superseded by plan 0005-dagre-module? (y/n)

User: yes

**Cancelled:** `plans/archive/0004-declaration-order-layout/`
**Status:** ❌ CANCELLED
**Reason:** Superseded by 0005-dagre-module
**Progress at cancellation:** 0/14 tasks (0%)
```

### Cancel already-archived plan (update status only)
```
User: /plan:cancel 0004

Claude: Plan 0004 is already in archive/ but shows status IN PROGRESS.
Update status to CANCELLED? (y/n)

User: yes

**Updated:** `plans/archive/0004-declaration-order-layout/`
**Status:** ❌ CANCELLED
```
