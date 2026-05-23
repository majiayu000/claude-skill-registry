---
name: ralph-execute
description: Execute iterative development loop through user stories. Implements one story at a time with quality gates, commits, and learning persistence. Ships features autonomously.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, Task
user_invocable: true
argument-hint: [--max-iterations N] [--story US-XXX] [--dry-run] [--skip-blocked]
---

# Ralph Execution Skill

Autonomously implement user stories from the PRD, running quality gates and committing after each successful story. Maintains progress across sessions. Ships features while you sleep.

## What is Ralph?

Ralph is an autonomous AI coding loop that ships features while you sleep. Each iteration is a fresh context window (keeping context small). Memory persists via git history, progress.txt, prd.json, and AGENTS.md.

## Invocation

```bash
/ralph-execute [options]
```

**Arguments:**
- `--max-iterations N` - Override max iterations (default: from prd.json or 10)
- `--story US-XXX` - Target a specific story instead of next priority
- `--dry-run` - Show what would be done without making changes
- `--skip-blocked` - Skip blocked stories without re-attempting

**Examples:**
```bash
/ralph-execute                        # Continue from where we left off
/ralph-execute --max-iterations 5     # Run up to 5 stories
/ralph-execute --story US-003         # Implement specific story
/ralph-execute --dry-run              # Preview next story
```

## Execution Flow

### Phase 1: Session Initialization

#### Step 1.1: Load PRD

Read `.ralph/prd.json`. If not found:
```
ERROR: No PRD found at .ralph/prd.json

Run /ralph-plan first to generate a PRD with user stories.
```

#### Step 1.2: Check for Branch Change (Archival)

If current branch differs from `prd.branchName`, archive previous run:
```bash
mkdir -p .ralph/archive/[old-branch]-[timestamp]
mv .ralph/prd.json .ralph/archive/[old-branch]-[timestamp]/
mv .ralph/progress.txt .ralph/archive/[old-branch]-[timestamp]/
```

#### Step 1.3: Verify Branch

```bash
git branch --show-current
```

If not on the correct branch:
```bash
git checkout [prd.branchName]
```

#### Step 1.4: Load Progress Context

Read `.ralph/progress.txt` to understand:
- Previous learnings and patterns
- Files modified in past iterations
- Common gotchas discovered

**CRITICAL**: This context informs implementation decisions. Always read progress.txt before implementing.

#### Step 1.5: Load AGENTS.md

Read root-level `AGENTS.md` and any directory-level AGENTS.md files for:
- Module-specific patterns
- API conventions
- Known gotchas

#### Step 1.6: Initialize TodoWrite for UI

Sync prd.json stories to TodoWrite for visual progress tracking.

### Phase 2: Story Selection

#### Step 2.1: Find Next Story

Select the highest-priority story where `status === "pending"`:

```javascript
const nextStory = prd.userStories
  .filter(s => s.status === 'pending')
  .sort((a, b) => a.priority - b.priority)[0];
```

If no pending stories:
- Check for blocked stories (offer to retry if `--skip-blocked` not set)
- If all passed/blocked, report completion

#### Step 2.2: Check Iteration Limits

```javascript
if (prd.summary.iterationsRun >= prd.config.maxIterations) {
  // Report: "Max iterations reached. Run with --max-iterations N to continue."
  // Exit gracefully
}
```

#### Step 2.3: Display Story Context

```
STARTING ITERATION [N]
━━━━━━━━━━━━━━━━━━━━━━

Story: US-002 - Add registration form
Priority: 2 of 8
Previous Attempts: 0

Description:
As a new user, I want to register an account so that I can access the platform.
Implementation should follow the LoginForm pattern already established.

Acceptance Criteria:
□ Registration form with email, password, confirm password fields
□ Form validation using zod schema
□ Integration with existing auth context
□ TypeScript compiles without errors

Relevant Learnings from Progress:
- LoginForm pattern: src/components/auth/LoginForm.tsx
- Form validation: react-hook-form + zod
- Auth context: src/contexts/AuthContext.tsx
```

### Phase 3: Story Implementation (Compound Engineering)

Each story follows the **Plan → Work → Review → Compound** cycle:

#### PLAN PHASE (40% of effort)

**Step 3.1: Mark Story In-Progress**
Update prd.json: `status: "in_progress"`
Update TodoWrite to show current task

