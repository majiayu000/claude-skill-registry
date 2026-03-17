---
name: documenting-sessions
description: Create consistent session summary documents with automatic linking and style checking
---

# Documenting Sessions

## Overview

Create professional session summary documents that track development work, link related artifacts, and apply clear writing standards.

**Core principle:** Evidence-based session summaries with verifiable commit history and artifact links.

**Announce at start:** "I'm using the documenting-sessions skill to [operation]."

## Session Document Template

Every session document uses this structure:

```markdown
# Session YYYY-MM-DD: [Title]

**Date:** YYYY-MM-DD
**Status:** ✅ COMPLETE | ⚠️ IN PROGRESS | ❌ BLOCKED
**Related Handoffs:** [Links to handoff files]
**Related Plans:** [Links to plan files]
**Commits:** [N commits, branch info]

---

## Executive Summary
[2-3 sentences: what was accomplished]

## Work Completed
- Task 1
- Task 2
- Task 3

## Technical Details
[Implementation notes, decisions made]

## Next Steps
[What remains, blockers, follow-ups]

## Files Changed
[Key files modified/created]
```

## Operations

### Create Session

**When:** Starting a development session or documenting completed work.

**Process:**

1. **Get information:**
   - Title (brief, descriptive)
   - Status (COMPLETE, IN PROGRESS, BLOCKED)
   - Related handoffs (paths to handoff files)
   - Related plans (paths to plan files)

2. **Generate filename:**
   ```python
   from datetime import date
   today = date.today().strftime('%Y-%m-%d')
   slug = title.lower().replace(' ', '-').replace('_', '-')
   filename = f"SESSION-{today}-{slug}.md"
   ```

3. **Create file at:** `/docs/sessions/{filename}`

4. **Content structure:**
   ```markdown
   # Session {today}: {Title}

   **Date:** {today}
   **Status:** {status_emoji} {STATUS}
   **Related Handoffs:** {handoff_links}
   **Related Plans:** {plan_links}
   **Commits:** [To be updated]

   ---

   ## Executive Summary

   [Summarize main accomplishment in 2-3 sentences]

   ## Work Completed

   - [Task 1]
   - [Task 2]
   - [Task 3]

   ## Technical Details

   [Implementation notes, architectural decisions, design choices]

   ## Next Steps

   [Remaining work, blockers, follow-up tasks]

   ## Files Changed

   [List key files that were created or modified]
   ```

5. **Status emoji mapping:**
   - ✅ COMPLETE
   - ⚠️ IN PROGRESS
   - ❌ BLOCKED

6. **Commit:**
   ```bash
   git add docs/sessions/{filename}
   git commit -m "docs: create session summary for {title}"
   ```

---

### Update Session

**When:** Adding work items, updating status, or recording commits.

**Process:**

1. **Load session file**
   - Read existing content
   - Identify sections to update

2. **Update work items:**
   - Add new items to "Work Completed" section
   - Use bullet points for each task/subtask
   - Be specific and actionable

3. **Update commit information:**
   ```bash
   # Count commits since session date
   SESSION_DATE=$(grep "^**Date:" session.md | cut -d' ' -f2)
   COMMITS=$(git log --oneline --since="$SESSION_DATE" | wc -l)
   BRANCH=$(git branch --show-current)

   # Update commits line
   **Commits:** $COMMITS commits to $BRANCH
   ```

4. **Update status if changed:**
   - Change status emoji and text
   - Add resolution notes if moving to COMPLETE

5. **Update next steps:**
   - Remove completed items
   - Add newly discovered tasks
   - Note any blockers

6. **Commit updates:**
   ```bash
   git add docs/sessions/{filename}
   git commit -m "docs: update session summary - {change description}"
   ```

---

### Link Artifacts

**When:** Completing session documentation and connecting to related work.

**Process:**

1. **Scan git commits for file changes:**
   ```bash
   SESSION_DATE=$(grep "^**Date:" session.md | cut -d' ' -f2)
   git diff --name-only $(git log --since="$SESSION_DATE" --format=%H | tail -1)..HEAD
   ```

2. **Identify related handoffs:**
   - Check for handoff files mentioned in commits
   - Search handoff content for references to this work
   - Look for handoffs with matching creation dates
   - Format: `[handoff-title](../handoffs/current/YYYY-MM-DD-handoff-name.md)`

3. **Find referenced plan files:**
   - Look for implementation plan references in commits
   - Check for plans in docs/plans/ matching the work
   - Format: `[plan-title](../plans/YYYY-MM-DD-plan-name.md)`

4. **Link to created/updated summaries:**
   - Identify new guides in docs/guides/
   - Identify new summaries in docs/summaries/
   - Add to "Files Changed" section with relative paths

5. **Verify all links:**
   - Test that linked files exist
   - Use relative paths from docs/sessions/
   - Example: `../handoffs/current/2025-11-14-feature-handoff.md`

---

### Apply Style

**When:** Finalizing session documentation before marking complete.

**Process:**

