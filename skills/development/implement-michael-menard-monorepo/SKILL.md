---
name: implement
description: Complete story implementation workflow from start to finish. Use when implementing user stories, features, or epics. Handles validation, development (with optional parallel execution), QA review, issue resolution, and PR creation. Can implement single stories, multiple stories, or entire epics in parallel.
---

# /implement - Complete Story Implementation Workflow

## Description

One-command story implementation from start to finish. Uses Claude Code's Task tool to spawn sub-agents for context-efficient parallel execution.

**Key Features:**
- Heavy phases (development, QA) delegated to sub-agents via Task tool
- Pre-flight checks validate environment before starting
- Resume capability for interrupted work
- Dry-run mode to preview actions
- Smart auto-detection of parallel mode

## Usage

```bash
# Simple story (single-agent)
/implement 1.2

# Complex story (parallel sub-agents)
/implement 1.1 --parallel

# With deep multi-specialist review
/implement 1.1 --parallel --deep-review

# Multiple stories in parallel
/implement 1.1,1.2,1.3 --parallel

# Quick review (skip deep analysis)
/implement 1.2 --quick-review

# Implement entire epic
/implement epic:3 --parallel --deep-review

# Implement epic (shorthand)
/implement 3 --epic --parallel --deep-review

# Preview what would happen (no changes made)
/implement 1.2 --dry-run

# Resume interrupted work
/implement 1.2 --resume

# After PR is merged - archive story and clean up
/implement 1.2 --complete
```

## Parameters

- **story number(s)** - Single story (e.g., `1.1`) or multiple stories (e.g., `1.1,1.2,1.3`)
- **epic:{number}** - Implement all stories in an epic (e.g., `epic:3` for Epic 3)
- **--epic** - Treat the number as an epic number
- **--parallel** - Use parallel sub-agent execution (auto-enabled for epics and complex stories)
- **--deep-review** - Multi-specialist QA review (security, performance, accessibility)
- **--quick-review** - Fast single-agent QA review
- **--skip-review** - Skip QA review (not recommended)
- **--dry-run** - Preview what would happen without making changes
- **--resume** - Continue from existing worktree/branch if present
- **--complete** - Run post-merge cleanup (archive story, close issue, clean worktree)

---

## EXECUTION INSTRUCTIONS

**CRITICAL: Follow these phases in order. Use Claude Code's Task tool for sub-agents. Use TodoWrite to track progress.**

---

## Phase -1: Pre-Flight Checks

**Run these checks BEFORE any other work. Fail fast on critical issues.**

```
1. GitHub CLI Authentication
   Run: gh auth status
   - FAIL if not authenticated
   - Provide: "Run 'gh auth login' to authenticate"

2. Git Status Check
   Run: git status --porcelain
   - WARN if uncommitted changes exist
   - ASK user: "Uncommitted changes detected. Continue anyway?"
   - Note: --resume flag skips this warning

3. Git Branch Check
   Run: git branch --show-current
   - FAIL if empty (detached HEAD state)
   - Provide: "Checkout a branch first: git checkout main"

4. Remote Accessibility
   Run: git ls-remote --exit-code origin (with timeout)
   - FAIL if cannot reach remote
   - Provide: "Check network connection or git remote configuration"

5. Story File Exists (quick check)
   Run: ls docs/stories/{STORY_NUM}.*.md
   - FAIL if no matching files
   - Provide: "Story file not found. Create with /create-story {STORY_NUM}"
```

**If --dry-run:** Report all check results and STOP here.

---

## Phase 0: Parse Arguments & Initialize

Parse the provided arguments to determine:
- Story number(s) or epic reference
- Execution mode (single vs parallel)
- Review type (deep, quick, skip)
- Special flags (--dry-run, --resume)

