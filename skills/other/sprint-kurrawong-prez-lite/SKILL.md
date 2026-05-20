---
name: sprint
description: Kanban workflow and sprint management guidance for task lifecycle, file management, and documentation maintenance. Use when working with kanban tasks, moving tasks through workflow stages, sprint planning or retrospectives, archiving completed sprints, or updating kanban files.
---

# Kanban & Documentation Workflow

> Instructions for progressing tasks through the kanban system and maintaining project documentation

## On Start

When this skill is invoked, immediately perform these steps **in order**:

### Step 0: Clean Up Completed Sprint

1. Read `docs/kanban/1-backlog.md`
2. If the backlog contains items marked ✅ (completed) or 🔄/👀 with no matching in-progress/reviewing entry:
   a. Check `docs/kanban/5-done.md` and `docs/kanban/sprints.md` to verify these items are recorded there
   b. If all backlog items are ✅, the sprint is complete — close it:
      - Update `sprints.md`: mark the sprint ✅, add completed tasks list and velocity
      - Move done items to `docs/kanban/9-archive.md` if they belong to a previous sprint
      - **Clear `1-backlog.md`** completely (leave only the header)
      - **Clear `2-todo.md`** sprint section (leave only the header)
      - Update `dashboard.md` to reflect the closed sprint
   c. If only some items are ✅, leave them but flag for the user
3. If the backlog is clean (empty or only unmarked items), skip to Step 1

### Step 1: Process Intray

1. Read `docs/intray.md`
2. If the intray has items:
   a. Parse each item and present them back to the user as a numbered list with a proposed **backlog title** and **one-line summary** for each
   b. If any item is ambiguous or unclear, ask clarifying questions **before** adding to backlog — do not guess
   c. Once confirmed, append items to `docs/kanban/1-backlog.md` using the **standardised backlog format** (see below)
   d. Clear `docs/intray.md` (leave the file empty)
3. If the intray is empty, skip to Step 2

**Standardised Backlog Format** (one entry per item in `1-backlog.md`):
```
### [Short imperative title]
[One-line description of what needs to happen and why]
```

Example:
```
### Fix background label resolution on concept pages
Predicate labels like "altLabel" show raw camelCase instead of resolved human-readable labels from background vocabularies.
```

### Step 2: Read Board State

1. Read all kanban files: `1-backlog.md`, `2-todo.md`, `3-in-progress.md`, `5-reviewing.md`, `5-done.md`, `dashboard.md`, `sprints.md`
2. Assess current state across all columns

### Step 3: Present Status and Options

Show a **brief status summary** — one line per column that has items, skip empty columns.

Then, based on board state, present **actionable options** using `AskUserQuestion`:

- If items are **in progress**: offer "Continue [task name]" with a one-line summary of where it left off
- If items are **in review**: offer "Approve [task name]" to move to done
- If backlog has items but nothing is in progress: offer "Start [highest priority task]"
- Always include "Stop here" as an option

Do NOT wait for further instructions before reading files. Start processing immediately.

---

## Visual Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         TASK LIFECYCLE                          │
└─────────────────────────────────────────────────────────────────┘

    📋 BACKLOG (1-backlog.md)
        │  All unstarted tasks
        │
        ↓ [Prioritize: Add done criteria]
        │  Mark: 🎯 [Task Name]
        ↓

    📝 TODO (2-todo.md)
        │  Prioritized for current sprint
        │  Has done criteria defined
        │
        ↓ [Start work]
        │  Mark: 🔄 [Task Name] in backlog
        ↓

    ⚙️ IN PROGRESS (3-in-progress.md)
        │  Actively implementing
        │  Testing incrementally
        │
        ↓ [Complete implementation + docs + tests]
        │  Mark: 👀 [Task Name] in backlog
        ↓

    👀 REVIEWING (5-reviewing.md)
        │  Awaiting human manual review
        │  User verifies against done criteria
        │
        ↓ [User approves] OR [Request changes → back to In Progress]
        │  Mark: ✅ [Task Name] in backlog
        ↓

    ✅ DONE (5-done.md)
        │  Reviewed & complete
        │  Update sprints.md
        │
        ↓ [After sprint ends + ALL backlog complete]
        │
        ↓

    🗄️ ARCHIVE (9-archive.md)
        │  Historical completed tasks
        │  Previous sprint outcomes
        └
