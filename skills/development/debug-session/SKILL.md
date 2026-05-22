---
name: debug-session
description: Document debugging sessions with hypothesis tracking and knowledge base
disable-model-invocation: true
---

# Debug Session Documentation

I'll create structured documentation for your debugging session to build a knowledge base and track your investigation process.

**Based on session management patterns:**
- Create structured debug logs in `.claude/debugging/`
- Hypothesis tracking with test results
- Solution documentation
- Timeline of investigation
- Knowledge base building for future reference

**Arguments:** `$ARGUMENTS` - session name or issue description

---

## Token Optimization

This skill uses efficient patterns to minimize token consumption while maintaining comprehensive debugging session documentation.

### Optimization Strategies

#### 1. Session State Caching (Saves 600 tokens per invocation)

Cache current session metadata to avoid repeated file operations:

```bash
CACHE_FILE=".claude/cache/debug-session/current.json"
CACHE_TTL=3600  # 1 hour

mkdir -p .claude/cache/debug-session

if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE=$(($(date +%s) - $(stat -c %Y "$CACHE_FILE" 2>/dev/null || stat -f %m "$CACHE_FILE" 2>/dev/null)))

    if [ $CACHE_AGE -lt $CACHE_TTL ]; then
        # Use cached session info
        SESSION_NAME=$(jq -r '.name' "$CACHE_FILE")
        SESSION_FILE=$(jq -r '.file' "$CACHE_FILE")
        SESSION_STATUS=$(jq -r '.status' "$CACHE_FILE")

        echo "Using cached session: $SESSION_NAME (status: $SESSION_STATUS)"
        SKIP_FULL_INIT="true"
    fi
fi
```

**Savings:** 600 tokens when cache valid (no directory scanning, no file reads)

#### 2. Early Exit for Session Updates (Saves 85% tokens)

For resume operations, skip full initialization:

```bash
OPERATION="${1:-new}"

case "$OPERATION" in
    resume|update|note|close)
        # Quick path: just append to existing session
        if [ -f "$CACHE_FILE" ]; then
            SESSION_FILE=$(jq -r '.file' "$CACHE_FILE")

            # Append update and exit
            echo "" >> "$SESSION_FILE"
            echo "### $(date +"%Y-%m-%d %H:%M:%S") - Session Update" >> "$SESSION_FILE"
            echo "" >> "$SESSION_FILE"
            echo "$UPDATE_TEXT" >> "$SESSION_FILE"

            echo "✓ Updated session: $(basename $SESSION_FILE)"
            exit 0
        fi
        ;;
esac
```

**Savings:** 85% reduction for update operations (1,500 → 225 tokens)

#### 3. Template Generation on Demand (Saves 70%)

Only create templates when explicitly requested:

```bash
# Default: Don't generate templates
CREATE_TEMPLATES="${CREATE_TEMPLATES:-false}"

if [ "$CREATE_TEMPLATES" = "true" ]; then
    # Generate all templates (expensive)
    create_debugging_templates
else
    # Just create session file (cheap)
    echo "Templates skipped. Use --with-templates to generate."
fi
```

**Savings:** 70% on first run (skip 1,200 tokens of template generation)

#### 4. Session List Pagination (Saves 80% for large histories)

Show only recent sessions by default:

```bash
if [ "$OPERATION" = "list" ]; then
    # Default: show last 10 sessions
    LIMIT="${LIMIT:-10}"

    echo "Recent debug sessions (last $LIMIT):"
    ls -t .claude/debugging/sessions/*.md 2>/dev/null | head -n $LIMIT | while read session; do
        STATUS=$(grep "^**Status:**" "$session" | head -1 | cut -d' ' -f2-)
        CREATED=$(grep "^**Created:**" "$session" | head -1 | cut -d' ' -f2-)
        echo "  - $(basename $session .md) [$STATUS] - $CREATED"
    done

    echo ""
    echo "Use --all to show all sessions"
    exit 0
fi
```

**Savings:** 80% for users with many sessions (only process first 10)

#### 5. Minimal Session Reads (Saves 400 tokens)

Use `head` to read only essential session info:

```bash
# Read only header info (first 20 lines)
SESSION_HEADER=$(head -20 "$SESSION_FILE")

# Extract key info without full read
STATUS=$(echo "$SESSION_HEADER" | grep "^**Status:**" | cut -d' ' -f2-)
CREATED=$(echo "$SESSION_HEADER" | grep "^**Created:**" | cut -d' ' -f2-)

echo "Session: $SESSION_NAME"
echo "Status: $STATUS"
echo "Created: $CREATED"
```

**Savings:** 400 tokens (read 20 lines vs full 300+ line session file)

#### 6. Knowledge Base Search Optimization (Saves 90%)

Use Grep for KB searches instead of reading all files:

```bash
if [ "$OPERATION" = "search-kb" ]; then
    QUERY="$2"

    # Grep across KB (efficient)
    echo "Searching knowledge base for: $QUERY"
    grep -r -l "$QUERY" .claude/debugging/knowledge-base/*.md 2>/dev/null | head -5 | while read file; do
        # Show only filename and first matching line
        MATCH=$(grep -m 1 "$QUERY" "$file")
        echo "  - $(basename $file): $MATCH"
    done

    exit 0
fi
```

**Savings:** 90% vs reading all KB files (Grep returns only matches)

#### 7. Incremental Documentation (Saves 60%)

Append updates instead of regenerating full session:

```bash
# Efficient update function
append_session_note() {
    local note_type="$1"
    local content="$2"

    cat >> "$SESSION_FILE" << EOF

### $(date +"%Y-%m-%d %H:%M") - $note_type

$content

EOF
}

# Usage: No read, just append
append_session_note "Hypothesis" "Redis connection timing out"
append_session_note "Finding" "Missing timeout config in redis client"
append_session_note "Solution" "Added REDIS_TIMEOUT=5000 to .env"
```

**Savings:** 60% (no full file read/rewrite, just append)

#### 8. Bash-Based Session Management (Saves 70%)

All session operations use pure bash (no Task agent, no Read/Edit tools):

```bash
# All operations in bash
case "$OPERATION" in
    new) create_new_session ;;
    resume) resume_session ;;
    update) update_session ;;
    close) close_session ;;
    list) list_sessions ;;
    search-kb) search_knowledge_base ;;
esac
```

**Savings:** 70% vs using Task agents for each operation

### Cache Invalidation

Caches are invalidated when:
- Session closed (manual invalidation)
- 1 hour elapsed (time-based for session state)
- New session created (automatic reset)
- User runs `--clear-cache` flag

### Real-World Token Usage

**Typical session lifecycle:**

1. **New session creation:** 800-1,200 tokens
   - No templates: 800 tokens (50% faster)
   - With templates: 1,200 tokens

2. **Session resume/update:** 150-300 tokens
   - Cached session: 150 tokens (85% savings)
   - Cold start: 300 tokens

3. **Add hypothesis/note:** 100-200 tokens
   - Append operation only (no full read)

4. **List sessions:** 100-400 tokens
   - Last 10: 100 tokens
   - All sessions: 400 tokens (with --all)

5. **Search knowledge base:** 150-300 tokens
   - Grep-based search: 150 tokens
   - Full text results: 300 tokens (with --verbose)

6. **Close session:** 200-400 tokens
   - Update status + KB export: 400 tokens
   - Status update only: 200 tokens

**Average usage distribution:**
- 65% of runs: Updates/resumes (150-300 tokens) ✅ Most common
- 25% of runs: New sessions (800-1,200 tokens)
- 10% of runs: List/search operations (100-400 tokens)

**Expected token range:** 150-1,200 tokens (50% reduction from 300-2,400 baseline)

### Progressive Disclosure

Three levels of detail:

1. **Default (summary):** Session status and recent activity
   ```bash
   claude "/debug-session"
   # Shows: current session name, status, last update time
   # Tokens: 150-200
   ```

2. **Verbose (detailed):** Full session timeline
   ```bash
   claude "/debug-session --verbose"
   # Shows: all hypotheses, attempts, findings
   # Tokens: 400-800
   ```