**Initialize progress tracking:**
```
TodoWrite([
  { content: "Pre-flight checks", status: "completed", activeForm: "Running pre-flight checks" },
  { content: "Story discovery & validation", status: "in_progress", activeForm: "Discovering story" },
  { content: "Development setup", status: "pending", activeForm: "Setting up development" },
  { content: "Implementation", status: "pending", activeForm: "Implementing story" },
  { content: "Quality assurance", status: "pending", activeForm: "Running QA review" },
  { content: "Create pull request", status: "pending", activeForm: "Creating PR" },
  { content: "Merge and archive", status: "pending", activeForm: "Merging PR and archiving story" }
])
```

---

## Phase 1: Story Discovery & Validation

**Use haiku model for fast, lightweight validation:**

```
Task(
  subagent_type: "Explore",
  model: "haiku",
  description: "Validate story {STORY_NUM}",
  prompt: "Find and validate story file for story {STORY_NUM}.

           Search in: docs/stories/
           Pattern: {STORY_NUM}.*.md

           Extract and return:
           1. story_file_path: Full path to story file
           2. story_title: Title from story file
           3. story_status: Status field (Approved, Ready, Draft, In Progress, Done, etc.)
           4. github_issue: Issue number if present (e.g., #123)
           5. tasks: List of task checkboxes from the story
           6. dependencies: Any story dependencies mentioned
           7. acceptance_criteria: List of acceptance criteria

           Validation rules:
           - FAIL if status is 'Done', 'Complete', or 'Implemented'
           - WARN if status is not 'Approved' or 'Ready'
           - WARN if no GitHub issue linked

           Return as structured data."
)
```

**For epic - filter out completed stories:**
```
Task(
  subagent_type: "Explore",
  model: "haiku",
  description: "Discover epic {EPIC_NUM} stories",
  prompt: "Find all implementable stories in Epic {EPIC_NUM}.

           Search: docs/stories/{EPIC_NUM}.*.md

           For each story, extract: file path, status, dependencies.

           FILTER OUT stories with status: Done, Complete, Implemented, Ready for Review

           Analyze dependencies between remaining stories.
           Create execution waves (stories with no deps first, then dependent stories).

           Return ordered list of stories to implement."
)
```

**Smart parallel detection:**
If story has 5+ tasks OR touches 3+ directories → suggest `--parallel`

---

## Phase 2: Development Setup (Resume-Aware)

**CRITICAL: Claude Code cannot "cd" persistently. All subsequent operations must use the WORKTREE_PATH explicitly.**

**Check for existing worktree/branch first:**

```bash
# Generate branch name and worktree directory name
BRANCH_NAME="feature/{STORY_NUM}-{slug}"
WORKTREE_DIR="{STORY_NUM}"  # Short name for directory (e.g., "wish-2002")

# Get absolute path to repo root
REPO_ROOT=$(git rev-parse --show-toplevel)
WORKTREE_PATH="${REPO_ROOT}/tree/${WORKTREE_DIR}"

# Check if worktree already exists
git worktree list | grep "${BRANCH_NAME}"

# Check if branch exists
git branch --list "${BRANCH_NAME}"
git branch -r --list "origin/${BRANCH_NAME}"
```

**If --resume or existing work found:**
- Verify worktree exists at `${WORKTREE_PATH}`
- Pull latest if remote exists: `git -C "${WORKTREE_PATH}" pull --rebase origin ${BRANCH_NAME}`
- Report: "Resuming work in worktree: ${WORKTREE_PATH}"

**If creating new:**
1. Ensure on main and up-to-date: `git checkout main && git pull`
2. Create worktree with short directory name: `git worktree add "${WORKTREE_PATH}" -b ${BRANCH_NAME}`
   - Worktree directory: `tree/{STORY_NUM}` (e.g., `tree/wish-2002`)
   - Branch name: `feature/{STORY_NUM}-{slug}` (e.g., `feature/wish-2002-add-item-flow`)
3. Verify creation: `ls "${WORKTREE_PATH}"`

**IMPORTANT: Store WORKTREE_PATH for use in Phase 3+. All git commands must use `git -C "${WORKTREE_PATH}"` and all file operations must use absolute paths within the worktree.**