```

**Backlog Status Markers:**
- (no marker) = Not started
- 🎯 = Prioritized (in todo)
- 🔄 = In progress
- 👀 = In review
- ✅ = Complete

---

## Task Lifecycle

### 1. Prioritizing Tasks (Backlog → Todo)

**When Moving to Todo:**
1. Review all items in `1-backlog.md`
2. Select highest priority items for current sprint
3. Move selected tasks to `2-todo.md` with:
   - Priority ranking (High/Medium/Low)
   - Detailed requirements
   - Acceptance criteria
   - Done criteria (what "complete" means)
4. Keep task in backlog but mark it (e.g., `🎯` or `→ Todo`)
5. Update `sprints.md` with current sprint goals

**Prioritization Criteria:**
- User value / impact
- Dependencies (blockers for other work)
- Effort vs. benefit
- Security/critical fixes first

### 2. Starting a New Task (Todo → In Progress)

**From Todo:**
1. Read task details from `2-todo.md`
2. Mark in backlog as currently active: `🔄 [Task Name]`
3. Move task to `3-in-progress.md`
4. Update `dashboard.md` swim lanes to reflect status
5. Add start date and owner (if team context)

**Task Information Required:**
- Clear description of what needs to be done
- Expected deliverables (code, docs, analysis)
- Files that will be affected
- Done criteria (from todo phase)
- Testing instructions (if applicable)

### 3. During Task Execution (In Progress)

**Code Changes:**
- Make focused changes related to the task
- Avoid scope creep - stick to the task description
- Test changes incrementally
- Build successfully before moving to review

**If Issues Arise:**
- Document the problem clearly
- Try alternative approaches
- Ask user for clarification if blocked
- Update task notes in `3-in-progress.md` with findings

### 4. Moving to Review (In Progress → Reviewing)

**Before Moving to Review:**
1. ✅ All code changes tested and working
2. ✅ Build passes (`pnpm build` successful)
3. ✅ Relevant documentation updated
4. ✅ Testing instructions provided
5. ✅ Done criteria met (from todo phase)

**Move to Reviewing:**
1. Move task from `3-in-progress.md` to `5-reviewing.md`
2. Update dashboard swim lanes
3. Keep backlog item marked as in-review: `👀 [Task Name]`
4. Include in review request:
   - What was accomplished
   - Files modified/created
   - How to test/verify
   - Done criteria checklist

**Review Requires:**
- **Human manual review** by user
- Verification against done criteria
- Testing of functionality
- Review of code/documentation quality

### 5. After Review (Reviewing → Done)

**If Review Passes:**
1. Move task from `5-reviewing.md` to `5-done.md`
2. Mark in backlog as complete: `✅ [Task Name]`
3. Update `dashboard.md` with new metrics
4. Update `sprints.md` with completed task

**Completion Summary in Done Should Include:**
- What was accomplished
- Files modified/created
- Key technical decisions made
- Test results
- Any follow-up items discovered
- Completion date

**If Review Requires Changes:**
1. Move task back to `3-in-progress.md`
2. Document required changes
3. Make changes and re-test
4. Move back to `5-reviewing.md` when ready

### 6. Archiving (After Backlog Complete)

**When to Archive:**
- Only after **ALL** items in backlog are complete (✅ marked)
- Tasks have been reviewed and moved to done
- Sprint is concluded

**Archive Process:**
1. Review all completed tasks in `5-done.md`
2. Move historical/completed tasks to `9-archive.md`
3. Keep recent achievements visible in `5-done.md`
4. Archive format: Task name + completion date + outcome summary
5. Update `sprints.md` to close current sprint
6. **Clear ALL items from `1-backlog.md`** (REQUIRED - leave completely empty)
   - No sprint history in backlog (history is in sprints.md and archive)
   - Backlog should be ready for new work only

**What to Archive:**
- Completed tasks from previous sprints
- Cancelled/obsolete tasks
- Historical context that's no longer actively referenced

**What to Keep in Done:**
- Recent achievements (current sprint)
- Important outcomes for reference
- Tasks referenced in current work

### 7. Updating the Dashboard

**After Each Task Completion:**
```bash
# Update these sections in dashboard.md:
- Progress Overview (percentages)
- Swim Lanes table (move cards)
- Metrics (files modified, build success)
- Recent Achievements (major completions)
- Next Actions (if priorities changed)
```

**Dashboard Metrics to Track:**
- Tasks Started / Completed
- Build Success Rate
- Files Modified
- Documentation Created
- Issues Found/Fixed
- Bundle Size Changes

### 8. Updating Sprints

**Current Sprint (`sprints.md`):**
- Sprint goal/theme
- Start date
- Planned tasks (from todo)
- In-progress tasks
- Completed tasks (move from done)
- Sprint metrics

**After Sprint Completion:**
1. Close current sprint section in `sprints.md`
2. Document:
   - Completed tasks
   - Sprint velocity
   - Key achievements
   - Lessons learned
3. Archive old done items to `9-archive.md`
4. Start new sprint section

**Sprint Format:**
```markdown
## Sprint N (YYYY-MM-DD to YYYY-MM-DD)

