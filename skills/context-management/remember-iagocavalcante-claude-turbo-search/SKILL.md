---
name: remember
description: Save the current work session to persistent memory for future context. Summarizes accomplishments, tracks files modified, and stores learnings for cross-session continuity.
---

# /remember - Save Session to Memory

Summarize the current work session and save it to persistent memory for future context.

## Instructions

When the user invokes `/remember`, you should:

### 1. Check for Activity Log

First, check if there's an activity log from this session:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "$PWD")
ACTIVITY_FILE="$REPO_ROOT/.claude-memory/activity.log"
if [ -f "$ACTIVITY_FILE" ]; then
    cat "$ACTIVITY_FILE"
fi
```

### 2. Analyze the Session

Review what was accomplished in this conversation:
- What files were read, created, or modified?
- What was the main goal or task?
- What key decisions were made?
- Were there any important patterns or learnings?

### 2.5. Compression Guidelines

When writing summaries, facts, or knowledge entries, follow these rules to maximize information density:

- **Resolve pronouns to concrete entities**: Write "JWT middleware validates tokens" not "it validates them"
- **Use absolute file paths**: Write "src/auth/middleware.ts" not "this file" or "the auth file"
- **Write dense, self-contained summaries**: Each memory entry should be understandable without the original conversation context
- **Avoid filler phrases**: Do not use "I think", "basically", "sort of", "actually" — state facts directly
- **Use ISO dates**: Write "2026-02-11" not "today" or "yesterday" — temporal references decay quickly

The system automatically compresses text at write time (normalizing dates, stripping filler), but writing clean summaries upfront produces better results.

### 3. Generate Summary

Create a concise summary (2-3 sentences) that captures:
- **What** was done (the main accomplishment)
- **Why** it matters (the purpose or problem solved)
- **Key details** (important files, patterns, or decisions)

### 4. Extract Metadata

Identify:
- **Files touched**: List of file paths worked on
- **Topics**: 3-5 keywords for searchability (e.g., "auth, jwt, middleware, security")
- **Tools used**: Main tools used (Read, Write, Edit, Bash, etc.)

### 5. Save to Memory

Use the memory-db.sh script to save:

```bash
PLUGIN_DIR="${PLUGIN_DIR:-$HOME/claude-turbo-search}"
MEMORY_SCRIPT="$PLUGIN_DIR/memory/memory-db.sh"

# Initialize if needed
"$MEMORY_SCRIPT" init

# Save session
"$MEMORY_SCRIPT" add-session \
    "YOUR_SUMMARY_HERE" \
    '["file1.ts", "file2.ts"]' \
    '["Read", "Edit", "Bash"]' \
    "topic1, topic2, topic3"
```

### 6. Optionally Add Knowledge or Facts

If during the session you learned something important about the codebase that should be remembered:

**For code area knowledge:**
```bash
"$MEMORY_SCRIPT" add-knowledge \
    "src/auth" \
    "Authentication module using JWT tokens with refresh token rotation" \
    "Tokens expire in 15min, refresh tokens in 7 days"
```

**For project facts:**
```bash
"$MEMORY_SCRIPT" add-fact "Uses PostgreSQL with Prisma ORM" "architecture"
"$MEMORY_SCRIPT" add-fact "All API routes require authentication except /health" "convention"
```

### 7. Clear Activity Log

After saving, clear the activity log:

```bash
ACTIVITY_FILE="$REPO_ROOT/.claude-memory/activity.log"
[ -f "$ACTIVITY_FILE" ] && rm "$ACTIVITY_FILE"
```

### 8. Confirm to User

Report what was saved:

```
Saved to memory:
- Summary: [your summary]
- Topics: [topics]
- Files: [count] files tracked

Memory now contains [X] sessions. Use /memory-stats to see details.
```

## Example Output

```
Saved to memory:
- Summary: Implemented JWT authentication with refresh token rotation. Added middleware for protected routes and updated user model with token fields.
- Topics: auth, jwt, middleware, tokens, security
- Files: 4 files tracked

Memory now contains 12 sessions.
```

## Additional Commands

If the user wants to add specific knowledge or facts, they can say:
- "Remember that this project uses X" -> Add as fact
- "Remember how the auth module works" -> Add as knowledge

Ask clarifying questions if the summary scope is unclear.