**Update GitHub issue (if present):**
```bash
# Remove any previous status labels
gh issue edit {ISSUE_NUMBER} \
  --remove-label "ready" \
  --remove-label "approved" \
  --remove-label "blocked" \
  --add-label "in-progress"

# Add implementation started comment with branch link
gh issue comment {ISSUE_NUMBER} --body "$(cat <<'EOF'
## Implementation Started

**Branch:** `{BRANCH_NAME}`
**Started by:** Claude Code
**Story file:** `docs/stories/{STORY_NUM}.*.md`

Work is in progress. PR will be created when ready.
EOF
)"
```

**Update story file status:**
```markdown
status: In Progress
```

---

## Phase 3: Implementation

**CRITICAL: Spawn sub-agent with full project context AND explicit worktree path.**

**Read CLAUDE.md first to include in prompt:**
```
CLAUDE_MD_CONTENT = Read("{WORKTREE_PATH}/CLAUDE.md")
```

**Single-agent mode (default):**
```
Task(
  subagent_type: "general-purpose",
  description: "Implement story {STORY_NUM}",
  prompt: "You are implementing story {STORY_NUM}.

           ## CRITICAL: Worktree Path
           **ALL work must happen in the worktree, not the main repo.**

           WORKTREE_PATH: {WORKTREE_PATH}

           - All file reads/writes must use absolute paths starting with {WORKTREE_PATH}
           - All git commands must use: git -C {WORKTREE_PATH} <command>
           - Example: git -C {WORKTREE_PATH} add .
           - Example: git -C {WORKTREE_PATH} commit -m 'message'
           - All pnpm commands must run from worktree: pnpm --prefix {WORKTREE_PATH} <command>

           ## Project Guidelines (MUST FOLLOW)
           {CLAUDE_MD_CONTENT}

           ## Story Details
           Story file: {WORKTREE_PATH}/docs/stories/{STORY_FILE_NAME}
           Tasks to implement:
           {TASK_LIST}

           ## Implementation Process
           For each task:
           1. Read and understand the requirement
           2. Implement the code changes following project guidelines
           3. Write tests (minimum 45% coverage)
           4. Run tests to verify: pnpm --prefix {WORKTREE_PATH} test
           5. Run type check: pnpm --prefix {WORKTREE_PATH} check-types
           6. Commit with: git -C {WORKTREE_PATH} add . && git -C {WORKTREE_PATH} commit -m 'message'

           ## Critical Rules (from CLAUDE.md)
           - Use @repo/ui for ALL UI components
           - Use @repo/logger instead of console.log
           - Use Zod schemas for types (never TypeScript interfaces)
           - NO barrel files
           - Follow component directory structure

           ## Output
           Report completion status for each task.
           List any issues encountered.
           Provide summary of files changed."
)
```

**Parallel mode (--parallel):**
```
# For multiple stories, spawn in parallel with run_in_background
# EACH agent gets its own WORKTREE_PATH for its story
Task(
  subagent_type: "general-purpose",
  description: "Implement story {STORY_1}",
  run_in_background: true,
  prompt: "..."  # Same as above with story-specific details and WORKTREE_PATH_1
)

Task(
  subagent_type: "general-purpose",
  description: "Implement story {STORY_2}",
  run_in_background: true,
  prompt: "..."  # Same as above with story-specific details and WORKTREE_PATH_2
)

# Collect results
TaskOutput(task_id: "{agent_id_1}")
TaskOutput(task_id: "{agent_id_2}")
```

**Update progress:**
```
TodoWrite([
  ...previous todos marked complete...,
  { content: "Quality assurance", status: "in_progress", activeForm: "Running QA review" }
])
```

---

## Phase 4: Quality Assurance

