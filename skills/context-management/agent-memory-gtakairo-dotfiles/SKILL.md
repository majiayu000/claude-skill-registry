---
name: agent-memory
description: "Retain and recall work context across sessions. Use when user asks to remember something, recall previous work, or reference past discussions. Triggered by phrases like 'remember this', 'save for later', 'recall', 'what did we discuss about'."
enabled: true
visibility: default
allowedTools: ["read", "write", "grep", "glob", "bash"]
---

# Agent Memory Skill

Enable context retention across Claude Code sessions by saving and recalling work memories.

## Purpose

This skill allows Claude to:
- **Remember** important context, decisions, and work items
- **Recall** previous discussions and findings
- **Maintain continuity** across multiple sessions
- **Reduce repetition** by referencing past work

## When to Use

Automatically triggered by phrases like:
- "Remember this for later"
- "Save this information"
- "Recall what we discussed about X"
- "What was our approach for Y?"
- "Retrieve memory about Z"

## Memory Operations

### 1. Saving Memories

When the user asks to remember something, create a new memory file:

**Process**:
1. Identify the topic/context to remember
2. Generate a descriptive memory ID (e.g., `issue-123`, `feature-auth`, `bug-database`)
3. Create markdown file in `memories/` directory
4. Include YAML frontmatter with metadata
5. Write detailed context in markdown body

**File Format**:
```yaml
---
summary: "Brief one-line description"
topic: "Main topic or feature"
created: "2026-01-14"
tags: ["tag1", "tag2"]
related: ["other-memory-id"]
---

# Detailed Context

## Background
[What led to this discussion]

## Key Points
- Important point 1
- Important point 2
- Decision made

## Next Steps
- [ ] Action item 1
- [ ] Action item 2

## References
- File: `src/module.js:42`
- PR: #123
- Issue: #456
```

**Example Memory Creation**:
```bash
# Create memory file
cat > .claude/skills/agent-memory/memories/database-migration.md << 'EOF'
---
summary: "Database migration strategy for user profiles"
topic: "database"
created: "2026-01-14"
tags: ["database", "migration", "users"]
---

# Database Migration Strategy

## Context
We need to add a `preferences` column to the users table to support
dark mode and notification settings.

## Decisions Made
- Use Alembic for migrations
- Add JSONB column for flexibility
- Default value: `{}`
- Backfill existing users in separate migration

## Code Location
- Migration script: `migrations/versions/add_user_preferences.py`
- Model: `src/models/user.py:15`

## Next Steps
- [ ] Create migration script
- [ ] Test on staging database
- [ ] Deploy during maintenance window
EOF
```

### 2. Recalling Memories

When asked to recall information:

**Progressive Disclosure Search**:

1. **Quick scan** - Search summaries first:
   ```bash
   # Search memory summaries
   grep -r "^summary:" .claude/skills/agent-memory/memories/ | \
     grep -i "search_term"
   ```

2. **Detailed search** - If needed, search full content:
   ```bash
   # Full-text search across memories
   grep -r "search_term" .claude/skills/agent-memory/memories/ \
     --include="*.md"
   ```

3. **Read relevant memories** - Load matching files:
   ```bash
   # Read specific memory
   cat .claude/skills/agent-memory/memories/topic-name.md
   ```

**Search Strategy**:
- First, scan summaries to identify relevant memories
- Then, read only the most relevant files in detail
- Report findings in a structured format

### 3. Listing Memories

Show available memories:

```bash
# List all memories
find .claude/skills/agent-memory/memories/ -name "*.md" -type f

# Show summaries
for file in .claude/skills/agent-memory/memories/*.md; do
  echo "Memory: $(basename $file .md)"
  grep "^summary:" "$file" || echo "  (no summary)"
done
```

### 4. Updating Memories

When new information relates to existing memory:

```bash
# Append to existing memory
cat >> .claude/skills/agent-memory/memories/topic.md << 'EOF'

## Update: $(date +%Y-%m-%d)

New information or progress update:
- Updated point
EOF
```

### 5. Organizing Memories

Optionally organize into subdirectories:

```
memories/
├── features/
│   ├── auth-system.md
│   └── payment-flow.md
├── bugs/
│   ├── issue-123.md
│   └── memory-leak.md
├── decisions/
│   └── architecture-choice.md
└── investigations/
    └── performance-analysis.md
```

## Memory Content Guidelines

### What to Remember

