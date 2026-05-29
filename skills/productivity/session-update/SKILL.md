---
name: session-update
description: Track progress with timestamps, git status, and todo list updates in current session
disable-model-invocation: true
---

## Token Optimization

This skill is inherently efficient due to its simple append-only workflow:

### 1. Minimal File Operations (Already Optimized)

**Pattern:** Append update to existing session file with Bash commands

```bash
# Append session update (200 tokens)
CURRENT_SESSION=$(cat .claude/sessions/.current-session 2>/dev/null)

cat >> "$CURRENT_SESSION" <<EOF

### Update - $(date '+%Y-%m-%d %H:%M')

**Summary**: $ARGUMENTS

**Git Changes**:
$(git status --porcelain | head -10)
$(git log -1 --oneline)

**Branch**: $(git branch --show-current)
EOF
```

**Token Usage:**
- Session file lookup: ~40 tokens
- Update template: ~100 tokens
- Git status commands: ~60 tokens
- **Total: ~200 tokens** (no optimization needed)

### 2. Early Exit for No Active Session (90% savings)

**Pattern:** Detect missing session immediately

```bash
# Quick check (80 tokens)
if [ ! -f ".claude/sessions/.current-session" ]; then
    echo "⚠️  No active session found"
    echo "   Start one with /session-start"
    exit 0  # 80 tokens total
fi

# Otherwise: Full update append (200 tokens)
```

**Savings:**
- No session: ~80 tokens (early exit)
- Full update: ~200 tokens
- **120 token savings (60%)** when no active session

### 3. Bash-Based Git Summary (No File Reads)

**Pattern:** Use git commands instead of reading changed files

```bash
# Bash-based git summary (60 tokens)
GIT_STATUS=$(git status --porcelain | head -10)
LAST_COMMIT=$(git log -1 --oneline)
BRANCH=$(git branch --show-current)

# Alternative: Read changed files (~300+ tokens)
# for file in $(git status --porcelain | awk '{print $2}'); do
#     Read "$file"  # 50-200 tokens per file
# done
```

**Token Usage:**
- Bash commands: ~60 tokens
- File reads: ~300+ tokens (reading changed files)
- Already optimized - **80% savings vs file reading**

### 4. Incremental TODO Status (Optional)

**Pattern:** Read TODO cache if available, skip if not

```bash
# Optional TODO status (100 tokens if available, 0 if not)
if [ -f ".claude/cache/todos/summary.json" ]; then
    TODO_STATUS=$(jq -r '.summary' .claude/cache/todos/summary.json)
    echo "**TODO Progress**: $TODO_STATUS"
fi

# Don't generate TODO status from scratch (would be 500+ tokens)
```

**Token Usage:**
- Cached TODO status: ~100 tokens
- Generate from scratch: ~500+ tokens
- **Skip if unavailable: 0 tokens** (graceful degradation)

### 5. Real-World Token Usage Distribution

**Typical Scenarios:**

1. **Standard Update (180-250 tokens)**
   - Session lookup: 40 tokens
   - Update template: 100 tokens
   - Git status: 60 tokens
   - TODO status (if cached): 100 tokens
   - **Total: ~300 tokens** (with TODO)
   - **Total: ~200 tokens** (without TODO)

2. **No Active Session - Early Exit (70-90 tokens)**
   - Session check: 40 tokens
   - Warning message: 40 tokens
   - **Total: ~80 tokens**

3. **Minimal Update (150-200 tokens)**
   - Session lookup: 40 tokens
   - Timestamp + message: 80 tokens
   - Git branch only: 30 tokens
   - **Total: ~150 tokens**

**Expected Token Usage:**
- **Baseline: 150-250 tokens** (already efficient)
- **Early exit: 80 tokens** (60% savings)
- **Average: ~200 tokens** (minimal overhead)

### Optimization Summary

| Strategy | Savings | When Applied |
|----------|---------|--------------|
| Minimal file operations | N/A | Already optimized |
| Early exit for no session | 120 tokens (60%) | No active session |
| Bash-based git summary | 240 tokens (80%) | Always (vs file reads) |
| Optional TODO status | 400 tokens (80%) | When cache unavailable |

**Key Insight:** This skill is already near-optimal at ~200 tokens due to its simple append workflow with Bash commands. No file reads are performed - only git commands and template appending. Early exit provides 60% savings when no session is active.

Update the current development session by:

1. Check if `.claude/sessions/.current-session` exists to find the active session
2. If no active session, inform user to start one with `/project:session-start`
3. If session exists, append to the session file with:
   - Current timestamp
   - The update: $ARGUMENTS (or if no arguments, summarize recent activities)
   - Git status summary:
     * Files added/modified/deleted (from `git status --porcelain`)
     * Current branch and last commit
   - Todo list status:
     * Number of completed/in-progress/pending tasks
     * List any newly completed tasks
   - Any issues encountered
   - Solutions implemented
   - Code changes made

Keep updates concise but comprehensive for future reference.

Example format:
```
### Update - 2025-06-16 12:15 PM

**Summary**: Implemented user authentication

**Git Changes**:
- Modified: app/middleware.ts, lib/auth.ts
- Added: app/login/page.tsx
- Current branch: main (commit: abc123)

**Todo Progress**: 3 completed, 1 in progress, 2 pending
- ✓ Completed: Set up auth middleware
- ✓ Completed: Create login page
- ✓ Completed: Add logout functionality

**Details**: [user's update or automatic summary]
```