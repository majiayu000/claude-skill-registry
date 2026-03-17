---
name: ux-feedback-patterns
description: |
  User feedback patterns for interactions - loading states, success/error messages,
  form validation, empty states. Ensures users understand system state and next steps.

  Use when implementing user-facing state changes and interactions:
  - Form submissions with validation feedback, success/error messages
  - Async operations needing loading indicators (API calls, data fetching)
  - Error handling flows with clear recovery paths and retry options
  - Empty state designs with helpful messaging (no data, no results)
  - User mentions "form", "loading", "error", "validation", "async", "API call"

  Keywords: loading, success, error, form, validation, async, feedback, toast, empty state

  Focus on WHEN to show feedback, WHAT type (toast/inline/modal), HOW LONG (timing).
---

# UX Feedback Patterns

## Purpose
Ensure users never wonder "What's happening?" or "Did that work?" through clear, consistent feedback patterns.

---

## Core Principle

**Users must receive feedback for EVERY interaction.**

Every user action needs feedback in one or more states:
1. Loading/Processing
2. Success
3. Error
4. Empty

---

## Loading States

### When to Show Loading

**Timing thresholds (adjust to your context):**
- **< 100ms**: Perceived as instant, no feedback needed
- **100-300ms**: Optional subtle indicator
- **300ms-1s**: Show spinner or skeleton
- **1-5s**: Spinner + explanatory text
- **5-10s**: Progress bar with percentage
- **10s+**: Progress bar + explanation + cancel option

### Loading Patterns

**Button Loading:**
- Disable button to prevent double-submission
- Show spinner inside button or change text
- Keep button in place (don't shift layout)

**Content Loading:**
- Prefer skeleton screens over spinners
- Match skeleton structure to actual content
- Maintain layout space (prevent content jump)

**Progress Indicators:**
- Use for file uploads, large operations
- Show percentage when determinable
- Provide cancel option for long operations

---

## Success States

### When to Show Success

**Always show for:**
- Form submissions
- Data mutations (create, update, delete)
- File uploads
- Account changes

**Skip for:**
- Very quick actions (near-instant completion)
- Continuous interactions (likes, toggles) - use optimistic updates
- Actions where feedback is inherent in result

### Success Patterns

**Toast Notifications:**
- Auto-dismiss after 3-5 seconds
- Position: top-right or top-center (consistent)
- Specific message, not generic "Success"

**Inline Messages:**
- For form submissions: show below form
- Less intrusive than toasts
- Can stay visible longer

**Visual Confirmation:**
- Button state change (e.g., "Save" → "Saved ✓")
- Brief color change (green tint)
- Return to normal after 2-3 seconds

---

## Error States

### Error Message Principles

**Be Specific:**
- ❌ "Error occurred"
- ✅ "Email already exists. Try logging in instead."

**Be Helpful:**
- Explain what happened
- Suggest what to do next
- Provide recovery action when possible

**Be Human:**
- Natural language, avoid technical jargon
- Don't blame user
- Empathetic tone for serious errors

**Severity Levels:**
- **Critical**: System failure, data loss - modal, manual dismiss
- **High**: Form validation, API errors - prominent, actionable
- **Medium**: Warnings, non-blocking - dismissible notices
- **Low**: Helper text, suggestions - subtle, informative

### Error Patterns

**Form Field Errors:**
- Show inline, next to/below field
- Trigger on blur (not every keystroke)
- Include error icon for visibility
- Keep visible until corrected

**Global Errors:**
- Prominent alert at top or modal
- Include error icon and title
- Explain what failed and why
- Provide action: Retry, Contact support, Learn more
- Manual dismiss (don't auto-hide critical errors)

**Error Recovery:**
- Always provide a path forward
- "Try Again" button for transient errors
- Link to help/support for persistent issues
- Save user's work when possible

---

## Empty States

### Never Show Blank Screens

**Empty state must include:**
1. **Icon/Illustration**: Visual context
2. **Title**: "No [items] yet"
3. **Description**: Brief explanation
4. **Action** (when possible): CTA to create first item

### Empty State Types

**First-Time Empty:**
- Welcoming, encouraging tone
- Clear next step to get started

**Search No Results:**
- Acknowledge the query
- Suggest alternatives (check spelling, try different terms)
- Provide way to clear/modify search

**Filtered Empty:**
- Explain filters are active
- Show way to clear filters

---

## Interaction Patterns

### Form Validation

**Validation Timing:**
- On blur: Validate individual field
- On submit: Validate entire form
- On change: Only for real-time feedback (password strength, username availability)

**Success Indicators:**
- Optional: show checkmark for valid fields
- Only after field touched
- Subtle, not distracting

### Button States

**Required states:**
- Default: Normal appearance
- Hover: Visual feedback
- Active/Pressed: Depressed appearance
- Loading: Spinner + disabled
- Disabled: Grayed out + tooltip/explanation
- Success: Brief confirmation (2-3s)

### Optimistic Updates

**Pattern:** Update UI immediately, rollback on error

**Best for:**
- Fast, reliable operations (likes, favorites)
- Low-stakes actions
- When instant feedback improves perceived performance

**How it works:**
1. Update UI immediately (assume success)
2. Send API request
3. If success: nothing (already updated)
4. If error: rollback + show error

**When NOT to use:**
- Destructive actions (delete)
- Complex validations
- Critical operations (payments)

### Destructive Actions

**Always confirm before:**
- Deleting items
- Permanent changes
- Bulk actions

**Confirmation pattern:**
- Modal dialog with clear title
- Explain consequences: "This cannot be undone"
- Primary action labeled clearly ("Delete", not "Yes")
- Use danger color (red) for destructive button
- Provide "Cancel" as escape hatch

---

## Best Practices

### Timing
- Feedback should feel immediate (instant perceived response)
- Success messages: auto-dismiss after 3-5 seconds
- Error messages: manual dismiss or longer timeout
- Loading threshold: Show indicators after ~300ms

### Tone
- Be specific, not vague
- Be helpful, suggest next steps
- Be human, avoid technical jargon
- Don't blame user

### Accessibility
- Use ARIA live regions for dynamic messages
- Associate errors with form fields
- Provide text alternatives for visual indicators
- Don't rely on color alone

### Consistency
- Same pattern for same action across app
- Predictable feedback locations
- Consistent timing and animations
- Unified messaging tone

---

## Common Mistakes

1. **Silent failures** - Action fails with no feedback
2. **Vague errors** - "Error" tells nothing useful
3. **No loading state** - User clicks repeatedly
4. **Blank screens** - Empty state without explanation
5. **Disabled without reason** - No tooltip explaining why
6. **Flickering loaders** - Show only for operations with noticeable delay
7. **Success overload** - Toast for every tiny action
8. **Technical error codes** - Show user-friendly messages
9. **No recovery path** - Error with no next step
10. **Blocking entire UI** - Use local loading when possible

---

## Validation Checklist

For every interactive feature:
- [ ] Loading state for async operations with noticeable delay
- [ ] Success feedback (toast, inline, or visual confirmation)
- [ ] Error messages specific and actionable
- [ ] Empty states have helpful messaging + action
- [ ] Optimistic updates rollback on failure
- [ ] Destructive actions require confirmation
- [ ] All feedback is accessible (ARIA, alt text)
- [ ] States are visually distinct and clear
- [ ] No silent failures
- [ ] Consistent patterns across application

---

## Key Takeaway

**Never leave users guessing.** Clear, timely feedback is the difference between a frustrating experience and a delightful one.

Timing guidelines are based on UX research but should be adjusted to your context. When in doubt, over-communicate rather than under-communicate.
