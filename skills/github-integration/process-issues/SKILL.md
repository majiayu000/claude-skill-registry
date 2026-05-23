---
name: process-issues
description: Process GitHub Issues - fetch open issues, read comments, analyze suggestions, find similar, create Beads tasks, propose fix plan
version: 1.1.0
---

# Process GitHub Issues

Automated workflow for processing GitHub Issues from repository.

## CRITICAL REQUIREMENTS

> **YOU MUST FOLLOW THESE RULES. NO EXCEPTIONS.**

### 1. BEADS IS MANDATORY

**EVERY issue MUST have a Beads task before fixing.** No direct fixes without tracking.

```bash
# ALWAYS run this FIRST for each issue:
bd create --type=<bug|task|feature> --priority=<1-3> --title="<issue_title>" --external-ref="gh-<number>"
bd update <task_id> --status=in_progress
```

### 2. READ ISSUE COMMENTS (MANDATORY)

**ALWAYS read comments to issues — they contain valuable insights:**

```bash
# View issue with all comments
gh issue view <number> --comments

# Or via API for structured data
gh api repos/maslennikov-ig/BuhBot/issues/<number>/comments --jq '.[].body'
```

**What to analyze in comments:**

- **User clarifications**: Additional context about the problem
- **Suggested solutions**: Community/team members often propose fixes
- **Workarounds**: Temporary solutions that hint at root cause
- **Related issues**: Links to other issues with same problem
- **Screenshots/logs**: Additional debugging information

**Decision making for suggestions:**

| Suggestion Type       | Action                                          |
| --------------------- | ----------------------------------------------- |
| Clear fix with code   | Verify correctness, adopt if valid              |
| Architecture proposal | Evaluate complexity, discuss with user if major |
| Workaround            | Note it, but look for proper fix                |
| Conflicting advice    | Analyze trade-offs, choose best approach        |
| Outdated advice       | Check if still relevant to current codebase     |

**Include in analysis:**

```markdown
### Comments Analysis

- **Useful suggestions**: <list helpful comments>
- **Decision**: Adopt / Modify / Reject with reason
```

### 3. SEARCH SIMILAR PROBLEMS FIRST (MANDATORY)

**Before fixing ANY issue, search BOTH sources:**

#### 2a. Search in Beads (closed tasks)

```bash
# Search by keywords from issue title/body
bd search "<keyword>" --type=bug --status=closed
bd search "<keyword>" --type=task --status=closed

# Example searches:
bd search "silent failure"
bd search "telegram"
bd search "SLA"
```

**What to look for in Beads:**

- Similar issue patterns in task titles
- Root cause analysis in task descriptions
- Fix approach and files changed

#### 2b. Search in GitHub (closed issues)

```bash
# Search closed issues
gh issue list --state closed --search "<keyword>"

# View specific closed issue for context
gh issue view <number>
```

#### 2c. If found similar resolved issue

1. **From Beads**: Read task description for root cause and fix approach
2. **From GitHub**: Read the closing comment — contains solution
3. Apply same solution pattern if applicable
4. **Reference in your fix**: `Similar to buh-xxx / gh-NN. Same fix applied.`

### 4. CONTEXT7 IS MANDATORY

**ALWAYS query documentation before implementing:**

```
mcp__context7__resolve-library-id → mcp__context7__query-docs
```

**When to use:**

- React/Next.js patterns
- Supabase queries
- BullMQ job handling
- Telegraf bot patterns
- Any external library involved

### 5. TASK COMPLEXITY ROUTING

**Route tasks by complexity:**

| Complexity  | Examples                              | Action                   |
| ----------- | ------------------------------------- | ------------------------ |
| **Simple**  | Typo fix, single import, config value | Execute directly         |
| **Medium**  | Multi-file fix, migration, API change | **Delegate to subagent** |
| **Complex** | Architecture change, new feature      | Ask user first           |

**Subagent selection for MEDIUM tasks:**

| Domain           | Subagent                             | When                     |
| ---------------- | ------------------------------------ | ------------------------ |
| DB/migrations    | `database-architect`                 | Schema changes, RLS      |
| UI components    | `nextjs-ui-designer`                 | New pages, components    |
| Backend services | `fullstack-nextjs-specialist`        | APIs, workers            |
| Types            | `typescript-types-specialist`        | Complex types, generics  |
| Telegram bot     | `telegraf-bot-middleware-specialist` | Bot handlers, middleware |
| SLA/monitoring   | `sla-backend-specialist`             | SLA timers, alerts       |

### 6. ISSUE LABELS → PRIORITY MAPPING