**Quick review (default) - use haiku for speed:**
```
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "QA review for story {STORY_NUM}",
  prompt: "Review implementation for story {STORY_NUM}.

           ## CRITICAL: Worktree Path
           WORKTREE_PATH: {WORKTREE_PATH}
           All commands must run from worktree using --prefix or -C flags.

           ## Required Checks (run these commands)
           1. pnpm --prefix {WORKTREE_PATH} test --filter='...[origin/main]'
           2. pnpm --prefix {WORKTREE_PATH} check-types --filter='...[origin/main]'
           3. pnpm --prefix {WORKTREE_PATH} lint --filter='...[origin/main]'

           ## Code Review Checks
           1. Verify all acceptance criteria from story are met
           2. Check for package duplication (no reimplementing @repo/ui, @repo/logger, etc.)
           3. Verify Zod schemas used (not TypeScript interfaces)
           4. Check no console.log statements
           5. Verify no barrel files created
           6. Check test coverage meets 45% minimum

           ## Output Format
           {
             checks: [
               { name: 'Tests', status: 'PASS|FAIL', details: '...' },
               { name: 'Types', status: 'PASS|FAIL', details: '...' },
               ...
             ],
             issues: [
               { id: 'ISSUE-001', severity: 'Critical|High|Medium|Low', description: '...', file: '...', line: N }
             ],
             gate: 'PASS|CONCERNS|FAIL',
             summary: '...'
           }"
)
```

**Deep review (--deep-review) - parallel specialists:**
```
# Run quick review first (required checks)
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Required checks",
  prompt: "WORKTREE_PATH: {WORKTREE_PATH}
           Run from worktree:
           pnpm --prefix {WORKTREE_PATH} test && pnpm --prefix {WORKTREE_PATH} check-types && pnpm --prefix {WORKTREE_PATH} lint
           Report PASS/FAIL for each."
)

# Then spawn specialists in parallel
Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Security review",
  run_in_background: true,
  prompt: "You are a security specialist reviewing {WORKTREE_PATH}.

           Check for:
           - Authentication/authorization issues
           - Injection vulnerabilities (SQL, XSS, command)
           - Sensitive data exposure
           - OWASP Top 10 issues
           - Hardcoded secrets or credentials

           Report findings with severity (Critical/High/Medium/Low).
           Include file path and line number for each finding."
)

Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Performance review",
  run_in_background: true,
  prompt: "You are a performance specialist reviewing {WORKTREE_PATH}.

           Check for:
           - N+1 query patterns
           - Missing database indexes
           - Unnecessary re-renders in React
           - Large bundle imports
           - Missing memoization
           - Inefficient algorithms

           Report findings with estimated impact (High/Medium/Low).
           Suggest specific optimizations."
)

Task(
  subagent_type: "general-purpose",
  model: "haiku",
  description: "Accessibility review",
  run_in_background: true,
  prompt: "You are an accessibility specialist reviewing {WORKTREE_PATH}.

           Check for:
           - WCAG 2.1 AA compliance
           - Keyboard navigation support
           - Screen reader compatibility
           - ARIA labels and roles
           - Color contrast issues
           - Focus management

           Report findings with WCAG criterion references."
)

# Collect all results
TaskOutput(task_id: "{required_checks_id}")
TaskOutput(task_id: "{security_id}")
TaskOutput(task_id: "{performance_id}")
TaskOutput(task_id: "{accessibility_id}")
```

**Aggregate and decide:**
- Any Critical issue → gate: FAIL
- 3+ High issues → gate: FAIL
- Any High issues → gate: CONCERNS
- Otherwise → gate: PASS

---

## Phase 5: Issue Resolution

**If gate is FAIL or CONCERNS:**

1. Display issues to user organized by severity
2. Ask: "Auto-fix issues? (y/n)"

**If yes, spawn fix agent:**
```
Task(
  subagent_type: "general-purpose",
  description: "Fix QA issues for {STORY_NUM}",
  prompt: "Fix these issues found during QA:

           {ISSUES_LIST_WITH_DETAILS}

           ## CRITICAL: Worktree Path
           WORKTREE_PATH: {WORKTREE_PATH}
           All file operations must use absolute paths within {WORKTREE_PATH}.
           All git commands must use: git -C {WORKTREE_PATH} <command>

           ## Project Guidelines
           {CLAUDE_MD_CONTENT}

           For each issue:
           1. Understand the root cause
           2. Implement the fix following project guidelines
           3. Add/update tests to prevent regression
           4. Verify fix works: pnpm --prefix {WORKTREE_PATH} test
           5. Commit with: git -C {WORKTREE_PATH} commit -m 'fix: {issue description}'

           Report status for each issue fixed."
)
```