**Step 3.2: Research Codebase**
- Read AGENTS.md + progress.txt "Codebase Patterns" section
- Find similar patterns in codebase using Glob/Grep
- Check commit history for related changes
- Identify existing components to reuse

**Step 3.3: Create Implementation Plan**
Before writing code, document:
- Which files to create/modify
- Which patterns to follow
- Potential gotchas to avoid

#### WORK PHASE (20% of effort)

**Step 3.4: Implement the Story**

**CRITICAL IMPLEMENTATION RULES:**
1. **ONE story at a time** - Never implement multiple stories in one iteration
2. **Follow existing patterns** - Match the codebase style exactly
3. **Minimal changes** - Only modify what's needed for this story
4. **Type safety first** - Ensure TypeScript compiles before other checks

**For UI Stories, Apply Frontend-Design Principles:**
- Design thinking first - establish aesthetic direction before coding
- Use distinctive fonts, cohesive color schemes with CSS variables
- High-impact moments (page-load) over scattered micro-interactions
- Avoid: generic system fonts, clichéd colors, cookie-cutter patterns

**Step 3.5: Run Quality Gates (Fail-Fast)**

Execute in order:

1. **TypeScript Check (Required)**
   ```bash
   npm run check 2>&1
   ```
   On failure: Parse error output, attempt fix, re-run (max 2 attempts)

2. **Lint Check (Required)**
   ```bash
   npm run lint 2>&1
   ```
   On failure: Run `npm run lint -- --fix`, then re-check

3. **Test Check (Optional)**
   ```bash
   npm run test 2>&1
   ```
   If configured in prd.json

4. **Build Check (Optional)**
   ```bash
   npm run build 2>&1
   ```
   If enabled in prd.json config

**Step 3.6: Browser Verification (UI Stories)**

For stories with `requiresBrowserVerification: true`:
- Use `visual-polish-inspector` skill or Chrome extension
- Navigate to the page where UI change was made
- Take screenshot to verify rendering
- Check browser console for JavaScript errors
- Test responsive behavior if applicable
- Record pass/fail in progress.txt

**Requirements:**
- Chrome browser open
- Claude in Chrome extension (v1.0.36+) installed
- Dev server running (`npm run dev`)

#### REVIEW PHASE (20% of effort)

**Step 3.7: Evaluate Quality**
Before committing, verify:
- Code quality: Clean, readable, follows patterns
- Security: No obvious vulnerabilities
- Performance: No unnecessary re-renders or expensive operations
- Testing: Adequate coverage for critical paths

**Step 3.8: Handle Failures**

On quality gate failure:
```javascript
story.failureCount += 1;

if (story.failureCount >= prd.config.maxFailuresPerStory) {
  story.status = 'blocked';
  story.blockedReason = '[Specific error message]';
  prd.summary.blocked += 1;
  prd.summary.pending -= 1;
  // Log to progress.txt
  // Continue to next story
} else {
  // Retry this story
}
```

#### COMPOUND PHASE (20% of effort)

**Step 3.9: Commit Changes**

If all quality gates pass:
```bash
git add -A
git commit -m "feat: US-XXX - [Story Title]

[Brief description of implementation]

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Step 3.10: Update prd.json**
```javascript
story.status = 'passed';
story.completedAt = new Date().toISOString();
story.commits.push(commitHash);
prd.summary.passed += 1;
prd.summary.pending -= 1;
prd.summary.iterationsRun += 1;
prd.updatedAt = new Date().toISOString();
```

**Step 3.11: Update AGENTS.md**

If reusable patterns were discovered, add to AGENTS.md:
```markdown
## Module: src/components/auth/
- Forms use react-hook-form + zod validation
- Auth state from `@clerk/nextjs`
- Follow LoginForm.tsx as pattern
```

**Good AGENTS.md additions:**
- "When modifying X, also update Y"
- "This module uses pattern Z"
- "Tests require dev server running"

**Don't add to AGENTS.md:**
- Story-specific details
- Temporary notes
- Info already in progress.txt

**Step 3.12: Append to progress.txt**

```
--- ITERATION [N] | US-XXX: [Title] ---
Timestamp: [ISO]
Status: PASSED

Learnings for future iterations:
- [Pattern discovered]
- [Gotcha avoided]

Files Modified:
- [file1] (created)
- [file2] (modified)