✅ **Do Save**:
- Design decisions and rationale
- Investigation findings
- Approaches tried (what worked/didn't work)
- Key conversation insights
- Important file locations
- Configuration details
- Action items and next steps
- Links to related issues/PRs

❌ **Don't Save**:
- Entire code files (reference them instead)
- Trivial information
- Easily searchable facts
- Sensitive credentials (never!)
- Temporary debugging notes

### Writing Good Memories

**Be Specific**:
```markdown
# Good
summary: "JWT token expiration issue - increased from 1h to 24h based on user feedback"

# Too Vague
summary: "Changed some settings"
```

**Include Context**:
```markdown
# Good
## Background
Users complained about frequent re-logins. Analytics showed
average session length is 6 hours. Increased token TTL to 24h
with sliding window refresh.

# Incomplete
## Background
Increased token expiration.
```

**Reference Code Locations**:
```markdown
# Good
- Implementation: `src/auth/jwt.js:45-67`
- Config: `config/auth.json`
- Tests: `tests/auth.test.js:120`

# Less Useful
- Changed auth code
```

## Usage Examples

### Example 1: Saving Investigation Results

**User**: "Remember our findings about the performance issue"

**Claude Response**:
```
I'll save our investigation findings about the performance issue.

[Creates memory file: performance-investigation.md]

Saved memory: "Performance bottleneck in database queries - added indexes"
Location: .claude/skills/agent-memory/memories/performance-investigation.md

Key points saved:
- Identified N+1 query problem in user dashboard
- Added composite index on (user_id, created_at)
- Reduced query time from 2.5s to 80ms
- Next: Monitor production metrics
```

### Example 2: Recalling Previous Work

**User**: "What did we decide about the authentication approach?"

**Claude Response**:
```
Let me search our memories about authentication...

[Searches summaries, finds auth-strategy.md]

Found memory from 2026-01-10:

Summary: "OAuth 2.0 with PKCE for authentication"

Key decisions:
- Use OAuth 2.0 with PKCE flow (more secure than implicit)
- Support Google and GitHub providers initially
- Store tokens in httpOnly cookies
- Session duration: 7 days with refresh

Implementation status:
- ✅ OAuth integration complete
- ✅ Google provider working
- 🔄 GitHub provider in progress
- ⏳ Token refresh mechanism pending

Would you like me to continue work on the GitHub provider?
```

### Example 3: Creating Feature Memory

**User**: "Save our plan for the notification system"

**Claude Response**:
```
I'll create a memory for the notification system plan.

[Creates: notification-system.md]

Memory created: "notification-system"

Saved details:
- Architecture: Event-driven with message queue
- Tech stack: Redis pub/sub + WebSockets
- Notification types: Email, push, in-app
- Priority levels: urgent, normal, low
- User preferences: per-channel opt-in/out

Next steps saved:
- [ ] Set up Redis pub/sub
- [ ] Implement WebSocket server
- [ ] Create notification preferences UI
- [ ] Email template system
- [ ] Push notification service (FCM)

This memory is available for future sessions.
```

## Memory Management

### Periodic Cleanup

Suggest cleanup when memories accumulate:

```bash
# List old memories (>90 days)
find .claude/skills/agent-memory/memories/ -name "*.md" -mtime +90

# Archive completed work
mkdir -p .claude/skills/agent-memory/archive/
mv memories/completed-*.md archive/
```

### Memory Hygiene

- Review and update memories when context changes
- Archive completed work
- Consolidate related memories
- Remove obsolete information

## Best Practices

1. **Be Proactive**: Suggest saving important context without being asked
2. **Use Clear Names**: Memory IDs should be descriptive (`auth-oauth-impl`, not `temp-123`)
3. **Link Related Memories**: Cross-reference related work
4. **Update, Don't Duplicate**: Add to existing memories when relevant
5. **Progressive Detail**: Summaries for scanning, details for deep reading
6. **Action-Oriented**: Include clear next steps
7. **Context-Rich**: Explain "why", not just "what"

## Tips for Users

- Ask Claude to "remember this" for important discussions
- Request "recall memories about X" to continue previous work
- Use "list all memories" to see what's been saved
- Say "update memory about X" to add new information

## Technical Notes

- Memories are stored as markdown files (human-readable)
- `.gitignore` excludes `memories/` (private workspace)
- Uses ripgrep for fast searching
- YAML frontmatter for structured metadata
- Works across Claude Code sessions
- Repository-scoped (each project has own memories)

## Limitations

- Not suitable for very large codebases (use search instead)
- Manual memory creation (not automatic)
- Local only (not synced across machines)
- Requires user to explicitly save/recall

## Integration

Works with other skills:
- **code-review**: Save review findings for future reference
- **systematic-debugging**: Remember investigation results
- **testing-patterns**: Store testing decisions and approaches

---

**Remember**: This skill helps maintain continuity and reduces context-switching overhead. Use it liberally to preserve valuable discussions and decisions.