1. **Invoke writing-clearly-and-concisely skill:**
   ```
   Use writing-clearly-and-concisely skill to improve this session document:
   [session content]
   ```

2. **Apply Strunk's Elements of Style rules:**
   - Simplify complex sentences
   - Remove needless words
   - Use active voice
   - Make definite assertions
   - Avoid overstatement

3. **Specific checks:**
   - **Executive Summary:** 2-3 clear sentences maximum
   - **Work Completed:** Action verbs (Created, Implemented, Fixed, Added)
   - **Technical Details:** Specific, concrete information
   - **Next Steps:** Clear, actionable items

4. **Before/After comparison:**
   - Show improvements made
   - Explain why changes strengthen the writing
   - Ensure technical accuracy preserved

5. **Save polished version:**
   ```bash
   git add docs/sessions/{filename}
   git commit -m "docs: apply style improvements to session summary"
   ```

---

## Integration

**Uses:**
- `superpowers:verification-before-completion` - Evidence-based commit verification
- `writing-clearly-and-concisely` - Final polish and style checking

**Used by:**
- `managing-handoffs` skill - Sessions linked from handoff metadata
- `project-status` skill - Shows recent sessions on dashboard
- Development workflows - Document work sessions

---

## Session Types

### Implementation Session
Focus on feature development, code commits, and deliverables.

**Emphasize:**
- What was built
- Technical decisions
- Test coverage
- Files changed

### Investigation Session
Focus on analysis, research, and findings.

**Emphasize:**
- Questions investigated
- Findings and conclusions
- Data analyzed
- Recommendations

### Debugging Session
Focus on problem resolution and root cause analysis.

**Emphasize:**
- Problem description
- Investigation steps
- Root cause identified
- Solution implemented

### Planning Session
Focus on design decisions and planning artifacts created.

**Emphasize:**
- Design choices made
- Alternatives considered
- Plans created
- Next implementation steps

---

## Common Mistakes

**Vague summaries:**
- **Problem:** "Made progress on the feature"
- **Fix:** "Implemented database migration and 3 API endpoints for import status tracking"

**Missing evidence:**
- **Problem:** Claims work complete without commit references
- **Fix:** Link specific commits or provide git log output

**Broken links:**
- **Problem:** Absolute paths or incorrect relative paths
- **Fix:** Use relative paths from docs/sessions/ directory

**Weak writing:**
- **Problem:** Passive voice, wordiness, vague statements
- **Fix:** Apply writing-clearly-and-concisely skill

---

## Red Flags

**Never:**
- Claim work complete without verification
- Use absolute file paths in links
- Skip the executive summary
- Leave status as IN PROGRESS for finished work
- Mark COMPLETE with incomplete next steps

**Always:**
- Verify commits exist for claimed work
- Use relative paths for artifact links
- Write 2-3 sentence executive summary
- Update status to match reality
- Clear next steps or mark none remaining

---

## Examples

### Good Executive Summary
"Successfully implemented Import Status Dashboard MVP with full-stack integration from PostgreSQL views to React components. All 8 planned tasks delivered including database migrations, API endpoints, and UI components with real-time auto-refresh. Dashboard now provides visibility into import pipeline health and data quality metrics."

### Poor Executive Summary
"Worked on the dashboard. Made good progress. Still some things to do."

### Good Work Completed
- Created 4 PostgreSQL views for import quality metrics
- Implemented ImportStatusController with 4 filtered endpoints
- Built ImportStatusDashboard React component with TanStack Query
- Added sortable ImportHistoryTable with 8 columns
- Integrated SystemHealthIndicator and QualityMetricsCards

### Poor Work Completed
- Did database stuff
- Made some API changes
- Updated the frontend
- Fixed bugs

---

## Verification Checklist

Before marking session COMPLETE:

- [ ] Executive summary exists and is 2-3 sentences
- [ ] All work items listed with specific actions
- [ ] Technical details capture key decisions
- [ ] Commit count and branch info accurate
- [ ] Related handoffs linked (if applicable)
- [ ] Related plans linked (if applicable)
- [ ] Files changed section lists key files
- [ ] Next steps clear or marked as none
- [ ] Style applied using writing-clearly-and-concisely
- [ ] All links verified to work

---

## Quick Reference

**Create session:**
```bash
# From skill
Operation: Create session
Title: {descriptive-title}
Status: IN PROGRESS
```

**Update commit count:**
```bash
git log --oneline --since="YYYY-MM-DD" | wc -l
```

**Find related files:**
```bash
git diff --name-only $(git log --since="YYYY-MM-DD" --format=%H | tail -1)..HEAD
```

**Apply style:**
```bash
# Invoke writing-clearly-and-concisely skill on session document
```

**Verify links:**
```bash
# From docs/sessions/ directory
cd /path/to/project/docs/sessions
# Test each link
ls -la ../handoffs/current/YYYY-MM-DD-handoff.md
ls -la ../plans/YYYY-MM-DD-plan.md
```
