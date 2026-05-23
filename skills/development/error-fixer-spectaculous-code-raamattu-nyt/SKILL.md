---
name: error-fixer
description: |
  Fix JavaScript and HTTP errors flagged for AI in the admin dashboard. Queries the database for
  errors with ai_status='flagged_for_ai', analyzes them, and attempts to fix them.

  Use when:
  - User says "fix errors" or "fix flagged errors"
  - User says "check error queue"
  - User mentions AI error queue or AI-flagged errors
  - After flagging errors in admin dashboard

  Triggers: "fix errors", "error queue", "ai errors", "flagged errors", "fix ai errors", "/fix-errors"
---

# Error Fixer

Fetch and fix errors flagged for AI correction in the admin dashboard. Supports both JS errors (`error_reports`) and HTTP errors (`http_error_logs`).

## Workflow

```
1. FETCH    → Get AI-flagged errors from both tables
2. ANALYZE  → Understand each error (stack trace, context, URL, status)
3. FIX      → Apply fixes using systematic debugging
4. MARK     → Mark errors as ai_fixed with notes
5. REPORT   → Summarize what was fixed
```

## Step 1: Fetch Flagged Errors

Query both error tables using Supabase MCP:

**JS Errors:**
```sql
SELECT id, error_type, error_message, stack_trace, context, user_action, ai_prompt, created_at
FROM error_reports WHERE ai_status = 'flagged_for_ai'
```

**HTTP Errors:**
```sql
SELECT id, method, url, status_code, response_body, request_context, navigation_path, ai_prompt, created_at
FROM http_error_logs WHERE ai_status = 'flagged_for_ai'
```

Or use RPC functions: `get_errors_for_ai()` and `get_http_errors_for_ai()`.

**Important:** The `ai_prompt` field contains specific instructions from the admin.

## Step 2: Analyze Each Error

### JS Errors
1. **Read the ai_prompt** - Admin's instruction
2. **Parse stack trace** - File path, line number, call chain
3. **Check context** - `route`, `action`, other data
4. **Read affected file(s)**

### HTTP Errors
1. **Read the ai_prompt** - Admin's instruction
2. **Check URL and status code** - What endpoint failed and why
3. **Review response_body** - Error message from server
4. **Check navigation_path** - User's journey to this error
5. **Find the code** - Locate fetch/API call that made this request

## Step 3: Fix Using Systematic Debugging

**DO NOT GUESS.** Follow systematic-debugging:

1. **Understand root cause** - Don't patch symptoms
2. **Find the actual source** - Trace back through stack/code
3. **Make minimal fix** - One change at a time
4. **Verify locally** - Run build/tests after fix

### Common JS Error Patterns

| Error Type | Common Fix |
|------------|------------|
| `TypeError: Cannot read property 'x' of undefined` | Add null checks, optional chaining |
| `TypeError: x is not a function` | Check imports, verify function exists |
| `ChunkLoadError` | Code splitting issue, check lazy imports |
| `NetworkError` | Add error handling, retry logic |

### Common HTTP Error Patterns

| Status | Common Fix |
|--------|------------|
| 400 Bad Request | Validate request params, check payload format |
| 401/403 Unauthorized | Check auth token, verify RLS policies |
| 404 Not Found | Verify endpoint exists, check URL construction |
| 500 Server Error | Check Edge Function logs, fix server-side code |
| CORS errors | Update Edge Function CORS headers |

## Step 4: Mark as Fixed

**JS Errors:** Call `mark_error_ai_fixed(p_id, p_fix_notes)`

**HTTP Errors:** Call `mark_http_error_ai_fixed(p_id, p_fix_notes)`

**Good fix notes examples:**
- "Added null check for user object in ProfileCard.tsx:45"
- "Fixed RLS policy for authenticated users on topics table"
- "Added missing CORS header to edge function"

## Step 5: Report Summary

```
## Error Fix Summary

### JS Errors
#### Fixed (X)
- [error_type] in file.tsx:line - Brief description

#### Could Not Fix (X)
- [error_type] - Reason

### HTTP Errors
#### Fixed (X)
- [status_code] [method] /path - Brief description

#### Could Not Fix (X)
- [status_code] [method] /path - Reason
```

## Database Schema Reference

```sql
-- error_reports (JS errors)
ai_status: 'pending' | 'flagged_for_ai' | 'ai_fixed' | 'verified'
ai_prompt: text
ai_fixed_at: timestamp
ai_fix_notes: text

-- http_error_logs (HTTP errors)
ai_status: 'pending' | 'flagged_for_ai' | 'ai_fixed' | 'verified'
ai_prompt: text
ai_fixed_at: timestamp
ai_fix_notes: text

-- RPC functions
get_errors_for_ai()              -- JS errors flagged for AI
get_http_errors_for_ai()         -- HTTP errors flagged for AI
mark_error_ai_fixed(p_id, p_fix_notes)       -- Mark JS error fixed
mark_http_error_ai_fixed(p_id, p_fix_notes)  -- Mark HTTP error fixed
```

## Best Practices

1. **Always read ai_prompt first** - Admin may have specific instructions
2. **Don't fix what you don't understand** - Mark as "could not fix"
3. **Run build after fixes** - Verify no new errors
4. **Write clear fix notes** - Help admin understand what changed
5. **Group related errors** - Multiple errors may have same root cause
6. **Check Edge Function logs** - For HTTP 500 errors, use Supabase MCP `get_logs`
