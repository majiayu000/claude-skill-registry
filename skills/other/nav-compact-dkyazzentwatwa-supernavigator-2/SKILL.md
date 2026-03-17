---
name: nav-compact
description: Clear conversation context while preserving knowledge via context marker. Use when user says "clear context", "start fresh", "done with this task", or when approaching token limits.
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Navigator Compact Skill

Clear your conversation context while preserving all knowledge in a context marker. Like git commit before switching branches - save your state, then start fresh.

## When to Invoke

Invoke this skill when the user:
- Says "clear context", "start fresh", "reset conversation"
- Says "I'm done with this task", "moving to next feature"
- Mentions "approaching token limit", "context getting full"
- Says "compact", "clean up context"
- After completing isolated sub-task

**DO NOT invoke** if:
- User is in middle of implementation
- Context is needed for next immediate step
- Less than 20 messages in conversation (not much to gain)

## Execution Steps

### Step 1: Check If Worth Compacting

Estimate conversation size:
- If < 20 messages: Suggest waiting
- If 20-50 messages: Safe to compact
- If > 50 messages: Highly recommended

Show message:
```
📊 Current session: ~[N] messages

Compacting will:
- Create marker with current state
- Clear conversation history
- Free up ~[X]k tokens for new work

Continue? [Y/n]:
```

### Step 2: Create Automatic Marker

Invoke `nav-marker` skill (or create marker directly) with auto-generated name:

```
Marker name: before-compact-{YYYY-MM-DD}-{HHmm}
Note: "Auto-created before compact"
```

This marker should capture:
- Last 10-15 messages summary
- Files modified
- Technical decisions
- Current progress
- Next steps

### Step 3: Set Active Marker

Write the marker filename to `.active` file:

```bash
echo "{marker-filename}.md" > .agent/.context-markers/.active
```

This tells `nav-start` to offer restoration on next session.

### Step 4: Display Compact Instructions

Show user how to compact:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  🗜️  Navigator Compact                                ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

✅ Context marker created:
   .agent/.context-markers/{marker-filename}.md

📋 Marker contains:
   - Conversation summary (last 15 messages)
   - Files you modified
   - Technical decisions made
   - Current progress & next steps

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 TO COMPACT:

Claude Code doesn't allow me to clear the conversation
programmatically. You need to do it manually:

**Method 1: New conversation**
1. Start a new conversation
2. Say "load my context" or "start my session"
3. I'll detect the active marker and restore your state

**Method 2: /clear command** (if available)
1. Type /clear
2. Say "load my context"
3. Active marker will be restored

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Your progress is saved. You won't lose any context.

Next session:
1. Say "start my session" or run /nav:start
2. I'll detect the marker: "{marker-filename}"
3. Confirm to restore, and you'll be back where you left off

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5: Confirm Marker Location

Verify marker was created:

```bash
ls -lh .agent/.context-markers/{marker-filename}.md
```

Show file size and confirm success:
```
✅ Marker saved successfully
   File: {marker-filename}.md
   Size: {X} KB (~{Y} tokens)

Your context is preserved!
```

## Important Notes

**Why manual compact?**

Claude Code conversations cannot be programmatically cleared from within a conversation. The user must:
- Start a new conversation, OR
- Use `/clear` command (if available)

This skill creates the marker and sets up auto-restoration, but the actual clearing must be done by the user.

**Auto-restoration workflow:**

```
Session 1:
  User: "Clear context"
  → nav-compact creates marker
  → Sets .active file
  → Instructs user how to clear

Session 2 (new conversation):
  User: "Start my session"
  → nav-start detects .active file
  → Offers to restore marker
  → User confirms
  → Context restored!
```

## Common Use Cases

### After Completing Feature
```
User: "Feature complete, clear context for next task"
→ Creates marker: "before-compact-2025-10-16-1430"
→ Captures: Feature implementation details
→ User starts new conversation
→ Restores marker, begins next feature
```

### Approaching Token Limit
```
User: "Context getting full, let's compact"
→ Creates marker: "before-compact-2025-10-16-1500"
→ Preserves: All current work
→ User clears conversation
→ Continues with fresh context
```

### Switching Between Tasks
```
User: "Done with auth, moving to payments"
→ Creates marker: "auth-feature-complete"
→ Clear context
→ New session: Fresh start for payments
→ Can restore auth marker later if needed
```

## Error Handling

**Marker creation fails**:
```
❌ Failed to create marker

Cannot compact without preserving context.
Fix marker creation first.
```

**Not enough context to preserve**:
```
⚠️  Very little context (< 10 messages)

Compacting now won't save much. Consider:
- Continue working
- Compact after more progress

Continue anyway? [y/N]:
```

**Active marker already exists**:
```
⚠️  Active marker already exists:
   .agent/.context-markers/.active

This means you have an unrestored marker from previous compact.

Options:
1. Load that marker first (recommended)
2. Overwrite with new marker
3. Cancel compact

Your choice [1-3]:
```

## Success Criteria

Compact is successful when:
- [ ] Context marker created successfully
- [ ] Marker contains comprehensive summary
- [ ] `.active` file created (for auto-restoration)
- [ ] User knows how to clear conversation
- [ ] User knows marker will auto-restore on next session

## Scripts

**compact.py**: Automated compact workflow
- Create marker
- Set active file
- Generate restore instructions

## Best Practices

**When to compact:**
- ✅ After completing isolated feature/sub-task
- ✅ After major documentation update
- ✅ Before switching to unrelated work
- ✅ When approaching 70%+ token usage
- ❌ In middle of implementation
- ❌ When context needed for next step
- ❌ After every few messages (wasteful)

**Compact frequency:**
- Small task (30 min): No compact needed
- Medium task (2-3 hours): Compact after completion
- Large task (full day): Compact at logical breakpoints
- Multi-day task: Compact at end of each session

## Notes

This skill automates the preparation for compacting but cannot clear the conversation itself (Claude Code limitation).

The value is in:
1. Automatic marker creation
2. Setting up auto-restoration
3. Guiding user through process
4. Preserving context seamlessly

This provides same functionality as `/nav:compact` command but with natural language invocation.
