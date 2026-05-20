---
name: error-handling-confirmation
description: |
  This skill normalizes errors and produces human-friendly confirmations across API and UI layers. It prevents silent failures, ensures graceful degradation, and maintains consistent UX quality. Use when implementing error responses, success confirmations, "not found" handling, or improving agent response quality.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Error Handling & Confirmation

## What This Skill Does

- Normalizes error responses into consistent, human-friendly formats
- Produces clear success confirmations that build user trust
- Handles "not found" and edge cases gracefully
- Prevents silent failures through explicit error surfacing
- Ensures agent/API responses maintain UX quality

## When to Use

- Implementing API error responses
- Creating user-facing error messages
- Adding success/confirmation feedback
- Handling "task not found" or similar scenarios
- Building fallback responses for AI agents
- Improving response quality and polish

## When NOT to Use

- Logging/monitoring (use observability patterns)
- Exception handling architecture (use language-specific patterns)
- Input validation logic (handle separately, use these patterns for messages)

---

## Core Principles

### 1. Never Blame the User

```
❌ "You entered an invalid email"
✅ "Please enter a valid email address"

❌ "You don't have permission"
✅ "This action requires additional permissions"
```

### 2. Be Specific and Actionable

```
❌ "An error occurred"
✅ "Unable to save task. Please check your connection and try again."

❌ "Invalid input"
✅ "Title must be less than 200 characters (currently 215)"
```

### 3. Use Plain Language

```
❌ "Error 0x80004005: Unspecified error"
✅ "Something went wrong. Please try again."

❌ "ECONNREFUSED 127.0.0.1:5432"
✅ "Unable to connect to the database. Please try again later."
```

### 4. Preserve User Trust

```
❌ Silent failure (no feedback)
✅ "We couldn't complete that action. Your data is safe."

❌ Technical stack trace
✅ "Something unexpected happened. Our team has been notified."
```

---

## Error Response Patterns

### API Error Structure

```python
# Standardized error response
{
    "error": {
        "code": "TASK_NOT_FOUND",      # Machine-readable
        "message": "Task not found",    # Human-readable
        "details": {}                   # Optional context
    }
}
```

### HTTP Status Code Mapping

| Scenario | Status | Code | Message |
|----------|--------|------|---------|
| Resource not found | 404 | `NOT_FOUND` | "{Resource} not found" |
| Access denied | 403 | `FORBIDDEN` | "You don't have access to this {resource}" |
| Auth required | 401 | `UNAUTHORIZED` | "Please sign in to continue" |
| Validation failed | 400 | `VALIDATION_ERROR` | Specific field message |
| Server error | 500 | `INTERNAL_ERROR` | "Something went wrong. Please try again." |
| Service unavailable | 503 | `SERVICE_UNAVAILABLE` | "Service temporarily unavailable" |

### Not Found Handling (Critical Pattern)

Distinguish between "doesn't exist" and "not yours":

```python
def get_task(task_id: int, user_id: str):
    task = db.get_task(task_id)

    if task is None:
        # Task doesn't exist at all
        raise NotFoundError("Task not found")

    if task.user_id != user_id:
        # Task exists but belongs to someone else
        raise ForbiddenError("You don't have access to this task")

    return task
```

**Why this matters**: Returning 404 for "not yours" leaks information about resource existence.

---

## Confirmation Patterns

### Success Messages

| Action | Confirmation |
|--------|--------------|
| Create | "Task created successfully" |
| Update | "Changes saved" |
| Delete | "Task deleted" |
| Complete | "Nice work! Task completed" |
| Bulk action | "3 tasks updated" |

### Confirmation Components

```typescript
// Toast notification pattern
addToast("Task created successfully", "success");
addToast("Unable to save changes", "error");
addToast("Are you sure?", "warning");
```

### Visual Feedback Hierarchy

1. **Immediate** - Button state change (loading → success)
2. **Transient** - Toast notification (auto-dismisses)
3. **Persistent** - Inline message (stays until resolved)
4. **Blocking** - Modal dialog (requires action)

---

## Graceful Degradation

### Fallback Strategy

```
Primary action fails
    ↓
Try recovery (retry, alternative)
    ↓
If still fails → Show friendly error
    ↓
Preserve user's work/state
    ↓
Offer clear next steps
```

