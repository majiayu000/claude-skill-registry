---
name: asking-questions
description: Guidance for asking clarifying questions when user requests are ambiguous, have multiple valid approaches, or require critical decisions. Use when implementation choices exist that could significantly affect outcomes.
metadata:
  version: 1.0.7
---

# Asking Questions

## Purpose

Ask clarifying questions when the answer materially changes what you'll build. This skill helps identify when to ask, how to structure questions effectively, and when to proceed autonomously.

## When to Use

Ask questions for:

1. **Ambiguous implementation choices** - Multiple valid technical approaches (middleware vs wrapper functions, library selection, architectural patterns)
2. **Missing critical context** - Specific information needed (database type, deployment platform, credential management)
3. **Potentially destructive actions** - Requests that could be interpreted dangerously ("clean up files" = delete vs archive)
4. **Scope clarification** - Vague terms like "refactor," "optimize," or "improve"
5. **Conflicting requirements** - Goals that may work against each other ("make it faster" + "add extensive logging")
6. **Technical trade-offs** - Solutions with different costs/benefits depending on priorities

## When NOT to Use

Don't ask when:
- **Request is clear and unambiguous** - One obvious implementation path
- **You can determine the answer from context** - Codebase patterns, project structure, existing conventions
- **Over-clarification** - Questions that don't materially affect implementation
- **Standard engineering practices** - Established patterns already in the codebase

## Question Structure

### Template

```
[Context: What you found/analyzed]

[Present 2-5 specific options with brief trade-offs]

[Direct question asking for preference]

[Optional: Offer to make reasonable default choice]
```

### Guidelines

1. **Acknowledge understanding first** - Show you've analyzed the situation
   - "I found your API endpoints and see you're using Express..."

2. **Present clear options** - Offer 2-5 specific choices with brief context
   ```
   I can implement this in several ways:
   1. **Global middleware** - Catches all errors centrally (simplest)
   2. **Wrapper functions** - More granular control per endpoint
   3. **Custom error classes** - Typed errors with status codes
   ```

3. **Ask directly** - Clear question that guides decision
   - "Which approach fits your needs?"

4. **Offer autonomy (optional)** - For less critical decisions
   - "I can implement option 2 as it's the safest, or let me know if you prefer something else."

## Progressive Disclosure

Layer questions instead of asking everything upfront:

**Good ✓**
- First: "For real-time updates, should I use WebSockets, Server-Sent Events, or polling?"
- Then: "For WebSockets, do you want Socket.io (easier) or native (lighter)?"

**Bad ✗**
- "For real-time updates should I use WebSockets or SSE or polling and if WebSockets should I use Socket.io or native and should I implement reconnection and what about authentication and..."

## Examples

### Good ✓

"I see you're using JWT authentication. To add refresh tokens, I can:
1. **httpOnly cookies** - More secure, harder to XSS
2. **localStorage** - Simpler, works with mobile apps  
3. **In-memory only** - Most secure, lost on refresh

What works best for your use case?"

### Bad ✗

"How should I implement the authentication refresh token storage mechanism considering security implications, XSS vulnerabilities, mobile compatibility, UX impacts, and compliance considerations?"

*Too verbose, no clear options, asks everything at once*

---

### Good ✓

"You mentioned 'clean up migrations.' Do you want me to archive them to /old-migrations or delete them entirely? (Note: deletion can break databases that haven't run them yet)"

### Bad ✗

"What do you mean by clean up?"

*Too vague, doesn't guide the decision*

## After Receiving an Answer

1. **Acknowledge** - Confirm you understood their choice
2. **Proceed immediately** - Don't ask if they want you to continue
3. **Apply preferences** - If they chose "security first" once, lean that direction for similar future choices

## Key Principle

**Ask only when the answer materially changes what you'll build.** Avoid building the wrong thing, not asking questions for the sake of asking.