Quality Gates:
- typecheck: PASSED
- lint: PASSED (auto-fixed 2 issues)
- test: SKIPPED
- browser: VERIFIED

Commit: [hash] - feat: US-XXX - [Title]
```

**Step 3.13: Consolidate Codebase Patterns**

Update the "CODEBASE PATTERNS (Consolidated)" section at the TOP of progress.txt with any new patterns discovered.

### Phase 4: Loop or Complete

#### Step 4.1: Check for Next Story

If pending stories remain AND iterations < max:
- **Continue to next iteration** (back to Phase 2)

#### Step 4.2: Handle Completion

If all stories passed or blocked:
```
RALPH EXECUTION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━

All [N] stories processed!

Summary:
- Iterations: [N]
- Stories Passed: [N]
- Stories Blocked: [N]
- Total Commits: [N]

Branch: [branch-name]
Ready for review and merge.

Key Learnings Captured:
1. [Learning 1]
2. [Learning 2]

Next Steps:
1. Review commits: git log --oneline -n [N]
2. Push branch: git push -u origin [branch-name]
3. Create PR: gh pr create
```

### Phase 5: Failure Handling

#### Blocked Story Notification

```
STORY BLOCKED: US-XXX
━━━━━━━━━━━━━━━━━━━━━

After 3 attempts, this story could not be completed.

Reason: [Specific blocker]

Recommended Action:
- [Suggestion based on error type]

Continuing with next priority story...
```

#### Append Failure to progress.txt

```
--- ITERATION [N] | US-XXX: [Title] (ATTEMPT 2/3) ---
Timestamp: [ISO]
Status: FAILED

Error:
[Error output]

Attempted Fix:
- [What was tried]

Result: Still failing. Will retry next iteration.
```

## Session Persistence

### Resuming Across Sessions

When `/ralph-execute` is run in a new session:
1. Read `.ralph/prd.json` for current state
2. Read `.ralph/progress.txt` for learned context
3. Read `AGENTS.md` for reusable patterns
4. Continue from first pending story

**The loop is stateless** - all state is in files, not memory.

### Cross-Session Learnings

progress.txt serves as persistent memory:
- Patterns discovered in iteration 1 inform iteration 5
- Gotchas are avoided in future stories
- File locations are remembered

**Always read progress.txt before implementing each story.**

## Critical Success Factors

### 1. Small Stories
Must fit in one context window.
```
❌ Too big: "Build entire auth system"
✅ Right size: "Add login form", "Add email validation", "Add auth server action"
```

### 2. Feedback Loops
Ralph needs fast feedback:
- `npm run check` (typecheck)
- `npm run lint`
- `npm run test`

Without these, broken code compounds.

### 3. Explicit Criteria
```
❌ Vague: "Users can log in"
✅ Explicit:
- Email/password fields
- Validates email format
- Shows error on failure
- typecheck passes
- Verify at localhost:3000/login
```

### 4. Learnings Compound
By story 10, Ralph knows patterns from stories 1-9.

### 5. CI Must Stay Green
Quality gates prevent error compounding across iterations.

## Common Gotchas

**Idempotent migrations:**
```sql
ADD COLUMN IF NOT EXISTS email TEXT;
```

**Interactive prompts:**
```bash
echo -e "\n\n\n" | npm run db:generate
```

**Schema changes:**
After editing schema, check: Server actions, UI components, API routes

**Fixing related files is OK:**
If typecheck requires other changes, make them. Not scope creep.

## Monitoring Progress

```bash
# Story status
cat .ralph/prd.json | jq '.userStories[] | {id, title, status}'

# Learnings
cat .ralph/progress.txt

# Recent commits
git log --oneline -10
```

## When NOT to Use Ralph

- Exploratory work
- Major refactors without criteria
- Security-critical code
- Anything needing human review

## Configuration Options

### prd.json Config Block

```json
"config": {
  "maxIterations": 10,        // Total iterations before stopping
  "maxFailuresPerStory": 3,   // Attempts before blocking
  "autoCommit": true          // Commit after each story
}
```

### Quality Gate Customization

```json
"qualityGates": {
  "typecheck": "npm run check",
  "lint": "npm run lint",
  "test": "npm run test",
  "build": null  // Set to null to skip
}
```

## Stop Condition

If ALL stories have `status: "passed"` or `status: "blocked"`, report completion.

Otherwise, continue to next pending story.
