---
name: log-debug-issue
description: Log problems, bugs, and debugging processes with solutions. Use when encountering issues during development, debugging problems, or documenting solutions for future reference. Maintains DEBUG_LOG.md with structured problem-solution entries.
---

# Debug Logger

Record problems, bugs, and debugging processes with structured solutions for future reference.

## When to Use

Use this skill when:
- Encountering a bug or error during development
- Debugging a complex issue that requires investigation
- Finding a solution to a problem that might recur
- Documenting workarounds or temporary fixes
- Tracking issues that need follow-up

## Workflow

### Step 1: Identify Problem
When an issue occurs, document it immediately:

**Key information to capture:**
- **Date & Time:** When did the issue occur?
- **Context:** What were you trying to do?
- **Symptoms:** What went wrong? Error messages, unexpected behavior
- **Environment:** OS, Python version, package versions, relevant configuration
- **Reproduction Steps:** How to reproduce the issue

### Step 2: Investigate & Debug
Record the debugging process:

**Document:**
- **Hypotheses:** What you think might be causing the issue
- **Tests/Experiments:** What you tried to diagnose the problem
- **Findings:** What you discovered during investigation
- **Resources:** Documentation consulted, forum posts, etc.

### Step 3: Solution & Fix
When a solution is found:

**Record:**
- **Root Cause:** The actual cause of the problem
- **Solution:** The fix implemented
- **Workaround:** Temporary fixes if permanent solution not yet available
- **Prevention:** How to prevent similar issues in future
- **Validation:** How you verified the fix works

### Step 4: Update DEBUG_LOG.md
Add the problem-solution entry to the debug log file (`.claude/DEBUG_LOG.md`):

## DEBUG_LOG.md Structure

```markdown
# Debug Log - VRP Toolkit Project

*Structured record of problems, bugs, and solutions encountered during development.*

## Active Issues 🚧
*Issues not yet resolved or needing follow-up.*

### [Issue Title]
**Date Opened:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Status:** Investigating / Needs Fix / Waiting

**Problem:**
[Brief description of the problem]

**Symptoms:**
- [Error messages]
- [Unexpected behavior]

**Current Investigation:**
- [Hypotheses being tested]
- [Tests performed]

**Next Steps:**
1. [Action item 1]
2. [Action item 2]

---

## Resolved Issues ✅
*Problems that have been solved.*

### [Issue Title]
**Date Opened:** YYYY-MM-DD
**Date Resolved:** YYYY-MM-DD
**Resolution Time:** [e.g., 2 hours]

**Problem:**
[Brief description of the problem]

**Symptoms:**
- [Error messages]
- [Unexpected behavior]

**Root Cause:**
[The underlying cause of the issue]

**Solution:**
[The fix implemented]

**Prevention:**
[How to prevent similar issues]

**Lessons Learned:**
[Key takeaways from this debugging process]

---

## Common Patterns & Solutions 🔧
*Recurring issues and their solutions for quick reference.*

### Pattern 1: [Pattern Name]
**Symptoms:** [Common symptoms]
**Cause:** [Typical cause]
**Solution:** [Standard solution]
**Example:** [Link to specific resolved issue]

### Pattern 2: [Pattern Name]
**Symptoms:** [Common symptoms]
**Cause:** [Typical cause]
**Solution:** [Standard solution]
**Example:** [Link to specific resolved issue]
```

## Entry Templates

### New Issue Template
```markdown
### [Brief descriptive title]
**Date Opened:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Status:** Investigating

**Problem:**
[What were you trying to do when the issue occurred?]

**Symptoms:**
- [Specific error messages with tracebacks]
- [Unexpected output or behavior]
- [What works vs what doesn't]

**Environment:**
- OS: [Operating system]
- Python: [Python version]
- Packages: [Relevant package versions]
- Context: [What part of the project]

**Reproduction Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Current Investigation:**
- **Hypothesis 1:** [What you think might be wrong]
  - Test: [What test you ran]
  - Result: [What happened]

**Next Steps:**
1. [Immediate next action]
2. [Longer-term investigation if needed]

---
```

### Resolved Issue Template
```markdown
### [Brief descriptive title]
**Date Opened:** YYYY-MM-DD
**Date Resolved:** YYYY-MM-DD
**Resolution Time:** [e.g., 45 minutes]

**Problem:**
[What was the problem?]

**Symptoms:**
- [Error messages]
- [Unexpected behavior]

**Root Cause:**
[The actual underlying cause - be specific]
- [Technical details]
- [Why it wasn't obvious]

**Solution:**
[The fix that worked]
- [Code changes made]
- [Configuration updates]
- [Workarounds implemented]

**Prevention:**
[How to prevent this issue in future]
- [Code patterns to avoid]
- [Tests to add]
- [Documentation to update]

**Lessons Learned:**
[Key insights from debugging]
- [What made debugging difficult/easy]
- [Tools or techniques that helped]
- [What to try first next time]

**Files Modified:**
- [path/to/file.py]
- [path/to/config.yaml]

---
```

## Integration with Other Skills

**update-task-board:** Active issues in DEBUG_LOG.md become tasks in CLAUDE.md "Blockers" or "In Progress" sections.

**git-log:** When fixing bugs documented in DEBUG_LOG.md, reference the issue in commit messages.

**build-session-context:** Check DEBUG_LOG.md for active issues when starting work.

**update-migration-log:** Document debugging efforts as part of migration or task completion.

## Usage Examples

### Example 1: Import Error
**Trigger:** `ImportError: cannot import name 'RealMap' from 'vrp_toolkit.data'`

**Debug process:**
1. Check `__init__.py` exports
2. Verify file paths
3. Check for circular imports
4. Find missing export and fix

**Entry:** Document the import error, investigation steps, and solution (adding missing export to `__init__.py`).

### Example 2: Algorithm Bug
**Trigger:** ALNS algorithm produces invalid routes

**Debug process:**
1. Check initial solution generation
2. Verify operator logic
3. Add debug prints
4. Find off-by-one error in indexing

**Entry:** Document the bug, debugging steps, and fix (correcting index calculation).

### Example 3: Dependency Issue
**Trigger:** Matplotlib fails to import on Windows

**Debug process:**
1. Check matplotlib version
2. Check backend configuration
3. Find Windows-specific issue
4. Implement workaround

**Entry:** Document the platform-specific issue and workaround.

## Maintenance Guidelines

### File Organization
- Keep "Active Issues" section at top for visibility
- Move resolved issues from "Active" to "Resolved"
- Regularly review "Common Patterns" and update based on new issues
- Use consistent formatting for easy scanning

### Status Tracking
- **Investigating:** Issue identified, debugging in progress
- **Needs Fix:** Root cause identified, fix needed
- **Waiting:** Blocked on external factor (e.g., dependency update)
- **Resolved:** Fix implemented and verified

### Regular Review
- Weekly: Review active issues, update status
- Monthly: Archive old resolved issues if file gets too large
- Project milestones: Summarize key learnings from debug log

## Automation Notes

When AI uses this skill, it should:
1. Create DEBUG_LOG.md if it doesn't exist
2. Add new issues to "Active Issues" section
3. Update issue status as investigation progresses
4. Move resolved issues to "Resolved" section
5. Extract patterns for "Common Patterns" section
6. Reference issues in commit messages when fixes are committed