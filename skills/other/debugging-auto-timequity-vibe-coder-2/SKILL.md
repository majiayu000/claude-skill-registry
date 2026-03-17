---
name: debugging-auto
description: Hidden automatic debugging when something breaks - user sees simple question or "fixing..." not stack traces or technical errors
---

# Automatic Debugging

## Overview

Part of the hidden validation layer. When code breaks during generation, fix it automatically without exposing technical details to user.

**Core principle:** User describes WHAT. We handle HOW - including when things break.

## When This Runs (Automatically)

- Test failures during `/mvp:build`
- Build errors after `/mvp:add`
- Runtime errors in preview
- Any unexpected behavior

## The Process

### 1. Capture Error (Hidden)

```
// User doesn't see this
Error: Cannot read property 'map' of undefined
  at UserList.tsx:15
  at renderWithHooks...
```

### 2. Analyze Root Cause (Hidden)

Apply systematic-debugging principles:
- What line failed?
- What value is undefined?
- Where should it come from?
- Why is it missing?

### 3. Fix Automatically (Hidden)

```typescript
// Before (broken)
const users = props.users;
return users.map(u => <User key={u.id} {...u} />);

// After (fixed)
const users = props.users ?? [];
return users.map(u => <User key={u.id} {...u} />);
```

### 4. Verify Fix (Hidden)

- Run tests
- Check build
- Smoke test feature

### 5. Continue (User Sees Progress)

**If fixed:** Continue silently, user never knows

**If can't fix:** Ask simple question

## User-Facing Questions

**Technical error → Simple question:**

| Error | User Question |
|-------|---------------|
| `undefined is not iterable` | "Should the list show empty when there's no data, or a message?" |
| `401 Unauthorized` | "Does this feature need login to work?" |
| `ENOENT: no such file` | "Where should we save the uploaded files?" |
| `Foreign key constraint` | "Can a user have multiple projects, or just one?" |

## What User NEVER Sees

- Stack traces
- Error codes
- Technical jargon
- "npm install failed"
- "TypeScript error TS2345"
- File paths
- Line numbers

## What User MAY See

- "Fixing a small issue..."
- "Making some adjustments..."
- Simple question about their preferences
- "✅ Done!"

## Escalation

**After 3 auto-fix attempts fail:**

1. Don't show technical error
2. Ask clarifying question about the feature
3. If still fails, simplify the feature
4. "I'll add a basic version first, we can enhance it later"

## Integration

**Called by:**
- **verification-gate** - When any check fails
- All `/mvp:*` commands on error

**Uses internally:**
- systematic-debugging principles (hidden)
- root-cause-tracing (hidden)

## Philosophy

The magic of vibe coding is that users don't need to be developers.

Every error message we show breaks that illusion.

Fix it silently. Ask simple questions. Never blame the user.
