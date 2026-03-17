---
name: ccc
description: Create context issue and compact conversation. Use when user types 'ccc' or when needing to save current session state, preserve context for future tasks, or before switching to a new major task.
model: haiku
---

# CCC - Create Context & Compact

## Purpose
Save the current session state and context to forward to another task. This preserves work progress and enables seamless task switching.

## When to Use
- User explicitly types `ccc`
- Before starting a major new task
- When conversation context is getting large
- Need to preserve current state for future reference

## Steps

### 1. Use CCC Script (No LLM needed - pure template filling)

This skill now uses `scripts/ccc_context.py` which automatically gathers git info and creates the context issue without requiring LLM processing. This saves 100% of LLM costs for this skill.

### 2. Execute Script

**Basic usage (auto-detect focus):**
```bash
python3 scripts/ccc_context.py
```

**With custom focus description:**
```bash
python3 scripts/ccc_context.py "Working on skill optimization"
```

The script will:
1. Gather git information automatically
   - Current branch
   - Changed files (git status)
   - Recent commits (git log -5)
2. Fill the context issue template
3. Create GitHub issue with "context" label
4. Return issue number and URL

### 3. Compact Conversation

After the script completes, tell the user:
```
Context issue created: #[issue-number]
Ready to compact conversation with: /compact
```

## Important Notes
- **Time Zone**: Always use GMT+7 (Bangkok) as primary time zone
- **Label**: Always add "context" label to the issue
- **Title Format**: "Context: [description] - YYYY-MM-DD HH:MM GMT+7"
- **Issue Number**: Save the issue number for reference
- **No Coding**: This is documentation only, no implementation

## Success Criteria
- ✅ Context issue created with all required sections
- ✅ Issue has "context" label
- ✅ User prompted to run /compact
- ✅ Issue number provided to user
