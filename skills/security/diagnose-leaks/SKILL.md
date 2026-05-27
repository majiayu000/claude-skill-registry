---
name: diagnose-leaks
description: Diagnose thinking trace leaks in Samara message output. Use when internal content appears in messages, session IDs leak to users, or thinking blocks become visible. Trigger words: leak, thinking trace, session ID, internal, sanitization, filtered.
context: fork
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Diagnose Thinking Trace Leaks

Debug and verify the three-layer defense against internal content leaking into user-visible messages.

## Background

Complex group chat scenarios with multiple concurrent requests (webcam + web fetch + conversation) can cause internal thinking traces and session IDs to leak. This skill helps diagnose such issues.

## Quick Diagnostics

### 1. Check for Recent Filtered Content
```bash
# Look for sanitization activity in logs (DEBUG level)
grep -i "Filtered from response" ~/.claude-mind/logs/samara.log | tail -20

# Check if sanitization is actively filtering
grep -E "(THINKING|SESSION_ID|ANTML)" ~/.claude-mind/logs/samara.log | tail -10
```

### 2. Verify MessageBus Routing
```bash
# All sends should go through MessageBus - look for source tags
grep -E "\[(iMessage|Location|Wake|Alert|Queue|Webcam|WebFetch)\]" ~/.claude-mind/logs/samara.log | tail -20

# Check for any direct sender bypasses (should NOT appear after fix)
grep "sender\.send" ~/Developer/samara-main/Samara/Samara/*.swift | grep -v MessageBus
```

### 3. Check Recent Episode Logs for Leaked Content
```bash
# Look for session ID patterns in episode logs (SHOULD NOT be there)
grep -E "\d{10}-\d{5}" ~/.claude-mind/memory/episodes/$(date +%Y-%m-%d).md

# Look for thinking block markers that escaped
grep -i "<thinking>" ~/.claude-mind/memory/episodes/$(date +%Y-%m-%d).md
```

### 4. Run Sanitization Tests
```bash
cd ~/Developer/samara-main/Samara
xcodebuild test -scheme SamaraTests -destination 'platform=macOS' 2>&1 | grep -E "SanitizationTests"
```

## Leak Patterns to Watch For

| Pattern | Meaning | Fix |
|---------|---------|-----|
| `1234567890-12345` | Session ID leaked | Check sanitizeResponse() |
| `<thinking>...</thinking>` | Thinking block escaped | Check regex pattern |
| `<invoke>...</invoke>` | XML marker leaked | Check antmlPattern |
| Scrambled multi-response | Streams crossed | Check TaskRouter isolation |

## Architecture Verification

### Layer 1: Output Sanitization
- File: `Samara/Samara/Actions/ClaudeInvoker.swift`
- Method: `sanitizeResponse()`
- Filters: `<thinking>` blocks, session IDs, XML markers

### Layer 2: MessageBus Coordination
- File: `Samara/Samara/Actions/MessageBus.swift`
- All sends should use `messageBus.send()` with type tag
- Verify: No direct `sender.send()` calls in main.swift

### Layer 3: TaskRouter Isolation
- File: `Samara/Samara/Mind/TaskRouter.swift`
- Classifies: conversation, webcam, webFetch, skill tasks
- Isolates parallel tasks to prevent cross-contamination

## If Leaks Are Found

1. **Identify the leak source** from logs
2. **Check if it's a new pattern** not covered by sanitization
3. **Add test case** to `SanitizationTests.swift`
4. **Update sanitizeResponse()** with new filter
5. **Rebuild Samara**: `~/.claude-mind/bin/update-samara`

## Report Template

When reporting a leak issue:
1. What content leaked (exact text)
2. Context (group chat? concurrent tasks?)
3. Timestamp (to correlate with logs)
4. Log entries showing sanitization activity
5. Whether tests pass