### Never Lose User Data

```typescript
// Bad: Silent failure
async function saveTask(task) {
    await api.save(task);  // If fails, data lost
}

// Good: Preserve on failure
async function saveTask(task) {
    try {
        await api.save(task);
        showSuccess("Task saved");
    } catch (error) {
        // Keep form data intact
        showError("Couldn't save. Your changes are preserved.");
        // Optionally save to localStorage as backup
    }
}
```

### Agent/Chatbot Fallbacks

```
User input not understood
    ↓
"I didn't quite catch that. Could you rephrase?"
    ↓
Still unclear after 2 attempts
    ↓
"I'm having trouble understanding. Here's what I can help with: [options]"
    ↓
Offer human escalation if available
```

---

## Message Templates

### Error Messages

```typescript
const ERROR_MESSAGES = {
    // Network
    NETWORK_ERROR: "Unable to connect. Please check your internet connection.",
    TIMEOUT: "Request timed out. Please try again.",

    // Auth
    SESSION_EXPIRED: "Your session has expired. Please sign in again.",
    UNAUTHORIZED: "Please sign in to continue.",
    FORBIDDEN: "You don't have permission to do this.",

    // Resources
    NOT_FOUND: "{resource} not found.",
    ALREADY_EXISTS: "A {resource} with this name already exists.",

    // Validation
    REQUIRED_FIELD: "{field} is required.",
    TOO_LONG: "{field} must be less than {max} characters.",
    INVALID_FORMAT: "Please enter a valid {field}.",

    // Server
    SERVER_ERROR: "Something went wrong. Please try again.",
    SERVICE_UNAVAILABLE: "Service temporarily unavailable. Please try again later.",

    // Generic fallback
    UNKNOWN: "An unexpected error occurred. Please try again."
};
```

### Success Messages

```typescript
const SUCCESS_MESSAGES = {
    // CRUD
    CREATED: "{resource} created successfully.",
    UPDATED: "Changes saved.",
    DELETED: "{resource} deleted.",

    // Actions
    COMPLETED: "Nice work! {resource} completed.",
    SAVED: "Saved.",
    SENT: "Sent successfully.",

    // Bulk
    BULK_UPDATE: "{count} items updated.",
    BULK_DELETE: "{count} items deleted."
};
```

---

## Implementation Checklist

### API Layer
- [ ] Consistent error response structure
- [ ] Appropriate HTTP status codes
- [ ] Human-readable messages (no technical jargon)
- [ ] Distinguish 403 vs 404 properly
- [ ] No sensitive data in error responses

### UI Layer
- [ ] Toast system for transient feedback
- [ ] Inline validation messages
- [ ] Loading states during operations
- [ ] Error boundaries for crashes
- [ ] Empty states for no-data scenarios

### User Experience
- [ ] No silent failures
- [ ] Clear next steps in error messages
- [ ] User data preserved on failure
- [ ] Consistent tone (friendly, not blaming)
- [ ] Appropriate visual feedback (icons, colors)

---

## Anti-Patterns

### Don't Do This

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Silent failure | User confused | Always show feedback |
| Technical jargon | User can't understand | Plain language |
| Generic "Error" | Not actionable | Be specific |
| Blame language | Damages trust | Use neutral tone |
| Stack traces | Security risk, confusing | Log server-side only |
| -1 or null returns | Easy to miss | Throw explicit errors |
| Alert boxes | Disruptive UX | Use toasts/inline |

### Security Considerations

```python
# Bad: Leaks information
"User admin@example.com not found"  # Confirms email doesn't exist

# Good: Generic auth messages
"Invalid email or password"  # Same message for both cases
```

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing error handling, toast system, message patterns |
| **Conversation** | User's specific requirements, tone preferences |
| **Skill References** | Domain patterns from `references/` |
| **User Guidelines** | Team's preferred messaging style |

---

## Integration with Other Skills

- **api-client-design**: Error response structure integration
- **frontend-architecture**: Toast and notification patterns
- **fastapi-architecture**: HTTPException handling
- **auth-aware-ui**: Auth error flow handling

---

## References

See `references/` for:
- `error-catalog.md` - Complete error code catalog
- `message-templates.md` - Copy-paste message templates
- `ux-patterns.md` - Visual feedback patterns