| GitHub Label  | Priority | Description                   |
| ------------- | -------- | ----------------------------- |
| `bug`         | P1-P2    | Bug fix (severity determines) |
| `enhancement` | P2-P3    | Feature improvement           |
| `UX`          | P2       | User experience issue         |
| `A11Y`        | P3       | Accessibility                 |
| `feature`     | P3       | New feature request           |

### 7. BUG FIXING PRINCIPLES

> **This is PRODUCTION. Every bug matters.**

**Fix fundamentally, not superficially:**

- Find and fix the ROOT CAUSE, not just symptoms
- If error happens in function X but cause is in function Y → fix Y
- Don't add workarounds/hacks that mask the problem
- Ask: "Why did this happen?" until you reach the actual cause

**Quality over speed:**

- Take time to understand the full context
- Test the fix mentally: "What else could break?"
- Check for similar patterns elsewhere in codebase
- One good fix > multiple quick patches

---

## Usage

Invoke via: `/process-issues` or "обработай GitHub issues"

Optional arguments:

- `/process-issues --label=bug` — only bug issues
- `/process-issues --limit=5` — process max 5 issues
- `/process-issues 123` — process specific issue #123

---

## Workflow

### Step 1: Fetch Open Issues

```bash
# Get all open issues sorted by priority
gh issue list --state open --json number,title,labels,body,createdAt --limit 50

# Or filter by label
gh issue list --state open --label bug --json number,title,labels,body
```

### Step 2: Analyze Each Issue

For each open issue:

1. **Read issue details**:

   ```bash
   gh issue view <number>
   ```

2. **Read and analyze comments** (MANDATORY):

   ```bash
   # View issue with all comments
   gh issue view <number> --comments

   # Or get comments via API for parsing
   gh api repos/maslennikov-ig/BuhBot/issues/<number>/comments
   ```

   **Analyze each comment for:**
   - Proposed solutions or code fixes
   - Additional context/reproduction steps
   - Links to related issues or PRs
   - Workarounds that hint at root cause

   **Make decision**: Adopt useful suggestions, note rejected ones with reason.

3. **Extract key information**:
   - Issue type (bug/feature/enhancement)
   - Affected files/components (from description)
   - Error messages (if bug)
   - Expected behavior
   - **Useful suggestions from comments**

4. **Search for similar resolved issues** (MANDATORY):

   ```bash
   # In Beads
   bd search "<keyword from issue>"

   # In GitHub
   gh issue list --state closed --search "<keyword>"
   ```

### Step 3: Create Analysis Plan

For each issue, generate:

```markdown
## Issue #NN: <title>

### Type & Priority

- Type: bug | feature | enhancement | UX
- Priority: P0 (blocker) | P1 (critical) | P2 (important) | P3 (nice-to-have)

### Comments Analysis

- **Total comments**: N
- **Useful suggestions**:
  - @user1: "Suggested fix X" → **Adopt** (valid approach)
  - @user2: "Try workaround Y" → **Note** (temporary, need proper fix)
  - @user3: "Related to #MM" → **Investigate** (check linked issue)
- **Rejected suggestions**:
  - @user4: "Do Z" → **Reject** (outdated, doesn't match current architecture)

### Similar Issues Found

- Beads: buh-xxx (similar problem with X, fixed by Y)
- GitHub: #NN (same root cause, fix in commit abc123)

### Root Cause Analysis

<Why this happens>

### Proposed Solution

1. <Step 1>
2. <Step 2>

### Files to Modify

- `path/to/file1.ts` — description
- `path/to/file2.tsx` — description

### Subagent Assignment

- Subagent: <name> | Execute directly
- Complexity: Simple | Medium | Complex

### Context7 Queries Needed

- [ ] Next.js: <topic>
- [ ] Supabase: <topic>
- [ ] Telegraf: <topic>
```

### Step 4: Create Beads Tasks

**For each issue:**

```bash
# Create task with external reference
bd create "<issue_title>" -t <bug|task|feature> -p <1-3> \
  --external-ref="gh-<number>" \
  -d "<root_cause_and_solution>"

# Save the task ID for tracking
```

**Task description template:**

```
GitHub Issue: #<number>
Root Cause: <why this happens>
Solution: <what needs to be done>
Files: <list of files>
Similar to: buh-xxx / gh-NN (if found)
```

### Step 5: Propose Execution Plan

Present to user:

```markdown
## GitHub Issues Processing Plan

### Summary

| #   | Issue | Type | Priority | Similar Found | Subagent           |
| --- | ----- | ---- | -------- | ------------- | ------------------ |
| 1   | #NN   | bug  | P1       | buh-xxx       | database-architect |
| 2   | #MM   | UX   | P2       | —             | nextjs-ui-designer |

### Beads Tasks Created

- buh-aaa: Issue #NN (P1)
- buh-bbb: Issue #MM (P2)

### Execution Order (by priority)

1. **P0-P1 (Critical)**: #NN, #MM
2. **P2 (Important)**: #XX
3. **P3 (Nice-to-have)**: #YY

### Questions for User

- Issue #ZZ: Need clarification on <topic>
- Issue #WW: Complex change, approve approach?

### Ready to Execute?

- [ ] Approve plan
- [ ] Modify priorities
- [ ] Skip certain issues
```

### Step 6: Execute Fixes (After User Approval)

**For each issue in priority order:**

1. **Claim Beads task**:

   ```bash
   bd update <task_id> --status=in_progress
   ```

2. **Query Context7** (if needed):

   ```
   mcp__context7__resolve-library-id → mcp__context7__query-docs
   ```

3. **Delegate or Execute**:
   - Simple: Execute directly
   - Medium: Delegate to subagent
   - Complex: Ask user first

4. **Verify**:

   ```bash
   npm run type-check
   npm run build
   ```

5. **Close GitHub Issue**:

   ```bash
   gh issue close <number> --comment "Fixed in commit <sha>

   **Solution:**
   <description of fix>

   Beads task: <task_id>"
   ```

6. **Close Beads Task**:
   ```bash
   bd close <task_id> --reason="Fixed: <description>"
   ```

### Step 7: Summary Report

```markdown
## Issues Processing Complete

### Results

| Issue | Status   | Beads Task | Commit |
| ----- | -------- | ---------- | ------ |
| #NN   | Fixed    | buh-aaa    | abc123 |
| #MM   | Fixed    | buh-bbb    | def456 |
| #XX   | Deferred | buh-ccc    | —      |

### Deferred Issues (need user input)

- #XX: <reason>

### Commits Made

- `abc123`: fix: <description>
- `def456`: feat: <description>

### Validation

- Type Check: PASS
- Build: PASS
```

---

## Issue Categories & Subagents

| Pattern in Issue        | Category      | Subagent                             | Priority |
| ----------------------- | ------------- | ------------------------------------ | -------- |
| `silent failure`        | Bug           | Same domain subagent                 | P1       |
| `not displayed`         | UI Bug        | `nextjs-ui-designer`                 | P2       |
| `not editable`          | UI Bug        | `nextjs-ui-designer`                 | P2       |
| `focus`, `scroll`       | UX            | `nextjs-ui-designer`                 | P2       |
| `keyboard`, `a11y`      | Accessibility | `nextjs-ui-designer`                 | P3       |
| `telegram`, `bot`       | Bot           | `telegraf-bot-middleware-specialist` | P2       |
| `SLA`, `timer`, `alert` | SLA           | `sla-backend-specialist`             | P2       |
| `database`, `migration` | DB            | `database-architect`                 | P2       |
| `tRPC`, `API`           | Backend       | `fullstack-nextjs-specialist`        | P2       |
| `type error`            | Types         | `typescript-types-specialist`        | P2       |

---

## Verification Checklist

Before marking ANY issue as fixed:

- [ ] Issue comments read and analyzed
- [ ] Useful suggestions considered (adopted/rejected with reason)
- [ ] Similar issues searched (Beads + GitHub)
- [ ] Beads task exists for this issue
- [ ] Context7 queried for relevant docs
- [ ] Root cause identified (not just symptom)
- [ ] Modified files reviewed with Read tool
- [ ] `npm run type-check` passes
- [ ] `npm run build` passes (or known pre-existing failures)
- [ ] GitHub issue closed with comment
- [ ] Beads task closed with reason

---

## Quick Commands Reference

```bash
# Fetch issues
gh issue list --state open --json number,title,labels,body

# View specific issue
gh issue view 123

# View issue with comments (IMPORTANT!)
gh issue view 123 --comments

# Get comments via API (structured)
gh api repos/maslennikov-ig/BuhBot/issues/123/comments

# Get comments as JSON for parsing
gh api repos/maslennikov-ig/BuhBot/issues/123/comments --jq '.[] | {author: .user.login, body: .body}'

# Search closed issues
gh issue list --state closed --search "keyword"

# Close issue with comment
gh issue close 123 --comment "Fixed in commit abc123"

# Add comment to issue
gh issue comment 123 --body "Analysis: ..."

# Create Beads task
bd create "Issue title" -t bug -p 1 --external-ref="gh-123"

# Search Beads
bd search "keyword"

# Close Beads task
bd close buh-xxx --reason="Fixed"
```

---

## Reference Docs

- CLAUDE.md: Main orchestration rules
- Beads Guide: `.claude/docs/beads-quickstart.md`