3. Re-run QA review after fixes
4. If still FAIL after 2 attempts → report to user and STOP

---

## Phase 6: Create Pull Request

**Only proceed if gate is PASS (or CONCERNS with user approval).**

```bash
# All git commands must use -C flag with worktree path

# Ensure all changes committed
git -C {WORKTREE_PATH} add -A
git -C {WORKTREE_PATH} status --porcelain
# If uncommitted changes, commit them

# Push branch
git -C {WORKTREE_PATH} push -u origin {BRANCH_NAME}

# Create PR
gh pr create \
  --title "feat({scope}): {story_title}" \
  --body "## Summary
Implements Story {STORY_NUM}: {story_title}

## Changes
{LIST_OF_CHANGES}

## Test Plan
{ACCEPTANCE_CRITERIA_AS_CHECKLIST}

## QA Status
Gate: {GATE_STATUS}
{QA_SUMMARY}

Closes #{ISSUE_NUMBER}

---
Generated with [Claude Code](https://claude.com/claude-code)"
```

**Update GitHub issue:**
```bash
gh issue edit {ISSUE_NUMBER} \
  --remove-label "in-progress" \
  --add-label "ready-for-review"

gh issue comment {ISSUE_NUMBER} --body "$(cat <<'EOF'
## Ready for Review

**Pull Request:** {PR_URL}
**QA Gate:** {GATE_STATUS}

### Changes Summary
{LIST_OF_CHANGES_BRIEF}

### Test Plan
{ACCEPTANCE_CRITERIA_AS_CHECKLIST}

---
Awaiting review and merge.
EOF
)"
```

**Update story file status:**
```markdown
status: Ready for Review
```

---

## Phase 7: Summary

**Report to user:**
```
═══════════════════════════════════════════════════════
  Story Implementation Complete
═══════════════════════════════════════════════════════

Story:      {STORY_NUM} - {STORY_TITLE}
Mode:       {single|parallel}
Review:     {quick|deep|skip}

Results:
  Files changed:  {N}
  Tests added:    {N}
  Coverage:       {N}%

QA Status:  {PASS|CONCERNS|FAIL}
  - Tests:        {PASS|FAIL}
  - Types:        {PASS|FAIL}
  - Lint:         {PASS|FAIL}
  {If deep review:}
  - Security:     {N issues}
  - Performance:  {N issues}
  - Accessibility:{N issues}

Pull Request: {PR_URL}
GitHub Issue: #{ISSUE_NUMBER} (labeled: ready-for-review)

Next Steps:
  - Review PR at {PR_URL}
  - Merge when approved
  - Run: /implement {STORY_NUM} --complete (to archive story)
  - Worktree at: tree/{STORY_NUM}
═══════════════════════════════════════════════════════
```

**Note:** Do NOT clear todos yet - Phase 8 handles completion after merge.

---

## Phase 8: Post-Merge Completion (--complete flag)

**This phase runs after the PR has been merged. Triggered by `/implement {STORY_NUM} --complete`.**

### 8.1 Verify PR is Merged

```bash
# Check PR status
PR_STATE=$(gh pr view {PR_URL} --json state -q '.state')

if [ "$PR_STATE" != "MERGED" ]; then
  echo "PR is not merged yet (state: $PR_STATE)"
  echo "Merge the PR first, then run: /implement {STORY_NUM} --complete"
  exit 1
fi
```

### 8.2 Archive Story File

