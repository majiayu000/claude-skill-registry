---
name: managing-handoffs
description: Create, update, and archive handoffs with proper metadata and verification
---

# Managing Handoffs

## Overview

Manage handoff documents through their full lifecycle: create → work → resolve → archive.

**Core principle:** Evidence-based verification before closing handoffs.

**Announce at start:** "I'm using the managing-handoffs skill to [operation]."

## Handoff Metadata Template

Every handoff uses this YAML frontmatter:

```yaml
---
type: handoff
status: active              # active | resolved | archived
created: YYYY-MM-DD
resolved_date: null
archived_date: null
related_sessions: []
related_plans: []
verification:
  implementation_complete: false
  documentation_exists: false
  tests_passing: false
  commits_made: false
---
```

## Operations

### Create Handoff

**When:** Starting new feature work or documenting incomplete work for handoff.

**Process:**

1. **Get information:**
   - Title (brief, descriptive)
   - Description (what needs to be done)
   - Related plans (implementation plan files)

2. **Generate filename:**
   ```python
   from datetime import date
   today = date.today().strftime('%Y-%m-%d')
   slug = title.lower().replace(' ', '-').replace('_', '-')
   filename = f"{today}-{slug}-handoff.md"
   ```

3. **Create file at:** `/docs/handoffs/current/{filename}`

4. **Content structure:**
   ```markdown
   ---
   type: handoff
   status: active
   created: {today}
   resolved_date: null
   archived_date: null
   related_sessions: []
   related_plans: [{plan_paths}]
   verification:
     implementation_complete: false
     documentation_exists: false
     tests_passing: false
     commits_made: false
   ---

   # {Title}

   **Created:** {today}
   **Status:** 🔴 Active

   ## Context

   {description}

   ## Tasks

   - [ ] {task 1}
   - [ ] {task 2}
   - [ ] {task 3}

   ## Implementation Notes

   [To be filled during work]

   ## Completion Criteria

   - [ ] All tasks complete
   - [ ] Code committed to git
   - [ ] Documentation updated (guides/summaries)
   - [ ] Tests passing (if applicable)
   - [ ] Session documented
   ```

5. **Commit:**
   ```bash
   git add docs/handoffs/current/{filename}
   git commit -m "docs: create handoff for {title}"
   ```

---

### Close Handoff

**When:** Work is complete and ready to mark resolved.

**Process:**

1. **Load handoff file**
   - Read YAML frontmatter
   - Verify status is 'active'

2. **Run verification checklist:**

   **Implementation Complete:**
   ```bash
   git log --oneline --since="$(yq -r .created handoff.md)" --grep="feat\\|fix\\|refactor"
   ```
   - Must have commits related to this work
   - Prompt: "Show me the commits for this work"

   **Documentation Exists:**
   - Check if guide/summary was created or updated
   - Scan git log for docs/ changes
   - Prompt: "What documentation was created/updated?"

   **Tests Passing (if applicable):**
   ```bash
   pytest tests/ -v
   ```
   - Run relevant tests
   - Must show 0 failures
   - Uses @superpowers:verification-before-completion

   **Commits Made:**
   - Verify git log shows activity
   - Confirm commits reference the work

3. **Verify all checklist items:**
   - If ANY item fails → STOP, cannot close
   - Report what's missing
   - Ask user to complete before closing

4. **Update metadata:**
   ```yaml
   status: resolved
   resolved_date: {today}
   related_sessions: [{session_files}]
   verification:
     implementation_complete: true
     documentation_exists: true
     tests_passing: true  # or N/A
     commits_made: true
   ```

5. **Update status in document:**
   - Change **Status:** 🔴 Active → 🟢 Resolved
   - Add completion date

6. **Move to resolved:**
   ```bash
   mv docs/handoffs/current/{filename} docs/handoffs/resolved/
   ```

7. **Commit:**
   ```bash
   git add docs/handoffs/
   git commit -m "docs: resolve handoff - {title}

   Verification complete:
   - Implementation: {commits}
   - Documentation: {docs}
   - Tests: {status}
   "
   ```

---

### Archive Handoff

**When:** Handoff has been resolved and is ready for archival.

**Process:**

1. **Verify handoff is resolved:**
   - Check metadata: status must be 'resolved'
   - Must be in /docs/handoffs/resolved/

2. **Add RESOLVED- prefix:**
   ```bash
   mv docs/handoffs/resolved/{filename} \
      docs/handoffs/archive/RESOLVED-{filename}
   ```

3. **Update metadata:**
   ```yaml
   status: archived
   archived_date: {today}
   ```

4. **Commit:**
   ```bash
   git add docs/handoffs/archive/
   git commit -m "docs: archive resolved handoff - {title}"
   ```

---

### List Handoffs

**When:** Checking project status, finding active work.

**Process:**

1. **Scan handoffs/current/:**
   ```bash
   find docs/handoffs/current -name "*.md" -type f
   ```

2. **For each handoff:**
   - Extract metadata (created date, title)
   - Calculate age (days since creation)
   - Get status

3. **Output format:**
   ```
   Active Handoffs (3):

   1. import-coverage-completion
      Created: 2025-11-13 (2 days ago)
      File: docs/handoffs/current/2025-11-13-import-coverage-completion-handoff.md

   2. formula-correction-audit
      Created: 2025-11-13 (2 days ago)
      File: docs/handoffs/current/2025-11-13-formula-correction-audit-handoff.md

   3. web-ui-phase-2
      Created: 2025-11-10 (5 days ago)
      File: docs/handoffs/current/2025-11-10-web-ui-phase-2-handoff.md
   ```

---

## Integration

**Uses:**
- `superpowers:verification-before-completion` - Evidence-based verification

**Used by:**
- `project-status` skill - Shows active handoffs
- Development workflows - Handoff creation and closure

---

## Common Mistakes

**Closing without verification:**
- **Problem:** Mark resolved without checking verification items
- **Fix:** Always run full verification checklist

**Missing documentation:**
- **Problem:** Close handoff without updating guides
- **Fix:** Require documentation_exists = true

**Archiving active handoffs:**
- **Problem:** Try to archive without resolving first
- **Fix:** Enforce status transitions (active → resolved → archived)

---

## Red Flags

**Never:**
- Close handoff without verification
- Skip test verification if tests exist
- Archive directly from active status
- Modify archived handoffs

**Always:**
- Run verification checklist
- Link related sessions and plans
- Update status atomically
- Commit each state transition
