---
description: Detects when user reports issues with recently completed work and suggests reopening relevant tasks or increments. Use when reporting bugs, regressions, or problems with recently finished features. Scans completed work from last 7 days and provides relevance-scored suggestions while checking WIP limits.
user-invocable: false
---

# Smart Reopen Detector

## Purpose

When you report an issue with recently completed work, I'll automatically:
1. 🔍 **Scan your recent work** (active + completed in last 7 days)
2. 🎯 **Identify related items** using keyword matching
3. 💡 **Suggest what to reopen** with relevance scoring
4. ⚠️  **Check WIP limits** before suggesting reopen

## When I Activate

I automatically activate when you mention these keywords:
- **Not working**: "not working", "broken", "failing", "error", "crash"
- **Quality issues**: "bug", "issue", "problem", "wrong", "incorrect", "missing"
- **Regressions**: "still broken", "regression", "broken again", "came back"

## How I Help

### Example 1: Issue Report
```
User: "The GitHub sync isn't working, it was just completed yesterday"
```

I'll respond with:
```
🔍 Scanning recent work...

Found 2 related item(s) in recent work:

📦 INCREMENT: 0031-external-tool-status-sync
   Increment: 0031-external-tool-status-sync
   Completed: 2 days ago
   Relevance: 15 points
   Matched: github, sync

✓ TASK: T-003 GitHub Content Sync
   Increment: 0031-external-tool-status-sync
   Completed: 1 day ago
   Relevance: 14 points
   Matched: github, sync

💡 Suggested action:
   /sw:reopen 0031-external-tool-status-sync --reason "GitHub sync not working"

Would you like me to:
1. Reopen the entire increment (checks WIP limits)
2. Reopen just task T-003 (targeted fix)
3. Show me the WIP status first
```

### Example 2: Specific Feature Broken
```
User: "The authentication is broken after the recent deployment"
```

I'll respond with:
```
🔍 Scanning recent work...

Found 3 related item(s) in recent work:

✓ TASK: T-012 Authentication Service
   Increment: 0025-user-auth
   Completed: 3 days ago
   Relevance: 10 points
   Matched: authentication

✓ TASK: T-014 JWT Token Validation
   Increment: 0025-user-auth
   Completed: 3 days ago
   Relevance: 7 points
   Matched: authentication

💡 Suggested action:
   /sw:reopen 0025-user-auth --task T-012 --reason "Authentication broken after deployment"

⚠️  Note: Increment 0025 was completed 3 days ago. Consider checking deployment config first.
```

### Example 3: No Recent Work Found
```
User: "The payment flow is not working"
```

I'll respond with:
```
🔍 Scanning recent work...

🔍 No related work found in recent activity (last 7 days)

The payment functionality might be:
1. From an older increment (>7 days ago)
2. Not yet implemented
3. Part of external dependencies

Would you like me to:
1. Search all increments (not just recent)
2. Create a new bug increment for investigation
3. Check the backlog for related work
```

## What I Do

### Step 1: Extract Keywords
From your message, I extract relevant keywords:
- Feature names (authentication, github, payment)
- Action words (sync, deploy, validate)
- Component names (api, database, frontend)

### Step 2: Scan Recent Work
I scan:
- ✅ **Active increments** (currently being worked on)
- ✅ **Recently completed** (last 7 days)
- ✅ **All tasks** from these increments

### Step 3: Score Matches
I assign relevance scores using:
- **+10 points**: Exact match in title/ID
- **+7 points**: Partial match in title
- **+5 points**: Match in increment ID
- **+3 points**: Match in description/AC

### Step 4: Suggest Actions
I provide:
- Top matches (up to 5)
- Relevance scores
- Suggested `/sw:reopen` command
- WIP limit warnings (if applicable)

## Smart Suggestions

### For Increments
```bash
# Reopen entire increment
/sw:reopen 0031-external-tool-status-sync --reason "GitHub sync failing"

# Check WIP limits first (recommended)
/sw:status
```

### For Specific Tasks
```bash
# Reopen single task (surgical fix)
/sw:reopen 0031 --task T-003 --reason "GitHub API 500 error"

# Reopen multiple related tasks
/sw:reopen 0031 --user-story US-001 --reason "All GitHub features broken"
```

### Force Reopen (Bypass WIP Limits)
```bash
# Use --force for critical production issues
/sw:reopen 0031 --force --reason "Production down, critical fix needed"
```

## WIP Limit Awareness

Before suggesting increment reopen, I check:
- ✅ Current active increment count
- ✅ Type-specific limits (feature: 2, refactor: 1, etc.)
- ⚠️  Warn if reopening will exceed limits

**Example Warning**:
```
⚠️  WIP LIMIT WARNING:
   Current active: 2 features
   Limit: 2 features
   Reopening 0031-external-tool-status-sync will EXCEED the limit!

   Options:
   1. Pause another feature first: /sw:pause 0030
   2. Complete another feature: /sw:done 0029
   3. Force reopen (not recommended): --force
```

## Integration with Commands

I work seamlessly with:
- `/sw:reopen` - Execute reopen action
- `/sw:status` - Check WIP limits
- `/sw:progress` - See increment progress
- `/sw:pause` - Pause another increment to make room

## When NOT to Use

I don't activate for:
- ❌ General questions about code
- ❌ Feature requests (use `/sw:increment`)
- ❌ Documentation questions
- ❌ Status inquiries (use `/sw:status`)

I **only** activate when you explicitly report something is broken/not working.

## Technical Implementation

**Core Logic**:
- Uses `RecentWorkScanner` to find matches
- Keyword extraction from user message
- Relevance scoring algorithm
- WIP limit validation before suggestions

**Smart Features**:
- Deduplication (same increment from active + recent)
- Recency bias (prefer more recent completions)
- Contextual hints (deployment, config, dependencies)

## Examples of Activation

### ✅ Will Activate
- "GitHub sync not working"
- "Authentication is broken"
- "Tests are failing after the last commit"
- "Deployment crashed"
- "API returns 500 error"
- "Still broken after the fix"

### ❌ Won't Activate
- "How does GitHub sync work?"
- "Can you add authentication?"
- "What's the status of increment 0031?"
- "Show me the progress"
- "Create a new feature for payments"

## Success Metrics

I'm successful when:
- ✅ You find the related work quickly (<30 seconds)
- ✅ The suggested reopen command is correct
- ✅ No false positives (only relevant matches)
- ✅ WIP limits are respected
- ✅ Clear next steps provided

---

**Auto-loads when**: You report issues with recently completed work
**Commands**: `/sw:reopen`, `/sw:status`
**Related Skills**: `increment-planner`, `tdd-workflow`

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/smart-reopen-detector.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