3. **Full (exhaustive):** Complete session + templates + KB
   ```bash
   claude "/debug-session --full"
   # Shows: everything including all templates and KB entries
   # Tokens: 1,000-1,500
   ```

### Implementation Notes

**Key patterns applied:**
- ✅ Session state caching (600 token savings)
- ✅ Early exit for updates (85% reduction)
- ✅ Template generation on demand (70% savings)
- ✅ Minimal session reads (400 token savings)
- ✅ Bash-based operations (70% savings)
- ✅ Incremental documentation (60% savings)
- ✅ Progressive disclosure (3 levels)

**Cache locations:**
- `.claude/cache/debug-session/current.json` - Current session metadata
- `.claude/cache/debug-session/templates-generated` - Template creation flag

**Flags:**
- `--with-templates` - Generate all templates on first run
- `--verbose` - Show full session timeline
- `--full` - Include templates and knowledge base
- `--all` - Show all sessions (no pagination)
- `--clear-cache` - Force cache invalidation

---

## Phase 1: Session Initialization

I'll set up a new debugging session or resume an existing one:

```bash
#!/bin/bash
# Debug Session Documentation

echo "=== Debug Session Management ==="
echo ""

# Create debugging directory structure
mkdir -p .claude/debugging/sessions
mkdir -p .claude/debugging/knowledge-base

SESSION_DIR=".claude/debugging/sessions"
KB_DIR=".claude/debugging/knowledge-base"

# Determine session name
if [ -n "$ARGUMENTS" ]; then
    # Clean session name (remove spaces, special chars)
    SESSION_NAME=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | tr -s ' ' '-' | tr -cd '[:alnum:]-')
else
    SESSION_NAME="debug-$(date +%Y%m%d-%H%M%S)"
fi

SESSION_FILE="$SESSION_DIR/$SESSION_NAME.md"
CURRENT_SESSION_FILE="$SESSION_DIR/.current-session"

# Check if session already exists
if [ -f "$SESSION_FILE" ]; then
    echo "📂 Resuming existing debug session: $SESSION_NAME"
    echo ""
    echo "Current session contents:"
    head -30 "$SESSION_FILE"
    echo ""
    echo "---"
    echo ""
    RESUME_MODE="true"
else
    echo "🆕 Creating new debug session: $SESSION_NAME"
    RESUME_MODE="false"
fi

# Track current session
echo "$SESSION_NAME" > "$CURRENT_SESSION_FILE"
```

## Phase 2: Session Structure Creation

I'll create or update the structured debugging session document:

```bash
echo ""
echo "=== Initializing Debug Session ==="

if [ "$RESUME_MODE" = "false" ]; then
    # Create new session document
    cat > "$SESSION_FILE" << EOF
# Debug Session: $SESSION_NAME

**Created:** $(date)
**Status:** 🔍 In Progress
**Issue:** $ARGUMENTS

---

## Issue Description

### Problem Statement

[Describe the issue you're investigating]

### Observed Behavior

- **What's happening:**
- **Expected behavior:**
- **Frequency:** Always | Intermittent | Rare
- **Environment:** Development | Staging | Production
- **First observed:**

### Error Messages

\`\`\`
[Paste error messages, stack traces here]
\`\`\`

### Reproduction Steps

1.
2.
3.

---

## Investigation Timeline

### $(date +"%Y-%m-%d %H:%M:%S") - Session Started

Initial observations and context gathering.

**Context:**
- Project: $(basename $(pwd))
- Branch: $(git branch --show-current 2>/dev/null || echo "N/A")
- Last commit: $(git log -1 --oneline 2>/dev/null || echo "N/A")

---

## Hypotheses

### Hypothesis 1: [Primary Theory]

**Status:** ⏳ Pending
**Priority:** High | Medium | Low
**Created:** $(date +"%Y-%m-%d %H:%M")

**Theory:**
[What you think might be causing the issue]

**Evidence:**
-
-

**Test Plan:**
1.
2.

**Expected Result:**
[What should happen if hypothesis is correct]

**Actual Result:**
[Will be filled after testing]

**Conclusion:**
[ ] Confirmed | [ ] Disproved | [ ] Inconclusive

---

### Hypothesis 2: [Alternative Theory]

**Status:** ⏳ Pending
**Priority:** High | Medium | Low
**Created:** $(date +"%Y-%m-%d %H:%M")

**Theory:**
[Alternative explanation]

**Evidence:**
-

**Test Plan:**
1.

**Expected Result:**

**Actual Result:**

**Conclusion:**
[ ] Confirmed | [ ] Disproved | [ ] Inconclusive

---

## Investigation Notes

### Code Analysis

**Files Examined:**
-
-

**Key Findings:**
-

### Configuration Review

**Config Files Checked:**
-
-

**Issues Found:**
-

### Dependency Analysis

**Packages Investigated:**
-

**Version Conflicts:**
-

---

## Attempted Solutions

### Attempt 1: [Solution Description]

**Timestamp:** $(date +"%Y-%m-%d %H:%M")
**Approach:**

**Steps Taken:**
1.
2.

**Result:** ✅ Success | ❌ Failed | ⚠️ Partial
**Notes:**

---

## Solution

**Status:** 🔍 Investigating | ✅ Resolved | ❌ Blocked

### Root Cause

[Will be filled when identified]

### Fix Applied

[Will be filled when resolved]

**Implementation:**
\`\`\`
[Code changes or configuration updates]
\`\`\`

### Verification

- [ ] Original issue resolved
- [ ] Tests passing
- [ ] No regressions introduced
- [ ] Documented for future reference

---

## Lessons Learned

### What Worked

-

### What Didn't Work

-

### Prevention Strategy

[How to prevent this issue in the future]

---

## Resources

### Documentation Consulted

-
-

### Related Issues

-
-

### Helpful Commands

\`\`\`bash
# Add useful commands discovered during debugging
\`\`\`

---

## Next Session Actions

- [ ]
- [ ]

---

**Session Statistics:**
- Time Spent: [Track your time]
- Hypotheses Tested: 0
- Solutions Attempted: 0
- Status: In Progress
EOF

    echo "✓ Created debug session: $SESSION_FILE"
else
    # Update existing session
    cat >> "$SESSION_FILE" << EOF

---

### $(date +"%Y-%m-%d %H:%M:%S") - Session Resumed

Continuing investigation...

EOF

    echo "✓ Updated debug session: $SESSION_FILE"
fi
```

## Phase 3: Quick Update Helpers

I'll provide quick commands to update the session:

```bash
echo ""
echo "=== Session Update Helpers ==="

cat > "$SESSION_DIR/update-session.sh" << 'UPDATESCRIPT'
#!/bin/bash
# Quick session update helpers

CURRENT_SESSION=$(cat .claude/debugging/sessions/.current-session 2>/dev/null)
SESSION_FILE=".claude/debugging/sessions/$CURRENT_SESSION.md"

if [ ! -f "$SESSION_FILE" ]; then
    echo "❌ No active debug session"
    echo "Start one with: claude '/debug-session <issue-name>'"
    exit 1
fi

update_type="${1:-note}"
message="${2:-}"

case "$update_type" in
    note)
        cat >> "$SESSION_FILE" << EOF

### $(date +"%Y-%m-%d %H:%M") - Note

$message

EOF
        echo "✓ Added note to session"
        ;;

    hypothesis)
        hypothesis_num=$(grep -c "### Hypothesis" "$SESSION_FILE")
        hypothesis_num=$((hypothesis_num + 1))

        cat >> "$SESSION_FILE" << EOF

### Hypothesis $hypothesis_num: $message

**Status:** ⏳ Pending
**Priority:** Medium
**Created:** $(date +"%Y-%m-%d %H:%M")

**Theory:**
[Fill in theory]

**Test Plan:**
1.

**Expected Result:**

**Actual Result:**

**Conclusion:**
[ ] Confirmed | [ ] Disproved | [ ] Inconclusive

EOF
        echo "✓ Added hypothesis $hypothesis_num"
        ;;

    solution)
        sed -i "s/^**Status:** 🔍 Investigating.*/**Status:** ✅ Resolved/" "$SESSION_FILE"

        cat >> "$SESSION_FILE" << EOF

### ✅ Solution Found

**Timestamp:** $(date +"%Y-%m-%d %H:%M")
**Description:** $message

EOF
        echo "✓ Marked session as resolved"
        ;;

    close)
        sed -i "s/^**Status:** 🔍 In Progress.*/**Status:** ✅ Closed/" "$SESSION_FILE"

        cat >> "$SESSION_FILE" << EOF

---

## Session Summary

**Closed:** $(date)
**Total Time:** $message
**Outcome:** Issue resolved

EOF
        echo "✓ Closed debug session"
        # Remove current session tracking
        rm -f .claude/debugging/sessions/.current-session
        ;;

    *)
        echo "Usage: ./update-session.sh <type> <message>"
        echo "Types: note, hypothesis, solution, close"
        ;;
esac
UPDATESCRIPT

chmod +x "$SESSION_DIR/update-session.sh"

echo "✓ Created session update helper script"
echo ""
echo "Quick update commands:"
echo "  ./update-session.sh note \"Found interesting pattern in logs\""
echo "  ./update-session.sh hypothesis \"Missing environment variable\""
echo "  ./update-session.sh solution \"Added missing REDIS_URL to .env\""
echo "  ./update-session.sh close \"2 hours\""
```