```bash
# Move story file to archive
STORY_FILE="docs/stories/{STORY_NUM}.*.md"
ARCHIVE_DIR="docs/_archive/completed-stories"

# Ensure archive directory exists
mkdir -p "$ARCHIVE_DIR"

# Move file
mv $STORY_FILE "$ARCHIVE_DIR/"

# Update story status in archived file
sed -i '' 's/^status:.*/status: Done/' "$ARCHIVE_DIR/{STORY_FILENAME}"

# Commit the archive move
git add docs/stories/ docs/_archive/completed-stories/
git commit -m "chore: archive completed story {STORY_NUM}"
```

### 8.3 Close GitHub Issue

```bash
gh issue edit {ISSUE_NUMBER} \
  --remove-label "ready-for-review" \
  --remove-label "in-progress" \
  --add-label "done"

gh issue comment {ISSUE_NUMBER} --body "$(cat <<'EOF'
## Story Complete

**PR Merged:** {PR_URL}
**Story Archived:** `docs/_archive/completed-stories/{STORY_FILENAME}`

This story has been successfully implemented and merged.
EOF
)"

# Close the issue
gh issue close {ISSUE_NUMBER}
```

### 8.4 Clean Up Worktree

```bash
# Remove the worktree (uses short story-based directory name)
git worktree remove tree/{STORY_NUM} --force

# Delete the local branch (remote already deleted by PR merge)
git branch -D {BRANCH_NAME}

# Prune any stale worktree references
git worktree prune
```

### 8.5 Final Summary

```
═══════════════════════════════════════════════════════
  Story Completed and Archived
═══════════════════════════════════════════════════════

Story:       {STORY_NUM} - {STORY_TITLE}
Status:      Done

Actions Completed:
  ✓ PR merged:     {PR_URL}
  ✓ Story archived: docs/_archive/completed-stories/{STORY_FILENAME}
  ✓ Issue closed:  #{ISSUE_NUMBER}
  ✓ Worktree removed: tree/{STORY_NUM}
  ✓ Branch cleaned up: {BRANCH_NAME}

═══════════════════════════════════════════════════════
```

**Clear todos:**
```
TodoWrite([])
```

---

## Sub-Agent Architecture

```
Main Orchestrator (this skill)
    │
    ├─▶ Pre-Flight Checks (inline, no sub-agent)
    │
    ├─▶ Task(Explore, haiku) ─── Story discovery/validation
    │
    ├─▶ Task(general-purpose) ─── Implementation
    │       └── Includes CLAUDE.md guidelines
    │
    └─▶ Task(general-purpose, haiku) ─── QA Review
            ├── Quick: Single agent
            └── Deep: Parallel specialists
                 ├── Security
                 ├── Performance
                 └── Accessibility
```

**Model Selection:**
- `haiku` - Validation, quick checks, specialist reviews (fast, cheap)
- `sonnet` (default) - Implementation, complex fixes (balanced)
- `opus` - Only if explicitly requested or critical decision needed

---

## Error Handling

**Critical Failures (STOP immediately):**
- Pre-flight check failures (gh auth, git state)
- Story file not found
- Story already completed
- QA gate FAIL after 2 fix attempts

**Recoverable Issues (warn and continue):**
- Uncommitted changes (with user approval)
- Missing GitHub issue link
- Story status not Approved/Ready

**Resume on Failure:**
Work is preserved in worktree. User can:
1. Fix issues manually
2. Run `/implement {story} --resume` to continue

---

## When to Use Each Mode

### Default (Single-Agent)
- Simple UI changes
- Documentation updates
- Small bug fixes
- Single-file modifications

### --parallel (Auto-suggested when beneficial)
- Multi-component features
- Full-stack implementations
- 5+ tasks in story
- Changes spanning 3+ directories

### --deep-review
- Security-sensitive (auth, payments, data access)
- Public-facing features
- Performance-critical paths
- Accessibility requirements

### --quick-review
- Internal tools
- Low-risk changes
- Hotfixes (after manual review)

### --dry-run
- Preview before starting
- Verify story is ready
- Check environment setup

### --resume
- Continue interrupted work
- Re-run after manual fixes

### --complete
- Run after PR is merged
- Archives story to `docs/_archive/completed-stories/`
- Closes GitHub issue with "done" label
- Cleans up worktree and branch
