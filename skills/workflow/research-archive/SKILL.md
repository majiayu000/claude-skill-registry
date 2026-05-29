---
name: research:archive
description: Archive completed research. Moves the research to archive/ and updates its status.
---

# Research Archive Skill

Archive a completed research plan after findings have been synthesized and consumed.

## Process

1. **Identify the research to archive:**
   - If the user specifies a number/name, use that
   - Otherwise, scan `research/NNNN-*/` (exclude `archive/` and unnumbered legacy directories) for research with status `"synthesized"` in `.research-state.json`
   - If multiple candidates, ask user to choose

2. **Verify completion:**
   - Check that `synthesis.md` exists
   - Check that findings files exist for each question
   - If synthesis is missing, ask: "Research has no synthesis yet. Archive anyway?"

3. **Update research files:**

   **Update `research-plan.md` status:**
   ```markdown
   ## Status: ARCHIVED

   **Archived:** YYYY-MM-DD
   ```

   **Update `.research-state.json`:**
   ```json
   {
     "status": "archived",
     "archived_at": "2026-01-28T10:30:00Z",
     "updated_at": "2026-01-28T10:30:00Z",
     ...existing fields...
   }
   ```

4. **Move to archive:**
   ```bash
   mv research/NNNN-topic-name research/archive/
   ```

5. **Confirm to user:**
   ```
   **Archived:** `research/archive/NNNN-topic-name/`
   **Status:** ARCHIVED
   **Questions:** N answered
   **Synthesis:** Yes/No
   **Archived:** YYYY-MM-DD
   ```

## Notes

- Research referenced by implementation plans (via relative paths like `../../research/NNNN-topic/`) will have broken links after archiving. The archive path becomes `../../research/archive/NNNN-topic/`. Consider this before archiving research that active plans reference.
- Unnumbered legacy research directories (e.g., `dagre-layout/`, `edge-routing-deep-dive/`) should not be archived through this skill — they predate the numbering convention.
