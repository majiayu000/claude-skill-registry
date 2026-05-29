---
name: idea-issue-creator
description: Transform bullet points into enhanced, prioritized items for MASTER_PLAN.md. Process ideas inbox and integrate with project tracking.
triggers:
  - new issues
  - go over issues
  - process ideas
  - check inbox
  - ideas inbox
  - /task
  - create task
  - start task
  - mark task done
---

# 💡 Idea-Issue Creator - Simple Workflow

**Status**: Production Ready - Simple & Practical

---

## 🎯 What It Does

Transforms simple bullet points into enhanced, prioritized items for your master plan.

**Input**: Simple bullet points with #hashtags
**Output**: Enhanced items with priority scoring and master plan integration

---

## 🗣️ Quick Commands

When you say these phrases, Claude will automatically check the inbox:

| You Say | Claude Does |
|---------|-------------|
| "new issues" | Check `ideas-issues.md` inbox |
| "go over issues" | Check `ideas-issues.md` inbox |
| "process ideas" | Run the full processing workflow |
| "check inbox" | Read `ideas-issues.md` for new items |

---

## 📝 Simple Input Format

The skill reads from: `docs/planning-ideas-issues/overview/ideas-issues.md`

Add your bullet points to that file:

```
## Ideas
- #feature add dark mode toggle
- #improvement better keyboard shortcuts
- #integration sync with google calendar

## Issues
- #bug fix login page crashing on mobile
- #performance app is slow loading calendar
- #ux can't find where to export tasks
```

**No complex formatting** - just bullets and hashtags!

---

## 🚀 Simple Workflow

### Step 1: Process Ideas
```bash
idea-creator process-ideas
```
- Parses your simple bullet points
- Auto-categorizes and scores items
- Generates suggestions

### Step 2: Review Items
```bash
idea-creator review-ideas
```
- Shows all processed items
- Displays priority and impact scores
- Shows suggestions and clarifying questions

### Step 3: Approve & Integrate
```bash
idea-creator approve-all
```
- Approves all pending items
- Automatically adds to master plan
- Updates planning documents

---

## 🛠️ Commands

| Command | What It Does |
|---------|-------------|
| `process-ideas` | Parse and enhance ideas from file |
| `review-ideas` | Review pending items for approval |
| `ask-questions` | Interactive Q&A session |
| `approve-all` | Approve all items and add to master plan |
| `status` | Show current processing status |
| `help` | Show usage guide |

---

## 🎯 Smart Features

### Automatic Enhancement
- **Priority Scoring**: Calculates priority from hashtags and content
- **Impact Assessment**: 1-10 scoring for each item
- **Smart Suggestions**: 3 relevant suggestions per item
- **Categorization**: Auto-detects bugs vs features vs improvements

### Smart Questions
- **Scope Assessment**: "Small fix vs large feature?"
- **Technical Requirements**: "Simple or complex implementation?"
- **User Impact**: "Who benefits most from this?"

### Automatic Integration
- **Master Plan Updates**: Items added to appropriate sections
- **Safe Operations**: Backups before any changes
- **Smart Placement**: Issues vs Features vs Improvements

---

## 📊 Output Examples

### Input:
```
- #bug fix login page crashing
```

### After Processing:
```
📝 "fix login page crashing"
   Priority: HIGH | Impact: 8/10 | Category: issue
   Tags: #bug
   💡 Suggestions: Add proper error handling, Implement session timeout
   ❓ Questions: What is scope? (Small fix/Medium task/Large feature)
```

---

## 🎯 Success Metrics

- ✅ **5-minute workflow**: From input to master plan integration
- ✅ **No complex setup**: Just write bullet points
- ✅ **Automatic enhancement**: AI-powered suggestions and scoring
- ✅ **Smart questions**: Relevant clarifying questions
- ✅ **One-click approval**: Quick approval and integration
- ✅ **Always usable**: Simple enough for daily use

---

## 🚀 Quick Task Command (`/task`)

Fast task creation that adds directly to MASTER_PLAN.md and marks as in-progress.

### Create & Start Task
```
/task "Fix the login bug"
/task P0 "Critical: database down"
```

**What happens:**
1. Runs `scripts/utils/get-next-task-id.cjs` → gets next ID (e.g., TASK-304)
2. Adds row to MASTER_PLAN.md Roadmap table:
   | **TASK-304** | **Fix the login bug** | **P1** | 🔄 **IN PROGRESS** | - |
3. Outputs confirmation with task ID

**Default Priority:** P1-HIGH (override with P0, P2, P3 prefix)

### Mark Task Done
```
/task done TASK-304
```

**What happens:**
1. Finds task row in Roadmap table
2. Updates to: `~~TASK-304~~` | ... | ✅ **DONE** (YYYY-MM-DD)
3. Adds strikethrough to ID

### Implementation Notes
- **Table insertion**: Find last `| TASK-` or `| BUG-` row, insert after
- **ID regex**: `/(?:TASK|BUG|IDEA|ISSUE)-(\d+)/g`
- **Date format**: `YYYY-MM-DD` (e.g., 2026-01-16)
- **Priority values**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)

---

## 🔧 File Structure & Data Flow

### File Roles
| File | Role | Lifecycle |
|------|------|-----------|
| `docs/planning-ideas-issues/overview/ideas-issues.md` | **Inbox** | Add items → Process → Clear |
| `docs/MASTER_PLAN.md` | **Active Tracking** | Items added here for work tracking |
| `docs/archive/2025/week-XX/ideas-issues-batch-*.md` | **Historical Record** | Archived after processing |
| `.claude/ideas-processed.json` | **State** | Tracks processing status |

### Complete Workflow
```
1. ADD → ideas-issues.md (inbox)
2. PROCESS → Enhance with scoring & suggestions
3. APPROVE → Add to MASTER_PLAN.md
4. ARCHIVE → Move to docs/archive/...
5. CLEAR → Empty ideas-issues.md inbox
```

### Archive Location
Processed batches are archived to:
`docs/archive/2025/week-XX-MonDD-DD/ideas-issues-batch-YYYY-MM-DD.md`

---

## 💡 Pro Tips

### Writing Better Ideas
- **Be specific**: "fix login page" vs "improve auth system"
- **Use hashtags**: `#bug`, `#feature`, `#performance`, `#ux`
- **Combine contexts**: "improve #ux #performance of calendar"

### Hashtag Categories
- **Type**: `#bug`, `#feature`, `#improvement`
- **Priority**: `#urgent`, `#critical`, `#low-priority`
- **Technical**: `#api`, `#frontend`, `#backend`, `#database`
- **User**: `#ux`, `#accessibility`, `#mobile`

### Getting Started
1. Add your ideas to `docs/planning-ideas-issues/overview/ideas-issues.md`
2. Run `idea-creator process-ideas`
3. Review items with `idea-creator review-ideas`
4. Approve with `idea-creator approve-all`

---

## 🎉 Why This Works

**Simplicity over complexity**: Bullet points are faster than forms
**AI-powered insights**: Automatic enhancement saves you time
**Smart integration**: Master plan updates are automatic
**Practical workflow**: Actually usable for daily planning

---

**Result**: Your thoughts become actionable items in your master plan, automatically enhanced and prioritized.

**One command**: `idea-creator process-ideas && idea-creator approve-all`
**Total time**: ~2 minutes
**Complexity**: ZERO - just write bullet points

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