**Goal:** [Sprint theme/objective]

**Completed:**
- ✅ Task 1 - [Brief outcome]
- ✅ Task 2 - [Brief outcome]

**Velocity:** X tasks completed
**Key Achievements:** [Major wins]
**Lessons Learned:** [Process improvements]
```

---

## Documentation Maintenance

### When to Update Documentation

**Feature Complete:**
1. Update feature doc in `docs/3-features/`
2. Add entry to `docs/4-roadmap/CHANGELOG.md`
3. Update `docs/4-roadmap/current.md` if milestone completed

**Specification Change:**
1. Update relevant spec in `docs/2-specification/`
2. Note change in spec's changelog section
3. Check if other docs reference the changed spec

**New Work Planning:**
1. Add to `docs/4-roadmap/backlog.md` with priority
2. Create `Idea-*.md` file only for exploratory design
3. Move to `docs/3-features/` once design is stable

**Bug Fix or Small Change:**
- Commit message only (no doc update needed)

### Documentation Structure

```
docs/
├── 1-vision/          # Principles, standards, architecture
├── 2-specification/   # Normative specs (data model, profiles, APIs)
├── 3-features/        # Feature documentation
├── 4-roadmap/         # Status, milestones, changelog, backlog
├── 5-technical/       # Setup, deployment, performance, security
├── kanban/            # Task management (this workflow)
└── archive/           # Historical documents
```

### Status Indicators

Use these in document headers and inline:

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete |
| 🔄 | In Progress |
| ⚠️ | Needs Update |
| ❌ | Not Started |
| 📋 | Planned |
| 💡 | Future Idea |

---

## Security Workflow

### When Security Issues Are Found

**Severity Classification:**
- 🔴 **Critical** (CVSS 9.0-10.0): Immediate action (same day)
- 🟠 **High** (CVSS 7.0-8.9): Fix within 1 week
- 🟡 **Medium** (CVSS 4.0-6.9): Fix within 2 weeks
- 🟢 **Low** (CVSS 0.1-3.9): Address in next sprint
- ℹ️ **Info** (CVSS 0.0): Best practices review

**Fix Workflow:**
1. Document issue in `docs/5-technical/security-audit.md`
2. Assign CVSS score and priority
3. Provide fix code/approach in audit doc
4. Implement fix in affected files
5. Test fix with `pnpm build`
6. Update audit doc with ✅ RESOLVED status
7. Update executive summary with resolved count
8. Commit with clear message: `fix(security): <description> (CVSS X.X)`

**Testing Security Fixes:**
- Always run full build after security changes
- Test in browser if UI-related (CSP, XSS fixes)
- Verify no new errors in console
- Check that functionality still works

---

## Build & Test Workflow

### Before Committing

**Required Checks:**
```bash
# 1. Build successfully
pnpm --filter web build

# 2. Type check (if TypeScript changes)
pnpm --filter web nuxt typecheck

# 3. Test affected features manually
pnpm --filter web dev
# Navigate to changed pages/components

# 4. Process data if data-processing changes
pnpm --filter data-processing process
```

### After Major Changes

**Full System Check:**
```bash
# Build all packages
pnpm build

# Generate static site
pnpm --filter web generate