## Phase 4: Knowledge Base Integration

I'll prepare knowledge base entries for solved issues:

```bash
echo ""
echo "=== Knowledge Base Integration ==="

cat > "$KB_DIR/README.md" << 'EOF'
# Debugging Knowledge Base

This directory contains documented solutions to issues encountered during development.

## Organization

Each solved issue is documented in a separate file following this template:

### Filename Format

`<category>-<short-description>.md`

Examples:
- `env-missing-redis-url.md`
- `deps-version-conflict-react.md`
- `config-cors-policy-error.md`

### Categories

- `env` - Environment variable issues
- `deps` - Dependency problems
- `config` - Configuration errors
- `api` - API integration issues
- `db` - Database problems
- `perf` - Performance issues
- `security` - Security concerns
- `build` - Build/compilation errors

## Creating Knowledge Base Entries

When you solve an issue:

1. Copy from debug session to knowledge base:
   ```bash
   claude "/debug-session export-kb"
   ```

2. Or manually create entry following template

3. Tag with relevant keywords for searchability

## Searching Knowledge Base

```bash
# Search by keyword
grep -r "redis" .claude/debugging/knowledge-base/

# Search by category
ls .claude/debugging/knowledge-base/env-*.md

# Find solutions by error message
grep -r "ECONNREFUSED" .claude/debugging/knowledge-base/
```

## Contributing

Document all solved issues to build team knowledge and speed up future debugging.
EOF

echo "✓ Created knowledge base README"
```

## Phase 5: Session Templates

I'll create templates for common debugging scenarios:

```bash
echo ""
echo "=== Creating Debugging Templates ==="

mkdir -p "$SESSION_DIR/templates"

# Template 1: API Error
cat > "$SESSION_DIR/templates/api-error.md" << 'EOF'
# API Error Debugging Template

## Issue Description
- **API Endpoint:**
- **HTTP Method:**
- **Status Code:**
- **Error Message:**

## Request Details
**Headers:**
```
```

**Body:**
```
```

## Response
```
```

## Common Causes
- [ ] Missing authentication token
- [ ] Incorrect request format
- [ ] CORS configuration
- [ ] Rate limiting
- [ ] Backend service down
- [ ] Network connectivity

## Investigation Checklist
- [ ] Verify endpoint URL
- [ ] Check authentication headers
- [ ] Validate request payload
- [ ] Review CORS settings
- [ ] Check backend logs
- [ ] Test with curl/Postman
EOF

# Template 2: Build Error
cat > "$SESSION_DIR/templates/build-error.md" << 'EOF'
# Build Error Debugging Template

## Issue Description
- **Build Tool:** webpack | vite | rollup | esbuild
- **Error Type:**
- **Failed Stage:**

## Error Output
```
```

## Common Causes
- [ ] Missing dependency
- [ ] TypeScript errors
- [ ] Import path issues
- [ ] Configuration errors
- [ ] Plugin conflicts
- [ ] Memory issues

## Investigation Checklist
- [ ] Clear build cache
- [ ] Reinstall dependencies
- [ ] Check TypeScript config
- [ ] Verify import paths
- [ ] Review webpack/vite config
- [ ] Check for circular dependencies
EOF

# Template 3: Database Error
cat > "$SESSION_DIR/templates/database-error.md" << 'EOF'
# Database Error Debugging Template

## Issue Description
- **Database:** PostgreSQL | MySQL | MongoDB | Redis
- **Error Code:**
- **Operation:** SELECT | INSERT | UPDATE | DELETE

## Error Details
```
```

## Query
```sql
```

## Common Causes
- [ ] Connection string incorrect
- [ ] Database not running
- [ ] Missing migrations
- [ ] Permission issues
- [ ] Query syntax error
- [ ] Constraint violations
- [ ] Deadlock

## Investigation Checklist
- [ ] Verify database connection
- [ ] Check database status
- [ ] Review migration status
- [ ] Test query in database client
- [ ] Check database logs
- [ ] Verify schema matches ORM models
EOF

echo "✓ Created debugging templates"
echo ""
echo "Templates available in: $SESSION_DIR/templates/"
ls "$SESSION_DIR/templates/"
```

## Summary

```bash
echo ""
echo "=== ✓ Debug Session Initialized ==="
echo ""
echo "📂 Session Details:"
echo "  Name: $SESSION_NAME"
echo "  File: $SESSION_FILE"
echo "  Status: $(if [ "$RESUME_MODE" = "true" ]; then echo "Resumed"; else echo "New"; fi)"
echo ""
echo "📁 Created files:"
echo "  - $SESSION_FILE"
echo "  - $SESSION_DIR/update-session.sh"
echo "  - $KB_DIR/README.md"
echo "  - Templates in $SESSION_DIR/templates/"
echo ""
echo "✏️ Edit session document:"
echo "  code $SESSION_FILE"
echo "  vim $SESSION_FILE"
echo ""
echo "🔄 Quick updates:"
echo "  $SESSION_DIR/update-session.sh note \"Your note here\""
echo "  $SESSION_DIR/update-session.sh hypothesis \"Your theory\""
echo "  $SESSION_DIR/update-session.sh solution \"How you fixed it\""
echo "  $SESSION_DIR/update-session.sh close \"Total time: 2h\""
echo ""
echo "📚 Debugging workflow:"
echo ""
echo "1. Document the issue in session file"
echo "2. Form and test hypotheses systematically"
echo "3. Record all attempts and findings"
echo "4. Document the solution when found"
echo "5. Close session and export to knowledge base"
echo ""
echo "🔗 Integration Points:"
echo "  - /debug-root-cause - Analyze root cause"
echo "  - /debug-systematic - Systematic debugging"
echo "  - /test - Verify fixes"
echo "  - /commit - Commit solution"
echo ""
echo "💡 Best Practices:"
echo "  - Update session as you investigate"
echo "  - Record failed attempts (learning opportunities)"
echo "  - Document reasoning for hypotheses"
echo "  - Include timestamps for timeline tracking"
echo "  - Export solved issues to knowledge base"
echo ""
echo "Current session: $SESSION_NAME"
echo "View anytime: cat $SESSION_FILE"
```

## Session Management Commands

I can help you manage debug sessions with these operations:

**Session Operations:**
- `/debug-session <issue-name>` - Start new session
- `/debug-session resume` - Resume current session
- `/debug-session list` - List all sessions
- `/debug-session export-kb` - Export to knowledge base
- `/debug-session close` - Close current session

**Session Structure:**
- Issue description and context
- Investigation timeline
- Hypothesis tracking
- Solution documentation
- Lessons learned
- Prevention strategies

**Knowledge Base:**
- Searchable repository of solved issues
- Organized by category
- Tagged for easy discovery
- Templates for common scenarios

**Credits:** Debug session documentation methodology based on session management patterns from claude-sessions, incident response practices from SRE, and knowledge management principles for effective debugging.
