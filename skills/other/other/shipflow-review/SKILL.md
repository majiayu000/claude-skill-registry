---
name: shipflow-review
description: Review recent work, generate summary, update docs, and plan next session
disable-model-invocation: false
argument-hint: [optional: daily, weekly, sprint, release]
---

## Context

- Current directory: !`pwd`
- **Master TASKS.md** (multi-project dashboard): !`cat /home/claude/shipflow_data/TASKS.md 2>/dev/null || echo "No master TASKS.md"`
- Local TASKS.md (if exists): !`cat TASKS.md 2>/dev/null || echo "No local TASKS.md"`
- Recent commits (last 10): !`git log --oneline --date=short --pretty=format:"%h %ad %s" -10 2>/dev/null || echo "Not a git repo"`
- Files changed recently: !`git diff --name-status HEAD~5..HEAD 2>/dev/null || echo "N/A"`
- Current branch: !`git branch --show-current 2>/dev/null`
- Git status: !`git status --short 2>/dev/null`
- CHANGELOG.md (last 30 lines): !`tail -30 CHANGELOG.md 2>/dev/null || echo "No CHANGELOG.md"`
- Workspace CLAUDE.md: !`head -20 /home/claude/CLAUDE.md 2>/dev/null || echo "N/A"`

## Multi-project tracking system

**CRITICAL**: This workspace tracks 12 projects from a single master file at `/home/claude/shipflow_data/TASKS.md`.

- **Always update `/home/claude/shipflow_data/TASKS.md`** as part of the review — check off completed tasks, update the Dashboard table, and refresh the "Last updated" date
- When reviewing from a sub-project directory, also consider the master-level cross-project concerns
- The review summary should reference which project(s) were worked on and how the master Dashboard changed
- When planning next session, suggest tasks from the master file's highest-priority items across all projects

## Your task

Conduct a comprehensive review of recent work and prepare for the next session.

### Workspace root detection

If the current directory has no `.git` directory (not a git repo) BUT contains multiple project subdirectories — you are at the **workspace root**. Use **AskUserQuestion**:
- Question: "Which project(s) should I review?"
- `multiSelect: true`
- One option per project: label = project name, description = recent commit count (run `git -C [path] log --oneline --since="7 days" 2>/dev/null | wc -l` for each)
- Only list projects with recent activity

### Steps

1. **Determine review scope** — if `$ARGUMENTS` is empty, use **AskUserQuestion**:
   - Question: "What time scope for this review?"
   - `multiSelect: false`
   - Options:
     - **Daily** — "Last 24 hours of work"
     - **Weekly** — "Last 7 days of commits" (Recommended)
     - **Sprint** — "Since last sprint start (~2 weeks)"
     - **Release** — "All changes since last release"

   If `$ARGUMENTS` is provided (daily/weekly/sprint/release), skip the prompt and use it directly.

2. **Analyze what was accomplished**:
   - Review completed tasks in TASKS.md
   - Examine git commits for actual changes
   - Identify files modified (from git diff)
   - Note any deployed changes or releases

3. **Assess work quality**:
   - Are there tests for new features?
   - Is documentation updated?
   - Are there any quick fixes that need proper solutions?
   - Any technical debt introduced?
   - Security or performance concerns?

4. **Update CHANGELOG.md**:
   - Add new section for this review period if needed
   - Use semantic versioning or date-based sections
   - Categorize changes:
     ```markdown
     ## [Version/Date]

     ### Added
     - New features

     ### Changed
     - Updates to existing features

     ### Fixed
     - Bug fixes

     ### Security
     - Security updates

     ### Deprecated
     - Features marked for removal
     ```
   - Keep entries user-focused (what changed, why it matters)

5. **Generate work summary**:
   - **Completed**: What was finished (with evidence)
   - **In Progress**: What's partially done
   - **Blocked**: What's stuck and why
   - **Learned**: Key insights or discoveries
   - **Metrics**: Commits, files changed, tests added, etc.

6. **Plan next session**:
   - Review remaining tasks in TASKS.md
   - Identify what should be prioritized next
   - Note any blockers that need addressing
   - Suggest 1-3 tasks for immediate focus
   - Flag anything that needs discussion/decisions

7. **Update TASKS.md**:
   - Archive completed tasks to a "Recently Completed" section
   - Add completion dates
   - Move old completed tasks to CHANGELOG or separate archive
   - Ensure In Progress and Todo sections are current

8. **Create review report**:
   - Save to `REVIEW-[DATE].md` in project root or docs folder
   - Include all sections above
   - Add links to relevant commits, PRs, issues
   - Make it readable for stakeholders (team, future you)

### Important

- **Always update the master `/home/claude/shipflow_data/TASKS.md`** — check off completed tasks, update Dashboard statuses, refresh "Last updated" date
- Be honest about progress - if less was done than planned, say why
- Focus on outcomes, not just activity
- Highlight wins and learnings
- Use metrics to show progress (# of tests, coverage, performance improvements)
- Flag technical debt clearly
- Make next steps actionable and specific
- Keep review concise but comprehensive
- Update CHANGELOG.md for user-facing changes only
- Archive old completed tasks to keep TASKS.md manageable
- Suggest process improvements if patterns emerge (e.g., always missing tests)
- When planning next session, pull top priorities from the master Dashboard across all 12 projects