# Preview production build
pnpm --filter web preview
```

---

## Common Task Patterns

### Pattern: Add New Feature

1. **Prioritize:** Add to todo with done criteria
2. **Start:** Mark 🔄 in backlog, move to in-progress
3. **Plan:** Enter plan mode if non-trivial (multiple files/approaches)
4. **Implement:** Make focused code changes
5. **Test:** Build + manual testing
6. **Document:** Update `docs/3-features/` + `CHANGELOG.md`
7. **Review Request:** Move to reviewing with test instructions
8. **User Review:** Human verification against done criteria
9. **Complete:** Move to done, mark ✅ in backlog, update sprints

### Pattern: Fix Bug

1. **Prioritize:** Add to todo with done criteria (bug fixed + tested)
2. **Start:** Mark 🔄 in backlog, move to in-progress
3. **Reproduce:** Verify bug exists
4. **Identify:** Find root cause in code
5. **Fix:** Minimal change to address issue
6. **Test:** Verify fix works, no regressions
7. **Review Request:** Move to reviewing with before/after demo
8. **User Review:** Verify bug is fixed
9. **Complete:** Move to done, mark ✅ in backlog

### Pattern: Analysis Task

1. **Prioritize:** Add to todo with done criteria (report complete)
2. **Start:** Mark 🔄 in backlog, move to in-progress
3. **Research:** Explore codebase, external standards, data
4. **Document:** Create detailed markdown in `docs/5-technical/`
5. **Summarize:** Key findings + recommendations
6. **Review Request:** Move to reviewing for user feedback
7. **User Review:** Verify analysis is complete and accurate
8. **Complete:** Move to done, update dashboard, mark ✅ in backlog
9. **Next Steps:** Create follow-up tasks if issues found

### Pattern: Security Fix

1. **Prioritize:** Add to todo (Critical = immediate, High = 1 week)
2. **Start:** Mark 🔄 in backlog, move to in-progress
3. **Assess:** Read security audit, understand issue
4. **Implement:** Apply fix from audit recommendations
5. **Test:** Build + browser testing for UI fixes
6. **Document:** Update audit doc with ✅ RESOLVED
7. **Review Request:** Move to reviewing with security test plan
8. **User Review:** Verify security issue is resolved
9. **Complete:** Move to done, mark ✅ in backlog, update sprints
10. **Commit:** Security commit message with CVSS score

---

## Kanban File Purposes

### `1-backlog.md`
**Purpose:** Unstarted tasks waiting to be prioritized or started
**Format:** Task name + brief description + priority
**Important:** Backlog contains ONLY unstarted/active work. After sprint ends, backlog is COMPLETELY EMPTY.

**Status Markers (during active sprint):**
- (no marker) = Not started
- 🎯 = Moved to todo (prioritized)
- 🔄 = Currently in progress
- 👀 = In review
- ✅ = Complete (will be cleared when sprint ends)

**After Sprint Ends:**
- **Completely empty** (no items, no history, no summaries)
- Sprint history is in `sprints.md` and `9-archive.md`
- Ready for new work only

### `2-todo.md`
**Purpose:** Prioritized tasks for current sprint, ready to start
**Format:**
- Task name + priority (High/Medium/Low)
- Detailed requirements
- Acceptance criteria
- **Done criteria** (what complete means)
- Expected deliverables

### `3-in-progress.md`
**Purpose:** Currently active work being implemented
**Format:**
- Task name + owner
- Progress notes
- Blockers (if any)
- Start date
- Files being modified

### `5-reviewing.md`
**Purpose:** Tasks awaiting **human manual review/approval**
**Format:**
- Task name
- What to review (code, docs, functionality)
- How to test/verify
- Done criteria checklist
- Review request date

**Important:** Tasks stay here until user reviews and approves

### `5-done.md`
**Purpose:** Completed and reviewed tasks (current sprint)
**Format:**
- Task name + completion date
- Summary of what was accomplished
- Files modified/created
- Key decisions made
- Test results
- Follow-up items (if any)

**Note:** Keep only recent/current sprint items here

### `9-archive.md`
**Purpose:** Historical completed tasks from previous sprints
**Format:**
- Sprint identifier
- Task name + completion date
- Brief outcome summary
- Reason for archival (sprint ended, obsolete, cancelled)

**When to Archive:** After ALL backlog items complete and sprint ends

### `dashboard.md`
**Purpose:** High-level overview + real-time metrics
**Format:**
- Progress percentages (backlog → done)
- Swim lanes table (visual kanban board)
- Metrics (velocity, files changed, build success)
- Recent achievements
- Next actions

### `sprints.md`
**Purpose:** Sprint planning, tracking, and retrospectives
**Format:**
- **Current Sprint:** Goals + in-progress + completed tasks
- **Previous Sprints:** Closed sprints with outcomes + velocity + lessons

**Update:** Add completed tasks from `5-done.md` to current sprint section

---

## Key Files to Update

| When... | Update... |
|---------|-----------|
| Prioritizing tasks | `2-todo.md` (add task) + `1-backlog.md` (mark 🎯) |
| Starting task | `3-in-progress.md` (add) + `1-backlog.md` (mark 🔄) |
| Ready for review | `5-reviewing.md` (add) + `1-backlog.md` (mark 👀) |
| Task reviewed & complete | `5-done.md` (add) + `1-backlog.md` (mark ✅) + `sprints.md` |
| Sprint ends | `sprints.md` (close sprint) + `9-archive.md` (move old done items) |
| Feature complete | `docs/4-roadmap/CHANGELOG.md` |
| Starting new phase | `docs/4-roadmap/current.md` |
| Bug fix or small change | Commit message only |
| API/spec change | `docs/2-specification/` + changelog |
| New idea documented | Create `Idea-*.md`, later migrate |
| Security issue fixed | `docs/5-technical/security-audit.md` |
| Analysis complete | `docs/5-technical/*.md` |
| Any task state change | `dashboard.md` (swim lanes + metrics) |

---

## Communication Pattern

### Task Completion Messages

**Good Pattern:**
```
✅ Issue #6: Path Traversal Fixed

Fixed in 5 scripts:
- process-vocab.js
- generate-vocab-metadata.js
...

Fix: Added path validation to prevent traversal attacks.
Testing: Build passed successfully.
```

**What to Include:**
- Clear confirmation of what was done
- List of affected files
- Key technical approach
- Test results
- Any follow-up needed

### Progress Updates

**When Working on Long Tasks:**
- Update every 3-5 tool calls
- Show incremental progress
- Flag blockers immediately
- Ask questions early, not after implementing

---

## Exceptions & Edge Cases

### When Build Fails
1. Don't mark task complete
2. Document the error
3. Investigate root cause
4. Try alternative approach or ask for help
5. Only mark done after successful build

### When Requirements Unclear
1. Don't guess and implement
2. Ask specific clarifying questions
3. Provide 2-3 options if multiple approaches viable
4. Wait for confirmation before proceeding

### When Discovering New Issues
1. Document in appropriate file (security audit, backlog, etc.)
2. Don't automatically expand scope
3. Finish current task first
4. Create new task for newly discovered work

### When User Feedback Requires Changes
1. Re-open task or create follow-up task
2. Apply requested changes
3. Re-test
4. Update completion summary with iterations

---

## Quality Standards

### Code Quality
- ✅ Builds successfully
- ✅ No new console errors
- ✅ Follows existing patterns
- ✅ Minimal scope (focused changes)
- ✅ Security-conscious

### Documentation Quality
- ✅ Clear, concise language
- ✅ Code examples where relevant
- ✅ Status indicators used correctly
- ✅ Cross-references to related docs
- ✅ Maintained structure/formatting

### Task Completion Quality
- ✅ All acceptance criteria met
- ✅ Testing instructions provided
- ✅ Relevant docs updated
- ✅ Dashboard metrics updated
- ✅ Clear completion summary

---

## Tools & Commands Reference

### Build & Dev
```bash
pnpm --filter web dev           # Start dev server
pnpm --filter web build         # Build for production
pnpm --filter web generate      # Generate static site
pnpm --filter web preview       # Preview production build
```

### Data Processing
```bash
pnpm --filter data-processing process   # Process vocabularies
```

### Web Components
```bash
cd packages/web-components
pnpm build                      # Build web components
```

### Type Checking
```bash
pnpm --filter web nuxt typecheck   # Check TypeScript types
```

---

## Best Practices

**DO:**
- ✅ Define done criteria when prioritizing to todo
- ✅ Mark backlog status (🎯 🔄 👀 ✅) as tasks progress
- ✅ Move to reviewing (not done) after implementation
- ✅ Wait for human review before marking done
- ✅ Update sprints.md when tasks complete
- ✅ Test changes before requesting review
- ✅ Keep tasks focused and scoped
- ✅ Document security fixes thoroughly
- ✅ Provide clear test instructions for reviewers
- ✅ Ask questions when requirements unclear
- ✅ Archive only after sprint ends and ALL backlog complete

**DON'T:**
- ❌ Skip defining done criteria in todo phase
- ❌ Move directly from in-progress to done (must go through reviewing)
- ❌ Mark tasks done without human review
- ❌ Archive before all backlog items complete
- ❌ Leave completed items in backlog after sprint ends
- ❌ Forget to update backlog status markers
- ❌ Skip updating sprints.md with completions
- ❌ Expand scope without discussion
- ❌ Skip documentation updates
- ❌ Ignore build failures
- ❌ Guess at unclear requirements
- ❌ Leave tasks in "in progress" limbo

---

## Summary

**The Complete Workflow:**

```
Backlog (unstarted)
    ↓ [Prioritize]
Todo (prioritized, ready to start)
    ↓ [Start work, mark 🔄 in backlog]
In Progress (actively working)
    ↓ [Implement, test, document]
Reviewing (awaiting human review)
    ↓ [User reviews against done criteria]
Done (reviewed & complete, mark ✅ in backlog)
    ↓ [Update sprints.md with completion]
Archive (after sprint ends, all backlog complete)
```

**The Core Loop:**
1. **Prioritize:** Select from backlog → move to todo with done criteria
2. **Start:** Pick task from todo → mark 🔄 in backlog → move to in-progress
3. **Implement:** Make changes → test with build → update docs
4. **Review Request:** Move to reviewing with test instructions
5. **Human Review:** User verifies against done criteria
6. **Complete:** Move to done → mark ✅ in backlog → update sprints
7. **Archive:** After sprint ends and all backlog complete → move to archive
8. **Next task**

**Key Principles:**
- **Prioritize explicitly** with done criteria before starting
- **Mark backlog status** (🎯 todo, 🔄 in-progress, 👀 reviewing, ✅ done)
- **Human review required** before marking done
- **Archive only after** sprint ends and all backlog complete
- **Update sprints.md** with completed tasks
- **Progress tasks systematically, document thoroughly, test completely**

---

## Quick Reference

### Backlog Status Markers (1-backlog.md)

| Marker | Meaning | File Location |
|--------|---------|---------------|
| (none) | Not started | `1-backlog.md` only |
| 🎯 | Prioritized | `1-backlog.md` + `2-todo.md` |
| 🔄 | In progress | `1-backlog.md` + `3-in-progress.md` |
| 👀 | In review | `1-backlog.md` + `5-reviewing.md` |
| ✅ | Complete | `1-backlog.md` + `5-done.md` + `sprints.md` |

### File Update Checklist

**When moving task through workflow:**

```
Backlog → Todo:
  ☐ Add to 2-todo.md with done criteria
  ☐ Mark 🎯 in 1-backlog.md
  ☐ Update dashboard swim lanes

Todo → In Progress:
  ☐ Add to 3-in-progress.md with start date
  ☐ Mark 🔄 in 1-backlog.md
  ☐ Update dashboard swim lanes

In Progress → Reviewing:
  ☐ Add to 5-reviewing.md with test instructions
  ☐ Mark 👀 in 1-backlog.md
  ☐ Update dashboard swim lanes
  ☐ Include done criteria checklist

Reviewing → Done:
  ☐ Add to 5-done.md with completion summary
  ☐ Mark ✅ in 1-backlog.md
  ☐ Add to sprints.md current sprint section
  ☐ Update dashboard swim lanes + metrics

Sprint End (All backlog ✅):
  ☐ Close sprint in sprints.md
  ☐ Move old done items to 9-archive.md
  ☐ **CLEAR ALL items from 1-backlog.md** (leave completely empty)
  ☐ Backlog ready for new work (history is in sprints.md/archive)
```

### Critical Workflow Rules

1. **Never skip reviewing stage** - Tasks must have human review
2. **Never archive mid-sprint** - Only after ALL backlog complete
3. **Always clear backlog after sprint** - Backlog is for unstarted work only
4. **Always mark backlog status** - Keep 1-backlog.md current during sprint
5. **Always define done criteria** - In todo phase before starting
6. **Always update sprints.md** - When tasks complete
